"""Exercise the normal sync lint gate with local fixtures and a fake Git executable."""
from datetime import date
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1]


class SyncLintTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='sync-lint-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.scripts = self.root / 'general/scripts'
        self.scripts.mkdir(parents=True)
        for name in ('agnix_update.py', 'agent_lint.py'):
            (self.scripts / name).write_text('raise SystemExit(0)\n')
        (self.scripts / 'build_index.py').write_text('print(0)\n')
        (self.scripts / 'ai_sync_message.py').write_text(
            'import sys\nsys.stdin.read()\nprint("Sync fixture")\n')
        (self.root / 'TODO.md').write_text('## Knowledge base\n\n')
        self.notes = self.root / '.sync-notes'
        self.notes.write_text('- fixture: preserve on failure\n')
        self.state = self.root / '.last-sync'
        self.state.write_text('2000-01-01\n')
        usage = self.root / 'personal/usage'
        usage.mkdir(parents=True)
        (usage / (date.today().isoformat() + '.txt')).write_text('fixture\n')
        bins = self.root / 'bin'
        bins.mkdir()
        git = bins / 'git'
        git.write_text('''#!/usr/bin/env python3
import sys
from pathlib import Path
args = sys.argv[1:]
with Path('git-calls.txt').open('a') as stream:
    stream.write(' '.join(args) + '\\n')
if args[:3] == ['diff', '--cached', '--quiet']:
    raise SystemExit(1)
if args[:3] == ['diff', '--cached', '--name-only']:
    print('personal/knowledge/example.md')
if args[:3] == ['diff', '--cached', '--name-status']:
    print('A\\tpersonal/knowledge/example.md')
if args[:2] == ['remote', 'get-url']:
    print('https://example.invalid/fixture.git')
''')
        git.chmod(0o755)
        self.env = dict(os.environ, AI_ROOT=str(self.root),
                        PATH=str(bins) + os.pathsep + os.environ['PATH'],
                        PYTHONDONTWRITEBYTECODE='1')

    def run_sync(self, checker):
        if checker is not None:
            (self.scripts / 'kb_lint.py').write_text(checker)
        result = subprocess.run(['bash', str(SCRIPTS / 'ai-sync.sh')],
                                cwd=str(self.root), env=self.env,
                                text=True, capture_output=True, timeout=15)
        calls = (self.root / 'git-calls.txt').read_text().splitlines()
        return result, calls

    def assert_blocked(self, result, calls):
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(any(c.split()[0] in ('commit', 'pull', 'push', 'reset')
                             for c in calls), calls)
        self.assertEqual(self.state.read_text(), '2000-01-01\n')
        self.assertEqual(self.notes.read_text(), '- fixture: preserve on failure\n')

    def assert_published(self, result, calls):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for action in ('commit', 'pull', 'push'):
            self.assertTrue(any(c.startswith(action + ' ') for c in calls), calls)
        self.assertEqual(self.state.read_text(), date.today().isoformat() + '\n')
        self.assertEqual(self.notes.read_text(), '')

    def test_checker_exception_stops_publication_and_exposes_diagnostic(self):
        result, calls = self.run_sync('raise RuntimeError("checker fixture failure")\n')
        self.assert_blocked(result, calls)
        self.assertIn('checker fixture failure', result.stderr)
        self.assertIn('kb_lint.py did not complete', result.stdout)

    def test_success_without_completion_summary_stops_publication(self):
        result, calls = self.run_sync('print("partial checker output")\n')
        self.assert_blocked(result, calls)
        self.assertIn('partial checker output', result.stderr)

    def test_missing_checker_stops_publication(self):
        result, calls = self.run_sync(None)
        self.assert_blocked(result, calls)
        self.assertIn('kb_lint.py', result.stderr)

    def test_completed_summary_cannot_hide_abnormal_exit(self):
        result, calls = self.run_sync(
            'print("kb-lint: 0 errors, 0 warnings (staged files only)")\n'
            'raise SystemExit(2)\n')
        self.assert_blocked(result, calls)

    def test_error_summary_requires_findings_exit_status(self):
        result, calls = self.run_sync(
            'print("E link        example.md: target not found")\n'
            'print("kb-lint: 1 errors, 0 warnings (staged files only)")\n')
        self.assert_blocked(result, calls)

    def test_clean_summary_cannot_hide_findings_exit_status(self):
        result, calls = self.run_sync(
            'print("kb-lint: 0 errors, 0 warnings (staged files only)")\n'
            'raise SystemExit(1)\n')
        self.assert_blocked(result, calls)

    def test_post_summary_crash_stops_publication(self):
        result, calls = self.run_sync(
            'print("kb-lint: 0 errors, 0 warnings (staged files only)", flush=True)\n'
            'raise RuntimeError("failure after output")\n')
        self.assert_blocked(result, calls)

    def test_completed_nonsecret_errors_remain_report_only(self):
        result, calls = self.run_sync(
            'print("E link        example.md: target not found")\n'
            'print("kb-lint: 1 errors, 0 warnings (staged files only)")\n'
            'raise SystemExit(1)\n')
        self.assert_published(result, calls)
        self.assertIn('lint findings to fix (commit proceeds)', result.stdout)

    def test_completed_warnings_remain_report_only(self):
        result, calls = self.run_sync(
            'print("W summary     example.md: missing summary")\n'
            'print("kb-lint: 0 errors, 1 warnings (staged files only)")\n')
        self.assert_published(result, calls)
        self.assertIn('W summary', result.stdout)

    def test_clean_completed_check_allows_publication(self):
        result, calls = self.run_sync(
            'print("kb-lint: 0 errors, 0 warnings (staged files only)")\n')
        self.assert_published(result, calls)

    def test_reported_secret_still_blocks_publication(self):
        result, calls = self.run_sync(
            'print("E secret      example.md: simulated credential")\n'
            'print("kb-lint: 1 errors, 0 warnings (staged files only)")\n'
            'raise SystemExit(1)\n')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(any(c.split()[0] in ('commit', 'pull', 'push') for c in calls))
        self.assertIn('E secret', result.stderr)
        self.assertEqual(self.state.read_text(), '2000-01-01\n')
        self.assertEqual(self.notes.read_text(), '- fixture: preserve on failure\n')

    def test_real_checker_clean_output_satisfies_gate(self):
        for name in ('kb_find.py',):
            shutil.copyfile(SCRIPTS / name, self.scripts / name)
        note = self.root / 'personal/knowledge/example.md'
        note.parent.mkdir(parents=True)
        note.write_text('---\nsystem: example\nstatus: verified\nchecked: 2026-11-05\n'
                        '---\n# Example\n')
        result, calls = self.run_sync((SCRIPTS / 'kb_lint.py').read_text())
        self.assert_published(result, calls)


if __name__ == '__main__':
    unittest.main()
