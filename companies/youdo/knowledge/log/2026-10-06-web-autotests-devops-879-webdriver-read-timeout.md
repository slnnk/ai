---
system: web-autotests
status: verified
checked: 2026-10-06
tags: [selenium, autotest-core, timeout, DevOps-879]
---
# Web autotests: DevOps-879 RemoteWebDriver read timeout in autotest-core

## Summary

DevOps-879: `autotest-core` now creates RemoteWebDriver with a bounded HTTP read timeout
(`autotests.remote.read.timeout`, minutes, default 10) instead of the selenium-java 3.141.59
default of 3 h. Merged, released and ticket closed by the user on 2026-10-06.

## Task

Set a sane read timeout for RemoteWebDriver so a hung Grid call fails in minutes, not 3 h.

## Context

Regress three/1621 and failed-tests rerun three/1623 each hung exactly 180 min on one WebDriver
call ([2026-10-02 log](2026-10-02-web-autotests-failed-rerun-3h-webdriver-read-timeout.md)).
Driver creation lives in `autotest-core` (`git@gitlab.youdo.sg:team-youdo-testers/autotest-core.git`),
not in `youdo.static`. No `pageLoadTimeout` is set in the library, so the W3C default 300 s applies;
10 min stays above it.

## Actions

- Branch `DevOps-879-http-timeout` from `master` `1980c7a`.
- `SeleniumTestConfigUtil.getRemoteReadTimeoutMinutes()`: reads `autotests.remote.read.timeout`
  via `getValueFromEnvOrConfig` (system property, env or `selenium.properties`); missing or
  unparsable -> 10.
- `Browser.java`: `new RemoteWebDriver(new HttpCommandExecutor(Collections.emptyMap(), new URL(REMOTE), remoteHttpClientFactory()), capabilities)`;
  the factory wraps a static `HttpClient.Factory.createDefault()` and sets only `readTimeout`.
- API checked in `selenium-remote-driver-3.141.59.jar`; compiled with
  `JAVA_HOME=/opt/android-studio-2024.1.1/android-studio/jbr bash gradlew compileJava`
  (no system JDK on the workstation; `--offline` fails on the missing aspectj plugin).

## Findings

- Override per run: `-Dautotests.remote.read.timeout=<minutes>`.
- Values <= 0 are passed through unchecked.

## Changes

`autotest-core`: `src/main/java/autotest/core/util/Browser.java`,
`src/main/java/autotest/core/util/config/SeleniumTestConfigUtil.java`. Merge, release and the
`youdo.static` bump were done by the user.

## Open items

None tracked: the user closed the task; QA will report problems. Not investigated: why Grid
nodes stop answering (hub inactivity timeouts) - the timeout only bounds the hang.

## Portable lesson

[selenium-java 3 default 3 h read timeout hides hung remote calls](../../../../general/knowledge/selenium/selenium-java-3-default-read-timeout-hang.md)
