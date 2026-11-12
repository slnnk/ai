---
system: android-farm
status: verified
checked: 2026-11-09
tags: [android-dig, gitlab-ci, loki, zabbix]
---
# Android farm: job 3282427 exceeded GitLab trace size

## Task
Read-only infrastructure diagnosis of GitLab Android autotest job 3282427 in `youdo/Test/youdo-android-testing`.

## Context
Job `autotests`, stage `tests`, pipeline `142526`, ref `Test-7062`, SHA `5cbe63fe265c09b65ecb5e46e9e48e3e8053615f`.
Runner 108: `gitlab-runner-docker-1 integrations-tests (172.28.0.171)`.
Job interval 2026-11-09 09:37:11–11:09:48 UTC / 12:37:11–14:09:48 Europe/Moscow.
Correlation interval 09:27:11–11:19:48 UTC / 12:27:11–14:19:48 Europe/Moscow.
See [farm map](../systems/android-farm/system-map.md).

## Actions
Used bundled read-only Zabbix inventory, Hub, GitLab job, project variables, Zabbix health and Loki collectors.
Inventory fetched at 11:58:54 UTC: Enabled hosts `M-K0056`, `M-K0057`, `M-K0058`; no maintenance or agent-interface errors.
Generated sanitized collector data is under `~/ai-data/android-dig/3282427/`; no raw trace persisted.
The standard trace reader rejected a response above 100 MiB; retried with a larger bound and completed. A temporary streaming summary was inspected and deleted because request payloads/headers are not suitable for durable storage.
Loki initial M-K0058 query hit its chunk cap; repeated with 100 chunks and 20000 events, obtaining complete collector coverage.

## Findings
- Full trace: 209371617 bytes (199.67 MiB), 1832332 normalized lines. CI context: `JOB_ID=1`, `STAND=test5`, `SUITE=[Регресс приложения]`, `APP_VERSION=4.0.275.feature-and-4674-ucassa-exp (142519)`; image `gradle:18`, Docker executor. Checkout, cache extraction and Nexus version-marker HTTP200 succeeded. Preparation included `Failed to restart emulator_2.service: Unit emulator_2.service not found.`; script continued. The missing preparation contract is already tracked centrally.
- Trace 09:46:38.845 UTC / 12:46:38.845 MSK: session creation failed for Xiaomi/Redmi Note 13 Pro `x4pf5l5haegykni7`: `Unknown input method io.appium.settings/.UnicodeIME cannot be enabled for user #0`, adb exit255. This repeats at 11:08:29.972 UTC / 14:08:29.972 MSK. This documents recurrence; the previously deferred root-cause/remediation investigation was not resumed.
- Trace 09:46:50–09:46:54 UTC: Grid new-session forwarding timeouts. At 09:47:01.165 UTC: `UiAutomator2 Server cannot start because the local port #15904 is busy`. At 09:47:21.048 UTC: session creation fails with `Could not proxy command` / `socket hang up`; later `The session ... is not known`. Extractor counts 2440 Grid and 4342 Appium matching lines, including duplicated stacktrace lines; these are not distinct failed-test counts.
- Trace ends at 11:08:44 UTC / 14:08:44 MSK inside DEBUG `TestEventLogger` output containing HTTP request/response and HTML report content. This identifies excessive console logging as the direct volume concern; the share caused specifically by session retries is not measured. No final build result, artifact upload or report-publication confirmation was present in the captured trace. Test assertions/product behavior were not investigated; no reliable final test count was available.
- Confirmed infrastructure failure: GitLab metadata reports `failed`, `failure_reason=trace_size_exceeded` at 11:09:48 UTC. This independently establishes the CI termination cause; it does not establish why logging grew.
- Current project routing definitions, fetched at 11:59:08 UTC, scope `*`: `APPIUM_NODES_1=192.168.30.31 192.168.30.32`, `SELENIUM_SERVER_1=http://192.168.30.30:4444/wd/hub`. Pool 2 addresses are outside current Enabled inventory. These are current project definitions, not historical/effective job variables; group, schedule, pipeline, dotenv and runner values are not covered.
- Zabbix: all 46 selected metrics have window data, no unsupported items or interface errors. No uptime reset; physical network error/drop counters remained zero. Physical ADB devices stayed `device` except `RZCY20AXJHN` on M-K0057, which stayed `unauthorized` (existing problem since September 22). No emulator ADB status histories were returned.
- M-K0057 root free-space alarm recovered at 09:38:36 UTC, recurred at 09:53:36 UTC and remained open at collection. Minimum free space was 16.8 GB; this is a threshold alarm, not a full filesystem. High-load alarm 10:43:33–10:47:33 UTC; low-idle alarm 10:46:08–10:50:09 UTC. Maximum per-core load 2.9832, maximum iowait 57.9631%. Memory pused peaked at 99.2852% (M-K0057) and 99.0425% (M-K0058); no OOM causality established.
- Loki selectors `{instance="M-K0056"}`, `{instance="M-K0057"}`, `{instance="M-K0058"}`, excluding security streams, cover the correlation interval with boundary samples and no final query truncation. Hub system journal exists but a Grid application log stream was not identified.
- M-K0058 `phone_tecno_cm7.service`: 250 `socket hang up` delete-session warnings, 09:53:11–11:02:59 UTC, plus two warnings that UiAutomator2 instrumentation was not running (09:52:06 and 10:38:09 UTC). ADB stayed `device`; this cannot prove UiAutomator2 health. Other nodes also emitted isolated delete-session warnings. Cleanup warnings alone do not establish failures of normal test commands or attribution to this job amid concurrent activity.
- Current Hub check 11:59:10 UTC: inventory-selected `192.168.30.30:4444`, Selenium 3.141.59, HTTP 200 in 299.9 ms. Seven slots, all busy, zero free, eight queued session requests: `saturated`, not Hub outage. All seven proxies registered and all Appium 1.22.3 status endpoints ready.
- Current devices: M-K0057 ports 15001 emulator-5554, 15002 emulator-5556, 15004 5b2d4fe2; M-K0058 ports 15001 emulator-5554, 15002 15888255AE004773, 15003 x4pf5l5haegykni7, 15004 RZ8R71ZRK8H. All busy at collection. Current status cannot prove historical recovery, ADB or UiAutomator2 command health.

