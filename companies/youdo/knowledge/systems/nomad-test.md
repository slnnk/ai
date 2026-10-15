---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [nomad, consul, terraform, vk-cloud, recovery]
---
# Nomad test platform and VK recovery

DevOps-898 TKB master-267 rollout blocked: all six Nomad jobs dead; worker Hangfire startup fails PG authentication on B2B PgBouncer5433. Empty authfile/database mappings confirmed on10.18.26.44; ordinary migrations use direct5432 and complete. No repository fix needed. User-approved sixDB/user configuration applied with reload only/PID43719 unchanged; all6DB SELECT1 pass on5432+5433 using actualworkercredentials. User-approved ordinary retries3230094–3230099 completed all6SUCCESS on test10–test15; Nomad master-267 running/healthy/restarts0 at2026-10-15 21:06UTC. [Evidence](../log/2026-10-15-postgresql-devops-898-tkb-pgbouncer-auth-failure.md).

## Summary

- DevOps-893 restored the Terraform-managed test services in VK Cloud and was closed by the user on2026-10-13.
- Repository: ~/git/terraform, approved branch DevOps-893-recover-nomad-on-vk.
- Separate root vk-test; Consul state terraform/vkcloud-terraform.
- Eight ready clients; deployed Traefik3/3, Redis16/16 and Jaeger8/8.
- Consul exporter, Kafka Schema Registry and Alloy traces are deployed and checked.
- Current endpoints and observation evidence live in current/service-addresses.env.
- User excluded test16/test17, redis-autotest and unused local job files.
- All3master Vault tokens were synchronized from secret/ansible/yandex and reloaded.
- Fresh master-token checks200; main Alloy8/8running verifies task Vault startup/rendering.
- All8configuredjobs deployed; CSI8healthy nodes/controllers after command correction.
- SSD lifecycle verified: ceph-ssd 1 GiB, ext4, write/read SHA-256, detach and delete; no temporary resources remain.
- Older paragraphs below retain historical recovery findings; dated updates supersede them.
- Deployment evidence, approvals and limitations are in the linked work logs.

## BuildAPI Kubernetes recovery follow-up (2026-10-14)

User requested BuildAPI restoration in VK Kubernetes rather than the historical Nomad CSI job. Existing cluster access, published CI image and scoped Terraform-identity CI kubeconfig are verified. Approved Vault backend role/token endpoint change passed using existing VK token, with no Nomad writes. Four-manifest MR !40 merged; release pipeline 140932/manual Kubernetes deploy 3226672 passed. Five workloads ready, MongoDB PVC Bound, primary BuildAPI route HTTP 200, pod Nomad jobs GET 200 and Redis SRV checks passed. User declined optional VK alias DNS work; no DNS changes were made and BuildAPI recovery is complete. See [BuildAPI access and CI image preparation](../log/2026-10-14-dev-deployment-devops-898-buildapi-vk-kubeconfig.md).

## DevOps-898 final approved launch completed (2026-10-14)

Ten single services and the explicitly limited LogReader test5 pilot are deployed through GitLab and runtime-verified: doc-generator master-137, DebuggingEvents 1.0.85, geocoder 1.2.12, call-service 0.0.9, chat-content 1.1.16, textvalidation 1.0.4, tinkoff 0.0.10, blec 1.0.2, pechkin 2.14.24, mailer 8.1.10 and LogReader 1.0.39. Service allocations run with expected versions; configured health checks pass where defined. Blec has no configured health check and its root route returns 404. LogReader has exactly one test5 group, HTTP 200, passing Consul and verified SQL SELECT 1 using its HCL Vault credentials. Test5 Consul SQL endpoint alone was updated by approved CAS. Other fifteen SQL stands remain a separate backlog dependency; full sixteen-stand acceptance is not claimed.

Socket is per stand and excluded from this rollout after the user's correction; reverse MR !82 merged into master 7f6d81b3 restores its original CI. User excluded unused vks-policy-generator and explicitly closed MR !18 without merge, new tag or deployment. Optional chat cache changes were not implemented; its new release build succeeded. Public-test remains unchanged. No YouTrack closure was performed. [Final launch versions, evidence and limits](../log/2026-10-14-nomad-test-devops-898-implementation.md#verified-final-launch-scope-2026-10-14). Historical progress sections below retain their dated observations.

## DevOps-898 GitLab rollout and Socket scope correction (2026-10-14)

Doc-generator is deployed through GitLab job 3226189 from pipeline 140895 with image `master-137`; Nomad job version 1, running allocation, Consul checks and configured HTTP health check pass. Its separately authorized production child pipeline 140898 succeeded. DebuggingEvents API and companion Elasticsearch are running from the initial approved direct deployment; TCP checks pass and Elasticsearch is green. GitLab deployment verification for DebuggingEvents remains pending.

Nine authorized release pipelines 140901–140909 cover geocoder, call-service, blec, mailer, LogReader, chat-content, tinkoff, vks-policy-generator and pechkin. Seven have ready manual VK jobs, no production jobs are active. Chat-content timeout and vks-policy-generator buster apt failures remain unresolved. Nexus nginx now whitelists VK gateway `10.18.20.3/32`; test/reload passed, observed HTTP 429 stopped and fresh NuGet restores pass.

The user requires Socket deployment per stand and cancelled its dynamic-mode change. Approved reverse branch `DevOps-898-restore-per-stand-socket-deploy` restores the original CI byte-for-byte; publication and merge remain pending. Remote Socket master still contains MR !81. The general manual-master shared-template proposal was rejected. Textvalidation local production-rule overrides were cancelled with no publication; explicitly requested new tag `1.0.4` was created at master `1fa42397` for standard manual release CI, with pipeline results pending. Public-test remains excluded. RabbitMQ retains old credentials on its new VM; other fifteen SQL stands still prevent full LogReader acceptance. [Current implementation and approvals](../log/2026-10-14-nomad-test-devops-898-implementation.md).

## Single and dynamic configuration merged; build preparation (2026-10-14)

DevOps-898: all four approved MRs merged (templates !88/master cda625bd, Socket !81/master 8b3912d8, DebuggingEvents !8/master 642d8dfa, textvalidation !37/master 1fa42397). Five CI lint checks passed, including preservation of Socket public-test behavior. RabbitMQ 3.8.34 runs with the old Vault login/password and 17 vhosts; Consul DNS and checks pass. Approved Vault endpoint changes preserve other fields. Test5 logging credentials passed SELECT 1. All 21 approved preparation retries are terminal: 13 set-variables and two prepare-nuget succeeded; six prepare-nuget failed with HTTP 429 under investigation. Seven separately approved release/master build jobs (3226175–3226181) are running. Application images and deployment are not yet verified. [Implementation](../log/2026-10-14-nomad-test-devops-898-implementation.md), [build evidence and approvals](../log/2026-10-14-nomad-test-devops-898-service-build-retries.md).

## Single and dynamic implementation start (2026-10-14)

DevOps-898 user-approved Docker auth applied to8VKNomadclients using the existing shared-role snapshot (MR1371source); no restarts. Authenticated NexusGET200verified8/8; registry auth retained. Rabbit10.18.26.7 is an empty VM; user clarified old login/password must be reused on new machine, no datastore migration inferred. Four task branch approvals pending, no app builds/deployments. test5YouDoLogsExceptions login/SELECT1verified with existing Vault credentials. [Implementation and approvals](../log/2026-10-14-nomad-test-devops-898-implementation.md).

## Single and dynamic service preflight (2026-10-14)

DevOps-898 live preflight verified8readyclients/24jobs/62runningallocs and ample scheduler headroom. User-approved NOMAD_TOKEN_VK_TEST/CONSUL_TOKEN_VK_TEST copied into GitLab youdo; both API200 and masked/unprotected/scope* verified. Docker runner105/106host connectivity passes; no fresh container-network test. All8clients lack Nexus auth;20expected app component manifest/tag checks show no ready images. Copied RabbitMQ address and shared logging SQL configuration remain Yandex; candidate VK RabbitMQ5672refuses. mssql-test5 accepted producer is running/passing at10.18.26.35:14305; LogReader consumes per-stand Consul server keys. DebuggingEvents has its own companion ES task, correcting the separate-backend hypothesis. No application rollout. [Preflight evidence](../log/2026-10-14-nomad-test-devops-898-preflight.md).

## Single and dynamic service recovery plan (2026-10-14)

Final plan updated after live preflight and13release-pipeline audits: repository configuration/source choices first, single rebuild afterward, then staged deployment with fixed verified tags. User explicitly returned to planning before build execution; no builds launched. Missing Nexus auth/tags and backend dependency blockers are prerequisites; test5SQLproducer accepted/reachable, other15LogReader targets fail. [Final plan](../log/2026-10-14-nomad-test-devops-898-single-dynamic-plan.md).

DevOps-898 scope is11single+2dynamic services from DevOps-A-33. Shared internal-test CI templates will switch to vk-test; public-test is explicitly excluded. Read-only audit found Socket CI mode true despite dynamic HCL and DebuggingEvents hardcoded Yandex Elasticsearch backend; effective app-group CI inheritance and dependency readiness remain execution preflight. Plan only; no repository or runtime changes. [Plan and evidence](../log/2026-10-14-nomad-test-devops-898-single-dynamic-plan.md).

## Large MSSQL refresh migration scope (2026-10-14)

DevOps-897 seven-stage VK adaptation2026-10-14: user requested start, selected ceph-ssd and rejected extra checks absent in legacy. Branch DevOps-897-recreate-large-mssql-on-vk from automation-test-yandex/origin/master0bfc65c; uri cloud tasks/defaults, independent-stage inventory discovery, VK backup UNC and three large stand endpoints locally adapted. Fixture5cases/syntax/diff passed; independent review proposals deferred at user direction. Live step1created base SSD400GiB af3c6ccb-402e-4d2e-9b0b-d1a5fe075842, currently creating; no guest/restore success yet. No Git publication. [Implementation and runtime state](../log/2026-10-14-nomad-test-devops-897-vk-mssql-adaptation.md).

DevOps-897 manual SQL backup delivery complete2026-10-14: source backup172.24.0.19 /backup/sql/test/CleanYouDo.bak copied to VK share10.18.26.4 /public/sql/CleanYouDo.bak,96708001792bytes/90.1GiB, file date2026-10-11MSK, mode0644; source/destination size+mtime match, source unchanged, temporary file absent, Samba active,129GiB free. User explicitly skipped checksum; no hash verification. This supersedes in-progress statements below. Image active400GiB prerequisite confirmed; guest boot/restore and DBA_Clean/UNC migration remain separate. [Delivery result and user scope correction](../log/2026-10-14-nomad-test-devops-897-mssql-vk-preflight-and-backup.md).

DevOps-897 image preflight2026-10-14: VK yc-sql-base d840325b-16fd-4ff9-943d-9599b6bbf495 active/private, Windows metadata, virtio/BIOS, raw400GiB/min_disk400; no guest boot verified. STD3-4-8/STD2-4-8 flavors match historical4vCPU/8GiB, aggregate headroom sufficient for temporary+3stand400GiB disks. VK /public/sql backup path initially absent; source CleanYouDo.bak90.1GiB dated2026-10-11 verified on ES source backup172.24.0.19. User-authorized manual copy is running to share10.18.26.4 via temporary file and checksum-before-publish. DBA_Clean producer still targets Yandex10.16.28.4 in tracked code; restore procedure still old10.16.26.4. [Preflight and delivery evidence](../log/2026-10-14-nomad-test-devops-897-mssql-vk-preflight-and-backup.md).

