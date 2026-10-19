"""Synthetic inputs only; transcript JavaScript must never be evaluated."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'token_usage_kb.py'
spec = importlib.util.spec_from_file_location('token_usage_kb', SCRIPT)
kb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kb)


class ShellClassificationTests(unittest.TestCase):
    def classify(self, command):
        return kb.classify_command(command, '/tmp', '/example/ai', home='/example')

    def test_multifile_cd_partial_and_index(self):
        result = self.classify('cd ~/ai/current; cat knowledge/log/a.md knowledge/log/b.md; '
                               'cat knowledge/log/c.md | head -5; sed -n "1,5p" knowledge/log/d.md; '
                               'cat knowledge/INDEX.md')
        self.assertEqual([kind for kind, _ in result], ['full', 'full', 'partial', 'partial', 'index'])
        self.assertEqual(result[0][1], '/example/ai/current/knowledge/log/a.md')

    def test_nonreads_and_heredoc(self):
        self.assertEqual(self.classify('echo "cat ~/ai/current/knowledge/log/a.md"; '
                                      '# cat ~/ai/current/knowledge/log/b.md\n'
                                      'python3 - <<\'PY\'\nprint("cat ~/ai/current/knowledge/log/c.md")\nPY\n'
                                      'cat > ~/ai/current/knowledge/log/write.md <<\'EOF\'\n'
                                      'cat ~/ai/current/knowledge/log/fake.md\nEOF'), [])

    def test_newline_after_comment_preserves_reader(self):
        self.assertEqual([kind for kind, _ in self.classify(
            '# mention only\ncat ~/ai/current/knowledge/log/a.md')], ['full'])

    def test_search_and_wrapper(self):
        result = self.classify('env KEY=value python3 ~/ai/general/scripts/kb_find.py nomad; '
                               'rg foo ~/ai/current/knowledge; '
                               'bash -c "head -5 ~/ai/current/knowledge/log/a.md"')
        self.assertEqual([kind for kind, _ in result], ['kb_find', 'search', 'partial'])

    def test_dynamic_paths_and_writes_not_reads(self):
        self.assertEqual(self.classify('cat "$UNKNOWN/knowledge/log/a.md"; '
                                      'cat ~/ai/current/knowledge/log/*.md; '
                                      'cat ~/ai/current/knowledge/log/a.md > /tmp/copy'), [])

    def test_parse_status(self):
        self.assertTrue(kb.classification_status('echo done'))
        self.assertFalse(kb.classification_status('cat "unterminated'))
        self.assertEqual(self.classify('cat "unterminated'), [])


class StaticExtractionTests(unittest.TestCase):
    def extract(self, source):
        result = kb.extract_shell_calls([source])[0]
        if result['unavailable']:
            self.skipTest('Node and Acorn required for extractor tests')
        return result

    def test_static_literals_templates_spreads_and_batch(self):
        source = ('const root="/example/ai"; const options={workdir:"/tmp"}; '
                  'await Promise.all([tools.exec_command({...options,cmd:`cat ${root}/current/knowledge/log/a.md`}),'
                  'tools.exec_command({cmd:"head -5 " + root + "/general/knowledge/a.md"})]); '
                  '// tools.exec_command({cmd:"false"})')
        result = self.extract(source)
        self.assertEqual(result['exec_nodes'], 2)
        self.assertEqual(result['unresolved'], 0)
        self.assertEqual(result['calls'][0], {'cmd': 'cat /example/ai/current/knowledge/log/a.md', 'workdir': '/tmp'})
        self.assertEqual(len(kb.extract_shell_calls([source, source])), 2)

    def test_dynamic_invalid_and_shadowed_sources(self):
        result = self.extract('let cmd="cat /example/ai/current/knowledge/a.md"; cmd=build(); '
                              'tools.exec_command({cmd}); tools.exec_command({cmd: dynamic()});')
        self.assertEqual(result['unresolved'], 2)
        self.assertEqual(result['calls'], [])
        self.assertEqual(self.extract('const broken = ;')['parse_error'], 1)
        self.assertEqual(self.extract('const cmd="echo outer"; function f(cmd) {tools.exec_command({cmd});}')['unresolved'], 1)

    def test_unknown_spread_is_unresolved(self):
        self.assertEqual(self.extract('tools.exec_command({cmd:"echo safe", ...unknown})')['unresolved'], 1)

    def test_dynamic_workdir_is_unresolved(self):
        self.assertEqual(self.extract('tools.exec_command({cmd:"cat relative.md", workdir:getcwd()})')['unresolved'], 1)

    def test_source_is_never_executed(self):
        result = self.extract('throw new Error("must not execute"); '
                              'tools.exec_command({cmd:"echo literal"});')
        self.assertEqual(result['calls'], [{'cmd': 'echo literal'}])

    def test_missing_node_and_acorn_explicit(self):
        result = kb.extract_shell_calls(['source'], node='/nonexistent-node')[0]
        self.assertEqual(result['unavailable'], 1)
        with patch.object(kb.subprocess, 'run', side_effect=kb.subprocess.CalledProcessError(1, 'node')):
            result = kb.extract_shell_calls(['one', 'two'])
        self.assertEqual([row['unavailable'] for row in result], [1, 1])


if __name__ == '__main__':
    unittest.main()
