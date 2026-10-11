---
system: gitlab
status: verified
checked: 2026-10-11
tags: [gitlab, recovery, registry]
---
# GitLab server and recovery state

## Summary

- GitLab CE 17.9.8 at `https://gitlab.youdo.sg`, recovered on `138.16.203.174`; root SSH available. Core services, health endpoints, API, repository HTTP reads and main checks pass on 2026-10-11.
- Registry enabled after explicit user approval on 2026-10-11; DNS is `138.16.203.174`, JWT authentication and authenticated `/v2/` checks pass. Base-images recovery later launched54pipelines:42succeeded,12failed;51completed/seed version/latest targets are independently verified, including Terraform1.7.5. Two tags remain blocked by parents. Missing backed-up artifacts and images are expected by the user. See the batch rebuild section for remaining image blockers.
- Silent Mode was disabled with explicit user approval on 2026-10-11; API mutation returned HTTP200/false. Independent GET and database reads confirmed persisted false at approximately 15:36–15:37 UTC. Generic webhook-disabled banners could arise solely from the former Silent Mode.
- Evidence and detailed limits: [restore verification](../log/2026-10-11-gitlab-restored-server-verification.md). Live follow-ups are in `~/ai/TODO.md`.

## Access and storage

- Existing API token variable `GITLAB_YOUDO_TOKEN` in `~/ai/current/.env`; administrator account ID 184. Never record token values.
- `/var/opt/gitlab` -> `/data/gitlab` on ext4, approximately 1.1T total / 62G used. Root 20G / 6.4G used; RAM 19Gi / 5.4Gi used.
- API snapshot: 498 projects, 254 users, 67 active. Project 216 `sysadmins/automation-services` tested via smart HTTP refs and README reads.
- Verified new ECDSA Git SSH host fingerprint: `SHA256:B8orh9AIJGui+bDHs9P6YqsDRhCCIIiEVnCB8WoLT9A`; obtained through trusted root SSH. Git SSH passed via the trusted IP host-key alias, returning master `7cff3d8c7006a0a2bf58b9b224a329326f921dbf`. Default domain SSH still has the prior-key mismatch; no `known_hosts` edit occurred.

## Recovery and registry

- Backup `/var/opt/gitlab/backup/1791595878_2026_10_10_17.9.8_gitlab_backup.tar`, about 26G, created `2026-10-10T01:31:18Z`; skips builds, artifacts, registry, packages.
- Old GitLab and registry endpoint `89.169.136.178` was functional in the [Jenkins recovery dependency audit](../log/2026-10-11-jenkins-devops-890-inventory-dependencies.md). Exact former backend cohosting was not established by KB.
- Registry DNS initially resolved to the old IP. The user changed it themselves; local and recovered-host checks now resolve `138.16.203.174` (TTL299). Before approved enablement, the recovered host had registry explicitly disabled in `/etc/gitlab/gitlab.rb:2140-2141` and effective YAML, despite a configured `registry_external_url`; no registry service runs. New project 625 job 3217894 fails pulling its Terraform image with connection timeout.
- After DNS update, `/v2/` HTTP401 challenges `service="dependency_proxy"`; only the GitLab Nginx vhost exists, no registry Nginx configuration or `/opt/gitlab/service/registry`. `/jwt/auth?service=container_registry` HTTP404. This pre-enablement endpoint was not a working registry despite HTTP401.
- User explicitly authorized `Включи registry`. Backup `/etc/gitlab/gitlab.rb.before-registry-20261011T155957Z` mode0600; recovery flags `registry['enable']` and `gitlab_rails['registry_enabled']` set true, registry Nginx certificate/key point to existing `/etc/gitlab/ssl/gitlab.youdo.sg.crt` and `.key`. Certificate SAN covers both names and is valid August 31–November 29. `gitlab-ctl reconfigure` exited0; registry running around 16:01 UTC.
- Current public `/v2/` has correct container_registry challenge and registry/2.0 header; PAT JWT endpoint HTTP200 and authenticated `/v2/` HEAD HTTP200. Terraform manifest `youdo/base-images/terraform:1.7.5` HTTP404 reflects expected missing images. The bootstrap image pair was later published under explicit approval; no CI retry occurred.
- Local health/readiness/liveness checks return HTTP200 after reconfigure. Public monitoring HTTP404 follows whitelist `127.0.0.0/8`, `::1/128` and does not imply outage; login HTTP200 after transient startup502. SMTP and `gitlab_email_enabled` remain false per recovery configuration; no mail changes authorized or performed.
- Missing historic artifacts and container images are expected. Database artifact rows alone do not demonstrate restored payload files.

