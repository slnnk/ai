#!/usr/bin/env python3
"""Create a knowledge-base note with the right path, name and frontmatter.

Usage:
    new_note.py log <system> <slug> [--layer current|personal] [--date YYYY-MM-DD] [--title T]
    new_note.py system <system> [<topic>] [--layer current|personal] [--title T]
    new_note.py recipe <technology> <slug> [--title T]
    new_note.py ... --status hypothesis      (default: verified)
    new_note.py ... --tags a,b,c

Examples:
    new_note.py log nomad-test agent-01-disk-full
        -> ~/ai/current/knowledge/log/2026-09-24-nomad-test-agent-01-disk-full.md
    new_note.py system nomad-test            -> ~/ai/current/knowledge/systems/nomad-test.md
    new_note.py system nomad-test nginx      -> ~/ai/current/knowledge/systems/nomad-test/nginx.md
    new_note.py recipe docker dind-flag-conflict
        -> ~/ai/general/knowledge/docker/dind-flag-conflict.md

Prints the created path. Refuses to overwrite an existing file (exit 1). Never edits
existing notes; open them directly instead.
"""
import argparse
import datetime as dt
import os
import pathlib
import re
import sys

AI_ROOT = pathlib.Path(os.environ.get("AI_ROOT", pathlib.Path.home() / "ai"))
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

LOG_BODY = """## Task

## Context

## Actions

## Findings

## Changes

## Open items

## Portable lesson

none
"""

SYSTEM_BODY = """## Purpose

## Components

## Delivery path

## Control points

## Operations

## Boundaries

## Access

Route only (bastion, VPN, inventory, role, vault path). Never the secret.
"""

RECIPE_BODY = """## Symptom

## Cause

## Fix

## Limits
"""


def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s


def check_slug(value, what):
    if not SLUG_RE.match(value):
        sys.exit(f"new_note: {what} must be lowercase kebab-case without dots, got {value!r} "
                 f"(suggestion: {slugify(value)})")


def frontmatter(system, status, checked, tags):
    tag_line = f"tags: [{', '.join(tags)}]\n" if tags else "tags: []\n"
    return f"---\nsystem: {system}\nstatus: {status}\nchecked: {checked}\n{tag_line}---\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", choices=["log", "system", "recipe"])
    ap.add_argument("system", help="system name (log/system) or technology (recipe)")
    ap.add_argument("slug", nargs="?", help="slug (log/recipe) or topic (system)")
    ap.add_argument("--layer", default="current", choices=["current", "personal"])
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--title")
    ap.add_argument("--status", default="verified", choices=["verified", "hypothesis", "outdated"])
    ap.add_argument("--tags", default="")
    a = ap.parse_args()

    check_slug(a.system, "system")
    if a.slug:
        check_slug(a.slug, "slug")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", a.date):
        sys.exit("new_note: --date must be YYYY-MM-DD")
    tags = [t.strip() for t in a.tags.split(",") if t.strip()]

    if a.kind == "log":
        if not a.slug:
            sys.exit("new_note: log needs <system> <slug>")
        path = AI_ROOT / a.layer / "knowledge" / "log" / f"{a.date}-{a.system}-{a.slug}.md"
        title = a.title or f"{a.system}: {a.slug.replace('-', ' ')}"
        body = LOG_BODY
    elif a.kind == "system":
        base = AI_ROOT / a.layer / "knowledge" / "systems"
        if a.slug:
            if (base / f"{a.system}.md").exists():
                sys.exit(f"new_note: {base / (a.system + '.md')} exists; a system is either one file or one directory")
            path = base / a.system / f"{a.slug}.md"
            title = a.title or f"{a.system}: {a.slug.replace('-', ' ')}"
        else:
            if (base / a.system).is_dir():
                sys.exit(f"new_note: {base / a.system}/ exists; add a topic instead: new_note.py system {a.system} <topic>")
            path = base / f"{a.system}.md"
            title = a.title or a.system
        body = SYSTEM_BODY
    else:
        if not a.slug:
            sys.exit("new_note: recipe needs <technology> <slug>")
        if a.layer != "current":
            sys.exit("new_note: recipes always live in general/")
        path = AI_ROOT / "general" / "knowledge" / a.system / f"{a.slug}.md"
        title = a.title or a.slug.replace("-", " ")
        body = RECIPE_BODY

    if path.exists():
        sys.exit(f"new_note: {path} already exists; edit it instead")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(frontmatter(a.system, a.status, a.date, tags) + f"# {title}\n\n" + body, encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
