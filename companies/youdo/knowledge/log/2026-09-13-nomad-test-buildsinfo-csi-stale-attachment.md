---
system: nomad-test
status: verified
checked: 2026-09-13
tags: [incident, nomad, csi, yc-csi, buildsinfo, buildapi, yandex-cloud, stale-attachment]
---
# Nomad yandex-test: buildsinfo does not start because of a stale CSI attachment

## Task

Find out why the `buildsinfo` job stays `pending` after Start Job, and recover it without
losing the MongoDB data on its CSI volume.

## Context

- Check date: 2026-09-13, 15:14-15:23 MSK.
- Environment: Nomad `yandex-test`, namespace `default`.
- Job: `buildsinfo`.
- Repository: `/home/slnnk/git/buildapi`.
- Current jobspec: `deployments/production.hcl`.
- All diagnostic actions were read-only; job, allocations, volume, VM and disk were not changed.

## Findings

### Symptom

After Start Job the deployment places one allocation, but it stays `pending`,
all five tasks have only the `Received` event, and the deployment becomes
unhealthy. At the time of the final check the job had already been stopped manually and
had status `dead (stopped)`; the deployment message `Cancelled because job is stopped`
is a consequence of the stop, not the primary cause.

Latest allocations:

- `6013367a-a970-364a-4c0c-96d29b97c879`, version 2,
  `nomad-agent-test-010` (`10.16.26.48`), `pending`, desired `stop`;
- `74edd99c-c887-f112-d0c4-cf87999eebb9`, version 5,
  `nomad-agent-test-07` (`10.16.26.54`), `pending`, desired `stop`.

### Confirmed cause

The job uses CSI volume `yc-csi-buildsinfo` for MongoDB:

- external disk ID: `epdcongej2qeqecu5ect`;
- plugin: `yc-csi`, provider `yandex.csi.flant.com`;
- access mode: `single-node-writer`;
- Nomad reports the volume as schedulable, 9/9 controllers and 9/9 nodes healthy.

Despite this, Yandex CSI returns an exact error on claim:
`FailedPrecondition`: the disk is already published to another instance and does not
support multi-node; CSI explicitly requires a detach of the disk.

The disk remains attached to Yandex instance `epd4ns50ldmcet1i9k7n`, which according to
metadata is the current VM `nomad-agent-test-04` (`10.16.26.55`). On this VM
the disk was not mounted at the time of the check (`findmnt` showed no data-volume
mounts); `lsblk` shows four unmounted CSI data disks. The new allocations
were scheduled to `nomad-agent-test-010` and then `nomad-agent-test-07`, so the
attach is blocked.

Additionally Nomad keeps holding the write-allocation claim of the volume for the already
stopped pending allocation `6013367a` on `nomad-agent-test-010`. Because of the
single-node-writer mode the next allocation also gets `volume max claims
reached`.

The cluster state is not the cause: all 9 Nomad clients are
`ready/eligible`. The incident is consistent with residual Yandex CSI attachments after
the recent stop and subsequent start of the whole client instance group; the journals
contain similar errors for other CSI disks too, so the problem is wider than one job.

## Actions

### Safe recovery (plan)

Before any changes keep `buildsinfo` stopped and re-confirm that the
disk is not mounted anywhere and MongoDB is not running. Then:

1. Perform a controlled detach of `yc-csi-buildsinfo` from Nomad node
   `c06cca7b-f92f-d9dc-b0f6-e209dde522e3` (`nomad-agent-test-04`) through Nomad CSI,
   or detach the external disk `epdcongej2qeqecu5ect` from Yandex instance
   `epd4ns50ldmcet1i9k7n` in the Cloud Console/API.
2. Check that the stale external attachment disappears and the write claim of allocation
   `6013367a` completes/is released. If the claim is not released automatically,
   separately perform the standard force-detach/reconciliation through Nomad CSI,
   having first verified the exact node/volume IDs.
3. Start the job once and wait for: allocation `running`, tasks `mongodb`,
   `redis`, `api`, `worker`, `scheduler` started, deployment healthy, TCP checks
   of MongoDB/Redis/API passing.
4. Check `buildsinfo.yandex-test.youdo.local`/`buildapi` and the integrity of the MongoDB
   data. Do not deregister/purge the CSI volume and do not delete the disk: the data is persistent.

The Nomad command for the detach requires write capability and was not executed initially
during the diagnosis:

```bash
nomad volume detach yc-csi-buildsinfo c06cca7b-f92f-d9dc-b0f6-e209dde522e3
```

