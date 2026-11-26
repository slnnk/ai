import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1]


class PostEditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.root = self.home / "ai"
        scripts = self.root / "general/scripts"
        scripts.mkdir(parents=True)
        for name in ("kb_post_edit.py", "kb_lint.py", "kb_paths.py", "kb_find.py"):
            shutil.copy(SCRIPTS / name, scripts / name)
        self.hook = scripts / "kb_post_edit.py"
        self.note = self.root / "general/knowledge/example.md"
        self.note.parent.mkdir(parents=True)
        self.env = {name: value for name, value in os.environ.items()
                    if not name.startswith("JCODE_HOOK_")}

    def run_hook(self, payload=None, **environment):
        return subprocess.run([sys.executable, str(self.hook)], input=json.dumps(payload),
                              env={**self.env, **environment}, text=True, capture_output=True)

    def edit(self, *paths):
        patch = "\n".join(f"*** Update File: {path}" for path in paths)
        return self.run_hook({"tool_name": "apply_patch", "cwd": str(self.home),
                              "tool_input": {"command": patch}})

    def test_codex_reports_only_requested_notes_and_no_source_values(self):
        credential = "gh" + "p_" + "x" * 36
        self.note.write_text(f"---\nsystem: test\nstatus: {credential}\nchecked: 2026-11-25\n---\n")
        unrelated = self.note.with_name("unrelated.md")
        unrelated.write_text("Missing metadata.")
        result = self.edit(self.note.relative_to(self.home))
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertEqual(output["hookEventName"], "PostToolUse")
        self.assertIn("E frontmatter", output["additionalContext"])
        self.assertIn("E secret", output["additionalContext"])
        self.assertNotIn(credential, result.stdout)
        self.assertNotIn(unrelated.name, result.stdout)

    def test_jcode_reports_edit_and_skips_read(self):
        self.note.write_text("Missing metadata.")
        env = dict(JCODE_HOOK_TOUCHED_PATHS=str(self.note))
        edit = self.run_hook(JCODE_HOOK_TOOL_NAME="write", **env)
        read = self.run_hook(JCODE_HOOK_TOOL_NAME="read", **env)
        self.assertIn("E frontmatter", edit.stdout)
        self.assertEqual(read.stdout, "")

    def test_clean_notes_and_outside_paths_are_silent(self):
        self.note.write_text("---\nsystem: test\nstatus: verified\nchecked: 2026-11-25\n---\n# Example\n")
        outside = self.home / "outside.md"
        outside.write_text("Missing metadata.")
        alias = self.note.with_name("external.md")
        alias.symlink_to(outside)
        result = self.edit(self.note, outside, alias, self.note.with_name("deleted.md"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
