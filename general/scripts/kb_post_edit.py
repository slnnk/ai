#!/usr/bin/env python3
"""Report KB lint findings after a supported file edit in Codex or Jcode."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
PATCH_PATH = re.compile(r"^\*\*\* (?:Add File|Update File|Move to): (.+)$", re.MULTILINE)
LINT_SUMMARY = re.compile(r"kb-lint: (\d+) errors, (\d+) warnings")
JCODE_EDIT_TOOLS = {"write", "edit", "multiedit", "apply_patch"}


def touched_paths(jcode):
    if jcode:
        if os.environ["JCODE_HOOK_TOOL_NAME"] not in JCODE_EDIT_TOOLS:
            return ()
        return os.environ.get("JCODE_HOOK_TOUCHED_PATHS", "").splitlines()

    event = json.load(sys.stdin)
    if event.get("tool_name") != "apply_patch":
        return ()
    patch = event["tool_input"]["command"]
    cwd = Path(event["cwd"])
    return (cwd / name for name in PATCH_PATH.findall(patch))


def kb_notes(paths):
    notes = set()
    for name in paths:
        path = Path(name).resolve()
        if ROOT not in path.parents or path.suffix != ".md" or not path.is_file():
            continue
        parts = path.relative_to(ROOT).parts
        if path == ROOT / "AGENTS.md" or parts[0] in {"general", "personal", "companies"} and ".git" not in parts:
            notes.add(path)
    return sorted(notes)


def feedback(text, jcode):
    if jcode:
        print(text)
    else:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": text,
        }}))


def main():
    jcode = "JCODE_HOOK_TOOL_NAME" in os.environ
    try:
        notes = kb_notes(touched_paths(jcode))
        if not notes:
            return
        result = subprocess.run(
            [sys.executable, str(ROOT / "general/scripts/kb_lint.py"),
             "--codes-only", "--paths", *map(str, notes)],
            env={**os.environ, "AI_ROOT": str(ROOT)},
            capture_output=True, text=True, timeout=4,
        )
    except (AttributeError, KeyError, TypeError, ValueError, OSError, RuntimeError, subprocess.TimeoutExpired):
        feedback("KB edit check could not complete. Run kb_lint.py for the edited notes.", jcode)
        return

    lines = result.stdout.splitlines()
    summary = LINT_SUMMARY.fullmatch(lines[-1]) if lines else None
    if summary is None or result.returncode != int(int(summary[1]) > 0):
        feedback("KB edit check could not complete. Run kb_lint.py for the edited notes.", jcode)
        return
    findings = [line for line in lines if line.startswith(("E ", "W "))]
    if findings:
        message = "\n".join(["KB lint findings in edited notes:", *findings[:12]])
        if len(findings) > 12:
            message += f"\n{len(findings) - 12} more findings. Run kb_lint.py --paths for details."
        feedback(message, jcode)


if __name__ == "__main__":
    main()
