---
system: mssql
status: verified
checked: 2026-08-02
tags: [mssql, restore, backup, smb, xp_dirtree, sqlcmd, ansible, automation-test-yandex]
---
# Failure restoring YouDo from an MS SQL backup (2026-08-02)

## Task

Restore the `YouDo` database with the procedure `dbo.sp_RestoreDB_FromBackup` through the Ansible role `yandex-mssql-test`; the restore failed.

## Context

- Repository: `/home/slnnk/git/automation-test-yandex`
- Role: `playbooks/roles/yandex-mssql-test`
- SQL Server from the output: `sql_0_1547`; `sqlcmd` launched from host `SQL_0_858`
- Task: restore of the `YouDo` database with the procedure `dbo.sp_RestoreDB_FromBackup`

## Findings

### Symptoms and cause

- SQL Server could not open `\\\\10.16.26.4\\public\\sql\\CleanYouDo.bak`: OS error 2, the file was not found at the computed path.
- In `playbooks/roles/yandex-mssql-test/files/RecreateDBProcedures.sql` the UNC directory is hardcoded as `\\\\10.16.26.4\\public\\sql\\`.
- The procedure looks for the latest directory in the `YYYY_MM_DD` format via `xp_dirtree`. If the directory is not found or the share is not visible, it silently uses the root of the share and builds the path `...\\CleanYouDo.bak`.
- Critical operation-order defect: the procedure drops the snapshots and the source `YouDo` database before `RESTORE FILELISTONLY`. Therefore, when the backup is unavailable, the restore aborts only after the database has already been dropped. The subsequent errors about the missing `CleanYouDo` and `YouDo` are cascading.
- Ansible uses `sqlcmd` without `-b`, so `rc: 0` is possible on SQL errors; failure is detected by an unreliable string check in `failed_when`.

### Access checks performed

- From the local machine `10.16.26.4:445/tcp` is reachable.
- A local SMB2/3 guest session establishes a connection to the server, but authentication is rejected: the server requires signing/encryption, which a guest session does not support. Therefore, without a share account it is impossible to obtain a listing locally and confirm the specific file.
- A read-only `xp_dirtree` call on SQL Server for `\\\\10.16.26.4\\public\\sql\\` returned zero entries. This is consistent either with an empty/missing directory or with the SQL Server service lacking permissions; the procedure did not find the exact file.
- The Ansible task `RestoreDB From Backup`, the related vars/defaults and the initial version of the task in git were checked. It contains only the SQL login password (`mssql_password`) and, separately, the WinRM password for Ansible's connection to the Windows host. There is no SMB account/password, `net use`, `cmdkey` or `New-SmbMapping`. The UNC file is opened directly by the SQL Server service under its own Windows service account.

## Open items

1. On `sql_0_1547`, check as the SQL Server service account the presence and readability of the current file in `\\\\10.16.26.4\\public\\sql\\` and the dated subdirectories.
2. Clarify whether the file server `10.16.26.4` is current; another copy of the SQL script (`playbooks/deploy/db/files/RecreateDBProcedures.sql`) specifies `172.26.0.115`.
3. After the backup is found, restore `YouDo`, if necessary passing the full path explicitly as the second parameter of the procedure.
4. Fix the procedure: before dropping the database, check the existence/readability of the backup and successfully run `RESTORE HEADERONLY`/`FILELISTONLY`; wrap the changes in `TRY/CATCH`.
5. Add `sqlcmd -b` and a non-zero return code check in Ansible.
6. The `dba_automation` password was disclosed in the user's diagnostic output; change it and remove the value from logs/history where possible. The secret value was not copied into this note.

## Portable lesson

`~/ai/general/knowledge/mssql/restore-procedure-drops-db-before-verifying-backup.md`
