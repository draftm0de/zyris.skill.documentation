import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT/'skills/zyris-skill-manager/scripts/publish_plan.py'
SPEC=importlib.util.spec_from_file_location('publish_plan',HELPER)
plan=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(plan)

class PublishPlanTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.work=Path(self.tmp.name).resolve();self.root=self.work/'source';self.root.mkdir();self.state=self.work/'private-journal'
        self.repo='https://github.com/example/fixture'
        (self.root/'plugin.json').write_text(json.dumps({'name':'fixture','repository':self.repo}))
        (self.root/'CHANGELOG.md').write_text('# Changelog\n\n## [0.1.0]\n\nFictional initial version.\n')
        (self.root/'.gitignore').write_text('.tmp/\ndist/\n')
        self.git('init','-q');self.git('config','user.name','Fixture');self.git('config','user.email','fixture@example.invalid')
        self.git('add','.');self.git('commit','-qm','fixture');self.git('remote','add','origin',self.repo)
        self.proposal={'files':['plugin.json','CHANGELOG.md'],
          'commit_message':'feat: fictional manager','pr_title':'Fictional manager','pr_body':'Fictional tested change',
          'branch':'codex/publish-manager','base_branch':'main','repository':self.repo,'merge_method':'squash',
          'checks':[{'name':'fixture','result':'passed','evidence':'fictional test log'}]}
    def git(self,*args):return subprocess.check_output(['git','-C',str(self.root),*args],stderr=subprocess.STDOUT)
    def prepare(self):return plan.prepare(self.root,self.proposal,self.state)
    def approve(self):
        result=self.prepare();return plan.approve(self.state,result['digest'],'Yes: approve message and all listed publication steps.', confirmed=True)
    def test_preparation_has_no_git_mutations_and_retry_is_identical(self):
        head=self.git('rev-parse','HEAD');status=self.git('status','--porcelain')
        first=self.prepare();self.assertEqual(first,self.prepare());self.assertEqual('prepared',first['stage'])
        self.assertEqual(head,self.git('rev-parse','HEAD'));self.assertEqual(status,self.git('status','--porcelain'))
    def test_denied_or_absent_approval_does_not_advance(self):
        data=self.prepare()
        with self.assertRaises(ValueError):plan.approve(self.state,data['digest'],'', confirmed=True)
        with self.assertRaises(ValueError):plan.checkpoint(self.state,'committed',{'commit':'b'*40})
        with self.assertRaises(ValueError):plan.approve(self.state,data['digest'],'No, do not publish', confirmed=False)
        self.assertEqual('prepared',plan.read(self.state)['stage'])
    def test_digest_mismatch_rejected(self):
        self.prepare()
        with self.assertRaises(ValueError):plan.approve(self.state,'wrong','yes', confirmed=True)
    def test_selected_file_drift_invalidates_approval(self):
        data=self.prepare();(self.root/'CHANGELOG.md').write_text('changed after review')
        with self.assertRaisesRegex(ValueError,'Source changed'):plan.approve(self.state,data['digest'],'yes', confirmed=True)
    def test_postapproval_drift_is_detected_before_commit(self):
        self.approve();(self.root/'plugin.json').write_text('{}')
        with self.assertRaises(ValueError):plan.ensure_current(plan.read(self.state))
    def test_unrelated_work_not_included_or_modified(self):
        (self.root/'unrelated.txt').write_text('keep private draft out')
        data=self.prepare();self.assertNotIn('unrelated.txt',data['plan']['snapshot']['files'])
        self.assertEqual('keep private draft out',(self.root/'unrelated.txt').read_text())
    def test_preexisting_index_preserved(self):
        (self.root/'staged.txt').write_text('preserve');self.git('add','staged.txt');before=self.git('diff','--cached','--binary')
        with self.assertRaisesRegex(ValueError,'staged'):self.prepare()
        self.assertEqual(before,self.git('diff','--cached','--binary'))
    def test_manifest_repository_conflict(self):
        (self.root/'plugin.json').write_text(json.dumps({'name':'fixture','repository':'https://github.com/example/other'}))
        with self.assertRaisesRegex(ValueError,'repository'):self.prepare()
    def test_version_and_legacy_journal_are_rejected(self):
        (self.root/'plugin.json').write_text(json.dumps({'name':'fixture','version':'1.0.0','repository':self.repo}))
        with self.assertRaisesRegex(ValueError,'omit'):self.prepare()
    def test_failed_check_blocks_plan(self):
        self.proposal['checks'][0]['result']='failed'
        with self.assertRaises(ValueError):self.prepare()
    def test_documentation_only_publish_needs_no_manifest_or_changelog_edit(self):
        (self.root/'README.md').write_text('Fictional documentation change')
        self.proposal['files']=['README.md']
        (self.root/'CHANGELOG.md').unlink()
        self.assertEqual(['README.md'],self.prepare()['plan']['proposal']['files'])
    def test_unselected_manifest_drift_invalidates_documentation_approval(self):
        (self.root/'README.md').write_text('Fictional docs')
        self.proposal['files']=['README.md']
        data=self.prepare()
        (self.root/'plugin.json').write_text(json.dumps({'name':'changed','repository':self.repo}))
        with self.assertRaisesRegex(ValueError,'Source changed'):plan.approve(self.state,data['digest'],'yes',confirmed=True)
    def test_legacy_journal_cannot_resume_under_new_workflow(self):
        data=self.prepare();data['plan']['schema_version']=1;data['digest']=plan.sha(plan.encoded(data['plan']))
        (self.state/'publication.json').write_bytes(plan.encoded(data))
        with self.assertRaisesRegex(ValueError,'Legacy publication journal'):plan.read(self.state)
    def test_unsafe_selected_files(self):
        for name in ('../outside','.env','.tmp/output','private.key'):
            self.proposal['files']=['plugin.json','CHANGELOG.md',name]
            with self.assertRaises(ValueError):self.prepare()
    def test_state_cannot_be_in_source_or_plugin(self):
        for state in (self.root/'private-state',HELPER.parent/'state'):
            with self.assertRaises(ValueError):plan.prepare(self.root,self.proposal,state)
    def test_tampered_plan_rejected(self):
        self.prepare();p=self.state/'publication.json';data=json.loads(p.read_text());data['plan']['proposal']['commit_message']='tampered';p.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError,'integrity'):plan.read(self.state)
    def test_lock_conflict_preserves_existing_journal(self):
        self.prepare();before=(self.state/'publication.json').read_bytes();(self.state/'.lock').touch()
        with self.assertRaises(FileExistsError):self.prepare()
        self.assertEqual(before,(self.state/'publication.json').read_bytes())
    def test_changed_message_requires_new_plan(self):
        self.prepare();self.proposal['commit_message']='different proposal'
        with self.assertRaisesRegex(ValueError,'new approval'):self.prepare()
    def test_complete_journal_and_identical_retry(self):
        self.approve();commit='b'*40;merged='c'*40
        steps=[('committed',{'commit':commit}),('pushed',{'commit':commit,'branch':self.proposal['branch']}),
         ('pr_open',{'url':self.repo+'/pull/1','head':commit}),
         ('checks_passed',{'head':commit,'checks':[{'name':'test','result':'passed'}]}),
         ('merged',{'commit':merged,'url':self.repo+'/pull/1'})]
        for stage,evidence in steps:
            current=plan.checkpoint(self.state,stage,evidence);self.assertEqual(current,plan.checkpoint(self.state,stage,evidence))
        self.assertEqual('merged',plan.read(self.state)['stage'])
        with self.assertRaises(ValueError):plan.checkpoint(self.state,'released',{'commit':merged})
    def test_changed_remote_head_and_failed_checks_stop(self):
        self.approve();plan.checkpoint(self.state,'committed',{'commit':'b'*40})
        with self.assertRaises(ValueError):plan.checkpoint(self.state,'pushed',{'commit':'c'*40,'branch':self.proposal['branch']})
        plan.checkpoint(self.state,'pushed',{'commit':'b'*40,'branch':self.proposal['branch']})
        plan.checkpoint(self.state,'pr_open',{'head':'b'*40,'url':self.repo+'/pull/1'})
        with self.assertRaises(ValueError):plan.checkpoint(self.state,'checks_passed',{'head':'b'*40,'checks':[{'result':'pending'}]})
    def test_extracted_runtime_prepares_without_manager_checkout(self):
        output=self.work/'artifacts'
        subprocess.run([sys.executable,'-B',str(ROOT/'scripts/plugin.py'),'build','--output',str(output)],check=True,capture_output=True)
        installed=self.work/'installed';installed.mkdir()
        with zipfile.ZipFile(output/'zyris-skill-manager-codex-plugin.zip') as archive:archive.extractall(installed)
        proposal=self.work/'proposal.json';proposal.write_text(json.dumps(self.proposal))
        helper=installed/'skills/zyris-skill-manager/scripts/publish_plan.py'
        result=subprocess.run([sys.executable,'-B',str(helper),'prepare','--source',str(self.root),'--proposal',str(proposal),'--state-dir',str(self.state)],cwd=self.work,capture_output=True,text=True,check=True)
        self.assertEqual('prepared',json.loads(result.stdout)['stage'])

if __name__=='__main__':unittest.main()
