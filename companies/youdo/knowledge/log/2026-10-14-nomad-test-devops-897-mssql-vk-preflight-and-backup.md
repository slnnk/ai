---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [mssql, vk-cloud, backup, airflow]
---
# DevOps-897: VK MSSQL image preflight and manual clean backup delivery

## Task

User requested read-only step1 of DevOps-897 (VK MSSQL image, VM/disk prerequisites and backup share). User then confirmed DBA_Clean as the probable delivery producer and explicitly requested manual backup delivery, directing reuse of the earlier ES transfer logs. Manual delivery authorization excludes VM creation, SQL restore, DAG triggering or repository changes.

## Context

Existing source helper /home/slnnk/ai-data/nomad-es-vk-transfer/transfer.py establishes backup-local root key and pinned VK host-key transport. Source root@172.24.0.19 reports hostname msk3-backup.youdo.corp; VK destination10.18.26.4 reports vk-ms1-share-test01. Existing [ES source evidence](2026-10-13-nomad-test-devops-894-es-source-check.md). All selected cloud checks are scoped GET requests after standard Keystone authentication.

## Actions

Ran ai-sync (no output); read current context/TODO/repos, delegated multi-file source/producer audit. Executed sanitized VK image/flavor/Compute limits/Cinder type+limit/Neutron subnet+security-group GET checks. Evidence /home/slnnk/ai-data/mssql-vk-dns/cloud-preflight.json. Read-only share SSH checked Samba export, path/file presence, disk capacity and service ports. Nomad agent01 TCP445 to share succeeded.

Source /backup/sql/test/CleanYouDo.bak stat:96708001792bytes (~90.1GiB), mtime2026-10-11 00:23:30MSK. Source mount /backup is ext4/md3, ~20TiBfree. No backup file contents downloaded locally.

Generated copy_backup.py under ai-data, reusing the exact public host-key pin from the proven ES helper. Initial transcription of the public key differed and strict checking rejected it; corrected by extracting the exact existing constant without weakening checking. Dry-run source-to-target preflight then succeeded. Target had234320269312bytes free, no final or partial file. Authorized apply created /public/sql and copied only to .CleanYouDo.bak.devops897.part. Source ES containers and other backups untouched. Initial transport evidence backup-transfer.log.

During transfer the user explicitly requested skipping checksum to launch sooner. Generated finish_without_checksum.py, identified the exact task rsync and Python-driver parent, suspended only the driver before its checksum phase while rsync continued uninterrupted. Waited for successful rsync exit, checked source size/mtime unchanged and destination size/mtime equal, renamed to CleanYouDo.bak, then terminated only the old paused driver. No copy restart and no checksum execution. Final evidence backup-finish-no-checksum.log confirms published/checksum_skipped=true/size_mtime_verified=true. Both SSH sessions completed.

## Findings

- Image yc-sql-base d840325b-16fd-4ff9-943d-9599b6bbf495 is active/private, owner matches project; created2026-10-13 18:30:49UTC, updated19:35:42UTC. Raw/bare, size and virtual_size429496729600bytes (400GiB), min_disk400GiB, min_ram0. Metadata os_type=windows, hw_disk_bus=virtio, hw_firmware_type=bios. Metadata does not prove VirtIO drivers, successful boot or SQL data date.
- Matching diskless flavors: STD3-4-8 ID3553977b-e3db-4ced-af76-dc30fd1f9eae and STD2-4-8 IDb95087f9-3a2f-4414-b068-7a01f982f960 (4vCPU/8192MiB). No flavor/type selected or VM created. Historical baseline4vCPU/8GiB/400GiB.
- Aggregate free quotas:103vCPU,239200MiB (~233.6GiB) RAM,15VM slots,3702GiB block storage and23volume slots. Four concurrent baseline VMs need16vCPU/32GiB RAM/1600GiB/4volumes. Aggregate headroom sufficient; per-volume-type quotas/AZ capacity not verified. Available types ceph-hdd,ceph-ssd,high-iops,high-iops-ha.
- Test subnet1e4f837d-d1df-4769-b661-6e0a56ff978b, network shared_network996906a7-99ca-42e7-a916-632cc7eb6a28, CIDR10.18.26.0/24, gateway10.18.26.254, DNS10.18.20.3, private DNS enabled. Security group test-internal90a05df6-da34-4928-b2f9-982ed51aab76 allows IPv4 protocol any from10.18.20.0/24,10.18.24.0/24,10.18.26.0/24; candidate for internal traffic, not yet selected/applied to SQL ports.
- No target vk-ms1-sql-base/test/test1/test6 VMs observed. Unrelated sql-report is outside task scope.
- Samba public is guest-enabled/read-write and exports /public/. /public is on root ext4/dev/vda1; about219GiB free before copy. /public/sql was absent; no CleanYouDo.bak found in bounded /public,/data,/backup search. smbd active and port445 listening, port873 not observed.
- Latest tracked DBA repo origin/master37d5330: DBA_Clean clean_rsync_to_test_yandex still deletes old /public/sql/CleanYouDo.bak and sends /backup/sql/test/CleanYouDo.bak to10.16.28.4::sql/. Legacy SQL procedure references old10.16.26.4 UNC, selecting latest YYYY_MM_DD folder then falling back to sql/CleanYouDo.bak. Manual VK delivery does not migrate producer or restore procedure. Deployed DAG/environment-selected Airflow connection not inspected; actual source file was verified through the existing ES route.

## Changes

Local generated helpers/evidence and knowledge bookkeeping; no repository changes. Authorized remote creation of /public/sql and successful one-time CleanYouDo.bak delivery. Final file96708001792bytes, mtime2026-10-10 21:23:30.638697941UTC (=2026-10-11 00:23:30MSK), mode0644, readable by youdo; temporary path absent. smbd active; root filesystem242GiB total113GiB used129GiB free after delivery. No source backup modification, SQL restore, VM create/delete, cloud quota changes or DAG execution.

## Risks and limits

Checksum was explicitly skipped by the user; transfer success is established by rsync exit0, unchanged source metadata, equal destination size/mtime and independent final SSH file inspection, not content-hash verification. SQL service identity SMB readability and RESTORE VERIFYONLY cannot be established without a guest/SQL check; metadata/file presence do not prove restore succeeds or database freshness. Existing samba-storage-vkcloud.yml expects old /dev/vdc mount at/public and conflicts with prior approved ES mounts, so it was not applied. DBA_Clean delivery and SQL restore UNC still need VK adaptation.

## Portable lesson

none