DevOps-897 DNS publication complete2026-10-14: user-approved commit06d4821a pushed and [MR1374](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1374) created; user merged as master454ef804. Remote description/path/SHA and fetched master DNS rule verified. Pipeline140836 skipped, no agent merge/deployment. This supersedes DNS publication-pending statements below; the larger MSSQL migration remains separate. [Publication evidence](../log/2026-10-14-nomad-test-devops-897-dnsmasq-private-forwarding.md).

DevOps-897 persistence prepared2026-10-14: approved task branch DevOps-897-fix-nomad-private-dns from automation-services/origin/master71c37b2f, one-line client variable fix applied/checks/review passed, Git publication pending. All3Nomad masters already use working systemd-resolved10.18.20.3, no dnsmasq installed; DNS verified11/11across8repaired clients+3unchanged masters. Authorized branch-switch conflict in unrelated main.tf comment resolved preserving user's local version and excluding it from task staging. [Latest implementation/approval evidence](../log/2026-10-14-nomad-test-devops-897-dnsmasq-private-forwarding.md).

DevOps-897 Nomad DNS fixed manually2026-10-14: all8clients route mcs.local through IPsec/BIND10.18.20.3 instead of unreachable direct VK DNS10.18.20.65; dnsmasq active and local/private/Consul/system lookups verified8/8. Neutron identifies .65 as network:dns service port in shared_network, also IP10.18.26.252 (not queried). Master Ansible still has direct .65 rule; minimal one-line artifact prepared, task branch approval pending. Pilot backup-in-conf-dir mistake briefly stopped agent01 DNS, corrected before other clients. This supersedes earlier unresolved timeout and built-in-DNS characterization of .3. [Repair evidence and approval state](../log/2026-10-14-nomad-test-devops-897-dnsmasq-private-forwarding.md).

VK private DNS checked on running VMs2026-10-14: domain mcs.local; resolver10.18.20.3 returns Jenkins controller/agent A records10.18.26.8/.26. Default DNS on Jenkins controller works. Nomad agent01 can resolve through direct @10.18.20.3 queries, but its default local dnsmasq10.18.26.34 times out for these mcs.local names; no root cause/fix performed. SQL registration and recreation propagation remain unverified. [Live DNS evidence](../log/2026-10-14-nomad-test-devops-897-vk-private-dns-check.md).

DevOps-897 covers adapting automation-test-yandex large MSSQL refresh to VK Cloud. Historical committed seven-stage weekend workflow creates sql-base (disk yc-sql-base) from yc-sql-service-os01, restores backups, publishes image yc-sql-base, then replaces sql-test/sql-test1/sql-test6 with disks yc-sql-test/yc-sql-test1/yc-sql-test6. Large/thick deployment restarts Windows MSSQLSERVER and separately resets SQL database snapshots; small/thin Nomad deployment is excluded from this task. Exact AWX schedule/workflow settings remain unverified. Historical names are distinct from existing uncommitted DevOps-889 Yandex recovery edits; no DevOps-897 repository/runtime changes or branch approval yet. [Investigation evidence](../log/2026-10-14-nomad-test-devops-897-large-mssql-legacy-workflow.md).

DevOps-897 user naming decision2026-10-14: use vk-ms1 for VM/disk/image names: vk-ms1-sql-base and vk-ms1-sql-test/test1/test6; prepared output image vk-ms1-sql-base. User reports an existing VK image named yc-sql-base (not independently checked); its current name is distinct from the selected output name. No resource rename or implementation is implied. [Decision evidence](../log/2026-10-14-nomad-test-devops-897-large-mssql-legacy-workflow.md).

## Purpose

DevOps-898 Billing user rollout accepted2026-10-15 20:31UTC: master-707/pipeline141010/source55fc06b, builds3229763/3229766SUCCESS; ordinary test10–test15 jobs3229810,3229812,3229813,3229816,3229818,3229819allSUCCESS. Nomad all6running/healthy/restarts0. User deployed; parent agent verified read-only. Parent pipeline still running for independent production/release stages. Remaining user order4: Landings→TKB→Tochka→Business. [Evidence](../log/2026-10-15-nomad-test-devops-898-billing-user-rollout.md).

DevOps-898 Mobile ID user rollout accepted2026-10-15 20:26UTC: master-58/pipeline141008 SUCCESS/build-webSUCCESS, ordinary test10–test15 jobs3229736–3229741 all SUCCESS, Nomad all6running/healthy/restarts0. User performed deployment; agent verified read-only. Remaining user order4: Landings→TKB→Tochka→Business. [Evidence](../log/2026-10-15-nomad-test-devops-898-mobile-id-user-rollout.md).

DevOps-8984fresh B2B master pipelines created2026-10-15 20:10UTC under explicit user approval: Billing141010/IID707,MobileID141008/IID58,TKB141009/IID267,Tochka141011/IID1767. Source SHAs matched prior audited masters, initial status allrunning/prep active/builds created. Auto production/release effects disclosed, no stand deploys played/source edits. [Evidence](../log/2026-10-15-nomad-test-devops-898-four-b2b-repositories-preflight.md).

DevOps-8984service repo audit2026-10-15: Billing master-705,MobileIDmaster-57,TKBmaster-264,Tochkamaster-1764 all latest builds success, targetVKjobs absent. No mandatory source changes found; current shared templates support their PG/migrations/external workloads. Fresh master pipelines recommended because old compiled pipelines predate VK adaptation, all include automatic production/release effects requiring approval. User order afterLandings remains Billing→MobileID→TKB→Tochka→Business. [Evidence](../log/2026-10-15-nomad-test-devops-898-four-b2b-repositories-preflight.md).

DevOps-898 B2B Landings accepted2026-10-16 00:08:46MSK: pipeline141019/master-109/source0d17499 builds3230136/3230137SUCCESS; user-approved ordinary parallel jobs3230150–3230155 allSUCCESS. Nomad test10–test15 allrunning/healthy/restarts0, IMAGE_TAGmaster-109. MR19 nginx port80 plus preserved8080 fixes earlier health failure. Checks only GitLab/Nomad; no HTTP/Consul probes in final monitor. Independent master production/release pipeline still running. [Evidence](../log/2026-10-16-nomad-test-devops-898-landings-b2b-rollout.md).

DevOps-898 B2B Landings stand-port fix published2026-10-16MSK: MR18 merged, pipeline141017/master-107 builds SUCCESS; ordinary jobs3230082–3230087 blocked waiting Nomad health because nginx listens8080 while stand template maps80. Six running allocations had zero restarts; API checks pass, web checks fail. User approved local additive listen80 plus publication and separately cancellation; commit172a557/MR19→master opened, syntax/review passed, MR pipeline141018 running. All6old deploy jobs terminal canceled00:00:49–53MSK; Nomad workloads not stopped/repaired by cancellation. Subsequently user explicitly approved merge and MR-pipeline stop: MR19 merged0d17499/noSquash, MR pipeline141018 terminal canceled00:02:43MSK. Automatic master push pipeline141019/IID109 running, expected master-109; web3230136running/API3230137pending. Stand jobs3230150–3230155 created, not approved/played. [Evidence](../log/2026-10-15-nomad-test-devops-898-landings-stand-port-fix.md).

DevOps-898 B2B Landings build repair published2026-10-15: pipeline141007 web3229694 failed npm EINTEGRITY; API3229695 succeeded, deployments skipped. User approved branch and publication; commit ee64ce0/MR18→master refreshes four integrity fields for unchanged private package versions and selects existing internal Node24 image. Full local Docker build and CI Lint passed; MR pipeline141016 created, checkout clean. No base-images changes, merge or stand deployment. [Evidence](../log/2026-10-15-nomad-test-devops-898-landings-build-integrity.md).

DevOps-898 B2B Landings readiness2026-10-15: latest master-104/pipeline139691/current master2f6e82ec success2images, no VK jobs. Stand config web/API only, no DB/migrations or per-stand PG/Rabbit/Redis. No required stand config edits found; fresh master pipeline recommended for merged VK templates, includes auto production canary/update/release. Build Node/lockfile engine mismatch noted, no upgrade without actual need. [Evidence](../log/2026-10-15-nomad-test-devops-898-landings-preflight.md).

DevOps-898 Kitcut accepted2026-10-15: master-103/pipeline141005 ordinary parallel test10–test15 jobs3229673–3229678 all SUCCESS, Nomad all6running/healthy/restarts0. recreate_db=false preserved; no service changes/reset override. Next user-ordered service Landings;6remain Landings→Billing→MobileID→TKB→Tochka→Business. [Evidence](../log/2026-10-15-nomad-test-devops-898-kitcut-b2b-rollout.md).

DevOps-898 Kitcut fresh build2026-10-15: user approved new master pipeline141005/IID103 on e3ac817c without service config changes; expected master-103. Initial prep jobs running,3image builds/tests created, production bridge created. Ordinary jobs3229673–3229678 not played; preserve recreate_db=false/create-if-absent. [Evidence](../log/2026-10-15-nomad-test-devops-898-kitcut-preflight.md).

DevOps-898 remaining order corrected by user2026-10-15: Kitcut→Landings→Billing→MobileID→TKB→Tochka→Business. Kitcut latest master-102/pipeline139611 success3images, no target VK jobs. No source edits needed: user rejected changing recreate_db=false; verified Ansible creates absent PostgreSQL DB independently, then migrations run. Proposed branch not created. Fresh master pipeline still needed for current VK templates, auto-production effects need approval. [Evidence](../log/2026-10-15-nomad-test-devops-898-kitcut-preflight.md).

DevOps-898 notifications accepted2026-10-15: master-190/pipeline141003 ordinary parallel test10–test15 jobs3229634–3229639 all SUCCESS, Nomad all6running/healthy/restarts0. No source changes/retries. Remaining catalog7: business,billing,landings,mobile-id,TKB,Tochka,Kitcut; shared doc-generator reused, common SMS/Fns/DocValidation and B2B auth/notifications complete. [Evidence](../log/2026-10-15-nomad-test-devops-898-notifications-b2b-rollout.md).

DevOps-898 notifications fresh build2026-10-15: user approved master pipeline including disclosed auto-production/release effects. Created141003/IID190 once on80051dad; initial3image builds/tests running, production bridge/release created. Expected master-190; ordinary test10–test15 jobs3229634–3229639 not played. [Evidence](../log/2026-10-15-nomad-test-devops-898-notifications-preflight.md).

DevOps-898 notifications readiness2026-10-15: current master80051dad/latest master-189/pipeline137494 success3images, no target VK jobs. No mandatory source changes; recommend fresh master pipeline to capture current VK templates, with auto-production child/release effects explicitly approved before launch. Worker retains existing external integrations. No pipeline/deploy run. [Evidence](../log/2026-10-15-nomad-test-devops-898-notifications-preflight.md).

DevOps-898 auth-service accepted2026-10-15: master-168/pipeline141000 deployed to test10–test15 by ordinary jobs with DB recreation. Initial6jobs failed from B2B PG capacity; after approved PG/PgBouncer1000 limits, approved retries3229609/3229612/3229610/3229614/3229613/3229611 all SUCCESS, Nomad all6running/healthy/restarts0. No source changes. Production downstream141002 last scheduled, not claimed successful. Next proposed service notifications. [Evidence](../log/2026-10-15-nomad-test-devops-898-auth-service-b2b-rollout.md).

