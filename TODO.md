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

### Security: leaked or plaintext credentials

- [ ] Rotate yc authorized key `aje1kjc599tg2oj7ok2d` (private part leaked into session output), update consumers, delete the old key (2026-09-13) — [src](companies/youdo/knowledge/log/2026-09-13-workstation-yc-cli-auth-recovery.md)
- [ ] Rotate the c2c prod PostgreSQL password printed in an agent session; consider a separate read-only role for agents (2026-09-23) — [src](companies/youdo/knowledge/log/2026-09-23-selectel-c2c-prod-postgres-access.md)
- [ ] Rotate the `dba_automation` SQL password disclosed in diagnostic output (2026-08-02) — [src](companies/youdo/knowledge/log/2026-08-02-mssql-yandex-mssql-restore-youdo.md)
- [ ] `buildapi/production.nomad`: check validity of plaintext `NOMAD_TOKEN`, `JENKINS_LOGIN`, `JENKINS_PASSWORD`; move to Vault and rotate (2026-09-13) — [src](companies/youdo/knowledge/log/2026-09-13-nomad-test-buildsinfo-csi-stale-attachment.md)
- [ ] Android/GitLab runner host_vars hold plaintext access material: migrate to Ansible Vault, rotate, verify runner registration/registry/S3 cache (2026-08) — [src](companies/youdo/knowledge/systems/android-farm/ci-cd.md), [src](companies/youdo/knowledge/systems/gitlab-ci/android-youdo4-dynamic-runner.md)
- [ ] `fastlane-docker` worktree: untracked Firebase service-account JSON; move to a protected GitLab file variable, keep ignored (2026-08) — [src](companies/youdo/knowledge/systems/android-farm/ci-cd.md)
- [ ] Android autotest reports: stop `--acl public-read` on Yandex Object Storage, redact headers and credential-bearing app URLs from HTML logs/capabilities (2026-08-12) — [src](companies/youdo/knowledge/log/2026-08-12-android-farm-autotests-report-3063278.md)
- [ ] Nexus `raw-private` is anonymously downloadable by URL: fix access; delete the ADB-key archive `/root/android-avd-nexus-5x-template-api29-20260805.tar.zst` on M-K0057 (2026-08-04) — [src](companies/youdo/knowledge/log/2026-08-04-android-farm-avd-template-transfer.md)
- [ ] Replace the workstation `~/.vault-token` with `root` policy by a token limited to `ansible-infra` (coordinate with the owner); ask Vault admins to map the LDAP group to read `secret/ansible/{prod_selectel,prod_yandex,common}` (2026-09-18) — [src](companies/youdo/knowledge/systems/automation-services/local-vault-ansible-access.md)
- [ ] infra-tf `dev/config/vmalertmanager.yml` and `prod/config/vmalertmanager.yml`: plaintext Rocket.Chat webhook token; move to Vault and rotate (2026-10-07) — [src](companies/youdo/knowledge/log/2026-10-07-dev-deployment-devops-886-ttl-controller.md)
- [ ] sc-except: move secrets out of `/data/docker-compose.yml` and Zabbix scripts (2026-06-13) — [src](companies/youdo/knowledge/log/2026-06-13-sc-except-mssql-unavailable.md)

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

- [x] DevOps-893: closed by user; published commit22e451e/MR440, VK CI plan/apply succeeded, all eight jobs checked, CSI8/8healthy and SSD lifecycle passed. Further plan convergence check waived by user; version difference is a hypothesis. External applications excluded (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nomad-test-devops-893-vk-ci-publication-preparation.md)

