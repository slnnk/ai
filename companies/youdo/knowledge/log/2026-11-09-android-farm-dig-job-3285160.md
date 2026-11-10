---
system: android-farm
status: verified
checked: 2026-11-09
tags: [android-dig, appium, grid, loki, zabbix]
---
# Android job3285160: current infrastructure check after farm recovery

## Task and verdict
User requested current logs of job3285160. Read-only diagnosis; no retries, cancellations, service/device changes, session deletion or product/test-code investigation.
Verdict: **No infrastructure failure found in the checked running-job snapshot**. Previous UnicodeIME/session-creation/systemPort/proxy failure signatures absent in trace and supporting operational logs. This is not a final job success verdict;13FAILED test-event lines exist and underlying locator/product/device-UI causes were not diagnosed.

## Job and snapshot times
Project `youdo/Test/youdo-android-testing`, jobautotests/stagetests, pipeline142559, refTest-7062, SHA5cbe63fe265c09b65ecb5e46e9e48e3e8053615f, runner108 `gitlab-runner-docker-1 integrations-tests (172.28.0.171)`.
Started2026-11-09 16:22:15.780UTC /19:22:15.780MSK. Stillrunning with no finished_at/failure_reason at final metadata fetch16:57:57UTC /19:57:57MSK.
Initial trace snapshot16:55:35UTC approximately9.87MB/87526normalizedlines. Later selected trace read10.29MB, last visible Gradle timestamp19:56:44.973MSK /16:56:44.973UTC. Monitoring window16:12:15–16:55:35UTC /19:12:15–19:55:35MSK (start−10minutes to actual collectiontime). Collector's normalized running-job correlation end adds10minutes; explicitly clamped monitoring end to collectiontime rather than querying the future or claiming a real finish timestamp.

## CI context and routing
Trace `JOB_ID=1`, standtest5, suite`[Упавшие тесты]`, previousfailedjob3282724/pipeline142540, app`4.0.275.feature-and-4674-ucassa-exp (142519)`.
Actual trace launch flags `-PautotestParallel=true`, `-PautotestThreadCount=15`, `-PautotestRetryCount=1`.
Current project variables scope`*`: APPIUM_NODES_1=M-K0057/M-K0058 inventoryIPs31/32, SELENIUM_SERVER_1=Hub30:4444/wd/hub. Pool2addresses outside Enabled scope. Values current at fetch, not historical effective job variables; group/pipeline/schedule/dotenv/runner overrides not covered.

## Evidence timeline
- Preparation: cache successfully extracted. `Failed to restart emulator_2.service: Unit emulator_2.service not found.` remains nonfatal preparation-contract drift (known second emulator absent on M-K0058); job continued.
-16:23:39UTC /19:23:39MSK and16:24:26UTC /19:24:26MSK: M-K0057emulator1/emulator2processes killed during known CI preparation/restarts. No corroborating OOM or host reboot; do not label controlled preparation kills as a spontaneous runtime outage.
-19:34:33MSK onwards test-event FAILED headers include testShare, testB2bStatusViaOfferAdding, testOfferAddedNotSelected, testOfferAddingNoFunds, testOfferAddingPackage and others. No test-data payloads retained.
- Through19:56:44MSK selected trace contains52PASSED/13FAILED terminal test-event lines and11NoSuchElementExceptionmatching lines. These are log-event/stacktrace-line counts, may include retries and are not a final unique-test verdict. Do not equate11exception lines to11distinct failing tests.
- At19:55:35MSK Hub7busy/0free/7queuedrequests, all7proxiesregistered and Appiumready. This is saturation under15requestedthreads, not a demonstrated Hub outage; waiting times and effective per-test deadlines remain unmeasured.
- Final metadata19:57:57MSK stillrunning; artifact/report publication not yet confirmed.

