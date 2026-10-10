---
system: jenkins
status: verified
checked: 2026-10-10
tags: [recovery, ansible, backup]
---
# DevOps-890: Jenkins recovery role and backup audit

## Summary

- Task: restore Jenkins on recovered zone-a controller/agent, validate workflows, then publish final changes.
- Controller `10.16.28.8`, agent `10.16.28.26`; both RUNNING, verified SSH root.
- Secondary disks 150/10 GiB are blank/unmounted; Docker and `/data` are absent; unzip is installed.
- Validated October 7 archive is 1.53 GB and records Jenkins 2.555.1; host home is `/data/jenkins/data/jenkins`.
- Archive contains controller config, credentials/encryption files, 11 job configs, 116 plugin archives and AutoTest node configuration.
- Local approved branch updates controller/agent image pins only; no task commit, push, MR or runtime changes.
- Remaining runtime gates: disks, inventory metadata, restore-before-start, agent secret/address, routing and backup source.
- User deferred publication until recovery and functional validation; see the numbered recovery sequence below.
- Read Findings for audit evidence; Recovery plan for ordering, acceptance gates and rollback.

## Task

Audit the Ansible Jenkins role and backup DAG for [DevOps-890](https://youtrack.youdo.com/youtrack/issue/DevOps-890), then update only controller/agent image versions to the latest available versioned tags, as requested by the user.

## Context

- Repository: `/home/slnnk/git/automation-services`; Yandex variables `inventories/yandex/group_vars/jenkins-yandex`.
- Source DAG: [backup_jenkins.py](https://gitlab.youdo.sg/sysadmins/dags_adm/-/blob/master/dags/backup_jenkins.py); read-only snapshot `/home/slnnk/ai-data/jenkins-recovery/backup_jenkins.py`.
- Canonical infrastructure map: [Terraform test-infra](../systems/yandex-cloud/terraform-test-infra.md).
- Controller `yc-a-jenkins-test`, `10.16.28.8`; agent `yc-a-jenkins-agent-test-01`, `10.16.28.26`; both live YC status RUNNING, zone `ru-central1-a`.

## Actions

- Ran daily knowledge sync; no reminders printed. Read task through YouTrack GET (description absent).
- Audited role, dependencies, Terraform inventory and VM cloud-init; independently checked `ansible-playbook jenkins.yml -i localhost, --syntax-check` (passes with missing target-group warnings).
- SSH read-only access to both new VMs works as `root`; `youdo` rejects local public keys. Record root as the verified recovery access route; do not infer access from cloud-init alone.
- Listed backup archives on `msk3-backup02.youdo.corp` (`172.24.0.18`), `/data/backup/jenkins-test/`. Fully read latest archive using `tar -tzf` with pipefail and summarized names without disclosing contents.
- Stream-read only version and node metadata from the archive; queried GitLab Git/registry tags and tag Dockerfiles using GET.
- User approved branch `DevOps-890-update-jenkins-images`, repository `automation-services`, base `origin/master`, and exactly two version changes. No publication or runtime approval was requested or granted.

## Findings

### Backup

- Latest available archive: `jenkins_20261007.tar.gz`, 1,532,460,486 bytes, mtime October 7 06:03. No October 8-10 archives were present at inspection.
- `tar -tzf` completed successfully: 72,925 entries; one controller config, one credentials file, both `secrets/master.key` and `secrets/hudson.util.Secret`, 11 job configurations, 116 plugin archives. This proves archive readability and required-file presence, not a successful runtime restore.
- Archive paths start at `data/jenkins/`. Actual host Jenkins home is `/data/jenkins/data/jenkins`, because controller compose mounts `/data/jenkins/data` to `/data` and sets `JENKINS_HOME=/data/jenkins/`. Restore must preserve this nesting; the archive also contains the host `.ssh` directory. No key values were read into outputs or notes.
- `jenkins.install.InstallUtil.lastExecVersion` is `2.555.1`. Recovered node `AutoTest` has label `autotest_web` and five executors.
- DAG `ADM_Backup_Jenkins`, cron `0 3 * * *`, runs through the Airflow connection `msk3-backup02`. It archives old source `jenkins-test.ru-central1.internal:/data/jenkins`, transfers via rsync, and removes files older than seven days only after transfer. New controller still resolves that old name to `10.16.26.16`; backup source requires deliberate adaptation when recovery runs.
- DAG backs up a running filesystem without quiescing Jenkins; application consistency remains unverified. Python AST and embedded shell syntax checks passed; Airflow runtime/import compatibility was not tested.

### Role and live VM readiness

- Existing Yandex controller tag `2-462` builds from `jenkins/jenkins:2.462-jdk11`; restoring a `2.555.1` home with it would downgrade Jenkins. Jenkins documents that downgrade is generally unsupported: [official upgrade guide](https://www.jenkins.io/doc/upgrade-guide/2.138/).
- Latest versioned controller Git tag `2.555.1.2` (May 14) corresponds to registry `2-555-1-2`; Dockerfile uses `jenkins/jenkins:2.555.1-jdk21`. Compared with `2.555.1`, it adds `/usr/local/bin/python` pointing to `/usr/bin/python3`.
- Latest versioned agent Git/registry tag is `3355.v388858a_47b_33.6` (July 7). Role previously pinned `3256.v88a_f6e922152`.
- Controller has blank 150 GiB `/dev/vdb`, agent blank 10 GiB `/dev/vdb`: no filesystem or mount on either. `/data` is absent. Boot filesystems are 20/10 GiB; role only creates `/data`, so automatic provisioning would use the boot disk unless data disks are prepared first.
- Docker is absent; `unzip` exists on both VMs, so the bind mount prerequisite is satisfied on these machines.
- Controller can resolve `vault.service.yandex-test.consul` to `10.16.28.16`; unauthenticated `/v1/sys/health` returns HTTP200. Registry DNS resolves. Authentication/private-image access was not tested. Zabbix DNS still points to `10.16.26.34`.
- Recovery Terraform output lacks required `host_type`. Controller needs `jenkins`, agent needs `jenkins-agent`, group `jenkins-yandex`, SSH route root. Live dynamic inventory was not run; older Ansible host resources still reference old machines.
- Role automatically starts Jenkins; no restore stage exists. Agent template hardcodes empty `JENKINS_SECRET` and node name `AutoTest`; `jenkins_ip` still uses the old controller DNS. Controller has no restart policy.

## Changes

On the approved branch `DevOps-890-update-jenkins-images`, changed exactly two lines in `inventories/yandex/group_vars/jenkins-yandex`: controller `2-462` -> `2-555-1-2`, agent `3256.v88a_f6e922152` -> `3355.v388858a_47b_33.6`. Both selected registry tags exist. Controller image uses Jenkins `2.555.1`/JDK21; selected agent uses inbound-agent `3355.v388858a_47b_33-17-alpine3.23-jdk21` and Maven `3.9.13-eclipse-temurin-21`. Registry agent image creation date is July 7 2026.

Scoped `git diff --check` passed. Playbook syntax check passed, with expected warnings because the localhost-only inventory lacks Jenkins groups. Both compose templates rendered successfully and parsed as YAML with the exact selected registry image references. Independent review confirmed exactly the two approved changes and string variable types. Full checkout diff-check additionally reports pre-existing whitespace in `roles/gitlab-runner/templates/cron-docker-clean.j2`; it is outside this task and preserved.

Unrelated pre-existing repository changes are preserved. No remote files, services, DNS, API objects or deployments changed. SSH accepted new host keys locally. No task commit, push or MR was made. Proposed publication names: commit `update jenkins controller and agent images`; MR `DevOps-890 Update Jenkins controller and agent images`; source `DevOps-890-update-jenkins-images`, target `master`. Publication requires a separate reviewed approval.

CI review: `.gitlab-ci.yml` has only the test stage and no includes/deployment triggers. Automatic Molecule jobs select changes in nginx/consul/nomad roles, so this inventory-only update matches none; new branch pushes skip them. Optional manual `molecule-nomad` runs Nomad role tests, not Jenkins deployment. Publication does not automatically start Jenkins provisioning.

## Risks

Deployment remains blocked by disk preparation, restore-before-start order, inventory metadata, old controller address and agent secret. These are recorded in `~/ai/TODO.md`; only the two version changes were requested for implementation.

## Recovery plan agreed for preparation (2026-10-10)

User explicitly deferred commit/push/MR until Jenkins is restored and functional checks pass; further recovery adaptations may be required. This section is a proposed operational sequence, not runtime approval. Open work remains tracked in `~/ai/TODO.md`.

1. **Refresh read-only preflight.** Verify root SSH, VM/disk identities and blank state, available capacity, latest backup list, registry access and Vault authentication. Inspect external `build.youdo.sg` routing/TLS, Zabbix destination and controller/agent dependencies. Record the selected backup date and intended restore point. Output: exact disk IDs, backup selection and dependency/routing findings.
2. **Prepare local recovery configuration.** Use the existing approved branch; preserve unrelated changes. Keep latest version pins. Prepare a task-local inventory selecting only `10.16.28.8` and `10.16.28.26`, group `jenkins-yandex`, root SSH, and `host_type=jenkins` / `jenkins-agent`. Follow the existing repository inventory pattern; do not broadly migrate Terraform inventory for this recovery. Point agent at the recovered controller. Make only necessary role changes, with concrete diffs reviewed under the supervised branch rules when scope expands. Secret must come from the established secret store or protected runtime input, never a committed value. Check syntax/list-hosts/template rendering before any run.
3. **Prepare data disks after explicit approval.** Reconfirm each `/dev/vdb` against YC disk ID, blank filesystem/partition table and lack of mount immediately before formatting. Initialize ext4 and mount via filesystem UUID at `/data`, controller 150 GiB and agent 10 GiB; persist mounts in fstab and check `findmnt`, `df` and `mount -a`. Output: `/data` resides on secondary disks, not boot disks. Formatting and remote configuration commands each need explicit approval.
4. **Restore controller data before running the Jenkins role.** Keep Jenkins stopped/uninstalled. Copy the selected archive to a staging location on the controller data disk, compare source/destination SHA256 and validate copied archive. Restore only the `data/jenkins/` subtree to `/` with root ownership preserved; verify `/data/jenkins/data/jenkins/config.xml`, jobs, plugins, encryption files and host SSH directory. Protect secret-file permissions and avoid printing contents. Do not unpack over an initialized/running Jenkins home. Original source backup remains untouched.
5. **Provision and start controller only.** Run the existing role with explicit inventory and a limit selecting controller only, after disk and restore gates. Role replaces the restored compose file with the latest image pin. Before start inspect restored queue, controller executors and scheduled jobs; prevent unintended automatic builds during recovery. Confirm current Zabbix destination or agree on handling a monitoring-only failure separately. Verify Docker mounts/image, startup logs, HTTP access, version 2.555.1, authentication, plugin loading, 11 archived job configurations and credential decryption through a benign connectivity check. Do not print secrets. No additional plugin/core upgrade during restore.
6. **Restore agent connectivity.** Inspect recovered AutoTest node configuration, work directory, launcher and labels; preserve node name `AutoTest`, five executors and existing label `autotest_web` unless the user explicitly changes them. Supply the node secret securely and the new controller URL; prepare agent directories and install/start only the agent host through the role. Verify online state, remoting/JDK21, filesystem permissions and availability of required tools. Review scheduling/queue before allowing normal executors. Previous workspace/cache contents are not part of the controller archive and are not assumed restored.
7. **Validate workflows and switch routing.** Inspect and update the existing external proxy/DNS route for `https://build.youdo.sg` to the new controller only after direct checks pass. Changing this route and starting jobs are separate approved external actions. Run a small authorized AutoTest job to check checkout/credentials/tools, one representative web/API test, and an agreed dev deployment only when recovered target services are ready. Check result/artifact links, callbacks, TLS and authentication through the public endpoint. Record infrastructure-dependent failures separately from Jenkins defects.
8. **Resume backups.** Inspect the deployed DAG and Airflow SSH connection before changing anything. Select one explicit source strategy: redirect the legacy controller DNS to the recovered VM if that name remains canonical, or change REMOTE_SERVER to the new canonical name; do not change both without need. Ensure `/data/backup` exists on the controller because the DAG writes its temporary archive there, and verify backup-host SSH access to the new machine. Keep the original archive available during recovery. Review DAG changes in its own approved branch if needed; delivery is repository master -> S3 -> cron, so avoid temporary edits on Airflow that synchronization overwrites. After approval, run one backup and validate the newly transferred archive and its restore paths, then confirm scheduled success.
9. **Accept recovery, then publish.** Reconcile final diffs after runtime findings, rerun relevant checks and summarize working controller/node/jobs/routing/backups plus any dependency limitations. Only then request the reviewed commit/push/MR approval with final names, explicit paths and CI effects. No merge or deployment follows implicitly from publication approval.

**Rollback:** retain the October 7 source archive and old infrastructure. If startup changes restored state or fails validation, stop only the new controller and restore from the untouched archive after explicit approval; do not downgrade the restored home. If routing was switched, restore its recorded previous destination when rollback is requested. A blank-disk format has no data rollback; its gate is fresh disk identity/emptiness verification. Backup retention needs consideration before a successful new run because the DAG then removes archives older than seven days.

## Portable lesson

none
