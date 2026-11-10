---
system: android-farm
status: verified
checked: 2026-11-09
tags: [appium, unicodeime, reinstall, canary]
---
# Xiaomi Settings reinstall and UnicodeIME regression test

## Task and authorization
User explicitly requested testing Settings reinstall after successful reboot recovery. Agent described the targeted uninstall/normal Appium reinstall/session check before execution. Scope was only reserved Xiaomi `x4pf5l5haegykni7` on M-K0058 `192.168.30.32`; production Appium remained stopped and no Grid return was authorized. No repo edits or farm-wide preparation.

## Context
Earlier [reboot verification](2026-11-09-android-farm-xiaomi-unicodeime-reboot.md): installed Settings3.4.0 retained, three serial UnicodeIME-enabled sessions passed. Before this experiment, direct read-only checks confirmed UnicodeIME listed, Settings3.4.0 lastUpdate18:22:43MSK, production unit inactive/MainPID0, no target ADB forward or15903/16003listener. Other-device forwards15901/15902/15904 remained active and were not touched.

## Actions and evidence
- Approved targeted command `adb -s x4pf5l5haegykni7 uninstall io.appium.settings` returned `Success`. No UiAutomator2 helper or test application uninstall was performed.
- Temporary loopback-only Appium16003 (`android-session-canary-20261109e.service`) with no nodeconfig/Grid registration then ran normal session initialization, unicodeKeyboardtrue/resetKeyboardtrue, systemPort15903, noResettrue/autoLaunchfalse, system Settings package. No special manual APK install or keyboard mutation outside normal Appium initialization.
-15:32:22.284UTC /18:32:22.284MSK: DEBUG confirms Settings absent and starts installing the Appium-bundled `settings_apk-debug.apk`.
-15:32:24.374UTC /18:32:24.374MSK: streamed installation reports `Success`.
-15:32:25.695UTC /18:32:25.695MSK: Appium calls `ime enable io.appium.settings/.UnicodeIME`.
-15:32:26.020UTC /18:32:26.020MSK: Android returns exit255, `Unknown input method io.appium.settings/.UnicodeIME cannot be enabled for user #0`.
- First createSession returned HTTP500 after4.106s. The planned3cycle loop stopped at this first creation failure; no subsequent command/quit cycles claimed.
- Immediately after uninstall, ime-list briefly retained the previous UnicodeIME entry; after install/failure it no longer listed it. Therefore an immediate post-uninstall list can be stale and is not proof of current working registration.
- Final read-only checks show Settings3.4.0 installed, firstInstallTime/lastUpdateTime18:32:24MSK, UnicodeIME absent from ime-list, ADB `device`.
- Machine logs exclusively from Loki: `{instance="M-K0058",job="integrations/journal",unit="android-session-canary-20261109e.service"}`,120entries, no1000-entry cap hit. Sanitized generated results at `~/ai-data/android-dig/session-canary-20261109/results-settings-reinstall.jsonl` and `loki-settings-reinstall.json`.

## Findings
Confirmed controlled regression: working UnicodeIME and3passing sessions before removal; targeted uninstall plus normal successful same-version reinstall then reproduced the original session-creation error without Grid routing or parallel sessions. Reboot recovery was temporary with respect to this preparation behavior. This establishes the destructive helper lifecycle as a reproducible trigger on this Xiaomi; the internal Android/MIUI reason for missing InputMethodManager registration remains unproven. It does not establish the cause of busy ports/unknown sessions on other farm devices.

## Changes and final state
Only the approved Settings uninstall/reinstall and isolated diagnostic session attempt. No second reboot performed. Zero remaining sessions, no Xiaomi ADB forward,15903/16003listeners absent, temporary Appium stopped. Production `phone_redmi_note_13_pro.service` remains inactive; Xiaomi is still outside Grid and currently has the reproduced IME defect. Other devices unchanged by the agent. All task background exec sessions completed.

## Status and next decision
Test completed, regression reproduced. Central [TODO](../../../../TODO.md), android-farm section, tracks preserving Settings during preparation as a proposal and recovering/revalidating Xiaomi before any separately approved Grid return. Existing successful-recovery observations remain historical, superseded by this controlled regression. No permanent CI/helper-script fix, new recovery reboot or production return executed. Recommendation is to avoid routine uninstall/reinstall of Settings, preserve the working helper, and validate compatibility/reinstallation as a separately controlled operation rather than every-job cleanup. Repository edits retain branch/base and publication approval gates.

## Portable lesson
none

## Superseding Xiaomi recovery — 2026-11-09 18:57 MSK

User-approved reboot followed by3UnicodeIME-enabled serial cycles passed with existing Settings3.4.0; production Appium started and Xiaomi registeredidle in Grid. Earlier isolated/broken state is historical. See [recovery and limits](2026-11-09-android-farm-devops-912-xiaomi-recovered.md).
