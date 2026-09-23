---
system: dev-deployment
status: verified
checked: 2026-06-17
tags: [helm-charts, jenkins, youdo-business-auth-service, youdo-kitcut, redis, dev-yml, aspnetcore-urls, vault]
---
# Dev deployment: youdo-business-auth-service Jenkins ephemeral dev deploy (and 2026-06-24 follow-ups)

Date: 2026-06-17 (with dated follow-up sections through 2026-06-24)

## Context

- Helm charts repo: `/home/slnnk/git/helm-charts`
- Service repo: `/home/slnnk/git/youdo-business-auth-service`
- Jenkins pipeline repo: `/home/slnnk/git/jenkins-pipelines`
- Target namespace pattern: `dev-{BUILD_NUMBER}`
- Target service release/resource pattern: `youdo-business-auth-service-{BUILD_NUMBER}`

## Actions

- Checked `youdo-business-auth-service/devops/dev.yml` against shared `microservice` chart.
- Compared with old `devops/config.yml` used by Nomad/Ansible.
- Found old inline `secrets` map, static RabbitMQ host, singular Ingress `host`, and static Postgres service name.
- Updated `microservice` chart to support `global.buildNumber`, `tpl` in env/Ingress values, `services[].envValueFrom`, per-secret VaultStaticSecret type, and Service creation independent of Ingress.
- Updated `/home/slnnk/git/youdo-business-auth-service/devops/dev.yml` for namespace-local RabbitMQ and build-numbered hosts/resources.
- Updated `/home/slnnk/git/jenkins-pipelines/pipelines/deploy-dev-b2b.Jenkinsfile` to deploy selected services after `ephemeral-namespace`.
- Recorded detailed notes in `/home/slnnk/git/helm-charts/docs/service-deploy-notes/youdo-business-auth-service.md`.

Validation:

- `helm lint ./ephemeral-namespace`: passed.
- `helm lint ./microservice`: passed.
- `helm template ns ./ephemeral-namespace ...`: passed.
- `helm template youdo-business-auth-service ./microservice ... -f /home/slnnk/git/youdo-business-auth-service/devops/dev.yml`: passed.

Pending (at the time):

- Run actual Jenkins trial deploy.
- Confirm Jenkins GitLab API-derived image tags match pushed images.
- Check rollout, Ingress, RabbitMQ connection, and migrations in `dev-{BUILD_NUMBER}`.
- If Jenkins script-security rejects new Groovy methods/calls, approve or refactor.

## dev.yml source rule update - 2026-06-24

Context: `/home/slnnk/git/helm-charts`, Jenkins ephemeral B2B dev deploy flow.

Decision: when authoring or auditing service `devops/dev.yml`, compare environment variables only against `config.yml`; if `config.yml` is absent, use `test.hcl`. Do not use `production.hcl` as the source for dev variables.

Updated file: `/home/slnnk/git/helm-charts/docs/agents-ephemeral-deploy-plan.md`.

Next impact: `youdo-business-doc-generator` was previously marked as based on `production.hcl`; recheck it against `test.hcl` under the current rule before treating it as fully validated.

## youdo.kitcut Redis check - 2026-06-24

Context: `/home/slnnk/git/youdo.kitcut`, `/home/slnnk/git/helm-charts` ephemeral B2B dev deploy.

Finding: `youdo.kitcut` uses Redis. `devops/config.yml` defines `Redis__ConnectionString` for both `web_env` and `api_env`; current `devops/dev.yml` sets `Redis__ConnectionString` to `redis:6379,...`.

Current chart gap: `microservice` chart has PostgreSQL support but no Redis Deployment/Service template, so `redis:6379` will not resolve unless Redis is provided separately in the namespace or by another chart.

Next step: before validating/deploying `youdo.kitcut`, decide whether ephemeral dev should add namespace-local Redis support or point kitcut to an existing shared dev Redis.

## ephemeral-namespace Redis - 2026-06-24

Context: `/home/slnnk/git/helm-charts`, Jenkins ephemeral B2B dev deploy flow.

Task: add Redis where namespace-local RabbitMQ is created, because `youdo.kitcut` requires `Redis__ConnectionString` and current `dev.yml` points to `redis:6379`.

