---
name: gitlab-workflow
description: Work with YouDo GitLab projects using local checkouts first. Use for repository code investigation, task branches, commits and MR preparation or publication on gitlab.youdo.sg. Preserve the two supervised approvals and inspect CI effects before publishing.
---

# Local Git and GitLab workflow

Use the existing checkout as the source of code. Use GitLab for remote revisions,
MR discussion, CI and project settings. This skill does not turn a discussion,
prepared proposal, snapshot file or remembered approval into permission to publish.

## Choose the current stage

- **Investigate or obtain code:** read [repository.md](references/repository.md).
  Locate/inspect locally; clone a missing project into `~/git`; refresh only when
  the task needs current remote state. Match the code revision to the question.
- **Implement:** read [conventions.md](references/conventions.md). Propose repo,
  branch (or reuse) and base; obtain approval before switching/creating a branch
  or editing repository task files. Knowledge-base bookkeeping is exempt.
- **Prepare or publish:** read [publication.md](references/publication.md) and
  [conventions.md](references/conventions.md). Prepare a reviewable diff, checks,
  names, body, source/target and CI effects. Obtain one publication approval.
  Then stage only reviewed task changes, commit, push and create/update the MR.
- **Verify or recover an uncertain publication:** read
  [publication.md](references/publication.md). Inspect remote state first; do not
  repeat a write merely because a later check failed.

## Constraints shared by all stages

Keep both approvals until the user explicitly changes the supervised mode.
Do not ask again for an already approved stage unless names, scope, source/target
or effects materially change. Project instructions take precedence inside a repo.
Preserve unrelated staged, unstaged and untracked work, including user edits in
task files. Never infer ownership from a file path or commit the entire index blindly.

No automatic pull, stash, reset, cleanup, worktrees, force push, tags, merge,
auto-merge, target-branch push, deployment or manual CI retries. Separate explicit
authorization is required for actions outside the publication sequence and for
release/deployment effects triggered by that sequence. Do not bypass CI.

The scripts never establish user consent. Record the actual original/final
proposals, concise approval evidence, corrections, checks, CI effects and results
in the task's existing work log. No secrets or full transcripts.

## Tools

- `python3 ~/ai/current/scripts/gitlab_repo.py --help`: local inspection,
  explicit clone/fetch, proposal snapshot and change detection. Local-only by default.
- `python3 ~/ai/current/scripts/gitlab_task_mr.py --help`: existing GitLab
  inspection, MR publication and verification helper. Mutation phases require
  the actual applicable user approval; there is no approval-bypass flag.

Load only the reference needed for the current stage. Use compact script output
before reading detailed diffs or logs. No `glab` installation is required.
