---
system: jenkins
status: verified
checked: 2026-10-13
tags: [jenkins, recovery, vkcloud, DevOps-892]
---

# DevOps-892: Jenkins recovery plan on VK hosts

## Summary

Prepare recovery independent of unavailable Yandex infrastructure. Task: [DevOps-892](https://youtrack.youdo.com/youtrack/issue/DevOps-892), newly created by the user. Historical Jenkins notes incorrectly used DevOps-890, which is the Nexus recovery issue. No previous completion status applies to DevOps-892.

Root SSH is verified on both VK hosts after the explicitly requested public-key installation. Remote changes in this task were limited to adding the user's public key and setting root SSH directory/file ownership and permissions. No disk formatting, software installation, Jenkins startup, DNS change or build execution occurred.

## Context and verified state

| Component | Host / address | Verified state on October 13 |
| --- | --- | --- |
| Controller | vk-ms1-jenkins-test / 10.18.26.8 | Root SSH; RAM approximately 8 GB; root disk 20 GB with 17 GB free; /dev/vdb 150 GB, no filesystem signature reported; no /data mount; Docker absent; Python3 present |
| Agent | vk-ms1-jenkins-agent-test-01 / 10.18.26.26 | Root SSH; RAM approximately 16 GB; root disk 10 GB with 7.2 GB free; /dev/vdb 10 GB, no filesystem signature reported; no /data mount; Docker absent; Python3 present |
| GitLab / registry | registry.youdo.sg and gitlab.youdo.sg / 138.16.203.174 | DNS resolves from both hosts; registry HTTPS /v2/ returns 401, indicating reachable authentication endpoint; exact image tags/authentication not yet verified |
| Vault | vault.service.consul / 172.28.0.154 and 172.28.0.155 | HTTP health readable from both hosts; initialized=true, sealed=false; authenticated secret access not yet verified |
| Backup | msk3-backup02.youdo.corp / 172.24.0.18 | Root SSH verified from workstation; latest matching archive listed is jenkins_20261007.tar.gz, 1532460486 bytes |
| Public URL | build.youdo.sg / 178.154.207.53 | Still resolves to historical Yandex endpoint; independent replacement ingress required |

Backup directory is /data/backup/jenkins-test. Historical SHA256 for the October 7 archive is 699f78d187419d4f1b401d2c8da2c0144eba4082877b882f49551d00e84041dd; recompute before transfer and on destination. Matching size alone is not an integrity check. Changes after October 7 are outside this restore point unless another independently accessible backup is found.

## Recovery plan

### 1. Prepare approved configuration and independent dependencies

Use existing checkout /home/slnnk/git/automation-services. Propose branch DevOps-892-restore-jenkins-on-vk based on master; verify master contains required Jenkins recovery changes from MR !1368 before finalizing the base. Current checkout is DevOps-890-nexus-docker-auth with unrelated changes: preserve them and obtain explicit branch approval before repository edits or switching. No git mutation is authorized by this plan.

Build a task-local inventory limited to the two hosts, ansible_user=root, Python3 and host_type=jenkins / jenkins-agent. Reuse existing roles with the minimum necessary overrides. Review playbook selectors: jenkins.yml currently targets jenkins-yandex and includes Vault, monitoring and immediate container startup. Use VK Vault settings and an explicitly checked secret mapping instead of inheriting Yandex endpoints or vault_secrets['yandex'].jenkins_client_docker_pass. Check package repositories, registry authorization, controller-to-GitLab/Vault and agent-to-controller/registry connectivity. No role run until the restore/start order is safe.

Verify manifests for controller registry.youdo.sg/sysadmins/devops-tools/jenkins:2-555-1-2 and agent registry.youdo.sg/sysadmins/devops-tools/jenkins-agent:3355.v388858a_47b_33.6. Historical digests: controller sha256:6f80988c634047436ac35994bb37e54e6c3b61650a9f7a87be7fa5aaf688dbe4; agent sha256:f40c3b92f4670dd59df5fca91c8158aeb6309982aec25788fb49fbd390f6dc2f. Do not start Jenkins 2.462 against the 2.555.1 home. If tags are missing, recover/rebuild compatible images under separate approval before proceeding.

Acceptance: configuration has no required Yandex dependency; exact image manifests and authenticated secret access work; proposed branch/base are approved before local repo changes.

### 2. Validate and prepare storage

Recheck /dev/vdb identity, size, signatures, mounts and existing data on each host before any destructive operation. Confirm each device is the intended data disk. After explicit approval, create ext4 only on the verified empty data disk, mount /data with UUID-based fstab, and check mount persistence and permissions. Ensure the service cannot silently write to the boot disk when /data is absent.

Controller: use the 150 GB data disk for restored home and archive staging. Agent: decide capacity before builds; 10 GB data and 10 GB boot disks are likely restrictive for Docker images, Java browser test images, workspaces and Gradle caches. Measure required image sizes and expected workload. Increasing disk capacity is a separately approved infrastructure change; otherwise document the accepted limited workload. Explicitly choose where Docker/containerd storage resides so it does not fill the root partition.

Acceptance: /data is mounted from the intended UUID; capacity supports archive, extraction and runtime; agent storage decision is recorded. Formatting and mount changes require concrete command approval.

### 3. Validate, transfer and restore backup while Jenkins is stopped

Prefer the newest independently accessible valid backup. Currently the latest listed archive is /data/backup/jenkins-test/jenkins_20261007.tar.gz on 172.24.0.18. Check checksum, gzip/tar integrity, paths, ownership, modes, Jenkins version marker, encryption material, jobs, plugins and available space. Treat the historical archive as a live-filesystem backup with limited consistency guarantees.

Transfer through an accessible path from backup host or workstation relay; do not depend on Yandex nodes. Recheck checksum after transfer. Restore the verified data/jenkins subtree preserving numeric ownership and permissions. Actual host JENKINS_HOME must be /data/jenkins/data/jenkins; compose mounts /data/jenkins/data to container /data and /data/jenkins/.ssh to /root/.ssh. Avoid an extra nested extraction level. Retain the original archive separately.

Before startup inspect restored queue, resumable pipelines, triggers, agent launch configuration, URLs and hardcoded Yandex endpoints. Prepare quiet startup that prevents unintended builds or deployments, including resumed pipelines; disabling triggers alone does not stop resumptions. Determine a supported recovery mechanism before starting the container.

Acceptance: matching checksums; expected 2.555.1 marker, 11 job configs and 116 plugin archives if using the October 7 backup; keys and permissions preserved; no controller running during extraction.

### 4. Start controller in a controlled state

Install required Docker/Compose and prerequisites, including /usr/bin/unzip expected by the role bind mount. Apply controller-only configuration, skip unavailable Yandex integrations and preserve quiet startup controls. Start only after restore verification. Verify authenticated API, Jenkins version, plugin loading, credentials decrypting without exposing values, logs, job configuration and available disk space. Set zero controller executors for builds and retain queue/triggers restrictions until dependencies are checked.

Check the known controller image issue: root Git config credential.interactive=never previously blocked GIT_ASKPASS branch parameters. Inspect effective config and reproduce branch listing read-only; apply a narrowly scoped approved correction if it recurs. Do not upgrade plugins as part of recovery without a demonstrated requirement.

Acceptance: controller health/API work internally at 10.18.26.8; restored jobs/plugins are readable; no unintended task has started.

### 5. Connect AutoTest agent

Recover AutoTest node configuration: label autotest_web, remoteFS /home/jenkins/work, historical five executors. Prepare /data/jenkins-agent/data, gradle-caches and .ssh. Obtain inbound agent secret from authenticated Jenkins API in process memory; use protected runtime injection and no_log, never notes or repository files. Connect via WebSocket to the new controller HTTP endpoint, avoiding the historical 49187/50000 inbound-port mismatch.

Verify image/JDK compatibility, workspace access, DNS, GitLab/registry access and controller reconnection. Confirm resource capacity supports five executors; reduce concurrency only with explicit scope approval if capacity is inadequate. Workspaces and caches will be cold; missing failedSuite before a first build is not evidence of failed restore.

Acceptance: AutoTest online at 10.18.26.26, correct label/remoteFS, verified tool availability and accepted capacity.

### 6. Restore independent public access

Select a reachable VK or corporate ingress with the required public IP, TLS material and administrative access. The old route build.youdo.sg -> Yandex balancer cannot be reused while Yandex is unavailable. Prepare proxy configuration to 10.18.26.8 with WebSocket support, certificate validation and rollback. Verify HTTPS and authenticated API against the new endpoint before an approved DNS cutover. Test WebSocket agent traffic if it will use the public URL.

Acceptance: build.youdo.sg resolves/routes to a working non-Yandex endpoint, valid TLS, Jenkins root URL correct and external integrations can reach it. Endpoint selection is still open. Proxy/TLS/DNS mutations require their concrete approvals.

### 7. Validate available workflows and release startup restrictions

Enumerate jobs and their restored dependencies, including GitLab, Nexus, Vault, Nomad test stands, Kubernetes dev, Selenium/Grid, S3/artifact storage and monitoring. Mark Yandex-only targets unavailable; restoration of Jenkins does not recover them. Verify Git branch parameters and credentials without displaying secrets. With explicit approval run one representative safe web/API workflow whose complete dependency chain is reachable. Authorize dev/test deploy jobs separately only when their targets are available. Restore triggers and release quiet mode only after review of queued/resumable jobs and intended effects.

Acceptance: distinguish platform health, independently available functional workflows and workflows blocked by Yandex; no claim of full recovery while required targets remain unavailable.

### 8. Restore backups and monitoring

Check independent Airflow and backup connectivity to the new controller. Existing ADM_Backup_Jenkins DAG used REMOTE_SERVER=jenkins-test.ru-central1.internal and /data/backup staging: update the canonical source to the new controller after approval. Avoid concurrent backup schedules aimed at obsolete hosts. Verify a fresh backup, checksum, retention and a documented consistent capture/restore method. Restore accessible Zabbix/Alloy endpoints using VK settings and check monitoring delivery.

Acceptance: a new verifiable backup is held outside the controller; monitoring checks the VK controller and agent, disk capacity, agent availability and backup age.

## Actions and key commands

Read-only checks: ssh with BatchMode=yes, explicit id_ed25519 identity and ForwardAgent=no; id, hostname, free, df, lsblk, blkid, wipefs -n; getent hosts; registry HTTPS HEAD /v2/; Vault GET /v1/sys/health; backup host archive listing. First connections saved new ECDSA host keys locally. After root authentication failed, youdo authenticated and sudo -n id -un confirmed root privilege.

Authorized change: added the local .ssh/id_ed25519.pub to /root/.ssh/authorized_keys on both hosts through youdo and sudo, preserving existing entries; set root ownership, directory 0700 and file 0600. Then independently authenticated as root on both hosts. No key material was recorded in this note.

## Findings and limits

Reachable registry authentication endpoint does not prove either exact image exists. Unsealed Vault does not prove the needed secret can be read. Data devices have no reported filesystem signatures but must be revalidated before formatting. Backup source is reachable from the workstation; direct transfer connectivity and checksum are not yet revalidated. Public ingress selection and agent disk capacity must be settled before their dependent stages.

## Changed files

This note; knowledge/systems/jenkins.md; ~/ai/TODO.md; generated knowledge index; ~/ai/.sync-notes. Local known_hosts gained the two VK hosts. Remote /root/.ssh/authorized_keys changed on the two specified hosts under user authorization. Repository task files are untouched.

## Risks

Backup restore point is October 7, so later controller changes may be lost. Restored queues/resumable builds may cause unintended deployment unless controlled before startup. Incorrect home nesting or losing secrets prevents recovery. Agent disks may fill during the first cold build. Public URL still targets Yandex. Exact images, secret mapping, workflow dependencies and new backup schedule remain subject to verification.
