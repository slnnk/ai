---
system: dev-deployment
status: verified
checked: 2026-07-30
tags: [dev-master, postgresql, data-loss, helm, migrations, node-replacement, incident, oom]
---
# dev-master: database recovery after Kubernetes node replacement

Date: 2026-07-30  
Project: `/home/slnnk/git/helm-charts`  
Environment: Yandex dev Kubernetes, namespace `dev-master`  
Kubeconfig: `/home/slnnk/.kube/config-yandex-dev`

## Context

When the single node was replaced, the `dev-master` pods were recreated on the new node. PostgreSQL in the `microservice` chart is deployed as a `Deployment` without a PVC or a separate data volume, so ten PostgreSQL pods initialised empty databases. A regular Deployment reschedule does not run the Helm migration hooks.

## Actions

- Checked the `initdb` logs, the absence of PVCs/volumes, and the number of user tables.
- Confirmed that before recovery most databases had `0` tables; in a few databases the runtime had created only the 12 tables of the `hangfire` schema.
- Preserved the current Helm values and image tags through the existing release revisions.
- Ran `helm upgrade <release> ./microservice --namespace dev-master --reuse-values --atomic --wait --timeout 10m` sequentially for:
  - `docvalidation`
  - `fns`
  - `youdo-business-auth-service`
  - `youdo-business-billing-service`
  - `youdo-kitcut`
  - `youdo-notifications`
  - `youdo-sms-service`
  - `youdo-business-tkb-proxy`
  - `youdo-business-tochka-proxy`
  - `youdo-business`
- All listed releases moved to revision 2 with status `deployed`.
- Pre/post migration hooks, including the mock migrations, completed successfully.

## Findings

Schema check after recovery:

- `docvalidation`: 12 tables
- `fns`: 8
- `youdo-business-auth-service`: 5
- `youdo-business-billing-service`: 5
- `youdo-business`: 196
- `youdo-business-mock`: 23
- `youdo-business-tkb-proxy`: 15
- `youdo-business-tochka-proxy`: 31
- `youdo-business-tochka-proxy-mock`: 31
- `youdo-kitcut`: 2
- `youdo-notifications`: 5
- `youdo-sms-service`: 5

RabbitMQ and 45 of 46 Deployments were Ready after recovery.

## Open items

Remaining risk:

`youdo-business-worker` remains in `CrashLoopBackOff`: the container exits as `OOMKilled` (exit 137) at request/limit `256Mi`. The other `youdo-business` components are Ready. The memory limit was not changed.

Without a PVC, PostgreSQL data will be lost again on any recreation of a PostgreSQL pod or the next node replacement. For a stable `dev-master`, persistence needs to be designed separately, or migration hooks need to be re-run automatically after a database is lost.

(Follow-up: on 2026-08-18 the chart's PostgreSQL was changed to a StatefulSet with a per-service PVC; see `~/ai/current/knowledge/systems/dev-deployment/helm-charts.md`.)

## Portable lesson

none
