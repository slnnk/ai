---
system: jenkins
status: verified
checked: 2026-10-15
tags: [jenkins, mssql, vk-cloud, recovery]
---
# Jenkins build5832: large MSSQL endpoint still points at Yandex

## Task

Diagnose the MSSQL Restore failure in dynamic_deploy build5832 without rerunning the job or changing infrastructure.

## Context

The large MSSQL seven-stage VK runtime run completed for test/test1/test6; its repository changes remain unpublished. See [runtime evidence](2026-10-14-nomad-test-devops-897-vk-mssql-adaptation.md) and [Restore address-only review](2026-10-14-jenkins-restore-playbooks-review.md).

## Actions and findings

Authenticated read-only Jenkins GET found build5832 FAILURE after approximately5.3minutes, TEST_INSTANCE=test and RESTORE=true. Checkout was origin/master commit381391de5d8c21b58ea73f928b5b52c6a63d68b3. The log invoked `playbooks/deploy/db/restartMSSQLSERVER.yml -i test_inventory.sh -l test -D`; failure was `test_sql0 -> localhost` timeout reaching `sql-test.ru-central1.internal:1433`. No `restoreSnapshotMaster.yml` invocation appeared: execution was blocked by the preceding MSSQL service restart/TCP check, not by the SQL snapshot procedure.

The minimal endpoint fix already exists locally in `group_vars/test.yml`, `test1.yml`, `test6.yml`: each `sql` value points at its vk-ms1-sql-test*.mcs.local FQDN. Those three one-line replacements are uncommitted; no new repository edits were needed for this diagnosis. In the restart playbook, `restartMSSQLSERVER.yml:2` imports the thick-VM path; `restartMSSQLSERVER_on_VM.yml:11` delegates TCP1433 checking to localhost using `sql`.

Read-only SSH from Jenkins controller root@10.18.26.8 ran getent/nc and verified all three VK hostnames resolve to their current addresses and accept TCP1433: test10.18.26.17, test1 10.18.26.121, test6 10.18.26.9. This supports publishing the existing endpoint corrections; it does not verify snapshot contents or a successful deployment.

Other log errors were separate: stopping the youdo-test prefix matched five other jobs and returned rc1; Nginx cleanup passed empty input to xargs rm and returned rc123. Parallel log headings interleaved, so adjacent labels did not reliably identify the failed task. No causal claim beyond these observed errors is made.

## Proposed publication scope

Proposed repository automation-test-yandex, base origin/master, branch `DevOps-897-point-large-mssql-to-vk`, containing only the three existing one-line `sql` endpoint changes in group_vars/test.yml/test1.yml/test6.yml. Supervised first-stage branch approval is pending; the proposal is not approved. The full seven-stage adaptation remains a separate publication scope. No branch switch, staging, commit, push, MR creation, Jenkins retry or external write occurred.

## Changes and limits

Only this note, existing Jenkins/nomad-test maps and the existing DevOps-897 backlog item were updated. No SQL snapshot restore, application behavior, schema/data contents or monitoring ingestion verification was performed. Existing snapshot error-propagation findings remain outside the minimal endpoint correction.


## Supervised training record: branch approved, publication pending

User explicitly answered yes to the first-stage branch proposal. Fetched origin/master381391d and created approved branch `DevOps-897-point-large-mssql-to-vk` from it in the existing automation-test-yandex checkout, preserving all prior local edits. Index remains empty. Reviewed scope is only the existing three sql endpoint replacements in group_vars/test.yml/test1.yml/test6.yml, +3/-3; full seven-stage changes remain excluded.

Actual live `ansible-inventory --list` was checked through sanitized output only, exit0: test_sql0 resolves to10.18.26.17 / vk-ms1-sql-test.mcs.local; test1_sql0 to10.18.26.121 / vk-ms1-sql-test1.mcs.local; test6_sql0 to10.18.26.9 / vk-ms1-sql-test6.mcs.local. YAML parsing and diff --check passed; restartMSSQLSERVER.yml and restoreSnapshotMaster.yml syntax checks both passed.

Read-only GitLab project530 inspection found no .gitlab-ci.yml, empty ci_config_path, auto_devops false and hooks[]. The only active integration is YouTrack with push/MR events. No automatic deployment trigger was discovered. Observed project settings: squash off, remove source branch true, assignee a.solonenko; no open MR for the source branch.

Second-stage publication proposal awaits explicit approval: commit `set large mssql endpoints to vk`; MR title `DevOps-897 Point large MSSQL endpoints to VK`; approved source branch to master. Prepared body `/home/slnnk/ai-data/jenkins-recovery/mssql-endpoints-mr-body.md` contains one short Russian paragraph followed by the task URL. No staging, commit, push, MR creation/update, merge or Jenkins rerun has occurred. First-stage approval does not authorize those pending publication actions.


## Supervised publication completed (2026-10-15)

User explicitly approved the second-stage publication proposal. Verified initially empty index, staged only group_vars/test.yml/test1.yml/test6.yml, reviewed actual full staged diff with zero context: exactly three sql endpoint substitutions; staged diff check passed. Created commit `cdb11b5522ec6c30fae9cd5086898ff70f2cd2ba` (`set large mssql endpoints to vk`) and pushed approved source `DevOps-897-point-large-mssql-to-vk`.

Created [MR113](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/113), title `DevOps-897 Point large MSSQL endpoints to VK`, target master, assignee a.solonenko, squash false, remove_source_branch true. Fresh API verification confirmed expected SHA/source/target, pipelines[] and exact MR body match to `/home/slnnk/ai-data/jenkins-recovery/mssql-endpoints-mr-body.md` (one Russian paragraph plus task URL).

Endpoint-fix publication is complete. Other sixteen local MSSQL modified/untracked paths were preserved and remain unpublished; the full seven-stage workflow adaptation is outside this MR. No merge or Jenkins rerun occurred. Merge/rollout and any retry remain pending separate authorization. This supersedes earlier publication-approval-pending observations; no broader permission inferred.


## Explicitly authorized MR113 merge (2026-10-15)

User explicitly instructed merging MR113. Guarded local helper `/home/slnnk/ai-data/jenkins-recovery/merge-mssql-endpoints113.py --apply` verified expected source SHA `cdb11b5522ec6c30fae9cd5086898ff70f2cd2ba`, source branch, target master and exactly the three approved existing changed files before its merge API call. Preserved project squash/source-removal settings.

Fresh GET confirmed MR state merged, merge SHA `cf88e42259787a8c6350771d17726bd4fcff3e30`; master at that SHA was verified through raw group_vars sql fields for test/test1/test6, all matching VK names. Endpoint publication and merge are complete. No Jenkins retry and no local Git switch/merge occurred; unpublished workflow changes remain preserved. Full seven-stage workflow publication is separate and remains pending. This supersedes earlier merge-pending observations; user merge permission does not imply permission to rerun Jenkins.


## User-reported playbook acceptance (2026-10-15)

After the MR113 endpoint fix merged to master `cf88e42259787a8c6350771d17726bd4fcff3e30`, user reported that the playbook completed successfully. Record this as user-reported acceptance of the endpoint fix. No new Jenkins build ID or execution log was provided or independently verified; no build number or broader application, SQL contents/schema or monitoring validation is inferred.

The endpoint-fix retry/verification follow-up is closed on that user report. Full seven-stage automation publication and the previously planned stage1 prepared-image default remain separate open work. No external/API, repository or Git action occurred for this acceptance bookkeeping.
