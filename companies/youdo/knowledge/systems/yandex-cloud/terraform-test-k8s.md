---
system: yandex-cloud
status: verified
checked: 2026-09-14
tags: [terraform, yandex-tf, test-k8s, managed-kubernetes, infra-tf, kubeconfig, autoscaling]
---
# Yandex Cloud test-k8s

## Context

- Last verified: 2026-09-14 (Europe/Moscow).
- Repository: `/home/slnnk/git/yandex-tf`.
- Safe origin: `git@gitlab.youdo.sg:sysadmins/yandex/yandex-tf.git`.
- Terraform root: `/home/slnnk/git/yandex-tf/test-k8s`.
- Purpose: Yandex Managed Kubernetes test environment.

## State and access map

- Remote state backend: Consul at `consul.service.selectel.consul:8500`, datacenter `selectel`.
- State path: `terraform/yandex-test-k8s`.
- Cloud provider: Yandex Cloud provider `~> 0.169.0`.
- Kubernetes provider: HashiCorp Kubernetes provider `~> 2.0`; authentication uses `yc managed-kubernetes create-token` with profile `terraform-k8s-test`.
- The Yandex service-account key is expected at `test-k8s/key.json`; the file was untracked as of the verification date. Do not copy its contents into notes.
- A working plan requires network/DNS access to internal Consul plus Yandex Cloud and the Kubernetes API.

## Plan check: 2026-08-14

- Command: `terraform -chdir=test-k8s plan -no-color -input=false -detailed-exitcode -out=/tmp/test-k8s.tfplan`.
- Result: exit code `0`; `No changes. Your infrastructure matches the configuration.`
- Refreshed objects included the service account and IAM bindings, shared VPC/subnet data, managed Kubernetes cluster, node group, and `kube-system/coredns-user` ConfigMap.
- `terraform fmt -check -diff` passed.
- The initial sandboxed validation/provider-schema attempt failed because provider subprocess execution was restricted; this was an execution-environment limitation, not a Terraform configuration error. The unrestricted full plan loaded providers and refreshed all resources successfully.
- No `apply` was run and no infrastructure changes were made.

### Recheck after node-group settings change

- Command: `terraform -chdir=test-k8s plan -no-color -input=false -detailed-exitcode -out=/tmp/test-k8s.tfplan`.
- Result: exit code `2`, meaning the plan contains changes.
- Summary: `Plan: 0 to add, 1 to change, 0 to destroy`.
- `yandex_kubernetes_node_group.kube_test_node_group` is planned for an in-place update.
- Planned setting: `instance_template.resources.memory` changes from `56` to `48`.
- No replacement or deletion is planned. No `apply` was run.

## Working tree observed

The plan included existing uncommitted changes under `test-k8s` (`k8s-cluster.tf`, `main.tf`, `outputs.tf`, `terraform.tfvars`, `variables.tf`) and new `coredns-custom.tf` and `sa.tf`. These files belong to the user's current work and were not modified during the check.

## Basic diagnosis

- Format: `terraform -chdir=test-k8s fmt -check -diff`.
- Plan: use the command above; do not disable state locking for a routine check.
- State/backend failures: verify corporate DNS/network reachability to `consul.service.selectel.consul:8500`.
- Authentication failures: verify the local Yandex service-account key location and the `yc` profile without logging secret contents.

## CI validate failure: 2026-09-14

- Context: GitLab MR 220, commit `29bd51e` (`add test-k8s to ci`), job `validate:test-k8s` on Docker runner `gitlab-runner-docker-1` with image `registry.youdo.sg/youdo/base-images/terraform:1.7.5`.
- The runner, image, repository checkout, Secure Files download, and `automation-services` clone all succeeded. The failure is configuration linting, not CI infrastructure.
- The newly enabled job runs `cd test-k8s && tflint`. TFLint exits with code 1 because `test-k8s/main.tf` has a `terraform` block but no `required_version`; rule `terraform_required_version` reports this as an issue even though its displayed severity is `Warning`.
- Neighboring roots (`network`, `prod`, `test-infra`, `public-test`) declare `required_version = ">= 1.0"`; `prod-pg` declares `>= 1.0.0`.
- Minimal remediation: add an intentional `required_version` constraint to the `terraform` block in `test-k8s/main.tf`. Since CI currently runs Terraform 1.7.5, a constraint such as `required_version = ">= 1.0"` matches the repository convention; a tighter upper bound should be selected only if compatibility has been assessed.
- No repository files or infrastructure were changed during this diagnosis.

