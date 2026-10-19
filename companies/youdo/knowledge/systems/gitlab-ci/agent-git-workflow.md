---
system: gitlab-ci
status: verified
checked: 2026-10-19
tags: [agents, gitlab, training, workflow]
---
# GitLab: supervised agent workflow and training

## Summary
Supervised policy approved on 2026-10-08; the original review date was 2026-10-30.
Local-first workflow, two approvals and detailed conventions are maintained in the
[gitlab-workflow skill](../../../skills/gitlab-workflow/SKILL.md), implemented on 2026-10-19.
The user received the early review and chose on 2026-10-19 to retain both approvals while automating information gathering and preparation of review materials. The next review is proposed for 2026-10-30 or the first active session after it.
Two approvals: branch before repository edits; commit message and MR title before publication.
No automatic transition on the deadline: the user decides after reviewing training results.
Global entry point: `~/ai/AGENTS.md`. Baseline: [weekly review](../../log/2026-10-08-gitlab-ci-agent-git-workflow-review.md).

## Active workflow
The canonical executable instructions are now the [gitlab-workflow skill](../../../skills/gitlab-workflow/SKILL.md).
Read its [repository procedure](../../../skills/gitlab-workflow/references/repository.md) for local-first
checkout/revision selection, [conventions](../../../skills/gitlab-workflow/references/conventions.md)
for branch approval, names and CI effects, and [publication procedure](../../../skills/gitlab-workflow/references/publication.md)
for the second approval, task-only staging, remote verification and training records.
This map retains history and task evidence; do not maintain a competing operational policy here.
Both supervised approvals remain active. The skill implementation does not authorize unattended publication.
[Implementation and offline checks](../../log/2026-10-19-gitlab-ci-gitlab-workflow-skill.md).

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