Changes: added `redis.enabled=true` defaults to `ephemeral-namespace/values.yaml`; added `ephemeral-namespace/templates/redis-deployment.yaml` and `ephemeral-namespace/templates/redis-service.yaml`; updated chart metadata and docs. Redis is internal-only ClusterIP service named `redis`, port `6379`, image `redis:7.2-alpine`, no auth, ephemeral `emptyDir` data.

Validation: `helm lint ./ephemeral-namespace` passed; `helm lint ./microservice` passed; `helm template ns ./ephemeral-namespace ... dev-123 ...` renders `Service/redis` and `Deployment/redis` in namespace `dev-123`.

Next: Jenkins deploy should create Redis automatically with namespace setup; verify `youdo.kitcut` pod starts and connects to namespace-local Redis during a real deploy.

## Redis developer access plan - 2026-06-24

Context: `/home/slnnk/git/helm-charts`, ephemeral Redis added to `ephemeral-namespace`.

Decision: do not implement developer external Redis access yet. Current Redis remains internal ClusterIP service `redis:6379` for workloads.

Future plan: developers do not have kubeconfig, so port-forward is not the target UX. Consider dev-only NodePort or equivalent TCP endpoint, with Jenkins printing a ready command like `redis-cli -h redis.dev.youdo.corp -p ${REDIS_NODE_PORT}`. Avoid implementing this until explicitly requested.

Updated plan: `/home/slnnk/git/helm-charts/docs/agents-ephemeral-deploy-plan.md` item 36.

## dev-84 check - 2026-06-24

Context: `/home/slnnk/git/helm-charts`, kubeconfig `/home/slnnk/.kube/config-yandex-dev`, Jenkins ephemeral namespace `dev-84`.

Findings:
- Namespace `dev-84` exists and is Active.
- Running/ready: RabbitMQ, auth-service postgres/web-ext/web-int, doc-generator api, kitcut postgres.
- Completed: auth-service pre-migrations, kitcut pre-migrations.
- Pending due to insufficient memory: `youdo-business-auth-service-84-migration-post-migrations-mgfxd`, `youdo-kitcut-84-api-7dfd9cfb95-spn57`.
- Failing: `youdo-kitcut-84-web-d698b957-wfrg7` in `CreateContainerConfigError` because Kubernetes Secret `youdo-kitcut-84-secrets-0` is not found.
- Root cause for missing secret: VaultStaticSecret `youdo-kitcut-84-secrets-0` is `SYNCED=False HEALTHY=False READY=False`; Vault error `empty response from Vault, path="secret/dev/projects/youdo-kitcut"`.
- Redis service is absent in `dev-84`; this namespace was created before the Redis addition to `ephemeral-namespace` was deployed/applied.

Ingresses present: `rabbitmq-84.dev.youdo.corp`, `business-auth-ext-84.dev.youdo.sg`, `business-auth-int-84.dev.youdo.sg`, `doc-generator-84.dev.youdo.corp`, `youdo-kitcut-api-84.dev.youdo.corp`, `s-84.dev.youdo.sg`.

Next steps:
1. Create/populate Vault secret at `secret/dev/projects/youdo-kitcut` with key `SentryDsn` or adjust kitcut `dev.yml` secret path/keys.
2. Re-run namespace setup with updated `ephemeral-namespace` chart if Redis is needed in `dev-84`.
3. Address memory pressure/capacity before expecting pending auth post-migration and kitcut api pod to schedule.

## dev-85 check - 2026-06-24

Context: `/home/slnnk/git/helm-charts`, kubeconfig `/home/slnnk/.kube/config-yandex-dev`, Jenkins ephemeral namespace `dev-85`.

Findings:
- Namespace `dev-85` exists and is Active.
- RabbitMQ, auth-service postgres/web-ext/web-int, doc-generator api, kitcut postgres are Running.
- Jobs completed: auth-service pre/post migrations, kitcut pre-migrations.
- All VaultStaticSecret resources are synced/healthy/ready, including `youdo-kitcut-85-secrets-0`.
- `youdo-kitcut-85-api` and `youdo-kitcut-85-web` are in CrashLoopBackOff.
- Logs for both kitcut containers show ASP.NET/Kestrel tries to bind `http://*:80` and fails with `System.Net.Sockets.SocketException (13): Permission denied`. The chart exposes/probes port 8080, but `youdo.kitcut/devops/dev.yml` does not set an app listen-port env var, so the image default remains port 80.
- `service/redis` is still absent in `dev-85`; namespace setup did not include the newly added Redis chart changes. `youdo-kitcut-85-env` contains `Redis__ConnectionString=redis:6379,...`, so Redis must be added before kitcut can fully work.

