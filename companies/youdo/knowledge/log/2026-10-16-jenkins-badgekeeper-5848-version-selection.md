---
system: jenkins
status: verified
checked: 2026-10-16
tags: [jenkins, buildapi, badgekeeper]
---

# Badgekeeper release redeployment in Jenkins 5848

## Summary

Jenkins dynamic_deploy5848 on test retried release21.13.5/pipeline140954, not the MR36/pipeline141089 deployed by GitLab3232612. The console explicitly records the release in the BuildAPI response; fallback was skipped. Earlier Jenkins5847 had already redeployed the same release via3232811.

## Task and context

User requested read-only explanation of https://build.youdo.sg/job/dynamic_deploy/5848 versus https://gitlab.youdo.sg/youdo/microservices/badgekeeper/-/jobs/3232612. No repository edits or external writes authorized or performed. Superpowers skills excluded by user.

## Evidence and actions

Read Jenkins build JSON/consoleText and GitLab project359 job metadata/traces with authenticated GET requests. Credentials came from current/.env and were not copied into this note. Reviewed automation-test-yandex/playbooks/deploy/docker/recreate_microservices.yml and buildapi/mongo_utils.py.

All times Europe/Moscow on2026-10-16:

- GitLab3232612 succeeded15:51:00–15:52:16 on test, MR36 commit5341e250, pipeline141089, feature ref Site-25717-Back-Dobavit-beidzh-Partner-Yudu. Nomad rollout succeeded; publication to /ms_builds/test/359 returned HTTP200 with insert1/deleted1.
- Jenkins5847, started by rkhakimov with MICROSERVICES=true, read BuildAPI record21.13.5/pipeline140954/job3232360. It retried that release as GitLab3232811 at17:15:03; job succeeded17:16:25.
- Jenkins5848 started17:32:30 by rkhakimov with MICROSERVICES=true. BuildAPI still selected21.13.5/pipeline140954, now pointing to3232811. Jenkins retried it as3232826 at17:39:42; success17:40:55. All badgekeeper fallback tasks were skipped.

## Cause

BuildAPI mongo_utils.delete_stale_ms_build sorts deployment records by timestamp, classifies default-branch and ordinary semver tags as master_builds, and, whenever that list is nonempty, deletes all other_builds (including feature branches). Thus publishing a new MR deployment while a release record exists removes the MR deployment metadata rather than replacing the effective selection. The3232612 insert1/deleted1 response and subsequent5847 selection of the preexisting release are consistent with this deterministic code path. No historical Mongo snapshot was read to identify the deleted document independently.

Jenkins recreate_microservices uses /ms_builds/test as its version source and retries the saved pipeline deploy job even when its status is already success. Therefore it reapplies the release retained by BuildAPI. The deployed ref was the tag21.13.5 at2aa95861, not a newly selected master HEAD. This is not fallback after an MR job failure.

## Changed files and limits

Only this knowledge log, the existing Jenkins system map, TODO.md and .sync-notes were updated. No runtime or repository task changes. Proposed correction: retain the most recent successful deployment as effective /ms_builds selection, keeping fallback-release metadata separate. Implementation requires a separate request and supervised branch approval.
