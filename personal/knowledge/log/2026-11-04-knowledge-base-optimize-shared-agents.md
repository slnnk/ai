---
system: knowledge-base
status: verified
checked: 2026-11-04
tags: [agents, instructions, optimization]
---
# Knowledge base: optimize shared agent instructions

## Summary

At the user's request, reviewed the complete shared AGENTS.md and its referenced README
procedures. Reduced the entry point from 6240 to 5036 bytes (19.3 percent), leaving
596 bytes below the 5632-byte warning threshold. Required behaviors and permissions remain.

## Task and authorization

The user requested a complete review and optimization after the new progress/status rule
exceeded the size threshold. This authorized local knowledge-base instruction edits;
repository task changes, external operations and terminal notification settings were outside scope.

## Actions and findings

- Compared every original section against its replacement and existing README procedures.
- A read-only delegated review checked easy-to-lose requirements and ambiguities.
- Shortened duplicated prose and kept explicit read triggers for mandatory details.
- Moved detailed progress/status instructions into the README and retained the 30-second
  interval and final background-status check directly in AGENTS.md.
- Clarified that local-edit permission remains subject to repository approval gates and
  replaced the ambiguous training reference with the named README section.
- Retained both approval gates, their scope/exclusions, explicit superpowers activation,
  pre-staged/mixed-change protection, secret boundaries, TODO output and bookkeeping checks.

## Changes and validation

- Canonical instructions: [AGENTS.md](../../../AGENTS.md).
- Procedure details: [README](../../../general/knowledge/README.md), including the new
  `Progress and execution status` section.
- `agent_lint.py --force`: zero errors and warnings; two informational diagnostics.
- `kb_lint.py`: zero errors and warnings after instruction edits; size warning removed.
- Final KB lint and index rebuild are required after writing this log.

## Status and risks

Instruction optimization completed. No task follow-up needs a new TODO entry; historical
optimization entries remain valid dated evidence. Static checks establish size and format,
not future behavioral compliance. No Git publication or external changes were performed.