## CI plan failure: job 3140739, 2026-09-14

- Job: `plan:test-k8s`, MR 220 at commit `61e351f`, Docker runner `gitlab-runner-docker-1`.
- Backend initialization, provider installation, Yandex Cloud reads, cluster refresh, and node-group refresh succeeded. The runner can reach Consul and Yandex Cloud.
- Failure occurred while refreshing `kubernetes_config_map_v1.coredns_custom` at the private Kubernetes API `https://10.16.26.3`: `getting credentials: exec: executable yc failed with exit code 1`.
- Root cause: `test-k8s/main.tf` configures the Kubernetes provider exec plugin to run `yc managed-kubernetes create-token --format=json --profile=terraform-k8s-test`, but `plan:test-k8s` only copies `.secure_files/key.json`; it does not create/configure the named YC CLI profile in the fresh CI container. The copied key authenticates the Yandex Terraform provider through `service_account_key_file`, but does not implicitly configure YC CLI.
- Remediation: configure the exact `terraform-k8s-test` YC profile from the service-account key before `terraform plan`, or remove the named-profile dependency and explicitly configure YC CLI authentication for the job. Avoid printing the key variable into logs.
- The credentials in `YC_TERRAFORM_KEY` are usable by YC CLI only after materializing the JSON as a permission-restricted file and passing it to `yc config set service-account-key`; YC CLI does not implicitly consume this project-specific variable name. Because the provider explicitly passes `--profile=terraform-k8s-test`, configure that exact profile in both `plan:test-k8s` and `apply:test-k8s`. The already downloaded/copied `test-k8s/key.json` can be used instead of writing the same key from the variable again, if it represents the intended Terraform service account.
- After configuring the profile, the service account behind the key must also have Kubernetes API authorization sufficient to manage the `kube-system/coredns-user` ConfigMap (through the appropriate Yandex Managed Kubernetes IAM role/RBAC). A token smoke test can be run with output discarded; never print the token or key in CI logs.
- `terraform-k8s-test` is an arbitrary local YC CLI configuration-profile name, not a Yandex Cloud service-account resource. The actual identity is determined by the service-account key loaded into that profile. The same key/account may be loaded into profiles with different names.
- In committed `yandex-tf` roots, only `test-k8s` references the named profile `terraform-k8s-test`. Other roots authenticate the Yandex Terraform provider directly with `service_account_key_file = "key.json"`. `test-infra` additionally runs `yc config set service-account-key ./sa-terraform.json`, but that configures the active/default YC profile, not the explicitly named `terraform-k8s-test` profile. `infra-tf/dev` uses the separate kubeconfig-based flow described below.
- This is separate from the earlier TFLint failure, which was fixed by commit `61e351f`.
- Comparison with successful job `1890645` (2024-05-16, commit `169347f`): that revision used only the Yandex provider plus `terraform-yc-kubernetes` module. Its initialized providers were Yandex, Random, and Time; it had no HashiCorp Kubernetes provider and no Terraform-managed `coredns-user` ConfigMap. Consequently it never executed `yc managed-kubernetes create-token` and did not require the `terraform-k8s-test` CLI profile.
- Commit `de10b76` (`add dev k8s`, 2026-09-14) replaced the old module-oriented configuration, introduced the Kubernetes provider with the named YC CLI profile, and added `test-k8s/coredns-custom.tf`. CI authentication preparation was not updated with those changes. The reused image tag is not the explanation: the old code path simply did not need Kubernetes API credentials.
- `infra-tf/master/dev` uses a different Kubernetes authentication contract. Its `plan:dev` overrides `KUBECONFIG2` with the protected GitLab variable `KUBECONFIG_YANDEX_DEV`; the common `before_script` writes that content to `~/.kube/config`; both Kubernetes and Helm providers use `config_path = var.kubeconfig_path`, whose default is that path. Thus `infra-tf/dev` consumes a ready kubeconfig and does not invoke YC CLI or require the `terraform-k8s-test` profile.
- Responsibility boundary: `yandex-tf/test-k8s` owns the Yandex Managed Kubernetes cluster lifecycle, while `infra-tf/dev` owns workloads/platform resources inside the already-created cluster (Consul state `terraform/yandex-k8s-dev`). Both kubeconfig-based and YC exec-token authentication can work, but the selected method must be provisioned in CI.

