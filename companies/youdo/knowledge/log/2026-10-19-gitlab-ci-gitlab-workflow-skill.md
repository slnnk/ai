---
system: gitlab-ci
status: verified
checked: 2026-10-19
tags: [agents, gitlab, skills, workflow]
---
# Local first GitLab workflow skill implementation

## Summary
Implemented the user's approved plan for a unified local-first Git/GitLab workflow.
The canonical operational instructions are [gitlab-workflow](../../skills/gitlab-workflow/SKILL.md), with repository, conventions and publication references.
Both supervised approvals remain active; implementation does not grant unattended publication, merge, release or deployment permissions.
Added local checkout discovery, explicit clone/fetch and proposal snapshots; extended the existing MR helper for exact verification and partial-success recovery.
Twenty offline regression tests passed. Local-only inspection of the existing automation-services checkout passed; no remote writes or changes to its working tree/index occurred.

## Task and context
The user requested a plan after discussing local-first GitLab access, the early training review and ready-made skills. They then explicitly instructed implementation: "Реализуй это."
The plan covers shared knowledge-base instructions/scripts, not modifications to a company project checkout. Existing unrelated changes in ~/ai were preserved; no new task branch, commit or push was required for KB maintenance.
Sources informing the design were OpenAI pr-draft-summary/yeet, GitLab's glab skill and official OpenAI guidance on progressive disclosure and script-based deterministic work. No third-party skill was installed and no glab dependency was added.

## Actions
- Ran ai-sync.sh; it completed without output or reminders. Read skill-creator and queried scoped agent-learning rules. Delegated multi-file inventory and review as required by AGENTS.md.
- Added a short SKILL.md with three references, retaining two approvals, existing-checkout preference, task-only changes and separate external-action permissions.
- Added gitlab_repo.py: local inspection, registry-first lookup, bounded immediate checkout discovery, explicit clone/fetch, verified catalog insertion and immutable pre-publication snapshots/checks.
- Kept gitlab_task_mr.py phases and flags compatible; added optional draft creation, exact MR/project/SHA/title/body verification, description reconciliation, project-settings verification and separate pipeline availability reporting.
- Timed-out creates/updates get read-only reconciliation, never an automatic repeated write. Returned MR identity and write state survive a later verification failure.
- Moved active detailed conventions from the training map/global entry point into skill references; retained historical corrections and the early-report decision in the existing map/backlog.
- Created discovery symlinks for Codex and Claude to the same current/ skill. Codex's read-only sandbox mount required escalation for that local link; creation completed. No unrelated skill links were replaced.

## Review findings and fixes
The read-only reviewer found four concrete issues in the initial implementation; all were fixed and covered by regressions:
- Catalog registration must insert in the repository table, before trailing relationship prose.
- All fetch/push URLs must match the project and be bound into the snapshot, since Git can push to multiple URLs.
- Same-named fork MRs must not be mistaken for a local-source-project MR.
- Dirty submodule contents are not fully represented by a superproject diff; snapshots now refuse dirty submodule worktrees/indexes without cleaning them.
The follow-up review confirmed these fixes and found no further blockers in the reviewed scope.

## Verification
- `python3 -m unittest discover -s ~/ai/current/scripts/tests -p test_gitlab_workflow.py -v`: 20 passed, including an independent reviewer run.
- `python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/ai/current/skills/gitlab-workflow`: valid.
- Both helper --help commands ran successfully.
- `python3 ~/ai/current/scripts/gitlab_repo.py inspect --project sysadmins/automation-services`: existing checkout found, 23 local changes reported, no network refresh. This observation does not assert current remote state.
- Offline fixtures exercise staged/unstaged/untracked preservation, missing/colliding/duplicate checkouts, origin/push URL mismatch, credential-free output, catalog placement, changed snapshots/body/proposals/target, dirty submodules, MR reuse, fork rejection, timeout reconciliation, pipeline GET403, title/body/SHA checks and null descriptions.
- Knowledge lint/index and scoped whitespace verification were run at delivery; existing unrelated warnings were retained.

## Changed files
- ~/ai/current/skills/gitlab-workflow/SKILL.md and references/{repository,publication,conventions}.md.
- ~/ai/current/scripts/gitlab_repo.py (new).
- ~/ai/current/scripts/gitlab_task_mr.py (existing helper extended).
- ~/ai/current/scripts/tests/test_gitlab_workflow.py (new offline tests).
- ~/ai/AGENTS.md, current/CONTEXT.md and current/knowledge/systems/gitlab-ci/agent-git-workflow.md (canonical routing and history).
- ~/ai/TODO.md, current/knowledge/INDEX.md and .sync-notes (bookkeeping).
- ~/.codex/skills/gitlab-workflow and ~/.claude/skills/gitlab-workflow (symlinks).

## Approval and Git outcome
Implementation authorization is the user's explicit instruction above. Repository training-stage approvals are not applicable to this KB implementation; no project branch/source/target, commit proposal or MR was created. All Git commits in the tests are confined to temporary fixtures. No live clone/fetch, GitLab API mutation, release or deployment was performed. The prior report's pending user decision on unattended automation remains open.

## Risks and limits
Snapshots detect changed files/parameters, not consent, hunk ownership or semantic CI effects. Agents must inspect the complete staged diff and actual pipeline rules. Snapshot checks run immediately before staging; intentional staging/commit changes the recorded state, so resulting commits require explicit comparison with the reviewed patch before push.
Dirty submodule snapshots stop rather than silently omitting nested changes. Clone/fetch and MR behavior were not exercised against live remote writes; offline tests cover the guarded paths. Fresh-client skill activation has not been demonstrated by a real new task; discovery links and direct AGENTS.md routing are installed.

## Portable lesson
No separate general recipe created; this implementation contains company policy and remains in current/.
