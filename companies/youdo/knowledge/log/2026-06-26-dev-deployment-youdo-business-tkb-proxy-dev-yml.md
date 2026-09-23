---
system: dev-deployment
status: verified
checked: 2026-06-26
tags: [helm-charts, dev-yml, onboarding, youdo-business-tkb-proxy, vault, rabbitmq]
---
# Dev deployment: youdo-business-tkb-proxy dev.yml onboarding

- Date: 2026-06-26

## Context

- `/home/slnnk/git/helm-charts` microservice chart and `/home/slnnk/git/youdo-business-tkb-proxy` service repo.
- Task: prepare `devops/dev.yml` for Jenkins ephemeral dev deploy, analogous to the successfully deployed Tochka proxy flow.

## Actions

- Read `docs/agents-ephemeral-deploy-plan.md` and recorded plan item 54 before edits.
- Used `/home/slnnk/git/youdo-business-tkb-proxy/devops/config.yml` as the source of test/dev env variables.
- Compared with `/home/slnnk/git/youdo-business-tochka-proxy/devops/dev.yml` and `.gitlab-ci.yml` image names.
- Created `/home/slnnk/git/youdo-business-tkb-proxy/devops/dev.yml`.
- Updated `docs/agents-ephemeral-deploy-plan.md` item 54 to Done.

## Findings

Result:

- Components: `web`, `mock-api`, `worker`, `worker-mock`.
- Images are resolved as `registry/.../web`, `mock-api`, `worker`, `worker-mock`, and `migrations` according to `.gitlab-ci.yml`.
- PostgreSQL: single namespace-local DB, matching TKB `devops/config.yml`; unlike Tochka, no second mock DB was added.
- Migrations: pre/post migrations use the default `migrations` image and `ConnectionStrings__default: pgService`.
- RabbitMQ: namespace-local `rabbitmq`, credentials from Vault path `dev/rabbitmq` keys `app-username` and `app-password`.
- Service secrets: Vault path `dev/projects/youdo-business-tkb-proxy`, keys `SentryDsn` and `TkbBankApiKey`.
- Ingress hosts: `youdo-business-tkb-proxy-webapp.dev.youdo.local` and `youdo-business-tkb-proxy-mock-webapp.dev.youdo.local`; chart renders build-specific hosts with `-{BUILD_NUMBER}`.
- Ports: container/probe port `8080`; Kubernetes Service port remains `80`.
- Memory: all workloads and migrations cap at `256Mi`; no CPU requests/limits.

Validation:

- `helm lint ./microservice` passed.
- `helm template test ./microservice --namespace dev-123 --set global.projectName=youdo-business-tkb-proxy-123 --set global.namespace=dev-123 --set global.buildNumber=123 --set image.registry=registry.example.com/youdo-business-tkb-proxy --set image.tag=v1 -f /home/slnnk/git/youdo-business-tkb-proxy/devops/dev.yml` passed.
- Render check confirmed images, `-123` ingress hosts, `8080` container/probe ports, Vault mappings, and no memory over `256Mi`.

## Changes

- `/home/slnnk/git/youdo-business-tkb-proxy/devops/dev.yml` (created).
- `/home/slnnk/git/helm-charts/docs/agents-ephemeral-deploy-plan.md` item 54.

## Open items

- Deploy through Jenkins and verify runtime health/logs.
- Confirm Vault path `dev/projects/youdo-business-tkb-proxy` contains `SentryDsn` and `TkbBankApiKey` before deploy.

## Portable lesson

none
