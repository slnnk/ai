---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [postgres, featuretoggle, test5]
---
# Featuretoggle test5 seed preparation

## Summary

Read-only preflight verified restored PostgreSQL source `featuretoggle` on `10.18.26.39` and empty destination `featuretoggle-test5`. Source has 149 features and 293 history rows; column schemas and four migration versions match. User explicitly approved the seed; copy completed and ordered data hashes matched the source.

## Task and context

User requested copying restored, stand-independent featuretoggle data to test5 during MSSQL recovery. The service actually uses PostgreSQL. Superpowers skills excluded by user.

## Actions and findings

Access: SSH `youdo@10.18.26.39`, local key `~/.ssh/id_ed25519`, then `sudo -n -u postgres`. Root SSH rejected. `psql -X -P pager=off` confirmed both databases; checked exact table counts, columns, constraints and migration versions. Source and target each have four VersionInfo rows. Target data tables both empty.

Prepared `/home/slnnk/ai-data/featuretoggle-test5/seed.py plan|apply`; plan passed. Apply copies only features and features_history with IDs and relations preserved, in one transaction with destination table locks and empty-table guards, then sets sequences from copied IDs and compares ordered data hashes. VersionInfo and source are untouched. Data streams remain in remote process memory; no copied personal data stored locally.

## Changed files and risks

Local seed helper and this note only. No repository changes. The approved external data copy completed successfully. Apply aborts if source row counts change, columns/migrations mismatch or target is nonempty. Service writes can affect post-commit verification; no service restart is planned. User replied `Да` to the exact seed proposal; the single approved command was executed successfully.

## Approved execution and verification

User approved copying 149 features and 293 history records to test5. Executed `python3 /home/slnnk/ai-data/featuretoggle-test5/seed.py apply`; exit0, verified=true. Destination counts149/293 and ordered content SHA256 values exactly matched source. Sequence state: features_id_seq350/is_called=true; features_history_id_seq521/is_called=true. Source and VersionInfo were not modified. No restart or deployment performed.

## Production CSV comparison

User supplied `/home/slnnk/features_202610151634.csv`,198rows, columns id/key/enabled/created/scope/description. Fresh read-only test5 export has149rows. Keys are unique in both exports; service repository GetAsync/SetAsync identifies features by key. Exactly49production keys missing ontest5 (38enabled/11disabled). All149existing test keys present in production CSV;31existing enabled values differ and will be preserved.

Prepared `/home/slnnk/ai-data/featuretoggle-test5/add-missing-prod.sql`: transaction, table lock, assertion49keys still missing, insert production key/enabled/created/scope/description using new test IDs. No existing row updates, history copy or source-template writes. Missing-key CSV and before snapshot in same local artifact directory. User approved and the remote insert completed; verification below.

## Approved production-key insert result

User explicitly replied `Да` to the49-key insert proposal. Executed prepared add-missing-prod.sql through SSH/psql on featuretoggle-test5: INSERT49, COMMIT, exit0. New IDs351–399. Read-only export confirmed198total keys, no missing production-CSV keys, all149pre-existing rows unchanged across all exported columns. All49new rows match CSV enabled/scope/description/created values (38enabled/11disabled), with independent test IDs. Existing31enabled differences remain preserved. Verification receipt: `/home/slnnk/ai-data/featuretoggle-test5/prod-add-verification.json`. Initial local timestamp comparison hit Python3.8 fromisoformat variable-fraction limitation; strptime parsing passed; no additional DB writes. History unchanged by insert SQL.

## Featuretoggle UI failure and production auth comparison

After seed user reported Venus feature-toggle generic loading failure. Read-only diagnostics: featuretoggle-test5 allocation36593983-6d9a-4ed6-5c96-8a41620a72f9, API10.18.26.38:24861, running0restarts. Direct GET /api/v1/features?scope=youdo returned500. Service logs show `System.NotSupportedException: Authentication method not supported (Received: 10)` from old Npgsql during DB authentication. UI request chain: Venus POST /api/feature-toggle/search -> service POST /api/v1/features/search; additional GetAll scope youdo also fails. Data is populated; DB authentication blocks reads.

Test PostgreSQL16 password_encryption=scram-sha-256; shared login youdo has SCRAM verifier and host-all-youdo0.0.0.0/0 SCRAM rule. Multiple services use this shared role. Prepared pg-auth-compat.py plan passed: existing live featuretoggle password verified via TCP, exact HBA rule located. No apply authorized or run. User questioned cross-service impact; explained shared-role change affects reconnects and proposed isolated featuretoggle role/config as an alternative. No alternative implementation or approval yet.

User stated production is Selectel managed PostgreSQL with no admin catalog/HBA access. Probed production C2C master.93570de9-4f4b-4932-9f57-b641e7ceb290.c.dbaas.selcloud.ru for user youdo/database featuretoggle on5432direct and5433pooler. Both returned AuthenticationMD5Password/code5. Probe sends StartupMessage only and closes before password; no authentication completed and no SQL executed. Helper: /home/slnnk/ai-data/featuretoggle-test5/probe-auth.py. This verifies client-facing MD5 on both paths; does not inspect stored verifier or hidden HBA. Production untouched.

References: https://www.postgresql.org/docs/current/protocol-message-formats.html and https://docs.selectel.ru/en/managed-databases/postgresql/connect-to-cluster/ . Reusable existing recipe: general/knowledge/postgresql/npgsql-authentication-method-not-supported-scram.md.

## Approved auth change and final scope correction

User first requested MD5 for all on test. Applied five host auth rules MD5, shared youdo existing password MD5 verifier, ALTER SYSTEM password_encryption=md5, reload. Role grafana_test verifier remained SCRAM because only a SCRAM secret is available in PgBouncer userlist; no plaintext password was available. First featuretoggle GET scope youdo returned200/189features.

User then narrowed scope: only youdo. Broad change had already completed; this was disclosed immediately. Applied requested narrowing: restored original generic loopback/replication SCRAM host rules from backup, kept remote IPv4 youdo MD5 rule and added explicit loopback IPv4/IPv6 MD5 exceptions for youdo before generic rules. ALTER SYSTEM RESET password_encryption restored effective scram-sha-256 for future password writes. Reload only, no restart. Current youdo verifier MD5 with unchanged password; grafana_test verifier SCRAM unchanged.

Backups: /etc/postgresql/16/main/pg_hba.conf.before-featuretoggle-md5-20261015T134714Z (initial configuration), /etc/postgresql/16/main/pg_hba.conf.before-youdo-only-20261015T134755Z (intermediate broad configuration). No HBA parse errors. Final direct GET http://10.18.26.38:24861/api/v1/features returned200 and198feature records. Protocol startup probe confirmed MD5/code5 for youdo/featuretoggle-test5 at10.18.26.39:5432. Browser session itself not tested; API is now readable. Existing youdo consumers share the same unchanged password; individual service reconnects were not forced.

Historical helper pg-auth-compat.py represents superseded broad scope and must not be rerun; final scope is only youdo.
