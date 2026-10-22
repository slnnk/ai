# TODO: the single backlog

The only live list of open work: company, personal and knowledge-base tasks. Notes in
`knowledge/log/` and `knowledge/systems/` keep their "Open items" as a dated snapshot; the
current state lives here.

Rules for agents:
- A new open item from your work goes here, under the right layer and system, as
  `- [ ] <action> (YYYY-MM-DD) — [src](<path to the note>)`. Do not keep a separate list
  in the note; the note may describe the risk, this file tracks the action.
- Closing an item: `[x]`, add `done YYYY-MM-DD` and a link to the evidence; move it to
  "Done" at the bottom. Delete done items after a month.
- Before starting work on a system, read its section here.
- `due YYYY-MM-DD` right after `- [ ]` makes `ai-sync.sh` print the item as a reminder on
  every daily sync from that date until it is closed.

Paths below are relative to `~/ai/`.

---

## YouDo (`current`)

### content / production S3

- [x] Prepare Selectel correlation for slow youdo-photos PUT: sampled trace148ae312ae4a95 shows24.246sS3/24.559saction, trace127cc1a1ed5770 thumbnail10.918s; reference currentofficialincident406434published13:57Moscow (slowuploads/500andfastretry409mechanism) and earlier406285resolved05:47; correlate earlier11:09/11:29symptoms and actualonset (2026-10-19) — [src](current/knowledge/log/2026-10-19-content-selectel-s3-put-latency-comparison.md) — Closed by user 2026-10-19: cause attributed to the Selectel incident; further incident diagnostics cancelled, not implemented.

- [x] Review Shift248 C2C creation outcome before retry; address Business30s deadline versus seven sequential successful Content uploads taking37.729s and obtain a sampled representative upload trace separating SQL, two storage writes, limiter wait and JPEG processing; historical incident flags00/0 yielded no saved spans, CPUthrottling counters0 (2026-10-19) — [src](current/knowledge/log/2026-10-19-content-s3-thumbnail-conflicts.md) — Closed by user 2026-10-19: cause attributed to the Selectel incident; further incident diagnostics cancelled, not implemented.

- [x] Diagnose repeated Content thumbnail PUT409 and anomalous object Max384/2026.10.19/21498533.jpeg: zero-filled prefix/empty ETag/HEAD200 but no list entry; correlate recorded S3 read request IDs with Selectel and obtain failed-PUT details. Eight keys now HEAD200; original JPEG header verified; bucket limits disabled per user screenshot (2026-10-19) — [src](current/knowledge/log/2026-10-19-content-s3-thumbnail-conflicts.md) — Closed by user 2026-10-19: cause attributed to the Selectel incident; further incident diagnostics cancelled, not implemented.


- [x] DevOps-898 HoustonV2Mock0.0.35 deployed by user through staging3232321/pipeline141077SUCCESS; VK1sharedallocationhealthy/0restarts/Consulpassing, test5Swagger+experimentsHTTP200. WrongSelecteljobuserdeleted, explicit-targetfixMR21verified (2026-10-16) — [src](current/knowledge/log/2026-10-16-nomad-test-devops-898-houstonv2mock-vk-assessment.md)

- [x] DevOps-898 Hub MongoDB256MiB released2.7.7by user merge/tag; CI141063/staging3232118SUCCESS, runtime memory256/healthy/0Mongo restarts verified (2026-10-16) — [src](current/knowledge/log/2026-10-16-nomad-test-devops-898-hub-mongodb-memory.md)

- [x] DevOps-898 Hub2.7.7+classifier2.6.10 deployed as shared VK services, emptyMongoaccepted; user merged/tagged, bothGitLabstagingSUCCESS/runtimehealthy/Consulpassing/HTTP200 (2026-10-16) — [src](current/knowledge/log/2026-10-16-nomad-test-devops-898-hub-mongodb-memory.md)

### Security: leaked or plaintext credentials

- [ ] Review exposed inline Consul token in automation-test-yandex nomad_environment.json.j2 Services.Consul.Token; determine validity and move/rotate under separate authorization (2026-10-21) — [src](current/knowledge/log/2026-10-21-nomad-test-monolith-data-dependencies.md)

- [ ] Review validity and rotate exposed inline APNs key at automation-test-yandex environment.json.j2 Push.Apns.PrivateKey; move to external secret under separate authorization (2026-10-21) — [src](current/knowledge/log/2026-10-21-nomad-test-daily-compilations-missing.md)

- [ ] Review/rotate hardcoded NuGet source credential in gitlab-ci-templates v3/.dotnet-nuget.yml:53; value encountered during read-only CI audit, record location only and use external CI secret under separate request (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-14-nomad-test-devops-898-service-build-retries.md)

- [ ] Rotate yc authorized key `aje1kjc599tg2oj7ok2d` (private part leaked into session output), update consumers, delete the old key (2026-09-13) — [src](companies/youdo/knowledge/log/2026-09-13-workstation-yc-cli-auth-recovery.md)
- [ ] Rotate the c2c prod PostgreSQL password printed in an agent session; consider a separate read-only role for agents (2026-09-23) — [src](companies/youdo/knowledge/log/2026-09-23-selectel-c2c-prod-postgres-access.md)
- [ ] Rotate the `dba_automation` SQL password disclosed in diagnostic output (2026-08-02) — [src](companies/youdo/knowledge/log/2026-08-02-mssql-yandex-mssql-restore-youdo.md)
- [x] DevOps-898 BuildAPI: VK release 0.5.13/pipeline 140932/manual deploy 3226672 complete; scoped CI kubeconfig and Vault role ready, existing Nomad token reused, 5 workloads Ready/PVC Bound/HTTP 200 (done 2026-10-15 Moscow) — [src](companies/youdo/knowledge/log/2026-10-15-dev-deployment-devops-898-buildapi-existing-nomad-token.md)
- [x] BuildAPI VK aliases: additional DNS work declined by user (“Не нужно”); existing wildcard observation retained, no DNS changes made; primary buildapi.dev.youdo.corp works (cancelled 2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-dev-deployment-devops-898-buildapi-existing-nomad-token.md)
- [ ] `buildapi/production.nomad`: check validity of plaintext `NOMAD_TOKEN`, `JENKINS_LOGIN`, `JENKINS_PASSWORD`; move to Vault and rotate (2026-09-13) — [src](companies/youdo/knowledge/log/2026-09-13-nomad-test-buildsinfo-csi-stale-attachment.md)
- [ ] Android/GitLab runner host_vars hold plaintext access material: migrate to Ansible Vault, rotate, verify runner registration/registry/S3 cache (2026-08) — [src](companies/youdo/knowledge/systems/android-farm/ci-cd.md), [src](companies/youdo/knowledge/systems/gitlab-ci/android-youdo4-dynamic-runner.md)
- [ ] `fastlane-docker` worktree: untracked Firebase service-account JSON; move to a protected GitLab file variable, keep ignored (2026-08) — [src](companies/youdo/knowledge/systems/android-farm/ci-cd.md)
- [ ] Android autotest reports: stop `--acl public-read` on Yandex Object Storage, redact headers and credential-bearing app URLs from HTML logs/capabilities (2026-08-12) — [src](companies/youdo/knowledge/log/2026-08-12-android-farm-autotests-report-3063278.md)
- [ ] Nexus `raw-private` is anonymously downloadable by URL: fix access; delete the ADB-key archive `/root/android-avd-nexus-5x-template-api29-20260805.tar.zst` on M-K0057 (2026-08-04) — [src](companies/youdo/knowledge/log/2026-08-04-android-farm-avd-template-transfer.md)
- [ ] Replace the workstation `~/.vault-token` with `root` policy by a token limited to `ansible-infra` (coordinate with the owner); ask Vault admins to map the LDAP group to read `secret/ansible/{prod_selectel,prod_yandex,common}` (2026-09-18) — [src](companies/youdo/knowledge/systems/automation-services/local-vault-ansible-access.md)
- [ ] infra-tf `dev/config/vmalertmanager.yml` and `prod/config/vmalertmanager.yml`: plaintext Rocket.Chat webhook token; move to Vault and rotate (2026-10-07) — [src](companies/youdo/knowledge/log/2026-10-07-dev-deployment-devops-886-ttl-controller.md)
- [ ] sc-except: move secrets out of `/data/docker-compose.yml` and Zabbix scripts (2026-06-13) — [src](companies/youdo/knowledge/log/2026-06-13-sc-except-mssql-unavailable.md)

- [x] Jenkins AutoTest: applied dnsmasq role; private youdo.local DNS works on host and agent container (2026-10-16) — [src](companies/youdo/knowledge/log/2026-10-16-jenkins-autotest-buildsinfo-local-dns.md)
- [ ] Jenkins: review/rotate inline curl -u credentials in legacy test buildsinfo and youdo_web_testing_one job builder configuration after diagnostic output exposure; do not record values (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-jenkins-devops-892-job-launch-audit.md)

### dev-deployment (B2B ephemeral dev, DevOps-832, DevOps-A-50)

Post-deploy autotests (DevOps-832), state checked in GitLab 2026-09-28:
- [ ] Tochka tests: 121 failures from removed `/v1/beneficiaries/createPerson`/IE (Site-24856); hand to QA to switch steps to v2 before relying on the Tochka suite (2026-09-29) — [src](companies/youdo/knowledge/systems/dev-deployment/post-deploy-autotests.md)
- [ ] Main `youdo.business` + `youdo-business-tests` + `youdo-business-ui-tests`: plan proposed 2026-09-28, awaiting decisions (endpoints, plugin `precondition` and `lib` in `youdo-business-tests-plugin`, test-client, UI template, memory); see the map section "youdo.business suite" — [src](companies/youdo/knowledge/systems/dev-deployment/post-deploy-autotests.md)
- [ ] TKB: two `IdentifyToBeneficiaryTest` failures (Billing `ACCOUNT_NOT_FOUND` for ephemeral accounts) remain after the memory fix; hand to QA/app owners — [src](companies/youdo/knowledge/log/2026-09-07-dev-deployment-tkb-pipeline-138093.md)
- [ ] Persist the `AuthRedirectUrl` / `business-mock-api-{buildId}.dev.youdo.sg` ingress correction in `youdo.business/devops/dev.yml` (only live-patched) — [src](companies/youdo/knowledge/log/2026-09-03-dev-deployment-devops-832-tochka-dev-autotests-prepared.md)
- [ ] Next fresh namespace: verify merged doc-generator and automation-web memory (512Mi/1Gi) under relevant load — [src](companies/youdo/knowledge/log/2026-09-04-dev-deployment-devops-832-handoff.md)
- [ ] Final closeout: first MR in Tochka/TKB/Billing after the merge must run deploy -> auto smoke on `autotests:latest` (proves the released images); youdo.business + UI still pending; then representative end-to-end deploys from `master` refs (auto smoke, manual regression, Allure/JUnit, cleanup); update DevOps-A-50 and the system map — [src](companies/youdo/knowledge/log/2026-09-03-dev-deployment-devops-832-tochka-dev-autotests.md)
- [ ] Contract tests: strict `DEV_NAMESPACE` validation and `TARGET_ENV_SUFFIX` derivation (empty, malformed, max length) — [src](companies/youdo/knowledge/systems/dev-deployment/post-deploy-autotests.md)

Platform hardening (roadmap phases 1, 3, 4):
- [ ] Failed first deploy leaks the namespace (no GitLab deployment, no `on_stop`): export dotenv/environment even on failure, or let Jenkins clean up / TTL controller (2026-10-06) — [src](companies/youdo/knowledge/log/2026-10-06-dev-deployment-hide-employee-api-swagger-namespace.md)
- [ ] Name length: guard Helm release names (53) and all generated names (StatefulSet pod labels/hostname, not only migration Jobs) against 63 chars, or shorten the branch-slug namespace suffix (2026-10-06) — [src](companies/youdo/knowledge/log/2026-10-06-dev-deployment-hide-employee-api-swagger-namespace.md)
- [ ] Jenkins lock keyed by the final namespace (GitLab `resource_group` is per project/ref; proven 2026-09-29: three services on task DevOps-832 deployed into `dev-devops-832` at once, Jenkins 166 failed with Helm `another operation ... is in progress`, smoke of 164/165 rejected by the ownership check) — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md)
- [ ] HTTP health smoke stage after rollout, driven by service health config — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md)
- [ ] `values.schema.json` and template regression tests for `ephemeral-namespace` and `microservice` charts; include 63-char migration Job name cases and a central name helper (2026-09-30: `helm-charts` `master` `4ab8743` shortened the name to `<projectName>-m<type>` but has no `trunc 63` guard) — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md), [src](companies/youdo/knowledge/log/2026-08-30-dev-deployment-jenkins-test-142-migration-job-name-length.md)
- [ ] Document source of truth/owner for Vault role `dev-ephemeral-deployer`; restrict `~/.kube/config-yandex-dev` permissions — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md)
- [ ] Reconcile or archive stale docs: `helm-charts/docs/agents-ephemeral-deploy-plan.md`, `helm-charts/AGENTS.md`, `examples/jenkins/Jenkinsfile.ephemeral-namespace` (`docs/ephemeral-namespace-role.md` rewritten in DevOps-883 branch 2026-10-07) — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md)
- [ ] Verify `youdo-notifications` and `docvalidation` fallback and ephemeral routing independently — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md)
- [ ] Rename Jenkins pilot job `test`, update the shared CI default/variable — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md)
- [ ] Monitoring: Helm release records in `default` without their namespace, stale `dev-*` namespaces, failed migrations, Vault secret failures, expired GitLab environments with live resources — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md)
- [ ] Operator docs: routine cleanup and recovery commands — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md)
- [ ] Delete stale stopped GitLab environments in docvalidation: id 440 `dev/youdo-microservices-docvalidation-` and 441 `...-devops-689-k8s`; names already use `dev/$CI_COMMIT_REF_SLUG`, `CI_PIPELINE_ID` gone (checked 2026-09-30) — [src](companies/youdo/knowledge/systems/dev-deployment/gitlab-ci-deploy-dev.md)
- [ ] Deferred by user 2026-10-08: reconsider `service.enabled: false` behavior in helm-charts before changing it; worker/scheduler expose a Hangfire status endpoint, so first determine the required Service/Ingress routes and preserve access. `microservice/templates/service.yaml:4` `ne ($serviceConfig.enabled | default true) false` renders a Service for explicit `false` (checked 2026-09-30); recipe [default true overrides false](general/knowledge/helm/default-true-overrides-false.md) — [src](companies/youdo/knowledge/log/2026-06-25-dev-deployment-docvalidation-dev-yml.md)
- [ ] Helm list merge makes generated `services[]` overrides fragile; move to a separate dependencies section or a fully merged values file; still a list at `microservice/values.yaml:197` in `4ab8743` (checked 2026-09-30) — [src](companies/youdo/knowledge/log/2026-06-18-dev-deployment-ephemeral-dev-dependencies.md)
- [ ] Vault `secret/dev/projects/youdo-kitcut`: add `SentryDsn` or fix the mapping; youdo.kitcut `b31af25` `devops/dev.yml:41-43` still maps `Sentry__Dsn: SentryDsn`, Vault key not checked (checked 2026-09-30) — [src](companies/youdo/knowledge/log/2026-06-17-dev-deployment-youdo-business-auth-service-jenkins-dev.md)


