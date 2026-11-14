---
system: home-network
status: verified
checked: 2026-11-14
tags: [ansible, docker, lampa, torrserver, jackett, deployment]
---
# Home media deployment on home-01

## Task and approval

After [local preparation](2026-11-14-home-network-ansible-home-media.md), user
explicitly requested `Примени плейбук`. Deployment applied home.yml only to
home-01 /192.168.168.2, without nftables. The command and its external effects
were described before execution. The sandbox execution approvals covered the
initial command and the Jackett-only retry after a registry timeout.

## Context

Existing ansible checkout master, no Git changes/publication in this task.
Read-only preflight confirmed root key authentication, Ubuntu26.04 x86_64,
approximately15GiB RAM and214GiB free root filesystem space. Existing host key
was checked through HostKeyAlias=192.168.168.180, retained from the static-IP
migration; StrictHostKeyChecking was not disabled.

## Actions and results

- Ran home.yml limited to home-01: bootstrapped ansible user/key/passwordless
  sudo; applied common hostname home-01, hosts resolution, Moscow timezone and
  locale; validated/reloaded SSH; installed Docker CE/Compose and media services.
- Initial command exited2: ok57/changed31/unreachable0/failed1. Lampa and
  TorrServer had passed readiness; Jackett image download failed with a response
  header timeout from lscr.io. FlareSolverr image had downloaded.
- Described and retried the same playbook with --tags jackett, same host limit
  and SSH key alias. Retry exited0: ok15/changed1/unreachable0/failed0. Jackett
  and FlareSolverr started and both readiness checks passed. No config/image
  changes were needed for the retry.
- Controller logs: ~/ai-data/home-media-deploy-20261114.log and
  ~/ai-data/home-media-deploy-20261114-retry.log. Logs contain no intentionally
  printed application secrets; Jackett settings tasks used no_log/diff suppression.

## Verification

Independent read-only SSH verified four running containers, restart policy
unless-stopped, zero restart counts, and bridge networks lampa_default,
torrserver_default and jackett_default. Published host addresses are only
192.168.168.2:8080/8090/9117. FlareSolverr has no host-published ports.
Hostname resolves locally through127.0.1.1 as home-01.

Independent controller LAN HTTP checks returned200 for Lampa root and MSX JSON,
TorrServer /echo, Jackett root and /UI/Dashboard. MSX action points to
http://192.168.168.2:8080. The playbook verified FlareSolverr HTTP readiness
from inside Jackett through http://flaresolverr:8191/.

## Status and risks

Deployment complete. Both Ansible processes exited and all diagnostic commands
finished; no task background operations remain. Docker services intentionally
remain running. No nftables role, PC migration, tracker credential changes or TV
cutover was performed. Runtime tracker challenge solving and actual TV playback
are not proven by HTTP readiness. Existing indexers/data and TV settings still
need a separately agreed migration; the central TODO retains that action.

Check services with docker ps or docker compose -p NAME -f /opt/NAME/docker-compose.yml ps
on home-01 (NAME=lampa,torrserver,jackett). Stop only if requested, using the same
Compose command with stop; stopping jackett also stops FlareSolverr.

## Portable lesson

none

## Task metrics: home-media-deployment-20261114

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "home-media-deployment-20261114",
  "created": "2026-11-14T19:37:01.215472+03:00",
  "first_result": "pass",
  "final_result": "pass",
  "state": "closed",
  "kind": "operations",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Deployment completed after transient registry retry; independent LAN HTTP and container checks in this note",
  "updated": "2026-11-14T19:37:01.215515+03:00"
}
```
