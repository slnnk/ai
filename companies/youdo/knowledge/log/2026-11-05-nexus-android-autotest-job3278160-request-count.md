---
system: nexus
status: verified
checked: 2026-11-05
tags: [nexus, gradle, cache, android]
---
# Android autotest job3278160: 637 Nexus Gradle requests with cache

## Task and scope
User requested counting Nexus requests before deciding on Android autotest Gradle cache changes. Read-only investigation, no implementation or CI execution authorized.
Latest12 project69 jobs confirm job3278160 remains the latest run; branch DevOps-908-gradle-image-18, commit7ac49405 (image18, before endpoint correction cdea3477), runner108.
[Job](https://gitlab.youdo.sg/youdo/Test/youdo-android-testing/-/jobs/3278160) interval Nov5 18:04:08–18:10:56 Moscow /15:04:08–15:10:56 UTC.

## Method and evidence
Read-only SSH to Nexus10.18.24.233 analyzed `/data/nexus/nexus-data/log/request.log` for18:04:08 inclusive to18:10:57 exclusive Moscow. All `/repository/` methods/statuses counted; zero parse failures.
Fetched a temporary sanitized GitLab trace; extracted `Performing HTTP GET/HEAD` entries targeting nexus.youdo.com. Compared the complete method/path multiset to server Gradle8.13 requests: exact637/637 match, no unmatched request on either side. This directly attributes requests to the job despite the shared reverse-proxy source IP172.18.0.1.
Evidence/scripts: `/home/slnnk/ai-data/nexus-usage/android-autotests/`; verified-summary.json and job3278160-nexus.json preserve aggregate and sanitized request evidence. Temporary trace removed after analysis.

## Counts
637 requests to maven-public by Gradle8.13/JDK21, all HTTP200, between18:08:58 and18:09:27 Moscow.
- HEAD312:183 POM,112 JAR,17 module.
- GET312 SHA1 checksums.
- GET2 SNAPSHOT maven-metadata.xml.
- GET6 JAR artifacts.
- GET5 POM documents.
624/637 (97.96%) requests are HEAD/checksum revalidation; they are not624 artifact downloads.
An additional job curl GET to raw-private/android/gitlab_youdo_version_1.txt returned404. Hence638 identified job repository requests in total. No APK retrieval was observed; the suite failed setup before UI execution.
Nexus received696 repository requests in the job window overall:637 Maven,57 NuGet,1 npm,1 raw-private. The58 concurrent NuGet/npm requests are excluded from this job's attribution.

## Cache assessment and limits
At the job revision cache restoration/saving is enabled for .gradle-cache/caches and GRADLE_USER_HOME points at .gradle-cache. Trace confirms restoration. The command always supplies --refresh-dependencies.
The measurements establish substantial dependency reuse with extensive remote revalidation, not absence of a Gradle cache. Removing unconditional refresh is a targeted candidate; exact savings require a later separately authorized comparable warm run.
Dependencies include autotest-core1.2.0-SNAPSHOT and youdo-api-testing1.2.2-SNAPSHOT, so any optimization must define snapshot freshness. A short TTL and an explicit force-refresh option are proposals, not applied changes.
The raw marker404 is a separate artifact/version-discovery issue, not a Maven cache failure; the terminal suite failure remains the previously documented Houston404.
No arbitrary Nexus endpoints were queried or packages downloaded; only logs and GitLab metadata/trace read. All task commands completed, no background operations remain.
Optimization remains a proposal in [central TODO](../../../../TODO.md), under Android farm; it is separate from the product Android feature/browserstack caching work in DevOps-904.

## Portable lesson
none

## SNAPSHOT freshness clarification (2026-11-05)
User clarified that autotest-core and youdo-api-testing are republished under the same versions in Nexus. Both declarations in the inspected build.gradle are SNAPSHOT coordinates, automatically treated as changing by Gradle.
Refined proposal: remove unconditional --refresh-dependencies and set `configurations.configureEach { resolutionStrategy.cacheChangingModulesFor 0, 'seconds' }` so changing modules are revalidated for each build while immutable dependencies retain normal cache behavior. The earlier15-minute TTL option is not the recommendation when each run must observe newly published snapshots.
Gradle default changing-module TTL is24hours; removing refresh alone would therefore change freshness. Mutable fixed release versions would additionally require explicit changing marking for those modules, but no such release coordinates were observed for these two libraries. Publication metadata/checksums must reflect the update. Exact Nexus savings remain unmeasured, and no edits or runs were performed.

## Approved local implementation follow-up (2026-11-05)
The user subsequently requested and approved local implementation in DevOps-908. [The publication log](2026-11-05-gitlab-ci-devops-908-gradle-image-18.md) records the prepared removal of unconditional refresh and changing-module TTL0. Static checks passed; expanded MR publication approval is pending. This supersedes the earlier no-implementation-approval status. No cache separation was implemented and no request-reduction measurement exists yet.

## Cache policy source publication (2026-11-05)
Approved follow-up commit91ce02f2 is now published and verified in MR1163. Unconditional refresh was removed and changing-module TTL0 added; no dependency-cache key/path splitting included. Earlier unpublished/pending-approval status is superseded. No new run or measured Nexus savings;637requests remains the unchanged pre-optimization baseline.

## Post-merge result measured (2026-11-05)
[Verification](2026-11-05-nexus-devops-908-autotest-cache-verified.md) after MR1163 merge confirms8Nexus requests/job on two successful master runs, versus316in a later successful warm pre-patch run and637in the original baseline. Both internal SNAPSHOT metadata and artifacts are checked each run. Earlier unmeasured status is superseded for these warm same-runner samples only; no new SNAPSHOT publication or cross-runner/cold test was performed.
