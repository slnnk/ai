---
system: helm
status: verified
checked: 2026-08-25
tags: [helm, atomic, hooks, pre-install, statefulset, pvc, cleanup, migrations]
---
# `helm upgrade --install --atomic` fails, the release is gone, but hook resources remain

## Symptom

An install fails (for example the application Deployment never becomes ready within
`--timeout`). `--atomic` uninstalls the release and `helm list` no longer shows it, yet the
namespace still contains a database StatefulSet, its pod and Service, a completed migration
Job, and a Bound PVC created by that release. The next install of the same release name may
then conflict with, or silently reuse, those leftovers.

## Cause

Resources annotated with `helm.sh/hook` (`pre-install`, `pre-upgrade`, ...) are **not part of
the release manifest**. Helm creates them, optionally deletes them according to
`helm.sh/hook-delete-policy`, and otherwise forgets about them. The atomic rollback removes
only tracked resources; hook resources without a matching delete policy survive. A
StatefulSet's `volumeClaimTemplates` PVCs additionally outlive the StatefulSet itself by
design.

## Fix

Decide per hook what must happen on failure and encode it:

```yaml
metadata:
  annotations:
    helm.sh/hook: pre-install,pre-upgrade
    helm.sh/hook-weight: "-5"
    # remove the previous run's object before creating a new one, and remove it on hook failure
    helm.sh/hook-delete-policy: before-hook-creation,hook-failed
```

For a database that must persist across upgrades, do **not** make it a hook; render it as a
normal chart resource (ordering handled by init containers or a wait Job), so `--atomic`
tracks it and `helm uninstall` removes it. Keep the data PVC's lifecycle explicit
(`persistentVolumeClaimRetentionPolicy` on the StatefulSet, or documented manual cleanup).

When cleaning up after a failed atomic install, check before reinstalling:

```bash
kubectl -n "$NS" get sts,job,pvc,svc -l app.kubernetes.io/instance="$RELEASE"
kubectl -n "$NS" delete sts,job,svc -l app.kubernetes.io/instance="$RELEASE"
kubectl -n "$NS" delete pvc -l app.kubernetes.io/instance="$RELEASE"   # only if data is disposable
```

## Limits

- `hook-failed` only fires when the **hook itself** fails; a hook that succeeded while the
  main rollout failed is kept unless you use `hook-succeeded` (which also deletes it after
  successful installs and defeats "persist across upgrades").
- Deleting the namespace removes everything, so throwaway environments can rely on that;
  shared namespaces cannot.
- Behaviour checked with Helm 3.20; hook semantics are unchanged across Helm 3.x.
