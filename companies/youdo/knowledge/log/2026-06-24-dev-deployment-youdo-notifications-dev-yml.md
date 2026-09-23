---
system: dev-deployment
status: verified
checked: 2026-06-24
tags: [helm-charts, dev-yml, onboarding, youdo-notifications, pgservice, rabbitmq, vault]
---
# Dev deployment: youdo-notifications dev.yml onboarding

Date: 2026-06-24
Updated: 2026-06-25

## Context

- Repository: `/home/slnnk/git/helm-charts`
- Service repository: `/home/slnnk/git/youdo.notifications`
- Task: prepare `devops/dev.yml` for Jenkins ephemeral dev deploy via shared `microservice` chart.

## Actions

- Read `docs/agents-ephemeral-deploy-plan.md` and `docs/service-dev-yml-contract.md`.
- Used `/home/slnnk/git/youdo.notifications/devops/config.yml` as the source for dev/test variables.
- Created `/home/slnnk/git/youdo.notifications/devops/dev.yml`.
- Confirmed Ingress hostname with user: `youdo-notifications.dev.youdo.corp`.
- Validated rendering with:
  `helm template test ./microservice --namespace dev-123 --set global.projectName=youdo-notifications-123 --set global.namespace=dev-123 --set-string global.buildNumber=123 --set image.registry=registry.example.com/youdo-notifications --set image.tag=v1 -f /home/slnnk/git/youdo.notifications/devops/dev.yml`
- Ran `helm lint ./microservice`; lint passed with only the chart icon recommendation.

## Findings

Result:
- `webapp` service uses image suffix `webapp`, exposes Ingress `youdo-notifications.dev.youdo.corp`, rendered as `youdo-notifications-{BUILD_NUMBER}.dev.youdo.corp`.
- `worker` service uses image suffix `worker`, no Ingress.
- Pre/post migration jobs use image suffix `migrations`; because `config.yml` explicitly has `ConnectionStrings__default` for migrations, `dev.yml` keeps `migrations_env.ConnectionStrings__default: pgService`. The `microservice` chart now expands `pgService` in `migrations_env` the same way it expands it in normal `env`.
- Follow-up audit of already onboarded services found `youdo.kitcut` still had a manual `migrations_env.Postgres__ConnectionString`; changed it to `pgService`.
- The chart now also expands `pgService` in `services[].env`, needed for `youdo-business-tickets` `ConnectionStrings__LlmPg`.
- Rendered all already onboarded services and confirmed no literal `pgService` remains in manifests.
- PostgreSQL is namespace-local via `database.type: pg`.
- RabbitMQ uses namespace-local host `rabbitmq`; username/password come from Vault path `dev/rabbitmq`.
- Sentry DSN comes from Vault path `dev/projects/youdo-notifications`, key `SentryDsn`.
- Runtime follow-up on 2026-06-25: worker health probes were removed from `/home/slnnk/git/youdo.notifications/devops/dev.yml` because worker does not expose `/_/heartbeat`; user confirmed `youdo-notifications` works after this change.

## Changes

- `/home/slnnk/git/youdo.notifications/devops/dev.yml` (created; worker probes removed on 2026-06-25).
- `/home/slnnk/git/youdo.kitcut/devops/dev.yml` (`migrations_env` switched to `pgService`).
- `microservice` chart: `pgService` expansion in `migrations_env` and `services[].env`.

## Open items

- Continue with the next service onboarding; for `youdo-notifications`, the known worker probe issue is closed.

## Portable lesson

none
