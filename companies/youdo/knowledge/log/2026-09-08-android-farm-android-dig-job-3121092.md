---
system: android-farm
status: verified
checked: 2026-09-08
tags: [android, android-dig, gitlab-ci, appium, systemport, samsung, redmi, job-3121092]
---
# Android infrastructure diagnosis — GitLab job 3121092

## Task

Read-only infrastructure diagnosis of GitLab autotest job `3121092` (UiAutomator2 `systemPort` 15903 busy on M-K0057, `UnicodeIME` missing on M-K0058), followed by direct SSH verification at the user's request.

## Context

- Date: 2026-09-08, Europe/Moscow.
- Job: `https://gitlab.youdo.sg/youdo/Test/youdo-android-testing/-/jobs/3121092`.
- Project/ref/SHA: `youdo/Test/youdo-android-testing`, `Test-7058`, `0b55826488a1714ad82c581aa86bd15533229205`.
- Verdict: **Confirmed infrastructure failure**.

## Job context

- GitLab status/failure reason: `failed` / `script_failure`; runner remained online.
- Job interval: 2026-09-08 08:06:01–08:23:04 UTC / 11:06:01–11:23:04 MSK.
- Correlation window: 07:56:01–08:33:04 UTC / 10:56:01–11:33:04 MSK.
- Runner: `gitlab-runner-docker-1 integrations-tests (172.28.0.171)`, Docker executor, Gradle image tag `12`.
- Selection: `JOB_ID=1`, `STAND=test1`, suite `[Упавшие тесты]`, predecessor failed job `3120886`; 75 tests completed, 58 failed, 9 skipped.
- Current project routing fetched at 08:44:03 UTC: `SELENIUM_SERVER_1=http://192.168.30.30:4444/wd/hub`, `APPIUM_NODES_1=192.168.30.31 192.168.30.32`. These are current project-level values, not a historical resolved environment; group/pipeline/schedule/runner overrides were not covered.

## Findings: confirmed infrastructure evidence

1. Device preparation reached both current Appium nodes, but `emulator_2.service` was absent on one target and `/opt/adb/adb_pkg.sh` was absent on both targets. The CI preparation continued despite these errors.
2. Beginning at 08:10:09 UTC / 11:10:09 MSK, the job repeatedly failed session creation with `UiAutomator2 Server cannot start because the local port #15903 is busy`.
3. Loki correlates those timestamps to `M-K0057`, `phone_samsung_galaxy_a55.service`, device `RZCY20AXJHN`: Appium repeatedly attempted cleanup of the `tcp:15903` ADB forward and reported that the listener was not found. Later direct SSH evidence showed that this port is normally owned by the ADB forward of an active session on the same device. The incident is therefore an overlapping session create/teardown race on that node/service path, not a foreign listener, GitLab runner outage, or Grid transport outage; the evidence does not identify which request first held the port.
4. A separate session failure at 08:10:15 UTC / 11:10:15 MSK affected `M-K0058`, `phone_redmi_note_13_pro.service`, device `x4pf5l5haegykni7`: Appium could not enable `io.appium.settings/.UnicodeIME` because the input method was unknown. The missing `adb_pkg.sh` preparation helper is direct evidence that helper-package repair/normalization did not run.
5. Zabbix ADB histories showed all monitored physical devices, including `RZCY20AXJHN` and `x4pf5l5haegykni7`, continuously in `device` state across the window. This excludes an ADB offline/unauthorized transport outage as the cause of these failures.

## Zabbix

- Inventory fetched at 08:43:59 UTC: Enabled Selenium hosts `M-K0056`, `M-K0057`, `M-K0058`; all agent interfaces available and none in maintenance.
- Historical collection found 0 current problems, 0 overlapping recent problems, 0 exact-window trigger transitions, 0 interface errors, 0 unsupported items, and data for all 46 selected metrics.
- Agent ping remained 1 and monitored network error/drop counters remained 0 on all three hosts.
- M-K0057 memory use was 91.3–99.25% and had a transient CPU iowait sample up to 66.26%; M-K0058 memory use was 93.1–98.81%. No Zabbix trigger or Loki OOM evidence correlated these resource levels to the decisive session errors, so they remain risk signals rather than assigned root causes.

## Loki

