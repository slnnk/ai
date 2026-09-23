---
system: nomad-test
status: verified
checked: 2026-09-13
tags: [nomad, terraform, yandex-cloud, instance-group, scale-down, capacity, mr-218, job-3138137]
---
# Yandex test Nomad agents: scale-down analysis 9 -> 8

## Task

Review the Terraform MR that reduces the `nomad-consul-agent-group` from 9 to 8 clients,
assess the risk of the apply, and record the live capacity and scheduler state before and
after the scale-down (which then continued to 7).

## Context

- Check date: 2026-09-13, Europe/Moscow
- Repository: `/home/slnnk/git/yandex-tf`
- Safe origin: `git@gitlab.youdo.sg:sysadmins/yandex/yandex-tf.git`
- Merge request pipeline: `138479`, ref `refs/merge-requests/218/head`
- Plan job: `3138137` (`plan:test-infra`), commit `45a98a03519ac895f888dddb9af357bd0639d878` (`decrease nomad clients`)
- Resource: `yandex_compute_instance_group.nomad_consul_agent_group`, Yandex Cloud group ID `cl1bk0eipvmmgiiju2a4`, name `nomad-consul-agent-group`

## Findings

### Verified facts

- The commit changes only `test-infra/compute-group-nomad-agent-test.tf`: `scale_policy.fixed_scale.size` from 9 to 8.
- Terraform plan in job `3138137`: `0 to add, 1 to change, 0 to destroy`; the only change is an in-place update of the group, `fixed_scale.size = 9 -> 8`.
- `instance_template`, `allocation_policy` and `deploy_policy` do not change in the plan. Therefore there is no reason in this plan for a rolling restart/recreate of the remaining VMs; Instance Groups should delete one surplus VM and keep the rest.
- The name of the VM to be deleted cannot be considered known. According to the Yandex Cloud documentation, when the target size is reduced, VMs that failed the health check are deleted first. Historically the previous reduction of this group deleted `nomad-agent-test-09` while `nomad-agent-test-010` remained, so the rule "the highest index gets deleted" is not confirmed here.
- Current `deploy_policy`: `max_unavailable = 1`, `max_expansion = 0`, `max_creating = 8`; the strategy is not set explicitly, the Yandex Cloud default is `PROACTIVE`. `max_unavailable = 1` limits the number of simultaneously unavailable VMs, but by itself does not limit the total number of VMs being updated if the instance template changes in the future.

### CI peculiarity and risk

- `apply:test-infra` does not use the saved plan from job `3138137`: it runs a new `terraform apply -auto-approve`, then repeats it a second time because of a workaround for the inventory.
- Therefore job `3138137` reliably describes the state as of 2026-09-13 18:10 MSK but is not a fixed apply artifact. Before a manual apply, check fresh output: only the group size change 9 -> 8 is acceptable; changes to `instance_template` would mean a risk of rolling restart/recreate.
- A local read-only query of the actual state through `yc` was not performed: the saved OAuth profile is rejected by the IAM exchange (`OAuth token ... issued after 2026-06-01 is not supported`). No secrets were saved or printed. See [yc CLI auth recovery](2026-09-13-workstation-yc-cli-auth-recovery.md).

### Operational effect

- Deleting one client VM will destroy its boot disk and the local Nomad client/allocation state. Nomad should reschedule the affected allocations onto the remaining clients if resources are available.
- After the apply check: the composition of the group's VMs, `nomad node status`, lost/pending allocations, blocked evaluations, Consul registrations/DNS and critical workloads. Related runtime context: [2026-09-11 agent group stop pilot](2026-09-11-nomad-test-agent-group-stop-pilot.md).

### Live capacity after the scale-down (2026-09-13, about 18:40 MSK)

