"""Behavioral checks for durable, scoped correction evidence."""
import concurrent.futures
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'agent_learning.py'
spec = importlib.util.spec_from_file_location('agent_learning', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class LearningTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / 'kb'
        self.target = self.base / 'policy.md'
        self.target.write_text('# Policy\n\nRespect discussion mode.\n')

    def run_cli(self, *args, ok=True):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = m.main(['--root', str(self.root), *args])
        self.assertEqual(code, 0 if ok else 1, err.getvalue())
        return out.getvalue() + err.getvalue()

    def record(self, event='event-1', scope='global', key='discussion', extra=(), kind='explicit'):
        return self.run_cli('record', '--key', key, '--event-id', event, '--scope', scope,
                            '--system', 'agents', '--kind', kind, '--summary', 'Обсуждение',
                            '--expected', 'Ждать разрешения', '--source', 'session:one', *extra)

    def test_dedup_across_agents_and_cyrillic_retrieval(self):
        self.record(extra=['--agent', 'codex'])
        self.record(extra=['--agent', 'claude'])
        self.record('event-2')
        self.assertEqual(len(m.records(self.root)[0][1]['occurrences']), 2)
        self.assertIn('Обсуждение', self.run_cli('query', 'ОБСУЖДЕНИЕ'))
        self.assertIn('recorded', self.run_cli('query', 'ОБСУЖДЕНИЕ'))

    def test_link_is_reference_only_inferred_never_active(self):
        before = self.target.read_bytes()
        self.record(kind='inferred')
        self.run_cli('link-rule', '--key', 'discussion', '--scope', 'global', '--target', str(self.target))
        self.assertEqual(self.target.read_bytes(), before)
        self.assertIn('[linked;', self.run_cli('query'))
        self.assertNotIn('[active;', self.run_cli('query'))
        self.record(key='explicit', extra=['--target', str(self.target)])
        self.assertIn('[active;', self.run_cli('query'))

    def test_repo_and_task_isolation(self):
        repo = self.base / 'repo'
        repo.mkdir()
        self.record(scope='repo', extra=['--repo', str(repo), '--layer', 'current'])
        self.assertNotIn('Обсуждение', self.run_cli('query'))
        self.assertNotIn('Обсуждение', self.run_cli('query', '--repo', str(self.base / 'other')))
        self.assertIn('Обсуждение', self.run_cli('query', '--repo', str(repo)))
        self.record(key='task', kind='task', extra=['--task-id', 'task-42'])
        self.assertNotIn('task [', self.run_cli('query'))
        self.assertIn('task [', self.run_cli('query', '--task-id', 'task-42'))

    def test_dry_run_creates_nothing_and_preserves_mtime(self):
        self.record(extra=['--dry-run'])
        self.assertFalse(self.root.exists())
        self.record()
        before = {str(p): (p.stat().st_mtime_ns, p.read_bytes()) for p in self.root.rglob('*') if p.is_file()}
        self.record('event-2', extra=['--dry-run'])
        self.run_cli('link-rule', '--scope', 'global', '--key', 'discussion', '--target', str(self.target), '--dry-run')
        self.run_cli('query')
        self.run_cli('report')
        self.run_cli('check')
        after = {str(p): (p.stat().st_mtime_ns, p.read_bytes()) for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_corruption_is_error_and_missing_is_explicit(self):
        self.assertIn('missing', self.run_cli('query'))
        self.record()
        path = m.records(self.root)[0][0]
        path.write_text('broken')
        for command in ('query', 'report', 'check'):
            self.assertIn('corrupted store', self.run_cli(command, ok=False))

    def test_evaluation_denominator_and_idempotence(self):
        self.record()
        self.assertIn('unknown', self.run_cli('report'))
        for event, outcome in [('e1', 'pass'), ('e2', 'fail'), ('e3', 'not-applicable'), ('e1', 'pass')]:
            self.run_cli('verify', '--key', 'discussion', '--scope', 'global', '--event-id', event,
                         '--source', 'test:case', '--outcome', outcome, '--rule-loaded', 'yes')
        report = self.run_cli('report')
        self.assertIn('applicable tested: 2', report)
        self.assertIn('success rate: 1/2', report)
        self.run_cli('verify', '--key', 'discussion', '--scope', 'global', '--event-id', 'e1',
                     '--source', 'test:case', '--outcome', 'fail', ok=False)

    def test_secret_and_target_rejection(self):
        for secret in ['Bearer abcdefghijklmnop', 'password=abc123456789', '-----BEGIN PRIVATE KEY-----']:
            self.run_cli('record', '--key', 'bad', '--event-id', 'bad', '--scope', 'global', '--system', 'agents',
                         '--kind', 'explicit', '--summary', secret, '--expected', 'safe', '--source', 'test', '--dry-run', ok=False)
        self.assertFalse(self.root.exists())
        self.record()
        self.run_cli('link-rule', '--key', 'discussion', '--scope', 'global', '--target', str(self.base / 'missing.md'), ok=False)
        other = self.base / 'script.sh'
        other.write_text('exit 1')
        self.run_cli('link-rule', '--key', 'discussion', '--scope', 'global', '--target', str(other), ok=False)
        self.run_cli('link-rule', '--key', 'discussion', '--scope', 'global', '--target', str(self.target))
        self.target.unlink()
        self.run_cli('check', ok=False)

    def test_machine_records_ignore_human_logs(self):
        folder = self.root / 'personal' / 'knowledge' / 'log'
        folder.mkdir(parents=True)
        human = folder / '2026-10-19-agent-learning-shared-correction-workflow.md'
        human.write_text('# Human work log\n')
        self.record()
        self.assertEqual(human.read_text(), '# Human work log\n')
        self.assertEqual(len(m.records(self.root)), 1)
        self.assertIn('valid: 1', self.run_cli('check'))

    def test_same_rule_distinct_task_identity_and_selector(self):
        self.record(kind='task', extra=['--task-id', 'one'])
        self.record(kind='task', extra=['--task-id', 'two'])
        self.assertEqual(len(m.records(self.root)), 2)
        self.run_cli('link-rule', '--key', 'discussion', '--scope', 'global',
                     '--target', str(self.target), ok=False)
        self.run_cli('link-rule', '--key', 'discussion', '--scope', 'global',
                     '--task-id', 'two', '--target', str(self.target))
        two = [d for _, d in m.records(self.root) if d['task_id'] == 'two'][0]
        self.assertEqual(two['target'], str(self.target))
        self.assertNotIn('canonical: ' + str(self.target), self.run_cli('query', '--task-id', 'one'))

    def test_global_rules_survive_current_scope_system_filter(self):
        self.record()
        self.assertIn('Обсуждение', self.run_cli('query', '--scope', 'current', '--system', 'deployment', 'обсуждение'))
        self.assertNotIn('Обсуждение', self.run_cli('query', '--scope', 'current', '--system', 'deployment', 'нет-совпадения'))
        self.assertFalse((self.root / '.agent-learning.lock').exists())

    def test_resolve_adopt_revise_reject_and_revision_evidence(self):
        self.record(kind='inferred')
        self.run_cli('resolve', '--key', 'discussion', '--scope', 'global', '--decision', 'adopted',
                     '--source', 'user:approval', ok=False)
        self.run_cli('resolve', '--key', 'discussion', '--scope', 'global', '--decision', 'adopted',
                     '--source', 'user:approval', '--target', str(self.target), '--expected', 'New expected behavior')
        self.assertIn('[active; inferred;', self.run_cli('query', 'unrelated-keyword'))
        self.assertIn('New expected behavior', self.run_cli('query'))
        self.run_cli('verify', '--key', 'discussion', '--scope', 'global', '--event-id', 'v1', '--source', 'test:one', '--outcome', 'pass')
        self.run_cli('resolve', '--key', 'discussion', '--scope', 'global', '--decision', 'adopted',
                     '--source', 'user:approval2', '--expected', 'Revised behavior')
        self.assertIn('historical evaluations (excluded): 1', self.run_cli('report'))
        self.assertIn('unknown', self.run_cli('report'))
        self.run_cli('resolve', '--key', 'discussion', '--scope', 'global', '--decision', 'rejected', '--source', 'user:reject')
        self.assertNotIn('discussion [', self.run_cli('query'))
        self.assertIn('[rejected;', self.run_cli('query', '--include-history'))

    def test_missing_target_repair(self):
        self.record(extra=['--target', str(self.target)])
        self.target.unlink()
        self.run_cli('query', ok=False)
        replacement = self.base / 'replacement.md'
        replacement.write_text('# New policy')
        self.run_cli('link-rule', '--key', 'discussion', '--scope', 'global', '--target', str(replacement))
        self.assertIn(str(replacement), self.run_cli('query'))

    def test_changed_event_conflict_and_truncation(self):
        self.record()
        self.run_cli('record', '--key', 'discussion', '--event-id', 'event-1', '--scope', 'global',
                     '--system', 'agents', '--kind', 'explicit', '--summary', 'Changed',
                     '--expected', 'Changed', '--source', 'session:one', ok=False)
        self.record(key='another')
        self.assertIn('showing 1 of 2', self.run_cli('query', '--limit', '1'))

    def test_inactive_missing_targets_do_not_poison_store(self):
        for decision in ('rejected', 'superseded'):
            key = 'old-' + decision
            self.target.write_text('# Policy')
            self.record(key=key, extra=['--target', str(self.target)])
            self.target.unlink()
            self.run_cli('query', ok=False)
            self.run_cli('resolve', '--key', key, '--scope', 'global',
                         '--decision', decision, '--source', 'user:decision')
            self.run_cli('check')
            self.run_cli('report')
            self.assertNotIn(key + ' [', self.run_cli('query'))
            self.assertIn('[' + decision + ';', self.run_cli('query', '--include-history'))

    def test_concurrent_writers_no_lost_occurrences(self):
        def record(i):
            return subprocess.run([sys.executable, str(SCRIPT), '--root', str(self.root), 'record',
                '--key', 'parallel', '--event-id', f'event-{i}', '--scope', 'global', '--system', 'agents',
                '--kind', 'explicit', '--summary', 'Parallel correction', '--expected', 'Preserve events',
                '--source', 'session:test'], capture_output=True, text=True)
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(record, list(range(12)) + list(range(6))))
        self.assertTrue(all(r.returncode == 0 for r in results), '\n'.join(r.stderr for r in results))
        self.assertEqual(len(m.records(self.root)), 1)
        self.assertEqual(len(m.records(self.root)[0][1]['occurrences']), 12)


if __name__ == '__main__':
    unittest.main()
