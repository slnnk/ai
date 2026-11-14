import argparse
import datetime as dt
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import agent_metrics as m


class MetricsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'kb'
        self.data = Path(self.tmp.name) / 'data'
        for layer in ('personal', 'current'):
            (self.root / layer / 'knowledge/log').mkdir(parents=True)
        self.note = self.root / 'personal/knowledge/log/task.md'
        self.note.write_text('# Task\n\nEvidence for the fixture.\n')

    def record(self, **kwargs):
        values = dict(source=str(self.note), task_id='task-one', evidence='task.md#evidence',
                      state=None, first_result=None, final_result=None, kind=None,
                      model=None, session_id=None, **{k: None for k in m.COUNTS})
        values.update(kwargs)
        m.record(self.root, argparse.Namespace(**values))

    def prepare(self):
        with patch.object(m, 'today', return_value=dt.date(2026, 11, 14)), \
             patch.object(m.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, 'usage fixture\n')):
            m.prepare(self.root, self.data)
        return json.loads((self.data / 'pending.json').read_text())

    def review_note(self, pending):
        self.note.write_text('# Review\n\n' + pending['sha256'] + '\n\n## Findings\n\n'
                             + 'No task evidence yet; the empty sample proves no quality result. ' * 4
                             + '\n## Actions\n\nCollect task outcomes.\n\n## Limits\n\nCoverage unknown.\n')

    def test_idempotent_update_is_one_task_and_preserves_first_failure(self):
        self.record(first_result='fail', corrections=2)
        before = self.note.read_text()
        self.record(first_result='fail', corrections=2)
        self.assertEqual(before, self.note.read_text())
        self.record(state='closed', final_result='pass')
        self.assertEqual(len(m.tasks(self.root)), 1)
        self.assertEqual(m.tasks(self.root)['task-one'][1]['first_result'], 'fail')
        with self.assertRaises(m.learning.Invalid):
            self.record(first_result='pass')

    def test_unknown_is_not_pass_and_denominator_is_explicit(self):
        self.record(state='closed')
        report = m.snapshot(self.root, dt.date(2000, 1, 1), dt.date(2100, 1, 1))
        self.assertEqual(report['summary']['first_result'], {'unknown': 1})
        self.assertEqual(report['summary']['counts']['corrections'], dict(total=None, assessed=0, eligible=1))

    def test_interval_excludes_current_day_and_includes_changed_old_tasks(self):
        with patch.object(m, 'stamp', return_value='2026-11-13T15:00:00+03:00'):
            self.record(state='closed', first_result='pass')
        self.assertEqual(m.snapshot(self.root, dt.date(2026, 11, 13), dt.date(2026, 11, 14))['summary']['closed_tasks'], 1)
        self.assertEqual(m.snapshot(self.root, dt.date(2026, 11, 14), dt.date(2026, 11, 15))['summary']['closed_tasks'], 0)

    def test_duplicate_identity_and_corrupt_blocks_are_errors(self):
        self.record()
        other = self.note.with_name('duplicate.md')
        other.write_text(self.note.read_text())
        with self.assertRaises(m.learning.Invalid):
            m.tasks(self.root)
        other.write_text(m.MARKER + '{}')
        with self.assertRaises(m.learning.Invalid):
            m.tasks(self.root)
        other.write_text(m.MARKER + 'null\n```')
        with self.assertRaises(m.learning.Invalid):
            m.tasks(self.root)

    def test_missing_root_does_not_become_empty_success(self):
        (self.root / 'current/knowledge/log').rmdir()
        with self.assertRaises(m.learning.Invalid):
            self.prepare()
        self.assertFalse((self.data / 'state.json').exists())

    def test_prepare_stays_pending_and_reuses_snapshot_without_model_call(self):
        pending = self.prepare()
        path = Path(pending['snapshot'])
        before = path.read_bytes()
        with patch.object(m.subprocess, 'run', side_effect=AssertionError('must not repeat resource collection')):
            m.prepare(self.root, self.data)
        self.assertEqual(before, path.read_bytes())
        self.assertFalse((self.data / 'state.json').exists())

    def test_review_requires_evidence_and_does_not_complete_on_failure(self):
        pending = self.prepare()
        with self.assertRaises(m.learning.Invalid):
            m.complete(self.root, self.data, str(self.note))
        self.assertTrue((self.data / 'pending.json').exists())
        self.review_note(pending)
        with patch.object(m, 'today', return_value=dt.date(2026, 11, 14)):
            m.complete(self.root, self.data, str(self.note))
            with patch.object(m, 'snapshot', side_effect=AssertionError('already reviewed')):
                m.prepare(self.root, self.data)
        self.assertFalse((self.data / 'pending.json').exists())

    def test_changed_snapshot_cannot_be_acknowledged(self):
        pending = self.prepare()
        self.review_note(pending)
        Path(pending['snapshot']).write_text('{}')
        with self.assertRaises(m.learning.Invalid):
            m.complete(self.root, self.data, str(self.note))

    def test_nonconsecutive_days_use_last_review_boundary(self):
        pending = self.prepare()
        self.review_note(pending)
        with patch.object(m, 'today', return_value=dt.date(2026, 11, 14)):
            m.complete(self.root, self.data, str(self.note))
        with patch.object(m, 'today', return_value=dt.date(2026, 11, 18)), \
             patch.object(m.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '')):
            m.prepare(self.root, self.data)
        new = json.loads((self.data / 'pending.json').read_text())
        self.assertEqual(new['start'], '2026-11-14')
        self.assertEqual(new['end_exclusive'], '2026-11-18')

    def test_invalid_values_and_external_sources_do_not_write(self):
        before = self.note.read_bytes()
        with self.assertRaises(m.learning.Invalid):
            self.record(corrections=-1)
        self.assertEqual(before, self.note.read_bytes())
        outside = Path(self.tmp.name) / 'outside.md'
        outside.write_text('# Outside')
        with self.assertRaises(m.learning.Invalid):
            self.record(source=str(outside))
        uncollected = self.root / 'README.md'
        uncollected.write_text('# Not a task log')
        with self.assertRaises(m.learning.Invalid):
            self.record(source=str(uncollected))

    def test_known_result_cannot_be_erased_and_usage_failure_stays_explicit(self):
        self.record(first_result='pass')
        with self.assertRaises(m.learning.Invalid):
            self.record(first_result='unknown')
        with patch.object(m.subprocess, 'run', side_effect=subprocess.TimeoutExpired('usage', 30)):
            m.prepare(self.root, self.data)
        pending = json.loads((self.data / 'pending.json').read_text())
        self.assertIn('unavailable', Path(pending['usage']).read_text())
        self.assertFalse((self.data / 'state.json').exists())

    def test_sync_calls_metrics_even_when_git_already_synced_today(self):
        scripts = self.root / 'general/scripts'
        scripts.mkdir(parents=True)
        for name in ('agnix_update.py', 'agent_lint.py'):
            (scripts / name).write_text('')
        (scripts / 'agent_metrics.py').write_text('print("daily analysis pending fixture")\n')
        (self.root / '.last-sync').write_text(dt.date.today().isoformat())
        import os
        result = subprocess.run(['bash', str(SCRIPTS / 'ai-sync.sh')],
                                env=dict(os.environ, AI_ROOT=str(self.root)), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('daily analysis pending fixture', result.stdout)


if __name__ == '__main__':
    unittest.main()
