---
system: dev-deployment
status: verified
checked: 2026-06-26
tags: [helm-charts, dev-yml, onboarding, youdo-business-landings, nginx, nodejs]
---
# Dev deployment: youdo-business-landings dev.yml onboarding

- Date: 2026-06-26

## Context

- `/home/slnnk/git/helm-charts` microservice chart and `/home/slnnk/git/youdo.business.landings` service repo.
- Task: prepare `devops/dev.yml` for Jenkins ephemeral dev deploy.

## Actions

- Used `/home/slnnk/git/youdo.business.landings/devops/config.yml` as the source of env vars.
- Created `/home/slnnk/git/youdo.business.landings/devops/dev.yml` with `web` and `api` components.
- Changed `/home/slnnk/git/youdo.business.landings/devops/nginx.conf` from `listen 80` to `listen 8080` so Kubernetes targetPort/probes work with the dev chart convention.
- Confirmed dev ingress hosts with the user: `b2b-landings.dev.youdo.local` and `b2b-landings-api.dev.youdo.local`.
- Updated `/home/slnnk/git/helm-charts/docs/agents-ephemeral-deploy-plan.md` item 56 to Done.

## Findings

Result:

- `web`: image suffix `web`, port `8080`, ingress `b2b-landings.dev.youdo.local`, probes on `/`.
- `api`: image suffix `api`, port `8080`, ingress `b2b-landings-api.dev.youdo.local`, probes on `/business/api/public-docs/terms`.
- Memory for both components capped at `256Mi`; no CPU requests/limits.
- Production-only Sentry/S3/DocsStorage variables were not copied because they are absent from `devops/config.yml`; this follows the current dev.yml rule learned from TKB.

Validation:

- `helm lint ./microservice` passed.
- `helm template test ./microservice --namespace dev-123 --set global.projectName=youdo-business-landings-123 --set global.namespace=dev-123 --set global.buildNumber=123 --set image.registry=registry.example.com/youdo-business-landings --set image.tag=v1 -f /home/slnnk/git/youdo.business.landings/devops/dev.yml` passed.
- Render check confirmed `web:v1`, `api:v1`, targetPort/containerPort `8080`, build-specific hosts `b2b-landings-123.dev.youdo.local` and `b2b-landings-api-123.dev.youdo.local`, and no memory over `256Mi`.

## Changes

- `/home/slnnk/git/youdo.business.landings/devops/dev.yml` (created).
- `/home/slnnk/git/youdo.business.landings/devops/nginx.conf` (`listen 8080`).
- `/home/slnnk/git/helm-charts/docs/agents-ephemeral-deploy-plan.md` item 56.

## Open items

- Deploy through Jenkins and verify runtime health.
- If api runtime requires S3/Sentry despite absence in `devops/config.yml`, update the service test config first, then mirror those variables into `dev.yml` through Vault mappings.

## Portable lesson

none