## Changes
Local diagnosis note and central backlog bookkeeping only. No repository, CI configuration, service, session, device or external tracker was changed.

## Status and risks
GitLab termination cause is confirmed. Console DEBUG/report/request logging is evidenced; exact per-source volume and final report/artifact completion are not established. Device cleanup errors and M-K0057 resource pressure are correlated observations with no proven causal link to trace size. Infrastructure follow-up proposals are tracked in the central [TODO](../../../../TODO.md), android-farm section; recording grants no remediation permission. Earlier deferred UnicodeIME root-cause/remediation investigation remains deferred. Confidence is high for CI termination and observed session-creation errors; a single causal chain from host pressure/device cleanup to log growth is unproven. Proposed CI logging changes should preserve detailed file artifacts, be reversible and be reviewed before an authorized canary; no automatic limit increase, retry or service reset was performed.

## Portable lesson
none

## Device identity correction and isolation — 2026-11-09

Direct read-only ADB and systemd inspection confirmed `x4pf5l5haegykni7` is Xiaomi model `23117RA68G`, Android13, `phone_redmi_note_13_pro.service`, Appium15003/systemPort15903. Earlier user-facing TECNO attribution was wrong. TECNO is `15888255AE004773`, `phone_tecno_cm7.service`, Appium15002/systemPort15902; its numerous cleanup warnings are separate evidence. User explicitly requested restoring TECNO and stopping the problematic Xiaomi service; both state changes were executed and verified. See [direct diagnosis](2026-11-09-android-farm-xiaomi-unicodeime-device-check.md).

## Resource follow-up cancelled — 2026-11-12

The user cancelled the separate M-K0057/M-K0058 memory/iowait/free-disk check because Zabbix already monitors these hosts. Historical resource measurements above remain observations, not an active follow-up or a proven cause of test failures. The central TODO entry is closed as cancelled; no new diagnostics or remediation performed. [Scoped decision](../systems/android-farm/system-map.md#resource-monitoring-decision--2026-11-12).

## DEBUG reduction proposal withdrawn — 2026-11-12

The user clarified that test logs are emitted only in DEBUG mode. Preserve DEBUG; the agent withdrew the blanket logging-reduction follow-up and closed its central TODO entry. Historical trace overflow remains evidence, not a current mandate to suppress required logs. No logging change or replacement task. [Scoped constraint](../systems/android-farm/ci-cd.md#autotest-debug-logging-constraint--2026-11-12).
