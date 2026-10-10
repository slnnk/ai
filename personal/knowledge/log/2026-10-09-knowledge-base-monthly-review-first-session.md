---
system: knowledge-base
status: verified
checked: 2026-10-09
tags: [knowledge-base, automation, staleness]
---
# Knowledge base: monthly review proposal on first session, starting November

## Task

Offer the knowledge-base staleness review on the first agent session in each month,
regardless of calendar day. The user deferred the first actual review to November 2026.

## Context

The daily sync already generated monthly backlog items, but had no November start gate.
Its existing TODO marker suppressed proposals for a pre-created monthly item. Historical
September notes describe the original October schedule and remain historical evidence.

## Actions

Updated the monthly block of `general/scripts/ai-sync.sh` to use the current session
date and the month of `.last-sync`, starting in `2026-11`. Refresh a pre-created open item
instead of duplicating it, record the actual proposal date, and print an explicit offer
requiring user agreement. Preserve the daily sync, git publication and dated reminders.

Aligned `AGENTS.md` and `general/knowledge/README.md`; rescheduled the existing October
TODO entry to November without marking the review completed.

## Findings

`bash -n general/scripts/ai-sync.sh` passed. Seven isolated checks executed the actual
monthly block with temporary TODO/state files and a stub for the stale-note count:
October suppressed; first November session on November 3; existing November item refreshed
without duplication; later November session suppressed; first December session on December
7; no candidates; dry run. All passed. No real review, git or network action was executed
by these checks. A failed overall sync does not advance `.last-sync`, so a retry can print
the monthly offer again; successful later syncs in the same month do not repeat it.

## Changes

- `general/scripts/ai-sync.sh`: November start gate, first-month sync detection and TODO refresh.
- `AGENTS.md`: first-session monthly offer and explicit user agreement.
- `general/knowledge/README.md`: canonical schedule and no automatic review.
- `TODO.md`: first review scheduled for November; no stale count assumed in advance.

## Risks

The November proposal depends on an agent running `ai-sync.sh` as instructed. It is not
a calendar scheduler. No reminder is offered if the stale-note count is zero. The existing
daily sync state is per machine; separate workstations can each offer their first monthly
review. No manual commit of the knowledge-base repository was performed.

## Portable lesson

For monthly prompts tied to interactive use, compare the current month with the previous
successful run rather than testing for calendar day 1. Pre-created backlog entries should
not suppress the first prompt.
