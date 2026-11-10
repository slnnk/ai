---
system: android-farm
status: verified
checked: 2026-11-09
tags: [appium, unicodeime, recovery, grid]
---
# DevOps-912: Xiaomi recovered and returned to Grid

## Task and authorization
User requested restoring Xiaomi after the controlled Settings reinstall reproduced IME failure. Prior proposed action explicitly included device reboot,3UnicodeIME-enabled diagnostic cycles, then production Appium start/Grid return if checks passed. Agent described and executed this sequence; no general CI restart, helper uninstall/reinstall, host reboot or change to other devices authorized/performed.

## Context
M-K0058 verified hostname/IP `192.168.30.32`, Xiaomi/RedmiNote13Pro model23117RA68G, UDID`x4pf5l5haegykni7`, Android13. Production `phone_redmi_note_13_pro.service` was inactive/MainPID0, ADBdevice, no target forward or15903/16003listener, UnicodeIME absent before recovery. Settings3.4.0 remained installed from18:32:24MSK controlled reinstall.
See [regression](2026-11-09-android-farm-xiaomi-settings-reinstall.md), [Settings-preservation implementation](2026-11-09-android-farm-devops-912-preserve-appium-settings.md), [Grid clean baseline](2026-11-09-android-farm-devops-912-grid-hub-restart.md).

## Actions and evidence
- Issued only targeted `adb -s x4pf5l5haegykni7 reboot`; ADB became absent, returned device, and `sys.boot_completed=1` was observed15:55:12UTC /18:55:12MSK.
- Temporary isolated loopback Appium16003, transient unit `android-session-canary-20261109f.service`, no Grid registration, fixed systemPort15903. Same guarded3serial create -> GETwindow/current/size -> quit probe, unicodeKeyboardtrue/resetKeyboardtrue, noResettrue/autoLaunchfalse, system Settings package.
- Probe15:55:43–15:56:05UTC /18:55:43–18:56:05MSK: all3creates/commands/quits HTTP200. Create10.946s/4.4s/4.147s; command0.011s/0.023s/0.009s; quit0.312s/0.406s/0.239s. Screen1080x2176. Target15903forward/listener present during sessions and absent immediately after every quit; zero remaining sessions.
- UnicodeIME was absent from initial pre-session list, then Appium successfully enabled it; subsequent snapshots and final ime-list contain `.UnicodeIME`. Do not claim reboot alone immediately exposed the IME.
- DEBUG logs exclusively through Loki selector `{instance="M-K0058",job="integrations/journal",unit="android-session-canary-20261109f.service"}`,569entries/no1000-entry cap hit. Three successful ime-enable calls; temporary Appium SIGTERM/shutdown at15:56:05. No manual install/uninstall; final package3.4.0firstInstallTime/lastUpdateTime unchanged18:32:24MSK.
- Guarded result assertions passed before production start:3cycles200, every forward removed after quit, no remaining session, temporary unit stopreturn0, final UnicodeIME present. Temporary16003listener absent.
- Started only `phone_redmi_note_13_pro.service`: active/running/MainPID355721, ActiveEnterTimestamp18:56:47MSK.
- Fresh Enabled Selenium inventory15:55:20UTC /18:55:20MSK. Hub check15:57:20UTC /18:57:20MSK confirms Xiaomi `REAL_DEVICE_x4pf5l5haegykni7`, M-K0058:15003, registered proxy, Appiumready, slotidle. Whole Grid7registered/7free/0busy/queue0; all7Appium endpoints reachable/ready.

## Changes and final state
Approved phone reboot, temporary sessions/cleanup and production Xiaomi Appium start. Device recovered and returned to Grid, Settings preserved without reinstallation; no leaked diagnostic session/forward/15903or16003listener. Other devices and containers not changed in this recovery. All task exec sessions finished; no background task remains.
Generated evidence: `~/ai-data/android-dig/session-canary-20261109/results-recovery.jsonl`, `loki-recovery.json`, `~/ai-data/android-dig/DevOps-912/grid-with-xiaomi-recovered.json`.

## Status and limits
Requested recovery complete. Local/merged DevOps-912preservation reduces the reproduced uninstall/reinstall trigger, but future deliberate helper replacement can still require controlled verification. Recovery is functional evidence, not an established internal Android/MIUI root cause. Other-device/Grid lifecycle/concurrency defects remain unproven/unresolved; full product tests were not run. Central [TODO](../../../../TODO.md), android-farm section, closes Xiaomi recovery and retains shared session diagnosis. Next direct-Appium versus Grid comparison and controlled concurrency remain proposed, not executed.

## Portable lesson
none
