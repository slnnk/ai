---
system: android-farm
status: verified
checked: 2026-08-12
tags: [android, appium, uiautomator2, tecno, hios, usf, miui, samsung, autofill, adb, selenium-grid, recovery]
---
# Android farm: Appium/device incident for report 3063278

## Task

Investigate the Appium/device failures behind Android test report `3063278` on farm hosts `192.168.30.147` (M-K0058) and `192.168.30.148` (M-K0057), recover the TECNO CM7 node, and follow up the reruns on branch `Test-7056`.

Date: 2026-08-12 (Europe/Moscow)

## Context and host map

- Investigation requested for Android test report `3063278`, test interval approximately 20:48–21:10 MSK.
- Root SSH access was used read-only; no services, sessions, devices, settings, or files on the farm were changed.
- `192.168.30.147` = `M-K0058`, 16 GiB RAM, root filesystem 28% used.
- `192.168.30.148` = `M-K0057`, 32 GiB RAM, root filesystem 71% used.
- Both hosts had very low load and ample available memory. No host resource exhaustion or relevant kernel USB disconnect/reset events were found in the incident window.
- Selenium Grid hub: `192.168.30.30:4444`.
- Appium is old on these hosts: Appium `1.22.3`, `appium-uiautomator2-driver 1.70.1`; platform-tools/ADB `37.0.1` on M-K0058.

## Device and Appium map

### M-K0058 / 192.168.30.147

- `15888255AE004773`: TECNO CM7, Android 16, Appium `phone_tecno_cm7.service`, port `15002`, UiAutomator2 system port `15902`.
- `RZ8R71ZRK8H`: Samsung SM-A125F, Android 11, Appium port `15004`.
- `x4pf5l5haegykni7`: Xiaomi 23117RA68G / Redmi Note 13 Pro, Android 13, Appium port `15003`.
- `emulator-5554`: Android 10 emulator. Emulator service is active but `phone_emulator_1.service` has been manually/inactively stopped since 17:39; port `15001` is not listening and the node is absent from Grid.

### M-K0057 / 192.168.30.148

- `5b2d4fe2`: Xiaomi 24115RA8EG / Redmi Note 14 Pro, Android 14, Appium port `15004`.
- `RZCY20AXJHN`: Samsung SM-A556E, Android 14, Appium port `15003`.
- `emulator-5554`: Android 10 emulator, Appium port `15001`.
- `emulator-5556`: Android 10 emulator, Appium port `15002`.
- `GHKBB23B15002735`: connected over USB for unrelated work. It is intentionally outside the Android/Appium farm scope; ignore its ADB state and do not include it in farm capacity or health checks.

## Confirmed root cause: TECNO CM7

- The report's `testOfferChangingCashToSbr` ran on TECNO CM7 and got `Could not proxy command to the remote server: timeout of 240000ms exceeded` twice.
- Appium journal confirms failed UiAutomator2 deletion at 20:49:02 because instrumentation had already crashed, and another 240-second proxy timeout ending at 21:01:25.
- TECNO logcat identifies the device-specific cause. The Transsion `com.transsion.usf` process (`Usf_Hiber`) freezes UID/package `io.appium.uiautomator2.server` roughly ten seconds after activity:
  - first observed freeze at 20:49:15;
  - second UiAutomator2 server started at 21:01:35 and was frozen at 21:01:45.
- At 21:01:35 Android force-stopped/restarted the UiAutomator2 server for new instrumentation, then `Usf_Hiber` froze the replacement again. This matches both test retries and explains why click, screenshot, page source, and device-info commands all stopped responding.
- Standard Android `deviceidle whitelist` already contains `io.appium.settings`, `io.appium.uiautomator2.server`, and `.server.test`; it does not prevent the proprietary Transsion freezer from acting.
- Hours later, Appium still reported the failed session as active and the host still had long-lived `adb shell am instrument` and logcat child processes. `/wd/hub/status` remained healthy, so a simple Appium-port health check cannot detect this failure.
- Appium has `--session-override`, but a subsequent session first tries to delete the stale session and can itself block for 240 seconds. Systemd `Restart=always` also does not help because the Appium Node process remains alive.
- There were no relevant USB disconnect/reset events, ADB remained `device`, `/data` was only 7% used, and the host was not resource constrained.

