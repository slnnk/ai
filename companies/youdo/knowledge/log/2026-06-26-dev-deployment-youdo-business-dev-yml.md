---
system: dev-deployment
status: verified
checked: 2026-06-26
tags: [helm-charts, dev-yml, onboarding, youdo-business, nomad-template, aspnetcore-urls, staging, domain-audit]
---
# Dev deployment: youdo.business dev.yml for ephemeral dev deploy

Date: 2026-06-26

## Context

helm-charts ephemeral Jenkins deploy flow, service repo `/home/slnnk/git/youdo.business`, reference test-stand template `/home/slnnk/git/automation-test-yandex/playbooks/deploy/docker/files/nomad_youdo-business/youdo-business.j2`.

## Task

Prepared `devops/dev.yml` for the main `youdo.business` service. This service is more complex than previous B2B services and uses a special Nomad template on test stands, so that template was treated as the source of truth instead of only service-local config files.

## Decisions

- Runtime components from the template: `worker`, `automation-web`, `bot-web`, `business-api`, `employee-web`, `business-web`, `mock-api`, `business-internal-api`.
- Migration images: default `migrations` plus `mock-migrations` via `mock_migrations` pre/post hooks.
- Database: ephemeral PostgreSQL with `mockDB: true` for main and mock DB contracts.
- Port adaptation: Nomad maps app ports to 80, but Kubernetes dev chart uses container/service port `8080` with `YouDo__Core__Port=8080`.
- Health checks: all runtime components use HTTP `/health` probes.
- Memory: all app components and PostgreSQL capped at `256Mi` for dev.
- RabbitMQ: namespace-local host `rabbitmq`; credentials come from Vault path `dev/rabbitmq` by key name, not plaintext.
- Secrets from the Nomad template were not copied as values. They are mapped by env key to Vault paths only:
  - `dev/logreader`
  - `dev/s3`
  - `dev/rabbitmq`
  - `dev/projects/youdo-business`
- Service URLs that belong to this deploy were moved into `routing.env` as `self`; dependency URLs use `dependency` rules where appropriate.
- Avoided placing routable URL variables in component-level `services[].env`, because service-level env overrides ConfigMap/routing output.

## Actions

Validation commands run from `/home/slnnk/git/helm-charts`:

```bash
helm lint ./microservice
helm template test ./microservice \
  --namespace dev-123 \
  --set global.projectName=youdo-business-123 \
  --set global.namespace=dev-123 \
  --set global.buildNumber=123 \
  --set image.registry=registry.example.com/youdo-business \
  --set image.tag=v1 \
  -f /home/slnnk/git/youdo.business/devops/dev.yml \
  >/tmp/youdo-business-render.yaml
```

Both commands succeeded.

Rendered checks confirmed:

- Images render as `registry.example.com/youdo-business/<component>:v1` for all runtime services.
- Migration images render as `migrations:v1` and `mock-migrations:v1`.
- Ingress hosts receive the build suffix, e.g. `business-123.dev.youdo.sg`, `business-api-123.dev.youdo.sg`, `youdo-business-mock-api-123.dev.youdo.corp`.
- Self-routed URLs receive the build suffix in the rendered ConfigMap.
- Dependency-routed URLs stay at defaults during a standalone Helm render unless the matching dependency is part of the selected environment.

## Follow-ups / risks

- Before deployment, ensure Vault path `dev/projects/youdo-business` contains all mapped keys required by the service. Do not store values in repo or notes.
- If runtime fails after a successful Helm render, the most likely causes are missing Vault keys, endpoint/domain mismatch, or a behavior difference between Nomad test stand and Kubernetes dev namespace.

## 2026-06-26 update

Removed the temporary YAML anchor/helper key `x-common-env` from `/home/slnnk/git/youdo.business/devops/dev.yml`. The common environment now lives directly under top-level `env`, matching the service dev.yml contract more closely and avoiding future schema issues. Revalidated with `helm lint ./microservice` and the same `helm template` command.

## 2026-06-26 domain audit

Audited all `/home/slnnk/git/*/devops/dev.yml` files for `youdo.local`. Found occurrences only in onboarded service configs and replaced them with `youdo.corp` in env, routing defaults/templates, and ingress hosts for:

- `youdo-business-billing-service`
- `youdo-business-tochka-proxy`
- `youdo-business-tkb-proxy`
- `youdo-business-mobile-id`
- `youdo.business.landings`
- `youdo.business`

Validation:

