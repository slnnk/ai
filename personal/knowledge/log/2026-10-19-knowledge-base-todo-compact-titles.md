---
system: knowledge-base
status: verified
checked: 2026-10-19
tags: [todo, agents, automation]
---
# Knowledge base: compact TODO titles and spacing

## Task

Correct the still-verbose TODO output and excessive spacing after the user's screenshot
and second feedback on slow chat output.

## Context

The prior Russian display contained full action descriptions and blank lines between
every task. It met the earlier language/metadata requirements but remained too lengthy.
The loaded rule said "concise" without a measurable bound; the renderer explicitly added
the unwanted blank lines. This was an insufficient presentation contract, not slow file IO.

## Actions

Replaced all 138 cached descriptions with short Russian action titles, typically 6–12
words. Added a hard 120-character validation limit; overlong titles require refresh rather
than automatic clipping. Removed blank lines between bullets within a group. Preserved
all open source items, ordering, useful IDs and explicit deferral/proposal labels; details
and full permission conditions remain in unchanged source TODO.

Updated AGENTS, the existing README display contract, tests and the same learning key.
The repeat is diagnosed from observed code and instructions: the prior rule was loaded,
but "concise" did not enforce short titles and spacing was unspecified. New regression
checks cover both spacing and the 120/121-character boundary.

## Findings

`python3 -m unittest discover -s ~/ai/general/scripts/tests -p test_todo.py -v`:
nine tests passed. Live audit retained all 138 tasks, maximum title length 101 characters,
no dates/source links/checkboxes, no inter-item blank lines. Output shrank from 24,188 to
10,930 characters (38,294 to 17,319 bytes), 199 lines. In-process render took 0.0052 seconds;
chat delivery latency was not measured. Original per-request full descriptions are no
longer generated; the cache is reused.

`agent_lint.py --force`: nine files, zero errors, four known warnings and two info
(PE-006 security/Git wording, CDX-CFG-025 schema mismatch and loading/size metadata).

## Changes

- `~/ai/general/scripts/todo.py` and `tests/test_todo.py`
- `~/ai/AGENTS.md`, `~/ai/general/knowledge/README.md`
- `~/ai-data/todo/display-ru.json` (derived presentation, outside Git)
- Existing correction evidence and prior display log linked to the current contract.

## Risks and reconciliation

Full chat output still contains 138 tasks; actual latency improvement is unmeasured.
Short titles intentionally omit implementation detail and never authorize execution.
Source TODO remains authoritative. Only task-related Knowledge base records were reviewed;
this request has no existing open entry and no remaining implementation action.

## Portable lesson

none
