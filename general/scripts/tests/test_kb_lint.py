"""Language warnings must distinguish prose from verbatim Markdown evidence."""
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest


SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "kb_lint.py"
RUSSIAN = "я" * 61
HEADER = "---\nsystem: example\nstatus: verified\nchecked: 2026-10-20\n---\n"


class LanguageTests(unittest.TestCase):
    def lint(self, body, layer="personal"):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            note = root / layer / "knowledge" / "example.md"
            note.parent.mkdir(parents=True)
            note.write_text(HEADER + body)
            return subprocess.run(
                [sys.executable, str(SCRIPT)], capture_output=True, text=True,
                env={**os.environ, "AI_ROOT": str(root)}, check=False,
            )

    def assert_language(self, body, expected):
        result = self.lint(body)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual("W language" in result.stdout, expected, result.stdout)

    def test_inline_evidence_does_not_warn(self):
        self.assert_language("Click `" + RUSSIAN + "` to continue.", False)

    def test_fenced_evidence_does_not_warn(self):
        self.assert_language("Example:\n```text\n" + RUSSIAN + "\n```\n", False)

    def test_russian_prose_still_warns_next_to_code(self):
        self.assert_language("`exact label` " + RUSSIAN, True)

    def test_multibacktick_span_can_contain_backticks(self):
        self.assert_language("Value: ``" + RUSSIAN + " ` literal``.", False)

    def test_multiline_code_span(self):
        self.assert_language("Value: `source\n" + RUSSIAN + "`.", False)

    def test_unmatched_delimiters_do_not_hide_prose(self):
        for body in ("`" + RUSSIAN, "``" + RUSSIAN + "`", RUSSIAN + "`"):
            with self.subTest(body=body):
                self.assert_language(body, True)

    def test_escaped_opening_is_prose(self):
        self.assert_language("\\`" + RUSSIAN + "`", True)

    def test_escaped_backslash_allows_code_span(self):
        self.assert_language("\\\\`" + RUSSIAN + "`", False)

    def test_threshold_is_unchanged(self):
        self.assert_language("я" * 60, False)
        self.assert_language("я" * 61, True)

    def test_secret_detection_still_checks_inline_code(self):
        result = self.lint("`glpat-" + "A" * 20 + "`")
        self.assertEqual(result.returncode, 1)
        self.assertIn("E secret", result.stdout)

    def test_leak_detection_still_checks_inline_code(self):
        result = self.lint("`service.corp`", layer="general")
        self.assertEqual(result.returncode, 1)
        self.assertIn("E leak", result.stdout)


if __name__ == "__main__":
    unittest.main()
