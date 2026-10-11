from pathlib import Path
import importlib.util,json,tempfile,unittest,io,contextlib,sys
root=Path(__file__).parent.resolve()
script=Path(sys.argv.pop(1)) if len(sys.argv)>1 and Path(sys.argv[1]).is_file() else Path(__file__).with_name('idea_swarm_intake.py')
spec=importlib.util.spec_from_file_location('capture_intake',script);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
packet={'version':1,'rawText':'original 🧠\r\n full meaning','tags':'  , preserve,, 中文\r\n ','source':'codex','sourceRef':'task:synthetic'}
class CaptureJsonBoundary(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(dir=root);self.base=Path(self.temp.name).resolve();assert self.base.is_relative_to(root)
  mod.ROOT=self.base;mod.IDEAS=self.base/'docs/ideas';mod.OUTBOX=mod.IDEAS/'_outbox'
 def tearDown(self):self.temp.cleanup()
 def run_main(self,args):
  with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):return mod.main(args)
 def reject_packet(self,key,value,key_text=None):
  text=json.dumps(packet,ensure_ascii=False)[:-1]+','+(key_text or json.dumps(key))+':'+json.dumps(value,ensure_ascii=False)+'}'
  p=self.base/'input.json';p.write_text(text,encoding='utf-8');before=p.read_bytes()
  self.assertEqual(self.run_main(['--packet',str(p)]),2);self.assertFalse(mod.IDEAS.exists());self.assertEqual(p.read_bytes(),before)
 def test_rawText_duplicate(self):self.reject_packet('rawText','discarded original')
 def test_tags_duplicate(self):self.reject_packet('tags','substituted tags')
 def test_source_duplicate(self):self.reject_packet('source','substituted attribution')
 def test_sourceRef_duplicate(self):self.reject_packet('sourceRef','task:substituted')
 def test_version_duplicate(self):self.reject_packet('version',1)
 def test_escaped_duplicate(self):self.reject_packet('rawText','substituted','"\\u0072awText"')
 def test_equal_duplicate(self):self.reject_packet('rawText',packet['rawText'])
 def test_valid_roundtrip_and_recovery(self):
  p=self.base/'input.json';p.write_text(json.dumps(packet,ensure_ascii=False),encoding='utf-8');self.assertEqual(self.run_main(['--packet',str(p)]),0)
  journal=next((mod.OUTBOX/'_pending').glob('*.json'));meta=json.loads(journal.read_bytes());self.assertEqual(meta['rawText'],packet['rawText']);self.assertEqual(meta['rawTags'],packet['tags'])
  outputs={str(p):p.read_bytes() for p in mod.IDEAS.rglob('*') if p.is_file()};self.assertEqual(self.run_main(['--recover-id',meta['ideaId']]),0);self.assertTrue(all(Path(p).read_bytes()==v for p,v in outputs.items()))
 def test_duplicate_recovery_journal_rejected_unchanged(self):
  self.assertEqual(self.run_main(['--text','journal original','--tags','keep']),0)
  journal=next((mod.OUTBOX/'_pending').glob('*.json'));meta=json.loads(journal.read_bytes());text=journal.read_text();journal.write_text(text.rstrip()[:-1]+',"rawText":'+json.dumps(meta['rawText'])+'}',encoding='utf-8')
  before={str(p):p.read_bytes() for p in mod.IDEAS.rglob('*') if p.is_file()};self.assertEqual(self.run_main(['--recover-id',meta['ideaId']]),2);self.assertTrue(all(Path(p).read_bytes()==v for p,v in before.items()))
 def test_nonobject_recovery_journal_rejected(self):
  self.assertEqual(self.run_main(['--text','journal original']),0);journal=next((mod.OUTBOX/'_pending').glob('*.json'));meta=json.loads(journal.read_bytes());journal.write_text('[]',encoding='utf-8');before={str(p):p.read_bytes() for p in mod.IDEAS.rglob('*') if p.is_file()}
  self.assertEqual(self.run_main(['--recover-id',meta['ideaId']]),2);self.assertTrue(all(Path(p).read_bytes()==v for p,v in before.items()))
 def test_literal_keys_in_rawText_survive(self):
  value={**packet,'rawText':'{"rawText":"a", "rawText":"b"}'};p=self.base/'input.json';p.write_text(json.dumps(value),encoding='utf-8');self.assertEqual(self.run_main(['--packet',str(p)]),0);meta=json.loads(next((mod.OUTBOX/'_pending').glob('*.json')).read_bytes());self.assertEqual(meta['rawText'],value['rawText'])
unittest.main(verbosity=2)
