---
system: nomad-test
status: hypothesis
checked: 2026-09-09
tags: [plan, nomad, consul, cost, instance-group, night-shutdown, yandex-cloud, terraform]
---
# Nomad test/dev: night shutdown of client nodes to reduce costs

## Task

Feasibility study: can the Yandex Cloud test/dev Nomad client nodes be stopped at night to
save money, and what is the safe way to do it.

## Context

- Research date: 2026-09-09
- Scope: Yandex Cloud test/dev, Nomad and Consul
- IaC: `/home/slnnk/git/yandex-tf/test-infra`
- Status: feasibility confirmed; the runtime pilot of stopping the client group started on 2026-09-11. The snapshot after the stop is recorded in [2026-09-11 agent group stop pilot](2026-09-11-nomad-test-agent-group-stop-pilot.md); verification of the recovery after start-up is still required.

## Findings

### Currently known topology

According to Terraform at the check date the roles are separated:

- `yandex_compute_instance_group.nomad_consul_agent_group` in
  `test-infra/compute-group-nomad-agent-test.tf`: 9 Nomad client VMs,
  each `standard-v3`, 16 vCPU, 80 GiB RAM, boot disk 93 GiB
  `network-ssd-nonreplicated`; instance group
  `nomad-consul-agent-group`.
- `yandex_compute_instance_group.nomad_consul_master_group` in
  `test-infra/compute-group-nomad-master-test.tf`: 3 Nomad/Consul master VMs,
  each 2 vCPU, 8 GiB RAM, boot disk 93 GiB
  `network-ssd-nonreplicated`; instance group
  `nomad-consul-master-group`, deletion protection enabled.
- `test-infra/ansible-hosts.tf` confirms: the agent group has
  `nomad_client=true`, `nomad_server=false`; the master group has
  `nomad_client=false`, `nomad_server=true`, `consul_server=true`.

### Conclusion

The main safe candidate for the night shutdown is the whole instance group
`nomad-consul-agent-group`. The three master nodes should be kept running so that
Nomad and Consul keep quorum, serve the control plane, periodic evaluations and the
service catalog.

Registered Nomad jobs are stored in the Raft state of the server nodes and do not
disappear when the clients are switched off. After the clients are lost, allocations will
be lost/pending depending on the job spec and the Nomad version. Service allocations for
which there is no suitable capacity remain unplaced and are scheduled once eligible/ready
clients appear. System jobs are re-evaluated when a client registers or transitions to
ready. A registered batch job that completed successfully does not restart by itself just
because the nodes are powered on; an interrupted batch allocation depends on the
restart/reschedule/disconnect policy. Periodic jobs require a separate check of the night
window and of the `prohibit_overlap` policy.

Yandex Cloud supports stopping an instance group as a whole. The VMs keep existing, the
compute resources of stopped VMs are not billed, while the disks continue to be billed. For
the current group this is preferable to changing `fixed_scale.size` to zero every day: the
VMs and client-local disks are preserved, start-up is faster and there is less risk of
losing local state. Scale-to-zero deletes the VMs; before such an option the client-local
data must be considered disposable, or snapshots/external storage must exist.

### Limitations and risks

- At night there will be a full outage of all workloads on the switched-off clients. The
  preservation of the job definitions itself does not mean the applications are available.
- Before the pilot, inventory host volumes, bind mounts, `ephemeral_disk`, Docker volumes,
  CSI node/controller plugins and databases on client-local disks.
- Do not use a drain of all clients as a mandatory step: drain is meant for migration and,
  when no remaining capacity exists, can hang until the deadline. For a planned full outage
  it is better to stop the applications/clients in a controlled way, having first forbidden
  new deploys and batch jobs.
- When the clients simply disappear, Nomad applies `disconnect`, node-lost and reschedule
  semantics. Before the pilot check the Nomad version and the jobs with `disconnect`,
  non-standard `reschedule`, singleton workloads and limited attempts.
- The Consul masters stay on. If Consul clients live only on the VMs being switched off,
  the service registrations will disappear for the night and be restored after the
  workloads start; this is expected but requires a check of DNS/ingress behaviour.
- The morning start must wait for the readiness of the Nomad clients, drivers/CNI/CSI and
  then check pending allocations, rather than treating the VM status as sufficient.
- Two of the three master nodes must never be switched off at the same time: Nomad and
  Consul would lose quorum. A full stop of the control plane can be considered only as a
  separate recovery-oriented scenario with durable disks, a correct start order and tested
  snapshots; the saving from three small master VMs is substantially smaller.

## Recommended pilot

1. Choose one agreed night window without CI deploys and batch/autotest runs.
2. Save a Nomad snapshot to external durable storage and check that there are three
   server peers and a leader; separately check the health of the Consul quorum.
3. Take an inventory of jobs/allocations and single out stateful/local-storage workloads.
4. Shut down the workloads or the Nomad agent on the clients cleanly and stop the whole
   `nomad-consul-agent-group` through the Yandex Instance Groups API/CLI.
5. In the morning start the same group, wait for all 9 VMs, Nomad node status `ready` and
   eligibility `eligible`, then check queued/pending/failed/lost allocations, system jobs,
   Consul registrations and application health checks.
6. Only after a successful pilot automate the schedule with preflight, a block on night CI
   runs, timeout, alert and an emergency manual command.

## Open items: data still to collect

- The actual Nomad/Consul version and agent configuration.
- The real list of jobs by type and their `disconnect`, `restart`, `reschedule`,
  `migrate`, periodic and parameterized parameters.
- The host/CSI volumes in use and the location of critical data.
- The acceptable morning recovery time and the exact night window.
- The current cost of the nine client VMs and disks to calculate the expected saving.

## Official sources checked on 2026-09-09

- HashiCorp Nomad: consensus protocol, scheduler types, job scheduling,
  disconnect block, node drain, allocation filesystems, snapshots.
- Yandex Cloud: stopping an instance group, stopping/pausing groups, Compute
  Cloud pricing.

## Portable lesson

none
