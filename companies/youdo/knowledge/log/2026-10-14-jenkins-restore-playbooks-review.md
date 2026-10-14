---
system: jenkins
status: verified
checked: 2026-10-14
tags: [ansible, recovery, review]
---
# Jenkins dynamic_deploy: Restore stage review

## Task

User requested checking playbooks used by Restore in dynamic_deploy. User clarified that this means the job stage, not controller provisioning. Read-only review; no repository edits, builds or remote mutations authorized or performed.

## Context

Repository /home/slnnk/git/automation-test-yandex has preserved unrelated recovery changes. Current Jenkins Pipeline was read through authenticated GET /job/dynamic_deploy/config.xml on controller 10.18.26.8; complete XML and credentials were not saved. Helper /home/slnnk/ai-data/jenkins-recovery/review-restore-stage.py prints only stage names, playbook selections, inventory selectors and endpoint hosts.

## Actions and findings

- Confirmed Restore uses restartMSSQLSERVER.yml and restoreSnapshotMaster.yml, recreate_db_postgres_monolith.yml, deploy_es_nomad.yml, rabbit/clear.yml, redis/flushdb.yml, s3/clear.yml and nginx/clear-cache.yml under playbooks/deploy/. Update B2B elastic calls b2bautomation.${test_instance}.youdo.sg. ES explicitly uses test_inventory.sh; other Ansible calls use INVENTORY.
- PG recreate_db_postgres_monolith.yml:15 terminates/drops lower-case instance_kraghag but creates quoted instance_Kraghag. Repeated reset will not remove the created database. psql has no explicit host/port; actual local cluster selection must be checked against inventory before changing it.
- MSSQL restoreSnapshotMaster.yml:24-37 lacks reliable SQL failure propagation, checking only Error. in stderr; login disabled at line15 is enabled only by final normal-path task. Procedures in deploy/db/files/RecreateDBProcedures.sql:249-263 return severity10 when database/snapshot is missing. A verified snapshot baseline and explicit prerequisite failures are needed; sqlcmd -b alone does not catch severity10.
- rabbit/clear.yml:15/21/33 ignores HTTP and parsing errors, allowing an unsuccessful purge to continue. Endpoint is already dc-driven with dc=vk-test.
- Static autotest/public-test inventories still contain Yandex addresses. Their effect depends on the INVENTORY selector; do not declare ordinary VK dynamic inventory stale based on these exceptions.
- s3/clear.yml has literal access material; record only its location and move access to Jenkins/environment in separately approved edits. Controller-delegated deletion is repeated per docker host. Existing Yandex S3 endpoint does not itself require migration.
- Redis flush_mode=all requires an instance-dedicated endpoint. Nginx cleanup hides errors. These are existing execution risks, not automatically proven VK routing defects.
- ES recovery has previous thin/thick acceptance; no new ES defect established in this review. B2B endpoint reachability was not tested.

## Validation

Repository code reviewed without execution of reset/clear tasks. Initial controller provisioning syntax check passed but does not validate this Restore stage. SQL semantics corroborated against official PostgreSQL quoted-identifier documentation and Microsoft sqlcmd error-severity documentation. All eight referenced Restore playbooks passed ansible-playbook -i localhost, --syntax-check (exit0); expected unmatched-host warnings. No inventory endpoint or task execution was validated.

## Changed files and risks

Only local review helper and knowledge-base files changed. No Git state changes or publication. Runtime prerequisites, inventory target correctness and successful full Restore remain unverified. Review is not acceptance of destructive reset operations.

## Related evidence

[Controller recovery map](../systems/jenkins.md) and [ES recovery context](2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

## User scope correction and address-only audit

User clarified that the playbooks worked and the requested review concerns old yandex-test addresses and minimal changes to verify deployment. Existing reset behavior and optional hardening are outside this task; earlier findings are not prerequisites for the minimal VK deployment test.

Current live dynamic_deploy defaults INVENTORY=test_inventory.sh, with explicit autotest inventory exceptions. Restore uses this selector except ES, which explicitly uses test_inventory.sh. Existing script queries dyninv.vk-test.youdo.local. A read-only live inventory query verified test5 dc=vk-test, PostgreSQL10.18.26.39, Rabbit10.18.26.7, load balancer10.18.20.97 and Nomad hosts10.18.26.34/.38/.37/.30. test5_lb-logreader still has172.26.0.111, but is not consumed by the reviewed Restore tasks.

No hardcoded old test addresses found in normal test5 Restore playbooks/includes: thin MSSQL Nomad URLs, Rabbit and Redis use dc; PostgreSQL/Nginx use inventory. Existing external Yandex S3 is not an old yandex-test service. SQL UNC172.26.0.115 belongs to a backup procedure not called by current snapshot Restore. Do not change those for the current run.

Read-only git show origin/master:group_vars/{test,test1,test6}.yml confirmed thick sql names remain sql-test.ru-central1.internal, sql-test1.ru-central1.internal and sql-test6.ru-central1.internal. Local VK replacements are preserved but unpublished, so master checkout still uses old names for these thick stands. Minimal address changes are needed only if selecting those stands; normal test5 Restore has no newly established address-edit requirement. Full dynamic_deploy contains stages outside Restore and is not proven end-to-end by this audit.

No repository edit, reset, deployment or external write performed after scope correction.
