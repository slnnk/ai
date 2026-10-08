---
system: kubernetes
status: verified
checked: 2026-10-07
tags: [k8s, ttl, rbac]
---
# k8s-ttl-controller with least-privilege RBAC

## Summary

TwiN `k8s-ttl-controller` (chart 0.4.0, app v1.4.0) ships a ClusterRole with get/list/delete on every
resource. Narrow it by setting `API_RESOURCES_TO_WATCH` and a matching custom ClusterRole; never narrow
RBAC alone.

## Symptom

Risk rather than failure: the default install can delete any annotated object cluster-wide. Narrowing only
the ClusterRole makes the controller hot-loop (100% CPU, log spam) on resources it cannot list.

## Cause

The controller lists every discovered resource (or only those in `API_RESOURCES_TO_WATCH`). In v1.4.0 a
list error inside the pagination loop does `continue` while `list == nil`, so the loop retries immediately
with no sleep.

## Fix

- Chart values: `clusterRole.create: false`, `clusterRoleBinding.create: false`,
  `env: [{name: API_RESOURCES_TO_WATCH, value: namespaces}]` (comma-separated plural resource names).
- Own ClusterRole: `""/namespaces` get, list, delete; `""` and `events.k8s.io` `events` create. Bind it to the
  chart's ServiceAccount (`serviceAccount.name`).
- Annotations: `k8s-ttl-controller.twin.sh/ttl: 7d` (units incl. `d`), optional
  `k8s-ttl-controller.twin.sh/refreshed-at: <RFC3339 UTC>` restarts the countdown.
- Reconcile interval is fixed at 5 minutes.

## Limits

- Deleting a namespace does not remove the Helm release record of a chart that created the namespace if
  that record is stored in another namespace (e.g. `default`); clean it up separately.
- When used as a backstop for another cleanup path (CI environment stop), set the TTL longer than that
  path so both do not race.