- Read endpoint: `http://loki.dev.youdo.corp`.
- Coverage was complete for the correlation window: all three `instance` values existed, all had operational streams and boundary samples, and no event query was truncated.
- Relevant selectors: `{instance="M-K0057", unit="phone_samsung_galaxy_a55.service"}` and `{instance="M-K0058", unit="phone_redmi_note_13_pro.service"}`.
- Emulator services were intentionally restarted by CI preparation; their SIGKILL-after-graceful-wait events are not independently classified as an outage.

## Current Selenium/Grid snapshot

- At 08:44:00 UTC, inventory-selected Hub `M-K0056` at `192.168.30.30:4444` responded in about 112 ms and identified Selenium 3.141.59.
- Hub state was `saturated`, not unhealthy: 8 total / 8 busy / 0 free slots with 7 queued new-session requests.
- All 8 proxies were registered and inventory-matched; all 8 direct Appium status endpoints were reachable and ready. This is current recovery/readiness evidence only, not proof of job-window health.

## Delivery and excluded scope

- No runner, dependency/network, or artifact-delivery failure was extracted. S3 report sync completed, GitLab archive and JUnit uploads returned HTTP 201, and the failure exit followed test failures.
- Product assertions, locators, and business behavior were not diagnosed. Parallel/replayed trace output prevents a reliable one-to-one attribution of all 58 failed tests, but the run is dominated by infrastructure session-creation failures.

## Open items: recommended infrastructure actions

1. On `M-K0057`, capture concurrent session-create/quit timing for the Samsung A55 service and verify that Grid/Appium does not release or reuse its single slot before UiAutomator2 cleanup has removed the ADB forward. Reproduce with a controlled create → quit → immediate create test before changing timeouts or service state.
2. Restore/provision `/opt/adb/adb_pkg.sh` consistently on both Appium nodes or replace the masked CI preparation with an authoritative helper-package check. Verify `io.appium.settings` and `.UnicodeIME` on `x4pf5l5haegykni7` before returning the device to the pool.
3. Reconcile the unconditional `EMULATORS="emulator_1 emulator_2"` preparation loop with per-host inventory so the expected absence of `emulator_2.service` is not silently ignored.
4. Make preparation fail fast for missing helper scripts and unexpected unit failures; retain explicit exceptions only for documented per-host topology.
5. Review sustained high memory use on M-K0057/M-K0058 separately; no causal link to this job was proven.

No retries, restarts, session kills, ADB mutations, or infrastructure changes were performed.

## Direct SSH verification of M-K0057 — 2026-09-08 11:54 MSK

Performed at the user's explicit request with read-only commands against `root@192.168.30.31`; the remote hostname returned `M-K0057`.

- `phone_samsung_galaxy_a55.service` was `active/running`, PID `518893`, with no systemd restarts. The same process has run since 2026-08-20 19:15 MSK and listens on Appium TCP `15003`.
- Its `ExecStart` fixes `udid=RZCY20AXJHN` and `systemPort=15903` and enables `--session-override`.
- The host journal contains **109** explicit `local port #15903 is busy` errors from 11:10:09 through 11:13:29 MSK. Cleanup attempts against `RZCY20AXJHN` returned `listener 'tcp:15903' not found`.
- At 11:54 MSK, TCP `15903` had no listener, `adb forward --list` was empty, Appium `:15003` was listening, and `/wd/hub/sessions` returned no active sessions. The collision had cleared without restarting the Appium systemd service.
- At 11:58:52 MSK, a newly active legitimate session made the lifecycle observable: PID `39064` (`adb`) listened on `127.0.0.1:15903`; `adb forward --list` mapped `RZCY20AXJHN tcp:15903 tcp:6790`; Appium `:15003` reported one session for that UDID and `systemPort=15903`. This proves that the port-busy condition is the same device's normal active-session forward, not an unrelated host process. During job 3121092, new session creation overlapped a still-held forward; the exact request-order race cannot be reconstructed retrospectively.
- `RZCY20AXJHN` was currently `device`; `io.appium.settings` was installed and `.UnicodeIME` appeared in `ime list -s`.
- `/opt/adb/adb_pkg.sh` was still absent, confirming persistent host/CI preparation-contract drift.
- Direct memory view showed 31 GiB total, 21 GiB available, 3.6 GiB free, 18 GiB buff/cache and essentially unused swap. The high Zabbix `vm.memory.size[pused]` percentage is therefore dominated by cache/accounting and is not evidence of immediate memory exhaustion.
- Root filesystem: 98 GiB total, 22 GiB available, 77% used.
- The unrelated USB device `GHKBB23B15002735` remained `unauthorized`; it is outside the Appium farm scope.

No state was changed over SSH.

## Portable lesson

none
