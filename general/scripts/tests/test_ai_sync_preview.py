"""Regression tests for a genuinely read-only ai-sync dry run."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from datetime import date

SCRIPTS = Path(__file__).resolve().parents[1]


class SyncPreviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='sync-preview-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.env = dict(os.environ, AI_ROOT=str(self.root), PYTHONDONTWRITEBYTECODE='1')
        # Do not let an enclosing Git environment affect fixture repositories.
        for key in ('GIT_INDEX_FILE', 'GIT_DIR', 'GIT_WORK_TREE', 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES'):
            self.env.pop(key, None)
        self.git('init', '-q')
        scripts = self.root / 'general/scripts'
        scripts.mkdir(parents=True)
        for name in ('ai_sync_preview.py', 'build_index.py'):
            shutil.copyfile(str(SCRIPTS / name), str(scripts / name))
        self.notes = self.root / 'personal/knowledge'
        self.notes.mkdir(parents=True)
        self.note = self.notes / 'example.md'
        self.note.write_text('---\nsystem: example\nstatus: verified\nchecked: 2026-10-19\n---\n# Example\n')
        (self.notes / 'INDEX.md').write_text('stale index\n')
        (self.root / '.gitignore').write_text('.sync-notes\n.last-sync\n__pycache__/\n*.py[cod]\n')
        self.mixed = self.root / 'mixed.txt'
        self.mixed.write_text('original\n')
        self.git('add', '-A')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'initial')
        self.mixed.write_text('staged change\n')
        self.git('add', 'mixed.txt')
        self.mixed.write_text('working change\n')
        (self.root / '.sync-notes').write_text('- example: preserved\n')
        (self.root / '.last-sync').write_text(date.today().isoformat() + '\n')

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=str(self.root), env=self.env)

    def snapshot(self):
        state = {}
        for path in self.root.rglob('*'):
            key = str(path.relative_to(self.root))
            if path.is_symlink():
                state[key] = ('link', os.readlink(str(path)))
            elif path.is_file():
                state[key] = (path.stat().st_mtime_ns, hashlib.sha256(path.read_bytes()).hexdigest())
        return state

    def dry_run(self):
        return subprocess.run(['bash', str(SCRIPTS / 'ai-sync.sh'), '--dry-run'],
                              cwd=str(self.root), env=self.env, text=True, capture_output=True)

    def test_dry_run_preserves_worktree_index_objects_and_state(self):
        before = self.snapshot()
        result = self.dry_run()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('personal/knowledge/INDEX.md', result.stdout)
        self.assertIn('mixed.txt', result.stdout)
        self.assertIn('weekly usage reports and monthly TODO updates are not generated', result.stdout)
        after = self.snapshot()
        self.assertEqual([], [key for key in before.keys() | after.keys() if before.get(key) != after.get(key)])
        self.assertEqual(self.git('show', ':mixed.txt'), b'staged change\n')
        self.assertEqual(self.mixed.read_text(), 'working change\n')

    def test_untracked_note_index_and_cache_ignore(self):
        (self.notes / 'new.md').write_text('---\nsystem: example\nstatus: verified\nchecked: 2026-10-19\n---\n# New\n')
        cache = self.root / 'general/scripts/__pycache__'
        cache.mkdir()
        (cache / 'generated.pyc').write_bytes(b'generated')
        before = self.snapshot()
        result = self.dry_run()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('personal/knowledge/new.md', result.stdout)
        self.assertNotIn('generated.pyc', result.stdout)
        after = self.snapshot()
        self.assertEqual([], [key for key in before.keys() | after.keys() if before.get(key) != after.get(key)])

    def test_current_symlink_targets_company_index_without_modifying_it(self):
        knowledge = self.root / 'companies/example/knowledge'
        knowledge.mkdir(parents=True)
        (knowledge / 'INDEX.md').write_text('stale company index\n')
        (self.root / 'current').symlink_to('companies/example')
        before = self.snapshot()
        result = self.dry_run()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('companies/example/knowledge/INDEX.md', result.stdout)
        self.assertNotIn("'current/knowledge/INDEX.md'", result.stdout)
        after = self.snapshot()
        self.assertEqual([], [key for key in before.keys() | after.keys() if before.get(key) != after.get(key)])

    def test_split_index_fails_without_refreshing_shared_index(self):
        self.git('update-index', '--split-index')
        before = self.snapshot()
        result = self.dry_run()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('split Git indexes are not supported', result.stderr)
        after = self.snapshot()
        self.assertEqual([], [key for key in before.keys() | after.keys() if before.get(key) != after.get(key)])

    def test_failure_preserves_existing_staging_and_files(self):
        # A malformed tracked Git index must cause a safe failure, never reset.
        (self.root / '.git/index').write_bytes(b'invalid index')
        before = self.snapshot()
        result = self.dry_run()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('preview failed', result.stderr)
        after = self.snapshot()
        self.assertEqual([], [key for key in before.keys() | after.keys() if before.get(key) != after.get(key)])


if __name__ == '__main__':
    unittest.main()
