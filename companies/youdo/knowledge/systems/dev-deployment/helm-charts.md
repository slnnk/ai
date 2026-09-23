---
system: dev-deployment
status: outdated
checked: 2026-08-18
tags: [helm, helm-charts, microservice, ephemeral-namespace, postgresql, pvc]
---
# Helm charts: B2B dev deployments

> Historical/component note. The authoritative cross-system status and rollout plan is `~/ai/current/knowledge/systems/dev-deployment/overview.md`. This file contains older chart-specific observations and includes obsolete namespace naming (`dev-{BUILD_NUMBER}`; namespaces are now task-based, e.g. `dev-devops-689`).

Last verified: 2026-08-18.

- Repository: `/home/slnnk/git/helm-charts` (`git@gitlab.youdo.sg:sysadmins/helm-charts.git`), branch snapshot: `master`.
- `ephemeral-namespace` prepares `dev-{BUILD_NUMBER}` namespaces with registry/Vault integration and namespace-local RabbitMQ/Redis.
- `microservice` deploys service workloads, migrations, ingress, Vault secrets, and optional PostgreSQL.
- Jenkins entry point is maintained in `/home/slnnk/git/jenkins-pipelines/pipelines/deploy-dev-b2b.Jenkinsfile`.

## PostgreSQL persistence

On 2026-08-18 the `microservice` PostgreSQL workload was changed from a hook-managed Deployment without a data volume to a hook-managed StatefulSet with a per-service PVC. The claim is mounted at `/var/lib/postgresql/data`, requests `5Gi` by default, and can be configured in a service `devops/dev.yml` through `database.size` (for example, `10Gi`). The generated claim name is `postgres-data-{projectName}-postgres-0`.

This addresses the data loss observed after the single Kubernetes node backing `dev-master` was replaced: PostgreSQL pods can now be recreated or rescheduled while retaining data on the PVC. Deleting the ephemeral namespace still deletes its PVCs and data. Because StatefulSet claims can outlive Helm-managed workload deletion, check/remove the PVC explicitly when uninstalling a release without deleting its namespace.

Validation performed in `/home/slnnk/git/helm-charts`:

- `helm lint ./microservice`
- `helm template` with no `database.size` rendered `storage: 5Gi`.
- `helm template` with `database.size=10Gi` rendered `storage: 10Gi`.

Primary contract and task history:

- `docs/service-dev-yml-contract.md`
- `docs/agents-ephemeral-deploy-plan.md`, item 66

## Related log entries

- `~/ai/current/knowledge/log/2026-07-30-dev-deployment-dev-master-node-replacement-db-recovery.md` (the data-loss incident that motivated the PVC change)
- `~/ai/current/knowledge/log/2026-06-25-dev-deployment-ephemeral-dev-memory-cap.md`
- `~/ai/current/knowledge/log/2026-06-18-dev-deployment-ephemeral-dev-dependencies.md`
