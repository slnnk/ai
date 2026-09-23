---
system: postgresql
status: verified
checked: 2026-06-23
tags: [postgresql, disk-space, hangfire, index-bloat, pg-b2b-test, zabbix]
---
# pg-b2b-test / PostgreSQL /data space check

## Task

Zabbix free space warning for `/data` on `pg-b2b-test`; find what consumes the space.

## Context

Date: 2026-06-23 MSK
Host: root@10.16.26.27 (`pg-b2b-test`)
Service: `postgresql@16-main.service`, PostgreSQL 16/main, port 5433
Data dir: `/data/main16`
Alert context: Zabbix free space warning for `/data`.

## Findings

### Current state

- `/data`: 59G total, 51G used, 5.5G free, 91% used.
- `/data/main16`: 51G.
- `/data/main16/base`: 50G.
- `/data/main16/pg_wal`: 1.2G.
- `/data/backup`: 8K.

Conclusion: disk usage is from PostgreSQL database heap/index files under `base`, not WAL or backups.

### Largest databases

- `test14_youdo-business`: 9848 MB
- `test15_youdo-business`: 6735 MB
- `test16_youdo-business`: 5546 MB
- `test10_youdo-business`: 4913 MB
- `test_youdo-business`: 4611 MB
- `test12_youdo-business`: 3897 MB
- `test11_youdo-business`: 3867 MB

### Largest objects observed

Repeated source of size: Hangfire tables/indexes plus log/event tables.

Examples:

- `test14_youdo-business`
  - `hangfire.state`: 3521 MB total, 1219 MB heap, 2301 MB indexes.
  - `hangfire.jobparameter`: 2894 MB total, 272 MB heap, 2622 MB indexes.
  - `public.entity_attribute_logs`: 1614 MB total.
  - Largest indexes: `hangfire.state.state_pkey` 1762 MB, `hangfire.jobparameter.ix_hangfire_jobparameter_jobidandname` 1541 MB, `hangfire.jobparameter.jobparameter_pkey` 1080 MB.
- `test15_youdo-business`
  - `hangfire.state`: 2197 MB total, 1564 MB indexes.
  - `public.entity_attribute_logs`: 1720 MB total.
  - `hangfire.jobparameter`: 1126 MB total, 960 MB indexes.
- `test16_youdo-business`
  - `public.entity_attribute_logs`: 2951 MB total.
  - `hangfire.jobparameter`: 544 MB total.
  - `hangfire.job`: 540 MB total.
  - `public.platform_events`: 420 MB total.
- `test10_youdo-business`
  - `hangfire.state`: 2387 MB total, 1692 MB indexes.
  - `hangfire.jobparameter`: 1142 MB total, 978 MB indexes.
  - `hangfire.job`: 761 MB total, 648 MB indexes.
- `test_youdo-business`
  - `public.platform_events`: 1192 MB total.
  - `hangfire.job`: 879 MB total, 706 MB indexes.
  - `hangfire.jobparameter`: 721 MB total.

Autovacuum is active, but Hangfire indexes are very large compared with live table heap in several test DBs. This suggests accumulated Hangfire history plus possible index bloat.

## Actions

Commands used:

- `df -h /data`
- `du -xhd1 /data | sort -h | tail -20`
- `pg_lsclusters`
- `du -xhd1 /data/main16 | sort -h | tail -20`
- `sudo -u postgres psql -p 5433 -F '|' -Atqc "select datname, pg_size_pretty(pg_database_size(oid)), pg_database_size(oid) from pg_database order by pg_database_size(oid) desc;"`
- Per-large-DB metadata queries against `pg_class`, `pg_namespace`, `pg_stat_user_tables`, `pg_stat_user_indexes`.

## Open items

Follow-up / safe options:

- Confirm whether old `test*` databases can be dropped or archived. Dropping unused test DBs is the quickest way to return space.
- Review Hangfire retention/cleanup in `test*_youdo-business`; tables `hangfire.state`, `hangfire.jobparameter`, `hangfire.job`, `hangfire.jobqueue`, `hangfire.lock`, `hangfire.counter` are repeated growth sources.
- If rows are already cleaned up, consider `REINDEX CONCURRENTLY` on large Hangfire indexes. This requires enough temporary/free disk headroom and should be planned carefully because only 5.5G is free now.
- For log tables (`entity_attribute_logs`, `platform_events`, `employee_logs`), check product retention policy before deleting/truncating.

## 2026-06-23 11:33 MSK follow-up check

Read-only SSH check on `root@10.16.26.27`.

- User context: before this check, the `hangfire` schema was manually removed and related services were restarted so they could recreate the schema.
- Host time: `Tue Jun 23 11:33:08 AM MSK 2026`.
- `/data`: 59G total, 24G used, 33G free, 42% used.
- This is a major improvement from the earlier 91% used / 5.5G free state.

Top 10 databases by `pg_database_size`, PostgreSQL port `5433`:

- `test_youdo-business`: 4611 MB
- `test16_youdo-business`: 3735 MB
- `test15_youdo-business`: 2229 MB
- `test14_youdo-business`: 1943 MB
- `test9_youdo-business`: 1927 MB
- `test3_youdo-business`: 1799 MB
- `test_youdo-business-tickets`: 644 MB
- `test6_youdo-business`: 608 MB
- `test13_youdo-business`: 603 MB
- `test15_youdo-business-tochka-proxy_1`: 370 MB

Command used:

- `ssh -o BatchMode=yes -o ConnectTimeout=10 root@10.16.26.27 "hostname; date; df -h /data; sudo -u postgres psql -p 5433 -F '|' -Atqc \"select datname, pg_size_pretty(pg_database_size(oid)) as pretty_size, pg_database_size(oid) as bytes from pg_database order by pg_database_size(oid) desc limit 10;\""`

## Portable lesson

none
