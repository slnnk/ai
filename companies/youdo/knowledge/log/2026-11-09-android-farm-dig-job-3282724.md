---
system: android-farm
status: verified
checked: 2026-11-09
tags: [android-dig, appium, selenium, loki]
---
# Android job3282724: session failures after Xiaomi isolation

## Task
Read-only investigation of persistent infrastructure errors in job3282724 after isolating Xiaomi `x4pf5l5haegykni7`. No new remediation authorized or performed.

## Context
Project `youdo/Test/youdo-android-testing`, `autotests`, stage `tests`, pipeline142540, `Test-7062`, SHA `5cbe63fe265c09b65ecb5e46e9e48e3e8053615f`, runner108 `gitlab-runner-docker-1 integrations-tests (172.28.0.171)`.
CI context: pool `JOB_ID=1`, stand `test5`, suite `[Упавшие тесты]`, previous failed job3282427/pipeline142526, app `4.0.275.feature-and-4674-ucassa-exp (142519)`.
Job14:09:50–16:07:03 MSK /11:09:50–13:07:03 UTC, query13:59:50–16:17:03 MSK /10:59:50–13:17:03 UTC.
Related [prior job](2026-11-09-android-farm-dig-job-3282427.md), [Xiaomi isolation](2026-11-09-android-farm-xiaomi-unicodeime-device-check.md), [farm map](../systems/android-farm/system-map.md).

## Actions
Fresh Enabled Selenium inventory, Hub/proxy/Appium status, GitLab metadata/trace/current project variables, historical Zabbix and Loki collectors. Generated sanitized summaries in `~/ai-data/android-dig/3282724/`. Full raw trace was not persisted. A streaming pass retained categorized infrastructure exceptions only, with final upload status stripped of runner tokens. Counts below are exception-line counts, not distinct sessions/tests, and include repeated reporting output.

## Findings
Confirmed infrastructure failure, broader than Xiaomi UnicodeIME: session-creation port conflicts and timeouts occur alongside Appium/UiAutomator2 session lifecycle errors across multiple registered devices.

### GitLab and console
- Status `failed`, `failure_reason=script_failure`, no trace-size termination. Trace201846752bytes, approximately1.75millionlines. `522 tests completed, 460 failed, 9 skipped`; archive and JUnit uploads both201Created. `BUILD FAILED`16:06:16MSK and final exit1. These totals do not classify all460failures as infrastructure.
- Before15:12MSK, session-exception lines include37Grid-forward timeouts,32busy-systemPort errors,295unknown-session errors and10instrumentation startup timeouts. UnicodeIME appears14:14:17MSK on Xiaomi.
- After15:12MSK, console includes34Grid-forward timeout lines,33busy-systemPort lines,1662unknown-session lines and11instrumentation startup-timeout lines. Port15901/15902 conflicts and60000msinstrumentation failures remain beyond Xiaomi isolation. These counts are not independent failure counts.
- Late16:05–16:06MSK output also includes old UnicodeIME and TECNO15002connection failures. Detailed request/HTML/report output is repeatedly re-emitted, so outer Gradle timestamps do not necessarily timestamp a new device operation. Do not claim Xiaomi rejoined Grid from the late repeated UnicodeIME stacktrace. TECNO was manually stopped15:07:32MSK and later restored at user's request; the trace includes the resulting15002connection errors from15:07:32onward. Do not attribute those known operator-intervention errors to a spontaneous outage.

### Loki correlation
Selectors `{instance="M-K0056"}`, `{instance="M-K0057"}`, `{instance="M-K0058"}`; operational journal streams present, beginning/end samples covered, final collector coverage complete with no event-query truncation. No Grid application-specific stream identified on Hub.
- After15:12MSK and before16:05MSK,586categorized Appium cleanup messages contain `The session identified by ... is not known` across M-K0057 emulator1/emulator2 and M-K0058 emulator1/SamsungA12/TECNO. These are independent machine-log evidence that the remaining farm still had session lifecycle failures, not merely repeated console output. Cleanup warnings alone do not establish whether the client, Appium, UiAutomator2 or routing invalidated the session first.
- Targeted15:25–15:35MSK query confirms unknown-session cleanup messages on these same5units. This is after Xiaomi shutdown.
- M-K0058 SamsungA12 `phone_samsung_galaxy_a12.service` at15:44:53MSK: cleanup proxy fails with `connect ECONNREFUSED 127.0.0.1:15904`; M-K0057 emulator1 at15:46:29MSK has `ECONNREFUSED 127.0.0.1:15901`; M-K0058 emulator1 at15:47:24MSK has `socket hang up`. Treat as teardown evidence, not independently proven normal-command failures.
- Emulator service process kills during preparation11:10–11:11UTC and after job finish13:08UTC align with known CI preparation behavior; not evidence of OOM without supporting signals.

### Zabbix
46selected metrics all have historical data; no unsupported items, interface errors or exact-window trigger transitions. Existing M-K0057 root-free threshold alarm overlaps the window; minimum free16.97GB. CPU per-core load max2.2949/iowait35.6137% onM-K0057; M-K0058load max1.053/iowait15.3055%. No observed reboot; physical ADB histories show `device` except long-standing M-K0057SamsungA55 `unauthorized`. ADB sampling gaps reach360seconds and emulator ADB items were not returned, so transient/UiAutomator2 faults are not ruled out.

### Current inventory, Grid and variables
Inventory fetched15:11:51UTC /18:11:51MSK, Enabled M-K0056/M-K0057/M-K0058. Hub selected from inventory `192.168.30.30:4444`, HTTP200/105.9ms. At18:12:04MSK:6slots busy,0free,9queued requests, `saturated`;6proxies registered and6Appium endpoints ready. Xiaomi remains absent. Registered M-K0057 ports15001emulator5554,15002emulator5556,15004Redmi5b2d4fe2; M-K0058ports15001emulator5554,15002TECNO15888255AE004773,15004SamsungRZ8R71ZRK8H. Current checks do not establish historical recovery or command health.
Current project scope `*` routing pool1 stillM-K0057/M-K0058 and Hub30:4444; pool2 outside current Enabled scope. Definitions are current, not historical effective variables; group/pipeline/schedule/dotenv/runner overrides not covered.

## Interpretation and next decision
Confirmed session failures span several devices; removing Xiaomi addresses only its IME issue. Likely shared session lifecycle/cleanup/forward ownership is involved, with Grid saturation as a concurrent condition. Neither a single root cause nor the initiating component is established. Existing CI configuration inspected earlier uses15threads against6current slots; queueing is expected, but excess thread count alone does not prove the invalid-session or busy-port cause.
A proposed controlled canary should use one reserved device and one worker, capture create/quit/request timing and port ownership, then compare bounded parallelism. It must not trigger host-wide preparation against devices serving other jobs. No blind timeout increase, broad restart, session kill or new job was performed. Assertions/locators/product behavior were excluded; precise infrastructure-versus-product test counts are not established.

## Changes
This local note and task-related central TODO evidence only; no remote state changes.

## Status and risks
Diagnosis completed with high confidence in ongoing infrastructure session failures, lower confidence in causal explanation. Follow-up proposals remain in central [TODO](../../../../TODO.md), android-farm section. Existing isolation remains intentional. Raw machine logs were obtained exclusively through Loki.

## Portable lesson
none
