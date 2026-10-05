---
system: sentry
status: verified
checked: 2026-10-02
tags: [sentry, k8s, mks-infra, infra-tf]
---
# Sentry (sentry.youdo.com)

## Summary
Self-hosted Sentry 25.9.0 in k8s cluster `mks-infra`, namespace `sentry`, Helm chart `sentry` `27.6.2`, deployed by `infra-tf/prod` (`prod/sentry.tf`, values `prod/config/sentry-values.yaml`). Filestore is Selectel S3 bucket `youdo-sentry` since 2026-10-02 (Helm revision 48, `infra-tf!175`). The old Yandex VM `sentry-prod01` was deleted 2026-09-17 and is unrelated.

## Access
- kubectl context `admin@mks-infra`; this workstation's default current-context is `yc-kube-test-temp`, so local `terraform plan` in `infra-tf/prod` needs `-var kubeconfig_path=<minified admin@mks-infra kubeconfig>`. CI job `plan:prod` in `sysadmins/infra-tf` runs plans.
- Terraform state: Consul `consul.service.selectel.consul:8500`, path `terraform/selectel-k8s-infra`, token `CONSUL_HTTP_TOKEN` in `current/.env`.
- Vault UI `vault.service.selectel.consul:8200`; k8s auth mount `kubernetes-infra`, role `resources` (bound SA names `*`, namespaces `*`; not in terraform).
- Postgres: pod `sentry-sentry-postgresql-0`, db `sentry`, user `postgres`, password in pod env `POSTGRES_PASSWORD`.

## Filestore
- `filestore.backend: s3`, bucket `youdo-sentry`, endpoint `https://s3.gis-1.storage.selcloud.ru`, region `gis-1`, `addressing_style: path`.
- Keys: `VaultStaticSecret` `sentry-s3-secrets` (kv-v1 `secret/resources/s3selectel`, keys `aws_access_key_id`/`aws_secret_access_key`, shared with Loki/Tempo) via `VaultAuth` `sentry/resources`; chart injects `S3_ACCESS_KEY_ID`/`S3_SECRET_ACCESS_KEY` into all Sentry pods.
- Why not filesystem: chart mounts the filesystem PVC only into web unless `persistentWorkers: true`; worker got `emptyDir`, so `assemble_artifacts` (sourcemaps, debug files) always failed. Only RWO cinder classes exist (`fast.ru-2`, `fast.ru-2c`).
- Read-only S3 check: `kubectl --context admin@mks-infra -n sentry exec deploy/sentry-worker -- sentry exec -c "from sentry.models.files.utils import get_storage; s=get_storage(); print(s.bucket_name, s.exists('x'))"`.

## Upgrade behaviour
- `helm_release` upgrade stays `pending-upgrade` for 10+ min while post-upgrade hook `sentry-kafka-provisioning` runs `kafka-topics.sh --create --if-not-exists` for 106 topics sequentially (one JVM each). Normal.
- A change in `config.yml` restarts nearly every Sentry pod (checksum annotation); expect a transient wave of Pending/ContainerCreating after the hook.
- `sentry-worker` logs rotate within hours; reproduce a problem and read logs right away.

## Projects
- `sentry/business-frontend` (id 45): LK UL frontend; sourcemaps uploaded as artifact bundles by `@sentry/vite-plugin` in job `build-business-web` of the `youdo.business` master pipeline, CI var `SENTRY_AUTH_TOKEN` (protected, masked, org token). Working since pipeline `140035` (2026-10-02). See [log](../log/2026-10-02-sentry-business-frontend-sourcemaps-blockers.md).