Deferred, decide later: Adminer / DB discovery; `youdo-business-tickets` onboarding — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md)

QA-owned, not DevOps: `ignoreFailures=true`; smoke/regress tag separation; Billing `GetYouDoBalanceHistoryTest` assertions; Tochka hard-coded token fallback — [src](companies/youdo/knowledge/log/2026-09-04-dev-deployment-devops-832-handoff.md)

### nomad-test / Consul (Yandex test)

- [x] Kafka MR3 merged with explicit approval as627242c9; pipeline141395/staging3242525 SUCCESS, full isolated kafka-vk-test healthy/alltasksrestart0, Consulpassing and REST/brokers200; existing VMbroker unchanged, productionmanual (2026-10-21) — [Kafka](current/knowledge/log/2026-10-21-nomad-test-kafka-vk-full-job.md)
- [x] Subcategory-predictor production promoted by user; deployment0a973c76SUCCESS/Promotedtrue/2of2healthy, both active replicas1.0.8/running/restart0, Consulpassing and health200; pipeline141391/deploy3242503SUCCESS (2026-10-21) — [src](current/knowledge/log/2026-10-21-nomad-test-subcategory-predictor-vk.md)
- [ ] Proposals: restore remaining monolith dependencies price-predictor, customer-task-recommendations and taskqualitycontrolfortest; taskqualitycontrol directly accounts for8Jenkins2020failures. Predictor retrycontract3242527/load3242528SUCCESS, readiness barrier optional rather than a blocker; Kafka REST restored (2026-10-21) — [inventory](current/knowledge/log/2026-10-21-nomad-test-monolith-data-dependencies.md), [predictor](current/knowledge/log/2026-10-21-nomad-test-subcategory-readiness-kafka-rest.md)

- [x] Recommendations mock0.0.16 restored by user rollout: MR14merged74f4115e, master141384/release141385/deploy3242474SUCCESS; registrydigest, VKhealthy0restarts/Consulpassing/root200 independently verified, no remote fixture writes (2026-10-21) — [src](current/knowledge/log/2026-10-21-nomad-test-recommendations-mock-vk.md)

- [x] Prepared: prepare restoration of shared data/daily-compilations subscription API in VK test; audit current CI, image and database prerequisites, obtain repository/deployment approvals before changes (2026-10-21) — [src](current/knowledge/log/2026-10-21-nomad-test-daily-compilations-missing.md) Preparation complete without CI edits; direct Nomad registration remains an unapproved exception.

- [x] Published: review and publish prepared daily-compilations staging CI dc/proxy=vk-test only, retaining the standard CI-supplied image version, then separately approve deployment with new empty PostgreSQL database; Nomad address/token unchanged, user requested no checks (2026-10-21) — [src](current/knowledge/log/2026-10-21-nomad-test-daily-compilations-missing.md) Completed as ef37ce8/MR9 on 2026-10-21; no merge or deployment.

- [x] Reviewed: review daily-compilations MR9 and pipeline141345, resolve VK Nomad address/token selection before separately approved merge/release/deployment; dc/proxy change published, no runtime changes (2026-10-21) — [src](current/knowledge/log/2026-10-21-nomad-test-daily-compilations-missing.md) MR9 user-merged as b1901e5; release0.5.15 build/release passed; staging3241027 failed403 against inherited old endpoint (2026-10-21).

- [x] Superseded/completed: configure project-only staging NOMAD_STAGE_ADDR/TOKEN for VK in daily-compilations, then separately approve retry of failed deployment3241027; release0.5.15 built, old inherited target caused submission403, VK job absent (2026-10-21) — [src](current/knowledge/log/2026-10-21-nomad-test-daily-compilations-missing.md) User selected Data-group correction instead; group values updated and temporary project overrides removed, independent GET verified (2026-10-21).

- [x] Completed via user retry: retry daily-compilations staging job3241027 after user-approved Data-group VK address/token correction, then verify allocations and API health; requires separate deployment approval (2026-10-21) — [src](current/knowledge/log/2026-10-21-nomad-test-daily-compilations-missing.md) User retry3241056 SUCCESS; API0.5.15 and PostgreSQL running/restarts0, Consulpassing and health/users GET200 verified (2026-10-21).

- [x] User promoted healthy daily-compilations0.5.15 production deployment edf404b3, then monitor rollout and job3241028 to terminal result; canary healthy/restarts0, shared health200, monitoring alone grants no promotion permission (2026-10-21) — [src](current/knowledge/log/2026-10-21-nomad-test-daily-compilations-missing.md) Completed: job3241028/pipeline141347 SUCCESS; production rollout2/2healthy/API0.5.15/0restarts, Consulpassing and health200 GET-verified (2026-10-21).

- [ ] Proposed: inspect RabbitMQ test1 exchange properties/bindings and prepare correction for youdo.user.signin and youdo.user.signout2 auto_delete mismatch; preserve consumers/bindings, obtain explicit approval before any runtime change; verify signin latency and event publication afterward (2026-10-20) — [src](current/knowledge/log/2026-10-20-nomad-test-test1-monolith-rabbitmq-exchange-latency.md)

- [x] Escrow job3236554 Docker DNS recovery: user follow-up plus fresh runner105 queries confirm both172.28.0.8/.9 return10.18.26.17 and host TCP1433 connects; immediate NXDOMAIN resolved, uncached stability/SQL authentication/CI retry unverified, no agent external changes (2026-10-20) — [src](current/knowledge/log/2026-10-20-nomad-test-escrow-job-3236554.md)

- [ ] HoustonV2Mock CI: consider persistent Buildx attestation compatibility setting for future releases; current0.0.34recovery uses pipeline-only override, no extra source changes requested (2026-10-16) — [src](current/knowledge/log/2026-10-16-nomad-test-devops-898-houstonv2mock-vk-assessment.md)

- [x] TKB ordinary retries3230094–3230099 after approved PgBouncer auth/routes fix: all6GitLabSUCCESS/Nomadhealthy/restarts0 (2026-10-16) — [src](current/knowledge/log/2026-10-15-postgresql-devops-898-tkb-pgbouncer-auth-failure.md)
- [x] Tochka ordinary retries3230100–3230105 after approved12PgBouncer routes: all6GitLabSUCCESS/Nomadhealthy/restarts0 (2026-10-16) — [src](current/knowledge/log/2026-10-15-postgresql-devops-898-tochka-pgbouncer-routes.md)

- [x] Cerberus2: standard GitLab redeploy with normal DBrecreation completed onall14stands; all14jobsSUCCESS/Nomadhealthy,42startupmarkers/current3ActiveperDB/noorphanActive, includingtest1/2/6/7. Manualmembershipproposaldiscarded/noSQLrepair; test11oneinitialrestartrecovered. Runtime5433/NoResettrue/30s verified, PG280total/Cerberus20/noqueue. Usercorrection: GitLabdeploydefault, retainnormalDBresetpolicy (done2026-10-16) — [src](current/knowledge/log/2026-10-16-nomad-test-cerberus-standard-gitlab-rollout.md)

- [x] DevOps-898 TKBmaster267/Tochkamaster1767 ordinary test10–test15 retries accepted after approved PgBouncer repair: all12GitLabSUCCESS/Nomadhealthy/restarts0. Billing707/MobileID58 already accepted; main Business remains last (2026-10-16) — [src](current/knowledge/log/2026-10-15-nomad-test-devops-898-four-b2b-repositories-preflight.md)

- [x] DevOps-898 Billing: user-deployed master-707/pipeline141010 ordinary test10–test15 jobs all SUCCESS/Nomad all6running/healthy/restarts0, read-only verified20:31UTC (done2026-10-15) — [src](current/knowledge/log/2026-10-15-nomad-test-devops-898-billing-user-rollout.md)

- [ ] DevOps-898 Billing production/release: parent141010 last running; verify independent production/release outcome separately, stand rollout accepted (2026-10-15) — [src](current/knowledge/log/2026-10-15-nomad-test-devops-898-billing-user-rollout.md)

- [x] DevOps-898 Mobile ID: user-deployed master-58/pipeline141008, ordinary jobs3229736–3229741 all SUCCESS/Nomad test10–test15 running/healthy/restarts0; read-only verified (done2026-10-15) — [src](current/knowledge/log/2026-10-15-nomad-test-devops-898-mobile-id-user-rollout.md)

- [x] DevOps-898 notifications: master-190 ordinary parallel deploy test10–test15 with DB recreation, jobs3229634–3229639 all SUCCESS/Nomad healthy/restarts0 (done2026-10-15) — [src](current/knowledge/log/2026-10-15-nomad-test-devops-898-notifications-b2b-rollout.md)

- [ ] DevOps-898 notifications production/release: downstream141004 last running, check final outcome separately; stand deployment accepted (2026-10-15) — [src](current/knowledge/log/2026-10-15-nomad-test-devops-898-notifications-preflight.md)

- [x] DevOps-898 auth-service: master-168 accepted on test10–test15 after B2BPG/PgBouncer1000 capacity fix and approved parallel ordinary retries, all6GitLab SUCCESS/Nomad healthy/restarts0 (done2026-10-15) — [src](current/knowledge/log/2026-10-15-nomad-test-devops-898-auth-service-b2b-rollout.md)

- [ ] DevOps-898 auth-service auto production downstream141002 last scheduled; check final production/release status separately, stand rollout already accepted (2026-10-15) — [src](current/knowledge/log/2026-10-15-nomad-test-devops-898-auth-service-preflight.md)

- [x] DevOps-898 SMS: master-191 deployed in parallel to test10–test15 using ordinary jobs with DB recreation; all6GitLab SUCCESS/Nomad healthy, all14target stands latest/healthy (done2026-10-15) — [src](current/knowledge/log/2026-10-15-nomad-test-devops-898-sms-b2b-rollout.md)

- [x] DevOps-898 keep-db routing: user merged MR91, mergeef128336/squash0cf1dde, GET verified; removes18child overrides, CI Lint/inheritance checks passed (done2026-10-15) — [src](current/knowledge/log/2026-10-15-gitlab-ci-devops-898-keep-db-vk-routing.md)

- [x] DevOps-898 Business master-21509: MR120 user-merged585b5992, approved ordinary retries3230182–3230187 all6SUCCESS/Nomadrunninghealthy/restarts0, all66taskimage references master21509. B2B13-service catalog delivery complete on test10–test15 with shared doc-generator (2026-10-16) — [src](current/knowledge/log/2026-10-16-nomad-test-devops-898-business-rollout.md)

- [x] DevOps-898 B2B Landings: master-109/pipeline141019 ordinary jobs3230150–3230155 allSUCCESS, Nomad test10–test15running/healthy/restarts0; user-approved deployment after nginx port fix MR19 merge, status-only verified00:08:46MSK (done2026-10-16) — [src](current/knowledge/log/2026-10-16-nomad-test-devops-898-landings-b2b-rollout.md)

- [x] DevOps-898 Landings production/release: pipeline141019 canary3230158/update3230159/release3230161 all SUCCESS verified; B2B stand rollout accepted (2026-10-16) — [src](current/knowledge/log/2026-10-16-nomad-test-devops-898-landings-b2b-rollout.md)

- [x] DevOps-898 Kitcut: master-103 ordinary parallel jobs3229673–3229678 test10–test15 SUCCESS/Nomad running/healthy/restarts0, recreate_db=false preserved, no source edits (done2026-10-15) — [src](current/knowledge/log/2026-10-15-nomad-test-devops-898-kitcut-b2b-rollout.md)

- [ ] DevOps-898 Kitcut production/release: child141006 last running; check final outcome separately, stand rollout accepted (2026-10-15) — [src](current/knowledge/log/2026-10-15-nomad-test-devops-898-kitcut-preflight.md)

- [x] DevOps-898 DocValidation: master-757 ordinary parallel deploy test10–test15 with DB recreation, jobs3227436–3227441 SUCCESS/Nomad healthy; latest release accepted on all14target stands (done2026-10-15) — [src](current/knowledge/log/2026-10-15-nomad-test-devops-898-docvalidation-b2b-rollout.md)

- [x] DevOps-898 Fns: master-598 deployed in parallel to test10–test15 with ordinary jobs/DB recreation, all6GitLab SUCCESS/Nomad healthy/restarts0; C2C8same release verified, no repo changes needed (done2026-10-15) — [src](current/knowledge/log/2026-10-15-nomad-test-devops-898-fns-preflight.md)

- [x] DevOps-898 current user-approved launch: ten single services and LogReader test5 deployed through GitLab and runtime-verified; Socket per-stand reverse MR82 merged, unused vks excluded/MR18 closed without merge/tag/deploy. Public-test unchanged; no YouTrack closure (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-14-nomad-test-devops-898-implementation.md)
- [x] Restore LogReader1.0.39 to all14active stands before YouTrack comment updates:13Consul endpoints corrected, persistent project stand variable saved, pipeline141021/build/tests/deploy3230221SUCCESS;14Nomadhealthy/Consulpassing/HTTP200/0restarts, SQLSELECT1 verified14/14 (done2026-10-16) — [src](current/knowledge/log/2026-10-16-nomad-test-logreader-all-active-stands.md)

- [x] DevOps-893: closed by user; published commit22e451e/MR440, VK CI plan/apply succeeded, all eight jobs checked, CSI8/8healthy and SSD lifecycle passed. Further plan convergence check waived by user; version difference is a hypothesis. External applications excluded (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nomad-test-devops-893-vk-ci-publication-preparation.md)

- [ ] agent-test-01: remove dnsmasq `log-queries` or log to a separate rotated file; size-based syslog rotation; check filesystem alerts before 100% (2026-09-22) — [src](companies/youdo/knowledge/log/2026-09-22-nomad-test-agent-test-01-disk-full.md)
- [ ] Night shutdown: collect Nomad/Consul versions, job `disconnect`/`reschedule` settings, host/CSI volumes, morning recovery window, cost of the 9 client VMs (2026-09-09) — [src](companies/youdo/knowledge/log/2026-09-09-nomad-test-night-shutdown-cost.md)
- [ ] After the next agent-group power-on: 9/9 nodes ready, quorum, blocked evals -> 0, `proxy.service` DNS vs nginx upstreams, CSI and periodic jobs (2026-09-11) — [src](companies/youdo/knowledge/log/2026-09-11-nomad-test-agent-group-stop-pilot.md)
- [ ] Follow up `http-headers-viewer` port conflict, `similar-tasks/indexer` prestart failure, stale `spb2` child of `jaeger-index-cleaner`; do not scale below 7 clients without reconciling reservations (2026-09-13) — [src](companies/youdo/knowledge/log/2026-09-13-nomad-test-agent-scale-down.md)
- [ ] Resource optimization: next iteration with pooled cross-stand soft reservation and global peak hard max; monitor OOM/restarts after lowered reservations (2026-09-13) — [src](companies/youdo/knowledge/log/2026-09-13-nomad-test-resource-optimization.md), [src](companies/youdo/knowledge/log/2026-09-09-nomad-test-automation-test-yandex-nomad-memory.md)
- [ ] Upgrade Nomad from `1.5.3` (all 7 clients and 3 servers on Yandex test, API 2026-09-30), fix `KillMode=process` (still in `automation-test-yandex` `deprecated/roles/nomad-client/templates/nomad.systemd.j2:10`); clean stale `/var/lib/nomad/alloc` on agent-test-02 (2026-07-21) — [src](companies/youdo/knowledge/log/2026-07-21-nomad-test-agent-test-02-crash-loop.md)

