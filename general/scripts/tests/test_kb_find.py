import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "kb_find.py"
if not SCRIPT.exists():
    SCRIPT = Path(__file__).with_name("kb_find.py")
spec = importlib.util.spec_from_file_location("kb_find", SCRIPT)
kb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kb)


class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.path = self.root / "general/knowledge/service/note.md"
        self.path.parent.mkdir(parents=True)

    def write(self, body, extra=""):
        self.path.write_text("---\nsystem: service\nstatus: verified\nchecked: 2026-11-04\n" + extra + "---\n# Service\n" + body)

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT)] + list(args), env=dict(os.environ, AI_ROOT=str(self.root)), capture_output=True, text=True)

    def test_context_selects_combined_terms_within_real_section(self):
        self.write("\n## Symptom\nalpha is observed.\n\n## Cause\nBefore.\nalpha and beta fail together.\nAfter.\n\n## Recovery\nDo something else.\n")
        p = self.run_cli("--json", "-n", "3", "alpha", "beta")
        self.assertEqual(p.returncode, 0, p.stderr)
        result = json.loads(p.stdout)["results"][0]
        self.assertEqual(result["section"]["heading"], "Cause")
        self.assertEqual([s["text"] for s in result["snippets"]], ["Before.", "alpha and beta fail together.", "After."])

    def test_fenced_example_does_not_create_a_section_or_anchor(self):
        self.write("\n## Cause\n~~~markdown\n## Fake\nalpha beta\n~~~\nActual answer.\n")
        text = self.path.read_text().splitlines()
        headings = list(kb.markdown_headings(text))
        self.assertNotIn("Fake", [h[2] for h in headings])
        p = self.run_cli("--json", "alpha", "beta")
        self.assertEqual(json.loads(p.stdout)["results"][0]["section"]["heading"], "Cause")

    def test_cause_can_use_one_fewer_symptom_term_without_selecting_title(self):
        self.write("\n## Symptom\nalpha beta occurs.\n\n## Cause\nalpha parser is broken.\n")
        r = json.loads(self.run_cli("--json", "alpha", "beta").stdout)["results"][0]
        self.assertEqual(r["section"]["heading"], "Cause")
        self.assertIn("alpha parser is broken.", [s["text"] for s in r["snippets"]])

    def test_nested_sections_and_budget_do_not_cross_into_sibling(self):
        self.write("\n## Settings\n### Specific fix\nalpha beta\n### Different\nUnrelated content.\n")
        result = json.loads(self.run_cli("--json", "-n", "8", "alpha", "beta").stdout)["results"][0]
        self.assertEqual(result["section"]["heading"], "Settings > Specific fix")
        self.assertNotIn("Unrelated content.", [s["text"] for s in result["snippets"]])
        self.assertLessEqual(len(result["snippets"]), 8)

    def test_scoped_cancellation_is_visible_even_without_term_matches_in_decision(self):
        summary = "Stop this extension; retain the completed results. " + "Important context. " * 10
        fields = "decision_state: cancelled\ndecision_scope: Optional extension only\ndecision_summary: " + summary + "\ndecision_date: 2026-11-04\ndecision_source: #final-decision\n"
        self.write("\n## History\nalpha beta\n\n## Final decision\nThe extension was cancelled.\n", fields)
        p = self.run_cli("alpha", "beta")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn(summary.strip(), p.stdout)
        self.assertLess(p.stdout.index("Current decision"), p.stdout.index("Section:"))
        result = json.loads(self.run_cli("--json", "alpha", "beta").stdout)["results"][0]
        self.assertEqual(result["status"], "verified")
        self.assertEqual(result["decision"]["scope"], "Optional extension only")
        self.assertTrue(result["decision"]["source_line"])

    def test_incomplete_or_broken_decision_fails_rather_than_hiding_warning(self):
        self.write("alpha beta", "decision_state: cancelled\n")
        p = self.run_cli("alpha")
        self.assertEqual(p.returncode, 2)
        self.assertEqual(p.stdout, "")
        self.assertIn("decision requires", p.stderr)
        for ref in ("missing.md#answer", "#missing", "../../../../outside.md#answer"):
            self.write("\n## Answer\nalpha", "decision_state: cancelled\ndecision_scope: Extension\ndecision_summary: Stop.\ndecision_date: 2026-11-04\ndecision_source: " + ref + "\n")
            self.assertEqual(self.run_cli("alpha").returncode, 2, ref)

    def test_decision_rejects_invalid_state_and_impossible_date(self):
        fields = dict(decision_state="cancelled", decision_scope="Extension", decision_summary="Stop.", decision_date="2026-11-04", decision_source="#answer")
        for key, bad in (("decision_state", "historical-guess"), ("decision_date", "2026-02-31")):
            changed = dict(fields, **{key: bad})
            self.write("\n## Answer\nalpha", "".join(k + ": " + v + "\n" for k, v in changed.items()))
            self.assertEqual(self.run_cli("alpha").returncode, 2)

    def test_kb_lint_checks_decision_source_and_scope_fields(self):
        lint = SCRIPT.with_name("kb_lint.py")
        fields = "decision_state: superseded\ndecision_scope: Old launch instruction\ndecision_summary: Use the later decision.\ndecision_date: 2026-11-04\ndecision_source: #decision\n"
        self.write("\n## Decision\nalpha", fields)
        def check():
            return subprocess.run([sys.executable, str(lint)], env=dict(os.environ, AI_ROOT=str(self.root)), capture_output=True, text=True)
        self.assertEqual(check().returncode, 0)
        self.write("\n## Decision\nalpha", fields.replace("#decision", "#missing"))
        self.assertEqual(check().returncode, 1)
        self.assertIn("E decision", check().stdout)

    def test_files_empty_modes_filters_and_literal_matching_remain_compatible(self):
        self.write("\n## Cause\nalpha [beta]\n")
        p = self.run_cli("--files", "-l", "general", "-s", "SERVICE", "[beta]")
        self.assertEqual(p.stdout, "~/ai/general/knowledge/service/note.md\n")
        self.assertEqual(self.run_cli("-l", "personal", "alpha").stdout, "kb-find: 0 notes\n")
        self.assertEqual(self.run_cli("alpha", "missing").returncode, 1)
        self.assertEqual(self.run_cli("--any", "alpha", "missing").returncode, 0)
        self.assertEqual(self.run_cli("--json", "--files", "alpha").returncode, 2)
        self.assertEqual(self.run_cli("-n", "-1", "alpha").returncode, 2)
        self.assertEqual(self.run_cli("--regex", "[").returncode, 2)
        r = json.loads(self.run_cli("--json", "-n", "0", "alpha").stdout)["results"][0]
        self.assertEqual(r["snippets"], [])


if __name__ == "__main__":
    unittest.main()
