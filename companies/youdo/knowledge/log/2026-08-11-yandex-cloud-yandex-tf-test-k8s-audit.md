---
system: yandex-cloud
status: verified
checked: 2026-08-11
tags: [terraform, yandex-tf, test-k8s, managed-kubernetes, destroy, terraform-yc-kubernetes, consul-backend]
---
# Yandex Cloud test-k8s: reproducibility check

Date: 2026-08-11 (Europe/Moscow)

## Task

Audit whether the `test-k8s` Terraform root of `yandex-tf` can be applied or reused for a new
deployment; then, after the user confirmed the old cluster must go, prepare and drive the destroy
of the old stopped cluster and record the newly deployed permanent cluster.

## Context and location

- Repository: `/home/slnnk/git/yandex-tf`.
- Terraform root module: `/home/slnnk/git/yandex-tf/test-k8s`.
- State backend: Consul `consul.service.selectel.consul:8500`, DC `selectel`, path `terraform/yandex-test-k8s`, HTTP.
- The Consul token is stored only in `~/ai/current/.env` as `CONSUL_HTTP_TOKEN`; the value is not recorded in the note.
- The Yandex provider uses `/home/slnnk/git/yandex-tf/test-k8s/key.json`; the key contents were not copied.
- The network is taken from folder `net-folder`: network `shared_network`, subnet `subnet-test` in `ru-central1-b`.

## Existing infrastructure

- Cluster: `kube-test-cb0io869`, ID `catvccgqb1dgo5dll6im`.
- At the time of the check the cluster status was `STOPPED`, health `HEALTHY`, master Kubernetes `1.28`, release channel `REGULAR`, no public master IP.
- Node group: `yc-k8s-test-01`, ID `catqvn41v9dpd3240d51`, status `STOPPED`, autoscale min=1/max=3/initial=1, zone `ru-central1-b`.
- The Terraform state contains the cluster and node group, two service accounts, IAM roles/bindings, a KMS key, three security groups and separate SG rules, plus network/folder data sources.

## Actions: checks performed

- `terraform init -reconfigure -input=false -no-color`: successfully connected to Consul and used the provider lock file.
- `terraform validate -no-color`: the configuration is syntactically valid.
- `terraform state list`: the state is readable, existing dependencies are listed.
- `terraform plan -input=false -lock-timeout=30s -detailed-exitcode -no-color`: did not complete because of a module configuration error.
- Through YC CLI with the service-account key, the cluster/node group statuses and `yc managed-kubernetes list-versions` were checked.
- The temporary YC CLI profile `codex-audit` was deleted, the original profile `default` was re-activated.

## Findings and causes

The current Terraform cannot be applied or used for a new deployment without fixes.

1. Plan fails in `.terraform/modules/kube/node_group.tf:33`: `node_groups_defaults` does not contain the key `template_name`. Before the error the plan showed `0 add, 4 change, 0 destroy`.
2. The configuration pins Kubernetes version `1.28` for the master and node group. As of 2026-08-11 the Yandex Cloud API returns the available versions: RAPID/REGULAR — `1.32`, `1.33`, `1.34`, `1.35`; STABLE — `1.32`, `1.33`, `1.34`. A new cluster of version `1.28` cannot be created.
3. The module source is not pinned to a tag/ref: `git::https://github.com/terraform-yc-modules/terraform-yc-kubernetes.git`. Locally installed commit is `c4aa438d7849df497524547267bc147e325439ab` (`1.1.3-2-gc4aa438`), remote HEAD during the check was `5886ea6321f4eb1fecddc3c1e19e5d59a6b895d5`. A fresh init may fetch different code.
4. `terraform fmt -check -diff` fails for `main.tf`, `k8s-cluster.tf`, `terraform.tfvars`.
5. `variables.tf` has a typo in the default zone: `ru-cenral1-a`. Currently `default_zone` is not set in tfvars; the subnet data source actually resolved to `ru-central1-b`, but the default should be fixed.
6. `terraform show -json` does not work with the current state/provider: schema version 0 for `yandex_iam_service_account.master` in state does not match version 1 of the provider. Normal refresh/plan did read the resources.
7. Before the check the working tree already contained a user change in `test-k8s/main.tf`: the Yandex provider constraint was changed from `~> 0.108.0` to `~> 0.169.0`. The audit did not create this change.
8. The original YC CLI profile `default` uses an OAuth credential that the API rejected as unsupported for IAM token exchange. The service-account key from `key.json` works.