### Default YC CLI profile remediation prepared

- Removed the workstation-specific `--profile=terraform-k8s-test` argument from the Kubernetes provider exec command in `test-k8s/main.tf`.
- Updated `plan:test-k8s` and `apply:test-k8s` in `.gitlab-ci.yml` to run `yc config set service-account-key ./key.json` after copying the Secure File. Both the Yandex Terraform provider and YC CLI now use the same key file; YC CLI uses its default/active profile.
- Removed the named profile from the operator command exposed by `test-k8s/outputs.tf`.
- Verification: `terraform fmt -check -diff test-k8s`, `git diff --check`, and YAML parsing passed; `terraform -chdir=test-k8s validate -no-color` passed when provider execution was allowed outside the filesystem sandbox.
- Changes are present in the working tree and were not committed or pushed. Existing unrelated untracked `test-k8s-temp/` was not modified.

## Ice Lake node-group change: 2026-09-14

- Scope checked: `yandex_kubernetes_node_group.kube_test_node_group` (`kube-test-node-group`, ID `catd0sn7d33n3rrgivh6`) in `test-k8s/k8s-cluster.tf`.
- Current template: `platform_id = "standard-v2"` (Intel Cascade Lake), 8 vCPU, 48 GB RAM, 100% core fraction, 93 GB `network-ssd-nonreplicated`. State shows subnet `subnet-test` in `ru-central1-b`.
- Changed `test-k8s/k8s-cluster.tf` from `platform_id = "standard-v2"` to `platform_id = "standard-v3"` (Intel Ice Lake). The existing 8-vCPU/48-GB shape is compatible with this standard platform.
- In Yandex Terraform provider `0.169.0`, `instance_template.platform_id` is not `ForceNew` and is included in the node-group update-field map. Terraform should therefore plan an in-place node-group update, while Managed Kubernetes reconciles/replaces the underlying VM nodes with the new template.
- The group has no explicit `deploy_policy`; documented defaults are `max_expansion = 3` and `max_unavailable = 0`, so replacement nodes should be created before old nodes are removed. Before apply, verify Compute/disk quotas and Ice Lake capacity in `ru-central1-b`, because temporary expansion and new non-replicated SSDs require spare quota/capacity.
- Operational risk: all nodes must be rotated. Check PDBs, required anti-affinity, local `emptyDir` workloads, and drain behavior; monitor node-group `Reconciling`, node readiness, and workload rescheduling. A Terraform plan must be reviewed before apply.
- Verification after the source change: `terraform fmt -check -diff test-k8s`, `git diff --check`, and `terraform -chdir=test-k8s validate -no-color` passed. The change remains uncommitted; no plan/apply or infrastructure mutation was performed. Existing unrelated untracked `test-k8s-temp/` was not modified.
- Added an explicit node-group `deploy_policy` with `max_expansion = 1` and `max_unavailable = 0` so the Ice Lake rollout creates at most one replacement node above the current target at a time and does not deliberately make an existing node unavailable before replacement capacity is ready. Validation and formatting checks passed. At the end of the edit, the earlier `standard-v3` change was staged while the new deploy-policy hunk was unstaged (`MM test-k8s/k8s-cluster.tf`); staging was left to the user.

## `test-k8s-temp` destroy preparation: 2026-09-14

