# Android-dig runbook

Last verified context: 2026-08-20, Europe/Moscow. Loki read endpoint updated from user-provided configuration on 2026-09-08; the Loki host selector was confirmed from Grafana Explore supplied by the user.

## Dynamic inventory requirement

Before GitLab trace analysis or Loki selection, run:

```bash
python3 scripts/zabbix_hosts.py --group Selenium --pretty
```

The output includes only Zabbix hosts whose host status is `Enabled` (`status=0`). Its `hosts[].technical_name` values are the canonical machine identifiers and the initial Loki `instance` values. Use only these hosts as the node scope. Preserve `source.fetched_at_utc` because this is a current inventory snapshot, not proof of group membership at the historical job time.

Do not substitute the static map when Zabbix is unavailable or the group is empty. A hostname or IP found only in a job trace, Loki, or old note does not expand scope; record it as an out-of-inventory clue. Zabbix monitoring interface IPs may differ from Appium, SSH, NAT, or historical addresses, so correlate primarily by `technical_name` and treat each IP with its source.

## Selenium Hub live check

Use the exact fresh inventory snapshot to locate and check the current Hub:

```bash
python3 scripts/zabbix_hosts.py --group Selenium \
  | python3 scripts/selenium_hub.py --inventory - --pretty
```

`selenium_hub.py` accepts only a fresh Enabled-only `Selenium` inventory. It selects exactly one host whose Zabbix `visible_name` ends case-insensitively in `-selenium-hub`, chooses its unique main agent-interface IP, and builds `http://<inventory-ip>:4444`. Do not supply a historical or hard-coded Hub address when an inventory snapshot is available.

The collector tries Selenium 3 `/wd/hub/status` first and Selenium 4 `/status` second, follows no redirects, emits response latency and normalized ready/build/node fields, and treats transport errors or unrecognized responses as evidence rather than collector failures.

For Selenium 3, it also combines three Hub sources:

- `/grid/api/hub` — total/free/busy slot counts and queued new-session requests;
- `/grid/console` — registered proxy IDs, device identifiers, Android versions, and point-in-time idle/busy classes;
- `/grid/api/proxy?id=<proxy-url>` — confirmation that each proxy remains registered.

For each registered proxy whose IP belongs to a current Enabled non-Hub Zabbix host, the collector checks the Appium `/wd/hub/status` or `/status` endpoint on the registered port. It skips direct requests to proxy IPs outside that inventory and reports a coverage gap instead of trusting Grid-supplied addresses as arbitrary HTTP targets. Checks run concurrently with bounded `--workers` and `--max-devices` limits.

Interpret the layers separately: Hub `ready`, registration, idle/busy, and Appium HTTP status are useful current signals, but none proves job-window health, ADB transport, device readiness, UiAutomator2 instrumentation, or successful command execution. Compare device identifiers with Zabbix ADB histories for the job window.

Selenium 3 reports `ready=false` when no slot is free even if the Hub and every registered node are functioning. When `/grid/api/hub` reports a positive total with `free=0`, classify this state as `saturated`; preserve the raw status verdict separately. Do not label capacity exhaustion as a Hub outage. Compare console busy counts with Hub busy-slot totals; a mismatch can be a collection-time race and is reported as an inconsistent snapshot rather than silently choosing one source.

## Historical system map

Execution route:

```text
GitLab test runner
  -> Selenium Grid hub M-K0056 (192.168.30.30:4444)
  -> Appium node on M-K0057 or M-K0058
  -> ADB
  -> emulator or physical Android device
```

- GitLab: `https://gitlab.youdo.sg`; Android autotest project is normally `youdo/Test/youdo-android-testing` (project ID 69).
- Zabbix API/panel: `http://zabbix-selectel.youdo.local`; token variable: `ZABBIX_PROD_TOKEN`.
- Loki read endpoint: `http://loki.dev.youdo.corp`; host logs arrive through Alloy.
- Selenium hub: Zabbix host `M-K0056-selenium-hub`, machine `M-K0056`, IP `192.168.30.30`.
- Appium host `M-K0058`, IP `192.168.30.147`: Android 10 emulator, TECNO CM7 Android 16, Samsung A12 Android 11, Redmi Note 13 Pro Android 13.
- Appium host `M-K0057`, IP `192.168.30.148`: two Android 10 emulators, Redmi Note 14 Pro Android 14, Samsung A55 Android 14.
- USB device `GHKBB23B15002735` on M-K0057 is outside the Android Appium farm and must not be diagnosed as part of it.
- Appium is managed by systemd; ports are generally `15001`–`15004`, with distinct UiAutomator2 `systemPort` values.
- CI selects pools through `JOB_ID`, `SELENIUM_SERVER_<JOB_ID>`, and `APPIUM_NODES_<JOB_ID>`. Preparation restarts emulator services and calls `/opt/adb/adb.sh` and `/opt/adb/adb_pkg.sh`; historical CI used `|| true`, so preparation errors can be masked.
- APKs are normally downloaded from Nexus `nexus.youdo.com/repository/raw/android/` during session creation.

