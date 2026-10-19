# Company conventions and branch approval

These are the canonical detailed conventions. Respect project-level exceptions.

## First approval

Investigate read-only, inspect project instructions, origin, identity, working tree,
existing branches/MRs and base/target. Propose the repository, branch name and base
branch. Obtain explicit confirmation before creating/switching the branch or editing
task files. Obtain approval to reuse an existing branch too. KB bookkeeping is exempt.
Discussion or a corrected name alone is not authorization for implementation/publication.

Implement only the requested change. Preserve unrelated index/worktree changes and
user edits within task files. Optional refactors, helpers, hardening and cleanup belong
in `~/ai/TODO.md`, unless separately requested. Keep adaptations to existing automation
limited to the targeting/configuration needed for the requested run.

## Names and MR text

- Branch: exact tracker ID plus short English kebab-case describing the change,
  e.g. `DevOps-879-http-timeout`. Do not invent a ticket or use merely the repo name.
  iOS task-only names such as `IOS-5054` are an established exception. Use one task
  branch/MR per repo; related repos may share the same branch name. Never overwrite
  another person's colliding branch.
- Commit: concise lowercase English action and object, normally without task ID or
  Conventional Commits prefixes. Prefer one coherent commit for a small change;
  split independent changes when useful. Avoid vague subjects such as `changes`.
- MR title: task ID plus short English summary, normally matching the commit subject.
- MR description: one short Russian paragraph explaining the change, then the task
  link, and nothing else. Keep checks, dependencies, other MRs and CI details in the
  approval summary/work log. No separate Closes rule. Project-mandated templates take
  precedence if they conflict; do not silently adopt a generic upstream template.
- Assign the user; do not invent reviewers or labels. Inspect actual project defaults.
  Observed infra defaults were target master, squash off and source deletion on merge
  on; YouDoApp uses develop and squash on. These are observations, not universal defaults.
- Draft when work/checks/dependencies remain incomplete; ready when agreed checks pass.
  Present that state for approval. Preserve an existing MR's readiness unless the user
  explicitly approves a change. A skipped pipeline or successful merge is not runtime proof.

## CI and releases

Before publication inspect the actual push/MR pipeline rules, includes and relevant
variables. Ordinary build/test/validation pipelines are covered by publication approval.
If push/MR creation can deploy, release artifacts, apply Terraform or perform destructive
work, explain the trigger, environment and effect and obtain approval explicitly covering
it before the triggering write. If effects cannot be established, resolve them before
publication. A proposal field asserting an effect is not a check of the actual CI rules.

Merge, auto-merge, target/protected-branch push, force push, remote branch deletion,
tags, rewriting history, tracker writes, deployment and manual job retry/play are outside
the two training approvals. Deletion-on-merge settings do not authorize deletion now.
Separate external actions retain their existing per-action approval requirements.

For `DEPLOY_PROD_MODE=manual`, prefer the standard fresh release tag at the merged
commit when updated HCL needs a new pipeline. Inspect normal tag rules; do not switch
delivery to master or add unrequested manual-production overrides to force a pipeline.
Tag creation still needs explicit release/build authorization; deployment stays separate.

For `youdo/base-images`, a release tag must target a commit on master after the reviewed
MR has merged. Verify the exact master SHA before any separately authorized tag creation.
Do not release an unmerged feature SHA. Historical corrections are recorded in the
[training map](../../../knowledge/systems/gitlab-ci/agent-git-workflow.md).

Use established deployment jobs and service-specific database behavior. Ordinary jobs
versus keep-db, `recreate_db` and migration policy are not agent preferences. Do not change
them to make a rollout easier without a request covering that behavior.
