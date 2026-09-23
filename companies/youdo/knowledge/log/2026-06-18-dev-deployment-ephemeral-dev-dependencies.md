---
system: dev-deployment
status: outdated
checked: 2026-06-18
tags: [helm-charts, routing, dependencies, decision, jenkins]
---
# Dev deployment: ephemeral dev dependency URL routing (decision note)

> Historical decision note. Current routing, service scope, runtime evidence, and rollout state are maintained in `~/ai/current/knowledge/systems/dev-deployment/overview.md`.

Date: 2026-06-18
Project: helm-charts, Jenkins ephemeral deploy flow
Repository: /home/slnnk/git/helm-charts

## Task

Problem: service env dependencies must point either to an ephemeral service in dev-{BUILD_NUMBER} when that dependency is part of the same Jenkins deploy set, or to the stable master dev endpoint when it is not selected.

## Findings

Recommended direction:
- Keep canonical service names without BUILD_NUMBER in a dependency manifest.
- Jenkins is the source of truth for selected services and passes selectedServices plus env.BUILD_NUMBER to Helm.
- Resolve each dependency by canonical service name: if dependency is in selectedServices, use <service>-<BUILD_NUMBER>.dev.youdo.corp or namespace-local Kubernetes DNS; otherwise use <service>.dev.youdo.corp.
- Prefer chart-level computed dependency env or a generated values overlay, not hand-edited per-build dev.yml files.
- BUILD_NUMBER must come from Jenkins env.BUILD_NUMBER.

## Open items

Risks/TODO:
- Helm list merge behavior makes generated overrides under services[] fragile; prefer a separate dependencyEnv/dependencies values section or generate a fully merged temporary values file.
- If services start with hard dependency availability, Jenkins should deploy/wait in dependency order where possible; cycles require application retries.

## Portable lesson

none