## Other report-related device findings

- Redmi Note 13 Pro (`x4pf5l5haegykni7`): the report screenshot is the HyperOS/MIUI control center. Device logs show a `control_center` SystemUI window present while the app was launched. The test helper only detects legacy notification-panel resource IDs and misses `miui.systemui.plugin`/new control center, so it did not close the overlay. This is a farm/test-session state reset problem, not an Appium daemon crash.
- Redmi Note 14 Pro (`5b2d4fe2`): Appium and UiAutomator2 stayed responsive; the app remained in `TourActivity` after the logged click on `Войти`. No Appium proxy timeout, ADB disconnect, host pressure, or app crash was found. Treat as UI transition/click flakiness and add a verified/retried transition rather than attributing it to the Appium host.
- Samsung A12, Samsung A55, and both M-K0057 emulators completed Appium commands. Their report failures are assertion/test-data/locator problems, not farm transport failures.

## Configuration and monitoring gaps

- TECNO node config advertises Android version `10.0` although the device is Android 16. Correct the Grid capability metadata to avoid incorrect scheduling/selection.
- Node health monitoring checks the Appium HTTP process, but not stale sessions, UiAutomator2 responsiveness, instrumentation age, foreground SystemUI overlays, ADB authorization, or Grid registration.
- `phone_emulator_1.service` on M-K0058 is enabled and has `Restart=always`, but a manual `systemctl stop` leaves it inactive indefinitely; the corresponding emulator remains running and consumes resources while providing no Grid capacity.
- Querying Appium `/wd/hub/sessions` exposes the full application-download capability URL, which contains embedded repository credentials. Do not log or publish that endpoint without redaction; rotate/remove embedded credentials and redact report capabilities.

## Open items: recommended remediation

1. Quarantine TECNO CM7 until Transsion/HiOS freezing is disabled for all Appium packages. Standard Doze whitelist is insufficient; validate the OEM USF/Phone Master/Battery Lab exclusion with a repeated UiAutomator2 command test lasting longer than the current 10-second freeze threshold.
2. After approved maintenance, terminate the stale TECNO session/instrumentation and restart `phone_tecno_cm7.service`; do not return it to Grid until the OEM-freezer test passes.
3. Add a watchdog that marks a node unhealthy/restarts it when an Appium session is old, `am instrument` exceeds a threshold, or a lightweight UiAutomator2 command cannot complete. `/status` alone is not sufficient.
4. Add a pre-session reset for physical devices: wake/unlock, `cmd statusbar collapse` or equivalent, verify the AUT is foreground, and clear unexpected system overlays. Extend the Java helper for modern MIUI/HyperOS resource IDs.
5. Decide whether M-K0058 `phone_emulator_1.service` should be running; if yes, start it and confirm Grid registration. Exclude out-of-scope USB device `GHKBB23B15002735` from Android-farm monitoring and capacity calculations.
6. Upgrade Appium 1.22.3 and its UiAutomator2 driver in a staged manner, especially for Android 16; keep one device/node as a canary and verify existing Android 10 emulators separately.

## Useful read-only checks

```bash
ssh root@192.168.30.147
/root/Android/Sdk/platform-tools/adb devices -l
systemctl status phone_tecno_cm7.service phone_emulator_1.service
journalctl -u phone_tecno_cm7.service --since '2026-08-12 20:40' --until '2026-08-12 21:20'
curl -s http://127.0.0.1:15002/wd/hub/status
# /wd/hub/sessions contains sensitive capabilities; redact before recording output.
```

