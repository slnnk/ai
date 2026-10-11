---
system: gitlab
status: verified
checked: 2026-10-11
tags: [gitlab, recovery, registry]
---
# Restored GitLab server verification

## Task

Check GitLab after backup recovery on another machine. Read-only SSH and API checks were authorized. The user later explicitly approved disabling Silent Mode ("Disable Silent Mode"), testing webhook 109, and enabling registry ("Enable registry"); these three bounded external actions were executed. The user subsequently authorized building/pushing the exact bootstrap image pair ("Build and push"), which completed. No repository changes or Git mutations were performed.

## Context

- Public GitLab: `https://gitlab.youdo.sg`; recovered host: `138.16.203.174`, SSH as `root`.
- Existing API credential: `GITLAB_YOUDO_TOKEN` in `~/ai/current/.env`; authenticated account ID 184, administrator. Credential values were not recorded.
- Earlier registry and GitLab public endpoint: `89.169.136.178`, verified in the [Jenkins dependency audit](2026-10-11-jenkins-devops-890-inventory-dependencies.md).

## Actions and key checks

Read service status, sanitized configuration, filesystem usage, backup metadata, recent error classes, installed application source, and database metadata. Used `gitlab:check`, health/liveness/readiness HTTP GETs, authenticated GitLab API GETs, smart HTTP repository refs/file reads, and SSH host-key comparison through the trusted root SSH session. The `gitlab:doctor:secrets` scan was still running at the time of this entry; partial results below are not a complete success claim.

## Findings

