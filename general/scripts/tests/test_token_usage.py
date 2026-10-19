"""End-to-end regression fixtures for Codex knowledge-base accounting."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import token_usage as usage


class CodexAccountingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.ai = self.root / 'ai'
        self.notes = self.ai / 'personal/knowledge'
        self.notes.mkdir(parents=True)
        self.note = self.notes / 'example.md'
        self.note.write_text('example\n')
        self.sessions = self.root / 'sessions'
        self.sessions.mkdir()
        self.since = datetime(2026, 10, 7, tzinfo=timezone.utc)
        self.patches = [patch.object(usage, 'CODEX', self.sessions),
                        patch.object(usage, 'CLAUDE', self.root / 'claude'),
                        patch.object(usage, 'AI_ROOT', self.ai)]
        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)

    def write_session(self, events, archived=False):
        base = self.root / 'archived_sessions' if archived else self.sessions
        base.mkdir(exist_ok=True)
        path = base / ('archive.jsonl' if archived else 'active.jsonl')
        path.write_text('\n'.join(json.dumps(e) for e in events) + '\n')

    def event(self, payload, date='2026-10-08T12:00:00Z', typ='response_item'):
        return {'timestamp': date, 'type': typ, 'payload': payload}

    def call(self, cmd, cid='call1'):
        return self.event({'type': 'function_call', 'name': 'functions.exec_command',
                           'call_id': cid, 'arguments': json.dumps({'cmd': cmd})})

    def test_direct_calls_decode_json_resolve_cwd_and_deduplicate(self):
        meta = self.event({'cwd': str(self.notes)}, '2026-10-01T00:00:00Z', 'session_meta')
        call = self.call('cat example.md')
        self.write_session([meta, dict(self.call('cat example.md', 'old'), timestamp='2026-10-01T00:00:00Z'), call, call])
        calls = list(usage.codex_tool_calls(self.since))
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][2], {'command': 'cat example.md', 'cwd': str(self.notes)})
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            stats = usage.kb_report(self.since)
        self.assertEqual(stats['codex']['full'], 1)
        self.assertEqual(stats['codex']['full_bytes'], self.note.stat().st_size)
        self.assertIn('1 direct calls', output.getvalue())

    def test_nested_wrapper_reports_distinct_reads_and_ignores_literal_paths(self):
        source = ('await tools.exec_command({cmd: ' + json.dumps('cat ' + str(self.note)) + '});\n'
                  'await tools.exec_command({cmd: ' + json.dumps("sed -n '1,2p' " + str(self.note)) + '});\n'
                  'await tools.exec_command({cmd: ' + json.dumps('echo cat ' + str(self.note)) + '});')
        self.write_session([self.event({'type': 'custom_tool_call', 'name': 'functions.exec', 'input': source})], archived=True)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            stats = usage.kb_report(self.since)
        self.assertEqual(stats['codex']['full'], 1)
        self.assertEqual(stats['codex']['partial'], 1)
        self.assertEqual(stats['codex']['full_bytes'], self.note.stat().st_size)
        self.assertIn('3 static calls', output.getvalue())

    def test_patch_tool_arguments_are_not_read_commands(self):
        self.write_session([self.event({'type': 'custom_tool_call', 'name': 'functions.apply_patch',
                                       'input': 'cat ' + str(self.note)})])
        self.assertEqual(list(usage.codex_tool_calls(self.since)), [])

    def test_unavailable_parser_is_visible_and_direct_calls_survive(self):
        self.write_session([self.call('cat ' + str(self.note)),
                            self.event({'type': 'custom_tool_call', 'name': 'functions.exec', 'input': 'some_js'})])
        result = {'calls': [], 'exec_nodes': 0, 'unresolved': 0, 'parse_error': 0, 'unavailable': 1}
        output = io.StringIO()
        with patch.object(usage, 'extract_shell_calls', return_value=[result]), contextlib.redirect_stdout(output):
            stats = usage.kb_report(self.since)
        self.assertEqual(stats['codex']['full'], 1)
        self.assertIn('1 wrappers unavailable', output.getvalue())
        self.assertIn('coverage is incomplete', output.getvalue())

    def test_claude_read_classification_unchanged(self):
        self.assertEqual(usage.classify('Read', {'file_path': str(self.note)})[0], 'full')
        self.assertEqual(usage.classify('Read', {'file_path': str(self.note), 'limit': 3})[0], 'partial')


if __name__ == '__main__':
    unittest.main()
