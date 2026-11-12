---
system: gitlab-ci
status: verified
checked: 2026-11-11
tags: [agents, gitlab, training, workflow]
---
# GitLab: supervised agent workflow and training

## Summary
Supervised policy approved on 2026-10-08; the original review date was 2026-10-30.
Local-first workflow, two approvals and detailed conventions are maintained in the
[gitlab-workflow skill](../../../skills/gitlab-workflow/SKILL.md), implemented on 2026-10-19.
The user received the early review and chose on 2026-10-19 to retain both approvals while automating information gathering and preparation of review materials. The follow-up review was delivered on 2026-11-04. The user approved observing the next five tasks with publication, followed by a comparison; the five-task threshold was reached, retrospectively reconciled on 2026-11-11; [comparison delivered on November 11](../../log/2026-11-11-gitlab-ci-agent-git-training-comparison.md); both approvals are retained.
Two approvals: branch before repository edits; commit message and MR title before publication.
No automatic transition on the deadline: the user decides after reviewing training results.
Global entry point: `~/ai/AGENTS.md`. Baseline: [weekly review](../../log/2026-10-08-gitlab-ci-agent-git-workflow-review.md).

## Continuous supervised learning from November 11
The [user decision and implementation](../../log/2026-11-11-gitlab-ci-continuous-learning-supervised.md) require ongoing learning from all available substantive discussions, especially repository scope, branch/commit/MR naming and YouTrack comment content. Apply the shared agent-learning capture/retrieve/evaluate cycle in each relevant task, retaining first-attempt failures and source evidence. Both repository approvals and exact-comment confirmation remain active. Review the evidence on **2026-11-20**; the date does not automatically change permissions. The central TODO holds the due reminder; the earlier five-publication experiment remains historical and complete.

## Active workflow
The canonical executable instructions are now the [gitlab-workflow skill](../../../skills/gitlab-workflow/SKILL.md).
Read its [repository procedure](../../../skills/gitlab-workflow/references/repository.md) for local-first
checkout/revision selection, [conventions](../../../skills/gitlab-workflow/references/conventions.md)
for branch approval, names and CI effects, and [publication procedure](../../../skills/gitlab-workflow/references/publication.md)
for the second approval, task-only staging, remote verification and training records.
This map retains history and task evidence; do not maintain a competing operational policy here.
Both supervised approvals remain active. The skill implementation does not authorize unattended publication.
[Implementation and offline checks](../../log/2026-10-19-gitlab-ci-gitlab-workflow-skill.md).

## Five-task follow-up approved on November 4

The user approved observing the next five tasks with Git/MR publication after the November 4 report. Both approval gates remain active. This is an observation stage using existing controls, not permission to execute backlog tasks, publish, merge or deploy autonomously. There is no calendar deadline or background scheduler.

For each task, use its existing work log to record the minimal requested deliverable and intended diff scope before editing; before publication inspect actual CI targets, inherited variables and automatic external effects; retain user corrections, original/final proposals, both approvals, validation or explicit scoped waivers, and actual publication/verification outcomes. Apply the existing canonical workflow; do not create additional skills or broaden task scope for this review.

Count distinct user-requested tasks first published after this approval. Multiple commits, MRs or repositories for one continuing task count once. Count a published task even when CI later fails; record that failure separately. Cancelled/unpublished attempts remain evidence, but do not advance the five-published-task count. Do not turn missing approval evidence into a success. Record a source link and concise outcome here when each task qualifies; keep actionable remaining work only in the central TODO.

Observed threshold: **5/5 reached**. Reconciled on 2026-11-11 after the user challenged the stale initial 0/5. At least six distinct published tasks are supported by the existing logs below. This is a conservative retrospective lower bound, not a claim that these are the exact first five publications in chronological order. DevOps-904 work is grouped once despite multiple repositories/MRs; continuing DevOps-908 and DevOps-916 publications each count once. The old zero was a bookkeeping omission, not absence of publication evidence.

