#!/usr/bin/env python3
"""Lint the ~/ai knowledge base against the conventions in AGENTS.md.

Usage:
    kb_lint.py              check all layers, print findings, exit 1 on errors
    kb_lint.py --staged     check only files staged in git (used by ai-sync.sh)
    kb_lint.py --quiet      print only the summary line

Checks (E = error, W = warning):
  E frontmatter    missing block, or system/status/checked missing or malformed
  E log-name       knowledge/log/ file not named YYYY-MM-DD-<system>-<slug>.md
  W log-system     the <system> part of a log filename differs from frontmatter
  E link           relative or ~/ai link target does not exist
  E secret         token/password/private key pattern in any file
  E leak           company identifier in general/ (from companies/*/lint-identifiers.txt
                   plus private IP ranges and *.corp hosts)
  W language       more than 60 Cyrillic characters outside code blocks (notes are English)

Exit codes: 0 clean or warnings only, 1 errors found, 2 usage error.
"""
import argparse
import os
import pathlib
import re
import subprocess
import sys

AI_ROOT = pathlib.Path(os.environ.get("AI_ROOT", pathlib.Path.home() / "ai"))
STATUSES = {"verified", "hypothesis", "outdated"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LOG_NAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
SKIP_NAMES = {"INDEX.md", "README.md", "CONTEXT.md", "TODO.md", "AGENTS.md"}
SECRET_RES = [
    re.compile(p) for p in (
        r"glpat-[A-Za-z0-9_-]{15,}",                 # GitLab PAT
        r"gh[pousr]_[A-Za-z0-9]{30,}",               # GitHub tokens
        r"AKIA[0-9A-Z]{16}",                          # AWS access key
        r"hvs\.[A-Za-z0-9]{20,}",                     # Vault token
        r"xox[abpr]-[A-Za-z0-9-]{20,}",               # Slack
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        r"(?i)(password|passwd|secret|token)\s*[=:]\s*['\"](?![$<{%])[^'\"\s]{8,}['\"]",  # literal, not $VAR or <placeholder>
        r"eyJ[A-Za-z0-9_-]{20,}\.eyJ[A-Za-z0-9_-]{20,}",  # JWT
    )
]
DEFAULT_LEAK_RES = [
    re.compile(r"\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
    re.compile(r"\b192\.168\.\d{1,3}\.\d{1,3}\b"),
    re.compile(r"\b172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}\b"),
    re.compile(r"\b[a-z0-9.-]+\.corp\b"),
]
LEAK_ALLOW_RES = [re.compile(r"\b192\.168\.[01]\.1\b"), re.compile(r"\b172\.17\.0\.\d+\b")]  # home router, docker default bridge


def find_cause(text, regexes):
    for r in regexes:
        m = r.search(text)
        if m:
            return m.group(0)
    return None


def strip_code(text):
    out, code = [], False
    for line in text.splitlines():
        if line.startswith("```"):
            code = not code
            continue
        if not code:
            out.append(line)
    return "\n".join(out)


def parse_frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    meta = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return meta
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    return None


def load_leak_patterns():
    pats = list(DEFAULT_LEAK_RES)
    for f in AI_ROOT.glob("companies/*/lint-identifiers.txt"):
        for line in f.read_text(errors="replace").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                pats.append(re.compile(re.escape(line), re.I))
    return pats


def note_files(staged_only):
    if staged_only:
        out = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
                             cwd=AI_ROOT, capture_output=True, text=True, check=True).stdout
        files = [AI_ROOT / p for p in out.split() if p.endswith(".md")]
        return [f for f in files if f.exists()]
    files = []
    for layer in ("general", "personal"):
        files += (AI_ROOT / layer).rglob("*.md")
    files += (AI_ROOT / "companies").rglob("*.md")
    return [f for f in files if ".git" not in f.parts]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--staged", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    leak_res = load_leak_patterns()
    errors, warnings = [], []

    def err(f, code, msg):
        errors.append(f"E {code:<11} {f.relative_to(AI_ROOT)}: {msg}")

    def warn(f, code, msg):
        warnings.append(f"W {code:<11} {f.relative_to(AI_ROOT)}: {msg}")

    for f in sorted(set(note_files(args.staged))):
        text = f.read_text(errors="replace")
        rel = f.relative_to(AI_ROOT)
        is_note = f.name not in SKIP_NAMES and "knowledge" in rel.parts and f.parent != AI_ROOT

        # secrets: every markdown file
        hit = find_cause(text, SECRET_RES)
        if hit:
            err(f, "secret", f"looks like a credential: {hit[:12]}...")

        # leaks: general layer only
        if rel.parts[0] == "general" and f.name not in SKIP_NAMES:
            # code blocks count too: recipes must be publishable as is
            for r in leak_res:
                m = r.search(text)
                if m and not any(a.search(m.group(0)) for a in LEAK_ALLOW_RES):
                    err(f, "leak", f"company identifier '{m.group(0)}'")
                    break

        if not is_note:
            continue

        # frontmatter
        meta = parse_frontmatter(text)
        if meta is None:
            err(f, "frontmatter", "missing frontmatter block")
        else:
            if not meta.get("system"):
                err(f, "frontmatter", "system is missing")
            if meta.get("status") not in STATUSES:
                err(f, "frontmatter", f"status must be one of {sorted(STATUSES)}, got {meta.get('status')!r}")
            if not DATE_RE.match(meta.get("checked", "")):
                err(f, "frontmatter", f"checked must be YYYY-MM-DD, got {meta.get('checked')!r}")

        # log filename
        if "log" in rel.parts and rel.parts[rel.parts.index("log") - 1] == "knowledge":
            m = LOG_NAME_RE.match(f.name)
            if not m:
                err(f, "log-name", "expected YYYY-MM-DD-<system>-<slug>.md, lowercase, no dots")
            elif meta and meta.get("system") and not m.group(2).startswith(meta["system"]):
                warn(f, "log-system", f"filename does not start with system '{meta['system']}'")

        # links
        for m in re.finditer(r"\]\(([^)\s#]+)(#[^)]*)?\)", text):
            t = m.group(1)
            if re.match(r"^[a-z][a-z0-9+.-]*://", t) or t.startswith("mailto:"):
                continue
            p = pathlib.Path(os.path.expanduser(t)) if t.startswith(("~", "/")) else (f.parent / t)
            if not p.exists():
                err(f, "link", f"target not found: {t}")

        # language
        cyr = len(re.findall(r"[А-Яа-яЁё]", strip_code(text)))
        if cyr > 60:
            warn(f, "language", f"{cyr} Cyrillic characters outside code blocks")

    if not args.quiet:
        for line in errors + warnings:
            print(line)
    print(f"kb-lint: {len(errors)} errors, {len(warnings)} warnings"
          + (" (staged files only)" if args.staged else ""))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
