---
system: dev-deployment
status: verified
checked: 2026-06-25
tags: [helm-charts, dev-yml, onboarding, youdo-sms-service, rabbitmq, vault]
---
# Dev deployment: youdo-sms-service dev.yml onboarding

Date: 2026-06-25
Updated: 2026-06-25

## Context

- Repository: `/home/slnnk/git/helm-charts`
- Service repository: `/home/slnnk/git/youdo-sms-service`
- Task: prepare `devops/dev.yml` for Jenkins ephemeral dev deploy via shared `microservice` chart.

## Actions

- Read `docs/agents-ephemeral-deploy-plan.md` and `docs/service-dev-yml-contract.md`.
- Used `/home/slnnk/git/youdo-sms-service/devops/config.yml` as the source for dev/test variables.
- Created `/home/slnnk/git/youdo-sms-service/devops/dev.yml`.
- Confirmed Ingress hostname with user: `youdo-sms-service.dev.youdo.corp`.
- Validated rendering with:
  `helm template test ./microservice --namespace dev-123 --set global.projectName=youdo-sms-service-123 --set global.namespace=dev-123 --set-string global.buildNumber=123 --set image.registry=registry.example.com/youdo-sms-service --set image.tag=v1 -f /home/slnnk/git/youdo-sms-service/devops/dev.yml`
- Ran `helm lint ./microservice`; lint passed with only the chart icon recommendation.

## Findings

Result:
- `webapp` service uses image suffix `webapp`, exposes Ingress `youdo-sms-service.dev.youdo.corp`, rendered as `youdo-sms-service-{BUILD_NUMBER}.dev.youdo.corp`.
- `worker` service uses image suffix `worker`, no Ingress, and no health probes.
- Pre/post migration jobs use image suffix `migrations`; because `config.yml` explicitly has `ConnectionStrings__default` for migrations, `dev.yml` keeps `migrations_env.ConnectionStrings__default: pgService`.
- PostgreSQL is namespace-local via `database.type: pg`.
- RabbitMQ uses namespace-local host `rabbitmq`; `RabbitMq__Url` is built as `amqp://$(RabbitMq__Username):$(RabbitMq__Password)@rabbitmq/`, with username/password read from namespace Secret `rabbitmq-auth` keys `rabbitmq-app-username` and `rabbitmq-app-password`.
- Sentry DSN comes from Vault path `dev/projects/youdo-sms-service`; only key names are recorded here, not values.
- Follow-up sync on 2026-06-25 after `devops/config.yml` changed on `master`: removed obsolete `IntellinSmsProviderSettings__Login`, `IntellinSmsProviderSettings__Password`, and `DevinoSmsProviderSettings__ApiKey` from `dev.yml`; kept only `Sentry__Dsn` in Vault mapping; added worker env `Admin__SendDirectAllowedPhones: "1,2"`.
- Runtime validation: user reported Jenkins deploy completed successfully after these changes.

## Changes

- `/home/slnnk/git/youdo-sms-service/devops/dev.yml` (created, then synced with `master` `config.yml`).

## Open items

- `youdo-sms-service` dev deploy flow is validated. Continue with next service onboarding or Jenkins smoke check hardening.

## Portable lesson

none