- User requested preparation through destroy plan only; no apply or cloud deletion was performed.
- Terraform root: `/home/slnnk/git/yandex-tf/test-k8s-temp` (untracked local directory). Dedicated Consul backend path: `terraform/yandex-test-k8s-temp`, separate from permanent `test-k8s` state.
- Refreshed target: stopped cluster `kube-test-temp` (`cate30plq4p8h3hkab00`) in `ru-central1-b`; stopped node group `kube-test-temp-node-group` (`catof0bd6l9rbnej3q9o`); dedicated service account `k8s-test-sa` (`ajeqajruh12b40tkav95`).
- Cross-state ownership check: permanent cluster `kube-test` (`catd03r096n9ih2qahac`) uses the distinct service account `k8s-test-main-sa` (`ajeooej0ch81ai4ka7su`) for both `service_account_id` and `node_service_account_id`. Temporary cluster `kube-test-temp` uses `k8s-test-sa` (`ajeqajruh12b40tkav95`) for both fields. Therefore deleting `k8s-test-sa` does not remove the service/node identity configured for permanent `test-k8s`. This proves Terraform linkage, but does not by itself exclude undocumented out-of-band consumers of keys issued to the temporary account.
- State contains 10 managed resources to destroy: cluster, node group, service account, and seven folder IAM bindings. Shared VPC, subnet, and network folder are data sources and are not destroy targets. The local CoreDNS ConfigMap file has no corresponding resource in state; deletion of the cluster removes any in-cluster objects with it.
- Saved destroy plan: `/tmp/test-k8s-temp-destroy.F7vQUc.tfplan`, mode `0600`, SHA-256 `240353f4e385c0747d35cf82cadcf156f5e66265e6c63bbdd8cfb108d65fe78c`; plan summary is `0 to add, 0 to change, 10 to destroy`.
- Pre-destroy state backup: `/tmp/test-k8s-temp-pre-destroy.8eoPVx.tfstate`, mode `0600`, SHA-256 `8db284bf735d6426ab5157da94a4f88da2c89df649b790e25038f112cee144cb`.
- YC CLI authentication was configured only in temporary XDG config directory `/tmp/test-k8s-temp-yc.k5OHVd`; that directory was deleted after planning. The source key remains at `test-k8s-temp/key.json`, and its permissions were tightened from `0664` to `0600` without reading or copying its contents.
- If state changes or significant time passes, discard/regenerate the saved plan rather than applying stale intent. The explicit apply command, when approved, is `terraform -chdir=test-k8s-temp apply /tmp/test-k8s-temp-destroy.F7vQUc.tfplan`.
- First manual apply attempt did not mutate infrastructure: Consul rejected state-lock creation with HTTP 403 and anonymous AccessorID `00000000-0000-0000-0000-000000000002`, lacking `session:write` on `sc-hashi-selectel-master-03`. Root cause is that the interactive shell did not export the working `CONSUL_HTTP_TOKEN`; the variable is present in `~/ai/current/.env`. Load/export it before retrying. Do not use `-lock=false` for this destroy.
- A subsequent manual apply of the saved destroy plan partially completed. All seven IAM bindings for `k8s-test-sa` were destroyed, then deletion of node group `catof0bd6l9rbnej3q9o` failed with Yandex API `FailedPrecondition`: deletion is not permitted while cluster `cate30plq4p8h3hkab00` is stopped. No cluster, node-group, or service-account deletion completed.
- Post-failure state contains only three managed resources: `yandex_kubernetes_node_group.kube-test-temp-node-group`, `yandex_kubernetes_cluster.kube-test-temp`, and `yandex_iam_service_account.k8s-test-sa`; both cluster and node group report `stopped`. The old saved destroy plan is stale after the partial apply and must not be reused.
- Safe recovery: recreate the seven IAM bindings from the normal Terraform configuration, start the cluster, wait for `running`, then generate a fresh destroy plan. Ensure the cluster resource depends on its required IAM bindings (or delete cluster resources in a controlled first phase) so a repeated full destroy does not revoke the service account roles before cluster/node-group deletion is accepted.
- A manual `yc managed-kubernetes cluster start --id cate30plq4p8h3hkab00` through the user's active `default` YC profile returned `PermissionDenied` (client request `d5a4fe7f-7454-4f70-aae3-bc7030f5eb3a`). This invocation did not explicitly use the Terraform key. Local `test-k8s-temp/key.json` belongs to separate operator service account `ajegfhq6i2abngq74fcc` (key ID `aje1kjc599tg2oj7ok2d`), not cluster service account `ajeqajruh12b40tkav95`. Retry start through a dedicated temporary named profile loaded from that key before concluding that deleted cluster-SA bindings must be restored; do not expose key contents.
- Start retry through an isolated YC config loaded from Terraform operator key `ajegfhq6i2abngq74fcc` also returned `PermissionDenied` (client request `15b1bab6-b397-43b6-bbcc-4f94ba9072ff`); the cluster remained stopped. The temporary YC config directory was removed.
- Prepared but did not apply targeted recovery plan `/tmp/test-k8s-temp-restore-iam.IyxTwW.tfplan` (mode `0600`): exactly `7 to add, 0 to change, 0 to destroy`, restoring the seven original bindings for cluster service account `ajeqajruh12b40tkav95`. Applying it is a privileged IAM mutation and requires explicit user confirmation before retrying cluster start.
- After explicit user approval, applied recovery plan `/tmp/test-k8s-temp-restore-iam.IyxTwW.tfplan`: `7 added, 0 changed, 0 destroyed`. All original IAM bindings are again present in Terraform state.
- Retried cluster start through an isolated YC config using Terraform operator key `ajegfhq6i2abngq74fcc`. Operation completed successfully in 2m46s: cluster `kube-test-temp` is `RUNNING / HEALTHY`, and node group `kube-test-temp-node-group` is `RUNNING` (verified separately). The temporary YC config was deleted afterward.
- No destroy was performed in this recovery step. The old destroy plan remains stale and must not be applied; create a fresh destroy plan after correcting dependency ordering so cluster/node-group deletion precedes removal of their service-account bindings.
- Added explicit `depends_on` in local `test-k8s-temp/k8s-cluster.tf` from the cluster to all seven service-account IAM bindings. This reverses destroy ordering so Terraform deletes node group, then cluster, then bindings and service account. `terraform validate`, `terraform fmt -check` for the changed file, and `git diff --check` passed; unrelated pre-existing formatting differences remain in `test-k8s-temp/main.tf` and `terraform.tfvars`.
- Fresh post-recovery destroy plan: `/tmp/test-k8s-temp-destroy-v2.CY7idl.tfplan`, mode `0600`, SHA-256 `84c98549a9a1e5142c7552e4d617d4c1832a877e660c01f743b4bb65d47ce2f0`. Refreshed cluster and node group are both `running`; plan is `0 to add, 0 to change, 10 to destroy`. Plan JSON confirms all seven explicit cluster dependencies.
- Fresh pre-destroy state backup: `/tmp/test-k8s-temp-pre-destroy-v2.keYb5D.tfstate`, mode `0600`, SHA-256 `b7f39c58d5d88b66c210b34d80a8a2995ab5d63ac0bb23b3501a4d03101f398b`. No apply was performed for the new destroy plan.

