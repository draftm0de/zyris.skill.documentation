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

ROOT = Path(__file__).resolve().parents[1]
if not (ROOT / 'plugin.json').is_file():
    ROOT = ROOT.parent
spec = importlib.util.spec_from_file_location('shared_installer', ROOT / 'scripts/plugin.py')
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)


class SharedInstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        source = self.root / 'custom/skills/fictional-skill'
        source.mkdir(parents=True)
        (source / 'SKILL.md').write_text('---\nname: fictional-skill\ndescription: Fictional test\n---\n# Test')
        self.manifest = {'name':'fictional-product', 'version':'2.3.4','description':'Fictional plugin',
            'extensions': {'io.zyris.distribution':{'skillRoot':'custom/skills'}}}
        self.write_manifest()
        for relative in ('scripts/plugin.py','install.sh','plugin.mk'):
            target = self.root / relative
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(ROOT / relative,target)
        (self.root / 'Makefile').write_text('include plugin.mk\n')

    def write_manifest(self):
        (self.root / 'plugin.json').write_text(json.dumps(self.manifest))

    def invoke(self, *args):
        return subprocess.run(args,cwd=self.root,capture_output=True,text=True,check=True)

    def test_arbitrary_manifest_drives_both_wrappers_and_update(self):
        first=json.loads(self.invoke('bash','install.sh','install','--target','claude','--dry-run').stdout)
        second=self.invoke('make','-s','install','TARGET=claude','DRY_RUN=1')
        self.assertEqual(first,json.loads(second.stdout))
        self.assertEqual('fictional-product',first['commands'][0][3])
        update=json.loads(self.invoke('bash','install.sh','update','--target','claude','--dry-run').stdout)
        self.assertEqual('fictional-product@fictional-product-local',update['commands'][1][3])
        catalog=json.loads((self.root/'dist/claude-marketplace/.claude-plugin/marketplace.json').read_text())
        self.assertEqual('fictional-product-local',catalog['name'])
        self.assertEqual('Fictional plugin',catalog['plugins'][0]['description'])

    def test_native_failure_propagates_and_chatgpt_never_executes_host(self):
        with patch.object(engine,'ROOT',self.root),patch.object(engine.shutil,'which',return_value='claude'),patch.object(engine.subprocess,'run',side_effect=subprocess.CalledProcessError(7,['claude'])) as run:
            with self.assertRaises(subprocess.CalledProcessError):engine.install('claude')
            run.reset_mock()
            self.assertFalse(engine.install('chatgpt')['installed'])
            run.assert_not_called()

    def test_manifest_paths_and_identity_are_validated(self):
        with patch.object(engine,'ROOT',self.root):
            for cfg in ({'skillRoot':'../external'},{'skillRoot':'custom/skills','files':{'../escape':'plugin.json'}},{'skillRoot':'custom/skills','files':{'plugin.json':'plugin.json'}}):
                self.manifest['extensions']['io.zyris.distribution']=cfg;self.write_manifest()
                with self.assertRaises(ValueError):engine.payload()
            self.manifest['name']='../bad';self.write_manifest()
            with self.assertRaises(ValueError):engine.configuration()

    def test_marketplace_marker_must_belong_to_this_plugin(self):
        market=self.root/'dist/claude-marketplace';market.mkdir(parents=True)
        (market/'.zyris-generated').write_text('another-plugin\n')
        with patch.object(engine,'ROOT',self.root):
            with self.assertRaisesRegex(ValueError,'unowned'):engine.build()
        self.assertEqual('another-plugin\n',(market/'.zyris-generated').read_text())

    def test_existing_skills_and_private_workspace_are_untouched(self):
        private=self.root/'private-training';private.mkdir();(private/'state.json').write_text('fictional-progress')
        legacy=self.root/'home/.agents/skills/fictional-skill';legacy.mkdir(parents=True);(legacy/'SKILL.md').write_text('preserve')
        env=dict(os.environ,HOME=str(self.root/'home'))
        for args in (('claude-chat',),('all',)):
            result=subprocess.run(['bash','install.sh',*args],cwd=self.root,env=env,capture_output=True)
            self.assertEqual(2,result.returncode)
        self.invoke('bash','install.sh','build')
        self.assertEqual('preserve',(legacy/'SKILL.md').read_text())
        self.assertEqual('fictional-progress',(private/'state.json').read_text())

    def test_bash_syntax(self):
        self.invoke('bash','-n','install.sh')

    def test_codex_package_and_native_command_routing(self):
        with patch.object(engine, 'ROOT', self.root), patch.object(engine.subprocess, 'run') as run:
            result = engine.install('codex', dry_run=True)
            run.assert_not_called()
            self.assertEqual(['codex','plugin','marketplace','add'], result['commands'][0][:4])
            self.assertEqual(['codex','plugin','add','fictional-product@fictional-product-local','--json'], result['commands'][1])
            self.assertFalse(result['executed'])
            import zipfile
            with zipfile.ZipFile(result['artifacts']['codex_zip']) as archive:
                manifest = json.loads(archive.read('.codex-plugin/plugin.json'))
                self.assertEqual('fictional-product', manifest['name'])
                self.assertEqual('./skills/', manifest['skills'])
                self.assertEqual(result['artifacts']['version'], manifest['version'])
                self.assertIn('skills/fictional-skill/SKILL.md', archive.namelist())
                self.assertNotIn('plugin.json', archive.namelist())
                self.assertNotIn('.claude-plugin/plugin.json', archive.namelist())
        second = json.loads(self.invoke('bash','install.sh','codex','--dry-run').stdout)
        self.assertEqual(result, second)
        update = json.loads(self.invoke('make','-s','update','TARGET=codex','DRY_RUN=1').stdout)
        self.assertEqual(result['commands'], update['commands'])

    def test_codex_missing_cli_and_failed_registration_never_report_success(self):
        with patch.object(engine,'ROOT',self.root), patch.object(engine.shutil,'which',return_value=None), patch.object(engine.subprocess,'run') as run:
            with self.assertRaisesRegex(ValueError, 'codex CLI not found'):engine.install('codex')
            run.assert_not_called()
        with patch.object(engine,'ROOT',self.root), patch.object(engine.shutil,'which',return_value='codex'), patch.object(engine.subprocess,'run',side_effect=subprocess.CalledProcessError(7,['codex'])) as run:
            with self.assertRaises(subprocess.CalledProcessError):engine.install('codex',update=True)
            self.assertEqual(1,run.call_count)

    @unittest.skipUnless(os.environ.get('ZYRIS_TEST_CODEX_NATIVE') == '1' and shutil.which('codex'), 'Opt-in real Codex CLI integration')
    def test_native_codex_install_reinstall_and_content_update(self):
        isolated = self.root / 'isolated-codex-home'
        isolated.mkdir()
        env = dict(os.environ, CODEX_HOME=str(isolated))
        def invoke(*args):
            return subprocess.run(args, cwd=self.root, env=env, capture_output=True, text=True, check=True, timeout=30)
        def installed():
            return json.loads(invoke('codex','plugin','list','--marketplace','fictional-product-local','--json').stdout)['installed'][0]
        invoke('make','-s','install','TARGET=codex')
        first = installed()
        self.assertTrue(first['enabled'])
        self.assertTrue(first['installed'])
        invoke('bash','install.sh','install','--target','codex')
        self.assertEqual(first['version'], installed()['version'])
        skill = self.root / 'custom/skills/fictional-skill/SKILL.md'
        skill.write_text(skill.read_text() + '\nUpdated fictional instructions.\n')
        invoke('make','-s','update','TARGET=codex')
        updated = installed()
        self.assertNotEqual(first['version'], updated['version'])
        cache = isolated / 'plugins/cache/fictional-product-local/fictional-product' / updated['version'] / 'skills/fictional-skill/SKILL.md'
        self.assertEqual(skill.read_bytes(), cache.read_bytes())
        self.assertFalse((isolated / 'skills').exists())
