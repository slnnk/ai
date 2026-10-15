---
system: postgresql
status: verified
checked: 2026-10-15
tags: [pgbouncer, antifraud, DevOps-899]
---

## Summary

User requested minimal PgBouncer authorization and Antifraud return to PgBouncer, without pool tuning. Live configuration applied; SELECT authenticated successfully through5433 against existing test4/test5 Antifraud databases. Antifraud MR146 merged and release23.8.8 pipeline140992 launched. Deployment not yet established.

## Scope and approvals

Stage1 branch DevOps-899-restore-pgbouncer-connections from origin/masterfb11521 explicitly approved before repository edits. Stage2 exact devops/config.yml +3/-3 runtimeports5432to5433, commit restore pgbouncer connections, MR DevOps-899 restore pgbouncer connections, source approvedbranch to master, Russianparagraph+DevOps-899link explicitly approved with merge,23.8.8tag onmergemaster and fourimagebuilds. User instructed cancel MRpipeline and merge without waiting; cancellation requested for140991(ref refs/merge-requests/146/head), not release140992.

A separate question proposed deploy ontest2/test3/test4/test5/test7 with ANSIBLE_SKIP_TAGS=dropdb to preserveexistingDBs; user response addressed MRpipeline cancellation/merge rather than explicitly confirming this deployment stage. No deploy jobs were played yet.

## Infrastructure changes

Host10.18.26.39: /etc/pgbouncer/pgbouncer.ini gained five explicit mappings antifraud2-test2/test3/test4/test5/test7 to same-namedlocalPG5432DBs. auth_file /etc/pgbouncer/userlist.txt gained youdo verifier copied in memory from pg_authid. Existing MD5 roleverifier/auth_type retained; password never printed or persisted in localartifacts. Existing Grafana SCRAMentry preserved. Fileowner/modes preserved, backup suffix .devops-899-antifraud-before; reload succeeded and serviceactive. Poolmode/defaultpoolsize/limits unchanged. SELECTcurrent_database/current_user through5433 with existingappcredentials succeeded in antifraud2-test4 and antifraud2-test5. No DBcreation/removal/sessiontermination.

## Repository and release

Only devops/config.yml three runtimeports changed. YAML/exactreplacement/diffcheck passed. Commit31af35774dd740c5170a1e91ea6f2be8237dfd8e. MR https://gitlab.youdo.sg/youdo/microservices/antifraud2/-/merge_requests/146 merged asb02e317a752ede337a0d5bfadca475e1af31cc8f. Tag23.8.8 points exactly to thatmergemaster. Fourimagebuilds3228846-3228849, releasepipeline https://gitlab.youdo.sg/youdo/microservices/antifraud2/-/pipelines/140992 . Productiondeploy remainsmanual.

## Evidence and limits

~/ai-data/jenkins-recovery/antifraud-pgbouncer899 contains redactedplan/applied/authverification/MRmerge/tag/pipeline receipts. Helpers configure-antifraud-pgbouncer899.py, verify-antifraud-pgbouncer899.py, antifraud-pgbouncer-release899.py. Runtimeconfigiscurrentlycanonical; noactiveAnsibleconfigsourcefound. Sessionpoolingunchangedwillnotguaranteereductionofpersistentidleconnections; connectioncapacityincidentnotdeclaredresolved.

## Final build-only scope

User explicitly selected "Пока только сборка" for rollout approval. No23.8.8deploy jobs played and no BuildAPIversionupdate. Releasepipeline140992 reachedmanual: build-api3228846, scheduler3228847, service3228848, migrations3228849 allSUCCESS; tests3228850SUCCESS. MRpipeline140991CANCELEDterminal verified. Fourbuilds tookabout200–320seconds; prepare18.5seconds. Futuredeploymentrequiresnewexplicitapproval; existingappsremainontheirpreviousruntimeconfigs. PgBouncer auth/mappings are applied andverifiedindependently.
