---
system: web-autotests
status: verified
checked: 2026-10-20
tags: [jenkins, selenium, kubernetes, autoscaling]
---
# Jenkins 2006 Kubernetes autoscaling evidence

## Task and context

Verify whether Kubernetes worker autoscaling operated during https://build.youdo.sg/job/youdo_web_testing_two/2006/.
Cluster: vk-ms1-k8s-test. Read-only investigation; no infrastructure changes.

## Actions

Read Jenkins metadata and console using credentials referenced in current/.env. Read Kubernetes events, nodes, ingresses and cluster-autoscaler-status using the existing private kubeconfig. Queried VictoriaMetrics node and Chrome deployment metrics over the build window; responses were HTTP200 with empty result arrays.
Generated evidence: /home/slnnk/ai-data/jenkins-2006-autoscale/ (private console, build metadata, events and query results).

## Findings

All timestamps below are UTC on 2026-10-20; Moscow time is UTC+3.

- Build ran09:37:39.741–14:04:38.846, duration4h26m59s, on AutoTest, origin/master, test1, suite `Регресс часть 1`. Result `FAILURE`;1594 tests,179 failures,0 errors,52 skipped. Console confirms Selenium Grid browser capabilities.
- At13:51:25, Chrome pod selenium-node-chrome-85c5d99c9f-h75b7 emitted `TriggeredScaleUp`, requesting workers3->4 (max10).
- New workers-2 instance registered13:56:30 (UID799c08f8-39ad-4813-ad88-e56c898e8aab); registration lag5m05s. This verifies successful node registration, not its exact Ready timestamp.
- At14:01:22 autoscaler marked that node for scale-down; `RemovingNode` followed14:02:31. Both scale-up and scale-down occurred inside the build window.
- After the build, another Chrome pod triggered3->4 at14:08:43, with another workers-2 instance registered14:12:53. This is separate from the build-window evidence.
- At14:14:14 cluster autoscaler was Running/Healthy,4Ready/target4/min3/max10.

## Changes

Added this evidence note and a dated pointer in the existing dev-deployment system map. No repository, cluster or external service settings changed.

## Status and risks

Worker autoscaling during the requested build is confirmed by Kubernetes events. Full-window node-count history is unavailable from the queried metrics, and events have limited retention. Shared Selenium demand cannot be uniquely attributed to this Jenkins build. This investigation does not determine why the tests failed or took4h27m. Existing user-closed web-autotest backlog entries remain closed; this read-only question adds no required follow-up.

## Portable lesson

none

## Duration investigation

A later same-day [duration analysis](2026-10-20-web-autotests-jenkins-2006-duration-api-latency.md) identifies slow client-observed stand API calls as the dominant sampled delay; browser-start median0.828s and effective test concurrency approximately11.45. Underlying API latency cause remains unisolated.
