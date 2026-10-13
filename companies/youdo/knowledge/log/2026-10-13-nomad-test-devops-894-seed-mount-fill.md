---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [elasticsearch, cinder, vk-cloud, filesystem]
---
# DevOps-894 ES seed disks mounted and filled from retained staging

## Summary

User explicitly requested executing allfour reviewed mount/fill steps. Completed onVKshare10.18.26.4: preserved rootstaging datasets in `/data/elastic-staging/{thin,thick}`, mounted5/40GiBCinderseeds at historical `/data/elastic/{thin,thick}`, saved/replaced the relevantfstabentries byUUID, filled bothfilesystems and verified checksum/metadata equality. Operationexit0; `seeds_prepared=true`, `staging_retained=true`. Independent mount/fstab/staging verification passed. No snapshot/ESstartup/cloudresource/repo changes performed.

## Task and authorization

[DevOps-894](https://youtrack.youdo.com/issue/DevOps-894), [format/operation review](2026-10-13-nomad-test-devops-894-thin-format.md). User instruction “execute allfourpoints” covers the described staging preservation, mount changes, fstabsave/update, copy and checksum verification. It does not authorize snapshots, cloning/ESjob launch, staging deletion or repository publication. The thin filesystem was already formatted under separate priorapproval; this operation performs noformatting.

## Actions and key command

Ran ai-sync (no output). Executed `ssh -o BatchMode=yes -o ForwardAgent=no -o ConnectTimeout=10 -o StrictHostKeyChecking=yes youdo@10.18.26.4 sudo -n python3 - --apply < ~/ai-data/nomad-es-vk-transfer/prepare_seeds.py`. Remotepreflight0 confirmed source directories onroot, expected5/40GiBvolume/device/filesystemUUIDs, empty/public exceptlost+found, noactiveusers and expectedfstab/publicrow.

Moved system-disk datasets to `/data/elastic-staging/thin` and`thick`, without deleting contents. Unmounted thick from/public. Mountedthin/thick at their historicalESpaths and checked actualdevices beforecopy. Saved `/etc/fstab.devops-894-before-es-seeds`, preserved otherfstabrows/mode/owner, replaced oldthick/publicrow with ESUUIDrows. Copied fromretainedstaging via `rsync -aH --numeric-ids --delete --exclude=lost+found --exclude=java_pid1.hprof`, then comparedchecksum/metadata with dry-run while noESwriter exists onshare. Temporaryread-only size/phase monitor stopped aftercompletion.

## Verified final layout

| Variant | Cinder ID | Device | Filesystem UUID | Persistent mount |
| --- | --- | --- | --- | --- |
| thin | `ad66e572-b39a-4ed7-86a6-eb5a094763cb` | `/dev/vdb` | `70806792-9f23-4776-8367-60b857a2c384` | `/data/elastic/thin` |
| thick | `6b8a8094-227f-4eb2-968c-5469e98fd92c` | `/dev/vdc` | `6b64dbf7-0b64-420c-8633-83ba496ff363` | `/data/elastic/thick` |

Bothvolumesceph-hdd/MS1 inCSIproject `6929552e493f46b899798519f279be0b`, onshare `vk-ms1-share-test01`UUID8e8a992d-a7c5-4c90-b472-dbbcae2cce0c. Bothfilesystemsext4. Stagingcopy `nodes` directories remain onroot `/dev/vda1`. `/public` is now an ordinaryrootdiskdirectory, no longer a dedicatedmount; nofiles werepresent onoldthickfilesystemexceptlost+found beforeuse.

Fstab entries:
```text
UUID=70806792-9f23-4776-8367-60b857a2c384 /data/elastic/thin ext4 defaults,nofail 0 2
UUID=6b64dbf7-0b64-420c-8633-83ba496ff363 /data/elastic/thick ext4 defaults,nofail 0 2
```

## Checks and results

Thin:120572815literalbytes,3872regularfiles,3971entries,0deletions; checksum/metadata comparison no differences, `checksum_verified=true`. Thick:22667132593literalbytes,5342regularfiles,5441entries,0deletions; copy~72.6MB/s; checksum/metadata comparison no differences, `checksum_verified=true`. Finalhelper output `seeds_prepared=true`, `staging_retained=true`,fstabbackup path; completeSSH/script exit0. Checksumphase waited forstorageI/O; no correctnessfailure reported.

Independent read-only `findmnt` verification matches exactpath/device/ext4/UUID pairs. Stagingbothnodes directories exist onroot. Fstab matches expectedtwoUUIDrows with `defaults,nofail 0 2`; backup exists, and comparing withbackup proves all unrelatedrows preserved. No dedicated/publicmount remains. No reboot orESstartup performed/claimed; targethas noDocker.

## Changed files and risks

Remote changes: stagingdirectory moves, thin/thickmounttable, `/etc/fstab` anditsbackup, bothCinderseedfilesystemcontents/metadata. Retainedrootcopies forrecovery. No backupsourcecontainers changed inthisstage. NoCloudPOSTexceptpreviouspreflightauth, snapshot, newvolume, Nomadjob, repositoryedit orGitpublication. Snapshotcreation still needs cleanlyquiescedfilesystems and separatelyapprovedaction; restoredESindex validity still unverified. Do not delete retainedstaging untilclone/ESvalidation is reviewed.

## Portable lesson

none