- [ ] agent-test-01: remove dnsmasq `log-queries` or log to a separate rotated file; size-based syslog rotation; check filesystem alerts before 100% (2026-09-22) — [src](companies/youdo/knowledge/log/2026-09-22-nomad-test-agent-test-01-disk-full.md)
- [ ] Night shutdown: collect Nomad/Consul versions, job `disconnect`/`reschedule` settings, host/CSI volumes, morning recovery window, cost of the 9 client VMs (2026-09-09) — [src](companies/youdo/knowledge/log/2026-09-09-nomad-test-night-shutdown-cost.md)
- [ ] After the next agent-group power-on: 9/9 nodes ready, quorum, blocked evals -> 0, `proxy.service` DNS vs nginx upstreams, CSI and periodic jobs (2026-09-11) — [src](companies/youdo/knowledge/log/2026-09-11-nomad-test-agent-group-stop-pilot.md)
- [ ] Follow up `http-headers-viewer` port conflict, `similar-tasks/indexer` prestart failure, stale `spb2` child of `jaeger-index-cleaner`; do not scale below 7 clients without reconciling reservations (2026-09-13) — [src](companies/youdo/knowledge/log/2026-09-13-nomad-test-agent-scale-down.md)
- [ ] Resource optimization: next iteration with pooled cross-stand soft reservation and global peak hard max; monitor OOM/restarts after lowered reservations (2026-09-13) — [src](companies/youdo/knowledge/log/2026-09-13-nomad-test-resource-optimization.md), [src](companies/youdo/knowledge/log/2026-09-09-nomad-test-automation-test-yandex-nomad-memory.md)
- [ ] Upgrade Nomad from `1.5.3` (all 7 clients and 3 servers on Yandex test, API 2026-09-30), fix `KillMode=process` (still in `automation-test-yandex` `deprecated/roles/nomad-client/templates/nomad.systemd.j2:10`); clean stale `/var/lib/nomad/alloc` on agent-test-02 (2026-07-21) — [src](companies/youdo/knowledge/log/2026-07-21-nomad-test-agent-test-02-crash-loop.md)

- [ ] DevOps-894: VK-only fast ES playbooks adapted, create_image executed and thin/thick snapshots available; clone/ES preparation checks removed per user; next review Git publication and pilot one stand, separately adapt DBA_Clean destination and restore AWX weekly workflow (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nomad-test-devops-894-playbook-adaptation.md)

### automation-services (nginx, Ansible)

- [ ] Yandex test nginx: dynamic upstream refresh for `proxy.service.yandex-test.consul` (or consul-template reload); drain procedure before removing a proxy client (2026-09-11) — [src](companies/youdo/knowledge/log/2026-09-11-automation-services-yandex-test-nginx-stale-nomad-proxy.md)
- [ ] Nexus nginx: fix client temp storage/buffering for large PUT uploads (HTTP 413/500) (2026-08-04) — [src](companies/youdo/knowledge/log/2026-08-04-android-farm-avd-template-transfer.md)
- [ ] prod_yandex GitLab runners: persist or roll back runtime-only `concurrent = 2`/`overlay2` on `10.16.24.173`; decide `docker builder prune`; review untracked host_vars in the worktree (2026-06-03); kept by the user 2026-09-30: runner host_vars moved to `deprecated/` in automation-services (AP-2228, `d3d6133c`), `10.16.24.173`/`concurrent = 2` not in the repo — [src](companies/youdo/knowledge/log/2026-06-03-gitlab-ci-prod-yandex-docker-3-dind-nexus.md)
- [ ] Apply the gitlab-runner playbook to the Selectel docker3 host (2026-06-04); kept by the user 2026-09-30: vars now in `deprecated/inventories/prod_selectel/host_vars/gitlab-runner-docker-3.yml` (`d13d56fd`), live host `gitlab-runner-dind03` — [src](companies/youdo/knowledge/log/2026-06-04-automation-services-prod-selectel-gitlab-runner-docker3-b2b.md)

### yandex-cloud / Terraform

