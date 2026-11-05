---
system: knowledge-base
status: verified
checked: 2026-11-05
tags: [sync, regression, agents]
---
# Sync stops when staged KB lint cannot complete

## Task

Implement only point 1 (F1) of the
[agent methodology review](2026-11-05-knowledge-base-agent-methodology-review.md):
stop sync when the staged KB checker fails. The user explicitly requested this fix.
Other review findings remain proposals; the entire `~/ai` repository is exempt from
the first repository approval gate. No publication was requested.

## Context

[ai-sync.sh](../../../general/scripts/ai-sync.sh) previously ignored the checker exit
status and only searched its output for `E secret`. Both ordinary findings and an
unhandled Python exception use exit 1, so checking the exit status alone would change
the existing report-only behavior or continue to accept failures.

## Actions

- Added isolated normal-sync tests using temporary files and a fake Git executable.
  Before the fix, five of the initial ten tests failed because publication continued.
- Capture the checker exit status immediately, require its exact final staged-summary
  line, and require exit 0 for zero errors or exit 1 for positive error counts.
- Reject missing/malformed/incomplete output, contradictory exit status and abnormal
  exits before commit, pull, push or success-date update. Print checker diagnostics.
- Preserve the staged index as prepared by sync, `.sync-notes` and the previous sync
  date on this new failure path. This does not restore staging from before `git add -A`.
- Use a fresh private temporary lint report; ordinary completed nonsecret findings
  remain report-only, and the existing detected-secret block remains active.
- Document the completion requirement in README Daily sync. No `kb_lint.py` changes.

## Findings

Verification:

- Twelve new regression tests passed: exception, absent script, incomplete output,
  abnormal status, both status/summary contradictions, post-summary exception,
  clean/warning/nonsecret/secret outcomes, and the real checker's clean output.
- Full general script suite: 117 tests passed.
- `bash -n general/scripts/ai-sync.sh` passed.
- `agent_lint.py --force`: 9 files, zero errors/warnings/info.
- Fixtures verify that checker failures invoke no commit/pull/push/reset and retain
  notes and the prior successful date. Git actions are mocked; no network is used.

The completion-summary format is now part of the sync/checker interface. A future
format change must update both sides and their regression coverage. Checking additional
secret file formats and unavailable KB roots remains outside this fix.

## Changes

- `general/scripts/ai-sync.sh`: validate successful checker completion.
- `general/scripts/tests/test_ai_sync_lint.py`: isolated sync regression coverage.
- `general/knowledge/README.md`: documented failure and findings behavior.
- Review status, central TODO, affected display title, index and final sync note.

Pre-existing README and other working-tree changes were preserved. No real commit,
push, MR or external state change was performed for this fix.

## Status and risks

F1 completed on 2026-11-05; remaining F2–F7 proposals are tracked in
[central TODO](../../../TODO.md), Knowledge base. This fix does not authorize them.
No background test processes or reviewer operations remain.

## Portable lesson

none