## Changes proposed by the plan before the error

- KMS key: description text fix.
- Kubernetes cluster: enabling audit logging.
- Main security group: adding egress for the pod/service CIDR (`172.17.0.0/16`, `172.18.0.0/16`).
- Master whitelist security group: adding egress UDP/123 to NTP and TCP/4443 to metric-server pods.
- There is a state address move for `k8s_nodes` to `k8s_nodes[0]`; the plan showed no deletions.

## Next steps (from the audit)

1. Choose a supported Kubernetes version and plan the upgrade of the existing stopped cluster along an allowed version chain; a direct jump from 1.28 may be forbidden.
2. Pin the module source to a specific tag/commit and check its migration notes.
3. Add `template_name = "{instance_group.id}-{instance.short_id}"` to `node_groups_defaults`, or move to a module version that handles partial defaults correctly.
4. Fix the default zone to `ru-central1-a` (or set the required zone explicitly), run `terraform fmt`.
5. Repeat `init`, `validate`, `plan`; separately check the update plan of the old cluster and the creation plan with an empty state.
6. Before apply, review the new SG egress rules and the enabling of audit logging with the infrastructure owner.

During the audit no apply/start/update was executed and no project files were edited.

## Clarification on deletion

The user confirmed that the old cluster must be deleted before the new deployment.

- Deleting the local `test-k8s` directory does not delete the infrastructure: the working state is located in Consul, and the resources will continue to exist in Yandex Cloud.
- Deleting the Yandex Cloud Folder manually is also not a correct Terraform workflow: the state in Consul would remain with references to deleted objects, and the former `folder_id` would become invalid.
- Normal order: keep the configuration and backend access, first obtain a successful `terraform plan -destroy`, then run an explicitly confirmed `terraform destroy`, verify the absence of managed resources, and only then delete the local directory or state.
- The shared network/subnet/folder are attached through data sources and should not be deleted by `terraform destroy` of this root module. Subject to deletion are the resources created by `module.kube`: cluster, node group, service accounts/IAM bindings, KMS key and security groups/rules.
- The user ran `terraform plan -destroy`: refresh of all resources passed, but the destroy plan confirmably failed with `Missing map element` at `.terraform/modules/kube/node_group.tf:33`, because the passed `node_groups_defaults` has no `template_name`. Before destroy the key must be added to the source `k8s-cluster.tf` and the plan repeated. The destroy itself has not been run yet.

## Prepared destroy plan

- `node_groups_defaults.template_name = "{instance_group.id}-{instance.short_id}"` was added to `/home/slnnk/git/yandex-tf/test-k8s/k8s-cluster.tf`; then the file was processed with `terraform fmt`.
- The saved plan `/tmp/yandex-test-k8s-destroy-20260811.tfplan` was created successfully, permissions `0600`, size 33150 bytes.
- SHA-256 of the plan: `c4a4862faa837f6dbc59d968f2cc248f30eb2539aa1e2ef6efe409f219895b6e`.
- Result: `0 to add, 0 to change, 17 to destroy`.
- All 17 deletions belong to `module.kube`: cluster/node group, service accounts and IAM bindings, KMS key/binding, three security groups and three separate SG rules, plus the Terraform helper resources `random_string` and `time_sleep`.
- The destroy plan does not delete the shared network `shared_network`, subnet `subnet-test` or Yandex Cloud folders.
- The plan was not applied. Apply command from the root module: `terraform apply /tmp/yandex-test-k8s-destroy-20260811.tfplan`.

