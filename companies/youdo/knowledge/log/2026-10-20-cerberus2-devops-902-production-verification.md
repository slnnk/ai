---
system: cerberus2
status: verified
checked: 2026-10-20
tags: [nomad, production, DevOps-902]
---
# Cerberus2 DevOps-902 production verification after internal .NET 2.1 image rollout

## Task

User reported merging MR27, creating a release tag, and deploying all test stands and production. Requested a read-only production health check of Nomad job `cerberus2` at `nomad.service.selectel.consul:4646`. No repair, restart, configuration change or deployment authorized/performed.

## Context

Source checkout `/home/slnnk/git/cerberus2`; [consumer image history](2026-10-15-base-images-dotnet21-mirrors.md). Credentials loaded from `current/.env`: `SELECTEL_PROD_NOMAD_TOKEN`, `CONSUL_HTTP_TOKEN`, `GITLAB_YOUDO_TOKEN`; values not logged. Production SSH route: `root@172.24.0.12`, existing workstation key. Sanitized generated evidence under `~/ai-data/gitlab-workflow/cerberus-dotnet21/cerberus2/`: `prod-status.json`, `prod-followup.json`, `container-probe.json`, `release-check.json`.

## Actions

Queried Nomad job/summary/deployments/allocations/stats and bounded stdout/stderr logs via GET. Queried Consul service health for `cerberus2` and `cerberus2-api`. Verified MR/tag/pipeline through GitLab GET. Issued HTTP GET to API paths directly and through the production proxy; repeated from the production host and container network namespace. Used read-only Docker inspect/top to identify the container and process state. No raw environment, job templates or user records retained.

## Findings

- GitLab MR27 merged at `2026-10-20T00:45:02.967+03:00`, merge commit `b87d8268c709eaa4bd539ac059a8bf236c64afd5`; tag `1.0.10` points to it. Pipeline141231 SUCCESS: all three image builds, all14 requested per-stand test deploy jobs, production stop/canary/update/start, release and monitoring jobs SUCCESS. Test runtime was not independently inspected in this task.
- Production Nomad job version11, stable/running, release metadata `VERSION=1.0.10`, image prefix `nexus.youdo.com/youdo/cerberus2`. Deployment `006ef1c4-2377-4d36-94af-3268fbd4d52f` successful, desired/healthy API1 and workers3; unhealthy/queued/failed/lost0. Active allocations: `c2f68a1d` on nomad01, `dc993e2d` on nomad03, `fa47e938` worker and `f9da691d` API on nomad02. All processes running with restart count0 through the final check at approximately00:59:57Moscow. API started00:50:20, workers00:52:47.
- Consul checks all passing; configured service checks are TCP only and do not establish HTTP or business readiness.
- All three worker logs reached `Finished BecomeActive` and lifecycle stage20000 by00:52:58. The final startup membership view contains3Active/343Dead/0Joining. This is log evidence, not an independent membership SQL query. Two startup Error events at00:52:55 concerned pings to old silo generations; those were superseded within seconds by successful activation. No later non-check warning/error found through the final sample; repeating connection-preamble warnings are consistent with the configured TCP checks. No observed `25006`, `53300`, startup loop or stderr output. Background worker business processing was not functionally tested.
- **Production API HTTP failure verified:** GET `/v1/sources` and `/swagger/index.html` received no HTTP bytes within6–15s. The failure repeats from the workstation, production host, Docker bridge `172.17.0.39:80`, and inside container network namespace at `127.0.0.1:80`; TCP connects in~0.1–0.3ms inside the host/container. Proxy GET `/v1/sources` also times out. Source has no Swagger middleware, so that route should return404 rather than hang; it is a basic HTTP responsiveness probe, not proof that Swagger is configured.
- API container `20941acedb72`, image `nexus.youdo.com/youdo/cerberus2/api:1.0.10`, host bind `172.24.0.12:23530` to container80. Loopback host127.0.0.1:23530 is not bound and returns connection refused; that probe is not evidence of a service failure. The container is running, not restarting or OOM-killed. `dotnet` process PID3716787 stateSLl,626threads,~1.2%CPU at check time. Thread count is an observation; thread starvation/deadlock or the cause of HTTP hangs has not been established.

## Changes

Only local diagnostic scripts/evidence and KB bookkeeping. Closed the completed internal-image source/publication task with merge/tag/deploy evidence; tracked the newly verified HTTP failure separately in [central TODO](../../../../TODO.md). Updated the consumer-image log and repository map. No external changes.

## Status and risks

Image switch and release delivery completed. Production rollout is green at scheduler/TCP level but API HTTP health failed, including inside the container. Production acceptance cannot be claimed. Root cause and any repair remain unresolved; no restart or rollback attempted. No ban/unban/massban requests or other mutation endpoints called.

## Portable lesson

none


## Test API comparison requested by user 2026-10-20

