---
system: knowledge-base
status: verified
checked: 2026-11-14
tags: [agents, context, resumption]
decision_state: cancelled
decision_scope: Optional fresh-session evaluation of the implemented startup and resumption changes only
decision_summary: The user retained the instruction changes without evaluation; no comparison or measurement follow-up is pending.
decision_date: 2026-11-14
decision_source: #evaluation-decision
---
# Task-scoped startup reading and compact resumption state

## Task

The user asked what the startup/coordination proposal meant, requested a concrete
recommendation, then authorized work with `Начинай` on 2026-11-14. The agreed narrowed
scope is task-scoped startup reading and compact checkpoints in existing long-task
records. Drop the separate coordinator idea for the selected single-Sol workflow;
concise tool output is already required. No routing, helper, hook or external change
was requested.

## Context

This implements a narrowed part of the [November 5 proposal](2026-11-05-knowledge-base-agent-methodology-review.md#context-engineering-discussion-follow-up).
The original E07/E08 comparative pilots remain design evidence, not executed pilots.
Existing unrelated edits in AGENTS.md, README.md, TODO.md and personal notes were
present before this task and must be preserved. Pre-edit snapshots and the task-only
instruction diff are in `~/ai-data/context-simplification/2026-11-14/`.

## Expected result and verification

Required result: personal work can omit company context; each operation still loads
its required rules; fully available current instructions need no duplicate read;
resumption preserves permission scope and evidence. Verify the task-only diff,
permission-block equality, heading references and five scenario walkthroughs. Run
agent instruction lint and KB lint. These checks do not establish fresh-agent
activation, actual cost savings or real interruption recovery.

## Actions

- Kept global instructions and permission gates; added task/action reading selection.
- Aligned the company context entry instruction with company-only applicability.
- Split checkout/Git details from Simplicity so references select the intended section.
- Added a compact checkpoint requirement to the existing progress instructions.
- Made progress, resumption, economical use and external changes sibling sections so
  reading one does not pull in the others as nested subsections.
- Preserved normal sync, scoped learning queries and mutable-state checks.

## Scenario review

This is a manual instruction walkthrough supported by source checks, not a fresh-session
behavior experiment. All cases include global/local instructions, assumption/economy
rules, normal sync and applicable learning retrieval.

| Case | Required reading/action | Reading that is not triggered by this case alone |
| --- | --- | --- |
| Personal explanation | Affected personal TODO/notes and their search rules | Company CONTEXT, repository edit/publication details; no checkpoint for a simple question |
| Company repository inspection | Company CONTEXT, repo catalog, repos.md, company GitLab skill; Checkout and Git changes for Git commands | Affected flow until edits, Review evidence until review, publication-stage details until publication |
| Code edit | Simplicity for a proposal, Affected flow, relevant project/skill rules; first repo approval before edits outside the exempt KB | No external publication/deployment permission inferred from edit approval |
| Publication | Supervised Git/MR training and company skill as applicable; actual diff, checks, names, branches and CI effects before confirmation | Merge, tag, deploy and other external writes remain outside publication approval |
| Resume after interruption | Checkpoint, evidence, missing/changed rules and mutable source/operation state | No duplicate completed action without reason; no approval inferred from the next-step field |

## Findings

The previous unconditional company context read was 9,869 bytes at inspection time;
this is a source-size observation, not token/cost savings. AGENTS.md remains within
the 5,632-byte lint limit. The pre-edit and post-edit Git-permission/external-change
blocks are byte-identical. New section references resolve. The new reuse rule explicitly
excludes truncated, missing, changed or uncertain instruction text and does not skip
required learning queries, sync calls or operational checks.

## Changes

- `~/ai/AGENTS.md`: scoped startup pointers and checkpoint trigger.
- `~/ai/general/knowledge/README.md`: Task context selection, Task resumption, and the
  Checkout and Git changes section boundary; existing prior edits retained.
- `~/ai/current/CONTEXT.md`: company-work trigger aligned.
- Existing proposal evidence and central TODO: narrowed implementation status and
  remaining fresh-session measurement proposal, preserving historical experiment results.

## Current checkpoint

- Goal: simplify reading and retain long-task state with unchanged permissions.
- Authorized scope: local instruction and KB changes following the user's request;
  no manual Git publication, external mutation, helpers or model experiment.
- Decisions: one Sol remains default; no separate coordinator; concise output uses
  the existing rule; keep mutable-state verification and all approval gates.
- Completed: instruction changes, pre-edit snapshots and task-only diff review;
  five scenario walkthroughs and permission-block equality check.
- Checks completed: agent-lint (9 files, zero findings), KB lint (zero findings),
  18 heading references resolved, AGENTS size and unchanged permission blocks.
- Index rebuilt successfully: 72 general, 104 personal and 527 company notes;
  no missing personal frontmatter. No task checks remain pending.
- Running operations: none at this checkpoint.
- Next permitted step: report closure; the user retained the changes without evaluation.
  No comparison, model run, external action or follow-up measurement is pending.

## Status and risks

Local instruction changes and the five-case walkthrough are complete.
Agent-lint checked 9 files with zero errors/warnings/info; KB lint reported zero
errors/warnings. The heading check initially rejected the existing training heading
because of its date suffix; the corrected resolver accepts that explicit suffix and
all 18 references resolve. See `~/ai-data/context-simplification/2026-11-14/static-checks.json`.
Existing learning outcomes single-sol-default, discussion-before-implementation
and verify-expected-results
were recorded as pass from observable implementation actions. During the later
closure turn, the scoped-startup-resumption rule received a first-attempt fail for
unnecessary rereading; see Evaluation decision. Same-session walkthroughs do not
establish fresh-session activation or measured benefit.
Fresh-session correctness, missed constraints, unnecessary reads, time/cost including
retries and real interruption recovery remain unmeasured. The user declined the optional
evaluation; the matching [central TODO](../../../TODO.md) entry is closed without
performing that evaluation. Implemented instructions remain in effect.

## Portable lesson

Task/action triggers can select existing canonical sections without adding a routing
service or another backlog. The actual behavioral benefit is unmeasured; the user chose to keep the change
without a dedicated evaluation.

## Evaluation decision

On 2026-11-14 the user explicitly chose `Оставим изменение без оценки`.
Retain the implemented instructions and close the optional evaluation without running
it. Earlier suggestions that the effect would become visible during normal work did
not establish a measurement mechanism. No user action or scheduled/background
comparison remains. Do not reopen this evaluation without a new user request.

Execution observation during this closure: the agent unnecessarily reread already
available README sections at task entry. This is a first observed failure of the new
current-text reuse rule, not evidence that the whole change fails or authority to
restart the declined evaluation. Record the applicable first-attempt outcome once;
no additional instruction change is authorized by this observation.