## CI kubeconfig investigation: 2026-08-17

- Yandex Cloud's static kubeconfig procedure was checked against the current documentation, updated 2026-08-12.
- The permanent `kube-test` master is private (`master.public_ip = false`), so CI runners must have routing and DNS/access to the cluster's internal API endpoint; a kubeconfig alone does not provide network reachability.
- The repository CI currently authenticates dynamically in `plan:test-infra` and `apply:test-infra`: it writes the protected `YC_TERRAFORM_KEY` value to a temporary service-account key file, configures `yc`, and runs `yc k8s cluster get-credentials --id $YC_TEST_K8S_ID --internal`.
- The user's default local `kubectl` context was not modified and still pointed to the older `yc-kube-test-temp` context at the start of the work.
- For CI that already has `yc`, prefer the existing short-lived token flow. If a static kubeconfig is required for a job without `yc`, create a dedicated in-cluster Kubernetes ServiceAccount in the workload namespace and bind only the required Role. Avoid the documentation example's `kube-system/admin-user` plus `cluster-admin` unless the pipeline genuinely administers the entire cluster.
- Store the resulting kubeconfig as a protected/masked GitLab CI file variable or in the organization's secret store. Never commit the kubeconfig or its bearer token.

### Static cluster-admin kubeconfig created

- Target cluster: `kube-test`, cluster ID `catd03r096n9ih2qahac`, status `RUNNING` when checked, internal API endpoint `https://10.16.26.3`.
- Following the Yandex Cloud static kubeconfig procedure, created Kubernetes objects:
  - `ServiceAccount/admin-user` in `kube-system`;
  - `Secret/admin-user-token` of type `kubernetes.io/service-account-token` in `kube-system`;
  - `ClusterRoleBinding/admin-user`, binding that ServiceAccount to `cluster-admin`.
