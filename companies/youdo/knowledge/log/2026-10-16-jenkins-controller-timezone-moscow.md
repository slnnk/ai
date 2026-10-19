---
system: jenkins
status: verified
checked: 2026-10-16
tags: [jenkins, timezone, vkcloud]
---
# Jenkins controller display timezone set to Moscow

## Task

Set the Jenkins server's default displayed time zone to Moscow for users who inherit the controller default.

## Context

The authenticated profile had no personal time-zone override. Jenkins reported `user.timezone=Etc/UTC`; the controller runs in Docker on `vk-ms1-jenkins-test` (`10.18.26.8`). The active Compose project uses `/data/jenkins/docker-compose.yml` plus the protected image override `/data/jenkins/compose-devops-891-image.yml`.

## Actions

- After the user approved the server-wide change, added `TZ=Europe/Moscow` and appended `-Dorg.apache.commons.jelly.tags.fmt.timeZone=Europe/Moscow` to the existing `JAVA_OPTS` in `/data/jenkins/docker-compose.yml`; preserved the existing CSP option and the image override.
- Validated the merged Compose configuration, then recreated the controller using `docker-compose -f /data/jenkins/docker-compose.yml -f /data/jenkins/compose-devops-891-image.yml up -d --no-deps --force-recreate jenkins` after separate user confirmation.

## Findings

- Jenkins 2.555.1 returned to service. The running container retained image digest `sha256:458ac695b4114f0f3f837a3c99294c1a82e629ab2b53b1be2ea35c97a9425e71` and exposes `TZ=Europe/Moscow` plus the Jelly formatter property.
- Authenticated `/manage/systemInfo` reports both `user.timezone` and `org.apache.commons.jelly.tags.fmt.timeZone` as `Europe/Moscow`. Jenkins API is ready; queue and busy executors are zero.
- The server default affects users who inherit it. Users with a personal time-zone preference may continue to see that preference.

## Changes

Remote Compose configuration updated and Jenkins container recreated. No host operating-system clock or time zone was changed.

## Open items

None.

## Portable lesson

none
