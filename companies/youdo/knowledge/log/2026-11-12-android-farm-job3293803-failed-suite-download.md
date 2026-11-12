---
system: android-farm
status: verified
checked: 2026-11-12
tags: [gitlab-ci, failed-suite, artifacts, xml]
---
# Job3293803: invalid retry suite during source artifact publication

## Task and scope

The user asked whether [job3293803](https://gitlab.youdo.sg/youdo/Test/youdo-android-testing/-/jobs/3293803) matches the previously discussed failed-suite download/XML issue. Read-only comparison of job trace, source job metadata, source trace artifact-publication timeline and current source artifact. No retry, service action, code change or broad host diagnosis requested/performed. Fresh Enabled Selenium inventory collected before trace inspection; GitLab trace fetch itself had already completed before inventory fetch. No full android-dig machine-health verdict is claimed from this narrow check.

## Verified evidence

- Target job master/f126825b, pipeline142797, runner108, test1, suite `[Упавшие тесты]`, source FAILED_JOB_ID3293664/sourcepipeline142792. November11start15:54:11.532UTC/18:54:11.532MSK, finish15:57:09.183UTC/18:57:09.183MSK, failed/script_failure, duration177.65s.
- Download block follows the notification HTTPresponse dated15:54:19UTC and precedes preparation-section start15:54:20UTC. Failed-suite download progress shows exactly27bytes. The job then prepares devices and launches Gradle. These are bounded trace times, not an exact download timestamp.
- At18:56:50.797MSK TestNG fails with `org.xml.sax.SAXParseException; lineNumber: 1; columnNumber: 1; Content is not allowed in prolog.` No actual test execution/session creation is evidenced; the failure occurs loading the suite. Full trace1128262bytes/4774lines has0collector infrastructure-signature matches. Known nonfatal emulator_2missing-service output is present; the emulator-preparation proposal remains user-cancelled and is not reopened.
- Source job3293664started18:32:31.196MSK, finished18:54:22MSK. Its trace confirms FailedTestSuite_3293664.xml found for upload. Artifact upload section starts15:54:19UTC/18:54:19MSK and ends15:54:21UTC/18:54:21MSK. The target therefore requested the source artifact during its publication, before source completion.
- Current read of exact source artifact API returns HTTP200, text/xml,2743bytes; XML parses successfully with root `suite`. Source artifacts not erased/expired at check (expirationNovember25). Current validity is not proof of its availability during the earlier target download.

## Interpretation

Confirmed same immediate failure class as historical job3120554: invalid retry-suite input causes TestNG parsing failure before tests. Strongly supported explanation is early retry/source-artifact publication race: target gets27bytes while source artifacts are still uploading, whereas later valid XML is2743bytes. HTTPstatus/body of the historical27bytes were not printed/preserved, so HTTP404/JSONerror is probable, not directly proven. Do not claim an identified exact payload or permanent artifact loss.

HTTP-error and XML checks would detect invalid input before device preparation. They would improve diagnosis but not by themselves remove the early-retry race; artifact-readiness/wait ordering needs consideration within the existing proposal, not an unapproved retry or new task. No implementation authorized by this question.

## Changes and status

Sanitized collector evidence: ~/ai-data/android-dig/job3293803.json, job3293803-source.json and job3293803-inventory.json. Temporary full trace removed after inspection. Updated existing failed-suite TODO and CI map with this recurrence; cancelled emulator/resource proposals remain cancelled. All commands finished, no background operations.

## Portable lesson

None.

## Source-job completion check requested — 2026-11-12

The user proposed checking that the source job has finished regardless of success/failure before downloading its artifact. Treat result acceptance as independent of job completion. Available job API exposes finished_at and pipeline.id; current CI already requests the source job after downloading XML, so that metadata request can move before download and serve the readiness check/pipelineid together. Proposed behavior: bounded polling while finished_at is null, then download once completed whether success or failed. Poll interval/timeout are implementation proposals, not yet agreed. Existing download HTTP/XML checks remain separately recorded; do not silently expand scope. No repository edits, waiting loop, retry or external change performed. Asked for task ID (DevOps-921is already closed and covers APK publication); concrete branch/base proposal and first approval remain pending. Existing checkout clean on DevOps-908-gradle-image-18, cached origin/master f126825b.
