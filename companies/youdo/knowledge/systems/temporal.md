---
system: temporal
status: hypothesis
checked: 2026-09-08
tags: [temporal, terraform, infra-tf, yandex-dev, kubernetes, postgresql, helm]
---
# Temporal in Yandex dev Kubernetes

Last verified: 2026-09-08. Status: Terraform changes prepared and validated;
not applied to the cluster in this session (hence `status: hypothesis` — the described
topology is the planned/rendered state, not a live-verified one).

## Purpose and ownership

- Temporal provides durable workflow orchestration for development workloads.
- Terraform repository: `/home/slnnk/git/infra-tf`.
- Safe origin: `git@gitlab.youdo.sg:sysadmins/infra-tf.git`.
- Root configuration: `dev/temporal.tf` and `dev/namespaces.tf`.
- Reusable module: `modules/temporal`.
- Terraform state backend: Consul path `terraform/yandex-k8s-dev` at
  `consul.service.selectel.consul:8500`, datacenter `selectel`.

## Dev topology

- Kubernetes namespace: `temporal`, owned by the dev root module and protected
  with `prevent_destroy`.
- Temporal Helm chart: official `temporal` chart `1.6.0` from
  `https://go.temporal.io/helm-charts`; server image version supplied by the
  chart is 1.31.2.
- PostgreSQL: embedded standalone Helm release `temporal-postgresql`, Bitnami
  chart `15.5.38`, PostgreSQL image
  `docker.io/bitnamilegacy/postgresql:16.4.0-debian-12-r14`.
- PostgreSQL service and password Secret: `temporal-postgresql`; Secret key
  consumed by Temporal is `password`. The password is chart-generated and is
  not stored in Terraform configuration/state.
- PostgreSQL PVC: 10Gi, StorageClass `yc-network-ssd`, ReadWriteOnce.
- Databases: `temporal` and `temporal_visibility`, owned by user `temporal`.
  The visibility database is created by the PostgreSQL first-boot init script.
- Temporal chart manages both database schemas but does not create databases.
- Default Temporal namespace retention: 3d; history shards: 512. The history
  shard count is immutable after first deployment.
- Web UI ingress: `http://temporal.dev.youdo.corp`, ingress class `traefik`,
  entrypoint `web`.
- SDK frontend inside the cluster:
  `temporal-frontend.temporal.svc.cluster.local:7233`.

## Reusable module and prod route

`modules/temporal` supports embedded and external PostgreSQL. For production,
set `embedded_postgresql=false`, pre-create both databases, deliver the DB
password to a Kubernetes Secret (normally through Vault Secrets Operator), and
set `postgresql_host`, `postgresql_port`, `postgresql_user`,
`postgresql_existing_secret`, and `postgresql_secret_key`. The external user
must own both databases or have equivalent schema DDL privileges.

## SSO and authorization

- Temporal Web UI supports OAuth2/OIDC SSO. The UI server currently uses only
  the first configured provider. Helm passes configuration through
  `web.additionalEnv`; `TEMPORAL_AUTH_CLIENT_SECRET` should come from
  `web.additionalEnvSecretName` and never from plain Terraform values.
- The browser callback is `/auth/sso/callback` and must exactly match the URI
  registered in the identity provider. Use HTTPS outside disposable local
  environments.
- UI SSO alone is not authorization for the Temporal gRPC frontend. To protect
  SDK/CLI and UI calls consistently, configure Temporal Server ClaimMapper and
  Authorizer/JWT validation (or an approved frontend proxy) separately.
- Current dev module configuration has no SSO and publishes the UI over HTTP.

## Verification performed

- `terraform fmt -check -recursive modules/temporal dev/temporal.tf dev/namespaces.tf`.
- `terraform -chdir=dev validate` with an isolated `TF_DATA_DIR` and backend disabled.
- `helm lint` and `helm template` for both downloaded charts.
- Isolated, local-state `terraform plan -refresh=false` for embedded mode:
  two resources (`helm_release.postgresql` and `helm_release.temporal`).
- Isolated external-mode plan: only `helm_release.temporal`.
- Render checks confirmed PostgreSQL image, generated Secret/key, init SQL,
  10Gi `yc-network-ssd` PVC, both schema containers, and the Traefik ingress.

## Operations and diagnostics

```bash
kubectl get pods,pvc,jobs,ingress -n temporal
kubectl get jobs -n temporal
kubectl logs -n temporal statefulset/temporal-postgresql
kubectl logs -n temporal job/<schema-job-name>
kubectl exec -n temporal deploy/temporal-admintools -- temporal operator namespace list
```

The schema Job name contains the chart version and Helm revision. The first
rendered name is `temporal-schema-1-6-0-1`; discover the actual name with
`kubectl get jobs -n temporal` after every upgrade.

## Risks and next steps

- No `terraform apply` was run. Review the real dev plan against Consul state,
  then apply during an agreed change window.
- The PostgreSQL image is pinned in Bitnami's legacy archive because current
  Bitnami charts use PostgreSQL 18 while Temporal documentation lists active
  test coverage through PostgreSQL 16. Review CVEs and choose a maintained
  PostgreSQL 16 image/chart migration before production use.
- Never change the PostgreSQL major image version against the existing PVC.
  Back up/snapshot first, then use dump/restore or supported `pg_upgrade`.
- Configure a PVC backup/snapshot policy before treating dev workflow history
  as recoverable data.
