---
system: dotnet
status: verified
checked: 2026-09-01
tags: [testcontainers, postgresql, timezone, CURRENT_DATE, DateTime.Now, flaky-tests, month-boundary]
---
# Integration tests fail only in the first hours of a month: process clock vs database clock

## Symptom

A handful of date-based integration tests (monthly aggregates, "last N months" risk rules)
fail with off-by-one results such as `expected 3, found 2` or a flag that should be `true`
being `false`. The same commit passed an hour earlier; the failing commit touched nothing near
the tests. The job started shortly after local midnight on the 1st of the month.

## Cause

The test builds its "current month" from the **process** clock (`DateTime.Now` in the
runner's local timezone, e.g. UTC+3), while the SQL under test computes the month from the
**database** clock (`CURRENT_DATE`, `now()`) inside a Testcontainers PostgreSQL that runs in
UTC. For a few hours after local midnight the two disagree on which month is current, so
rows inserted "this month" by the test are "next month" for the database and get excluded by
predicates like:

```sql
r.operation_time < date_trunc('month', CURRENT_DATE) + interval '1 month'
```

Anchoring timestamps to the 15th protects against day/DST conversion, but not against the
two clocks naming different months.

## Fix

Preferred: take the anchor from the same clock the SQL uses.

```csharp
var currentMonth = await connection.ExecuteScalarAsync<DateTime>(
    "select date_trunc('month', CURRENT_DATE)::date");
```

Or use `DateTime.UtcNow` everywhere and make the SQL use `timezone('UTC', now())`.

Infrastructure alternative (simpler, but environment-dependent): pin both sides to one zone,
e.g. start the container with `-c timezone=Europe/Moscow` (Testcontainers:
`.WithCommand("-c", "timezone=Europe/Moscow")`) and run tests with `TZ=Europe/Moscow`.

## Limits

- Retrying "later in the day" hides the failure until the next month boundary; the window
  recurs every month for (UTC offset) hours.
- Applies equally to MSSQL (`GETDATE()` vs `SYSUTCDATETIME()`) and any DB with its own
  session timezone.