- `rg 'youdo\.local' /home/slnnk/git/*/devops/dev.yml` returned no matches.
- `helm lint ./microservice` succeeded.
- `helm template` succeeded for all six affected service dev.yml files with `global.buildNumber=123`.
- Rendered manifests also had no `youdo.local`; ingress and URL templates render under `dev.youdo.corp` where changed.

## 2026-06-26 dev-106 deployment failure investigation

Checked namespace `dev-106` with kubeconfig `/home/slnnk/.kube/config-yandex-dev`.

Findings:

- Namespace annotations point to Jenkins build `http://jenkins-test.ru-central1.internal/job/test/106/`.
- Jenkins consoleText request returned `403`, so console logs were not available from this session.
- `helm list -a -n dev-106` did not show `youdo-business-106`; the release had already rolled back/cleaned up.
- Only `youdo-business-106-postgres`, service, and `youdo-business-106-env` ConfigMap remained for the service.
- Events showed main and mock migrations completed, secrets were synced during the failed rollout, all runtime components were created and started, then readiness probes to `:8080/health` failed with connection refused and containers entered BackOff.
- App pods were already deleted, so `kubectl logs` could not be collected.
- Live ConfigMap showed `Environment`, `ASPNETCORE_ENVIRONMENT`, and `REACT_APP_ENVIRONMENT` were `Development`.
- The reference Nomad test-stand template for this service uses `Staging` for `Environment` and `ASPNETCORE_ENVIRONMENT`. Source code has `env.IsDevelopment()` branches that enable local SPA dev-server behavior in several web components, which is not appropriate for test container deploys.

Fix applied locally:

- Changed `/home/slnnk/git/youdo.business/devops/dev.yml` common env from `Development` to `Staging` for `Environment`, `ASPNETCORE_ENVIRONMENT`, and `REACT_APP_ENVIRONMENT`.
- Added missing non-secret `IntellectDialog__ProviderId` from the Nomad template.
- Revalidated with `helm lint ./microservice` and `helm template` for `youdo-business-106` using image tag `devops-689-k8s-134273`.

Residual risk:

- Because rollback removed pods, the exact application exception was not recoverable. If the next deployment still fails, collect logs before rollback cleanup or expose Jenkins console output.

## 2026-06-26 dev-107 deployment monitoring

Observed namespace `dev-107` after user started a new deploy.

Findings:

- `youdo-business-107` release stayed `pending-install`.
- Main and mock migrations completed.
- All runtime components entered CrashLoop/BackOff.
- Captured logs before cleanup. Multiple components (`business-api`, `business-web`, `mock-api`, `automation-web`, `worker`) failed with the same root cause: Kestrel tried to bind `http://*:80` and crashed as non-root with `System.Net.Sockets.SocketException (13): Permission denied`.
- Live ConfigMap showed `ASPNETCORE_ENVIRONMENT=Development`, no `ASPNETCORE_URLS`, no `HTTP_PORTS`, `YouDo__Core__Port=8080`, and `Sentry__Environment=Development_dev-107`.
- The app images use `ASPNETCORE_URLS`/default URL binding, so `YouDo__Core__Port=8080` alone does not change the actual listen port.

Fix applied locally in `/home/slnnk/git/youdo.business/devops/dev.yml`:

- `Environment=Staging`
- `ASPNETCORE_ENVIRONMENT=Staging`
- `REACT_APP_ENVIRONMENT=Staging`
- `ASPNETCORE_URLS=http://*:8080`
- `HTTP_PORTS=8080`
- `Sentry__Environment=Staging_{{ .Values.global.namespace }}`
- `IntellectDialog__ProviderId` added from the Nomad template

Validation:

- `helm lint ./microservice` succeeded.
- `helm template` for `youdo-business-107` renders `ASPNETCORE_URLS=http://*:8080`, `HTTP_PORTS=8080`, and `Sentry__Environment=Staging_dev-107`.

Current state:

- Existing `dev-107` deployment uses the old ConfigMap and remains failing; it needs a new deploy with the updated config.

## Changes

- `/home/slnnk/git/youdo.business/devops/dev.yml` (created; anchor removed; `Staging`, `ASPNETCORE_URLS`, `HTTP_PORTS`, `IntellectDialog__ProviderId`).
- `devops/dev.yml` of the six services listed in the domain audit (`youdo.local` -> `youdo.corp`).

## Open items

- New deploy with the updated `dev-107` config.
- Confirm Vault keys under `dev/projects/youdo-business` before deploy.

## Portable lesson

`~/ai/general/knowledge/dotnet/aspnet-container-default-port-8080-healthcheck.md`
