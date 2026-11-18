import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'skills/zyris-skill-documentation/scripts'))
import repository_policy as policy
import plugin_audit as audit


class RepositoryPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.repo = self.root/'repo'
        self.repo.mkdir()
        (self.repo/'.gitignore').write_bytes((ROOT/'skills/zyris-skill-documentation/templates/plugin/gitignore.txt').read_bytes())
        subprocess.run(['git','init','--quiet','--template=',str(self.repo)],check=True)

    def test_ignore_rules_work_and_nested_negations_fail_without_mutation(self):
        self.assertEqual(([], []), policy.hygiene(self.repo))
        nested=self.repo/'skills/example'
        nested.mkdir(parents=True)
        (nested/'.gitignore').write_text('!*.pyc\n')
        before={str(p):p.read_bytes() for p in self.repo.rglob('*') if p.is_file()}
        errors, _=policy.hygiene(self.repo)
        self.assertTrue(any('skills/example/probe.pyc' in e for e in errors))
        self.assertEqual(before,{str(p):p.read_bytes() for p in self.repo.rglob('*') if p.is_file()})

    def test_missing_rules_and_tracked_outputs_are_reported(self):
        (self.repo/'.gitignore').write_text('.DS_Store\n')
        self.assertTrue(policy.hygiene(self.repo)[0])
        (self.repo/'.gitignore').write_bytes((ROOT/'skills/zyris-skill-documentation/templates/plugin/gitignore.txt').read_bytes())
        local=self.repo/'.tmp/evidence.txt'
        local.parent.mkdir();local.write_text('Fictional evidence to preserve')
        subprocess.run(['git','-C',str(self.repo),'add','-f','.tmp/evidence.txt'],check=True)
        errors,_=policy.hygiene(self.repo)
        self.assertTrue(any('already tracked' in e for e in errors))
        self.assertEqual('Fictional evidence to preserve',local.read_text())

    def test_missing_git_is_not_reported_as_success(self):
        with patch.object(policy,'git',side_effect=FileNotFoundError('git unavailable')):
            errors,warnings=policy.hygiene(self.repo)
        self.assertFalse(errors)
        self.assertTrue(any('incomplete' in w for w in warnings))

    def test_python_is_parsed_not_executed_and_missing_import_is_visible(self):
        files={'skills/example/scripts/main.py':b'import os\nimport helper\nraise RuntimeError("never execute")\n',
               'skills/example/scripts/helper.py':b'value = 1\n'}
        self.assertEqual(([],[]),policy.python_payload(files))
        del files['skills/example/scripts/helper.py']
        self.assertTrue(policy.python_payload(files)[1])
        files['skills/example/scripts/main.py']=b'def broken(\n'
        self.assertTrue(policy.python_payload(files)[0])

    def test_init_ships_ignore_template_without_verify_or_empty_work_folders(self):
        source=self.root/'source';source.mkdir()
        (source/'SKILL.md').write_text('---\nname: fictional-example\ndescription: Fictional test.\n---\n# Example\n')
        output=self.root/'output'
        with patch.object(audit,'audit',side_effect=AssertionError('init must not verify')):
            audit.initialize(source,output,languages=['en'])
        self.assertEqual((self.repo/'.gitignore').read_bytes(),(output/'.gitignore').read_bytes())
        for name in ('.tmp','dist','.idea','.venv','__pycache__'):
            self.assertFalse((output/name).exists(),name)
        self.assertFalse((output/'gitignore.txt').exists())

    def test_extracted_packages_run_independently_and_can_initialize(self):
        build=self.root/'build'
        subprocess.run([sys.executable,str(ROOT/'scripts/plugin.py'),'build','--output',str(build)],check=True,capture_output=True)
        env={k:v for k,v in os.environ.items() if k not in ('PYTHONPATH','PYTHONHOME','PYTHONDONTWRITEBYTECODE')}
        source=self.root/'fictional-source';source.mkdir()
        (source/'SKILL.md').write_text('---\nname: fictional-example\ndescription: Fictional test.\n---\n# Example\n')
        for archive in build.glob('*.zip'):
            with self.subTest(archive=archive.name):
                extracted=self.root/archive.stem
                with zipfile.ZipFile(archive) as z: z.extractall(extracted)
                scripts=extracted/'skills/zyris-skill-documentation/scripts'
                inspected=subprocess.run([sys.executable,str(scripts/'documentation.py'),'inspect','--source',str(source)],cwd=self.root,env=env,check=True,capture_output=True,text=True)
                self.assertEqual('fictional-example',json.loads(inspected.stdout)['name'])
                output=self.root/(archive.stem+'-initialized')
                subprocess.run([sys.executable,str(scripts/'plugin_audit.py'),'init','--source',str(source),'--output',str(output),'--languages','en'],cwd=self.root,env=env,check=True,capture_output=True)
                self.assertTrue((output/'.gitignore').is_file())
                report=subprocess.run([sys.executable,str(scripts/'plugin_audit.py'),'verify','--source',str(output)],cwd=self.root,env=env,capture_output=True,text=True)
                self.assertEqual(1,report.returncode)  # Unfinished docs are intentionally not certified.
                checks=json.loads(report.stdout)['checks']
                self.assertTrue(all(c['status']=='pass' for c in checks if c['id'].startswith('installer:')))
                self.assertFalse(list(extracted.rglob('__pycache__')))
                self.assertFalse(list(output.rglob('__pycache__')))
