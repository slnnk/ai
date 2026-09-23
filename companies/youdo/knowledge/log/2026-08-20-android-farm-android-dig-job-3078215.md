---
system: android-farm
status: verified
checked: 2026-08-20
tags: [android, android-dig, gitlab-ci, appium, unicodeime, redmi, job-3078215]
---
# Android infrastructure diagnosis: GitLab job 3078215

## Task

Read-only infrastructure diagnosis of GitLab autotest job `3078215` (Appium session creation failure on Redmi Note 13 Pro).

## Context

- Date: 2026-08-20 (Europe/Moscow)
- Project: `youdo/Test/youdo-android-testing`, branch `master`, commit `38f5a58f56ec3792344de1b2ceac1b9ae0c57d20`
- Job: `https://gitlab.youdo.sg/youdo/Test/youdo-android-testing/-/jobs/3078215`
- Pipeline: 137053; suite `[СБР]`; stand `test8`; `JOB_ID=1`
- Read-only investigation; no services, devices, jobs, or monitoring state were changed.

## Verdict

**Confirmed infrastructure failure.** One of five failed tests could not create an Appium session on Xiaomi Redmi Note 13 Pro (`x4pf5l5haegykni7`) because the Appium Settings helper input method `io.appium.settings/.UnicodeIME` was absent or not registered for Android user 0. This is device/Appium preparation drift, not ADB transport loss.

The other four failures were outside the infrastructure scope: three `NoSuchElementException` failures on active sessions and one application/API response mismatch (`H2 500`, expected 200).

## Job and correlation window

- Job status: failed (`script_failure`, exit code 1); 10 tests, 5 failed.
- Job interval: 2026-08-20 16:40:45–16:58:51 UTC / 19:40:45–19:58:51 MSK.
- Correlation window: 16:30:45–17:08:51 UTC / 19:30:45–20:08:51 MSK.
- Runner: `gitlab-runner-docker-1 integrations-tests (172.28.0.171)`, runner ID 108; current GitLab state was online/active.
- Artifact archive and JUnit upload both completed with HTTP 201; failure was not artifact delivery.

## Routing and current inventory

Inventory fetched from Zabbix group `Selenium` at 2026-08-20 16:59:18 UTC. Enabled hosts only:

- `M-K0056` / visible `M-K0056-selenium-hub`, agent IP `192.168.30.30`;
- `M-K0057`, agent IP `192.168.30.31`;
- `M-K0058`, agent IP `192.168.30.32`.

Current project variables fetched at 16:59:47 UTC route `JOB_ID=1` to `SELENIUM_SERVER_1=http://192.168.30.30:4444/wd/hub` and Appium nodes `192.168.30.31 192.168.30.32`. These definitions are current, not a historical variable snapshot; trace evidence confirms the same Hub and job ID.

The implicated device belongs to `M-K0058`, unit `phone_redmi_note_13_pro.service`, Appium/Grid port 15003, UiAutomator2 `systemPort=15903`.

## Findings: evidence timeline

- 19:40–19:42 MSK: CI preparation reached both Appium hosts. It reported `Failed to restart emulator_2.service: Unit emulator_2.service not found`, then printed `Success` for preparation of `x4pf5l5haegykni7`. This unrelated missing unit is on the shared preparation path and should be cleaned up, but it is not the failed Redmi service.
- 19:50:35 MSK: Loki `{instance="M-K0058", unit="phone_redmi_note_13_pro.service"}` shows an old session closing after the 600-second new-command timeout; UiAutomator2 instrumentation was no longer running.
- 19:50:38 MSK: the job reports `SessionNotCreatedException`; ADB command `ime enable io.appium.settings/.UnicodeIME` exits 255 because the input method is unknown for user 0.
- 19:50:38 MSK: Loki on the same host/unit/UDID reports cleanup failure because forward `tcp:15903` was absent, corroborating the exact Appium node and session teardown path.
- Throughout the correlation window, Zabbix `adb_dev.status[x4pf5l5haegykni7]` sampled 14 times and remained `device`; agent ping remained 1. There is no evidence of `offline`, `unauthorized`, host reboot, or network errors.
- By 19:53:06 MSK, a new session for the same UDID and `systemPort=15903` existed, so the helper/session problem recovered transiently; a later failure on this device was `NoSuchElementException`, outside infrastructure diagnosis.
- 19:58:49–19:58:51 MSK: failure cache, archive, and JUnit artifacts were uploaded successfully.

## Zabbix and capacity

- No current problems, interface errors, unsupported items, or missing window metric data across the three Enabled hosts.
- `M-K0058`: ADB stayed `device`; CPU per-core load max 1.1631; agent stayed reachable; root free space remained about 60 GB. Used-memory metric was high (93.1–99.1%, last 98.7%) but no OOM/reboot signal or causal link to the missing IME was found.
- `M-K0057`: separate CPU/load alerts ran 19:52:33–19:58:33 and 19:56:08–19:59:08 MSK; CPU idle reached 0.73%. This host was not the failed Redmi/Appium node. Used-memory metric was also high (up to 99.3%).

## Current Selenium/Grid state

Checked at 2026-08-20 16:59:25 UTC using the same inventory snapshot:

- Selenium 3.141.59 Hub `M-K0056` at `192.168.30.30:4444` was reachable/ready in 90.7 ms.
- 8 total slots, 8 free, 0 busy, 0 queued requests; all 8 proxies still registered.
- Seven Appium endpoints were reachable/ready. `M-K0057:15002` was registered but returned connection refused, so the current Grid verdict was degraded. This is a different host/device from the job's Redmi failure and was observed after job completion.
- Current HTTP/Grid state does not prove historical ADB or UiAutomator2 health.

## Loki coverage

- All three inventory instances existed and had operational journald streams; no result query was truncated.
- Relevant selector: `{instance="M-K0058", unit="phone_redmi_note_13_pro.service"}` around 16:49:30–16:51:00 UTC.
- Overall coverage was marked incomplete because last operational boundary samples stopped roughly 8.5 minutes before the query window end. The decisive job-time slice itself was covered.

## Open items: recommended infrastructure actions

1. Before returning `x4pf5l5haegykni7` to Grid, verify read-only package/IME state (`pm path io.appium.settings`, `ime list -a`) and confirm `io.appium.settings/.UnicodeIME` is registered for user 0.
2. Reinstall/restore the Appium Settings helper using the established preparation mechanism, then validate creation and deletion of a minimal Appium session with `unicodeKeyboard=true`. Roll back by restoring the previously approved helper version if the new helper causes compatibility issues.
3. Make device preparation fail when helper installation or IME registration verification fails; current generic `Success` output produced a false-positive preparation result.
4. Investigate the separate current `M-K0057:15002` connection refusal and remove/fix the stale `emulator_2.service` restart reference. Keep these separate from job 3078215's root cause.
5. Review sustained memory pressure on both Appium hosts and the transient M-K0057 CPU saturation, but do not attribute this job's missing IME to resource pressure without OOM/service evidence.

## Open items: confidence and gaps

Confidence is high for the failed session's device-preparation cause: the job contains the decisive ADB/IME error, Loki correlates the host/unit/UDID and cleanup timestamp, and Zabbix excludes an ADB transport outage. Loki did not retain boundary samples to the full +10-minute end, and project variables are current rather than historical. No mutating validation was performed.

## Portable lesson

none
