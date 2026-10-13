---
system: knowledge-base
status: verified
checked: 2026-10-12
tags: [agents, sync, backlog, audit]
---
# Knowledge base two week agent behaviour and daily sync review

## Summary

For 2026-09-28 through 2026-10-11 inclusive, all 11 daily sync commits contain substantive work records. Central backlog discipline is partly effective: most explicit follow-up sections redirect to TODO or record no open work, but separate lists have become stale. Four notes were reconciled and two optional proposals moved to decision items in the central backlog. No stronger skill workflow is justified by this evidence alone.

## Task and context

Complete the due 2026-10-12 observation proposed on 2026-09-23 and extended on 2026-09-28. The criteria were a non-empty "Work recorded by agents" section when "Files" is non-empty, and tracking new open items in `~/ai/TODO.md` rather than only in notes. Scope is the knowledge-base process across agents, not a complete operational permission or secret-handling audit.

## Actions and evidence

Ran the normal daily `ai-sync.sh`; it returned without output because today's sync was already recorded. Inspected `TODO.md`, company context, README daily-sync policy, scripts and read-only git history. Delegated the multi-file commit and note reviews as required by AGENTS.md. Key checks: `git -C ~/ai log --since=2026-09-28T00:00:00 --until=2026-10-12T00:00:00`, commit bodies/diffs, historical TODO snapshots, `kb_lint.py`, and `build_index.py`.

The commit review covers all 11 message bodies and selected diffs. The backlog review covers 61 log notes dated within the period, including 20 explicit follow-up sections. Current and historical TODO were compared for candidate omissions.

## Sync findings

| Measure | Result |
| --- | --- |
| Sync commits dated September 28 through October 11 | 11 |
| Commits with substantive work records | 11 of 11 |
| Recorded work lines | 201 |
| File changes across commits | 163, including 17 index changes |
| Text diff total | +7176 / -542 |
| Empty or index-only commits | 0 |

Examples: `07d0908` (September 30) records the deployment-lock cause, stages and 23-consumer checks; `942f7f9` (October 6) records corrections to fastlane findings and monitoring gaps; `67ed9fd` (October 9) records Git/MR approval rules and preservation of unrelated changes; `a69e917` (October 11) distinguishes verified recovery, hypotheses and unapplied proposals.

One exact duplicate work line was found in `c615a26` (October 8), about `gitlab-ci-templates 6d9b695` and TTL preparation. `86bad9b` (October 1) added three generated `.pyc` files. Messages can be too long: `7ee86c8` (October 10) has 47 work lines, often recording successive stages of the same task. A concise final result, reason/check and remaining risk would make the daily summary easier to read; detailed approvals belong in task logs.

Commit date differs from work date because sync runs at the start of a subsequent task and then exits on later successful calls that day. September 26 work was committed on September 28; September 28 work on September 30; October 2 work on October 5. Missing commit dates September 29, October 3 and October 4 do not establish missing sync runs.

For October 11 work, separately inspected `bfd3181` (October 12 at 00:01, 56 work lines and changes to 14 October 11 logs) and `210ea98` (October 12 at 10:59, two additional Nexus work lines). These are excluded from the 11-commit/201-line totals above.

Script inspection found that `ai_sync_message.py` permits Files-only messages; it did not produce one in this sample. The script has no duplicate or system-coverage check. `ai-sync.sh --dry-run` currently rebuilds indexes and runs `git add -A`/`git reset`, despite promising no changes. This was found by inspection, not by executing dry-run. Script changes are separate backlog work.

## Backlog findings

Of 20 explicit follow-up sections, 10 redirect to TODO, four state there is no open work, and six contain separate lists. This is evidence of a reconciliation problem, not a demonstrated loss of mandatory user tasks.

| Note | Finding before reconciliation |
| --- | --- |
| [RabbitMQ signin](~/ai/current/knowledge/log/2026-10-07-rabbitmq-test5-signin-exchange-auto-delete-mismatch.md) | Still prescribed deletion after the October 7 completed fix. Broader exchange checking remained an untracked proposal. |
| [Hangfire shutdown](~/ai/current/knowledge/log/2026-10-01-youdo-business-worker-hard-kill-hangfire-lock.md) | Startup-lock improvement remained open in the note, although TODO closed it on October 1 without separate action, with recurrence as the reopening condition. Historical TODO confirms it was tracked. |
| [Cerberus](~/ai/current/knowledge/log/2026-09-30-cerberus2-readonly-transaction-check.md) | Follow-up diagnostics persisted after the user's October 1 decision to stop further work. |
| [RP consolidation](~/ai/current/knowledge/log/2026-09-30-rp-rp-skill-consolidation.md) | Optional deletion of the obsolete local copy remained only in the note. |

The deletion and broader exchange check have no established user authorization or present necessity; they are now decision items, not instructions to execute. Earlier policy allowed dated snapshots in notes; by snapshot `86bad9b` the policy prohibited independent TODO lists. The October 7 RabbitMQ list therefore shows that stronger wording alone did not eliminate stale follow-ups.

## Changes and disposition

Closed the original observation reminder in `~/ai/TODO.md` with this report as evidence. Replaced the four proven stale or untracked lists above with dated status and central-backlog references, preserving completed work and user decisions. Added decision items for the two optional proposals, a possible final note-to-TODO reconciliation check, sync-summary/generated-file improvements, and a separate dry-run defect fix. Created this log and rebuilt indexes; appended a what-and-why sync note.

The existing AGENTS.md already requires a single backlog. No extra skill or duplicate rule was introduced; the audit supports checking reconciliation at task completion before expanding instructions. No manual git state changes, deletions, publication or infrastructure mutations were performed by this review.

## Validation and limits

After edits, `kb_lint.py` reports zero errors and six existing warnings: AGENTS.md size and five older notes with Cyrillic prose. `build_index.py` rebuild and `--check` succeed. The review introduces no additional warnings.

Notes are agent self-reports. Log-note dates do not cover every file changed during the period, and some October 11 notes were updated on October 12. Commit bodies cannot establish every sync invocation, failed push, task-to-summary completeness, permission compliance or absence of secret leaks in raw sessions. No claim about those behaviours is made. The token-cost comparison due October 14, Git training review due October 30 and November staleness review remain separate.

## Portable lesson

A single backlog needs reconciliation at task completion: a completed decision in TODO can coexist with obsolete action wording in a dated log. A non-empty daily work section establishes recorded substance, but does not prove every change or action was covered.
