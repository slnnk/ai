---
system: dev-deployment
status: verified
checked: 2026-06-26
tags: [helm-charts, dev-yml, onboarding, youdo-business-mobile-id, external-image, vault, routing]
---
# Dev deployment: youdo-business-mobile-id dev.yml onboarding

- Date: 2026-06-26

## Context

- `/home/slnnk/git/helm-charts` microservice chart and `/home/slnnk/git/youdo-business-mobile-id` service repo.
- Task: prepare `devops/dev.yml` for Jenkins ephemeral dev deploy after reviewing the successful user-updated TKB proxy dev.yml.

## TKB conclusion used for this work

- The final successful TKB `dev.yml` follows `devops/config.yml` strictly, not production.hcl and not the full Tochka shape.
- Only components enabled/described in test config should be deployed. For TKB that meant `mock-api` and `worker-mock`, not production-only `web`/`worker`.
- Do not add service-specific secrets absent from `config.yml`; TKB kept Sentry/RabbitMQ only.

## Actions

Mobile ID actions:

- Added minimal `microservice` chart support for `services[].image` as a full image override, needed by `external_image: mobile1d/test-mno:v1.0.6`.
- Documented `services[].image` in `docs/service-dev-yml-contract.md`.
- Created `/home/slnnk/git/youdo-business-mobile-id/devops/dev.yml` from `devops/config.yml`.
- Described two components: `web` and external `mobileid`.
- Kept namespace-local RabbitMQ (`rabbitmq`) and Redis (`redis:6379`).
- Moved `Sentry__Dsn`, `Mts__YouDoPrivateSigKeyBase64`, and `Mts__YouDoPrivateEncKeyBase64` to Vault path `dev/projects/youdo-business-mobile-id`.
- Mapped RabbitMQ credentials from Vault path `dev/rabbitmq` keys `app-username` and `app-password`.
- Added self routing for MTS callback/JWKS URLs so build-specific hosts are rendered.
- Capped memory at `256Mi`; no CPU requests/limits.

## Findings

Validation:

- `helm lint ./microservice` passed.
- `helm template test ./microservice --namespace dev-123 --set global.projectName=youdo-business-mobile-id-123 --set global.namespace=dev-123 --set global.buildNumber=123 --set image.registry=registry.example.com/youdo-business-mobile-id --set image.tag=v1 -f /home/slnnk/git/youdo-business-mobile-id/devops/dev.yml` passed.
- Render check confirmed `web:v1`, full external image `mobile1d/test-mno:v1.0.6`, build-specific ingress hosts, callback routing URLs, Vault mappings, and no memory over `256Mi`.

## Changes

- `microservice` chart: `services[].image` full image override; `docs/service-dev-yml-contract.md`.
- `/home/slnnk/git/youdo-business-mobile-id/devops/dev.yml` (created).

## Open items

- Before Jenkins deploy, confirm Vault path `dev/projects/youdo-business-mobile-id` has keys `SentryDsn`, `MtsYouDoPrivateSigKeyBase64`, and `MtsYouDoPrivateEncKeyBase64`.
- Deploy through Jenkins and verify `web` health `/_/healthcheck` and `mobileid` health `/health`.

## Portable lesson

none