- In Nomad: 8 clients `ready` and the deleted `nomad-agent-test-010` in `down`; of the ready clients only 7 are `eligible`, because `nomad-agent-test-08` remains `ineligible` and has no allocations.
- Each VM provides Nomad roughly 31,984 MHz CPU and 78 GiB RAM.
- Actual host utilization across the eight ready VMs at the snapshot: about 41,854 MHz CPU of 255,872 (16.4%) and 209.7 GiB RAM of 624 GiB (33.6%). This is a point-in-time snapshot, not a historical peak.
- Scheduler allocations on the seven eligible VMs reserve about 200,600 MHz CPU of 223,888 (89.6%) and 427.8 GiB RAM of 546 GiB (78.4%). The scheduler has `MemoryOversubscriptionEnabled=true`, algorithm `binpack`; preemption for system/service/batch is disabled.
- `nomad-agent-test-04` holds only three system allocations (`alloy`, `jaeger-agent`, `plugin-yc-csi-monolith`): 700 MHz CPU and 868 MiB RAM. `nomad-agent-test-08` is completely empty.
- Practical conclusion: one more VM can be removed safely — the empty `nomad-agent-test-08`; the number of schedulable clients will stay at 7. Technically `nomad-agent-test-04` could also be removed without migrating service allocations, but after that the reservations of the remaining six VMs would amount to about 104% of their total CPU and 91% of RAM. That would leave almost zero scheduler/failover/deploy headroom, so 6 VMs cannot be considered a safe permanent configuration without revising resource requests and observing peaks.
- A blind scale-down by `fixed_scale.size` alone does not guarantee that the empty/light VM is chosen. To go down to 7, specifically `nomad-agent-test-08` should be removed in a controlled way, or an unambiguous instance choice must be ensured beforehand; before any further reduction a drain pilot of the chosen VM and a check of queued/blocked allocations are needed.

### Actual result after the apply

- The user confirmed: only `nomad-agent-test-010` was deleted; the other VMs were not restarted.
- Read-only Nomad snapshot after the deletion: `nomad-agent-test-010` has ID `24384c4e-81e0-5f09-32fa-76fb471e5bc7`, status `down`, scheduling eligibility `ineligible`, heartbeat missed at `2026-09-13 18:23:31 MSK`.
- Before deletion the node was taken out correctly: the events contain `Node marked as ineligible`, setting of the drain strategy and `Node drain complete`. CSI volumes `test11/test13/test14/test15-yc-csi-es` were unmounted successfully before the VM was deleted.
- There are no active resources on the old node; the remaining allocations have `Desired=stop` and client status `lost` or `failed`. Manual node cleanup is not needed: with `server.node_gc_threshold` not overridden, Nomad removes the terminal node automatically after roughly 24 hours (the GC scan usually runs every 5 minutes).
- Do not run `nomad system gc` just for this record: the command affects all terminal objects in the cluster. A targeted purge is also unnecessary as long as the stale node does not interfere with operations.
- Separately discovered: of the eight `ready` clients `nomad-agent-test-08` (`e1f55790-5783-3a1f-9199-faebbcdeb0c0`) remains `ineligible` and has 0 allocations; its drain completed at `2026-09-13 15:38:18 MSK`. Therefore the actual schedulable capacity right now is 7 clients. If this is not an intentional cordon, after confirmation eligibility should be restored with `nomad node eligibility -enable e1f55790-5783-3a1f-9199-faebbcdeb0c0`.
- System jobs at the snapshot: `jaeger-agent` — 7 running, `plugin-yc-csi-monolith` — 7 running, `alloy` — 6 running + 1 starting. This is consistent with seven eligible nodes. Elasticsearch jobs `test11/test13/test14/test15` have job status `running`.
- The queue contains one delayed reschedule job `similar-tasks`; it appeared before the deletion of `010` and does not look like a consequence of the scale-down. The only blocked eval belongs to the old periodic run `jaeger-index-cleaner/periodic-1730246400`.

### Actual result of the scale-down 8 -> 7

- The user confirmed the deletion of `nomad-agent-test-08`, which before the operation was `ineligible` and had no allocations.
- In the first snapshot right after the deletion Nomad still showed `08` as `ready/ineligible`: the client's heartbeat TTL had not yet expired. A normal transition to `down` and then automatic node GC is expected.
- System jobs are already in a consistent state for seven working clients: `alloy` — 7 running, `jaeger-agent` — 7 running, `plugin-yc-csi-monolith` — 7 running.
- No new blocked/pending evaluations caused by the deletion were found. The pre-existing delayed reschedule `similar-tasks` and the old blocked periodic `jaeger-index-cleaner` remain.
- After the deletion of `08` the target size of the group is 7 VMs. Further blind scale-down is not recommended: next time Yandex Cloud may pick a loaded client; the separate candidate `04` is almost empty, but reducing to 6 leaves insufficient scheduler headroom by reservations.

### Historical observed metrics from VictoriaMetrics

- Source found on 2026-09-13: Alloy/cAdvisor -> `vmagent.dev.youdo.corp` -> VictoriaMetrics; query endpoint `http://vmselect.dev.youdo.corp/select/0/prometheus/api/v1`.
- Over the available window of up to 7 days, the sum over Nomad containers: CPU average 15.37 cores, P95 22.65, max 53.45; working-set RAM average 156.6 GiB, P95 263.5 GiB, max 272.0 GiB.
- The data contains scrape gaps, so peaks/P95 are more useful than the average. By observed usage six VMs have a large physical margin, however the Nomad reservations after moving to six exceed the total CPU capacity; the decision about the next scale-down requires reconciling resource requests and a controlled drain, not only a cAdvisor estimate.
- Detailed map and PromQL: `~/ai/current/knowledge/log/2026-09-13-monitoring-yandex-test-nomad-container-metrics.md` (migrated from the old monitoring note; verify the final location).

