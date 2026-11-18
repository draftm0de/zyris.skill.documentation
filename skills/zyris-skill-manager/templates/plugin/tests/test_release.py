"""Release contract tests using fictional isolated repositories."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'plugin.json').exists())
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'scripts'))
# Load the repository's exact scripts, independent of unittest's discovery path.
# Extracted-package execution is a separate regression gate for these dynamic imports.
def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
release = load_script('release')
publish = load_script('publish')

class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'source'; self.root.mkdir()
        self.out = Path(self.tmp.name) / 'bundle'
        (self.root / 'skills/fictional').mkdir(parents=True)
        (self.root / 'skills/fictional/SKILL.md').write_text('---\nname: fictional\ndescription: Fictional fixture\n---\nSay hello.\n')
        self.manifest = {'name':'fictional', 'version':'1.0.0', 'description':'Fictional fixture', 'repository':'https://github.com/example/fictional'}
        (self.root / 'plugin.json').write_text(json.dumps(self.manifest))
        (self.root / 'CHANGELOG.md').write_text('# Changelog\n\n## [1.0.0]\n\nFictional changes.\n')
        self.run_git('init', '-q'); self.run_git('add', '.')
        self.run_git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture')
        self.run_git('tag','v1.0.0')
        self.patcher=patch.object(release.plugin,'ROOT', self.root); self.patcher.start(); self.addCleanup(self.patcher.stop)
    def run_git(self,*args):
        return subprocess.check_output(['git','-C',str(self.root),*args],stderr=subprocess.STDOUT)
    def prepare(self): return release.prepare('v1.0.0',self.out)
    def test_reproducible_and_idempotent(self):
        self.prepare(); first=release.snapshot(self.out)
        self.prepare(); other=self.out.with_name('other'); release.prepare('v1.0.0',other)
        self.assertEqual(first,release.snapshot(other)); self.assertEqual(first,release.snapshot(self.out))
    def test_version_and_dirty_conflicts(self):
        for tag in ('1.0.0','v2.0.0','v1.0.0-rc.01','v1.0.0-foo'):
            with self.assertRaises(ValueError): release.prepare(tag,self.out)
        (self.root/'untracked').write_text('dirty')
        with self.assertRaisesRegex(ValueError,'clean'): self.prepare()
    def test_wrong_tag_commit(self):
        (self.root/'new').write_text('fixture'); self.run_git('add','.'); self.run_git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','second')
        with self.assertRaisesRegex(ValueError,'HEAD'): self.prepare()
    def test_prerelease(self):
        (self.root/'CHANGELOG.md').write_text('# Changelog\n\n## [1.0.0-rc.1]\n\nFictional prerelease.\n')
        record=release.prepare('v1.0.0-rc.1',self.out,True)
        self.assertEqual('1.0.0-rc.1',record['version'])
        with self.assertRaisesRegex(ValueError,'Preview'): release.verify_bundle(self.out)
    def test_corrupt_and_conflicting_outputs(self):
        self.prepare(); (self.out/'release-notes.md').write_text('corrupt')
        with self.assertRaisesRegex(ValueError,'Checksum'): release.verify_bundle(self.out)
        with self.assertRaisesRegex(ValueError,'Immutable'): self.prepare()
    def test_lock_and_atomic_failure_resume(self):
        lock=self.out.with_name('bundle.lock'); lock.write_text('other process')
        with self.assertRaises(FileExistsError): self.prepare()
        self.assertFalse(self.out.exists()); lock.unlink()
        with patch.object(release.os,'rename',side_effect=OSError('disk failure')):
            with self.assertRaises(OSError): self.prepare()
        self.assertFalse(lock.exists()); self.prepare(); release.verify_bundle(self.out)
    def test_complete_catalog_and_no_local_paths(self):
        self.prepare(); output=self.out.with_name('catalog'); release.catalog([self.out],output)
        files=release.snapshot(output)
        for manifest in ('.codex-plugin/plugin.json','.claude-plugin/plugin.json'):
            self.assertEqual('1.0.0',json.loads(files['plugins/fictional/'+manifest])['version'])
        self.assertIn('plugins/fictional/skills/fictional/SKILL.md',files)
        self.assertNotIn(str(self.root).encode(),b''.join(files.values()))
        with self.assertRaisesRegex(ValueError,'duplicate'): release.catalog([self.out,self.out],self.out.with_name('invalid'))
    def test_publication_resume_and_conflict(self):
        record=self.prepare(); local=release.snapshot(self.out); calls=[]
        def fake(*args):
            calls.append(args)
            if args[0]=='api' and args[1].endswith('/commits/v1.0.0'): return json.dumps({'sha':record['commit']})
            if args[0]=='api': return json.dumps([[{'tag_name':'v1.0.0','body':local['release-notes.md'].decode()}]])
            if args[:2]==('release','view'): return json.dumps({'assets':[{'name':'release.json'}],'isDraft':True})
            if args[:2]==('release','download'):
                Path(args[-1],'release.json').write_bytes(local['release.json']); return ''
            return ''
        with patch.object(publish,'gh',side_effect=fake): publish.publish(self.out,'example/fictional')
        uploads=[c[3] for c in calls if c[:2]==('release','upload')]
        self.assertNotIn(str(self.out/'release.json'),uploads)
        self.assertEqual(len(local)-1,len(uploads))
        self.assertTrue(any(c[:2]==('release','edit') for c in calls))
    def test_partial_upload_failure_does_not_publish(self):
        record=self.prepare(); calls=[]
        def fake(*args):
            calls.append(args)
            if args[0]=='api' and args[1].endswith('/commits/v1.0.0'): return json.dumps({'sha':record['commit']})
            if args[0]=='api': return '[[]]'
            if args[:2]==('release','view'): return '{"assets":[],"isDraft":true}'
            if args[:2]==('release','upload'): raise subprocess.CalledProcessError(1,args)
            return ''
        with patch.object(publish,'gh',side_effect=fake):
            with self.assertRaises(subprocess.CalledProcessError): publish.publish(self.out,'example/fictional')
        self.assertFalse(any(c[:2]==('release','edit') for c in calls))

    def test_publication_rejects_existing_asset_conflict(self):
        record=self.prepare(); local=release.snapshot(self.out); calls=[]
        def fake(*args):
            calls.append(args)
            if args[0]=='api' and args[1].endswith('/commits/v1.0.0'): return json.dumps({'sha':record['commit']})
            if args[0]=='api': return json.dumps([[{'tag_name':'v1.0.0','body':local['release-notes.md'].decode()}]])
            if args[:2]==('release','view'): return json.dumps({'assets':[{'name':'release.json'}],'isDraft':True})
            if args[:2]==('release','download'):
                Path(args[-1],'release.json').write_text('conflicting bytes'); return ''
            return ''
        with patch.object(publish,'gh',side_effect=fake):
            with self.assertRaisesRegex(ValueError,'asset conflict'): publish.publish(self.out,'example/fictional')
        self.assertFalse(any(c[:2] in [('release','upload'),('release','edit')] for c in calls))
    def test_published_partial_release_is_never_modified(self):
        record=self.prepare(); local=release.snapshot(self.out); calls=[]
        def fake(*args):
            calls.append(args)
            if args[0]=='api' and args[1].endswith('/commits/v1.0.0'): return json.dumps({'sha':record['commit']})
            if args[0]=='api': return json.dumps([[{'tag_name':'v1.0.0','body':local['release-notes.md'].decode()}]])
            if args[:2]==('release','view'): return '{"assets":[],"isDraft":false}'
            return ''
        with patch.object(publish,'gh',side_effect=fake):
            with self.assertRaisesRegex(ValueError,'published release'): publish.publish(self.out,'example/fictional')
        self.assertFalse(any(c[:2] in [('release','upload'),('release','edit')] for c in calls))
    def test_artifact_version_conflict_even_with_valid_checksums(self):
        record=self.prepare(); path=self.out/'fictional-1.0.0-codex.zip'
        import zipfile
        with zipfile.ZipFile(path) as archive: files={n:archive.read(n) for n in archive.namelist()}
        manifest=json.loads(files['.codex-plugin/plugin.json']);manifest['version']='9.0.0'
        files['.codex-plugin/plugin.json']=release.encode(manifest);release.plugin.archive(path,files)
        record['assets'][path.name]=release.digest(path.read_bytes());(self.out/'release.json').write_bytes(release.encode(record))
        files=release.snapshot(self.out)
        (self.out/'SHA256SUMS').write_text(''.join(f'{release.digest(data)}  {name}\n' for name,data in sorted(files.items()) if name!='SHA256SUMS'))
        with self.assertRaisesRegex(ValueError,'Artifact/manifest'):release.verify_bundle(self.out)

    def test_release_notes_derive_only_selected_changelog_section(self):
        (self.root/'CHANGELOG.md').write_text('# Changelog\n\n## [1.0.0] - pending\n\nSelected changes.\n\n## [0.9.0]\n\nOld changes.\n')
        release.prepare('v1.0.0',self.out,True)
        notes=(self.out/'release-notes.md').read_text()
        self.assertIn('Selected changes.',notes);self.assertNotIn('Old changes.',notes)
    def test_missing_changelog_version_blocks_release(self):
        (self.root/'CHANGELOG.md').write_text('# Changelog\n\n## [Unreleased]\n\nNot versioned.\n')
        with self.assertRaisesRegex(ValueError,'CHANGELOG'):release.prepare('v1.0.0',self.out,True)

if __name__=='__main__': unittest.main()