This map is historical context only. Never use it to construct the current node list; the Enabled hosts returned from the Zabbix `Selenium` group are authoritative. Reconcile supporting roles and addresses with job evidence, Zabbix, Loki, and `~/ai/current/knowledge/youdo-android-testing/system-map.md`.

## GitLab collection

Use the bundled read-only collector:

```bash
python3 scripts/gitlab_job.py 'https://gitlab.youdo.sg/<namespace>/<project>/-/jobs/<job_id>' --pretty
```

The script validates the host before sending `GITLAB_YOUDO_TOKEN`, reads that variable from the process environment or `~/ai/current/.env`, fetches metadata and trace, calculates the ±10-minute correlation window, extracts safe CI context and host clues, and emits categorized sanitized infrastructure events as JSON. It never emits the token or an unsanitized trace.

When signal extraction is not enough, use a temporary destination:

```bash
python3 scripts/gitlab_job.py '<job-url>' --pretty --sanitized-trace-output /tmp/android-dig-<job-id>.trace
```

The trace is redacted and created with mode `0600`; still treat it as sensitive and delete it after the diagnosis. Use `--metadata-only` when trace access is unnecessary. Run `python3 scripts/gitlab_job.py --help` for CA, timeout, size, token-variable, and allowed-host controls.

Internally, the script parses URLs shaped like `https://gitlab.youdo.sg/<namespace>/<project>/-/jobs/<job_id>`, percent-encodes the project path, and uses:

```text
GET /api/v4/projects/<encoded-project-path>/jobs/<job_id>
GET /api/v4/projects/<encoded-project-path>/jobs/<job_id>/trace
```

If useful, inspect pipeline jobs and artifacts through the corresponding read-only GitLab v4 endpoints. Do not expose token-bearing headers or credential-bearing capability URLs.

Extract job start/end, duration, queued duration, timeout/cancel/runner-system-failure state, runner, visible CI selection variables, ref/SHA, failed preparation, dependency/network errors, session IDs, Appium URL/port, device/model/UDID, Grid node, and artifact/report upload result.

After fetching the job, read the project-level CI/CD variable definitions for the repository derived from the same job URL:

```bash
python3 scripts/gitlab_ci_variables.py '<job-url>' --pretty
```

Use `--key-regex '^APPIUM_NODES_|^SELENIUM_SERVER_'` when only routing variables are needed. The collector validates the job URL and GitLab host, confirms the job exists, follows GitLab pagination, and reads:

```text
GET /api/v4/projects/<encoded-project-path>/jobs/<job_id>
GET /api/v4/projects/<encoded-project-path>/variables?per_page=100&page=<n>
```

It emits variable keys, environment scopes, types, and protection/masking flags. Values are visible only for the diagnostic routing allowlist (`APPIUM_NODES*`, `SELENIUM_SERVER*`, `JOB_ID`, `STAND`, `SUITE`, and `EMULATORS`); masked, hidden, file, secret-like, and other values are redacted. Do not weaken this policy during diagnosis.

These endpoints return the current project-level definitions, not a historical snapshot from the job start and not the fully resolved variables available to a particular job. When current values disagree with values evidenced in the trace, preserve both timestamps and use the trace as the job-time fact. Group, instance, pipeline, trigger, schedule, dotenv, and runner variables may override or supplement project definitions. Keep duplicate keys with different environment scopes distinct, compare the scope to the job environment when available, and report unresolved precedence as an evidence gap.

Useful trace signatures include `runner_system_failure`, `no space left`, `i/o timeout`, `connection refused`, `connection reset`, `timed out`, `EAI_AGAIN`, `NXDOMAIN`, `SessionNotCreatedException`, `Could not proxy command`, `UiAutomator2`, `instrumentation`, `adb`, `offline`, `unauthorized`, `device not found`, `systemPort`, `socket hang up`, `502`, `503`, `504`, missing preparation scripts, and artifact upload failures.

