---
system: jenkins
status: verified
checked: 2026-10-22
tags: [jenkins, timezone, autotest]
---
# AutoTest agent Moscow timezone investigation and change proposal

## Task

Investigate the user-reported three-hour discrepancy in web autotests and prepare the analogous Moscow timezone change for the Jenkins agent. External changes require explicit approval of the concrete command.

## Context

Reported artifact: https://build.youdo.sg/job/youdo_web_testing_two/2026/artifact/uitests/logs_html/TaskTwoBrowsersTestSuite_testFlowInOpenTask.html
Controller display timezone was changed separately on 2026-10-16. Agent is `AutoTest` on `vk-ms1-jenkins-agent-test-01`, `10.18.26.26`.

## Actions

Read authenticated Jenkins build/node metadata and inspected host/container timezone and sanitized Compose structure over SSH. No remote modifications or test runs.

## Findings

- Build 2026 ran on `AutoTest` and finished `FAILURE`. All five executors were idle during inspection; node online.
- Host and container report UTC. Container has neither `TZ` nor Java timezone override. `/etc/localtime` and `/etc/timezone` are read-only host mounts; host uses `Etc/UTC`.
- Container `jenkins-agent-jenkins_agent-1` runs JDK 21.0.10 and contains Moscow zoneinfo. Active Compose is `/data/jenkins-agent/docker-compose.yml`, service `jenkins_agent`; environment uses list syntax.
- Artifact was fetched successfully using authenticated HTTP; bounded assertion filtering did not independently establish the exact expected/actual timestamp pair. The runtime timezone discrepancy is confirmed.

## Changes

Prepared local helper `/home/slnnk/ai-data/jenkins-recovery/set-agent-timezone.py`. Proposed additions: `TZ=Europe/Moscow` and `JAVA_TOOL_OPTIONS=-Duser.timezone=Europe/Moscow` to the agent environment, then recreate only `jenkins_agent`. Existing configuration is backed up with mode 0600; merged Compose must differ only in these two variables. Helper checks all executors idle and queue empty before SSH; this is a point-in-time check, not a scheduling lock. Host timezone remains unchanged.

Dry preview and embedded Python compilation passed. User approved runtime application with `Примени`. Executed `python3 /home/slnnk/ai-data/jenkins-recovery/set-agent-timezone.py --apply`: idle/empty-queue guards passed, merged Compose matched exactly the two reviewed environment additions, protected backup created at `/data/jenkins-agent/docker-compose.yml.before-timezone-20261022T080316Z`, and only the agent container was recreated successfully at 08:03:17 UTC.

Independent read-only checks at 08:03:52 UTC confirmed the container running with its original image reference, `TZ=Europe/Moscow`, `JAVA_TOOL_OPTIONS=-Duser.timezone=Europe/Moscow`, container date `2026-10-22T11:03:52+03:00`, and Java 21.0.10 reporting `user.timezone = Europe/Moscow`. Jenkins API reports `AutoTest` online, not temporarily offline, with all five executors idle. Host OS remains `Etc/UTC`. No repository edits, Git mutations or test runs. The reported test was not rerun; functional verification will come from a subsequent run. Canonical Ansible does not yet include these runtime settings; a future role apply may overwrite them and requires separate repository proposal/approval if requested.

## Open items

Runtime timezone change and container/JVM/connectivity verification are complete. The central Jenkins recovery item tracks canonical configuration alignment; the task-specific timezone item is closed. No test success is claimed.

## Portable lesson

none
