---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [postgres, featuretoggle, test5]
---
# Featuretoggle stand clones from configured test5

## Summary

User requested copying configured featuretoggle-test5 to test,test1-test4,test6-test7,test10-test15. Read-only preflight: all13destinations absent at10.18.26.39. Source198features/301history/fourVersionInfo rows. Prepared one-snapshot pg_dump/pg_restore clone command; user-approved clone execution completed and verified for all13destinations.

## Task and context

Test5 features were configured by user after seed and MD5 auth recovery; source must be the current test5, not the original stand-independent template. Previous work: [seed/auth](2026-10-15-nomad-test-featuretoggle-test5-seed.md).

## Actions and findings

SSH youdo@10.18.26.39, sudo -n -u postgres. Verified source tables and exact target database absence. Source owner postgres, encodingUTF8, collate/ctypeC.UTF-8. ID sequence states399/529, bothis_called=true.

Prepared /home/slnnk/ai-data/featuretoggle-test5/clone-stands.py plan|apply. Read-only plan passed after accounting for source ownerpostgres. Proposed target owner youdo permits service connection and migrations. One custom-format pg_dump stays in remote process memory; each new DB created from template0 and restored atomically with roleyoudo/no-owner/no-privileges. No existing DB overwrite, source disconnect/restart, original template change, deploy or service restart. Compare ordered hashes/counts for all three tables plus sequences against source before dump; assert source unchanged before creating destinations. Stop on first failure; earlier completed targets remain reported, no automatic deletion.

## Changed files and risks

Only local helper and KB notes changed. The approved external clone command completed successfully. New DBs will contain copied history user IDs as part of explicitly requested clone. Concurrent source changes abort preparation; later source edits naturally diverge from the one snapshot. Service rollout and UI access on other stands not included. Pending work tracked in ~/ai/TODO.md.

## Approval, execution and results

User explicitly replied `Да` to creation of13databases from the current configured test5 snapshot with owneryoudo. Executed `python3 /home/slnnk/ai-data/featuretoggle-test5/clone-stands.py apply`; exit0, verified_count13, source_unchanged=true. Completed featuretoggle-test, featuretoggle-test1 through-test4, featuretoggle-test6 through-test7, featuretoggle-test10 through-test15.

Each target restored successfully with198features/301history/fourVersionInfo rows; ordered table content hashes matched source for all three tables and sequence states matched399/529, bothis_called=true. No source disconnections or service restarts. One dump reused for all destinations; no dump stored on disk. Application deployment/UI verification on target stands was not performed.

## Main template refresh preparation

User next requested updating stand-independent featuretoggle from configured test5. Read-only preflight: main149features/293history/fourVersionInfo and no other active connections; test5198features/301history/fourVersionInfo. Schemas and migration versions match; AppliedOn metadata differs and will be copied as data. Prepared /home/slnnk/ai-data/featuretoggle-test5/refresh-template.py plan|apply; plan passed. Apply creates protected full custom-format backup under /var/tmp on DB host, validates backup archive, copies all three tables and sequences from test5 into main in one transaction (TRUNCATE RESTART IDENTITY plus data-only dump), checks table hashes and sequence states. Source, schema/extensions and existing database owner preserved. User explicitly approved; refresh completed and verified below.

## Main template refresh execution

User replied `Да` to reviewed main template overwrite with backup. Executed refresh-template.py apply, exit0/verified=true/source_unchanged=true. Full pre-refresh backup at10.18.26.39:/var/tmp/featuretoggle-before-test5-refresh-20261015T144416Z-2gy3p95c.dump,57470bytes, mode0600, archive listing validated. Main featuretoggle now198features/301history/fourVersionInfo rows; ordered hashes match test5 for all three tables, sequences399/529is_called=true. Main schema/extensions/owner unchanged. No source mutation or service restart.
