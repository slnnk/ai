---
system: nomad-test
status: verified
checked: 2026-07-21
tags: [incident, nomad, crash-loop, csi, state.db, panic, nomad-1.5.3, nomad-agent-test-02]
---
# 2026-07-21 Nomad yandex-test: nomad-agent-test-02 crash loop

## Task

Services do not start on Nomad client `nomad-agent-test-02`; find the cause, stabilize the
node and return it to scheduling.

## Context

- Cluster: `http://nomad.service.yandex-test.consul:4646`
- Problem node: `root@10.16.26.64`
- Hostname: `nomad-agent-test-02.ru-central1.internal`
- Nomad node id: `fa132122-b34d-798c-f652-1df678a9c74e`
- Nomad version on node: `1.5.3`
- Docker version on node: `27.3.1`
- Check date: `2026-07-21 10:51-10:55 MSK`

## Findings

### Symptom

Services do not start on `nomad-agent-test-02`. In Nomad the node is briefly visible as `ready`, but all new allocations on it stay `pending`; `Allocated Resources` shows `0/31984 MHz` and `0 B/78 GiB`.

Examples of pending allocations after the node re-registered:

- `plugin-yc-csi-monolith.csi[0]` alloc `6a4a67f4`
- `attribution-test*`
- `logreader-test*`
- `youdo-test12-web`, `youdo-test14-web`, `youdo-test16-web`
- `youdo-sms-service-test*`

### Facts found

- The node rebooted / lost heartbeat:
  - `2026-07-21 10:41:54` `Node heartbeat missed`
  - `2026-07-21 10:43:40` `Node reregistered by heartbeat`
  - earlier the same day there were similar `heartbeat missed` events at `05:06`, `05:42`, `09:49`, `09:59`.
- `systemctl show nomad` showed a crash loop:
  - `ActiveState=activating`
  - `SubState=auto-restart`
  - `MainPID=0`
  - `NRestarts=133`
- The `systemd` unit has `KillMode=process`, because of which child processes remain after crashes:
  - `pgrep -fc "/usr/local/bin/nomad logmon"` showed about `659`
  - `TasksCurrent` of `nomad.service` reached approximately `8445`
- There was no critical pressure on disk or memory:
  - root fs about `56%`
  - RAM about `6-7 GiB` of `78 GiB`
- After boot Docker massively logged cancelled pulls:
  - `Pull session cancelled`
  - `Not continuing with pull after error: context canceled`
  - a separate pull: `manifest unknown: Failed to fetch "4.0.1"`

### Root cause

The immediate reason why services do not start on the node: the main Nomad client process falls into a crash loop with a Go panic:

```text
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x18 pc=0x177bbb7]
github.com/hashicorp/nomad/client/structs.(*AllocHookResources).GetCSIMounts
github.com/hashicorp/nomad/client/allocrunner/taskrunner.(*volumeHook).prepareCSIVolumes
github.com/hashicorp/nomad/client/allocrunner/taskrunner.(*volumeHook).Prestart
github.com/hashicorp/nomad/client/allocrunner/taskrunner.(*TaskRunner).prestart
github.com/hashicorp/nomad/client/allocrunner/taskrunner.(*TaskRunner).Run
```

The panic reproduces every few seconds after `client: started client`, during the restore/start of allocations and the preparation of volumes. This looks like a bug/crash of Nomad `1.5.3` while restoring allocation state / the CSI volume hook after a lost heartbeat or inconsistent local state.

The Docker pull errors are a consequence of the short life cycles of the Nomad client: the agent starts `Downloading image`, then crashes, and Docker receives a context cancellation.

## Actions

### Commands used

```bash
nomad node status -address="$NOMAD_YANDEX_TEST_ADDR" -token="$NOMAD_YANDEX_TEST_TOKEN"
nomad node status -address="$NOMAD_YANDEX_TEST_ADDR" -token="$NOMAD_YANDEX_TEST_TOKEN" -verbose fa132122
nomad node status -address="$NOMAD_YANDEX_TEST_ADDR" -token="$NOMAD_YANDEX_TEST_TOKEN" -allocs fa132122
nomad alloc status -address="$NOMAD_YANDEX_TEST_ADDR" -token="$NOMAD_YANDEX_TEST_TOKEN" 6a4a67f4

ssh root@10.16.26.64 'systemctl is-active nomad docker containerd consul; df -h; free -m; uptime'
ssh root@10.16.26.64 'journalctl -u nomad --since "2026-07-21 10:43:00" --no-pager'
ssh root@10.16.26.64 'journalctl -u docker --since "30 min ago" --no-pager'
ssh root@10.16.26.64 'systemctl show nomad -p ActiveState -p SubState -p MainPID -p NRestarts'
ssh root@10.16.26.64 'pgrep -fc "/usr/local/bin/nomad logmon"'
```

### Recommended actions

Safe stabilization:

1. Temporarily forbid new allocations on the node via `nomad node eligibility -disable fa132122`.
2. Stop the Nomad crash loop.
3. Remove the orphaned `nomad logmon`/`docker_logger` processes.
4. After stopping, back up `/var/lib/nomad/client/state.db`.
5. Start Nomad with a clean client state or after removing the problematic stale allocations, then check that the panic is gone.
6. Return eligibility only after a stable start and recovery of allocations.

