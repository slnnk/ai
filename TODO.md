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

- [ ] agent-test-01: remove dnsmasq `log-queries` or log to a separate rotated file; size-based syslog rotation; check filesystem alerts before 100% (2026-09-22) — [src](companies/youdo/knowledge/log/2026-09-22-nomad-test-agent-test-01-disk-full.md)
- [ ] Night shutdown: collect Nomad/Consul versions, job `disconnect`/`reschedule` settings, host/CSI volumes, morning recovery window, cost of the 9 client VMs (2026-09-09) — [src](companies/youdo/knowledge/log/2026-09-09-nomad-test-night-shutdown-cost.md)
- [ ] After the next agent-group power-on: 9/9 nodes ready, quorum, blocked evals -> 0, `proxy.service` DNS vs nginx upstreams, CSI and periodic jobs (2026-09-11) — [src](companies/youdo/knowledge/log/2026-09-11-nomad-test-agent-group-stop-pilot.md)
- [ ] Follow up `http-headers-viewer` port conflict, `similar-tasks/indexer` prestart failure, stale `spb2` child of `jaeger-index-cleaner`; do not scale below 7 clients without reconciling reservations (2026-09-13) — [src](companies/youdo/knowledge/log/2026-09-13-nomad-test-agent-scale-down.md)
- [ ] Resource optimization: next iteration with pooled cross-stand soft reservation and global peak hard max; monitor OOM/restarts after lowered reservations (2026-09-13) — [src](companies/youdo/knowledge/log/2026-09-13-nomad-test-resource-optimization.md), [src](companies/youdo/knowledge/log/2026-09-09-nomad-test-automation-test-yandex-nomad-memory.md)
- [ ] Upgrade Nomad from `1.5.3` (all 7 clients and 3 servers on Yandex test, API 2026-09-30), fix `KillMode=process` (still in `automation-test-yandex` `deprecated/roles/nomad-client/templates/nomad.systemd.j2:10`); clean stale `/var/lib/nomad/alloc` on agent-test-02 (2026-07-21) — [src](companies/youdo/knowledge/log/2026-07-21-nomad-test-agent-test-02-crash-loop.md)

### automation-services (nginx, Ansible)

- [ ] Yandex test nginx: dynamic upstream refresh for `proxy.service.yandex-test.consul` (or consul-template reload); drain procedure before removing a proxy client (2026-09-11) — [src](companies/youdo/knowledge/log/2026-09-11-automation-services-yandex-test-nginx-stale-nomad-proxy.md)
- [ ] Nexus nginx: fix client temp storage/buffering for large PUT uploads (HTTP 413/500) (2026-08-04) — [src](companies/youdo/knowledge/log/2026-08-04-android-farm-avd-template-transfer.md)
- [ ] prod_yandex GitLab runners: persist or roll back runtime-only `concurrent = 2`/`overlay2` on `10.16.24.173`; decide `docker builder prune`; review untracked host_vars in the worktree (2026-06-03); kept by the user 2026-09-30: runner host_vars moved to `deprecated/` in automation-services (AP-2228, `d3d6133c`), `10.16.24.173`/`concurrent = 2` not in the repo — [src](companies/youdo/knowledge/log/2026-06-03-gitlab-ci-prod-yandex-docker-3-dind-nexus.md)
- [ ] Apply the gitlab-runner playbook to the Selectel docker3 host (2026-06-04); kept by the user 2026-09-30: vars now in `deprecated/inventories/prod_selectel/host_vars/gitlab-runner-docker-3.yml` (`d13d56fd`), live host `gitlab-runner-dind03` — [src](companies/youdo/knowledge/log/2026-06-04-automation-services-prod-selectel-gitlab-runner-docker3-b2b.md)

### yandex-cloud / Terraform

- [ ] `yandex-tf/.gitlab-ci.yml`: `workflow:rules` for MR and default branch only (deferred by the user 2026-09-23) — [src](companies/youdo/knowledge/log/2026-09-23-yandex-cloud-yandex-tf-network-ansible-job.md)
- [ ] Ansible for `ipsec`/`balancers_test` is manual; nothing re-applies config after VM changes (2026-09-23) — [src](companies/youdo/knowledge/log/2026-09-23-yandex-cloud-yandex-tf-network-ansible-job.md)
- [ ] test-k8s: choose K8s version and upgrade chain, pin module source, fix `template_name`/default zone, re-plan; review SG egress and audit logging (2026-08-11) — [src](companies/youdo/knowledge/log/2026-08-11-yandex-cloud-yandex-tf-test-k8s-audit.md)
- [ ] K8s sizing for Nomad migration: 10-14 days of metrics, folder quotas, `maxPods`/pod CIDR, autoscaler 14-16 nodes (2026-08-11) — [src](companies/youdo/knowledge/log/2026-08-11-yandex-cloud-k8s-nomad-sizing.md)
- [ ] Temporal dev: review plan and apply in a change window; PVC backup policy; maintained PostgreSQL 16 image before prod — [src](companies/youdo/knowledge/systems/temporal.md)

### selectel

- [ ] `prod-dbaas-grants` CI apply: `-parallelism=1` or a dependency chain; retry and confirm an empty plan (2026-09-21) — [src](companies/youdo/knowledge/log/2026-09-21-selectel-tf-job-3163660-postgresql-acl-race.md)

### ios-ci

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

### web-autotests (Jenkins `Web+API Tests`, Selenium Grid k8s-dev)

