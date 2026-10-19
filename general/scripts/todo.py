#!/usr/bin/env python3
"""Render the shared Markdown backlog without model-dependent summarization."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


DEFAULT_FILE = Path(__file__).resolve().parents[2] / "TODO.md"
DEFAULT_DISPLAY = Path.home() / "ai-data" / "todo" / "display-ru.json"
MAX_DESCRIPTION_LENGTH = 120
HEADING = re.compile(r"^(#{2,6})\s+(.+?)\s*#*\s*$")
CHECKBOX = re.compile(r"^([ \t]*)[-*+] \[([ xX])\] (.*)$")


def entries(markdown):
    """Yield heading paths and open items, including indented continuations."""
    headings = []
    pending = None
    fence = None
    for line in markdown.splitlines():
        stripped = line.lstrip()
        marker = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                fence = None
            continue
        if marker:
            if pending:
                yield pending[0], "\n".join(pending[1])
                pending = None
            fence = marker[1]
            continue
        checkbox = CHECKBOX.match(line)
        if pending:
            if not checkbox and line.startswith(("  ", "\t")):
                pending[1].append(line)
                continue
            yield pending[0], "\n".join(pending[1])
            pending = None
        heading = HEADING.match(line)
        if heading:
            level = len(heading[1])
            headings = [(n, title) for n, title in headings if n < level]
            headings.append((level, heading[2]))
        elif checkbox and checkbox[2] == " ":
            pending = (tuple(title for _, title in headings), [line])
    if pending:
        yield pending[0], "\n".join(pending[1])


def task_key(item):
    return hashlib.sha256(item.encode("utf-8")).hexdigest()


def select(markdown, display, layer=None, system=None, query=None):
    selected = []
    for headings, item in entries(markdown):
        if layer and (not headings or layer.casefold() not in headings[0].casefold()):
            continue
        if system and not any(system.casefold() in h.casefold() for h in headings[1:]):
            continue
        searchable = "\n".join(headings) + "\n" + item
        searchable += "\n" + display.get("tasks", {}).get(task_key(item), "")
        if query and query.casefold() not in searchable.casefold():
            continue
        selected.append((headings, item))
    return selected


def valid_description(value):
    return (isinstance(value, str) and bool(re.search(r"[А-Яа-яЁё]", value))
            and len(value) <= MAX_DESCRIPTION_LENGTH
            and "\n" not in value and not re.search(r"\d{4}-\d{2}-\d{2}|\[[ xX]\]|\]\(|https?://", value)
            and not value.startswith(("- ", "* ", "+ ")))


def missing_descriptions(selected, display):
    missing = {"tasks": {}, "headings": {}}
    for headings, item in selected:
        key = task_key(item)
        if not valid_description(display.get("tasks", {}).get(key)):
            missing["tasks"][key] = item
        for heading in headings:
            if not valid_description(display.get("headings", {}).get(heading)):
                missing["headings"][heading] = heading
    return missing


def render(selected, display):
    if not selected:
        return "Открытых задач нет.\n"
    missing = missing_descriptions(selected, display)
    if any(missing.values()):
        raise ValueError("Russian descriptions are missing or stale; run with --missing and update --display JSON")
    output = [f"Открытые задачи: {len(selected)}"]
    previous = None
    for headings, item in selected:
        if headings != previous:
            titles = [display["headings"][h] for h in headings] or ["Без раздела"]
            output.extend(["", "### " + " → ".join(titles), ""])
            previous = headings
        output.append("- " + display["tasks"][task_key(item)])
    return "\n".join(output) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE, help="Backlog file (default: ~/ai/TODO.md)")
    parser.add_argument("--display", type=Path, default=DEFAULT_DISPLAY, help="Derived Russian display cache JSON")
    parser.add_argument("--missing", action="store_true", help="Print JSON of missing/stale descriptions for an agent to translate")
    parser.add_argument("--layer", help="Case-insensitive substring of the layer heading")
    parser.add_argument("--system", help="Case-insensitive substring of a heading below the layer")
    parser.add_argument("--query", help="Case-insensitive literal substring of headings or task text")
    args = parser.parse_args()
    path = args.file.expanduser().absolute()
    try:
        markdown = path.read_text(encoding="utf-8")
        cache = args.display.expanduser()
        display = json.loads(cache.read_text(encoding="utf-8")) if cache.exists() else {}
        if (not isinstance(display, dict)
                or any(not isinstance(display.get(k, {}), dict) for k in ("tasks", "headings"))):
            raise ValueError("Display cache must contain tasks and headings objects")
    except (OSError, UnicodeError) as exc:
        print(f"Cannot read backlog {path}: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Invalid display cache: {exc}", file=sys.stderr)
        return 1
    selected = select(markdown, display, args.layer, args.system, args.query)
    if args.missing:
        print(json.dumps(missing_descriptions(selected, display), ensure_ascii=False, indent=2))
        return 0
    try:
        print(render(selected, display), end="")
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
