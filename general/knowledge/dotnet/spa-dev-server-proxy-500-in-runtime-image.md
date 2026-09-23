---
system: dotnet
status: verified
checked: 2026-09-03
tags: [aspnet, spa, vite, ASPNETCORE_ENVIRONMENT, IsDevelopment, http-500, docker]
---
# ASP.NET SPA host returns HTTP 500 at `/` in a container while `/health` is 200

## Symptom

A containerised ASP.NET Core app that serves a compiled SPA answers `200` on `/health` and
readiness stays green, but the root URL (and any SPA route) returns `500` with an exception
like:

```text
An error occurred trying to start process 'npm' with working directory 'spa'. No such file or directory
```

The stack trace goes through `UseProxyToSpaDevelopmentServer` (or a custom Vite/webpack
dev-server launcher).

## Cause

The deployment sets `ASPNETCORE_ENVIRONMENT=Development`. `Startup`/`Program` wraps the SPA
dev-server proxy in `if (env.IsDevelopment())`, so the runtime tries to spawn `npm run dev`
inside the container. The final runtime image intentionally contains neither `npm` nor the
SPA sources (they only exist in the multi-stage build's `spa-build` stage); the compiled
bundle *is* present under `/app/spa/build`, but the code path never reaches the static-file
fallback. Health endpoints are mapped before the SPA fallback, so probes do not detect it.

## Fix

Use a non-Development environment name for container deployments, for example:

```yaml
env:
  ASPNETCORE_ENVIRONMENT: "Staging"
  # keep any app-specific "Environment"/"REACT_APP_ENVIRONMENT" variables aligned
```

Why `Staging` rather than `Production`: it disables the exact `IsDevelopment()` branch while
keeping `!IsProduction()` conveniences (Swagger, detailed errors). If no
`appsettings.Staging.json` exists, `appsettings.json` plus environment variables/secrets
remain the configuration source, so nothing else changes.

Verify after redeploy: `GET /` returns the SPA `index.html` (200), `GET /health` still 200,
zero restarts, and no `npm` in the logs. Apply the same value to every web component that
shares the branch (`automation`, `mock`, `employee`-style front ends often share a startup
helper).

## Limits

- If your test stand (Nomad, Compose, etc.) already runs the app with `Staging`, mirror that
  value; diverging environment names between stands cause exactly this class of surprise.
- Do not fix it by adding `npm`/sources to the runtime image; that defeats the multi-stage
  build and still starts a dev server in production-like environments.
- `ASPNETCORE_ENVIRONMENT` also selects `appsettings.{Env}.json`; check nothing important
  lives only in `appsettings.Development.json`.
