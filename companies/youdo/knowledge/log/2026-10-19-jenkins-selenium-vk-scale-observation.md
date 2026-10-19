---
system: jenkins
status: verified
checked: 2026-10-19
tags: [selenium, kubernetes, vk, autoscaler]
---

# Selenium VK autoscaling observation

## Summary

User-started autotests activated Selenium Chrome pods in vk-ms1-k8s-test. Demand-driven worker scaling succeeded3->4: requested12:15:37UTC, workers-3 observed Ready12:21:18UTC, all12Chrome pods Ready12:21:57UTC and again12:22:34UTC. Final snapshot around12:30UTC:11/11Chrome pods Ready, no Pending and0restarts; Hub/scaler1/1Ready. No remote state was changed by the agent.

## Context and actions

Read-only kubectl get pods/deployments/hpa/events, autoscaler status ConfigMap and recent Hub logs. Compact monitoring helper: /home/slnnk/ai-data/buildapi-vk/monitor_selenium.py --interval30 --minutes20 (use normal argument spacing). Existing private kubeconfig and exec authentication reused; no credentials copied.

## Findings

- KEDA activated Chrome0->1 at12:14:39UTC; HPA increased1->4 at12:14:53,4->8 at12:15:08,8->12 at12:15:23.
- Eight Chrome pods became Ready on the initial three workers, seven on newly added workers-2. Four pods remained Pending: scheduler reported insufficient memory/CPU.
- Image pull onto workers-2 succeeded in approximately27seconds including waiting (image2.21GB). No registry DNS failure appeared in the observed launch events.
- At12:15:37UTC, TriggeredScaleUp requested3->4 (max10), autoscaler InProgress. Workers-3 was Ready by12:21:18UTC; all12Chrome pods Ready by12:21:57UTC. Approximate observed provisioning interval5m41s, total until all Chrome Ready6m20s. Monitoring ended after two consecutive ready snapshots.
- Hub logs around15:25–15:30Moscow contain node draining/removal, subsequent browser session creation and normal QUIT session closure. Draining is observed lifecycle behavior; no claim that every test passed.
- Final snapshot around15:30Moscow: Chrome11/11Ready, restarts0, HPA desired/current11, metric0/target1; Hub and external scaler Ready. This was a later pod population than the initial12, consistent with scaling/lifecycle activity; exact cause of each replacement was not investigated.
- This verifies one successful demand-driven expansion, superseding the earlier absence of such evidence. It does not establish the cause of October16 provisioning timeouts or guarantee all future scaling operations.

## Changed files and limits

Added this log, updated the canonical dev-deployment map and existing backlog observation. No repository, test configuration, deployment or cloud changes made. Test outcomes and Jenkins job result were outside this observation; managed autoscaler raw logs remain unavailable via cluster pods.
