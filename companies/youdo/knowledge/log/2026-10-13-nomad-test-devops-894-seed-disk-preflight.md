---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [elasticsearch, cinder, vk-cloud, ansible]
---
# DevOps-894 existing Cinder seed volumes and historical mount layout

## Summary

User requested the next DevOps-894 stage and supplied the original Yandex disk screenshot. Existing VK share already has the intended Cinder seed disks: `vk-ms1-share-base-thin`5GiB and `vk-ms1-share-base-thick`40GiB, bothceph-hdd/MS1, in the CSI project. New disks are unnecessary. Historical Ansible explicitly mounted ES volumes at `/data/elastic/thin` and `/data/elastic/thick`; keep those paths in VK. Preflight only: no formatting, mount, seed fill or snapshot operation performed.

## Task and context

[DevOps-894](https://youtrack.youdo.com/issue/DevOps-894), [migration plan](2026-10-13-nomad-test-devops-894-elasticsearch-vk-plan.md). Both [thin](2026-10-13-nomad-test-devops-894-thin-transfer.md)/[thick](2026-10-13-nomad-test-devops-894-thick-transfer.md) cold copies reside on share system disk. Next-stage instruction permits preparation/read-only work; specific destructive formatting and remote mount/copy/fstab commands still require reviewed approval under user rules.

## Actions

Ran ai-sync (no output), delegated multi-file cloud-helper and historical mount-code reads. SSHyoudo→sudo read `lsblk`, disk signatures, usage/mounts, metadata UUID, fstab, stable disk paths and `/public` process users. Issued an explicitly approved temporary Keystone auth token; credentials read from Vault `secret/admin/vk-csi` and held in memory. Cinder/Nova GETs matched server/volumes/types/quotas/snapshots; no cloud resource mutation. No auth response, credential or private key persisted.

## Verified VK identities

Server `vk-ms1-share-test01`,10.18.26.4,UUID `8e8a992d-a7c5-4c90-b472-dbbcae2cce0c`,ACTIVE/MS1. Project `6929552e493f46b899798519f279be0b`,RegionOne, matches CSI credential scope.

| Role | Cinder ID/name | Host device/stable path | State |
| --- | --- | --- | --- |
| thin | `ad66e572-b39a-4ed7-86a6-eb5a094763cb`, `vk-ms1-share-base-thin` | `/dev/vdb`, `/dev/disk/by-id/virtio-ad66e572-b39a-4ed7-8` | 5GiB,ceph-hdd,in-use onshare; no signatures or mount |
| thick | `6b8a8094-227f-4eb2-968c-5469e98fd92c`, `vk-ms1-share-base-thick` | `/dev/vdc`, `/dev/disk/by-id/virtio-6b8a8094-227f-4eb2-9` | 40GiB,ceph-hdd,in-use onshare; ext4mounted/public |
| root | `3ad9df36-d3e7-4050-b193-0748166aed17`, `boot-vk-ms1-share-test01` | `/dev/vda` | 250GiB,ceph-hdd,bootable; staging files onrootpartition |

Thick filesystemUUID `6b64dbf7-0b64-420c-8633-83ba496ff363`. `/public` contains only `lost+found`,0regularfiles at top level;~37.1GiBfree, no users per`fuser -m` (rc1). Existingfstab: `UUID=6b64dbf7-0b64-420c-8633-83ba496ff363 /public ext4 defaults 0 2`. Absence of user files is not implicit authorization to reformat; thick FS can be retained and remounted at its historical ES path. Thin wipefs--no-act reports no signatures; format still requires explicit approval.

Quota observations:49/90volumes,3763/8500GiB,0/200snapshots,0reserved relevant entries. No existing snapshots of the selected disks or ES-base-named snapshots. These are observations, not permissions/backend snapshot success guarantees. ceph-hdd is the intended base type; previous DevOps-893 smoke proved ceph-ssd only. HDD snapshot restore/CSI consumption still need a real test.

## Historical layout evidence

User screenshot shows Yandex `share-test01`, `yc-csi-es-base-thin`5GiBHDD, `yc-csi-es-base-thick`40GiBHDD and250GiBbootdisk inru-central1-b. It proves the original disk identities/sizes, not guest availability or mount state.

`automation-services/playbooks/yandex-test/yandex_share_mount.yml:41-48` mounts `/dev/vdb` at `/data/elastic/thick`;`:56-63` mounts `/dev/vdc` at `/data/elastic/thin`, bothext4. Persistentfstab entries at`:65-81` use `defaults,nofail`. `yandex-tf/test-infra/data.tf:19-25` selects the same named disks; attachment order in`compute-share-test.tf:36-43` isthickfirst/thinsecond. This establishes intended historical mapping. Current VK device order is reversed; use verified Cinder IDs/stable paths/UUIDs instead of copying olddevice names.

DBA_Clean only specifies rsync destination paths, not mounts. Historical `/public` is a separate Samba share in`automation-services/inventories/yandex/group_vars/share-test:13-14`; it is not the old ES volume path. Terraform's mount-playbook reference is commented out; automatic execution not established. Old mount playbook's `findmnt` failure checks can fail before mounting an initially unmounted device; do not execute it blindly.

## Proposed next actions and changes

First proposed destructive action: format ONLY the verified5GiBthin volume asext4, command `sudo -n mkfs.ext4 -L es-base-thin /dev/disk/by-id/virtio-ad66e572-b39a-4ed7-8`, after rechecking stable mapping, capacity, signatures and absence of mounts. Approval not yet obtained. This leaves rootstaging data and40GiBthick filesystem untouched.

Then review a mount/data-fill operation preserving rootstaging copies: move them to a separate staging path (same filesystem, no deletion), mount thin/thick volumes at `/data/elastic/thin` and `/data/elastic/thick`, replace the old thick/public fstab entry and add thin byUUID, copy staging datasets into volume roots excludingheapdump andlost+found, checksum-verify. Keep staging copies until ES/clone validation succeeds. Changes to mounts/fstab/data writes require explicit approval before execution. No source backup container stop required for these localstaging-to-seed copies.

Local provisional helper `~/ai-data/nomad-es-vk-transfer/prepare_seeds.py` initially proposed `/mnt/es-base-thin` plus existing/public. Historical discovery supersedes that layout; `--apply` is now disabled before any remote changes. It must be rewritten/reviewed before use. Only local draft/KB files changed; no repo training branch approved or edited.

Later user explicitly approved ONLY formattingthin. Executed guarded `mkfs.ext4 -L es-base-thin` on stable5GiBdevice; verifiedfilesystemUUID `70806792-9f23-4776-8367-60b857a2c384`,TYPEext4,LABELes-base-thin. No mount or data-fill/fstab action performed. Helper subsequently rewritten to the historical/data/elastic paths with no formatting; actual read-only preflight exited0. [Format and next-step review](2026-10-13-nomad-test-devops-894-thin-format.md).

## Risks and limits

Mounting over current data paths would hide system-disk copies; preserve/move staging first. Do notformat thick orroot. Snapshot publication requires cleanly quiesced seed filesystems and separate approval; no snapshot or restored ES verification performed. Preparation disks already exist, so current stage adds no storage capacity or new cloud resources.

## Portable lesson

none
