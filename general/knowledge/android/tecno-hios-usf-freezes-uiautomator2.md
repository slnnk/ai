---
system: android
status: verified
checked: 2026-08-13
tags: [android, appium, uiautomator2, tecno, transsion, hios, usf, process-freezing]
---
# TECNO/Transsion HiOS freezes the UiAutomator2 server about 10 s after start

## Symptom

On a TECNO (Transsion, HiOS) phone attached to an Appium node, every session works for roughly ten
seconds and then all commands hang: Appium reports
`Could not proxy command to the remote server: timeout of 240000ms exceeded` for click, screenshot,
page source and device-info; deleting the session also blocks for 240 s. Appium `/status` stays
healthy, `adb devices` shows `device`, USB and host resources are fine. Logcat shows the vendor
process `com.transsion.usf` (`Usf_Hiber`) logging `freeze uid: <uid> io.appium.uiautomator2.server`
and the UID moving to `FrozenState`.

## Cause

HiOS ships a proprietary process freezer ("USF"/hiber) that suspends background UIDs independently
of the standard Android Doze/App Standby machinery. The standard `deviceidle whitelist` already
containing `io.appium.settings`, `io.appium.uiautomator2.server` and `.server.test` does not stop it.
Things that do **not** work on production firmware (`ro.debuggable=0`):

- Phone Master "auto-start", "background", "App Booster" or Battery Lab exclusions (the effective
  USF `whitePackages` list is not updated by them);
- `usf -hiber disable` / `-ability -disable -hiber` (`is_enabled_hiber` stays `true`);
- `-load_config -hiber <json>` (gated by `PermissionUtils.isDebuggable()`, a no-op);
- `pm disable-user --user 0 com.transsion.usf` (re-enabled automatically on next boot);
- `pm disable-user --user 0 com.transsion.usf/.UsfMainService`
  (`SecurityException: Shell cannot change component state`);
- `am force-stop` (USF runs as UID `system`, bound persistently from `system_server`);
- rebooting.

## Fix

Remove the USF controller for the primary user only; the factory APK stays on the system partition:

```bash
adb -s <udid> shell pm uninstall --user 0 com.transsion.usf
adb -s <udid> reboot
# verify after boot
adb -s <udid> shell pm list packages --user 0 | grep transsion.usf   # empty
adb -s <udid> shell 'ps -A | grep -i usf'                              # no UsfMainService
```

Validate before returning the device to the pool: run an isolated UiAutomator2 instrumentation
(or an Appium canary session outside the Grid) and send commands for at least 60 s; previously it
stopped answering after the first ~10 s.

Rollback:

```bash
adb -s <udid> shell cmd package install-existing --user 0 com.transsion.usf
adb -s <udid> reboot
```

## Limits

- Native `init.svc.hiber` keeps running but without the Java controller it did not freeze the
  instrumentation in the observed case (Android 16, HiOS). Other firmware versions may differ.
- Removing USF may change power/thermal/network optimisation behaviour; watch battery, temperature
  and connectivity on the device.
- An Appium `/status` health check cannot detect this failure; monitor session age, `am instrument`
  process age or a periodic lightweight UiAutomator2 command instead.
- Alternative if uninstall is unacceptable: rebuild the UiAutomator2 server/test APKs under a package
  id that is already in the factory USF whitelist (for example `com.github.uiautomator`); upgrading
  Appium alone keeps the frozen package id and does not help.