- [ ] DevOps-889: adapt the weekend scheduler to use mssql_inventory.ini after publication; existing dynamic inventory has no client-side folder filter (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-889-mssql-recovery-plan.md)
- [ ] MSSQL refresh proposal: verify exact backup readability/type/date and destination capacity before dropping DB; add sqlcmd -b and guaranteed login re-enable on failure (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-889-mssql-recovery-plan.md)
- [ ] MSSQL refresh proposal: version prepared images and retain the last good image until acceptance; define retention and image quota needs separately (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-889-mssql-recovery-plan.md)
- [ ] MSSQL refresh proposal: distinguish missing resources from API errors and validate intended folder/resource before deletion; add quota preflight only if separately requested (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-889-mssql-recovery-plan.md)
- [ ] MSSQL refresh proposal: replace fixed waits/ignored errors with readiness checks for all three VMs, SQL hostname and monitoring; review xp_cmdshell dependency and fragile ping parsing (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-889-mssql-recovery-plan.md)
- [ ] MSSQL automation proposal: migrate plaintext credentials in SQL/Windows group_vars, tester task and inventory client to the established secret store; preserve values only in approved secret locations (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-889-mssql-recovery-plan.md)

- [ ] DevOps-889: HDD selected; base fits current quotas, resolve final-three HDD capacity (505/1100 GiB usage/limit; minimum 1705 GiB MSSQL alone or conditional 1825 GiB with ES on same three stands; propose 2000 GiB, confirm ES stand scope), recheck resource state before approved runtime retry (2026-10-10) — [src](companies/youdo/knowledge/log/2026-10-10-yandex-cloud-devops-889-mssql-hdd-disk-selection.md)

- [ ] DevOps-889: minimal seven-stage destination/inventory and HDD edits checked; execute each reviewed stage with explicit runtime approval, resolve final HDD quota before step_6, then review publication (2026-10-10) — [src](companies/youdo/knowledge/log/2026-10-10-yandex-cloud-devops-889-mssql-hdd-disk-selection.md)

- [x] DevOps-888: deploy a recovery cluster and CoreDNS after runnernetwork fix; job3217390 successful, nodeReady and refreshplan no changes (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-888-dev-k8s-e-recovery.md)
- [ ] DevOps-888: reconcile infra-tf/dev declarations/addresses with terraform/yandex-dev-k8s-a before apply; checked plan deletes cluster, cloud identity, CI identity, Vault reviewer and VSO (2026-10-10) — [src](companies/youdo/knowledge/log/2026-10-10-yandex-cloud-devops-888-vault-integration.md)
- [ ] DevOps-888: after infra-tf/dev state and platform reconciliation, verify dev-ephemeral-deployer login and registry/RabbitMQ secret sync in a dev-* namespace; Sentry resources integration already works (2026-10-10) — [src](companies/youdo/knowledge/log/2026-10-10-yandex-cloud-devops-888-vault-integration.md)
- [ ] DevOps-888: verify corporate DNS from a workload and prepare application/data recovery plus infra-tf/dev integration with yc-a-k8s-dev (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-888-a-cluster-ready.md)
- [x] DevOps-888: review CI and merge MR !236 for already manually applied Terraform CI identity before another masterapply; kubeconfig exported/protected/tested, update CI integration after approval (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-888-ci-kubeconfig.md) — done 2026-10-09; MR merged/pipeline140514 converged, current CI kubeconfig delivered; variable update not performed by agent
- [x] DevOps-888: compare CI1.7.5 and local1.9.4 plans for empty in-place CI Secret diff in job3217580 before diagnosing token change (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-888-job-3217580.md) — closed 2026-10-09 after user CI apply and repeat plan no changes; exact cause unproven
- [ ] DevOps-888: verify original kube-test private API from runner/bastion and assess zonal-master recovery vs new a workers (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-888-original-cluster-migration-check.md)
- [ ] DevOps-888: resolve Compute CPU/RAM quota headroom for preserved max10 workers and rollout capacity; initial1 fits (2026-10-09) — [src](companies/youdo/knowledge/log/2026-10-09-yandex-cloud-devops-888-yc-a-k8s-dev.md)

