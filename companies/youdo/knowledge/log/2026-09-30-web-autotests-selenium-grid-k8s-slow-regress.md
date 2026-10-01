---
system: web-autotests
status: verified
checked: 2026-09-30
tags: [selenium, keda, jenkins, autotests, kubernetes]
---
# Web autotests slow after Selenoid -> Selenium Grid k8s-dev

## Task

QA complained that web autotests in Jenkins view `Web+API Tests`
(`youdo_web_testing_one|two|three`, repo `youdo.static`, `uitests/`) became slow after the
switch from Nomad Selenoid+GGR to Selenium Grid in k8s-dev (`infra-tf` `dev/selenium.tf`,
`dev/config/selenium-grid-values.yaml`). Find the cause and old regress durations in S3.

## Context

- Switch: `youdo.static` commit `e7466339f0` (2026-09-18, DEVOPS-809) set
  `remote="http://selenium.dev.youdo.corp/wd/hub"` in `uitests/config/selenium.conf`.
- Old grid: 3 VM `sel-test-01..03`, Selenoid `-limit 10` each, about 30 parallel sessions,
  warm local docker.
- New grid: chart `selenium-grid` 0.59.1, `autoscaling.scalingType: job`,
  `minReplicaCount: 0`, `maxReplicaCount: 10`, `nodeMaxSessions: 1`, chart default
  `autoscaling.scaledOptions.pollingInterval: 20`; one Chrome pod per session
  (request 1 CPU / 2Gi, limit 2 CPU / 3Gi).
- `RegressPartOneTestSuite.xml`: `parallel="methods" thread-count="12"`;
  `AllTestSuiteParallel.xml`: `thread-count="23"`. The three Jenkins jobs share one grid.

## Actions

- Jenkins API `allBuilds` of the three jobs: retention is only 30 builds (oldest
  2026-09-13), so only one pre-switch regress survives.
- Compared `uitests/report/report.html` and per-test `logs_html/*.html` artifacts of
  builds two/1978 (Selenoid) vs one/3327, one/3344, three/1594 (k8s).
- S3: `aws --profile s3yandexc2c --endpoint-url https://storage.yandexcloud.net`;
  bucket `youdo-smokus`, prefixes `yandex/youdo.static/<gitlab job id>/` and
  `yandex/youdo/<id>/` hold 167 reports, all `[Smokus]` from GitLab, 2026-08-03..09-09.
  No regress reports in Yandex or Selectel S3 profiles.
- Cluster check with `kubectl --context yc-kube-test-temp` timed out (no API access from
  the workstation at that time); ScaledJob live values not verified.

## Findings

| Build | Grid | Tests | Wall | Sum of test times | Median test |
|---|---|---|---|---|---|
| two/1978 2026-09-13 test7 | Selenoid | 1594 | 1h29m | 943 min | 25 s |
| one/3327 2026-09-21 test1 | k8s | 1594 | 2h57m | 1959 min | 61 s |
| three/1594 2026-09-25 test6 | k8s | 1594 | 3h05m | 2017 min | 61 s |
| one/3344 2026-09-30 test1 | k8s | 1594 | 2h52m | 1873 min | 58 s |

- Effective parallelism unchanged (~11); every test got ~2.4x longer.
- Sample of 40 identical tests, gap before the `remote IP` log line (new WebDriver
  session): Selenoid median 1.5 s, p90 2.8 s; k8s median 18.3 s, p90 48 s, max 78 s.
  Session start is ~75% of the added time. Browser steps themselves run at the same pace.
- Cause: new session per test + KEDA job scaling from zero (poll every 20 s, then Job,
  scheduling, container start, node registration). p90/max point to queueing: 12 threads
  (plus parallel jobs) vs `maxReplicaCount: 10`, and cluster-autoscaler scale-up with
  image pull on fresh nodes (hypothesis).
- Remaining ~25% of added time: not isolated (hypothesis: CPU throttling of 1 CPU pods or
  network path k8s -> test stands).
- Smokus (42 tests) is not affected noticeably: S3 median 11 min (n=105), Jenkins now 10-11.

## Changes

None; only analysis. Proposed values changes in `infra-tf` (not applied):
`autoscaling.scaledOptions.pollingInterval` 20 -> 2-5, `maxReplicaCount` 10 -> >=30,
warm pool (`minReplicaCount`) or `scalingType: deployment` with node reuse.

## Open items

In `~/ai/TODO.md` under web-autotests.

## Portable lesson

[Selenium Grid with KEDA job scaling: slow session start per test](../../../../general/knowledge/selenium/keda-job-scaling-slow-session-start.md)
