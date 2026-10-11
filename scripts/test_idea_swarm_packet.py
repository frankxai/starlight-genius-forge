import contextlib,hashlib,io,json,sys,tempfile,unittest
from pathlib import Path

SOURCE=Path(__file__).with_name('idea_swarm_intake.py')
FIXTURE=Path(__file__).with_name('synthetic-browser-packet.json')
class Packets(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='idea-packet-proof-')
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.ns={'__name__':'private_packet_probe','__file__':str(SOURCE)}
        exec(compile(SOURCE.read_text(encoding='utf-8'),str(SOURCE),'exec'),self.ns)
        self.ns.update(ROOT=self.root,IDEAS=self.root/'docs/ideas',OUTBOX=self.root/'docs/ideas/_outbox')
        self.packet=json.loads(FIXTURE.read_bytes())
        self.input=self.root/'packet.json'
    def call(self,packet=None,extra=()):
        self.input.write_text(json.dumps(self.packet if packet is None else packet),encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):return self.ns['main'](['--packet',str(self.input),*extra])
    def assert_no_capture(self):self.assertFalse((self.root/'docs').exists())
    def test_actual_browser_blob_import_keeps_full_exact_text_and_tags(self):
        self.input.write_bytes(FIXTURE.read_bytes())
        with contextlib.redirect_stdout(io.StringIO()):self.assertEqual(self.ns['main'](['--packet',str(self.input)]),0)
        meta=json.loads(next((self.root/'docs/ideas/_outbox').glob('*.json')).read_bytes())
        self.assertEqual(meta['rawText'],self.packet['rawText'])
        self.assertEqual(meta['rawTextSha256'],hashlib.sha256(self.packet['rawText'].encode()).hexdigest())
        self.assertEqual(meta['source'],'idea-swarm-cockpit')
        self.assertEqual(meta['tags'],[t.strip() for t in self.packet['tags'].split(',')])
        self.assertIn(self.packet['rawText'].encode(),(self.root/meta['cardPath']).read_bytes())
    def test_unknown_fields_and_boolean_version_denied(self):
        for p in [{**self.packet,'extra':'unexpected'},{**self.packet,'version':True}]:self.assertEqual(self.call(p),2);self.assert_no_capture()
    def test_wrong_text_or_tags_or_locator_types_denied(self):
        for k in ['rawText','tags','source','sourceRef']:
            self.assertEqual(self.call({**self.packet,k:42}),2);self.assert_no_capture()
    def test_conflicting_arguments_denied(self):
        for extra in [('--text','other'),('--file','other'),('--source','other'),('--tags','other'),('--source-ref','other'),('--recover-id','isw-20261010-test-'+'0'*32)]:
            with self.assertRaises(SystemExit) as error:self.call(extra=extra)
            self.assertEqual(error.exception.code,2);self.assert_no_capture()
    def test_malformed_and_non_object_json_denied(self):
        for data in [b'{',b'[]',b'null',b'\xff']:
            self.input.write_bytes(data)
            with contextlib.redirect_stderr(io.StringIO()):self.assertEqual(self.ns['main'](['--packet',str(self.input)]),2)
            self.assert_no_capture()
    def test_blank_text_and_blank_locator_denied(self):
        for p in [{**self.packet,'rawText':' \r\n '},{**self.packet,'sourceRef':' '}]:self.assertEqual(self.call(p),2);self.assert_no_capture()
    def test_unencodable_original_denied_before_any_capture(self):
        self.assertEqual(self.call({**self.packet,'rawText':'\ud800'}),2);self.assert_no_capture()
if __name__=='__main__':unittest.main()
