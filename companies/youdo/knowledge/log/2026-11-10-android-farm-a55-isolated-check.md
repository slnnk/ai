---
system: android-farm
status: verified
checked: 2026-11-10
tags: [appium, adb, samsung, canary]
---
# Android farm: isolated Samsung A55 readiness and Appium canary

## Task and authorization
Work tracked as DevOps-914, as explicitly identified by the user on2026-11-10.

Following [job3287595](2026-11-10-android-farm-dig-job-3287595.md), the user reported stopping Samsung A55 Appium and requested a device check. Read-only investigation ran first. The agent presented a concrete three-cycle isolated create/command/quit probe, including possible UiAutomator2 helper installation, temporary keyboard changes, localhost-only Appium16003, production service staying stopped, and cleanup. The user explicitly approved: `Да, запустить проверку`. No reboot, broad reset, helper removal, production restart or Grid return was authorized.

## Context
M-K0057, current Enabled Selenium inventory fetched2026-11-10 12:01:37UTC, monitoring/SSH address192.168.30.31. Samsung A55 RZCY20AXJHN, actual model SM-A556E, Android15. Appium production15003/systemPort15903. Inventory-selected Hub192.168.30.30:4444 checked12:01:55UTC:7registered/7idle/queue0, A55 absent. [System map](../systems/android-farm/system-map.md).

## Actions
Used read-only SSH/ADB status and service/package/resource probes; no SSH/journalctl log reads. Machine logs queried exclusively through Loki. After approval ran the prepared local script over one SSH invocation, launching transient android-a55-canary-20261110 on127.0.0.1:16003 without Grid registration. Capabilities: exact UDID, UiAutomator2, systemPort15903, noReset=true, autoLaunch=false, skipUnlock=true, UnicodeIME enabled, resetKeyboard=true, installation timeout20000ms matching job default. Stop at first failed cycle, then close own sessions and stop the transient service. Postcheck at12:07:58–12:07:59UTC /15:07:58–15:07:59MSK.
Generated scripts/results are under ~/ai-data/android-dig/a55-check-20261110/. Script compiled locally before execution. No product APK download or launch.

## Findings
-12:03:24UTC /15:03:24MSK baseline: production service inactive/dead/MainPID0 since14:59:08MSK;15003/15903/16003 not listening; existing ADB server active. Device state device, sys.boot_completed=1, boot animation stopped. Android activity/package/settings/input_method/window services all found; read-only settings command works.
- Device memory available about4.45GB, /data10%used/about100.5GBavailable, battery84%,36.8C, USBpowered. Device uptime4228420s indicates no full kernel reboot in this observation; does not exclude historical Android framework restart. Current data does not implicate device disk/RAM exhaustion.
- io.appium.settings3.4.0/versionCode30 installed for user0 since14:00:27MSK; UnicodeIME registered. UiAutomator2 server4.27.0/versionCode95 installed, firstInstall14:41:19MSK, lastUpdate14:43:15MSK. Its test package io.appium.uiautomator2.server.test is absent. This is not the Xiaomi UnicodeIME-registration symptom.
- Android reports a staged mainline_train_primary system update ready=true/applied=false. Its causal connection to this incident is unknown; no apply, reboot or update change was attempted.
-12:06:09.223UTC /15:06:09.223MSK: first isolated session creation starts.12:06:33.810UTC /15:06:33.810MSK returns HTTP500 after24.587s. Direct Appium response: `adb -P 5037 -s RZCY20AXJHN install -r --no-incremental .../appium-uiautomator2-server-debug-androidTest.apk` timed out after20000ms. Session id absent. This reproduces device/helper installation failure without Grid, without parallel workers and with other production sessions excluded from the target. Three cycles were planned; only one was attempted because the first failed. No simple session command or successful quit cycle could be exercised.
-12:06:33.926UTC: Appium sessions0.12:06:33.942UTC: temporary service stop returned0.12:06:34.064UTC: production stillinactive. Final target ADB forwards empty;15903 absent. Postcheck12:07:59UTC confirms production inactive, no15003/15903/16003listeners, Android services stillfound, ADBdevice, settings/UnicodeIME preserved; server.test stillabsent. Main-server APK path changed during Appium initialization, consistent with helper reinstallation/update; settings package path unchanged. No full device reboot performed.
- Loki historical A55 service query corroborates job-time activity-service failures and transient device absence. Targeted `{instance="M-K0057",job="integrations/journal",unit="android-a55-canary-20261110"}` returned0entries twice after the isolated test; temporary-unit ingestion/label coverage is unverified. No host log fallback used. Canary verdict rests on direct Appium response and ADB/postchecks, not Loki silence.

