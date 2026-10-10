---
system: youdo-chat-agent
status: verified
checked: 2026-10-09
tags: [DevOps-882, nomad, ci]
---
# Chat agent production delivery

## Purpose and components
.NET Telegram long-polling bot over public MCP, repository `/home/slnnk/git/youdo-chat-agent` (`youdo/ai/youdo-chat-agent`). Web handles OAuth login/callback; bot processes messages and Hangfire jobs. Database `chat_agent` belongs to shared `youdo` on C2C. Public nginx routing uses existing [Selectel edge](automation-services/prod-selectel-nginx.md).

## Delivery path
Published branch DevOps-882-prod-deploy in [MR !9](https://gitlab.youdo.sg/youdo/ai/youdo-chat-agent/-/merge_requests/9), commit 13fd1ff, adds web/bot image publish jobs and v3/.deploy-prod-full-auto.yml. On master: stop svc -> pre-migrations -> web canary -> promote -> post-migrations -> svc scale 1. No service deployment is claimed. HCL web count 2, svc initial count 0, no svc canary, kill_timeout 80s. Both listen port 80; web checks /health, bot checks /_/heartbeat. Public web Host chat-agent.youdo.com; bot internal router only. Geocoder uses its internal proxy route.

## Access and operations
Master pipeline [140457](https://gitlab.youdo.sg/youdo/ai/youdo-chat-agent/-/pipelines/140457) and production child 140458 completed successfully on 2026-10-09, verified via GitLab API. All deployment steps and release passed. Public /health requests from the agent network return protection-layer HTTP 403; end-to-end bot login remains unverified.

Vault references secret/dotnet/chat-agent (six developer-owned keys), secret/resources/databases/postgres C2C fields; policies resources and dotnet. Tooling credentials remain in current/.env or GitLab variables; values are never recorded. Migration CI variables DB_ADDR and POSTGRES_YOUDO_PASSWORD select the deployment database. Runtime uncertainties are recorded in the task log. User confirmed DevOps scope complete on 2026-10-09: infrastructure configured and service launched in production; functional checks belong to developers.

## Related work
[Production preparation](../log/2026-10-09-youdo-chat-agent-prod-deploy.md), [initial infrastructure](../log/2026-10-08-gitlab-ci-devops-882-chat-agent-infrastructure.md).
