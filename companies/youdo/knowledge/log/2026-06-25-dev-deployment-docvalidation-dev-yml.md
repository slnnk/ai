---
system: dev-deployment
status: verified
checked: 2026-06-25
tags: [helm-charts, dev-yml, onboarding, docvalidation, postgresql, npgsql, md5, scram, loki]
---
# Dev deployment: docvalidation dev.yml onboarding

Date: 2026-06-25

## Context

- Repository: `/home/slnnk/git/helm-charts`
- Service repository: `/home/slnnk/git/docvalidation`
- Task: prepare `devops/dev.yml` for Jenkins ephemeral dev deploy via shared `microservice` chart.

## Actions

- Read `docs/agents-ephemeral-deploy-plan.md` and `docs/service-dev-yml-contract.md`.
- Used `/home/slnnk/git/docvalidation/devops/config.yml` as the source for dev/test variables.
- Created `/home/slnnk/git/docvalidation/devops/dev.yml`.
- Confirmed Ingress hostname with user: `docvalidation.dev.youdo.corp`.
- Validated rendering with:
  `helm template test ./microservice --namespace dev-123 --set global.projectName=docvalidation-123 --set global.namespace=dev-123 --set-string global.buildNumber=123 --set image.registry=registry.example.com/docvalidation --set image.tag=v1 -f /home/slnnk/git/docvalidation/devops/dev.yml`
- Ran `helm lint ./microservice`; lint passed with only the chart icon recommendation.

## Findings

Result:
- `api` service uses image suffix `api`, exposes Ingress `docvalidation.dev.youdo.corp`, rendered as `docvalidation-{BUILD_NUMBER}.dev.youdo.corp`.
- `service` uses image suffix `service`; no Ingress and no health probes.
- `scheduler` uses image suffix `scheduler`; no Ingress and no health probes.
- Pre/post migration jobs use image suffix `migrations`; no `migrations_env` is set because `config.yml` has no `pre_migrations_env` or `post_migrations_env`. The chart still provides its standard `CON_STR` for PostgreSQL migrations.
- PostgreSQL is namespace-local via `database.type: pg`.
- RabbitMQ uses namespace-local host `rabbitmq`; `RabbitMq__Url` is built as `amqp://$(RabbitMq__Username):$(RabbitMq__Password)@rabbitmq/`, with username/password read from namespace Secret `rabbitmq-auth` keys `rabbitmq-app-username` and `rabbitmq-app-password`.
- `Exceptional` comes from Vault path `resources/databases/mssql`, key `logreader_conn_string`; no secret values are recorded here.
- `YouDoApi__Endpoint` has dependency routing for `youdo-business`: default `http://youdo-business-mock-api.dev.youdo.corp`, selected template `http://youdo-business-mock-api-{buildId}.dev.youdo.corp`.
- `Cerberus__Endpoint` is fixed to `http://cerberus-api.proxy-sel.youdo.local` because `cerberus2` is not part of the B2B Jenkins deploy list.

Risks / next steps (at onboarding time):
- First Jenkins deploy should verify access to Vault path `resources/databases/mssql`.
- First Jenkins deploy should verify RabbitMQ env expansion and `api` `/hc`.
- The `microservice` chart currently still renders ClusterIP Services for `service` and `scheduler` even with `service.enabled: false`; this is due to template default behavior and is a chart cleanup candidate.

## Runtime check: dev-93

Date: 2026-06-25

Findings:
- `api` pod was in `CrashLoopBackOff`; logs showed the application started and listened on `http://[::]:8080`, while kubelet probes targeted `:80/hc`. Kubelet killed the pod after liveness failures.
- `scheduler` pod stayed Running but logged repeated `Npgsql` errors: `Authentication method not supported (Received: 10)`. PostgreSQL 16 in the namespace used `scram-sha-256` auth, unsupported by this service's old Npgsql client.

Fix prepared:
- Set `/home/slnnk/git/docvalidation/devops/dev.yml` `services[].name=api` `port: 8080`.
- Changed `microservice` chart PostgreSQL defaults to md5 auth for ephemeral dev: `POSTGRES_HOST_AUTH_METHOD=md5` and `password_encryption=md5`.

Next step:
- Redeploy `docvalidation` and verify `api` is Ready and scheduler no longer logs the Npgsql auth error.

## Runtime check: dev-94

Date: 2026-06-25