## Zabbix checks

Use JSON-RPC at `POST http://zabbix-selectel.youdo.local/api_jsonrpc.php` with `Authorization: Bearer $ZABBIX_PROD_TOKEN` and `Content-Type: application/json-rpc`.

`scripts/zabbix_hosts.py` first resolves the exact `Selenium` group through `hostgroup.get`, then calls `host.get` with that `groupid` and `filter.status=0`. It normalizes host names, maintenance state, agent-interface availability/errors, and provides `loki_instances`. The script validates the endpoint host before sending the token and reads `ZABBIX_PROD_TOKEN` from the process environment or `~/ai/current/.env`.

Use the exact fresh inventory snapshot for health collection:

```bash
python3 scripts/zabbix_hosts.py --group Selenium \
  | python3 scripts/zabbix_health.py --inventory - \
      --start <query_start_epoch_seconds> \
      --end <query_end_epoch_seconds> \
      --pretty
```

`zabbix_health.py` rejects non-Enabled, wrong-group, empty, duplicate, or stale inventory. It collects:

- current interface failures and unsupported item errors;
- unresolved problems, recently resolved problems overlapping the window within a documented lookback, and exact-window problem/recovery trigger transitions;
- dynamically discovered core metrics: agent ping, CPU load/idle/iowait, memory usage, root filesystem free space, uptime/reboots, physical-interface errors/drops, and every `adb_dev.status[UDID]` item;
- per-item first/last/min/max/average, sample count and maximum sample gap; ADB value transitions; uptime resets; hourly trend fallback when raw numeric history is absent.

The script summarizes samples rather than emitting the complete history. Extend item selection only when needed with repeated `--include-key-regex`; use `--include-loopback` only when loopback diagnostics matter. The default metric window is limited to 24 hours and the inventory must be no more than 15 minutes old.

Both bundled Zabbix scripts use read-only calls only. The health collector uses `event.get`, `problem.get`, `item.get`, `history.get`, and `trend.get` against hostids from the supplied Enabled inventory.

Check CPU/load, memory, disk/inodes, network, agent availability, process/service state, and ADB discovery/device status where items exist. Use epoch seconds for filters. Do not assume identical item names across hosts. The hub had only generic Linux monitoring at last verification; absence of a Grid trigger is not proof that Grid was healthy.

Report job-window and current state separately. Mark `current healthy, historical state unknown` when retention or item coverage is insufficient.

## Loki label discovery and queries

Base URL: `http://loki.dev.youdo.corp`. Use:

```bash
python3 scripts/zabbix_hosts.py --group Selenium \
  | python3 scripts/loki_logs.py --inventory - \
      --start <query_start_epoch_seconds> \
      --end <query_end_epoch_seconds> \
      --pretty
```

`loki_logs.py` validates a fresh Enabled-only `Selenium` inventory and the Loki origin before making requests. It queries exact-window `instance` values and stream series, excludes the known `integrations/security`/Falco stream from operational evidence, samples the first and last operational entry, and searches for infrastructure candidates. Full result pages are recursively split by time; categorized lines are sanitized and capped. Read `coverage.<host>.status`, boundary samples, and `event_query_truncated` before interpreting silence. The default window limit is 24 hours and inventory freshness is 15 minutes. No Loki credential is currently required or stored.

For manual schema investigation, the collector uses these read-only routes:

```text
GET /loki/api/v1/labels?start=<ns>&end=<ns>
GET /loki/api/v1/label/<label>/values?start=<ns>&end=<ns>
GET /loki/api/v1/series?match[]=<urlencoded-selector>&start=<ns>&end=<ns>
GET /loki/api/v1/query_range?query=<urlencoded-logql>&start=<ns>&end=<ns>&direction=forward&limit=<n>
```

The confirmed Alloy host label is `instance`. Grafana Explore returns logs for the Selenium hub with:

```logql
{instance="M-K0056"}
```

Use the corresponding canonical machine name as the first selector for other farm hosts, for example `{instance="M-K0057"}` or `{instance="M-K0058"}`, but verify that the value exists for the exact job interval before relying on an empty result.

Query `GET /loki/api/v1/label/instance/values?start=<ns>&end=<ns>` first. If the expected instance value is absent, list labels for the interval and inspect common Alloy alternatives such as `host`, `hostname`, `nodename`, `service_name`, `unit`, `systemd_unit`, `job`, and `filename`. This fallback protects against renamed machines, retention gaps, or an Alloy label-schema change.

