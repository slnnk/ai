---
system: k8s
status: verified
checked: 2026-06-11
tags: [kubernetes, pvc, storageclass, pending, managed-kubernetes, rollout-timeout]
---
# PVC stays Pending: "no persistent volumes available for this claim and no storage class is set"

## Symptom

A deployment never becomes ready; the pod is `Pending` and the CI job fails at
`kubectl rollout status --timeout=180s`. `kubectl describe pvc <name>` shows:

```text
Warning  ProvisioningFailed / FailedBinding  no persistent volumes available for this claim and no storage class is set
```

## Cause

The PVC manifest omits `storageClassName`. Kubernetes then uses the cluster's **default**
StorageClass, and this cluster has none (`kubectl get storageclass` shows classes but no
`(default)` marker). Without a class the claim waits for a manually created PV that matches
it, which never appears. Managed clusters frequently ship several classes and no default so
that users choose disk tiers deliberately.

## Fix

```bash
kubectl get storageclass                      # pick the right tier/zone
kubectl patch pvc <name> -n <ns> -p '{"spec":{"storageClassName":"<class>"}}'   # unblock the live claim
```

Patching works only while the PVC is unbound and the field is unset. Then fix the manifest so
the next deploy is correct:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-data
spec:
  storageClassName: <class>
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 2Gi
```

Alternatively mark one class as default cluster-wide:
`kubectl annotate storageclass <class> storageclass.kubernetes.io/is-default-class=true`.

Also raise the CI rollout timeout for first deploys: a cold image pull plus volume
provisioning easily exceeds 180 s; 600 s is a safer ceiling for a `Recreate` single-replica app.

## Limits

- Zone-scoped classes (e.g. `fast.<zone>`) bind only for pods schedulable in that zone
  (`volumeBindingMode: WaitForFirstConsumer` helps).
- Changing `storageClassName` on a bound PVC is not possible; recreate the claim (data loss
  unless migrated).
