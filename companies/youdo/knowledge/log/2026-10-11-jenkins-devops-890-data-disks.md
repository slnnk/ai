---
system: jenkins
status: verified
checked: 2026-10-11
tags: [recovery, disks, approval]
---
# DevOps-890: Jenkins data disk preparation

## Task

Proceed to stage 2 of DevOps-890: prepare the secondary disks for controller/agent. The user's instruction authorizes preparation and inspection; their global rule still requires approval before each command modifying a remote VM. Publication remains deferred.

## Context

- [Recovery plan](2026-10-10-jenkins-devops-890-recovery-audit.md); [completed stage 1](2026-10-11-jenkins-devops-890-inventory-dependencies.md).
- Controller root@10.16.28.8, instance fhm4ftsgv29i98121g9a; secondary disk fhmdpb2gokdnv6n4272h, serial matches, /dev/vdb, 161061273600 bytes (150 GiB).
- Agent root@10.16.28.26, instance fhmoo7mfbchbet7pak4f; secondary disk fhm6c0201e8kqngbjcu1, serial matches, /dev/vdb, 10737418240 bytes (10 GiB).

## Actions

Read-only YC instance GET and root SSH lsblk/wipefs/findmnt/fstab inspection on both hosts. Prepared local reviewed operation `/home/slnnk/ai-data/jenkins-recovery/prepare-data-disk.sh`; bash syntax check passed. No remote modifying command executed at this checkpoint.

## Findings

Both selected secondary disks have no partitions, filesystem signatures or mounts. /data is absent; fstab contains only boot root/EFI mounts. Controller root disk serial fhmid37u9acmbj1r493t (20 GiB) and agent root serial fhmo9rohopabc4voj0h9 (10 GiB) are distinct from target disks.

The preceding findings describe the initial read-only preflight; both disks were subsequently formatted/mounted under separate explicit approvals, as recorded below.

## Changes

Local operation script checks root identity, hostname, disk serial, exact byte size, absence of partitions/signatures/mounts and existing /data/fstab entries immediately before changes. On approval it backs up fstab, runs mkfs.ext4 without force, creates /data, appends UUID-based ext4 defaults entry, verifies fstab, mounts only /data and verifies UUID/type/capacity. It does not start services, reboot or modify boot disks.

Proposed first command (controller only):

```bash
ssh -o BatchMode=yes -o ForwardAgent=no root@10.16.28.8 'bash -s -- yc-a-jenkins-test fhmdpb2gokdnv6n4272h 161061273600' < /home/slnnk/ai-data/jenkins-recovery/prepare-data-disk.sh
```

User approved the controller command with "Выполни". It ran successfully (exit0) after an outside-sandbox retry; the initial sandbox call could not connect and made no remote change. The guarded operation was independently reviewed before approval.

Controller result: /dev/vdb is ext4, UUID `4163bab1-c2db-47ab-9d06-735de2a6d5ff`, mounted read/write at /data; df reports147G total,140G available. fstab contains `UUID=4163bab1-c2db-47ab-9d06-735de2a6d5ff /data ext4 defaults 0 2`. Original fstab backup is `/etc/fstab.devops-890.20261010T213227Z.bak` (111 bytes). Independent read-only SSH verification confirmed mount, UUID, fstab and backup; root remains /dev/vda1. fstab verification returned0 errors and one warning: systemd retains its prior configuration until daemon-reload or reboot. No daemon-reload or reboot was executed; a runtime manager refresh requires a separately approved command.

User separately approved agent preparation with "Да". Executed the same guarded script on root@10.16.28.26 with hostname yc-a-jenkins-agent-test-01, serial fhm6c0201e8kqngbjcu1 and exact size10737418240. Initial sandbox SSH was denied before connecting; outside-sandbox retry completed exit0.

Agent result: /dev/vdb is ext4, UUID `29f70714-aea1-4217-b197-463b9182d4f9`, mounted read/write at /data; df reports9.8G total,9.3G available. fstab persists the UUID-based ext4 defaults entry; backup `/etc/fstab.devops-890.20261010T213358Z.bak` is111 bytes. Independent read-only SSH verification confirmed mount/UUID/fstab/backup and root remaining on /dev/vda1. fstab verification has0 errors and the same systemd stale-configuration warning.

Proposed next action, separately awaiting approval: one Ansible invocation on the explicit two-host recovery inventory to run only `ansible.builtin.systemd_service daemon_reload=true`. Installed ansible-doc confirms no service name/state is needed and no service start/stop is requested. list-hosts confirms only the new controller/agent. This refreshes systemd's fstab-generated mount configuration. No task commit, push or MR.

```bash
ansible jenkins-yandex -i inventories/yandex/jenkins-recovery.ini -m ansible.builtin.systemd_service -a 'daemon_reload=true'
```

User approved this two-host daemon-reload with "да". The initial sandbox attempt could not connect; outside-sandbox execution succeeded on both hosts. The module reported SUCCESS/changed=false; independent verification provides the runtime evidence: data.mount is active/mounted, generated from `/run/systemd/generator/data.mount`, `NeedDaemonReload=no`, source /dev/vdb and destination /data on both. `findmnt --verify --tab-file /etc/fstab` reports no errors or warnings on each host; mounted UUIDs still match the controller/agent values above. No service start/restart or reboot was requested. Stage2 disk preparation is complete; data restoration has not begun.

## Risks

Formatting cannot restore previous disk data; the safety gate is fresh identity/emptiness checks. A partial failure after formatting must be inspected before retry; the script deliberately refuses existing signatures rather than formatting again. Source backup and root filesystem remain untouched. Open recovery work is tracked in ~/ai/TODO.md.

## Portable lesson

none
