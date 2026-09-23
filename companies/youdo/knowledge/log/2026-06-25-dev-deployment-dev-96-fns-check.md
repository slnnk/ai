---
system: dev-deployment
status: verified
checked: 2026-06-25
tags: [helm-charts, fns, docvalidation, rabbitmq, env-expansion, probes, dev-96]
---
# Dev deployment: dev-96 Fns deploy check

Date: 2026-06-25

## Context

- Repository: `/home/slnnk/git/helm-charts`
- Service repository: `/home/slnnk/git/Fns`
- Cluster kubeconfig: `/home/slnnk/.kube/config-yandex-dev`
- Namespace: `dev-96`
- Services in test run: `docvalidation`, `fns`

## Actions

Checks:
- `kubectl -n dev-96 get pods -o wide`
- `kubectl -n dev-96 get deploy,svc,ingress`
- `helm -n dev-96 list --all`
- `kubectl -n dev-96 logs deploy/fns-96-service`
- `kubectl -n dev-96 logs deploy/rabbitmq`
- `helm template` for `/home/slnnk/git/Fns/devops/dev.yml`

## Findings

- Namespace infra is healthy: `rabbitmq` and `redis` are running.
- `docvalidation-96` is healthy and Helm status is `deployed`.
- `fns-96` is stuck in Helm status `pending-install`; only pre-migration completed, post-migration has not run.
- `fns-96-api` is `0/1 Running` with restarts because the deployed liveness/readiness probes target port `80` while the application listens on `8080`.
- `fns-96-service` and `fns-96-scheduler` are running, but RabbitMQ connections fail with `ACCESS_REFUSED`.
- RabbitMQ logs show literal username `$(RabbitMq__Username)`, meaning `RabbitMq__Url` was rendered from global ConfigMap/env before Kubernetes could expand the secret-backed username/password variables.

## Changes

Source fixes applied:
- `/home/slnnk/git/Fns/devops/dev.yml`
  - Added `api.port: 8080`.
  - Added `database.memoryLimit: 256Mi`.
  - Moved `RabbitMq__Url` from top-level `env` into each service's local `env` block after `envValueFrom`.
  - Secret mappings were left as edited by the user: `dev/logreader` / `LogreaderConnectionString` and `dev/projects/fns` / `OpenApiMasterToken`.

Validation:
- `helm template` renders `fns-123-api` service targetPort/probes on `8080`.
- `RabbitMq__Password` and `RabbitMq__Username` render before service-local `RabbitMq__Url`.
- All Fns workloads render with `256Mi` memory request/limit.

## Open items

- User confirmed the `fns` redeploy completed successfully after the source fixes.
- Audit other prepared `dev.yml` files that keep `RabbitMq__Url` in global `env`; move URL to service-local `env` or add a chart-level safer RabbitMQ helper.

## Portable lesson

`~/ai/general/knowledge/k8s/dependent-env-var-expansion-order.md`
