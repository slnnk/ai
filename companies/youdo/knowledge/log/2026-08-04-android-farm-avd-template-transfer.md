---
system: android-farm
status: verified
checked: 2026-08-04
tags: [android, emulator, avd, sparse, fallocate, adb, nexus, nginx, ansible, adb_devices, appium, disk]
---
# Android farm: transferring an AVD template between hosts

## Task

Transfer the AVD `Nexus 5X Template` (Android 10 / API 29 / x86) from farm host `M-K0057` to `M-K0058`, free the full root disk on the source, publish a canonical AVD archive to Nexus, and then rebuild `M-K0058` through Ansible (`roles/adb_devices`). The note was kept as a running log from 2026-08-04 to 2026-08-13.

## Context

- Date: 2026-08-04
- Context: Android emulator farm, source host `192.168.50.108` (`M-K0057`), target host `192.168.50.116` (`M-K0058`), access as `root`.
- Object: AVD `Nexus 5X Template` from the screenshot, Android 10 / API 29 / x86.

## Findings: conclusion

An AVD can be transferred to another Linux host. On the source host, under `root`, its data is normally located in `/root/.android/avd/<name>.avd/`, and the registration file is `/root/.android/avd/<name>.ini`.

The target host needs:

- a compatible Android Emulator version;
- the same SDK system image (for this AVD: API 29 and the corresponding x86 image/tag; see `config.ini` for the exact parameters);
- hardware virtualisation/KVM for acceptable performance;
- corrected absolute paths in `<name>.ini` and, if present, in `config.ini`.

The AVD should be copied only after the emulator process has fully terminated. After the transfer, the first start is more reliable as a cold boot (`-no-snapshot-load`), because snapshots depend on the emulator version, the system image and the AVD settings. When transferring between different users, the path `/root/...` must be replaced with the actual home directory of the target user.

## Recommended process

1. On the source, determine the exact name with `emulator -list-avds` and the parameters from `config.ini`.
2. On the target, install the corresponding system image with `sdkmanager`.
3. Transfer the `<name>.avd/` directory and the `<name>.ini` file together, preserving sparse files (`rsync -aS`).
4. Check/fix the paths and perform the first cold boot.
5. For replication across the farm create a separate copy/name of the AVD on every node; keep in mind that a full clone preserves user data and identifiers inside Android.

## Next steps (initial assessment)

- On the source, the AVD `Nexus 5X Template` is registered by the file `/root/.android/avd/Nexus_5X_Template.ini`, and its data lives in `/root/.android/avd/Nexus_5X.avd` (8.5 GB). Internal `AvdId=Nexus_5X_Template`.
- Required image: `system-images/android-29/google_apis_playstore/x86/`; ABI `x86`, API 29, data partition 20G.
- Emulator on the source: `36.6.11.0`, build `15507667`, path `/root/Android/Sdk/emulator/emulator`.
- On the source the 98 GB root partition is 100% full; only `Nexus_5X_1` and `Nexus_5X_2` are currently running, the template is not started.
- On the target the architecture is `x86_64`, `/dev/kvm` is available, about 81 GB is free on `/`.
- On the target Android Studio `/opt/android-studio-2025.2.3/android-studio/bin/studio.sh` was found, but no Android SDK/Emulator and no AVD were detected under `root` or under local users. The same IDE version by itself does not install the SDK system image.
- Before the transfer, install on the target the Android SDK command-line tools, an Emulator of a compatible version and the package `system-images;android-29;google_apis_playstore;x86`, or carefully transfer a compatible SDK from the source.

## Findings: disk usage analysis of M-K0057

As of 2026-08-04 the root ext4 partition: 98 GB, 94 GB used, 0 available, 100% usage. Inodes are only 4% used; the problem is specifically data blocks.

Main consumers:

- `/root/.android/avd`: 72 GB;
  - `Nexus_5X_1.avd`: 34 GB;
  - `Nexus_5X_2.avd`: 30 GB;
  - template `Nexus_5X.avd`: 8.5 GB;
