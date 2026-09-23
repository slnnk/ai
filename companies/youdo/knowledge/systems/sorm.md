---
system: sorm
status: verified
checked: 2026-09-22
tags: [sorm, production-readiness, nomad, rabbitmq, kafka, ftp, vault, gitlab-ci-templates, DevOps-767]
---
# YouDo SORM: production-readiness map

- Checked: 2026-09-22
- Repository: `/home/slnnk/git/sorm`
- Safe origin: `git@gitlab.youdo.sg:youdo/microservices/sorm.git`
- Branch/commit observed: `DevOps-767-prod`, `2220503b6f2b67801db3f75d56c779609476c9f4`
- Scope: repository-based readiness review; no live production systems were queried.

## Runtime route

RabbitMQ live vhost and optional historical/migration vhost → durable `youdo.sorm.*` queues → PostgreSQL inbox and domain tables → batching/outbox → Kafka topics. Media URLs from events are downloaded directly over HTTP(S), packed under local `/tmp`, uploaded atomically as `/content/<id>.dat.tmp`, then renamed to `.dat` on the ORI FTP server.

GitLab CI includes shared `v3` .NET/deploy templates. It builds separate `service` and `migrations` images. Production is described by `devops/production.hcl`: Nomad job `youdo-sorm`, three Docker allocations, Vault policies `resources` and `dotnet`, 1024 MiB reserved/2048 MiB max memory each; no explicit CPU allocation is currently set. The working tree selects the new shared manual template `v3/.deploy-prod-svc-migrations.yml`, which stops `svc`, runs pre-migrations, performs the standard Nomad update, and starts `svc` again.

## External resources and access

- PostgreSQL database `sorm` on the same managed C2C PostgreSQL cluster used by Attribution. Production obtains `managed_host_c2c`, `managed_port_c2c` and the shared `youdo` credential from Vault `secret/resources/databases/postgres`; the connection string uses `SSL Mode=Disable`. Operator confirmed on 2026-09-22 that the database has been created and the required access granted. Deployment still needs a compatible migration job and operational backup/restore coverage.
- RabbitMQ: live `/` and historical `SormProd` vhosts in the current production HCL, both on `rabbit-cls.youdo.local:5672`. Exchanges must already exist because exchange declaration is commented out; the service declares durable, non-auto-delete `youdo.sorm.*` queues and bindings. Code contains 55 unique queue definitions and 24 unique source exchanges: the live connection registers 52 consumers and needs all 24 exchanges, while the historical connection registers 30 consumers and needs the 7 C2C exchanges (`youdo.events`, `youdo.escrow`, `youdo.pack`, `youdo.finance.user.transactions`, `youdo.chat.broadcast`, `youdo.user.signin`, `youdo.user.signout2`). Account `youdo` needs access to both vhosts and permissions sufficient to declare/consume the queues and bind them to the source exchanges. Three service replicas become competing consumers on the same queues within each vhost.
- Kafka: ten logical topics from `TopicName`: `Aaa`, `Connection`, `Users`, `DictTelcos`, `DictServices`, `DictEvents`, `DictResources`, `DictUserTypes`, `DictPaymentServices`, `Data`, unless overridden with `Kafka__TopicNames__*`. Code calls `CreateTopicIfNotExists`; grant create/describe/write or pre-create topics and restrict ACLs accordingly. Confirm topic naming, partition count/order policy, retention and broker message-size settings with the receiver.
- ORI FTP: host/port/user/password supplied from Vault; account needs list/existence checks, create `/content/*.tmp`, rename, and delete temp files. Verify passive ports/firewall, capacity/quota and receiver-side cleanup/log access. Current client is FluentFTP, not SFTP despite some documentation wording.
- HTTP(S): allocations need DNS/routes/egress to every media/CDN URL carried by events.
- Observability: Prometheus exporter listens on 9464. OTel traces are configured for `http://tempo.service.consul:55681/v1/traces`; Sentry requires DSN/egress.

On 2026-09-22, `OTEL_EXPORTER_OTLP_ENDPOINT=http://tempo.service.consul:55681/v1/traces` and explicit `RabbitMqMigration__Enabled=true` were added to `devops/production.hcl`, bringing its application environment variable set in line with `devops/config.yml`. Infrastructure-level `service_cpu: 100` still has no matching `cpu` entry in the production resources block. Test-only `pre_migrations*`, `db_*`, `recreate_db`, `service` and `service_check` keys are deployment-generator controls rather than application environment variables and do not map one-to-one into Nomad HCL; production migrations are nevertheless missing as described below.

## Vault contract from production HCL

- `secret/resources/databases/postgres`: `managed_host_c2c`, `managed_port_c2c`, `youdo_password`; used to construct `ConnectionStrings__DefaultConnection` with database `sorm`.
- `secret/dotnet/sorm`: `sentry_dsn`, `sftp_host`, `sftp_port`, `sftp_username`, `sftp_password`. The former `conn_string` key is no longer consumed by the service job.
- `secret/resources/kafka`: `broker` (only one broker key is currently rendered).
- `secret/resources/rabbitmq`: `youdo_password`; username and broker hostname are hardcoded in the HCL.
- Operator confirmed on 2026-09-22 that production Vault policies/paths/required keys and the protected GitLab variables used by production migrations were checked and are ready. Treat the Vault readiness item as complete; do not record secret values.
- Do not copy secret values to Markdown. Repository-tracked test configuration currently contains plaintext credentials/DSN and must be removed and rotated before release.