Findings:
- `docvalidation-94-api`, `docvalidation-94-service`, and `docvalidation-94-scheduler` were all `Running` with zero restarts; migration jobs were `Completed`.
- API logs showed the application listening on `http://[::]:8080`, and probes now target port `8080`.
- Scheduler still logged `Npgsql` `Authentication method not supported (Received: 10)` after the first chart md5 change.
- Postgres deployment contained `POSTGRES_HOST_AUTH_METHOD=md5` and `password_encryption=md5`; live Postgres also reported `password_encryption = md5`, and `pg_hba.conf` had `host all all all md5`.
- The root cause was the stored role password: `pg_authid` showed `youdo` still had a `SCRAM-SHA-256` password hash.

Actions:
- Changed `microservice/templates/postgres-deployment.yaml` to add a `postStart` hook for md5 mode. The hook waits for Postgres and rewrites the current role password after init so the stored hash becomes `md5...`.
- Applied the equivalent SQL manually in ephemeral namespace `dev-94` to verify the diagnosis: `SET password_encryption = 'md5'; ALTER ROLE CURRENT_USER WITH PASSWORD ...`.
- Rechecked `pg_authid`; `youdo` password prefix changed to `md5`.
- Rechecked fresh scheduler logs; jobs completed normally and no new `Authentication method not supported` errors appeared.
- Revalidated locally with `helm template` for `docvalidation` and `helm lint ./microservice`.

Result:
- `dev-94` is healthy after the md5 role password rewrite.
- The persisted chart change should make future ephemeral PostgreSQL deployments compatible with services using old Npgsql clients.

## Runtime check: dev-95 all prepared services

Date: 2026-06-25

Context:
- Namespace: `dev-95`
- Services observed: `docvalidation`, `youdo-business-auth-service`, `youdo-business-doc-generator`, `youdo.kitcut`, `youdo.notifications`, `youdo-sms-service`, plus namespace-local RabbitMQ and Redis.

Findings:
- All migration jobs completed successfully.
- All running app deployments were Ready except `youdo-notifications-95-worker`.
- `youdo-notifications-95-worker` stayed `Pending` because the only node had insufficient schedulable memory. The pod requests `512Mi` memory and limits `1Gi`; the node was already at about 97% allocated memory requests.
- Fresh logs for the running app deployments had no `Error`, `Fatal`, `Exception`, old Npgsql auth error, panic, or crash matches.
- All namespace-local Postgres roles checked in `dev-95` had `md5...` password hashes for role `youdo`.
- Some Postgres pods had a single restart due to the first md5 `postStart` hook racing PostgreSQL init before `POSTGRES_DB` existed. They recovered and were Running, but the chart hook was made more robust.

Actions:
- Updated `microservice/templates/postgres-deployment.yaml` so the md5 `postStart` hook retries the actual `psql` role password rewrite through the `postgres` database until it succeeds.
- Validated with `helm template` for `docvalidation` and `helm lint ./microservice`.

Result:
- `dev-95` is mostly healthy; the remaining blocker is cluster capacity for `youdo-notifications-95-worker`, not an application crash.
- Future Postgres deployments should avoid the one-time `FailedPostStartHook` restart caused by the init race.

Follow-up:
- User approved stopping Loki because it was not needed temporarily.
- Scaled `loki` namespace workloads down: `deployment/loki-read` to 0 replicas; `statefulset/loki-backend`, `loki-chunks-cache`, `loki-results-cache`, and `loki-write` to 0 replicas.
- Stopped `daemonset/loki-canary` by patching a non-matching node selector: `loki.youdo/disabled=true`.
- After Loki stopped, node memory requests dropped from about `12746Mi/13442Mi` to about `7178Mi/13442Mi`.
- `youdo-notifications-95-worker` scheduled and became Ready; fresh logs showed PostgreSQL readiness and MassTransit bus start.
- Rollback path for Loki: restore original replica counts (`loki-read=2`, `loki-backend=2`, `loki-chunks-cache=1`, `loki-results-cache=1`, `loki-write=2`) and remove the `loki.youdo/disabled` nodeSelector from `daemonset/loki-canary`.

## Changes

- `/home/slnnk/git/docvalidation/devops/dev.yml` (created; `api` port 8080).
- `microservice` chart PostgreSQL defaults: `POSTGRES_HOST_AUTH_METHOD=md5`, `password_encryption=md5`, and a retrying `postStart` hook that rewrites the role password to an md5 hash.
- Live: Loki workloads in namespace `loki` scaled to zero (rollback path above).

## Open items

- Chart cleanup: Services still rendered for `service`/`scheduler` with `service.enabled: false`.
- Restore Loki when needed using the recorded replica counts.

## Portable lesson

`~/ai/general/knowledge/postgresql/npgsql-authentication-method-not-supported-scram.md`
