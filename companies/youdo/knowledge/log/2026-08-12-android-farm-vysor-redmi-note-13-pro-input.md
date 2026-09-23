---
system: android-farm
status: verified
checked: 2026-08-12
tags: [android, vysor, adb, miui, redmi, input, adbinput]
---
# Vysor: no control of Redmi Note 13 Pro while the stream is running

## Task

Restore Vysor/ADB input control of the Redmi Note 13 Pro farm device whose screen streams fine but ignores clicks and keys.

## Context

- Date: 2026-08-12
- Android farm host: `root@192.168.30.147`, hostname `M-K0058`
- Device: serial `x4pf5l5haegykni7`, model `23117RA68G` / Redmi Note 13 Pro, Android 13, MIUI 14 (`V14.0.5.0.TNFRUXM`)
- ADB: `/root/Android/Sdk/platform-tools/adb`; device configuration: `/opt/adb/redmi_note_13_pro.json`

## Findings: symptom and cause

Vysor connects and shows the screen, but clicks and keys do not work. The device is present in `adb devices -l` with state `device`; USB and the video stream are fine.

The check `adb -s x4pf5l5haegykni7 shell input keyevent 0` returns `SecurityException: Injecting input events requires ... INJECT_EVENTS`. On MIUI the protected property `persist.security.adbinput=0` is set: the option "Отладка по USB (Настройки безопасности)" (USB debugging (Security settings)) is turned off.

An attempt to run `setprop persist.security.adbinput 1` from an ordinary ADB shell is rejected; there is no root (`su`) on the phone. Therefore the toggle has to be enabled locally on the phone screen.

## Open items: what to do

On the phone: `Настройки → Расширенные настройки → Для разработчиков → Отладка по USB (Настройки безопасности)` (Settings → Additional settings → Developer options → USB debugging (Security settings)). A Mi account, a SIM card and confirmation of warnings may be requested. The developer settings screen was opened remotely with the command:

```bash
/root/Android/Sdk/platform-tools/adb -s x4pf5l5haegykni7 shell am start -a android.settings.APPLICATION_DEVELOPMENT_SETTINGS
```

After enabling, check:

```bash
/root/Android/Sdk/platform-tools/adb -s x4pf5l5haegykni7 shell getprop persist.security.adbinput
/root/Android/Sdk/platform-tools/adb -s x4pf5l5haegykni7 shell input keyevent 0
```

Expected: property value `1`, no `SecurityException`, and control restored in Vysor. If Vysor does not pick up the change immediately, reconnect it to the device.

## Portable lesson

none
