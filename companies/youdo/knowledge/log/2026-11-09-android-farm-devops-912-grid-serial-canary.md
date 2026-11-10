---
system: android-farm
status: verified
checked: 2026-11-09
tags: [appium, grid, canary, session]
---
# DevOps-912: restart active Appium services and serial Grid canary

## Task and authorization
User explicitly requested restarting Appium for all devices, then item1: one worker through Grid, five create -> simple command -> quit cycles per device, checking sessions and port release. Agent stated seven registered/active devices scope; the inactive SamsungA55/RZCY20AXJHN onM-K0057 remained stopped/unauthorized and outside current Grid scope. No device/host reboot, helper removal, application deployment or parallel-load run authorized/performed.

## Baseline and restarts
Fresh Enabled inventory scope M-K0056/M-K0057/M-K0058. Before/after restarts Grid had7registered/7idle slots, queue0. Production Appium1.22.3; Hub3.141.59, all nodes maxSession1.
- M-K0057 `192.168.30.31`: restarted phone_emulator_1/phone_emulator_2/phone_redmi_note_14_pro,19:03:47MSK /16:03:47UTC; active MainPID844492/844493/844509.
- M-K0058 `192.168.30.32`: restarted phone_emulator_1/phone_tecno_cm7/phone_redmi_note_13_pro/phone_samsung_galaxy_a12,19:04:06MSK /16:04:06UTC; active MainPID356283/356281/356264/356298.
- No service config/log-level changes, ADB reset, helper reinstall or global adb.sh preparation. Xiaomi remained healthy with UnicodeIME after prior recovery.

## Probe method
Generated local one-worker controller `~/ai-data/android-dig/DevOps-912/grid-canary/probe.py`. Guarded baseline requires0sessions on all7Appium backends and no target forward/listener. Every native session created through `http://192.168.30.30:4444/wd/hub` with UiAutomator2, unicodeKeyboardtrue/resetKeyboardtrue, noResettrue/autoLaunchfalse, system Settings package; no APK download/install or real app/test-data actions. Node default UDID/systemPort retained; client never overrides them. Simple command GETwindow/current/size through Grid.
Hub has actual `org.openqa.grid.internal.utils.DefaultCapabilityMatcher`. Its standard matching keys do not include custom:device, so the probe did not claim target routing from that metadata. It verified actual proxy via Grid testsession API and matched exact backend session, counted each of seven actualhost:port endpoints including the two emulator5554instances. Grid naturally rotated nodes; cycles were interleaved among nodes with one active session globally, not five adjacent immediate requests pinned to a single node.
During each cycle, read-only SSH observed the actual node UDID,ADBdevice state, systemPort listener and ADB forward. After Grid DELETE, backend session list was empty, forward/listener absent, Grid7free/queue0. Controller only deletes its own known session on failure; no broad cleanup.
An initial harness attempt stopped before creating any session because Python3.8lacks str.removeprefix. Fixed string slicing and restarted with empty-session baseline; prerun evidence retained. This is not a farm failure or a tested cycle.

## Results
Probe window2026-11-09 16:06:59.701–16:10:46.565UTC /19:06:59.701–19:10:46.565MSK, first create16:07:06UTC. Exactly35cycles completed, every endpoint5/5.

| Actual Appium endpoint | Passed cycles |
| --- | --- |
| 192.168.30.31:15001 | 5/5 |
| 192.168.30.31:15002 | 5/5 |
| 192.168.30.31:15004 | 5/5 |
| 192.168.30.32:15001 | 5/5 |
| 192.168.30.32:15002 | 5/5 |
| 192.168.30.32:15003 | 5/5 |
| 192.168.30.32:15004 | 5/5 |

Devices: M-K0057ports15001emulator5554,15002emulator5556,15004Redmi5b2d4fe2; M-K0058ports15001emulator5554,15002TECNO15888255AE004773,15003Xiaomix4pf5l5haegykni7,15004SamsungRZ8R71ZRK8H.
All35create/35command/35quit HTTP200. Create2.632–8.998seconds, command0.097–0.124s, quit0.167–0.546s. No SessionNotCreated, port-busy, unknown-session or instrumentation-startup timeout in probe results. After every quit all7slots free, queue0; exact backend session empty and target forward/listener gone. Final backend session lists all0. Assertions checked complete=true/errors=[],35passedcycles, eachcount5, allHTTP200, everycleanup and hubstate.

## Loki and final state
Bundled collector window16:03:30–16:10:56UTC covers restarts/probe. All3canonical instances have operational streams, both boundary samples covered, no event-query truncation; coverage_complete=true. The140categorized entries are only repeated `[BaseDriver]   uiautomator2ServerLaunchTimeout` and `[BaseDriver]   adbExecTimeout` capability-name warning lines, not execution timeouts. No other categorized infrastructure event emitted. Machine logs read exclusively through Loki.
Final fresh inventory/Hub collector confirms7registeredproxies,7reachable/readyAppium endpoints,7idle/0busy slots, queue0. All task exec sessions completed, no background diagnostic operation or session remains; production Appium services stay running as requested. SamsungA55unit remains inactive.
Evidence: summary.json/progress.jsonl/loki.json/final-grid.json/final-inventory.json under generated directory above. Original before/after-restart Hub snapshots in parent directory.

## Interpretation and limits
Serial native infrastructure path through Grid is currently healthy for these35cycles after clearing old sessions and restarting services. This does not prove a permanent fix of historical failures or assign their initiating cause. Grid parallelism, overlapping CI host-wide preparation, actual app download/install/navigation/assertions and an immediate pinned create/quit/create race were not tested. Existing Settings preservation remains in place; no test configuration or repository files changed in this task.
Original item1 completed. Remaining proposed stages: concurrency2/4/6with stop/correlation at first fault, then a small real-test canary and evidence-based fix. Central [TODO](../../../../TODO.md), android-farm section, tracks that remaining work; user has not authorized parallel/real-test stages in this turn.

## Portable lesson
none