## Recovery attempt: 2026-08-13

- `phone_tecno_cm7.service` was kept stopped/failed and the TECNO node was not returned to Selenium Grid.
- The stale UiAutomator2 instrumentation and Appium packages were force-stopped successfully.
- TECNO USF exposes a built-in hibernation configuration interface. Its active `whitePackages` did not contain `io.appium.settings`, `io.appium.uiautomator2.server`, or `io.appium.uiautomator2.server.test`.
- `pm disable-user` and `am force-stop` cannot stop `com.transsion.usf`: it runs as UID `system` and is persistently bound from `system_server`. The package was re-enabled after this reversible check.
- The documented USF `-hiber disable` and `-ability -disable -hiber` commands did not change `is_enabled_hiber`, which remained `true`.
- A validated copy of the dumped hiber JSON with all three Appium packages added to `whitePackages` was passed to `-load_config -hiber`, but a subsequent config dump did not contain the additions. Treat the hot-load attempt as not applied.
- A direct UiAutomator2 smoke test, isolated from Appium and Grid, returned one HTTP response and then timed out from about 10 seconds onward, reproducing the OEM freeze.
- The temporary smoke-test unit, instrumentation, and ADB forward were removed afterward. `phone_tecno_cm7.service` remained stopped/failed.
- Next step: on the physical phone, use TECNO Battery Lab/Phone Master to give unrestricted/background/autostart protection to all three Appium packages, then rerun the isolated smoke test for at least 60 seconds before starting the Appium service.
- Internet guidance for TECNO aggressive process killing was checked. On this device, background use and Phone Master Auto-start were already allowed for all three Appium packages; Battery Saver was off and the current battery mode was Balanced.
- The three Appium helpers were also tried through Phone Master App Booster. An isolated smoke test still failed: UiAutomator2 started at `15:34:04`, then USF changed UID `10303` (`io.appium.uiautomator2.server`) to `FrozenState` at `15:34:08`. HTTP stopped responding immediately afterward.
- App Booster therefore does not feed the effective USF hibernation whitelist for this instrumentation process. The temporary smoke unit and instrumentation were cleaned up; the Appium node remains stopped/failed.
- Decompilation confirmed that USF `-load_config` is gated by `PermissionUtils.isDebuggable()` and is a no-op on this production build (`ro.debuggable=0`). Updating the JSON via shell is not available without root/debug firmware.
- Viable next workaround: build a TECNO-only UiAutomator2 server/test pair under package IDs already present in the factory USF whitelist (for example `com.github.uiautomator` and `.test`), then use a TECNO-only copy/configuration of the driver and validate it before Grid registration. An Appium upgrade is still recommended for Android 16 compatibility, but changing versions alone retains the frozen `io.appium.uiautomator2.server` package ID and is not expected to fix USF.
- At user request, TECNO CM7 was rebooted on 2026-08-13 at `15:46:54` MSK. Android reported `sys.boot_completed=1` at `15:47:39`; ADB authorization returned successfully. Device uptime check confirmed a fresh boot and USF restarted with a new PID. The keyguard was showing after boot, `hiber` remained enabled, and `phone_tecno_cm7.service` remained stopped/failed, so the node was not returned to Grid.
- Post-reboot isolated smoke test also failed. USF logged UID `10303` entering `RunningState` at `15:53:28`, UiAutomator2 started at `15:53:29`, and USF moved the UID to `FrozenState` at `15:53:33` (`freeze uid: 10303 io.appium.uiautomator2.server`). HTTP answered once and then timed out. Reboot therefore does not synchronize Phone Master protected/autostart/background settings into the effective USF hiber whitelist. Test instrumentation and ADB forwarding were removed afterward; the Appium node remains stopped/failed.
- `pm disable-user --user 0 com.transsion.usf` succeeded before a reboot at `15:57:15`, but HiOS automatically restored the package to `enabled=1` during boot and restarted both `com.transsion.usf` and native `init.svc.hiber`. Package disable is therefore not persistent on this firmware.
- A more targeted `pm disable-user --user 0 com.transsion.usf/.UsfMainService` was rejected by Package Manager with `SecurityException: Shell cannot change component state`. The command aborted before its planned reboot, so no additional reboot occurred.
- Working remediation applied on 2026-08-13: `pm uninstall --user 0 com.transsion.usf`, followed by reboot at `16:00:04` MSK. This removed USF only for Android user 0; the factory APK remains intact at `/system_ext/priv-app/UsfApp/UsfApp.apk`.
- After boot, `com.transsion.usf` was absent from the user-0 package list, no USF process or `UsfMainService` was running. The native `init.svc.hiber` process remained `running`, but without the USF controller it did not freeze UiAutomator2.
- Direct UiAutomator2 verification passed for 60 seconds with consistent HTTP responses and no freeze log entries.
- A standalone Appium 1.22.3 canary (not registered in Grid) created a real session and completed 12 commands over one minute, all HTTP 200 in approximately 16–25 ms; the session was deleted cleanly.
- `phone_tecno_cm7.service` was started at `16:05:24` and registered in Selenium Grid as `REAL_DEVICE_15888255AE004773`. Grid immediately assigned queued work. Production observation for one minute showed a stable UiAutomator2 PID, active instrumentation, active Appium unit, no USF process, and no proxy/instrumentation/transport errors.
- Rollback if system side effects appear: `adb -s 15888255AE004773 shell cmd package install-existing --user 0 com.transsion.usf`, then reboot the device and revalidate. Stop `phone_tecno_cm7.service` before rollback so the device is removed from Grid.
- Remaining risk: removing the user-0 USF package may disable other TECNO power/network optimization behavior. Monitor general device stability, thermals, networking, and battery behavior. The native `hiber` init service still reports running even though the Java USF controller is absent.

