#!/usr/bin/env python3
"""Repeat fixed KB questions after retrieval changes; real cases stay outside general/.

kb_benchmark.py --cases ~/ai-data/kb-retrieval/suite-v2.json --output-dir /tmp/kb-check
Exit 0: completed and enforced checks passed; 1: regression; 2: invalid suite/tool failure.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys
import time

ROOT = Path(os.environ.get("AI_ROOT", Path.home() / "ai")).resolve()


def normalized(value):
    return " ".join(value.casefold().split())


def check_definition(case):
    return {"answer_anchors": case["answer_anchors"],
            "required_decision": case.get("required_decision"),
            "require_answer": case.get("require_answer", False)}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def corpus():
    return {str(p.relative_to(ROOT)): sha(p) for layer in ("general", "personal", "current")
            for p in sorted((ROOT / layer / "knowledge").resolve().rglob("*.md"))
            if p.name not in {"INDEX.md", "README.md"}}


def load_cases(path):
    suite = json.loads(path.read_text())
    if not isinstance(suite, dict) or suite.get("schema_version") != 2:
        raise ValueError("expected suite schema_version 2 with stable text anchors")
    cases = suite["cases"]
    if not isinstance(cases, list) or not cases or len({c["id"] for c in cases}) != len(cases):
        raise ValueError("empty suite or duplicate case IDs")
    for c in cases:
        if not isinstance(c["id"], str) or not c["id"].strip():
            raise ValueError("case IDs must be nonempty strings")
        if "require_answer" in c and not isinstance(c["require_answer"], bool):
            raise ValueError("require_answer must be boolean")
        if "required_decision" in c:
            required = c["required_decision"]
            if not isinstance(required, dict) or not all(isinstance(required.get(k), str) and required[k].strip()
                    for k in ("state", "scope_contains", "summary_contains")):
                raise ValueError("required_decision needs nonempty state/scope/summary checks")
        target = (ROOT / c["expected_path"]).resolve()
        if ROOT not in target.parents or not target.is_file():
            raise ValueError("invalid expected path for " + c["id"])
        text = normalized(target.read_text())
        if not isinstance(c.get("answer_anchors"), list) or not c["answer_anchors"] or not all(isinstance(a, str) and a.strip() and normalized(a) in text for a in c["answer_anchors"]):
            raise ValueError("answer anchor missing from source for " + c["id"])
        if not isinstance(c.get("queries"), dict) or not c["queries"] or any(not isinstance(q, list) or not q or not all(isinstance(t, str) and t.strip() for t in q) for q in c["queries"].values()):
            raise ValueError("invalid queries for " + c["id"])
        if c.get("layer") not in {"general", "personal", "current"}:
            raise ValueError("invalid layer for " + c["id"])
    return suite


def evaluate(case, output):
    target = "~/ai/" + case["expected_path"]
    rank = next((i for i, r in enumerate(output["results"], 1) if r["path"] == target), None)
    found = output["results"][rank - 1] if rank else None
    # Check the actually rendered/clipped text, not the source line number.
    visible = normalized("\n".join(s["text"] for s in found["snippets"])) if found else ""
    answer = any(normalized(a) in visible for a in case["answer_anchors"])
    expected = case.get("required_decision")
    decision_ok = None
    if expected:
        d = found.get("decision") if found else None
        decision_ok = bool(d and d.get("state") == expected["state"] and d.get("source") and
                           d.get("source_line") and normalized(expected["summary_contains"]) in normalized(d.get("summary", "")) and
                           normalized(expected["scope_contains"]) in normalized(d.get("scope", "")))
    return {"rank_top5": rank, "answer_visible": answer, "decision_visible": decision_ok,
            "target_section": found.get("section", {}).get("heading") if found and found.get("section") else None,
            "result_paths": [r["path"] for r in output["results"]],
            "snippet_lines": [s["line"] for s in found["snippets"]] if found else []}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cases", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    ap.add_argument("--search-script", type=Path, default=Path(__file__).with_name("kb_find.py"))
    ap.add_argument("--repeats", type=int, default=1)
    ap.add_argument("--lines", type=int, default=5)
    ap.add_argument("--baseline", type=Path, help="previous results.json for per-condition regression checks")
    ap.add_argument("--enforce", action="store_true", help="require configured checks on scoped operational queries")
    args = ap.parse_args()
    if args.repeats < 1 or args.lines < 0:
        ap.error("repeats must be positive and lines nonnegative")
    try:
        cases_hash = sha(args.cases)
        suite = load_cases(args.cases)
        if args.enforce and any("operational" not in c["queries"] for c in suite["cases"]):
            raise ValueError("--enforce requires operational queries for every case")
        if args.output_dir.exists():
            raise ValueError("output directory already exists; choose a fresh path")
        args.output_dir.mkdir(parents=True)
        before = corpus()
        script_hash = sha(args.search_script)
        previous = {}
        if args.baseline:
            previous = {(r["id"], r["variant"], r["mode"]): r for r in json.loads(args.baseline.read_text())}
            if any("check_definition" not in r for r in previous.values()):
                raise ValueError("baseline lacks frozen check definitions; create an explicitly reviewed v2 baseline")
        rows = []
        regressions = []
        for c in suite["cases"]:
            for variant, query in c["queries"].items():
                for mode in ("default_and", "scoped_and"):
                    cmd = [sys.executable, str(args.search_script), "--json", "-m", "5", "-n", str(args.lines)]
                    if mode == "scoped_and":
                        cmd += ["-l", c["layer"]]
                    cmd += query
                    timings = []
                    first = None
                    for _ in range(args.repeats):
                        start = time.perf_counter()
                        p = subprocess.run(cmd, text=True, capture_output=True, timeout=30)
                        timings.append((time.perf_counter() - start) * 1000)
                        if p.returncode not in {0, 1} or p.stderr.strip():
                            raise ValueError("search failed for " + c["id"] + "/" + variant)
                        result = json.loads(p.stdout)
                        if bool(result["total_matches"]) != (p.returncode == 0):
                            raise ValueError("inconsistent search exit code")
                        if first is not None and result != first:
                            raise ValueError("nondeterministic search results")
                        first = result
                    row = dict(id=c["id"], expected_path=c["expected_path"], check_definition=check_definition(c), variant=variant, mode=mode, query=query,
                               total_matches=result["total_matches"], latency_ms=timings,
                               output_bytes=len(p.stdout.encode()), **evaluate(c, result))
                    rows.append(row)
                    prev = previous.get((c["id"], variant, mode))
                    if prev:
                        if prev["check_definition"] != check_definition(c):
                            raise ValueError("baseline answer or decision definition differs for " + c["id"])
                        if prev["query"] != query or prev.get("expected_path", c["expected_path"]) != c["expected_path"]:
                            raise ValueError("baseline query or target differs for " + c["id"])
                        for key in ("answer_visible", "decision_visible"):
                            if prev.get(key) and not row.get(key):
                                regressions.append(c["id"] + "/" + variant + "/" + mode + ": lost " + key)
                        if prev.get("rank_top5") and not row["rank_top5"]:
                            regressions.append(c["id"] + "/" + variant + "/" + mode + ": lost target")
                    if args.enforce and variant == "operational" and mode == "scoped_and":
                        if not row["rank_top5"]:
                            regressions.append(c["id"] + ": target missing")
                        if c.get("require_answer") and not row["answer_visible"]:
                            regressions.append(c["id"] + ": required answer not visible")
                        if c.get("required_decision") and not row["decision_visible"]:
                            regressions.append(c["id"] + ": required decision not visible")
        if before != corpus() or script_hash != sha(args.search_script):
            raise ValueError("corpus or search script changed during measurement")
        if cases_hash != sha(args.cases):
            raise ValueError("case suite changed during measurement")
        missing = set(previous) - {(r["id"], r["variant"], r["mode"]) for r in rows}
        if missing:
            raise ValueError("baseline conditions removed from suite")
        groups = []
        for variant in sorted({v for c in suite["cases"] for v in c["queries"]}):
            for mode in ("default_and", "scoped_and"):
                group = [r for r in rows if r["variant"] == variant and r["mode"] == mode]
                groups.append({"variant": variant, "mode": mode, "n": len(group),
                    "top1": sum(r["rank_top5"] == 1 for r in group),
                    "top5": sum(r["rank_top5"] is not None for r in group),
                    "answers": sum(r["answer_visible"] for r in group),
                    "decisions": sum(r["decision_visible"] is True for r in group),
                    "median_ms": round(statistics.median(t for r in group for t in r["latency_ms"]), 2)})
        manifest = {"schema_version": 2, "cases_sha256": cases_hash, "script_sha256": script_hash,
                    "script": str(args.search_script), "corpus": before, "python": sys.version,
                    "lines": args.lines, "repeats": args.repeats, "corpus_unchanged": True,
                    "scope": "Constructed queries; no spontaneous agent query preparation evaluated."}
        for filename, value in (("manifest.json", manifest), ("results.json", rows),
                                ("summary.json", {"groups": groups, "regressions": regressions}), ("cases.json", suite)):
            (args.output_dir / filename).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({"conditions": len(rows), "groups": groups, "regressions": regressions}, ensure_ascii=False, indent=2))
        return 1 if regressions else 0
    except (ValueError, OSError, KeyError, TypeError, subprocess.TimeoutExpired) as e:
        print("kb-benchmark: error: " + str(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
