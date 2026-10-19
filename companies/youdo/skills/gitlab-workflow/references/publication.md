# Prepare, publish and verify

## Prepare the second approval

Read [conventions.md](conventions.md). Review tracked and untracked changes, including
the entire existing index. Identify task hunks separately from the user's changes even
inside the same file. Run appropriate checks; review the actual net diff and CI effects.

Present one reviewable proposal: repo, concrete diff summary, check results, commit
message, MR title/body/readiness, source/target and CI effects. Do not request permission
for an abstract publication before preparing these details. Record original and final
names even when accepted without correction.

For substantive publication, save the proposal outside the checkout under
`~/ai-data/gitlab-workflow/<task>/<repo>/`. Keep descriptions in a literal UTF-8 file;
do not interpolate backticks or `$` through a shell. A proposal JSON has these fields:

```json
{
  "project": "group/project",
  "source": "DevOps-123-describe-change",
  "target": "master",
  "base_ref": "origin/master",
  "task_paths": ["path/to/task-file"],
  "commit_message": "describe change",
  "title": "DevOps-123 Describe change",
  "body_file": "body.txt",
  "checks": ["actual command: observed result"],
  "ci_effects": "observed push/MR triggers and any approved deployment/release effects"
}
```

`body_file` is absolute or relative to the proposal file. `task_paths` names explicit
relative files, not ownership of every hunk within them. Include the exact `Draft: `
prefix in `title` for an approved draft. Use actual checked results and CI effects,
not the example values. The proposal and body must contain no credentials or raw logs.

Capture the prepared state before asking for publication approval:

```bash
python3 ~/ai/current/scripts/gitlab_repo.py snapshot --project group/project --repo /absolute/checkout --proposal-file /absolute/proposal.json --record /absolute/snapshot.json
```

The snapshot binds HEAD, branch, origin/push origin, tracked/staged diffs, untracked
file hashes, body, complete proposal and cached base/target SHAs. It contains no diff
contents and refuses to overwrite a record. It does not prove change ownership, inspect
CI semantics or authorize any command. Obtain and record the user's actual confirmation.
Dirty submodule worktrees/indexes are refused because superproject diffs do not bind
their file contents. Preserve those changes and resolve their scope before preparing
a publication; do not clean them automatically.

## Execute the approved publication

1. Immediately before staging, run the same command with phase `check`. A mismatch
   stops publication. Inspect the difference and renew approval for material changes;
   do not replace the snapshot just to make it pass. Do not fetch between approval and
   this check without accounting for changed refs. This guard is before staging, since
   authorized staging/commit will intentionally change the captured state.
2. Stage only reviewed task hunks. Never use `git add -A`/`.`. Inspect the entire staged
   diff, not merely task paths, for pre-staged user work and mixed edits. Commit only
   the reviewed patch while preserving unrelated index/worktree work. If isolation
   cannot be done safely, stop and explain the concrete conflict; do not reset/stash
   user work. A successful snapshot comparison is not permission to commit other hunks.
3. Commit the approved message and inspect the resulting commit against the reviewed
   task patch. Ensure no hook or concurrent session changed the intended contents.
   Record the full SHA; stop before push if the actual commit differs from the proposal.
4. Push the approved source branch to the verified origin, without force. A push error
   requires inspecting remote state, not pulling master or retrying blindly. Never
   push the target branch as a substitute. Account for approved automatic CI effects.
5. Run the existing MR helper with `publish`, the exact `--project`, `--branch`,
   `--target`, `--title`, `--body-file` and full `--expected-sha`. It creates a missing
   MR or reconciles the description of the existing matching MR, preserving project
   settings and readiness. A title/target mismatch stops rather than silently changing
   the agreed MR. Inspect and propose that change separately if required.
   Same-named fork MRs are refused; source and target project IDs must match the project.

One confirmation covers this approved staging/commit/push/MR sequence; do not ask again
for each command. It does not cover merge, release, deployment or other external writes.
Sandbox approvals still apply. Local snapshot/CLI flags never substitute for consent.

## Verification and recovery

Use `verify` with the same expected SHA, title and body after publication or an uncertain
result. The helper verifies branch SHA, MR SHA, source/target, title and description.
Exact verification flags are optional for backwards compatibility, so always provide
them in this workflow. Keep descriptions free of terminal newlines; the helper strips
terminal newlines from the desired file before sending/comparing it.

Output separates `write_state`, MR identity and `verified` from `pipeline_verification`.
A pipeline GET403 after successful MR creation reports the MR as verified with pipeline
verification unavailable; do not create another MR. Pipeline status `failed`, `running`,
`skipped` or an empty list must be reported as observed, not inferred successful.
The helper uses API GETs, avoiding interactive retry menus on nominal read operations.

After a timed-out create/update it attempts read-only reconciliation once, never a second
write. Exit 2 with an uncertain or created write state requires read-only inspection
before any retry. Preserve the reported MR URL/IID even when verification fails. For a
new MR, check agreed project settings too; for a reused MR, preserve existing metadata.

Record commit/push/MR/check outcomes separately, including an unattempted or uncertain
step. Return commit SHA, branch, MR link, check results and any real dependency. Do not
claim deployment success from source publication, static checks or a merge.

## Training record

In the task's existing English work log retain task/repo/date, original/final names,
source/target, both approval references or concise non-sensitive quotes, corrections
and scope, validation, CI effects, publication outcome, MR URL and recovery errors.
Mark pending/declined stages accurately. Link durable corrections to their canonical
rule using agent-learning. Put actionable open work only in `~/ai/TODO.md`.
