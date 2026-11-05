---
system: nexus
status: verified
checked: 2026-11-05
tags: [nexus, gradle, cache, android, verified]
---
# DevOps-908: autotest cache cuts warm Nexus requests from 316 to 8

## Task
User reports MR merged and several pipelines started; inspect actual cache reuse and Nexus request counts. Read-only verification; no new pipeline/merge/retry or configuration change.

## Source and execution identity
MR1163 independently confirmed merged at20:02:27 Moscow, merge commitf126825b2f64098a57e37e6f9ec201764523a55a. Both inspected post-merge jobs run that exact SHA on master. Exact-revision YAML/build.gradle confirm --refresh-dependencies removed and cacheChangingModulesFor0seconds present.
Generated evidence/scripts: `/home/slnnk/ai-data/nexus-usage/android-autotests/post-merge/`, including gitlab-runs.json, nexus.json, merge.json and verified-summary.json. Raw traces were processed in memory and not stored. Collected Nexus request.log read-only over SSH, zero parse failures; compared complete Gradle method/path multisets against trace per job. All three comparisons match exactly.

## Measured result
| Job | SHA | Moscow interval Nov5 | Outcome | Nexus Gradle requests | HEAD | GET |
| --- | --- | --- | --- | --- | --- | --- |
| 3278749 | cdea3477, before cache patch | 19:46:24–19:50:46 | success | 316 | 314 | 2 |
| 3278752 | f126825b, merged policy | 20:13:01–20:18:41 | success | 8 | 6 | 2 |
| 3278763 | f126825b, merged policy | 20:19:25–20:28:20 | success | 8 | 6 | 2 |
All counted Gradle requests are maven-public/HTTP200. Proxy source IP is shared but exact trace/server method/path matching establishes attribution. Unrelated repository requests in those job windows (3/258/10) are excluded.
Warm-before vs warm-after reduction:308 requests/job,97.468%;39.5times fewer. Relative to original [job3278160 baseline](2026-11-05-nexus-android-autotest-job3278160-request-count.md)637requests, reduction98.744%; the immediate warm316baseline is the fairer comparison.

## Cache and SNAPSHOT evidence
All3jobs on runner108 successfully download/extract and upload cache key failed-suite-cache-1 via S3. Each later job restores the preceding saved cache (ETags change as expected). No cache miss/extraction failure observed.
Each post-merge run makes exactly4requests per internal SNAPSHOT: HEAD+GET maven-metadata.xml, HEAD timestamped POM and HEAD timestamped JAR. Coordinates autotest-core1.2.0-SNAPSHOT and youdo-api-testing1.2.2-SNAPSHOT.
Metadata GETs occurred20:14:55 and20:21:14 Moscow. Trace reports cached POM/JAR up-to-date; no JAR body GETs or ordinary release-dependency Nexus requests were required in the two post-merge jobs.
Thus checks for fresh internal library publications remain active on every inspected run, while unchanged release dependencies reuse cache. No new SNAPSHOT publication occurred between these observed runs, so fetching an actually changed publication has not been directly tested.

## Limits and status
Two warm runs on the same runner/JOB_ID1 are verified. Cold-cache initialization, runner changes, JOB_ID2/protected-cache partition differences, concurrency and arbitrary future SNAPSHOT republication are not established by this sample. No blanket full-cache-performance or global Nexus-load reduction claim.
Total job/Gradle duration is affected by test/device execution and differs across runs; request savings do not prove faster test completion. No broad CI-speed claim made.
The requested publication/merge/runtime-cache validation scope is complete; corresponding DevOps-908 TODO closed. Cache-key splitting was not included. Device UnicodeIME issue remains separately deferred by user and was not investigated again.
All commands finished, no background operations remain. Existing repo source is not mutated by this verification.

## Portable lesson
none

## DevOps-904 Markdown result comment published (2026-11-05)
User requested a comment for DevOps-904, then specified repository/changes/effect structure and numeric-only effect, and explicitly authorized publication with Markdown formatting.
Read-only inspection confirmed issue71-138586 (`[Nexus] Превышение лимитов`),4existing comments and no matching Gradle-autotest result. Created one comment74-125202; GET read-back verified exact Markdown text with bold labels and inline-code identifiers. Effect contains only316→8requests/run,308fewer,−97.5%.
Local approved text and receipt are under `/home/slnnk/ai-data/nexus-usage/android-autotests/devops-904-comment/`. No issue state or other fields changed. This records the autotest repository result only; it does not complete the distinct product Android feature/browserstack cache proposal in the DevOps-904 backlog. No background operations remain.
