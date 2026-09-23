---
system: youdo-business
status: verified
checked: 2026-09-22
tags: [nomad, yandex-test, hangfire, postgresql, permission-denied, youdo-business-tickets]
---
# 2026-09-22: youdo-business-tickets-test13 worker cannot create Hangfire schema

## Task

Explain why the worker task of Nomad job `youdo-business-tickets-test13` kept failing after deployment.

## Context

- Investigation date: 2026-09-22, Europe/Moscow.
- Environment: Nomad `yandex-test`, namespace `default`.
- Job: `youdo-business-tickets-test13`.
- Fresh allocation after manual rerun: `642a0c8f-7f98-8652-9a42-50e8173946e0`, job version 1, node `nomad-agent-test-02`.
- Image version: `site-25535-support-chat-attachments-138638`.
- Source commit: `9de5242a6ecde94598fc37e78f0e064e3e450353`.
- Related GitLab pipeline/job: pipeline `138638`, deploy job `3165888`.
- Repository: `/home/slnnk/git/youdo-business-tickets`.

## Findings

### Verified failure chain

1. The pre-migration lifecycle task exits successfully with code 0.
2. API, web, and bot start successfully.
3. `youdo-business-tickets-worker-test13` fails during Hangfire initialization and repeats after restart.
4. PostgreSQL returns SQLSTATE `42501`: `permission denied for database test13_youdo-business-tickets`.
5. The failing statement is `CREATE SCHEMA "hangfire"` from `Hangfire.PostgreSql.PostgreSqlObjectsInstaller.Install`.
6. The exception propagates through `Infrastructure.BackgroundJob.Hangfire.SetupExtensions.AddHangfire` line 22 and `Worker.Program.Main` line 13.
7. The process aborts in `entrypoint.sh`, producing container exit code 134. Nomad reports `oom_killed=false`.
8. The same failure happened on the previous deployment across several Nomad clients, so this is not a node-specific or image-pull problem.

### Root cause

The recreated/new test database does not contain the Hangfire schema, while the application database role does not have permission to create schemas in that database. Hangfire attempts automatic object installation at worker startup, and the unhandled database authorization error terminates the worker.

### Remediation options

- Preferred least-privilege path: create schema `hangfire` in `test13_youdo-business-tickets` as an administrative/provisioning role, set the appropriate owner/grants for the application role, then rerun/restart the job.
- Alternatively, grant the application role enough database-level privilege to create the schema, let Hangfire initialize it, and revoke the extra privilege afterward if policy requires it.
- Long term: make test database provisioning/migrations create and grant the Hangfire schema explicitly so recreated stands do not depend on application-time DDL privileges.

Do not treat sibling exit 137 or the Nomad progress deadline as the primary failure. The primary fault is PostgreSQL authorization during Hangfire schema installation.

## Actions

Read-only diagnostics used:

- Nomad HTTP API: job allocations, allocation state, client task logs.
- Worker stderr/stdout from allocation `642a0c8f`.
- Local source and deployment metadata from the Nomad job.

No job, database, or infrastructure mutation was performed during the investigation.

### Resolution verification

After the user launched a new deployment with database recreation:

- new allocation `d5ea7ec9-546e-5be9-b558-294d6fcb55bc` on `nomad-agent-test-01` became healthy;
- Nomad deployment `3d1fff1e` completed successfully with one healthy and zero unhealthy allocations;
- pre-migrations completed with exit code 0;
- worker remained running with zero restarts;
- worker stderr was empty and no Error/Fatal/exception entries were present in stdout;
- Hangfire logged `Hangfire SQL objects installed.`, announced its server, and started all dispatchers;
- MassTransit connected successfully to the `test13` RabbitMQ virtual host.

This confirms that database recreation/provisioning restored sufficient database ownership or schema-creation rights and resolved the original startup failure.

## Portable lesson

[`~/ai/general/knowledge/dotnet/hangfire-postgresql-create-schema-permission-denied.md`](../../../../general/knowledge/dotnet/hangfire-postgresql-create-schema-permission-denied.md)
