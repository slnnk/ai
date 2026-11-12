---
system: android-farm
status: verified
checked: 2026-11-12
tags: [android-dig, appium, grid, loki, zabbix]
---
# Android job3285160: final outcome after farm recovery

## Task

The user requested the final outcome of [job3285160](https://gitlab.youdo.sg/youdo/Test/youdo-android-testing/-/jobs/3285160), completing the pending final review after the [November 9 running-job snapshots](2026-11-09-android-farm-dig-job-3285160.md). Read-only diagnosis; no retries, service changes, device commands or external writes.

## Context and final result

- Project `youdo/Test/youdo-android-testing`, pipeline142559, ref `Test-7062`, SHA `5cbe63fe265c09b65ecb5e46e9e48e3e8053615f`, runner108.
- Execution November9 16:22:15–19:21:25UTC /19:22:15–22:21:25MSK, duration10749seconds. Final status `failed`, GitLab reason `script_failure`.
- Full trace104074014bytes/929846normalizedlines fetched November12. Gradle final summary: `469 tests completed, 76 failed, 9 skipped`; HTML artifact independently confirms469total/384successful/76failed/9skipped.
- At22:20:24MSK Gradle reports `Execution failed for task ':test'`, `There were failing tests`, `BUILD FAILED in 2h 54m 50s`. Job ends `exit code 1`.
- HTML report uploaded to object storage; GitLab archive and JUnit uploads each returned `201 Created`. Artifact metadata confirms archive38690613bytes and JUnit3897148bytes, expiration November23. HTML report read successfully through the job artifact API. [Published report](https://reports.youdo.com/yandex/youdo-android-testing/3285160/report/report.html); the independent read used the GitLab artifact copy.
- Console terminal-event counts385PASSED/85FAILED/9SKIPPED include retries and are not final unique-test totals. Use the Gradle/HTML totals above.

## Infrastructure evidence

**Verdict: no confirmed recurrence of the earlier Appium/Grid/ADB infrastructure failure chain over the complete execution.** Final job failure is explicitly test-task failure; this does not prove the root cause of every failed test.

- Full-trace collector reports0Appium/UiAutomator,0Grid,0runner,0network-dependency,0artifact-delivery and0preparation-category matches. Three apparent ADB matches are false positives: the USB regex matches `usBusinessExecutor STANDARD_ERROR` inside a test name/header. Adjacent lines are `INFO: Detected dialect: W3C`, with test commands continuing; no USB fault is evidenced.
- Earlier `UnicodeIME`, session-creation, busy-systemPort and proxy failure signatures did not recur. Known nonfatal missing `emulator_2.service` preparation drift remains historical evidence; zero collector counts do not erase it.
- Separate manual scan finds20`java.net.SocketTimeoutException` lines, including replayed test logs. They are request-retry warnings, not evidence of the earlier Appium transport chain. Their destination, successful recovery and contribution to failed tests were not established. No claim that every dependency was healthy or every failed test was a locator/product defect.
- Exact correlation window November9 16:12:15–19:31:25UTC /19:12:15–22:31:25MSK. Fresh Enabled Selenium inventory fetched November12 16:04:31UTC contains M-K0056/M-K0057/M-K0058; this is current membership, not a historical membership snapshot.
- Zabbix46selectedmetrics all have window data;0interfaceerrors/unsupporteditems. Four CPU trigger transitions on M-K0057 are the two previously recorded low-idle episodes20:43–20:46 and20:49–20:58MSK, both recovered. Existing low-disk alarm remains; M-K0057minimum root free16.66GB. No sampled host uptime reset. Active physical devices remain `device`; excluded/unregistered-at-job-time Samsung A55 remains `unauthorized`. Emulator ADB history is absent; physical sample gaps up to121seconds prevent continuous transport guarantees.
- Loki selectors `{instance="M-K0056"}`, `{instance="M-K0057"}`, `{instance="M-K0058"}` cover the complete correlation window: all3operational streams, boundary samples present, no truncation, `coverage_complete=true`.2483categorizedevents:2463capability-name warnings (`adbExecTimeout`/`uiautomator2ServerLaunchTimeout`),20remainingentries concern emulator preparation/restart output including service kills. Start-of-job kills match controlled preparation; end-window restarts begin22:21:23MSK around job completion and continue after finish. Their initiator was not established; they do not demonstrate a prior mid-test outage. No categorized session/proxy/IME/USB failure found. Dedicated Hub application-log coverage remains unproven.
- Current November12 16:04:43UTC Hub HTTP200/99.4ms;8registered/busy,0free,7queued,all8proxiesregistered/Appiumreachable-ready. This is current saturation, not historical job evidence or a Hub outage. Historical job used15threads/7slots, with saturation already observed November9; its causal contribution to failed tests remains unverified.

## Changes and status

Sanitized collector summaries are under `~/ai-data/android-dig/3285160/*-final-20261112.json`; temporary full/tail traces were removed after analysis. Updated the historical snapshot note, existing Android system map and the affected central [TODO](../../../../TODO.md) item. Final-outcome review is complete; broader lifecycle/concurrency canary proposal remains open and unapproved. No new remediation authorized. All collectors completed; no background operations remain.

## Portable lesson

None. The ADB matcher false positives were classified manually; no collector/skill changes were requested or made.

## Follow-up proposal withdrawal — 2026-11-12

The user challenged the remaining lifecycle proposal, pointing out that A55 was already checked successfully. Verified [A55 evidence](2026-11-10-android-farm-a55-isolated-check.md): after the Play Protect intervention all3isolated create/command/quit cycles passed; production return was checked, and DevOps-914 was accepted closed. Earlier [fleet parallel checks](2026-11-09-android-farm-devops-912-grid-parallel-canary.md) passed60/60cycles at2/4/6workers. Together with the final real-job review above, these results give no concrete reason to keep the extra canary as required work. The agent withdrew the redundant follow-up proposal and closed its existing central TODO entry. This supersedes the open-proposal status in this note and older linked logs; it does not claim an additional limited-concurrency product-test canary ran, or a permanent fleet-wide guarantee. No external actions or background operations.
