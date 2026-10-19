#!/usr/bin/env python3
"""Summarize token usage of Claude Code and Codex sessions from their local transcripts.

Usage:
    token_usage.py              last 7 days, totals per agent/project/model + top 5 sessions
    token_usage.py --days 30    other window
    token_usage.py --top 10     more sessions in the top list
    token_usage.py --kb         also: how agents accessed the knowledge base
    token_usage.py --brief      one summary line (used by ai-sync.sh)

Sources (read only):
    ~/.claude/projects/<project>/*.jsonl and .../subagents/*.jsonl
        assistant entries carry message.usage; one response may span several entries with
        the same message.id, so usage is counted once per id.
    ~/.codex/sessions/YYYY/MM/DD/*.jsonl
        event_msg/token_count carries a cumulative total_token_usage; the last one per
        session is taken. Codex `input_tokens` includes cached tokens; they are split out.

Columns: fresh input, cache read, cache write, output, in tokens (k = thousand, M = million).
--kb classifies tool calls (heuristic, by paths in the command or Read call):
    kb_find   a call of kb_find.py
    search    grep/rg over knowledge/ or ~/ai
    index     reading an INDEX.md
    full      Read without offset/limit, or cat/less of a note without head/sed/grep
    partial   Read with offset/limit, or head/tail/sed -n/awk on a note
Codex: statically extract nested shell calls from functions.exec, then classify
individual shell commands (including cwd/cd and partial-read pipelines).
Requires Node.js and Acorn for JS wrappers; missing dependencies and unsupported
calls are reported as incomplete coverage, never guessed as reads.
Counts are requested static reads, not confirmed output or token savings.
"full KiB" uses current note file sizes, not historical returned bytes.
Claude tool classification retains its existing heuristics.

No prices: multiply by the current price list yourself if a cost is needed.
Record expensive sessions and why in the knowledge-base log (see ~/ai/TODO.md).
"""
import argparse
import json
import os
import re
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

from token_usage_kb import extract_shell_calls, classify_command, classification_status

HOME = Path.home()
CLAUDE = Path(os.environ.get("CLAUDE_PROJECTS", HOME / ".claude/projects"))
CODEX = Path(os.environ.get("CODEX_SESSIONS", HOME / ".codex/sessions"))
AI_ROOT = Path(os.environ.get("AI_ROOT", HOME / "ai"))


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def fmt(n):
    return f"{n / 1e6:.1f}M" if n >= 1e6 else f"{n / 1e3:.0f}k" if n >= 1e3 else str(n)


def short_cwd(p):
    p = str(p or "?")
    return "~" + p[len(str(HOME)):] if p.startswith(str(HOME)) else p


def claude_sessions(since):
    """Yield (session_id, project, model, first_ts, [fresh, cache_read, cache_write, out])."""
    sessions = {}
    for f in CLAUDE.rglob("*.jsonl"):
        if datetime.fromtimestamp(f.stat().st_mtime, timezone.utc) < since:
            continue
        seen = set()
        with f.open(errors="replace") as fh:
            for line in fh:
                if '"usage"' not in line:
                    continue
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                m = d.get("message") or {}
                u = m.get("usage")
                if not u or not d.get("timestamp") or ts(d["timestamp"]) < since:
                    continue
                mid = m.get("id") or d.get("requestId") or d.get("uuid")
                if mid in seen:
                    continue
                seen.add(mid)
                sid = d.get("sessionId") or f.stem
                model = m.get("model", "?")
                if model == "<synthetic>":
                    continue
                s = sessions.setdefault((sid, model), {"cwd": d.get("cwd"), "ts": d["timestamp"], "t": [0, 0, 0, 0]})
                t = s["t"]
                t[0] += u.get("input_tokens", 0)
                t[1] += u.get("cache_read_input_tokens", 0)
                t[2] += u.get("cache_creation_input_tokens", 0)
                t[3] += u.get("output_tokens", 0)
                s["ts"] = min(s["ts"], d["timestamp"])
    for (sid, model), s in sessions.items():
        yield sid, short_cwd(s["cwd"]), model, s["ts"], s["t"]


