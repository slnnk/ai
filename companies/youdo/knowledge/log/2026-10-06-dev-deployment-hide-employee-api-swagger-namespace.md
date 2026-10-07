---
system: dev-deployment
status: verified
checked: 2026-10-06
tags: [kubernetes, postgres, naming]
---
# Stale namespace dev-hide-employee-api-swagger: 63-char names and full PG volume

## Task

The user asked what namespace `dev-hide-employee-api-swagger` is (read-only check, 2026-10-06).

## Context

Created 2026-09-15 by Jenkins build `test/163` from `youdo.business` pipeline `138657`, job `3145570` (triggered by a developer, not DevOps). Branch had no task ID, so the namespace uses the branch slug `hide-employee-api-swagger`. Was already the only leftover `dev-*` namespace on 2026-08-31/09-30 checks (see `2026-09-30-knowledge-base-stale-map-live-checks.md`).

## Actions

`kubectl -n dev-hide-employee-api-swagger get ns/pods/pvc/sts/events`, `helm list -a`, postgres pod logs. Then, with the user's approval (2026-10-06): `helm uninstall --wait` of the 7 service releases in the namespace, `helm -n default uninstall dev-hide-employee-api-swagger` (the `ephemeral-namespace` release, which removed the namespace); orphaned hook StatefulSets/PVCs went with the namespace. PV `pvc-731fa64b-...` (youdo-business postgres, reclaim `Delete`) briefly stayed `Released` with `VolumeFailedDelete ... still attached to node` until the CSI detached it.

## Findings

- Age 21 days despite `ttl: 7d`: TTL labels are metadata only; GitLab never tracked it (see below).
- Helm: 7 releases deployed (`youdo-business` rev 4); no releases for auth-service, tkb-proxy, tochka-proxy, notifications, but their postgres StatefulSets and Pending PVCs exist.
- 63-char limit: StatefulSets `youdo-business-auth-service-`, `-tkb-proxy-`, `-tochka-proxy-`, `youdo-notifications-hide-employee-api-swagger-postgres` cannot create pods (`metadata.labels`/`spec.hostname` must be no more than 63 characters). Long branch slug + long service name overflows; same class as the migration Job name item in TODO.
- `youdo-business-...-postgres-0` CrashLoopBackOff, 260 restarts over 26h: WAL recovery fails with `No space left on device` on the 5Gi `yc-network-hdd` PVC. All youdo-business app pods wait in `Init:0/1` on it.
- Healthy: docvalidation, fns, kitcut, landings, mobile-id, sms-service, rabbitmq, redis.

### GitLab and Jenkins (checked 2026-10-06, GET only)

- MR `youdo.business!3770` "Hide employee API methods from Swagger", branch `hide-employee-api-swagger`, merged 2026-09-15 21:37:57 MSK.
- Pipeline `138657` has two `1 deploy dev` runs, both failed: `3145476` (20:48-20:59, Jenkins `test/162`) and `3145570` (21:21-21:38, Jenkins `test/163`). Helm releases dated 20:15 come from an earlier deploy not identified here.
- Jenkins `162`/`163` failures: Helm release names over 53 chars rejected (`youdo-business-billing-service-...`, `youdo-business-doc-generator-...`: `invalid release name ... must not be longer than 53`); `youdo-notifications`, `auth-service`, `tkb-proxy`, `tochka-proxy` failed pre-install hook (`timed out waiting for the condition`, the 63-char postgres pod name) and were uninstalled by `--atomic`, leaving hook StatefulSets/PVCs orphaned; in `163` the `youdo-business` upgrade hit `context deadline exceeded` and was rolled back.
- GitLab job uploaded no `deploy-dev.env` (failure path), so no deployment was recorded: environment `502` `dev/hide-employee-api-swagger` has `last_deployment: null`, `auto_stop_at: null`, and became `stopped` at the MR merge without any `3 delete dev` run.
- Cause of the leak: Jenkins creates the namespace before success, but cleanup exists only via a successful GitLab deployment (`on_stop`/`auto_stop_in`). A failed first deploy leaves an unmanaged namespace.

## Changes

Dev cluster: namespace `dev-hide-employee-api-swagger` and all its Helm releases deleted (2026-10-06). GitLab environment `502` left as is (already stopped).

## Open items

In `~/ai/TODO.md` (dev-deployment).

## Portable lesson

none