## Live farm check: 2026-08-13 16:11–16:14 MSK

- M-K0058 (`.147`): TECNO CM7, Samsung A12, and Redmi Note 13 Pro had active instrumentation and responsive UiAutomator2 forwards (roughly 20–35 ms). All related Appium units were active. No current proxy timeout, instrumentation failure, device crash/ANR, OOM, or unrelated USB failure was found. Kernel USB disconnects in this interval corresponded to the intentionally rebooted TECNO.
- M-K0057 (`.148`): both emulators, Samsung A55, and Redmi Note 14 Pro had active new instrumentation and responsive UiAutomator2 forwards (roughly 5–54 ms). No current crash/ANR, kernel USB/OOM event, or transport timeout was found. `GHKBB23B15002735` is used for unrelated tasks and is excluded from farm checks.
- Previous sessions on all four M-K0057 nodes were cleaned up around `16:12` after inactivity. Three explicitly logged `New Command Timeout of 600 seconds expired`; cleanup then warned that instrumentation was already absent. Both emulator forwards were also already missing. Grid immediately created new sessions, which were healthy during the check.
- Interpretation: the M-K0057 event looks like sessions abandoned by the test runner/client without a timely `quit`, rather than simultaneous device or host failure. Follow up in the runner/report logs if these sessions correspond to unexpected test gaps; ensure `driver.quit()` runs in `finally` and consider a shorter stale-session watchdog.
- Follow-up at `16:17` MSK: all current UiAutomator2 forwards on `.147` and `.148` were responsive, all expected instrumentation processes were active, and no Appium units were failed. No new proxy, socket, ADB, or instrumentation errors were found. The first production TECNO session closed cleanly at `16:15:49` due to `New Command Timeout of 600 seconds`; Grid then started a new healthy TECNO session. This reinforces the test-runner/session-cleanup issue rather than a TECNO transport regression.

## TECNO stalled-test diagnosis: 2026-08-13 16:20–16:29 MSK