def codex_sessions(since):
    for f in CODEX.rglob("*.jsonl"):
        if datetime.fromtimestamp(f.stat().st_mtime, timezone.utc) < since:
            continue
        cwd = model = first = None
        last = None
        with f.open(errors="replace") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                p = d.get("payload") or {}
                if d.get("type") == "session_meta":
                    cwd, first = p.get("cwd"), p.get("timestamp") or d.get("timestamp")
                elif d.get("type") == "turn_context":
                    model = p.get("model") or model
                elif p.get("type") == "token_count" and p.get("info"):
                    last = p["info"].get("total_token_usage")
        if not last or not first or ts(first) < since:
            continue
        cached = last.get("cached_input_tokens", 0)
        t = [last.get("input_tokens", 0) - cached, cached,
             last.get("cache_write_input_tokens", 0), last.get("output_tokens", 0)]
        yield f.stem[-36:], short_cwd(cwd), model or "?", first, t


KB_NOTE_RE = re.compile(r"(?:general|personal|current|companies/[\w.-]+)/knowledge/[^\s'\"`|;)<>]+\.md")
KB_DIR_RE = re.compile(r"(?:~/ai\b|/ai/(?:general|personal|current|companies)\b|\b(?:general|personal|current|companies/[\w.-]+)/knowledge\b)")


def claude_tool_calls(since):
    """Yield (session_id, tool_name, input dict) for Claude tool_use blocks."""
    for f in CLAUDE.rglob("*.jsonl"):
        if datetime.fromtimestamp(f.stat().st_mtime, timezone.utc) < since:
            continue
        seen = set()
        with f.open(errors="replace") as fh:
            for line in fh:
                if '"tool_use"' not in line:
                    continue
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                if not d.get("timestamp") or ts(d["timestamp"]) < since:
                    continue
                content = (d.get("message") or {}).get("content")
                if not isinstance(content, list):
                    continue
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("id") not in seen:
                        seen.add(c.get("id"))
                        yield d.get("sessionId") or f.stem, c.get("name"), c.get("input") or {}


def codex_tool_calls(since, coverage=None):
    """Yield extracted shell calls; never execute code from the transcripts.

    JS wrappers are parsed in batches. Direct shell calls are decoded separately;
    unrelated tool arguments (e.g. apply_patch) are not shell commands.
    """
    coverage = coverage if coverage is not None else defaultdict(int)
    pending = []

    def flush():
        sources = [source for _, _, source in pending]
        for (sid, cwd, _), result in zip(pending, extract_shell_calls(sources)):
            coverage["wrappers"] += 1
            for key in ("exec_nodes", "unresolved", "parse_error", "unavailable"):
                coverage[key] += result[key]
            coverage["static"] += len(result["calls"])
            for call in result["calls"]:
                yield sid, "shell", {"command": call["cmd"],
                                     "cwd": call.get("workdir") or cwd}
        pending.clear()

    # Archived sessions can contain recent tool calls too.
    roots = [CODEX, CODEX.parent / "archived_sessions"]
    seen_files = set()
    for root in roots:
        for f in root.rglob("*.jsonl"):
            resolved = f.resolve()
            if resolved in seen_files:
                continue
            seen_files.add(resolved)
            if datetime.fromtimestamp(f.stat().st_mtime, timezone.utc) < since:
                continue
            cwd = str(HOME)
            seen_calls = set()
            with f.open(errors="replace") as fh:
                for line in fh:
                    try:
                        d = json.loads(line)
                    except ValueError:
                        continue
                    p = d.get("payload") or {}
                    if d.get("type") in ("session_meta", "turn_context"):
                        cwd = p.get("cwd") or cwd
                        continue
                    if d.get("type") != "response_item" or not d.get("timestamp"):
                        continue
                    if ts(d["timestamp"]) < since:
                        continue
                    typ = p.get("type")
                    if typ not in ("custom_tool_call", "function_call", "local_shell_call"):
                        continue
                    cid = p.get("call_id") or p.get("id")
                    if cid and cid in seen_calls:
                        continue
                    if cid:
                        seen_calls.add(cid)
                    name = p.get("name", "")
                    sid = f.stem[-36:]
                    if name in ("functions.exec", "exec") and typ == "custom_tool_call":
                        source = p.get("input")
                        if isinstance(source, str):
                            pending.append((sid, cwd, source))
                            if len(pending) >= 400:
                                yield from flush()
                        else:
                            coverage["invalid_calls"] += 1
                        continue
                    if typ == "local_shell_call":
                        args = p.get("action") or {}
                    elif name in ("exec_command", "functions.exec_command", "shell", "functions.shell", "shell_command", "functions.shell_command"):
                        args = p.get("arguments") if typ == "function_call" else p.get("input")
                        try:
                            args = json.loads(args) if isinstance(args, str) else args
                        except ValueError:
                            coverage["invalid_calls"] += 1
                            continue
                    else:
                        continue
                    if not isinstance(args, dict):
                        coverage["invalid_calls"] += 1
                        continue
                    cmd = args.get("cmd", args.get("command"))
                    if isinstance(cmd, list):
                        # local_shell_call uses argv; only unwrap known shell -c forms.
                        if len(cmd) >= 3 and Path(str(cmd[0])).name in ("bash", "sh", "zsh") and cmd[1] in ("-c", "-lc", "-ic"):
                            cmd = cmd[2]
                        else:
                            import shlex
                            cmd = shlex.join(cmd) if all(isinstance(x, str) for x in cmd) else None
                    if not isinstance(cmd, str):
                        coverage["invalid_calls"] += 1
                        continue
                    coverage["direct"] += 1
                    yield sid, "shell", {"command": cmd, "cwd": args.get("workdir") or args.get("cwd") or cwd}
    if pending:
        yield from flush()