- Static kubeconfig path: `/home/slnnk/.kube/test-k8s-ci.kubeconfig`; permissions `0600`. It contains an embedded cluster CA and bearer token, has context `default`, and does not contain an `exec` authentication plugin.
- Verification succeeded using only the static kubeconfig: namespaces were listed and `kubectl auth can-i '*' '*'` returned `yes`.
- Temporary kubeconfig, CA, and manifest files under `/tmp/test-k8s-kubeconfig.0QZPPF` were removed after verification.
- The cluster has only an internal endpoint. A GitLab runner must reach `10.16.26.3:443`; storing the file in GitLab does not solve routing.
- Treat the kubeconfig as a secret. Store it as a protected GitLab file variable/secure file; do not commit it to Git.
- Revoke this credential by deleting the token Secret. Fully remove the identity and binding with:
  `kubectl --kubeconfig <admin-config> delete clusterrolebinding admin-user secret admin-user-token serviceaccount admin-user -n kube-system`

## `infra-tf/dev` plan: 2026-08-17

- Related repository: `/home/slnnk/git/infra-tf`; safe origin `git@gitlab.youdo.sg:sysadmins/infra-tf.git`; working branch observed as `DevOps-689-yandex-dev`.
- Terraform root: `/home/slnnk/git/infra-tf/dev`.
- Provider authentication: variable `kubeconfig_path`; plan used `/home/slnnk/.kube/test-k8s-ci.kubeconfig` through `TF_VAR_kubeconfig_path`.
- Remote state: Consul `consul.service.selectel.consul:8500`, datacenter `selectel`, path `terraform/yandex-k8s-dev`.
- The normal plan could not acquire the state lock. Lock ID was `eb9bd028-360d-4531-c293-d173f5858af1`, held by `root@runner-t1rtu4a-project-564-concurrent-0` for a Terraform plan created at `2026-08-17 08:31:28 UTC`.
- A read-only diagnostic plan was therefore run with `-lock=false`; it completed successfully with `Plan: 12 to add, 0 to change, 0 to destroy`. No plan file was saved and no apply was run.
- Planned creates: namespaces `loki`, `traefik`, `vault`, `victoriametrics`; ConfigMaps `vmalert-rules-general` and `vmalert-rules-services`; Helm releases Traefik, Vault, Vault Secrets Operator, VMagent, VMalert, and VictoriaMetrics cluster.
- Refresh explicitly reported out-of-band deletion of the `victoriametrics` namespace, general alert-rules ConfigMap, and Helm releases Traefik, Vault, VMagent, VMalert, and VMcluster.
- Treat this plan as diagnostic only because it was produced without the state lock while CI was operating on the same state. Before apply, rerun a normal locked plan after the CI lock is released and verify that the kubeconfig targets the intended cluster for state path `terraform/yandex-k8s-dev`.
- Security risk: rendered Helm values in Terraform plan output expose credentials/webhook material already present in repository configuration. Do not paste or archive raw plan output in notes or CI logs; move those values to the approved secret store and mark Terraform inputs sensitive where possible.
- Existing unrelated untracked directory `helm-charts/` was observed and left untouched.

### CI apply failure and cluster state

- CI apply started at `2026-08-17 08:38:41 UTC` on `root@runner-t1rtu4a-project-564-concurrent-0` and ended with exit code 1. The Consul state lock was released normally after job completion; no force-unlock was used.
- Root cause: the CI runner timed out downloading Helm repository indexes from `https://traefik.github.io/charts/index.yaml` and `https://victoriametrics.github.io/helm-charts/index.yaml` (`context deadline exceeded while awaiting headers`). This is runner egress/DNS/proxy connectivity to GitHub Pages, before Kubernetes workload creation.
- Successful partial apply: namespaces `loki`, `traefik`, `vault`, and `victoriametrics`; both VictoriaMetrics rules ConfigMaps; Helm releases `vault` 0.27.0 and `vault-secrets-operator` 1.5.1.
- Verified cluster state after failure: Vault agent injector was `1/1 Running`; Vault Secrets Operator controller was `2/2 Running`; zero restarts and no Warning events. `VaultAuth/default` and `VaultConnection/default` were accepted.
- Missing after failure: Traefik and VictoriaMetrics cluster/agent/alert releases. The `traefik` and `victoriametrics` namespaces had no corresponding workloads; no scheduling, image-pull, or PVC failure occurred because Helm never submitted those manifests.
- A post-failure diagnostic plan with state locking available and `-refresh=false` reported `4 to add, 2 to change, 0 to destroy`; the creates were Traefik, VMcluster, VMagent, and VMalert. Rerun a normal refresh-enabled plan before retrying apply.
- Remediation path: restore HTTPS access from the Docker GitLab runner to the two GitHub Pages hosts, configure the required corporate proxy/allowlist, or mirror/pin the Helm charts in the internal `sysadmins/helm-charts` repository or another internal chart registry and point Terraform modules there. Test from the same runner image/network namespace, not only from a workstation.

