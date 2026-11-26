---
system: nexus
status: verified
checked: 2026-11-25
tags: [incident, storage, compaction]
---
# Nexus data disk exhaustion and current write health

## Task

Check the suspected Nexus disk exhaustion. Read-only production diagnosis.

## Context

[System map](../systems/nexus.md) and [November 5 incident](2026-11-05-nexus-devops-910-disk-diagnosis.md). Nexus on `msk3-nexus.youdo.corp` uses `/dev/vdb` mounted at `/data`.

## Actions

Read `df -hT / /data`, `df -i /data`, Nexus status, authenticated task and blob-store GETs, and bounded task, application and request logs through SSH.

## Findings

- November 25, 15:51–16:06 MSK: application logs recorded `No space left on device`. Nexus request logs show 47 HTTP 500 responses in the 15:51–16:06 minute buckets, 46 PATCH and one PUT.
- At 17:44 MSK, `/data` was 98% used with 4,899,594,240 bytes available (4.56 GiB). Root was 30% used with 6.8 GiB available, and data inode usage was 2%. Nexus reported about 164.9 GiB of content in `docker-hosted`.
- The scheduled `docker-hosted` compaction completed at 03:00. Later runs completed at 17:11 and 17:18 MSK. All 12 compaction tasks last reported OK and were waiting. Examined task logs did not report reclaimed byte totals.
- At 17:44 MSK, status and writable endpoints returned HTTP 200 and all 12 blob stores reported available. Observed Docker API writes from the 17:18 minute bucket onward included 8 POST and 8 PATCH responses with HTTP 202 and 12 PUT responses with HTTP 201. No synthetic write was sent.

## Changes

Local knowledge base only. The diagnostic initiated no production changes or background operations.

## Status and risks

The requested diagnosis is complete. Disk exhaustion occurred earlier today and successful writes were observed later, with a narrow capacity margin at the check. November 5 DevOps-910 remains historically closed. No cleanup, capacity change or new maintenance task was requested.

## Cleaner follow-up

Nexus request logs contain successful manifest deletion responses from the `cleaner` account on every day from November 11 through 25. The 04:00 MSK scheduled window on November 25 had 40 successful search requests and 32 manifest DELETEs accepted with HTTP 202. The 17:17 run had 43 successful searches and 12 accepted manifest DELETEs. The 17:44 user-triggered run (Nomad allocation `14b565bb-a96e-8d28-4d9d-efd65387f063`) completed with exit 0 and zero restarts, matching the user-supplied pagination and stop messages. Nexus logged 43 HTTP 200 search requests and zero manifest DELETEs for that run. The 17:17 allocation also completed with exit 0 and zero restarts. The parent remained enabled at 04:00 MSK.

The scheduled Docker compaction ran at 03:00 MSK, before the cleaner at 04:00. Physical space can be reclaimed by a later compaction. At 17:47 MSK the disk was still 98% used with 4.6 GiB available. The evidence rules out a sustained cleaner stoppage across the observed days. It does not quantify reclaimable bytes or establish whether retention is sufficient for current growth. The agent performed read-only checks only.

## Cleaner restart loop after retention change

The user reduced the age threshold and supplied fatal Docker manifest DELETE errors. In Nexus request logs from 17:57 MSK, the observed cleaner window contained 265 HTTP 202 responses and 20 HTTP 404 responses. Every 404 targeted an identical image path and digest already accepted with HTTP 202, typically in the same second. Nomad allocation `7384c3d3-58b0-5bf0-983e-6f42ca831fd7` had 21 restarts and was pending at the last read, with repeated exit 1 events. The local source enumerates tags, sends DELETE by image and digest, and exits on the first non-202 response. Duplicate digest requests explain the observed 404s; whether all duplicate candidates arise from distinct tags was not independently verified. The user-triggered run remained active at the last check. No production changes or cleanup were initiated by the agent. The disk had 4,949,708,800 bytes available during the request-log check.

## Compaction after the reduced retention run

The authenticated task API and task log confirm `Compact docker-hosted` ran at 18:03:06–07 MSK with `blobsOlderThan=0` and finished OK. The log records six empty directories removed and provides no reclaimed byte count. From 17:57 until that compaction started, Nexus recorded 332 accepted manifest DELETEs and 30 repeated 404s. At 18:05 MSK `/data` remained 98% used with 4.3 GiB available.