| Task | Publication evidence | Recorded result |
| --- | --- | --- |
| DevOps-904 | [Android cache MR2922](../../log/2026-11-05-nexus-devops-904-android-product-cache-proposal.md), [Business gates MR3918](../../log/2026-11-05-nexus-business-gates-recent-cache-check.md) | November 5: approved publication, task-only staged diff and remote verification; grouped conservatively as one task. |
| DevOps-907 | [DNS forwarder MR1388](../../log/2026-11-05-corporate-network-public-test-consul-stale-forwarder.md) | November 5: both approvals, one-file commit, separate MR verification; pipeline skipped. |
| DevOps-908 | [Autotest MR1163](../../log/2026-11-05-gitlab-ci-devops-908-gradle-image-18.md) | November 5: approved initial publication and separately approved endpoint/cache scope extensions; one task. Later two successful warm-cache runs recorded. |
| DevOps-912 | [Appium Settings MR1390](../../log/2026-11-09-android-farm-devops-912-preserve-appium-settings.md) | November 9: both approvals, one-template commit and remote verification; skipped CI distinguished from test success. |
| DevOps-913 | [Client headers MR1391](../../log/2026-11-10-automation-services-devops-913-client-headers.md) | November 10: user corrected initial port-forwarding proposal; final three-line diff, both approvals, scoped checks and verified publication. |
| DevOps-916 | [Stand settings MR130/MR131](../../log/2026-11-10-nomad-test-devops-916-call-masking-config.md) | November 10: user corrected template placement; branch-base conflict handled with renewed approval, unrelated files preserved, both publications verified; one task. |

This reconciliation reads existing records only; it is not a new GitLab/API audit or the full comparison. The initial prospective counter was never updated despite these task logs. The [comparison with the November 4 baseline](../../log/2026-11-11-gitlab-ci-agent-git-training-comparison.md) was delivered on November 11 at the user request; the central TODO action is closed. Both approvals remain active; no additional five publications are required.

Original observation deliverable, completed on November 11: prepare a concise comparison with the November 4 baseline: repeated user interventions, scope corrections, approval compliance, naming changes, task-only staging, CI-effect predictions and verified publication outcomes. Assess what preparation can be automated; do not change permissions without an explicit user decision. The completed review action is retained in [central TODO](../../../../../TODO.md).

## Correction-application audit on November 11
The [audit](../../log/2026-11-11-gitlab-ci-correction-application-audit.md) traces seven correction families to later applicable work. Checkout preservation, naming/MR text and master-based base-images tags have distinct-task application evidence; scope expansion recurred. Local builds and clickable links have within-task application evidence. Historical rule-read evidence is unknown. The zero counter and zero registered outcome evaluations before this audit demonstrate failed ongoing measurement. Publication counts are not learning scores; both approvals remain active.

## Training corrections
- 2026-10-08, DevOps-882: use the existing checkout rather than separate worktrees;
  preserve unrelated staged/unstaged and mixed user edits; commit only task changes.
  MR descriptions changed from detailed English text to a short Russian paragraph and
  task link. Evidence: [infrastructure work log](../../log/2026-10-08-gitlab-ci-devops-882-chat-agent-infrastructure.md).
- 2026-10-09, DevOps-882: branch suffix describes the change, not the repository.
  Evidence: [service deployment log](../../log/2026-10-09-youdo-chat-agent-prod-deploy.md).
- The retired separate Closes rule and observed project exceptions are recorded in
  the [baseline review](../../log/2026-10-08-gitlab-ci-agent-git-workflow-review.md) and adoption history.
  Active project conventions live in the skill reference above.

## Manual-mode release source selection

User correction, DevOps-898, 2026-10-14: for projects using `DEPLOY_PROD_MODE=manual`, prefer a fresh release tag at the merged commit when a new pipeline needs updated HCL. Inspect the standard tag rules first. Do not automatically switch delivery to master or add unrequested production-manual overrides to create a pipeline. Creating a tag still requires explicit authorization covering its release/build effects; deployment remains a separate action. Textvalidation tag `1.0.4` was explicitly requested after twelve proposed local rule lines were cancelled without publication.

## Base-images release tags must use master