- Selenium Grid created TECNO session `e07364c6-c953-444d-ab4a-fc9bb31ba5c8`; the AUT was foreground in `com.youdo.authImpl.tour.android.TourActivity`, with no crash, ANR, keyguard, or system overlay.
- UiAutomator2 instrumentation remained alive. Read-only commands sent directly to the active Appium session succeeded: window size returned `1080x2301`, and page source returned a valid 9,041-byte hierarchy. This proves the Appium-to-UiAutomator2 command path was responsive after the USF remediation.
- The hierarchy exposed an enabled, displayed, clickable `Войти` element with resource ID `com.sebbia.youdo.test:id/authViaSmsButton`. A device screenshot also showed the normal first tour screen and visible green `Войти` button.
- Selenium Grid's `/grid/api/testsession` reported about 438 seconds of inactivity for the same session. The direct diagnostic calls bypassed Grid, so they did not invalidate that counter. The test client therefore created the session but sent no subsequent WebDriver command through Grid for more than seven minutes.
- Conclusion: this occurrence is not a TECNO click/input failure. The runner is stalled between driver/session creation and its first element lookup/action, or has abandoned the session. Inspect the corresponding runner/build log and thread state; ensure setup failures cannot bypass `driver.quit()`.
- No click was injected during diagnosis, to avoid changing the active test state. Do not infer command inactivity solely from the Appium journal while the node uses `--log-level warn`; use Grid inactivity metadata or temporarily increased logging in a maintenance window.

## GitLab rerun analysis: jobs 3064682, 3064994, 3065134

- GitLab project: `youdo/Test/youdo-android-testing`, project ID `69`; access token is stored only as `GITLAB_YOUDO_TOKEN` in `~/ai/current/.env` (value intentionally omitted here).
- All three jobs ran commit `d324ae8e` on branch `Test-7056`:
  - job `3064682`, pipeline IID `2201`: 39 tests, 13 passed, 17 failed, 9 skipped; duration about 42m40s;
  - job `3064994`, pipeline IID `2202`: 26 tests, 6 passed, 11 failed, 9 skipped; duration about 13m44s;
  - job `3065134`, pipeline IID `2203`: 20 tests, 0 passed, 11 failed, 9 skipped; duration about 3m53s.
- Job `3065134` is an infrastructure/network failure. Every attempted test failed at new-session creation because Appium could not download the APK: DNS lookup of `nexus.youdo.com` returned `getaddrinfo EAI_AGAIN`. There were no test actions or device-specific failures in this run.
- Connectivity was restored when rechecked: both `.147` and `.148` resolved `nexus.youdo.com` in about 20 ms and established HTTPS in about 40–50 ms. All three `.147` Appium units (TECNO CM7, Samsung A12, Redmi Note 13 Pro) were active and all in-scope USB devices were `device` in ADB.
- Samsung A12 `RZ8R71ZRK8H` was genuinely in landscape during jobs `3064682` and `3064994`: all 11 unique failure screenshots assigned to it were `1600x720`. This was not report rendering. Current system settings have auto-rotate enabled (`accelerometer_rotation=1`) and there is no test/session setup that forces portrait, so a physical/sensor rotation can persist through multiple tests. At the later live check the device had returned to `ROTATION_0` portrait.
- Xiaomi `x4pf5l5haegykni7` was repeatedly blocked by the expanded MIUI/HyperOS control center. In job `3064994`, all 8 unique Xiaomi failure screenshots ended at `Войти` not found; inspected screenshots show the control center fully covering the AUT. In job `3064682`, 13 of 14 unique Xiaomi failure screenshots had the same `Войти` symptom, and inspected early/late screenshots show the same control center from 16:23 through 16:34.

## GitLab rerun analysis: job 3065145

