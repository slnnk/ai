---
system: nomad
status: verified
checked: 2026-09-13
tags: [nomad, csi, volume, FailedPrecondition, single-node-writer, detach, cloud-disk]
---
# Nomad CSI: `FailedPrecondition` stale disk attachment after clients were stopped and started

## Symptom

After a Nomad client fleet was stopped and started (VM stop/start, instance group
stop, mass reboot), a job with a CSI volume (`access_mode = "single-node-writer"`)
places an allocation that never leaves `pending`; all tasks show only the `Received`
event and the deployment goes unhealthy. `nomad volume status <vol>` reports the volume as
`Schedulable`, controllers and nodes healthy. The client journal shows the CSI controller
rejecting the publish with `FailedPrecondition`: the disk is already published to another
instance and does not support multi-node attachment; detach required.

Follow-up symptoms:

- a later allocation fails with `volume max claims reached` because Nomad still records a
  write claim for the old, stopped `pending` allocation;
- on the node named by the cloud API the disk is visible in `lsblk` but not mounted
  (`findmnt` shows nothing);
- `nomad volume detach <vol> <node-id>` returns HTTP 500
  `rpc error: Unknown allocation`.

## Cause

The cloud disk is attached at the infrastructure level to the VM where the volume was
last mounted. When the client went away abruptly, the CSI node plugin never ran
`NodeUnstage`/`ControllerUnpublish`, so the cloud still lists the attachment while Nomad's
own claim bookkeeping refers to an allocation that no longer exists on any client. Nomad
cannot resolve the attachment through its normal path because `volume detach` needs a
known allocation/node claim to drive the CSI RPCs, and that claim is gone. The volume
looks healthy to Nomad (plugin health is about the plugin, not the disk), so the scheduler
keeps placing the allocation on other nodes where attach is impossible.

## Fix

Do this only after confirming the disk is not mounted anywhere and the stateful process
(database) is not running; the data on the disk is persistent and must not be purged.

1. Try Nomad first:

   ```bash
   nomad volume status <volume-id>          # note Node ID(s) in Allocations/claims
   nomad volume detach <volume-id> <node-id>
   ```

   If it fails with `Unknown allocation`, Nomad has no claim to act on.
2. Detach at the cloud layer (console, CLI or API): detach `<external disk id>` from
   `<instance id>`. Verify the instance/disk IDs through the cloud API and the node's
   metadata endpoint before acting, and confirm the disk disappears from `lsblk` on that
   node.
3. Re-check `nomad volume status <volume-id>`: the stale write claim (`Write Allocs`) is
   normally cleared immediately once the external attachment is gone. If it is not, run the
   volume's reconciliation/force detach as documented for your Nomad version, again with
   verified IDs.
4. Start the job once and watch the allocation reach `running`, the deployment become
   healthy and the data survive (application-level check).

Prevention: drain clients (`nomad node drain -enable`) before stopping them so CSI volumes
are unmounted and unpublished cleanly; after any ungraceful fleet stop, expect this on
every single-node-writer volume and check the client journals for `FailedPrecondition`.

## Limits

- Verified with Nomad 1.5.x and a cloud CSI driver for block disks; the exact error text
  comes from the driver, but the mechanism (cloud attachment outlives Nomad's claim) is
  generic.
- `nomad volume deregister -force` / re-register also clears claims but loses volume
  metadata and does not fix the cloud-side attachment; prefer the cloud detach.
- Do not run `nomad system gc` just to clean this up; it affects all terminal objects.