## Infrastructure sources
Fresh Selenium Enabled inventory16:55:20UTC: M-K0056/M-K0057/M-K0058, no substitute hosts. Trace infrastructure-signature counts all0: runner, networkdependency, Grid, Appium/UiAutomator, ADB, preparation-specific matcher, artifactdelivery. The generic missing-emulator-service line above was found by additional safe extraction even though the collector matcher did not classify it.
Current Hub inventory-selected192.168.30.30:4444 HTTP200/readycapacitysaturated. Registered7devices: M-K0057ports15001emulator5554/15002emulator5556/15004Redmi5b2d4fe2; M-K0058ports15001emulator5554/15002TECNO15888255AE004773/15003Xiaomix4pf5l5haegykni7/15004SamsungRZ8R71ZRK8H. Allbusy at snapshot and Appiumstatusready; current HTTP status alone does not prove command health.
Zabbix46selectedmetrics all have window data,0interfaceerrors/unsupporteditems/exact-windowtriggertransitions. Physical ADBstatusdevice throughout sampled window, except inactive/unregisteredSamsungA55RZCY20AXJHN remainsunauthorized. Emulator ADBitems not returned; physical sample gaps up to121seconds, not continuous transport proof. M-K0057existing root-space threshold alarm persists, min16.71GBfree; CPUload/coremax3.0085/iowait40.5789%. M-K0058load/coremax1.6969/iowait3.0668%, rootfree51.11GBmin. Resource peaks alone do not establish test failures.
Loki exact canonical selectors `{instance="M-K0056"}`, `{instance="M-K0057"}`, `{instance="M-K0058"}` for checked window, operational streams present on3hosts, both boundarysamplescovered, no querytruncation, coverage_complete=true.572categorized events mostly capability-name warnings(281adbExecTimeout/281uiautomator2ServerLaunchTimeout), not real timeout errors; remaining10emulator/2systemd candidates correspond to preparation/restart output. No correlated session/proxy/IME/device-transport error. Hub-specific Grid application logs not identified separately from generic journal coverage.

## Interpretation and exclusions
Current execution differs materially from older jobs: sessions now create and tests run without the prior transport/IME/systemPort failure chain in checked snapshots. Element lookup failures are present; absent screenshot/page-source proof of system-UI obstruction, do not relabel them as infrastructure faults or claim a product root cause. No assertion/locator/application changes recommended from this skill.
Monitoring ends19:55:35MSK, trace selected through19:56:44MSK, final metadata19:57:57MSK; later job events are outside this snapshot. Job stillrunning, final counts/report uploads and any later failures unknown.15threads exceed7slots; cap-aware trial remains a proposal, not an authorized change.

## Changes and remaining work
Local sanitized collector output under `~/ai-data/android-dig/3285160/`; no full raw trace or sensitive request payloads persisted. This note and scoped central TODO evidence only. Existing central [TODO](../../../../TODO.md), android-farm section, tracks real-test validation and preparation-contract drift. Real-test job started externally; this read-only review does not authorize interfering with it. Finish/final-report review remains a proposal for a later snapshot, not a background watcher. All task command sessions finished, no background operation remains.

## Portable lesson
none

## Fresh infrastructure recheck — 2026-11-09 21:27 MSK

User asked whether infrastructure errors exist now; prior snapshot was explicitly limited to19:56MSK. Refetched fresh Enabled inventory, whole trace, current Hub, full-window Zabbix/Loki and metadata, read-only.
- Trace source18:26:12UTC /21:26:12MSK:36074034bytes/328093normalizedlines. All8infrastructure signal-category counts0; no SessionNotCreated, busy-systemPort, UnicodeIME, proxy/transport/ADB/runner/network/artifact error reported by extraction. No claim that final test assertions passed; final counts were not re-extracted in this narrow recheck.
- Full monitoring window16:12:15–18:26:30UTC /19:12:15–21:26:30MSK. Loki3instancesoperational/boundarycovered/noquerytruncation/coverage_complete=true.1634categorizedentries:1624only capability-name warning lines(812each adbExecTimeout/uiautomator2ServerLaunchTimeout), remaining10emulator/2systemdpreparation messages already explained above. No other categorized infrastructure event.
- Zabbix46metrics have window data,0interfaceerrors/unsupporteditems. New M-K0057low-CPU-idle episodes17:43:08–17:46:08UTC /20:43:08–20:46:08MSK and17:49:08–17:58:08UTC /20:49:08–20:58:08MSK, both recovered. Resource pressure is real but no correlated session/transport failure established; existing CPU/memory/disk follow-up already tracked centrally.
- Current Hub7busy/0free,8queuedrequests,7Appiumendpointsreachable/ready. Capacity saturation with configured15threads, not confirmed Hub outage. Existing nonfatal missingemulator_2service preparation drift remains a separate known issue and is not erased by zero signature counts.
- Metadata18:27:07UTC /21:27:07MSK stillrunning, no finished_at/failure_reason. No final execution/report outcome yet. No intervention or background watcher started; all recheck tool sessions completed.
Verdict remains: no confirmed recurrence of the earlier Appium/Grid/ADB infrastructure failure chain in the checked snapshot. This does not establish product/test-code root cause, absence of every possible infrastructure defect, or successful final job completion. Evidence files end `-latest.json` under generated job directory; older counts/snapshots above remain historical.
