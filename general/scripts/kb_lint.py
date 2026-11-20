#!/usr/bin/env python3
"""Lint the ~/ai knowledge base against the conventions in AGENTS.md.

Usage:
    kb_lint.py              check all layers, print findings, exit 1 on errors
    kb_lint.py --staged     check only files staged in git (used by ai-sync.sh)
    kb_lint.py --commit-message FILE  check a generated Git commit message for credentials
    kb_lint.py --quiet      print only the summary line

Checks (E = error, W = warning):
  E frontmatter    missing block, or system/status/checked missing or malformed
  E log-name       knowledge/log/ file not named YYYY-MM-DD-<system>-<slug>.md
  W log-system     the <system> part of a log filename differs from frontmatter
  E link           relative or ~/ai link target does not exist
  E secret         token/password/private key pattern in any file
  E leak           company identifier in general/ (from companies/*/lint-identifiers.txt
                   plus private IP ranges and *.corp hosts)
  W language       more than 60 Cyrillic characters outside code (notes are English)

Exit codes: 0 clean or warnings only, 1 errors found, 2 usage error.
"""
import argparse
import codecs
import os
import pathlib
import re
import subprocess
import sys

from kb_paths import DEFAULT_LAYERS, knowledge_dirs, markdown_files

AI_ROOT = pathlib.Path(os.environ.get("AI_ROOT", pathlib.Path.home() / "ai"))
STATUSES = {"verified", "hypothesis", "outdated"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LOG_NAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
SUMMARY_MIN_BYTES = 8 * 1024
AGENTS_MAX_BYTES = 5632
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
    prose = "\n".join(out)
    # Code spans close only with a backtick run of the same length. Unmatched
    # or escaped opening delimiters remain prose so they cannot hide warnings.
    runs = list(re.finditer(r"`+", prose))
    out, start, i = [], 0, 0
    while i < len(runs):
        opening = runs[i]
        pos = opening.start()
        while pos > 0 and prose[pos - 1] == "\\":
            pos -= 1
        if (opening.start() - pos) % 2:
            i += 1
            continue
        closing = next((j for j in range(i + 1, len(runs))
                        if len(runs[j].group()) == len(opening.group())), None)
        if closing is None:
            i += 1
            continue
        out.append(prose[start:opening.start()])
        out.append(" ")
        start = runs[closing].end()
        i = closing + 1
    out.append(prose[start:])
    return "".join(out)


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


def working_notes():
    for knowledge in knowledge_dirs(AI_ROOT, DEFAULT_LAYERS):
        # Validate the configured knowledge roots even though lint also checks
        # Markdown outside them and reads the company layer by its real path.
        with os.scandir(knowledge):
            pass
    for layer in ("general", "personal", "companies"):
        directory = AI_ROOT / layer
        if directory.exists() or directory.is_symlink():
            yield from markdown_files(directory)
    if (AI_ROOT / "AGENTS.md").exists():
        yield AI_ROOT / "AGENTS.md"


def git(*args):
    return subprocess.run(["git", *args], cwd=AI_ROOT, stdout=subprocess.PIPE, check=True,
                          env={**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"}).stdout


def staged_blobs():
    top = pathlib.Path(os.fsdecode(git("rev-parse", "--show-toplevel")[:-1]))
    if top.resolve() != AI_ROOT.resolve():
        raise ValueError(f"{AI_ROOT}: expected Git repository root")
    raw = git("diff", "--cached", "--raw", "--no-abbrev", "--no-renames",
              "--ita-invisible-in-index", "-z")
    entries = raw.split(b"\0")
    if entries[-1] or len(entries) % 2 != 1:
        raise ValueError("incomplete staged file inventory")
    for header, name in zip(entries[0:-1:2], entries[1::2]):
        _, mode, _, oid, status = header.split()
        path = AI_ROOT / os.fsdecode(name)
        if status == b"D":
            continue
        if status not in (b"A", b"M", b"T"):
            raise ValueError(f"{str(path)!r}: cannot inspect index entry ({os.fsdecode(status)})")
        # A gitlink stores a commit ID and has no file contents in this repo.
        if mode == b"160000":
            yield path, mode, None
            continue
        try:
            yield path, mode, git("cat-file", "blob", oid.decode("ascii"))
        except subprocess.CalledProcessError as error:
            raise ValueError(f"{str(path)!r}: cannot read staged blob") from error


def decode_blob(blob):
    if blob.startswith((codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE)):
        return blob.decode("utf-32", errors="replace")
    if blob.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        return blob.decode("utf-16", errors="replace")
    return blob.decode("utf-8-sig", errors="replace")


def lint_inputs(staged, report_secret):
    if not staged:
        for path in sorted(set(working_notes())):
            text = path.read_text(errors="replace")
            if find_cause(text, SECRET_RES):
                report_secret(path, "looks like a credential")
            yield path, text
        return
    for path, mode, blob in staged_blobs():
        if path.name == ".env":
            report_secret(path, ".env files must not be staged")
        if blob is None:
            continue
        text = decode_blob(blob)
        if find_cause(text, SECRET_RES):
            report_secret(path, "looks like a credential")
        if path.suffix == ".md" and mode != b"120000":
            yield path, text


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    inputs = ap.add_mutually_exclusive_group()
    inputs.add_argument("--staged", action="store_true")
    inputs.add_argument("--commit-message", type=pathlib.Path)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if args.commit_message is not None:
        try:
            text = decode_blob(args.commit_message.read_bytes())
        except OSError:
            print("kb-lint: cannot read generated commit message", file=sys.stderr)
            return 2
        if find_cause(text, SECRET_RES):
            print("E secret      generated commit message: looks like a credential", file=sys.stderr)
            return 1
        return 0

    leak_res = load_leak_patterns()
    errors, warnings = [], []

    def err(f, code, msg):
        errors.append(f"E {code:<11} {f.relative_to(AI_ROOT)}: {msg}")

    def warn(f, code, msg):
        warnings.append(f"W {code:<11} {f.relative_to(AI_ROOT)}: {msg}")

    def report_secret(path, message):
        # Escape newlines/control characters and never show credential bytes.
        errors.append(f"E secret      {str(path.relative_to(AI_ROOT))!r}: {message}")

    for f, text in lint_inputs(args.staged, report_secret):
        rel = f.relative_to(AI_ROOT)
        is_note = f.name not in SKIP_NAMES and "knowledge" in rel.parts and f.parent != AI_ROOT

        if f == AI_ROOT / "AGENTS.md" and len(text.encode()) > AGENTS_MAX_BYTES:
            warn(f, "size", f"{len(text.encode())} bytes, over {AGENTS_MAX_BYTES}; move details to "
                            "general/knowledge/README.md or CONTEXT.md")

        # leaks: general layer only
        if rel.parts[0] == "general" and (f.name == "README.md" or f.name not in SKIP_NAMES):
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
            # Scoped decisions are independent of the note's evidence status.
            from kb_find import decision
            try:
                decision(meta, f, AI_ROOT)
            except (ValueError, OSError) as e:
                err(f, "decision", str(e))

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

        # summary: long maps and recipes are read on every task; logs are not
        if (len(text.encode()) > SUMMARY_MIN_BYTES and "log" not in rel.parts
                and f.name != "repos.md"
                and not re.search(r"^## Summary\b", text, re.M)):
            warn(f, "summary", f"{len(text.encode()) // 1024} KB and no '## Summary' section")

        # language
        cyr = len(re.findall(r"[А-Яа-яЁё]", strip_code(text)))
        if cyr > 60:
            warn(f, "language", f"{cyr} Cyrillic characters outside code blocks and inline code")

    if not args.quiet:
        for line in errors + warnings:
            print(line)
    print(f"kb-lint: {len(errors)} errors, {len(warnings)} warnings"
          + (" (staged files only)" if args.staged else ""))
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"kb-lint: error: {error}", file=sys.stderr)
        sys.exit(2)
