---
system: youdo-business
status: verified
checked: 2026-10-16
tags: [gitlab, nomad, jarvis]
---

# DevOps-900: production nodes API host override

## Summary

Added `YouDo__HttpClient__AI__Host = "http://10.18.26.48:3001"` to all four production tasks in `youdo-business-tickets`: web, bot, api, worker. Committed and merged through MR !112; production pipeline launch checked separately, runtime outcome not yet verified.

## Context and findings

Jarvis is exposed at `https://jarvis.youdo.com`. Web, bot and worker appsettings default to `http://10.16.26.47:3001`. The user first supplied `https://nodes.youdo.com`, then explicitly requested the private HTTP endpoint above for production. The AI client appends `/api/v2/ai`.

## Actions and changed files

Repository: `/home/slnnk/git/youdo-business-tickets`. Only `devops/production.hcl` changed: four added environment variables beside the AI timeout settings. Existing untracked `devops/dev.yml` preserved.

## Checks and risks

`git diff --check` passed. `nomad job validate -var=dc=validation devops/production.hcl` passed locally. Driver validation was skipped because no Nomad agent was reachable. Existing warning: svc group max_parallel 1 exceeds count 0. Validation without a dc override fails because the template default is empty. No connectivity or runtime verification performed. Use the established GitLab production deploy workflow for rollout.

## Training record

Task: DevOps-900. Proposed and approved branch: `DevOps-900-update-nodes-api-host`, base `master`. User supplied the task ID, then explicitly replied "Да" to the exact branch proposal. Branch created; local changes authorized. Proposed commit: `update production nodes api host`. Proposed MR title: `DevOps-900 Update production nodes API host`. Source: approved task branch; target: master. Stage 2 publication approval pending; no commit, push or MR created. Production CI uses `v3/.deploy-prod-full-auto.yml` with `DEPLOY_PROD_MODE: auto`; publication must account for deployment effects and needs separate explicit approval covering them. No deployment approval was requested or granted.

## Publication and merge

The user explicitly requested publication and immediate merge, then clarified that the release must proceed quickly. This authorized the established automatic production release triggered on master. Commit `4eb06056315e94a3416cdb5f2771cd9c9150d257`, message `update production nodes api host`. MR title `DevOps-900 Update production nodes API host`; [MR !112](https://gitlab.youdo.sg/youdo/microservices/youdo-business-tickets/-/merge_requests/112), source approved task branch, target master. Preserved project squash=true and source deletion settings. Independent review found no actionable issues. GitLab initially returned 422 while mergeability was checking; GET confirmed opened/checking before retry. Merge succeeded: `4d711bc290789dd341f3c3182889837d41588b91`; squash `49f0856a67092dc15cf9aea8956a43adea91b87a`. MR pipeline 141041 was running at merge. Runtime deployment completion not claimed. The helper first rejected an abbreviated expected SHA without remote changes; retried with the full SHA.

## Follow-up: nodes-api OpenAI connectivity

User supplied a screenshot showing a 10-second connection timeout to api.openai.com:443 and requested SSH checks as youdo. Connected read-only to 10.18.26.48; hostname vk-ms1-nodes-api. Host resolver systemd-resolved uses upstream 10.18.20.3 and resolves api.openai.com to corporate proxy address 10.255.0.31; chatgpt.com resolves to 10.255.0.11. Route to 10.255.0.31 goes through 10.18.26.254 on ens3, source 10.18.26.48.

Host curl to https://api.openai.com/v1/models failed with connection timeout after 10002 ms, before TLS or HTTP. TCP probes to 10.255.0.31:443 and 10.255.0.11:443 both timed out. Control HTTPS to https://example.com succeeded with HTTP 200, connect 0.054 s, TLS 0.118 s.

Service runs in Docker container nodes, image registry.nodes.ws/nodes:1.8.2, network nodes_default. Via sudo docker exec nodes node, DNS likewise returned 10.255.0.31; TCP to api.openai.com:443 timed out while example.com:443 connected. Docker read access required sudo -n; no configuration or services were changed. Checks used getent, curl, ip route get, resolvectl dns, nc and Node dns/net modules. No credentials or authenticated OpenAI calls used.

Finding: reproduced network reachability failure from both the host and service container to the corporate OpenAI proxy range. Exact failing hop / firewall rule remains unverified; need route/ACL/proxy-side review for source 10.18.26.48 to 10.255.0.31:443 (also 10.255.0.11:443). This is separate from the Jarvis-to-nodes host override and occurs before API authorization.