- [ ] Jenkins controller DNS: integrate verified standalone dnsmasq role/overrides into canonical automation-services Jenkins configuration on an approved task branch; preserve unrelated changes (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md)
- [x] DevOps-894: working dynamic_deploy ES runtime acceptance verified on test5 in build5826 SUCCESS with ELASTIC=true; standalone thin/thick checks previously passed (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-build5826-plan-reconciliation.md)
- [x] DevOps-894: Jenkins ES-only test job/credentials created; controller dnsmasq and global dc fixed; check3, full thin/test5 build5 and thick/test40GiB build6 SUCCESS; large ES dataset74,235,448docs verified (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-14-nomad-test-devops-894-jenkins-es-plan.md)
- [ ] DevOps-894: Cinder readiness wait and repeat test/thick reset verified: full deploy89.680s, repeat102.438s without manual force; automation published via Draft MR104; separately adapt DBA_Clean destination and restore AWX weekly workflow (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nomad-test-devops-894-playbook-adaptation.md)
- [x] DevOps-894: user-approved ES healthy_deadline2m/progress_deadline3m applied to templates and all14stands; simultaneous full deployment passed121.790s without retries (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-14-nomad-test-devops-894-es-unlimited-redeploy.md)
- [x] DevOps-891 / DevOps-894: ES/head mirrors released via MR40 and rolled out to all13requested stands; DevOps-894 automation published via Draft MR104; Jenkins thin/thick deployments verified by builds5/6 (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-14-nomad-test-devops-891-es-image-mirrors.md)

### Cerberus2 / production


### automation-services (nginx, Ansible)

- [x] DevOps-897: verify VK MSSQL image and manually deliver CleanYouDo.bak90.1GiB to share10.18.26.4; active400GiB image confirmed, copied backup datedOct11, size/mtime verified, checksum skipped at user request (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-14-nomad-test-devops-897-mssql-vk-preflight-and-backup.md)

- [ ] DevOps-897: publish/review completed seven-stage VK MSSQL adaptation and apply previously planned stage1 prepared-image default; approved task branch/local uri adaptation withSSD400GiB and5fixturecases, base VM10.18.26.9 DHCP repaired/step1green, step2reboot completed with ignoredWindowsUpdate failures, step3restore completed/baseSHUTOFF, preparedimage active400GiB/stage4cleanup completed2026-10-15, stage5done/noexistingtargets; stage6completed2026-10-15 all3ACTIVE/high-iops400GiB/MS1 and WinRM passed, stage7completed2026-10-15 renames/Zabbix/SQL-server-name correction/reboots passed all3, full runtime run complete; application/SQL contents/monitoring ingestion unverified; publication pending; Jenkins5832 old thick SQL endpoint fix published as cdb11b5/[MR113](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/113), user-authorized MR113 merge completed/mastercf88e422 endpoint fields verified; endpoint retry/verification closed on user-reported successful playbook2026-10-15 (no independent new build/log check); full workflow publication remains pending ([diagnosis](companies/youdo/knowledge/log/2026-10-15-jenkins-build5832-mssql-old-endpoint.md)); migrate DBA_Clean delivery separately from one-time manual copy (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-14-nomad-test-devops-897-vk-mssql-adaptation.md)
- [ ] MSSQL optional proposals only: disk-image provenance on reuse and exact boot-disk attachment ownership on deletion; user rejected adding new checks to DevOps-897 current run, implement only under separate request (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-14-nomad-test-devops-897-vk-mssql-adaptation.md)

- [x] DevOps-897: fix mcs.local query timeouts on8Nomad clients; route through IPsec/BIND10.18.20.3, private/system/Consul DNS verified8/8 (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-14-nomad-test-devops-897-dnsmasq-private-forwarding.md)
- [x] DevOps-897: publish automation-services one-line Nomad dnsmasq fix; user-approved06d4821a/MR1374, user merged master454ef804, pipeline140836skipped; normal DNS verified11/11nodes (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-14-nomad-test-devops-897-dnsmasq-private-forwarding.md)

- [ ] Yandex test nginx: dynamic upstream refresh for `proxy.service.yandex-test.consul` (or consul-template reload); drain procedure before removing a proxy client (2026-09-11) — [src](companies/youdo/knowledge/log/2026-09-11-automation-services-yandex-test-nginx-stale-nomad-proxy.md)
- [ ] Nexus nginx: fix client temp storage/buffering for large PUT uploads (HTTP 413/500) (2026-08-04) — [src](companies/youdo/knowledge/log/2026-08-04-android-farm-avd-template-transfer.md)
- [ ] prod_yandex GitLab runners: persist or roll back runtime-only `concurrent = 2`/`overlay2` on `10.16.24.173`; decide `docker builder prune`; review untracked host_vars in the worktree (2026-06-03); kept by the user 2026-09-30: runner host_vars moved to `deprecated/` in automation-services (AP-2228, `d3d6133c`), `10.16.24.173`/`concurrent = 2` not in the repo — [src](companies/youdo/knowledge/log/2026-06-03-gitlab-ci-prod-yandex-docker-3-dind-nexus.md)
- [ ] Apply the gitlab-runner playbook to the Selectel docker3 host (2026-06-04); kept by the user 2026-09-30: vars now in `deprecated/inventories/prod_selectel/host_vars/gitlab-runner-docker-3.yml` (`d13d56fd`), live host `gitlab-runner-dind03` — [src](companies/youdo/knowledge/log/2026-06-04-automation-services-prod-selectel-gitlab-runner-docker3-b2b.md)

### yandex-cloud / Terraform

- [ ] MSSQL refresh proposal: verify exact backup readability/type/date and destination capacity before dropping DB; add sqlcmd -b and guaranteed login re-enable on failure (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-889-mssql-recovery-plan.md)
- [ ] MSSQL refresh proposal: version prepared images and retain the last good image until acceptance; define retention and image quota needs separately (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-889-mssql-recovery-plan.md)
- [ ] MSSQL refresh proposal: distinguish missing resources from API errors and validate intended folder/resource before deletion; add quota preflight only if separately requested (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-889-mssql-recovery-plan.md)
- [ ] MSSQL refresh proposal: replace fixed waits/ignored errors with readiness checks for all three VMs, SQL hostname and monitoring; review xp_cmdshell dependency and fragile ping parsing (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-889-mssql-recovery-plan.md)
- [ ] MSSQL automation proposal: migrate plaintext credentials in SQL/Windows group_vars, tester task and inventory client to the established secret store; preserve values only in approved secret locations (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-889-mssql-recovery-plan.md)



- [x] DevOps-888: deploy a recovery cluster and CoreDNS after runnernetwork fix; job3217390 successful, nodeReady and refreshplan no changes (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-888-dev-k8s-e-recovery.md)
- [x] DevOps-888: review CI and merge MR !236 for already manually applied Terraform CI identity before another masterapply; kubeconfig exported/protected/tested, update CI integration after approval (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-888-ci-kubeconfig.md) — done 2026-10-09; MR merged/pipeline140514 converged, current CI kubeconfig delivered; variable update not performed by agent
- [x] DevOps-888: compare CI1.7.5 and local1.9.4 plans for empty in-place CI Secret diff in job3217580 before diagnosing token change (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-888-job-3217580.md) — closed 2026-10-09 after user CI apply and repeat plan no changes; exact cause unproven

- [ ] `yandex-tf/.gitlab-ci.yml`: `workflow:rules` for MR and default branch only (deferred by the user 2026-09-23) — [src](companies/youdo/knowledge/log/2026-09-23-yandex-cloud-yandex-tf-network-ansible-job.md)
- [ ] Ansible for `ipsec`/`balancers_test` is manual; nothing re-applies config after VM changes (2026-09-23) — [src](companies/youdo/knowledge/log/2026-09-23-yandex-cloud-yandex-tf-network-ansible-job.md)
- [ ] test-k8s: choose K8s version and upgrade chain, pin module source, fix `template_name`/default zone, re-plan; review SG egress and audit logging (2026-08-11) — [src](companies/youdo/knowledge/log/2026-08-11-yandex-cloud-yandex-tf-test-k8s-audit.md)
- [ ] K8s sizing for Nomad migration: 10-14 days of metrics, folder quotas, `maxPods`/pod CIDR, autoscaler 14-16 nodes (2026-08-11) — [src](companies/youdo/knowledge/log/2026-08-11-yandex-cloud-k8s-nomad-sizing.md)
- [ ] Temporal dev: review plan and apply in a change window; PVC backup policy; maintained PostgreSQL 16 image before prod — [src](companies/youdo/knowledge/systems/temporal.md)

### selectel


### ios-ci

- [x] Restore DNS reachability for `idcn-10`: user-approved Ethernet DNS `172.28.0.200` applied; default GitLab resolution/HTTPS pass, runner 93 online confirmed by GitLab GET at 21:32 MSK (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-ios-ci-runner-offline-dns-unreachable.md)
- [x] DevOps-880: release/TestFlight API-key auth verified by successful job 3230246 (v4.233.0); user confirmed APPLE_DEVELOPER_USER may remain and removal is unnecessary. Cleanup cancelled; local backlog item closed, external ticket unchanged (2026-10-20) — [src](current/knowledge/log/2026-09-14-ios-ci-fastlane-spaceauth-service-key.md)

### android-farm

- [ ] Restore `/opt/adb/adb_pkg.sh` on both Appium nodes or fix the CI contract; drop `|| true` masking; reconcile `EMULATORS="emulator_1 emulator_2"` with per-host inventory; fail fast on helper/IME errors (2026-09-08) — [src](companies/youdo/knowledge/log/2026-09-08-android-farm-android-dig-job-3121092.md), [src](companies/youdo/knowledge/systems/android-farm/system-map.md)
- [ ] Gate_K (Kazan): clean srv0 `192.168.60.10` leftovers (disabled dstnat/static, layer7 mangle marks, srcnat masquerade "DNS Forwarding for ...", IPsec `peer1` to `185.11.49.180`, `192.168.60.0/27` in `ip service ssh/ftp`); check whether `youdo.test` is still used in Kazan; update team doc `docs/infra/office.md` (2026-10-01) — [src](companies/youdo/knowledge/log/2026-10-01-android-farm-kazan-gate-k-dns-forward-to-decommissioned-srv0.md)
- [ ] Samsung A55 on M-K0057: reproduce create -> quit -> create race on port `15903` before changing timeouts (2026-09-08) — [src](companies/youdo/knowledge/log/2026-09-08-android-farm-android-dig-job-3121092.md)
- [ ] Validate `FailedTestSuite.xml` download (HTTP status, XML check) before Gradle (2026-09-07) — [src](companies/youdo/knowledge/log/2026-09-07-android-farm-android-dig-job-3120554.md)
- [ ] Trend memory pressure on M-K0057/M-K0058 and the M-K0057 iowait spike (2026-09-07) — [src](companies/youdo/knowledge/log/2026-09-07-android-farm-android-dig-job-3120554.md)
- [ ] Appium watchdog beyond `/status`; pre-session reset for MIUI/HyperOS overlays; staged Appium 1.22.3 upgrade with a canary (2026-08-12) — [src](companies/youdo/knowledge/log/2026-08-12-android-farm-appium-147-148.md)
- [ ] Hotfix pipeline fix on `DevOps-833-fix-hotfix`: merge and verify with a real hotfix build; protected environments for store jobs; pin images by digest (2026-08) — [src](companies/youdo/knowledge/systems/android-farm/ci-cd.md)
- [ ] CI suites: `InfoMessagesTestSuite` option is broken (XML and class absent); `MindBoxTestSuite` has zero enabled tests — [src](companies/youdo/knowledge/systems/android-farm/ci-suites.md)
- [ ] M-K0056: monitor Selenium Grid on `4444` in Zabbix; check active-checks timeout to `172.24.0.107:10051` (2026-08-13) — [src](companies/youdo/knowledge/log/2026-08-13-android-farm-selenium-hub-zabbix.md)

### Jenkins recovery (DevOps-892)

- [x] DevOps-903 Jenkins nginx cache cleanup: xargs -r validated, published d26e37e/MR122 and user-merged d9ee37a; fetched master verified, no live deployment (done 2026-10-20) — [src](current/knowledge/log/2026-10-20-jenkins-devops-903-empty-nginx-cache-cleanup.md)

- [ ] Rotate BuildAPI credential stored as buildsinfo_pass in automation-test-yandex/group_vars/all.yml after agent diff hunk-header exposure; do not record its value (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-static-vk-deploy-audit.md)


- [x] Merge static/common BuildAPI MR108 and configure project278 VK_TEST_NOMAD_TOKEN completed; build5823 passed config upload, no static deployment performed (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-static-vk-deploy-audit.md)


- [x] test5 Rabbit cleanup accepted by user for Jenkins after local clear.yml success (ok3/failed0/ignored0, no401); Jenkins rerun not claimed. Optional nginx empty-input handling remains separate (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-build5826-errors-and-disable-quiet-hook.md)


- [ ] Optional separate Restore hardening review (outside minimal VK address-adaptation scope): PG naming, MSSQL failure handling, Rabbit error reporting and S3 secret injection; do not implement during current deployment test (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-14-jenkins-restore-playbooks-review.md)


- [x] Verify actual Jenkins job launch and controller credentialed GitLab checkout: test-git4 SUCCESS, revision a240575a6a360a908005fb3f1814fca13ee6e065; agent checkout remains pending (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-jenkins-devops-892-git-smoke.md)

- [ ] Finish Jenkins VK recovery: controller/AutoTest restored, public HTTPS and controller checkout verified; dynamic_deploy5826 SUCCESS with Restore/ES/monolith/static/Suggestions. Remaining: AutoTest actual checkout/workflow; Airflow backup source/SSH/staging and verified fresh off-controller backup; align canonical Ansible image/DNS with working overrides. Monitoring and Git publication deferred by user. Public WebSocket forwarding only needed if agent uses public endpoint (2026-10-15) — [plan](companies/youdo/knowledge/log/2026-10-13-jenkins-devops-892-vk-recovery-plan.md), [latest acceptance](companies/youdo/knowledge/log/2026-10-15-jenkins-build5826-plan-reconciliation.md)

- [x] Persistent controller Git correction DevOps-891 complete: .dockerignore MR17 merged96a754a6, master pipeline140773SUCCESS, digest458ac695… deployed by approved recreation; root .git/key absent, stored-credential lookup205/master and API acceptance pass (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-jenkins-devops-891-fixed-image-recreation.md)

- [ ] Review and approve proposed Ansible recovery stages/guards, endpoint and secret parameters, DNS/Nginx rollback, Docker/containerd storage and consistent backup verification (2026-10-11) — [src](companies/youdo/knowledge/log/2026-10-11-jenkins-devops-890-recovery-runbook.md)

