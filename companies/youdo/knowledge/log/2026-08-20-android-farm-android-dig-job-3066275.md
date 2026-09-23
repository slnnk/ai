---
system: android-farm
status: verified
checked: 2026-08-20
tags: [android, android-dig, gitlab-ci, zabbix, loki, appium, job-3066275]
---
# Android-dig: GitLab job 3066275 — GitLab source pass

## Task

Diagnose GitLab autotest job `3066275` for infrastructure failures using the new `android-dig` collectors (GitLab trace, Zabbix, Loki).

## Context

- Checked: 2026-08-20, Europe/Moscow.
- Job: `https://gitlab.youdo.sg/youdo/Test/youdo-android-testing/-/jobs/3066275`.
- Scope completed: GitLab metadata/trace, dynamic Enabled inventory, Zabbix errors/metrics, and Loki coverage/log collection. Loki retention/ingestion did not provide operational machine logs for the historical interval, so a complete three-source causal confirmation is not possible.

## Job metadata

- Project: `youdo/Test/youdo-android-testing`.
- Status/reason: `failed` / `script_failure`.
- Ref/SHA: `Test-7058`, `39abaea81de6bcf39fc9b3d737bbb401e5dd7eb5`.
- Job interval: 2026-08-14 13:40:31–14:05:02 MSK (10:40:31–11:05:02 UTC).
- Diagnostic correlation window: 2026-08-14 10:30:31–11:15:02 UTC.
- Runner: `gitlab-runner-docker-1 integrations-tests (172.28.0.171)`; GitLab reported it online at the 2026-08-20 query time, which does not establish its historical state during the job.
- CI context: logical `JOB_ID=1`, stand `test9`, suite `[Упавшие тесты]`, source failed job `3066274`, failed pipeline `136763`.
- Trace size: 8,579,251 bytes / 58,065 lines.

## Infrastructure evidence from the trace

- Device preparation printed `/opt/adb/adb_pkg.sh: No such file or directory` twice, consistent with the preparation loop reaching both Appium hosts while errors remain masked by the CI `|| true` behavior.
- At 13:43:19 MSK and again at 14:04:46 MSK, session creation failed for Xiaomi/Redmi UDID `x4pf5l5haegykni7`: Appium's ADB command could not enable `io.appium.settings/.UnicodeIME` because Android reported `Unknown input method`. The maintained farm map places this device on M-K0058 / `192.168.30.147`.
- The collector found no high-confidence runner-system, network/dependency, or artifact-upload error signature after filters were tuned against the real trace. This is only trace evidence, not proof that those layers were healthy.
- Device capabilities were normalized separately from errors for six devices, including UDID/model/platform/systemPort. This prevents ordinary capability dumps from being misclassified as Appium failures.

## Changes: collector created and verified

- Path: `~/ai/current/skills/android-dig/scripts/gitlab_job.py`.
- Accepts a GitLab job URL and uses GitLab API v4 metadata and trace endpoints.
- Reads `GITLAB_YOUDO_TOKEN` from the environment or `~/ai/current/.env`; validates the destination hostname before loading/sending it.
- Emits normalized JSON: job, runner, UTC/MSK times, exact epoch seconds/nanoseconds, CI context, host clues, devices, signal counts, and sanitized matching events.
- Optional full trace output is sanitized, written with mode `0600`, and must be treated as sensitive because arbitrary test payloads may remain even after credential redaction.
- Live metadata+trace pass succeeded on job 3066275 under Python 3.8.10.
- Temporary sanitized-trace mode was verified at `0600`; the test file was removed afterward.
- Negative checks passed: an unapproved host and a missing token both stop with exit code 2 before an API request.
- Global skill validation: `Skill is valid!`.

## Zabbix correlation added on 2026-08-20

- Fresh inventory was obtained from the exact `Selenium` group with host status `Enabled`; the queried hostids were M-K0056 `10590`, M-K0057 `10588`, and M-K0058 `10589`.
- Health query used the GitLab-derived correlation window 2026-08-14 10:30:31–11:15:02 UTC.
- Zabbix recorded a High trigger on M-K0057: `CPU idle time is less than 20% for over 10 minutes` at 10:59:08 UTC, recovered at 11:05:08 UTC. In-window CPU idle reached 0.9327%, and per-core one-minute load reached 2.8063.
- M-K0058 also experienced load during the window (CPU idle minimum 11.7928%, per-core one-minute load maximum 1.6021) but had no trigger transition in the queried interval.
- M-K0056 remained lightly loaded in the sampled metrics (CPU idle minimum 98.1016%).
- Every discovered physical-device status item remained `device` throughout the window. In particular, `adb_dev.status[x4pf5l5haegykni7]` had 22 samples, all `device`; this argues against an ADB offline/unauthorized transport failure and is consistent with the narrower Appium helper/IME registration error seen in the job trace.
- At query time there were no current Zabbix problems, unavailable inventory interfaces, or unsupported monitored items for the three hosts.
- The collector selected 46 metrics, had history for every selected item, and reported no result truncation for value types 0, 3, or 4.
- Collector: `~/ai/current/skills/android-dig/scripts/zabbix_health.py`; it consumes a fresh `zabbix_hosts.py` snapshot and summarizes history rather than persisting raw samples.

## Loki correlation added on 2026-08-20

- Query window: 2026-08-14 10:30:31–11:15:02 UTC, taken from the GitLab collector.
- The fresh Enabled inventory contained M-K0056, M-K0057, and M-K0058. Exact-window Loki `instance` values contained only M-K0058.
- M-K0056 and M-K0057 had status `instance_absent`. M-K0058 had one stream only: Falco security events (`job=integrations/security`, `filename=/var/log/falco/events.json`), so its status was `security_only`.
- There were no operational Appium/ADB/systemd streams or boundary samples for the window. This is an explicit Loki coverage gap, not evidence of machine health and not evidence against the GitLab/Zabbix findings.
- Collector: `~/ai/current/skills/android-dig/scripts/loki_logs.py`. A separate current 15-minute validation found operational Alloy journald streams and boundary coverage for all three current hosts, which confirms the query/schema implementation while not repairing historical coverage.

## Findings: current evidence assessment

- GitLab directly shows infrastructure preparation/helper failures for M-K0058's device path, while Zabbix shows the affected UDID remained connected and M-K0058 was loaded but without a matching trigger. This narrows the likely cause to Appium helper/IME/device-preparation state rather than ADB transport loss.
- Loki cannot corroborate the historical causal chain because operational streams are absent. Any final verdict must state this gap; the available GitLab evidence remains direct, but the requested three-source confirmation is unavailable.

## Portable lesson

none
