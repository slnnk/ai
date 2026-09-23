---
system: k8s
status: verified
checked: 2026-09-04
tags: [kubernetes, cluster-autoscaler, scale-down, coredns, kube-dns-autoscaler, anti-affinity, emptyDir, safe-to-evict]
---
# Autoscaled node group stays at two nodes although one node would fit the load

## Symptom

A managed node group with `min=1` was scaled up to two nodes (event `TriggeredScaleUp 1->2`) and
never goes back to one, even though total requests (and actual usage) fit a single node with
headroom. Neither node has the `cluster-autoscaler.kubernetes.io/scale-down-disabled` annotation.

## Cause

Cluster Autoscaler removes a node only if every non-DaemonSet pod on it can be evicted and
rescheduled elsewhere. Typical blockers found by inspecting the pods on the candidate node:

1. `kube-system/kube-dns-autoscaler` with `preventSinglePointFailure: true` keeps at least two
   CoreDNS replicas while there is more than one node; the CoreDNS pods carry no
   `cluster-autoscaler.kubernetes.io/safe-to-evict: "true"` annotation, so the autoscaler treats
   them as pinning the node.
2. Workloads with required pod anti-affinity on `kubernetes.io/hostname` and two replicas
   (typical for Loki `backend`/`read`/`write`, message brokers, etc.). One replica sits on each
   node; the second node can never be emptied.
3. Pods using local storage (`emptyDir`, `hostPath`) are non-evictable by default unless annotated
   `safe-to-evict: "true"`; caches, Redis, RabbitMQ and monitoring agents often qualify.
4. PodDisruptionBudgets with `maxUnavailable: 0`.

Also note that the original scale-up may have been caused by a transient scheduling conflict (for
example a host-port clash during bootstrap), not by resource pressure: the autoscaler acts on
unschedulable pods, not on utilization thresholds.

## Fix

Diagnose per node:

```bash
kubectl get pods -A --field-selector spec.nodeName=<node> -o json | jq -r '
  .items[] | select(.metadata.ownerReferences[0].kind != "DaemonSet") |
  [.metadata.namespace, .metadata.name,
   (.metadata.annotations["cluster-autoscaler.kubernetes.io/safe-to-evict"] // "-"),
   ([.spec.volumes[]? | select(.emptyDir or .hostPath) | .name] | join(",")),
   (.spec.affinity.podAntiAffinity != null)] | @tsv'
kubectl -n kube-system get cm kube-dns-autoscaler -o jsonpath='{.data.linear}'
kubectl get pdb -A
```

Then decide deliberately:

- accept a single point of failure on the test cluster: set `preventSinglePointFailure: false` in
  the `kube-dns-autoscaler` ConfigMap (or lower `coresPerReplica`/`nodesPerReplica`), reduce
  anti-affinity replicas to one or make the anti-affinity `preferred`, and annotate stateless
  emptyDir pods with `cluster-autoscaler.kubernetes.io/safe-to-evict: "true"`;
- or keep the second node and stop expecting scale-down.

## Limits

- Managed offerings (checked: Yandex Managed Kubernetes, CA defaults) do not let you tune the
  autoscaler's own scale-down thresholds or kubelet eviction settings; only workload-side changes
  are available.
- Making CoreDNS single-replica means DNS outage during node replacement; only do it where that is
  acceptable.
- `safe-to-evict: "true"` on a pod with real local state causes data loss on eviction; use it only
  for caches and agents.