- [ ] Historical Yandex recovery follow-ups (superseded by the VK recovery above while Yandex is unavailable): verify representative workflows, restore backup DAG and monitoring; runtime changes require explicit approvals. Stage1 done October11: two-host/root inventory, Vault/registry authorization with VAULT_YANDEX_TEST_TOKEN. Stage2 done: both disks ext4/mounted at /data, UUID fstab entries and systemd mount units verified after approved daemon-reload. Stage3 done October11: backup restored and independently verified (11 jobs,116 plugins); Stage4 done October11: controller apply passed, API auth works,11 jobs/116 active plugins; Stage5 done October11: agent deployed, AutoTest online via WebSocket with5 executors. Stage6 done October11: public build.youdo.sg routes to newcontroller, HTTPS/API verified; localbalancer DNS/upstream persistence prepared. Publication completed October11 under explicit approval: five-file commit3ad647f0ff6ed5b8d17e14f42401b0577a5ede21, [MR !1368](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1368) targetingmaster; pipeline140550 skipped, no merge/deployment. User excluded recoveryinventory, which remains local/untracked; functional workflows/backup/monitoring still open (2026-10-10) — [plan](companies/youdo/knowledge/log/2026-10-10-jenkins-devops-890-recovery-audit.md), [stage 1](companies/youdo/knowledge/log/2026-10-11-jenkins-devops-890-inventory-dependencies.md), [stage 2](companies/youdo/knowledge/log/2026-10-11-jenkins-devops-890-data-disks.md)

- [x] BuildAPI latest-feature selection proposal cancelled by user on 2026-10-20: current release selection and badgekeeper redeployment are correct behavior; no fix required or implemented (investigation 2026-10-16) — [src](current/knowledge/log/2026-10-16-jenkins-badgekeeper-5848-version-selection.md)

- [x] Jenkins test2/test3/test7 deployment and BuildAPI follow-up closed by user on 2026-10-20: deployment now works correctly and BuildAPI updates; historical failures5828/5829/5830 retained as evidence, no new fixes or independent checks claimed;5831/test8SUCCESS was followed by user-approved retirement — [src](current/knowledge/log/2026-10-16-nomad-test-recovery-comment-completeness-recheck.md)

### Nomad cron image recovery (DevOps-895; base dependency DevOps-891)

- [x] Accept user-reported DevOps-895 closure: all eight cron image references restored; four post-restore parents/worker image identity and eighteen retained-history caveats remain documented, not additional restoration blockers. Cleaner excluded; further runtime audit only on separate user request (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-14-nexus-nomad-cron-runtime-audit.md)

