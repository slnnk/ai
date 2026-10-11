---
system: jenkins
status: verified
checked: 2026-10-11
tags: [recovery, backup, restore, approval]
---
# DevOps-890: backup transfer and restore

## Task

Begin stage3 of DevOps-890: transfer and restore the validated Jenkins backup before controller provisioning. User authorized preparation with "Начинай"; modifying commands still require explicit action approval under global instructions. Publication remains deferred.

## Context

- [Plan](2026-10-10-jenkins-devops-890-recovery-audit.md), [completed disk stage](2026-10-11-jenkins-devops-890-data-disks.md).
- Source root@msk3-backup02.youdo.corp `/data/backup/jenkins-test/jenkins_20261007.tar.gz`; destination root@10.16.28.8.
- Restore home must be `/data/jenkins/data/jenkins`; archive prefix is `data/jenkins/`.

## Actions

Fresh read-only controller checks confirm expected /data UUID4163bab1-c2db-47ab-9d06-735de2a6d5ff,149327106048 bytes available, only lost+found present; no Docker, active Jenkins service or Java process. Both Jenkins home and staging directory are absent.

Delegated read-only source metadata inspection and SHA256 calculation. Latest archive remains October7; compressed1532460486 bytes, expanded regular-file bytes3273951444 (3.049GiB),72925 entries/69970 regular files. No absolute/traversal paths, outside-prefix entries or external symlink/hardlink targets. Controller config, credentials, key files, jobs, plugins and AutoTest node configuration are present. Private SSH key mode0600 and known_hosts files0600; values never printed.

## Findings

Selected archive SHA256: `699f78d187419d4f1b401d2c8da2c0144eba4082877b882f49551d00e84041dd`. Target capacity comfortably accommodates the compressed archive plus expanded contents. Source is to remain untouched; no localhost archive copy is needed.

## Changes

Prepared local operation `/home/slnnk/ai-data/jenkins-recovery/transfer-jenkins-backup.py`. Default invocation performs only plan/shell-syntax validation. `--apply` streams source SSH stdout into receiver SSH stdin, creates controller `/data/jenkins-recovery` mode0700 and archive `.partial` mode0600, then verifies exact size/SHA before final rename. Receiver checks hostname, mounted data UUID/type, capacity, absent Jenkins home/staging and inactive processes/services. Independent review found fail-open status checks; fixed them so inspection errors abort rather than implying no service/container.

Proposed modifying command, pending explicit approval:

```bash
python3 /home/slnnk/ai-data/jenkins-recovery/transfer-jenkins-backup.py --apply
```

This action creates only the protected staging directory and archive on controller. It does not extract data, start Jenkins, alter source backup, change routing or publish code. Extraction will be a separate reviewed action after destination checksum/structure verification. No remote modifications occurred in this stage yet.

User approved the transfer with "Сделай". Sandbox attempt failed to establish either SSH connection; outside-sandbox retry is transferring data. Receiver has created the protected staging directory and `.partial` file. Read-only progress snapshots showed90046464 and699023360 bytes; final checksum/rename still pending at this checkpoint. Independent re-review confirmed corrected process/container guards.

Prepared next local operation `/home/slnnk/ai-data/jenkins-recovery/restore-jenkins-backup.sh`, pending separate extraction approval. It requires the final archive/hash/size, expected /data UUID, absent destination and stopped Jenkins; performs gzip test, extracts only data/jenkins/ with original ownership/modes, verifies nested home/config/keys/AutoTest/version and reports metadata/counts. No Jenkins startup or backup deletion. Bash syntax and independent review passed; reviewer used a harmless synthetic fixture to verify GNUtar recursive directory selection and0600 preservation without touching real data.

Transfer completed exit0 under the user's approval. Final destination `/data/jenkins-recovery/jenkins_20261007.tar.gz`,1532460486 bytes,root:root0600; staging directoryroot:root0700. Receiver SHA256 matched expected source. Independent read-only SHA256 computation after completion returned the same699f78d187419d4f1b401d2c8da2c0144eba4082877b882f49551d00e84041dd. No partial file remains, /data/jenkins is still absent,138GiB available. Source backup unchanged and no local archive copy created.

Next modifying operation, pending separate approval:

```bash
ssh -o BatchMode=yes -o ForwardAgent=no -o ConnectTimeout=8 root@10.16.28.8 'bash -s' < /home/slnnk/ai-data/jenkins-recovery/restore-jenkins-backup.sh
```

Scope: restore only /data/jenkins from the validated archive, retaining archive and preserving owners/modes; verify required files and counters, leave Jenkins stopped.

## Restore approval and result (October 11)

User explicitly approved the proposed extraction command with "Сделай". The sandbox attempt failed before connection; the identical outside-sandbox command completed exit0. It extracted only `data/jenkins/` into `/`, retaining the archive and original ownership/modes. Required Jenkins configuration, credentials, both encryption files and AutoTest node configuration are present. Restored version marker is2.555.1, with11 job configuration files and116 plugin archives; `/data/jenkins` occupies3.3GiB.

Independent read-only SSH verification completed exit0: required files are nonempty, counters/version match, SSH private key isroot:root0600, staging directory0700 and archive0600. Docker is still absent; no Java process or active Jenkins service exists. `/data` remains mounted from the expected ext4 UUID4163bab1-c2db-47ab-9d06-735de2a6d5ff, with135GiB available. Controller provisioning/start, agent configuration and routing remain pending separate authorization. No Git publication occurred.

## Risks

Post-extraction startup review parsed all11 job configurations: no XML TimerTrigger or SCMTrigger entries, restored queue has zero items, no builds marked running or resumable program.dat files. Built-in controller retains10 executors in NORMAL mode and can execute newly submitted jobs. Verified next controller-only command retains Vault/Jenkins tasks and skips monitoring deployment: `ansible-playbook -i inventories/yandex/jenkins-recovery.ini jenkins.yml --limit yc-a-jenkins-test --skip-tags zabbix-agent2,alloy`. It installs Docker/Compose, writes registry authentication and compose files, creates required directories/symlink and starts the selected controller image; not executed at this checkpoint.

Archive contains private Jenkins credentials/key material; staging permissions are deliberately restricted and secrets must not appear in outputs or notes. Failed transfer retains partial data for inspection and refuses unreviewed overwrite/retry. Global open recovery state lives in ~/ai/TODO.md.

## Portable lesson

none
