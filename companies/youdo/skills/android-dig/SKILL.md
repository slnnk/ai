---
name: android-dig
description: Diagnose infrastructure failures in YouDo Android autotest GitLab jobs by correlating the job trace with Zabbix health and Alloy-delivered machine logs in Loki. Use when given a GitLab job URL and the requested scope is CI, runner, network, Selenium/Grid, Appium, ADB, emulator/device, host, artifact delivery, or other test-infrastructure health; do not investigate assertion, locator, test-data, or product-code defects beyond separating them from infrastructure.
---

# Android infrastructure diagnosis

Accept a GitLab Android-autotest job URL as the primary input and produce an evidence-backed infrastructure verdict. Stay read-only unless the user separately authorizes remediation.

Before making API calls, read [references/runbook.md](references/runbook.md). It contains the current system map, API routes, Loki label-discovery procedure, signal matrix, and report contract.

## Scope boundary

Investigate:

- GitLab runner/executor, checkout, cache, dependency resolution, job timeout, artifacts, and report publication;
- DNS, routing, TLS, Nexus/download failures, registry, and other service dependencies;
- Selenium/Grid availability, queueing, session routing, and abandoned sessions;
- Appium service/session creation, UiAutomator2, `systemPort`, helper packages, and proxy timeouts;
- ADB transport, device `offline`/`unauthorized`, USB resets, emulator boot, host resources, OOM, disk, and systemd failures;
- device preparation drift and OS overlays when they prevent the application from being exercised.

Do not debug or propose fixes for test assertions, locators, stale expected values, test data, or application business behavior. Mention such failures only as excluded evidence needed to explain why they are not infrastructure failures.

## Required workflow

1. Validate and parse the URL. Require a concrete `/-/jobs/<id>` URL, derive the GitLab origin and URL-encoded project path, and reject unrelated hosts unless the user explicitly broadens scope.
2. Load access variables from `~/ai/current/.env` without printing their values. Use `GITLAB_YOUDO_TOKEN` for GitLab and `ZABBIX_PROD_TOKEN` for Zabbix. If a required credential is absent, report exactly which variable is missing and continue with all sources that remain available.
3. Before inspecting the job, obtain the current node inventory with `scripts/zabbix_hosts.py --group Selenium --pretty`. The authoritative scope is only hosts returned by Zabbix with host status `Enabled`; do not build the node list from hard-coded names, historical notes, GitLab variables, or Loki label values. Preserve the inventory fetch timestamp. If the group is missing, empty, or unavailable, report the inventory gap and do not silently substitute the historical map.
4. Check the current Selenium Hub and its registered devices with the same inventory snapshot: `scripts/selenium_hub.py --inventory <snapshot-or-stdin> --pretty`. The script must select exactly one Enabled host whose Zabbix `visible_name` ends in `-selenium-hub`, derive the HTTP address from that host's main agent-interface IP, and probe port `4444`; never hard-code the Hub IP. For Selenium 3, collect Hub slot totals, registered device/proxy identities, point-in-time idle/busy state, per-proxy registration status, and direct Appium status only for node IPs present in the current Enabled inventory. Interpret `ready=false` with all known slots busy as `saturated`, not as an unhealthy Hub. Treat all results as current evidence only; Hub/Appium status does not prove historical job health, ADB transport, or UiAutomator2 command health.
5. Fetch and normalize GitLab metadata and trace with `scripts/gitlab_job.py <job-url> --pretty`. Use its correlation window, CI context, host clues, devices, and sanitized infrastructure events as the initial evidence set. Request `--sanitized-trace-output <temporary-path>` only when the summarized events are insufficient, and delete that temporary file after analysis. Establish runner, status, stage, pipeline, ref/SHA, preparation results, final upload state, device/UDID/Appium/Grid clues, and every infrastructure-signature timestamp. Preserve the timezone supplied by GitLab and use the script's UTC/Moscow normalization.
6. Fetch project-level CI/CD variables for the repository derived from the same job URL with `scripts/gitlab_ci_variables.py <job-url> --pretty`. Use diagnostic routing values such as `APPIUM_NODES_*` and `SELENIUM_SERVER_*` to reconcile the job's configured endpoints with inventory and trace clues. Treat the returned definitions as current at fetch time, not as a historical snapshot for the job; prefer trace evidence when the values differ. Treat environment scopes separately and report that group, pipeline, schedule, dotenv, runner, and other non-project sources are not covered. Never bypass the script's value-redaction policy or copy secret values into reports or notes.
7. Define the correlation window as job start minus 10 minutes through job finish plus 10 minutes. If the job is still running, use the current time as the end. Preserve both UTC and Europe/Moscow time in the final timeline.
8. Identify implicated components by intersecting job clues and project-variable routing values with the Enabled Selenium inventory. Use the Zabbix technical host name as the canonical machine identifier and Loki `instance` value. Treat Zabbix interface IPs, Appium/SSH addresses, and historical map addresses as source-specific attributes; never assume they are interchangeable. Mention trace or variable clues outside the current Enabled inventory as out-of-scope evidence rather than adding those machines to the diagnosis.
9. Pipe the same inventory snapshot into `scripts/zabbix_health.py --inventory - --start <query_start_epoch_seconds> --end <query_end_epoch_seconds> --pretty`. Use its interface errors, unsupported items, current/overlapping problems, exact-window trigger transitions, and metric summaries for the Enabled hosts. Check ADB status histories where present. A healthy current value does not disprove a historical outage, and absent history must be reported using the script's coverage fields.
10. Pipe the same inventory snapshot into `scripts/loki_logs.py --inventory - --start <query_start_epoch_seconds> --end <query_end_epoch_seconds> --pretty`. It checks exact-window `instance` values and streams, distinguishes operational logs from Falco/security-only coverage, samples ingestion boundaries, splits result-limited queries, sanitizes log lines, and emits categorized infrastructure events. Treat `instance_absent`, `security_only`, missing boundary samples, or truncation as coverage gaps, not healthy evidence. Use manual label discovery from the runbook only if the script reports an API/schema mismatch. Machine logs must come exclusively from Loki; do not use SSH, `journalctl`, or direct host files as a substitute.
11. Correlate sources by timestamp and causality. Prefer a chain such as job symptom → configured project variable → Hub/Grid state → matching Loki event → Zabbix state/change. Distinguish confirmed facts, likely explanations, and gaps. Never infer that silence in Loki proves health until label coverage and ingestion for the host/window are verified.
12. Return the report contract from the runbook. Keep excluded test-code/product failures short. Recommend infrastructure checks or remediation, but do not retry/cancel jobs, restart services, reboot devices, kill sessions, run mutating ADB commands, or change Zabbix without explicit authorization.
13. Record significant findings in `~/ai/current/knowledge/log/YYYY-MM-DD-android-farm-dig-job-<id>.md`; update the Android system map only for stable, newly verified facts. Never persist secrets or raw logs containing credentials, cookies, tokens, private URLs, or sensitive test payloads.

## Evidence standard

Use one of these verdicts:

- **Confirmed infrastructure failure** — direct infrastructure error in the job plus corroboration, or an independently decisive infrastructure signal.
- **Probable infrastructure failure** — strong correlated evidence with one source missing or ambiguous.
- **No infrastructure failure found** — checked sources cover the relevant interval and show a healthy execution path; failures are outside this skill's scope.
- **Insufficient evidence** — access, retention, label coverage, or timestamps prevent a reliable conclusion.

Do not call an assertion or element lookup an infrastructure failure merely because it ran on a device. Conversely, treat session creation, transport, host, device readiness, system UI state, and artifact-delivery failures as infrastructure when supported by evidence.