## Deployment gaps/blockers found

1. A shared manual production template `v3/.deploy-prod-svc-migrations.yml` was prepared in local `gitlab-ci-templates`: stop `svc` → one pre-migration job → standard Nomad update → start `svc` at `DEPLOY_PROD_SERVICES_COUNT` → rollback. It follows the existing manual-template convention and only composes hidden jobs from `v3/.deploy-prod.yml`; no custom `needs`, `dependencies`, failure-policy override, or Nomad command override remains. There is no canary or post-migration phase. SORM now includes that template. Its migrations image has a project-specific `devops/migrations.sh` entrypoint consuming the standard `DB_SERVER`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` contract and invoking FluentMigrator explicitly with `--Direction Up`; both test and production deploy templates provide those variables. Test deployment history also confirmed the former generic-entrypoint path worked for version `0.0.7`, but the new contract removes reliance on implicit enum defaults. `Direction=Down` calls `MigrateDown(0)` and must not be used as a normal release rollback. The shared-template change must be merged/published before the SORM include can resolve in GitLab CI.

   Test verification on 2026-09-22: GitLab job `3170494` in pipeline `139263`, commit `338d136d60cdfc0167ae0d63921db753cb303ad2`, successfully deployed image tag `devops-767-prod-139263` to Nomad job `youdo-sorm-test9`. Allocation `b600c389-c8ec-7a81-6cce-cdde1811c3de` shows `youdo-sorm-premigrations-test9` terminated with exit code 0 and `Failed=false`; the service task then started and remains running. Nomad marked deployment `7cab7ec9` successful with one healthy allocation. This verifies the new migrations image and `DB_*` entrypoint on test; it does not yet verify the new production template.
2. Nomad exposes only port 9464 (Prometheus listener) and registers it in Consul. ASP.NET `/health/live` and `/health/ready` are on the Kestrel listener, but no Kestrel port is mapped and Nomad uses `health_check = "task_states"`; the orchestrator therefore does not use application readiness. On 2026-09-22 the operator explicitly excluded health-check implementation from the infrastructure/deployment work: this remains a development-team debt and is not a blocker for the current production rollout preparation.
3. `RabbitMqMigration:Enabled` is explicitly set to true in the production HCL, so every production allocation will consume both live and historical vhosts immediately. Coordinate backlog loading and producer rollout; disable it if the historical feed is not meant to start with the live service.
4. Application code declares 55 queues/bindings but deliberately does not declare RabbitMQ exchanges. All 24 referenced C2C/B2B exchanges must exist with compatible types before service start.
5. No production alert rules are present for inbox backlog, `GaveUp`, outbox failures, pending correlations, consumer errors, DB saturation, RabbitMQ queue depth, Kafka publish failure, FTP failure, or allocation restarts. Dashboard files are development assets, not proof of production monitoring.
6. Product/contract acceptance is incomplete per `docs/implementation-checklist.md`: unresolved Kafka `Data` vs `Connection`, message key/partitioning, dictionary record format and resource code 16, historical three-year run, retention/erasure policy, FTP receiver logs, and several payload-format/completeness questions.
7. Known correctness risk `docs/known-issues/2026-09-22-edit-data-out-of-order.md`: late edit events can roll saved resource state backward.
8. `FilePackUploadService:SkipUnavailableContent` defaults false; old/unavailable CDN objects can exhaust inbox attempts and become `GaveUp`. Product and receiver must decide whether production sets it true.
9. The production job has no explicit disk/ephemeral-space sizing or monitoring for `/tmp`, where content is downloaded and packed.
10. Current resource sizing has no load-test evidence; the three-year historical migration has not been proven at production-like volume.

## Release gate

For the infrastructure/deployment scope: the shared CI template is published and SORM pipeline `139263` verified both images plus the changed migration contract on test. Next validate the rendered production Nomad job and required Vault keys; confirm RabbitMQ exchanges/permissions, Kafka access/topics, FTP access and network routes; then create the production semver tag and execute the existing manual jobs in order: stop services, pre migrations, update, start three services. Verify Nomad allocations, migration logs, service logs and the expected queue/topic/FTP activity. The existing manual-template convention does not enforce job order with `needs`; operators must run the numbered manual jobs in sequence. Application liveness/readiness integration is explicitly outside this infrastructure task and remains with developers.

## Verification limitation

The repository could not be built locally during this review because the host has no `dotnet` executable. The latest repository checklist records a prior successful test run, but it is not evidence for the current commit; require a green current GitLab pipeline before release.

## Related log entries

- [`../log/2026-09-22-rabbitmq-config-migration.md`](../log/2026-09-22-rabbitmq-config-migration.md): RabbitMQ node `rabbit@sorm-rabbitmq` on `172.28.0.186` (vhost `sorm`).
