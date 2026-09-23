---
system: nomad-test
status: verified
checked: 2026-09-11
tags: [nomad, consul, instance-group, stop-pilot, cost, yandex-cloud, node-gc]
---
# Nomad yandex-test: runtime snapshot after stopping the client instance group

## Task

Check the behaviour of the cluster during the resource-optimization pilot after the group of
client VMs was stopped manually. This is the runtime snapshot of the pilot planned in
[Nomad test/dev: night shutdown of client nodes](2026-09-09-nomad-test-night-shutdown-cost.md).

## Context

- Check date: 2026-09-11 23:23 MSK
- Environment: Yandex Cloud test, Nomad/Consul `yandex-test`
- Instance group: `nomad-consul-agent-group`
- IaC: `/home/slnnk/git/yandex-tf/test-infra/compute-group-nomad-agent-test.tf`
- Goal: check the behaviour of the cluster during the resource-optimization pilot after a manual stop of the client VM group.
- All checks performed were read-only; VMs, jobs, allocations, Nomad, Consul and nginx were not changed.

## Findings: confirmed state

- The current Terraform configuration of the group defines 9 clients with 16 vCPU / 80 GiB RAM each; the earlier number of 10 from the sizing snapshot of 2026-08-11 is outdated.
- During the check the stop propagated gradually: first Nomad showed 7 clients `down` and 2 `ready`, then all 9 clients became `down`.
- Final consistent snapshot from each of the three Nomad servers: 9 registered nodes, 9 `down`, 0 `ready`.
- Nomad control plane is healthy: 3/3 voter servers `alive`/healthy, leader `nomad-consul-master-test-01` (`10.16.26.11`), Autopilot `Healthy=true`, `FailureTolerance=1`; Raft term/index match on all three servers.
- Job snapshot: 382 jobs total; service — 330 `pending` and 47 `dead`; system — 3 with job-level status `running`; batch — 1 `pending` and 1 with job-level status `running`. The status of system/batch jobs does not mean running allocations when there are no clients.
- Allocation snapshot after the stop: 475 allocations, of which 473 `lost` with desired status `stop` and 2 old `failed` allocations of job `similar-tasks` with desired status `run`; there are no running allocations.
- Scheduler snapshot: 1237 evaluations, of which 331 `blocked`, 868 `complete`, 38 `canceled`; the blocked evaluations belong to 331 jobs. The main current reason is the absence of available client nodes.
- Consul DNS `proxy.service.yandex-test.consul` returns no A records after the clients were stopped. `nomad.service.yandex-test.consul` keeps returning the three master IPs: `10.16.26.11`, `.12`, `.13`.

## Interpretation and risks

- Control plane and job definitions are preserved, but the data plane is completely unavailable; the test applications are, as expected, in a full outage.
- After the instance group is started one has to wait not only for the VM status but for all 9 Nomad clients to be `ready`/`eligible`, for drivers and Consul registrations to recover, and then for the 331 blocked evaluations to disappear and allocations to start.
- After the clients return, check the system jobs `alloy`, `jaeger-agent`, `plugin-yc-csi-monolith`, the service job `traefik2-service`, CSI/host-volume workloads, pending/failed allocations and application health checks.
- Because of the known static resolution of the Consul-backed upstream in nginx, after the membership of `proxy.service` changes the upstream addresses on the balancer must be checked. If needed, perform a separate controlled `nginx -t` and graceful reload; no reload was performed as part of this snapshot. See [Yandex test nginx balancers](../systems/automation-services/yandex-test-nginx.md).
- It was not possible to check the runtime status of the instance group directly through `yc`: the local OAuth token is not supported by the current IAM token exchange; this is a local CLI authentication problem (see [yc CLI auth recovery](2026-09-13-workstation-yc-cli-auth-recovery.md)), and the fact of the stop was confirmed independently through Nomad and Consul DNS.

## Actions: read-only checks used

- Nomad: `/v1/agent/members`, `/v1/operator/autopilot/health`, `/v1/nodes?stale=false`, `/v1/jobs?stale=false`, `/v1/allocations?stale=false`, `/v1/evaluations?stale=false`.
- CLI: `nomad node status -verbose`, `nomad status`.
- DNS: `dig @10.16.26.11 proxy.service.yandex-test.consul A` and `nomad.service.yandex-test.consul A`.

## Open items: next control snapshot after power-on

1. Make sure all 9 VMs of the group are running and Nomad shows 9/9 nodes `ready` and `eligible`.
2. Check Nomad Autopilot and leader/quorum; separately check Consul quorum when suitable ACL access is available.
3. Check the dynamics of jobs/evaluations/allocations: blocked should tend to zero, service jobs should return to `running`, lost allocations should be replaced by new running allocations.
4. Check Consul DNS `proxy.service` and the actual nginx upstream addresses, then the critical test URLs.
5. Check CSI/host-volume workloads and batch/periodic jobs that may have been interrupted or missed their launch window.

## Expected node GC behaviour over the weekend (hypothesis)

- On the live Nomad servers the parameter `server.node_gc_threshold` is not set. For Nomad 1.5.3 the default `24h` applies; server GC checks terminal nodes periodically (the documented interval is 5 minutes). Therefore, when stopped from Thursday/Friday until Monday, the records of all 9 `down` clients will most likely disappear from `nomad node status` even before the VMs are started.
- Disappearance of the record from server state does not prevent the client from registering later. On start the Nomad client registers again and starts heartbeating; the scheduler creates new allocations for pending service/system jobs.
- An essential difference from the previously removed `nomad-agent-test-09`: shrinking the instance group deleted the VM, whereas the stop operation preserves the VM and its boot disk. The current client configuration uses a persistent `data_dir = /var/lib/nomad`; as long as the disk is intact the client state/identity is preserved.
- Even if the server has already garbage-collected the node record, the preserved VM should register again. A new server-side lifecycle / new allocations are possible; the old `lost` allocations should not be expected to continue as processes.
- Main conditions for a successful return: the VM must not be deleted/recreated, `/var/lib/nomad` must not be wiped or corrupted, systemd `nomad` and the local Consul must start, and network/DNS and access to the Nomad servers `10.16.26.11-13:4647` must be available.
- If scale-to-zero/recreate is used instead of stop, the disk or client state may disappear and the client will receive a new identity. It will usually still be able to register as a new node, but host-volume/node-specific state and local allocation data will require a separate check.

## Portable lesson

none