Long term:

- Check known bugs of Nomad `1.5.3` around CSI volumes and client allocation restore.
- Plan an upgrade of Nomad client/server to a supported version.
- Fix the unit's `KillMode=process`: in a crash loop the child `nomad logmon` processes must not accumulate indefinitely.

### Continuation 2026-07-21 11:03-11:14 MSK

The user disabled eligibility and fully rebooted the server. After the reboot the problem persisted:

- boot: `2026-07-21 11:03`
- `systemctl show nomad`: `ActiveState=activating`, `SubState=auto-restart`, `NRestarts=14`, then the counter kept growing
- the panic stayed the same: `prepareCSIVolumes` / `GetCSIMounts`

Actions performed:

```bash
nomad node drain -address="$NOMAD_YANDEX_TEST_ADDR" -token="$NOMAD_YANDEX_TEST_TOKEN" -enable -yes fa132122
ssh root@10.16.26.64 'systemctl stop nomad'
ssh root@10.16.26.64 'mkdir -p /var/lib/nomad/client/backups'
ssh root@10.16.26.64 'cp -a /var/lib/nomad/client/state.db /var/lib/nomad/client/backups/state.db.20260721-111011'
ssh root@10.16.26.64 'mv /var/lib/nomad/client/state.db /var/lib/nomad/client/state.db.disabled-20260721-111011'
ssh root@10.16.26.64 'systemctl start nomad'
```

Important: `client-id` and `secret-id` were left in place so that the node does not register as a new one.

Result:

- The Nomad client stabilized after `state.db` was disabled.
- `systemctl show nomad`: `ActiveState=active`, `SubState=running`, `NRestarts=0`, `MainPID=111857`.
- `Drain complete` received at `2026-07-21 11:13:01`.
- The node stayed `Eligibility=ineligible`.
- Allocated resources after drain: `0/31984 MHz`, `0 B/78 GiB`.
- One main process remained on the node: `/usr/local/bin/nomad agent -config /etc/nomad.d/client.hcl`.

Side observations after the start:

- Many old allocations failed because of missing Docker tags:
  - `manifest unknown` for `nexus.youdo.com/youdo/microservices/attribution/migrations:1.0.16`
  - `nexus.youdo.com/youdo/microservices/youdo.kitcut/migrations:1.0.0`
  - `nexus.youdo.com/youdo/microservices/youdo-sms-service/migrations:1.0.0`
  - `registry.youdo.sg/youdo/youdo/*:134179`
- There were warnings `error creating task api socket ... bind: invalid argument`, probably from old alloc dirs.
- `/var/lib/nomad/alloc` after the drain occupies about `4.8G`; it can be cleaned after confirming that a rollback of the old state is not needed.

Current safe state:

- Do not put the node back into scheduling until a decision on cleanup and, preferably, an upgrade/fix of Nomad.
- To return to the cluster: after an additional check clean the stale `/var/lib/nomad/alloc`, then `nomad node eligibility -enable fa132122`.

### Returning the node to scheduling

At `2026-07-21 11:15 MSK` the user asked to enable the node. Before enabling:

- `Nomad`: `active/running`
- `NRestarts=0`
- `Drain=false`
- `Eligibility=ineligible`
- `Allocated Resources`: `0 CPU`, `0 memory`

Command:

```bash
nomad node eligibility -address="$NOMAD_YANDEX_TEST_ADDR" -token="$NOMAD_YANDEX_TEST_TOKEN" -enable fa132122
```

Result:

- `Eligibility=eligible`
- `Status=ready`
- `CSI Controllers=yc-csi`, `CSI Drivers=yc-csi`
- Node event: `Node marked as eligible for scheduling`
- Node event: `CSI healthy`
- Nomad process on host remained stable: `ActiveState=active`, `SubState=running`, `NRestarts=0`

After enabling, allocations immediately started being assigned to the node. Some started, some failed on missing Docker images (`manifest unknown`), for example:

- `registry.youdo.sg/youdo/youdo/web/kassa:134179`
- `registry.youdo.sg/youdo/youdo/api:134179`
- `nexus.youdo.com/youdo/microservices/attribution/migrations:1.0.16`
- `nexus.youdo.com/youdo/microservices/youdo.kitcut/migrations:1.0.0`
- `nexus.youdo.com/youdo/microservices/youdo-sms-service/migrations:*`

This is a separate problem of image availability/currency, not a return of the Nomad crash loop.

## Changes

- `/var/lib/nomad/client/state.db` on `nomad-agent-test-02` moved aside (backup in `/var/lib/nomad/client/backups/state.db.20260721-111011`); Nomad restarted; node drained, then eligibility re-enabled.

## Open items

- Clean stale `/var/lib/nomad/alloc` (about 4.8G) once the old state rollback is ruled out.
- Upgrade Nomad from `1.5.3`; fix `KillMode=process` in the systemd unit.
- Investigate the missing Docker image tags (`manifest unknown`) separately.

## Portable lesson

[Nomad client crash loop: panic in `GetCSIMounts`/`prepareCSIVolumes` on allocation restore](../../../../general/knowledge/nomad/client-crash-loop-csi-mounts-panic-on-restore.md)
