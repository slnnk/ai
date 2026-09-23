---
system: android-farm
status: verified
checked: 2026-08-20
tags: [android, android-dig, skill, gitlab, zabbix, loki, selenium-grid]
---
# Global skill `android-dig` — 2026-08-20

## Task and context

- Created a global Codex skill for infrastructure-only diagnosis of YouDo Android autotest jobs from a GitLab job URL.
- Scope: GitLab runner and artifact flow, network/DNS/Nexus, Selenium/Grid, Appium, UiAutomator2, ADB, emulator/device readiness, host/systemd/resources, and device-preparation drift.
- Explicitly excluded from investigation: test assertions, locators, expected data, test implementation, and product business logic, except for briefly classifying them as non-infrastructure failures.

## Changes: files

- Skill entrypoint: `~/ai/current/skills/android-dig/SKILL.md`.
- Operational/API runbook: `~/ai/current/skills/android-dig/references/runbook.md`.
- UI metadata: `~/ai/current/skills/android-dig/agents/openai.yaml`.
- GitLab collector: `~/ai/current/skills/android-dig/scripts/gitlab_job.py`.
- GitLab project-variable collector: `~/ai/current/skills/android-dig/scripts/gitlab_ci_variables.py`.
- Dynamic Zabbix inventory collector: `~/ai/current/skills/android-dig/scripts/zabbix_hosts.py`.
- Inventory-driven Selenium Hub checker: `~/ai/current/skills/android-dig/scripts/selenium_hub.py`.
- Zabbix error/metric collector: `~/ai/current/skills/android-dig/scripts/zabbix_health.py`.
- Loki coverage/log collector: `~/ai/current/skills/android-dig/scripts/loki_logs.py`.

## Data sources and access route

- GitLab: `https://gitlab.youdo.sg`; job metadata and trace via GitLab API v4. Token location: `GITLAB_YOUDO_TOKEN` in `~/ai/current/.env` (value not copied).
- Zabbix: `http://zabbix-selectel.youdo.local/api_jsonrpc.php`; read-only health, events, problems, and item history. Token location: `ZABBIX_PROD_TOKEN` in `~/ai/current/.env` (value not copied).
- Loki: `http://loki-read.yandex-test.youdo.local`; machine logs delivered by Alloy. On 2026-08-20 the user supplied a Grafana Explore example confirming the host label and hub selector `{instance="M-K0056"}`. The skill now starts with `instance=<canonical-machine-name>` and verifies the value for the job window; generic label discovery remains the fallback for schema changes or missing coverage.
- Known test path: GitLab runner → Selenium hub M-K0056 / `192.168.30.30:4444` → Appium on M-K0057 / `192.168.30.148` or M-K0058 / `192.168.30.147` → ADB → Android device/emulator.

## Important behavior

- Default execution is read-only. Diagnosis does not retry/cancel jobs, restart services, reboot devices, kill sessions, mutate device state, or change monitoring.
- Machine logs must be read from Loki, not via SSH, `journalctl`, or direct files.
- The job interval is expanded by 10 minutes on each side and correlated across GitLab, historical/current Zabbix state, and Loki.
- Required verdict classes: confirmed infrastructure failure, probable infrastructure failure, no infrastructure failure found, or insufficient evidence.
- Empty Loki results are not treated as proof of health until stream selection and Alloy ingestion coverage are verified.
- The Loki collector consumes the same fresh Enabled-only `Selenium` inventory, validates the read endpoint, checks exact-window `instance` values and series, separates Falco/security-only streams from operational journals, samples both window boundaries, recursively splits full result pages, and emits only sanitized, locally classified infrastructure events.
- Significant future diagnoses are recorded in `~/ai/current/knowledge/log/YYYY-MM-DD-android-farm-android-dig-job-<job-id>.md`, with secrets and sensitive raw logs excluded.

## Project CI/CD variable collector update (2026-08-20)

- Added read-only `~/ai/current/skills/android-dig/scripts/gitlab_ci_variables.py`.
- Input is the same concrete GitLab autotest job URL used by `gitlab_job.py`; the script derives and validates the project path, confirms the job exists, and retrieves paginated project-level CI/CD variable definitions.
- Output includes key, environment scope, variable type, protected/masked/hidden/raw flags, and a value governed by a diagnostic allowlist. Only Appium/Selenium routing and basic selection values are shown; masked, hidden, file, secret-like, and non-allowlisted values are redacted.
- The workflow and runbook now require comparing project routing variables with job trace clues and the current Enabled Zabbix inventory. Project variables are explicitly not treated as the fully resolved job environment: group, pipeline, schedule, dotenv, runner, and other sources remain outside this collector.
- GitLab returns current project definitions rather than a historical job-time snapshot. The collector and instructions expose this limitation and require trace evidence to win when historical and current values differ.
- Live read-only smoke test against job `3077287` succeeded: five Appium/Selenium variables were selected, four routing values were visible, and the file-valued SSH key was redacted. At 2026-08-20 16:22:03 UTC, current `APPIUM_NODES_1` contained the Zabbix monitoring-side `.31/.32` addresses, while the earlier job trace contained `.147/.148`; this demonstrates why the fetch timestamp and historical limitation are required.

## Selenium Hub live-check update (2026-08-20)

