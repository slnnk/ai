---
system: mssql
status: verified
checked: 2026-06-13
tags: [sql-server-linux, docker, vm.max_map_count, OutOfMemoryException, error-701]
---
# SQL Server on Linux crashes with OutOfMemoryException at the default vm.max_map_count

## Symptom

A containerized SQL Server (Linux) exits with code 1 and is not restarted;
port 1433 is down. `docker inspect` shows `OOMKilled=false`, no memory limit,
disk is not full and the kernel log has no OOM killer entries. The SQL errorlog
before the crash contains:

- many `Not enough storage is available to process this command` read warnings
  for the `.mdf` file;
- `Error: 701 ... There is insufficient system memory in resource pool
  'internal' to run this query`;
- finally `Unhandled Exception: System.OutOfMemoryException`.

The crash dump metadata (`/var/opt/mssql/log/`) shows
`VMA Count: 65532  VMA Limit: 65530  Percent VMA Used: 100`.

## Cause

SQL Server's Linux host extension maps memory in many small regions. When the
process reaches the kernel per-process limit of memory mappings
(`vm.max_map_count`, default `65530`), `mmap` fails and SQL Server reports it as
internal memory pressure and I/O read failures, then aborts. It is a mapping
count limit, not a byte limit, so it happens with plenty of free RAM and disk.

## Fix

Raise the limit on the host (the container shares the kernel value) and make
it persistent, then start the container and run an integrity check because the
engine logged read failures on the data file:

```bash
sysctl -w vm.max_map_count=262144
echo 'vm.max_map_count=262144' > /etc/sysctl.d/99-mssql.conf
docker compose -f /path/docker-compose.yml up -d mssql
# inside the container
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -Q "DBCC CHECKDB ([DbName]) WITH NO_INFOMSGS, ALL_ERRORMSGS;"
```

Also add `restart: unless-stopped` (or `always`) to the compose service so a
crash does not turn into an outage, and consider `max server memory` plus a
Docker memory limit.

## Limits

- Verified on `mcr.microsoft.com/mssql/server:2017-CU15-ubuntu`; newer versions
  raise the same error but Microsoft's docs recommend the higher
  `vm.max_map_count` for all SQL Server on Linux installs.
- Expect a load spike after recovery: clients that queued writes/deletes
  during the outage flood the instance with lock waits (`LCK_M_*`) and high
  CPU; that is backlog, not a second failure.
- `DBCC CHECKDB` on a ~20 GB database took about 15 minutes on 2 vCPU.
