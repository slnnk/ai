---
system: nexus
status: verified
checked: 2026-11-05
tags: [nexus, android, storage, incident]
---
# Android publication job3273026: Nexus data disk full and hidden HTTP500

## Task
Explain [job3273026](https://gitlab.youdo.sg/team-youdo-android/android-youdo4/-/jobs/3273026), read-only. The earlier autotest Gradle-cache patch remains local and awaiting publication approval; this diagnosis did not replace or publish it.

## Job evidence
Project79/team-youdo-android/android-youdo4, `regress_publish_for_tests_job_1`, stage publish_for_tests, ref staging, commit43e1eaaefa3f26578715be7ad5d8607f2e3682ce, pipeline142214, runner116. Executed Nov5 18:54:40–18:55:08 Moscow /15:54:40–15:55:08 UTC. GitLab status success, allow_failure=true.
This job publishes an already-built APK, not a Gradle build. APK upload size65,673,106bytes (~62.6MiB), version text25bytes.
At18:55:07 Moscow both PUTs to `/repository/raw-private/android/gitlab_youdo_1.apk` and `/repository/raw-private/android/gitlab_youdo_version_1.txt` returned HTTP500. Trace says full request bodies were sent; successful storage is not established.
Exact-revision CI YAML read through GitLab confirms `.publish_for_tests` uses curl -v --upload-file without --fail/--fail-with-body or explicit HTTP-status validation. Thus HTTP500 did not produce a failing curl exit and job ended `Job succeeded`. allow_failure is separate and did not cause this successful process exit.

## Proxy and server corroboration
Public LB172.28.0.141 `/var/log/nginx/nexus.youdo.com-access.log` records both PUT500s at15:55:07 UTC with upstream10.18.24.233:80. The live raw-private location proxies to msk3-nexus.youdo.corp. This verifies backend route, not a DNS/TLS/runner failure.
Nexus request.log stopped at18:52:58 Moscow, before those requests; nexus.log had no new matching entries. Absence of entries must not be interpreted as lack of upstream traffic.
Read-only SSH to Nexus10.18.24.233 around19:05 Moscow: container nexus-nexus-1 running for3weeks, image sonatype/nexus3:3.96.4,8081 listening. Root filesystem29%used/6.8Gfree. `/data` on `/dev/vdb` is100%used:210241744896bytes total,199819030528used,0available. Inode use3%.
Docker output at19:05:55 Moscow explicitly reports `java.io.IOException: No space left on device` when writing nexus.log, and FileBlobStore warnings: stores maven-cache/default/docker-hosted/nuget-cache not writable, usable space0. Thus storage exhaustion is confirmed and explains silent file logging and write failures. No contemporaneous on-disk application stack for18:55 can be recovered from the stopped logs.
Blast radius extends beyond Android publication to writes on the shared Nexus data filesystem; complete repository/read availability was not tested.

## Actions and status
Read-only GitLab/SSH analysis only. No build/Gradle invocation (prohibited by android-youdo4 AGENTS.md), source edit, upload retry, cleanup, deletion, expansion or service restart.
Exact CI/evidence helpers are under `/home/slnnk/ai-data/android-dig/3273026/`. Temporary sanitized trace was deleted after analysis.
Current issue is Nexus storage exhaustion, not Gradle cache behavior. Recommend first measuring data usage and selecting reviewed expansion/cleanup; arbitrary blob-file deletion is not a proposed repair. Publication scripts should separately fail on HTTP errors, then artifact delivery should be retried only after storage repair and explicit authorization.
Remaining storage restoration and publication-error detection are proposals in [central TODO](../../../../TODO.md). All SSH commands finished; no background operations remain. The stopped file logs may omit requests after18:52:58, so Nexus request-count measurements for later intervals would be incomplete.

## Portable lesson
none

## Later remediation and Android run (2026-11-05)
User reports Nexus cleaned and Android uploaded. Separate [DevOps-910 recovery evidence](2026-11-05-nexus-devops-910-disk-diagnosis.md) records approved storage/API restoration and task closure; no new Nexus remediation is required or authorized by this Android diagnosis.
[Job3278748](2026-11-05-android-farm-dig-job-3278748.md) reads version4.0.274.staging(142214) and reaches device session creation, failing instead on UnicodeIME. The original active-storage status is superseded by DevOps-910; CI publication HTTP-error handling remains a distinct open proposal.
