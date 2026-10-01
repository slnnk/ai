#!/usr/bin/env python3
"""Search the ~/ai knowledge base and print a compact hit list instead of whole notes.

Usage:
    kb_find.py nomad csi                 notes containing all keywords (case-insensitive)
    kb_find.py --any rabbitmq sorm       notes containing at least one keyword
    kb_find.py -l current -s nomad-test  only the current layer, only system nomad-test
    kb_find.py -n 5 vault                up to 5 matching lines per note (default 3)
    kb_find.py --files vault             paths only, one per line

For each note it prints the path, system, status, checked date, title, the `## Summary`
flag and the first matching lines with line numbers. Notes are ranked by hits in the
filename/title/system first, then by the number of matching lines. Read the note itself
only after picking it from this list, and then only the needed section (`sed -n A,Bp`).

Keywords are plain substrings; a keyword may be a Python regex with --regex.
"""
import argparse
import os
import re
import sys
from pathlib import Path

AI_ROOT = Path(os.environ.get("AI_ROOT", Path.home() / "ai"))
DEFAULT_LAYERS = ["general", "personal", "current"]
SKIP = {"INDEX.md", "README.md"}
LINE_WIDTH = 160


def parse_frontmatter(lines):
    if not lines or lines[0].strip() != "---":
        return {}, 0
    meta = {}
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return meta, i + 1
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    return {}, 0


def notes(layers):
    for layer in layers:
        root = (AI_ROOT / layer / "knowledge").resolve()
        if root.is_dir():
            for f in sorted(root.rglob("*.md")):
                if f.name not in SKIP:
                    yield f


def display(f):
    try:
        return "~/ai/" + str(f.relative_to(AI_ROOT.resolve()))
    except ValueError:
        return str(f)


def clip(line, pats):
    line = line.strip()
    if len(line) <= LINE_WIDTH:
        return line
    m = pats[0].search(line) if pats else None
    start = max(0, (m.start() if m else 0) - LINE_WIDTH // 3)
    return ("..." if start else "") + line[start:start + LINE_WIDTH] + "..."


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("keywords", nargs="+")
    ap.add_argument("-l", "--layer", action="append", help="general, personal, current (repeatable)")
    ap.add_argument("-s", "--system", help="only notes whose frontmatter system contains this")
    ap.add_argument("-n", "--lines", type=int, default=3, help="matching lines per note (default 3)")
    ap.add_argument("-m", "--max-notes", type=int, default=15, help="notes to print (default 15)")
    ap.add_argument("--any", action="store_true", help="match any keyword instead of all")
    ap.add_argument("--regex", action="store_true", help="treat keywords as regular expressions")
    ap.add_argument("--files", action="store_true", help="print paths only")
    args = ap.parse_args()

    pats = [re.compile(k if args.regex else re.escape(k), re.I) for k in args.keywords]
    match = any if args.any else all
    results = []

    for f in notes(args.layer or DEFAULT_LAYERS):
        text = f.read_text(errors="replace")
        if not match(p.search(text) for p in pats):
            continue
        lines = text.splitlines()
        meta, body_start = parse_frontmatter(lines)
        if args.system and args.system.lower() not in meta.get("system", "").lower():
            continue
        title = next((l[2:].strip() for l in lines[body_start:] if l.startswith("# ")), f.stem)
        head = f"{f.name} {title} {meta.get('system', '')}"
        head_hits = sum(1 for p in pats if p.search(head))
        hits = [(i + 1, l) for i, l in enumerate(lines)
                if i >= body_start and l.strip() != f"# {title}" and any(p.search(l) for p in pats)]
        results.append((head_hits, len(hits), f, meta, title, hits,
                        any(l.startswith("## Summary") for l in lines), len(text)))

    results.sort(key=lambda r: (-r[0], -r[1], str(r[2])))
    for head_hits, n, f, meta, title, hits, has_summary, size in results[:args.max_notes]:
        if args.files:
            print(display(f))
            continue
        print(f"{display(f)}  [{meta.get('system', '?')} | {meta.get('status', '?')} | "
              f"{meta.get('checked', '?')} | {size // 1024} KB{' | summary' if has_summary else ''}]")
        print(f"  # {title}")
        for no, line in hits[:args.lines]:
            print(f"  {no}: {clip(line, pats)}")
        if n > args.lines:
            print(f"  (+{n - args.lines} more lines)")
    if not args.files:
        more = len(results) - args.max_notes
        print(f"kb-find: {len(results)} notes" + (f", {more} not shown (-m)" if more > 0 else ""))
    return 0 if results else 1


if __name__ == "__main__":
    sys.exit(main())
