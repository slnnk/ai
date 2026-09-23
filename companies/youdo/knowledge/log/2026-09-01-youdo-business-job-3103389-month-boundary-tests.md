---
system: youdo-business
status: verified
checked: 2026-09-01
tags: [gitlab-ci, dotnet-unit-tests, integration-tests, timezone, postgresql, testcontainers, month-boundary]
---
# youdo.business job 3103389: CompanyRisks tests fail at month boundary

Date: 2026-09-01 (Europe/Moscow)

## Task

Explain the CompanyRisks integration test failures in job `3103389`.

## Context

- GitLab project: `youdo/microservices/youdo.business` (project ID 423).
- Job: `3103389`, `dotnet-unit-tests`, pipeline `137723`.
- MR ref: `refs/merge-requests/3567/head`.
- Commit: `0982af7cf57f64af6b0f605e10551c3fb09cedcf` (`Merge branch 'master' into DevOps-689-k8s`).
- Runner: `gitlab-runner-docker-1 integrations-tests (172.28.0.171)`.
- Started: `2026-09-01 01:58:50 +03:00`, which is still `2026-08-31 22:58:50 UTC`.

## Findings

### Result

The ordinary unit-test assembly passed: 379/379. The integration-test assembly failed 9 of 590 tests; all failures are in:

- `CompanyRisks/LongTermPartnershipRiskTests`;
- `CompanyRisks/SignificantIncomeShareRiskTests`.

The characteristic errors are one missing calendar month (`expected 3, found 2`; `expected 6, found 5`) and risks expected to be realised becoming false.

### Root cause

The tests construct `_currentMonth` from the test process `DateTime.Now`. At job start Moscow local time was already September 1. The PostgreSQL Testcontainers instance uses its own/default timezone and the SQL views calculate their month with `CURRENT_DATE`; at the same instant UTC was still August 31. The tests therefore inserted September as the current month, while PostgreSQL still considered August current and excluded the future September receipt via:

```sql
r.operation_time < date_trunc('month', CURRENT_DATE) + interval '1 month'
```

This produces exactly the observed off-by-one results. Anchoring receipt timestamps on the 15th protects timestamp conversion, but does not synchronize which calendar month the test process and PostgreSQL call current.

The previous job for the same MR, `3103125`, passed at `2026-08-31 22:31 +03:00`, before the Moscow month rollover. The failing merge commit changed frontend files and did not modify the CompanyRisks tests, handlers, or SQL views. The `devops/dev.yml` Staging change is not consumed by this test job and is unrelated.

### Recommended fix

Preferred robust correction: derive the integration-test month anchor from PostgreSQL `CURRENT_DATE`, the same clock used by the views, instead of process `DateTime.Now`. This makes the tests deterministic across runner/database timezone differences.

An infrastructure-level alternative is to configure both the test process and PostgreSQL container explicitly to the same timezone (for example PostgreSQL `-c timezone=Europe/Moscow` plus runner `TZ=Europe/Moscow`). This is simpler but leaves the tests dependent on environment configuration.

The failure should disappear naturally once UTC also reaches September, but retrying later only masks the recurring three-hour failure window at every month boundary.

## Changes

No source or CI change was made during this diagnostic turn.

## Portable lesson

[`~/ai/general/knowledge/dotnet/integration-tests-fail-at-month-boundary-timezone-mismatch.md`](../../../../general/knowledge/dotnet/integration-tests-fail-at-month-boundary-timezone-mismatch.md)
