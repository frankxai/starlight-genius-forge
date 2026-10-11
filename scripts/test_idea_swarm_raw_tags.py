import contextlib, hashlib, io, json, os, tempfile, unittest
from pathlib import Path

SOURCE = Path(os.environ.get('IDEA_INTAKE_PROBE_SOURCE', str(Path(__file__).with_name('idea_swarm_intake.py'))))

class RawTags(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='idea-exact-tags-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.ns = {'__name__': 'synthetic_tag_probe', '__file__': str(SOURCE)}
        exec(compile(SOURCE.read_text(encoding='utf-8'), str(SOURCE), 'exec'), self.ns)
        self.ns.update(ROOT=self.root, IDEAS=self.root/'docs/ideas', OUTBOX=self.root/'docs/ideas/_outbox')
        self.raw = '  hardware,  Bücher  ,\r\n community,, hardware  '
        packet = self.root/'packet.json'
        packet.write_text(json.dumps({'version':1, 'rawText':'Synthetic authoring device and community concept', 'tags':self.raw, 'source':'synthetic', 'sourceRef':None}), encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.ns['main'](['--packet',str(packet)]), 0)
        self.journal = next((self.root/'docs/ideas/_outbox/_pending').glob('*.json'))
        self.meta = json.loads(self.journal.read_bytes())
        self.final = self.root/'docs/ideas/_outbox'/f"{self.meta['ideaId']}.json"

    def recover(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return self.ns['main'](['--recover-id',self.meta['ideaId']])

    def test_exact_tags_and_hash_in_journal_and_final(self):
        for file in (self.journal, self.final):
            saved = json.loads(file.read_bytes())
            self.assertEqual(saved.get('rawTags'), self.raw)
            self.assertEqual(saved.get('rawTagsSha256'), hashlib.sha256(self.raw.encode()).hexdigest())
            self.assertEqual(saved['tags'], ['hardware','Bücher','community','hardware'])

    def test_recovery_recreates_exact_original_tags(self):
        self.final.unlink()
        self.assertEqual(self.recover(), 0)
        self.assertEqual(json.loads(self.final.read_bytes()).get('rawTags'), self.raw)

    def test_changed_original_tag_hash_is_rejected_before_extension(self):
        self.final.unlink()
        self.meta.update(rawTags=self.raw, rawTagsSha256='0'*64)
        self.journal.write_text(json.dumps(self.meta),encoding='utf-8')
        self.assertEqual(self.recover(),2)
        self.assertFalse(self.final.exists())

    def test_legacy_journal_remains_recoverable_without_invented_raw_tags(self):
        self.final.unlink()
        self.meta.pop('rawTags',None)
        self.meta.pop('rawTagsSha256',None)
        self.journal.write_text(json.dumps(self.meta,indent=2)+'\n',encoding='utf-8')
        self.assertEqual(self.recover(),0)
        self.assertNotIn('rawTags',json.loads(self.final.read_bytes()))

if __name__ == '__main__': unittest.main()
