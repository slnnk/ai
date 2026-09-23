---
system: dev-deployment
status: verified
checked: 2026-09-01
tags: [youdo-business, employee-web, aspnetcore-environment, vite, spa, http-500, dev-yml, staging]
---
# Employee dev ingress root returns HTTP 500

Date: 2026-09-01 (Europe/Moscow)

## Context

- URL: `https://employee-devops-689.dev.youdo.sg/`.
- Namespace: `dev-devops-689`.
- Deployment: `youdo-business-devops-689-employee-web`.
- Image: `nexus.youdo.com/youdo/microservices/youdo.business/employee-web:devops-689-k8s-137718`.
- Repository: `/home/slnnk/git/youdo.business`, branch `DevOps-689-k8s`.

## Findings

Evidence and root cause: a correlated root request returned HTTP 500 with an application JSON exception. Pod logs reported:

```text
An error occurred trying to start process 'npm' with working directory 'spa'. No such file or directory
```

The stack enters `YouDo.Business.Infrastructure.ViteDevServerLauncher` from `EmployeeSpace` `UseProxyToSpaDevelopmentServer`. The conditions are:

- shared `devops/dev.yml` sets `ASPNETCORE_ENVIRONMENT=Development`;
- `YouDo.Business.EmployeeSpace.Infrastructure.Web/Startup.cs` enables the Vite proxy under `env.IsDevelopment()`;
- the final Docker image correctly contains the compiled SPA at `/app/spa/build/index.html`;
- the final ASP.NET runtime image intentionally has neither `npm` nor the SPA source directory, because npm runs only in the Docker `spa-build` stage.

The readiness check remains green because `/health` is mapped before SPA fallback and does not exercise the root route. Nginx and Traefik are not the cause; direct Traefik returns the same 500.

## Changes

Correction prepared:

The active Nomad test template at `/home/slnnk/git/automation-test-yandex/playbooks/deploy/docker/files/nomad_youdo-business/youdo-business.j2` was checked and uses `Staging` consistently for `Environment`, `ASPNETCORE_ENVIRONMENT`, `REACT_APP_ENVIRONMENT`, and Sentry environment naming across the components.

The same contract was applied locally to `/home/slnnk/git/youdo.business/devops/dev.yml` on branch `DevOps-689-k8s`: all four remaining `Development` values were changed to `Staging`. This global values change covers employee-web as well as automation-web and mock-api, avoiding their equivalent Development-only Vite branches.

Why `Staging` is appropriate:

- it disables the exact `env.IsDevelopment()` Vite branch;
- it retains `!env.IsProduction()` behavior such as Swagger in the dev environment;
- there is no `appsettings.Staging.json`, so normal `appsettings.json` plus Kubernetes env/secrets remain the configuration sources;
- the separate application variable `Environment=Development` and Sentry dev naming can remain unchanged.

Local validation passed:

- `helm lint` of the current `microservice` chart with `devops/dev.yml`;
- `helm template` rendered `Environment=Staging`, `ASPNETCORE_ENVIRONMENT=Staging`, `REACT_APP_ENVIRONMENT=Staging`, and `Sentry__Environment=Staging_dev-devops-689`;
- no `Development` value remains in `devops/dev.yml`;
- `git diff --check` passed.

## Open items

After publishing the branch and repeating the primary deployment, verify employee root static index delivery, `/health` HTTP 200, pod logs, and no restarts. Also test the authenticated/fallback paths of automation-web and mock-api.

No live-cluster change was made; publication and runtime verification remain pending. (Runtime-proven on 2026-09-03: `2026-09-03-dev-deployment-youdo-business-dev-deploy-pipeline-137949.md`.)

## Portable lesson

`~/ai/general/knowledge/dotnet/spa-dev-server-proxy-500-in-runtime-image.md`
