---
system: android-farm
status: verified
checked: 2026-11-09
tags: [appium, adb, unicodeime]
---
# Xiaomi UnicodeIME diagnosis and Appium isolation

## Task
User resumed diagnosis of `x4pf5l5haegykni7` after reporting Appium disabled, then explicitly requested starting TECNO and stopping the problematic device systemd unit. Investigation stayed read-only except these two specifically requested service changes.

## Context
M-K0058, verified SSH hostname, inventory/SSH IP `192.168.30.32`. Fresh Enabled Selenium inventory fetched 12:09:44 UTC, Hub checked 12:09:59 UTC /15:09:59 MSK.
Related [job3282427 report](2026-11-09-android-farm-dig-job-3282427.md) and [farm map](../systems/android-farm/system-map.md).

## Actions and evidence
- ADB get-state/getprop, package manager, IME lists/settings and dumpsys; read systemd properties, deployed preparation script and installed Appium source. Machine logs queried only through Loki; no SSH journal/logcat collection.
- Corrected an earlier agent factual mistake: `x4pf5l5haegykni7` is Xiaomi model `23117RA68G` / Redmi Note13Pro, Android13, MIUI `V140`, build `V14.0.5.0.TNFRUXM`. Its unit is `phone_redmi_note_13_pro.service`, Appium15003/systemPort15903. TECNO is the distinct UDID `15888255AE004773`, unit `phone_tecno_cm7.service`, Appium15002/systemPort15902. Direct evidence agrees with the existing Ansible device map.
- Before authorized switching, TECNO was inactive, stopped at15:07:32 MSK; Xiaomi Appium remained active with no systemd restarts and an ADB forward to15903. Hub had6busy slots, including Xiaomi and excluding TECNO. Thus the user's first manual stop had affected the other device.
- User request: start TECNO, stop the problematic device systemd. Executed `systemctl start phone_tecno_cm7.service` then `systemctl stop phone_redmi_note_13_pro.service` on M-K0058. Verified TECNO `active/running`, MainPID306889; Xiaomi `inactive/dead`, MainPID0. No enable/disable, reboot, helper installation/removal or test job mutation was performed by the agent.
- Xiaomi remained ADB `device`. Appium Settings `3.4.0`, versionCode30, installed/enabled for user0, neither hidden nor suspended. Both `.AppiumIME` and `.UnicodeIME` resolve as input methods. `.UnicodeIME` was enabled and selected; InputMethodManager reported it bound and system ready.
- Helper firstInstallTime/lastUpdateTime both `2026-11-09 14:14:16` device local time, after the investigated job ended14:09:48 MSK. Current healthy registration cannot reconstruct the earlier failure state.
- GitLab project69 latest100jobs showed job3282427 12:37:11–14:09:48 MSK followed by running3282724 starting14:09:50 MSK. No overlapping same-project job was found for3282427 in this bounded query. Other project/manual clients are not covered. Later helper installation is consistent with next-run preparation, but the installing actor is not established.
- Deployed `/opt/adb/adb.sh` prepares every authorized device on the host and uninstalls `io.appium.settings`, both UiAutomator2 helpers and the test APK. There is no per-device reservation/lock in this script. Ansible template has the same helper removal; deployed script additionally removes the test APK. `/opt/adb/adb_pkg.sh` is absent on this host; current inspected CI invokes only adb.sh.
- Installed Appium1.22.3/android-driver4.51.0 normally calls `pushSettingsApp` before `initUnicodeKeyboard`; the latter immediately enables/sets `.UnicodeIME` with no explicit wait for InputMethodManager registration. `skipDeviceInitialization` bypasses helper initialization. No such skip setting was found in the inspected local shared-client source. The real failed-session initialization path is not fully recorded.
- Inspected local checkouts without edits/fetch: automation-services `cedd1283487a6f49677c18ad53a5fd9325748fc6` (unrelated changes preserved), youdo-android-testing `91ce02f2e47e05f44d3fa8fea710dc57acc03e84`, autotest-core `e071a765bab7bff531af7a328aa40e3a7661daec`. They are supporting source context, not a claim that every file matches failed-job SHA `5cbe63fe`. CI uses15threads and host-wide preparation; shared client sets `unicodeKeyboard=true`.
- Targeted Loki operational query on `instance=M-K0058`, `unit=phone_redmi_note_13_pro.service` for09:27:11–11:19:48 UTC returned201matches for installation/IME keywords, consisting of repeated BaseDriver capability warnings rather than decisive installation/IME failure evidence. Warn-level service logging does not provide the package-manager/IME lifecycle needed to prove a race.

## Findings
Confirmed failure mechanism in job3282427: Android could not enable `.UnicodeIME` for user0 during session creation. It is device/Appium initialization, not lost ADB transport. Current package/IME state is healthy after a later reinstall. Exact historical root cause remains unproven. Candidate explanations are transient IME-registration timing after helper installation, or helper removal during another session; the latter is enabled by host-wide destructive preparation but no overlapping same-project job was found. Do not present these hypotheses as confirmed causes or perform speculative reinstalls.

## Changes
Only explicitly requested remote systemd start/stop, this note, identity correction in the job note and task-scoped TODO reconciliation. No repository edits or publication.

## Status and risks
TECNO restored; Xiaomi Appium isolated. Diagnosis finished with historical evidence limits. Returning Xiaomi to Grid or reproducing through install/uninstall/session creation requires an explicitly approved scoped experiment, detailed diagnostics and a restoration plan. Central [TODO](../../../../TODO.md), android-farm section, tracks the proposed controlled reproduction and preparation/session safeguards; prior deferral of diagnosis is superseded by this user's new request, while remediation remains unapproved.

## Portable lesson
none

## Later controlled reproduction — 2026-11-09 18:22–18:24 MSK

User approved proposed item1. Settings was absent again before the canary; Appium installed3.4.0 successfully, but InputMethodManager omitted UnicodeIME while PackageManager resolved the service, reproducing session creation failure without Grid or parallelism. Three serial create/command/quit cycles with diagnostic UnicodeIME bypass passed and released the port. Earlier healthy-IME observation remains historical. Production Appium remains stopped. See [canary evidence and limits](2026-11-09-android-farm-session-canary.md).

## Later recovery — 2026-11-09 18:29 MSK

User-approved phone reboot followed by Appium initialization recovered UnicodeIME without reinstalling Settings3.4.0;3/3cycles with unicodeKeyboardtrue passed. Earlier failed/absent-IME observations remain historical evidence. Production unit stays stopped, return-to-Grid remains proposed. See [reboot verification](2026-11-09-android-farm-xiaomi-unicodeime-reboot.md).