## Partial application of the destroy plan

The user ran the saved destroy plan. The apply completed partially:

- Deleted `module.kube.yandex_vpc_security_group_rule.k8s_node_ports[0]`, `k8s_node_ssh_access_rule[0]`, `k8s_outgoing_traffic[0]`.
- Deleted `module.kube.yandex_kms_symmetric_key_iam_binding.encrypter_decrypter[0]`.
- Deletion of node group `catqvn41v9dpd3240d51` was not performed: the Yandex API returned `FailedPrecondition: operation is not permitted because the cluster is stopped` (operation `catri1uge7610j8o8af0`).
- The cluster must be started temporarily, wait for status `RUNNING`, then create a new destroy plan from the updated state. The old `/tmp/yandex-test-k8s-destroy-20260811.tfplan` must not be applied again.
- The remaining dependent resources were not deleted in this run. The new plan/state must be checked before continuing.

## Deletion completed

- After starting the stopped cluster the user applied the new `/tmp/yandex-test-k8s-destroy-v2.tfplan`.
- The second apply successfully deleted the remaining 13 resources: node group, Kubernetes cluster, the two remaining security groups and the node security group, KMS key, three folder IAM memberships, two service accounts, `time_sleep` and `random_string`.
- Terraform finished with: `Apply complete! Resources: 0 added, 0 changed, 13 destroyed.` Together with the four objects of the first partial apply, all 17 objects of the original destroy plan were deleted.
- Post-deletion control: `terraform state list` returned no resources; a repeated `terraform plan -destroy` finished with `No changes. No objects need to be destroyed.`
- The shared network/subnet/folders were not deleted. The old binary plan files in `/tmp` must not be applied any more; they can be deleted as sensitive temporary artifacts.

## New permanent cluster deployed

- Cluster `kube-test`, ID `catd03r096n9ih2qahac`: Kubernetes `1.34`, channel `STABLE`, zonal master in `ru-central1-b`, private endpoint, state after creation `RUNNING/HEALTHY`.
- Pod CIDR: `10.128.0.0/16`; Service CIDR: `10.144.0.0/16`. The ranges are set explicitly because the defaults `10.112.0.0/16` and `10.96.0.0/16` are taken by the temporary cluster.
- Node group `kube-test-node-group`, ID `catd0sn7d33n3rrgivh6`: `standard-v2`, 8 vCPU, 56 GiB RAM, non-replicated SSD 93 GiB, autoscale min/initial/max `1/1/10`.
- The requested 50 GiB is impossible on `standard-v2` with 8 vCPU: the provider allows an 8 GiB step. 56 GiB was chosen so as not to reduce the ordered capacity.
- Quota `vpc.subnets.count` was initially `11/12`; the user raised the limit to 15, after which the cluster successfully reserved two service subnets.
- During bootstrap the Cluster Autoscaler grew the group from 1 to 2 nodes: pod `calico-typha` temporarily could not be placed because of an occupied host port. Event: `TriggeredScaleUp`, `1->2 (max: 10)`. This is scheduling-based scaling, not a 15% actual-utilization threshold.
- The automatically created ConfigMap `kube-system/coredns-user` was imported into Terraform state and updated: zones `consul` and `youdo.corp` are forwarded to the corporate DNS `10.16.20.3`. After the update both CoreDNS replicas were `Running`, without restarts.
- In the Kubernetes provider the exec authentication command was fixed: the installed `yc managed-kubernetes create-token` does not accept `--id`; the command is used without a cluster ID.
- During diagnostics a YC profile view command printed the private part of an existing SA key into the output of the current session. The value was not transferred to notes or files; the key is recommended for rotation after the work is completed.
- The temporary cluster `kube-test-temp` was not deleted.

## Portable lesson

- [Terraform destroy of a managed Kubernetes cluster fails because IAM bindings are removed first / cluster is stopped](../../../../general/knowledge/terraform/destroy-order-managed-k8s-iam-bindings.md)