- [ ] `yandex-tf/.gitlab-ci.yml`: `workflow:rules` for MR and default branch only (deferred by the user 2026-09-23) — [src](companies/youdo/knowledge/log/2026-09-23-yandex-cloud-yandex-tf-network-ansible-job.md)
- [ ] Ansible for `ipsec`/`balancers_test` is manual; nothing re-applies config after VM changes (2026-09-23) — [src](companies/youdo/knowledge/log/2026-09-23-yandex-cloud-yandex-tf-network-ansible-job.md)
- [ ] test-k8s: choose K8s version and upgrade chain, pin module source, fix `template_name`/default zone, re-plan; review SG egress and audit logging (2026-08-11) — [src](companies/youdo/knowledge/log/2026-08-11-yandex-cloud-yandex-tf-test-k8s-audit.md)
- [ ] K8s sizing for Nomad migration: 10-14 days of metrics, folder quotas, `maxPods`/pod CIDR, autoscaler 14-16 nodes (2026-08-11) — [src](companies/youdo/knowledge/log/2026-08-11-yandex-cloud-k8s-nomad-sizing.md)
- [ ] Temporal dev: review plan and apply in a change window; PVC backup policy; maintained PostgreSQL 16 image before prod — [src](companies/youdo/knowledge/systems/temporal.md)

### selectel


### ios-ci

- [x] Restore DNS reachability for `idcn-10`: user-approved Ethernet DNS `172.28.0.200` applied; default GitLab resolution/HTTPS pass, runner 93 online confirmed by GitLab GET at 21:32 MSK (2026-10-12) — [src](companies/youdo/knowledge/log/2026-10-12-ios-ci-runner-offline-dns-unreachable.md)
- [ ] YouDoApp fastlane (DevOps-880): move `build_release` `testflight` from Apple-ID session to App Store Connect API key; key setup per https://developer.apple.com/documentation/appstoreconnectapi/creating-api-keys-for-app-store-connect-api (no `app_store_connect_api_key` in `develop` Fastfile; fastlane `2.240.0` pinned in `Gemfile` and installed on `idcn-10` by the user; checked 2026-10-05; 2026-10-06: `ASC_KEY_ID`/`ASC_ISSUER_ID`/`ASC_KEY_CONTENT` (base64 .p8, masked, not protected — no protected tags) added in GitLab; branch `IOS-5054`: `testflight` uses `app_store_connect_api_key`, all three `sigh download_all` CI calls use `--api_key_path`; 2026-10-07: MR !3273 merged (`bf7d07f089`), `Build beta ad-hoc` and `Build development` pass with API key; remaining: the first release job (`testflight` with API key), then drop `APPLE_DEVELOPER_USER`/`FASTLANE_SESSION` if unused) (2026-09-14) — [src](companies/youdo/knowledge/log/2026-09-14-ios-ci-fastlane-spaceauth-service-key.md)

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

- [x] Verify actual Jenkins job launch and controller credentialed GitLab checkout: test-git4 SUCCESS, revision a240575a6a360a908005fb3f1814fca13ee6e065; agent checkout remains pending (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-jenkins-devops-892-git-smoke.md)

- [ ] Finish Jenkins VK recovery: controller 10.18.26.8 and AutoTest 10.18.26.26 restored and internally verified; quiet mode restored after explicit user approval; API verified quietingDown=true. test-git4 SUCCESS on controller, queue0; permanent recovery hook remains. Agent current disk approved, 7.8 GB free. Replacement balancer 10.18.20.97 supplied by user: existing Nginx route HTTPS200/TLS verified with forced address; public DNS IP138.16.201.238 verified HTTPS200/TLS through corporate OpenVPN (already allowed source45.159.210.228). Local138.16.201.238/32 TrustTunnel exclusion prepared; user screenshot subsequently confirms authenticated browser access at https://build.youdo.sg. Active client route/restart status was not independently checked. Temporary runtime firewall ACCEPT for172.28.0.200/32 TCP80/443 removed at explicit user request; absence verified and public HTTPS through corporate OpenVPN still returns200. No firewall persistence is needed for that removed rule. Browser access is verified by the user; WebSocket forwarding remains to be verified. Restore backup DAG/source and backup-host SSH access. User deferred monitoring and Ansible Git publication on October13; keep local Ansible changes. Align approved Ansible/base compose image with verified digest override later; current base2-555-1-2 could restore defective image on future base-only apply. Actual job launch and controller credentialed GitLab checkout verified by test-git4 SUCCESS; AutoTest actual checkout remains pending. Downstream failures due to unavailable infrastructure are acceptable for this acceptance stage. Both hosts GitLab DNS/HTTPS200 verified. General quiet-mode release/removal of the persistent recovery hook still needs approval (2026-10-13) — [plan](companies/youdo/knowledge/log/2026-10-13-jenkins-devops-892-vk-recovery-plan.md), [balancer check](companies/youdo/knowledge/log/2026-10-13-jenkins-devops-892-vk-balancer-check.md)

