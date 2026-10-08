---
system: gitlab-ci
status: verified
checked: 2026-10-08
tags: [agents, gitlab, training, workflow]
---
# GitLab: supervised agent workflow and training

## Summary
Active policy approved by the user on 2026-10-08. Training runs through 2026-10-30.
Two approvals: branch before repository edits; commit message and MR title before publication.
No automatic transition on the deadline: the user decides after reviewing training results.
Global entry point: `~/ai/AGENTS.md`. Baseline: [weekly review](../../log/2026-10-08-gitlab-ci-agent-git-workflow-review.md).

## Workflow and approval boundaries
1. Investigate read-only. Inspect project instructions, origin, git identity, working tree,
   existing branches/MRs and the required base/target. Propose branch name and repository.
   Wait for explicit confirmation before creating or switching branches and editing task
   files. For existing branches, obtain approval to reuse them. KB notes are exempt.
2. Implement on the approved branch. Preserve unrelated staged/unstaged changes. Run
   checks appropriate to the change and review the final diff for scope and secrets.
   Work in the existing checkout (`~/git/<repo>`), not a separate worktree, unless the
   user explicitly requests one. This preference was clarified on 2026-10-08 after
   DevOps-882 was initially prepared in separate worktrees. If unrelated local changes
   prevent switching branches, explain the conflict before moving or discarding them.
3. Propose the commit message and MR title together. Include repository, source/target,
   concrete change summary, actual check results and CI effects. Present the MR body if
   needed to make publication reviewable. Wait for explicit confirmation.
4. On confirmation, stage explicit task paths, inspect the staged diff, commit, push the
   approved branch and create/update its MR. Include only changes made by the agent
   for this task, unless the user explicitly requests additional changes. Check the
   entire staged diff for pre-staged user changes and mixed edits in task files;
   path selection alone is insufficient. Preserve unrelated index and working-tree
   changes. This user clarification was recorded on 2026-10-08 during DevOps-882.
   This one approval covers the publication
   sequence, overriding global per-command Git/external-state approval only for this
   sequence. Apply wording corrections before execution; a correction is not approval
   unless the user clearly authorizes the corrected version. Renew approval for material
   changes to names, scope, source/target or effects. Do not repeat already satisfied gates.
5. Verify remote SHA, MR source/target and latest pipeline state for that SHA. Inspect
   remote state before retrying a timed-out write to avoid duplicate commits/MRs.
   Return commit SHA, branch, MR URL, checks and pending dependencies. Merge stays manual.

## Naming and MR conventions
- Branch: exact tracker ID + short English kebab-case, e.g. `DevOps-879-http-timeout`.
  Respect established project exceptions, including iOS task-only branch `IOS-5054`.
  Do not invent a ticket. One task branch/MR per repo; related repos may share a branch
  name. Reuse the task's MR; never overwrite another person's colliding branch.
- Commit: concise lowercase English action + object, normally without task prefix and
  without introducing Conventional Commits. Prefer one coherent commit for a small
  completed change, splitting independent changes when useful. Avoid vague `bump`,
  `fix`, `changes`. Example: `set selenium http read timeout`.
- MR title: task ID + short English summary, normally matching the commit subject.
- MR body: one short paragraph in Russian describing the change, then a link to the
  task, and nothing else. Do not add checks, related tasks/MRs, dependencies or CI
  details. Keep that information in the work log and publication approval summary.
  This user correction supersedes the earlier detailed English descriptions
  (2026-10-08, DevOps-882). There is no separate Closes policy.
- Assign the user; do not invent reviewers/labels. Honor mandatory project settings.
  Observed infrastructure choices: squash off, branch deletion on merge on, target master.
  YouDoApp exception: squash on, target develop. Check the actual project each time.
- Draft if work/checks/dependencies are incomplete, ready when agreed checks pass. State
  missing checks in the work log and publication approval summary, not in the MR body;
  never claim runtime success merely from a merge or static validation.

## CI and excluded actions
Inspect push/MR pipeline rules before publication. Ordinary build/test/validation pipelines
are covered by publication approval. Automatic deployment, Terraform apply, destructive
operations or artifact releases require approval explicitly covering the effect before the
triggering push/MR. Manual deployment/retry buttons are not covered. Do not bypass CI.
No merge/auto-merge, direct target/protected branch push, force push, immediate remote branch
deletion, tags, history rewriting or tracker closure API call is authorized by training gates.
Source deletion on merge is a GitLab setting for a later user-approved merge, not permission
to delete now. Do not stash/reset/discard user changes or rewrite identity.

## Learning records and rule updates
Each task work-log entry must include a Training record with:
- Date, task, repo; proposed/final branch, commit message, MR title and source/target.
- Stage 1 and stage 2 approval evidence: a concise non-sensitive quote or session reference;
  mark skipped/declined/pending stages accurately. No approval means no dependent action.
- User corrections, their reason if provided, general rule derived, and canonical rule
  location updated. Distinguish a reusable preference from a task/project-only exception.
- Check results, publication outcome, MR link and errors or avoidable approval requests.

Update reusable corrections in this map immediately; also update global AGENTS.md when the
correction affects all agents. Add project-specific exceptions here without broadening the
global permission model. Preserve original proposals in task logs so the review can compare
first attempts to final accepted values. Record accepted proposals even with no corrections.
Avoid copying entire private conversations; never record secrets. Existing per-task logs
hold evidence; no separate backlog is kept here.

## October 30 review
The due action lives in `~/ai/TODO.md`. On October 30 or the first active session after it,
prepare a dated local report from training work logs and GitLab read-only evidence as needed.
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
