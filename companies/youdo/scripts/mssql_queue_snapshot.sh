#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  mssql_queue_snapshot.sh [--host HOST] [--container NAME] [--user USER]

Collect a lightweight SQL Server queue/load snapshot from a Dockerized MSSQL
instance over SSH.

Defaults:
  --host       root@sc-except01.youdo.corp
  --container data-mssql-1
  --user       sa

The script expects SQL Server password to be available inside the container as
SA_PASSWORD. It does not print the password.
EOF
}

host="root@sc-except01.youdo.corp"
container="data-mssql-1"
sql_user="sa"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host)
      host="${2:?--host requires a value}"
      shift 2
      ;;
    --container)
      container="${2:?--container requires a value}"
      shift 2
      ;;
    --user)
      sql_user="${2:?--user requires a value}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

sql="
SET NOCOUNT ON;
SELECT
  (SELECT COUNT(*) FROM sys.dm_exec_requests WHERE session_id > 50) AS active_requests,
  (SELECT COUNT(*) FROM sys.dm_exec_sessions WHERE is_user_process = 1) AS user_sessions,
  (SELECT COUNT(*) FROM sys.dm_exec_requests WHERE session_id > 50 AND wait_type LIKE 'LCK%') AS lock_waits,
  (SELECT COUNT(*) FROM sys.dm_exec_requests WHERE session_id > 50 AND status IN ('running','runnable')) AS running_runnable;

SELECT TOP 10
  command,
  status,
  wait_type,
  blocking_session_id,
  COUNT(*) AS cnt
FROM sys.dm_exec_requests
WHERE session_id > 50
GROUP BY command, status, wait_type, blocking_session_id
ORDER BY cnt DESC;
"

remote_cmd=$(cat <<EOF
date -u '+%F %T UTC'
docker stats --no-stream --format 'cpu={{.CPUPerc}} mem={{.MemUsage}} pids={{.PIDs}}' '$container'
docker exec '$container' bash -lc '/opt/mssql-tools/bin/sqlcmd -S localhost -U "$sql_user" -P "\$SA_PASSWORD" -l 30 -h -1 -W -s "|" -Q "$sql"'
EOF
)

ssh -o BatchMode=yes "$host" "$remote_cmd"
