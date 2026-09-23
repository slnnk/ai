---
system: dev-deployment
status: verified
checked: 2026-06-25
tags: [helm-charts, dev-yml, onboarding, fns, routing, vault, rabbitmq]
---
# Dev deployment: Fns dev.yml onboarding

Date: 2026-06-25

## Context

- Repository: `/home/slnnk/git/helm-charts`
- Service repository: `/home/slnnk/git/Fns`
- Task: prepare `devops/dev.yml` for Jenkins ephemeral dev deploy via shared `microservice` chart.

## Actions

- Read `docs/agents-ephemeral-deploy-plan.md` and `docs/service-dev-yml-contract.md`.
- Used `/home/slnnk/git/Fns/devops/config.yml` as the source for dev/test variables.
- Confirmed ingress hostname with user: `fns.dev.youdo.corp`.
- Created `/home/slnnk/git/Fns/devops/dev.yml`.
- Validated rendering with:
  `helm template test ./microservice --namespace dev-123 --set global.projectName=fns-123 --set global.namespace=dev-123 --set-string global.buildNumber=123 --set image.registry=registry.example.com/fns --set image.tag=v1 -f /home/slnnk/git/Fns/devops/dev.yml`

## Findings

Result:
- `api` service uses ingress `fns.dev.youdo.corp`, rendered as `fns-{BUILD_NUMBER}.dev.youdo.corp`, and probes `/health`.
- `service` and `scheduler` are configured without Ingress and with `memory`/`memoryLimit` capped at `256Mi`.
- PostgreSQL is namespace-local via `database.type: pg`, with `memory` and `memoryLimit` both set to `256Mi`.
- RabbitMQ uses namespace-local host `rabbitmq`; `RabbitMq__Url` is built as `amqp://$(RabbitMq__Username):$(RabbitMq__Password)@rabbitmq/`, with username/password read from namespace Secret `rabbitmq-auth`.
- `Exceptional` comes from Vault path `resources/databases/mssql`, key `logreader_conn_string`, matching the `docvalidation` pattern.
- `FnsAuthServiceClient__OpenApiMasterToken` comes from Vault path `dev/projects/fns`, key `openapi_master_token`.
- `DocValidationClient__BaseAddress` uses dependency routing for `docvalidation`: default `http://docvalidation.dev.youdo.corp/api/v1`, selected template `http://docvalidation-{buildId}.dev.youdo.corp/api/v1`.

Validation:
- `helm template` rendered successfully for the `fns` values file.
- Rendered manifests kept memory requests/limits at or below `256Mi`.

Notes:
- The current `microservice` chart still renders `Service` objects for `service` and `scheduler` even when `service.enabled: false`; this is the same template behavior already tracked in the main plan.

## Changes

- `/home/slnnk/git/Fns/devops/dev.yml` (created).

## Portable lesson

none
