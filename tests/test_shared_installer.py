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
        source = self.root / 'skills/fictional-skill'
        source.mkdir(parents=True)
        (source / 'SKILL.md').write_text('---\nname: fictional-skill\ndescription: Fictional test\n---\n# Test')
        self.manifest = {'name':'fictional-product', 'repository':'https://github.com/example/fictional-product','description':'Fictional plugin',
            'extensions': {'io.zyris.distribution':{'skillRoot':'skills'}}}
        self.write_manifest()
        with patch.object(engine, 'ROOT', self.root): engine.repository_metadata()
        for relative in ('scripts/plugin.py','install.sh','plugin.mk'):
            target = self.root / relative
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(ROOT / relative,target)
        (self.root / 'Makefile').write_text('include plugin.mk\n')

    def write_manifest(self):
        (self.root / 'plugin.json').write_text(json.dumps(self.manifest))

    def invoke(self, *args):
        return subprocess.run(args,cwd=self.root,capture_output=True,text=True,check=True)

    def test_extra_file_mapping_cannot_ship_local_outputs_or_bytecode(self):
        for relative in ('.tmp/report.txt', 'dist/old.zip', '.idea/workspace.xml',
                         '__pycache__/module.pyc', 'module.pyo', 'module.pyd', '.DS_Store'):
            with self.subTest(relative=relative):
                source = self.root / relative
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_text('Fictional local output')
                self.manifest['extensions']['io.zyris.distribution']['files'] = {'assets/leak.txt': relative}
                self.write_manifest()
                with self.assertRaisesRegex(ValueError, 'Generated/local'):
                    engine.configuration(self.root)
        self.manifest['extensions']['io.zyris.distribution']['files'] = {'dist/leak.txt': 'plugin.json'}
        self.write_manifest()
        with self.assertRaisesRegex(ValueError, 'Generated/local'):
            engine.configuration(self.root)

    def test_arbitrary_manifest_drives_both_wrappers_and_update(self):
        first=json.loads(self.invoke('bash','install.sh','install','--target','claude','--dry-run').stdout)
        second=self.invoke('make','-s','install','TARGET=claude','DRY_RUN=1')
        self.assertEqual(first,json.loads(second.stdout))
        self.assertEqual(self.manifest['repository'],first['commands'][0][4])
        update=json.loads(self.invoke('bash','install.sh','update','--target','claude','--dry-run').stdout)
        self.assertEqual('fictional-product@fictional-product-marketplace',update['commands'][1][3])
        catalog=json.loads((self.root/'.claude-plugin/marketplace.json').read_text())
        self.assertEqual('fictional-product-marketplace',catalog['name'])
        self.assertEqual('Fictional plugin',catalog['plugins'][0]['description'])

    def test_native_failure_propagates_and_chatgpt_never_executes_host(self):
        with patch.object(engine,'ROOT',self.root),patch.object(engine.shutil,'which',return_value='claude'),patch.object(engine.subprocess,'run',side_effect=subprocess.CalledProcessError(7,['claude'])) as run:
            with self.assertRaises(subprocess.CalledProcessError):engine.install('claude')
            run.reset_mock()
            self.assertFalse(engine.install('chatgpt')['installed'])
            run.assert_not_called()

    def test_manifest_paths_and_identity_are_validated(self):
        with patch.object(engine,'ROOT',self.root):
            for cfg in ({'skillRoot':'../external'},{'skillRoot':'skills','files':{'../escape':'plugin.json'}},{'skillRoot':'skills','files':{'plugin.json':'plugin.json'}}):
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
            self.assertEqual(['codex','plugin','add','fictional-product@fictional-product-marketplace'], result['commands'][1])
            self.assertFalse(result['executed'])
            import zipfile
            artifacts = engine.build()
            with zipfile.ZipFile(artifacts['codex_zip']) as archive:
                manifest = json.loads(archive.read('.codex-plugin/plugin.json'))
                self.assertEqual('fictional-product', manifest['name'])
                self.assertEqual('./skills/', manifest['skills'])
                self.assertEqual(artifacts['version'], manifest['version'])
                self.assertIn('skills/fictional-skill/SKILL.md', archive.namelist())
                self.assertNotIn('plugin.json', archive.namelist())
                self.assertNotIn('.claude-plugin/plugin.json', archive.namelist())
        second = json.loads(self.invoke('bash','install.sh','codex','--dry-run').stdout)
        self.assertEqual(result, second)
        update = json.loads(self.invoke('make','-s','update','TARGET=codex','DRY_RUN=1').stdout)
        self.assertEqual([['codex','plugin','marketplace','upgrade','fictional-product-marketplace','--json']], update['commands'])

    def test_codex_missing_cli_and_failed_registration_never_report_success(self):
        with patch.object(engine,'ROOT',self.root), patch.object(engine.shutil,'which',return_value=None), patch.object(engine.subprocess,'run') as run:
            with self.assertRaisesRegex(ValueError, 'codex CLI not found'):engine.install('codex')
            run.assert_not_called()
        with patch.object(engine,'ROOT',self.root), patch.object(engine.shutil,'which',return_value='codex'), patch.object(engine.subprocess,'run',side_effect=subprocess.CalledProcessError(7,['codex'])) as run:
            with self.assertRaises(subprocess.CalledProcessError):engine.install('codex',update=True)
            self.assertEqual(1,run.call_count)

    @unittest.skipUnless(os.environ.get('ZYRIS_TEST_CODEX_NATIVE') == '1' and shutil.which('codex'), 'Opt-in real Codex CLI integration')
    def test_native_git_update_without_manifest_version(self):
        isolated = self.root / 'isolated-home'; isolated.mkdir()
        codex_home = isolated / '.codex'; codex_home.mkdir()
        env = dict(os.environ, HOME=str(isolated), CODEX_HOME=str(codex_home))
        def invoke(*args):
            return subprocess.run(args, cwd=self.root, env=env, capture_output=True, text=True, check=True, timeout=30)
        invoke('git','init','-q')
        invoke('git','add','--','plugin.json','skills','.claude-plugin','.agents')
        def commit(message): invoke('git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qam',message)
        commit('initial fictional plugin')
        (codex_home/'config.toml').write_text('[marketplaces.fictional-product-marketplace]\nsource_type = "git"\nsource = '+json.dumps(str(self.root))+'\n')
        invoke('codex','plugin','marketplace','upgrade','fictional-product-marketplace','--json')
        result=json.loads(invoke('codex','plugin','add','fictional-product@fictional-product-marketplace','--json').stdout)
        cache=Path(result['installedPath'])/'skills/fictional-skill/SKILL.md'
        skill=self.root/'skills/fictional-skill/SKILL.md'
        self.assertEqual(skill.read_bytes(),cache.read_bytes())
        skill.write_text(skill.read_text()+'\nUpdated fictional instructions.\n');commit('update fictional instructions')
        invoke('codex','plugin','marketplace','upgrade','fictional-product-marketplace','--json')
        self.assertEqual(skill.read_bytes(),cache.read_bytes())
        self.assertNotIn('version',json.loads((self.root/'plugin.json').read_text()))
