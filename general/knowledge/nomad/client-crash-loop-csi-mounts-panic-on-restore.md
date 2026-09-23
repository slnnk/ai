---
system: nomad
status: verified
checked: 2026-07-21
tags: [nomad, client, crash-loop, panic, csi, state.db, systemd, KillMode, logmon]
---
# Nomad client crash loop: panic in `GetCSIMounts`/`prepareCSIVolumes` while restoring allocations

## Symptom

A Nomad client node briefly shows `ready`, then every allocation placed on it stays
`pending`; `Allocated Resources` is `0/… MHz`, `0 B/… GiB`. The server logs repeated
`Node heartbeat missed` / `Node reregistered by heartbeat` for that node. On the host:

```text
systemctl show nomad -p ActiveState -p SubState -p MainPID -p NRestarts
ActiveState=activating  SubState=auto-restart  MainPID=0  NRestarts=133
```

`journalctl -u nomad` shows, seconds after `client: started client`:

```text
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation ...]
github.com/hashicorp/nomad/client/structs.(*AllocHookResources).GetCSIMounts
github.com/hashicorp/nomad/client/allocrunner/taskrunner.(*volumeHook).prepareCSIVolumes
github.com/hashicorp/nomad/client/allocrunner/taskrunner.(*volumeHook).Prestart
```

Side effects: Docker logs `Pull session cancelled` / `context canceled` (the agent dies
mid-pull), and if the unit uses `KillMode=process`, hundreds of orphaned
`nomad logmon` / `docker_logger` processes accumulate (`pgrep -fc "nomad logmon"`,
`TasksCurrent` in the thousands). Disk and RAM are fine. A full reboot does not help.

## Cause

On start the client restores allocations from its local state database
(`<data_dir>/client/state.db`). With Nomad 1.5.x, an allocation that uses a CSI volume and
was interrupted at the wrong moment (lost heartbeat, hard reboot) is restored with
incomplete hook resources, and the volume hook dereferences a nil pointer. Because the
faulty record is persisted, every restart hits the same panic; systemd keeps restarting the
agent and the node flaps between `ready` and heartbeat-missed.

## Fix

Take the node out of scheduling and start the client without the corrupted local state,
keeping its identity:

```bash
nomad node eligibility -disable <node-id>
nomad node drain -enable -yes <node-id>

ssh root@<node> 'systemctl stop nomad'
ssh root@<node> 'pkill -f "nomad logmon"; pkill -f docker_logger'      # orphans, if any
ssh root@<node> 'mkdir -p /var/lib/nomad/client/backups && \
  cp -a /var/lib/nomad/client/state.db /var/lib/nomad/client/backups/state.db.$(date +%Y%m%d-%H%M%S) && \
  mv /var/lib/nomad/client/state.db /var/lib/nomad/client/state.db.disabled'
ssh root@<node> 'systemctl start nomad'
ssh root@<node> 'systemctl show nomad -p ActiveState -p SubState -p NRestarts'   # active/running/0
```

Leave `client-id` and `secret-id` in `<data_dir>/client/` in place so the node re-registers
under the same node ID instead of appearing as a new node. Wait for `Drain complete`, then
`nomad node eligibility -enable <node-id>`. Old allocation directories under
`<data_dir>/alloc` can be removed once a rollback of the saved `state.db` is ruled out.

Long term: upgrade the client off the affected 1.5.x release, and set the systemd unit to
`KillMode=control-group` (or `mixed`) so a crash-looping agent does not leak
`logmon`/`docker_logger` children.

## Limits

- Removing `state.db` discards the client's knowledge of its running allocations: any
  containers still running from before are orphaned and the server reschedules the
  allocations elsewhere. Do this after a drain, on a node you are prepared to lose.
- Observed on Nomad 1.5.3 with Docker 27.x and a CSI plugin; newer releases may have fixed
  the nil dereference, but the state-reset procedure applies to any unrecoverable
  restore-time panic.
- Allocations that then fail with `manifest unknown` on image pull are a separate registry
  or tag problem, not a return of the crash loop.