- Checked on 2026-08-13. Job `3065145`, pipeline IID `2204`, commit `d324ae8e`, branch `Test-7056`, stand `test6`: 20 tests, 4 passed, 7 failed, 9 skipped; job duration about 12m32s and test duration about 9m44s.
- One confirmed infrastructure failure occurred during the first attempt of `ProfileTestSuite.testRefillAccount`: Appium could not create a session on Redmi Note 13 Pro `x4pf5l5haegykni7`. Enabling `io.appium.settings/.UnicodeIME` returned `Unknown input method ... cannot be enabled for user #0`, causing `SessionNotCreatedException`. The Appium unit was `phone_redmi_note_13_pro.service` on M-K0058 (`192.168.30.147`, Kazan office).
- The failure was transient: a later retry ran on Samsung A55 and reached the application assertion. A read-only post-job check found `io.appium.settings` installed, `.UnicodeIME` registered, and the Redmi Appium unit active. The warn-level Appium journal records cleanup of a missing `systemPort` forward but does not contain enough detail to prove whether the helper installation raced Android package/IME registration. Treat it as an Appium/device-preparation defect; verify helper package and IME registration before admitting the node to Grid or retry session setup after reinstalling the helper.
- No Appium proxy timeout, UiAutomator2 crash, ADB offline/unauthorized state, runner failure, Nexus/DNS failure, host resource failure, HTTP 5xx, or artifact-upload failure was present in this job.
- The other final failures reached responsive devices and produced screenshots/page source. They are application/test/state issues rather than transport infrastructure:
  - registration through VK: first attempt reached an external browser warning page; retry remained on onboarding because the login transition did not complete;
  - account refill: balance became 500 but the expected refill operation row was absent for the selected date range;
  - basic 25-response package: expected price `4,680` no longer matches the visible `5,150` price;
  - profile share: Android system share sheet opened, but the test searched for literal text `Поделиться`, which is absent on the inspected OS variants;
  - unsuccessful refill: both attempts remained on onboarding after the `Войти` action;
  - package purchase with sufficient balance: both attempts reached payment flow but the expected `Оплачено` state did not appear;
  - uninsured SBR executor: first attempt could not find the response button; retry reached the T-Bank card form, where the generic native `EditText` locator did not find the visually present card field.
- The job infrastructure itself completed normally: runner started without queue pressure, reports/cache/artifacts/JUnit were uploaded, and the job failed solely because Gradle reported failing tests.
- Security observation: an HTML test log contains a push-notification token in a logged API payload. The value was not copied into this note. Redact notification/device tokens during report generation and review retention/public-read exposure of these artifacts.

### Samsung A12 card-scan autofill popup

- The `Сканировать новую карту` popup in `testUninsuredExecutorSelectionTaskSBR` is Android Autofill UI supplied by Google Play Services, not part of the T-Bank page. Page source identifies `android:id/autofill_dataset_picker`, `android:id/autofill_dataset_list`, and package `com.google.android.gms`.
- Read-only device inspection on Samsung A12 `RZ8R71ZRK8H` confirmed the active service is `com.google.android.gms/.autofill.service.AutofillService`; `dumpsys autofill` records requests from the YouDo test package.
- On a dedicated test device it can be disabled globally with `adb shell settings put secure autofill_service null`, followed by `adb shell cmd autofill reset`; restore with `adb shell settings put secure autofill_service com.google.android.gms/.autofill.service.AutofillService` and reset cached sessions. Verify with `settings get secure autofill_service` and `dumpsys autofill` before rollout.
- Existing `BaseScreen.closeAutocompleteSettingsIfNeeded()` detects `android:id/autofill_dataset_list`, but its dismissal is defective: it obtains absolute pixel coordinates and passes them to `clickByCoordinates(double,double)`, which interprets arguments as screen multipliers and multiplies them by width/height again. This explains why the popup remained and obscured the underlying WebView hierarchy. Fix the helper or disable Autofill during device preparation.

#### Autofill disabled across the farm: 2026-08-13

