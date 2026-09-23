---
system: android-farm
status: verified
checked: 2026-09-07
tags: [android, android-dig, gitlab-ci, testng, loki, job-3120554]
---
# Android infrastructure diagnosis — GitLab job 3120554

## Task

Read-only infrastructure diagnosis of GitLab autotest job `3120554` (retry suite failed before any Android session).

## Context

- Date: 2026-09-07 (Europe/Moscow)
- Project: `youdo/Test/youdo-android-testing`
- Job: `https://gitlab.youdo.sg/youdo/Test/youdo-android-testing/-/jobs/3120554`
- Scope: read-only GitLab trace/metadata, current Enabled Selenium inventory, current Selenium/Grid/Appium status, project routing variables, historical Zabbix state, and Loki coverage.
- Verdict: **No infrastructure failure found**. The job failed before any Android test or WebDriver/Appium session was created because TestNG could not parse the retry suite XML (`SAXParseException`, invalid content at line 1 column 1). Two missing `/opt/adb/adb_pkg.sh` preparation calls show non-causal configuration drift that was masked and did not lead to the observed exit.

## Job and correlation window

- Job status/failure: `failed`, `script_failure`; stage/name `tests` / `autotests`.
- Ref/SHA: `Test-7058`, `cac3f87b51818b012298be4ad29654a61a160c9c`.
- Pipeline: `138084`; runner `gitlab-runner-docker-1 integrations-tests (172.28.0.171)`, runner ID 108, online/active at collection.
- Job interval: 2026-09-07 16:55:50–16:58:42 UTC / 19:55:50–19:58:42 MSK.
- Correlation window: 2026-09-07 16:45:50–17:08:42 UTC / 19:45:50–20:08:42 MSK.
- Context: `JOB_ID=1`, `STAND=test1`, `SUITE=[Упавшие тесты]`, app version `4.0.268.staging (138041)`, source failed job `3118121` / pipeline `138054`.
- Source job 3118121 ran against the same SHA/ref and finished failed at 19:56:08 MSK. The retry job downloaded small inputs for the failed-suite path, then TestNG rejected the suite XML immediately. No test case or Android session started.
- Failure artifacts were still delivered: archive and JUnit uploads both returned HTTP 201. The expected renamed failed-suite XML and report HTML were absent, which also caused non-fatal after-script warnings.

## Inventory and routing

- Inventory fetched at 2026-09-07 20:01:52 UTC from Zabbix group `Selenium`, Enabled-only: `M-K0056` (`192.168.30.30`, hub), `M-K0057` (`192.168.30.31`), and `M-K0058` (`192.168.30.32`). All agent interfaces were available and no host was in maintenance.
- Current project variables fetched at 20:03:03 UTC route `JOB_ID=1` to `SELENIUM_SERVER_1=http://192.168.30.30:4444/wd/hub` and `APPIUM_NODES_1=192.168.30.31 192.168.30.32`, matching the fresh inventory. They are current definitions, not a historical effective-variable snapshot; group/pipeline/schedule/dotenv/runner variables are not covered.

## Findings: timeline and evidence

- 19:55:50 MSK: job started after 2.3 seconds queued; runner checkout/build path continued without runner, cache, DNS, TLS, Nexus, or Grid errors.
- Preparation: two calls to `/opt/adb/adb_pkg.sh` returned `No such file or directory`. The script continued; no corresponding ADB/session failure followed.
- 19:58:32.594 MSK: Gradle Test Executor failed while TestNG parsed the suite, with `SAXParseException: Content is not allowed in prolog` at line 1, column 1.
- 19:58:32.682 MSK: Gradle reported `There were failing tests`; this wrapper message represents the suite parser failure, not an executed Android assertion.
- 19:58:42 MSK: job ended exit code 1 after cache and artifact publication; GitLab accepted archive and JUnit artifacts with HTTP 201.

## Zabbix

