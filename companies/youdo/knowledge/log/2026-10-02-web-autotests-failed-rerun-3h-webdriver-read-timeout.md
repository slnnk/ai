---
system: web-autotests
status: verified
checked: 2026-10-02
tags: [selenium, jenkins, autotests, timeout]
---
# Web autotests: failed-tests rerun three/1623 hung 3 h on WebDriver read timeout

## Summary

`youdo_web_testing_three` #1623 (rerun of the 116 failed tests of #1622, `FailedTestSuite_0001622.xml`,
`parallel="methods" thread-count="12"`, `test1`, `origin/testFixTests`) took 233.7 min. All tests
except one finished by ~17:35; one WebDriver call then waited exactly 180 min (selenium-java
3.141.59 default HTTP read timeout). Same failure as three/1621. Session start is fine (median 0.7 s).

## Task

QA: report https://build.youdo.sg/job/youdo_web_testing_three/1623/artifact/uitests/report/report.html,
the run took very long.

## Context

- Previous analysis: [2026-10-01 log](2026-10-01-web-autotests-selenium-keda-polling-interval-effect.md)
  (`scalingType: deployment`, 1621 hang).
- Rerun is triggered by the job's post-build script with `failedSuiteAuto=FailedTestSuite_000<prev>.xml`,
  `-Dautotests.retry.count=1`. The suite XML is generated on the agent and archived as artifact.

## Actions

- Jenkins API: build params, `consoleText`, `report.html`, all 112 `logs_html/*.html`,
  `FailedTestSuite_0001622.xml` artifact.
- `current/scripts/jenkins_session_start_gap.py youdo_web_testing_three 1623`: 52 tests with a
  session, median 0.7 s, p90 8.8 s, max 60.9 s, sum 5.5 min.
- Timeline from first/last log line per test (10 min buckets): 35 + 40 tests started 17:14-17:30,
  from 17:35 to 21:07 only one test running.
- `kubectl --context yc-kube-test-temp` timed out again (no API access); hub log for the session not checked.

## Findings

- Hanging test: `LinksTestSuite.testDirectAccessToExternalLinkWithTrustedTrueOfHost`, session
  `5a33fc5c9e8d454b03abf2ea8d155124`. Last line `17:38:54,643 Окно браузера №2 открыто`, next
  `20:38:54,663 UnreachableBrowserException` from `RemoteWebDriver$RemoteTargetLocator.activeElement`
  in `autotest.core.util.Interaction.switchToWindow(Interaction.java:430)`. Gap 180m00s = 3 h
  default read timeout. The test opens external links (`xn--j1ail.xn--p1ai/ad.php?...`) in a
  second window; the call after the switch never got a response (cause on the node side not
  established; hypothesis: same as 1621, grid kills the session on inactivity while the
  request is in flight).
- After the timeout the retry ran 20:39-21:07 and passed. `report.html` shows 49.5 min for the
  test, it does not count the hang.
- Without the hang the rerun would take about 25-30 min (sum of all other test times ~146 min / 12 threads,
  plus tail of the long Links tests).
- 40 failures are functional / stand-related: `Ошибка при получении paymentId или requestId`
  (SBR, `SocketTimeoutException` in okhttp HTTP/2), insurance titles not shown, 4 `ТЕСТ НЕ НАПИСАН`,
  52 skipped as dependents.
- `autotest.core` (WebDriver creation, `Interaction`) is not in `youdo.static`; it is an external
  library dependency, so the timeout fix belongs there.

## Changes

None; analysis only.

## Open items

In `~/ai/TODO.md` under web-autotests (WebDriver read timeout item, now with two occurrences).

## Portable lesson

[selenium-java 3 default 3 h read timeout hides hung remote calls](../../../../general/knowledge/selenium/selenium-java-3-default-read-timeout-hang.md)
