import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT=Path(__file__).resolve().parents[1]
if not (ROOT/'plugin.json').exists():ROOT=ROOT.parent
spec=importlib.util.spec_from_file_location('docs_export',ROOT/'scripts/export_docs.py')
engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine)


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name).resolve()/'repo';self.root.mkdir()
        (self.root/'docs/en').mkdir(parents=True)
        (self.root/'docs/assets').mkdir()
        (self.root/'docs/assets/icon.png').write_bytes(b'fictional public image')
        (self.root/'LICENSE').write_text('Fictional license fixture')
        (self.root/'README.md').write_text('# Fictional product\n\n[Usage](docs/en/usage.md#start)\n![Icon](docs/assets/icon.png)\n[License](LICENSE)\n')
        (self.root/'docs/en/usage.md').write_text('# Usage\n\n## Start\n\n[Home](../../README.md)\n[External](https://example.com/)\n')
        self.plugin={'name':'fictional-product','version':'1.2.3','description':'From plugin.json','license':'MIT'}
        self.config={'schema_version':1,'documentation':{'languages':['en'],'default_language':'en'},
                     'export':{'schema_version':1,'pages':{'overview':{'en':'README.md'},'usage':{'en':'docs/en/usage.md'}},'assets':['docs/assets/icon.png']}}
        self.save()

    def save(self):
        (self.root/'plugin.json').write_text(json.dumps(self.plugin))
        (self.root/'docs/documentation.json').write_text(json.dumps(self.config))

    def test_export_is_reproducible_verbatim_and_tracks_sources(self):
        before={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        first=engine.export(self.root);archive=Path(first['output']);original=archive.read_bytes()
        second=engine.export(self.root);self.assertEqual(original,archive.read_bytes())
        with zipfile.ZipFile(archive) as package:
            index=json.loads(package.read('index.json'))
            self.assertEqual('zyris.documentation',index['format'])
            self.assertEqual(self.plugin,index['plugin'])
            self.assertEqual({'index.json','content/README.md','content/docs/en/usage.md','content/docs/assets/icon.png'},set(package.namelist()))
            for page in index['pages']+index['assets']:
                self.assertEqual(before[page['source_path']],package.read(page['file']))
            links=index['pages'][0]['links']
            self.assertEqual({'page','asset','repository'},{link['kind'] for link in links})
            self.assertEqual('start',next(link['fragment'] for link in links if link['kind']=='page'))
        for path,content in before.items():self.assertEqual(content,(self.root/path).read_bytes())
        self.plugin['version']='2.0.0';self.save()
        changed=engine.export(self.root)
        self.assertNotEqual(first['source']['content_sha256'],changed['source']['content_sha256'])
        self.assertFalse(first['published'])

    def test_bilingual_and_english_default(self):
        (self.root/'docs/de').mkdir()
        (self.root/'README.de.md').write_text('# Produkt\n[English](README.md)\n')
        (self.root/'docs/de/usage.md').write_text('# Nutzung\n[Start](../../README.de.md)\n')
        self.config['documentation']['languages']=['en','de']
        self.config['export']['pages']['overview']['de']='README.de.md'
        self.config['export']['pages']['usage']['de']='docs/de/usage.md';self.save()
        index,_=engine.build_files(self.root)
        self.assertEqual(4,len(index['pages']))
        self.assertEqual('en',index['documentation']['default_language'])
        del self.config['export']['pages']['usage']['de'];self.save()
        with self.assertRaisesRegex(ValueError,'exactly'):engine.build_files(self.root)

    def test_rejects_drift_private_paths_links_and_incomplete_content(self):
        bad_values=[('assets',['../secret.png']),('assets',['docs/.env']),('product_name','duplicated fact')]
        for key,value in bad_values:
            original=json.loads(json.dumps(self.config))
            self.config['export'][key]=value;self.save()
            with self.subTest(value=value),self.assertRaises(ValueError):engine.build_files(self.root)
            self.config=original;self.save()
        for content in ('# Page\n[Broken](missing.md)', '# Page\n[Wrong anchor](docs/en/usage.md#missing)', '# Page\n{{UNWRITTEN}}', '# Page\n[Unsafe](javascript:alert)', '# Page\n[Private](.env)', '# Page\n[External path](../secret.md)'):
            (self.root/'README.md').write_text(content)
            with self.subTest(content=content),self.assertRaises(ValueError):engine.build_files(self.root)
        self.assertFalse((self.root/'dist').exists())

    def test_asset_must_be_declared_and_symlinks_are_refused(self):
        self.config['export']['assets']=[];self.save()
        with self.assertRaisesRegex(ValueError,'not declared'):engine.build_files(self.root)
        self.config['export']['assets']=['docs/assets/icon.png'];self.save()
        image=self.root/'docs/assets/icon.png';image.unlink();image.symlink_to(self.root/'LICENSE')
        with self.assertRaisesRegex(ValueError,'symlink'):engine.build_files(self.root)

    def test_read_only_check_and_atomic_failure_preserve_existing_export(self):
        result=engine.export(self.root,check=True)
        self.assertTrue(result['valid']);self.assertFalse((self.root/'dist').exists())
        existing=Path(engine.export(self.root)['output']);before=existing.read_bytes()
        with patch.object(engine.os,'replace',side_effect=OSError('fictional write failure')):
            with self.assertRaises(OSError):engine.export(self.root)
        self.assertEqual(before,existing.read_bytes())
        self.assertEqual([existing],list(existing.parent.iterdir()))
        foreign=existing.parent/'foreign.zip';foreign.write_bytes(b'user-owned data')
        with self.assertRaisesRegex(ValueError,'unowned'):engine.export(self.root,foreign)
        self.assertEqual(b'user-owned data',foreign.read_bytes())
        with self.assertRaisesRegex(ValueError,'dist'):engine.export(self.root,self.root/'docs/source.zip')

    def test_references_html_and_code_examples(self):
        page=self.root/'README.md'
        page.write_text('''# Fictional
[Read][guide]
[guide]: docs/en/usage.md#start
<img src="docs/assets/icon.png" alt="icon">
```markdown
[Not a link](missing-example.md)
```
`[Not a link](missing-inline.md)`
''')
        index,_=engine.build_files(self.root)
        self.assertEqual(2,len(index['pages'][0]['links']))

    @unittest.skipUnless(shutil.which('git'),'Git required for provenance test')
    def test_provenance_marks_dirty_worktree_instead_of_claiming_commit_matches(self):
        def git(*args):return subprocess.run(['git','-C',str(self.root),*args],check=True,capture_output=True)
        git('init');(self.root/'.gitignore').write_text('dist/\n')
        git('add','.');git('-c','user.name=Fictional Test','-c','user.email=test@example.invalid','commit','-m','Fixture')
        source=engine.build_files(self.root)[0]['source']
        self.assertFalse(source['working_tree_dirty']);self.assertEqual(40,len(source['revision']))
        (self.root/'README.md').write_text((self.root/'README.md').read_text()+'\nChanged locally.\n')
        changed=engine.build_files(self.root)[0]['source']
        self.assertTrue(changed['working_tree_dirty']);self.assertEqual(source['revision'],changed['revision'])
        self.assertNotEqual(source['content_sha256'],changed['content_sha256'])

    def test_packaged_documentation_plugin_can_export_without_checkout(self):
        if not (ROOT / 'skills/zyris-skill-documentation').exists():
            self.skipTest('Documentation plugin package acceptance only')
        package_dir=self.root.parent/'plugin-package'
        subprocess.run([os.sys.executable,str(ROOT/'scripts/plugin.py'),'build','--output',str(package_dir)],check=True,capture_output=True)
        installed=self.root.parent/'installed'
        with zipfile.ZipFile(package_dir/'zyris-skill-documentation-codex-plugin.zip') as package:
            package.extractall(installed)
        helper=installed/'skills/zyris-skill-documentation/scripts/documentation.py'
        result=subprocess.run([os.sys.executable,str(helper),'export','--source',str(self.root),'--check'],check=True,capture_output=True,text=True)
        self.assertTrue(json.loads(result.stdout)['valid'])
        self.assertFalse((self.root/'dist').exists())
