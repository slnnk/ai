---
system: dev-deployment
status: verified
checked: 2026-10-15
tags: [buildapi, vk-cloud, vault, nomad, gitlab-ci]
---
# DevOps-898 BuildAPI backend approval and existing Nomad token correction

## Summary

User explicitly approved the reviewed backend changes, four-manifest publication and deployment, then corrected the backend route: use the existing Nomad token rather than creating a new token. The local helper was adjusted and read-only preflight passed. Root executed the approved apply successfully, then published the four-manifest change as MR !40. Application deployment and runtime verification completed successfully.

## Approved final backend effects

`python3 /home/slnnk/ai-data/buildapi-vk/backend_updates.py --apply` now creates only absent Vault role `auth/kubernetes-vk-dev/role/buildapi`, bound to ServiceAccount `default` in namespace `buildapi`, existing policy `buildapi`, TTL 86400, with no audience override. It verifies existing `VK_TEST_NOMAD_TOKEN` from `current/.env` via jobs GET, then replaces only `NOMAD_TOKEN` in `secret/admin/buildapi`, preserving `GITLAB_TOKEN` and every other field. No credential values are recorded.

All Nomad ACL/token write code was removed. The API helper explicitly refuses every Nomad method other than GET. Earlier new ACL policy/client token proposal was never applied and is superseded by the user correction. Role conflict, concurrent secret and read-back checks remain. The existing token stays available in its original credential source even if a Vault write fails; journal contains no secrets or token accessors.

## Checks and files

Python compile and help checks passed. Live default preflight used GET only: existing environment token jobs GET 200; old stored BuildAPI token jobs GET 403; required Vault policy exists and VK buildapi role is absent. Updated local helper and `backend-updates-README.md`; original kubeconfig and repository changes remain untouched by this subtask.

## Context and limits

See [October 14 investigation and release record](2026-10-14-dev-deployment-devops-898-buildapi-vk-kubeconfig.md). Root verified backend apply: VK role created with reviewed bounds/policy/TTL; existing Nomad token jobs GET 200; Vault read-back confirmed only NOMAD_TOKEN replacement, all other fields preserved. No Nomad writes, ACL policy changes or new token creation occurred.

Four-manifest commit `385e9748fd1d248dc1b9dfec212963a80f9e6ad8` (+10/-10) was pushed to approved `DevOps-898-deploy-buildapi-on-vk-k8s`, [MR !40](https://gitlab.youdo.sg/sysadmins/buildapi/-/merge_requests/40) created. User authorized merge/release/deployment sequence; MR !40 pipeline `140931` passed lint `3226666`, kustomize `3226667`, build `3226668`. MR !40 merged as master `9531d9efe2cfc1003412a055732addd08e35b70e`; release tag `0.5.13` was created on exactly that master SHA. Release pipeline `140932` succeeded: lint `3226669`, kustomize `3226670`, build `3226671`, manual `deploy k8s` job `3226672`. The later verified runtime results below supersede the immediate empty pipeline GET. Release CI uses the selected `0.5.13` API/payload image tags, preserving existing latest images. Deployment and application runtime checks passed as recorded below.

This choice to reuse the existing token is specific to this BuildAPI recovery request; it does not establish general authorization to distribute operator tokens or mutate unrelated secrets.

## Verified deployment result (2026-10-15 Europe/Moscow)

Root verified `audit-runtime.json`: five workloads each 1/1 ready, five pods Running/Ready with zero restarts. MongoDB PVC `data-buildapi-mongo-0` is Bound, 2Gi, StorageClass `csi-ceph-ssd-ms1`. BuildAPI VaultAuth is valid; both VaultStaticSecrets are synced/ready. Kubernetes ingress is `10.18.26.60`; primary `http://buildapi.dev.youdo.corp` and direct ingress HTTP checks returned 200, including metrics.

Read-only application-pod checks confirmed VK Nomad jobs GET 200 (45 jobs) with the reused existing token, and Redis SRV `test5.cache.service.vk-test.consul` resolving one record/port 1905 through all three configured resolver addresses. No new Nomad policy or token was ever created. CI kubeconfig, Vault role/secret adaptation, release and application deployment work are complete.

Optional aliases `buildapi.vk-test.youdo.local` and `buildsinfo.vk-test.youdo.local` still follow wildcard Nomad ingress addresses rather than Kubernetes ingress; the user declined additional DNS work on October 15. Primary route works. No DNS mutation occurred; this optional work is cancelled and is not a remaining task blocker. Observations are dated October 15 in Moscow, although some UTC event timestamps fall on October 14.

## User closeout

User declined additional VK alias DNS work. BuildAPI recovery is complete at `http://buildapi.dev.youdo.corp`, release `0.5.13`, verified GitLab deploy job `3226672`. No further infrastructure or DNS investigation is requested.
