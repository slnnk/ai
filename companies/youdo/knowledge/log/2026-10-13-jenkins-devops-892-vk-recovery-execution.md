---
system: jenkins
status: verified
checked: 2026-10-13
tags: [jenkins, recovery, vkcloud, DevOps-892, DevOps-891]
---

# DevOps-892: VK recovery execution and DevOps-891 image rebuilds

## Summary

User authorized starting the VK Jenkins recovery plan and assigning Jenkins image rebuilds to DevOps-891. Controller and AutoTest agent are running and internally verified; controller remains in recovery quiet mode. Public routing is deferred because the user confirmed no replacement balancer is available yet. Functional Git credential check is in progress. Existing DevOps-891 recovery comment74-124638 updated in place and exact-text GET verified, preserving previous content and adding Jenkins pipeline links.

## Context and approvals

- Root SSH on10.18.26.8 and10.18.26.26 verified in preceding plan stage after authorized public-key installation.
- User explicitly approved automation-services branch DevOps-892-restore-jenkins-on-vk from origin/master. Fetch advanced master to bffef350; branch created; hashes of16 unrelated modified/untracked files preserved. No commit/push/MR action yet.
- User separately approved controller disk formatting/mount and agent disk formatting/mount. Guarded scripts verified exact hostname, serial, size and absent signatures before mkfs. Controller UUID937fca4e-18b8-4bc1-a1a2-5b4d1e5931f4; agent UUIDb1457393-253d-4960-9278-b9b6ad40161a. Both/data ext4 mounts verified and fstab/systemd reloaded.
- User separately approved controller/agent tag pipelines, including version publication and latest overwrite; approved backup transfer, restore and Docker/Compose runtime preparation on both hosts.
- User provided VK_VAULT_TOKEN in company.env for http://vault.service.vk-test.consul:8200. Token values never recorded here.

## Actions and key commands

Adapted existing guarded helpers in ~/ai-data/jenkins-recovery with DevOps-892 suffix, exact VK addresses and filesystem UUID. bash-n and plan-only receiver checks passed. Source checksum and gzip integrity passed. Transfer created/data/jenkins-recovery/jenkins_20261007.tar.gz mode0600 and verified1532460486bytes plus SHA256699f78d187419d4f1b401d2c8da2c0144eba4082877b882f49551d00e84041dd. Restore preserved keys/ownership/modes and verified2.555.1,11job configs and116plugin archives.

Read-only restored-home audit: zero queue items, zero jobs with triggers, zero unfinished build.xml records, zero XML parse failures and no init.groovy.d scripts. Controller has10executors historically; no configuration changed for them.

Prepared runtime via run-vk-ansible.py prepare --execute and existing docker-compose -> docker roles. Guard verified/data UUID and redirected fresh Docker/containerd storage to/data before package installation. Jenkins is not part of this stage. First invocation was interrupted before execution; log did not exist. Resumed the same approved command after user asked about Ansible roles. No common role exists in this checkout; base_linux was not included.

## Image recovery (DevOps-891)