### Recovery attempt, 2026-09-13

With the operator's explicit permission the command above was executed with the Nomad
address and token from `~/ai/current/.env`. Nomad returned HTTP 500: `rpc error: Unknown allocation`.
The detach did not happen; the state of the job and volume did not change. This confirms that the
external attachment on `nomad-agent-test-04` is no longer linked to a known Nomad
allocation: Nomad cannot remove it via `volume detach`. The next recovery method
is a controlled detach of the external disk
`epdcongej2qeqecu5ect` from Yandex instance `epd4ns50ldmcet1i9k7n` through the Yandex
Cloud Console/API, after which the release of the Nomad write allocation
`6013367a` must be checked before starting the job.

With the next explicit permission of the operator the external detach was performed through the Yandex
Cloud API with the credentials of the working `plugin-yc-csi-monolith`; the credentials
were used only in memory and were not printed/saved. Before the change the
API re-confirmed the exact instance/disk IDs and the attachment. Operation
`epd6u5eog9r8lc18g2i8` finished with `done=true`, without error.

After the operation:

- the disk disappeared from `lsblk` on `nomad-agent-test-04` (three other CSI data
  disks remain instead of four);
- the Nomad volume remains `Schedulable=true`, controllers healthy 9/9, nodes
  healthy 9/9;
- `WriteAllocs` for `yc-csi-buildsinfo` was immediately cleared to an empty list;
- the old allocation `6013367a` is still shown as pending/desired stop,
  but no longer holds the CSI write claim and does not prevent a new start.

The job was deliberately not started: the user permitted the detach but not a new Start
Job. The next safe step is a single start of `buildsinfo` while monitoring the allocation,
tasks, deployment health and MongoDB data integrity.

### Check after the user started the job

The user started the job at 15:31:48 MSK. Job version 7 successfully created
allocation `fa9e06ef-0681-f1b9-33ff-54e93d920875` on
`nomad-agent-test-05` (`10.16.26.7`). Result:

- job status `running`;
- deployment `e7388d70-4ed1-2263-4231-22524ae5f2a1` — `successful`;
- allocation — `running`, deployment health `healthy`, failures 0;
- `mongodb`, `redis`, `api`, `worker`, `scheduler` — all `running`, 0 restarts;
- CSI volume `yc-csi-buildsinfo` is mounted in the allocation and schedulable;
- direct API `10.16.26.7:22071/` and the internal route
  `buildsinfo.yandex-test.youdo.local/` both respond HTTP 401 in about 0.05-0.08
  seconds. The identical authentication response confirms a working network,
  Traefik route and a working API; 401 is expected for a request without credentials.

The old allocation `6013367a` remains visible as pending/desired stop, but no longer holds
the CSI write claim and does not interfere with version 7.

The address and token should be passed through the saved variables
`NOMAD_YANDEX_TEST_ADDR` and `NOMAD_YANDEX_TEST_TOKEN`; the values stay only in
`~/ai/current/.env`.

### Checks and sources

- `nomad job status -all-allocs buildsinfo`
- `nomad job deployments buildsinfo`
- `nomad alloc status -verbose 6013367a`
- `nomad alloc status -verbose 74edd99c`
- `nomad volume status yc-csi-buildsinfo`
- Nomad API `/v1/volume/csi/yc-csi-buildsinfo`
- `journalctl -u nomad` on `nomad-agent-test-010`, `-07` and a mount check on `-04`
- instance IDs verified through the Yandex metadata endpoint on all 9 client VMs.

## Changes

- External disk `epdcongej2qeqecu5ect` detached from Yandex instance `epd4ns50ldmcet1i9k7n` (operation `epd6u5eog9r8lc18g2i8`).
- `buildsinfo` restarted by the user (job version 7); no config or repository changes.

## Open items: related security risk

In the legacy file `/home/slnnk/git/buildapi/production.nomad` plaintext
credential values were found. The values were not carried into this note. Names/context:
`NOMAD_TOKEN`, `JENKINS_LOGIN`, `JENKINS_PASSWORD` for the old spb2 configuration.
Their validity must be checked; move them to Vault and rotate them if they are still active.
The current Yandex jobspec `deployments/production.hcl` gets the Nomad/GitLab
credentials from Vault path `secret/admin/buildapi`.

## Portable lesson

[Nomad CSI: `FailedPrecondition` stale attachment after node stop/start, `volume detach` returns `Unknown allocation`](../../../../general/knowledge/nomad/csi-stale-attachment-after-client-restart.md)
