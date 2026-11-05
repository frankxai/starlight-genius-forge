import contextlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest
import tempfile
from unittest import mock
from uuid import uuid4

SOURCE = Path(__file__).with_name('idea_swarm_intake.py')

class FrozenDate:
    @classmethod
    def now(cls, tz):
        return datetime(2026, 10, 10, 12, tzinfo=timezone.utc)

class IntakePreservation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='idea-swarm-intake-test-')
        self.root = Path(self.temp.name)
        assert self.root.resolve().is_relative_to(Path(tempfile.gettempdir()).resolve())
        assert self.root.resolve() != Path(tempfile.gettempdir()).resolve()
        self.addCleanup(self.temp.cleanup)
        self.ns = {'__name__': 'private_probe', '__file__': str(SOURCE)}
        exec(compile(SOURCE.read_text(encoding='utf-8'), str(SOURCE), 'exec'), self.ns)
        self.ns.update(ROOT=self.root, IDEAS=self.root / 'docs/ideas', OUTBOX=self.root / 'docs/ideas/_outbox', datetime=FrozenDate)

    def capture(self, text, source='synthetic-probe'):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return self.ns['main'](['--text', text, '--source', source])

    def cards(self):
        return list((self.root / 'docs/ideas').glob('*.md'))

    def test_same_prefix_keeps_both_complete_captures(self):
        prefix = 'A shared synthetic opening sentence for independent inventions ' * 2
        texts = [prefix + '\n' + ('detail ' * 500) + '\nFIRST final meaning', prefix + '\n' + ('detail ' * 500) + '\nSECOND final meaning']
        for text in texts:
            self.assertEqual(self.capture(text), 0)
        self.assertEqual(len(self.cards()), 2)
        contents = [p.read_text(encoding='utf-8') for p in self.cards()]
        for text in texts:
            self.assertTrue(any(text in value for value in contents))

    def test_non_ascii_captures_keep_both(self):
        for text in ['海洋の発明', '教育の発明']:
            self.assertEqual(self.capture(text), 0)
        self.assertEqual(len(self.cards()), 2)

    def test_repeated_text_keeps_each_provenance(self):
        text = 'A repeated synthetic invention with independent source provenance'
        for source in ['original-source-a', 'original-source-b']:
            self.assertEqual(self.capture(text, source), 0)
        self.assertEqual(len(self.cards()), 2)
        metas = [json.loads(p.read_text(encoding='utf-8')) for p in (self.root / 'docs/ideas/_outbox').glob('*.json')]
        self.assertEqual({m['source'] for m in metas}, {'original-source-a', 'original-source-b'})

    def test_forced_identifier_collision_preserves_existing_bytes(self):
        self.ns['uuid4'] = lambda: SimpleNamespace(hex='0' * 32)
        text = 'A synthetic collision probe with one fixed identifier'
        self.assertEqual(self.capture(text, 'first-source'), 0)
        before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(self.capture(text, 'second-source'), 2)
        self.assertEqual({p: p.read_bytes() for p in before}, before)

    def test_existing_outbox_prevents_partial_capture_and_overwrite(self):
        self.ns['uuid4'] = lambda: SimpleNamespace(hex='0' * 32)
        text = 'A synthetic capture with an already occupied outbox'
        self.assertEqual(self.capture(text), 0)
        card = self.cards()[0]
        occupied = next((self.root / 'docs/ideas/_outbox').glob('*.json'))
        before = occupied.read_bytes()
        meta = json.loads(before)
        issue = self.root / meta['issueBodyPath']
        for source, target in [(card, self.root / 'previous-card.md'), (issue, self.root / 'previous-issue.md')]:
            assert source.resolve().is_relative_to(self.root.resolve())
            assert target.resolve().is_relative_to(self.root.resolve())
            source.rename(target)
        self.assertEqual(self.capture(text), 2)
        self.assertEqual(occupied.read_bytes(), before)
        self.assertEqual(self.cards(), [])

    def test_long_capture_retains_raw_text_and_links(self):
        text = 'A long synthetic capture\n' + 'meaningful synthetic detail\n' * 300 + 'FINAL source meaning'
        self.assertEqual(self.capture(text), 0)
        card = self.cards()[0]
        self.assertIn(text, card.read_text(encoding='utf-8'))
        meta = json.loads(next((self.root / 'docs/ideas/_outbox').glob('*.json')).read_text(encoding='utf-8'))
        self.assertEqual((self.root / meta['cardPath']).resolve(), card.resolve())
        self.assertTrue((self.root / meta['issueBodyPath']).exists())

    def test_empty_capture_creates_no_card(self):
        self.assertEqual(self.capture('   \n'), 2)
        self.assertEqual(self.cards(), [])

    def test_file_input_keeps_complete_unicode_meaning(self):
        text = 'Synthetic file capture\n' + '海洋と教育の発明\n' * 400 + 'FINAL complete meaning'
        source = self.root / 'synthetic-input.md'
        source.write_text(text, encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()):
            result = self.ns['main'](['--file', str(source), '--source', 'synthetic-file'])
        self.assertEqual(result, 0)
        self.assertIn(text, self.cards()[0].read_text(encoding='utf-8'))
        self.assertEqual(source.read_text(encoding='utf-8'), text)

    def test_racing_existing_card_is_never_overwritten(self):
        original_open = Path.open
        occupied = None
        def racing(path, mode='r', *args, **kwargs):
            nonlocal occupied
            if mode in ('w', 'x') and occupied is None:
                occupied = path
                with original_open(path, 'w', encoding='utf-8') as stream:
                    stream.write('preserved synthetic competing capture')
            return original_open(path, mode, *args, **kwargs)
        with mock.patch.object(Path, 'open', racing):
            with self.assertRaises(FileExistsError):
                self.capture('Synthetic competing capture probe')
        self.assertIsNotNone(occupied)
        self.assertEqual(occupied.read_text(encoding='utf-8'), 'preserved synthetic competing capture')

    def test_interrupted_outbox_keeps_recoverable_exact_journal(self):
        text = 'Synthetic interrupted capture\n' + 'source meaning\n' * 200
        original_open = Path.open
        writes = 0
        def interrupted(path, mode='r', *args, **kwargs):
            nonlocal writes
            if mode in ('w', 'x'):
                writes += 1
                if writes == 2:
                    raise OSError('synthetic outbox interruption')
            return original_open(path, mode, *args, **kwargs)
        with mock.patch.object(Path, 'open', interrupted):
            with self.assertRaises(OSError):
                self.capture(text)
        self.assertEqual(len(self.cards()), 0)
        journals = list((self.root / "docs/ideas/_outbox/_pending").glob("*.json"))
        self.assertEqual(len(journals), 1)
        meta = json.loads(journals[0].read_bytes())
        self.assertEqual(meta["rawText"], text)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.ns["main"](["--recover-id", meta["ideaId"]]), 0)
        self.assertIn(text, self.cards()[0].read_text(encoding="utf-8"))

    def test_exact_text_metadata_retains_outer_whitespace_and_crlf(self):
        import hashlib
        text = '  Original synthetic wording\r\n\t海洋\r\n\r\n  '
        self.assertEqual(self.capture(text), 0)
        meta = json.loads(next((self.root / 'docs/ideas/_outbox').glob('*.json')).read_bytes())
        self.assertEqual(meta.get('rawText'), text)
        self.assertEqual(meta.get('rawTextSha256'), hashlib.sha256(text.encode('utf-8')).hexdigest())
        self.assertIn(text.encode('utf-8'), self.cards()[0].read_bytes())

    def test_file_bytes_preserve_crlf_and_utf8_bom(self):
        import hashlib
        text = '\ufeff  Original file\r\n海洋\r\n  '
        source = self.root / 'exact-input.txt'
        original = text.encode('utf-8')
        source.write_bytes(original)
        with contextlib.redirect_stdout(io.StringIO()):
            result = self.ns['main'](['--file', str(source), '--source', 'synthetic-file'])
        self.assertEqual(result, 0)
        meta = json.loads(next((self.root / 'docs/ideas/_outbox').glob('*.json')).read_bytes())
        self.assertEqual(meta.get('rawText'), text)
        self.assertEqual(meta.get('rawTextSha256'), hashlib.sha256(original).hexdigest())
        self.assertEqual(source.read_bytes(), original)

    def test_source_locator_is_retained_as_supplied_unverified_data(self):
        locator = 'native-session:synthetic/record/5?kind=founder-draft'
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try:
                result = self.ns['main'](['--text', 'Synthetic original prompt', '--source-ref', locator])
            except SystemExit as e:
                result = e.code
        self.assertEqual(result, 0)
        meta = json.loads(next((self.root / 'docs/ideas/_outbox').glob('*.json')).read_bytes())
        self.assertEqual(meta.get('sourceRef'), locator)
        self.assertNotIn('sourceVerified', meta)

    def test_blank_source_locator_refuses_before_creating_files(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try:
                result = self.ns['main'](['--text', 'Synthetic original prompt', '--source-ref', '   '])
            except SystemExit as e:
                result = e.code
        self.assertEqual(result, 2)
        self.assertEqual(self.cards(), [])

if __name__ == '__main__':
    unittest.main(verbosity=2)