A read-only scan of local blob properties and allocated payload blocks after compaction found 36 soft-deleted payloads with 168,611,840 bytes allocated (161 MiB). About 165.1 GiB of layer payloads were not marked deleted. This scan did not establish which layers were still referenced and cannot quantify the space Docker GC would reclaim. The complete task API list contained Docker `assetBlob.cleanup` but no `repository.docker.gc`. Sonatype documents [Docker garbage collection and file blob compaction](https://help.sonatype.com/en/cleanup-policies.html#docker-cleanup-strategies) as separate steps and [digest-only image implications](https://help.sonatype.com/en/tasks.html). No task was created, changed or triggered by the agent. The November 5 decision about adding tasks remains historical context.

## Docker GC creation decision

The user declined the proposed creation of one manual `Docker - Delete unused manifests and images` task for `docker-hosted` with a 24-hour deployment offset. A read-only preflight confirmed that the hosted repository was online and the complete Nexus task list contained no Docker GC task. No task was created or launched. The storage observation remains recorded above.

## User-created Docker GC task

After declining agent-side creation, the user created the task independently and requested a read-only check. Nexus REST GET verified task `3ad9b584-58e5-48c2-b3e4-4bfdd281a55b`, type `repository.docker.gc`, enabled, repository `docker-hosted`, deployment offset 24 hours. It is scheduled daily at 00:45 MSK, with the existing compaction scheduled at 03:00 MSK and cleaner at 04:00 MSK. The first GC execution started at 18:11:26 MSK and was still RUNNING when checked at 18:12 MSK. The log corroborated the target repository. No exit result or reclaimed capacity was available; `/data` was at 98% used with about 4.2 GiB free. The agent did not run or change any Nexus task.

## First Docker GC and compaction result

Docker GC finished OK at 18:12:39 MSK and logged 18,352 unused layers removed. The user subsequently ran `Compact docker-hosted`. It finished OK at 18:13:35 MSK, and its log recorded 30 empty directories removed. At 18:15:38 MSK `/data` had 4,377,239,552 bytes available (4.08 GiB) and Nexus writable returned 200.

A local scan found 27,628 payloads without the deletion flag (177,541,214,208 allocated bytes, 165.35 GiB) and 12 flagged payloads (113,020,928 allocated bytes, about 108 MiB), all flagged in the 18:14 MSK minute after compaction. There is no large soft-deleted backlog to explain the space usage as a deletions-index issue. The 18,352 logged layer removals did not correspond to an observable drop in physical disk allocation. The Docker-specific `assetBlob.cleanup` last ran at 18:01:48 MSK, before Docker GC, and was next scheduled for 18:30 MSK. [Sonatype documents](https://help.sonatype.com/en/cleanup-policies.html#cleanup-tasks) that this task soft-deletes orphaned assets after component removal. Whether the next pass will flag the payloads from this GC is not verified. The agent did not trigger any tasks.

## Storage recovery verified

Nexus logs verify that the administrator manually ran `Cleanup unused docker blobs from nexus` from 18:16:19 to 18:16:32 MSK with result OK, after Docker GC and the ineffective first compaction. The following `Compact docker-hosted` ran from 18:16:44 to 18:16:54 and completed OK. Its log reports 3,500 empty directories removed. This observed sequence is Docker GC, Docker asset blob cleanup, then compaction.

At 18:22:05 MSK, `df -B1 /data` reported 62,802,120,704 used bytes, 136,986,107,904 available bytes (127.58 GiB) and 32% usage. Available space increased by 132,608,868,352 bytes (123.50 GiB) compared with the 18:15:38 check. Both Nexus status endpoints returned HTTP 200 and all three cleanup tasks were WAITING with last result OK. Recovery verified. The agent performed read-only checks. No historical ticket or backlog status changed.

## Cleaner errors after storage recovery

The 17:57 and 18:22 child jobs were stopped and dead at the 18:23 MSK verification, with 30 and 4 restarts respectively. Nexus logged 69 accepted cleaner manifest DELETEs and four HTTP 404 responses after storage recovery. Each 404 followed acceptance for the same image and digest. The 04:00 MSK periodic parent remained enabled. The current local cleaner logic uses search results grouped by image and evaluated per tag but deletes by digest. A proposed change is to evaluate all tag-retention rules first, protect any digest with a retained tag (including `latest`), and issue one DELETE for each remaining image and digest. Cover repeated digest, mixed retained/expired tags, and unexpected status handling before deployment. The proposal is recorded in the central TODO and does not authorize changes. No jobs or repositories were changed by the agent.

## First delivery of the cleaner diff

The user requested a diff. Repository `sysadmins/devops-tools/nexus-cleaner`, existing checkout `/home/slnnk/git/nexus-cleaner`, base `master` at `ba922e38f8905e5464ac22a38eafcdc84b6f917b` verified with `git ls-remote`. The proposal was prepared from a Git archive in a temporary directory. Its actual first-delivery artifact is `/home/slnnk/ai-data/nexus-cleaner/2026-11-25-preserve-shared-digests.patch`, 5,358 bytes, SHA-256 `11ee244a30bd6decf7d370de5c92a719699d7e066436884ba39e77a4d7c031dc`. Retain the patch for review or application.

The patch evaluates all tags for each image before deletion. It protects digests with `latest`, a branch tag within the age limit, or one of the retained master tags. It deduplicates the remaining candidates by digest for each image before issuing DELETE. Unexpected Nexus response handling and log message names remain unchanged. Regression cases cover duplicates across branch and release tags and retention shared with each tag class.

`git apply --check --whitespace=error-all`, `go test -count=1 -v ./...` and `go vet ./...` passed. The tests ran in the archive copy and did not call production Nexus. The repository status retained only the pre-existing untracked `t.go`. No branch, commit, publication, deployment or production cleaner run was requested or performed. The existing central implementation proposal stays open. First-delivery correction status is pending user review.

## DevOps-929 MR preparation

YouTrack GET confirmed [DevOps-929](https://youtrack.youdo.com/issue/DevOps-929) describes the prepared patch. GitLab project 518 is `sysadmins/devops-tools/nexus-cleaner` with default branch `master`. No matching MR or branch existed. The user explicitly approved the first stage for `DevOps-929-fix-cleaner-digest-deletion` from verified `master` at `ba922e38f8905e5464ac22a38eafcdc84b6f917b` and application of the reviewed patch. The resulting branch contains the two patch paths, with the pre-existing untracked `t.go` preserved and the index empty. Three regression subtests, Go vet, diff check and reverse patch check passed in the checkout.

Publication proposal communicated as commit `fix duplicate manifest deletions`, Ready MR `DevOps-929 Fix duplicate manifest deletions` from the approved branch to `master`, assigned to `a.solonenko` with squash off and source deletion on merge. The exact body and snapshot are in `/home/slnnk/ai-data/gitlab-workflow/DevOps-929/nexus-cleaner/`. The MR event triggers a build and push of the branch image to Nexus. Deployment is manual and only available for release tags. The user explicitly approved the presented publication with `Опубликуй`. The pre-stage snapshot matched, and the staged and committed contents matched the reviewed files byte-for-byte. Commit `c28ed15aa009f251f033778918cc92ca1ef96fcd` was pushed to the approved source branch, with only the two approved paths. The pre-existing untracked `t.go` was preserved. [MR !3](https://gitlab.youdo.sg/sysadmins/devops-tools/nexus-cleaner/-/merge_requests/3) was created and independently verified against the exact commit, source, target, title and body. Assignee, readiness, squash and source deletion match the proposal. [Pipeline 144179](https://gitlab.youdo.sg/sysadmins/devops-tools/nexus-cleaner/-/pipelines/144179) was observed running. The publication request is complete. Merge, release and production deployment remain outside this approval.

## DevOps-929 first MR build failed

[Job 3324368](https://gitlab.youdo.sg/sysadmins/devops-tools/nexus-cleaner/-/jobs/3324368) for commit `c28ed15` and pipeline 144179 failed at 18:39 MSK. Runner 105 pulled `golang:1.21.6-alpine` successfully. Docker build step 4 ran Go and failed downloading existing dependency `github.com/rs/zerolog@v1.31.0` from `proxy.golang.org:443` with `i/o timeout`. It did not reach compilation or the Nexus push. The reviewed patch does not change the module requirements or Dockerfile. Local tests and vet had passed earlier. The trace establishes a dependency download timeout inside Docker build, with the underlying network cause and recurrence unverified. No retry was requested or launched.

## Portable lesson

None.

## Task metrics: nexus-20261125-data-disk-capacity

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "nexus-20261125-data-disk-capacity",
  "created": "2026-11-25T17:45:17.745771+03:00",
  "first_result": "pass",
  "final_result": "pass",
  "state": "closed",
  "kind": "diagnostics",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Findings and Cleaner follow-up in the task note",
  "updated": "2026-11-25T17:47:37.749709+03:00"
}
```

## Task metrics: nexus-cleaner-20261125-shared-digest-diff

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "nexus-cleaner-20261125-shared-digest-diff",
  "created": "2026-11-25T18:27:11.059805+03:00",
  "first_result": "pass",
  "final_result": "pass",
  "state": "closed",
  "kind": "code",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "First diff matched DevOps-929 and passed regression tests. Both approvals and verified MR !3 recorded in DevOps-929 MR preparation.",
  "updated": "2026-11-25T18:38:46.382368+03:00"
}
```