- [x] Persistent controller Git correction DevOps-891 complete: .dockerignore MR17 merged96a754a6, master pipeline140773SUCCESS, digest458ac695… deployed by approved recreation; root .git/key absent, stored-credential lookup205/master and API acceptance pass (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-jenkins-devops-891-fixed-image-recreation.md)

- [ ] Review and approve proposed Ansible recovery stages/guards, endpoint and secret parameters, DNS/Nginx rollback, Docker/containerd storage and consistent backup verification (2026-10-11) — [src](companies/youdo/knowledge/log/2026-10-11-jenkins-devops-890-recovery-runbook.md)

- [ ] Historical Yandex recovery follow-ups (superseded by the VK recovery above while Yandex is unavailable): verify representative workflows, restore backup DAG and monitoring; runtime changes require explicit approvals. Stage1 done October11: two-host/root inventory, Vault/registry authorization with VAULT_YANDEX_TEST_TOKEN. Stage2 done: both disks ext4/mounted at /data, UUID fstab entries and systemd mount units verified after approved daemon-reload. Stage3 done October11: backup restored and independently verified (11 jobs,116 plugins); Stage4 done October11: controller apply passed, API auth works,11 jobs/116 active plugins; Stage5 done October11: agent deployed, AutoTest online via WebSocket with5 executors. Stage6 done October11: public build.youdo.sg routes to newcontroller, HTTPS/API verified; localbalancer DNS/upstream persistence prepared. Publication completed October11 under explicit approval: five-file commit3ad647f0ff6ed5b8d17e14f42401b0577a5ede21, [MR !1368](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1368) targetingmaster; pipeline140550 skipped, no merge/deployment. User excluded recoveryinventory, which remains local/untracked; functional workflows/backup/monitoring still open (2026-10-10) — [plan](companies/youdo/knowledge/log/2026-10-10-jenkins-devops-890-recovery-audit.md), [stage 1](companies/youdo/knowledge/log/2026-10-11-jenkins-devops-890-inventory-dependencies.md), [stage 2](companies/youdo/knowledge/log/2026-10-11-jenkins-devops-890-data-disks.md)

### GitLab extraform image recovery