def classify(name, inp):
    """Return (kind, [note paths]) or (None, [])."""
    if name == "Read":
        path = inp.get("file_path", "")
        if not KB_NOTE_RE.search(path):
            return None, []
        if path.endswith("INDEX.md"):
            return "index", [path]
        return ("partial" if inp.get("offset") or inp.get("limit") else "full"), [path]
    cmd = inp.get("command") if isinstance(inp.get("command"), str) else None
    if not cmd:
        return None, []
    if "kb_find.py" in cmd:
        return "kb_find", []
    notes = KB_NOTE_RE.findall(cmd)
    searching = re.search(r"\b(grep|rg|ugrep)\b", cmd)
    if not notes:
        return ("search", []) if searching and KB_DIR_RE.search(cmd) else (None, [])
    if any(n.endswith("INDEX.md") for n in notes):
        return "index", notes
    if re.search(r"\b(head|tail|sed -n|awk)\b", cmd):
        return "partial", notes
    if searching:
        return "search", notes
    if re.search(r"\b(cat|less|bat|more)\b", cmd):
        return "full", notes
    return None, []


def note_size(path):
    p = Path(os.path.expanduser(path))
    if not p.is_absolute():
        p = AI_ROOT / p
    try:
        return p.resolve().stat().st_size
    except OSError:
        return 0


