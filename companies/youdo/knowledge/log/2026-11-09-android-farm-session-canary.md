---
system: android-farm
status: verified
checked: 2026-11-09
tags: [appium, canary, uiautomator2]
---
# Android isolated sequential session canary

## Task and authorization
User explicitly approved item1: one reserved device, one worker, repeat create session -> simple command -> quit, observing Appium requests and port release. This covered the scoped diagnostic sessions and temporary process cleanup; no general CI changes, service recovery or increased parallelism was authorized.

## Context
M-K0058 `192.168.30.32`; Xiaomi/RedmiNote13Pro `x4pf5l5haegykni7`, Android13. Production `phone_redmi_note_13_pro.service` was inactive, MainPID0; no target ADB forward and15903/16003listeners before testing. Other devices had existing forwards15901/15902/15904 and were not touched.
See [device check](2026-11-09-android-farm-xiaomi-unicodeime-device-check.md) and [multi-device incident](2026-11-09-android-farm-dig-job-3282724.md).

## Actions
Used an isolated temporary Appium1.22.3 process, loopback `127.0.0.1:16003`, no nodeconfig or Grid registration. Separate transient systemd units with RuntimeMaxSec480, TimeoutStopSec15, KillModecontrol-group and automatic stop in finally. Machine DEBUG logs were read exclusively from Loki through Alloy, selectors `instance=M-K0058`, `job=integrations/journal`, `unit=android-session-canary-20261109b.service` and `...09c.service`. Diagnostic script/results live under `~/ai-data/android-dig/session-canary-20261109/`.
Capabilities used UiAutomator2, fixed UDID/systemPort15903, system Settings package with autoLaunchfalse/noResettrue, skipUnlocktrue, adbExecTimeout60000, instrumentation launch60000, newCommandTimeout60. No test APK download, host-wide preparation, helper uninstall or device reboot performed. Appium initialization installed required helpers as part of approved session creation. Simple command was GETwindow/current/size. All sessions were serial; no deliberate inter-cycle sleep (read-only snapshots add short observation overhead).

## Evidence timeline
All times2026-11-09 UTC /Europe-Moscow UTC+3.
-15:22:16–15:22:18UTC /18:22:16–18:22:18MSK: initial harness attempt failed before device initialization because temporary unit lacked ANDROID_HOME/ANDROID_SDK_ROOT. This is a diagnostic harness error, not farm evidence. Temporary process stopped, no session/forward left. Harness fixed by setting both SDK variables to `/root/Android/Sdk`.
-15:22:41–15:22:45UTC /18:22:41–18:22:45MSK: unicodeKeyboardtrue reproduction. Before session, `ime list -s` lacked AppiumIME. DEBUG showed Settings not installed; Appium streamed installation of Settings3.4.0 successfully at15:22:43.535UTC. At15:22:44.530UTC it attempted `ime enable io.appium.settings/.UnicodeIME`; Android returned exit255/`Unknown input method ... cannot be enabled for user #0`. Create returned HTTP500 after2.149s; no session or port forward remained. Temporary Appium stopped.
- Read-only postcheck: package3.4.0/versionCode30 installed for user0, installedtrue/hiddenfalse/suspendedfalse/enabled0, firstInstallTime18:22:43MSK. PackageManager resolves both `.AppiumIME` and `.UnicodeIME` services with BIND_INPUT_METHOD, but `ime list -s` still listed only Google keyboard/voice IME. This is a mismatch between package service registration and InputMethodManager available-method list, not total package absence or ADB transport loss. The trigger/internal Android cause is not established. Earlier15:10MSK inspection had shown registered AppiumIME; between checks the package became absent, but the removing actor is not established.
-15:23:56–15:24:14UTC /18:23:56–18:24:14MSK: same isolated device with unicodeKeyboardfalse/resetKeyboardfalse only in diagnostic capabilities. Three create -> screen-size GET -> quit cycles all HTTP200. Screen1080x2176. Forward `x4pf5l5haegykni7 tcp:15903 tcp:6790` and ADB listener appeared during each session and disappeared immediately after each quit. No busy-port or unknown-session error. Appium reported zero remaining sessions, then temporary service stopped.

## Findings and limits
Confirmed independent Xiaomi IME initialization defect reproduced with no Grid routing or parallel sessions. Settings package installation succeeds but InputMethodManager does not expose UnicodeIME even though PackageManager resolves its services. Appium fails before UiAutomator2 session creation in that variant.
Three serial cycles bypassing UnicodeIME passed and cleaned up correctly; no sequential port-release race was reproduced on this isolated device. This is not proof of all-farm health, parallel-session correctness, normal test application behavior or Grid routing correctness. It does not explain multi-device failures in job3282724 and does not prove host-wide preparation/concurrency was their cause. Do not change production unicodeKeyboard from this diagnostic bypass alone.

## Changes and final state
Only approved temporary Appium/session activity on the reserved Xiaomi. Settings/helper packages may be installed by normal initialization; no speculative uninstall/reinstall/reset or permanent config edit. Production Xiaomi unit remains inactive and outside Grid. Temporary units stopped,15903/16003listeners absent, no target forward or remaining diagnostic session; other device forwards unchanged in final snapshots. Diagnostic exec completed; no task background operation remains.

## Status and remaining decisions
Item1 completed; controlled canary did not reproduce a sequential cleanup defect. Items2–4 of the proposed plan remain conditional/proposed and unexecuted; see central [TODO](../../../../TODO.md), android-farm section. Fixing Xiaomi IME registration, testing another device/through Grid or increasing parallelism requires a separately scoped next action. Notes and TODO reconciled; no repo publication or CI run performed.

## Portable lesson
none

## Later recovery — 2026-11-09 18:29 MSK

User-approved phone reboot followed by Appium initialization recovered UnicodeIME without reinstalling Settings3.4.0;3/3cycles with unicodeKeyboardtrue passed. Earlier failed/absent-IME observations remain historical evidence. Production unit stays stopped, return-to-Grid remains proposed. See [reboot verification](2026-11-09-android-farm-xiaomi-unicodeime-reboot.md).
