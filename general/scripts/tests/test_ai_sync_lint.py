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
        for name in ('agnix_update.py', 'agent_lint.py', 'agent_metrics.py'):
            (self.scripts / name).write_text('raise SystemExit(0)\n')
        (self.scripts / 'build_index.py').write_text('print(0)\n')
        (self.scripts / 'ai_sync_message.py').write_text(
            'import sys\nsys.stdin.read()\nprint("Sync fixture")\n')
        (self.root / 'TODO.md').write_text('## Knowledge base\n\n')
        self.index = self.root / '.git' / 'index'
        self.index.parent.mkdir()
        self.index.write_bytes(b'original staging')
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
import os
import sys
from pathlib import Path
args = sys.argv[1:]
with Path('git-calls.txt').open('a') as stream:
    stream.write(' '.join(args) + '\\n')
if args == ['symbolic-ref', '-q', 'HEAD']:
    print(os.environ.get('FIXTURE_BRANCH', 'refs/heads/main'))
if args == ['rev-parse', '--git-path', 'index']:
    print('.git/index')
if args == ['rev-parse', '--verify', 'refs/heads/main']:
    print('b' * 40)
if args == ['add', '-A']:
    Path(os.environ['GIT_INDEX_FILE']).write_bytes(b'new staging')
if args[:3] == ['diff', '--cached', '--quiet']:
    raise SystemExit(1)
if args[:3] == ['diff', '--cached', '--name-only']:
    print('personal/knowledge/example.md')
if args[:3] == ['diff', '--cached', '--name-status']:
    print('A\\tpersonal/knowledge/example.md')
if args[:3] == ['rev-parse', '--show-toplevel']:
    print(Path.cwd())
if args[:3] == ['diff', '--cached', '--raw']:
    oid = 'a' * 40
    sys.stdout.write(f':000000 100644 {"0" * 40} {oid} A\\0personal/knowledge/example.md\\0')
if args[:2] == ['cat-file', 'blob']:
    sys.stdout.buffer.write(Path('personal/knowledge/example.md').read_bytes())
if args[:2] == ['remote', 'get-url']:
    if os.environ.get('FIXTURE_NO_REMOTE'):
        raise SystemExit(2)
    print('https://example.invalid/fixture.git')
if args[:2] == ['push', '-q'] and os.environ.get('FIXTURE_PUSH_FAIL'):
    raise SystemExit(1)
''')
        git.chmod(0o755)
        self.env = dict(os.environ, AI_ROOT=str(self.root),
                        PATH=str(bins) + os.pathsep + os.environ['PATH'],
                        PYTHONDONTWRITEBYTECODE='1')

    def run_sync(self, checker):
        if checker is not None:
            (self.scripts / 'kb_lint.py').write_text(
                'import sys\nif "--commit-message" in sys.argv: raise SystemExit(0)\n' + checker)
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
        self.assertEqual(self.index.read_bytes(), b'original staging')

    def assert_published(self, result, calls):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for action in ('commit', 'pull', 'push'):
            self.assertTrue(any(c.startswith(action + ' ') for c in calls), calls)
        self.assertEqual(self.state.read_text(), date.today().isoformat() + '\n')
        self.assertEqual(self.notes.read_text(), '')
        self.assertEqual(self.index.read_bytes(), b'new staging')
        self.assertIn('push -q origin ' + 'b' * 40 + ':refs/heads/main', calls)

    def test_wrong_branch_stops_before_staging(self):
        self.env['FIXTURE_BRANCH'] = 'refs/heads/other'
        result, calls = self.run_sync(None)
        self.assert_blocked(result, calls)
        self.assertNotIn('add -A', calls)
        self.assertIn('switch to main', result.stdout)

    def test_missing_origin_stops_before_staging(self):
        self.env['FIXTURE_NO_REMOTE'] = '1'
        result, calls = self.run_sync(None)
        self.assert_blocked(result, calls)
        self.assertNotIn('add -A', calls)
        self.assertIn('origin is not configured', result.stdout)

    def test_push_failure_keeps_previous_date(self):
        self.env['FIXTURE_PUSH_FAIL'] = '1'
        result, calls = self.run_sync(
            'print("kb-lint: 0 errors, 0 warnings (staged files only)")\n')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('push (commit is saved locally', result.stdout)
        self.assertEqual(self.state.read_text(), '2000-01-01\n')

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
        self.assert_blocked(result, calls)
        self.assertIn('E secret', result.stderr)
        self.assertEqual(self.state.read_text(), '2000-01-01\n')
        self.assertEqual(self.notes.read_text(), '- fixture: preserve on failure\n')

    def test_real_checker_clean_output_satisfies_gate(self):
        for name in ('kb_find.py', 'kb_paths.py'):
            shutil.copyfile(SCRIPTS / name, self.scripts / name)
        note = self.root / 'personal/knowledge/example.md'
        note.parent.mkdir(parents=True)
        note.write_text('---\nsystem: example\nstatus: verified\nchecked: 2026-11-05\n'
                        '---\n# Example\n')
        shutil.copyfile(SCRIPTS / 'kb_lint.py', self.scripts / 'kb_lint.py')
        result, calls = self.run_sync(None)
        self.assert_published(result, calls)

    def test_real_checker_blob_read_failure_satisfies_failure_gate(self):
        shutil.copyfile(SCRIPTS / 'kb_paths.py', self.scripts / 'kb_paths.py')
        shutil.copyfile(SCRIPTS / 'kb_lint.py', self.scripts / 'kb_lint.py')
        result, calls = self.run_sync(None)
        self.assert_blocked(result, calls)
        self.assertIn('cannot read staged blob', result.stderr)

    def test_secret_in_commit_message_blocks_publication_without_echoing_value(self):
        for name in ('kb_lint.py', 'kb_find.py', 'kb_paths.py', 'ai_sync_message.py'):
            shutil.copyfile(SCRIPTS / name, self.scripts / name)
        note = self.root / 'personal/knowledge/example.md'
        note.parent.mkdir(parents=True)
        note.write_text('---\nsystem: example\nstatus: verified\nchecked: 2026-11-05\n'
                        '---\n# Example\n')
        marker = 'glpat-' + 'a' * 19
        notes = '- fixture: ' + marker + '\n'
        self.notes.write_text(notes)
        result, calls = self.run_sync(None)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('E secret      generated commit message', result.stderr)
        self.assertNotIn(marker, result.stdout + result.stderr)
        self.assertFalse(any(c.split()[0] in ('commit', 'pull', 'push', 'reset')
                             for c in calls), calls)
        self.assertEqual(self.index.read_bytes(), b'original staging')
        self.assertEqual(self.state.read_text(), '2000-01-01\n')
        self.assertEqual(self.notes.read_text(), notes)


if __name__ == '__main__':
    unittest.main()
