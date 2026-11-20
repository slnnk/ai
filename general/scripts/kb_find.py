#!/usr/bin/env python3
"""Search KB notes with section context and explicit scoped decisions.

AND is the default; use --any for alternatives, -l for layers, -s for a system.
-n limits displayed context lines (default 5). --files keeps path-only output;
--json provides structured results for repeatable retrieval checks.
"""
import argparse
import datetime
import json
import os
import re
import shlex
import sys
from pathlib import Path

from kb_paths import DEFAULT_LAYERS, knowledge_dirs, markdown_files

AI_ROOT = Path(os.environ.get("AI_ROOT", Path.home() / "ai"))
SKIP = {"INDEX.md", "README.md"}
LINE_WIDTH = 240
DECISION_FIELDS = ("decision_state", "decision_scope", "decision_summary", "decision_date", "decision_source")
DECISION_STATES = {"active", "cancelled", "superseded", "restricted"}


def parse_frontmatter(lines):
    if not lines or lines[0].strip() != "---":
        return {}, 0
    meta = {}
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            return meta, i + 1
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    return {}, 0


def notes(layers=None):
    seen = set()
    for root in knowledge_dirs(AI_ROOT, layers or DEFAULT_LAYERS, explicit=layers is not None):
        paths = sorted(markdown_files(root))
        canonical_root = root.resolve()
        for path in paths:
            f = canonical_root / path.relative_to(root)
            if f.name not in SKIP and f not in seen:
                seen.add(f)
                yield f


def display(f):
    try:
        return "~/ai/" + str(f.relative_to(AI_ROOT.resolve()))
    except ValueError:
        return str(f)


def markdown_headings(lines, start=0):
    """Yield real ATX headings and GitHub-style anchors, ignoring fenced examples."""
    fence = None
    anchors = set()
    for i in range(start, len(lines)):
        line = lines[i]
        m = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if m and m[1][0] == fence[0] and len(m[1]) >= len(fence) and not m[2].strip():
                fence = None
            continue
        if m:
            fence = m[1]
            continue
        m = re.match(r"^ {0,3}(#{1,6})\s+(.+?)\s*$", line)
        if m:
            title = re.sub(r"\s+#+\s*$", "", m[2])
            anchor = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
            base = anchor
            count = 0
            while anchor in anchors:
                count += 1
                anchor = base + "-" + str(count)
            anchors.add(anchor)
            yield i, len(m[1]), title, anchor


def decision(meta, f, root=None):
    """Validate an explicit decision; never infer cancellation from historical prose."""
    if not any(k in meta for k in DECISION_FIELDS):
        return None
    missing = [k for k in DECISION_FIELDS if not meta.get(k) or meta[k] in {"|", ">"}]
    if missing:
        raise ValueError("decision requires single-line fields: " + ", ".join(missing))
    if meta["decision_state"] not in DECISION_STATES:
        raise ValueError("invalid decision_state")
    try:
        datetime.date.fromisoformat(meta["decision_date"])
    except ValueError:
        raise ValueError("invalid decision_date (expected YYYY-MM-DD)")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta["decision_date"]):
        raise ValueError("invalid decision_date (expected YYYY-MM-DD)")
    base = (root or AI_ROOT).resolve()
    path, sep, anchor = meta["decision_source"].partition("#")
    if ":" in path or path.startswith(("/", "~")):
        raise ValueError("decision_source must be a relative Markdown reference")
    source = (f.parent / path).resolve() if path else f.resolve()
    try:
        source.relative_to(base)
    except ValueError:
        raise ValueError("decision_source escapes the knowledge root")
    if source.suffix != ".md" or not source.is_file():
        raise ValueError("decision_source does not name an existing Markdown note")
    source_lines = source.read_text(errors="replace").splitlines()
    _, body = parse_frontmatter(source_lines)
    headings = list(markdown_headings(source_lines, body))
    if not sep or not anchor:
        raise ValueError("decision_source must identify an explicit heading anchor")
    found = next((i + 1 for i, _, _, a in headings if a == anchor), None)
    if found is None:
        raise ValueError("decision_source heading anchor does not exist")
    return {"state": meta["decision_state"], "scope": meta["decision_scope"],
            "summary": meta["decision_summary"], "date": meta["decision_date"],
            "source": display(source), "source_line": found, "source_anchor": anchor}


def sections(lines, body_start):
    result = []
    stack = []
    start = body_start
    label = "Introduction"
    for i, level, title, _ in markdown_headings(lines, body_start):
        if i > start:
            result.append({"start": start, "end": i, "heading": label})
        stack = [(n, t) for n, t in stack if n < level]
        stack.append((level, title))
        label = " > ".join(t for n, t in stack if n > 1) or title
        start = i
    if start < len(lines):
        result.append({"start": start, "end": len(lines), "heading": label})
    return result