- Omnibus GitLab CE `17.9.8`; main checks and migrations pass. `/-/health`, `/-/liveness`, and `/-/readiness` return HTTP200; database, Redis and Gitaly checks succeed. TLS and authenticated API work.
- API contains 498 projects, 254 users, 67 active users. Project 216 `sysadmins/automation-services` smart HTTP refs and README reads return HTTP200.
- `/var/opt/gitlab` points to `/data/gitlab`, ext4, approximately 1.1T total / 62G used. Root filesystem 20G / 6.4G used; RAM 19Gi / 5.4Gi used.
- SSH Git host key changed after recovery. ECDSA fingerprint `SHA256:B8orh9AIJGui+bDHs9P6YqsDRhCCIIiEVnCB8WoLT9A` matched through trusted root SSH. Git SSH transport passed with `HostKeyAlias=138.16.203.174`, using the already trusted IP key; `git ls-remote` of `refs/heads/master` returned `7cff3d8c7006a0a2bf58b9b224a329326f921dbf`. No `known_hosts` edit occurred. Default domain-based SSH still has the old-key mismatch; affected clients need the verified key.
- Silent Mode was initially enabled. Source `app/models/concerns/web_hooks/auto_disabling.rb:42-43` returns all hooks from the disabled scope in Silent Mode; `HasWebHooks.any_hook_failed?` calls `hooks.disabled.exists?`, which triggers the generic retry-failure banner. This banner alone does not prove new delivery failures. Redis callout cache expires after one hour; API `alert_status: executable` does not override global Silent Mode.
- At approximately 15:36 UTC the user approved disabling Silent Mode with "Disable Silent Mode". A single authenticated `PUT /api/v4/application/settings` with `silent_mode_enabled: false`, pinned to `138.16.203.174` with verified TLS, returned HTTP200 and `silent_mode_enabled: false`. Independent application-settings GET returned false and direct database read confirmed persisted `f` at approximately 15:36–15:37 UTC. Together with the subsequently approved hook 109 test, this was one of exactly three agent-performed external actions; registry DNS was updated by the user.
- Historical hook 56 targets `youdo.myjetbrains.com`, latest HTTP404, 326 logs; hook 72 targets `youtrack.youdo.com`, latest HTTP401, 523 logs. Hook 109 targets `youtrack.youdo.com`, latest HTTP204, 523 logs, `recent_failures=0`. Latest inspected deliveries were October 9, before this restore.
- Registry DNS initially remained `89.169.136.178`, the old endpoint, and timed out. The user subsequently updated DNS themselves: local and recovered-host resolution now returns `138.16.203.174` (observed TTL299). Before enablement, `/etc/gitlab/gitlab.rb:2140-2141` explicitly disabled registry; effective application YAML also had registry disabled. `registry_external_url` existed, but no registry service was running.
- After the user DNS change and before enablement, registry `/v2/` returned TLS-verified HTTP401, but the authentication challenge uses `service="dependency_proxy"`: this is the GitLab Dependency Proxy fallback, not a functioning container registry. There was no Nginx registry configuration or `/opt/gitlab/service/registry` directory, only the GitLab vhost. `/jwt/auth?service=container_registry` returns HTTP404. Registry was still disabled at that point; HTTP401 alone is insufficient acceptance evidence.
- Project 625 `sysadmins/vkcloud-tf`, job 3217894 fails with `runner_system_failure`: image `registry.youdo.sg/youdo/base-images/terraform:1.7.5` cannot be pulled because the registry connection times out.
- Backup `/var/opt/gitlab/backup/1791595878_2026_10_10_17.9.8_gitlab_backup.tar`, approximately 26G, metadata created `2026-10-10T01:31:18Z`, skips `builds`, `artifacts`, `registry`, and `packages`. The user explicitly confirmed missing artifacts and container images are expected for this recovery.
- Database has 306118 artifact rows with local `file_store=1`; six actual local files were found. Sample archive for job 3217826 / artifact 567 returns HTTP404. This is expected given excluded artifacts, not an additional restore defect.
- Recent Rails tail has no WARN/ERROR/FATAL or HTTP>=500; Nginx error log empty. Sidekiq repeatedly warns `NameError: uninitialized constant Gitlab::BackgroundMigration::SetProjectVulnerabilityCount` in `Database::BatchedBackgroundMigration::MainExecutionWorker`. Migration ID 332 targets `project_settings.project_id`, status 1, created April 26 and updated June 16; it predates recovery. This class mismatch is documented for GitLab 17.4 to 17.5 in [official upgrade notes](https://docs.gitlab.com/update/versions/gitlab_17_changes/). No remediation was attempted.
- The user explicitly instructed "Enable registry". One approved SSH action backed up `/etc/gitlab/gitlab.rb` to `/etc/gitlab/gitlab.rb.before-registry-20261011T155957Z` (mode0600), changed recovery flags `registry['enable']` and `gitlab_rails['registry_enabled']` from false to true, and set `registry_nginx['ssl_certificate']='/etc/gitlab/ssl/gitlab.youdo.sg.crt'` and `registry_nginx['ssl_certificate_key']='/etc/gitlab/ssl/gitlab.youdo.sg.key'`. Existing certificate SAN covers both GitLab and registry, valid August 31–November 29. `gitlab-ctl reconfigure` exited 0 and restarted Puma, Sidekiq, Nginx; registry PID 83414 was running at approximately 16:01 UTC.
- After transient startup HTTP502, login returns HTTP200. Public registry `/v2/` now returns the correct HTTP401 challenge (`service="container_registry"`, `Docker-Distribution-Api-Version: registry/2.0`). Existing PAT obtains HTTP200 from GitLab `/jwt/auth`; authenticated registry `/v2/` HEAD returns HTTP200. Terraform image manifest `youdo/base-images/terraform:1.7.5` returns HTTP404, expected because backup excluded images. No CI retry or image publication was performed.
- Local health/readiness/liveness with `--resolve gitlab.youdo.sg:443:127.0.0.1` return HTTP200 after reconfigure. Public health/readiness now return HTTP404 due generated monitoring whitelist `127.0.0.0/8`, `::1/128` (`gitlab.yml:793-795`); this is an access limitation, not an outage. Initial pre-reconfigure public HTTP200 results above describe the earlier state. Silent Mode remains persisted false.
- Recovery configuration has SMTP and `gitlab_email_enabled` false. Registry approval did not authorize enabling email; these settings were retained.
- The user reported YouTrack was also restored. Existing `YOUTRACK_TOKEN` succeeds: `GET /api/users/me` HTTP200, login `a.solonenko`, ID `25-546`; `GET /api/admin/integrations/vcsHostingProcessors` HTTP200 returns 14 integrations. Automation-services integration `230-3` is enabled, server `155-1` (`GitLabServer`), project Site `66-0`. No credential loss or rotation is established; webhook-specific credentials are separate from the working tooling token. The user explicitly approved the hook 109 Push test ("Send test #109"). One `POST /api/v4/projects/216/hooks/109/test/push_events`, pinned to `138.16.203.174`, returned HTTP201 Created. Follow-up database log for `push_hooks` confirms HTTP204, duration `0.052193`, at `2026-10-11T15:45:58.390632Z`; the previous entry was also HTTP204 at `15:45:43.857373Z`. Hook 109 has `recent_failures=0`, `disabled_until=NULL`. Current delivery/authentication works after recovery; issue updates/linkage were not verified end to end. Hooks 56 and 72 remain historical legacy-cleanup findings.
- Partial `gitlab:doctor:secrets` output reports zero failures for many models, including User, WebHook, Integration and ApplicationSetting. Full completion remains unverified. The scan began approximately 15:27 UTC; remote Ruby PID 77979 was still running after 19:21 at approximately 15:46 UTC. Root agent execution session 66856 holds its output; sessions are agent-scoped, so delegated monitoring cannot read that session. Do not terminate the remote scan merely to finish the audit.

## Base-image bootstrap investigation

- [Job 3217900](https://gitlab.youdo.sg/youdo/base-images/-/jobs/3217900), tag `microsoft/aspnet/10.0`, fails during `prepare_executor`: missing manifest `registry.youdo.sg/youdo/base-images/docker:dind`, runner 105 docker1 (`172.28.0.171`). Registry service works; absent image payload is the current blocker.
- Read-only local research of `/home/slnnk/git/base-images` (clean HEAD `1600dcf7ed81fe268ef5e1b9cf925eaeb25736c9`) and `/home/slnnk/git/gitlab-ci-templates` (clean HEAD `69cec4d8b8cf742b74ef6db6c21134293dee1997`). Local tag `microsoft/aspnet/10.0` points to `4dad59bc3be954df6e65cd2192a7cb6548737724`; Exact GitLab API reads at job commit `a6d14d5fa5f9989865f23b6ac962e0df8a1b8b50` independently confirm public FROM values `docker:20.10.17-git` and `docker:20.10.17-dind`; local tag is not the job commit. No repository edits were authorized or made.
- `.gitlab-ci.yml` includes `partials/.build-base-image-tag.yml` from templates master, extends `.build_tag_single_baseimage_docker`. Exact bootstrap job image is `registry.youdo.sg/youdo/base-images/docker:git`; service is `registry.youdo.sg/youdo/base-images/docker:dind`, alias docker. Both must exist before the pipeline can build images including those bootstrap images themselves.
- `docker/git/Dockerfile` uses public `docker:20.10.17-git` plus `apk add --no-cache curl`. `docker/dind/Dockerfile` uses public `docker:20.10.17-dind`, creates `/sys/kernel/security` and `/lib/modules`, and adds curl. Both match current HEAD and local aspnet tag. No private FROM dependency blocks manual bootstrap.
- Once separately approved on a chosen build host with Docker and registry credentials, build with `docker build --platform linux/amd64 -f docker/git/Dockerfile -t registry.youdo.sg/youdo/base-images/docker:git .` and analogous `docker/dind/Dockerfile` / `docker:dind`; authenticate using `docker login --password-stdin`, then push these two exact tags. None of these build/login/push commands were executed by this investigation.
- Seeding both images removes the observed executor bootstrap blocker; it does not guarantee the entire build. Target aspnet uses public `mcr.microsoft.com/dotnet/sdk:10.0-resolute` and `mcr.microsoft.com/dotnet/aspnet:10.0-resolute`, external tool/package/CA downloads. Template uses buildx docker-container driver, which may need its public BuildKit image, and authenticates both registry and Nexus.
- A surviving runner Docker cache could supply the exact pair only if effective pull policy allows cached images (for example `if-not-present`); an `always` pull still requires registry manifests. Runner cache/pull-policy was not remotely investigated. Replacing template images with public Docker tags requires separately approved repository changes; manual seed avoids those edits.

## Approved bootstrap image publication

- The user explicitly instructed "Build and push", authorizing builds and publication of the exact `registry.youdo.sg/youdo/base-images/docker:git` and `docker:dind` pair. Local Docker27.2.0, Linux amd64; repository remained clean.
- Original dind Dockerfile built and container checks passed: Docker/dockerd20.10.17, curl8.5.0 and required directories. Local image ID `sha256:bfd120932fe1d11dc408570271339221c3a9b3e3c9ca32ffcc9d0721a0685f24`.
- Original git Dockerfile produced curl8.5.0 with libcurl7.83.1-r2; `curl --version` exited127 due missing `curl_global_trace`. A task-run-only Dockerfile `/home/slnnk/ai-data/gitlab-recovery/docker-git-bootstrap.Dockerfile` changes its RUN to `apk add --no-cache --upgrade curl libcurl`. No repository file changed. Rebuilt git image `sha256:a0d202e64c91704b44971e4c1a437d52f1d6eab82fc5f292d102f5ded65a0c1e` passes checks with curl/libcurl8.5.0, Docker20.10.17 and Git2.36.2.
- Generated `/home/slnnk/ai-data/gitlab-recovery/push_bootstrap.py` exposes `git`/`dind` choices and `--help`, pushing through Docker Engine Unix API with `X-Registry-Auth`; PAT stayed in process memory and no login credential file was written. Both pushes report `push_complete=True`.
- Published dind digest `sha256:25d0dc348346212a869c21cb5339b0b2071bd40f663433a81000114ad3c1a5e6`, manifest size3873; git digest `sha256:a20947f03eb44288957ccc5a6deb39e986a7bf286274c0ea321995b86af7cf7a`, size2625. Independent authenticated manifest/config-blob GETs verified both digests, config hashes against local image IDs, and Linux/amd64 architecture.
- The approved pair is now available; other missing images still require rebuilding/publication. No CI retry was launched and no Git mutations occurred. Durable repository curl/libcurl fix requires separate supervised branch approval; current-run repair remains outside the repository.

## Changed files

Created this log and the [GitLab system map](../systems/gitlab.md); added follow-up actions to `~/ai/TODO.md`. No repository files changed. The approved registry action changed `/etc/gitlab/gitlab.rb` and regenerated runtime configuration via reconfigure. External actions were explicitly approved and executed: settings PUT disabling Silent Mode, POST testing hook 109, remote registry enable/reconfigure, and publication of the exact bootstrap image pair. Temporary build/push tooling lives in `~/ai-data/gitlab-recovery`; repository files remained unchanged.

## Risks and limits

Registry is now enabled and authenticated access works; absent required images still block image-based CI. Missing old images and artifacts are accepted by the user. Silent Mode was disabled after explicit user approval; independent GET and database reads confirmed persisted false. Outbound webhook behavior can now resume. Historical webhook faults and the stale background migration require separate review. One manual hook 109 test was triggered after explicit approval. Registry configuration was repaired under explicit approval. The explicitly approved bootstrap pair was published; no pipeline retry, Git push or deployment was triggered.

## Verbatim approval evidence

```text
Да, отключи
Да, отправить тест #109
Включи registry
Собери и запушь
```

## Nexus dependency after bootstrap

Job [3217901](https://gitlab.youdo.sg/youdo/base-images/-/jobs/3217901) passed restored bootstrap image preparation and failed at Nexus login with connection refused. The user requested fresh Nexus on `10.18.24.233`; root SSH and existing separate `/data` disk are verified. A minimal external Ansible plan using existing roles is prepared, syntax-checked and bounded to one host; no apply yet. See [Nexus plan](2026-10-11-nexus-fresh-recovery-plan.md).


## ASP.NET 10 recovery verification

Read-only GET verification on 2026-10-11: user-provided [job 3217903](https://gitlab.youdo.sg/youdo/base-images/-/jobs/3217903) and pipeline 139034 report success, finished at 21:20:07 +03:00. Ref `microsoft/aspnet/10.0`, commit `a6d14d5fa5f9989865f23b6ac962e0df8a1b8b50`. Trace confirms both registry/Nexus logins succeeded and the manifest was pushed. Independent authenticated registry manifest and config-blob GETs verify `registry.youdo.sg/youdo/base-images/microsoft/aspnet:10.0`, Linux/amd64, digest `sha256:d92d424dec5d317feaade3f96547ebf8a6cbfc6362d6cb766946160fdecdf2d7`, matching the trace. This supersedes the Nexus login blocker for this job. No runtime container check, new pipeline, retry, publication or deployment was performed by this verification. SDK 10 was not verified. Local changes: this audit and the existing GitLab map.