- `/root/Android/Sdk`: 3.9 GB (of which the needed API 29 system image is 2.4 GB);
- `/opt/android-studio-2025.2.3`: 3.3 GB;
- `/var/log`: 1.2 GB, mostly the unopened `/var/log/syslog.1` of 932 MB;
- `/var/cache/apt`: 606 MB;
- `/tmp`: 559 MB, predominantly copies of `gitlab_youdo_1.apk` left over from 2026-07-23 and later;
- `/root/.cache`: 313 MB, `/root/.npm`: 97 MB;
- systemd journal: 186 MB.

The main anomaly: `userdata-qemu.img` has a logical size of 20 GB in all three AVDs. In the template it is sparse and physically occupies about 136 MB, but in `Nexus_5X_1` and `Nexus_5X_2` each one physically occupies the full 20 GB. The ext4 UUID is identical, which matches their origin as clones; the sparse layout was probably lost during copying. The QCOW2 overlays additionally occupy 9.3 GB and 8.6 GB and contain the current device changes — they must not be deleted.

Recommendations:

1. Without stopping the farm: clean the APT cache (~606 MB), the old temporary APKs (~559 MB), rotate/compress `syslog.1` (~932 MB), and if necessary the user caches (~410 MB).
2. After a regular stop of each AVD, individually re-sparsify its `userdata-qemu.img` (for example in-place `fallocate --dig-holes`, with verification of the result and of start-up). Potential release — up to ~40 GB. Do not perform on a running QEMU and do not touch the `.qcow2` files.
3. The template's `default_boot` snapshot occupies 3.7 GB; it can be deleted only if the Quick Boot state is not needed and a cold boot is acceptable. For a transfer to another Emulator a cold boot is preferable anyway.
4. Configure a limit/rotation for syslog and periodic cleanup of temporary APKs, otherwise the small partition will fill up again.

The cause of the fast syslog growth is confirmed: both Appium instances (`emulator_1`, `emulator_2`, Appium 1.22.3) run with debug logging and write several lines roughly every 5 seconds for the health check `GET /wd/hub/status`. Over a week this produced a `syslog.1` of 932 MB. The Appium log level must be lowered/debug disabled, or these health-check records filtered out, and a stricter size-based rotation set for syslog.

## Actions: compaction of Nexus_5X_2

Date: 2026-08-04.

- Verified that there are no active Appium sessions.
- Discovered the actual mapping: AVD `Nexus_5X_2` uses `emulator-5554`, systemd unit `emulator_2.service`, but the associated Appium unit is named `phone_emulator_1.service` and listens on port 15001. The Appium and AVD names are cross-swapped; `phone_emulator_2` belongs to `emulator-5556` / `Nexus_5X_1`.
- `phone_emulator_1.service` and `emulator_2.service` were stopped normally; the absence of QEMU and of open files in `/root/.android/avd/Nexus_5X_2.avd` was confirmed.
- In-place compaction performed: `fallocate --dig-holes /root/.android/avd/Nexus_5X_2.avd/userdata-qemu.img`.
- The physical size of the backing file decreased from ~20 GB to 4.9 MB while the logical size of 20 GB was preserved.
- `/root/Android/Sdk/emulator/qemu-img check .../userdata-qemu.img.qcow2` completed without errors.
- Partition `/`: before the operation 100% and 0 free; after the operation 82% and 18 GB free.
- `emulator_2.service` started, `emulator-5554` reported AVD name `Nexus_5X_2` and `sys.boot_completed=1`.
- `phone_emulator_1.service` started; Appium 1.22.3 answers on `http://127.0.0.1:15001/wd/hub/status`.
- After boot the backing file kept its physical size of 4.9 MB.

## Actions: compaction of Nexus_5X_1

Date: 2026-08-04.

