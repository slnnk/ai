---
system: gitlab-ci
status: hypothesis
checked: 2026-09-16
tags: [gitlab-runner, kubernetes, android, autoscaling, terraform, vault, yandex-cloud, selectel]
---
# android-youdo4 dynamic Kubernetes runner

Last checked: 2026-09-09

Status: architecture agreed in principle; no repository or infrastructure
changes have been made.

## Decision update: 2026-09-16

- Final target is Yandex Managed Kubernetes, using the existing `kube-test`
  cluster managed from `/home/slnnk/git/yandex-tf/test-k8s`.
- The earlier Selectel `mks-infra` target documented below is superseded and
  retained only as historical design context. Do not implement the Android
  runner in Selectel unless the decision is explicitly revisited.
- Preserve the same architecture: one always-on runner-manager pod on the
  permanent node group and a separate tainted Android CI node group that
  autoscales from zero for Kubernetes executor job pods.
- Kubernetes platform resources and the runner Helm release belong in the
  Yandex-cluster Terraform/Helm management path (currently related to
  `/home/slnnk/git/infra-tf/dev`); exact ownership must be confirmed before
  implementation to avoid splitting one release across Terraform states.

## Yandex runner-manager implementation: 2026-09-16

- Added, but did not apply, the runner-manager definition in
  `/home/slnnk/git/infra-tf/dev`:
  - namespace ownership in `dev/namespaces.tf`;
  - VSO token synchronization and Helm release in
    `dev/gitlab-runner-android.tf`;
  - chart configuration in
    `dev/config/gitlab-runner-android-values.yaml`;
  - prerequisites and operational checks in
    `dev/GITLAB_RUNNER_ANDROID.md`.
- Pinned official chart `0.74.3`, which runs GitLab Runner `17.9.3`, matching
  the existing VM runner version.
- Manager: one non-privileged pod, `100m/128Mi` requests and `500m/512Mi`
  limits, namespace-scoped least-privilege Role, metrics on port `9252`, and
  global concurrency `6` matching the live VM runner.
- Manager has required node affinity excluding nodes labeled
  `workload.youdo.sg/gitlab-android`; live permanent `kube-test` nodes were
  checked read-only and did not have that label.
- Future job pods require label `workload.youdo.sg/gitlab-android=true` and
  taint toleration `workload.youdo.sg/gitlab-android=true:NoSchedule`.
- Runner token is expected from Vault KV v1 path
  `secret/resources/gitlab-runner-android`, with keys `runner-token` and an
  empty `runner-registration-token`; values are not stored in Git or Terraform.
  The VSO resource currently authenticates through the existing
  `kubernetes-dev` / `resources` role. Confirm that role accepts the new
  namespace and can read this path before apply.
- Live baseline was read safely from
  `root@172.28.0.175:/etc/gitlab-runner/config.toml` without copying secrets.
  Host `gitlab-runner-android` runs Runner `17.9.3`; config SHA-256 at check time
  was `f7a7917e1223556e63a79ef586a6701e4beb5403a331bc1c4539a77f0f4b603f`.
  Relevant settings are `concurrent=6`, `output_limit=204800`, shared S3 cache
  at `storage.yandexcloud.net` bucket `youdo-gitlab-runner`, pull policy
  `if-not-present` with `always` allowed, `DOCKER_AUTH_CONFIG`, and timezone
  `Europe/Moscow`.
- Added VSO destinations for S3 credentials at
  `secret/resources/gitlab-runner-android-cache` (`accesskey`, `secretkey`) and
  registry configuration at `secret/resources/gitlab-runner-android-registry`
  (`DOCKER_AUTH_CONFIG`). Values were not read into notes or committed.
- Docker-only privileged mode, host cache/daemon mounts, TLS variables, and
  insecure-registry daemon arguments were intentionally not migrated to the
  Kubernetes executor. The reviewed project jobs do not demonstrate a DinD
  requirement; registry trust on containerd nodes is a separate node-image
  concern if an insecure endpoint is later required.
- A read-only Vault API check of the `resources` role was attempted with the
  available local Vault token and returned HTTP 403. No Vault state changed;
  an operator with permission to read `auth/kubernetes-dev/role/resources`
  must perform the prerequisite check.
