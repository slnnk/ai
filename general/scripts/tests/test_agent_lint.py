"""Behavioral checks for change-aware lint checkpoints and same-day sync integration."""
import datetime
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('agent_lint', SCRIPTS/'agent_lint.py')
LINT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINT)


class AgentLintTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'kb'; self.root.mkdir()
        self.runtime = self.base / 'home'; self.runtime.mkdir()
        self.state = self.base / 'state'
        self.marker = self.base / 'calls'
        self.mode = self.base / 'mode'; self.mode.write_text('ok')
        self.instructions = self.root / 'AGENTS.md'; self.instructions.write_text('# policy\n')
        self.skill = self.root / 'general/skills/example'; self.skill.mkdir(parents=True)
        (self.skill / 'SKILL.md').write_text('---\nname: example\ndescription: fixture\n---\n')
        (self.skill / 'references').mkdir()
        self.resource = self.skill / 'references/stage.md'; self.resource.write_text('Keep approvals.\n')
        self.fakebin = self.base / 'bin'; self.fakebin.mkdir()
        self.agnix = self.fakebin / 'agnix'
        self.agnix.write_text('''#!/usr/bin/env python3
import json, os, pathlib, sys, time
marker=pathlib.Path(os.environ['LINT_TEST_MARKER'])
with marker.open('a') as f: f.write('called\\n')
(marker.parent/'arguments.json').write_text(json.dumps({'argv':sys.argv[1:],'cwd':os.getcwd()}))
mode=pathlib.Path(os.environ['LINT_TEST_MODE']).read_text()
if mode=='timeout': time.sleep(1)
if mode=='mutate': pathlib.Path(os.environ['LINT_TEST_INPUT']).write_text('changed during check')
if mode=='malformed': print('not JSON'); raise SystemExit(0)
level='error' if mode=='error' else 'warning'
print(json.dumps({'version':'fake','files_checked':2,'diagnostics':[{'level':level,'rule':'TEST-001','file':'fixture.md','line':1,'column':1,'message':'TEST_SECRET_DO_NOT_STORE','source':'TEST_SECRET_DO_NOT_STORE'}]}))
raise SystemExit(1 if mode=='error' else 0)
''')
        self.agnix.chmod(0o700)
        self.env = dict(os.environ, HOME=str(self.runtime), AI_ROOT=str(self.root),
                        AI_LINT_STATE_DIR=str(self.state), LINT_TEST_MARKER=str(self.marker),
                        LINT_TEST_MODE=str(self.mode), LINT_TEST_INPUT=str(self.instructions),
                        PATH=str(self.fakebin)+os.pathsep+os.environ['PATH'])

    def run_lint(self, *args):
        return subprocess.run([sys.executable, '-B', str(SCRIPTS/'agent_lint.py'),
                               '--root', str(self.root), '--runtime-home', str(self.runtime),
                               '--state-dir', str(self.state), '--agnix', str(self.agnix), *args],
                              env=self.env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def calls(self):
        return len(self.marker.read_text().splitlines()) if self.marker.exists() else 0

    def test_success_skips_unchanged_and_force_reruns(self):
        self.assertEqual(self.run_lint().returncode, 0)
        checkpoint = (self.state/'success.json').read_bytes()
        self.assertEqual(self.run_lint().stdout, '')
        self.assertEqual(self.calls(), 1)
        self.assertEqual((self.state/'success.json').read_bytes(), checkpoint)
        self.assertEqual(self.run_lint('--force').returncode, 0)
        self.assertEqual(self.calls(), 2)

    def test_resource_changes_and_deletion_invalidate_checkpoint(self):
        self.run_lint()
        self.resource.write_text('Changed approval reference.\n')
        self.assertEqual(self.run_lint().returncode, 0)
        self.resource.unlink()
        self.assertEqual(self.run_lint().returncode, 0)
        self.assertEqual(self.calls(), 3)

    def test_new_instruction_and_deleted_instruction_are_detected(self):
        self.run_lint()
        extra=self.root/'AGENTS.override.md'; extra.write_text('Project policy')
        self.run_lint(); extra.unlink(); self.run_lint()
        self.assertEqual(self.calls(), 3)

    def test_settings_change_invalidates(self):
        config=self.runtime/'.codex/config.toml'; config.parent.mkdir()
        config.write_text('model="fixture"\n'); self.run_lint()
        config.write_text('model="another-fixture"\n'); self.run_lint()
        self.assertEqual(self.calls(), 2)

    def test_linter_binary_change_invalidates(self):
        self.run_lint(); self.agnix.write_text(self.agnix.read_text()+'\n# version update\n')
        self.run_lint(); self.assertEqual(self.calls(), 2)

    def test_error_findings_are_retried_and_not_success(self):
        self.mode.write_text('error')
        self.assertEqual(self.run_lint().returncode, 1)
        self.assertFalse((self.state/'success.json').exists())
        self.assertEqual(self.run_lint().returncode, 1)
        self.assertEqual(self.calls(), 2)

    def test_malformed_and_timeout_keep_previous_checkpoint(self):
        self.run_lint(); checkpoint=(self.state/'success.json').read_bytes()
        self.instructions.write_text('new')
        for mode in ['malformed', 'timeout']:
            self.mode.write_text(mode)
            self.assertEqual(self.run_lint('--timeout', '0.1').returncode, 1)
            self.assertEqual((self.state/'success.json').read_bytes(), checkpoint)
        self.mode.write_text('ok'); self.assertEqual(self.run_lint().returncode, 0)

    def test_missing_executable_is_visible_and_not_success(self):
        self.agnix.unlink(); result=self.run_lint()
        self.assertEqual(result.returncode, 1)
        self.assertIn('missing', result.stdout)
        self.assertFalse((self.state/'success.json').exists())

    def test_inputs_changed_during_scan_are_not_checkpointed(self):
        self.mode.write_text('mutate')
        result=self.run_lint(); self.assertEqual(result.returncode, 1)
        self.assertIn('changed during check',result.stdout)
        self.assertFalse((self.state/'success.json').exists())

    def test_report_omits_source_and_messages(self):
        self.run_lint()
        text=(self.state/'report.json').read_text()
        self.assertNotIn('TEST_SECRET_DO_NOT_STORE', text)
        self.assertNotIn('message',text)
        self.assertEqual(json.loads(text)['counts']['warning'],1)

    def test_service_tier_rechecks_are_reported_without_hiding_invalid_values(self):
        # On Python 3.10 the installed tomli lives in the real user's site-packages.
        # Runtime lint inputs are still isolated through explicit --runtime-home.
        self.env['HOME'] = os.environ['HOME']
        config = self.runtime/'.codex/config.toml'; config.parent.mkdir()
        config.write_text('[profiles.standard]\nservice_tier = "default"\n[profiles.other]\nservice_tier = "bogus"\n')
        payload = {'version': '0.59.0', 'files_checked': 2, 'diagnostics': [
            {'level': 'warning', 'rule': 'CDX-CFG-025', 'file': str(config),
             'line': line, 'column': 1, 'message': 'TEST_SECRET_DO_NOT_STORE'} for line in [2, 4]]}
        self.agnix.write_text('#!/usr/bin/env python3\nimport json\nprint(json.dumps('+repr(payload)+'))\n')
        result = self.run_lint('--force'); self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads((self.state/'report.json').read_text())
        self.assertEqual(report['counts']['warning'], 1)
        self.assertEqual(report['diagnostics'][0]['line'], 4)
        self.assertEqual(report['compatibility_rechecks'], {'CDX-CFG-025': 1})
        self.assertNotIn('TEST_SECRET_DO_NOT_STORE', (self.state/'report.json').read_text())
        config.write_text(config.read_text().replace('bogus', 'priority'))
        result = self.run_lint('--force'); self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads((self.state/'report.json').read_text())
        self.assertEqual(report['counts']['warning'], 0)
        self.assertEqual(report['compatibility_rechecks'], {'CDX-CFG-025': 2})
        self.assertTrue((self.state/'success.json').exists())
        self.assertEqual(self.run_lint().stdout, '')

    def test_explicit_repo_inputs_invalidate(self):
        extra=self.base/'repo'; extra.mkdir()
        file=extra/'AGENTS.md'; file.write_text('foreign checkout policy')
        self.run_lint(str(extra)); file.write_text('updated foreign policy')
        self.run_lint(str(extra)); self.assertEqual(self.calls(), 2)

    def test_linter_config_changes_and_cwd_are_deterministic(self):
        self.run_lint()
        config=self.root/'.agnix.toml'; config.write_text('severity = "warning"')
        self.run_lint(); config.unlink(); self.run_lint()
        self.assertEqual(self.calls(),3)
        recorded=json.loads((self.base/'arguments.json').read_text())
        self.assertEqual(recorded['cwd'],str(self.root))

    def test_runtime_skill_link_rewiring_is_detected(self):
        directory=self.runtime/'.codex/skills'; directory.mkdir(parents=True)
        link=directory/'example'; link.symlink_to(self.skill)
        self.run_lint()
        replacement=self.base/'replacement'; shutil.copytree(self.skill,replacement)
        link.unlink(); link.symlink_to(replacement)
        self.run_lint(); self.assertEqual(self.calls(),2)
        (replacement/'references/stage.md').write_text('Changed runtime reference')
        self.run_lint(); self.assertEqual(self.calls(),3)

    def test_instruction_aliases_keep_tool_specific_filenames(self):
        for directory,name in [('.codex','AGENTS.md'),('.claude','CLAUDE.md')]:
            folder=self.runtime/directory; folder.mkdir()
            (folder/name).symlink_to(self.instructions)
        self.run_lint()
        args=json.loads((self.base/'arguments.json').read_text())['argv']
        self.assertIn(str(self.instructions),args)
        self.assertIn(str(self.runtime/'.claude/CLAUDE.md'),args)
        self.assertNotIn(str(self.runtime/'.codex/AGENTS.md'),args)

    def test_global_claude_local_settings_and_rules_are_watched(self):
        folder=self.runtime/'.claude'; folder.mkdir()
        settings=folder/'settings.local.json'; settings.write_text('{}')
        rules=folder/'rules'; rules.mkdir(); rule=rules/'local.md'; rule.write_text('policy')
        self.run_lint(); settings.write_text('{"fixture":true}'); self.run_lint()
        rule.write_text('updated policy'); self.run_lint(); self.assertEqual(self.calls(),3)

    def test_same_day_sync_lints_changes_without_git(self):
        scripts=self.root/'general/scripts'; scripts.mkdir(parents=True)
        for name in ['agent_lint.py','ai-sync.sh']:
            shutil.copyfile(SCRIPTS/name,scripts/name)
        (self.root/'.last-sync').write_text(datetime.date.today().isoformat()+'\n')
        git=self.fakebin/'git'; git.write_text('#!/bin/sh\necho forbidden-git >> "'+str(self.base/'git-calls')+'"\nexit 99\n'); git.chmod(0o700)
        def sync(*args):
            return subprocess.run(['bash',str(scripts/'ai-sync.sh'),*args],env=self.env,
                                  text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        first=sync(); self.assertEqual(first.returncode,0,first.stderr)
        self.assertIn('agent-lint:',first.stdout); self.assertEqual(self.calls(),1)
        self.assertEqual(sync().stdout,''); self.assertEqual(self.calls(),1)
        self.instructions.write_text('edited after daily sync')
        self.assertEqual(sync().returncode,0); self.assertEqual(self.calls(),2)
        self.mode.write_text('error'); self.instructions.write_text('another edit')
        error=sync(); self.assertEqual(error.returncode,0); self.assertIn('retry',error.stdout)
        checkpoint=(self.state/'success.json').read_bytes()
        for flag in ['--status','--help']:
            self.assertEqual(sync(flag).returncode,0)
            self.assertEqual(self.calls(),3)
            self.assertEqual((self.state/'success.json').read_bytes(),checkpoint)
        self.assertFalse((self.base/'git-calls').exists())


class ServiceTierCompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = self.root/'.codex/config.toml'
        self.config.parent.mkdir()
        self.item = {'rule': 'CDX-CFG-025', 'level': 'warning',
                     'file': '.codex/config.toml', 'line': 1}

    def recheck(self, source, item=None, version='0.59.0'):
        self.config.write_text(source)
        return LINT.stale_service_tier_finding(item or self.item, version, self.root, [self.config])

    def test_schema_examples_are_rechecked_with_toml_quotes_comments_and_profiles(self):
        for value in ['default', 'priority']:
            for quote in ['"', "'"]:
                with self.subTest(value=value, quote=quote):
                    line = 'service_tier = '+quote+value+quote+' # explicit tier\n'
                    self.assertTrue(self.recheck(line))
                    item = dict(self.item, line=2)
                    self.assertTrue(self.recheck('[profiles.standard]\n'+line, item))

    def test_native_values_and_invalid_values_are_not_filtered(self):
        for value in ['fast', 'flex', 'bogus', 'DEFAULT', '', 'priority-extra']:
            with self.subTest(value=value):
                self.assertFalse(self.recheck('service_tier = "'+value+'"\n'))

    def test_other_rules_versions_and_errors_are_preserved(self):
        source = 'service_tier = "default"\n'
        for item in [dict(self.item, rule='OTHER'), dict(self.item, level='error')]:
            self.assertFalse(self.recheck(source, item))
        for version in ['0.58.0', '0.60.0', None]:
            self.assertFalse(self.recheck(source, version=version))

    def test_malformed_and_multiline_source_are_preserved(self):
        self.assertFalse(self.recheck('service_tier = "default"\nbroken = [\n'))
        source = 'description = \'\'\'\nservice_tier = "default"\n\'\'\'\n'
        self.assertFalse(self.recheck(source, dict(self.item, line=2)))

    def test_diagnostic_must_point_at_actual_input_and_matching_line(self):
        source = 'model = "fixture"\nservice_tier = "default"\n'
        for line in [0, -1, True, '2', 1, 99]:
            self.assertFalse(self.recheck(source, dict(self.item, line=line)))
        outside = self.root/'other/.codex/config.toml'
        outside.parent.mkdir(parents=True)
        outside.write_text('service_tier = "default"\n')
        self.assertFalse(self.recheck(source, dict(self.item, file=str(outside))))
        self.assertTrue(self.recheck(source, dict(self.item, line=2, file=str(self.config))))

    def test_mixed_profiles_preserve_invalid_warning(self):
        source = '[profiles.standard]\nservice_tier = "default"\n[profiles.other]\nservice_tier = "bogus"\n'
        self.assertTrue(self.recheck(source, dict(self.item, line=2)))
        self.assertFalse(self.recheck(source, dict(self.item, line=4)))


if __name__ == '__main__':
    unittest.main()
