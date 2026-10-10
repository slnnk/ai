---
system: yandex-cloud
status: verified
checked: 2026-10-09
tags: [kubernetes, recovery, migration]
---
# DevOps-888: check original cluster recovery by cross-zone nodes

## Summary
Original kube-test is zonal with one master in ru-central1-b, not regional. Cloud reports RUNNING/HEALTHY; four worker VMs are RUNNING_ACTUAL in b. Private Kubernetes API readyz and node-list GETs timed out from this workstation using an existing matching kubeconfig. Cloud status does not establish Kubernetes readiness. No infrastructure changes made.

## Task and context
User supplied a Yandex incident update stating regional master components can now be relocated from ru-central1-b and recommends new node groups in other zones. Investigated applicability to original cluster catd03r096n9ih2qahac before changing the separate recovery route published in MR !235.

## Actions and findings
Bounded read-only YC CLI queries using existing terraform-k8s-test profile confirm master.zonal_master zone_id ru-central1-b, etcd_cluster_size1, location subnet e2lk85dmf4e93a2emoe7, Kubernetes1.34, private endpoint https://10.16.26.3. Node group catd0sn7d33n3rrgivh6 is RUNNING, allocation b only, instance group cl1e8jt27j03mj4g8q0g, autoscaling1-10. Its four VMs report RUNNING_ACTUAL in b. Existing CI kubeconfig explicitly matching this endpoint was used for bounded readyz/nodes reads; both timed out. Credentials and full object/config contents were not copied to notes.

## Interpretation and limits
The supplied incident announcement applies to regional masters and does not directly establish a supported relocation operation for this single zonal master. API timeouts are observations from this workstation only; private routing/VPN and control-plane availability must be separated by checking from an established runner/bastion route. No node Ready, pod health, PV or data availability claim is supported by the cloud flags. Workload/PV inventory was unavailable in these checks.

## Recovery options
If Kubernetes API works from the normal management network, prepare a separately reviewed node group in ru-central1-a with existing shared-VPC subnet e9b32eqch1la7rq0ed6e, matching original cluster version1.34. Check IAM for the original cluster SA to use the subnet in the other folder, egress/security groups, quotas, pod scheduling constraints, PDBs, PVC/PV zone affinity and load balancer routing. Existing manifests/secrets/controllers remain in that same cluster, but disks/data in b require independent migration/recovery. Original master remains in b unless Yandex confirms a supported migration/recovery operation.

If API remains unavailable from the established route, ask Yandex support about zonal-master recovery/relocation for exact cluster ID; adding workers alone does not fix an unavailable control plane. Keep the separate yc-a-k8s-dev1.35/fresh-state recovery route as an alternative; its cluster creation does not restore original workloads/data automatically. Existing checkout test-k8s describes the separate recovery backend, so any original-cluster change must be reconciled with its original terraform/yandex-test-k8s state and reviewed separately, avoiding ownership confusion.

## Sources
- [Yandex migration guide](https://yandex.cloud/ru/docs/managed-kubernetes/tutorials/migration-to-an-availability-zone): new groups and gradual migration; scheduling constraints; stateful disk snapshot/restore.
- [YC cluster update CLI](https://yandex.cloud/en/docs/managed-kubernetes/cli-ref/v0/cluster/update): master-location described for regional master locations.
- [Incident page](https://status.yandex.cloud/ru/incidents/2092): browser returned a JavaScript shell; exact supplied update attributed to the user, not independently retrieved.

## Changes and approvals
Read-only investigation and KB bookkeeping only. No repo edits, cloud operations, node-group creation, master update, Kubernetes mutation, Terraform state change, deployment or MR change. Subsequent concrete external actions require their own approval under the global instructions. Follow-up work is tracked in ~/ai/TODO.md.