- Added read-only `~/ai/current/skills/android-dig/scripts/selenium_hub.py`.
- The collector consumes the same fresh Enabled-only `Selenium` Zabbix inventory used by the diagnosis, selects exactly one host by the `visible_name` suffix `-selenium-hub`, and derives the Hub IP from its unique main agent interface instead of using a static address.
- It checks port `4444`, tries Selenium 3 `/wd/hub/status` and Selenium 4 `/status` without following redirects, and returns normalized current readiness and latency. Instructions explicitly prevent treating this point-in-time result as historical job health or proof of Appium-node reachability.
- Live read-only smoke test at 2026-08-20 16:27:29 UTC selected `M-K0056-selenium-hub` / technical host `M-K0056` / main Zabbix interface `192.168.30.30`, then received HTTP `200` from `/wd/hub/status` in 98.4 ms. The Hub identified itself as Selenium `3.141.59`, revision `e82be7d358`, with `ready=true` and `Hub has capacity`.
- Device-status extension verified at 2026-08-20 16:38:20 UTC. The collector combined `/grid/api/hub`, `/grid/console`, and one `/grid/api/proxy` request per registration, then queried Appium status concurrently only on node IPs matched to the Enabled Zabbix inventory. Hub reported 8 total/8 free/0 busy slots and no queued new-session requests; the console exposed 8 registered Android proxies, all 8 proxy API lookups succeeded, all 8 mapped to M-K0057/M-K0058 inventory IPs, and all 8 Appium 1.22.3 status endpoints returned ready. Every slot was idle at collection time.
- Direct node checks are SSRF-bounded: a Grid proxy IP absent from the current Enabled inventory is reported and skipped. The output explicitly says that registration and Appium HTTP readiness do not prove ADB or UiAutomator2 health.
- Busy-path regression at 2026-08-20 16:40:36 UTC observed a real active test load: all 8 slots and all 8 named device proxies were busy, every Grid proxy lookup and Appium status check remained healthy, and Hub `/status` returned raw `ready=false` because free capacity was zero. The collector now classifies this combination as `saturated` rather than `not_ready`; it also recovers device IDs for busy slots from `/grid/api/proxy` because the Grid Console omits their capability image while occupied.

## Validation

- Ran `quick_validate.py ~/ai/current/skills/android-dig`.
- Result: `Skill is valid!`.
- Confirmed no scaffold `TODO`/placeholder markers remain.
- On 2026-08-20 the GitLab collector was prepared for job URL input. It validates the destination host before sending `GITLAB_YOUDO_TOKEN`, normalizes job metadata and the diagnostic time window, categorizes sanitized infrastructure trace events, and can write only a sanitized trace with mode `0600`.
- Live validation target: GitLab job `3066275` in `youdo/Test/youdo-android-testing` (job interval 2026-08-14 13:40:31–14:05:02 MSK; runner `gitlab-runner-docker-1 integrations-tests (172.28.0.171)`).
- Full metadata+trace test passed with the host Python 3.8.10. High-confidence filters extracted missing device-preparation helpers and repeated Appium/ADB IME session-creation failures without classifying ordinary capabilities, test assertions, successful TLS handshakes, or artifact archiving as infrastructure errors.

## Open items

- The host label is confirmed as `instance` for M-K0056. On the first real Appium-host diagnosis, verify that M-K0057 and M-K0058 use the same canonical instance values and document any available systemd unit label.

## Dynamic node scope update — 2026-08-20

- User clarified that Selenium nodes can change. `android-dig` must begin by resolving the exact Zabbix host group `Selenium` and selecting only hosts with Zabbix host status `Enabled` (`status=0`).
- Static notes, GitLab trace addresses, and Loki labels are not allowed to add nodes to the current diagnostic scope.
- Live Zabbix check returned group `Selenium`, groupid `61`, and Enabled technical hosts `M-K0056`, `M-K0057`, and `M-K0058`; all three main agent interfaces reported `available=1` at check time.
- Zabbix interface IPs were `192.168.30.30`, `.31`, and `.32`. The latter two differ from historical Appium/SSH addresses `.148` and `.147`; therefore the technical hostname is the canonical join key and IPs remain source-specific.
- The health collector consumes that exact fresh inventory snapshot, queries only its hostids, and returns current/historical errors plus summarized core/ADB metrics for a supplied job correlation window. It does not emit raw history rows by default.

## Loki collector update — 2026-08-20

- Added read-only `scripts/loki_logs.py`; default endpoint is `http://loki-read.yandex-test.youdo.local`, with no Loki credential required at verification time.
- Confirmed API routes: `label/instance/values`, `series`, and `query_range`. Confirmed useful labels: `instance`, `job`, `service_name`, `unit`, and `filename`.
- Default event search covers host resources/systemd, network/dependencies, Selenium/Grid, Appium/UiAutomator2, ADB/USB, and emulator failures. Broad Loki candidates are reclassified locally; known Falco service noise is omitted.
- Coverage is false unless every inventory host has operational streams, first/last samples are within the configured boundary-gap threshold, and no event query was truncated. `instance_absent` and `security_only` are explicit gaps.
- Live current-window validation found operational journald streams for M-K0056, M-K0057, and M-K0058 and boundary coverage for all three. Historical job 3066275 validation found M-K0056/M-K0057 absent and only a Falco stream for M-K0058, correctly producing incomplete coverage and no fabricated health claim.
- Tests passed under Python 3.8: help/syntax, live historical and current Loki requests, disallowed endpoint rejection, stale inventory rejection, and `quick_validate.py` (`Skill is valid!`).

## Portable lesson

none
