---
system: jenkins
status: verified
checked: 2026-10-15
tags: [jenkins, vk-test, deploy]
---
# dynamic_deploy test5 repeat after SSH credential alignment

## Task and authorization

User explicitly requested repeating deployment after root SSH key installation and PostgreSQL stage credential alignment. Same parameters as5819 retained: test5, master, monolith139914, static metadata139593, BRANCHgitlab; RESTORE/REDIS/RABBIT/ELASTIC/S3/NGINX/SUGGESTIONS_REINDEX true; RESTORE_B2B_ELASTIC/WEB_STATIC/MICROSERVICES false. Large DB stands excluded. Approval covers this one repeat, not an additional automatic build.

## Actions and findings

- Existing deploy helper extended with --receipt to retain prior receipts and prevent accidental duplicate launch. POST returned201, queue19130, requested2026-10-14T21:25:38UTC (October15MSK).
- [Build5820](https://build.youdo.sg/job/dynamic_deploy/5820/) completed FAILURE in74388ms. Fresh API verified all parameters match. master checkout9ad35fb8.
- PostgreSQL uses the credential ssh temporary key, but again fails Host key verification failed before reset. Nginx now authenticates and runs cleanup (rm missing operand ignored, no unreachable). Rabbit401 remains ignored. MSSQL thin, Redis/S3 executed; ES deployment ran. Monolith and Postupdate remain skipped because Restore failed.
- Installed Ansible plugin version635.v34b_48e979c86. Investigation found the earlier agent hostKeyChecking=false insertion ineffective: AnsiblePlaybookStep.setHostKeyChecking is deprecated and has an empty body. Correct supported flag is disableHostKeyChecking=true.
- Corrected just the PostgreSQL stage flag under the existing authorized credential alignment scope. GET verified exact script and unchanged other XML settings. Changed script SHA2565dd2515bb205fe742db1206fe9e6ff9cb4cff28785717bbca2ab713478e3614d to fe0c3a782d18b6d02b889f5b9be27699512134b5fb9fec1b996670c7ebc6482d; exact new ScriptApproval verified, other pending entries preserved. No further build launched.
- User suggested the existing Nginx env.ANSIBLE_HOST_KEY_CHECKING='False' snippet. Live GET confirmed Nginx contains that assignment, explaining its effective host-check override. The corrected plugin flag sets the same environment variable to False for the Ansible invocation; another duplicate env assignment was not added.

## Changed files and validation

Only local helpers/receipts/KB files and authorized PostgreSQL job-setting correction. No repository task files or Git state changed. Scripts compile; exact config GET and ScriptApproval verification passed. Receipt ~/ai-data/jenkins-recovery/test5-deploy-retry-20261015.json. New flag end-to-end acceptance requires a separately authorized deployment.

## Risks and limits

Monolith139914 has not been deployed by either failed attempt. Jenkins credential/root access independently verified, but the full Ansible PG reset after correcting the flag is untested. Rabbit credentials remain unresolved. Existing reset behavior outside minimal migration scope left unchanged.

## Sources

[AnsiblePlaybookStep implementation](https://github.com/jenkinsci/ansible-plugin/blob/master/src/main/java/org/jenkinsci/plugins/ansible/workflow/AnsiblePlaybookStep.java), [environment propagation](https://github.com/jenkinsci/ansible-plugin/blob/master/src/main/java/org/jenkinsci/plugins/ansible/AbstractAnsibleInvocation.java), [prior key alignment](2026-10-15-jenkins-ssh-credential-vk-access.md).

## Authorized third attempt: build5821

User explicitly authorized another launch after the supported host-key flag correction. POST201/queue19132 requested2026-10-14T21:30:27UTC; [build5821](https://build.youdo.sg/job/dynamic_deploy/5821/) FAILURE in74981ms, all submitted parameters match previous attempts. Receipt ~/ai-data/jenkins-recovery/test5-deploy-retry-hostkey-20261015.json.

PostgreSQL SSH now succeeds (unreachable0). First reset task fails rc2 on local socket /var/run/postgresql/.s.PGSQL.5432: Peer authentication failed for user postgres. No PostgreSQL reset change occurred (changed0 failed1). SQL client runs as Unix root with -U postgres. Nginx SSH works; empty cache deletion ignored. Rabbit401ignored3 remains; MSSQL thin, ES, Redis/S3 completed. Monolith and suggestions again skipped.

At user's question about pg_hba, a read-only query executed as Unix postgres succeeded/current_user postgres. Active /etc/postgresql/16/main/pg_hba.conf rules:118 local all postgres peer,123 local all all peer,130 local replication all peer. Minimal candidate adaptation is running existing SQL commands as Unix postgres (become true/become_user postgres), without changing authentication rules. No repository edit or remote pg_hba change performed; repository branch approval is required before an implementation task. [Official peer authentication semantics](https://www.postgresql.org/docs/16/auth-peer.html).

## Proposed supervised branch for peer-auth fix

User requested applying become true/become_user postgres. Before repository file edits, proposed repository /home/slnnk/git/automation-test-yandex, base origin/master, task branch DevOps-892-fix-postgres-restore-user. Approval pending. Scope only playbooks/deploy/db/recreate_db_postgres_monolith.yml, two play-level settings; SQL statements and pre-existing large MSSQL modifications remain unchanged. Prepared candidate outside repository at ~/ai-data/jenkins-recovery/recreate_db_postgres_monolith-candidate.yml; offline syntax-check passed with expected unmatched postgres host warning. No Git state change or repository edit performed yet.

## Peer-auth fix approval, publication and merge

User explicitly approved branch DevOps-892-fix-postgres-restore-user in automation-test-yandex from origin/master. Then user instructed no additional checks, push and merge, then launch job. This directly authorized publication/merge/runtime launch; no additional training-stage confirmation requested.

Fetched master unchanged9ad35fb8; created approved branch in existing checkout. Added exactly become true and become_user postgres at play level in playbooks/deploy/db/recreate_db_postgres_monolith.yml. Original SQL and no-EOF-newline preserved. Staged diff contained only this file, +2/-0; other19modified/untracked files excluded. Additional tests/baseline comparison skipped per user instruction; candidate syntax check passed earlier.

Commit53e96e7d153242068efdca2a21203eb7b44b7ac4, message run postgres restore as postgres. Pushed branch; [MR107](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/107), title DevOps-892 Run PostgreSQL restore as postgres, source approved branch, targetmaster, assignee a.solonenko, squashfalse. Description one Russian paragraph and DevOps-892 link only. Merged through exact-SHA guarded API; merge18c8d0e7ab05fe67df08f7fd1c20efb8127e01f4. No CI configuration change or manual test job started.

User-authorized queue19134 requested2026-10-14T21:37:04UTC, [build5822](https://build.youdo.sg/job/dynamic_deploy/5822/) running. Same parameters/releases as earlier; receipt ~/ai-data/jenkins-recovery/test5-deploy-retry-pg-user-20261015.json.

Read-only console confirms checkout18c8d0e7 and all five PostgreSQL resets complete: ok5changed5failed0unreachable0. Redis/S3/MSSQL thin complete; Rabbit401/Nginx empty cache cleanup ignored. ES deployment ongoing at first checkpoint. Only job outcome monitored, no additional tests.

## Final build5822 log diagnosis (user-requested)

Build5822 FAILURE370631ms. After successful Restore, app_deploy unpacked artifact and generated/patched/merged configs. First blocking task Upload environment.json to buildsinfo returned404 for http://buildapi.yandex-test.youdo.local/upload (prepare_configs.yml125, globalbuildsinfo_addr). Rescue notification to notify_url timed out, secondary to upload failure; recapok44changed13failed1rescued1skipped44.

prepare_configs precedes nomad.yml, so monolith rollout did not run. Post update and Suggestions reindex skipped. User-approved static address commitf424127/MR108 already corrects the shared buildsinfo_addr to http://buildapi.dev.youdo.corp. No extra source edit needed for this observed obsolete URL. Upload against corrected endpoint/full deployment remain unverified; MR108 unmerged.