- Verified the absence of active Appium sessions on port 15002.
- Confirmed the mapping: `Nexus_5X_1` = `emulator-5556` = `emulator_1.service`; the associated Appium is `phone_emulator_2.service`.
- `phone_emulator_2.service` and `emulator_1.service` were stopped normally; the absence of QEMU and of open AVD files was confirmed.
- Ran `fallocate --dig-holes /root/.android/avd/Nexus_5X_1.avd/userdata-qemu.img`.
- The physical size of the backing file decreased from ~20 GB to 4.9 MB at a logical size of 20 GB.
- The `qemu-img check` of `userdata-qemu.img.qcow2` completed without errors.
- After the operation and start-up, free space on `/`: 39 GB, 59% usage (before compacting the two AVDs it was 100%).
- `Nexus_5X_1` booted (`sys.boot_completed=1`), Appium 1.22.3 answers on port 15002.
- Post-boot control: `emulator-5554` = `Nexus_5X_2`, `emulator-5556` = `Nexus_5X_1`; both backing files keep their sparse layout.

## Actions: template transfer to M-K0058

Date: 2026-08-04.

- On `192.168.50.116` confirmed `/root/Android/Sdk/emulator/emulator`, the system image `/root/Android/Sdk/system-images/android-29/google_apis_playstore/x86`, KVM and sufficient space.
- The template was stopped on the source; there were no open files.
- Performed a direct streaming transfer from M-K0057 to M-K0058 through GNU tar with `--sparse`, into a staging directory with an atomic move after successful extraction.
- On the target `/root/.android/avd/Nexus_5X.avd` and `/root/.android/avd/Nexus_5X_Template.ini` were created; `emulator -list-avds` shows `Nexus_5X_Template`.
- After the initial copy the sparse backing file physically occupied 136 MB at a logical size of 20 GB; `qemu-img check` of the QCOW2 passed without errors.
- The Emulator on the target is newer than on the source: 37.1.11 versus 36.6.11, therefore the Quick Boot snapshot was not used.
- The first smoke test revealed the missing SDK skin `nexus_5x`; the ~100 KB directory was transferred from the source to `/root/Android/Sdk/skins/nexus_5x`.
- After installing the skin the Emulator starts the AVD, but the ADB transport has state `unauthorized`: the template userdata trusts the ADB key of the source host, while the target has a different `/root/.android/adbkey`. The `-skip-adb-auth` parameter did not solve the problem on the Google Play user image.
- The smoke test was stopped; the template on the target was left switched off. After the trial cold boots the physical size of the AVD grew to 9.8 GB; 66 GB is free on the target.
- For headless/Appium operation it is necessary either to confirm the target's ADB key interactively in the dialog inside Android, or, with explicit permission, to transfer the trusted ADB key pair of the source farm host. Key values/contents were not copied into the notes.

## Actions: ADB key transfer and final check

Date: 2026-08-04.

- With the user's explicit permission the standard pair `/root/.android/adbkey` and `/root/.android/adbkey.pub` was transferred from M-K0057 to M-K0058.
- The target's previous pair was preserved in `/root/.android/adbkey-backup-20260804`; the directory has mode 700, the private key mode 600.
- Before installation the private/public parts were checked for correspondence without printing the contents. Secret values and fingerprints were not saved in the long-lived note.
- A direct start of a fresh AVD with the target Emulator 37.1.11 at first remained `unauthorized`, although the key files on the source and the target matched.
- Confirmed that on the source the same template with the current key gets ADB state `device`.
- For compatibility, the source Emulator 36.6.11 was transferred side by side, without replacing the target Emulator 37, into `/root/Android/Sdk/emulator-36.6.11` (819 MB). The system image on both nodes is revision 9.
- The AVD on the target was refreshed again from a clean source copy and then booted once with Emulator 36.6.11. Result: `sys.boot_completed=1`, ADB state `device`, Android 10 / API 29, Appium 1.22.3 on port 15001 answers.
- After this initialisation a repeated cold boot was performed with the standard `/root/Android/Sdk/emulator/emulator` 37.1.11: boot successful, ADB state `device`, AVD name `Nexus_5X_Template`, Appium active.
- After the check the template was stopped normally; `qemu-img check` found no errors. Final physical size of the AVD about 9.5 GB.
- The 9.8 GB test copy of the AVD created for rollback was deleted after the successful check; the canonical copy remains on the source. About 66 GB is free on the target.
- Result: `Nexus_5X_Template` on M-K0058 is ready to be started with the standard Emulator 37.1.11 and to work through Appium `phone_emulator_1.service` / port 15001 / `emulator-5554`.

## Actions: archive prepared for Nexus

