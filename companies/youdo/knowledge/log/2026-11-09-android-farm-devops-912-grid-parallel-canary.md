---
system: android-farm
status: verified
checked: 2026-11-09
tags: [appium, grid, parallel, canary]
---
# DevOps-912: Grid lifecycle canary at2/4/6workers

## Task and authorization
User explicitly approved proposed item2: Grid lifecycle testing with2then4then6workers, stop at first fault and correlate requests/sessionIDs/ports/Loki. This covered controlled diagnostic session creation/commands/cleanup. No real autotest job, application APK installation, service restart, device reboot, timeout/configuration change or oversubscribed15worker run authorized/performed.

## Context and baseline
Fresh Enabled Selenium inventory M-K0056Hub/M-K0057/M-K0058. Grid and all7Appium endpoints initially ready,7idle/0busy slots,queue0. Prior [35serial cycles](2026-11-09-android-farm-devops-912-grid-serial-canary.md) passed after7activeAppium restarts. Inactive unauthorized SamsungA55was not brought into scope. Xiaomi remained recovered and registered.
Generated controller `~/ai-data/android-dig/DevOps-912/grid-parallel/probe.py`, results `summary.json` and `progress.jsonl`; Python3.8compatible, compiled before execution.

## Method
Each level executed5cycles per worker,10/20/30total. First-wave creation synchronized; allNsession IDs existed before commands, proving real peak2/4/6instead of merely concurrent requests. Remaining cycles independently created/commanded/quit, allowing one worker to request a new session while others still worked/closed.
Same native diagnostic capabilities as serial test: UiAutomator2, system Settings package, autoLaunchfalse/noResettrue, unicodeKeyboardtrue/resetKeyboardtrue, skipUnlocktrue, existing node UDID/systemPort defaults retained. Simple command GETwindow/current/size through Hub. No host-wide adb.sh/device cleanup, deliberate helper install/uninstall or test data/business actions.
Actual proxy identity verified using Grid testsession API. Each worker checked that its own ID existed at the backend, target ADBdevice/forward/listener present during execution, command/quitHTTP200, and closedIDabsent afterwards. A newly assigned session on the same node may legitimately retain a forward, so post-quit existence alone was recorded rather than incorrectly classified as leakage; complete session/port release was required at each level boundary. No such post-quit forward was observed in this run.
Before and after every level: all7backend session lists empty, no target listener/forward on any node, Grid7free/queue0. No level advances without clean state. First error would stop new requests, abort initial barriers and close only own exact session IDs; no error occurred.

## Results
Window2026-11-09 16:17:21.021–16:19:41.044UTC /19:17:21.021–19:19:41.044MSK.

| Workers | Passed cycles | Actual peak sessions | Max create seconds | Max quit seconds |
| --- | --- | --- | --- | --- |
| 2 | 10/10 | 2 | 7.057 | 0.627 |
| 4 | 20/20 | 4 | 7.181 | 0.455 |
| 6 | 30/30 | 6 | 7.144 | 0.518 |

All60create/60command/60quit requestsHTTP200, no SessionNotCreated/unknown-session/systemPortbusy/instrumentation timeout. All phase complete flags true, no worker/controller errors, exact expected counts checked, initial/final baselines clean. All7actual node endpoints exercised,8or9cycles each across levels.
Peak concurrency proofs depend on first-wave active-session barrier plus backend ownership checks; later cycles naturally had variable overlap as faster workers progressed/finished. This is a bounded lifecycle stress probe, not a sustained long-duration benchmark.

## Loki and final verification
Bundled Loki collector queried16:17:10–16:19:51UTC with fresh Enabled inventory. All3canonical instances have operational streams and boundary coverage, no truncation, coverage_complete=true. Its238categorized candidates are only repeated `[BaseDriver]   uiautomator2ServerLaunchTimeout` and `[BaseDriver]   adbExecTimeout` capability-name warning lines,119each; these are not command timeouts. Machine logs exclusively from Loki.
Final Hub collector confirms7registered proxies,7Appium endpoints reachable/ready,7free/0busy slots,queue0. All worker/controller tasks joined and exec exited0; no diagnostic session, target forward/listener or background operation remains. Production services remain running; no host/service change in this turn.
Evidence `~/ai-data/android-dig/DevOps-912/grid-parallel/`: summary.json,progress.jsonl,loki.json,final-inventory.json,final-grid.json.

## Interpretation and remaining decision
No infrastructure failure found in these60native lifecycle cycles at2/4/6workers after the earlier resets/cleanup and Settings preservation. This does not establish a permanent fix or cause of historical job3282427/3282724failures. It does not cover real application navigation/installation/download, long idle/session duration, overlapping CI device preparation,15workers exceeding7slots, or assertions/test data.
Approved item2 completed. Remaining original item3is a small real-test canary with limited concurrency and evidence-based correction only if reproduced. Real autotests were not restarted. Central [TODO](../../../../TODO.md), android-farm session-diagnosis entry, tracks this proposal; planning does not authorize execution.

## Changes
Generated diagnostic script/results, local knowledge note/map link and scoped central TODO updates only. No repository edit, publication or CI mutation.

## Portable lesson
none
