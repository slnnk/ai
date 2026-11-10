---
system: android-farm
status: verified
checked: 2026-11-10
tags: [android-dig, appium, adb, loki, zabbix]
---
# Android farm: job 3287595 Samsung A55 infrastructure failure

## Task
Read-only infrastructure diagnosis of [job3287595](https://gitlab.youdo.sg/youdo/Test/youdo-android-testing/-/jobs/3287595). Verdict: **Confirmed infrastructure failure** on Samsung A55 RZCY20AXJHN, M-K0057, Appium15003/systemPort15903. Root cause of Android instability remains unknown.

## Context
Project youdo/Test/youdo-android-testing; pipeline142644; ref Test-7062; SHA e707f9c4a7869614c4c521d607e100738f5156bc. Job autotests/tests failed with script_failure after1375s; runner108 gitlab-runner-docker-1 integrations-tests172.28.0.171. JOB_ID1, test5, suite `[Упавшие тесты]`, prior job3287209. App version4.0.275.feature-and-4674-ucassa-exp(142519). Fifteen test threads.
Job2026-11-10 11:25:19–11:48:14UTC /14:25:19–14:48:14MSK. Correlation11:15:19–11:58:14UTC /14:15:19–14:58:14MSK.
[System map](../systems/android-farm/system-map.md).

## Actions
Used bundled android-dig collectors: zabbix_hosts, selenium_hub, gitlab_job, gitlab_ci_variables, zabbix_health and loki_logs. Zabbix inventory fetched11:55:50UTC: Enabled M-K0056(.30), M-K0057(.31), M-K0058(.32), no maintenance/interface errors. The same snapshot scoped Hub, health and Loki queries. Sanitized collector JSON retained under ~/ai-data/android-dig-3287595-*.json; temporary full trace deleted after analysis. No remote mutations, SSH, retries, ADB commands or service changes.

## Findings
- Preparation restarted emulators; trace reports `Failed to restart emulator_2.service: Unit emulator_2.service not found.` and package-not-found messages but proceeds. Loki SIGKILL exits during11:26UTC align with CI preparation; not proof of an independent emulator crash.
-11:29:49.252UTC /14:29:49.252MSK: first job SessionNotCreatedException for A55, adb install of appium-uiautomator2-server-v4.27.0.apk exceeds20000ms. Repeats throughout execution, last logged14:47:49MSK. Full trace has88 exception lines of this type,31 missing Android settings-service lines and7 device-not-connected lines; repeated stack traces are not distinct failed-test counts.
- Loki `{instance="M-K0057",unit="phone_samsung_galaxy_a55.service",job="integrations/journal"}` corroborates failed UiAutomator2 cleanup at11:29:48.872UTC and repeatedly afterward. At11:41:52.605UTC /14:41:52.605MSK: `Failure calling service activity: Broken pipe (32)`;11:41:53 onward: `Can't find service: activity`, missing15903 forward. Job14:41:52.952MSK also reports `Can't find service: settings`;14:42:14 and14:47:45MSK reports A55 absent from connected devices. This confirms Android/device readiness failure, not an assertion issue. Reboot, USB failure, Android system_server failure and external intervention are unproven explanations.
- Zabbix has46 metrics with history, no unsupported items or exact-window trigger transitions. A55 remains `device` in21 samples at120s cadence; transient disconnects and Android-service failures evade this coarse transport check. Other monitored physical devices also remain `device`; emulator ADB status coverage is absent.
- M-K0057 resource pressure: memory80.65–99.23%, load/core max2.4421, idle minimum1.85%, iowait max21.30%, root free minimum16.58GB. A root-free-space<20% problem started2026-11-09 09:53:36UTC and remains open; returned event omits host association, so do not independently assign it from the event alone. M-K0058 memory93.43–99.06%, iowait max2.18%, free50.62GB. No host uptime resets or agent-ping drops. These ranges are window aggregates; resource pressure causality is unproven.
- Loki operational streams and boundary samples exist for all3hosts; no query/stream truncation, no security-only gap. Boundary tail samples precede configured window end by69–116s; collection11:57UTC occurred before nominal11:58:14UTC end, but covers finished job. Selector `{instance=~"M-K0056|M-K0057|M-K0058"}`, interval above. Capability names containing timeout in BaseDriver logs are configuration fields, not failures.
- Current Hub at11:56:18UTC /14:56:18MSK, inventory-derived192.168.30.30:4444: Selenium3.141.59, ready, HTTP200/83.7ms,8total/8free/0busy/queue0. All8proxies registered and all8Appium1.22.3 status endpoints ready. Devices: M-K0057 emulator-5554:15001, emulator-5556:15002, RZCY20AXJHN:15003,5b2d4fe2:15004; M-K0058 emulator-5554:15001,15888255AE004773:15002,x4pf5l5haegykni7:15003,RZ8R71ZRK8H:15004. All idle. Current HTTP readiness does not demonstrate recovered A55 Android commands/session creation; console Android versions are generic and not authoritative device versions.
- Project variables fetched11:56:34UTC: APPIUM_NODES_1=.31/.32 and SELENIUM_SERVER_1=.30:4444 align with JOB_ID1/inventory. Pool2 addresses are outside Enabled inventory and unused by this job. Definitions are current, scope `*`, not historical resolved job values; group/pipeline/schedule/dotenv/runner overrides were not collected.
- Runner checkout/cache and Nexus version download succeeded. Final Gradle result: `57 tests completed, 48 failed, 9 skipped`. No passing tests in this summary. NoSuchElementException appears18times, excluded from product/locator investigation; do not attribute all48 failures to A55. Reports uploaded to object storage; cache and GitLab archive/JUnit uploads succeeded (201). No artifact-delivery failure.

## Changes
Only this diagnosis log, central TODO proposal and generated indexes. No stable new topology facts require a map rewrite.

## Status and risks
Diagnosis complete. High confidence in device/Appium infrastructure failure; low confidence in underlying trigger or recovery. Current HTTP status cannot certify A55 healthy. Recommended isolated A55 readiness/session canary and any recovery require separate explicit authorization; see central [android-farm backlog](../../../../TODO.md#android-farm). Existing preparation-contract and memory-pressure proposals remain open. Avoid global resets during other sessions; preserve io.appium.settings per DevOps-912. No task background operations remain.

## Portable lesson
none

## Follow-up — 2026-11-10 15:08 MSK

User stopped A55 Appium and approved an isolated session canary. First create failed on20sUiAutomator2 androidTestAPK installation; production remainsstopped. This supersedes HTTP-only recovery uncertainty with a reproduced isolated failure. See [follow-up](2026-11-10-android-farm-a55-isolated-check.md); exact cause remainsunknown.