### Local apply after CI failure

- A local `terraform apply -no-color -input=false -auto-approve -lock-timeout=30s` was run from `/home/slnnk/git/infra-tf/dev` with `TF_VAR_kubeconfig_path=/home/slnnk/.kube/test-k8s-ci.kubeconfig` and the normal Consul state lock.
- The local host could reach the GitHub Pages Helm repositories. VMcluster, VMagent, VMalert, and the Traefik Kubernetes resources were created.
- VictoriaMetrics verification: VMagent, VMalert server, VMalertmanager, vmauth (two pods), vminsert, vmselect, and vmstorage were all Ready/Running with zero restarts. The `10Gi` vmstorage PVC bound successfully using `yc-network-ssd`.
- Traefik pod was Ready/Running with zero restarts, but Service `traefik` remained `LoadBalancer` with external IP pending.
- Apply exited with code 1 after the Traefik Helm timeout. Kubernetes Warning events report `ResourceExhausted`: Yandex Cloud quota `ylb.networkLoadBalancers.count` is exceeded. This is now the only apply blocker.
- The failed Traefik release is present both in Helm and Terraform state with status `failed`; Terraform marked the resource tainted. A refresh-enabled post-apply plan reported `1 to add, 0 to change, 1 to destroy` for replacement of only `module.traefik.helm_release.traefik`.
- Do not rerun apply until Network Load Balancer quota is increased or an existing unused load balancer is safely removed. The next apply will uninstall/reinstall the tainted Traefik release and can briefly interrupt its pod. No force-unlock, manual Helm uninstall, or state manipulation was performed.

### Traefik LoadBalancer recovery

- After the Yandex Network Load Balancer quota was increased, retrying apply showed that the original requested internal IP `10.16.26.100` was already in use (`FailedPrecondition: Internal address in use`).
- Changed `/home/slnnk/git/infra-tf/dev/traefik.tf` setting `service_spec_loadbalancerip` from `10.16.26.100` to `10.16.26.101`; this is inside subnet `10.16.26.0/24` (`e2lk85dmf4e93a2emoe7`).
- Applied the change with the normal Consul state lock. Terraform replaced only the tainted Traefik Helm release: `1 added, 0 changed, 1 destroyed`.
- Verified result: Helm release `traefik` revision 1 is `deployed`; pod is Ready/Running with zero restarts; Service is type `LoadBalancer` and received internal address `10.16.26.101` on ports 80 and 443.
- A refresh-enabled `terraform plan -detailed-exitcode` returned exit code 0 and `No changes`. Historical Warning events for quota exhaustion and old IP conflict remain in the namespace event history but no warning was generated for the final Service.
- The source change in `dev/traefik.tf` remains uncommitted. Existing unrelated untracked directory `helm-charts/` remains untouched.

## Kubelet eviction settings: 2026-09-04

- Live cluster version: Kubernetes `v1.34.1`; two observed nodes `cl1e8jt27j03mj4g8q0g-ovir` and `cl1e8jt27j03mj4g8q0g-ylyr`.
- Read `/api/v1/nodes/<node>/proxy/configz` through `/home/slnnk/.kube/config-yandex-dev`. Both kubelets use the same hard thresholds: `memory.available=100Mi`, `nodefs.available=10%`, and `nodefs.inodesFree=5%`.
- `evictionSoft`, `evictionSoftGracePeriod`, and `evictionMinimumReclaim` are unset. `evictionPressureTransitionPeriod=5m`; `mergeDefaultEvictionSettings=false`.
- The memory threshold is the standard Linux kubelet hard-eviction default. Yandex Managed Kubernetes additionally accounts for 100 MB of eviction reserve when calculating allocatable node memory.
- The current Yandex Terraform provider `0.169.0` schema for `yandex_kubernetes_node_group` exposes no kubelet or eviction configuration block. Current YC CLI node-group update options likewise expose no kubelet/eviction option. Therefore the threshold is not configurable through the supported Managed Kubernetes node-group API/Terraform surface used by this cluster; it is per-kubelet, not a namespace Kubernetes object.
- For supported operation, control risk using node sizing/autoscaling, realistic requests, PriorityClasses, and monitoring. Directly editing managed-node kubelet files/flags would be an unsupported, nonpersistent workaround and may be lost on node repair/recreation.
## Node group autoscaling state: 2026-09-04

