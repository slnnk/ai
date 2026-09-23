---
system: mssql
status: verified
checked: 2026-08-02
tags: [restore, backup, unc, xp_dirtree, sqlcmd, ansible, t-sql]
---
# Restore procedure drops the database before checking the backup; sqlcmd hides the error

## Symptom

An automated "recreate test database from backup" step leaves the environment
with no database at all. The SQL output shows
`Cannot open backup device '\\server\share\path\Clean.bak'. Operating system
error 2 (The system cannot find the file specified)`, followed by cascading
errors that the restored database and the original database do not exist.
The Ansible task that ran it reports `rc: 0`.

## Cause

Three independent defects that compound:

1. The stored procedure resolves the backup location with `xp_dirtree` over a
   hardcoded UNC share and picks the newest `YYYY_MM_DD` folder. When the share
   is not visible to the SQL Server service account (or is empty), the loop
   finds nothing and silently falls back to the share root, producing a path
   that does not exist. `xp_dirtree` returning zero rows is indistinguishable
   from "no permission".
2. The procedure drops snapshots and the target database *before* it runs
   `RESTORE FILELISTONLY`/`RESTORE DATABASE`. A missing backup therefore
   destroys data instead of failing early.
3. `sqlcmd` without `-b` exits 0 on T-SQL errors; the caller relied on a
   `failed_when` string match on the output.

The UNC file is opened by the SQL Server *service account*, not by the
`sqlcmd` login and not by the automation's WinRM/SSH user, so the share
permissions to check are those of the service account.

## Fix

In the procedure:

```sql
-- validate before any destructive step
RESTORE HEADERONLY FROM DISK = @BackupFile;     -- fails fast if the file is unreadable
RESTORE FILELISTONLY FROM DISK = @BackupFile;
BEGIN TRY
    -- drop snapshots / SET SINGLE_USER WITH ROLLBACK IMMEDIATE / DROP DATABASE
    -- RESTORE DATABASE ... WITH MOVE ..., REPLACE
END TRY
BEGIN CATCH
    THROW;   -- surface the error, do not fall back to a guessed path
END CATCH;
```

Accept the full backup path as an explicit parameter and fail if the
`xp_dirtree` lookup returns no folder instead of defaulting to the share root.

In the automation:

```yaml
- name: restore
  ansible.windows.win_command: sqlcmd -S {{ host }} -U {{ user }} -P {{ pass }} -b -Q "EXEC dbo.sp_RestoreDB_FromBackup"
  register: r
  failed_when: r.rc != 0
```

To check the share from the SQL side without touching data:
`EXEC xp_dirtree '\\server\share\path', 1, 1;`

## Limits

- `-b` makes `sqlcmd` return 1 on any error of severity >= 11; warnings still
  pass.
- Guest SMB sessions cannot be used to verify the share from a Linux
  controller when the server requires signing/encryption; test as the service
  account on the SQL host instead.
- Keep only one copy of the procedure source; two copies with different file
  server addresses were the second half of this incident.