At verification on 2026-08-20 for GitLab job 3066275's interval, Loki exposed labels including `instance`, `job`, `service_name`, `unit`, and `filename`. Of the current Enabled hosts, only `M-K0058` had an `instance` value, and its sole stream was Falco (`job=integrations/security`, `filename=/var/log/falco/events.json`). This is a historical-window coverage gap, not evidence that the farm was healthy. Re-query for every job because nodes and streams change.

Build the narrowest supported selector. Start with the exact host and add a service/unit label only when that label has been confirmed, for example:

```logql
{instance="M-K0058", systemd_unit=~"phone_.*|emulator_.*|appium.*"}
```

For a farm-wide correlation, use `{instance=~"M-K0056|M-K0057|M-K0058"}` and then narrow by unit or line pattern. If `instance` is unavailable, use another discovered selective stream label plus a line filter for hostname/IP; do not start with an unbounded all-stream query. URL-encode LogQL.

Query in layers:

1. Verify ingestion with a small unfiltered sample from selected host streams around job start, middle, and end.
2. Query implicated systemd/Appium/emulator/Alloy/kernel streams.
3. Apply targeted case-insensitive patterns such as `(?i)error|fail|timeout|offline|unauthorized|disconnect|reset|oom|killed|no space|dns|resolve|EAI_AGAIN|instrumentation|uiautomator|systemPort|proxy`.
4. Query before the first symptom to establish cause and after it to see recovery.

Split by host, unit, pattern, and time when results hit limits. An empty query is meaningful only after confirming streams and Alloy ingestion for that host/window. Note gaps, delayed ingestion, or clock skew explicitly.

Machine logs must come from Loki. Do not fall back to SSH, `journalctl`, `/var/log`, Docker logs, or direct files. If Loki lacks coverage, limit the verdict accordingly.

## Infrastructure classification matrix

| Symptom | Interpretation | Corroborate with |
|---|---|---|
| Runner did not start, executor/network/cache failure | CI infrastructure | GitLab runner reason, Zabbix runner state, Loki runner logs if onboarded |
| APK/dependency cannot resolve or download | DNS/network/Nexus/artifact delivery | host Loki DNS/TLS errors, Zabbix network state, HTTP status |
| Session cannot be created | Grid/Appium/device readiness | Grid routing, Appium unit logs, ADB/device state, helper/package errors |
| `Could not proxy`, UiAutomator2 timeout/crash | Appium ↔ UiAutomator2/device transport | Appium logs, instrumentation exit, ADB/USB/kernel events |
| Device offline/unauthorized/not found | ADB/USB/device infrastructure | ADB monitoring item, kernel USB events, Appium timestamp |
| System panel, lockscreen, rotation, helper drift blocks actions | Device preparation infrastructure | screenshot/page-source clue plus preparation or host/device evidence |
| Stale/new-command timeout after client silence | Runner/framework lifecycle; not automatically device outage | Grid inactivity and absence of Appium/ADB faults |
| Assertion mismatch after healthy commands | Out of scope | mention briefly; do not investigate |
| Element absent while AUT is responsive | Usually out of scope unless system UI/device state obscures AUT | page source/screenshot and transport health |

Avoid single-keyword diagnosis: classify `timeout` by the layer and nearby evidence.

## Final report contract

Write in the user's language and lead with:

1. **Verdict** — one evidence-standard label and cause summary.
2. **Job** — URL/ID, project/ref/SHA, status, UTC and Europe/Moscow interval, runner, stand/suite.
3. **Evidence timeline** — correlated job, Zabbix, and Loki facts with component and source.
4. **Affected infrastructure** — component, blast radius, and recovery state.
5. **Zabbix** — historical/current state and monitoring gaps.
6. **Selenium/Grid** — inventory-selected Hub address, current readiness/latency, slot totals, registered devices with idle/busy and proxy/Appium status, plus the boundary between these current checks and historical evidence.
7. **Loki** — human-readable selectors/time slices, decisive events, and coverage; no large raw logs.
8. **Excluded failures** — compact list/count of test/product failures not diagnosed.
9. **Next infrastructure actions** — prioritized recommendations only, with rollback considerations.
10. **Confidence and gaps** — facts versus inference and missing access/retention/labels.

Redact tokens, passwords, cookies, authorization headers, embedded Nexus credentials, notification/device tokens, private keys, and sensitive test payloads. Store only short sanitized evidence excerpts in the operational note.