B2B PG capacity2026-10-15: auth ordinary jobs3229573–3229578 failed before SQL changes with too many clients. User requested limits matching C2C. Applied10.18.26.44 PostgreSQL max_connections100->1000 with2.405srestart, runtime1000/no pending restart; PgBouncer max_client_conn100->1000, softnofile1024->2048/hard524288 retained, reload/PID43719unchanged, auth/pool settings preserved. Auth retries not yet approved. [Evidence](../log/2026-10-15-postgresql-b2b-connection-limits-1000.md).

DevOps-898 auth fresh build2026-10-15: user approved new master pipeline after auto-production/NuGet effects disclosed. Pipeline141000/IID168 created once on f0d4a2f; initial status running,3image builds/build-libs/tests running, production bridge created/no downstream yet. Ordinary test10–test15 jobs3229573–3229578 not played. [Evidence](../log/2026-10-15-nomad-test-devops-898-auth-service-preflight.md).

DevOps-898 auth-service readiness2026-10-15: no mandatory repo changes; latest master-167/pipeline139444 success/builds3of3, masterf0d4a2f. VK target jobs absent. Existing pipeline predates VK template adaptation; recommend fresh master pipeline, but DEPLOY_PROD_MODE=auto enables production child/migrations and conditional build-libs may publish3NuGet packages. No new pipeline/deploy authorized or run. [Evidence](../log/2026-10-15-nomad-test-devops-898-auth-service-preflight.md).

DevOps-898 DocValidation expansion complete2026-10-15: master-757 deployed in parallel with DB recreation to test10–test15 via jobs3227436–3227441, all6GitLab SUCCESS/Nomad running/healthy. Restartstest12=1/test14=1, others0. Combined with accepted C2C8status, current release present on all14target stands. Common SMS/Fns/DocValidation rollout complete; next proposed B2B service auth. [Evidence](../log/2026-10-15-nomad-test-devops-898-docvalidation-b2b-rollout.md).

DevOps-898 DocValidation readiness2026-10-15: latest master-757/pipeline140949 successful, builds4/4; all8C2Cjobs running/healthy/restarts0. test10–test15 absent with ordinary manual jobs3227436–3227441 available. No code/config changes needed; current ordinary C2C jobs prove cloning from DocValidation template on common PG. No new deployment yet. [Evidence](../log/2026-10-15-nomad-test-devops-898-docvalidation-preflight.md).

DevOps-898 Fns expansion2026-10-15: no repository changes needed; latest master-598/pipeline140951 deployed via ordinary jobs3227508–3227513 to test10–test15 in parallel with DB recreation. All6GitLab SUCCESS/Nomad running/healthy/restarts0, C2C8already verified on same release; all14target stands current. Fns intentionally uses common PostgreSQL with per-stand DBfns-{{instance}}, RabbitMQ and matching DocValidation endpoints. [Evidence](../log/2026-10-15-nomad-test-devops-898-fns-preflight.md).

B2B deployment to test10–test15 was scoped on 2026-10-15 to the 13-service active Jenkins Groovy catalog, continuing DevOps-898. Reuse doc-generator already deployed as a shared service under that task; six new instances are not required. SMS, DocValidation and Fns are also needed on C2C stands. Custom business deployment recreates main/mock databases, so data policy must be explicit before execution. No rollout performed during planning. See [planning evidence](../log/2026-10-15-nomad-test-b2b-test10-15-deployment-plan.md).

Nomad test platform services, Consul configuration and telemetry managed by `sysadmins/terraform`. VK recovery under DevOps-893 permits fresh empty data. This map records verified source behavior; proposed VK runtime details are explicitly unverified.

## Components

After user edits and explicit cleanup, vk-test/jobs contains only seven actively referenced files: Traefik, Redis, Jaeger agent, CSI, Alloy traces, Kafka schema registry, Consul exporter. Eleven inactive job files removed locally; user-edited nomad.tf preserved. Original Yandex root unaffected.

VK-specific user scope corrections: Redis only for test,test1–test15; omit test16/test17 and redis-autotest. Existing Yandex source retains its original configuration. Next saved Redis plan is16 groups/16GiB, not yet applied.

- `/home/slnnk/git/terraform`: test Nomad jobs, monitoring modules and Consul KV. No cloud VM provisioning or registered CSI volumes in inspected source.
- Traefik, OAuth proxy, Selenoid GGR/iOS, 18 stand Redis and three autotest Redis, Baget, Jaeger agent, Alloy, Mimir, VictoriaMetrics, Grafana, Tempo and Loki.
- External job repositories consume CSI volumes; BuildAPI MongoDB historically uses `yc-csi-buildsinfo`.

## Delivery path

October13 [local preparation](../log/2026-10-13-nomad-test-devops-893-vk-traefik-preparation.md): all28 tracked environment files copied as-is into vk-test with target substitutions and necessary Cinder conversion. Source active/commented state preserved from34b581b. Init and validate passed; saved targeted Traefik plan1add/0change/0destroy awaits apply approval. No CI or runtime changes.

DevOps-893 final user-approved target layout: separate `vk-test/` root, Consul backend path `terraform/vkcloud-terraform`. This supersedes the earlier proposed `terraform/vk-test`. Approved branch created from freshly fetched origin/master34b581b; Traefik is locally prepared first, not deployed.

GitLab CI validates/plans/applies environment roots. Existing `yandex-test` auto-applies on master and applies manually on other branches. Proposed recovery root `vk-test` must initially deploy through approved manual stages and separate Consul state `terraform/vk-test`, without migrating Yandex state.

## Control points

Existing CSI job `yandex-test/jobs/csi-plugin.hcl` deploys Yandex driver v0.10.0, privileged monolith plugin `yc-csi`. Proposed replacement is OpenStack Cinder with Nomad ID `vk-csi`; compatibility requires a disposable-disk mount/detach/reattach test on VK. At least three clients are needed for current Traefik static port placement; Redis alone reserves 21 GiB.

## Operations

Corrective CSI apply approved/completed:8tasksrunning, provider cinder.csi.openstack.org,8/8healthy nodes andcontrollers. All current jobs deployed. CSI disk create/attach/mount/detach operations have not been exercised; no disks/volumes created. Full Terraform convergence check pending final result. Map records local-socket-only plugin status.

CSI initial approved apply registered systemjob but8/8tasks failed. Stderr unknown-endpointflag in /go-runner; source image CMDbinary was displaced by Nomadargs. Verified binary/bin/cinder-csi-plugin, added config.command locally, updatedplanawaitsapproval. All7otherjobs running38activeallocations. [Diagnosis](../log/2026-10-13-nomad-test-devops-893-vk-csi-deployment.md).

Main Alloy approved/applied1add and healthy8/8; every direct readiness/metrics endpoint200. Job starts with monitoring Vault policy and mandatory secret template, verifying restored Nomad→Vault task integration. Shared module unchanged. Map updated with dynamic perclient ports. Only CSI remains undeployed pending cloud credentials/secret/policy and approval. [Evidence](../log/2026-10-13-nomad-test-devops-893-vk-alloy.md).

Alloy traces approved/applied and running on10.18.26.37:28760, OTLPregistration30254. Direct readiness/metrics200; end-to-end delivery untested. Map updated. Remaining active scope: main Alloy module and CSI, with shared Vault credential repair and CSI cloud credentials still required. [Deployment evidence](../log/2026-10-13-nomad-test-devops-893-vk-alloy-traces.md).

Kafka Schema Registry approved/applied and healthy: one allocation running on10.18.26.34:31264, Consul passing, /subjects200empty. Address map updated. Alloy traces is next; unused Vault declaration removed locally because no secrets are consumed. Shared Vault repair remains required for main Alloy module and CSI.

Consul exporter corrective apply completed after approval: one active allocation running, Consul HTTPcheck passing, /metrics200 and consul_up=1 at10.18.26.35:28270. Removed only unused Vault declaration; common Nomad→Vault token remains broken. Map updated. Next Kafka Schema Registry plan ready with VK Kafka DNS correction, not deployed.

Consul exporter initial approved apply registered job but allocation failed: Vault token derivation403invalid token, no service registration. Job has no secret dependencies; unused monitoring Vault block removed locally. Updated targeted plan1change awaits approval. Shared Nomad→Vault credential remains broken for jobs that need secrets. [Failure and fix proposal](../log/2026-10-13-nomad-test-devops-893-vk-consul-exporter.md).

Jaeger agent approved/applied1add0change0destroy;8/8allocations running and registrations present on8clients. Job has no application health checks; trace delivery not tested. Address map updated. [Deployment and cleanup evidence](../log/2026-10-13-nomad-test-devops-893-vk-jaeger-agent-deployment.md).

Redis deployed after explicit approval:16/16 allocations running and cache TCPhealth passing for test,test1–test15, ports1900–1915. Runtime endpoints recorded in service-addresses.env. [Deployment evidence](../log/2026-10-13-nomad-test-devops-893-vk-redis-deployment.md). Next Jaeger agent plan prepared, not applied.

First VK deployment completed after explicit user approval: traefik2-service3/3 allocations running; proxy and proxy-ui passing on10.18.26.30/.10/.21:80/8080. Addresses added to service-addresses.env. Redis test-stand plan is next; no other services deployed yet.

October13 [preflight](../log/2026-10-13-nomad-test-devops-893-vk-preflight.md): eight clients have ample free resources and ports; metadata UUID/AZMS1 available. Basic secret schemas exist, but configured Nomad server Vault tokens return403. CSI secret/policy absent; prom-ruller1.2.2 manifest unavailable; Grafana5433 must change to actual5432. Existing Yandex S3 buckets pass HEAD with target credentials. User stopped additional preflight and chose individual service rollout, starting Traefik then Redis. SSH route is `youdo` plus noninteractive sudo; root authentication fails.

Follow the [DevOps-893 deployment plan and secret matrix](../log/2026-10-13-nomad-test-devops-893-vk-deployment-plan.md). [Live access checks](../log/2026-10-13-nomad-test-devops-893-vk-access.md) verified Nomad/Consul/Vault endpoints, datacenter `vk-test`, management/root tokens and eight ready clients on1.5.3. Default namespace has no jobs/CSI volumes, CSI plugin list is empty, and target state keys do not exist. Full capacity and Nomad→Vault integration remain unverified. Job apply, secret updates, bucket creation, DNS/identity changes and external consumer deployment require reviewed explicit approvals.

Nonsecret address map grouped by datacenter: [service-addresses.env](../../service-addresses.env). API endpoints were contacted directly; other service IPs/ports and health are from Consul catalog.

## Boundaries

Keep production apply outside test recovery. Review the two production Alloy test-domain references separately. Empty bootstrap data does not authorize deletion of existing storage. Preserve disabled jobs and unrelated repositories. Loki/Tempo Yandex S3 dependencies and Mimir shared secret need explicit target configuration.

## Access

