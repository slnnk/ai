---
system: sentry
status: verified
checked: 2026-10-02
tags: [sentry, gitlab-ci, youdo.business, sourcemaps]
---
# Sentry: business-frontend sourcemaps blockers

## Task
Frontend asked devops to (1) add CI variable `SENTRY_AUTH_TOKEN` for master builds of `business-web`, (2) fix artifact bundle assembly on `sentry.youdo.com` (project `sentry/business-frontend`, id 45). User asked whether it relates to `youdo.business!3782`.

## Context
- Repo `youdo/microservices/youdo.business`, job `build-business-web` (example job `3198018`, pipeline `139941`, commit `1bbde9ad65`, ref master, success).
- Token pass-through is already on master: `.gitlab-ci.yml:300` `--build-arg BUSINESS_FRONTEND_SENTRY_AUTH_TOKEN="$SENTRY_AUTH_TOKEN"`; `devops/Dockerfile:83,113` reads it via `printenv` only when `CI_COMMIT_BRANCH=master`.
- `!3782` (Site-25569, not merged on 2026-10-02) has identical lines there; the blockers do not depend on it.
- `YouDo.Business.Web/spa/vite.config.ts`: `@sentry/vite-plugin ^5.4.0`, enabled only with a token; upload errors are logged, build exits 0, assemble is not polled. Adding the token cannot break the build.

## Actions
- GitLab API GET: project variables, groups `youdo`, `youdo/microservices`, instance (`/admin/ci/variables`).
- `getent hosts sentry.youdo.com` -> `91.206.127.88`, `/api/0/` -> 200.

## Findings
- `SENTRY_AUTH_TOKEN` exists at no level (project, both groups, instance). Only `*_FRONTEND_SENTRY_DSN` vars exist (unprotected, unmasked). Blocker 1 confirmed.
- `master` is a protected branch, so a protected variable reaches master builds.
- Live `sentry.youdo.com` runs in k8s cluster `mks-infra` (context `admin@mks-infra`), namespace `sentry`, Helm chart `sentry` `27.6.2` (app 25.9.0) from `infra-tf/prod/sentry.tf`, values `infra-tf/prod/config/sentry-values.yaml`. The deleted Yandex VM `sentry-prod01` is unrelated.
- Root cause of blocker 2 (assemble -> `{"state":"error","detail":"internal server error"}`), verified from manifests: `filestore.backend: filesystem` with PVC `sentry-data` (10Gi, RWO, `fast.ru-2c`, cinder) mounted only into `sentry-web` at `/var/lib/sentry/files`; `sentry-worker` gets `emptyDir` at the same path, because chart default `filestore.filesystem.persistence.persistentWorkers: false`. Web stores uploaded chunks on the PVC; `assemble_artifacts` runs in the worker and cannot see them. The chart comment itself says private source maps need `persistentWorkers`.
- Worker logs and `exec` into prod pods were blocked by the agent permission classifier; confirm the traceback with `kubectl --context admin@mks-infra -n sentry logs deploy/sentry-worker --since=48h | grep -i -A5 assemble`.
- Web and worker run on different nodes (`mks-infra-node-3n5k3`, `mks-infra-node-r0d48`); only cinder RWO classes exist (`fast.ru-2`, `fast.ru-2c`), no RWX. `persistentWorkers: true` mounts the claim into 29 templates (worker, cron, consumers), so with RWO it causes Multi-Attach unless every pod sits on one node.
- S3 buckets are not managed in `selectel-tf` (master `0d44d8c`: only `ansible_host`/`ansible_group`/`postgresql_*` resources) nor anywhere in `infra-tf`; existing Selectel buckets `youdo-loki`, `youdo-tempo` (endpoint `https://s3.gis-1.storage.selcloud.ru`, region `gis-1`, path-style) are referenced only in Helm values, so they were presumably created in the Selectel panel (hypothesis).
- Credential pattern to reuse: `infra-tf/prod/loki.tf` — `VaultAuth` (mount `kubernetes-infra`, role `resources`) + `VaultStaticSecret` `loki-s3-secrets` from Vault kv-v1 `secret/resources/s3selectel`. For Sentry: same in namespace `sentry`, then `filestore.s3.existingSecret` with `accessKeyIdRef`/`secretAccessKeyRef` set to that secret's key names (not read).
- Chart 27.6.2: `filestore.*` is global — `filestore.backend`/options go into the shared `config.yml`/`sentry.conf.py` ConfigMap, and S3 keys from `filestore.s3.existingSecret` are injected by helper `sentry.env` into 32 templates (web, worker, worker-events, worker-transactions, cron, cleanup, ingest consumers, hooks). Switching to `s3` drops PVC `sentry-data` from the release (`pvc.yaml` renders only for `filesystem`, no `helm.sh/resource-policy: keep`), so Helm deletes it and its files — back it up first.
- Filestore contents on 2026-10-02: PVC `sentry-data` 13M used of 9.8G (`df`/`du` in `sentry-web`). Postgres `sentry`: `sentry_file` has only 3 rows of type `artifact.bundle` (2026-09-17, size NULL = the failed manual uploads); `sentry_fileblob` 0 rows, `sentry_artifactbundle` 0, `sentry_projectdsymfile` 0. Nothing worth migrating; PVC can be dropped when switching to S3.
- `sentry-worker` logs start at 2026-10-02 15:51Z (rotated), so the 17.09 traceback is gone; reproduce one upload and read logs right after. No separate taskworker deployment; assemble runs in `sentry-worker`.
- Access: project `.claude/settings.local.json` allows `kubectl --context admin@mks-infra -n sentry exec|logs` for the agent (user-approved 2026-10-02).
- Fix options: (a) recommended: `filestore.backend: s3` with Selectel S3 bucket, `filestore.s3.existingSecret` (keys `s3-access-key-id`, `s3-secret-access-key`), `endpointUrl`, `bucketName`; existing PVC files (attachments, debug files, release files) are not migrated automatically. (b) quick: `persistentWorkers: true` + affinity pinning web/worker/cron/consumers to one node; fragile.
- Also likely affected: anything assembled in the worker from chunks (debug information files, e.g. mobile dSYM/ProGuard) (hypothesis).

