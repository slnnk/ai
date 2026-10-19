---
system: vk-cloud
status: verified
checked: 2026-10-19
tags: [vk, kubernetes, autoscaler]
---

# VK Kubernetes manual minimum scale check

## Summary

At 12:06–12:08 UTC (15:06–15:08 Moscow), vk-ms1-k8s-test has two old Ready workers. User increased the minimum worker count; autoscaler now sees minSize3/maxSize10 and cloudProviderTarget3. No third node registered during observation. This confirms configuration propagation, not successful provisioning.

## Context and actions

Read-only kubectl with the existing operational kubeconfig: get nodes -o wide, get configmap cluster-autoscaler-status -n kube-system, get events -A, get pods -A. No infrastructure changes or restart was performed. Diagnostic API helper is /home/slnnk/ai-data/buildapi-vk/check_scale.py; credentials are read in memory from existing private configuration.

## Findings

- Status snapshot 2026-10-19T12:08:04Z: autoscaler Running, health Healthy, scaleUp NoActivity, backoffInfo empty, registered ready/total2, unregistered0, longUnregistered0. Group ID3KgZpXnMR0RsZbcUhqHFjUKSXlZ; min3/max10/target3.
- Workers0/1 remain Ready at10.18.26.62 and10.18.26.113, age approximately five days. No new worker appeared during the check.
- Available event stream contained no scaling events or new ScaleUpTimedOut. No autoscaler pod is exposed across visible namespaces, so raw process logs could not be read through kubectl logs. The ConfigMap and Kubernetes events are status evidence, not raw autoscaler logs.
- Catalog container-infra endpoint RegionOne https://msk.cloud.vk.ru/infra/kubernetes/v1: the kubeconfig identity returned an empty cluster list; automation identity returned403 for /clusters. These responses do not establish actual provider group state. Nova server listings do not expose the existing workers under either queried identity, so absence of a third worker VM cannot be concluded from those listings.
- Prior October16 requests2->3->4 timed out registering workers after approximately15minutes; same root cause is possible but unproven for this manual increase.

## Changed files and risks

Added this observation and updated the existing dev-deployment overview and backlog evidence. No repository task files, external resources, credentials or service addresses changed. Provider-side operation details and raw managed autoscaler logs remain unavailable with verified access; root cause and operation start time are unknown.

## Monitoring outcome at 12:11 UTC

User requested monitoring until a new worker or error. At12:11UTC (15:11Moscow), workers-2 was observed Ready, age104seconds, IP10.18.26.125, Kubernetesv1.35.6. Autoscaler snapshot12:11:16Z confirms registered3/ready3, target3, min3/max10 and Healthy. Thus the manual minimum increase successfully added registered capacity; the earlier two-worker discrepancy was transient. Startup Calico readiness warnings were recorded at12:09:49–50Z; current pod readiness is checked separately. This does not establish that demand-driven autoscaling from the October16 incident is repaired.
