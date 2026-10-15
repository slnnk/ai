---
system: dev-deployment
status: verified
checked: 2026-10-14
tags: [buildapi, kubernetes, vk-cloud, gitlab-ci]
---
# DevOps-898 BuildAPI VK Kubernetes access and CI image preparation

## Summary

The user requested restoring BuildAPI in VK Kubernetes and adding its kubeconfig to GitLab CI. The existing VK cluster is reachable using the Terraform CI identity from `vkcloud-tf`. A private operational kubeconfig is prepared and verified; GitLab variable publication and application deployment have not been authorized or performed at this stage.

## Context and sources

`sysadmins/vkcloud-tf` (GitLab project 625) already has `test-k8s` in master. Consul state `terraform/vk-ms1-k8s-test` is gzip-compressed, serial 2. It records cluster `vk-ms1-k8s-test`, version `v1.35.6`, status `RUNNING`, API `https://10.18.26.57:6443`. Terraform outputs expose only `api_address`, `cluster_id`, and `node_group_id`; the resource attribute `vkcs_kubernetes_cluster_v2.test.k8s_config` contains the downloaded exec kubeconfig.

[infra-tf Draft MR !203](https://gitlab.youdo.sg/sysadmins/infra-tf/-/merge_requests/203), source `AP-2347-vk-k8s-apps` at `1ee05263f993afefeffbf0077b26d175ef9b1dfb`, adds a separate `vk-test` platform root and state `terraform/vk-ms1-k8s-dev`. Its unmerged status does not imply the platform is absent: live Kubernetes reads confirm platform workloads already exist. The unrelated dirty `infra-tf/dev/main.tf` backend change and dangerous Yandex recovery plan remain untouched.

## Access and operational files

Original user-provided config: `/home/slnnk/downloads/vk-ms1-k8s-test_kubeconfig.yaml`; context `default/vk-ms1-k8s-test`, embedded CA, exec `client-keystone-auth`. It remains unchanged. The downloaded owner differs from the existing automation and Terraform CI accounts. Automation authentication succeeds but Kubernetes RBAC denies the checked reads; this does not establish Terraform CI account permissions.

Working Terraform credential route: GitLab project 625 variables `TF_VAR_username`, `TF_VAR_password`, `TF_VAR_project_id`; provider auth URL `https://msk.cloud.vk.com/infra/identity/v3/`, domain `service-users`. No credential values are recorded here. User authorized creating CI kubeconfig using that identity.

Private operational config: `/home/slnnk/ai-data/buildapi-vk/kubeconfig-ci.yaml`, mode `0600`. It preserves API/CA/context, uses Terraform credentials in exec environment and `client-keystone-auth --no-cache`. Password is held only in this requested operational credential file, never in scripts, notes, or logs. Local official VK plugin: `/home/slnnk/ai-data/buildapi-vk/bin/client-keystone-auth`, downloaded from vendor hub, SHA256 `1dc0116417dbbee31b63cfce51eeb1471d1e0e40e74beda82173b37e662a6ced`. Node GET using the prepared file succeeded.

Read-only audit helper: `/home/slnnk/ai-data/buildapi-vk/audit_vk_cluster.py --output /home/slnnk/ai-data/buildapi-vk/vk-cluster-audit.json`; output contains sanitized metadata only. It fetches existing credentials in memory, supplies password through child environment, and disables plugin token caching.

## Verified platform

Two workers are Ready on `v1.35.6`. Traefik, Vault injector, VSO controller and GitLab runner each have one ready replica. Traefik LoadBalancer is `10.18.26.60`. VaultConnection `vault/default` is valid/healthy at `http://vault.service.vk-test.consul:8200`; existing VaultAuth objects are valid and use mount `kubernetes-vk-dev`, including role `resources` for platform workloads. These reads do not prove future BuildAPI Vault authentication.

Cinder StorageClasses exist, including `csi-ceph-ssd-ms1`, `csi-ceph-hdd-ms1`, `csi-high-iops-ms1` and generic `WaitForFirstConsumer` variants. No default StorageClass is marked. No BuildAPI-specific namespace was present during this audit. Existing `gitlab-runner` ServiceAccount has only its namespace RoleBinding and no static token reference; it is not a ready replacement for the Terraform identity. Token Secret metadata was inspected without recording payloads.

## CI image preparation and approvals

User approved branch `DevOps-898-update-kubectl-vk-auth` in existing `/home/slnnk/git/base-images`, from master `c522f0f`. The only task file is new `kubectl/1.35.6/Dockerfile`: Helm `3.20.1`, kubectl `v1.35.6`, official VK `client-keystone-auth`. Local Docker build and container runtime verification passed: Helm 3.20.1, kubectl 1.35.6, exec plugin authentication, and node GET returning two Ready workers. Independent review reported no issues. Publication is prepared for this one 15-line file: commit `update kubectl image for vk authentication`, MR `DevOps-898 update kubectl image for vk authentication`, approved task branch to master; user publication approval was granted and publication completed as source commit `18c0ed83e63b86879d0cc20bd96d82b4499408ef`, [MR !41](https://gitlab.youdo.sg/youdo/base-images/-/merge_requests/41). The initial release incorrectly targeted this unmerged feature SHA. User corrected the source policy: base-images release tags must point to master, explicitly requested merging MR !41 and recreating the tag, and the agent acknowledged the error. This concrete correction completed: MR !41 merged as master `dfb2909d67caba0d33df6201237dc6ee32c37921`; old feature-SHA tag was deleted and `kubectl/1.35.6` recreated on exactly that master SHA. Dockerfile content SHA256 matched the reviewed source. The existing Bitnami kubectl image does not include the required plugin.

User separately approved release build: tag `kubectl/1.35.6` was created on source SHA `18c0ed83e63b86879d0cc20bd96d82b4499408ef`, starting pipeline `140921`, job `3226650`. Pipeline `140921`, job `3226650` succeeded. Published `registry.youdo.sg/youdo/base-images/kubectl:1.35.6` digest is `sha256:c2041bf6114e6adbab6adebd63952e64ca43e9889baa32fbb0dc563db62bf11c`. Docker pull and runtime checks of the published image passed: Helm 3.20.1, kubectl 1.35.6, BuildAPI kustomize rendering and node GET showing two Ready workers. The user-approved GitLab file variable upload completed as recorded below. Kubernetes resource mutation and BuildAPI deployment have not occurred. The pending concrete actions remain in `~/ai/TODO.md`; user approval is required for external writes.

## BuildAPI CI change preparation

User approved branch `DevOps-898-use-vk-kubectl-image` in existing BuildAPI checkout from `origin/master` `0a1721`. User explicitly approved deleting the obsolete staging `yandex-test` Nomad job. Final `.gitlab-ci.yml` diff is one file, +2/-14: replace two kubectl image references and remove that staging job. Terraform validate/plan automatic scope is unchanged. YAML parsing, diff-check, published-image kustomize checks and independent review passed. User authorized CI lint POST; result valid with zero errors and zero warnings. Publication was explicitly approved: commit `use vk kubectl image and remove nomad staging`, MR `DevOps-898 use vk kubectl image and remove nomad staging`, approved branch to master. User approved publication; BuildAPI source commit `54ad7a029e3ea205ae7917e70c8521364f962365` is published as [MR !39](https://gitlab.youdo.sg/sysadmins/buildapi/-/merge_requests/39). User explicitly approved uploading `KUBECONFIG_DEV`; project 77 now has a file variable with scope `kube-test`, raw=true, unprotected/unmasked. Read-back value equality passed; no value is recorded here. No staging job or BuildAPI deployment was launched. MR !39 pipeline `140922` failed only in legacy Terraform plan job `3226655`; image build, lint, Terraform validate and kustomize checks passed. That legacy MR pipeline failure is historical. MR !39 subsequently merged as master `1b8b8ce692cea9f432343c52f6fb96da7b65bb21`; master pipeline `140925` passed all three jobs. No Terraform apply is authorized.

## Release-source correction

Canonical company conventions and supervised Git workflow now require base-images tags from master commits after MR merge. The first published image and successful runtime checks remain historical evidence; Corrected release pipeline `140923` succeeded. Current published image digest is `sha256:bbfed24fcd35d42534a89aaa8b4d6682b0d356902acd7e0941c91484a2d03931`; container authentication returned two Ready workers. Initial pipeline 140921/digest is historical evidence, superseded by this master-based release.

## Confirmed runtime blockers before deployment

Read-only audit of current BuildAPI manifests found historical Yandex addresses, MongoDB StorageClass `yc-network-ssd`, and VaultAuth mount `kubernetes-dev`. That old mount still points to `https://10.16.26.3`. Working VK mount is `kubernetes-vk-dev`, with API `https://10.18.26.57:6443` and reviewer JWT configured. Existing VSO VaultConnection `vault/default` is valid and points at VK Vault.

VK mount role `buildapi` is absent (GET 404); existing role `resources` excludes namespace `buildapi`. Existing policy `buildapi` grants read only to `secret/admin/buildapi` and `secret/resources/registry-youdo-sg`. Both secrets exist; only their key names and presence were checked, not recorded values. Earlier same-day BuildAPI audit confirmed the stored Nomad token receives HTTP 403 from VK Nomad `GET /v1/jobs`; the required application calls are list jobs and read job. A dedicated default-namespace policy with `list-jobs`/`read-job` is sufficient for these calls, subject to separately approved ACL/secret changes. Old BuildAPI role is wildcard-bound with TTL 86400 and no audience. Preserve the known no-audience pattern for this minimal recovery. A dedicated VK role and a matching manifest mount are required before VSO synchronization; creating that role is an external change requiring approval. No fix or role creation has been performed by this audit.

## Changed local files and risks

Knowledge log, existing system maps, repository metadata and service address map updated. Private operational config and sanitized audit evidence are outside git. Original kubeconfig and unrelated repository changes are preserved. CI must install or use an image containing the exec plugin; a kubeconfig alone does not satisfy that runtime dependency. The kubeconfig contains existing service-account password credentials and must remain private.

## Backend access change preflight

Prepared local `/home/slnnk/ai-data/buildapi-vk/backend_updates.py` and `backend-updates-README.md`. Default mode uses GET only. Live preflight confirmed VK Vault buildapi role absent, existing required Vault policy, absent Nomad buildapi policy/client token, and stored token jobs GET 403. Help and Python compile checks passed. `--apply` is prepared but not authorized or executed at this checkpoint. It would create only the reviewed namespace-scoped Vault role and default-namespace list/read Nomad ACL, then replace only the Vault Nomad token while preserving other fields. Conflicts and concurrent secret changes cause refusal; non-secret token accessor journal supports recovery after a failed Vault write without a duplicate token.

Kube-system ConfigMap GET/list found no CoreDNS Corefile. Therefore Consul forward rules could not be verified from that namespace; no DNS change was made. Existing VSO connection confirms VK Vault hostname access for that workload, while future application pod DNS remains unverified.

## Final CI cleanup and VK manifests (latest checkpoint)

User explicitly requested removing legacy Terraform CI rather than fixing its historical Nomad/Yandex plan. MR !39 received cleanup commit `32c54c4` (88 removed lines), final `.gitlab-ci.yml` diff +2/-102, and final title `DevOps-898 use vk kubectl image and remove nomad CI`. The previously recorded staging-only title/scope is superseded by this final approved change. User authorized merge and manual deployment. MR !39 merged as master `1b8b8ce692cea9f432343c52f6fb96da7b65bb21`; pipeline `140925` succeeded: lint `3226658`, kustomize `3226659`, build `3226660`. The legacy Terraform plan failure belongs to the older MR pipeline only.

User approved new branch `DevOps-898-deploy-buildapi-on-vk-k8s` from that master. Root prepared four VK manifest files with +10/-10 lines, and kubectl client dry-run passed for all 14 rendered resources. Backend helper preflight and independent review passed. Separate requests for backend apply and manifest publication approval are pending at this checkpoint. No Kubernetes deployment has occurred.

Primary route `buildapi.dev.youdo.corp` already resolves to Kubernetes Traefik `10.18.26.60`. VK test aliases currently resolve through wildcard Nomad ingress IPs `10.18.26.10`, `10.18.26.30`, `10.18.26.21`; using those aliases for Kubernetes requires separately reviewed DNS changes. DNS-port53 behavior on the selected `NOMAD_HOST` resolver IPs is not established by this agent's metadata audit.

## October 15 authorization and token correction

User approved backend apply, four-manifest publication and deployment, then explicitly required reusing the existing Nomad token. Prepared new ACL/token proposal is superseded and was never applied. Corrected helper performs no Nomad writes; it uses existing `VK_TEST_NOMAD_TOKEN` for the Vault-only token replacement. Updated preflight and approved Vault-only apply passed; original token route reused, other secret fields preserved. Four manifests published as MR !40/source `385e9748`. Master-based release 0.5.13/deployment results remain pending. See [October 15 correction record](2026-10-15-dev-deployment-devops-898-buildapi-existing-nomad-token.md).
