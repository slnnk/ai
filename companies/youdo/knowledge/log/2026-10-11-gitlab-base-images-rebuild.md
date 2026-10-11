---
system: gitlab
status: verified
checked: 2026-10-11
tags: [gitlab, registry, recovery, base-images]
---
# GitLab base-images dependency-aware recovery

## Summary

- The user authorized rebuilding existing base-images tags with dependency ordering.
- All54eligible pipelines were launched; no duplicate pipeline IDs or refs.
- Snapshot: 42 successful, 12 failed, 0 running; three verified seeds preserved, two blocked, one invalid tag excluded.
- Independent authenticated registry verification passed for all51 completed-image/version/latest targets at `2026-10-11T18:54:09.496577+00:00`.
- Dependency and overlapping tag order were independently audited; no orchestration errors found.
- Final pipeline [libreoffice6.0-focal](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140593) also succeeded; the coordinator exited0 with no queued or active pipelines.
- Failed builds need separate network/source/Dockerfile remediation; repository files were not changed.
- The local coordinator finished; no waiting or active pipelines remain.

## Task

The user explicitly requested: "Запусти ты пересборку образов, с учетом зависимостей." This authorizes rebuilding existing base-images tags and publishing their images through the project CI. No repository edits, tag moves, commits, deployment or other-project builds were performed.

## Context

Project `youdo/base-images`, ID483, https://gitlab.youdo.sg/youdo/base-images. Backup excluded registry payloads. Existing bootstrap `docker:git`, `docker:dind` and `microsoft/aspnet:10.0` were independently verified and preserved. See [restore audit](2026-10-11-gitlab-restored-server-verification.md) and [system map](../systems/gitlab.md).

## Actions

Read-only remote inventory of all60 Git tags and exact Dockerfile commits, including BOM-aware FROM parsing. A local operational helper persists pipeline IDs and dependency state, validates tag SHA before creation, uses at most four active pipelines and verifies published manifests after successful build jobs. The approved execution command is:

```sh
python3 /home/slnnk/ai-data/gitlab-recovery/rebuild_images.py run --execute --concurrency 4 --interval 20
```

Initial launches: Terraform1.7.5 pipeline140545, kubectl1.34.0 pipeline140546, Packer1.10.2 pipeline140547 and SDK10 pipeline140548. All final IDs/results are persisted in the generated state and summarized below.

## Findings

60tags: 59have Dockerfiles. `not-exist/none` is excluded. Three verified seed images are preserved.55tags are eligible for rebuild; `nomad-n-tools/1.1+latest` is blocked because authenticated registry GET for its external parent `registry.youdo.sg/sysadmins/nomad:latest` returns404.

Required parent order: `microsoft/aspnet/6.0-focal` before `6.0-focal-libreoffice`; `microsoft/aspnet/8.0` before `8.0-libreoffice`. Serialize overlapping tags: AWSCLI2.7 before2.13 for `latest`; dotnet-core-aspnet3.1+latest before patched3.1; dotnet-sdk8.0 before8.0+latest. Failed parent builds block dependents. Failure of an older overlapping tag does not block the newer version.

`elasticsearch/8.5.2-m1` requires external Nexus image `msk3-nexus.youdo.corp/elasticsearch/elasticsearch:8.5.2-arm64`; availability is only proven by the actual build. Historical upstream package/image availability may cause failures. Rebuilt images need not have pre-loss digests.

## Changes

Local helper `/home/slnnk/ai-data/gitlab-recovery/rebuild_images.py`, inventory/state `/home/slnnk/ai-data/gitlab-recovery/rebuild-state.json`, delegated local audit `local-dependencies.json`; this work log, existing GitLab map and shared backlog. Credentials stay in process memory. External mutations are pipeline creation and the resulting image publications, within the user-requested rebuild.

## Risks and limits

No repository fixes are included. Historical broken Dockerfiles require the separate task-branch approval mandated by supervised workflow. Recovery of the external Nomad parent is not claimed. Successful CI plus registry manifests establish image publication, not workload deployment or runtime correctness.

## Portable lesson

none


## Launch outcomes
All54pipelines were created, IDs140545–140598. Current status snapshot: `{"success": 42, "failed": 12, "seeded": 3, "blocked": 2, "excluded": 1}`. The three seed images were not rebuilt. Registry read-only verification: all51 expected targets matched their final publisher digests, including ordered latest aliases and the final LibreOffice image. Compact per-tag results: `/home/slnnk/ai-data/gitlab-recovery/rebuild-results.csv`; complete state/error evidence: `rebuild-state.json`; independent digest audit: `rebuild-verification.json`.

| Failed tag | Pipeline | Observed blocker |
| --- | --- | --- |
| `microsoft/aspnet/8.0` | [140549](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140549) | Debian HTTP endpoint10.255.0.50 timeout |
| `microsoft/dotnet-aspnet/6.0` | [140554](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140554) | Debian HTTP endpoint10.255.0.50 timeout |
| `awx-ee/24.6.1` | [140555](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140555) | Nomad download from hashicorp-releases.yandexcloud.net returned HTTP504 |
| `microsoft/aspnet/6.0` | [140557](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140557) | Debian HTTP endpoint10.255.0.50 timeout |
| `microsoft/dotnet-aspnet/5.0` | [140558](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140558) | Debian HTTP endpoint10.255.0.50 timeout |
| `maven/3.8.6` | [140567](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140567) | Old jq/libjq1 Debian package URLs return404 |
| `microsoft/dotnet-core-sdk/3.1-gdilibs` | [140572](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140572) | Mono GPG keyserver: Cannot assign requested address |
| `curl/8.2.1+latest` | [140575](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140575) | Pinned curl8.2.1-r0 APK package selection fails |
| `microsoft/dotnet-sdk/6.0-nodejs-cake` | [140577](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140577) | Debian HTTP timeout; package dirmngr unavailable |
| `elasticsearch/8.5.2-m1` | [140585](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140585) | External Nexus parent8.5.2-arm64 not found |
| `openjdk-11/gradle-7.5.1+latest` | [140591](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140591) | Base gradle-7.5.1-openjdk-11 unavailable/unauthorized |
| `microsoft/aspnet-6/6.0+latest` | [140592](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140592) | Unpinned dotnet-trace10 incompatible with net6.0 |

Two unlaunched tags: `microsoft/aspnet/8.0-libreoffice` waits for its failed parent; `nomad-n-tools/1.1+latest` lacks external `sysadmins/nomad:latest`. `not-exist/none` is excluded because no Dockerfile exists at the tag commit.

Read-only comparison proved Debian HTTP timeouts affect both runners105/docker-1 and106/docker-2. SDK/ASP.NET10 succeeded on the same runner106. Workstation deb.debian.org DNS is public Fastly; build logs show10.255.0.50. Hypothesis: an unreachable shared DNS-rewritten mirror/cache or apt proxy. Exact configuration origin is not proven; no remote repair was attempted.