Date: 2026-08-05.

- On M-K0057 `/root/android-avd-nexus-5x-template-api29-20260805.tar.zst` was prepared with mode 600.
- Included: the AVD template, the registration `.ini`, Emulator 36.6.11, platform-tools, the API 29 Google Play x86 system image revision 9, the skin `nexus_5x`, SDK licenses and the ADB key pair.
- The archive was created with GNU tar with `--sparse` and zstd level 6; zstd integrity and contents were verified.
- Size: 7,368,236,061 bytes (7.37 GB / 6.86 GiB). The SHA-256 is saved next to it in a `.sha256` of the same name; the value is not duplicated in the note.
- Nexus `raw-private` turned out to be available for anonymous listing and download. An unencrypted archive with a private ADB key must not be uploaded there.
- To finish, encryption of the archive with safe storage of the decryption key and Nexus credentials with PUT rights are needed. At the time of the check there were no suitable Nexus credentials in `~/ai/current/.env`.
- An external check of `https://nexus.youdo.com` without authorisation confirmed the download of an existing object from `raw-private` by direct URL (HTTP 206), as well as of the same object through the raw group `raw` (HTTP 206). The REST API `/service/rest/v1/assets` returns 404 from outside, but that does not protect known direct URLs. An archive with the ADB private key can be published there only in encrypted form.

### Attempt to prepare a safe AVD-only archive

Date: 2026-08-09.

- A new object `raw-private/android/emulator.tar.zst` was agreed, containing only the directory `/root/.android/avd/Nexus_5X.avd` — without the registration `.ini`, the Android SDK, the Emulator and the ADB keys. The `.ini` was to be generated from the role's Jinja template.
- The creation did not happen: a direct SSH connection to M-K0057 (`192.168.50.108`) returned `No route to host`; the checked routes through the Nexus/VPN gateway also gave no access to the office network.
- The subsequent check of the upload method to Nexus was interrupted by the user. There is no confirmation in the logs of the creation of `emulator.tar.zst`, of a checksum, or of an upload of the object to Nexus.
- Therefore the only confirmed existing archive on M-K0057 remains the one from 2026-08-05, `/root/android-avd-nexus-5x-template-api29-20260805.tar.zst`, which among other things contains the ADB keys. The actual state of the host should be re-checked before use.

### AVD-only archive created; upload through the proxy not completed

Date: 2026-08-13.

- On M-K0057 `/root/emulator.tar.zst` was created: 5,951,611,784 bytes, mode 600. The archive contains a single root directory `Nexus_5X.avd` (33 objects), without `.ini`, SDK or ADB keys; `zstd -t`, the contents check and the SHA-256 passed.
- The external upload to `https://nexus.youdo.com/repository/raw-private/android/emulator.tar.zst` was rejected by the reverse proxy with HTTP 413.
- The upload through `http://msk3-nexus.youdo.corp/...` reached nginx but ended with HTTP 500: nginx buffered the 5.95 GB request body in `/var/cache/nginx/client_temp` on the 9.8 GB root `/dev/vda2`. Zabbix recorded 0.88% free space on `/`; after the nginx temporary file was deleted the free space was restored.
- State of nexus-prod-01 after recovery: `/` 7.1/9.8 GB (77%, 2.3 GB free), `/data` 101/167 GB (64%, 58 GB free), no inode pressure, `/var/cache/nginx` about 4 MB. Nexus data is located at `/data/nexus/nexus-data`.
- The object `raw-private/android/emulator.tar.zst` is absent after the failed attempts (HTTP 404). The upload must not be repeated through nginx; direct access to the Nexus backend `127.0.0.1:8081`, moving the nginx client temp to `/data`, or disabling request buffering for this location is needed.

### AVD-only archive uploaded directly to the Nexus backend

Date: 2026-08-13.

- A temporary SSH tunnel to `nexus-prod-01:127.0.0.1:8081` was created; a small streaming PUT into the raw repository succeeded, the probe's contents were verified and the probe deleted.
- `/root/emulator.tar.zst` was streamed from M-K0057 directly into the Nexus backend, bypassing nginx. The Nexus root `/` stayed at 77% during the upload, the nginx cache at about 4 MB; the blob was written to `/data`.
- Published:
  - `https://nexus.youdo.com/repository/raw-private/android/emulator.tar.zst`
  - `https://nexus.youdo.com/repository/raw-private/android/emulator.tar.zst.sha256`
