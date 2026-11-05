---
system: nexus
status: verified
checked: 2026-11-04
tags: [usage, limits, read-only]
---
# Nexus CE usage: October 28 to November 3

## Task

Check Nexus daily request-limit usage for the last week. Seven complete Moscow calendar days: 2026-10-28 through 2026-11-03; current partial day reported separately.

## Context

[Nexus map](../systems/nexus.md), existing DevOps-904 request-reduction item in `~/ai/TODO.md`. Existing verified limit basis: 100,000 requests per rolling 24 hours; calendar totals alone cannot determine compliance.

## Actions

Read-only authenticated GET of usage-history and SSH streaming aggregation of retained request logs. No remote files, configuration, CI, repositories or tracker state changed. Local artifacts: `~/ai-data/nexus-usage/nov04-api.json`, `nov04_week_remote.py`, `nov04-week.json`. Server snapshot 2026-11-04 02:47:45 Moscow.

## Findings

Only `/repository/*` requests count, following the previously reconciled UI/log definition. Parse failures: zero. Included all methods/statuses. Scanned the preceding day too; calculated the exact trailing 86,400-second count at each request and at midnight, sorted by event timestamp. Day boundaries use Moscow UTC+03:00; rolling windows use elapsed seconds.

| Moscow date | Calendar requests | Maximum rolling 24h | Limit usage at peak |
| --- | ---: | ---: | ---: |
| 2026-10-28 | 64,058 | 64,058 | 64.06% |
| 2026-10-29 | 85,896 | 105,806 | 105.81% |
| 2026-10-30 | 93,581 | 97,098 | 97.10% |
| 2026-10-31 | 16,134 | 99,645 | 99.64% |
| 2026-11-01 | 1,953 | 16,134 | 16.13% |
| 2026-11-02 | 74,405 | 74,611 | 74.61% |
| 2026-11-03 | 38,795 | 75,852 | 75.85% |

Seven-day total: 374,822 requests. One date exceeded the limit: October 29, peak 105,806 at 14:58:43 Moscow (+5.806%). October 31 peak 99,645 left only 355 requests of headroom. Current rolling count: 39,366 (39.366%); November 4 partial calendar day: 814 requests. API hourly history (all seven entries labelled November 3) ranges 38,795–50,424 and cannot supply seven distinct calendar days; last API sample 39,202 predates log snapshot. November 3 calendar total 38,795 matches an API sample exactly.

## Changes

Local evidence and this log; added the latest measurement to the existing system map. No infrastructure or application edits.

## Status and risks

Check complete; no background operations remain. Existing DevOps-904 action in `~/ai/TODO.md` remains open: sustained compliance is not achieved, because one rolling peak exceeded the limit. No new implementation is authorized by this inspection. Previously recorded November 13 enforcement date was user-supplied; not revalidated here. No claim about component-count limit or actual blocking is made from request totals alone.

## Portable lesson

none
