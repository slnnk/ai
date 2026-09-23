---
system: k8s
status: verified
checked: 2026-08-25
tags: [kubernetes, namespace, terminating, kubectl-wait, helm, ci, ephemeral-environments]
---
# Recreating a namespace right after deleting it fails: namespace is still `Terminating`

## Symptom

A cleanup job runs `helm uninstall` + `kubectl delete namespace <ns>` and exits successfully.
A deploy job started seconds later fails during `helm upgrade --install --create-namespace`
or `kubectl create namespace` with a message that the namespace exists and is
`Terminating` (`object is being deleted: namespaces "<ns>" already exists`). A minute later
the namespace is gone and a retry works.

## Cause

`kubectl delete namespace` returns as soon as the API server **accepts** the deletion. The
namespace controller then deletes every object inside and waits for finalizers; during that
time the namespace object still exists with `status.phase: Terminating` and cannot be
recreated. Ephemeral-environment pipelines that delete and redeploy the same stable
namespace name (task-based naming) hit this race routinely; it is not a stuck finalizer.

## Fix

Make deletion synchronous in the cleanup job and treat "already gone" as success:

```bash
kubectl delete namespace "$NS" --ignore-not-found
kubectl wait --for=delete "namespace/$NS" --timeout=5m
echo "Namespace $NS is fully deleted"
```

Optionally make the deploy side defensive as well: before creating the namespace, if it
exists in `Terminating`, wait for it to disappear instead of failing:

```bash
if [ "$(kubectl get ns "$NS" -o jsonpath='{.status.phase}' 2>/dev/null)" = "Terminating" ]; then
  kubectl wait --for=delete "namespace/$NS" --timeout=5m
fi
```

If the namespace was created by a Helm release living in another namespace (a "namespace
chart"), uninstall that release **before** deleting the namespace, otherwise the release
secret leaks and the next install may conflict on ownership.

## Limits

- `kubectl wait --for=delete` needs kubectl >= 1.15; it exits immediately if the object is
  already absent.
- A namespace that stays `Terminating` beyond the timeout is a different problem (orphaned
  finalizers, an unavailable aggregated API service); inspect
  `kubectl get ns <ns> -o json | jq .status.conditions` instead of force-removing finalizers.
- Verified on Kubernetes 1.34 with a delete-to-redeploy gap of ~19 seconds.