### Current scheduler problems (2026-09-13, about 20:45 MSK)

- `jaeger-index-cleaner/periodic-1730246400`: job `pending`, one queued allocation; evaluation `e461d013` is `blocked` with reason `No nodes were eligible for evaluation`. The job requires DC `spb2`, while the available clients belong to `yandex-test`. This is an old periodic child created on 2024-10-30.
- `http-headers-viewer`: the job is formally `running`, but allocation `6bde1ede` (`web`, node `nomad-agent-test-07`) has `Desired=run`, `ClientStatus=failed`. Task `app` exhausted 3 restart attempts; Docker cannot bind `10.16.26.54:21834` because the port is already in use. The second of the two allocations works; the latest deployment failed, healthy 1/2.
- `similar-tasks`: the job is formally `running`, but allocation `0e35e0b6` of group `indexer` went from `pending` to `failed`; the prestart task `create-index` exits with exit code 1 and goes into delayed reschedule. Evaluation `9347f4eb` has status `pending`, reason `created for delayed rescheduling`. The other groups `elasticsearch` and `similar-tasks` are working.
- At the final snapshot there were no other allocations with `DesiredStatus=run` and a `ClientStatus` other than `running`.
- The API also holds 160 latest deployments with status `failed`/unhealthy, most with a `progress deadline` around the time of the scale-down. A deployment status is a stored rollout result and by itself does not prove a current breakage; therefore these records are not included in the main current list without a check of live allocation/service health.

#### Dead jobs and terminal allocations in the same snapshot

- The Nomad API returned 50 jobs with status `dead`; all in namespace `default`, type `service`. Full list: `broadcast-test4`, `cerberus2-test11`, `cerberus2-test13`, `houston-hub`, `youdo-business-landings-test14`, `youdo-business-landings-test7`, `youdo-business-mobile-id-test15`, `youdo-business-sber-proxy-test11`, `youdo-business-test`, `youdo-business-test1`, `youdo-business-test3`, `youdo-business-test5`, `youdo-business-test6`, `youdo-business-tickets-test`, `youdo-business-tickets-test14`, `youdo-business-tkb-proxy-test`, `youdo-business-tochka-proxy-test`, `youdo-business-tochka-proxy-test13`, `youdo-business-tochka-proxy-test3`, `youdo-business-tochka-proxy-test6`, `youdo-chat-agent-test8`, `youdo-front-landings-test`, `youdo-front-landings-test2`, `youdo-front-landings-test3`, `youdo-front-landings-test4`, `youdo-front-landings-test5`, `youdo-front-landings-test6`, `youdo-front-landings-test7`, `youdo-jivo-bot-test`, `youdo-kitcut-test`, `youdo-notifications-test`, `youdo-notifications-test1`, `youdo-notifications-test10`, `youdo-notifications-test12`, `youdo-notifications-test13`, `youdo-notifications-test15`, `youdo-notifications-test16`, `youdo-notifications-test2`, `youdo-notifications-test3`, `youdo-notifications-test4`, `youdo-notifications-test5`, `youdo-notifications-test6`, `youdo-notifications-test7`, `youdo-notifications-test8`, `youdo-notifications-test9`, `youdo-sms-service-test10`, `youdo-sms-service-test11`, `youdo-sms-service-test13`, `youdo-static-test3`, `youdo-static-test5`.
- 4 more allocations with `DesiredStatus=stop` are visible: `youdo-cryptopro/youdo-cryptopro` allocation `3abc1c6c` on `nomad-agent-test-02` completed successfully after a job update; three previous `similar-tasks/indexer` allocations (`996b7cf0` on `02`, `ba952468` on `04`, `da5bb07c` on `03`) failed and were replaced by delayed reschedule.
- These four terminal allocations require no resources and should disappear through the normal Nomad allocation GC. They matter as the history of the cause of the current `similar-tasks/indexer` restart loop, but are not additional running problem instances.

## Open items

- Confirm whether `nomad-agent-test-08` being `ineligible` was intentional (it was subsequently deleted in the 8 -> 7 step).
- Do not scale below 7 without reconciling resource requests and a controlled drain of the chosen VM.
- Follow up on `http-headers-viewer` port conflict, `similar-tasks/indexer` prestart failure and the stale `spb2` periodic child of `jaeger-index-cleaner`.

## Portable lesson

none
