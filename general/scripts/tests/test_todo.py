"""Behavioral checks for the shared backlog renderer (stdlib only)."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "todo.py"
SPEC = importlib.util.spec_from_file_location("todo", SCRIPT)
todo = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(todo)


def display_for(source):
    return {
        "tasks": {todo.task_key(item): "Проверить задачу " + str(i) for i, (_, item) in enumerate(todo.entries(source))},
        "headings": {h: "Раздел " + h for headings, _ in todo.entries(source) for h in headings},
    }


class TodoTests(unittest.TestCase):
    def test_exact_russian_bullets_without_source_metadata(self):
        source = "## Personal\n### Network\n- [x] Finished\n- [ ] Original (2026-10-19) — [src](personal/note.md)\n  Context.\n"
        cache = display_for(source)
        output = todo.render(todo.select(source, cache), cache)
        self.assertEqual(output, "Открытые задачи: 1\n\n### Раздел Personal → Раздел Network\n\n- Проверить задачу 0\n")
        for unwanted in ("[ ]", "src", "2026-10-19", "Context.", "Original"):
            self.assertNotIn(unwanted, output)

    def test_heading_reset_order_checked_and_fences(self):
        source = "## First\n### System\n- [ ] Z\n- [X] Closed\n```markdown\n## Fake\n- [ ] Example\n```\n~~~\n- [ ] Another example\n~~~\n## Next\n- [ ] A\n"
        self.assertEqual(list(todo.entries(source)), [(("First", "System"), "- [ ] Z"), (("Next",), "- [ ] A")])

    def test_filters_case_insensitive_literal_and_combined(self):
        source = "## Personal\n### VPN\n- [ ] Check [one]\n## Other\n### VPN\n- [ ] Two\n"
        cache = display_for(source)
        selected = todo.select(source, cache, layer="PERSON", system="vpn", query="[ONE]")
        self.assertEqual(len(selected), 1)
        self.assertEqual(todo.select(source, cache, layer="Personal", query="Two"), [])
        self.assertEqual(len(todo.select(source, cache, query="ПРОВЕРИТЬ ЗАДАЧУ 1")), 1)
        self.assertEqual(len(todo.select(source, cache, system="vpn")), 2)

    def test_empty(self):
        self.assertEqual(todo.render([], {}), "Открытых задач нет.\n")

    def test_no_blank_lines_between_items(self):
        source = "## Test\n- [ ] One\n- [ ] Two\n## Next\n- [ ] Three\n"
        cache = display_for(source)
        output = todo.render(todo.select(source, cache), cache)
        self.assertIn("- Проверить задачу 0\n- Проверить задачу 1\n\n### Раздел Next\n\n- Проверить задачу 2", output)

    def test_title_length_limit_requires_refresh_without_truncation(self):
        self.assertTrue(todo.valid_description("Я" * 120))
        self.assertFalse(todo.valid_description("Я" * 121))
        source = "## Test\n- [ ] Original\n"
        cache = display_for(source)
        key = next(iter(cache["tasks"]))
        cache["tasks"][key] = "Длинное описание " * 10
        self.assertIn(key, todo.missing_descriptions(todo.select(source, cache), cache)["tasks"])
        with self.assertRaises(ValueError):
            todo.render(todo.select(source, cache), cache)

    def test_changed_source_invalidates_cache_and_closed_items_disappear(self):
        source = "## Test\n- [ ] Original\n"
        cache = display_for(source)
        edited = source.replace("Original", "Changed")
        missing = todo.missing_descriptions(todo.select(edited, cache), cache)
        self.assertEqual(list(missing["tasks"].values()), ["- [ ] Changed"])
        with self.assertRaises(ValueError):
            todo.render(todo.select(edited, cache), cache)
        closed = source.replace("[ ]", "[x]")
        self.assertEqual(todo.render(todo.select(closed, cache), cache), "Открытых задач нет.\n")

    def test_invalid_descriptions_require_refresh(self):
        for description in ("English only", "Задача 2026-10-19", "Задача [src](note.md)", "Задача [ ]", "- Задача", "Задача\nстрока"):
            self.assertFalse(todo.valid_description(description), description)

    def test_cli_file_missing_and_cache_refresh(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "TODO.md"
            cache_path = Path(directory) / "display.json"
            source = "## Test\n- [ ] Original\n"
            path.write_text(source, encoding="utf-8")
            cmd = [sys.executable, str(SCRIPT), "--file", str(path), "--display", str(cache_path)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            result = subprocess.run(cmd + ["--missing"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(len(json.loads(result.stdout)["tasks"]), 1)
            cache_path.write_text(json.dumps(display_for(source)), encoding="utf-8")
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertIn("- Проверить задачу 0", result.stdout)
            path.unlink()
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