- At user request, Android Autofill was disabled and cached Autofill sessions were reset on all eight currently connected farm devices in the Kazan office:
  - M-K0058 / `192.168.30.147`: TECNO CM7, Samsung A12, Redmi Note 13 Pro, and `emulator-5554`;
  - M-K0057 / `192.168.30.148`: Redmi Note 14 Pro, Samsung A55, `emulator-5554`, and `emulator-5556`.
- Verification on every target returned `settings get secure autofill_service` = `null` and `dumpsys autofill` cached services = `none`.
- Unrelated USB device `GHKBB23B15002735` was not connected during the rollout and remains outside farm scope.
- Persistence was added to `/home/slnnk/git/automation-services/roles/adb_devices/templates/adb.sh.j2`: for every connected device the preparation script now sets `secure.autofill_service` to `null` and calls `cmd autofill reset`.
- Repository validation passed: `bash -n`, `git diff --check`, and `ansible-playbook -i inventories/office/hosts adb_devices.yml --syntax-check`. Syntax check retains the repository's pre-existing warning about invalid characters in group names.
- The Ansible role was not rolled out to the hosts in this step; only the device settings were applied live and the repository template was changed. Existing unrelated dirty-worktree changes were preserved.
- The Xiaomi issue persisted after the jobs: live `dumpsys window` showed `mCurrentFocus=... control_center`. Samsung also had `NotificationShade` focused at the time of the live check, demonstrating that system UI state is not reset reliably between sessions.
- The project does contain host-level preparation in `.gitlab-ci.yml`: for every host in `APPIUM_NODES`, CI invokes `/opt/adb/adb.sh` and `/opt/adb/adb_pkg.sh uninstall $PACKAGE`. The role template `automation-services/roles/adb_devices/templates/adb.sh.j2` disables accelerometer rotation, sets `user_rotation=0`, grants permissions, and removes Appium helper packages.
- However, this preparation did **not** run on M-K0058 (`.147`), which hosts Samsung A12 and Redmi Note 13 Pro. All three job traces contain `bash: /opt/adb/adb.sh: No such file or directory` and the same error for `adb_pkg.sh`. A live filesystem check confirmed that both files are absent on `.147`; Samsung and Xiaomi both still had `accelerometer_rotation=1`.
- M-K0057 (`.148`) had `/opt/adb/adb.sh` deployed and matching the role template. The job trace's subsequent `Success` results are consistent with preparation continuing on the other host. `adb_pkg.sh` was absent during the later live check and should also be reconciled with the CI contract.
- `.gitlab-ci.yml` appends `|| true` to every restart and preparation SSH command. This masks missing scripts and lets tests start on unprepared devices. Thus the immediate cause of the Samsung orientation issue in these jobs is a deployment/configuration drift on `.147`, not an absence of intended CI preparation.
- Even when deployed, the current script does not wake/unlock devices, collapse notification/control-center panels, or verify the focused unobscured AUT. `BaseScreen.closeNotificationsPanelWithCheckVisible()` checks only three legacy SystemUI resource IDs documented for Android 6/7 and is invoked only from the `MainScreen` constructor, so modern MIUI `control_center` is not detected.
- Recommended fix: restore the role-managed scripts on `.147`, reconcile `adb_pkg.sh` on both nodes, and make CI fail fast when preparation is missing or fails. Extend preparation to wake/unlock, collapse system panels, normalize portrait with a verified postcondition, and verify that the AUT is focused. Keep the UI-level panel closer as a fallback for modern MIUI/HyperOS and Samsung SystemUI.
- At user request on 2026-08-13 17:43 MSK, the current role template `roles/adb_devices/templates/adb.sh.j2` was copied to M-K0058 (`.147`) as `/opt/adb/adb.sh`, owned by `root:root` with mode `0755`. Source and destination SHA-256 matched (`916d94c4...f561`). The script was not executed during this deployment, so active Appium sessions and device state were not disturbed.

## Portable lesson

- `~/ai/general/knowledge/android/tecno-hios-usf-freezes-uiautomator2.md`
