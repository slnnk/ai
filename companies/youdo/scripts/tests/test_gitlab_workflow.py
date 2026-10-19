"""Offline regression tests; Git writes are confined to TemporaryDirectory fixtures."""
import argparse
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

SCRIPTS = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


repo_tool = load('gitlab_repo')
mr_tool = load('gitlab_task_mr')


class LocalRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'git/service'
        self.repo.mkdir(parents=True)
        self.env = dict(os.environ, GIT_AUTHOR_NAME='Fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                        GIT_COMMITTER_NAME='Fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid',
                        GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1')
        self.git('init', '-q')
        self.git('checkout', '-qb', 'DevOps-1-change')
        (self.repo / 'task.txt').write_text('base\n')
        (self.repo / 'user.txt').write_text('user base\n')
        self.git('add', 'task.txt', 'user.txt')
        self.git('-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
        self.git('remote', 'add', 'origin', 'git@gitlab.youdo.sg:group/service.git')
        self.git('update-ref', 'refs/remotes/origin/master', 'HEAD')
        self.registry = self.root / 'repos.md'
        self.registry.write_text('| Path | Origin | Purpose | System | Checked |\n')
        self.body = self.root / 'body.txt'
        self.body.write_text('Change.\n\nhttps://example.invalid/task\n')
        self.proposal = self.root / 'proposal.json'
        self.proposal_data = dict(project='group/service', source='DevOps-1-change', target='master',
                                  base_ref='origin/master', task_paths=['task.txt'],
                                  commit_message='change task', title='DevOps-1 Change task',
                                  body_file=str(self.body), checks=['fixture passed'],
                                  ci_effects='ordinary validation only')
        self.proposal.write_text(json.dumps(self.proposal_data))

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.repo), *args], env=self.env,
                              check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout

    def cli(self, phase, *extra):
        return subprocess.run([sys.executable, str(SCRIPTS / 'gitlab_repo.py'), phase,
                               '--project', 'group/service', '--root', str(self.root / 'git'),
                               '--registry', str(self.registry), *map(str, extra)],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=self.env)

    def snapshot(self):
        return repo_tool.proposal_state(self.repo, 'group/service', self.proposal)

    def test_inspect_preserves_staged_unstaged_and_untracked(self):
        (self.repo / 'user.txt').write_text('staged user\n')
        self.git('add', 'user.txt')
        (self.repo / 'task.txt').write_text('local task\n')
        (self.repo / 'new file').write_text('untracked\n')
        before = repo_tool.repo_state(self.repo)
        result = self.cli('inspect')
        self.assertEqual(result.returncode, 0, result.stdout)
        summary = json.loads(result.stdout)
        self.assertEqual(summary['change_count'], 3)
        self.assertEqual({x['status'] for x in summary['changes']}, {'M ', ' M', '??'})
        self.assertEqual(repo_tool.repo_state(self.repo), before)

    def test_catalog_precedes_scan_and_supports_legacy_path(self):
        legacy = self.root / 'legacy'
        self.repo.rename(legacy)
        self.registry.write_text('| `{}` | `https://gitlab.youdo.sg/group/service.git` | x | x | 2026-10-19 |\n'.format(legacy))
        self.assertEqual(repo_tool.locate('group/service', self.root / 'git', self.registry), legacy)

    def test_origin_and_push_mismatch_refused(self):
        with self.assertRaisesRegex(ValueError, 'Origin does not match'):
            repo_tool.verify_repo(self.repo, 'other/service')
        self.git('remote', 'set-url', '--push', 'origin', 'git@gitlab.youdo.sg:other/service.git')
        with self.assertRaisesRegex(ValueError, 'push URL'):
            repo_tool.verify_repo(self.repo, 'group/service')

    def test_all_push_urls_checked(self):
        self.git('remote', 'set-url', '--add', '--push', 'origin', 'git@gitlab.youdo.sg:group/service.git')
        self.git('remote', 'set-url', '--add', '--push', 'origin', 'git@gitlab.youdo.sg:other/service.git')
        with self.assertRaisesRegex(ValueError, 'push URL'):
            repo_tool.verify_repo(self.repo, 'group/service')

    def test_catalog_registration_stays_inside_table(self):
        self.registry.write_text('| Path | Origin | Purpose | System | Checked |\n'
                                 '| --- | --- | --- | --- | --- |\n\n## Relationships\nKeep this prose.\n')
        repo_tool.register(self.registry, self.repo, 'group/service', 'Fixture source', 'gitlab-ci')
        text = self.registry.read_text()
        self.assertLess(text.index('group/service'), text.index('## Relationships'))
        self.assertTrue(text.endswith('Keep this prose.\n'))
        self.assertEqual(list(repo_tool.registry_rows(self.registry)),
                         [(self.repo, 'git@gitlab.youdo.sg:group/service.git')])

    def test_missing_checkout_and_clone_collision_never_network(self):
        self.git('remote', 'set-url', 'origin', 'git@gitlab.youdo.sg:other/service.git')
        result = self.cli('inspect')
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)['found'])
        result = self.cli('clone')
        self.assertEqual(result.returncode, 2)
        self.assertIn(b'destination occupied', result.stdout)
        self.assertTrue((self.repo / 'task.txt').exists())

    def test_duplicate_checkouts_require_explicit_selection(self):
        import shutil
        shutil.copytree(self.repo, self.root / 'git/another')
        result = self.cli('inspect')
        self.assertEqual(result.returncode, 2)
        self.assertIn(b'Multiple matching', result.stdout)

    def test_snapshot_binds_tracked_staged_untracked_body_and_proposal(self):
        (self.repo / 'new').write_text('one')
        initial = self.snapshot()
        (self.repo / 'new').write_text('two')
        self.assertNotEqual(initial, self.snapshot())
        (self.repo / 'new').write_text('one')
        (self.repo / 'task.txt').write_text('changed\n')
        self.assertNotEqual(initial, self.snapshot())
        self.git('add', 'task.txt')
        staged = self.snapshot()
        self.assertNotEqual(staged['state']['staged_diff_hash'], initial['state']['staged_diff_hash'])
        self.body.write_text('different body')
        self.assertNotEqual(staged, self.snapshot())
        before = self.snapshot()
        self.proposal_data['ci_effects'] = 'automatic deployment'
        self.proposal.write_text(json.dumps(self.proposal_data))
        self.assertNotEqual(before, self.snapshot())

    def test_snapshot_cli_detects_target_change_and_never_overwrites(self):
        record = self.root / 'record.json'
        flags = ('--record', record, '--proposal-file', self.proposal)
        self.assertEqual(self.cli('snapshot', *flags).returncode, 0)
        self.assertEqual(self.cli('check', *flags).returncode, 0)
        self.assertEqual(self.cli('snapshot', *flags).returncode, 2)
        (self.repo / 'task.txt').write_text('new commit\n')
        self.git('add', 'task.txt')
        self.git('-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture second')
        self.git('update-ref', 'refs/remotes/origin/master', 'HEAD')
        self.assertEqual(self.cli('check', *flags).returncode, 2)
        self.assertFalse(json.loads(self.cli('snapshot', '--record', self.root / 'second.json',
                                            '--proposal-file', self.proposal).stdout)['grants_approval'])

    def test_credential_url_is_not_reported(self):
        self.git('remote', 'set-url', 'origin', 'https://fixture:DO_NOT_PRINT@gitlab.youdo.sg/group/service.git')
        result = self.cli('inspect')
        self.assertEqual(result.returncode, 0)
        self.assertNotIn(b'DO_NOT_PRINT', result.stdout + result.stderr)

    def test_dirty_submodule_snapshot_refused(self):
        import shutil
        source = self.root / 'submodule-source'
        shutil.copytree(self.repo, source)
        self.git('-c', 'protocol.file.allow=always', 'submodule', 'add', str(source), 'module')
        self.git('-c', 'commit.gpgsign=false', 'commit', '-qam', 'fixture submodule')
        self.snapshot()
        (self.repo / 'module/task.txt').write_text('dirty submodule\n')
        with self.assertRaisesRegex(ValueError, 'Dirty submodule'):
            self.snapshot()


