---
system: jenkins
status: verified
checked: 2026-10-11
tags: [recovery, ansible, backup]
---
# DevOps-890: Jenkins recovery role and backup audit

## Summary

- Task: restore Jenkins on recovered zone-a controller/agent, validate workflows, then publish final changes.
- Controller `10.16.28.8`, agent `10.16.28.26`; both RUNNING, verified SSH root.
- Stage2 completed October11: secondary disks150/10GiB are ext4 at /data with UUID fstab entries; systemd mount units verified. Docker is absent; unzip installed.
- Validated October 7 archive is 1.53 GB and records Jenkins 2.555.1; host home is `/data/jenkins/data/jenkins`.
- Archive contains controller config, credentials/encryption files, 11 job configs, 116 plugin archives and AutoTest node configuration.
- Controller/agent recovery and public routing are verified. Five repository changes published as commit `3ad647f0ff6ed5b8d17e14f42401b0577a5ede21` in [MR !1368](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1368); recovery inventory remains local/untracked by explicit task-specific user exclusion.
- Remaining acceptance: representative functional workflows, backup-source adaptation and monitoring; track open work in `~/ai/TODO.md`.
- Backup transfer/restoration completed October 11 with matching SHA256 and preserved ownership/modes. Controller is Jenkins 2.555.1; AutoTest is online through WebSocket with five executors; public HTTPS/API checks passed.
- User superseded the earlier publication deferral, reviewed final scope and explicitly approved commit/push/MR; no merge or deployment was authorized.
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

## Stage 1 completion (2026-10-11)

Stage 1 completed on October 11 after the user's explicit start instruction: two-host inventory, root/Python connectivity, Vault role checks and registry manifest authorization passed with the existing Yandex-specific token. Public route remains on the old controller; TLS is healthy. See [stage 1 evidence](2026-10-11-jenkins-devops-890-inventory-dependencies.md). Publication remains deferred by the user.

## Portable lesson

none

## Publication preparation (October 11)

User now requests publication and the complete task-related change list, superseding the earlier defer-publication preference. Read-only final diff/index review and independent six-file package review passed; index is empty. Scope: inventories/yandex/jenkins-recovery.ini (new), inventories/yandex/group_vars/jenkins-yandex, inventories/yandex/group_vars/balancers_test, roles/jenkins/tasks/install-jenkins-agent.yml, roles/jenkins/templates/docker-compose-agent.j2 and roles/nginx/templates/vhost/build.youdo.sg.j2. Preexisting Terraform backend switch in inventories/yandex/main.tf and runner changes are excluded.

Proposed source remains approved DevOps-890-update-jenkins-images, targetmaster in sysadmins/automation-services (project216). Commit: restore jenkins on recovered vms. MR title: DevOps-890 Restore Jenkins on recovered VMs. MR body prepared as one Russian paragraph plus task link in /home/slnnk/ai-data/jenkins-recovery/mr-body.txt. GitLab read-only inspect finds no open MR for the source branch; project defaultmaster, squashdefaultoff. CI contains test jobs only: firstbranchpush skips automaticjobs, laternginxchanges canrun molecule-nginx; MR mayofferoptionalmanualmolecule-nomad. Noautomaticruntime deploy.

Prior syntax/YAML/render/scoped-diff checks and all runtime controller/agent/publicHTTPS/API checks passed. Final independent package review reports no material issues. Publication approval summary must be shown before staging/commit/push/MR creation under the supervised workflow. No state-changing Git operation occurred at this checkpoint.

## Publication approval and scope correction (October 11)

User confirmed the proposed publication with one task-specific exclusion: do not include inventories/yandex/jenkins-recovery.ini. Final approved package contains five tracked files (all proposed paths except the recovery inventory). Branch/target, commit message and MR title remain unchanged. MR body corrected before execution to omit the inventory claim. Approval covers staging these five explicit paths, committing, pushing the approved branch and creating/updating its MR; no merge/deployment. Recovery inventory stays local/untracked, unrelated user changes remain excluded. This exception is specific to DevOps-890 and does not change general Git policy.

## Publication result (2026-10-11)

User-approved publication completed on `DevOps-890-update-jenkins-images` targeting `master`. Commit `3ad647f0ff6ed5b8d17e14f42401b0577a5ede21` (`restore jenkins on recovered vms`) contains exactly five approved paths: `inventories/yandex/group_vars/jenkins-yandex`, `inventories/yandex/group_vars/balancers_test`, `roles/jenkins/tasks/install-jenkins-agent.yml`, `roles/jenkins/templates/docker-compose-agent.j2`, and `roles/nginx/templates/vhost/build.youdo.sg.j2`.

Published [MR !1368](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1368), title `DevOps-890 Restore Jenkins on recovered VMs`; source/target/SHA matched read-only API verification. Squash is disabled and source-branch removal is enabled. Pipeline `140550` is skipped, as expected from first-branch-push rules; CI has no automatic deployment. MR description was corrected before publication to omit the excluded inventory.

The user specifically excluded `inventories/yandex/jenkins-recovery.ini`; it remains local/untracked. This task-specific exclusion grants no broader policy change. Staged index is empty; unrelated Terraform backend and runner edits were neither staged nor changed. No merge, deployment or new runtime action followed publication. Functional workflows, backup adaptation and monitoring remain open in `~/ai/TODO.md`.

## Local inventory cleanup (October 11)

User explicitly requested removal of inventories/yandex/jenkins-recovery.ini after its exclusion from publication. Verified it was untracked, deleted the local file and verified absence. No commit/push or runtime change required. Historical recovery commands reference the deleted temporary inventory; recreate an explicit two-host inventory before reusing those commands or local apply helpers. Published commit/MR are unchanged.
