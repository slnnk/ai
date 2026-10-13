---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [elasticsearch, cinder, vk-cloud, filesystem]
---
# DevOps-894 thin seed filesystem formatted; mount and fill prepared

## Summary

User explicitly approved formatting ONLY the5GiBthin Cinder seed disk. Guarded format completed asext4,LABELes-base-thin,UUID `70806792-9f23-4776-8367-60b857a2c384`. Thick filesystem, root staging copies, mounts andfstab remain untouched. Prepared/reviewed next mount/fill script, with actual read-only preflight0; apply is awaiting separate approval.

## Task and context

[DevOps-894](https://youtrack.youdo.com/issue/DevOps-894); [disk/mount preflight](2026-10-13-nomad-test-devops-894-seed-disk-preflight.md). User answeredyes to the specificthin-format proposal, not mount/fill/fstab/cloud-snapshot changes. VM10.18.26.4 `vk-ms1-share-test01`; executed viaSSHyoudo→sudo.

## Actions and key commands

Ran ai-sync (no output). One approved remote invocation repeated host, stable-device→/dev/vdb, exact5368709120-bytecapacity, nomount and nosignature guards before `mkfs.ext4 -L es-base-thin /dev/disk/by-id/virtio-ad66e572-b39a-4ed7-8`. Freshblkid verifiedext4,label and UUID. Remote operationexit0. Noformatforce flag, no40GiBdisk orroot changes.

## Verified filesystem

ThinCinderUUID `ad66e572-b39a-4ed7-86a6-eb5a094763cb`,5GiBceph-hdd/MS1,filesystemUUID `70806792-9f23-4776-8367-60b857a2c384`. Remains unmounted. ThickCinderUUID `6b8a8094-227f-4eb2-968c-5469e98fd92c`,40GiB,existingfilesystemUUID `6b64dbf7-0b64-420c-8633-83ba496ff363` stillmounted/public.

## Next reviewed operation (not executed)

Rewrote local `~/ai-data/nomad-es-vk-transfer/prepare_seeds.py` to preserve the historical ES mount paths. Default mode is read-only; `--apply` performs no formatting. Scope of the proposed single invocation:

1. Move existing system-disk datasets to `/data/elastic-staging/{thin,thick}` on the same rootfilesystem; retain both copies.
2. Unmount existing40GiBdisk from/public; mountthin/thick at `/data/elastic/thin` and `/data/elastic/thick` using verified stable paths/UUIDs. No source backup container stop needed.
3. Save `/etc/fstab.devops-894-before-es-seeds`, atomically replace ONLY the old thick/public entry and addtwoESUUIDentries, preserving other rows and file ownership/mode.
4. Populate seed filesystem roots from retainedstaging usingrsync,numericowners,excludinglost+found andheapdump; verifychecksum/metadata match. Keep staging andfstabbackup for recovery.

Plannedfstab rows:
```text
UUID=70806792-9f23-4776-8367-60b857a2c384 /data/elastic/thin ext4 defaults,nofail 0 2
UUID=6b64dbf7-0b64-420c-8633-83ba496ff363 /data/elastic/thick ext4 defaults,nofail 0 2
```

Actualdefault-mode preflight onshare exited0 and confirmed source data remains on `/dev/vda1`, matchingcloudvolumes/filesystemUUIDs, empty/public exceptlost+found/noactiveusers, noexistingstaging/backup, and expectedfstab/publicentry. Local syntax/help andfourfstabchecks passed: preserve unrelatedroot row and setcorrectESUUIDs; rejectforeignsource,duplicate/publicentries and existing conflictingESpaths. No success claims for the unappliedoperation. The reviewed command is `ssh -o BatchMode=yes -o ForwardAgent=no -o ConnectTimeout=10 -o StrictHostKeyChecking=yes youdo@10.18.26.4 sudo -n python3 - --apply < ~/ai-data/nomad-es-vk-transfer/prepare_seeds.py`.

## Changed files and risks

Actualremotechange: thinblockvolume filesystem created; existing prior absence ofsignatures verified beforedestructiveaction. Localhelper/KB updated. No repository files/branch, existingthickformat, fstab, mounts, targetdata, sourcecontainer orcloudresource changed. Nextoperation can leave partial mounts/fstab/copies onfailure; it retainsoriginalstaging andfstabbackup, and rejectsblindreruns. Anyfailure must be inspected before newchanges. Snapshots andrestoredESboot remain future separatelyauthorizedsteps.

## Portable lesson

none