- Validation evidence: `terraform validate` passed; `terraform fmt -check` and
  `git diff --check` passed; official chart download, `helm lint`, and local
  render passed. Render confirmed one manager replica on permanent nodes,
  namespace-scoped explicit RBAC, and Android-only scheduling for job pods.
- No Terraform plan/apply, Kubernetes mutation, GitLab runner registration, or
  Vault write was performed.

## Goal and decisions

- Pilot project: `team-youdo-android/android-youdo4`.
- GitLab project URL:
  `https://gitlab.youdo.sg/team-youdo-android/android-youdo4`.
- Move all project CI jobs, including feature, regression, BrowserStack, Nexus
  uploads, notifications, and manual store publication jobs.
- Target the existing Selectel Managed Kubernetes cluster `mks-infra` and add a
  dedicated autoscaled node group.
- Cold-start delay while a node is provisioned is acceptable.
- Desired idle state: no Android job pods and zero nodes in the Android CI node
  group. One small GitLab Runner manager pod remains on the permanent platform
  node group so it can poll GitLab.

## Repositories and ownership

| Component | Local repository/path | Responsibility |
|---|---|---|
| Android application CI | `/home/slnnk/git/android-youdo4/.gitlab-ci.yml` | Job definitions, runner tag, job-specific resource requests and Gradle cache declaration. |
| Existing VM runner | `/home/slnnk/git/automation-services/inventories/prod_yandex/host_vars/gitlab-runner-android.yml` and corresponding Selectel inventory | Current Docker executor configuration and S3 cache contract; contains access material that must not be copied to documentation. |
| Current Android runner VM | `/home/slnnk/git/selectel-tf/prod/compute-gitlab-runners.tf` | Existing fixed runner shape and disk baseline. |
| `mks-infra` cluster/node groups | `/home/slnnk/git/selectel-tf/prod-mks` | Selectel MKS cluster and dedicated Android CI node group. Terraform backend: Consul path `terraform/selectel-mks`. |
| Cluster platform services | `/home/slnnk/git/infra-tf/prod` | Namespace, Helm release, RBAC, Vault Secret Operator resources, monitoring. Terraform backend: Consul path `terraform/selectel-k8s-infra`. |
| Android Gradle image | `/home/slnnk/git/gradle` | Builds `registry.youdo.sg/sysadmins/devops-tools/gradle`; `android-youdo4` currently consumes tag `18`. |
| Store publishing image | `/home/slnnk/git/fastlane-docker` | Images used by Google Play, Huawei AppGallery, and RuStore publication jobs. |

Safe origins:

- `git@gitlab.youdo.sg:team-youdo-android/android-youdo4.git`
- `git@gitlab.youdo.sg:sysadmins/selectel/selectel-tf.git`
- `git@gitlab.youdo.sg:sysadmins/infra-tf.git`
- `git@gitlab.youdo.sg:sysadmins/automation-services.git`

## Verified current state

### Project CI

The current GitLab API version of `develop/.gitlab-ci.yml` was checked read-only.
The file blob is `dd1ac3701250f52fc2956b64dcd7702992f34455`, last changed by commit
`227f7518c3415d0527e55607044c93c75ec98b2f`. The local `origin/develop` ref is
older, while the local branch `DevOps-833-fix-hotfix` contains that current CI
blob; do not treat the stale remote-tracking ref as the current server state.

All visible jobs use tag `gitlab-runner-android-dind01-runner`. Main workloads:

- `feature`, `regress`, and `hotfix`: Gradle Android builds in
  `registry.youdo.sg/sysadmins/devops-tools/gradle:18`;
- BrowserStack jobs: Gradle upload tasks after the corresponding build;
- notification jobs: `python:3.6-alpine3.10` and YouTrack/notification scripts;
- test publication jobs: upload APK/version files to Nexus;
- manual publication jobs: Fastlane images for Huawei, RuStore, and Google Play.

Recent GitLab job data shows approximately 15-minute successful `feature`
builds and approximately 85-90-minute successful `regress` builds. Queue time on
the existing warm runner was generally a few seconds. Work arrives in bursts
with idle gaps; manual jobs can run substantially later than the pipeline that
created them.