## Verdict
Confirmed infrastructure failure remains reproducible on the isolated Samsung A55: UiAutomator2 instrumentation/test APK installation exceeds20s, blocking session creation. Read-only Android service responsiveness is insufficient to return it to the Grid. Exact cause of package installation delay is unproven; no claim of permanent failure, a necessary reboot, or successful recovery.

## Changes and remaining status
Updated this log, the existing map and central [android-farm backlog](../../../../TODO.md#android-farm). Existing Samsung proposal now records the approved canary result; preparation/memory/lifecycle proposals remain separate and open. Next proposed diagnostic is a separately approved bounded installation attempt with elapsed-time/installer-state evidence; a longer timeout must be treated as an experiment, not a proven fix. Production remains stopped, A55 outside Grid. All task commands completed; no task background operation remains.

## Portable lesson
none

## Installer diagnosis and user intervention — 2026-11-10 15:10–15:19 MSK

The user asked to continue diagnosis. Read-only device state at12:10:28UTC showed lockscreen/inputrestricted and focused PlayProtectDialogsActivity from com.android.vending; installd/package services responded and no target adb install client remained. A bounded direct installation of the identical733759-byte test APK was described and explicitly approved through the execution approval prompt; started12:12:44.632UTC. It waited beyond20s and60s and was bounded at120.177s/12:14:44.808UTC, killing only its own adb client. The test package remainedabsent and production Appium inactive. The Android installer request itself was not explicitly abandoned; do not infer that client timeout removes device-side pending state.

The agent separately requested permission to wake/unlock by swipe and inspect the hidden Play Protect dialog without clicking installation buttons or changing protection. User approved `Да, разблокировать и посмотреть`. After one wake/swipe the screenshot showed Google Play Protect for `io.appium.uiautomator2.server.test`: `Подозрительное приложение заблокировано`; explanatory text: `Это приложение было разработано для более ранней версии Android, поэтому в нем нет новых функций защиты конфиденциальности.` The dialog offered `Подробнее` and `OK`. Neither was clicked by the agent. This is direct evidence of the current test APK installation blocker, not just a slow transport hypothesis. Screenshot ~/ai-data/android-dig/a55-check-20261110/play-protect.png.

Read-only aapt2 metadata of the bundled APK: package io.appium.uiautomator2.server.test, targetSdkVersion30, compiled againstAPI30/Android11; device Android15. SHA256eb5e26c23cb3ea26663a40f06a9528c3647942c11391da72729280094cfa5116. Hash identifies the local artifact; no independent upstream authenticity check was performed. [Google developer guidance](https://developers.google.com/android/play-protect/warning-dev-guidance#android-app-compatibility-too-low-warning) describes the older-target privacy warning. This does not prove malicious code or explain every historical activity/settings-service disappearance. Historical staged system update remains unproven as a cause.

The user then reported `Я отключил play защиту`. This is a user-performed security-setting change; the agent did not disable Play Protect or other protection. Read-only postcheck showed a responsive launcher, no remaining own install client, and helper test package stillabsent. The same previously reviewed three-cycle isolated canary was explicitly reapproved through the execution prompt and rerun with the same20sinstall timeout, UnicodeIME enabled, noReset=true, autoLaunch=false and production Appium stopped.

## Final verified outcome — 2026-11-10 15:18–15:19 MSK

All three create/command/quit cycles passed with HTTP200 after the user's Play Protect intervention. Session creation times7.449s,4.749s,3.904s. Each GET window/current/size returned1080x2340 in7–11ms; quit times0.435s/0.418s/0.365s. Each immediate next create worked, and every quit released the target forward/systemPort15903. No sleeps between cycles. At12:18:30.794UTC: sessions0, forwards0, no15903listener, ADBdevice and UnicodeIME registered; transient Appium stop returned0, production unit remainedinactive. Final read-only postcheck confirms both UiAutomator2 server and test APK are installed, Android services respond, and15003/15903/16003 are not listening. All task processes finished; no task background operation remains.

This supersedes the earlier unresolved installation blocker: Play Protect prevented the test helper installation; after the user disabled protection, installation/session lifecycle succeeded with the original20stimeout. It does not establish a permanent fleet-wide fix, Grid-path or product-test success, or the cause of all historical Android service failures. User-disabled protection is a retained change/risk. No Grid return or production restart was authorized or performed. Central Samsung backlog retains the proposed production return/Grid verification as the remaining decision; no separate backlog was created. A supported Appium/UiAutomator2 upgrade may be considered separately to avoid relying on a global protection disable; no upgrade was implemented.

## User-started production return — 2026-11-10 15:22 MSK

User reported starting Appium. Read-only verification with fresh Enabled Selenium inventory: production phone_samsung_galaxy_a55.service active/running/MainPID933581 since15:20:00MSK. ADB RZCY20AXJHN device, Android activity/package/settings/input_method/window services found, no forwards. Hub snapshot12:21:57UTC /15:21:57MSK: A55 registered at M-K0057/192.168.30.31:15003, proxy API success, Appium ready, slotidle. Whole Grid8registered/8free/0busy, all8Appium statusesready. No new Grid session/product test created and no agent remote mutation performed during this check. This supersedes the intentionallystopped production state above. Samsung diagnosis, isolated3cyclevalidation and user-performed production return are complete; broader real-test/Grid lifecycle work remains in the existing separate central backlog proposal, with no new execution authorization. User-disabled Play Protect and unproven historical Android service-failure cause remain limitations. All check commands finished; no task background operations remain. Evidence: ~/ai-data/android-dig/a55-check-20261110/return-inventory.json, return-hub.json and return-device.jsonl.

## DevOps-914 comment publication — 2026-11-10

User approved the drafted recovery comment after explicitly removing its final paragraph about absent full autotest rerun, disabled Play Protect and future compatibility work. This is a task-specific wording decision; diagnostic evidence/limitations above are preserved. User explicitly requested posting the corrected comment. GET confirmed DevOps-914 `[Android] Восстановить устройство Samsung A55`, with no existing comments. Posted exactly the approved recovery text as comment74-125430; response text matched. No issue fields or status were changed. Publication receipt and approved body are stored under ~/ai-data/android-dig/a55-check-20261110/. No further publication action remains.

## User-confirmed task closure — 2026-11-10

After comment74-125430 publication, the user explicitly reported that DevOps-914 was already closed. Record task closure as user-confirmed; no independent issue-state query or external mutation was performed. The Samsung recovery entry in the central TODO is already checked and agrees with this closure. No further work is pending under DevOps-914; broader separately tracked farm tasks and historical verification limits are not reopened by this status update.

## Historical race backlog reconciliation — 2026-11-12

The user questioned whether the September8proposal to reproduce the A55 create/quit/create race was still relevant after the successful November10checks. It was an older separate central TODO entry left open despite the accepted recovery. The existing3/3immediate lifecycle cycles each released15903, production return was verified and DevOps-914 was user-confirmed closed. Closed that stale proposal as superseded and corrected the system-map current-problem wording. No additional reproduction or permanent September-race root-cause fix is claimed. The successful November9real job3285160 infrastructure review excluded the then-inactive A55, so it is not evidence of A55 stability; A55 closure relies on its own November10evidence. Historical incident details remain preserved. No external actions or background work.