- Managed Kubernetes node group: `kube-test-node-group` (`catd0sn7d33n3rrgivh6`), instance group `cl1e8jt27j03mj4g8q0g`.
- Terraform resource `yandex_kubernetes_node_group.kube_test_node_group` uses automatic scaling: `min=1`, `initial=1`, `max=10`; two nodes are not statically declared.
- At inspection time, the underlying instance group had `target_size=2` and `running_actual_count=2`. Its reported `fixed_scale.size=2` is the current concrete target maintained underneath the Managed Kubernetes node-group autoscaler, not the Terraform scaling policy.
- Nodes were created at different times: `cl1e8jt27j03mj4g8q0g-ovir` on 2026-08-24 and `cl1e8jt27j03mj4g8q0g-ylyr` on 2026-08-27. This is consistent with a scale-up from the initial single node.
- Conclusion: the second node was almost certainly added by node-group autoscaling. Available Kubernetes events and accessible control-plane logs do not retain enough history to identify the exact unschedulable pod that triggered the 2026-08-27 scale-up or completely exclude a manual control-plane resize.
- The Tochka resource adjustment made on 2026-09-04 did not create the second node because that node already existed since 2026-08-27.
- A group remains at two nodes while workloads cannot safely be consolidated onto one node because of resource requests, scheduling/topology rules, persistent volumes, disruption budgets, system workloads, or autoscaler timing constraints.

### Confirmed scale-down blockers (checked 2026-09-04)

- Current actual usage: node `ovir` 2217m CPU / 16292Mi RAM, node `ylyr` 914m CPU / 11996Mi RAM.
- Scheduled requests: `ovir` 4380m CPU / 20244Mi RAM; `ylyr` 2180m CPU / 16576Mi RAM. Combined requests are approximately 6560m CPU and 36820Mi RAM versus 7910m CPU and 44384Mi allocatable on one node, before removing duplicate DaemonSet requests. Raw CPU/RAM capacity therefore is not the principal blocker.
- `kube-system/kube-dns-autoscaler` has `preventSinglePointFailure: true`, so it keeps two CoreDNS replicas while the group has more than one node. Its pod template does not have `cluster-autoscaler.kubernetes.io/safe-to-evict: "true"`. Yandex Managed Kubernetes documents this as a reason an autoscaled group does not shrink from two nodes to one.
- Loki has two replicas of `backend`, `read`, and `write`, with required pod anti-affinity on `kubernetes.io/hostname`. One replica of every pair is on each node, so the scheduler cannot move both replicas onto a single remaining node.
- Multiple non-DaemonSet pods on `ylyr` use `emptyDir` (including Redis, RabbitMQ and monitoring workloads). Yandex documents pods with local storage as non-evictable by default unless explicitly annotated `cluster-autoscaler.kubernetes.io/safe-to-evict: "true"`; these are additional possible blockers.
- No `cluster-autoscaler.kubernetes.io/scale-down-disabled` annotation was present on either node, and no pod explicitly had `safe-to-evict: "false"`.
- Conclusion: scale-down to one node is intentionally impossible with the current availability and eviction settings. Changing it requires accepting single-node/single-point-of-failure behavior and adjusting CoreDNS plus monitoring scheduling/eviction policies.

## Related recipes

- [Terraform destroy of a managed Kubernetes cluster stops half-way](../../../../../general/knowledge/terraform/destroy-order-managed-k8s-iam-bindings.md)
- [Autoscaled node group stays at two nodes although one node would fit the load](../../../../../general/knowledge/k8s/cluster-autoscaler-cannot-scale-down-to-one-node.md)
