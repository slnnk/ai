---
system: dev-deployment
status: verified
checked: 2026-06-25
tags: [helm-charts, dev-yml, onboarding, youdo-business-tochka-proxy, mockdb, migrations, vault]
---
# Dev deployment: youdo-business-tochka-proxy dev.yml

Date: 2026-06-25

## Context

- Helm charts repository: `/home/slnnk/git/helm-charts`
- Service repository: `/home/slnnk/git/youdo-business-tochka-proxy`
- Target file: `/home/slnnk/git/youdo-business-tochka-proxy/devops/dev.yml`
- Source config: `devops/config.yml`, checked against `devops/production.hcl` and service source.

User confirmations:
- The service needs two PostgreSQL databases: one for proxy and one for mock.
- Proxy web ingress host: `youdo-business-tochka-proxy-webapp.dev.youdo.local`
- Mock web ingress host: `youdo-business-tochka-proxy-mock-webapp.dev.youdo.local`

## Actions

Implemented:
- Added `devops/dev.yml` for four images/components:
  - `proxy-webapp`
  - `mock-webapp`
  - `proxy-worker`
  - `mock-worker`
- Added four migration jobs:
  - `migrations` use `migrations_env.ConnectionStrings__default: pgService`.
  - `mock_migrations` use `mock_migrations_env.ConnectionStrings__default: pgMockService`.
- Used namespace-local RabbitMQ service `rabbitmq`.
- Since Tochka proxy uses separate RabbitMQ settings rather than a full interpolated URL, `RabbitMq__Username` and `RabbitMq__Password` are supplied through the service `secrets` block from Vault path `dev/rabbitmq`.
- Capped all workload and PostgreSQL memory requests/limits at `256Mi`.
- Set all service container ports and probes to `8080`; Kubernetes Service port remains `80` and targets `8080`.
- Used Vault paths from production patterns for S3 and TochkaBank/Sentry secret material; no secret values were copied into notes or configs.

## Changes

Chart changes:
- `microservice` now supports `database.mockDB: true`, creating `{projectName}-mock` in the same dev PostgreSQL pod.
- Added `pgMockService` alias for service env and mock migrations.
- Added `mock_migrations` and `mock_migrations_env`.
- Fixed `migrations[].env` so the `pgService` and `pgMockService` aliases expand like `migrations_env` and `services[].env`.

Service: `/home/slnnk/git/youdo-business-tochka-proxy/devops/dev.yml` (created).

## Findings

Validation:
- `helm lint ./microservice` passed.
- `helm template` for `youdo-business-tochka-proxy-123` rendered:
  - two ingress hosts with build suffix `-123`;
  - main and mock database connection strings;
  - PostgreSQL postStart creation of the mock database;
  - all app resources at `256Mi`.

## Open items

- Deploy via Jenkins and verify migrations, pod readiness, RabbitMQ auth, VaultStaticSecret sync, and both ingress health endpoints.

## Portable lesson

none
