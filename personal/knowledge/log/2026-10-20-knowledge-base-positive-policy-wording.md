---
system: knowledge-base
status: verified
checked: 2026-10-20
tags: [agents, agnix, policy]
---
# Knowledge base: positive policy wording with PE-006 retained

## Task

User requested implementation and verification of positive wording for the three
historical PE-006 findings, retaining the rule and the underlying restrictions.

## Context and findings

Canonical policy: `~/ai/AGENTS.md`; Claude and Codex global aliases resolve to this file.
The [original warning audit](2026-10-20-knowledge-base-lint-warning-review.md) recorded
three findings before the previous instruction shortening. The pre-edit baseline in this
task already had no PE-006 findings:9files,0errors,1warning,2informational findings.
The earlier conversational explanation relied on the historical audit, not a current scan.

## Changes

Reworded secret handling, necessary personal data and Git authorization as explicit permitted
actions. Secret values remain excluded from notes/scripts/logs; user access values belong
only in the layer .env; discovered secret locations, variable names and access routes can
be recorded. Git changes still require an explicit request in the current task, with the
same daily-sync and confirmed-training exceptions and both supervised approval gates.
No linter rule, suppression, agent setting, publication or external service was changed.

## Verification

- Forced agent lint:9files,0errors,1warning,2informational findings; PE-006 absent.
- Isolated temporary CLAUDE.md control with a negative-only instruction produced PE-006.
  The updated policy produced no PE-006 using the same binary and CLI options, including
  --ignore-inline-suppressions. This confirms the rule remains active.
- Full KB lint:0errors,0warnings. Shared instructions remain below the size threshold.
- Reviewed the narrow policy edit for preserved restrictions and exceptions.

## Status and risks

Completed. Remaining CDX-CFG-025 concerns unchanged Codex service_tier; AGM-004 and
CDX-AG-008 remain informational. These are separate from the requested three warnings.
No open follow-up arose for this task; related completed TODO records stay unchanged.
Static lint verifies warning behavior, not future model compliance.

## Portable lesson

None; canonical policy remains in AGENTS.md.