- [x] Enable instance/shared runners for `data/dockers`: done by the user; build running (user-reported, 2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-gitlab-extraform-python-uv-runner-disabled.md)
- [x] Verify Python UV base build3222108: GET confirms success after user enabled instance runners; extraform retry3222248 then fails at frozen dependency download youdo-basis10.0.2 from legacy PyPI, recovery continues separately (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-recovery-plan.md)
- [x] Restore youdo-basis10.0.2: exact locked wheel/sdist rebuilt from unchanged source using historical tools, approved publication and Nexus metadata hashes verified (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-basis-recovery.md)
- [x] Build extraform0.31.17 locally from unchanged release GitSHA3c04a38b; image/runtime metadata verified and original checkout branch restored clean (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-basis-recovery.md)
- [x] Publish runtime-required extraform registry tag0-31-17 after approval; independent manifest/config digest matches local release-source image, no aliases/deployment/job execution (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-basis-recovery.md)
- [x] Inventory known company Nomad periodic parents:160jobs/23periodic/eightuniqueimages; extraform image restored for four tasks (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Restore four more periodic runtime images: daily-compilations-generator0.6.9/cashflowmaster/nexus-cleaner0.0.10/youtrack_sprints_creatormaster approved pushes exit0 and independent remote-config matches local images; with extraform five ofeight images cover19of23tasks. No deployments/periodic runs (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Build approved exact historical release copies rowers-ranker0.19.3 and recommended-tasks-generator1.16.24 with only five Pipfile.lock hash replacements: both original Dockerfiles/builds/safe metadata checks passed, tags and other source files verified unchanged; no Git or runtime publication (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Publish final three approved periodic runtime tags ab-pipeline:master/rowers-ranker:0.19.3/recommended-tasks-generator:1.16.24; push exit0 and independent configs match. Final manifest GETs verify8of8runtime refs for23periodic jobs; seven configs match our publications and cashflow:master is a verified later CI image, not overwritten. No job/deploy/merge (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)


### Nexus recovery (DevOps-890; Python libraries/PyPI included)

- [ ] DevOps-904: reduce Nexus CE requests before enforcement on 2026-11-13: disable background .NET workload advertising in applicable CI, DevOps-904 MR10113/pipeline141244 published as abc9c7ae1a5, CI SUCCESS, user retry3236903 verified warm-cache reuse across runners and npm2,835→924requests (67.4% reduction;922tarball requests remain; MR10113 user-merged as55ff066a0e1d on2026-10-20; release date unknown), verify full Business pipeline141254 and changed-input NuGet cache-mount reuse after MR3863 (approved single-line fix36ec7c61d published; user-run jobs3237183/3237312SUCCESS,125.70→24.59s, repeated restore/publish layers CACHED and zeroNuGet in repeat interval; first-window377requests shared with parallel builds; no merge/deployment); further monolith NuGet and residual npm investigation deferred by user on 2026-10-20 (monolith/npm enough for now), Tickets/Giveaway investigation completed:44/44cache extraction successes; migration EF phases repeat1,557ordinary NuGet requests across7jobs onOct19; propose consistent package path and explicit startup build before skipping redundant EF build (Giveaway Db/Bot distinction; implementation needs approvals), then measure a busy day; Oct19/20 runner/job comparison completed, monolith and Business internal-api identified as main sources; specific workload/NuGet implementation changes still require applicable approvals; one cold/warm pair measured; sustained busy-day effect remains to verify; remaining actions require their applicable approvals (2026-10-20) — [src](companies/youdo/knowledge/log/2026-10-20-nexus-ce-request-limit-analysis.md); [comparison](companies/youdo/knowledge/log/2026-10-20-nexus-gitlab-consumers-oct19-20.md)

- [x] Apply user-corrected recovery task scope and publish exact-GET-verified comments: Python/PyPI DevOps-890 comment74-124640 updated, cron images DevOps-895 comment74-124666 created, data/dockers base DevOps-891 comment74-124638 updated; unrelated content/Git names preserved (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-14-nexus-recovery-task-comment-reconciliation.md)

- [x] Configure Nexus LDAP under DevOps-890: FreeIPA LDAPS/CA, nexus-users wildcard read/publication, nexus-admins → nx-admin; connection/mapping and11GETchecks passed, user confirmed admin LDAP login (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-ldap-enabled.md)

- [x] Restore Nexus PyPI storage/repositories/CI identity: two File stores, private/proxy/group, nx-pypi/pypi applied after approval; exact GET configs and CI-auth200/invalid401 verified, unrelated settings preserved (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-recovery-plan.md)
- [x] User updated pypi.youdo.local DNS to10.18.24.233; supplied authoritative dig @172.28.0.9 at17:29MSK, TTL3600 (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-recovery-plan.md)
- [x] Verify pypi.youdo.local workstation default DNS propagation: resolves10.18.24.233, ordinary/simple request follows to group indexHTTP200 without forced address and without package downloads; prior stale DNS superseded. Runner171/172 host DNS/index200 also verified (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-recovery-plan.md)
- [ ] Check PyPI resolver behavior in actual runner containers as needed; successful local builds used explicit host mapping. Existing CI private publication endpoint is verified; legacy root POST mapping remains untested, no routing changes unless a demonstrated gap is separately approved (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [ ] Investigate data library CI queue cause if needed before remaining publish retries: project207 shared runners enabled, runner services active/poll204, pending-build instance/protected flags true; stale queue-flag hypothesis disproved. Original retry3222818 canceled for approved local fallback (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-basis-recovery.md)
- [x] Publish and Nexus GET-checksum-verify26of32required PyPI versions:5modern exact wheel+sdist,11Poetry exact-wheel-only,10setuptools exact-source requirements-only sdists without historical hashes (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Publish eventum1.0.1 reproduced exact wheel (poetry-core1.0.7); Nexus GET metadata verifies original SHA256 (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Obtain supervised local branch approval and prepare DevOps-891-restore-python-package-hashes from master in five consumer projects: user confirmed; ten hash-only replacements verified locally, no staging/commit/push/MR (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Build all five approved consumer repair branches locally with their original Dockerfiles: all build/safe metadata probe exit0 and expected package versions match (daily old-Python probe repeated with existing pkg_resources); full pytest/app/default-CMD/DB services not run and no image pushes (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Enable shared runners for the five consumer projects per explicit user instruction: only task-quality-control208 required authorized PUT; final GET verifies all five true, no pipeline retry/push/deployment (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Review five consumer diffs/checks and CI effects; user approved stage-two commits/push/MRs including automatic branch-image/latest effects. Five reviewed hash-only commits/MRs published, final remote SHA/MR parameters GET-verified, local checkouts clean and approved commit scope verified; no merge/deploy/tag move (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Verify explicitly authorized daily retry3223283 failed00:07:14MSK with first-RUN cgroup launch error after base pull (CLI/DinD19.03.12), samepipeline140782/SHAa6592bb2; no source/runner change, no push (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Approve daily-compilations task branch/master/MR8 reuse and add exactly three build-only Docker29.9.0 override lines; release/global references retained, semantic YAML/diff checks passed, index empty/no commit/push (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Approve and publish daily Docker29.9.0 build overrides: commit6e5c72a4 update docker cli and dind pushed, MR8 DevOps-891 restore python builds updated and remote SHA/body/settings GET-verified; localclean, latest effects approved/no merge/deploy (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Verify daily Docker29.9.0 correction140798/build3223284 success00:16:24MSK: branch/latest digest851d4a7f, no automated test job; MR8 unmerged, no deployment (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Merge daily-compilations MR8 after explicit approval/mergeability refresh/green140798: expectedSHA6e5c72a4, GET merged/master39b7fd86 at00:18:57MSK; ab/rowers untouched (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Verify daily-compilations post-merge master140799/build3223285 success00:20:13MSK at39b7fd86, master/latest digest0dd8eb93; sole build job/no automatedtests, no manual deployment/tag action (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Merge ab-pipeline MR50 and rowers-ranker MR79 after explicit user approval and green heads: expected SHAs/settings verified, GET merged/master7a430478 and f754bce4 at00:22MSK (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Verify ab-pipeline master140800 success00:24:14MSK: build/test/Nomad lint/Ruff/mypy all success, master/latest digest85eaaadb; productiondeploy3223291 remains manual/untouched (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Verify user-executed ab productiondeploy3223291 success00:25:48–00:25:53MSK via GET only; agent did not deploy, Nomad allocation/application health not checked (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Verify rowers-ranker master140801 success00:29:58.275MSK: build3223292/test3223293/Nomad lint3223294 success, master/latest digest7dbf90e3; all five MRs merged/all five master CIs green, no agent deployment (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Complete follow-up for initial recommended3223107/daily3223113 timeouts: explicitly approved recommended retry/pipeline passed; daily retry revealed cgroup launch error resolved by separately approved matching Docker29.9.0 build overrides with pipeline140798 success. Exact original timeout/network mechanisms remain unproven (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Verify explicitly authorized recommended-tasks-generator retry3223259 succeeded at23:51MSK: sameSHA5899dd9e, final branch/latest manifests digest1a1ceb2c; original push-timeout root cause unproven (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Obtain supervised task-quality-control branch reuse approval and apply minimal build-job Docker29.9.0-cli/DinD pin locally in .gitlab-ci.yml; exactly two lines, release job untouched, diff check passes, not staged/committed/pushed (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Validate/review task-quality-control two-line Docker29.9.0 build edit; user approved stage-two latest CI effects, commit1459a1f8 pushed and MR57 updated to DevOps-891 restore python builds with GET-verified SHA/settings/body and clean checkout (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Verify recommended-tasks-generator pipeline140780 fully successful at23:55:39MSK: build3223259, Nomad lint3223109 and test3223108 all success; MR78 remains unmerged (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Merge recommended-tasks-generator MR78 after explicit user approval and successful head CI: expectedSHA5899dd9e, independent GET merged/newmaster1fa2457d, other MRs untouched (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Verify recommended-tasks-generator post-merge master140796 success at00:08:12MSK/newmaster1fa2457d: build3223279/test3223280 success, no further tag/manual deployment/job execution (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Verify task-quality-control Docker29.9.0 correction: pipeline140795/build3223277/test3223278 all success, final branch/latest digestb1f0871a, old cgroup error absent; MR57 remains unmerged, no merge/deployment (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Merge task-quality-control MR57 after explicit approval and green pipeline140795: expectedSHA1459a1f8, GET merged/mastera51285b3 at00:04:57MSK, settings preserved/other MRs untouched (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Verify task-quality-control master140797 post-merge success00:14:41MSK: build3223281/test3223282 success, master/latest digest48f271a4, no tag/manual deployment/periodic action (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Resolve task-quality-control first RUN container-launch cgroup failure before pip (3223110/140781, runner105/client+DinD19.03.12); matching Docker29.9.0 correction separately approved/published and full CI140795 passed; original host cgroupv2 remains unverified, no runner changes (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Verify automatic CI/registry results of five consumer hash MRs: final snapshot ab140778/rowers140779 full success; task-quality cgroup failure, recommended3223107 push timeout and daily3223113 base-pull timeout remain separate infrastructure work; no manual jobs/retries/deployment authorized. Historical rowers0.19.3/recommended1.16.24 require separate newrelease/image policy; no tag moves (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Publish six rebuilt PyPI versions after separate approval: metronom3.2.3 wheel+sdist,castle5.2.0/5.2.1,basis2.1.2,toster4.2.0,iss2.0.0 sdists; seven Nexus GET-checksum matches,32of32version availability. Original consumer hashes differ; local repair publication remains pending (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)

- [ ] Configure regular Nexus backups (database, configuration and blob stores) and verify restoration (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-nexus-recovery-status-comment.md)

- [ ] Republish required mobile APK/ZIP into restored raw-private through approved CI jobs; verify Android/iOS Appium downloads (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-nexus-raw-recovery-plan.md)

- [x] Restore raw/raw-private blob/repositories/role/raw identity; configuration/auth verified, done2026-10-12 (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-nexus-raw-recovery-plan.md)

- [ ] Review/merge MR1371 common Nomad Nexus Docker auth and DinD28.5.2; user declined manual CI, controller must provide NEXUS_DOCKER_PASSWORD (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-nexus-automation-services-nomad-docker-auth.md)

- [x] Recover circular Maven bootstrap dependencies between youdo-business-tests and TKB/Sber test snapshots; full snapshots, builds and approved latest tags verified; done2026-10-12 — [src](companies/youdo/knowledge/log/2026-10-12-nexus-youdo-business-tests-maven-recovery-diagnosis.md)

- [x] Restored UI latest0.39.0 after explicit approval: identical-byte republish, integrity unchanged and ALLOW_ONCE restored/verified; done2026-10-12 — [src](companies/youdo/knowledge/log/2026-10-12-nexus-npm-library-restoration.md)

- [x] Publish user scope correction to common Nomad Nexus Docker auth in MR1371 after approval;5c623f52 published, role defaults common, three host_vars removed, static checks/review pass (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-nexus-sorm-runner-image-auth.md)

- [x] Configure Nexus docker account on requested Nomad clients172.24.0.11/.12/.13; saved config and node-side service manifest200 verified on all, no restart (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-nexus-sorm-runner-image-auth.md)

- [ ] Persist approved runtime Nexus DOCKER_AUTH_CONFIG entries for171/172 in configuration management after separate repository approval (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-nexus-sorm-runner-image-auth.md)

- [x] Add Nexus image-pull auth to all runner entries on172.28.0.171/.172; files and automatic reload verified, no CI retry (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-nexus-sorm-runner-image-auth.md)

- [x] Nexus npm steps1-3: separate stores, npm-private/npmjs-proxy/npm group, nx-npm/npm user and NpmToken applied; internal principal/metadata verified; done2026-10-12 — [src](companies/youdo/knowledge/log/2026-10-12-nexus-npm-recovery-applied.md)
- [x] Replaced project496 NPM_TOKEN after explicit approval; GET verified exact value and preserved metadata; no CI retry; done2026-10-12 — [src](companies/youdo/knowledge/log/2026-10-12-nexus-npm-recovery-applied.md)
- [ ] Add public Nexus npm nginx location after branch/remote approval; current LB lacks /repository/npm and returns404 (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-nexus-npm-recovery-applied.md)
- [x] Published all6requested private npm pairs; CI3219467/3219468/3213529 and local ESLint1.2.5/cursor0.0.3 metadata verified; done2026-10-12 — [src](companies/youdo/knowledge/log/2026-10-12-nexus-npm-library-restoration.md)
- [ ] Review npm consumer lock integrity: UI0.17.5/0.39.0, ESLint1.2.5 and cursor0.0.3 metadata differs from existing locks; ESLint2.1/Prettier match, no full install compatibility claimed (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-nexus-npm-library-restoration.md)

- [x] Restore RabbitHole1.4.1/1.4.2/1.4.3 and Coworking1.0.7/1.3.3/1.3.4; CI/manual historical rebuild publications approved and version presence verified; done2026-10-12 — [src](companies/youdo/knowledge/log/2026-10-12-nexus-library-publish-retries.md)

- [x] NuGet recovery steps1-4: separate stores, legacy endpoints, nuget user/nx-nuget role applied and GET-verified; public package/metadata reads200 and authenticated principal verified; done2026-10-12 — [src](companies/youdo/knowledge/log/2026-10-12-nexus-nuget-recovery-applied.md)
- [x] Restore all143required private/custom NuGet version pairs across52package IDs; final public metadataHTTP200 verified after historical retries and separately approved fallback uploads; done2026-10-12 — [src](companies/youdo/knowledge/log/2026-10-12-nexus-next-library-recovery.md)
- [x] Restore YouDo.ServiceCore.Logging1.0.16 and YouDo.ServiceCore.Metrics1.0.16: user published from CI, both public Nexus metadata HTTP200 verified; done2026-10-12 — [src](companies/youdo/knowledge/log/2026-10-12-nexus-business-job-3219724-nuget.md)
- [x] Verify youdo.business MR3843 build after Logging/Metrics1.0.16 publication: user confirmed success; done2026-10-12 — [src](companies/youdo/knowledge/log/2026-10-12-nexus-business-job-3219724-nuget.md)
- [ ] Check representative service NuGet restore and transitive/version gaps after publication recovery; deferred by user to prioritize restoration. Mailer prerelease keeps Contract>=1.9.3 and currently resolves1.9.4 (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-nexus-next-library-recovery.md)

- [ ] Disable temporary Nexus anonymous access after recovery and configuring credentials for Android/autotest-core; current nx-anonymous permits read/browse of all repositories, including hosted/private content (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-nexus-temporary-anonymous-access.md)

- [x] Applied approved Maven storage/proxy/group configuration; GET settings verified and five representative upstream POMs fetched through public group with admin auth; done2026-10-11 — [src](companies/youdo/knowledge/log/2026-10-11-nexus-fresh-recovery-plan.md)
- [x] Created approved Maven CI user `maven` and sole consolidated role `nx-maven`, GET-verified exact privileges and CI credential POM200; anonymous remains disabled; done2026-10-11 — [src](companies/youdo/knowledge/log/2026-10-11-nexus-fresh-recovery-plan.md)
- [ ] Configure Maven credentials for Android and autotest-core before disabling temporary anonymous access; dependency blocks lack credentials and autotest-core first `gradle :jar` lacks Nexus property flags, so cover both repository auth and the first command. Anonymous temporarily enabled by user request; public POM200 verified (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-nexus-temporary-anonymous-access.md)
- [ ] Resolve Cyberity Maven upstream connection timeout from workstation and Nexus host; proxy configured, artifact availability unverified (2026-10-11) — [src](companies/youdo/knowledge/log/2026-10-11-nexus-fresh-recovery-plan.md)

- [x] Fresh Nexus3.96.4 deployed on `10.18.24.233` after explicit approval; apply exit0 and local/external REST/UI HTTP200, separate data storage verified; done2026-10-11 — [src](companies/youdo/knowledge/log/2026-10-11-nexus-fresh-recovery-plan.md)
- [x] Nexus Docker hosted/group repositories, blob stores, DockerToken realm and gitlab CI user initialized after approval excluding Docker Hub proxy; GET-verified configuration, no CI retry; done2026-10-11 — [src](companies/youdo/knowledge/log/2026-10-11-nexus-fresh-recovery-plan.md)
- [x] Nexus internal Docker `/v2/` existing GitLab CI credentials HTTP200 verified; Basic challenge compatible, DockerToken active; no Docker CLI/CI retry claimed; done2026-10-11 — [src](companies/youdo/knowledge/log/2026-10-11-nexus-fresh-recovery-plan.md)
- [x] Public Nexus Maven authenticated reads verified: Jivo2.6.0 POM/AAR and AGP8.13.2 POM HTTP200, XML/ZIP validated; anonymous401 expected; done2026-10-12 — [src](companies/youdo/knowledge/log/2026-10-12-nexus-public-lb-route-verification.md)
- [x] Verify public Nexus Docker access through nexus.youdo.com: CI credentials /v2/ and SORM migrations0.0.22 manifest HEAD200, anonymous401 due forceBasicAuth (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-nexus-public-lb-route-verification.md)
- [x] Review cleaner client stale credentials/rate-limit429 separately from working gitlab CI user (2026-10-11); cleaner account restored, crash-loop child stopped, cooldown cleared; user-triggered allocation ab7c7a54 completed exit0/zero restarts and Nexus accepted108DELETE requests with202 on2026-10-20 — [src](companies/youdo/knowledge/log/2026-10-20-nexus-cleaner-recovery-assessment.md)

### GitLab recovery

- [ ] If requested separately, persist the Ansible5.10.0 Ubuntu package-manager adaptation upstream; the historical tag recipe fails on its mutable Ubuntu Nomad parent (2026-10-19) — [src](companies/youdo/knowledge/log/2026-10-19-gitlab-ansible-playbook-3236157-local-build.md)

- [x] Manual Molecule job3219872 start declined by user after f4018c2b DinD28.5.2 publication in MR1371; not run, no CI-success claim (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-nexus-automation-services-nomad-docker-auth.md)

- [x] Publish reviewed ansible-molecule-toolset Dockerfile recovery after approval;81f3a8e/[MR1](https://gitlab.youdo.sg/sysadmins/ansible-molecule-toolset/-/merge_requests/1) published, remote SHA/MR verified, local build passed (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-gitlab-ansible-molecule-toolset-recovery.md)
- [x] Restore ansible-molecule-toolset master/latest through master release; user-supplied pipeline140669/jobs3219854/3219855 GET-verified successful, existing DevOps-891 comment updated as requested (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-gitlab-ansible-molecule-toolset-recovery.md)
- [ ] Retry automation-services molecule-nomad after authorization; previous job3219595 failed before tests because image was missing, toolset master/latest now published (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-gitlab-ansible-molecule-toolset-recovery.md)

- [x] GitLab registry enabled/reconfigured after explicit approval; user DNS update to `138.16.203.174`, JWT and authenticated `/v2/` HTTP200 verified; done 2026-10-11 — [src](companies/youdo/knowledge/log/2026-10-11-gitlab-restored-server-verification.md)
- [x] Bootstrap `youdo/base-images/docker:git` and `docker:dind` built/pushed after explicit approval; authenticated manifest/config hashes and container checks pass; done 2026-10-11 — [src](companies/youdo/knowledge/log/2026-10-11-gitlab-restored-server-verification.md)
- [x] DevOps-891 inspected image recovery complete: final nomad-n-tools pipeline140629/job3218418 succeeded;1.1/latest digests match and pulled-image runtime passed. Task closed by user2026-10-12; handoff comment published. Final registry reconciliation69/69; inventory56success/3seeds/1excluded placeholder, noneactive/failed/blocked (done2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-gitlab-devops-891-final-nomad-tools.md)
- [x] DevOps-891 Fastlane image: MR6 merged, Fastlane2.241.0/Huawei1.1.3/RuStore1.1.0/frozen dependencies and manifest publication fix; version0.0.9/latest release digests and absence of plugin activation errors verified (done2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-gitlab-devops-891-fastlane-upgrade-legacy-archive.md)
- [x] Fastlane Ruby3.4 bundled startup: latestFastlane declares abbrev, Faraday2 aligns RuStore1.1.0; direct/bundled startup and explicit plugin loading passed without network (done2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-gitlab-devops-891-fastlane-upgrade-legacy-archive.md)
- [x] DevOps-891 Nomad/AWX release: MRs merged, Nomad master/latest, AWX24.6.1 and ansible-playbook master/latest successful; authenticated digests match traces (done2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-gitlab-devops-891-official-hashicorp-releases.md)
- [ ] After separate task-branch approval, fix base-images `docker/git/Dockerfile` to keep curl/libcurl versions coherent; task-run temporary `--upgrade curl libcurl` build passed, repository unchanged (2026-10-11) — [src](companies/youdo/knowledge/log/2026-10-11-gitlab-restored-server-verification.md)
- [x] GitLab Silent Mode disabled after explicit user approval; settings PUT returned HTTP200/false, independent GET and database reads confirmed persisted false; done 2026-10-11 — [src](companies/youdo/knowledge/log/2026-10-11-gitlab-restored-server-verification.md)
- [ ] Review historical webhook 56 HTTP404 and webhook 72 HTTP401; current hook 109 delivery/authentication verified HTTP204 by approved test, legacy cleanup requires explicit permission (2026-10-11) — [src](companies/youdo/knowledge/log/2026-10-11-gitlab-restored-server-verification.md)
- [ ] Inspect/remediate preexisting `SetProjectVulnerabilityCount` background migration 332 after review and repair permission (2026-10-11) — [src](companies/youdo/knowledge/log/2026-10-11-gitlab-restored-server-verification.md)
- [ ] Update affected domain SSH clients for the verified changed host key; Git SSH transport already passed using the trusted IP host-key alias (2026-10-11) — [src](companies/youdo/knowledge/log/2026-10-11-gitlab-restored-server-verification.md)

### Agent Git/MR training

- [x] Implement the unified local-first GitLab workflow skill, repository helper and guarded MR verification while retaining both approvals (2026-10-19) — [src](companies/youdo/knowledge/log/2026-10-19-gitlab-ci-gitlab-workflow-skill.md)
- [x] Prepare Git/MR training results early at the user's request; report covers 2026-10-08 through 2026-10-19 instead of waiting until October 30 (2026-10-19) — [src](companies/youdo/knowledge/log/2026-10-19-gitlab-ci-agent-git-training-early-report.md)
- [x] Review the early Git/MR training report: user chose to retain both approvals while automating information gathering and review-material preparation (2026-10-19) — [src](companies/youdo/knowledge/log/2026-10-19-gitlab-ci-agent-git-training-early-report.md)

- [ ] due 2026-10-30 (proposed; first active session on/after): review Git/MR training since October 19; assess task scope, task-only staging, approval compliance, CI-effect predictions, publication verification and corrections; retain both approvals unless explicitly changed — [src](companies/youdo/knowledge/systems/gitlab-ci/agent-git-workflow.md)

### youdo-chat-agent (DevOps-882)

- [x] Infrastructure and production launch completed; pipelines 140457/140458 successful. User closed DevOps scope on 2026-10-09; functional verification belongs to developers. Additional inferred operational checks and shared-template improvements were not requested and are not completion blockers — [src](companies/youdo/knowledge/log/2026-10-09-youdo-chat-agent-prod-deploy.md)

### Corporate network access

- [x] Diagnose s.zubakha macOS buildsinfo access: system resolver failed despite correct direct DNS and working forced-IP HTTP; user configured /etc/resolver/youdo.local with 172.30.63.1, ordinary curl HTTP401 verified by screenshot (2026-10-21) — [src](companies/youdo/knowledge/log/2026-10-21-corporate-network-szubakha-buildsinfo.md)

### Other systems

- [x] DevOps-896 / dynamic_inventory closed by the user on 2026-10-14; prepare/release/deploy: MR26 merged2bc44941; approved VK Consul/Vault/CI config, release-0.56.4, no-attestation rebuild140830 and manual deployment3224500 succeeded; DNS/direct GET200,16stands/64Nomad aliases/0SQL (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-13-gitlab-ci-dynamic-inventory-vk-migration-plan.md)
- [x] DevOps-896: accept user-reported closure; consumer cutover, live SQL mapping and repeated-refresh caveats are retained in the work log without reopening the task or claiming verification. Further work requires a separate request (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-13-gitlab-ci-dynamic-inventory-vk-migration-plan.md)

- [x] Remove obsolete local `~/mygit/youdo-ai` after explicit user request; deletion verified, canonical RP skill links/data retained (2026-10-19) — [src](current/knowledge/log/2026-10-19-rp-obsolete-local-copy-removed.md)
- [ ] Decide whether a broader read-only check of other test5 RabbitMQ exchanges is still needed after the signin fix; optional proposal (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-07-rabbitmq-test5-signin-exchange-auto-delete-mismatch.md)

- [x] nomad-test / gitlab-ci dynamic_inventory: dnsmasq port 53 proxy restored by the user's temporary playbook on `10.16.28.11-13`; verified 2026-10-10 15:51:31 MSK, both runners resolve through Windows `.8`/`.9` with `NOERROR` and Nomad leader GET succeeds — [src](companies/youdo/knowledge/log/2026-10-10-gitlab-ci-dynamic-inventory-consul-dns.md)
- [ ] yandex-tf AP-2347: integrate recovery module `recovery_hosts` into Terraform Ansible inventory instead of legacy `nomad_master_ips`/old `10.16.26.x` resources; proposed branch `AP-2347-recovery-ansible-inventory` from `origin/master` explicitly deferred by the user, temporary three-master inventory prepared locally (2026-10-10) — [src](companies/youdo/knowledge/log/2026-10-10-gitlab-ci-dynamic-inventory-consul-dns.md)
- [ ] automation-services dnsmasq: after a separate code-change request, make the `/etc/resolv.conf` symlink condition tolerate missing files with `resolv_conf_stat.stat.islnk | default(false)`; interrupted runs currently omit `stat.islnk` and fail on rerun (2026-10-10) — [src](companies/youdo/knowledge/log/2026-10-10-gitlab-ci-dynamic-inventory-consul-dns.md)
- [ ] gitlab-ci Nomad canary rollback: unsafe with concurrent deployments (`nomad job promote` targets the latest one) — [src](companies/youdo/knowledge/systems/gitlab-ci/nomad-canary-rollback.md)
- [ ] youdo.business dotnet tests: xUnit already capped (`79254cc49`, `maxParallelThreads: 4`); remaining: dedicated runner or lower concurrency for `dotnet-unit-tests`, `section_start` timing sections (checked 2026-09-30) — [src](companies/youdo/knowledge/log/2026-09-03-youdo-business-dotnet-tests-duration.md)
- [ ] Base images: LibreOffice PPA still via plain `add-apt-repository` (3 images), move to explicit key + `signed-by`; buster archive sources only in `dotnet-core-aspnet/3.1`, missing in other 3.1 images; `3.1-gdilibs`/`3.1-libvips*` still use `apt-key adv` (checked 2026-09-30) — [src](companies/youdo/knowledge/log/2026-06-26-base-images-docker-libreoffice-ppa-gpg-timeout.md), [src](companies/youdo/knowledge/log/2026-06-26-base-images-dotnet-aspnet-3-1-buster-archive.md)

Application-side findings handed to developers, not tracked as DevOps work: geocoder
suggest HTTP 500, docvalidation passport mapping, escrow Tinkoff 502, `lead_companies`
schema drift, tracing of `YouDo.Web.MvcApplication`, youdo-mcp Data Protection keys
stored unencrypted in `data_protection_keys` (no `ProtectKeysWith*`). See the respective logs.

---

## Personal

### TrustTunnel client

- [x] TrustTunnel corporate endpoint exclusion active with both VPNs connected; Nexus UI GET and default-MSS6000-byte request HTTP200 verified; browser refresh/symptom confirmation belongs to user; done2026-10-11 — [src](personal/knowledge/log/2026-10-11-trusttunnel-client-corporate-vpn-exclusion.md)


- [ ] Home network phase 1: TV and Lampa via Media Station X, C64 backup, device list, tunnel speed test (2026-09-26) — [src](personal/knowledge/log/2026-09-26-home-network-initial-plan.md)
- [ ] Bench tests: podkop fail-open on `ifdown tun0`, FakeIP DNS with AdGuard Home DoT upstream, VPS public IP from inside the tunnel (2026-09-26) — [src](personal/knowledge/log/2026-09-26-home-network-initial-plan.md)
- [ ] `home-infra`: choose where to host the git repo; move the router password out of the plaintext inventory once Vault is ready (2026-09-26) — [src](personal/knowledge/log/2026-09-26-home-network-initial-plan.md)

---

## Knowledge base

- [x] Shorten shared AGENTS.md:12189to5593bytes, detailed procedures moved into README with explicit read triggers; permissions and both Git approvals preserved; KB0errors/5existingwarnings, agent9files/0errors/1existingwarning (2026-10-20) — [src](personal/knowledge/log/2026-10-20-knowledge-base-shorten-shared-agents.md), [original proposal](personal/knowledge/log/2026-10-20-knowledge-base-lint-warning-review.md)
- [x] Correct kb_lint inline-code language false positives and mark exact source labels consistently; Russian prose checks preserved, 11 regression tests passed, full KB 0 errors/0 warnings (2026-10-20) — [result](personal/knowledge/log/2026-10-20-knowledge-base-language-inline-code-fix.md) — [src](personal/knowledge/log/2026-10-20-knowledge-base-lint-warning-review.md), [evidence](current/knowledge/log/2026-10-20-knowledge-base-language-warning-audit.md)

- [x] Require report-only agnix after agent instruction/skill/settings changes and add change-aware ai-sync fallback before same-day Git skip;16new tests+10sync tests,live9files0errors,previous optional mode superseded; no auto-fix or Git blocking gate (2026-10-19) — [src](personal/knowledge/log/2026-10-19-knowledge-base-agnix-enforcement.md)
- [ ] Document installation and setup rules for `~/ai` on another PC: prerequisites, clone/layout and `current` symlink, agent instruction/skill links, secrets and generated data outside Git, external tools such as pinned agnix, and first-run checks (2026-10-19) — [src](personal/knowledge/log/2026-10-19-knowledge-base-agnix-instruction-loading-pilot.md)
- [x] Research additional local-agent rules, skills and knowledge retrieval for Claude Code, Codex and portable use; expanded through Context Awesome/awesome lists and original sources, bounded local inventory and recommendations documented; no installation/configuration changes (2026-10-19) — [src](personal/knowledge/log/2026-10-19-knowledge-base-agent-capabilities-research.md)
- [x] Complete agent pilot1 and retain agnix by explicit user decision as optional manual report-only lint: isolated0.59.0, native Codex loading probe,8files/9classified diagnostics; KB-root duplication and stale Claude cache identified, fixes deferred (2026-10-19) — [src](personal/knowledge/log/2026-10-19-knowledge-base-agnix-instruction-loading-pilot.md); original optional mode subsequently superseded by [mandatory checks and sync fallback](personal/knowledge/log/2026-10-19-knowledge-base-agnix-enforcement.md), and deferred findings fixed in step3
- [x] Complete bounded agent pilot2 on Codex using Skill Creator methodology: five paired scenarios,17/17 assertions per condition, three expected native skill-read probes; no added quality benefit demonstrated, rules unchanged; Claude-specific extension blocked separately (2026-10-19) — [src](personal/knowledge/log/2026-10-19-knowledge-base-skill-evaluation-pilot.md)
- [ ] Resume Claude skill evaluation after organization access is restored or another authentication method is explicitly authorized; current startup returns is_error with subscription access disabled,0tokens; do not count it as a passed/failed behavioral trial (2026-10-19) — [src](personal/knowledge/log/2026-10-19-knowledge-base-skill-evaluation-pilot.md)
- [x] Complete agent step3: explicit canonical paths, stale Claude cache replaced with pointers, Codex KB-cwd duplicate instructions removed through bounded project override; native loading1copy in3cwd,agnix0errors,five fresh regression runs17/17 checks; approval policy preserved (2026-10-19) — [src](personal/knowledge/log/2026-10-19-knowledge-base-local-rule-corrections.md)
- [ ] Choose next proposed agent pilot step4-9; broader/adversarial/repeated skill tests remain proposals and later implementation is not yet authorized (2026-10-19) — [completed corrections](personal/knowledge/log/2026-10-19-knowledge-base-local-rule-corrections.md), [trial order](personal/knowledge/log/2026-10-19-knowledge-base-agent-capabilities-research.md)
- [ ] Monthly staleness review 2026-11: first review; offer on the first agent session in November, not necessarily November 1; refresh the due-note count with `general/scripts/build_index.py --stale 30`; wait for user agreement (rescheduled by user 2026-10-09) — [src](personal/knowledge/log/2026-10-09-knowledge-base-monthly-review-first-session.md)
- [x] Adopt mandatory final note-to-TODO reconciliation for substantial work: only task-affected records, source-linked remaining actions, consistent completed/cancelled/deferred status, preserved history and proposals without execution permission (2026-10-19) — [src](personal/knowledge/log/2026-10-19-knowledge-base-agent-learning-record-final-note-todo-reconciliation-da23f6ff0112c778d7f8.md)
- [x] Shorten sync work summaries and exclude generated Python cache: exact deduplication, grouping, bounded note references and one final result per task; six bytecode files removed from tracking with local copies retained (2026-10-19) — [src](personal/knowledge/log/2026-10-19-knowledge-base-sync-preview-and-summary.md)
- [x] Fix `ai-sync.sh --dry-run`: private temporary index/object store and in-memory regenerated indexes; 10 sync tests and live zero-change snapshot passed; unsupported shared Git storage fails safely (2026-10-19) — [src](personal/knowledge/log/2026-10-19-knowledge-base-sync-preview-and-summary.md)

### Token cost optimization (proposed 2026-09-23)

- [ ] due 2026-10-21: compare Codex October 7–13 baseline with October 14–20 using `ai-data/token-cost/audit.py --end-date 2026-10-21`; normalize full/partial reads and full-size proxy per KB-active and tool-active session, report parser coverage; decide whether reading rules need adjustment (2026-10-14) — [src](personal/knowledge/log/2026-10-14-knowledge-base-token-cost-comparison.md)
- [x] Improve automated `token_usage.py --kb` Codex accounting: nested static shell extraction, per-command/file reads and explicit incomplete coverage; 17 tests and live report passed, token-total brief output unchanged (2026-10-19) — [src](personal/knowledge/log/2026-10-19-knowledge-base-codex-nested-shell-accounting.md)


---

## Done

- [x] Investigate cause of Cerberus2 production API HTTP hang after release1.0.10: user API restart at01:04:45 restored /v1/sources HTTP200/~0.17s, threads859before/69after; source has synchronous retry-forever Orleans client initialization, suspected but unproven; no code/config repair authorized (2026-10-20) — [src](current/knowledge/log/2026-10-20-cerberus2-devops-902-production-verification.md) — Closed by user 2026-10-20: further diagnosis not required; API recovered after user restart, root cause not established.

- [x] DevOps-902 Cerberus2: internal SDK2.1/ASP.NET2.1 switch merged as MR27/b87d8268, tag1.0.10/pipeline141231 SUCCESS;14test deploys and production rollout completed by user and CI verified. Production HTTP recovered after user API restart; remaining diagnosis cancelled by user 2026-10-20 (done2026-10-20) — [src](current/knowledge/log/2026-10-20-cerberus2-devops-902-production-verification.md)

- [x] Compare KB access with September 30 baseline: Claude full reads 47 -> 5 (October 8) -> 1 (October 14), estimated full KiB 1086 -> 25 -> 10. User switched to Codex, so this does not prove optimization. Corrected Oct7–13 Codex baseline: 17 full/292 partial reads, 250.46 KiB proxy in 101 KB-active sessions; previous-week local history absent. Rule effectiveness remains unverified; next comparison due Oct21. done 2026-10-14 — [src](personal/knowledge/log/2026-10-14-knowledge-base-token-cost-comparison.md)

- [x] Two-week agent behaviour review for 2026-09-28 through 2026-10-11: all 11 sync commits have substantive work records; stale note follow-ups reconciled, two optional proposals moved to the central backlog; done 2026-10-12 — [src](personal/knowledge/log/2026-10-12-knowledge-base-agent-behaviour-two-week-review.md)

- [x] Elasticsearch msk3-elastic-cls02: analyze heap dump, heap/GC alerts, upgrade planning — closed without action, done 2026-10-09: no longer relevant by user decision — [src](companies/youdo/knowledge/log/2026-07-31-elasticsearch-msk3-elastic-cls02-restart.md)
- [x] sc-mta-01 postfix: mass-mailing bursts and SMTP egress/NAT limits — closed without action, done 2026-10-09: no longer relevant by user decision — [src](companies/youdo/knowledge/systems/mail/sc-mta-01-postfix.md)

- [x] DevOps-887: added `-parallelism=1` to `prod-dbaas-grants` CI apply; MR !93 merged and task closed by the user; done 2026-10-09. Apply/empty plan not independently verified by the agent — [MR](https://gitlab.youdo.sg/sysadmins/selectel/selectel-tf/-/merge_requests/93), [task](https://youtrack.youdo.com/youtrack/issue/DevOps-887), [src](companies/youdo/knowledge/log/2026-09-21-selectel-tf-job-3163660-postgresql-acl-race.md)

- [x] Runner `idcn-10`: disk cleanup and monitoring verified — cron succeeded on 2026-10-07 and 2026-10-08 (30,923M and 17,612M freed), Zabbix trigger 568940 recovered to OK; observation period accepted as sufficient by the user; the intentionally absent YouDoApp job `timeout:` remains unchanged — done 2026-10-08 — [src](companies/youdo/knowledge/log/2026-09-30-ios-ci-job-3195403-disk-full-hang.md)

- [x] DevOps-886 k8s-ttl-controller installed as safety net (TTL deploy 8d / update 6d), verified end to end, YouTrack closed by the user (2026-10-07) — [src](companies/youdo/knowledge/log/2026-10-07-dev-deployment-devops-886-ttl-controller.md)

- [x] test5: delete exchange `youdo.user.signin` (auto_delete=false vs publisher true) so it is redeclared; check bindings first; needs admin creds and approval (2026-10-07) — [src](companies/youdo/knowledge/log/2026-10-07-rabbitmq-test5-signin-exchange-auto-delete-mismatch.md) — done 2026-10-07

- [x] Deleted stale namespace `dev-hide-employee-api-swagger` and its Helm releases (2026-10-06) — [src](companies/youdo/knowledge/log/2026-10-06-dev-deployment-hide-employee-api-swagger-namespace.md)

- [x] iOS `.ipa` in Nexus: change `5cf852ca96` exists only on `IOS-5008`; YouDoApp `develop` still uploads `gitlab_youdo.zip` (`Fastfile:481-508`) and `Build development` keeps `YDMainApp.app.zip` (checked 2026-09-30) — closed without action 2026-10-05: not the user's task (user) — [src](companies/youdo/knowledge/log/2026-08-04-ios-ci-build-dev-ipa.md)
- [x] web-autotests: raise Jenkins `youdo_web_testing_*` retention (30 builds) or upload regress reports to S3 — closed without action 2026-10-01: the one-off Selenoid vs k8s comparison is done, extra report storage not needed (user) — [src](companies/youdo/knowledge/log/2026-09-30-web-autotests-selenium-grid-k8s-slow-regress.md)
- [x] lenochka.youdo.sg: rotate the basic-auth password, update `LENOCHKA_PASS`, move the plaintext `curl -u` in youdo.business job `notify` to a masked variable — closed without action 2026-10-01: lenochka is planned to be decommissioned (user) — [src](companies/youdo/knowledge/systems/gitlab-ci/resource-groups.md)
- [x] web-autotests: infra-tf `dev/config/selenium-grid-values.yaml`: `pollingInterval` 3, `maxReplicaCount` 20 (`77ce4c2`); Smokus session start median 50-70 s -> 10.5 s (2026-10-01) — [src](companies/youdo/knowledge/log/2026-10-01-web-autotests-selenium-keda-polling-interval-effect.md)
- [x] web-autotests: Re-measured regress part 1: `scalingType: deployment` (`10062f0`) gives 108 min, session start median 0.7 s (was ~3 h, 24 s) (2026-10-01) — [src](companies/youdo/knowledge/log/2026-10-01-web-autotests-selenium-keda-polling-interval-effect.md)
- [x] cerberus2: Restart cerberus2 worker on msk3-nomad01; repeat API unbans that failed with 25006 — dropped 2026-10-01, no further work on cerberus2 by user decision — [src](companies/youdo/knowledge/log/2026-09-30-cerberus2-readonly-transaction-check.md)
- [x] youdo-business: Forward SIGTERM in gitlab-ci-templates v3/files/dotnet.entrypoint.sh (merged 7fabb47, 2026-10-01) — [src](companies/youdo/knowledge/log/2026-10-01-youdo-business-worker-hard-kill-hangfire-lock.md)
- [x] youdo-business: Hangfire lock on worker restart — closed 2026-10-01 without separate action: DevOps-872 entrypoint fix delivers SIGTERM, workers stop gracefully; reopen if lock errors recur — [src](companies/youdo/knowledge/log/2026-09-11-youdo-business-test14-hangfire-lock.md), [src](companies/youdo/knowledge/log/2026-10-01-youdo-business-worker-hard-kill-hangfire-lock.md)
- [x] android-farm: farm logs not reaching Loki 2026-09-14..2026-10-01 — Gate_K DNATed youdo.* DNS to decommissioned srv0; DNAT disabled, streams arrive (2026-10-01) — [src](companies/youdo/knowledge/log/2026-10-01-android-farm-kazan-gate-k-dns-forward-to-decommissioned-srv0.md)
- [x] android-dig: `instance` labels `M-K0057`/`M-K0058` confirmed in Loki (2026-10-01) — [src](companies/youdo/knowledge/log/2026-10-01-android-farm-kazan-gate-k-dns-forward-to-decommissioned-srv0.md)

- [x] Knowledge base: feed `knowledge/log/` and `TODO.md` into the `rp` skill — closed without action 2026-09-30: not relevant, `rp` unused and may be redone (user).
- [x] Jenkins root URL `https://build.youdo.sg/` — closed 2026-09-30: already in place (user; builds from 121 show the external URL) — [src](companies/youdo/knowledge/systems/dev-deployment/gitlab-ci-deploy-dev.md)
- [x] team-copilot: `ANTHROPIC_BASE_URL` in Vault — closed without action 2026-09-30: not relevant (user); repo passes it through `envFrom` — [src](companies/youdo/knowledge/log/2026-06-11-team-copilot-deploy-gitlab-ci.md)
- [x] Knowledge base: walked through all 22 `(confirm)` items with the user and a read-only check (done 2026-09-30) — [src](companies/youdo/knowledge/log/2026-09-30-knowledge-base-todo-confirm-review.md)
- [x] Audit `dev.yml` files that keep `RabbitMq__Url` in global `env`; move to service-local env or a chart helper — done: no global `RabbitMq__Url` in any `devops/dev.yml` on master; docvalidation, Fns, youdo-sms-service keep it under `services[].env` (checked 2026-09-30) — [src](companies/youdo/knowledge/log/2026-06-25-dev-deployment-dev-96-fns-check.md)
- [x] `youdo-business-worker` OOMKilled at 256Mi on `dev-master` — done: youdo.business `3f8c5dab9` sets worker `memory`/`memoryLimit: 512Mi` in `devops/dev.yml` (checked 2026-09-30) — [src](companies/youdo/knowledge/log/2026-07-30-dev-deployment-dev-master-node-replacement-db-recovery.md)
- [x] rp: open follow-ups — Tinkoff notifications IP access (DevOps-812), iOS physical-phone task (DevOps-810) — done: YouTrack: DevOps-812 Fixed 2026-07-22, DevOps-810 Fixed 2026-07-21 (checked 2026-09-30) — [src](companies/youdo/knowledge/log/2026-07-22-rp-devops-sprint-185-reports.md)
- [x] Consul master CPU: reduce `vmagent` Consul SD scope (~8930 services), lower `waitTime`, persistent per-process CPU telemetry (2026-06-05) — closed without action 2026-09-30: not relevant (user) — [src](companies/youdo/knowledge/log/2026-06-05-nomad-test-master-03-cpu-unavailable.md)
- [x] Nexus pulls: use `msk3-nexus.youdo.corp` in Nomad image refs or split-horizon DNS; disable nginx buffering for registry paths; OrientDB "No space left"; hand PMTU/MSS `172.28.0.0/24 -> 10.16.x.x` to network owner (2026-06-17) — closed without action 2026-09-30: not relevant (user) — [src](companies/youdo/knowledge/log/2026-06-17-nexus-nomad-pull-latency.md)
- [x] Runner `idcn-10`: disk cleanup routine (DerivedData, Archives, stale workspaces); SwiftPM cache / Git HTTP/1.1 if GitHub HTTP/2 failures recur — closed without action 2026-09-30: not relevant (user) — [src](companies/youdo/knowledge/log/2026-07-20-ios-ci-runner-dns-rubygems.md), [src](companies/youdo/knowledge/log/2026-08-31-ios-ci-job-3102258-github-http2-failure.md)
- [x] Host `192.168.50.17`: backup, NVMe replacement (Percentage Used 222%), kernel log alerts, reduce `emulator_1` log verbosity (2026-08-03) — closed without action 2026-09-30: not relevant (user) — [src](companies/youdo/knowledge/log/2026-08-03-android-farm-ssh-192-168-50-17-connection-reset.md)
- [x] MSSQL `RecreateDBProcedures`: check backup readability before drop, `TRY/CATCH`, `sqlcmd -b` in Ansible; confirm file server `10.16.26.4` vs `172.26.0.115` (2026-08-02) — closed without action 2026-09-30: not relevant (user) — [src](companies/youdo/knowledge/log/2026-08-02-mssql-yandex-mssql-restore-youdo.md)
- [x] sc-except: restart policy/alert for the stopped container; MSSQL memory limits (2026-06-13) — closed without action 2026-09-30: not relevant (user) — [src](companies/youdo/knowledge/log/2026-06-13-sc-except-mssql-unavailable.md)
- [x] pg-b2b-test `10.16.26.27`: drop/archive unused `test*` DBs, Hangfire retention (2026-06-23) — closed without action 2026-09-30: not relevant (user) — [src](companies/youdo/knowledge/log/2026-06-23-postgresql-pg-b2b-test-10-16-26-27-data-space.md)
- [x] Knowledge base: `companies/youdo/CONTEXT.md` reviewed with the user: Jenkins role, Nomad->K8s direction, fuller stack, ticket formats, sorm out of scope, team-skills line removed (done 2026-09-30) — [src](personal/knowledge/log/2026-09-30-knowledge-base-memory-migration-env-cleanup.md)
- [x] Knowledge base: link team skills `~/git/ai-skills/skills/*` into `companies/youdo/skills/` — closed without action 2026-09-30: not relevant (user).
- [x] Knowledge base: staleness review mechanism: `build_index.py --stale 30` (maps 30 days, recipes 180, hypotheses) and a monthly TODO item from `ai-sync.sh`; first review arrives as the 2026-10 item (13 notes due on 2026-09-30) (done 2026-09-30) — [src](personal/knowledge/log/2026-09-30-knowledge-base-memory-migration-env-cleanup.md)
- [x] Knowledge base: `companies/youdo/.env` empty line removed (done 2026-09-30) — [src](personal/knowledge/log/2026-09-30-knowledge-base-memory-migration-env-cleanup.md)
- [x] Knowledge base: Claude per-project memory reviewed (9 dirs, 2 non-empty); scope-of-cleanup rule moved to `AGENTS.md` "Code changes", repo policy to `general/knowledge/README.md` "Daily sync" (done 2026-09-30) — [src](personal/knowledge/log/2026-09-30-knowledge-base-memory-migration-env-cleanup.md)
- [x] youdo-mcp: port/health-check fixed at platform level: `base-images` master `a6d14d5` (`dotnet-10-ports`) sets `ASPNETCORE_HTTP_PORTS=80`/`ASPNETCORE_URLS=http://*:80` in `aspnet:10.0` (user, checked 2026-09-30); a service image built after that merge is needed for prod (done 2026-09-30) — [src](companies/youdo/knowledge/log/2026-09-18-youdo-mcp-test-nomad-healthcheck.md)
- [x] youdo-mcp: OpenIddict PFX values uploaded to Vault by the user; handoff directory `/tmp/youdo-mcp-openiddict-100y-final.68VN7g` no longer exists (done 2026-09-30) — [src](companies/youdo/knowledge/log/2026-09-21-youdo-mcp-openiddict-vault-pfx.md)
- [x] android-farm: Loki read route — obsolete: Loki moved to the dev cluster, `loki-read.yandex-test.youdo.local` retired (user, 2026-09-30); `android-dig` already reads `http://loki.dev.youdo.corp` (200 on 2026-09-30) (done 2026-09-30) — [src](companies/youdo/knowledge/log/2026-09-30-knowledge-base-stale-map-live-checks.md)
- [x] Token cost: stale questions in map Summaries resolved by read-only checks (test-k8s node group and `kube-test-temp`, build 145 revision, `dev-119`, DevOps-A-50, runner VM address and planned tag); only the Alloy push URL remains, moved to android-farm (done 2026-09-30) — [src](companies/youdo/knowledge/log/2026-09-30-knowledge-base-stale-map-live-checks.md)
- [x] Token cost: habit "one session per task; the knowledge base carries context between sessions" accepted by the user (done 2026-09-30).
- [x] Token cost: weekly measurement automated (`ai-sync.sh` writes `personal/usage/YYYY-MM-DD.txt` via `token_usage.py --kb` and a summary line into the commit); `token_usage.py --kb` measures kb_find vs full/partial reads; `kb_lint.py` warns when `AGENTS.md` exceeds 5.5 KB (done 2026-09-30) — [src](personal/knowledge/log/2026-09-30-knowledge-base-token-cost-kb-find-summaries.md)
- [x] RabbitMQ (sorm): move `RABBITMQ_ERLANG_COOKIE`/`DEFAULT_USER`/`DEFAULT_PASS` out of `docker-compose.yml`, rotate; cookie into a file (2026-09-22) — closed without action 2026-09-30: sorm handed over to another engineer — [src](companies/youdo/knowledge/log/2026-09-22-rabbitmq-config-migration.md)
- [x] RabbitMQ (sorm): delete old Mnesia `rabbit@spb2-rabbit01*` after application-level check (2026-09-22) — closed without action 2026-09-30: sorm handed over to another engineer — [src](companies/youdo/knowledge/log/2026-09-22-rabbitmq-config-migration.md)
- [x] sorm: open question which RabbitMQ is current (`rabbit@sorm-rabbitmq` vs `rabbit-cls.youdo.local`) — closed 2026-09-30, handed over — [src](companies/youdo/knowledge/systems/sorm.md)
- [x] Token cost: reconciled stale sections in 12 maps (inline `superseded` markers, current-state tables corrected from evidence in the note and TODO Done); resolved from local clones: templates `master` has MR-only rules and `GITLAB_PROJECT_ID`, docvalidation dropped the temporary `ref`, helm `PGDATA` fix merged (done 2026-09-30) — [src](personal/knowledge/log/2026-09-30-knowledge-base-token-cost-kb-find-summaries.md)
- [x] Token cost: `## Summary` in all 14 maps over 8 KB; AGENTS.md cut from 6829 to 5084 bytes with a "Token economy" section (scripts first, delegate >3 files to a subagent, compact output, `model:` line in prompts); model tier in both prompts; `general/scripts/token_usage.py` for the weekly check (done 2026-09-30) — [src](personal/knowledge/log/2026-09-30-knowledge-base-token-cost-kb-find-summaries.md)
- [x] Token cost: `general/scripts/kb_find.py` added, AGENTS.md "Before a task" points to it and to reading long notes by Summary + section; `kb_lint.py` warns on maps/recipes over 8 KB without `## Summary`; summaries added to 6 largest maps (done 2026-09-30) — [src](personal/knowledge/log/2026-09-30-knowledge-base-token-cost-kb-find-summaries.md)
- [x] `companies/youdo/.env`: renamed `ZABBIZ_DEV_TOKEN` to `ZABBIX_DEV_TOKEN` (done 2026-09-23).
- [x] dev-deployment TKB: memory fix `aa4d083` deployed (pipeline 138096, job 3120801, 2026-09-07); smoke 3120883 and regression 3120884 172/174 each, same 2 failures; peak memory not recorded (checked 2026-09-28) — [src](companies/youdo/knowledge/systems/dev-deployment/post-deploy-autotests.md)
- [x] dev-deployment: real `auto_stop_in: 7 days` expiry: `3 delete dev` 3120803 started 2026-09-14 23:24, 7 days after deploy 3120801, uninstalled release and deleted `dev-devops-832` (checked 2026-09-28) — [src](companies/youdo/knowledge/systems/dev-deployment/post-deploy-autotests.md)
- [x] DevOps-832 Tochka/TKB/Billing merged: test projects (!85, !16, !64, 01:11) with `publish-maven` + `update latests`; services !237 (01:18), !63 (01:31), !97 (01:38), master CI without pins, master pipelines green; namespace `dev-devops-832` deleted, all three environments stopped; TKB repeat deploy (Jenkins 169) done (2026-09-29) — [src](companies/youdo/knowledge/systems/dev-deployment/post-deploy-autotests.md)
- [x] dev-deployment: templates `DevOps-832-dev-autotests` merged to `master` (`12b72c9`, then `76347cd` with the suffix fix `29734d7`); test projects pushed with `DEV_HOST_SUFFIX` (tochka `d6cb806`, tkb `71ead24`, billing `b76bb67`) (done 2026-09-29)
- [x] DevOps-846 follow-ups closed by the user: concurrent case accepted as verified (test_signals), `oldest_first` not needed for now, manual prod templates need no lock, `test_signals` ref not important (done 2026-09-28) — [src](companies/youdo/knowledge/log/2026-09-28-gitlab-ci-devops-846-prod-deploy-lock-rollout.md)
- [x] DevOps-846: MR !82 and youdo.business replica jobs merged, pipeline 139705 OK (done 2026-09-28) — [src](companies/youdo/knowledge/log/2026-09-28-gitlab-ci-devops-846-prod-deploy-lock-rollout.md)
- [x] DevOps-846: linted all 23 auto-template consumers against the lock, only youdo.business affected (done 2026-09-28) — [src](companies/youdo/knowledge/systems/gitlab-ci/resource-groups.md)
- [x] Consolidated open items from all notes into this file (done 2026-09-28).

## Corporate network access

- [x] VK connectivity incident: user confirmed nginx/Nexus/Nomad recovery and then all Jenkins UI/version/branch functions working; no agent runtime changes or builds, exact root cause and sustained stability unverified, support draft not sent by agent (2026-10-21) — [src](current/knowledge/log/2026-10-21-vk-cloud-inter-subnet-access-outage.md)

- [x] VPN access to 10.18.24.233: user confirmed access works and requested closure on 2026-10-20; further packet-loss investigation closed without additional diagnostics or network changes (original 2026-10-11) — [src](companies/youdo/knowledge/log/2026-10-11-corporate-network-ssh-10-18-24-233.md)
- [x] Complete host-specific SSH config for 10.18.24.233: user runs prepared sudo script to exclude SendEnv, then verify plain interactive login (2026-10-11) — [src](companies/youdo/knowledge/log/2026-10-11-corporate-network-ssh-10-18-24-233.md)

- [x] dynamic_inventory CI: permanent registry-compatible image publication cancelled by the user on 2026-10-20 because no service updates are planned; closed without CI changes or image publication (original proposal 2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-13-gitlab-ci-dynamic-inventory-vk-migration-plan.md)

- [x] nomad-test DevOps-897: confirmed deletion of PA2 disk af3c6ccb-402e-4d2e-9b0b-d1a5fe075842 with fresh token, DELETE202/GET404; no replacement or VM (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-14-nomad-test-devops-897-small-mssql-test5.md)
- [x] nomad-test DevOps-897: published dad41d4/MR106 and explicitly authorized merge to master9ad35fb; one-line absent MSSQL job handling on DevOps-897-handle-missing-mssql-job; only deploy_mssql_nomad.yml, exclude all large DB local edits (2026-10-14) — [src](companies/youdo/knowledge/log/2026-10-14-nomad-test-devops-897-small-mssql-test5.md)

- [x] Monolith fresh NuGet restore/build3226699 andDocker3226700 completed after corrected MassTransit1.8.1 publication; direct Nomadtest5 version3 deployment successful, both groups healthy19services/restarts0; no source changes (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-monolith-messagebus-assembly-mismatch.md)

- [x] Check final Jenkins dynamic_deploy5824: FAILURE onPostupdateauth timeout; monolith/static rollout successful andNomadhealthy/restarts0 (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-test5-full-deploy-with-static.md)

- [x] Suggestions reindex deployment blocker superseded: Jenkins5826 SUCCESS with SUGGESTIONS_REINDEX=true; no claim about intervening fix/root cause (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-build5826-plan-reconciliation.md)

- [x] Jenkins recovery quiet hook removed from startup at user request; backup retained outside init.groovy.d with0600/root, independent SSH check and API quietingDown=false; no restart (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-build5826-errors-and-disable-quiet-hook.md)

- [x] Jenkins dynamic_deploy BuildAPI publication: four URLs corrected, HTTP failure handling enabled, exact script hash/approval verified; restored5826 test5 current/history metadata and checked rendered home; no deploy rerun (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-buildapi-publication-fix.md)


- [x] DevOps-899: eight selected Monolith services rebuilt/deployed on test5 and accepted in BuildAPI; antifraud23.8.7 directPG5432, escrow13.8.12/shared router healthy, monolith VK routing fixed, config/preprod audited. Form excluded (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-devops-899-monolith-microservice-recovery.md)
- [x] Next test5 rollout: seven Nomad services deployed (broadcast1.2.11, featuretoggle1.0.11, Content2.5.13, Landings1.3.35, trackingpixel1.0.5, Socket1.2.9, Help1.0.14); moderation1.0.45 S3 accepted. BuildAPI metadata/live checked; Landings/Socket UI limits retained. Cerberus excluded (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-next-test5-service-rollout.md)
- [x] BuildAPI UI: map YouDo.Socket project name to socketchat Consul service for rendered version cell; closed without implementation at user request on 2026-10-20: not needed; historical live API and deployed1.2.9 were correct (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-next-test5-service-rollout.md)
- [x] DevOps-899: seeded eight-service BuildAPI catalogs for13other stands with104correct per-stand manualjob IDs/URLs; GET verified, test5 unchanged (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-devops-899-monolith-microservice-recovery.md)
- [x] Runner DNS investigation closed by user: currently working; no further diagnosis requested. Historical NXDOMAIN and green zero-task deploys retained; no runner DNS change or root-cause verification performed in this closure (2026-10-20) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-devops-899-monolith-microservice-recovery.md)
- [x] Verify final devdocker pipeline140984: master_build3228589FAILED/test3228588SUCCESS; independent PostgreSQL10publication and Broadcast acceptance retained, full6image recovery not established (checked2026-10-16) — [src](current/knowledge/log/2026-10-16-nomad-test-recovery-comment-completeness-recheck.md)

### Featuretoggle test5

- [x] User-approved featuretoggle-to-test5 PostgreSQL seed completed:149 features/293history rows; ordered data hashes match, ID sequences350/521 (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-nomad-test-featuretoggle-test5-seed.md)
- [x] Inserted49missing production-CSV feature keys into test5 (38enabled/11disabled); verified198total keys and149existing rows unchanged (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-nomad-test-featuretoggle-test5-seed.md)
- [x] Resolved featuretoggle-test5 old Npgsql auth with user-approved MD5 only for shared youdo role; default/other roles retain SCRAM, API HTTP200/198features verified (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-nomad-test-featuretoggle-test5-seed.md)

- [x] SMS test5 master-191: all3images+188tests passed; approvedB2B44CIpublickeyadded/rootSSHverified; deploy3228662SUCCESS, migrations/webapp/worker healthy, BuildAPI accepted (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-nomad-test-sms-service-test5-deployment-analysis.md)

- [x] User-approved13featuretoggle DB clones completed from configured test5 to test,test1-test4,test6-test7,test10-test15; all hashes/sequences verified, source unchanged (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-nomad-test-featuretoggle-stand-clones.md)
- [x] User-approved main featuretoggle refresh completed from configured test5 with protected backup;198features/301history, hashes/sequences verified (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-nomad-test-featuretoggle-stand-clones.md)

- [x] Antifraud: subsequent user rollout jobs3229391–3229395 succeeded on test2/3/4/5/7; all allocations healthy and BuildAPI23.8.8 reconciled automatically (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-postgresql-antifraud-pgbouncer-minimal-setup.md)

- [x] C2C PostgreSQL39: raise max_connections100→500, restart cluster16/main and verify SQL/PgBouncer/Antifraud health (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-postgresql-c2c-max-connections-500.md)

- [x] PgBouncer PG39: max_client_conn100→500 approved/applied via reload; live SHOW CONFIG500 verified, backend cap10/2 preserved (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-postgresql-antifraud-five-stand-acceptance.md)

- [x] Broadcast1.2.11: all eight test/test1-test7 accepted; seven new jobs succeeded, test5 retained, all migrations0/healthy0restarts/BuildAPI matched (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-broadcast-eight-stand-rollout.md)

- [x] FeatureToggle1.0.11: all eight parallel test/test1-test7 jobs SUCCESS, Nomad running/healthy/zero restarts; user-requested status-only checks (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-featuretoggle-eight-stand-rollout.md)
- [x] Landings1.3.35: all eight parallel test/test1-test7 jobs SUCCESS, Nomad running/healthy/zero restarts; status-only validation (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-landings-eight-stand-rollout.md)

- [x] Socket1.2.9: test5 CLI monitoring failure diagnosed; user-requested retry3229442 SUCCESS; all eight jobs SUCCESS and Nomad healthy/zero restarts (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-socket-eight-stand-rollout.md)

- [x] Help1.0.14: all eight parallel test/test1-test7 deploy jobs SUCCESS, Nomad running/healthy0restarts, status-only checks (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-help-eight-stand-rollout.md)

- [x] Content2.5.13: all eight parallel deploy jobs SUCCESS and Nomad running/healthy0restarts, GitLab/Nomad statuses only (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-content-eight-stand-rollout.md)

- [x] SMS master-191: all eight parallel jobs SUCCESS, Nomad running/healthy0restarts, status-only checks (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-sms-eight-stand-rollout.md)

- [x] Moderation1.0.45: seven parallel static publication jobs SUCCESS; test5 retained; selected eight-stand rollout sequence complete (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-moderation-seven-stand-publication.md)

- [x] Cerberus2:1.0.9 accepted on14stands test/test1-test7/test10-test15; GitLab all SUCCESS/Nomad all running/healthy, PG/PgBouncer1000 applied (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-jenkins-cerberus-eight-stand-rollout.md)

- [x] Base-images: SDK2.1/ASP.NET2.1 recipes MR42 merged/tagged, both images locally built/checked/pushed and registry verified; SDKCI canceled/runtimeCI succeeded (2026-10-15) — [src](companies/youdo/knowledge/log/2026-10-15-base-images-dotnet21-mirrors.md)

- [x] Update existing YouTrack summary comments for DevOps-899/898/894/892/891/896/889 after full evidence reconciliation; user correction applied,7existingIDs preserved/exact readback verified/no new comments/closed states retained (done2026-10-16) — [src](current/knowledge/log/2026-10-16-nomad-test-recovery-existing-comments-updated.md)

### VK test mailer SMTP

- [x] Review and approve mail authentication recovery: PTR for138.16.203.115, DKIM integration and DMARC; handed over to another employee per user on 2026-10-20, removed from the user backlog without implementation; historical findings: Gmail test lands in spam and Yandex rejects554 (2026-10-16) — [src](current/knowledge/log/2026-10-16-nomad-test-mailer-smtp-diagnosis.md)

- [x] Correlate newly reported undelivered mail: three Yandex attempts reached recipient MX and were bounced5545.7.1 suspicionofSPAM; VK SMTP trust works (2026-10-16) — [src](current/knowledge/log/2026-10-16-nomad-test-mailer-smtp-diagnosis.md)

- [x] Apply user-approved VK egress85.192.34.208/32 SMTP trust on postfix-test: persistent/effective config, check/reload, RCPT250 and ordinaryDATA sessions verified (2026-10-16) — [src](current/knowledge/log/2026-10-16-nomad-test-mailer-smtp-diagnosis.md)
- [x] Review mailer scheduler OOM, historical API PostgreSQL-limit failures, System.Data.SqlClient logger mismatch and SMTP greeting/CRLF handling separately; closed by user on 2026-10-20: mailer works correctly on test stands, no further investigation requested; no new fixes or independent verification claimed (original findings 2026-10-16) — [src](current/knowledge/log/2026-10-16-nomad-test-mailer-smtp-diagnosis.md)
- [x] SMTP trust MR1379 user-authorized merged200eada5 into master; task commit ff104e33, CI141074 skipped; runtime and canonical Ansible now aligned (2026-10-16) — [src](current/knowledge/log/2026-10-16-nomad-test-mailer-smtp-diagnosis.md)


### web-autotests — user-accepted closure (2026-10-20)

- [x] Investigate VK Cloud worker creation/registration: quota API shows88 vCPU/150 GB RAM free and autoscaler requests remain below max10, but new nodes timed out registering; inspect provider events/logs. Validate worker-host DNS path to registry.youdo.sg (transient timeout in build3362; none in3363 retry chain) (2026-10-16) — [src](companies/youdo/knowledge/log/2026-10-16-jenkins-selenium-vk-grid-session-eof.md) Manual minimum increase on2026-10-19 succeeded by12:11UTC: min3/target3/Ready3, new workers-2; subsequent Selenium demand-driven3->4scale-up succeeded by12:21UTC/all12ChromeReady12:22UTC, while historical timeout root cause/provider logs remain unresolved ([check](current/knowledge/log/2026-10-19-vk-cloud-k8s-manual-minimum-scale-check.md)). Evening20:17UTC check confirmed Selenium-driven3->4->5->6 scaling, all6Ready/min3/max10 and3scale-down candidates; historical timeout cause remains open ([evidence](current/knowledge/log/2026-10-19-vk-cloud-k8s-six-workers-selenium.md)). Closed by user on 2026-10-20: system now works; follow-up no longer required. No independent root-cause, DNS, QA, state-leak or timing verification claimed.
- [x] Wait for QA feedback on web autotests after `scalingType: deployment`; for a fair wall-time comparison with Selenoid run regress part 1 from `master` on `test7` (2026-10-01) — [src](companies/youdo/knowledge/log/2026-10-01-web-autotests-selenium-keda-polling-interval-effect.md) Closed by user on 2026-10-20: system now works; follow-up no longer required. No independent root-cause, DNS, QA, state-leak or timing verification claimed.
- [x] Selenium Grid deployment mode: during the next regress runs (only then do chrome pods exist; none on 2026-10-01, no tests running) watch scale-down of busy node pods and browser state leaks across sessions (2026-10-01) — [src](companies/youdo/knowledge/log/2026-10-01-web-autotests-selenium-keda-polling-interval-effect.md) Closed by user on 2026-10-20: system now works; follow-up no longer required. No independent root-cause, DNS, QA, state-leak or timing verification claimed.
- [x] Regress 108 vs 94 min (three/1622 vs Selenoid two/1978): stands currently have problems with SBR (safe deal) and insurance (reported to the user 2026-10-01), likely part of the gap; re-measure after the stands are fixed, and only if a gap remains check Chrome pod CPU throttling in VictoriaMetrics (`container_cpu_cfs_throttled_periods_total` / `container_cpu_cfs_periods_total`, pods `selenium-node-chrome`); image pre-pull is moot in deployment mode (2026-10-01) — [src](companies/youdo/knowledge/log/2026-09-30-web-autotests-selenium-grid-k8s-slow-regress.md) Closed by user on 2026-10-20: system now works; follow-up no longer required. No independent root-cause, DNS, QA, state-leak or timing verification claimed.

### Yandex recovery DevOps-889/888 — superseded by VK migration

- [x] DevOps-889: adapt the weekend scheduler to use mssql_inventory.ini after publication; existing dynamic inventory has no client-side folder filter (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-889-mssql-recovery-plan.md) Closed by user on 2026-10-20 as obsolete after migration to VK Cloud; no completion of the original Yandex action claimed.
- [x] DevOps-889: HDD selected; base fits current quotas, resolve final-three HDD capacity (505/1100 GiB usage/limit; minimum 1705 GiB MSSQL alone or conditional 1825 GiB with ES on same three stands; propose 2000 GiB, confirm ES stand scope), recheck resource state before approved runtime retry (2026-10-10) — [src](companies/youdo/knowledge/log/2026-10-10-yandex-cloud-devops-889-mssql-hdd-disk-selection.md) Closed by user on 2026-10-20 as obsolete after migration to VK Cloud; no completion of the original Yandex action claimed.
- [x] DevOps-889: minimal seven-stage destination/inventory and HDD edits checked; execute each reviewed stage with explicit runtime approval, resolve final HDD quota before step_6, then review publication (2026-10-10) — [src](companies/youdo/knowledge/log/2026-10-10-yandex-cloud-devops-889-mssql-hdd-disk-selection.md) Closed by user on 2026-10-20 as obsolete after migration to VK Cloud; no completion of the original Yandex action claimed.
- [x] DevOps-888: reconcile infra-tf/dev declarations/addresses with terraform/yandex-dev-k8s-a before apply; checked plan deletes cluster, cloud identity, CI identity, Vault reviewer and VSO (2026-10-10) — [src](companies/youdo/knowledge/log/2026-10-10-yandex-cloud-devops-888-vault-integration.md) Closed by user on 2026-10-20 as obsolete after migration to VK Cloud; no completion of the original Yandex action claimed.
- [x] DevOps-888: after infra-tf/dev state and platform reconciliation, verify dev-ephemeral-deployer login and registry/RabbitMQ secret sync in a dev-* namespace; Sentry resources integration already works (2026-10-10) — [src](companies/youdo/knowledge/log/2026-10-10-yandex-cloud-devops-888-vault-integration.md) Closed by user on 2026-10-20 as obsolete after migration to VK Cloud; no completion of the original Yandex action claimed.
- [x] DevOps-888: verify corporate DNS from a workload and prepare application/data recovery plus infra-tf/dev integration with yc-a-k8s-dev (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-888-a-cluster-ready.md) Closed by user on 2026-10-20 as obsolete after migration to VK Cloud; no completion of the original Yandex action claimed.
- [x] DevOps-888: verify original kube-test private API from runner/bastion and assess zonal-master recovery vs new a workers (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-888-original-cluster-migration-check.md) Closed by user on 2026-10-20 as obsolete after migration to VK Cloud; no completion of the original Yandex action claimed.
- [x] DevOps-888: resolve Compute CPU/RAM quota headroom for preserved max10 workers and rollout capacity; initial1 fits (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-888-yc-a-k8s-dev.md) Closed by user on 2026-10-20 as obsolete after migration to VK Cloud; no completion of the original Yandex action claimed.