Next steps:
1. Fix `youdo.kitcut/devops/dev.yml` so web/api listen on 8080, likely by adding the same K8s-specific port env used by this service/base image.
2. Re-apply updated `ephemeral-namespace` for build 85 or run a fresh build after Redis support is included, so `Service/redis` and `Deployment/redis` exist.

## Jenkins test/85 log/access check - 2026-06-24

Context: user asked to check `https://build.youdo.sg/view/DevOps/job/test/85` after pushing changes.

Jenkins access: direct `curl https://build.youdo.sg/view/DevOps/job/test/85/consoleText` from sandbox failed DNS; outside sandbox Jenkins responded HTTP 403, so console log was not readable without auth/cookie/token.

Cluster evidence: Helm release `ns-dev-85` is in namespace `default`. `helm get manifest ns-dev-85` contains RabbitMQ resources but no Redis resources. `helm get values ns-dev-85 --all` contains `rabbitmq` but no `redis` block. `kubectl -n dev-85 get svc redis` returns NotFound.

Git evidence: after `git fetch origin master`, local `master` is ahead of `origin/master` by 1 commit. Local HEAD `53cb453 update chart` contains Redis files (`ephemeral-namespace/templates/redis-deployment.yaml`, `redis-service.yaml`, values/docs changes), while `origin/master` remains `5bd8c9f update deploy ms`. Therefore Jenkins build 85 could not have used Redis chart changes from GitLab master.

Conclusion: either commit `53cb453` was not pushed to the remote branch Jenkins checks out, or Jenkins uses a different remote/branch than local `origin/master`. Next step: push local master or verify the Jenkins checkout branch/remote in console log with authorized access.

## youdo.kitcut port env fix - 2026-06-24

Context: `/home/slnnk/git/youdo.kitcut`, failure observed in `dev-85`: web/api CrashLoopBackOff because ASP.NET tried to bind `http://*:80` and non-root container got `Permission denied`.

Change: added `YouDo__Core__Port: "8080"` to `/home/slnnk/git/youdo.kitcut/devops/dev.yml` env, matching other onboarded services.

Validation: `helm template youdo-kitcut-123 ./microservice ... -f /home/slnnk/git/youdo.kitcut/devops/dev.yml` renders `YouDo__Core__Port: "8080"` in ConfigMap and service containers use `containerPort: 8080`.

Remaining: commit/push the service repo change and rerun Jenkins; ensure namespace setup includes Redis support, otherwise kitcut will later fail on `redis:6379`.

## dev-86 check - 2026-06-24

Context: `/home/slnnk/git/helm-charts`, namespace `dev-86`.

Findings: Redis is now present and Running (`service/redis`, `deployment/redis`, image `redis:7.2-alpine`). RabbitMQ, auth-service, doc-generator, postgres pods and migrations are healthy/complete. VaultStaticSecrets are all synced/healthy/ready.

Remaining failure: `youdo-kitcut-86-api` and `youdo-kitcut-86-web` are in CrashLoopBackOff. Logs still show ASP.NET/Kestrel binding to `http://*:80` and failing with `System.Net.Sockets.SocketException (13): Permission denied`.

Important detail: `youdo-kitcut-86-env` ConfigMap contains `YouDo__Core__Port: "8080"`, but kitcut code does not use that setting to configure Kestrel. Base image sets `ASPNETCORE_URLS=http://*:80` and `ASPNETCORE_HTTP_PORTS=80`; logs confirm URLS wins. Likely fix for kitcut: set `ASPNETCORE_URLS: "http://*:8080"` in `devops/dev.yml` (possibly also `ASPNETCORE_HTTP_PORTS: "8080"`, but URLS is the critical override).

## youdo.kitcut ASPNETCORE_URLS fix - 2026-06-24

Context: `/home/slnnk/git/youdo.kitcut`, dev-86 showed kitcut still binding `http://*:80` despite `YouDo__Core__Port=8080`.

Change: replaced `YouDo__Core__Port: "8080"` with `ASPNETCORE_URLS: "http://*:8080"` in `/home/slnnk/git/youdo.kitcut/devops/dev.yml`.