- [ ] Wait for QA feedback on web autotests after `scalingType: deployment`; for a fair wall-time comparison with Selenoid run regress part 1 from `master` on `test7` (2026-10-01) — [src](companies/youdo/knowledge/log/2026-10-01-web-autotests-selenium-keda-polling-interval-effect.md)
- [ ] Selenium Grid deployment mode: during the next regress runs (only then do chrome pods exist; none on 2026-10-01, no tests running) watch scale-down of busy node pods and browser state leaks across sessions (2026-10-01) — [src](companies/youdo/knowledge/log/2026-10-01-web-autotests-selenium-keda-polling-interval-effect.md)
- [ ] Regress 108 vs 94 min (three/1622 vs Selenoid two/1978): stands currently have problems with SBR (safe deal) and insurance (reported to the user 2026-10-01), likely part of the gap; re-measure after the stands are fixed, and only if a gap remains check Chrome pod CPU throttling in VictoriaMetrics (`container_cpu_cfs_throttled_periods_total` / `container_cpu_cfs_periods_total`, pods `selenium-node-chrome`); image pre-pull is moot in deployment mode (2026-10-01) — [src](companies/youdo/knowledge/log/2026-09-30-web-autotests-selenium-grid-k8s-slow-regress.md)

### Agent Git/MR training

- [ ] due 2026-10-30: Prepare Git/MR training results for 2026-10-08 through 2026-10-30: proposal acceptance, user corrections, rule updates, permission/check outcomes and recommendation; review with the user before automation or extended training. Keep supervised mode until that decision (2026-10-08) — [src](companies/youdo/knowledge/systems/gitlab-ci/agent-git-workflow.md)

### Other systems

- [ ] Elasticsearch msk3-elastic-cls02: analyze heap dump `/data/data-es6/java_pid1.hprof` (sensitive, 16 GB), heap/GC alerts, plan upgrade from 6.8.23 (2026-07-31) — [src](companies/youdo/knowledge/log/2026-07-31-elasticsearch-msk3-elastic-cls02-restart.md)
- [ ] sc-mta-01 postfix: correlate mass-mailing bursts, check SMTP egress/NAT limits, consider transport rate limits — [src](companies/youdo/knowledge/systems/mail/sc-mta-01-postfix.md)
- [ ] gitlab-ci Nomad canary rollback: unsafe with concurrent deployments (`nomad job promote` targets the latest one) — [src](companies/youdo/knowledge/systems/gitlab-ci/nomad-canary-rollback.md)
- [ ] youdo.business dotnet tests: xUnit already capped (`79254cc49`, `maxParallelThreads: 4`); remaining: dedicated runner or lower concurrency for `dotnet-unit-tests`, `section_start` timing sections (checked 2026-09-30) — [src](companies/youdo/knowledge/log/2026-09-03-youdo-business-dotnet-tests-duration.md)
- [ ] Base images: LibreOffice PPA still via plain `add-apt-repository` (3 images), move to explicit key + `signed-by`; buster archive sources only in `dotnet-core-aspnet/3.1`, missing in other 3.1 images; `3.1-gdilibs`/`3.1-libvips*` still use `apt-key adv` (checked 2026-09-30) — [src](companies/youdo/knowledge/log/2026-06-26-base-images-docker-libreoffice-ppa-gpg-timeout.md), [src](companies/youdo/knowledge/log/2026-06-26-base-images-dotnet-aspnet-3-1-buster-archive.md)

Application-side findings handed to developers, not tracked as DevOps work: geocoder
suggest HTTP 500, docvalidation passport mapping, escrow Tinkoff 502, `lead_companies`
schema drift, tracing of `YouDo.Web.MvcApplication`, youdo-mcp Data Protection keys
stored unencrypted in `data_protection_keys` (no `ProtectKeysWith*`). See the respective logs.

---

## Personal

- [ ] Home network phase 1: TV and Lampa via Media Station X, C64 backup, device list, tunnel speed test (2026-09-26) — [src](personal/knowledge/log/2026-09-26-home-network-initial-plan.md)
- [ ] Bench tests: podkop fail-open on `ifdown tun0`, FakeIP DNS with AdGuard Home DoT upstream, VPS public IP from inside the tunnel (2026-09-26) — [src](personal/knowledge/log/2026-09-26-home-network-initial-plan.md)
- [ ] `home-infra`: choose where to host the git repo; move the router password out of the plaintext inventory once Vault is ready (2026-09-26) — [src](personal/knowledge/log/2026-09-26-home-network-initial-plan.md)

---

## Knowledge base

- [ ] Monthly staleness review 2026-10: 15 notes due; list with `general/scripts/build_index.py --stale 30`; per note confirm, fix or set `status: outdated`, bump `checked`; offer to the user, do not run unasked (2026-10-01)
- [ ] due 2026-10-12: Observe agent behaviour for two weeks (from 2026-09-28): do daily sync commits have a non-empty
      "Work recorded by agents" section when "Files" is non-empty? Do agents add new open
      items here instead of only in notes? If not, tighten AGENTS.md or move the rule into
      a skill. (proposed 2026-09-23, extended 2026-09-28)

### Token cost optimization (proposed 2026-09-23)

- [ ] due 2026-10-14: compare `personal/usage/*.txt` (the `--kb` block) with the 2026-09-30
      baseline (claude 7 days: kb_find 8, full reads 47 / 1086 KB, partial 79, search 142).
      If full reads do not drop, tighten the rule or move it into a skill (2026-09-30) — [src](personal/knowledge/log/2026-09-30-knowledge-base-token-cost-kb-find-summaries.md)

---

## Done

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
