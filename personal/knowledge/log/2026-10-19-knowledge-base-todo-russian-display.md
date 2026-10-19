---
system: knowledge-base
status: verified
checked: 2026-10-19
tags: [todo, agents, automation]
---
# Knowledge base: concise Russian TODO display

## Task

Apply the user's corrected TODO presentation: Russian descriptions, ordinary bullet
lists, no dates, source links or checkboxes. Retain the short `todo` and `задачи` triggers.

## Context

The earlier verbatim display was too lengthy in chat. The script itself took 0.075 seconds;
the previous full output was 47,744 bytes. The user explicitly replaced its display
requirements; source storage rules and execution permissions remain unchanged.

## Actions

Changed the renderer to use a derived Russian display cache under `~/ai-data/todo/`.
Prepared descriptions for all 138 open entries and 22 headings. Descriptions preserve
pending actions, identifiers, deferrals and permission limits while removing completed
history and source metadata. SHA-256 keys bind each description to the complete original
entry. A changed entry requires refresh; closed entries are never displayed from cache.

Updated shared AGENTS and the existing README contract. Added `--missing` JSON output
for agents to refresh only affected entries; no translation service or external API is
used. Recorded the correction under the existing `deterministic-todo-output` learning key.

## Findings

The presentation was subsequently tightened after user feedback: [compact titles and
spacing](2026-10-19-knowledge-base-todo-compact-titles.md) supersede the full descriptions
and inter-item blank lines recorded here. Russian language, source-keyed caching and
metadata omission remain active.

Seven behavioral tests passed, including exact Russian bullet output, source changes,
closed tasks, missing-cache refresh, filters and CLI errors. Live output contains all
138 entries with Russian descriptions, no ISO dates, source links or checkboxes:
38,294 bytes / 24,188 characters, 0.075 seconds. The full list remains lengthy; no
chat-generation latency improvement was independently measured.

`agent_lint.py --force`: nine files, zero errors, four existing warnings and two info.
Diagnostics remain the known PE-006 security/Git wording, CDX-CFG-025 configuration
schema mismatch and instruction-file size/loading metadata; no settings changed.

## Changes

- `~/ai/general/scripts/todo.py` and `tests/test_todo.py`
- `~/ai/AGENTS.md` and `~/ai/general/knowledge/README.md`
- Derived translations: `~/ai-data/todo/display-ru.json` (outside Git)
- Existing learning evidence and prior task log updated to supersede the old contract.

## Risks and reconciliation

The cache must be rebuilt on another machine; `--missing` documents the recovery route.
An agent-generated concise translation can lose nuance; source TODO remains authoritative.
Only display is changed: no task closed, no source task rewritten, no external action.
The affected Knowledge base TODO section has no outstanding item for this request;
no new open work remains. Optional backlog cleanup remains outside scope.

## Portable lesson

none
