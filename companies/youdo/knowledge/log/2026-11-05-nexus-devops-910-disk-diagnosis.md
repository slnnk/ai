---
system: nexus
status: verified
checked: 2026-11-05
tags: [nexus, storage, incident, compaction]
decision_state: cancelled
decision_scope: Additional maintenance jobs proposed after the twelve daily compaction tasks
decision_summary: The user declined adding further jobs; the existing daily compaction setup remains in place.
decision_date: 2026-11-05
decision_source: #decision-record
---
# DevOps-910 Nexus data disk exhaustion and compaction assessment

## Task
Diagnose [DevOps-910](https://youtrack.youdo.com/issue/DevOps-910) and assess whether compact blob stores should be configured. Read-only remote investigation; no repair authorized. Issue GET confirms title `[Nexus] Закончилось место в /data`, no description/comments.

## Context and actions
Nexus3.96.4 on10.18.24.233; root SSH, GET REST, filesystem statistics and blob metadata inspection. Existing [system map](../systems/nexus.md), [initial outage](2026-11-05-nexus-android-publish-job3273026-disk-full.md), [cleaner evidence](2026-10-20-nexus-cleaner-recovery-assessment.md). Generated helper/evidence: `/home/slnnk/ai-data/nexus-disk-910/`.

## Findings
At19:09 Moscow `/data` on/dev/vdb ext4: total210241744896bytes, used200164515840bytes, available0; inode usage3%. Raw device214748364800bytes (200GiB), no existing unallocated device capacity verified. Root filesystem29%used,7242452992bytes available.
Physical allocated directory usage: `/data`200171663360bytes; Nexus198503845888bytes; blobs196142428160bytes. Docker/containerd are about1.7GB combined. Main blob stores:

| Store | Allocated bytes |
| --- | ---: |
| docker-hosted | 180653731840 |
| npm-cache | 9989959680 |
| nuget-cache | 3361067008 |
| maven-cache | 1236475904 |
| pypi-cache | 513495040 |
| raw-hosted | 193482752 |

Nexus container remains up3weeks. Localhost8081 status GET returns200. Workstation and SSH-localhost authenticated requests to tasks/blobstores/repositories REST returned503; this does not establish a total application outage. H2 database file about895MiB. App/container logs continue showing failures under disk exhaustion. Request file logging stopped18:52:58 and later totals are incomplete.

## Compaction assessment
Sonatype documents that cleanup soft-deletes blobs; `Admin - Compact blob store` (`blobstore.compact`) physically removes already soft-deleted data. Compaction does not compress active artifacts. Separate per-store tasks and retention policies are needed for ongoing space management. Docker orphan/unused manifest and image cleanup is distinct from hard deletion; review actual task states before configuring.
Sources: [Out of disk space](https://support.sonatype.com/hc/en-us/articles/360000096228-What-to-Do-When-the-Blobstore-is-Out-of-Disk-Space), [Cleanup policies](https://help.sonatype.com/en/cleanup-policies.html), [Tasks](https://help.sonatype.com/en/tasks.html).

## Deleted payload measurement
A complete read-only scan of blob `.properties` files matched exact `deleted=true` markers and summed adjacent `.bytes` logical lengths. SSH exit0, no read errors reported. Total99074534176bytes (92.27GiB) of already soft-deleted payload:

| Store | Deleted count | Deleted payload bytes | GiB |
| --- | ---: | ---: | ---: |
| docker-hosted | 47748 | 92698003249 | 86.33 |
| npm-cache | 9577 | 6096386659 | 5.68 |
| pypi-cache | 176 | 244708092 | 0.23 |
| nuget-cache | 646 | 28230807 | 0.03 |

Other stores add small amounts. The scan was live and is not a transactional snapshot. No deleted-file removal was performed. There are no `blobstore.compact` logs among retained task logs;26 `repository.cleanup` logs exist. This supports missing/not-running compaction as a likely accumulation mechanism, but API503 prevents proof of current task configuration/schedule. Root-only deletion-index glob returned nothing; it is not evidence that nested index structures are absent and no rebuild is proposed.

## Proposed recovery
Recover a working free-space margin first, preferably a reviewed disk expansion if administration is blocked; alternatively review a specific expendable file action separately. Then inspect existing task definitions and create/enable/run `Admin - Compact blob store` for docker-hosted first and npm-cache next, respecting deleted-blob retention. Verify actual df reduction, task result and blob-store write health. Schedule per-store compaction after cleanup and review retention/space alerting. Each remote mutation requires explicit approval. No arbitrary blob deletion, reserved-block tuning, repair task or direct H2 edit is authorized or proposed as the first action.

## Changes
Local diagnostic helper and KB bookkeeping only. No remote cleanup, task changes, API mutations, restart, resize or publication.

## Status and risks
Read-only diagnosis complete; storage outage remains unresolved and repair requires explicit action approval. All task SSH commands exited; no background operations remain. Central backlog: [TODO](../../../../TODO.md). A filesystem metadata scan measures logical payload sizes, which differ from allocated disk space; it cannot promise exact compaction recovery or prove every deleted blob is present in the deletion index.

## Portable lesson
none

## Working-space candidate follow-up
User asked whether files can be removed to restore API. Read-only SSH found seven H2 ZIP backup archives under `/data/nexus/nexus-data/backup/airflow-files`, dated2026-10-29 through2026-11-04, allocated1154076672bytes combined. Root filesystem has7242420224bytes available, enough to preserve all seven under proposed `/root/nexus-backup-DevOps-910/` while removing their source copies only after hash verification. This is a proposal, not performed. At the later check `/data` used200321925120bytes, available0; reserved blocks2548032×4096bytes explain why freeing1.07GiB produces a smaller available margin, estimated roughly0.5GiB subject to concurrent writes. Docker JSON log is about659MB and growing but direct deletion/truncation is not the preferred first action. API recovery after obtaining space remains to verify; no restart is approved or assumed necessary. All diagnostic commands finished.

## Approved backup move and API result
User explicitly approved the seven-archive copy/verify/remove-source operation. Executed one SSH mutation via `/home/slnnk/ai-data/nexus-disk-910/move_approved_backups.py`: all seven approved ZIPs copied into `/root/nexus-backup-DevOps-910/`, SHA-256 verified before any source removal and again before removal; all source files removed only after validation. Total payload1154053153bytes, allocated source size1154076672bytes. SSH exit0; evidence `backup-move-result.txt` contains checksums. Root now6088339456bytes available; `/data`613867520bytes available immediately after move (585MiB),613134336bytes at19:16:55 Moscow. Backups remain preserved outside the normal backup directory; normal backup creation/retention was not changed.

Read-only post-check: writable endpoint200, authenticated status/tasks/blobstores503. Unauthenticated tasks403 is an authorization response, not admin API recovery. Latest application errors explicitly show H2 `The database has been closed [90098-240]`, with retained cause MVStore write failure/`No space left on device`. Database remains closed after space recovery; this is not evidence of a new failure to write with585MiB available. Propose controlled `docker restart --timeout 120 nexus-nexus-1` and read-only startup/API checks; restart is not yet authorized. The restart interrupts Nexus reads/writes and database startup health remains to verify. No compaction or other mutation performed. All started commands have finished; no background operations remain.

## Approved restart and restored API
User explicitly approved `docker restart --timeout 120 nexus-nexus-1`; one SSH mutation completed exit0. Startup initially reset connections, then authenticated status/writable/tasks/blobstores all returned200. All12blob stores report unavailable=false. Free space610942976bytes (~582.6MiB), root6088314880bytes. Evidence `/home/slnnk/ai-data/nexus-disk-910/post-move-api.jsonl` now contains post-restart checks. No persistent database recovery error established after startup; earlier ENOSPC stack traces in shutdown output are historical, not fresh startup failures.

Fresh task GET confirms14tasks and no `blobstore.compact`. Existing `assetBlob.cleanup` tasks for six formats and repository cleanup have recent OK results. H2 backup next run2026-11-05T19:30UTC/22:30Moscow could consume part of the small remaining margin. GET template confirms supported REST task creation: type `blobstore.compact`, properties `blobstoreName` and `blobsOlderThan` (default0days), manual frequency available. Next proposed action is create/configure compaction, starting docker-hosted then npm-cache; permanent removal of already soft-deleted blobs must be explicitly approved before mutation. No task creation, task launch, compaction or additional runtime change performed. All SSH/background commands finished.

## Approved Docker compaction completed
User requested `Сделай для docker` after the recommendation to configure and run compaction. Executed task creation and launch for docker-hosted only; no npm or other-store compaction. Payload: type `blobstore.compact`, name `Compact docker-hosted`, enabled=true, manual schedule, properties `blobstoreName=docker-hosted`, `blobsOlderThan=0`, no notification address. Creation HTTP201; exact GET verified store/retention/manual schedule before run HTTP204. Task ID33b3f5b4-ecf6-4f21-9e4f-e2c7d44c8aad, run started2026-11-05T16:21:01.231UTC/19:21Moscow. Polling observed RUNNING then WAITING/lastRunResult=OK; no scheduled next run.

Post-run `/data` used106365759488bytes, available93422469120bytes (87.01GiB), about50.6% of df total used. Relative to pre-compaction post-restart sample used199177285632bytes, net allocated usage dropped92811526144bytes (86.44GiB), subject to simultaneous ordinary writes. Docker blob REST metrics now17532blobs/87704061926payload bytes (before65223blobs/180177428759bytes); REST metrics/counts differ from raw metadata scan and should not be conflated. Authenticated status/writable/tasks/blobstores allHTTP200; docker-hosted unavailable=false. Task creation/start evidence `docker-compaction-start.jsonl`; timestamped API snapshots under `/home/slnnk/ai-data/nexus-disk-910/`. No package upload/download retry was performed.

Storage emergency is resolved by observed free-space recovery and healthy API; ongoing retention prevention remains proposed. The created task uses manual scheduling; adding regular Docker compaction or compacting npm/other stores requires a separate requested action. Previously moved seven H2 backups remain preserved in/root/nexus-backup-DevOps-910. All started local/SSH commands finished, compaction finishedOK, no task background operations remain. Relevant backlog is reconciled with central TODO.

## Approved daily compaction schedules for all stores
User explicitly requested one compaction task per blob store starting daily03:00 with15minute spacing. Interpreted local time as Moscow UTC+03:00 and announced it before execution. Current inventory12stores; reused existing Docker task and created11tasks. All enabled, property blobsOlderThan0, Quartz cron with `timeZoneOffset=+03:00`. Input frequency is `cron`; Nexus GET normalizes schedule to `advanced`. Existing Docker PUT actually returned204 despite cached OpenAPI documenting200. Initial helper stopped on these response-format mismatches; GET confirmed the schedule persisted, then helper validation was corrected and existing matching configuration reused. No task duplicates or unintended immediate runs.

| Moscow daily start | Store | Task ID |
| --- | --- | --- |
| 03:00 | `docker-hosted` | `33b3f5b4-ecf6-4f21-9e4f-e2c7d44c8aad` |
| 03:15 | `npm-cache` | `f3e6f89f-8b0f-4e03-b40e-01ecffb5461b` |
| 03:30 | `nuget-cache` | `a3e4bbdd-5be3-4148-a092-4d83fe5718bc` |
| 03:45 | `maven-cache` | `2745d333-130a-4403-971c-3368d5c654ff` |
| 04:00 | `pypi-cache` | `99defb45-c0f8-4ff3-b947-d7802a4381ec` |
| 04:15 | `raw-hosted` | `afa13c0d-2eaf-4290-81ce-ea30d4200791` |
| 04:30 | `maven-hosted` | `e57421a5-3ef7-4388-98d7-fc3d75c89185` |
| 04:45 | `npm-hosted` | `14203555-b310-4dc4-b79a-ad08280c5408` |
| 05:00 | `nuget-hosted` | `5df93c62-9360-4f3e-a98d-49723e6a593a` |
| 05:15 | `default` | `eb76ee7c-dbc3-4564-a2af-90dc8b37ad95` |
| 05:30 | `pypi-hosted` | `13b1c6de-37f0-4481-b0a8-8f5180912785` |
| 05:45 | `docker-cache` | `048b8f71-3dcd-4eea-a662-1ccd0b00af74` |

All12task definitions reread after writes: expected store, retention, cron expression, timezone, enabled state, exact count and nextRun validated; no task RUNNING. Next first cycle2026-11-06 03:00–05:45Moscow /00:00–02:45UTC. This configures start-time spacing, not a completion dependency; a run lasting more than15minutes may overlap a later task. No immediate npm/other-store compaction was requested or performed; first scheduled outcomes remain unobserved. No change to repository cleanup or backup schedules. Evidence `/home/slnnk/ai-data/nexus-disk-910/compaction-schedules.jsonl`, helper `schedule_compaction.py`; SSH exit0. All task commands finished; no active task background operations remain. Supersedes prior statements that regular scheduling remains unconfigured/proposed; optional alerting review and first-cycle observation remain central-backlog proposals only.

## Decision record
User explicitly declined adding further jobs (`Ничего не будем добавлять`) and requested returning the seven moved backup archives. Cancellation applies only to the extra proposed incomplete Docker upload cleanup, Docker unused manifests/images GC, and blob temporary-file jobs; it does not cancel or remove the12already configured daily compaction tasks. No extra jobs were created and none should be added under the prior recommendation.

## Approved archive return
Executed `/home/slnnk/ai-data/nexus-disk-910/restore_backups.py` over SSH, exit0: seven specified ZIPs dated2026-10-29 through2026-11-04 restored from `/root/nexus-backup-DevOps-910/` to original `/data/nexus/nexus-data/backup/airflow-files/`. Checked all sources against original SHA-256 values from the first move, refused destination collisions, copied all, restored UID/GID200:200, fsynced and verified all destination hashes before removing any root source. All seven root copies removed after verification; empty temporary root directory removed. Original file modes and timestamps preserved by copy2. Final data available91810373632bytes (~85.50GiB), root available7242313728bytes (~6.75GiB). Evidence `backup-restore-result.jsonl`. This supersedes all historical statements that these seven backups remain under/root; archive restore here is file relocation only, not database restore. Existing compaction schedules unchanged. All task commands finished; no background operations remain.

## Cleaner attribution correction
User clarified that old Docker content is cleaned by the separate `nexus-cleaner` service. Incident summaries must distinguish external retention/deletion from Nexus hard deletion: nexus-cleaner deletes old Docker image manifests using Nexus APIs; `Admin - Compact blob store` reclaims physically stored soft-deleted blobs. Do not attribute the incident's accumulated Docker deletions exclusively to built-in `Cleanup service`. Evidence already exists in [cleaner recovery](2026-10-20-nexus-cleaner-recovery-assessment.md): accepted108DELETE responses202 and successful external cleaner run; attribution of every deleted blob to that service was not measured. Existing built-in asset cleanup/repository cleanup tasks also exist, but are separate mechanisms. This factual clarification changes documentation/comment wording only, not external permissions or runtime configuration. No background operations.

## Requested YouTrack summary published
User explicitly requested adding the corrected summary to DevOps-910. GET inspection found no duplicate or related existing summary; POST created comment74-125200. Independent exact-text GET verification passed. Comment names external nexus-cleaner separately from compaction, records H2/API recovery,86.4GiB reclaimed,12daily schedules03:00–05:45Moscow, verified backup return and85.5GiB free at completion. Only comment content changed; issue state not changed. Evidence under `/home/slnnk/ai-data/nexus-disk-910/youtrack/`. Command exit0, no background operations. Existing central TODO follow-up for scheduled-cycle observation/alerting review remains a proposal; publication completes requested reporting.

## User-reported task closure
On2026-11-05 the user reported DevOps-910 closed. Accepted task as complete and closed the remaining optional scheduled-cycle/alerting follow-up in central TODO without executing it. First scheduled-cycle outcomes remain unobserved; alerting was not changed. These documented limits are not open incident blockers and do not reopen the accepted task. Future investigation requires a new request. No YouTrack state mutation or additional infrastructure check performed; existing12daily compaction tasks retained. All task operations finished, no background operations.