- The Nexus blob size matched the source: 5,951,611,784 bytes. The SHA-256 was computed directly on the blob at `/data/nexus/nexus-data/blobs/default` and matched the original checksum; the value itself is stored in the `.sha256` next to the object and is not duplicated in the note.
- The external URL was checked with a range request (HTTP 206); the checksum file downloads and matches. After the upload `/data` is 68% used (about 52 GB free), `/` — 77% (2.3 GB free).
- The temporary SSH tunnel was closed; the local intermediate files `/tmp/emulator*` were deleted. The original safe archive and checksum were left on M-K0057 for recovery/re-publication.

## Findings: Google account automation

- BrowserStack historically accepted a Google username/password through the `appStoreConfiguration` capability and prepared the Google Play login on a real Android device.
- According to the current official BrowserStack documentation this capability is deprecated since 2024-09-30; the ordinary Google login flow now has to be automated in the test code.
- For the local farm the equivalent supported approach: open the Android add-account UI through ADB and drive it with Appium/UiAutomator2, or sign in interactively once in the template. There is no direct standard ADB command for adding a Google account.
- Do not pass the password through Appium capabilities/CLI under the current debug logging; use a test account and secret storage, and take Google's 2FA/CAPTCHA and security challenges into account.

## Actions: M-K0058 full manual cleanup before Ansible automation

Date: 2026-08-06.

- With the user's explicit confirmation, on `M-K0058` (`192.168.50.116`) `emulator_1.service` and `phone_emulator_1.service` were stopped and disabled; Android Studio was terminated.
- The package `android-studio-2025.2.3` and the PPA file `/etc/apt/sources.list.d/maarten-fonville-ubuntu-android-studio-noble.sources` were removed.
- Removed: the Android SDK, Emulator and system images from `/root/Android`, the AVDs and all ADB keys/backups from `/root/.android`, the Android Studio config/cache, `/opt/adb` and the related systemd unit files.
- The global `appium@1.22.3` was removed through npm; Node.js/npm were kept.
- Removed the leftovers `/root/.emulator_console_auth_token`, `/tmp/android-root`, `/tmp/adb.0.log`, `/tmp/appium-emu36-status.json` and the transient unit `avd-template-smoke.service`.
- Java, KVM, VNC and the shared Java configuration `/root/.java` were deliberately kept for the subsequent automated installation.
- Control: no related processes, systemd units, dpkg packages or paths for Android/Studio/Emulator/Appium/ADB/AVD were found. About 84 GB is free on `/`, 11% usage.
- Next step: design the Ansible automation for installing Android Studio/SDK, creating the AVD and configuring the services on the clean M-K0058.

## Changes: Ansible Android SDK bootstrap prepared

Date: 2026-08-06.

- A separate `tasks/sdk.yml` was added to `roles/adb_devices`; at the time of writing the changes had not yet been deployed to M-K0058.
- Pinned: the official Android Command-line Tools 22.0 build 15859902 with SHA-256, SDK root `/root/Android/Sdk` and the API 29 Google Play x86 package set.
- Licenses are always accepted by the role through `sdkmanager --licenses`, without a separate feature flag, by the user's decision.
- Command-line Tools 22.0 require JDK 17; the role installs JDK 17 for the SDK tasks while keeping JDK 11 and the current `JAVA_HOME` of Appium 1.22.3 unchanged.
- The legacy skin `nexus_5x` is not installed: for the future headless AVD a skin resolution of `1080x1920` is set.
- Selective rollout: `ansible-playbook -i inventories/office/hosts adb_devices.yml --limit M-K0058 --tags android-sdk` performs only the SDK bootstrap and does not start the Emulator/Appium units.
- Syntax check and `--list-tasks` passed successfully.

## Actions: M-K0058 Android SDK deployed through Ansible

Date: 2026-08-06.

