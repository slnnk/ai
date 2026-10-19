---
system: vk-cloud
status: verified
checked: 2026-10-19
tags: [vk, kubernetes, selenium, autoscaling]
---
# VK Kubernetes six-worker Selenium scaling diagnosis

## Summary

At 20:17–20:20 UTC (23:17–23:20 Moscow), all six workers were Ready. Selenium Chrome demand caused the latest growth: HPA reached16 replicas at20:06:47UTC and pending Chrome pods directly triggered cluster autoscaler3->4->5->6. Minimum remains3, maximum10. No infrastructure changes were made.

## Task and context

Explain why vk-ms1-k8s-test has six nodes and what increased demand. Earlier same-day checks proved scaling to four; this investigation checks the latest evening burst.

## Actions and key commands

Used existing private kubeconfig at /home/slnnk/ai-data/buildapi-vk/kubeconfig-ci.yaml. Read-only kubectl: get nodes, get events -A (then bounded reason-specific JSONPath), get hpa -A, get deployment selenium-node-chrome -n selenium, get configmap cluster-autoscaler-status -n kube-system, top nodes, top pods -A sorted by cpu/memory. Inspected pod placement on workers-1. No secrets copied.

## Findings

- HPA events:2 replicas20:01:16UTC,4 at20:01:46,8 at20:02:01,11 at20:04:01,14 at20:05:47,16 at20:06:47. Scale-up reason: external metric s0-selenium-grid-chrome above target.
- Chrome requests1CPU/2Gi per pod, limits2CPU/3Gi;16 replicas request16CPU/32Gi in total. Each worker has7910m CPU and roughly27.2Gi allocatable RAM.
- TriggeredScaleUp events identify Chrome pods directly:3->4 at20:04:00UTC (z6b9n),4->5 at20:06:50 (7sn8b),5->6 at20:09:20 (2p8ps). Scheduler reports Insufficient cpu and Insufficient memory.
- New workers registered at20:09:08,20:11:44,20:13:05UTC. Autoscaler at20:17:49: Healthy, target6/min3/max10, scaleUp NoActivity, scaleDown CandidatesPresent with3 candidates.
- Chrome had already decreased to8Ready replicas at20:17UTC; scale-down completion was not observed. The six nodes reflect recent peak requests and delayed removal, rather than six continuously saturated hosts.
- One sample of workers-1: CPU99%, RAM97%; other workers CPU0–16%, RAM4–44%. Top CPU consumers include Sentry ClickHouse and taskworker-ingest plus Chrome; Loki chunks cache uses about4Gi RAM. Workers-1 hosts both Sentry and monitoring pods. This shows concentrated background load; no historical baseline was collected to attribute an increase in Sentry load.
- Exact originating Jenkins build/test suite was not established. Direct evidence identifies Selenium browser demand as the scale-up trigger. Historical provider registration timeout remains unresolved; successful current scaling does not explain the earlier failure.

## Changed files and risks

Added this log; linked current observation from existing dev-deployment overview and the existing web-autotests TODO entry. No cluster, repository or service configuration changed. Node removal timing and background-load evolution were not established.