Authenticated manifests initially404 for both required images. Existing tags/SHAs verified before pipeline creation. Controller project391 ref2.555.1.2 SHA75865e16c836d43294aa4d08e7ae4ee6f9b4010e: [pipeline140738](https://gitlab.youdo.sg/sysadmins/devops-tools/jenkins/-/pipelines/140738), build3221016. Agent project425 ref3355.v388858a_47b_33.6 SHA77bbffb8e8c96ae94f57ea48acb57fc00c8bc61d: [pipeline140739](https://gitlab.youdo.sg/sysadmins/devops-tools/jenkins-agent/-/pipelines/140739), build3221018/latest3221019 succeeded. Agent version/latest authenticated manifests both sha256:2bd47b51f2e63488631a2de675870424d4a62066d33ebd4880751693318c9731, matching push trace. Controller build3221016/latest3221017 and pipeline140738 succeeded. Version/latest manifests and push trace match sha256:75671f1c83e6bd85fed477171096dd6b6e91c2254cefbc4051c3a332b07d60fa. Public Yandex downloads were reachable; no speculative Dockerfile change made.

## Vault and service authentication

Cached CLI token denied documents on initial vault.service.consul endpoint. New VK_VAULT_TOKEN accepted on explicitly provided VK-test endpoint; secret/ansible/vkcloud404, common and yandex readable. Jenkins registry password exists at secret/ansible/yandex keyjenkins_client_docker_pass in this independent VK Vault. Verified service account nomad can read the published agent manifest. The document name yandex is historical; recovery uses the VK endpoint, not a Yandex service. No personal GitLab token needs to be stored on Jenkins hosts.

## Changed files

Repository task changes: jenkins.yml host selector; inventories/vkcloud/jenkins-recovery.ini; inventories/vkcloud/group_vars/jenkins-vkcloud; roles/jenkins/tasks/{docker-auth,install-jenkins,install-jenkins-agent}.yml; roles/jenkins/templates/docker-compose-agent.j2. Added runtime registry mapping, WebSocket agent secret injection, protected secret file/rendering and explicit startup toggle (false for recovery). No unrelated files edited; user-file hashes verified.

External local helpers/receipts/logs in ~/ai-data/jenkins-recovery; this log and existing plan/system/backlog will reflect final stage results. Credentials remain in memory or protected runtime files. No git publication yet.

## Verification

Ansible syntax checks passed for runtime preparation and Jenkins play. Task-specific git diff --check passed; whole-checkout check flagged pre-existing whitespace in roles/gitlab-runner/templates/cron-docker-clean.j2, which is unrelated and unchanged. Backup digest/restore checks and offline audit passed. Runtime preparation: both hosts ok24/changed13/failed0. Controller configuration-only apply ok28/changed4/failed0; startup remained disabled during apply. Guarded startup verified absent home standalone/init/boot hooks and absent image reference hooks, then pulled the verified digest, installed recovery quiet hook and started compose. Independent API verified2.555.1,11jobs,116active plugins,quietingDown=true and queue0. Agent apply ok30/changed6/failed0; API verifies AutoTest online with5executors. Images digests match on both hosts; data space controller131GBfree,agent7.8GBfree.

## Risks and limits

October7restore point excludes later changes. Agent10GBdata capacity remains constrained and user approved use of current disk; cold build capacity must be checked. Public ingress still points to Yandex. Full workflow acceptance depends on independently available test targets. Recovery has not been declared complete.

A read-only diff accidentally displayed a credential-bearing unrelated line in roles/gitlab-runner/vars/main.yml. Value is not repeated or recorded here; only location/access route is retained. Assess validity and rotation separately.

## User corrections and current limits

User clarified that Jenkins image rebuild results belong in the existing DevOps-891 recovery comment. User then requested normal repository/result entries matching the existing format, no separate dated supplement, and repository links at the beginning. Applied exactly: controller/agent repo links near the top, normal results bullets with pipelines/jobs/digests, no supplement heading. Existing unrelated content preserved; final published comment74-124638 updated1791888705096 SHA2560ff122d29d569b4ddc91e0d426dfc092a8cfe6fb71e3ea0e2c099be1f1f9177d, exact-text GET verified. This is task-scoped wording feedback, not broader mutation permission.

User asked whether Docker uses Ansible roles: confirmed existing docker-compose includes docker; common role absent in this checkout, base_linux not run. User confirmed replacement public balancer has not been provisioned; public route is intentionally deferred. No DNS, TLS, ingress changes made.

Known historical image issue detected: docker exec jenkins git-C/ config--get credential.interactive returns never. User approved scoped Script Console git ls-remote probe to determine current functional effect before any correction. No functional build, quiet-mode release, monitoring change or backup schedule change yet.

## Git parameter correction

Approved diagnostic probe through Script Console reproduced the actual failure: credential found with username/password present, gitRemoteRead=false, passwordPromptFailure=true, no authentication rejection/TLS/execution error. User separately approved ssh root@10.18.26.8 'docker exec jenkins git -C / config --local --unset credential.interactive'. Command succeeded. Repeated authorized probe returned gitRemoteRead=true and branchCount=205. No service restart or job execution. Persistent image fix remains separate work because the runtime change is lost on container recreation.

Startup review found missing standalone/boot-failure hook guards. Added fail-closed home checks and read-only streaming image layer audit before hook creation/start; syntax passed, actual image hook list empty. No inspection container created.

## Deferred actions confirmed by user

Stage2 publication proposal: seven task files (+35/-4), commit `restore jenkins on vk hosts`, MR `DevOps-892 Restore Jenkins on VK hosts`, source `DevOps-892-restore-jenkins-on-vk`, target `master`. Proposed description: one short Russian paragraph about VK image/Vault/WebSocket configuration and separate startup, then DevOps-892 link. Existing CI has no Jenkins coverage or automatic deploy; first branch push expected skipped. User explicitly answered to defer publication. No staging, commit, push or MR creation occurred. User also explicitly deferred Zabbix installation; no monitoring apply executed.

Remaining dependency audit: controller reaches Zabbix172.28.0.120:10051; Loki endpoint times out. sc-airflow172.28.0.118 healthy; deployed `/opt/airflow/dags/dag_bag1_adm/backup_jenkins.py` still targets jenkins-test.ru-central1.internal, which is NXDOMAIN from backup host; last three scheduled runs Oct11-13 failed. Backup host SSH to new controller stops at missing ED25519 known-host entry; backup identity authentication has not been tested. New controller `/data/backup` absent. Durable source is `/home/slnnk/git/dags_adm/dags/backup_jenkins.py`, clean checkout DevOps-686-clean-gitlab; changes require a separately approved task branch. No backup scheduler mutation, new archive, key authorization or source edit executed.

`/home/slnnk/ai-data/jenkins-recovery/devops-892.patch` retained locally. Current browser URL http://10.18.26.8/; network access/VPN required. Public ingress deferred by user because balancer is not yet provisioned.

## DevOps-892 recovery comment publication

User explicitly requested a comment covering completed work, the next recovery sequence, remaining work, Ansible automation proposals and the controller image Git correction. Read-only API confirmed DevOps-892 summary `[Recovery] Восстановить Jenkins` and no prior comments. Fresh Jenkins API confirmed 2.555.1, 11 jobs, AutoTest online with 5 executors, quietingDown=true and queue empty.

Prepared exact Russian comment in `/home/slnnk/ai-data/jenkins-recovery/devops-892-comment.txt`. Posted under the explicit request; returned comment id74-124647. Exact-text GET verification succeeded: 9325 characters, SHA256faa17e9e9aae4bba1689b70dd5c72e4cc1f8b3d8b51221131bad19617f92df77. Receipt `/home/slnnk/ai-data/jenkins-recovery/devops-892-comment-result.json`. Checked identical comments before POST to avoid duplicates.

Comment separates completed work from proposals and remaining actions, includes repository links at the beginning, and explicitly records deferred publication/monitoring/public ingress, untested workflows, pending backup migration, recovery quiet hook persistence and loss of runtime Git config correction on container recreation. A repeat build of unchanged controller sources is insufficient; a narrowly scoped image fix and verification after recreation are proposed, with image work tracked in DevOps-891. No further runtime, repository or image changes were made by this documentation request; issue status unchanged.