- [x] Enable instance/shared runners for `data/dockers`: done by the user; build running (user-reported, 2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-gitlab-extraform-python-uv-runner-disabled.md)
- [x] Verify Python UV base build3222108: GET confirms success after user enabled instance runners; extraform retry3222248 then fails at frozen dependency download youdo-basis10.0.2 from legacy PyPI, recovery continues separately (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-recovery-plan.md)
- [x] Restore youdo-basis10.0.2: exact locked wheel/sdist rebuilt from unchanged source using historical tools, approved publication and Nexus metadata hashes verified (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-basis-recovery.md)
- [x] Build extraform0.31.17 locally from unchanged release GitSHA3c04a38b; image/runtime metadata verified and original checkout branch restored clean (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-basis-recovery.md)
- [x] Publish runtime-required extraform registry tag0-31-17 after approval; independent manifest/config digest matches local release-source image, no aliases/deployment/job execution (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-basis-recovery.md)
- [x] Inventory known company Nomad periodic parents:160jobs/23periodic/eightuniqueimages; extraform image restored for four tasks (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Restore four more periodic runtime images: daily-compilations-generator0.6.9/cashflowmaster/nexus-cleaner0.0.10/youtrack_sprints_creatormaster approved pushes exit0 and independent remote-config matches local images; with extraform five ofeight images cover19of23tasks. No deployments/periodic runs (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Build approved exact historical release copies rowers-ranker0.19.3 and recommended-tasks-generator1.16.24 with only five Pipfile.lock hash replacements: both original Dockerfiles/builds/safe metadata checks passed, tags and other source files verified unchanged; no Git or runtime publication (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Publish final three approved periodic runtime tags ab-pipeline:master/rowers-ranker:0.19.3/recommended-tasks-generator:1.16.24; push exit0 and independent configs match. Final manifest GETs verify8of8runtime refs for23periodic jobs; seven configs match our publications and cashflow:master is a verified later CI image, not overwritten. No job/deploy/merge (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)

### web-autotests (Jenkins `Web+API Tests`, Selenium Grid k8s-dev)

- [ ] Wait for QA feedback on web autotests after `scalingType: deployment`; for a fair wall-time comparison with Selenoid run regress part 1 from `master` on `test7` (2026-10-01) — [src](companies/youdo/knowledge/log/2026-10-01-web-autotests-selenium-keda-polling-interval-effect.md)
- [ ] Selenium Grid deployment mode: during the next regress runs (only then do chrome pods exist; none on 2026-10-01, no tests running) watch scale-down of busy node pods and browser state leaks across sessions (2026-10-01) — [src](companies/youdo/knowledge/log/2026-10-01-web-autotests-selenium-keda-polling-interval-effect.md)
- [ ] Regress 108 vs 94 min (three/1622 vs Selenoid two/1978): stands currently have problems with SBR (safe deal) and insurance (reported to the user 2026-10-01), likely part of the gap; re-measure after the stands are fixed, and only if a gap remains check Chrome pod CPU throttling in VictoriaMetrics (`container_cpu_cfs_throttled_periods_total` / `container_cpu_cfs_periods_total`, pods `selenium-node-chrome`); image pre-pull is moot in deployment mode (2026-10-01) — [src](companies/youdo/knowledge/log/2026-09-30-web-autotests-selenium-grid-k8s-slow-regress.md)

### Nexus recovery

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
- [ ] Investigate recommended3223107 successful-build push finalization (runner105/client25.0.5-git/DinD20.10,14of15layers pushed, prep22m09) and daily3223113 base-pull extraction/registration (runner106/client+DinD19.03.12,8downloads complete/3pulls complete, prep10m18); both hit1hour, specific network cause unproven, no fixes/retries authorized by hash MRs (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Verify explicitly authorized recommended-tasks-generator retry3223259 succeeded at23:51MSK: sameSHA5899dd9e, final branch/latest manifests digest1a1ceb2c; original push-timeout root cause unproven (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Obtain supervised task-quality-control branch reuse approval and apply minimal build-job Docker29.9.0-cli/DinD pin locally in .gitlab-ci.yml; exactly two lines, release job untouched, diff check passes, not staged/committed/pushed (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Validate/review task-quality-control two-line Docker29.9.0 build edit; user approved stage-two latest CI effects, commit1459a1f8 pushed and MR57 updated to DevOps-891 restore python builds with GET-verified SHA/settings/body and clean checkout (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Verify recommended-tasks-generator pipeline140780 fully successful at23:55:39MSK: build3223259, Nomad lint3223109 and test3223108 all success; MR78 remains unmerged (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [x] Merge recommended-tasks-generator MR78 after explicit user approval and successful head CI: expectedSHA5899dd9e, independent GET merged/newmaster1fa2457d, other MRs untouched (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [ ] Monitor recommended-tasks-generator master pipeline140796 after approved MR78 merge; newmaster1fa2457d, created, no tag/manual deployment/job execution (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [ ] Monitor task-quality-control Docker29.9.0 correction pipeline140795/build3223277 (running, trace confirms new executor/service; test3223278 created); CI completion and cgroup correction not yet verified, no merge/deployment (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
- [ ] Investigate task-quality-control first RUN container-launch cgroup failure before pip (3223110/140781, runner105/client+DinD19.03.12); host cgroupv2 is unverified. Compatibility/runner changes and retry require separate authorization, not implemented in hash-only MRs (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-nexus-pypi-library-batch-recovery.md)
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
- [ ] Review cleaner client stale credentials/rate-limit429 separately from working gitlab CI user (2026-10-11) — [src](companies/youdo/knowledge/log/2026-10-11-nexus-fresh-recovery-plan.md)

### GitLab recovery

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

- [ ] due 2026-10-30: Prepare Git/MR training results for 2026-10-08 through 2026-10-30: proposal acceptance, user corrections, rule updates, permission/check outcomes and recommendation; review with the user before automation or extended training. Keep supervised mode until that decision (2026-10-08) — [src](companies/youdo/knowledge/systems/gitlab-ci/agent-git-workflow.md)

### youdo-chat-agent (DevOps-882)

- [x] Infrastructure and production launch completed; pipelines 140457/140458 successful. User closed DevOps scope on 2026-10-09; functional verification belongs to developers. Additional inferred operational checks and shared-template improvements were not requested and are not completion blockers — [src](companies/youdo/knowledge/log/2026-10-09-youdo-chat-agent-prod-deploy.md)

### Other systems

- [ ] dynamic_inventory: review VK migration plan, confirm SQL VM/network/stage mapping and consumers, then implement through supervised branch/publication stages; runtime and release actions need separate approvals (2026-10-13) — [src](companies/youdo/knowledge/log/2026-10-13-gitlab-ci-dynamic-inventory-vk-migration-plan.md)

- [ ] Decide whether to remove the obsolete local `~/mygit/youdo-ai` copy; optional proposal only, no deletion authorized (2026-10-12) — [src](companies/youdo/knowledge/log/2026-09-30-rp-rp-skill-consolidation.md)
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

- [ ] Monthly staleness review 2026-11: first review; offer on the first agent session in November, not necessarily November 1; refresh the due-note count with `general/scripts/build_index.py --stale 30`; wait for user agreement (rescheduled by user 2026-10-09) — [src](personal/knowledge/log/2026-10-09-knowledge-base-monthly-review-first-session.md)
- [ ] Decide whether to enforce a final note-to-TODO reconciliation check: the two-week audit found stale note lists and two untracked proposals (2026-10-12) — [src](personal/knowledge/log/2026-10-12-knowledge-base-agent-behaviour-two-week-review.md)
- [ ] Decide whether to shorten sync work summaries and exclude generated `__pycache__` files; keep audit details in task logs (2026-10-12) — [src](personal/knowledge/log/2026-10-12-knowledge-base-agent-behaviour-two-week-review.md)
- [ ] Fix `ai-sync.sh --dry-run` semantics in a separate task: existing code rebuilds indexes and changes the git index despite promising no changes; defect identified by inspection (2026-10-12) — [src](personal/knowledge/log/2026-10-12-knowledge-base-agent-behaviour-two-week-review.md)

### Token cost optimization (proposed 2026-09-23)

- [ ] due 2026-10-14: compare `personal/usage/*.txt` (the `--kb` block) with the 2026-09-30
      baseline (claude 7 days: kb_find 8, full reads 47 / 1086 KB, partial 79, search 142).
      If full reads do not drop, tighten the rule or move it into a skill (2026-09-30) — [src](personal/knowledge/log/2026-09-30-knowledge-base-token-cost-kb-find-summaries.md)

---

## Done

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

- [ ] Diagnose size-dependent packet loss on VPN tun1 toward 10.18.24.233; SSH algorithm-list restriction permits youdo login (2026-10-11) — [src](companies/youdo/knowledge/log/2026-10-11-corporate-network-ssh-10-18-24-233.md)
- [x] Complete host-specific SSH config for 10.18.24.233: user runs prepared sudo script to exclude SendEnv, then verify plain interactive login (2026-10-11) — [src](companies/youdo/knowledge/log/2026-10-11-corporate-network-ssh-10-18-24-233.md)
