---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [auth, b2b, preflight, gitlab]
---
# DevOps-898 auth service readiness

## Task

Check youdo-business-auth-service readiness as the next B2B service under DevOps-898. User agreed to checking; no pipeline/deployment authorization given in this turn. No superpowers skills used.

## Context

Project544, existing checkout `/home/slnnk/git/youdo-business-auth-service`, clean DevOps-689-k8s preserved. Fetched origin read-only; authoritative masterf0d4a2fb971b4b2a8e4aafe7e2990ef3221f61f3. Latest generated release master-167/pipeline139444, all3web-int/web-ext/migrations builds success, pipeline success.

## Actions

KB search, read-only GitLab/Nomad audit and delegated multi-file config/CI/build review. Evidence `/home/slnnk/ai-data/DevOps-898/auth-service-preflight.json`, checked2026-10-15T19:07:15Z. No Consul/HTTP/business probes, mutations or repo edits.

## Findings

- No mandatory source/config changes found. CI uses v3/.deploy-test.yml, .NET8, per-stand enabled. WITHOUT_DROP_DB=true adds keep-db jobs without disabling ordinary jobs.
- All target B2B Nomad jobs test10–test15 absent. Old pipeline139444 offers ordinary manual jobs3176953–3176958, but compiled configuration predates VK shared-template adaptation. Do not assume these jobs inherit later merged template fixes.
- Recommend a fresh master pipeline to load current merged VK templates and rebuild release images. Existing DEPLOY_PROD_MODE=auto and .deploy-prod-web-migrations-auto.yml enable automatic production child deployment/migrations. New pipeline launch needs explicit authorization covering those effects; none was requested/executed.
- Source CI also defines build-libs: master rule with changes src/libs/version.json, builds/publishes3NuGet libraries if selected. Do not claim this job is excluded without evaluating pipeline rules in the chosen trigger context.
- Runtime uses B2B PostgreSQL/auto per-stand DB/pre-post migrations, dynamic PG port, per-stand RabbitMQ and shared Keycloak auth-tech. SMS client points to business mock API for the same stand, not directly to standalone SMS. Both web-int and web-ext workloads included.

## Changes

Local read-only helper output, refreshed Git refs and KB bookkeeping only. No task branch, repository edits, build, release, deployment or API writes.

## Limits

Prepared configuration is not runtime acceptance. Dependency/runtime behavior not exercised. The current user request was checking only; next proposed action is a separately approved fresh master pipeline with its automatic production effects disclosed.

## User-approved fresh master pipeline

After disclosure of auto production deployment/migrations and possible NuGet publishing, user explicitly requested "Создай новый пайплайн на мастере". Created exactly one pipeline141000/IID168 at2026-10-15 19:09:47UTC, refmaster, SHAverifiedf0d4a2fb971b4b2a8e4aafe7e2990ef3221f61f3. [Pipeline](https://gitlab.youdo.sg/youdo/microservices/youdo-business-auth-service/-/pipelines/141000). Receipt-backed helper `/home/slnnk/ai-data/DevOps-898/auth-service-pipeline.py create|status`; evidence directory `auth-service-build/`.

Initial GET verification pipeline running; set-variables/prepare-nuget/set-variables-nomad success; build-web-int3229554/build-web-ext3229555/build-migrations3229556/build-libs3229557/unit-tests3229558 running. build-libs actually selected by current rules, so library publication is part of the approved pipeline. Production bridge created but no downstream ID yet. No claim builds/tests/release/production completed. Expected generated image tag master-168 after builds. Normal stand jobs3229573–3229578 created for test10–test15, not played. Creating the pipeline does not separately authorize manually deploying stands.

User reported build complete; subsequent GET confirms all3image builds, build-libs and dotnet-unit-tests SUCCESS. Parent pipeline still running; auto-production downstream141002 running, release job still created. Ordinary stand jobs3229573–3229578 now manual/ready. Prepared local helper `/home/slnnk/ai-data/DevOps-898/deploy-auth-service-stands.py launch|status`, pinned pipeline141000/master-168 and source SHA; no job plays executed. Await deployment approval for six ordinary parallel jobs with DB recreation.

Subsequent approved deployment hit B2B PG connection exhaustion. User-authorized limits1000 applied; separately approved six-job retry completed SUCCESS/Nomad healthy/master-168/restarts0 on test10–test15. [Final rollout evidence](2026-10-15-nomad-test-devops-898-auth-service-b2b-rollout.md).

## Portable lesson

none
