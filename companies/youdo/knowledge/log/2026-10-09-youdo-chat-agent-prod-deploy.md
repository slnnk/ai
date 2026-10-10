---
system: youdo-chat-agent
status: verified
checked: 2026-10-09
tags: [DevOps-882, nomad, ci, training]
---
# Chat agent: production Nomad and CI deployment preparation

## Task
User requested `devops/production.hcl` and connected production CI for [DevOps-882](https://youtrack.youdo.com/youtrack/issue/DevOps-882), explicitly choosing automatic deployment after merge to master like giveaway-bot.

## Context
Existing checkout `/home/slnnk/git/youdo-chat-agent`, base `origin/master` `4b4397c`. Reference: giveaway-bot production HCL/CI and shared v3 templates. [Previous infrastructure work](2026-10-08-gitlab-ci-devops-882-chat-agent-infrastructure.md), [service map](../systems/youdo-chat-agent.md).

## Actions and changes
- `.gitlab-ci.yml`: 23 added lines, full-auto production include, mode auto, PostgreSQL database chat_agent, service count 1, explicit web/bot publish jobs with matching project and assembly paths.
- New `devops/production.hcl`: 235 lines. Web count 2/canary 1, `/web` image, public Host chat-agent.youdo.com. Svc count 0/canary 0 during web rollout, `/bot` image, task kill_timeout 80s; final CI scale starts one bot. User changed web count and removed explicit cpu=100 in both groups; both changes were explicitly approved for inclusion.
- Environment templates reference the six requested keys under secret/dotnet/chat-agent, shared C2C PostgreSQL host/explicit port and youdo password, plus internal Geocoder route. No secret values recorded.
- Full-auto DAG stops svc, runs pre-migrations, deploys/promotes web, runs post-migrations, starts svc. Feature branch publication does not deploy; merge to master triggers automatic production/release CI.

## Verification
Parent agent reports Nomad 1.3.5 validate passed, with expected svc count 0/max_parallel 1 warning; no Docker agent validation available. Terraform formatter stdin check and Go text/template rendering with synthetic Vault data passed. GitLab parent dry-run and child static lint passed without errors/warnings. Code review found no blocking task defects. Shared stop template suppresses stop errors and has no explicit old-task drain check; shared template was not modified.

## Training record
- Branch proposals: DevOps-882-chat-agent rejected because suffix repeated repository name; add-production-nomad-job corrected; final approved DevOps-882-prod-deploy, source/target master.
- Stage 1: user explicitly approved service branch, HCL and CI edits in existing checkout, and selected automatic deployment after merge to master.
- Reusable naming correction: branch suffix describes the change, rather than repeating repository name. Updated canonical workflow and global AGENTS.
- Stage 2 approved: user said publish the service changes, then include my edit in the commit for web count=2, and answered yes, include for removal of cpu=100. Commit `13fd1ff589882e9e8d4affc5a9df4defd0047423`, subject `add production nomad deployment`; MR title `DevOps-882 add production nomad deployment`; source DevOps-882-prod-deploy -> master.
- MR body format remains one short Russian change paragraph plus task link only. Checks, prerequisites and CI effects remain here and in the approval summary.
- Published [service MR !9](https://gitlab.youdo.sg/youdo/ai/youdo-chat-agent/-/merge_requests/9). Checked actual staged diff: exactly .gitlab-ci.yml and devops/production.hcl, 258 insertions; no other changes. Local checkout clean after commit and push. Remote SHA verified by publication helper; assignee a.solonenko, squash false, remove source branch true. Pipeline list initially empty. No merge or deployment performed.
- Repeated Terraform format check, Nomad validate and staged diff whitespace check passed before commit, with the previously documented svc count warning. Commands: `git add -- .gitlab-ci.yml devops/production.hcl`, `git commit -m 'add production nomad deployment'`, `git push -u origin DevOps-882-prod-deploy`, approved gitlab_task_mr.py publication helper.

## Rollout result
User reported successful deployment and provided pipeline 140457. Read-only GitLab API independently confirmed master pipeline [140457](https://gitlab.youdo.sg/youdo/ai/youdo-chat-agent/-/pipelines/140457) and child production pipeline [140458](https://gitlab.youdo.sg/youdo/ai/youdo-chat-agent/-/pipelines/140458) both success, SHA 026216ca4f811ea5ebd4158c37e22a91786cc3a9. Build web/bot/migrations, unit tests, release and all six deployment steps succeeded; rollback remains manual. Child finished 2026-10-09 00:35:27 +03:00. Sanitized API snapshot: ~/ai-data/devops-882/pipeline-140457.json. External /health still returns protection-layer HTTP 403 from the agent network; application health and Telegram OAuth flow not independently confirmed.

## Remaining operational uncertainty
Unverified details recorded during preparation: client max_kill_timeout >=80s (documented default 30s), migration DB_ADDR/POSTGRES_YOUDO_PASSWORD selecting C2C, developer Vault write access, outbound Telegram/OpenRouter HTTPS and team-only access. These were not independently verified; successful CI does not establish every runtime detail. [Nomad client setting](https://developer.hashicorp.com/nomad/docs/configuration/client#max_kill_timeout).

## Completion and ownership
On 2026-10-09 the user clarified that the assigned scope was infrastructure configuration and production launch only. That scope is complete; developers will perform further functional checks. Closed the inferred follow-up checklist in ~/ai/TODO.md as outside the requested completion scope, without claiming those checks were performed. Shared-template stop/drain improvements remain an observation, not an assigned task. No further investigation, external ticket update or developer notification requested.

## Portable lesson
None.
