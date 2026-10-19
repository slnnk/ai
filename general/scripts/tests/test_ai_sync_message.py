"""Deterministic checks for compact daily sync messages."""
import contextlib
import importlib.util
import io
import pathlib
import tempfile
import unittest
from unittest import mock


SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "ai_sync_message.py"
SPEC = importlib.util.spec_from_file_location("ai_sync_message", SCRIPT)
MESSAGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MESSAGE)


class SyncMessageTests(unittest.TestCase):
    def test_deduplicate_and_group_without_losing_distinct_tasks(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "notes"
            path.write_text(
                "- agent: fixed dry-run; checked staged changes; risk none\n"
                "- vpn: restored access\n"
                "* agent: fixed dry-run; checked staged changes; risk none\n"
                "- agent: compared token usage; new parser remains optional\n"
            )
            groups = MESSAGE.work_groups(path)
        self.assertEqual(list(groups), ["agent", "vpn"])
        self.assertEqual(groups["agent"], [
            "fixed dry-run; checked staged changes; risk none",
            "compared token usage; new parser remains optional",
        ])

    def test_missing_notes_and_unprefixed_records(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "notes"
            self.assertEqual(MESSAGE.work_groups(path), {})
            path.write_text("\n- No prefix\nhttps://example.test/path\n")
            self.assertEqual(MESSAGE.work_groups(path), {
                "Other": ["No prefix", "https://example.test/path"],
            })

    def test_file_summary_bounds_references_and_counts_every_file(self):
        files = [("M", "note{}.md".format(n), "Title {}".format(n))
                 for n in range(12)]
        files += [("A", "helper.py", None), ("D", "old.md", None)]
        output = "\n".join(MESSAGE.file_summary(files))
        self.assertIn("12 updated, 1 added, 1 removed", output)
        self.assertIn("4 more reference notes", output)
        self.assertIn("note7.md", output)
        self.assertNotIn("note8.md", output)
        self.assertNotIn("helper.py", output)

    def test_cli_keeps_subject_and_work_details(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "notes"
            path.write_text("- agents: preserve staged changes; regression passed\n")
            output = io.StringIO()
            with mock.patch("sys.argv", [str(SCRIPT), "2026-10-19", str(path)]), \
                    mock.patch("sys.stdin", io.StringIO("M\tgeneral/scripts/a.py\nM\tgeneral/knowledge/INDEX.md\nM\t.gitignore\n")), \
                    contextlib.redirect_stdout(output):
                MESSAGE.main()
        self.assertTrue(output.getvalue().startswith("Sync 2026-10-19: general/scripts\n"))
        self.assertIn("agents: preserve staged changes; regression passed", output.getvalue())
        self.assertIn("Files: 3 updated", output.getvalue())

    def test_many_stages_render_once_per_system_without_hiding_tasks(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "notes"
            path.write_text("\n".join(
                "- system{}: task {} verified".format(n % 3, n)
                for n in range(47)
            ))
            output = io.StringIO()
            with mock.patch("sys.argv", [str(SCRIPT), "2026-10-19", str(path)]), \
                    mock.patch("sys.stdin", io.StringIO()), \
                    contextlib.redirect_stdout(output):
                MESSAGE.main()
        rendered = output.getvalue()
        self.assertEqual(sum(line.startswith("- system")
                             for line in rendered.splitlines()), 3)
        for n in range(47):
            self.assertIn("task {} verified".format(n), rendered)


if __name__ == "__main__":
    unittest.main()