User correction, DevOps-898, 2026-10-14: `youdo/base-images` release tags must point to commits on `master`, after the reviewed MR is merged. The initial `kubectl/1.35.6` tag incorrectly targeted unmerged feature SHA `18c0ed83`; the agent acknowledged the mistake. User explicitly requested merging MR !41 and recreating that tag, authorizing this concrete merge/tag replacement/rebuild sequence. Do not infer general permission to merge, replace tags, or rebuild unrelated images. Verify the resulting master SHA and rebuilt image before claiming release completion.

## Learning records and rule updates

Kitcut correction2026-10-15 under DevOps-898: user rejected the proposed recreate_db=false→true change. Ordinary deployment must retain service-specific DB behavior unless explicitly changed; create-if-absent in shared Ansible is independent of recreate_db and migrations still run. Selecting ordinary jobs does not authorize overriding this service setting or imply such a source edit is necessary. Proposed branch was not approved/created. [Evidence](../../log/2026-10-15-nomad-test-devops-898-kitcut-preflight.md).

DevOps-898 stand recovery correction2026-10-15: use ordinary deployment jobs with database recreation for the stand rollout; do not choose keep-db as an agent preference. Acceptance requested by the user is GitLab and Nomad job statuses only. This determines job selection/check scope, not standing permission for unrequested external mutations. Keep-db templates are fixed independently for correctness. [Evidence](../../log/2026-10-15-gitlab-ci-devops-898-keep-db-vk-routing.md).
Training record requirements and durable correction handling are maintained in the
[publication reference](../../../skills/gitlab-workflow/references/publication.md#training-record).
Keep original proposals and approval evidence in per-task logs; the map links history,
while operational corrections update the appropriate skill reference and global boundaries
in AGENTS.md when applicable. Task-specific exceptions do not broaden permissions.

## October 30 review

Follow-up delivered on 2026-11-04: [report](../../log/2026-11-04-gitlab-ci-agent-git-training-followup-report.md). This supersedes the pending preparation/reminder status below, retaining its history. The report recommends keeping both approvals; no user permission change or new schedule is inferred.

The user requested early delivery on 2026-10-19. The [early training report](../../log/2026-10-19-gitlab-ci-agent-git-training-early-report.md)
covers October 8–19 and fulfills report preparation ahead of the original date. After discussing the report, the user explicitly chose to retain both approval gates while automating information gathering and review-material preparation.
The next review is proposed for October 30 or the first active session after it, focusing on work since October 19: scope control, task-only staging, approvals, predicted CI effects, remote publication verification and corrections. The date is an assistant proposal; no background job was scheduled.

The completed preparation and pending review actions live in `~/ai/TODO.md`. The original
plan was to prepare a dated local report on October 30 or the first active session after it,
using training work logs and GitLab read-only evidence as needed.
Include number of eligible tasks and observed records; first-proposal acceptance separately
for branch, commit and MR; correction patterns and examples; permission violations/errors;
validation/publication outcomes and remaining ambiguities. Do not fabricate metrics when
logs are incomplete. Report an explicit recommendation and proposed rule changes.
User review determines full automation or further training. Supervised gates remain active
until an explicit decision, even after October 30. This is a startup reminder, not a background
scheduler; a report cannot run without an active agent session.

## Adoption history
- 2026-10-08: user approved the baseline rules with a two-stage training override, removed
  the separate Closes rule as redundant with automatic MR creation behavior, required
  feedback to update canonical rules, and set the review date to October 30.
- [Adoption log](../../log/2026-10-08-gitlab-ci-agent-git-training-adoption.md).

## Minimal adaptation scope (user correction, 2026-10-09)

For existing infrastructure automation, keep adaptations limited to the configuration and targeting needed for the requested run. Do not expand folder/zone/network migration work into SQL behavior changes, refactoring, helpers or test infrastructure. Put optional improvements in the single TODO list and implement them only on a separate request. DevOps-889 evidence: user rejected the expanded implementation; final changes are destination/name/subnet arguments, scoped inventory/play host groups and the required target DNS lookup in the existing Zabbix script. See the [work log](../../log/2026-10-09-yandex-cloud-devops-889-mssql-recovery-plan.md). This correction narrows scope; it grants no additional Git or external-action permissions.