## Changes
- `infra-tf` branch `sentry-filestore-s3` (from `origin/master` `106891c`, uncommitted): `prod/sentry.tf` adds `VaultAuth` `sentry/resources` (mount `kubernetes-infra`, role `resources`) and `VaultStaticSecret` `sentry-s3-secrets` (kv-v1 `secret/resources/s3selectel`, keys `aws_access_key_id`/`aws_secret_access_key`); `module.sentry` depends on it. `prod/config/sentry-values.yaml`: `filestore.backend: s3`, bucket `youdo-sentry` (created by user 2026-10-02), endpoint `https://s3.gis-1.storage.selcloud.ru`, `region_name: gis-1`, `addressing_style: path`.
- Checks: `terraform fmt` clean; `terraform validate` OK on a scratch copy (`init -backend=false`); `helm template` of chart 27.6.2 renders `filestore.backend: "s3"`, S3 env refs in all Sentry pods, no `sentry-data` PVC.
- User pushed it as `sysadmins/infra-tf!175` (commit `d330906`); CI `plan:prod` job `3202326` (pipeline `140032`): `Plan: 2 to add, 1 to change, 0 to destroy` — the two VSO manifests plus in-place `module.sentry.helm_release.sentry`; values diff vs deployed revision 47 is only the `filestore` block. User confirmed bucket region `gis-1` and `s3selectel` access to `youdo-sentry`.
- Gotcha: `prod` provider uses `~/.kube/config` current-context, which on this workstation is `yc-kube-test-temp`, not `mks-infra`; local plans need `-var kubeconfig_path=<minified admin@mks-infra kubeconfig>`.
- Applied by user 2026-10-02 (Helm revision 48 `deployed`, 16:50Z start): `sentry-s3-secrets` created, PVC `sentry-data` deleted, web/worker have S3 env, worker `get_storage()` = `S3Boto3Storage youdo-sentry`, read-only `exists()` OK; hook `sentry-kafka-provisioning` took 10+ min; after rollout 60 Running / 13 Completed, no restarts; `/api/0/` and `/_health/` 200. End-to-end sourcemap upload not yet tested. System map: [sentry](../systems/sentry.md).
- 2026-10-02 evening: user created GitLab var `SENTRY_AUTH_TOKEN` in `youdo.business` (protected, masked, scope `*`, Sentry org token) and merged `infra-tf!175` (merge commit `513089ba`). Token lists `/projects/sentry/business-frontend/files/artifact-bundles/` (0 bundles yet); `/organizations/sentry/` returns 403, expected for an org:ci token. Last master `build-business-web` before the var: job `3202189` (`64f9e087`).
- End-to-end verified 2026-10-02: master pipeline `140035` (`64f9e087`), job `build-business-web` `3202381`: 62 chunks with `map:`, plugin output `Upload type: artifact bundle`, Bundle ID `edaa301c-9554-57f3-9ddd-c60fd1e7480b`, release = commit SHA; token not present in the job log. Sentry API lists the bundle (124 files, 2026-10-02T17:17:58Z). `business-web-gates` is only lint + tests, unrelated to Sentry. Absence of `.map` in the final image not checked.
- Prerequisites not verifiable by the agent: Vault role `auth/kubernetes-infra/role/resources` is not in terraform (used by namespaces `alloy`, `loki`, `monitoring`), verified by user in Vault UI (`vault.service.selectel.consul:8200`) on 2026-10-02: `bound_service_account_names: *`, `bound_service_account_namespaces: *`, so namespace `sentry` can log in, and the role already reads `secret/resources/s3selectel` for Loki; the `s3selectel` S3 user must have access to `youdo-sentry`; bucket region assumed `gis-1`.

## Open items
See `~/ai/TODO.md` section sentry.

## Portable lesson
[Sentry Helm: artifact assemble fails with filesystem filestore](../../../../general/knowledge/sentry/helm-filestore-worker-emptydir.md)
