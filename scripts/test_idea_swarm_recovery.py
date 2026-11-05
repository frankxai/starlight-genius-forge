import contextlib,hashlib,io,json,sys,tempfile,unittest,subprocess
from pathlib import Path
from unittest import mock

SOURCE=Path(sys.argv.pop(1)) if len(sys.argv)>1 and Path(sys.argv[1]).is_file() else Path(__file__).with_name('idea_swarm_intake.py')
class Recovery(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='idea-recovery-proof-')
        self.root=Path(self.temp.name)
        assert self.root.resolve().is_relative_to(Path(tempfile.gettempdir()).resolve())
        self.addCleanup(self.temp.cleanup)
        self.ns={'__name__':'private_probe','__file__':str(SOURCE)}
        exec(compile(SOURCE.read_text(encoding='utf-8'),str(SOURCE),'exec'),self.ns)
        self.ns.update(ROOT=self.root,IDEAS=self.root/'docs/ideas',OUTBOX=self.root/'docs/ideas/_outbox')
        self.text='\ufeff  Original synthetic invention\r\n海洋\r\n'+('meaning\r\n'*300)+'  '
    def run_cli(self,args):
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):return self.ns['main'](args)
    def interrupt(self,n):
        writer=self.ns['write_new'];calls=0
        def fail(path,text):
            nonlocal calls
            calls+=1
            if calls==n:raise OSError('synthetic interrupted save')
            return writer(path,text)
        self.ns['write_new']=fail
        try:
            with self.assertRaises(OSError):self.run_cli(['--text',self.text,'--source-ref','synthetic:original/record/1'])
        finally:self.ns['write_new']=writer
        journals=list((self.root/'docs/ideas/_outbox/_pending').glob('*.json'))
        self.assertEqual(len(journals),1,'Exact-text recovery journal must precede outputs')
        self.journal=journals[0];self.meta=json.loads(self.journal.read_bytes())
        self.assertEqual(self.meta['rawText'],self.text)
        return self.meta['ideaId']
    def verify(self,identifier):
        self.assertEqual(self.run_cli(['--recover-id',identifier]),0)
        meta=json.loads((self.root/'docs/ideas/_outbox'/f'{identifier}.json').read_bytes())
        self.assertEqual(meta['rawText'],self.text)
        self.assertEqual(meta['rawTextSha256'],hashlib.sha256(self.text.encode()).hexdigest())
        self.assertEqual(meta['sourceRef'],'synthetic:original/record/1')
        self.assertIn(self.text.encode(),(self.root/meta['cardPath']).read_bytes())
        self.assertTrue((self.root/meta['issueBodyPath']).exists())
    def test_interruption_before_card_recovers(self):self.verify(self.interrupt(2))
    def test_interruption_before_issue_recovers(self):self.verify(self.interrupt(3))
    def test_interruption_before_metadata_recovers(self):self.verify(self.interrupt(4))
    def test_recovery_is_idempotent(self):
        identifier=self.interrupt(3);self.verify(identifier)
        before={p:p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.verify(identifier)
        self.assertEqual(before,{p:p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
    def test_hash_tamper_is_refused_without_outputs(self):
        identifier=self.interrupt(2);self.meta['rawText']='different source'
        self.journal.write_text(json.dumps(self.meta),encoding='utf-8')
        self.assertEqual(self.run_cli(['--recover-id',identifier]),2)
        self.assertEqual(list((self.root/'docs/ideas').glob('*.md')),[])
    def test_destination_conflict_preserves_every_byte(self):
        identifier=self.interrupt(2)
        conflict=self.root/self.meta['issueBodyPath'];conflict.write_bytes(b'other owned capture')
        before={p:p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(self.run_cli(['--recover-id',identifier]),2)
        self.assertEqual(before,{p:p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
    def test_path_tamper_is_refused(self):
        identifier=self.interrupt(2);self.meta['cardPath']='../outside.md'
        self.journal.write_text(json.dumps(self.meta),encoding='utf-8')
        self.assertEqual(self.run_cli(['--recover-id',identifier]),2)
    def test_recovery_identity_mismatch_is_refused(self):
        identifier=self.interrupt(2);self.meta['ideaId']=identifier[:-1]+('f' if identifier[-1]!='f' else 'e')
        self.journal.write_text(json.dumps(self.meta),encoding='utf-8')
        self.assertEqual(self.run_cli(['--recover-id',identifier]),2)
    def test_actual_process_exit_after_card_is_recoverable(self):
        code='''import os,sys
from pathlib import Path
ns={'__name__':'private_probe','__file__':sys.argv[1]}
exec(compile(Path(sys.argv[1]).read_text(encoding='utf-8'),sys.argv[1],'exec'),ns)
root=Path(sys.argv[2]);ns.update(ROOT=root,IDEAS=root/'docs/ideas',OUTBOX=root/'docs/ideas/_outbox')
writer=ns['write_new']
def exit_after_card(path,text):
    writer(path,text)
    if path.parent==ns['IDEAS']:os._exit(23)
ns['write_new']=exit_after_card
ns['main'](['--text',sys.argv[3],'--source-ref','synthetic:original/record/1'])
'''
        result=subprocess.run([sys.executable,'-c',code,str(SOURCE),str(self.root),self.text],capture_output=True,timeout=10)
        self.assertEqual(result.returncode,23)
        journals=list((self.root/'docs/ideas/_outbox/_pending').glob('*.json'))
        self.assertEqual(len(journals),1)
        self.assertEqual(len(list((self.root/'docs/ideas').glob('*.md'))),1)
        self.verify(json.loads(journals[0].read_bytes())['ideaId'])
    def test_failed_atomic_publication_leaves_no_partial_journal(self):
        with mock.patch('os.link',side_effect=OSError('synthetic publication failure')):
            with self.assertRaises(OSError):self.run_cli(['--text',self.text])
        self.assertEqual([p for p in self.root.rglob('*') if p.is_file()],[])

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Recovery))
    print(json.dumps({'tests':result.testsRun,'passed':result.testsRun-len(result.failures)-len(result.errors),'failed':len(result.failures)+len(result.errors)}))
    raise SystemExit(0 if result.wasSuccessful() else 1)
