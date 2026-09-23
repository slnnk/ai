---
system: dev-deployment
status: outdated
checked: 2026-06-25
tags: [helm-charts, memory, resources, decision, dev-yml]
---
# Dev deployment: ephemeral dev memory cap (decision note)

> Historical decision note. The current operational contract and service rollout state are maintained in `~/ai/current/knowledge/systems/dev-deployment/overview.md`. The 256Mi cap was later relaxed for several workloads (512Mi request / 1Gi limit); see the DevOps-832 log entries.

Date: 2026-06-25
Project: helm-charts / Jenkins ephemeral deploy flow
Repository: /home/slnnk/git/helm-charts

## Findings

Decision: ephemeral dev workloads are capped at 256Mi memory request/limit so the full test service set can fit in the cluster. This rule intentionally overrides higher memory values from service config.yml/test.hcl for devops/dev.yml authoring.

## Changes

Changes made:
- Updated docs/agents-ephemeral-deploy-plan.md item 47 as done.
- Updated docs/service-dev-yml-contract.md and microservice/README.md with the 256Mi rule.
- Updated microservice defaults so migration memoryLimit is 256Mi and PostgreSQL limit defaults to database.memory instead of memory * 2.
- Updated prepared service devops/dev.yml files for youdo-business-auth-service, youdo-business-doc-generator, youdo-business-tickets, youdo.kitcut, youdo.notifications, youdo-sms-service, and docvalidation: service components now use memory/memoryLimit no higher than 256Mi.

## Actions

Validation:
- helm lint ./microservice passed.
- helm template rendered all prepared services with buildNumber=123.
- Rendered manifests were scanned for memory values above 256Mi; none remained.

## Portable lesson

none
