#!/usr/bin/env python3
"""Compose the commit message for ai-sync.sh.

Usage: git diff --cached --name-status | ai_sync_message.py <date> <notes-file>

Subject lists the touched areas; the body holds the agents' lines from <notes-file>
and every changed note with its title, taken from the first H1 of the file.
Run from the repository root.
"""
import pathlib
import re
import sys

STATUS_WORD = {"A": "added", "M": "updated", "D": "removed", "R": "renamed"}
SKIP = ("INDEX.md", ".gitignore")


def meta(path):
    """Return (system, title) from a note's frontmatter and first H1."""
    p = pathlib.Path(path)
    if p.suffix != ".md" or not p.exists():
        return None, None
    system = title = None
    try:
        for line in p.read_text(errors="replace").splitlines()[:40]:
            m = re.match(r"^system:\s*(\S+)", line)
            if m and not system:
                system = m.group(1)
            if line.startswith("# ") and not title:
                title = line[2:].strip()
            if system and title:
                break
    except OSError:
        pass
    return system, title


def area(path, system):
    parts = pathlib.Path(path).parts
    if parts[0] == "companies" and len(parts) > 2:
        return parts[1]
    if parts[0] in ("general", "personal") and len(parts) > 2 and parts[1] == "knowledge":
        return f"{parts[0]}/{parts[2]}" if len(parts) > 3 else parts[0]
    if parts[0] in ("general", "personal"):
        return f"{parts[0]}/{parts[1]}" if len(parts) > 1 else parts[0]
    return parts[0]


def main():
    today, notes_path = sys.argv[1], sys.argv[2]
    files, areas = [], []
    for line in sys.stdin:
        cols = line.rstrip("\n").split("\t")
        if len(cols) < 2:
            continue
        status, path = cols[0][0], cols[-1]
        if path.endswith(SKIP):
            continue
        system, title = meta(path) if status != "D" else (None, None)
        label = area(path, system)
        if label not in areas:
            areas.append(label)
        files.append((status, path, title))

    notes = []
    np = pathlib.Path(notes_path)
    if np.exists():
        notes = [l.strip().lstrip("-* ") for l in np.read_text(errors="replace").splitlines() if l.strip()]

    subject = ", ".join(areas[:4]) + (" ..." if len(areas) > 4 else "")
    print(f"Sync {today}: {subject or 'index and housekeeping'}")
    print()
    if notes:
        print("Work recorded by agents:")
        for n in notes:
            print(f"- {n}")
        print()
    if files:
        print("Files:")
        for status, path, title in files:
            print(f"- {STATUS_WORD.get(status, status)} {path}" + (f": {title}" if title else ""))


if __name__ == "__main__":
    main()
