---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [cerberus, pgbouncer, gitlab, DevOps-899]
---
# Cerberus PgBouncer source MR, 30-second shutdown and 20-stand pool capacity

## Summary

Published Cerberus runtime PgBouncer settings and 30-second shutdown timeout as [MR117](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/117), subsequently user-merged and verified. Applied approved PgBouncer capacity for up to 20 Antifraud and 20 Cerberus stands plus Grafana, adding only mappings for existing Cerberus databases. Applied the 30-second timeout to the existing test1 pilot. Other stands have not been rolled out; backend saturation was last observed, so capacity relief and sustained Cerberus readiness are not claimed.

## Task, approvals and training record

User requested 30-second stop timeout, publication of persistent Cerberus PgBouncer source settings, and PgBouncer sized for 20 Antifraud/Cerberus stands plus Grafana. Stage 1 asynchronous approval explicitly confirmed branch `DevOps-899-use-pgbouncer-for-cerberus` from master in `automation-test-yandex`. Fetched and switched in the existing checkout; all 16 unrelated MSSQL modified/untracked paths were preserved, with no worktree or stash.

User clarified that capacity should cover 20 stands but new mappings should be added only for existing databases. This config-capacity request authorized the scoped apply; no broader service rollout, merge or membership cleanup was inferred.

Stage 2 asynchronous approval covered the reviewed exact publication names/scope: commit `use pgbouncer and extend cerberus shutdown timeout`; MR title `DevOps-899 use PgBouncer and extend Cerberus shutdown timeout`; source `DevOps-899-use-pgbouncer-for-cerberus` to master. Staged only the task template, inspected exact staged diff and committed `461bb0534ebf5210d68f7862cf2268164cf903ec`, pushed and created MR117. Assignee a.solonenko, squash false and remove-source true preserved. Description is one short Russian paragraph plus task link, stored at `/home/slnnk/ai-data/jenkins-recovery/cerberus-pgbouncer-publication/mr-description.txt`. Read-only verification passed after one transient network timeout. No merge, ordinary deployment or other stand switch was performed; no CI configuration and pipelines list empty.

## Repository changes and checks

Only `playbooks/deploy/docker/files/nomad_cerberus/cerberus.j2` changed, +8/-4: four runtime task kill_timeout values set to 30s and four PostgreSql assignments given Port=5433 and No Reset On Close=true. Pre/post migration connection strings remain direct 5432; existing recreation policy and all other task settings retained.

Exact staged diff contained only that file. In-memory template rendering and nomad validate passed for test, test1 and test15; diff check passed. Remote MR verification passed. Publication changes future deployments after merge; it does not automatically switch the remaining current direct clients.

## Applied PgBouncer capacity

Helper `/home/slnnk/ai-data/jenkins-recovery/size-c2c-pgbouncer-20-stands.py`; receipt `/home/slnnk/ai-data/jenkins-recovery/c2c-pgbouncer-capacity20/applied.json`. On C2C 10.18.26.39, added 13 mappings for existing Cerberus databases, yielding 14 Cerberus transaction pools, each maximum 10/minimum 0/reserve 0. Preserved all 14 existing Antifraud transaction mappings with maximum 2 each; eight Antifraud databases currently exist, while six pre-existing mappings without current databases were preserved. No additional nonexistent database mappings were introduced.

Grafana remains session mode, pool_size 20/max_db_connections 20. Capacity budget is 20*10 Cerberus + 20*2 Antifraud + 20 Grafana = 260 PostgreSQL backends. Shared youdo max_user_connections increased 20 to 250; max_client_conn 1000 to 3000. File-descriptor soft limit increased 2048 to 4096, hard limit 524288 retained, persisted in existing `/etc/systemd/system/pgbouncer.service.d/devops-899-client-limit1000.conf` and applied with daemon-reload/prlimit. PgBouncer configuration reloaded without restart, PID 114852 unchanged. Authentication and existing Antifraud mapping settings verified unchanged.

Backups: `/etc/pgbouncer/pgbouncer.ini.before-20-stand-capacity-20261015` and `/etc/systemd/system/pgbouncer.service.d/devops-899-client-limit1000.conf.before-20-stand-capacity-20261015`.

## Applied test1 timeout and final runtime limits

Direct Nomad CAS update of test1 changed ModifyIndex 19922 to 21058/version 2, touching only four runtime timeouts to 30 seconds. Plan: one in-place update, zero destructive updates; migration settings and databases unchanged. Receipts `/home/slnnk/ai-data/jenkins-recovery/cerberus-pgbouncer-test1/timeout-plan.json` and timeout-applied.json.

Final read asserted all four runtime timeouts 30 seconds and PgBouncer 5433. Current allocation 25545ef6-c94a-26e7-985f-665a65751fa9 version 2 was running/healthy with zero restarts at that moment. This is a snapshot, not sustained readiness acceptance; the [earlier membership/startup diagnosis](2026-10-15-nomad-test-cerberus-test1-pgbouncer-pilot.md) is not declared resolved.

Final PostgreSQL audit at 20:56:52 UTC found no PgBouncer waiting, but 1000 client backends (mostly idle), pg_stat_activity 1005 including five auxiliary processes, and 777 idle Cerberus connections. Only test1 runtime uses PgBouncer; the other 13 existing Cerberus stands remain direct. New pool capacity does not release those existing direct connections. MR merge/rollout and any membership recovery remain separate approved actions; no database cleanup was performed.

## User merge verification (2026-10-16 local date)

User reported merging MR117. Direct GET confirmed state merged, merged_at 2026-10-15T23:58:44.928+03:00, merge commit 078c906b24fb5883395a2b76bd3964fbc4598d84, squash commit null. Fetched origin/master now points to that merge; its Cerberus template bytes exactly match reviewed source commit 461bb0534ebf5210d68f7862cf2268164cf903ec. Source persistence is complete, so future ordinary deployments use the updated template.

The user's merge report does not authorize deployment. No infrastructure write, deployment, local branch switch or local Git merge was performed in this verification. Remaining 13 stands have not been switched through the merged template; rollout and sustained runtime verification remain pending.

## Final changed scope

Repository task file, scoped local helper/receipts and KB bookkeeping only, plus the explicitly authorized PgBouncer configuration/limit and test1 runtime timeout changes described above. Unrelated MSSQL work preserved. No secrets are recorded here. Central follow-up in `~/ai/TODO.md` covers source merge/rollout, membership recovery and sustained verification; notes contain no separate task backlog.