Read-only comparison covered all14stands `test`, `test1`–`test7`, `test10`–`test15` in VK Nomad. Discovered current API IP/port from each running allocation. Direct HTTP GET `/v1/sources` returned200 with a valid JSON list of9sources on every stand; the source controller calls `ISourcesRegistryGrain.Sources()` through Orleans, so this verifies an application route beyond TCP readiness. No returned source records or user data retained. GET `/__cerberus_readonly_probe__` returned404 on all14, confirming ordinary HTTP routing responsiveness. This differs from the production timeout observed above; it does not establish its cause.

All14current allocations healthy, all14API tasks restart0. Three worker tasks have one historical restart each on test2/test10/test15; this check does not diagnose their cause or claim all workers never restarted. Successful source-request timings range0.123–7.872s; test12 was slowest7.872s. These are single requests, not a latency benchmark or sustained availability test. No mutation endpoints, infrastructure changes or repair performed. Sanitized per-stand result: `~/ai-data/gitlab-workflow/cerberus-dotnet21/cerberus2/test-api-status.json`. No new open test failures; the existing production HTTP issue remains open in central TODO.


## Process diagnosis and user API restart 2026-10-20

Before the user restart, the API process thread count grew from626 to859, with852threads waiting in `futex_wait_queue_me`; test5 had44threads. The production process was not CPU-quota-throttled (`nr_throttled=0`, no quota), PID-limited (`pids.max=max`, maxevents0), or out of memory (memoryfailcnt0, ~306MiB cgroup usage against2GiB). Both prod and test5 use `nexus.youdo.com/youdo/cerberus2/api:1.0.10`; image configuration digests were not compared. Production has40host CPUs, test5 has16; no evidence attributes the hang to that difference. The high/growing blocked-thread count makes application blocking/thread starvation a working hypothesis, not a proven managed stack diagnosis.

Code investigation: `src/Cerberus.API/IocModule.cs` creates the singleton Orleans client synchronously via `client.Connect().GetAwaiter().GetResult()` inside `WaitAndRetryForever` with1sdelay, without logging caught failures in that factory. An API/Orleans initialization blockage during rollout is therefore a candidate mechanism. No stack trace or dependency evidence proved that this was the specific blocked operation. A read-only SSH dependency diagnostic timed out without a result; no DB queries or network probe outcomes from that attempt are claimed.

User independently restarted API. Nomad confirmed restart1 and new API `StartedAt=2026-10-19T22:04:45.735286042Z` (01:04:45Moscow); worker restart counts remain0. Previous process terminated with137 after the explicitly requested restart; this does not establish OOM. New container `c8eb9857f250`, dotnetPID3750909, same image1.0.10,69threads vs859 before. No CPU throttling/PID exhaustion/memory failure observed after restart. Runtime comparison evidence is `runtime-comparison.json` (latest snapshot; pre-restart counts retained in this note).

Post-restart verification: production proxy GET `/v1/sources` HTTP200, valid response521bytes in0.169s; independent curl returned200 in0.193057s. Unknown `/swagger/index.html` returns404 again, as expected for an unconfigured route. All Nomad/Consul checks remain passing; no new API startup Error/Fatal/stderr observed. `prod-status.json` now holds the post-restart snapshot, superseding the initial failure snapshot whose observed facts remain above. The user restart restored HTTP service; root cause and recurrence risk remain unresolved. No agent restart, deployment, resource/configuration or code change performed.

## YouTrack update preparation

User requested an image-update comment in DevOps-902. Read-only GET verified issue71-138572, expected Cerberus2 image-switch title, and zero existing comments. Prepared exact Russian text in `~/ai-data/gitlab-workflow/cerberus-dotnet21/cerberus2/youtrack-comment.txt`: internal image references, MR27/release1.0.10/releaseCI141231, all14test HTTP successes, production HTTP recovery after user restart, cause unproven. Creating a single comment awaits explicit per-action external-write confirmation; no tracker write performed.

Task-specific user edit: removed the entire final API-validation/production-hang/restart paragraph from the proposed DevOps-902 comment. Final proposed text contains only internal SDK/runtime references and MR/release/successful pipeline/deploy summary. This supersedes the earlier draft description; publication remains unapproved and unperformed.

User explicitly approved publication of the shortened comment. Created DevOps-902 comment `74-124711` and verified exact text by GET; SHA256 `1f2ac9d8699c1f0588fef5d4f165a1380dbf1db64547ae512fb1a9648aab5599`. It contains only internal image references and MR27/release1.0.10/successful pipeline/deploy summary; the excluded API diagnosis paragraph was not published. Receipt: `~/ai-data/gitlab-workflow/cerberus-dotnet21/cerberus2/youtrack-comment-receipt.json`. Earlier pending-publication status is superseded; existing root-cause backlog item unchanged.

## Final user disposition 2026-10-20

User explicitly closed the remaining Cerberus2 production-hang investigation as unnecessary. Central TODO entry is closed as cancelled diagnostics, not as an implemented fix. HTTP recovery after the user API restart remains verified; the original root cause remains unproven. Prior pending-investigation wording is superseded by this decision. No further diagnosis or external change performed.
