---
system: gitlab-ci
status: verified
checked: 2026-10-08
tags: [DevOps-882, training, nginx, postgresql, vault]
---
# DevOps-882: chat-agent infrastructure preparation

## Task
Prepare infrastructure requested by [DevOps-882](https://youtrack.youdo.com/youtrack/issue/DevOps-882), using DevOps-861 and DevOps-864 as references.

## Context
Repositories: `automation-services`, `selectel-tf`, and read-only service reference `/home/slnnk/git/youdo-chat-agent`.
Existing nginx map: [Selectel edge](../systems/automation-services/prod-selectel-nginx.md).
Git policy: [supervised workflow](../systems/gitlab-ci/agent-git-workflow.md).

## Actions
Read the three issues through authenticated YouTrack GET, KB notes, project instructions, service configuration and infrastructure CI. Tokens were loaded from `current/.env`; values were not recorded. Latest GitLab Terraform GET was cancelled before execution; local repository findings are not proof of current runtime state.

## Findings
- Required nginx name is `chat-agent.youdo.com`, using existing wildcard DNS/TLS and shared `traefik.youdo.com` template with the public Host. Append the vhost to the existing list.
- Database name is `chat_agent` on C2C, with DDL/create-schema capability for migrations and Hangfire. Terraform paths are `prod-dbaas/terraform.tfvars` and `prod-dbaas-grants/terraform.tfvars`; preserve existing resource indexes.
- Requested Vault path is `secret/dotnet/chat-agent`; developer supplies `BotToken`, `BotUsername`, `OAuthClientId`, `OAuthClientSecret`, `OpenRouterApiKey`, and `SentryDsnChatAgent`. Creation and write permissions remain to be checked separately.
- Developer owns the future `production.hcl`, including singleton svc and kill_timeout >=80s. Local master currently contains migration Dockerfile/script, no production Nomad file or deployment include. Application drain default is 75s. Shared v3 deploy template does not override kill_timeout (parent investigation).
- Outbound HTTPS to `api.telegram.org` and `openrouter.ai` still needs live verification from Nomad.
- Infrastructure MR runs Terraform validation/plans; applies are manual. Inventory-only nginx change does not trigger the nginx Molecule job.

## Changes
Local implementation on approved `DevOps-882-chat-agent` worktrees, from fetched `origin/master` bases `automation-services` `1a1ea524` and `selectel-tf` `67f46a1`:
- `automation-services/inventories/prod_selectel/group_vars/balancers`: appended `chat-agent.youdo.com` using `traefik.youdo.com`, wildcard TLS, state present.
- `selectel-tf/prod-dbaas/terraform.tfvars`: appended `chat_agent` to C2C database list, preserving count-based existing indexes and owner convention.
- `selectel-tf/prod-dbaas-grants/terraform.tfvars`: appended `chat_agent` to C2C baseline grants list.
Total: three files, ten added lines. No service-repository changes.

On the user's request, transferred the verified changes to the original checkouts
`/home/slnnk/git/automation-services` and `/home/slnnk/git/selectel-tf` on the same
approved branch. Unrelated tracked and untracked local changes were preserved.
Task files were checked byte-for-byte against the prepared worktree copies before
removing the redundant worktrees. Commands: save task-only `git diff --binary`, detach
temporary worktrees, `git switch DevOps-882-chat-agent` in original checkouts, `git apply
--check` and `git apply`, verify copied files, reverse task patches in temporary
worktrees, then `git worktree remove` without force.

## Verification
- YAML parsing and strict Jinja rendering passed; existing vhost renders unchanged.
- Both Terraform stacks validated after provider initialization with `init -backend=false`.
- Grants stack formatting passed. Database stack tfvars formatting fails on the same pre-existing baseline; unrelated formatting was preserved.
- Full local plan stopped because backend initialization is required. Local cloud `TF_VAR_*` credentials are absent; authenticated plans should run through the repository MR CI variables.
- Diff review found append-only changes in scope. New database receives existing C2C owner, supplying DDL and schema creation for Hangfire; baseline grants apply ancillary access in `public`.
- MR CI runs four automatic validation/plan jobs and exposes two manual applies. Apply database creation before grants; new-database grants planning may depend on database existence.
- Publication completed as recorded below; the agent performed no runtime provisioning,
  deployment, Vault writes, or merges. The subsequent operator rollout is recorded below.

## Operator rollout
The user reported completing Terraform apply and applying the Ansible role in the
current session on 2026-10-08. This is operator-reported completion of the database/nginx
rollout, not an independent runtime verification. Apply output and the exact Terraform
stacks applied were not supplied; the separate grants outcome is not independently
confirmed. Outbound HTTPS from Nomad remains unverified.

The user subsequently reported creating `secret/dotnet/chat-agent` in Vault. The
provided UI screenshot shows all six expected key names: `BotToken`, `BotUsername`,
`OAuthClientId`, `OAuthClientSecret`, `OpenRouterApiKey`, and `SentryDsnChatAgent`.
Values are masked and were not read or recorded. This confirms the operator report
and visible key presence; value validity and developer write permissions are not
confirmed by the screenshot.

## Training record
- Proposed and approved branch: `DevOps-882-chat-agent`, base/target `master` in both `automation-services` and `selectel-tf`.
- Approved isolated directories: `/home/slnnk/git-worktrees/DevOps-882/automation-services` and `/home/slnnk/git-worktrees/DevOps-882/selectel-tf`.
- Stage 1: user approved preparing local edits in the two repositories on the proposed branch (current session; parent confirmation). Preserve unrelated changes in original checkouts.
- Stage 2 approved: user said “Правки проверил, можешь создать МР.” This approval covered only the reviewed commits, branch pushes and MR creation.
- Accepted automation commit `add chat-agent nginx vhost`, MR title `DevOps-882 add chat-agent nginx vhost`; accepted Terraform commit `add chat_agent database and grants`, MR title `DevOps-882 add chat_agent database and grants`. Source `DevOps-882-chat-agent` -> target `master` in both repositories.
- Entire staged diff was checked as task-only: three files, ten added lines. Unrelated tracked/untracked changes were preserved.
- Publication result: automation commit `a87b482b09137f32d7a1b7301c309387b504b63a`, [MR !1364](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1364); Terraform commit `34061c2abde1fcd19348be9ea1939e1eea880886`, [MR !92](https://gitlab.youdo.sg/sysadmins/selectel/selectel-tf/-/merge_requests/92). Both assigned to `a.solonenko`, squash disabled, source deletion on merge enabled.
- Initial read-only verification: Terraform pipeline `140439` created; no automation pipeline observed yet. These initial states are not final CI results.
- Local helper `current/scripts/gitlab_task_mr.py` created with `inspect`, `publish`, `verify`, and `--help`. It reads the GitLab token from the existing environment file and avoids emitting token values. `publish` remains subject to explicit Stage 2 approval.
- No service branch proposed: developer owns its deployment configuration. No naming corrections reported.
- User correction: Molecule is obsolete and explicitly excluded from this task. Recorded as the current Selectel nginx validation instruction in the existing system map; historical repository Molecule examples are not a required check.
- User correction: work in original repository directories instead of separate
  git-worktrees. Applied to this task and recorded in `~/ai/AGENTS.md` and the canonical
  workflow map. Final review locations are `~/git/automation-services` and
  `~/git/selectel-tf`; original worktree proposal is retained above as training evidence.
- After transfer, task-only `git diff --check` passed in both original checkouts.
  Full automation-services diff also includes pre-existing runner changes; its
  `cron-docker-clean.j2` trailing whitespace is unrelated and was preserved.
- User correction: commits must include only agent changes for the current task,
  unless the user explicitly requests additional changes. Recorded in global
  `~/ai/AGENTS.md` and the canonical workflow map. For DevOps-882 this limits the
  proposed publication to the three task changes above; unrelated runner and
  compute-file changes remain excluded, including any pre-staged or mixed-file edits.

## MR description correction
The user explicitly requested updating both MR descriptions and established a global format: one short Russian paragraph describing the change, followed by the task link only. Checks, related tasks/MRs, dependencies, and CI details are excluded from MR bodies; keep them in the work log and approval summary. The parent agent updated `~/ai/AGENTS.md` and the canonical `agent-git-workflow.md`, replacing the previous conflicting body guidance.

Both local body files and remote descriptions were updated with the requested GET/PUT/GET verification. Both Terraform MR !92 and automation MR !1364 matched the requested bodies in final GET verification after normalizing the final newline with `.rstrip("\n")`. GitLab strips a trailing LF from descriptions. Titles, branches, assignees and squash/source-deletion settings were unchanged.

`current/scripts/gitlab_task_mr.py` now supports `update-description --iid --body-file` and reads the exact body from a UTF-8 file, using GET before PUT and GET afterwards to verify the resulting description. The user request authorized these description updates; it did not authorize deployment or merge.

## Risks
The user reported the Terraform and Ansible rollout above. Actual owner/grants, nginx
routing and application readiness have not been independently verified. Vault writes,
service launch, further runtime changes and tracker updates still require separate
applicable approval. No permission for additional external writes was inferred from
the rollout report.

## Portable lesson
None; existing [Traefik Host routing recipe](../../../../general/knowledge/nginx/traefik-host-router-behind-nginx.md) applies.