- Selective rollout `--limit M-K0058 --tags android-sdk` performed; the first full run was successful: `ok=14`, `changed=5`, `failed=0`.
- Installed: JDK 17.0.19, Android Command-line Tools 22.0, ADB/platform-tools 37.0.1, Emulator 37.1.11, platform API 29, build-tools 29.0.3 and `system-images;android-29;google_apis_playstore;x86`.
- Licenses accepted; `/root/Android/Sdk/licenses/android-sdk-license` is present. The SDK occupies about 3.7 GB.
- The first `get_url` did not work because of an incompatibility of the old Ansible HTTPS wrapper with the Python library (`CustomHTTPSConnection`/`cert_file`). The download was replaced with `curl` with SHA-256 verification.
- The first direct curl was reset by Google (`rc=35`, connection reset). HTTP/1.1, retry, resume and a connect timeout were added to the role; the next download and the SHA-256 check succeeded.
- A repeated run confirmed the idempotence of the dependency/directory/archive/extraction stages, but hung on the network call `sdkmanager --licenses`; the check was interrupted after five minutes. `timeout 300` was added to the role for the license check.
- Command-line Tools 22.0 warn that `sdkmanager` is deprecated in favour of the new `android sdk`, but the current commands keep working. The CLI migration should be considered as a separate change after the new interface stabilises.
- Control on the host: all required paths are present; AVDs not yet created; Emulator/Appium systemd units absent.

## Changes: M-K0058 Ansible automation of the Android emulator and Appium completed

Date: 2026-08-07.

- Automation of Android Studio, AVD, cold-boot smoke test, systemd emulator and Appium with a real UiAutomator2 smoke session was added to `roles/adb_devices`.
- Android Studio 2025.2.3.9 installed. AVD `Nexus_5X_1` created: Android 10 / API 29 / Google Play x86, RAM 8192 MB, skin 1080x1920, data partition 20G.
- By the user's explicit exception, the ADB host key pair from M-K0057 is stored in `roles/adb_devices/files/adbkey{,.pub}` and applied to all managed hosts. The key contents and fingerprint are not recorded in the note.
- For the headless ADB dialog `/opt/adb/authorize-emulator-adb.sh` was installed. Its call was added to the `ExecStartPost` of the emulator unit, so authorisation is performed on every start before the service becomes active.
- Working units: `emulator_1.service` (`emulator-5554`) and `phone_emulator_1.service` (Appium 1.22.3, port 15001). Appium uses UiAutomator2 systemPort 15901.
- The Appium systemd PATH was fixed: a single literal PATH is applied; the readiness helper additionally uses absolute paths of the system utilities. Service output is directed to the journal, the Appium log level lowered to warn.
- The control Ansible run of Studio/AVD/emulator/Appium finished with `changed=0`, `failed=0`. After a separate control reboot both units automatically became active, ADB returned `device`, Appium status — HTTP 200, a UiAutomator2 session was successfully created and deleted.
- The temporary compatible copy `/root/Android/Sdk/emulator-36.6.11` and the archive `/var/cache/android-sdk/emulator-linux_x64-15507667.zip` were removed from M-K0058 as unused; the role works with the standard Emulator 37.1.11.
- Main changes: `roles/adb_devices/{defaults,handlers,tasks,templates,files}` and `inventories/office/host_vars/M-K0058.yml`. Do not duplicate secret values in documentation or logs.

## Open items

- Nexus `raw-private` is anonymously downloadable by known URL; never upload an unencrypted archive containing the shared ADB private key.
- Large uploads through the Nexus nginx front end are blocked (HTTP 413 externally, HTTP 500 internally due to buffering on the small root filesystem) until the nginx client temp storage/buffering is fixed.
- The ADB host key pair shared across managed hosts lives in `roles/adb_devices/files/`; keep it out of notes, logs and public repositories.
- The 2026-08-05 archive with ADB keys still exists on M-K0057 (`/root/android-avd-nexus-5x-template-api29-20260805.tar.zst`).

## Portable lesson

- `~/ai/general/knowledge/android/emulator-avd-transfer-and-sparse-userdata.md`
- `~/ai/general/knowledge/nginx/large-put-upload-buffered-on-small-root-disk.md`
