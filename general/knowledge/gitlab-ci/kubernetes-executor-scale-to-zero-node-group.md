---
system: gitlab-ci
status: hypothesis
checked: 2026-09-16
tags: [gitlab-runner, kubernetes-executor, helm, cluster-autoscaler, scale-to-zero, taints, keda]
---
# Scale-to-zero GitLab runners on Kubernetes: keep the manager, scale the node group

## Symptom

You want CI capacity that costs nothing while idle, so you try to scale the GitLab Runner
Deployment itself to zero (HPA/KEDA on CPU or a custom metric). Jobs then queue forever or
start with large delays, because nothing is left to notice them.

## Cause

GitLab Runner is a **poller**: the manager process asks GitLab for jobs; GitLab never pushes.
With zero manager replicas no component discovers the next job. KEDA (2.20 checked) has no
built-in GitLab-queue scaler, and a custom external scaler must handle tokens, tag matching,
rate limits and races, while still needing something running all the time.

## Fix

Scale the **nodes**, not the manager:

```text
GitLab -> 1 small always-on runner-manager pod (permanent node group)
       -> 1 pod per job (Kubernetes executor)
       -> dedicated CI node group, autoscaled 0..N by Cluster Autoscaler
```

1. Install the official `gitlab-runner` Helm chart with one replica, ~`100m/128Mi` requests,
   a namespace-scoped Role, and node affinity that keeps it **off** the CI nodes.
2. Create a separate node group with `min=0`, an explicit `max`, a label and a taint, for
   example `workload=ci:NoSchedule`.
3. In the runner config give job pods the matching selector and toleration:

   ```toml
   [runners.kubernetes]
     [runners.kubernetes.node_selector]
       "workload" = "ci"
     [runners.kubernetes.node_tolerations]
       "workload=ci" = "NoSchedule"
   ```

4. Give every job pod **resource requests**: Cluster Autoscaler scales on unschedulable
   pods and their requests, not on utilization. Heavy builds must request enough to force a
   node; light jobs (notifications, uploads) should request little.
5. Raise the pod scheduling/startup timeouts so the first job survives a cold VM boot plus
   image pull (typically several minutes). Optionally keep one warm node during business hours.
6. Do not attach a shared PVC (Gradle/NuGet cache) to job pods: a bound volume can keep a
   node alive and prevent scale-down. Use the runner's object-storage cache instead.

Validate before cutover from a pod on the CI node group: reachability of GitLab, the
container registry, package mirrors, object-storage cache and any external APIs; then test a
cold start, job success, cache behavior, pod cleanup, and the group returning to zero.

## Limits

- Managed Kubernetes providers differ: some require at least two nodes in other groups before
  a group may reach zero, and count `max` toward cloud quotas. Default scale-down delay is
  usually ~10 minutes of low utilization.
- Jobs that need the host Docker socket, node-local image cache, fixed host paths or
  attached devices cannot move unchanged. Privileged DinD works but widens the security
  boundary; isolate it on its own runner.
- Cold start latency is inherent; if unacceptable, keep `min=1`.
- Reviewed against GitLab Runner 17.9 / chart 0.74 docs; not yet run in production.
