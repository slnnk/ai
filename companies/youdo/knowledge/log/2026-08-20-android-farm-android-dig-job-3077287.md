---
system: android-farm
status: verified
checked: 2026-08-20
tags: [android, android-dig, gitlab-ci, selenium-grid, appium, network, job-3077287]
---
# Android infrastructure diagnosis: GitLab job 3077287

## Task

Read-only infrastructure diagnosis of GitLab autotest job `3077287` (`No route to host` towards the configured Appium nodes).

## Context

- Date: 2026-08-20 (Europe/Moscow)
- Job: `https://gitlab.youdo.sg/youdo/Test/youdo-android-testing/-/jobs/3077287`
- Project: `youdo/Test/youdo-android-testing`
- Scope: read-only GitLab trace, current Enabled Selenium inventory, historical Zabbix health, and Alloy-delivered Loki logs.
- Verdict: **Confirmed infrastructure failure** — CI preparation and Selenium Grid could not reach the configured Appium/SSH addresses `192.168.30.147` and `192.168.30.148` (`No route to host`). The exact lower-level cause is narrowed to stale/mismatched Appium addresses or missing routing to those source-specific addresses; available read-only evidence does not distinguish them.

## Job context

- Pipeline `137053`, job `autotests`, stage `tests`, status `failed`, failure reason `script_failure`.
- Ref `master`, commit `38f5a58f56ec3792344de1b2ceac1b9ae0c57d20` (`update ci`).
- Runner `gitlab-runner-docker-1 integrations-tests (172.28.0.171)`, runner ID `108`, online at collection time.
- Parameters: `JOB_ID=1`, `STAND=test8`, `SUITE=[СБР]`, application `4.0.267.feature-and-4660-flex-form-date (136597)`.
- Runtime: 2026-08-20 15:41:47–15:45:00 UTC / 18:41:47–18:45:00 MSK. Correlation window: 15:31:47–15:55:00 UTC / 18:31:47–18:55:00 MSK.

## Findings: evidence and timeline

- 15:42:16–15:43:04 UTC / 18:42:16–18:43:04 MSK: CI preparation attempted SSH-based emulator/device preparation through `APPIUM_NODES`. Both `192.168.30.147:22` and `192.168.30.148:22` repeatedly returned `No route to host`. The preparation continued, so the error was not made fatal.
- 15:43:04 UTC / 18:43:04 MSK: Gradle/TestNG execution started against the configured Selenium server.
- 15:44:19–15:44:47 UTC / 18:44:19–18:44:47 MSK: ten suite tests failed while creating remote sessions. Selenium reported `SessionNotCreatedException` and `Error forwarding the request No route to host (Host unreachable)`.
- 15:44:48 UTC / 18:44:48 MSK: Gradle reported failing tests. The generated report counted 10 errors; all observed failures share the session-routing infrastructure cause, so no separate assertion/product failure was identified.
- 15:44:52–15:44:59 UTC / 18:44:52–18:44:59 MSK: report upload to object storage and GitLab archive/JUnit artifact uploads completed successfully (`201 Created`). The final job failure was therefore not artifact delivery.

## Current inventory and Zabbix

- Inventory snapshot fetched 2026-08-20 16:06:57 UTC / 19:06:57 MSK from Enabled hosts in Zabbix group `Selenium`: `M-K0056`, `M-K0057`, `M-K0058`; no maintenance and all agent interfaces currently available.
- Current Zabbix monitoring interfaces: M-K0056 `192.168.30.30`, M-K0057 `192.168.30.31`, M-K0058 `192.168.30.32`. These are not assumed interchangeable with the job's Appium/SSH addresses `.148` and `.147`.
- For the exact correlation window all three hosts had continuous `agent.ping=1`; no interface errors, current/overlapping problems, trigger transitions, unsupported selected items, uptime resets, disk exhaustion, CPU saturation, or interface error/drop counters were found.
- M-K0057 ADB items `5b2d4fe2` and `RZCY20AXJHN` remained `device` for all 12 samples. M-K0058 ADB items `15888255AE004773`, `RZ8R71ZRK8H`, and `x4pf5l5haegykni7` remained `device` for all 12 samples.
- M-K0057/M-K0058 memory usage was consistently high (about 98.8%/98.5%), but CPU remained about 98.6%/99.0% idle, iowait was low, no OOM/reboot/trigger signal appeared, and this does not explain simultaneous `No route to host` from CI/Grid.

## Loki

- Queried operational streams for `{instance="M-K0056"}`, `{instance="M-K0057"}`, and `{instance="M-K0058"}` over 15:31:47–15:55:00 UTC, excluding security-only streams.
- All three hosts had operational journald streams, boundary samples were within the accepted five-minute gap, no query was truncated, and collector coverage was complete.
- No categorized Appium/ADB/Grid/network failure was present in the available machine streams. A narrower search for route failure, link/carrier/DHCP/address changes, Appium, Selenium, and connection refusal also returned no candidates.
- The available stream set was generic journald/cron/init/VNC rather than explicit Appium units. Thus Loki corroborates that hosts were emitting logs but does not prove Appium service health or explain why the runner/Grid could not route to `.147/.148`.

## Findings: cause, impact, and recovery state

- Confirmed failed layer: network reachability/session routing from the GitLab runner and Selenium Grid toward both configured Appium node addresses.
- Probable configuration dimension: the job targets historical Appium/SSH IPs `.147/.148`, while current Zabbix monitoring interfaces are `.32/.31`. This is evidence of address-role mismatch, not proof that those historical addresses must be removed; they may be valid secondary/source-specific addresses when routing works.
- Blast radius: logical pool `JOB_ID=1` and all 10 parallel `[СБР]` session attempts in this job. Evidence is insufficient to claim all pools or all users were affected.
- Current state: Zabbix agents and monitored ADB transports are healthy after the job. End-to-end recovery of runner/Grid-to-Appium connectivity has not been verified.

## Open items: recommended next actions

1. From the runner network and from M-K0056, perform read-only route/TCP checks to the configured `.147/.148` SSH and Appium ports; compare with `.31/.32` without changing configuration.
2. Resolve `APPIUM_NODES_1` and Grid node registrations to their intended host/interface ownership. If `.147/.148` are stale, update both CI variables and Grid registrations together; retain the old values for rollback until a canary passes.
3. If `.147/.148` remain intended secondary addresses, restore the route/VLAN/firewall path and verify SSH plus Appium `/status` from the actual runner/Grid sources.
4. Make device-preparation reachability failures fatal instead of continuing into a guaranteed ten-test failure; stage this CI change and retain an easy revert.
5. Run a small session-creation canary before retrying the full suite. Validate Grid registration, Appium session creation, one UiAutomator2 command, and report publication.
6. Separately review the persistent high memory percentage on M-K0057/M-K0058, including available memory and swap, but do not treat it as this incident's cause without an OOM/service signal.

## Open items: gaps

- No runner-side routing table, Grid node registry snapshot, or Appium unit logs were available from the permitted read-only sources.
- Zabbix interface IPs are monitoring attributes and do not establish whether `.147/.148` should exist as secondary Appium/SSH addresses.
- Follow-up at 2026-08-20 16:22:03 UTC used the new read-only project-variable collector. Current `APPIUM_NODES_1` was `.31 .32`, whereas the job-time trace had `.147 .148`. This confirms that the project definition changed or another variable source supplied the historical values, but the project-variable API provides no historical snapshot to distinguish those cases.
- No infrastructure state was changed and the failed job was not retried.

## Portable lesson

none
