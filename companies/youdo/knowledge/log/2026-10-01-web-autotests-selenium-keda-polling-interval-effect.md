---
system: web-autotests
status: verified
checked: 2026-10-01
tags: [selenium, keda, jenkins, autotests, kubernetes]
---
# Selenium Grid k8s-dev: effect of pollingInterval 3 and maxReplicaCount 20

## Task

Check whether the `infra-tf` change of 2026-10-01 sped up WebDriver session start for web
autotests (Jenkins `youdo_web_testing_three` build 1614).

## Context

- `infra-tf` commit `77ce4c2` "update selenium autoscaling config",
  `dev/config/selenium-grid-values.yaml`: `maxReplicaCount` 10 -> 20, added
  `autoscaling.scaledOptions.pollingInterval: 3`. Previous analysis:
  [2026-09-30 slow regress](2026-09-30-web-autotests-selenium-grid-k8s-slow-regress.md).
- Live check: ScaledJob `selenium/selenium-node-chrome` has `pollingInterval: 3`,
  max 20, `scalingStrategy: accurate`, `successfulJobsHistoryLimit: 0`.
- Working kubeconfig for the dev cluster: `~/.kube/config-yandex-dev`
  (`kubectl --context yc-kube-test-temp` from the default kubeconfig times out on
  `10.16.26.68:443`).
- Build 1614 ran `[Smokus]` (`SmokeTestSuite.xml`, `thread-count="12"`, 42 tests) on
  `test13`, not the regress suite.

## Actions

- New script `current/scripts/jenkins_session_start_gap.py <job> <build> ...`: per-test
  `logs_html` gap before the first `remote IP` line (same method as 2026-09-30).
- Sampled Grid GraphQL (`http://selenium.dev.youdo.corp/graphql`, `grid{sessionCount
  nodeCount sessionQueueSize}`) every 5 s during the run: max 11 sessions, queue at most 2.

## Findings

| Build | Grid / settings | Wall | Median | p90 | Max | Sum of gaps |
|---|---|---|---|---|---|---|
| two/1979 09-14 | Selenoid | 25.0 min | 1.2 s | 1.7 s | 62 s | 1.8 min |
| one/3326 09-21 | k8s, poll 20, max 10 | 10.9 min | 72 s | 145 s | 231 s | 54 min |
| one/3337 09-28 | k8s, poll 20, max 10 | 10.5 min | 62 s | 166 s | 379 s | 55 min |
| one/3343 09-30 | k8s, poll 20, max 10 | 11.4 min | 51 s | 137 s | 218 s | 45 min |
| three/1614 10-01 | k8s, poll 3, max 20 | 8.3 min | 10.5 s | 33.5 s | 61 s | 11.5 min |

- Session start dropped about 5x (median 50-70 s -> 10.5 s, p90 ~140 s -> 34 s), Smokus
  wall time 10.5-11.4 -> 8.3 min.
- Still ~7x slower than Selenoid (1-2 s): the rest is Job pod creation, scheduling and
  Chrome node start/registration per session.
- 8 failures in 1614 are functional (SMS code, offers, image display), no
  SessionNotCreated or grid errors.
- Smokus never exceeds 12 parallel sessions, so `maxReplicaCount: 20` was not exercised;
  the effect on regress (12-23 threads, several jobs at once) is not measured yet.

## Regress three/1621 (RegressPartOneTestSuite, test1): hang after the last test

- Started 12:04:14; last test log line 14:21:38 (about 2h17m vs 2h52m-3h05m before), then
  the build stayed running with an empty grid (0 sessions, 0 nodes).
- Jenkins agent `AutoTest` = `jenkins-agent-test-01` (`10.16.26.23`, ssh `root`), agent in
  docker container `jenkins-agent-jenkins_agent-1`; host resources fine (load 0.16, 12 GB
  RAM available, 2 GB disk free). The controller seen in systemInfo is `10.16.26.16`.
- Thread dump of the surefire fork (`docker exec jenkins-agent-jenkins_agent-1 jstack`,
  with the user's permission): 11 TestNG workers idle, `main` in
  `ThreadPoolExecutor.awaitTermination`; worker `Тест-3` renamed to `Forwarding findElement
  on session 539c0c19... to remote`, blocked in OkHttp `readResponseHeaders` from
  `VariableOfferPriceTestSuite.testDifferentBudget` (`TaskPage.java:5198`).
- Hub log: session `539c0c19...` created 12:40:32 on node `10.128.156.126`, deleted
  12:45:58 "session timed out due to inactivity"; the in-flight findElement never got a
  response. Client `selenium-java` 3.141.59 has a default HTTP read timeout of 3 hours, so
  the thread unblocks about 15:40 and the build only then finishes.
- 13 inactivity timeouts in the hub log during the run; cause of the node not answering
  (Chrome hang, pod kill) not established: k8s events had expired and dev Loki has no
  `namespace` label for selenium pods (hypothesis: pod logs are not collected).
- Earlier k8s regress builds (one/3344, three/1594, one/3327) ended right after the last
  test log line, no test over 15 min, so the 3 h hang is new in 1621.

## Regress three/1622 with `scalingType: deployment`

- `infra-tf` `10062f0` (2026-10-01 15:21) `scalingType: job` -> `deployment` (ScaledObject
  on Deployment `selenium-node-chrome`, min 0, max 20, poll 3); 13 node pods during the run.
  `77ce4c2` was rewritten as `dc2d879`.
- RegressPartOneTestSuite, 1594 tests, `jenkins_session_start_gap.py`:

| Build | Settings | Wall | Median | p90 | Max | Sum of gaps | Failures |
|---|---|---|---|---|---|---|---|
| two/1978 09-13 | Selenoid | 93.8 min | 1.5 s | 2.4 s | 62 s | 40 min | - |
| one/3327 09-21 | job, poll 20, max 10 | 179.1 min | 23.1 s | 59.7 s | 213 s | 686 min | 66 |
| three/1594 09-25 | job, poll 20, max 10 | 187.6 min | 24.3 s | 58.9 s | 288 s | 714 min | 84 |
| one/3344 09-30 | job, poll 20, max 10 | 174.3 min | 23.8 s | 55.8 s | 165 s | 655 min | 65 |
| three/1621 10-01 | job, poll 3, max 20 | aborted (tests ~137 min) | - | - | - | - | - |
| three/1622 10-01 | deployment, poll 3, max 20 | 108.4 min | 0.7 s | 1.6 s | 61 s | 31 min | 64 |

- Session start is now at Selenoid level; wall 108 vs 94 min, the rest is not isolated
  (hypothesis: CPU limits of Chrome pods or network path k8s -> test stands).
- Build parameters (`stand`, `branch`): two/1978 `test7` `master`; one/3327 `test1`
  `devops-809-change-selenium-address`; three/1594 `test6` `master`; one/3344 `test1` `master`;
  three/1622 `test1` `testFixTests`. Stand and branch differ, so wall-time comparison with
  Selenoid is approximate.
- Failure count unchanged (64 vs 65-84), so pod reuse did not add failures in this run.

## Changes

- `infra-tf` values change by the user (above); new script
  `current/scripts/jenkins_session_start_gap.py`.

## Open items

In `~/ai/TODO.md` under web-autotests.

## Portable lesson

[Selenium Grid with KEDA job scaling: slow session start per test](../../../../general/knowledge/selenium/keda-job-scaling-slow-session-start.md)
