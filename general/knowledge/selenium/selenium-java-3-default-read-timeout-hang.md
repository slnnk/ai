---
system: selenium
status: verified
checked: 2026-10-02
tags: [selenium, timeout, java]
---
# selenium-java 3: default 3 h read timeout turns a dead node into a 3 h build

## Symptom

A parallel UI test run (TestNG/JUnit + RemoteWebDriver against Selenium Grid) finishes all
tests in minutes, then the build sits idle for hours with an empty grid. One test log shows a
gap of exactly 180 minutes, followed by `UnreachableBrowserException: Error communicating with
the remote browser`. A thread dump shows one worker blocked in OkHttp `readResponseHeaders`.

## Cause

selenium-java 3.x (e.g. 3.141.59) creates its OkHttp client with a 3 h read timeout. If the
grid node stops answering a command (browser hang, pod restart, the hub closing the session on
inactivity while a request is in flight), the client waits the full 3 h. Test-framework
timeouts do not interrupt a blocked socket read.

## Fix

- Give RemoteWebDriver an `HttpCommandExecutor` with a custom `HttpClient.Factory` whose builder
  sets `readTimeout` to a few minutes (longer than the slowest legitimate command, e.g. page
  load timeout plus margin) and a short `connectionTimeout`. Sketch, check against the
  library version in use:
  `new RemoteWebDriver(new HttpCommandExecutor(emptyMap(), hubUrl, factory), caps)`.
- Or move to Selenium 4, where `ClientConfig.defaultConfig().readTimeout(...)` is passed to
  `RemoteWebDriver.builder()`; its default read timeout is 3 min.
- To confirm: diff timestamps in the test log (gap = 10800 s) or `jstack` the test JVM.

## Limits

The timeout only bounds the damage; the test still fails and needs a retry. The node-side
cause (why the browser stopped answering) must be found separately from grid/node logs.