def kb_report(since):
    kinds = ["kb_find", "search", "index", "full", "partial"]
    stats = defaultdict(lambda: defaultdict(int))
    sessions = defaultdict(set)
    full_notes = defaultdict(int)
    coverage = defaultdict(int)
    for agent, calls in (("claude", claude_tool_calls(since)),
                         ("codex", codex_tool_calls(since, coverage))):
        for sid, name, inp in calls:
            if agent == "codex":
                if not classification_status(inp["command"]):
                    coverage["shell_parse_error"] += 1
                entries = [(kind, [path] if path else []) for kind, path in
                           classify_command(inp["command"], inp["cwd"], str(AI_ROOT), str(HOME))]
            else:
                kind, notes = classify(name, inp)
                entries = [(kind, notes)] if kind else []
            for kind, notes in entries:
                stats[agent][kind] += 1
                sessions[agent].add(sid)
                if kind == "full":
                    for n in notes:
                        full_notes[n.split("knowledge/", 1)[-1]] += 1
                        stats[agent]["full_bytes"] += note_size(n)
    print("\nKnowledge-base access (heuristic, see --help):")
    print(f"{'agent':<7} {'sess':>4} " + " ".join(f"{k:>8}" for k in kinds) + f" {'full KiB':>8}")
    for agent in ("claude", "codex"):
        st = stats[agent]
        print(f"{agent:<7} {len(sessions[agent]):>4} " + " ".join(f"{st[k]:>8}" for k in kinds)
              + f" {st['full_bytes'] // 1024:>8}")
    print("Codex parser coverage: "
          f"{coverage['wrappers']} wrappers, {coverage['exec_nodes']} shell sites, "
          f"{coverage['static']} static calls, {coverage['direct']} direct calls; "
          f"{coverage['unresolved']} dynamic sites, {coverage['parse_error']} JS parse failures, "
          f"{coverage['unavailable']} wrappers unavailable, "
          f"{coverage['invalid_calls']} invalid calls, {coverage['shell_parse_error']} shell parse failures.")
    if any(coverage[k] for k in ("unresolved", "parse_error", "unavailable", "invalid_calls", "shell_parse_error")):
        print("Codex coverage is incomplete; excluded calls are not treated as zero KB access.")
    print("KB counts describe static requested reads; full KiB is a current-file-size estimate, not token usage.")
    print("Shell parsing is heuristic: dynamic paths, custom readers and runtime control flow may be missed.")
    if full_notes:
        print("Most read in full:")
        for n, c in sorted(full_notes.items(), key=lambda kv: -kv[1])[:5]:
            print(f"  {c:>3}x {n}")
    return stats


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--kb", action="store_true", help="add knowledge-base access statistics")
    ap.add_argument("--brief", action="store_true", help="print one summary line only")
    args = ap.parse_args()
    since = datetime.now(timezone.utc) - timedelta(days=args.days)

    rows = [("claude",) + r for r in claude_sessions(since)] + [("codex",) + r for r in codex_sessions(since)]
    if not rows:
        print(f"token-usage: no sessions in the last {args.days} days")
        return 1

    if args.brief:
        tot = [sum(r[5][i] for r in rows) for i in range(4)]
        n = {a: len({r[1] for r in rows if r[0] == a}) for a in ("claude", "codex")}
        print(f"token-usage {args.days}d: claude {n['claude']} / codex {n['codex']} sessions, "
              f"input {fmt(tot[0] + tot[1] + tot[2])} (cache read {fmt(tot[1])}), output {fmt(tot[3])}")
        return 0

    groups = defaultdict(lambda: [0, 0, 0, 0, set()])
    for agent, sid, cwd, model, _, t in rows:
        g = groups[(agent, cwd, model)]
        for i in range(4):
            g[i] += t[i]
        g[4].add(sid)

    hdr = f"{'agent':<7} {'project':<34} {'model':<20} {'sess':>4} {'fresh':>7} {'c.read':>7} {'c.write':>7} {'out':>7}"
    print(f"Token usage, last {args.days} days (since {since:%Y-%m-%d})")
    print(hdr)
    total = [0, 0, 0, 0]
    for (agent, cwd, model), g in sorted(groups.items(), key=lambda kv: -(kv[1][1] + kv[1][2] + kv[1][0])):
        print(f"{agent:<7} {cwd[-34:]:<34} {model[-20:]:<20} {len(g[4]):>4} "
              + " ".join(f"{fmt(g[i]):>7}" for i in range(4)))
        for i in range(4):
            total[i] += g[i]
    print(f"{'total':<63} {len({r[1] for r in rows}):>4} " + " ".join(f"{fmt(v):>7}" for v in total))

    print(f"\nTop {args.top} sessions by input (fresh + cache read + cache write):")
    by_sess = defaultdict(lambda: [0, 0, "", "", ""])
    for agent, sid, cwd, model, first, t in rows:
        s = by_sess[(agent, sid)]
        s[0] += t[0] + t[1] + t[2]
        s[1] += t[3]
        s[2], s[3], s[4] = cwd, first[:16].replace("T", " "), agent
    for (agent, sid), s in sorted(by_sess.items(), key=lambda kv: -kv[1][0])[:args.top]:
        print(f"  {s[3]}  {agent:<6} {fmt(s[0]):>7} in {fmt(s[1]):>6} out  {s[2]}  {sid[:8]}")
    if args.kb:
        kb_report(since)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
