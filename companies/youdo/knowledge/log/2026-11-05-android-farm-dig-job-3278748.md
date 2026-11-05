---
system: android-farm
status: verified
checked: 2026-11-05
tags: [android, appium, adb, incident]
---
# Android job3278748: Appium UnicodeIME session creation failure

## Task and verdict
User reports Nexus cleaned and Android uploaded, then requests inspection of [job3278748](https://gitlab.youdo.sg/youdo/Test/youdo-android-testing/-/jobs/3278748).
Confirmed infrastructure failure: Appium session creation fails because Android user0 cannot enable `io.appium.settings/.UnicodeIME` on device `x4pf5l5haegykni7`. The exact helper-package/IME registration defect is not yet established; absence of an available input method does not by itself prove the entire package is missing.

## Job
Project69, pipeline142404, branch DevOps-908-gradle-image-18, commitcdea347741d72635371e4bdd80becd645a2efadf, runner108 at172.28.0.171. Job failed/script_failure.
Nov5 19:38:44–19:46:30 Moscow /16:38:44–16:46:30 UTC. Correlation query19:28:44–19:56:30 Moscow /16:28:44–16:56:30 UTC.
JOB_ID1, test5, Debug; APP_VERSION now `4.0.274.staging (142214)` rather than an error path. Endpoint-change commit is present. Local Gradle-cache follow-up is not committed/published and is not part of this run.
Trace result `4 tests completed, 1 failed`; `testRefillAccount1` fails at19:45:53 Moscow /16:45:53 UTC, repeating during reporting at19:46:16. Error: ADB `shell ime enable io.appium.settings/.UnicodeIME` exits255, `Unknown input method io.appium.settings/.UnicodeIME cannot be enabled for user #0`. Gradle ends failed19:46:17; archive and JUnit uploads both201. Report publication succeeds.
Previous terminal Houston404 is not the observed failure in this run. Preparation also reports missing emulator_2.service, package removal failures and unknown app-package permission errors, masked by CI continuation. No assertion/locator/product debugging performed.

## Inventory and live Grid
Enabled Selenium inventory fetched16:48:50 UTC includes canonical M-K0056/M-K0057/M-K0058; current routing definitions scope* use APPIUM_NODES_1=192.168.30.31/32, SELENIUM_SERVER_1=http://192.168.30.30:4444/wd/hub. Project-variable fetch excludes group/pipeline/schedule/dotenv/runner overrides.
Inventory-selected Hub M-K0056/192.168.30.30:4444 checked16:48:59 UTC: Selenium3.141.59, ready, HTTP200/83.8ms,7total/7free/0busy, queue0.
All7 registered proxies confirm registration and Appium1.22.3 HTTP200/ready; all idle in this snapshot:
- M-K0057/192.168.30.31:15001 emulator-5554,15002 emulator-5556,15004 5b2d4fe2.
- M-K0058/192.168.30.32:15001 emulator-5554,15002 15888255AE004773,15003 x4pf5l5haegykni7,15004 RZ8R71ZRK8H.
The implicated proxy is15003 on M-K0058. Current HTTP readiness is not historical session/IME-health proof. Grid advertises Android10 for all proxies; actual device OS versions were not independently checked.

## Zabbix and Loki correlation
Zabbix selects46metrics across3hosts;0interface errors,0unsupported selected items,0window trigger transitions and0selected metrics without data. The target ADB item has10samples, all `device`, between19:30:19 and19:48:19 Moscow, max gap120s. Transport presence is confirmed, IME correctness is not monitored.
M-K0058 root free space stays~57.7–58.4GB; no saturation signal explains the observed failure. Memory-used percentage reaches99.0% on M-K0058/99.2% on M-K0057 but no matching OOM was established. One preexisting unresolved ADB alert concerns RZCY20AXJHN (sinceSep22), not the failing device; no causal attribution made.
Loki has operational streams for all3hosts, no query truncation. Target selector `{instance="M-K0058",job="integrations/journal",unit="phone_redmi_note_13_pro.service"}`. At19:45:40 Moscow Appium driver messages appear; at19:45:53.321 logs show failed cleanup of absent systemPort15903 forward for the same target UDID. This corroborates failed session lifecycle; cleanup error is secondary, not the demonstrated initial cause.
A targeted Loki slice19:44:30–19:46:30 found3filtered entries and did not independently reproduce the full UnicodeIME stack. The decisive IME error is in GitLab.
The requested +10-minute tail ended19:56:30, after collection around19:49:35. Therefore collector boundary_coverage=false is partly expected; it must not be reported as log loss. Operational logs exist across the actual job time; endpoint samples extend after finish. No absence-of-errors health claim made.

## Status and next checks
Read-only diagnosis complete; no device/package/service changes, retries or session termination. Device/helper IME registration remains unresolved and linked from the existing device-preparation TODO. Next proposal is inspect installed io.appium.settings version/package and registered input methods for user0, then choose a narrowly reviewed helper repair; do not disable Unicode keyboard blindly or reinstall packages without authorization.
User-reported Nexus cleanup/upload supersedes the prior active-storage-outage status; successful version reading is observed. Separate [DevOps-910 evidence](2026-11-05-nexus-devops-910-disk-diagnosis.md) records the recovery and user task closure; this diagnosis did not remeasure free capacity or reopen that work.
Evidence under `/home/slnnk/ai-data/android-dig/3278748/`; temporary sanitized trace deleted. No background operations remain. Gradle-cache publication stays separately pending under DevOps-908.

## Portable lesson
none

## User deferral of device repair (2026-11-05)
User explicitly requested adding device x4pf5l5haegykni7 to TODO for later investigation. A separate deferred Android-farm entry now tracks this specific IME issue; it is not part of DevOps-908 implementation or a prerequisite to publishing the already prepared Gradle-cache patch. The older broad helper/IME preparation task remains unchanged and no duplicate device-specific evidence stays appended there.
No more device work is authorized until a new request. No repair, retry, service or capability change was performed.
