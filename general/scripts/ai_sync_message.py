#!/usr/bin/env python3
"""Compose the commit message for ai-sync.sh.

Usage: git diff --cached --name-status | ai_sync_message.py <date> <notes-file>

Subject lists the touched areas; the body deduplicates work notes by system and
lists a bounded selection of changed reference notes. Distinct work records are
kept verbatim: inferring which earlier stages are superseded can hide tasks.
Run from the repository root.
"""
import pathlib
import re
import sys
import argparse
from collections import Counter

STATUS_WORD = {"A": "added", "M": "updated", "D": "removed", "R": "renamed"}
SKIP = ("INDEX.md", ".gitignore")
MAX_NOTE_REFERENCES = 8


def work_groups(notes_path):
    """Deduplicate exact records and group system prefixes in encounter order."""
    groups = {}
    seen = set()
    path = pathlib.Path(notes_path)
    if not path.exists():
        return groups
    for raw in path.read_text(errors="replace").splitlines():
        line = re.sub(r"^[-*]\s+", "", raw.strip())
        if not line or line in seen:
            continue
        seen.add(line)
        match = re.match(r"^([\w./-]+):\s+(.+)$", line)
        system, text = match.groups() if match else ("Other", line)
        groups.setdefault(system, []).append(text)
    return groups


def file_summary(files):
    """Count all changes; link a bounded selection of substantive notes."""
    counts = Counter(status for status, _, _ in files)
    summary = ", ".join(
        "{} {}".format(count, STATUS_WORD.get(status, status))
        for status, count in counts.items()
    )
    lines = ["Files: {} (full paths: git show --stat).".format(summary)]
    notes = [(path, title) for status, path, title in files
             if title and status != "D"]
    if notes:
        lines.append("Reference notes:")
        for path, _ in notes[:MAX_NOTE_REFERENCES]:
            lines.append("- {}".format(path))
        remaining = len(notes) - MAX_NOTE_REFERENCES
        if remaining > 0:
            lines.append("- {} more reference notes; see git show --stat.".format(remaining))
    return lines


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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="Date for the daily commit subject")
    parser.add_argument("notes_file", help="File containing agent work records")
    args = parser.parse_args()
    today, notes_path = args.date, args.notes_file
    files, areas = [], []
    for line in sys.stdin:
        cols = line.rstrip("\n").split("\t")
        if len(cols) < 2:
            continue
        status, path = cols[0][0], cols[-1]
        if path.endswith(SKIP):
            files.append((status, path, None))
            continue
        system, title = meta(path) if status != "D" else (None, None)
        label = area(path, system)
        if label not in areas:
            areas.append(label)
        files.append((status, path, title))

    groups = work_groups(notes_path)

    subject = ", ".join(areas[:4]) + (" ..." if len(areas) > 4 else "")
    print(f"Sync {today}: {subject or 'index and housekeeping'}")
    print()
    if groups:
        print("Work recorded by agents:")
        for system, records in groups.items():
            print("- {}: {}".format(system, "; ".join(records)))
        print()
    if files:
        print("\n".join(file_summary(files)))


if __name__ == "__main__":
    main()
