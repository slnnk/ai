---
system: knowledge-base
status: verified
checked: 2026-10-19
tags: [todo, agents, automation]
---
# Knowledge base: deterministic TODO output

## Task

Standardize backlog replies across agents and support the short requests `todo` and
`задачи`, following the user's implementation request.

## Context

The shared backlog had storage rules but no presentation contract. Agents could choose
different subsets or paraphrase tasks. Codex, Claude Code and Gemini instruction files
already link to the same `~/ai/AGENTS.md`.

## Actions

Added a dependency-free Python renderer, a shared invocation rule and a documented
output contract. Default output contains every unchecked item in file order, original
wording and dates, heading paths and clickable source links. Explicit subset filters
use case-insensitive literal substring matching; listing grants no execution permission.

Key checks:
- `python3 -m unittest discover -s ~/ai/general/scripts/tests -p test_todo.py -v`:
  six tests passed (exact output, grouping, continuations, fenced examples, filters,
  links, empty results and CLI read failures).
- Live backlog audit: 138 unchecked items matched 138 rendered items; repeated renders
  were byte-identical, 47,744 bytes. No tasks were rewritten or closed.
- `python3 ~/ai/general/scripts/agent_lint.py --force`: nine files, zero errors,
  four warnings and two informational findings; diagnostics cover existing credential
  wording, Codex configuration and instruction-file size/loading metadata.
- `kb_lint.py`: zero errors, six warnings (existing instruction size and older company
  note language). `build_index.py` refreshed the personal index. Scoped `git diff --check`
  passed; the broader check found an unrelated trailing blank line in a tracing map,
  which was preserved.

## Findings

Superseded presentation contract: the user subsequently requested concise Russian bullet
descriptions without dates, source links or checkboxes. See [current display](2026-10-19-knowledge-base-todo-russian-display.md).
The earlier verbatim-output behavior below records the original implementation only.

The same script produces the complete Markdown response for all supported agents.
Completed entries are excluded even when mixed into active sections. Missing or unreadable
input returns an error rather than an empty list. Runtime is compatible with local Python 3.8.

## Changes

- `~/ai/general/scripts/todo.py`
- `~/ai/general/scripts/tests/test_todo.py`
- `~/ai/AGENTS.md`, Backlog section
- `~/ai/general/knowledge/README.md`, script registry and TODO output contract
- Explicit preference evidence: [learning record](2026-10-19-knowledge-base-agent-learning-record-deterministic-todo-output-6e6f49793b9a5cca0b27.md), linked to the shared instruction rule

## Risks and reconciliation

The current backlog is verbose, so complete output is lengthy by design. Automatic
instruction loading in every fresh agent session was not behaviorally tested here;
shared instruction symlinks were checked. The Knowledge base backlog section was
reviewed: this request has no existing open item, no new open action remains, and
unrelated entries are unchanged. Optional backlog cleanup was not implemented.

## Portable lesson

none
