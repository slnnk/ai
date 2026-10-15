---
system: postgresql
status: verified
checked: 2026-10-16
tags: [postgresql, pgbouncer, tochka, devops-898]
---
# DevOps-898 Tochka PgBouncer routes and connection verification

## Summary

User explicitly requested adding Tochka PgBouncer routes after the analogous TKB failure. Parent agent added12 scoped routes on B2B PostgreSQL10.18.26.44 and reloaded PgBouncer without changing PID43719, existing TKB routes or authentication. Actual application credentials passed24/24 SELECT1 checks across12databases and ports5432/5433. User subsequently explicitly approved both service retries. Parent started six ordinary Tochka jobs3230100–3230105/test10–test15 with DB recreation; all six are now SUCCESS, with Nomad running/healthy/restarts0 at2026-10-15 21:08:48UTC (2026-10-16 Moscow).

## Context and diagnosis

[Pipeline141011](https://gitlab.youdo.sg/youdo/microservices/youdo-business-tochka-proxy/-/pipelines/141011), project492, release master-1767. Pipeline root status success did not represent stand deployment success: ordinary jobs3229834,3229835,3229838 for test10–test12 failed; jobs3229840,3229843,3229847 for test13–test15 were canceled. All six reached Run nomad task. Nomad jobs were dead with restart count2 in the parent snapshot. Evidence `/home/slnnk/ai-data/DevOps-898/tochka-failed-deploy-preflight.json`.

Nomad test10 allocation5f0e2c43-d6f4-22c0-8b3f-674160299f7d proxy-worker and mock-worker both logged Fatal Application not started with Npgsql.PostgresException SQLSTATE08P01 and password authentication failure. Each worker restart count1. The inspected migration tasks had no matching authentication error. Raw logs/configurations and credentials were not copied.

Actual generated DB names from all six GitLab traces: test10_youdo-business-tochka-proxy and test10_youdo-business-tochka-proxy_1, with corresponding pairs for test11,test12,test13,test14,test15. Config origin/master devops/config.yml9–12 specifies b2b pool, auto DB name and db_count2; pre/post migrations for both databases are enabled. Observed historical fatal was authentication failure; a missing-database error was not observed in the inspected logs.

## Approval, action and verification

User explicitly said to add PgBouncer routes for Tochka. Parent executed `/home/slnnk/ai-data/DevOps-898/b2b-pgbouncer-routes.py --service youdo-business-tochka-proxy --apply`. Exit0; twelve routes added in `/etc/pgbouncer/pgbouncer.ini`. Existing authentication, TKB routes and settings preserved. Reload only; PID43719 unchanged. No PostgreSQL restart, repository changes or service deployment retry.

Parent then executed read-only `/home/slnnk/ai-data/DevOps-898/tkb-pgbouncer-readcheck.py --service youdo-business-tochka-proxy`, deriving actual task credentials in memory without persisting their values. Both databases on every target stand passed SELECT1 on direct PostgreSQL5432 and PgBouncer5433:24/24 successful. This proves current credential-and-route connectivity after the earlier shared TKB SCRAM authentication repair and these added routes; it does not prove a deployment has been retried or is healthy.

## Risks and limits

Scope limited to12Tochka database routes for test10–test15 on B2B10.18.26.44. C2C PostgreSQL is separate and untouched. Historical failed allocations were replaced by the approved ordinary retries; current rollout accepted through GitLab/Nomad statuses. No HTTP/Consul/business probes were performed.

## Authorized rollout continuation

At 2026-10-15 21:03:55 UTC, Tochka retry jobs3230100–3230102/test10–test12 SUCCESS with Nomad running/healthy, restarts0. test13–test15/jobs3230103–3230105 pending. Read-only monitor `/home/slnnk/ai-data/DevOps-898/bank-rollout-status.py` saves sanitized current statuses to `tochka-pgbouncer-retry-status.json`. No further retries or source changes made.

## Final Tochka acceptance

2026-10-15 21:08:48UTC (2026-10-16 Moscow): all six ordinary retry jobs3230100–3230105/test10–test15 SUCCESS. All six current Nomad allocations master-1767 running/healthy=true/restarts0. Verification used GitLab deployment jobs and Nomad statuses only. Source repositories unchanged. Sanitized final artifact `/home/slnnk/ai-data/DevOps-898/tochka-pgbouncer-retry-status.json`.
