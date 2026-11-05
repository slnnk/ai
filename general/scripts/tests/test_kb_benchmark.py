import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "kb_benchmark.py"
if not SCRIPT.exists():
    SCRIPT = Path(__file__).with_name("kb_benchmark.py")
spec = importlib.util.spec_from_file_location("kb_benchmark", SCRIPT)
bench = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bench)


class BenchmarkTests(unittest.TestCase):
    def test_visible_answer_uses_clipped_text_not_source_line_number(self):
        case = {"expected_path": "general/knowledge/a.md", "answer_anchors": ["the decisive answer"]}
        data = {"results": [{"path": "~/ai/general/knowledge/a.md", "snippets": [{"line": 20, "text": "...clipped other context"}]}]}
        self.assertFalse(bench.evaluate(case, data)["answer_visible"])
        data["results"][0]["snippets"] = [{"line": 99, "text": "The decisive"}, {"line": 100, "text": "answer"}]
        self.assertTrue(bench.evaluate(case, data)["answer_visible"])

    def test_decision_requires_state_scope_summary_and_source(self):
        case = {"expected_path": "general/knowledge/a.md", "answer_anchors": ["answer"],
                "required_decision": {"state": "cancelled", "scope_contains": "extension", "summary_contains": "stop"}}
        result = {"path": "~/ai/general/knowledge/a.md", "snippets": [], "decision": {"state": "cancelled", "scope": "extension", "summary": "Stop", "source": "~/ai/a.md", "source_line": 4}}
        self.assertTrue(bench.evaluate(case, {"results": [result]})["decision_visible"])
        result["decision"]["source_line"] = None
        self.assertFalse(bench.evaluate(case, {"results": [result]})["decision_visible"])

    def test_cli_detects_lost_answer_and_invalid_source_anchor_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            note = root / "general/knowledge/a.md"
            note.parent.mkdir(parents=True)
            note.write_text("---\nsystem: demo\nstatus: verified\nchecked: 2026-11-04\n---\n# Demo\n## Cause\nalpha beta decisive answer\n")
            cases = root / "cases.json"
            suite = {"schema_version": 2, "cases": [{"id": "a", "layer": "general", "expected_path": "general/knowledge/a.md", "queries": {"operational": ["alpha", "beta"]}, "answer_anchors": ["decisive answer"], "require_answer": True}]}
            cases.write_text(json.dumps(suite))
            cmd = [sys.executable, str(SCRIPT), "--cases", str(cases), "--output-dir", str(root / "run"), "--enforce"]
            env = dict(os.environ, AI_ROOT=str(root))
            p = subprocess.run(cmd, env=env, text=True, capture_output=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(subprocess.run(cmd, env=env, capture_output=True).returncode, 2)
            # Moving source lines leaves stable anchors valid.
            note.write_text(note.read_text().replace("# Demo", "\n\n# Demo"))
            cmd[cmd.index(str(root / "run"))] = str(root / "shifted")
            self.assertEqual(subprocess.run(cmd, env=env, capture_output=True).returncode, 0)
            # Visible alternative source text cannot replace the baseline's answer.
            baseline_run = root / "run/results.json"
            suite["cases"][0]["answer_anchors"] = ["alpha beta"]
            cases.write_text(json.dumps(suite))
            changed = list(cmd)
            changed[changed.index(str(root / "shifted"))] = str(root / "changed-anchor")
            self.assertEqual(subprocess.run(changed + ["--baseline", str(baseline_run)], env=env, capture_output=True).returncode, 2)
            suite["cases"][0]["answer_anchors"] = ["decisive answer"]
            cases.write_text(json.dumps(suite))
            # A clipped answer with a zero-line budget must fail enforcement.
            cmd[cmd.index(str(root / "shifted"))] = str(root / "lost")
            self.assertEqual(subprocess.run(cmd + ["--lines", "0"], env=env, capture_output=True).returncode, 1)
            # Renaming the enforced variant must not silently skip the checks.
            suite["cases"][0]["queries"] = {"exact": ["alpha", "beta"]}
            cases.write_text(json.dumps(suite))
            cmd[cmd.index(str(root / "lost"))] = str(root / "wrong-variant")
            self.assertEqual(subprocess.run(cmd, env=env, capture_output=True).returncode, 2)
            # A baseline cannot pass by deleting or renaming conditions.
            suite["cases"][0]["queries"] = {"operational": ["alpha", "beta"]}
            cases.write_text(json.dumps(suite))
            baseline = root / "baseline.json"
            old_rows = json.loads(baseline_run.read_text())
            old_rows[0]["id"] = "removed"
            baseline.write_text(json.dumps(old_rows))
            cmd[cmd.index(str(root / "wrong-variant"))] = str(root / "removed-case")
            self.assertEqual(subprocess.run(cmd + ["--baseline", str(baseline)], env=env, capture_output=True).returncode, 2)
            suite["cases"][0]["answer_anchors"] = ["not present in the source"]
            cases.write_text(json.dumps(suite))
            cmd[cmd.index(str(root / "removed-case"))] = str(root / "invalid")
            self.assertEqual(subprocess.run(cmd, env=env, capture_output=True).returncode, 2)
            for bad in ([""], "decisive answer"):
                suite["cases"][0]["answer_anchors"] = bad
                cases.write_text(json.dumps(suite))
                self.assertEqual(subprocess.run(cmd, env=env, capture_output=True).returncode, 2)
            suite["cases"][0]["answer_anchors"] = ["decisive answer"]
            suite["cases"][0]["queries"] = {"operational": "alpha"}
            cases.write_text(json.dumps(suite))
            self.assertEqual(subprocess.run(cmd, env=env, capture_output=True).returncode, 2)


if __name__ == "__main__":
    unittest.main()