Validation: `helm template youdo-kitcut-123 ./microservice ... -f /home/slnnk/git/youdo.kitcut/devops/dev.yml` renders `ASPNETCORE_URLS: "http://*:8080"`, no `YouDo__Core__Port`, and both service containers/probes stay on 8080.

Next: commit/push `youdo.kitcut` change and rerun Jenkins.

## Jenkins test/87 log check - 2026-06-24

Context: authorized Jenkins read of `https://build.youdo.sg/view/DevOps/job/test/87` using `JENKINS_USER=technical` and token from user-provided credentials saved in `~/ai/current/.env`.

Result: build `#87` failed, but the actual deployment outcome was mixed: `youdo-business-doc-generator-87` deployed and passed the pod-running check; `youdo-kitcut-87` deployed and passed the pod-running check; `youdo-business-auth-service-87` deployed its workloads, but the pipeline failed in the post-rollout pod-status verification.

Important details:
- Jenkins checked out `helm-charts` revision `53cb4538c2b87bec4403b14a823d3c83ab2a7177` (commit message: `update chart`).
- Namespace setup `ns-dev-87` included RabbitMQ and Redis; both were created and RabbitMQ rolled out successfully.
- `dev-87` manifest shows `service/redis` and `deployment/redis` present and healthy.
- `youdo-kitcut-87` completed successfully at the pod level: `api`, `postgres`, and `web` were Running.
- Failure reason in `youdo-business-auth-service` branch: the script printed `ERROR: 2 pod(s) are not in Running state.` immediately after listing `migration-pre` and `migration-post` Jobs as `Completed`. The pipeline is counting completed migration jobs as non-running pods, so the check is too strict for a namespace that intentionally includes Jobs.

Conclusion: build 87 did not fail because of Redis or kitcut runtime. The failure is the pod-state check in the auth-service branch, which should ignore `Completed` migration Jobs or filter them out before asserting all pods are Running.

## Jenkins pod-check fix - 2026-06-24

Context: `/home/slnnk/git/jenkins-pipelines/pipelines/deploy-dev-b2b.Jenkinsfile` build test/87 failed because final pod-state check counted Completed migration Jobs as non-Running pods.

Change: updated the pod selector in the post-rollout verification block to exclude job pods with labels `batch.kubernetes.io/job-name` and `job-name`.

Exact change: `-l "app.kubernetes.io/instance=${SERVICE_RELEASE},!batch.kubernetes.io/job-name,!job-name"`.

Purpose: keep the strict Running-state check for deployment pods, but stop false failures from completed migration Jobs.

## Findings

- ASP.NET Core images in this stack bind to port 80 by default via `ASPNETCORE_URLS`; a non-root container cannot bind it. The application-level `YouDo__Core__Port` setting is not honored by every service (kitcut ignores it); `ASPNETCORE_URLS=http://*:8080` is the reliable override.
- A post-rollout "all pods Running" check must exclude Job pods (completed migrations) or it produces false failures.
- A Jenkins build can only use chart changes that are actually pushed to the branch Jenkins checks out; local-ahead commits explain "missing" resources.

## Changes

- `microservice` chart: `global.buildNumber`, `tpl` support, `services[].envValueFrom`, per-secret VaultStaticSecret type, Service independent of Ingress.
- `ephemeral-namespace` chart: Redis Deployment/Service (`redis:7.2-alpine`, ClusterIP `redis:6379`).
- `/home/slnnk/git/youdo-business-auth-service/devops/dev.yml`, `/home/slnnk/git/youdo.kitcut/devops/dev.yml` (`ASPNETCORE_URLS`).
- `/home/slnnk/git/jenkins-pipelines/pipelines/deploy-dev-b2b.Jenkinsfile`: service deployment after namespace, Job-pod exclusion in the pod check.
- `/home/slnnk/git/helm-charts/docs/agents-ephemeral-deploy-plan.md` items 36 and the dev.yml source rule.

## Open items

- Populate Vault `secret/dev/projects/youdo-kitcut` (`SentryDsn`) or adjust kitcut secret mapping.
- Address cluster memory capacity for pending pods.
- Developer Redis access is deferred until requested.

## Portable lesson

- `~/ai/general/knowledge/dotnet/aspnet-container-default-port-8080-healthcheck.md`
- `~/ai/general/knowledge/k8s/post-rollout-pod-phase-check-false-failures.md`