def clip(line, pats):
    line = line.strip()
    if len(line) <= LINE_WIDTH:
        return line
    matches = [(m.start(), m.end(), k) for k, p in enumerate(pats) for m in p.finditer(line)]
    starts = {max(0, a - LINE_WIDTH // 3) for a, _, _ in matches} or {0}
    start = max(starts, key=lambda s: (len({k for a, b, k in matches if s <= a and b <= s + LINE_WIDTH}),
                                      sum(s <= a and b <= s + LINE_WIDTH for a, b, _ in matches), -s))
    return ("..." if start else "") + line[start:start + LINE_WIDTH] + "..."


def context(lines, body_start, pats, budget):
    """Choose a relevant section and a coherent bounded window within it."""
    candidates = []
    for section in sections(lines, body_start):
        section = dict(section)
        # The heading is rendered separately; do not select a title-only excerpt.
        if re.match(r"^ {0,3}#{1,6}\s", lines[section["start"]]):
            section["start"] += 1
        while section["start"] < section["end"] and not lines[section["start"]].strip():
            section["start"] += 1
        while section["end"] > section["start"] and not lines[section["end"] - 1].strip():
            section["end"] -= 1
        indices = list(range(section["start"], section["end"]))
        hits = [i for i in indices if any(p.search(lines[i]) for p in pats)]
        if not hits:
            continue
        coverage = sum(any(p.search(lines[i]) for i in indices) for p in pats)
        heading_hits = sum(bool(p.search(section["heading"])) for p in pats)
        answer_section = bool(re.search(r"\b(cause|summary|decision|fix|resolution)\b", section["heading"], re.I))
        # A cause/summary/decision may use one fewer repeated symptom term.
        # Prefer it on that narrow tie, without selecting a nonmatching section.
        score = (coverage + int(answer_section), answer_section, coverage,
                 heading_hits, len(hits) / max(1, len(indices)), -section["start"])
        candidates.append((score, section, hits))
    if not candidates:
        return None, []
    _, selected, hits = max(candidates, key=lambda c: c[0])
    if budget == 0:
        return selected, []
    width = min(budget, selected["end"] - selected["start"])
    windows = []
    for start in range(selected["start"], selected["end"] - width + 1):
        indices = range(start, start + width)
        score = (sum(any(p.search(lines[i]) for i in indices) for p in pats),
                 sum(any(p.search(lines[i]) for p in pats) for i in indices),
                 -abs((start + (width - 1) / 2) - hits[0]), -start)
        windows.append((score, start))
    start = max(windows)[1]
    return selected, [{"line": i + 1, "text": clip(lines[i], pats)} for i in range(start, start + width)]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("keywords", nargs="+")
    ap.add_argument("-l", "--layer", action="append")
    ap.add_argument("-s", "--system")
    ap.add_argument("-n", "--lines", type=int, default=5, help="context line budget per note (default 5)")
    ap.add_argument("-m", "--max-notes", type=int, default=15)
    ap.add_argument("--offset", type=int, default=0, help="skip ranked notes for continuation")
    ap.add_argument("--any", action="store_true")
    ap.add_argument("--regex", action="store_true")
    output = ap.add_mutually_exclusive_group()
    output.add_argument("--files", action="store_true")
    output.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.lines < 0 or args.max_notes < 0 or args.offset < 0:
        ap.error("line and note limits must be nonnegative")
    try:
        pats = [re.compile(k if args.regex else re.escape(k), re.I) for k in args.keywords]
    except re.error as e:
        ap.error(str(e))
    match = any if args.any else all
    results = []
    try:
        for f in notes(args.layer):
            text = f.read_text(errors="replace")
            if not match(p.search(text) for p in pats):
                continue
            lines = text.splitlines()
            meta, body_start = parse_frontmatter(lines)
            if args.system and args.system.lower() not in meta.get("system", "").lower():
                continue
            title = next((t for _, level, t, _ in markdown_headings(lines, body_start) if level == 1), f.stem)
            head = "{} {} {}".format(f.name, title, meta.get("system", ""))
            head_hits = sum(bool(p.search(head)) for p in pats)
            hits = [(i + 1, l) for i, l in enumerate(lines) if i >= body_start and
                    l.strip() != "# " + title and any(p.search(l) for p in pats)]
            # Living maps and portable recipes get a one-term tie preference.
            # Density replaces raw frequency so repeated log lines cannot dominate.
            relative_parts = f.relative_to(AI_ROOT.resolve()).parts
            canonical = 'systems' in relative_parts or (relative_parts[0] == 'general' and 'log' not in relative_parts)
            score = (head_hits + int(canonical), canonical, head_hits,
                     len(hits) / max(1, len(lines) - body_start))
            results.append((score, len(hits), f, meta, title, lines, body_start, len(text.encode())))
        results.sort(key=lambda r: (tuple(-x for x in r[0]), str(r[2])))
        rendered = []
        for _, _, f, meta, title, lines, body_start, size in results[args.offset:args.offset + args.max_notes]:
            if args.files:
                rendered.append({"path": display(f)})
                continue
            section, snippets = context(lines, body_start, pats, args.lines)
            visible = "\n".join(s["text"] for s in snippets)
            clipped = [s["line"] for s in snippets if s["text"] != lines[s["line"] - 1].strip()]
            shown_indices = {s['line'] - 1 for s in snippets}
            omitted_matches = any(i not in shown_indices and any(p.search(l) for p in pats)
                                  for i, l in enumerate(lines) if i >= body_start)
            coverage = {"matched_terms": [k for k, p in zip(args.keywords, pats) if any(p.search(l) for l in lines)],
                        "visible_terms": [k for k, p in zip(args.keywords, pats) if p.search(visible)],
                        "matching_lines": sum(any(p.search(l) for p in pats) for l in lines[body_start:]),
                        "shown_lines": len(snippets), "clipped_lines": clipped,
                        "excerpt_truncated": bool(clipped) or omitted_matches or bool(section and len(snippets) < section["end"] - section["start"])}
            rendered.append({"path": display(f), "coverage": coverage, "system": meta.get("system", "?"),
                "status": meta.get("status", "?"), "checked": meta.get("checked", "?"),
                "title": title, "size_bytes": size, "has_summary": any(l.startswith("## Summary") for l in lines),
                "decision": decision(meta, f), "section": section, "snippets": snippets})
    except (OSError, RuntimeError, ValueError) as e:
        print("kb-find: error: " + str(e), file=sys.stderr)
        return 2
    end = args.offset + len(rendered)
    truncated = end < len(results)
    command = [sys.executable, str(Path(__file__).resolve())]
    for layer in args.layer or []:
        command += ['-l', layer]
    if args.system:
        command += ['-s', args.system]
    command += ['-n', str(args.lines), '-m', str(args.max_notes or 15), '--offset', str(end)]
    command += [flag for flag in ('--any', '--regex', '--files', '--json') if getattr(args, flag[2:])]
    command += ['--', *args.keywords]
    next_command = command if truncated else None
    if args.json:
        print(json.dumps({"schema_version": 1, "total_matches": len(results), "shown_notes": len(rendered),
                          "offset": args.offset, "truncated": truncated, "next_command": next_command,
                          "results": rendered}, ensure_ascii=False))
    elif args.files:
        for r in rendered:
            print(r["path"])
        if truncated:
            print('kb-find: truncated; next: ' + shlex.join(next_command), file=sys.stderr)
    else:
        for r in rendered:
            print("{}  [{} | {} | {} | {} KB{}]".format(r["path"], r["system"], r["status"],
                  r["checked"], r["size_bytes"] // 1024, " | summary" if r["has_summary"] else ""))
            print("  # " + r["title"])
            if r["decision"]:
                d = r["decision"]
                print("  ! Current decision [{}; {}; {}]: {}".format(d["state"], d["scope"], d["date"], d["summary"]))
                print("  ! Source: {}:{}".format(d["source"], d["source_line"]))
            if r["section"]:
                print("  Section: " + r["section"]["heading"])
            for snippet in r["snippets"]:
                print("  {}: {}".format(snippet["line"], snippet["text"]))
            c = r['coverage']
            print('  Coverage: {}/{} terms visible; {}/{} matching lines shown{}'.format(
                len(c['visible_terms']), len(c['matched_terms']),
                sum(any(p.search(s['text']) for p in pats) for s in r['snippets']), c['matching_lines'],
                '; excerpt incomplete; read {}:{} (full section/source)'.format(r['path'], r['section']['start'] + 1 if r['section'] else 1) if c['excerpt_truncated'] else ''))
        print("kb-find: {} notes; showing {}; offset {}".format(len(results), len(rendered), args.offset) if results else 'kb-find: 0 notes')
        if truncated:
            print('kb-find: truncated; next: ' + shlex.join(next_command))
    return 0 if results else 1


if __name__ == "__main__":
    sys.exit(main())