### Existing Android runner

- GitLab job records identify the active manager as
  `gitlab-runner-android (10.16.24.175)`.
- Docker executor, privileged mode, shared S3 cache configuration,
  `concurrent=3`.
- The project CI itself does not declare Docker services or run Docker commands;
  its Gradle and publication containers execute directly. Privileged mode is
  therefore not a demonstrated requirement for this pipeline and should not be
  enabled in the Kubernetes pilot unless a runtime test proves it necessary.
- Existing VM definition: 6 vCPU, 32 GiB RAM, 15 GiB boot volume plus 100 GiB
  fast data volume.
- Existing runner mounts a host cache directory and daemon configuration and
  uses `if-not-present` image pulls. A scale-to-zero Kubernetes group will lose
  node-local image and Gradle caches, so cold builds and explicit distributed
  cache behavior must be tested.

### `mks-infra`

Repository snapshot in `/home/slnnk/git/selectel-tf/prod-mks`:

- cluster name `mks-infra`;
- Kubernetes `1.33.5`;
- private Kubernetes API;
- region `ru-2`, availability zone `ru-2c`;
- existing permanent node group: three nodes, each 8 vCPU / 30 GiB RAM;
- Selectel Terraform provider constraint `~> 7.1.0`;
- local `selectel-tf` checkout is on user branch `DevOps-778-b2b-db`; preserve
  unrelated work.

Selectel supports Cluster Autoscaler and scale-to-zero for a node group when at
least two working nodes remain in other groups. `mks-infra` currently describes
three permanent nodes, so the proposed topology meets that prerequisite at the
configuration level. Runtime state and quotas still need read-only verification
before planning/apply.

The provider resource `selectel_mks_nodegroup_v1` supports
`enable_autoscale`, `autoscale_min_nodes`, `autoscale_max_nodes`, labels, and
taints. Selectel Cluster Autoscaler is managed by MKS and reacts to unschedulable
`Pending` pods based on declared CPU/RAM requests. Default low-utilization
scale-down delay is 10 minutes.

## Selected architecture

```text
GitLab android-youdo4
        |
        | runner long polling
        v
GitLab Runner manager Deployment (replicas=1)
namespace: gitlab-runner-android
scheduled on permanent mks-infra nodes
        |
        | creates one Kubernetes pod per accepted job
        v
job pod Pending, selected/tolerated only for Android CI nodes
        |
        v
Selectel Cluster Autoscaler
dedicated Android CI node group: 0 -> 1..3 -> 0
```

Initial proposed node-group parameters (design, not yet applied):

- `nodes_count = 0`;
- `enable_autoscale = true`;
- `autoscale_min_nodes = 0`;
- `autoscale_max_nodes = 3`;
- 8 vCPU, 32 GiB RAM per node;
- 100 GiB `fast.ru-2c` volume;
- non-preemptible nodes for the first rollout;
- label `workload=gitlab-android`;
- taint `workload=gitlab-android:NoSchedule`.

Keep Cluster Autoscaler `zeroOrMaxNodeScaling=false` so the group can grow one
node at a time. Karpenter is not selected: it adds another controller and
requires changes to autoscaling/auto-recovery policy that are not justified for
one fixed Android worker shape. VM Docker Autoscaler is also not selected because
the agreed target is `mks-infra`.

## Proposed runner behavior

- Official GitLab Runner Helm chart with Kubernetes executor.
- One project-scoped, protected runner, initially with a new tag such as
  `k8s-android-dynamic`.
- Manager pod pinned to permanent platform nodes; job pods pinned to and
  tolerant of only the dedicated Android CI group.
- Runner concurrency/limit initially 3 to preserve the current upper bound.
- Default job resources plus bounded per-job overrides. Heavy Gradle builds
  should reserve enough memory to trigger a dedicated node; notification/upload
  jobs should request much less. Exact requests require measurement or a staged
  trial and are not yet approved.
- Non-privileged job pods by default.
- Registry pull secret and runner authentication token supplied through the
  approved Vault/VSO path; no secret values in Terraform, Helm values, Git, or
  this note.