CSI final user choice: reuse existing admin Vault policy. Verified its secret/* read rights cover secret/admin/vk-csi; plugin uses policies=[admin]. No separate vk-csi policy publication needed. Targeted CSI plan awaits apply approval.

CSI credentials now stored at user-requested secret/admin/vk-csi, fieldcloud_conf; old secret/vk/csi proposal superseded. User-supplied login/password in current/.env VK_CSI_USER/VK_CSI_PASSWORD; VK_CSI_PROJECT_ID corrected to RCOpenStackUUID. RCsource ~/downloads/nomad-csi-openrc.sh. Plugin references new path; read-only vk-csi policy proposal awaits publication approval. Auth endpoint/region recorded in addressmap; cloud auth not yet tested.

Manual token replacement approved/completed October13: all three Nomad masters now use existing nomad_vault_token from secret/ansible/yandex, synchronized into server.hcl and reloaded bySIGHUP. Token validation and effective config/API200 on all3; Nomad services active. Prior invalid-token statements describe the historical state. Actual task-token derivation will be checked with next approved main Alloy deployment. [Replacement evidence](../log/2026-10-13-nomad-test-devops-893-vk-vault-token-replacement.md).

Fresh October13 master verification: all three /etc/nomad.d/server.hcl files AND effective Nomad configs enable Vault at the correct VK URL with a token configured. The server credentials each return403invalid token. Describe this as configured integration with broken authentication, not missing integration. Nomad API listens on actual10.18.26.11/.12/.13 addresses;127.0.0.1 API probe is not applicable.

VK Vault route: `http://vault.service.vk-test.consul:8200`. User-supplied verified operator variables in `~/ai/current/.env`: `VK_TEST_VAULT_TOKEN`, `VK_TEST_NOMAD_TOKEN`, `VK_TEST_CONSUL_TOKEN`. Earlier Jenkins recovery used `VK_VAULT_TOKEN`; do not confuse the names. Nomad server integration still needs verification. Required Vault schemas/policies and proposed GitLab CI variables are in the linked plan; no secret values are stored in notes.

## VK SSD lifecycle verified 2026-10-13

Cinder type=ceph-ssd and availability=MS1 passed dynamic provisioning through vk-csi, 1 GiB ext4 volume, single-node-writer/file-system, mounting at /data, 4 MiB write/read checksum verification, detach and deletion. API verified cloud/Nomad volume absence and completed/purged test job. No permanent resources or Terraform changes. Evidence: [SSD lifecycle log](../log/2026-10-13-nomad-test-devops-893-vk-ssd-lifecycle.md).

## VK CI publication preparation 2026-10-13

Local CI adds automatic plan:vk-test and master-only manual apply:vk-test, with existing inherited group VK Nomad/Consul tokens. CI lint and Terraform validation passed; full plan No changes. Exact publication scope is .gitlab-ci.yml plus17newvk-testfiles, preserving user edits. Commit/push/MR awaits supervised publication approval. External application migration is excluded from DevOps-893 by the user. [Publication preparation and approval record](../log/2026-10-13-nomad-test-devops-893-vk-ci-publication-preparation.md).

## VK publication 2026-10-13

User approved final CI scope including disabling Yandex test/public-test jobs. Published commit22e451e and [MR440](https://gitlab.youdo.sg/sysadmins/terraform/-/merge_requests/440), targetmaster, no merge/apply. Pipeline140765 running at last observation; plan:vk-test running, existing unrestricted plan:production also included. Description readback exact match; checkout clean.

## VK CI apply verified 2026-10-13

User-run apply:vk-test [job3222681](https://gitlab.youdo.sg/sysadmins/terraform/-/jobs/3222681) succeeded with0add/8change/0destroy. Fresh direct-IP Nomad checks show all eight jobs working,46runningallocations, CSI8/8healthy nodes/controllers. Local Consul DNS currently fails, preventing a post-apply convergence plan; prior CI1.7.5 plan hidden eight updates differed from local1.9.4Nochanges, exact cause unproven. [Evidence and limitations](../log/2026-10-13-nomad-test-devops-893-vk-ci-publication-preparation.md).

## DevOps-893 closed 2026-10-13

User reported task closure after successful deployment, SSD lifecycle verification, GitLab publication/CI and runtime checks. User waived additional plan convergence verification. The proposed cause of prior CI/local plan differences is differing Terraform versions1.7.5/1.9.4 (hypothesis, not proven). Existing YouTrack work comment74-124648 corrected and verified. No pending work for this task; older convergence caveats above are historical and do not represent required follow-up.

## DevOps-894 Elasticsearch migration plan 2026-10-13

Current working-job preflight2026-10-14: final `dynamic_deploy` Pipeline approved and GET-verified; Jenkins enabled/not quieting down. Minimal ES flags still execute unconditional app stop, monolith deploy and buildsinfo update. Valid `MONOLITH_PIPELINE_ID` and `STATIC_PIPELINE_ID` are required even when `WEB_STATIC=false`; role may rebuild missing artifacts/images. Use an available stand and compatible existing versions. `test5` is verified thin/5GiB; full reset uses `retry(2)`. Runtime acceptance of the working job remains pending. [Preset and limits](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md#working-job-minimal-run-preflight-2026-10-14).

User requested analysis/planning for `automation-test-yandex` and confirmed preserving recreation from prepared data. Current ES deployment clones Yandex thin/thick Compute images after deleting the stand disk. [Plan and source analysis](../log/2026-10-13-nomad-test-devops-894-elasticsearch-vk-plan.md) recommend Cinder snapshots and CSI-managed volume create/delete with `vk-csi`, plus a scoped VK inventory and service domain. Empty-volume lifecycle is already verified; seed import, snapshot restore and ES data validation remain unverified. No repository or runtime changes authorized or made. Proposed task branch is unapproved. This supersedes the October10 Yandex-only ES destination proposal for this VK task.

Producer follow-up: fresh `dba/origin/master` (`37d5330`,2026-10-09) `airflow_dags/mssql_clean_jobs.py` defines Saturday DAG `DBA_Clean`, independently recalled by the user. It reindexes prepared SQL `CleanYouDo`/`YouDo_preseed`, then cold-copies ES data to `10.16.28.4:/data/elastic/{thick,thin}`. Actual source Airflow Connections, destination disk mounts, deployed code and subsequent YC image publication linkage are unverified. Migration should restore this regular preparation chain and publish Cinder snapshots only after data validation; replacing Nomad volume settings alone does not restore the producer.

User identified `10.16.28.4` as Yandex and likely unavailable; outage not measured. Recovery must start from prepared data on the producer's backup source, or regeneration from the prepared SQL datasets, then deliver directly to VK seed volumes. Old destination access and YC disk/image mapping are not prerequisites. Check producer task success and source container state independently of failed copy tasks; no DAG trigger authorized.

User confirmed ES base image refresh ran through the now-unavailable Yandex AWX instance in two stages (corrected three). Repository tags are `delete_image` and `create_image`; historical AWX settings remain unretrieved. Preserve weekly preparation plus playbook/AWX publication when replacing images with Cinder snapshots; do not assume snapshot publication belongs inside `DBA_Clean`. Publish/validate new snapshots before obsolete-artifact cleanup; retain a usable previous version on failure. AWX recovery/configuration changes require separate scope and authorization.

Source check2026-10-13: user screenshot maps `backup_server_prod` to172.24.0.19; SSH confirms `msk3-backup.youdo.corp`. `/backup/sql/elastic/data/nodes` (~21.1GiB) and `/backup/sql/elastic_smalldb/data/nodes` (~130MiB) exist and are mounted by running ES6.8.23 containers `elasticsearch1`/`elasticsearch_smalldb_1`. User waived date relevance for this stage. Exclude the separate2.05GBheapdump from seed transfer, without deleting it. [Read-only source evidence and limits](../log/2026-10-13-nomad-test-devops-894-es-source-check.md); index integrity not checked, no runtime mutations.

VK seed destination2026-10-13: user supplied10.18.26.4, inventoryshare-test01; SSH asyoudo confirms `vk-ms1-share-test01.mcs.local`,~4GBRAM and NOPASSWD sudo. Root key login denied. Existing disks:250Groot,5Gno reported filesystem/mount,40Gext4mounted/public. ES target directories absent. Destination accessible; existing/public usage and cloud volume identity must be established before a reviewed mount/format/copy proposal. No remote changes made. Address map updated with verified host/IP/login and limits.

Later user approval2026-10-13: created `/data/elastic/thin` and `/data/elastic/thick` on root `/dev/vda1` with owner/groupyoudo(1001),0755 and verified writable;239.48GiBfree. These are system-disk staging paths, not standalone seed disks. No transfer/format/container/snapshot action performed. Existing5G/40Gdisks unchanged. Standalone Cinder snapshot publication still requires a reviewed data-volume preparation step.

Transfer-route check2026-10-13, root-only per user: root on172.24.0.19 can reach SSH10.18.26.4 but authentication asroot returns `Permission denied (publickey,password)`. No root credential installation or copying authorized/performed; remote known_hosts unchanged. Source→root transfer is blocked until approved access configuration is supplied or changed.

Later approved key installation2026-10-13: user requested adding backuproot public key toshare. RSA public key appended toshare `/root/.ssh/authorized_keys` without removing existing keys;0600root-owned, exactlyone match. Backup-local `/root/.ssh/id_rsa` with agent disabled successfully authenticates asroot to10.18.26.4 (`id -un`→root,rc0). [Evidence and limits](../log/2026-10-13-nomad-test-devops-894-backup-share-root-key.md). Source persistent known_hosts unchanged; test pinned host key transiently. Data transfer/DAG changes not authorized/performed.

Approved thin transfer2026-10-13 completed:120572815bytes copied to10.18.26.4 `/data/elastic/thin/` with sourcecontainerstopped; checksum/metadata verification no differences, source `elasticsearch_smalldb_1` restarted/runningtrue,rc0. Share has no Docker; target ES boot remains unverified. Thick preflight0deletions,22667132593bytes (~21.1GiB), excludesheapdump; actual thick transfer unapproved. [Transfer evidence](../log/2026-10-13-nomad-test-devops-894-thin-transfer.md).

Later approved thick transfer2026-10-13 completed:22667132593bytes to10.18.26.4 `/data/elastic/thick/`,5342regularfiles, heapdump excluded, checksum/metadata no differences, source `elasticsearch1` restarted/runningtrue,rc0. Bothdatasets now staged onshare rootdisk; no Docker/ES test, Cinder snapshot or DAG/repo change. Temporary size monitor stopped. [Thick evidence](../log/2026-10-13-nomad-test-devops-894-thick-transfer.md).

Seed preflight2026-10-13: existing Cinder `vk-ms1-share-base-thin`5GiBUUIDad66e572-b39a-4ed7-86a6-eb5a094763cb and `vk-ms1-share-base-thick`40GiBUUID6b8a8094-227f-4eb2-968c-5469e98fd92c areceph-hdd/MS1 onshare, sameCSIproject. Thin/dev/vdb has no signatures; thick/dev/vdc ext4mounted/public onlylost+found/noactiveusers. New disks unnecessary. Historical Ansible confirms actualintendedESmounts `/data/elastic/{thin,thick}`, so preserve paths and staging before mounting; current device order is reversed fromoldYandex. Formatting/mount/fstab/fill proposals still unapproved. [Identity/mount evidence](../log/2026-10-13-nomad-test-devops-894-seed-disk-preflight.md).

Later approvedthinformat2026-10-13: ext4,labeles-base-thin,filesystemUUID70806792-9f23-4776-8367-60b857a2c384 verified on5GiBdisk. Stillunmounted; existingthick/public androotstaging untouched. Preparedhelper read-onlypreflight0 for stage-preservingmount/fill andUUIDfstabentries; actualapplyawaitsapproval. [Format/operation review](../log/2026-10-13-nomad-test-devops-894-thin-format.md).

User-approvedfourstepseedpreparation2026-10-13 completed: rootcopies retained at `/data/elastic-staging/{thin,thick}`;5GiBthin/dev/vdb and40GiBthick/dev/vdc ext4 mounted at `/data/elastic/{thin,thick}`;UUIDfstabrows use defaults,nofail,backup `/etc/fstab.devops-894-before-es-seeds`,otherrows unchanged. Bothseedcontents checksum/metadata matchstaging;applyrc0. /publicno longerdedicatedmount. Snapshots/ESstartup unperformed;stagingretained. [Finalmount/fillevidence](../log/2026-10-13-nomad-test-devops-894-seed-mount-fill.md).


Approved seed snapshots 2026-10-13: thin `c249047d-e6c3-4b9f-b78a-a1ceef11c206` (5 GiB) and thick `bb8ea2de-2484-4169-9438-df5352643bd4` (40 GiB) are available/100%, from their verified Cinder seeds. Each filesystem was unmounted during snapshot creation and remounted, UUID checks passed; root staging retained. CSI clone/ES startup remains unverified. [Snapshot evidence](../log/2026-10-13-nomad-test-devops-894-seed-snapshots.md).


CSI ES restore verified 2026-10-13: both retained thin/thick snapshots restored into temporary ceph-hdd 5/40 GiB clones through vk-csi. ES6.8.23 booted with all five indices/five aliases and21activeprimaryshards; index names/UUIDs/docs.count/aliases matched source. Both single-node clusters yellow with27unassigned replicas, same as source. Temporary jobs stopped/purged and clones deleted/cloud+Nomad404; snapshots/seeds retained. This supersedes earlier unverified ES restore statements. Repository/DAG/AWX migration is still pending. [Validation evidence](../log/2026-10-13-nomad-test-devops-894-es-clone-validation.md).


DevOps-894 local playbook adaptation 2026-10-13: user approved branch `DevOps-894-deploy-elasticsearch-on-vk` from automation-test-yandex/origin/master. Scoped inventories/vk_es and ES task paths implement validated Cinder snapshot deployment/weekly publication, preserve Yandex/public-test and AWX tag names. Both entrypoints syntax-check, template parse and11local fixture scenarios passed; review findings corrected. No infrastructure apply or Git publication. DAG destination and unavailable AWX workflow still require separate work. [Implementation evidence and approvals](../log/2026-10-13-nomad-test-devops-894-playbook-adaptation.md).


DevOps-894 explicit scope correction 2026-10-13: ES playbooks now VK-only. Removed legacy YC tasks/template, es_cloud branching and Yandex template fallbacks; public-test bind-mount template preserved with VK API entrypoint. This supersedes the earlier statement that these adapted ES entrypoints retain Yandex behavior. Unrelated MSSQL and other repository code remain outside scope. Syntax/templates and11fixture scenarios rechecked; no live apply or Git publication. [Correction evidence](../log/2026-10-13-nomad-test-devops-894-playbook-adaptation.md).


DevOps-894 fast-deploy correction 2026-10-13: per explicit user instruction, ES deployment now waits only for blocking `nomad job run` success after CSI reset. Removed separate plugin, disk, claim/allocation and ES health checks from the deployment path; only operational CSI delete retry remains. run_es performs no Cinder authentication or snapshot lookup. Prepared snapshot validation remains in the separate publication workflow. Current syntax/template/focused success-failure fixtures pass; no live apply or Git publication. Earlier extensive-deploy-check descriptions are superseded. [Evidence](../log/2026-10-13-nomad-test-devops-894-playbook-adaptation.md).


DevOps-894 actual create_image stage and fast-publication correction 2026-10-13: local AWX entrypoint run succeeded, failed0/exit0, publishing thin5GiB snapshot0d38e5f9-3c42-4923-9e29-4c50bb1de70c and thick40GiB snapshotef5fb5f1-c828-4605-9f1c-81022edd988b; mounts restored and temporary validation resources removed. User then explicitly removed clone/ES validation from future snapshot preparation. Publication now directly marks available snapshots es_published=true; no Nomad/ES checks. This supersedes all earlier claims that weekly publication must validate a disposable clone. Fallback inventory IDs updated to these prepared snapshots, previous artifacts retained, delete_image not run. No live rerun or Git publication. [Run evidence and steering](../log/2026-10-13-nomad-test-devops-894-awx-create-image-run.md).


DevOps-894 fixed-name correction 2026-10-14: per explicit user request, use original delete_image→create_image order and permanent snapshots vk-ms1-share-base-thin/thick. Removed version timestamps, retention, metadata publication and snapshot UUID fallback inventory. Deployment resolves the name to its CSI UUID automatically. This supersedes October13 versioned/publication-metadata design. Local create/delete/full-order fixtures and syntax pass. Existing prepared snapshots still have versioned cloud names; one-time rename helper prepared, awaiting specific approval, no cloud changes this turn. [Correction and pending rename](../log/2026-10-14-nomad-test-devops-894-fixed-snapshot-names.md).


DevOps-894 approved rename completed 2026-10-14: prepared snapshots now have permanent names vk-ms1-share-base-thin (0d38e5f9-3c42-4923-9e29-4c50bb1de70c) and vk-ms1-share-base-thick (ef5fb5f1-c828-4605-9f1c-81022edd988b). Helper exit0 and GET confirms both available. This clears the prior pending-rename condition; fixed-name lookup is usable without recreating data. [Approval/results](../log/2026-10-14-nomad-test-devops-894-fixed-snapshot-names.md).


DevOps-894 timed original-order refresh completed 2026-10-14: user-approved delete_image10.391s, create_image17.112s, total27.503s; both exit0/failed0. Exact permanent names vk-ms1-share-base-thin/thick deleted then recreated, snapshots ready and seed mounts restored. Prior snapshot IDs recorded in rename notes are now deleted/historical. Runtime selection remains by name, no new UUID inventory. No ES checks/clones, retention or metadata publication. Local timings exclude AWX queue/pod startup; no AWX configuration or Git publication. [Timing evidence](../log/2026-10-14-nomad-test-devops-894-refresh-timing.md).


DevOps-894 Nomad-only deployment and test pilot verified2026-10-14: explicit user instruction removed all direct cloud calls from deploy; Nomad/vk-csi create/delete/attach disks. Snapshot chosen via Nomad CSI list by ExternalSourceVolumeID (stable thin/thick seed) and latest ready CreateTime; provider names are empty, no snapshot UUID inventory. This supersedes fixed-name Cinder lookup/direct readiness polling described earlier. First pilot exposed absent-volume deletion handling and creating-disk attach race; fixed existence skip and Nomad reschedule5s with explicit attempts0/interval0. Final Ansible stop_es,run_es test/thick completed0/failed0 in60.037s, existing40GiB disk retained. Configured ES/head URLs recorded, HTTP/DNS not checked. Git publication and DBA_Clean/AWX migration still pending. [Pilot evidence](../log/2026-10-14-nomad-test-devops-894-test-thick-deploy.md), [Nomad-only implementation](../log/2026-10-14-nomad-test-devops-894-nomad-only-deploy.md).


DevOps-894 full reset/manual cleanup 2026-10-14: full run failed145.559s because CSI tried attaching a creating disk; earlier successful stop/run pilot remains distinct. Added Nomad claim-release wait after job purge and external-disk disappearance wait before replacement creation. User requested manual deletion, then explicitly authorized force dropping terminal claims. Cleanup completed: elasticsearch-test job absent, test-vk-csi-es registration absent, backing40GiB disk e963460d-a6f2-42f2-8fc8-42f502b9e417 absent from CSI provider list. Seeds/snapshots retained; no further deployment initiated. Full-cycle repeatability remains unresolved. [Evidence](../log/2026-10-14-nomad-test-devops-894-test-full-cycle.md).


DevOps-894 post-cleanup repeat failed2026-10-14 after125.805s: new disk942a91e9-d525-4df9-8297-2c16ee8b47e0 exists and elasticsearch-test was submitted; attach failed while Cinder creating. These resources have not been cleaned up. Current CSI returns no per-disk available condition (Status empty/IsAbnormal false); plugin healthy and Schedulable true do not prove disk readiness. No further changes applied. [Evidence](../log/2026-10-14-nomad-test-devops-894-test-full-cycle.md).


DevOps-894 readiness correction2026-10-14: user explicitly permitted direct VK Cloud polling. Deployment still creates/deletes through Nomad CSI, but reads ExternalID and polls Cinder until available before submitting job (create_disk/run_es). Existing scoped cloud auth reused; VK_CSI_* credentials required for deploy. Error statuses and retry exhaustion prevent job submission. Three actual Ansible fixtures and syntax-check pass; no live rerun or Git publication. This supersedes the earlier strictly Nomad-only deployment requirement. [Evidence](../log/2026-10-14-nomad-test-devops-894-cinder-readiness.md).


DevOps-894 readiness live verification2026-10-14: approved manual cleanup removed elasticsearch-test and backing disk942a91e9-d525-4df9-8297-2c16ee8b47e0, followed by full Ansible test/thick run with Cinder readiness polling. Three retries until available, then blocking Nomad deployment success; exit0/failed0 in89.680s. Stand is deployed again. This supersedes earlier failed-run/no-live-readiness statements; repeated reset of the now-successful allocation remains unverified. Seeds/snapshots retained. [Evidence](../log/2026-10-14-nomad-test-devops-894-cinder-readiness.md).


DevOps-894 repeat reset verified2026-10-14: user-authorized full test/thick Ansible reset succeeded102.438s, exit0/failed0, without manual force. Job stop→claim release(two retries)→CSI disk deletion→external disappearance(one retry)→snapshot clone→Cinder available(three retries)→Nomad deployment success. This clears the prior successful-allocation repeatability limitation. Two consecutive complete deployments passed89.680/102.438s. [Evidence](../log/2026-10-14-nomad-test-devops-894-cinder-readiness.md).


DevOps-894 requested ES stand batch verified2026-10-14: test1–test7 and test10–test15 all successfully deployed via Ansible. test1/test6 thick40GiB, other11thin5GiB. Initial batch315.412s succeeded12/13; test3healthy_deadline exceeded during task startup/image download, then stop_es,run_es retry succeeded62.088s on existing disk. Final13/13Nomad deployment success; no HTTP/index checks or Git publication. [Evidence](../log/2026-10-14-nomad-test-devops-894-es-stands-batch.md).


ES internal image mirrors prepared2026-10-14: approved base-images branch DevOps-891-mirror-elasticsearch-images from origin/master8759867 contains two digest-pinned FROM Dockerfiles for Elasticsearch6.8.23 and elasticsearch-head/sha-1a888b928135. Existing DevOps-894 thin/thick/public-test Nomad templates now reference corresponding registry.youdo.sg/youdo/base-images targets locally. Template parsing, syntax and focused review pass. No image build/publication or redeployment; do not deploy these local references before release-tag builds. [Evidence/approvals](../log/2026-10-14-nomad-test-devops-891-es-image-mirrors.md).


ES mirrors MR published2026-10-14 after explicit approval: base-images commit2e19eb0, [MR40](https://gitlab.youdo.sg/youdo/base-images/-/merge_requests/40), approved branch→master, only two Dockerfiles. No pipelines because builds are tag-driven; no merge/tags/images/deployments. Automation image references remain local pending availability and separate rollout authorization. [Evidence](../log/2026-10-14-nomad-test-devops-891-es-image-mirrors.md).


ES mirror release verified2026-10-14: explicitly approved MR40mergec522f0f and release tags elasticsearch/6.8.23, elasticsearch-head/sha-1a888b928135. Both tag pipelines140808/140809 and jobs3223683/3223684 success. Authenticated manifest-only checks verify both internal images available for linux/amd64. This clears pending-image availability; stand image rollout remains separate, not performed. [Evidence/digests](../log/2026-10-14-nomad-test-devops-891-es-image-mirrors.md).


DevOps-894 all-at-once internal-image rollout verified2026-10-14: authorized13concurrent full resets completed159.555s,11success. test2/test4hit1mhealthy_deadline; container start was35.84/43.30s after allocation, task setup→start0.3–0.4s with no image-download events. Exact pre-run delay origin not established; download is not supported as the primary bottleneck. Concurrent stop/run retries succeeded59.892/61.107s, final13/13Nomad deployment successes. GET all13job configs confirms both internal registry image refs. No Git publication/ESHTTPchecks. [Evidence](../log/2026-10-14-nomad-test-devops-894-es-unlimited-redeploy.md).


DevOps-894 deadline adjustment2026-10-14: user chose healthy_deadline2m/progress_deadline3m; both thin/thick templates updated locally, TCP/min-healthy behavior retained. Nomad parse/diff checks pass. Running jobs not changed; next deployment applies these settings. [Evidence](../log/2026-10-14-nomad-test-devops-894-es-unlimited-redeploy.md).


DevOps-894 all14deadline rollout verified2026-10-14: user-authorized simultaneous full deployment of test/test1–7/test10–15 completed121.790s,14/14exit0 with no retry deployments. test/test1/test6thick40GiB; other11thin5GiB. Templates with internal registry images and healthy2m/progress3m applied; no healthy-deadline misses. Prior pending-runtime-deadline statement superseded. [Evidence](../log/2026-10-14-nomad-test-devops-894-es-all-stands-deadlines.md).

DevOps-894 Jenkins ES integration plan proposed2026-10-14: live dynamic_deploy is an inline Pipeline on linux, checking out automation-test-yandex at AUTOMATION_BRANCH. ES stage still uses legacy dynamic inventory and host limit; proposed scoped VK inventory, explicit instance/type and credentials bindings affect only the ES stage. No Jenkins configuration or repository changes applied. [Proposed plan](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md). User correction (2026-10-14): Jenkins must use test_inventory, currently being restored by the user; separate vk_es inventory is superseded for Jenkins. Verify the restored inventory contract before adapting the playbook/job.

DevOps-894 inventory endpoint correction (2026-10-14): user requested http://dyninv.vk-test.youdo.local; test_inventory.sh now targets it locally. Shell syntax verified; DNS/HTTP unprobed, no Git publication. [Jenkins plan and update](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

## VK dynamic inventory deployed (2026-10-14)

DevOps-896 release-0.56.4 runs API/updater job dynamic-inventory, default namespace, on vk-ms1-nomad-agent-test-06; routed dyninv.vk-test.youdo.local GET200,16stands/64Nomad aliases/0SQL. Clients01-04 represented;05-08 excluded per user. No SQL prerequisite for infrastructure groups. User closed DevOps-896 on2026-10-14 and accepted VK service recovery as complete. Consumer cutover/liveSQL mapping/repeated-refresh observation were not verified in this run; retain these as historical limits, not open requirements of the closed task. Further work requires a separate request. [Deployment evidence](../log/2026-10-13-gitlab-ci-dynamic-inventory-vk-migration-plan.md).

DevOps-894 Jenkins preparation update (2026-10-14): user required global group_vars/all.yml and common nomad_token from injected VK_TEST_NOMAD_TOKEN; agent-created inventories/vk_es removed. ES-only Jenkinsfile/XML prepared locally, check mode default and test_inventory stand selection verified against recorded contract. No remote publication/build. Automation cloud credentials come from dynamic-inventory (Vault/Consul), with Cinder permissions still unverified. [Final preparation and checks](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

Jenkins VK credentials created (2026-10-14, explicit user approval): vk-test-nomad and vk-test-consul are Secret text; vk-test-cloud is the dynamic-inventory automation Username/password. Types independently verified via credential config GET; no job/build yet. Common nomad_token reads externally bound VK_TEST_NOMAD_TOKEN. [Approval and creation evidence](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

Jenkins ES test job created (2026-10-14, explicit approval): https://build.youdo.sg/job/dynamic_deploy_es_vk_test/, exact Pipeline/parameters verified, manual-only, RECREATE_DATA=false, zero builds. Task branch publication remains pending before runtime validation; working dynamic_deploy unchanged. [Creation evidence and publication proposal](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

DevOps-894 automation published (2026-10-14, explicit approval): commitd66c21d, [Draft MR104](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/104), taskbranch→master verified, pipelines[]. Jenkins test job can now checkout the published branch; first check-only build approval pending. No merge or build. [Publication evidence](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

Jenkins ES test build1 (2026-10-14): user-approved check-only run initially queued due quietingDown=true; user-approved cancelQuietDown verifiedfalse. Build1 failed before Ansible: python3 absent on linux/controller. Local Pipeline fix selects python3 or image-provided python3.8; remote update/check-only retry approval pending. [Build diagnosis and approvals](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

Jenkins ES build2/DNS root cause (2026-10-14): approved Python fix worked; build2 failed before Ansible on inventory. Controller ens3 DNS10.18.20.3 knows dyninv record, but resolved only has mcs.local and rejects .local lookup. Proposed runtime addition ~vk-test.youdo.local preserving current search/server awaits approval; no persistent DNS change or build retry. [Exact evidence and prepared helper](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

Jenkins DNS role and checkbuild3 verified (2026-10-14): user-approved dnsmasq apply on controller10.18.26.8, persistent config/loopback compatibility checks passed. Existing Docker resolver127.0.0.53 now answers dyninv. Jenkins ES testbuild3 SUCCESS, one test5 target, checkchanged0/failed0, no reset. Full reset/Cinder-account validation approval pending; repository integration of controller overrides separate. [Apply/build evidence](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

DevOps-894 fullbuild4 placement failure (2026-10-14): Nomad job Datacenters[yandex-test] vs8readyeligible vk-test nodes. Global all.yml dc overrode raw inventory dc; user-approved local common dc correction tovk-test resolves/renders correctly. Fix publication and build4 stop/full retry pending approval. [Root cause and checks](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

Jenkins ES thin/thick verification complete (2026-10-14): build5/test5thin SUCCESS72.115s; build6/testthick SUCCESS100.608s. Thick CSI actual40GiB/source configuredthickseed, healthy Nomad/Consul, ES74,235,448primary docs/single-nodeyellow. No force/manual corrections. MR104 d95b385 remainsDraft/unmerged; working dynamic_deploy unchanged. [Final runtime evidence](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).

DevOps-894 master/working job update (2026-10-14): MR104 merged0bfc65c; dynamic_deploy ES uses VK bindings/test_inventory and retry2(first+one repeat), common Nomad binding covers all roles. UTF8 post encoding corrected and savedsourceverified. Existing unsandboxedscriptapproval remainspending, no build started. ProjectIDmove into global repo vars proposed as follow-up after userrequest. [Final changes/corrections](../log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md).


DevOps-897 small MSSQL test5 deployed2026-10-14 using existing Ansible + test_inventory.sh and run_es tag after absent-job error. mssql-test5 task running; sql-test5 registered10.18.26.35:14305 on agent08. Subsequent requested case-insensitive absent-job handling published as dad41d4/MR106 and explicitly user-authorized merge completed to master9ad35fb; unrelated large DB edits preserved. Wrong-zone base disk deletion still pending creating; force-delete forbidden. [Evidence](../log/2026-10-14-nomad-test-devops-897-small-mssql-test5.md).

DevOps-897 base PA2 disk deletion confirmed2026-10-14: after creating completed, fresh token found available; earlier waiting helper had stopped on expired-token401. Resumed previously authorized deletion, DELETE202 then exact GET404; no replacement or VM created. [Evidence](../log/2026-10-14-nomad-test-devops-897-small-mssql-test5.md).

Large DB work resumed on user request2026-10-14 after deleting PA2 seed disk. Existing seven-stage edits run from current checkout without further changes. New MS1 ceph-ssd400GiB disk b6553d1a-35f7-4bbd-88c0-0b699212f090 creating; live step1 session94081 waits then creates VM/WinRM. [Live adaptation](../log/2026-10-14-nomad-test-devops-897-vk-mssql-adaptation.md).

Base guest network repaired via user-approvedDHCP command2026-10-14: stale172.26.0.103/24 replaced by10.18.26.9, WinRM/RDP/SQL reachable, authenticatedWinRM works. Step1green; stage2Windowsupdatesfailed0x80073712/noinstalls, legacyignore_errors preserved and reboot succeeded. Stage3restore started after usercontinue. [Evidence](../log/2026-10-14-nomad-test-devops-897-vk-mssql-adaptation.md).

DevOps-897 small MSSQL fleet2026-10-14 20:04UTC: deployedmissing10test2-4/test7/test10-15 using existing Ansible+VKtest_inventory; preservedrunningtest5.11/11NomadSQLtasksrunning andConsulSQLservicesregistered, noSQLcontentsquery. LargeYouDo restore stage3completed/baseSHUTOFF; interruptedstep4notexecuted, preparedimageabsent. [Evidence](../log/2026-10-14-nomad-test-devops-897-small-mssql-test5.md).

DevOps-897 user explicitly launched onlystage4today2026-10-14: Cinder uploadstoppedbase bootdisk accepted, preparedimagevk-ms1-sql-base pending; Ansible18374will clean temporarybase resources afteractiveimage. No stages5-7 launched and originalyc-sql-base retained. [Evidence](../log/2026-10-14-nomad-test-devops-897-vk-mssql-adaptation.md).

DevOps-897 stage5 explicitly executed2026-10-14: all3exactmanagedstand names andnameddisks/ports absent, so no deletions; Ansiblefailed0. Stage6/7notlaunched. [Evidence](../log/2026-10-14-nomad-test-devops-897-vk-mssql-adaptation.md).

DevOps-897 stage4 completed andverified2026-10-15: preparedimageb204affb-cf20-473c-816e-09cb03d76421 active400GiB; Ansiblefailed0; temporarybaseVM/port/disk deleted, freshAPI noVM/volume. Stage5done/noexistingtargets; stage6/7notstarted. [Evidence](../log/2026-10-14-nomad-test-devops-897-vk-mssql-adaptation.md).

## Test5 monolith internal routing recovery (2026-10-15)

Ansible automation-test-yandex group_vars/all.yml formerly hardcoded traefik_domain=yandex-test.youdo.local while dc=vk-test. DevOps-899 MR111 merged342b1d5 derives the routing suffix fromdc. Live youdo-test5 had exactly four internal Host tags corrected (API, SSR, moderation-tickets, moderator-boris), preserving images/config templates/data; CAS8381→8948, evaluation completed, both allocations healthy. API /api/v1/state changed404→200 through the VK hostname. Escrow13.8.12 health checks now pass and its saved/live/rendered BuildAPI data matches. Config master/preprod is a base input overwritten by Ansible; no config-repo DNS changes were needed. See [execution evidence](../log/2026-10-15-jenkins-devops-899-monolith-microservice-recovery.md).

## DevOps-899 next test5 iteration accepted (2026-10-15)

Seven selected Nomad services deployed: broadcast1.2.11, featuretoggle1.0.11, Content2.5.13, Landings1.3.35, trackingpixel1.0.5, Socket1.2.9, Help1.0.14. Moderation1.0.45 assets published to S3 with explicit prefix replacement approval. Current BuildAPI source/version metadata verified; Landings HTML absent by existing webEx_check=false design, Socket version-cell mapping absent, APIs correct. Broadcast finaldeploy3228256 healthy after localdevdocker/postgres:latest recovery; ContentMR64fixedcredentialaliases. Cerberus/MiniSape/WalletOne/Form/B2B excluded. See [execution log](../log/2026-10-15-jenkins-next-test5-service-rollout.md).

## Featuretoggle test5 seed preflight (2026-10-15)

Restored PostgreSQL source `featuretoggle` at `10.18.26.39` contains149features/293history rows; `featuretoggle-test5` has empty data tables and matching columns/migration versions. User-approved copy completed: destination149features/293history, ordered data hashes match source; ID sequences350/521 with is_called=true. Source and VersionInfo unchanged. [Work log](../log/2026-10-15-nomad-test-featuretoggle-test5-seed.md).

Production CSV reconciliation (2026-10-15): user-approved49missing feature keys inserted into featuretoggle-test5, IDs351–399. Total198keys now matches production CSV;149existing rows preserved exactly. New values38enabled/11disabled match supplied CSV; existing31enabled differences retained. See seed work log above.

Featuretoggle UI auth blocker (2026-10-15): API returns500 with old Npgsql Authentication method not supported/code10; test PG16 shared youdo role and HBA use SCRAM. Selectel production C2C challenge verified MD5/code5 for youdo/featuretoggle on5432and5433, no password/SQL sent. No auth changes made; shared-role scope versus dedicated featuretoggle role requires user decision. See featuretoggle seed work log.

Featuretoggle auth fixed (2026-10-15): final user-approved MD5 scope is role youdo only on10.18.26.39, including role-specific loopback rules; other generic/replication rules and default password_encryption remain SCRAM. Password unchanged; grafana_test unchanged. Initial authorized broad MD5 apply was immediately narrowed at user correction. Reload only. Final API GET /api/v1/features HTTP200/198features; direct protocol MD5 verified. Browser not directly tested. Backups and exact actions in featuretoggle seed work log.

DevOps-897 stage6 launched2026-10-15 at user request for only vk-ms1-sql-test/test1/test6 with scoped high-iops disk override,400GiB, explicit Cinder/Nova MS1. Prepared image b204affb-cf20-473c-816e-09cb03d76421 active400GiB; high-iops supports MS1 and compute/volume MS1 available. Syntax/diff checks passed; live Ansible session96718 progressing, completion not yet verified; stage7 not launched. Existing DevOps-899-fix-microservice-postgres-auth checkout/prior edits preserved, no Git publication. This supersedes earlier stage6-not-started observations. [Evidence](../log/2026-10-14-nomad-test-devops-897-vk-mssql-adaptation.md).

DevOps-897 stage6 parallel continuation2026-10-15: user requested concurrent creation. First disk vk-ms1-sql-test/599ef47e-db00-4d17-ad10-7a54c4a0c480 was downloading400GiB/high-iops/MS1, no VM yet. Local sequential controller96718 stopped(SIGINT/exit99), disk preserved. Generated runner gained stage6-only --stand singleton selection; syntax passed, no new repository edit. Three independent controllers launched: test43477,test1 51636,test6 43232; all retain high-iops/MS1, completion pending, stage7 not launched. Supersedes prior sequential-run status. [Evidence](../log/2026-10-14-nomad-test-devops-897-vk-mssql-adaptation.md).

SMS service test5 accepted2026-10-15: master-191 fromcurrentmaster21060f7, pipeline140987, deploy3228662SUCCESS. Threeimagesand188tests passed; TestcontainersPostgreSQL11.5 preloadedonlyrunner171, matchingC2CCIpublickey addedB2BPG44root withbackup. Migrationscomplete, webapp/workerhealthy0restarts, Consulpassing, webappheartbeat200, BuildAPImetadata/live/HTMLaccepted. No servicerepository/Ansible changes or realSMSsend. See [SMS deployment record](../log/2026-10-15-nomad-test-sms-service-test5-deployment-analysis.md).

Featuretoggle stand clones preflight (2026-10-15): source featuretoggle-test5 now198features/301history after user configuration; all13requested target DBs absent. User-approved one-snapshot clones completed for test,test1–4,test6–7,test10–15, owneryoudo. All13verified:198features/301history/fourVersionInfo, table hashes and sequences match; source unchanged. No stand service deploy/restart or UI verification. [Work log](../log/2026-10-15-nomad-test-featuretoggle-stand-clones.md).

Main featuretoggle template refreshed from configured test5 after explicit user approval (2026-10-15):198features/301history/fourVersionInfo, all ordered table hashes and ID sequences399/529match test5. Protected full pre-refresh backup under /var/tmp/featuretoggle-before-test5-refresh-20261015T144416Z-2gy3p95c.dump on10.18.26.39; source unchanged. Exact execution in stand-clones work log.

### C2C PostgreSQL connection budget (2026-10-15)

Read-only audit: PG39 max_connections100,95/97clientbackends idle at snapshot; youdo superuser91connections/34DBs. PgBouncer1.22on5433 onlyconfiguredforGrafana, missingyoudoauth/mappings and implicit sessionmode. Proposed bounded transactionpool for compatibleappclients, directmigrations/Userinsurance sessionlocks. Nothing applied. [Audit](../log/2026-10-15-postgresql-c2c-pgbouncer-capacity-audit.md).

### Minimal Antifraud PgBouncer authorization applied (2026-10-15)

PG39PgBouncer5433 now accepts youdo and fiveexplicitAntifraudtest2/3/4/5/7mappings; SELECTtest4/5verified. No poolmode/limitchange. AntifraudMR146merged,23.8.8pipeline140992 all4images/tests passed; user selected build-only, newversionnotdeployed. [Evidence](../log/2026-10-15-postgresql-antifraud-pgbouncer-minimal-setup.md).

### Antifraud transaction pools applied (2026-10-15)

PG39 PgBouncer now has14active-stand Antifraud mappings with transaction mode, pool2/maxdb2/min0/reserve0, aggregate youdo cap10, idle backend timeout30s. All five Antifraud jobs stopped by user request; pilot test5 restarted with23.8.8/recreation and is healthy without restarts, both migrations exit0 and logs clean. Other four remain stopped. CIjob3229011 still waiting inside nomad run despite completed deployment; BuildAPI publication pending. [Evidence](../log/2026-10-15-postgresql-antifraud-transaction-pool-test5.md).

DevOps-897 stage6 completed2026-10-15: all three parallel controllers exit0/failed0/unreachable0 and WinRM wait passed. Fresh API confirms test10.18.26.17, test1 10.18.26.121, test6 10.18.26.9 all Nova ACTIVE/MS1 and boot disks in-use400GiB/high-iops/MS1. Address map updated; old base10.18.26.9 now belongs to test6. SQL contents unverified, stage7 not run, Git publication pending. Supersedes earlier stage6-in-progress observations. [Evidence and resource IDs](../log/2026-10-14-nomad-test-devops-897-vk-mssql-adaptation.md).

### C2C PostgreSQL connection capacity500 (2026-10-15)

User-authorized PG39 max_connections100→500 applied in /etc/postgresql/16/main/postgresql.conf; cluster16/main restart2.831s, runtime500/pending_restartfalse verified. PgBouncer unchanged; SQL through5433 and Antifraudtest5 Consul checks pass. Other Antifraud stands remain stopped. [Evidence](../log/2026-10-15-postgresql-c2c-max-connections-500.md).

DevOps-897 stage7 completed2026-10-15 on explicit user request: run_workflow.py --stage step_7/session12238 exit0, all3VMs ok7/changed6/failed0/unreachable0/ignored0. Windows names sql-test/sql-test1/sql-test6, rename reboots, VBS/Zabbix FQDN updates, sqlcmd -b sp_CorrectServerName and final reboots passed. Seven-stage runtime run complete; Git publication/review and future stage1 prepared-image default remain pending. Application, SQL schema/contents and monitoring ingestion not verified. Supersedes stage7-pending observations. [Evidence](../log/2026-10-14-nomad-test-devops-897-vk-mssql-adaptation.md).

Jenkins dynamic_deploy5832 FAILURE2026-10-15 for test/RESTOREtrue: master381391de5d8c21b58ea73f928b5b52c6a63d68b3 still uses old thick MSSQL endpoint, causing controller TCP1433 timeout to sql-test.ru-central1.internal in restartMSSQLSERVER; snapshot Restore never invoked. Controller DNS/TCP1433 succeeds for all3VK names/addresses. User-approved three-variable endpoint publication completed as cdb11b5522ec6c30fae9cd5086898ff70f2cd2ba / [MR113](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/113), source DevOps-897-point-large-mssql-to-vk to master; effective inventory and syntax/YAML/diff checks passed, pipelines[]. User explicitly authorized MR113 merge; fresh GET confirms merged cf88e42259787a8c6350771d17726bd4fcff3e30 and master SQL fields point at VK for all3stands. User subsequently reported successful playbook execution after the endpoint merge; endpoint fix accepted on that report, no independent new build/log verification. No local Git merge/switch; full workflow publication remains separate/pending. [Diagnosis and separate errors](../log/2026-10-15-jenkins-build5832-mssql-old-endpoint.md).

### Five-stand Antifraud acceptance after user rollout (2026-10-15)

All five test2/3/4/5/7 Antifraud23.8.8 jobs3229391–3229395 succeeded; current allocations healthy and BuildAPI matching. Four zero restarts, test7 one startup restart from transient PgBouncer max_client_conn100 saturation. All five use10 PostgreSQL backends total (2perDB), PG500 capacity retained. Raising PgBouncer client cap500 proposed, not applied. [Evidence](../log/2026-10-15-postgresql-antifraud-five-stand-acceptance.md).

### PgBouncer client capacity500 (2026-10-15)

PG39 /etc/pgbouncer/pgbouncer.ini max_client_conn500 applied via reload and confirmed by live SHOW CONFIG; process PID unchanged. Existing soft nofile1024 sufficient; auth/mappings/backend cap10peruser/2perDB unchanged. PostgreSQL max_connections already500. [Evidence](../log/2026-10-15-postgresql-pgbouncer-client-limit-500.md).

### Broadcast accepted on test/test1-test7 (2026-10-15)

Broadcast1.2.11 pipeline140972 accepted on all eight stands. Seven new jobs3228251/252/253/254/255/257/258 succeeded; test5job3228256 retained. Every current allocation healthy/zero restarts; all16migrationtasks exit0; BuildAPI metadata matches. Runtime PostgreSQLdirect5432. [Evidence](../log/2026-10-15-jenkins-broadcast-eight-stand-rollout.md).

### FeatureToggle accepted on test/test1-test7 (2026-10-15)

FeatureToggle1.0.11 pipeline140973 deployed in parallel on all eight stands. Jobs3228285–3228289/3229418/3228291/3228292 succeeded in39–56s. Nomad all running/healthy/zero restarts. Release recreate_db=false retained; user limited checks to GitLab/Nomad statuses, no data/API/BuildAPI validation. [Evidence](../log/2026-10-15-jenkins-featuretoggle-eight-stand-rollout.md).

### Landings accepted on test/test1-test7 (2026-10-15)

Landings1.3.35 pipeline140974 deployed concurrently to all eight stands. Jobs3228315-3228319/3229437/3228321/3228322 all succeeded in22-41seconds. Nomad `youdo-front-landings-<stand>` all running/healthy/zero restarts. User-requested checks limited to GitLab/Nomad statuses; existing recreate_db=false retained. [Evidence](../log/2026-10-15-jenkins-landings-eight-stand-rollout.md).

### Socket rollout on test/test1-test7 (2026-10-15)

Socket1.2.9 pipeline140976: seven jobs3228379-3228383/3228385/3228386 succeeded; test5 retry3229440 failed7.07s. All eight `socketChat-<stand>` jobs remain running, two healthy allocations each, zero restarts; existing test5 retained. Checks limited to GitLab/Nomad statuses; failure not diagnosed or retried. TrackingPixel excluded by user from current rollout sequence. [Evidence](../log/2026-10-15-jenkins-socket-eight-stand-rollout.md).

### Socket retry accepted and Help accepted (2026-10-15)

User-requested Socket test5 retry3229442 succeeded32.88s; now all eight Socket jobs successful, all16allocations running/healthy0restarts. Initial test5failure was Nomad CLI `Error fetching deployment` after successful submission. [Socket evidence](../log/2026-10-15-jenkins-socket-eight-stand-rollout.md).

Help1.0.14 pipeline140977 deployed concurrently on test/test1-test7, jobs3228407-3228411/3229441/3228413/3228414 all successful31-39s, all eight jobs/allocations running/healthy0restarts. Verification limited to GitLab/Nomad statuses. [Help evidence](../log/2026-10-15-jenkins-help-eight-stand-rollout.md).

### Content accepted on test/test1-test7 (2026-10-15)

Content2.5.13 pipeline140983 deployed concurrently to all eight stands: jobs3228565-3228569/3229459/3228571/3228572 all SUCCESS35-78s. Nomad `youdo-content-<stand>` all running/healthy/zero restarts. GitLab/Nomad statuses only, as user requested. [Evidence](../log/2026-10-15-jenkins-content-eight-stand-rollout.md).

### SMS accepted on test/test1-test7 (2026-10-15)

DevOps-898 expansion completed2026-10-15 18:39UTC: ordinary jobs3228623–3228628 deployed master-191 to test10–test15 in parallel with DB recreation, all6GitLab SUCCESS/Nomad running/healthy/restarts0. Latest release now healthy on all14target stands. User acceptance is GitLab/Nomad job statuses only; remaining stand rollout uses ordinary jobs with DB recreation. Keep-db routing fix published in MR91, merge pending. [Final rollout](../log/2026-10-15-nomad-test-devops-898-sms-b2b-rollout.md).

Live audit2026-10-15 18:28UTC confirms latest SMS release master-191/current master21060f7 on all8C2C stands, running/healthy with passing webapp+worker Consul checks and zero restarts. SMS absent on all6B2B stands test10–test15 (also excluded test8/test9). Latest pipeline140987 has successful image builds but aggregate failed due deploy-monitoring3228652 runner_system_failure. [Audit](../log/2026-10-15-nomad-test-devops-898-sms-all-stands-audit.md).

SMS master-191 pipeline140987 deployed concurrently to all eight stands: jobs3228613-3228617/3229460/3228619/3228620 all SUCCESS101-114s. Nomad `youdo-sms-service-<stand>` all running/healthy/zero restarts. GitLab/Nomad statuses only as requested. [Evidence](../log/2026-10-15-jenkins-sms-eight-stand-rollout.md).

### Moderation static publication complete (2026-10-15)

Moderation1.0.45 pipeline140978 published in parallel to test/test1-test4/test6/test7; jobs3228432-3228436/3228438/3228439 all SUCCESS150-173s. Existing test5job3228437 retained. Static only, no Nomad deployment; GitLab statuses checked as requested. Selected rollout sequence now complete: Broadcast, FeatureToggle, Landings, Socket, Help, Content, SMS and Moderation on test/test1-test7; TrackingPixel excluded, Cerberus2 postponed. [Evidence](../log/2026-10-15-jenkins-moderation-seven-stand-publication.md).

### Cerberus empty-DB adaptation prepared (2026-10-15)

User reopened Cerberus2 and explicitly selected empty databases for all stands. Approved branch `DevOps-899-create-empty-cerberus-databases` from mastercf88e422; local cerberus2.yml+5/-19 removes template clone/stand conditions and uses raw/become postgres/pager off. Syntax/YAML/diff checks pass; unrelated16MSSQL paths retained. Publication pending, no build/deploy. [Evidence](../log/2026-10-15-jenkins-cerberus-empty-databases.md).

Cerberus follow-up: approved patch published as13a23b1/[MR114](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/114), explicitly approved merge completed master248bf03e. Remote master matches reviewed file; all16unrelated MSSQL paths preserved. Build/deploy not yet triggered.

### C2C connection capacity1000 effective (2026-10-15)

User-requested PostgreSQL max_connections500->1000 applied on10.18.26.39, postgresql@16-main restart4.362s, SQL confirms1000/no pending restart. PgBouncer max_client_conn500->1000 effective via reload/PID unchanged; softnofile2048 runtime+persistent, hard524288 retained. Auth/pool mode/backend limits unchanged. Cerberus rollout capacity failures led to change; five jobs needed recovery after PG restart. [Evidence](../log/2026-10-15-postgresql-c2c-connection-limits-1000.md).

### Cerberus1.0.9 rollout status snapshot; runtime acceptance superseded (2026-10-15)

Cerberus1.0.9 pipeline140997 accepted on test/test1-test7/test10-test15: all14GitLab deploy jobs SUCCESS, all14Nomad jobs running/healthy. Original raw folding bug fixed via Ansible MR115/masterd2c5b9b. Capacity failures resolved with user-requested PG/PgBouncer1000; user explicitly chose normal redeploy with DB recreation for five runtimes lost after PG restart. Final jobs3229541/3229545/3229546/3229547/3229542/3229548/3229534/3229537/3229503/3229504/3229549/3229506/3229507/3229543 by stand order. Status-only verification; historical restarts test6/test7=3,test11=2, currently healthy. [Evidence](../log/2026-10-15-jenkins-cerberus-eight-stand-rollout.md).

.NET2.1 SDK/runtime mirror recipes base-imagesMR42/masterab4e5860 published/tagged. Direct registry push explicitly authorized after CI BuildKit external pull delay; SDKCI3229538 canceled, runtimeCI3229539 succeeded. Both registry manifests match checked local images. Cerberus CI consumer refs explicitly deferred. [Mirror evidence](../log/2026-10-15-base-images-dotnet21-mirrors.md).

### Cerberus runtime restart investigation (2026-10-15)

MR117 merge verified on2026-10-16localdate after user report: merged_at2026-10-15T23:58:44.928+03, master078c906b24fb5883395a2b76bd3964fbc4598d84, no squash. Fetched origin/master template exactly matches approved461bb053source. Source persistence complete; remaining13standrollout and sustained readiness stillpending. User merge report is not deployment authorization; no deploy/currentbranchswitch/localmerge performed. [Merge evidence](../log/2026-10-15-nomad-test-cerberus-pgbouncer-source-capacity20.md).

Follow-up source publication and capacity applied: [MR117](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/117)/461bb053 on DevOps-899-use-pgbouncer-for-cerberus, one template +8/-4 for4runtime5433/No Reset On Close=true and kill_timeout30s; migrations direct5432, notmerged/pipelinesempty/noordinarydeploy. Approved PgBouncer capacity:14existingCerberusDBpools/max10,14priorAntifraudroutes/max2preserved(8actualDBs), Grafanasession/max20; budget20*10+20*2+20=260, youdocap250/clientcap3000/softFD4096. Reload/PID114852unchanged. Test1timeoutCASversion2/index21058 applied; currentalloc25545ef6-c94a-26e7-985f-665a65751fa9 snapshothealthy/rest0, not sustained acceptance.20:56:52UTC PG1000clientbackends/777Cerberusidle/noPgBouncerwaiting; other13stands stilldirect, no capacity relief claimed. No merge/cleanup/otherstandswitch. [Scope, approvals, verification and pending recovery](../log/2026-10-15-nomad-test-cerberus-pgbouncer-source-capacity20.md).

Actual deployed worker/API1.0.9 entrypoint verified read-only in auto-rescheduled pilotalloc3afa1815-44dd-3c4e-7e10-da3003c9de2b/node10.18.26.30: `/app/entrypoint.sh` hashes match fixed templates7fabb47/MR85. PID1bash/childdotnet/M_TAGunset confirms runtime forwarding branch active (TERM/INT→childSIGTERM/wait). LiveKillTimeout5s/KillSignalempty; no signal/shutdown test performed. AppStartAsync failure skipping explicitStopAsync remains separate, originalstalecreationcause unproven. [Actual image/process evidence](../log/2026-10-15-nomad-test-cerberus-test1-pgbouncer-pilot.md).

User explicitly approved consumer pilot on test1: direct Nomad CAS update20:32:36UTC/index19922/version1 replaced one allocation;4runtime PostgreSql settings now5433/No Reset On Close=true, migrations remain direct5432, noDBrecreation/sourceedits. Newalloc5adea323-d524-9790-1c08-b54a951ba605 on10.18.26.21;20:38:23UTC all3workers Restarts1 after stage19999 MembershipOracle5mintimeout/exit134, APIrestart0, Nomadhealthy stilltrue.20:38:25UTC PgBouncer1server/0waiting/123queries, PGtotal974; membership6Active/18Joining/78Dead, initialpilotgeneration stillJoining and obsolete Active10.18.26.38:15001 observed. Switch complete but sustainedstartup failed, with no observed pool queue. Ordinary CI can overwrite this runtime-only change; source persistence and any membership recovery require separate applicable approvals. [Pilot evidence](../log/2026-10-15-nomad-test-cerberus-test1-pgbouncer-pilot.md).

Subsequent explicitly approved PgBouncer preparation: C2C10.18.26.39:5433 now has Cerberus_test1 transaction mapping to localPG5432, pool_size10/min0/reserve0/maxdb10; shared youdo cap10→20. Reload/PID114852 unchanged, runtime mapping enabled/current_connections0, global settings/auth/16existing DB mappings preserved. First perDB reserve_pool_size key rejected by1.22; corrected to reserve_pool and runtime verified. No consumer switch/rerun/deploy; Orleans compatibility and membership recovery remain pending. [Approved preparation evidence](../log/2026-10-15-postgresql-cerberus-test1-pgbouncer-pool.md).

Read-only 20:12–20:15UTC audit supersedes sustained-health interpretation of the rollout snapshot above: initial observed test1/test2/test6/test7 failed allocations8/11/10/8; GC changes those counts and current restart counts hide replacement history. Logs show MembershipOracle activation timeout5min at stage19999, then startup rejection to dead silo endpoints at stage20000; test2/test6 also PostgreSQL53300. Final PG39 snapshot20:15:50UTC:972/1000connections,729toCerberusDBs/allidle; test1/test2/test6 current3workers eachRestarts1, Nomadhealthy remainedtrue during restarts. test1 membership retains old10.18.26.37 Active endpoints while current10.18.26.34 silos remain Joining; ConnectionRefused evidenced. Test template has3workers+API, no explicit runtime pool bounds, directPG connections, and TCP-only health checks that do not establish Orleans startup completion. Immediate failure chain is verified; original trigger remains unproven. No fixes/restarts/deployments/membership edits authorized/performed. [Evidence, source analysis and limits](../log/2026-10-15-nomad-test-cerberus-restart-loop-membership.md).

DevOps-898 Tochka PgBouncer repair2026-10-15: user-approved12routes (two DBs per test10–test15) added on B2B10.18.26.44; reload-only PID43719 unchanged, TKB/auth preserved. Actual credentials SELECT1 passed24/24 across5432/5433. Pipeline141011 root success masked3failed+3canceled ordinary jobs; prior Nomad worker fatal08P01 auth failure. User-approved ordinary retry jobs3230100–3230105 allSUCCESS; all6Nomad master-1767 running/healthy/restarts0 at2026-10-15 21:08UTC. [Evidence](../log/2026-10-15-postgresql-devops-898-tochka-pgbouncer-routes.md).