class FakeGitLab:
    def __init__(self):
        self.calls = []
        self.mr = None
        self.sha = 'a' * 40
        self.pipeline_error = False
        self.post_timeout = False
        self.put_timeout = False
        self.corrupt_body = False

    def __call__(self, path, method='GET', payload=None, **params):
        self.calls.append((path, method, copy.deepcopy(payload)))
        if path == 'projects/group%2Fservice':
            return dict(id=1, default_branch='master', squash_option='default_on',
                        remove_source_branch_after_merge=False)
        if path == 'user':
            return dict(id=7, username='fixture')
        if path.endswith('/repository/branches/DevOps-1-change'):
            return {'commit': {'id': self.sha}}
        if path.endswith('/merge_requests'):
            if method == 'POST':
                self.mr = dict(iid=4, web_url='https://example.invalid/mr/4', sha=self.sha,
                               source_project_id=1, target_project_id=1,
                               source_branch=payload['source_branch'], target_branch=payload['target_branch'],
                               title=payload['title'], description=payload['description'],
                               squash=payload['squash'], force_remove_source_branch=False,
                               should_remove_source_branch=True, assignees=[{'username': 'fixture'}], draft=False)
                if self.corrupt_body:
                    self.mr['description'] = 'wrong'
                if self.post_timeout:
                    raise URLError('fixture timeout')
                return copy.deepcopy(self.mr)
            return [copy.deepcopy(self.mr)] if self.mr else []
        if path.endswith('/merge_requests/4'):
            if method == 'PUT':
                self.mr.update(payload)
                if self.put_timeout:
                    raise URLError('fixture timeout')
            return copy.deepcopy(self.mr)
        if path.endswith('/pipelines'):
            if self.pipeline_error:
                raise HTTPError('https://example.invalid', 403, 'fixture', {}, None)
            return [{'id': 3, 'status': 'failed', 'web_url': 'https://example.invalid/pipeline/3'}]
        raise AssertionError((path, method, params))


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.body = Path(self.temp.name) / 'body'
        self.body.write_text('Reviewed body\n')
        self.api = FakeGitLab()
        self.args = argparse.Namespace(phase='publish', project='group/service', branch='DevOps-1-change',
                                       target='master', title='DevOps-1 Change', body_file=self.body,
                                       expected_sha=self.api.sha, iid=None, draft=False)

    def run_phase(self):
        return mr_tool.run(self.args, self.api)

    def writes(self):
        return [x for x in self.api.calls if x[1] != 'GET']

    def test_pipeline_403_keeps_verified_created_mr(self):
        self.api.pipeline_error = True
        result, code = self.run_phase()
        self.assertEqual(code, 0)
        self.assertTrue(result['verified'])
        self.assertEqual(result['write_state'], 'created')
        self.assertEqual(result['pipeline_verification'], 'unavailable')
        self.assertEqual(result['iid'], 4)
        self.assertFalse(result['remove_source_branch'])
        self.assertEqual(len(self.writes()), 1)

    def test_create_timeout_reconciles_without_duplicate_write(self):
        self.api.post_timeout = True
        result, code = self.run_phase()
        self.assertEqual(code, 0)
        self.assertEqual(result['write_state'], 'found_after_uncertain_creation')
        self.assertEqual(len(self.writes()), 1)

    def test_create_timeout_without_reconciled_mr_never_repeats_write(self):
        actual = self.api

        def api(path, method='GET', payload=None, **params):
            if method == 'POST':
                actual.calls.append((path, method, payload))
                raise URLError('fixture timeout before response')
            return actual(path, method=method, payload=payload, **params)

        result, code = mr_tool.run(self.args, api)
        self.assertEqual(code, 2)
        self.assertEqual(result['write_state'], 'creation_uncertain')
        self.assertEqual(result['next_action'], 'inspect_read_only_before_any_retry')
        self.assertEqual(len(self.writes()), 1)

    def test_reuse_updates_body_preserves_readiness_and_settings(self):
        self.run_phase()
        self.api.mr['draft'] = True
        self.api.mr['title'] = self.args.title = 'Draft: DevOps-1 Change'
        self.body.write_text('New reviewed body\n')
        self.api.calls.clear()
        self.api.put_timeout = True
        result, code = self.run_phase()
        self.assertEqual(code, 0)
        self.assertTrue(result['draft'])
        self.assertEqual(self.api.mr['description'], 'New reviewed body')
        self.assertEqual([call[1] for call in self.writes()], ['PUT'])
        self.assertEqual(self.writes()[0][2], {'description': 'New reviewed body'})

    def test_title_target_and_sha_mismatch_prevent_write(self):
        self.run_phase()
        for field, value in [('title', 'Other'), ('target_branch', 'develop'), ('sha', 'b' * 40)]:
            with self.subTest(field=field):
                original = self.api.mr[field]
                self.api.mr[field] = value
                self.api.calls.clear()
                with self.assertRaises(ValueError):
                    self.run_phase()
                self.assertEqual(self.writes(), [])
                self.api.mr[field] = original
        self.api.sha = 'c' * 40
        self.api.calls.clear()
        with self.assertRaises(ValueError):
            self.run_phase()
        self.assertEqual(self.writes(), [])

    def test_fork_mr_never_updated_or_reused(self):
        self.run_phase()
        self.api.mr['source_project_id'] = 99
        self.body.write_text('Changed body')
        self.api.calls.clear()
        with self.assertRaisesRegex(ValueError, 'another source/target project'):
            self.run_phase()
        self.assertEqual(self.writes(), [])
        self.args.phase = 'update-description'
        self.args.iid = 4
        with self.assertRaisesRegex(ValueError, 'another source/target project'):
            self.run_phase()
        self.assertEqual(self.writes(), [])

    def test_wrong_remote_description_is_failed_verification_after_create(self):
        self.api.corrupt_body = True
        result, code = self.run_phase()
        self.assertEqual(code, 2)
        self.assertEqual(result['write_state'], 'created')
        self.assertEqual(result['iid'], 4)
        self.assertFalse(result['verified'])
        self.assertEqual(len(self.writes()), 1)

    def test_verify_checks_title_body_and_reports_failed_pipeline_without_writes(self):
        self.run_phase()
        self.args.phase = 'verify'
        self.api.calls.clear()
        result, code = self.run_phase()
        self.assertEqual(code, 0)
        self.assertEqual(result['pipelines'][0]['status'], 'failed')
        self.assertEqual(self.writes(), [])
        self.body.write_text('Unapproved difference')
        result, code = self.run_phase()
        self.assertEqual(code, 2)
        self.assertFalse(result['verified'])
        self.assertEqual(self.writes(), [])

    def test_null_description_inspection_and_update(self):
        self.run_phase()
        self.api.mr['description'] = None
        self.args.iid = 4
        self.args.phase = 'inspect'
        result, code = self.run_phase()
        self.assertEqual(code, 0)
        self.assertFalse(result['exact_match'])
        self.args.phase = 'update-description'
        result, code = self.run_phase()
        self.assertEqual(code, 0)
        self.assertTrue(result['description_verified'])


if __name__ == '__main__':
    unittest.main()
