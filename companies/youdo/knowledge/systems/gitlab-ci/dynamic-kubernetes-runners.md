---
system: gitlab-ci
status: hypothesis
checked: 2026-09-16
tags: [gitlab-runner, kubernetes, autoscaling, scale-to-zero, yandex-cloud]
---
# Dynamic GitLab runners in Kubernetes

Last checked: 2026-09-09. Design document; no runner has been applied yet (see the 2026-09-16 update).

## Context and feasibility

- GitLab coordinator: `https://gitlab.youdo.sg` (self-managed).
- Current general-purpose Linux runners are Docker/DinD hosts managed from
  `/home/slnnk/git/automation-services`, primarily Selectel hosts
  `172.28.0.171` through `172.28.0.173`.
- The Ansible role pins Linux GitLab Runner `17.9.3-1` at the time of review.
- No existing Kubernetes-executor deployment was found in `automation-services`,
  `infra-tf`, `yandex-tf`, or `helm-charts`.
- A Kubernetes runner is feasible with the official GitLab Runner Helm chart.
  The runner manager polls GitLab and creates one Kubernetes pod per accepted CI
  job.

## Recommended architecture

Use practical scale-to-zero rather than scaling the runner manager itself to
zero:

`GitLab -> small always-on runner-manager pod -> per-job pod -> dedicated autoscaled node group (0..N)`

- Keep one low-resource runner-manager pod on the cluster's existing permanent
  node group. It is the component that polls GitLab for work.
- Add a dedicated CI node group with `auto_scale.min = 0`, an explicit maximum,
  labels and a taint. Select it from GitLab job pods with node selector and
  toleration.
- With an empty queue there are no CI job pods and the CI node group can reach
  zero nodes. When the manager creates an unschedulable job pod, Yandex Managed
  Kubernetes Cluster Autoscaler adds a node; after job pods disappear it scales
  the group down again.
- Do not scale the manager Deployment to zero based only on ordinary Kubernetes
  metrics: no component would remain to poll GitLab and discover the next job.
  KEDA 2.20 does not provide a built-in GitLab Runner queue scaler. A custom
  external scaler/API poller is possible but adds token handling, tag-matching,
  race, rate-limit, and availability complexity without removing the need for a
  continuously running polling component.

## Fit with the current Yandex cluster

The current working tree at `/home/slnnk/git/yandex-tf/test-k8s/k8s-cluster.tf`
describes cluster `kube-test`, Kubernetes `1.34`, and one node group sized as
8 vCPU / 48 GiB with autoscaling `min=1`, `initial=1`, `max=10`. The yandex-tf
working tree already contains unrelated user changes, so these values are a
configuration snapshot, not a runtime verification.

Do not repurpose that shared node group for scale-to-zero: it hosts permanent
dev/platform workloads and has minimum one node. Add a separate CI node group.
Keep the manager on the permanent group and isolate CI workers using labels,
taints, resource requests/limits, priority classes, and namespace/RBAC.

Yandex Managed Kubernetes currently accepts zero as the minimum size of an
autoscaled node group. Cluster Autoscaler reacts to unschedulable pods based on
their resource requests. Yandex counts the configured maximum group size toward
cloud quotas, so choose `max` deliberately.

## Migration and operational constraints

1. Start with a new protected runner and tag such as `k8s-dynamic`; migrate a
   representative non-production build/test subset before changing existing
   tags.
2. Reuse the existing object-storage cache contract (bucket name is already
   present in runner inventory), but supply access through the approved secret
   path/Kubernetes Secret or Vault operator. Never copy credentials into Helm
   values or Terraform state. Existing runner inventory contains plaintext
   access material and should be migrated/rotated separately; values were not
   copied into this note.
3. Validate egress and DNS from job pods to GitLab, GitLab Registry, Nexus,
   object storage, and required corporate/test services.
4. Existing jobs that depend on a host Docker socket, persistent local Docker
   layer cache, fixed host paths, attached devices, or macOS/Windows cannot move
   unchanged. Privileged DinD is possible in Kubernetes but expands the security
   boundary; prefer BuildKit/rootless builders where compatible and isolate any
   privileged runner.
5. Account for cold-start queue latency while a node VM boots. Set runner pod
   scheduling/startup timeouts accordingly; optionally keep one warm CI node
   during business hours if latency is unacceptable.
6. Preserve the current runners during the pilot for rollback. Monitor GitLab
   queue duration, runner request failures, pending/unschedulable pods, node-group
   scaling failures, image pull time, cache hit rate, and Yandex quotas.

## Sources

- GitLab Runner Helm chart: https://docs.gitlab.com/runner/install/kubernetes/
- GitLab Kubernetes executor: https://docs.gitlab.com/runner/executors/kubernetes/
- GitLab runner autoscaling overview: https://docs.gitlab.com/runner/runner_autoscale/
- Yandex node-group autoscaling: https://yandex.cloud/en/docs/managed-kubernetes/concepts/node-group/cluster-autoscaler
- Yandex NodeGroup API limits: https://yandex.cloud/en/docs/managed-kubernetes/managed-kubernetes/api-ref/NodeGroup/get
- KEDA scaler catalog: https://keda.sh/docs/latest/scalers

## Next step

Prepare a read-only capacity and compatibility inventory: job counts and queue
peaks by runner tag, CPU/RAM requests, privileged DinD/socket usage, cache and
network dependencies. Then choose the first pilot tag and CI node-group shape.

## 2026-09-09 selected pilot

The first selected project is `team-youdo-android/android-youdo4`; all of its CI
jobs are in scope. The target is the existing Selectel Managed Kubernetes
cluster `mks-infra`, using a separate node group that scales from zero. Cold
startup delay is accepted. The project-specific verified map and proposed
rollout are in [`android-youdo4-dynamic-runner.md`](android-youdo4-dynamic-runner.md) in this directory.

## 2026-09-16 target update

- Final target changed from Selectel `mks-infra` to Yandex Managed Kubernetes
  cluster `kube-test`, managed from `/home/slnnk/git/yandex-tf/test-k8s`.
- The architecture remains unchanged: an always-on runner-manager on permanent
  nodes creates Kubernetes executor job pods on a dedicated, tainted Android CI
  node group with autoscaling from zero.
- Treat the 2026-09-09 Selectel target above as superseded historical context.

## Portable lesson

[`~/ai/general/knowledge/gitlab-ci/kubernetes-executor-scale-to-zero-node-group.md`](../../../../../general/knowledge/gitlab-ci/kubernetes-executor-scale-to-zero-node-group.md)
