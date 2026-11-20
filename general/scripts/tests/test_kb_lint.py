"""Verify Markdown diagnostics, staged secret checks, and directory failures."""
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
    def lint(self, body, layer="personal", filename="example.md", header=HEADER):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            note = root / layer / "knowledge" / filename
            note.parent.mkdir(parents=True)
            note.write_text(header + body)
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

    def test_portable_readme_checks_identifiers_without_requiring_frontmatter(self):
        result = self.lint("Example: `service.corp`", layer="general", filename="README.md", header="")
        self.assertEqual(result.returncode, 1)
        self.assertIn("E leak", result.stdout)
        self.assertNotIn("frontmatter", result.stdout)


class StagedSecretsTests(unittest.TestCase):
    def setUp(self):
        repo = tempfile.TemporaryDirectory()
        self.addCleanup(repo.cleanup)
        self.root = pathlib.Path(repo.name)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.env.update(AI_ROOT=str(self.root))
        self.git("init", "-q")
        self.secret = "glpat-" + "A" * 20

    def git(self, *args):
        return subprocess.run(["git", *args], env=self.env, cwd=self.root, check=True,
                              capture_output=True)

    def lint(self):
        return subprocess.run([sys.executable, str(SCRIPT), "--staged"], capture_output=True,
                              text=True, env=self.env)

    def test_full_staged_blobs_including_nonmarkdown_and_non_utf8(self):
        for name in ("a script.py", "config\nfile.yml", "old.bak"):
            (self.root / name).write_bytes(("x = " + self.secret).encode("utf-16"))
            self.git("add", "--", name)
            (self.root / name).unlink()
        result = self.lint()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(result.stdout.count("E secret"), 3, result.stdout)
        self.assertIn("config\\nfile.yml", result.stdout)
        self.assertNotIn(self.secret, result.stdout + result.stderr)

    def test_worktree_only_secret_is_outside_staged_check(self):
        path = self.root / "example.json"
        path.write_text("{}")
        self.git("add", "--", path.name)
        path.write_text(self.secret)
        result = self.lint()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_full_blob_includes_unchanged_lines_in_modified_file(self):
        path = self.root / "example"
        prefix = self.secret + "\n" + "\n" * 10
        path.write_text(prefix + "before\n")
        self.git("add", "--", path.name)
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "commit", "-qm", "initial")
        path.write_text(prefix + "after\n")
        self.git("add", "--", path.name)
        self.assertIn("E secret", self.lint().stdout)

    def test_env_gate_uses_exact_staged_path(self):
        path = self.root / "dir with space"
        path.mkdir()
        (path / ".env").write_text("KEY=value")
        (path / ".env.example").write_text("KEY=value")
        self.git("add", "-A")
        result = self.lint()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(result.stdout.count("E secret"), 1, result.stdout)
        self.assertIn("dir with space/.env", result.stdout)

    def test_missing_staged_blob_fails_without_success_summary(self):
        path = self.root / "example"
        path.write_text("fixture\n")
        self.git("add", "--", path.name)
        oid = self.git("rev-parse", ":example").stdout.decode().strip()
        (self.root / ".git/objects" / oid[:2] / oid[2:]).unlink()
        result = self.lint()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("cannot read staged blob", result.stderr)
        self.assertNotIn("errors,", result.stdout)


class DirectoryChecksTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = pathlib.Path(directory.name) / "kb"

    def run_cli(self, script, *args):
        return subprocess.run([sys.executable, str(SCRIPT.with_name(script)), *args],
                              env={**os.environ, "AI_ROOT": str(self.root)},
                              capture_output=True, text=True)

    def test_missing_root_and_broken_layer_are_incomplete(self):
        for broken_layer in (False, True):
            if broken_layer:
                (self.root / "general/knowledge").mkdir(parents=True)
                (self.root / "current").symlink_to("unavailable-company")
            for script, args in (("kb_find.py", ("query",)),
                                 ("kb_lint.py", ()),
                                 ("build_index.py", ("--check",)),
                                 ("build_index.py", ("--stale", "30", "--count"))):
                with self.subTest(script=script, args=args, broken_layer=broken_layer):
                    result = self.run_cli(script, *args)
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                    self.assertFalse(result.stdout)
                    self.assertIn(str(self.root / "current" if broken_layer else self.root),
                                  result.stderr)

    def test_empty_readable_layer_and_missing_explicit_layer_are_distinct(self):
        (self.root / "general/knowledge").mkdir(parents=True)
        empty = self.run_cli("kb_find.py", "query")
        self.assertEqual(empty.returncode, 1, empty.stderr)
        self.assertIn("0 notes", empty.stdout)
        for script, args in (("kb_find.py", ("-l", "personal", "query")),
                             ("build_index.py", ("--check", str(self.root / "personal")))):
            missing = self.run_cli(script, *args)
            self.assertEqual(missing.returncode, 2, missing.stdout + missing.stderr)
            self.assertIn("personal/knowledge", missing.stderr)

    @unittest.skipIf(os.geteuid() == 0, "root can read directories without permission bits")
    def test_unreadable_nested_directory_stops_every_check(self):
        blocked = self.root / "general/knowledge/blocked"
        blocked.mkdir(parents=True)
        blocked.chmod(0)
        self.addCleanup(blocked.chmod, 0o700)
        for script, args in (("kb_find.py", ("anything",)),
                             ("kb_lint.py", ()),
                             ("build_index.py", ())):
            with self.subTest(script=script):
                result = self.run_cli(script, *args)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn(str(blocked), result.stderr)
                self.assertFalse(result.stdout)
        self.assertFalse((blocked.parent / "INDEX.md").exists())


if __name__ == "__main__":
    unittest.main()
