---
system: android
status: verified
checked: 2026-08-13
tags: [android, emulator, avd, sparse, fallocate, qemu, adb, kvm]
---
# Moving Android emulator AVDs between hosts and keeping userdata sparse

## Symptom

- An emulator host runs out of disk: every cloned AVD's `userdata-qemu.img` physically occupies its
  full logical size (for example 20 GB each) although the original template's image is only a few
  hundred MB on disk. `du` vs `ls -l` differ for the template but not for the clones.
- After copying an AVD to another host it boots, but ADB shows the transport as `unauthorized`
  forever, so Appium/headless use is impossible.
- After copying, the emulator complains about a missing skin or fails to load the Quick Boot snapshot.

## Cause

- `userdata-qemu.img` is a sparse file. Copying it with a tool that does not preserve holes
  (`cp` without `--sparse`, `scp`, `tar` without `--sparse`, some rsync invocations) materialises every
  zero block. The QCOW2 overlay (`userdata-qemu.img.qcow2`) holds the real changes; the base image is
  mostly zeros.
- The userdata of the template already trusts the ADB public key of the source host
  (`/root/.android/adbkey.pub`). The target host has a different `~/.android/adbkey`, so `adbd` in the
  image asks for interactive confirmation. `-skip-adb-auth` does not help on Google Play (user) images.
- Quick Boot snapshots are tied to the emulator version, system image revision and AVD config;
  skins referenced in `config.ini` live in the SDK (`$SDK/skins/<name>`), not in the AVD directory.

## Fix

Re-sparsify a bloated base image in place (emulator fully stopped, no QEMU process, no open files):

```bash
systemctl stop appium-for-this-avd.service emulator-for-this-avd.service
lsof +D ~/.android/avd/<name>.avd || true          # must be empty
fallocate --dig-holes ~/.android/avd/<name>.avd/userdata-qemu.img
$ANDROID_SDK_ROOT/emulator/qemu-img check ~/.android/avd/<name>.avd/userdata-qemu.img.qcow2
du -h --apparent-size ~/.android/avd/<name>.avd/userdata-qemu.img   # logical size unchanged
du -h ~/.android/avd/<name>.avd/userdata-qemu.img                   # physical size now MBs
```

Observed: 20 GB -> 4.9 MB physical per AVD, boot and Appium session unaffected. Never touch the
`.qcow2` overlay and never run this on a live QEMU.

Transfer an AVD preserving sparseness (both `<name>.avd/` and `<name>.ini`):

```bash
rsync -aS ~/.android/avd/<name>.avd ~/.android/avd/<name>.ini root@target:~/.android/avd/
# or streaming
tar --sparse -C ~/.android/avd -cf - <name>.avd <name>.ini | ssh root@target 'tar -C ~/.android/avd/.staging -xf -'
```

Then on the target: fix absolute paths in `<name>.ini` (and `config.ini` if present), install the exact
system image (`sdkmanager "system-images;android-29;google_apis_playstore;x86"`), copy the skin if
`config.ini` references one, and do the first start as a cold boot (`-no-snapshot-load`).

For headless ADB authorization either confirm the dialog once on the emulator screen, or (with
explicit approval, since it is a private key) install the same `adbkey`/`adbkey.pub` pair that the image
already trusts on the target host, back up the old pair with mode 600, and restart the ADB server.
If the new emulator version still shows `unauthorized`, boot once with the emulator version the image
was created with, then switch back; that initialised the trust in the observed case.

## Limits

- `fallocate --dig-holes` needs a filesystem with hole support (ext4, xfs); results persist across
  boots as long as the guest does not rewrite the zeroed blocks.
- A full clone keeps Android identifiers and user data; for a farm, create one renamed copy per node
  from a single template instead of cloning running instances.
- Emulator health-check logging (Appium `GET /wd/hub/status` at debug level every few seconds) can
  fill `/var/log/syslog` by hundreds of MB per week; lower the Appium log level to `warn`.
