---
system: automation-services
status: verified
checked: 2026-07-22
tags: [ansible, adb_devices, android, ca-certificates, adb]
---
# automation-services: adb_devices CA certificates

## Task

Add CA certificate installation (Russian trusted root/sub CA) for Android farm devices to the `adb_devices` Ansible role.

## Context

- Date: 2026-07-22
- Repository: /home/slnnk/git/automation-services
- Context: role adb_devices on Android runner hosts; ADB path is /root/Android/Sdk/platform-tools/adb.

## Changes

- Added explicit CA installation tasks to roles/adb_devices/tasks/ca.yml.
- Added defaults in roles/adb_devices/defaults/main.yml: adb_devices_adb_path, adb_devices_ca_workdir, adb_devices_ca_archives.
- Imported ca.yml from roles/adb_devices/tasks/main.yml with tags never and ca.

## Findings: behavior

- Downloads CA archives from https://gu-st.ru/content/lending/android_russian_trusted_root_ca.zip and https://gu-st.ru/content/lending/russian_trusted_sub_ca.zip.
- Extracts both archives under /opt/adb/ca/extracted.
- Converts valid PEM or DER X.509 files to Android system CA format using openssl subject_hash_old.
- Installs all prepared certificates to /system/etc/security/cacerts/ on every connected device reported by /root/Android/Sdk/platform-tools/adb devices with state device.
- Runs adb root, adb remount, adb push, chmod 644 and reboots each target device.

## Actions: run

ansible-playbook -i inventories/office/hosts adb_devices.yml --tags ca

## Verification

- Syntax check passed with ANSIBLE_LOCAL_TEMP=/tmp/ansible-local ansible-playbook --syntax-check adb_devices.yml.
- Task listing with --tags ca shows only CA tasks, all tagged ca and never.

## Open items: risks / TODO

- Devices must allow adb root and adb remount; regular non-root physical Android devices will fail at system CA installation.
- Emulator images may need to be started with writable system support for remount to work.

## 2026-07-22 follow-up

- Observed failure on M-K0043: adb root returned `adb: unable to connect for root: closed` and rc=1.
- Updated CA installation shell to tolerate adb root failure, wait for the device again, and let adb remount/push be the real failure point.
- This keeps rooted emulators working when adb root restarts/disconnects adbd, while still failing if system remount is not possible.

## 2026-07-22 user CA change

- Changed adb_devices CA installation from Android system store to user CA store flow for browser use.
- Removed adb root/remount/push-to-/system behavior from the install shell.
- New flow prepares .crt files, pushes them to /sdcard/Download/russian-ca, and opens android.credentials.INSTALL for each certificate on every connected adb device.
- Installation now requires UI confirmation on the device/emulator; adb cannot silently add user CA certificates on normal Android.
- Added defaults: adb_devices_ca_device_dir and adb_devices_ca_install_pause.

## Portable lesson

none
