---
system: selenium
status: verified
checked: 2026-09-30
tags: [selenium, keda, kubernetes]
---
# Selenium Grid with KEDA job scaling: slow session start per test

## Symptom

After moving UI tests from Selenoid (warm docker hosts) to the `selenium-grid` Helm chart
with `autoscaling.scalingType: job`, the same suite with the same thread count takes about
2x longer. Browser steps run at the old pace; the extra time sits before the first command
of each test, where the WebDriver session is created (tens of seconds instead of 1-3 s).

## Cause

- The suite opens a new session per test method. With `scalingType: job`,
  `minReplicaCount: 0` and `nodeMaxSessions: 1`, every session waits for KEDA to notice the
  queued request (chart default `autoscaling.scaledOptions.pollingInterval: 20` s), then
  for a Job and a pod to be scheduled, the browser container to start and the node to
  register with the hub.
- Long tails come from `maxReplicaCount` below the total test thread count (requests
  queue) and from cluster-autoscaler adding nodes that must pull the browser image first.

## Fix

- Measure first: compare per-test logs before/after and time the gap before the first
  browser command; compare wall time with the sum of test durations to separate
  "slower tests" from "less parallelism".
- Lower `autoscaling.scaledOptions.pollingInterval` to a few seconds. Observed effect of
  20 -> 3 s on a 12-thread suite: median session start ~60 s -> ~10 s, p90 ~140 s -> ~35 s;
  the remaining ~10 s is Job pod start and node registration. Switching to
  `scalingType: deployment` removed it: on a 1600-test, 12-thread suite median session start
  ~24 s -> 0.7 s and wall time ~3 h -> 1 h 48 min.
- Set `maxReplicaCount` at least to the sum of threads of suites that run at once, and make
  sure the node group can host that many browser pods.
- Keep a warm pool: `minReplicaCount` near the usual thread count, or use
  `scalingType: deployment` so node pods are reused between sessions.
- Pre-pull the browser image on nodes (DaemonSet) or keep a minimum node count so scale-up
  does not add image pull time.

## Limits

Warm pools cost idle capacity. `scalingType: deployment` reuses node pods, so a crashed
browser can affect the next session; job scaling gives stronger isolation.
