---
system: android-farm
status: verified
checked: 2026-11-09
tags: [appium, adb, unicodeime, reboot]
---
# Xiaomi UnicodeIME recovery by reboot and verification

## Task and authorization
User approved the proposed next action: reboot only Xiaomi `x4pf5l5haegykni7`, check IME registration and run3serial cycles with unicodeKeyboardtrue while keeping production Appium stopped and the device outside Grid. No farm host reboot or production return authorized.

## Context
Host M-K0058, SSH verified `192.168.30.32`, device model23117RA68G/Android13. Previous [isolated canary](2026-11-09-android-farm-session-canary.md) reproduced UnicodeIME failure despite successful Settings3.4.0 installation;3cycles with UnicodeIME bypass passed. Before reboot the production Xiaomi unit was inactive/MainPID0, no target ADB forward or15903/16003listener, and ime-list omitted AppiumIME.

## Actions and findings
- Executed only `adb -s x4pf5l5haegykni7 reboot` on M-K0058. Host/other devices not rebooted; existing forwards for TECNO/Samsung/emulator remained.
- ADB temporarily lost the device, then returned `device`; `sys.boot_completed=1` and device uptime94.70seconds confirmed reboot. The bounded initial wait expired just before a subsequent read-only check found the completed boot; no repeat reboot was issued.
- Immediately after boot, `ime list -s` still omitted AppiumIME. Do not claim reboot alone immediately repopulated the IME list.
- At15:29:30–15:29:51UTC /18:29:30–18:29:51MSK, temporary unit `android-session-canary-20261109d.service` ran loopback-only Appium16003 without Grid registration. Same guarded single-device test as prior canary, now unicodeKeyboardtrue/resetKeyboardtrue, systemPort15903, noResettrue, autoLaunchfalse and system Settings package. Three sequential create -> GETwindow/current/size -> quit cycles.
- All3creates/3commands/3quits HTTP200. Create durations9.482s,4.503s,4.98s (exact values in generated results are authoritative); port15903forward appeared during each session and was absent immediately after each quit. No port-busy/unknown-session/UnicodeIME failure. Screen1080x2176.
- DEBUG evidence obtained only from Loki, selector `{instance="M-K0058",job="integrations/journal",unit="android-session-canary-20261109d.service"}`: first session found installed Settings3.4.0 and explicitly skipped installation/upgrade; then launched helper, successfully enabled and selected UnicodeIME. Subsequent sessions also enabled/selected it successfully. No helper uninstall/reinstall was performed in this verification.
- Final read-only `ime list -s` includes `io.appium.settings/.UnicodeIME`. Settings remains3.4.0, firstInstallTime/lastUpdateTime unchanged18:22:43MSK. Reboot plus subsequent Appium initialization recovered the function with the same installed APK; the initiating Android/MIUI registration defect is still unproven.

## Changes and final state
Only the approved phone reboot and bounded temporary diagnostic sessions. Temporary Appium stopped, zero remaining diagnostic sessions,15903/16003listeners absent, no Xiaomi forward. Production `phone_redmi_note_13_pro.service` remains inactive; device not returned to Grid. Other devices unchanged by the agent. All task exec sessions completed, no background task remains.
Generated results and sanitized Loki logs under `~/ai-data/android-dig/session-canary-20261109/`, results-after-reboot.jsonl and loki-after-reboot.json.

## Status and risks
Functional recovery verified3/3with UnicodeIME enabled, not a permanent root-cause fix or proof that CI helper removal cannot reintroduce the defect. Separate approval needed to return production Appium to Grid. Existing central [TODO](../../../../TODO.md), android-farm section, tracks return proposal and preparation/session safeguards. Other-device/Grid concurrency failures from job3282724 remain unresolved; no CI retry, unrelated reset or repository change performed.

## Portable lesson
none

## Superseding controlled reinstall test — 2026-11-09 18:32 MSK

User requested Settings reinstall verification. Targeted uninstall plus successful same-version3.4.0normal Appium installation reproduced UnicodeIME failure on first session. Earlier3/3recovery is historical, not current device health. Production Appium remains stopped and current IME registration is broken again; no second reboot performed. See [reinstall regression](2026-11-09-android-farm-xiaomi-settings-reinstall.md).