- Exact-window collection at 20:05:14 UTC covered all 3 hosts and all 46 selected metrics: 0 current or overlapping problems, 0 trigger transitions, 0 interface errors, 0 unsupported items, and 0 metrics without window data.
- Agent ping remained 1 for every host; no uptime resets or network interface errors/drops were observed. Disk remained ample (minimum free: hub about 86.3 GB, M-K0057 about 22.9 GB, M-K0058 about 58.2 GB).
- All five monitored physical-device ADB histories remained `device` throughout the window (11–12 samples each, maximum gaps 120–121 seconds): M-K0057 `5b2d4fe2`, `RZCY20AXJHN`; M-K0058 `15888255AE004773`, `RZ8R71ZRK8H`, `x4pf5l5haegykni7`.
- M-K0057/M-K0058 showed high memory-use samples (max 99.13% / 98.78%); M-K0057 also had a one-sample iowait peak of 20.92%. There were no Zabbix problems, reboots, ADB transitions, or job trace symptoms tying these resource values to this failure. They are operational watch items, not a causal finding.

## Current Selenium/Grid/Appium state

- Checked at 2026-09-07 20:03:01 UTC using inventory-selected `M-K0056` at `192.168.30.30:4444`.
- Selenium 3.141.59 replied HTTP 200 in 95 ms. It reported raw `ready=false` only because all 8 slots were busy: total 8, free 0, busy 8, with 7 new-session requests queued. Operational classification: `saturated`, not Hub outage.
- Grid console and hub totals agreed: 8 registered/busy proxies. All 8 proxy API checks passed and all 8 direct Appium 1.22.3 status checks returned ready (80–89 ms): M-K0057 ports 15001–15004 and M-K0058 ports 15001–15004.
- This check is current, about three hours after the historical job, and cannot prove historical Grid/UiAutomator2 health. The job itself never reached Grid, so the present saturation is not causal for job 3120554.

## Loki coverage

- `loki_logs.py` failed with HTTP 404. Required manual discovery against `http://loki-read.yandex-test.youdo.local` also returned 404 for `/loki/api/v1/labels`, `/api/v1/labels`, `/ready`, and `/` in the exact interval.
- Therefore no `instance` values, selectors, boundary samples, operational streams, or infrastructure events could be collected for `{instance=~"M-K0056|M-K0057|M-K0058"}`. This is an API/route coverage gap, not evidence of healthy host logs.

## Open items: excluded failures and next actions

- Excluded from Android infrastructure diagnosis: malformed/non-XML failed-suite input consumed by TestNG. Investigate the producer/download/validation logic for `FailedTestSuite.xml` between job 3118121 and retry job 3120554; require HTTP success, XML content type or signature, non-trivial size, and XML validation before Gradle starts. Preserve the bad payload only in approved protected artifacts if needed.
- Fix the CI preparation contract for `/opt/adb/adb_pkg.sh`: either restore/provision the script on both current Appium nodes or remove/update the stale invocation. Remove `|| true` masking for mandatory preparation, or emit an explicit degraded warning when optional. Roll back by restoring the previous known-good helper/package-cleanup behavior.
- Restore/confirm the Loki read route used by the collector and Grafana datasource, then validate `/loki/api/v1/labels` and exact-window `instance` coverage. Do not infer machine health from the present 404.
- Separately trend M-K0057/M-K0058 memory pressure and the M-K0057 iowait spike; no remediation is justified from this job alone.

## Open items: confidence and gaps

- High confidence that Grid/Appium/ADB did not cause this job failure: the decisive exception occurred during local TestNG suite parsing before session creation, trace contains no session/ADB/Grid errors, Zabbix fully covers the exact window, and artifact upload succeeded.
- Loki evidence is unavailable due HTTP 404. Current Hub status is not historical evidence. Project variables are current and only project-scoped. The trace's collapsed shell block does not expose the exact suite download command or payload, so the mechanism that produced the invalid XML remains a hypothesis pending inspection of protected CI configuration/artifacts.
- Temporary sanitized trace and inventory snapshot were deleted after analysis. No credentials or raw sensitive payloads were persisted.

## Portable lesson

none