- Existing GitLab protected/masked variables remain the source for keystore,
  Nexus, BrowserStack, YouTrack/notification, and store credentials.
- Use the existing object-storage runner cache backend, but add an explicit,
  controlled Gradle cache contract in `.gitlab-ci.yml`; do not use a shared PVC
  that could pin the CI node group above zero.

## Network and dependency checks before cutover

From an Android job pod in `mks-infra`, verify:

- `gitlab.youdo.sg` and GitLab artifacts/API;
- `registry.youdo.sg` image pulls;
- Nexus endpoints used for APK upload and any internal Maven repositories;
- Maven Central, Google Android repositories, and other Gradle dependencies;
- BrowserStack API;
- YouTrack/notification destinations used by repository scripts;
- Huawei, RuStore, and Google Play endpoints used by Fastlane;
- object-storage cache endpoint;
- DNS, TLS trust, NAT/egress, and any required corporate routes.

## Rollout and rollback concept

1. Verify actual `mks-infra` state/quotas and measure current Android job resource
   peaks if monitoring retention permits.
2. Add the dedicated node group in `selectel-tf/prod-mks`.
3. Add namespace, least-privilege RBAC, VSO-managed secrets, and pinned Helm
   release in `infra-tf/prod`.
4. Register a new project runner with a unique tag. Keep the old VM runner
   available.
5. Change all `android-youdo4` jobs to the new tag on a test branch. Exercise the
   feature and regression paths; manual external store publication should be
   runtime-proven only during a legitimate release, not triggered solely as an
   infrastructure test.
6. Validate cold start, job success/artifacts, cache behavior, job cleanup, and
   node-group return to zero.
7. Merge the tag switch, observe several real pipelines, then pause (do not
   immediately delete) the old Android VM runner.
8. Rollback: pause the Kubernetes runner, restore the old tag/runner, and retry
   affected jobs. Do not destroy the node group until rollback observation is
   complete.

## Monitoring and risks

- GitLab queued duration and runner polling failures.
- Kubernetes Pending/unschedulable events and pod startup timeout.
- MKS node-group statuses, provision time, scale-down delay, and project quotas.
- Container image pull duration and failures.
- CPU/RAM/OOM, ephemeral disk usage, Gradle cache hit rate, artifact upload.
- Jobs are not currently rare every day: recent history contains bursts and
  overlapping pipelines. `max=3` is a compatibility ceiling, not a forecast.
- The large Android SDK image and absent node-local cache can materially extend
  the first job after scale-to-zero.
- Manual publish jobs may be started long after their upstream build and will
  cause another cold node start.
- Existing runner inventory contains plaintext access material. Values were not
  copied; migration and rotation should be handled separately.

## Sources checked

- GitLab Runner Helm chart:
  https://docs.gitlab.com/runner/install/kubernetes/
- GitLab Kubernetes executor:
  https://docs.gitlab.com/runner/executors/kubernetes/
- GitLab Helm chart private registry configuration:
  https://docs.gitlab.com/runner/install/kubernetes_helm_chart_configuration/
- Selectel MKS autoscaling and scale-to-zero:
  https://docs.selectel.ru/managed-kubernetes/node-groups/autoscaling/
- Selectel Terraform node-group resource:
  https://docs.selectel.ru/terraform/selectel-provider-reference/resources/mks_nodegroup_v1/

## Open design items

- Exact CPU/RAM requests and limits for heavy, BrowserStack, notification, Nexus,
  and Fastlane jobs.
- Whether the existing S3 cache credentials/backend can be reused directly from
  `mks-infra` and the desired Vault path/role.
- Helm chart/app version pin compatible with the self-managed GitLab instance;
  current GitLab server version still needs verification.
- Expected cold node/image-pull time and required runner `poll_timeout`/
  `pod_pending_timeout`-related settings for the installed Runner version.
- Final tag-switch and production validation window.

## Related

- General architecture and constraints: [`dynamic-kubernetes-runners.md`](dynamic-kubernetes-runners.md).
- Portable lesson: [`~/ai/general/knowledge/gitlab-ci/kubernetes-executor-scale-to-zero-node-group.md`](../../../../../general/knowledge/gitlab-ci/kubernetes-executor-scale-to-zero-node-group.md).
