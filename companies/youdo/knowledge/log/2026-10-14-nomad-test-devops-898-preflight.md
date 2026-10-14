---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [nomad, vk-cloud, gitlab-ci, recovery]
---
# DevOps-898 read-only VK service deployment preflight

## Summary

The initial preflight found missing images/authentication and stale backend addresses for thirteen candidates. Those launch prerequisites were resolved for the final user-approved target: ten single services and LogReader test5 are deployed through GitLab and runtime-verified. Socket was corrected to per-stand delivery and its CI restored; unused vks-policy-generator was excluded. Public-test remains unchanged. Full sixteen-stand LogReader acceptance still depends on the other fifteen SQL stands. See [final launch evidence](2026-10-14-nomad-test-devops-898-implementation.md#verified-final-launch-scope-2026-10-14); observations below preserve the historical preflight.

## Task and context

Source: [DevOps-898](https://youtrack.youdo.com/youtrack/issue/DevOps-898). [Implementation plan](2026-10-14-nomad-test-devops-898-single-dynamic-plan.md). User requested step1, then explicitly requested adding NOMAD_TOKEN_VK_TEST and CONSUL_TOKEN_VK_TEST to youdo. User confirms mssql-test5 deployment already verified and should generate the correct address; do not reopen its producer recovery without contrary evidence.

## Actions and commands

Read-only GitLab GET project/group variables, ancestry, runners, current template source and service HCL; Nomad nodes/jobs/allocation details; Consul catalog/health/KV; Vault secret schema/policies. SSH read-only DNS/TCP checks from runner hosts172.28.0.171/.172 and Nomad client01 10.18.26.34. Registry HEAD/GET manifest/tag checks; no pulls, CI runs, new workloads, token issuance or restarts. Existing local probe helpers inspected before adapting.

Local helper directory: /home/slnnk/ai-data/DevOps-898/scripts. Sanitized evidence directory: /home/slnnk/ai-data/DevOps-898. No credential values persisted.

User-authorized publication: copy_ci_variables.py --apply GETs sysadmins group3 and youdo group8, copies only the two approved masked/unprotected/scope* token variables, refuses differing existing values, then GET-verifies equality and API access. Both creates and equality checks succeeded; local report formatting subsequently failed on null Policies. Corrected null handling and reran; both already equal, no second mutation. Final artifact ci-variables-copy.json confirms Nomad ACL HTTP200/management and Consul ACL HTTP200/global-management.

## CI and runner findings

All13apps inherit youdo, not sysadmins. Before the approved copy, no VK tokens existed in youdo or intervening microservices/vsk/mail groups or project overrides; thus the original assumption of app inheritance was wrong. Both approved variables now reside at group youdo, masked=true, protected=false, environment_scope=*. No secret values were printed. Old Yandex variables remain untouched. No VK Nomad address alias existed at preflight; planned nonsecret explicit address is valid.

All13projects enable instance/shared runners. Docker runners105/106 are online/unpaused and available for unprotected jobs. Both hosts resolve all3VK Nomad masters and GET leader succeeds. Docker configured resolvers172.28.0.8/.9 return NOERROR for VK Nomad. This proves host/configured-resolver path, not fresh job-container network execution; no shared docker run/exec was authorized or performed.

NOMAD_IP_ADDR project overrides in call-service/textvalidation/mailer are legacy non-VK values with no direct consumers in their CI/devops files or local shared-template tree; do not replace unused keys blindly. Remote template master is6d9b6955a2c77369813136fde1875fee565fdd82; local clean checkout69cec4d is stale, so refresh before implementation. All13 includes are unpinned. Global/group GitLab code search GET returns400 (scope does not have a valid value); consumers outside these13 remain unverified, requiring impact inventory before publication. NEXUS_PUBLIC_HOST=nexus.youdo.com, NEXUS_HOST=msk3-nexus.youdo.corp.

## Platform and capacity findings

8/8nodes ready, eligible, undrained in vk-test;24runningjobs,62runningallocations; target13applications absent. Vault initialized/unsealed/active1.21.4. Consul93passingchecks,0warning,1critical. The critical check is unrelated external elasticsearch on10.18.26.32:9201; TCP refused. elastic-b2b on the same host9200 is passing/open. This does not block DebuggingEvents companion Elasticsearch, which is inside its own job.

Scheduler capacity260144MHz CPU/514400MiB RAM; allocated18820MHz/43772MiB; unreserved headroom241324MHz/470628MiB. Target steady reservations31800MHz/54016MiB, conservative lifecycle32120MHz/55652MiB, including16Socket/LogReader stands, Socket two tasks per stand, mailer10schedulers+10dispatchers. Aggregate reservations fit comfortably; this is not a placement plan, real usage or filesystem-free-space check.

## Backend findings

Nomad client01 resolves/reaches Nomad4646, Consul8500, Vault8200, registry443, Nexus443, DockerHub443 and external Yandex S3443. PostgreSQL10.18.26.39:5432 and b2b10.18.26.44:5432, Kafka10.18.26.5:9092, all16Redis ports and all3Traefik endpoints are reachable. PostgreSQL5433 is also open now, superseding older refusal observations; service catalog still advertises5432. TCP is not application login or schema acceptance.

mssql-test5 is running; service sql-test5.service.vk-test.consul on10.18.26.35:14305 is passing and TCP open from client01. User confirms deployment accepted; do not repeat MSSQL recovery. All16 test_instances/<stand>/mssql_db keys exist and are nonempty. LogReader uses each key as Data Source (server address), with USER/PASSWORD from Vault and fixed Initial Catalog=YouDoLogsExceptions; it does not use the shared LOGREADER_CONN_STRING.

All8referenced Vault paths/observed required field names exist. Stale values remain: secret/resources/rabbitmq ADDR=rabbitmq.service.yandex-test.consul:5672 (DNS fails from client01); candidate VK rabbit host10.18.26.7:5672 refuses TCP and has no rabbitmq service registration. call-service/mailer/Socket depend on this broker. Shared MSSQL LOGREADER_CONN_STRING points to sql-test.ru-central1.internal:1433 (DNS fails from client01), affecting geocoder/mailer logging. textvalidation HCL96 and DebuggingEvents HCL66 hardcode the same obsolete MSSQL host. PostgreSQL Vault ADDR retains yandex-test DC alias but resolves/reaches VK10.18.26.39:5432; migrate spelling to avoid old DC reliance.

DebuggingEvents includes its own elasticsearch:7.17.14 task3072MiB, so old debuggingevents-elastic-master.yandex-test.youdo.local must point to its own new VK route; no separate ES recovery is implied. Generated configuration bind mount only; no persistent data volume in this HCL. Doc-generator/chat-content still consume external Yandex S3; object storage migration is outside this domain/CI task. Socket uses external https://<stand>.youdo.sg; readiness of external API/SMTP/iDigital and dependencies inside images is unverified.

## LogReader SQL consumer and Vault policy follow-up

All16SQLkeys parsed after correcting whitespace-after-comma handling. test5 key sql-test5.service.yandex-test.consul,14305 resolves10.18.26.35 and TCP opens from client01, matching the accepted producer. The key still spells the old DC alias; functionality is verified, spelling migration remains distinct. All15other SQLtargets fail DNS/TCP at this observation; no conclusion that the verified test5producer is broken. Policies dotnet/resources GET-confirmed and grant read on secret/dotnet/* and secret/resources/*, covering all8required paths. Per-allocation issuance awaits actual deployment. Evidence logreader-sql-preflight.json and vault-policy-preflight.json.

## Image findings

All13HCL have no explicit Docker auth blocks. All8Nomad clients use /root/.docker/config.json with registry.youdo.sg auth only; no nexus.youdo.com auth. Anonymous Nexus manifest HEAD401 Basic. Using existing private Nexus reader credential,20unique app component latest manifest HEAD404 and tags/list GET200 returns empty tags[] at all20expected paths; this API does not distinguish absent repositories from empty ones. Current remote templates lowercase NEXUS_PUBLIC_HOST/CI_PROJECT_PATH. APP_IMAGE_TAG is CI_COMMIT_TAG, else master-CI_PIPELINE_IID for auto/master, otherwise CI_COMMIT_REF_SLUG-CI_PIPELINE_ID. latest is baseline only; no deployment release tag selected. DockerHub elasticsearch:7.17.14 manifest is available200 from client01. GitLab alternative registry inventory denied403; no alternate image availability claim. Do not trigger builds or modify auth under this preflight authorization.

## Changes, approvals and risks

External: only the two user-requested youdo group variables created. No branch changes, repository edits, merge/push/MR, pipelines or runtime deployments. Local: log, plan correction, canonical map, address map observation comments and backlog; sanitized operational helpers/evidence outside git. Further required work is tracked only in ~/ai/TODO.md. Public-test untouched. Application rollout cannot be accepted until images/auth, RabbitMQ and necessary SQL consumers are addressed; successful infrastructure probes alone do not imply all13services ready.

## Portable lesson

none