## Webhooks and background jobs

- When enabled, Silent Mode makes `WebHooks::AutoDisabling.disabled` return all hooks and `executable` return none; UI banner wording about retries is generic. Hook status API must be interpreted together with global Silent Mode.
- User explicitly approved one `PUT /api/v4/application/settings` setting `silent_mode_enabled: false`; TLS verified and request pinned to the recovered IP. HTTP200 returned false; independent GET and database reads confirmed persisted false. The other agent-performed external actions were the explicitly approved hook 109 Push test and registry enable/reconfigure; registry DNS was changed by the user.
- Historical hook 56 `youdo.myjetbrains.com` HTTP404; hook 72 `youtrack.youdo.com` HTTP401; hook 109 same current domain HTTP204 and zero recent failures. Inspected latest deliveries were October 9.
- Restored YouTrack tooling token still works (`users/me` HTTP200, account `25-546`); its 14 VCS integrations include enabled automation-services `230-3`, server `155-1` GitLabServer, Site project `66-0`. User-approved hook 109 Push test returned HTTP201 and follow-up `push_hooks` delivery HTTP204 at `2026-10-11T15:45:58.390632Z`, duration `0.052193`; `recent_failures=0`, `disabled_until=NULL`. Current delivery/authentication works; no evidence of lost current secret. Issue updates/linkage are not verified end to end. Hooks 56/72 remain historical legacy findings.
- Preexisting background migration ID 332, `SetProjectVulnerabilityCount`, targets `project_settings.project_id` and raises missing-class NameError. Created April 26, updated June 16. See [official 17.x upgrade notes](https://docs.gitlab.com/update/versions/gitlab_17_changes/); no repairs performed.
- Recent Rails/Nginx logs show no sampled server errors. Secrets doctor is only partially verified while running; zero failures shown for inspected models, not a completed full-scan result.

## Base-image pipeline bootstrap

After registry enablement, job [3217900](https://gitlab.youdo.sg/youdo/base-images/-/jobs/3217900) fails at executor preparation because `registry.youdo.sg/youdo/base-images/docker:dind` is absent. The tag-build template also requires `registry.youdo.sg/youdo/base-images/docker:git` as its job image. Their repository Dockerfiles depend only on public `docker:20.10.17-dind` and `docker:20.10.17-git`, respectively; manually building/pushing this exact pair under separate approval can remove the bootstrap cycle. Full build still needs external package/image access and credentials. The initial research performed no seed or repository changes; subsequent explicit `Собери и запушь` approval completed publication of both bootstrap tags. git digest `sha256:a20947f03eb44288957ccc5a6deb39e986a7bf286274c0ea321995b86af7cf7a`; dind digest `sha256:25d0dc348346212a869c21cb5339b0b2071bd40f663433a81000114ad3c1a5e6`; independent manifest/config verification and Linux/amd64 checks pass. Original git Dockerfile required a task-run-only `--upgrade curl libcurl` adjustment due curl/libcurl ABI mismatch; repository unchanged. No CI retry was launched; detailed commands and limitations are in the [audit](../log/2026-10-11-gitlab-restored-server-verification.md).


## Verified recovered ASP.NET image

On 2026-10-11, [job 3217903](https://gitlab.youdo.sg/youdo/base-images/-/jobs/3217903) successfully rebuilt and published `microsoft/aspnet:10.0`. Both login steps passed, superseding the earlier Nexus blocker for this job. Independent manifest/config GETs confirmed Linux/amd64 and digest `sha256:d92d424dec5d317feaade3f96547ebf8a6cbfc6362d6cb766946160fdecdf2d7`, matching the push trace. Other images and runtime execution remain unverified.


## Base-images batch rebuild

User explicitly authorized dependency-aware rebuilding on2026-10-11. Remote inventory has60tags,59Dockerfiles. Three verified bootstrap/ASP.NET10 tags are preserved. All54unblocked pipelines were launched with at most four active pipelines; snapshot: 42 success and12failed; the coordinator finished, no pipelines remain active. Authenticated manifest verification passed for all51 completed/seed version/latest targets. ASP.NET8 failed at Debian HTTP download and its LibreOffice child was not launched. `nomad-n-tools/1.1+latest` is blocked by missing external `sysadmins/nomad:latest` (authenticated manifest404); `not-exist/none` is excluded. Parent image and overlapping latest/version tags are ordered. IDs and final outcomes: [batch work log](../log/2026-10-11-gitlab-base-images-rebuild.md); live generated state is `/home/slnnk/ai-data/gitlab-recovery/rebuild-state.json`.
