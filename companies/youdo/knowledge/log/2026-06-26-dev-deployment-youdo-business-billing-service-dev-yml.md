---
system: dev-deployment
status: verified
checked: 2026-06-26
tags: [helm-charts, dev-yml, onboarding, youdo-business-billing-service, vault, rabbitmq]
---
# Dev deployment: youdo-business-billing-service dev.yml onboarding

- Date: 2026-06-26

## Context

- `/home/slnnk/git/helm-charts` microservice chart and `/home/slnnk/git/youdo-business-billing-service` service repo.
- Task: prepare `devops/dev.yml` for Jenkins ephemeral dev deploy after landings deploy was confirmed successful.

## Actions

- Used `/home/slnnk/git/youdo-business-billing-service/devops/config.yml` as the source of env vars.
- Created `/home/slnnk/git/youdo-business-billing-service/devops/dev.yml`.
- Added namespace-local PostgreSQL via `database.type: pg`.
- Added pre/post migrations using the default `migrations` image and `migrations_env.ConnectionStrings__default: pgService`.
- Added `webapp` component with ingress `youdo-business-billing-service-webapp.dev.youdo.local`.
- Mapped `Sentry__Dsn` through Vault path `dev/projects/youdo-business-billing-service` key `SentryDsn`.
- Mapped RabbitMQ credentials through Vault path `dev/rabbitmq` keys `app-username` and `app-password`.
- Preserved `webEx_check: false` from config.yml by omitting webapp liveness/readiness probes.
- Updated `/home/slnnk/git/helm-charts/docs/agents-ephemeral-deploy-plan.md` item 57 to Done.

## Findings

Result:

- `webapp`: image suffix `webapp`, port `8080`, ingress host `youdo-business-billing-service-webapp.dev.youdo.local`, no probes.
- PostgreSQL and migrations are namespace-local.
- RabbitMQ host is namespace-local `rabbitmq`; virtual host `/`.
- Memory capped at `256Mi`; no CPU requests/limits.

Validation:

- `helm lint ./microservice` passed.
- `helm template test ./microservice --namespace dev-123 --set global.projectName=youdo-business-billing-service-123 --set global.namespace=dev-123 --set global.buildNumber=123 --set image.registry=registry.example.com/youdo-business-billing-service --set image.tag=v1 -f /home/slnnk/git/youdo-business-billing-service/devops/dev.yml` passed.
- Render check confirmed `webapp:v1`, `migrations:v1`, build-specific ingress host, Vault mappings, no webapp probes, and no memory over `256Mi`.

## Changes

- `/home/slnnk/git/youdo-business-billing-service/devops/dev.yml` (created).
- `/home/slnnk/git/helm-charts/docs/agents-ephemeral-deploy-plan.md` item 57.

## Open items

- Deploy through Jenkins and verify runtime startup.
- Before deploy, confirm Vault path `dev/projects/youdo-business-billing-service` has key `SentryDsn`.

## Portable lesson

none
