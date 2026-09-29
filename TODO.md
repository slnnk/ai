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
- Items marked `(confirm)` were collected from old notes on 2026-09-28 and may already be
  done or no longer relevant; confirm with the user, then close or keep.

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
- [ ] RabbitMQ (sorm): move `RABBITMQ_ERLANG_COOKIE`/`DEFAULT_USER`/`DEFAULT_PASS` out of `docker-compose.yml`, rotate; cookie into a file (2026-09-22) — [src](companies/youdo/knowledge/log/2026-09-22-rabbitmq-config-migration.md)
- [ ] youdo.business `.gitlab-ci.yml` job `notify`: plaintext Basic Auth for `lenochka.youdo.sg` in the `curl -u` line; move to a masked CI variable and rotate (2026-09-28) — [src](companies/youdo/knowledge/systems/gitlab-ci/resource-groups.md)
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
- [ ] Jenkins lock keyed by the final namespace (GitLab `resource_group` is per project/ref; proven 2026-09-29: three services on task DevOps-832 deployed into `dev-devops-832` at once, Jenkins 166 failed with Helm `another operation ... is in progress`, smoke of 164/165 rejected by the ownership check) — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md)
- [ ] HTTP health smoke stage after rollout, driven by service health config — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md)
- [ ] `values.schema.json` and template regression tests for `ephemeral-namespace` and `microservice` charts; include 63-char migration Job name cases and a central name helper — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md), [src](companies/youdo/knowledge/log/2026-08-30-dev-deployment-jenkins-test-142-migration-job-name-length.md)
- [ ] Decide TTL-controller ownership or standardize GitLab `on_stop` (real `auto_stop_in` expiry verified 2026-09-14, see Done) — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md)
- [ ] Document source of truth/owner for Vault role `dev-ephemeral-deployer`; restrict `~/.kube/config-yandex-dev` permissions — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md)
- [ ] Reconcile or archive stale docs: `helm-charts/docs/agents-ephemeral-deploy-plan.md`, `helm-charts/AGENTS.md`, `helm-charts/docs/ephemeral-namespace-role.md` — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md)
- [ ] Verify `youdo-notifications` and `docvalidation` fallback and ephemeral routing independently — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md)
- [ ] Rename Jenkins pilot job `test`, update the shared CI default/variable — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md)
- [ ] Monitoring: stale `dev-*` namespaces, failed migrations, Vault secret failures, expired GitLab environments with live resources — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md)
- [ ] Operator docs: routine cleanup and recovery commands — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md)
- [ ] Jenkins root URL: set Location URL to `https://build.youdo.sg/` (or normalize in `.deploy-dev.yml` and the Jenkinsfile) (confirm) — [src](companies/youdo/knowledge/systems/dev-deployment/gitlab-ci-deploy-dev.md)
- [ ] Environment names: `CI_PIPELINE_ID` -> `CI_PIPELINE_IID`; remove old stopped GitLab Environment records (confirm) — [src](companies/youdo/knowledge/systems/dev-deployment/gitlab-ci-deploy-dev.md)
- [ ] Audit `dev.yml` files that keep `RabbitMq__Url` in global `env`; move to service-local env or a chart helper (confirm) — [src](companies/youdo/knowledge/log/2026-06-25-dev-deployment-dev-96-fns-check.md)
- [ ] Chart cleanup: Services still rendered for components with `service.enabled: false` (confirm) — [src](companies/youdo/knowledge/log/2026-06-25-dev-deployment-docvalidation-dev-yml.md)
- [ ] Helm list merge makes generated `services[]` overrides fragile; move to a separate dependencies section or a fully merged values file (confirm) — [src](companies/youdo/knowledge/log/2026-06-18-dev-deployment-ephemeral-dev-dependencies.md)
- [ ] `youdo-business-worker` OOMKilled at 256Mi on `dev-master` (confirm) — [src](companies/youdo/knowledge/log/2026-07-30-dev-deployment-dev-master-node-replacement-db-recovery.md)
- [ ] Vault `secret/dev/projects/youdo-kitcut`: add `SentryDsn` or fix the mapping (confirm) — [src](companies/youdo/knowledge/log/2026-06-17-dev-deployment-youdo-business-auth-service-jenkins-dev.md)

Deferred, decide later: developer Redis access without cluster kubeconfig; Adminer / DB discovery; `youdo-business-tickets` onboarding — [src](companies/youdo/knowledge/systems/dev-deployment/overview.md)

QA-owned, not DevOps: `ignoreFailures=true`; smoke/regress tag separation; Billing `GetYouDoBalanceHistoryTest` assertions; Tochka hard-coded token fallback — [src](companies/youdo/knowledge/log/2026-09-04-dev-deployment-devops-832-handoff.md)

### nomad-test / Consul (Yandex test)

- [ ] agent-test-01: remove dnsmasq `log-queries` or log to a separate rotated file; size-based syslog rotation; check filesystem alerts before 100% (2026-09-22) — [src](companies/youdo/knowledge/log/2026-09-22-nomad-test-agent-test-01-disk-full.md)
- [ ] Night shutdown: collect Nomad/Consul versions, job `disconnect`/`reschedule` settings, host/CSI volumes, morning recovery window, cost of the 9 client VMs (2026-09-09) — [src](companies/youdo/knowledge/log/2026-09-09-nomad-test-night-shutdown-cost.md)
- [ ] After the next agent-group power-on: 9/9 nodes ready, quorum, blocked evals -> 0, `proxy.service` DNS vs nginx upstreams, CSI and periodic jobs (2026-09-11) — [src](companies/youdo/knowledge/log/2026-09-11-nomad-test-agent-group-stop-pilot.md)
- [ ] Follow up `http-headers-viewer` port conflict, `similar-tasks/indexer` prestart failure, stale `spb2` child of `jaeger-index-cleaner`; do not scale below 7 clients without reconciling reservations (2026-09-13) — [src](companies/youdo/knowledge/log/2026-09-13-nomad-test-agent-scale-down.md)
- [ ] Resource optimization: next iteration with pooled cross-stand soft reservation and global peak hard max; monitor OOM/restarts after lowered reservations (2026-09-13) — [src](companies/youdo/knowledge/log/2026-09-13-nomad-test-resource-optimization.md), [src](companies/youdo/knowledge/log/2026-09-09-nomad-test-automation-test-yandex-nomad-memory.md)
- [ ] Hangfire lock on worker restart: tolerate `PostgreSqlDistributedLockException` at recurring-job registration, avoid old/new worker overlap (2026-09-11) — [src](companies/youdo/knowledge/log/2026-09-11-youdo-business-test14-hangfire-lock.md)
- [ ] Upgrade Nomad from `1.5.3`, fix `KillMode=process`; clean stale `/var/lib/nomad/alloc` on agent-test-02 (2026-07-21) (confirm) — [src](companies/youdo/knowledge/log/2026-07-21-nomad-test-agent-test-02-crash-loop.md)
- [ ] Consul master CPU: reduce `vmagent` Consul SD scope (~8930 services), lower `waitTime`, persistent per-process CPU telemetry (2026-06-05) (confirm) — [src](companies/youdo/knowledge/log/2026-06-05-nomad-test-master-03-cpu-unavailable.md)
- [ ] Nexus pulls: use `msk3-nexus.youdo.corp` in Nomad image refs or split-horizon DNS; disable nginx buffering for registry paths; OrientDB "No space left"; hand PMTU/MSS `172.28.0.0/24 -> 10.16.x.x` to network owner (2026-06-17) (confirm) — [src](companies/youdo/knowledge/log/2026-06-17-nexus-nomad-pull-latency.md)

### automation-services (nginx, Ansible)

- [ ] Yandex test nginx: dynamic upstream refresh for `proxy.service.yandex-test.consul` (or consul-template reload); drain procedure before removing a proxy client (2026-09-11) — [src](companies/youdo/knowledge/log/2026-09-11-automation-services-yandex-test-nginx-stale-nomad-proxy.md)
- [ ] Nexus nginx: fix client temp storage/buffering for large PUT uploads (HTTP 413/500) (2026-08-04) — [src](companies/youdo/knowledge/log/2026-08-04-android-farm-avd-template-transfer.md)
- [ ] prod_yandex GitLab runners: persist or roll back runtime-only `concurrent = 2`/`overlay2` on `10.16.24.173`; decide `docker builder prune`; review untracked host_vars in the worktree (2026-06-03) (confirm) — [src](companies/youdo/knowledge/log/2026-06-03-gitlab-ci-prod-yandex-docker-3-dind-nexus.md)
- [ ] Apply the gitlab-runner playbook to the Selectel docker3 host (2026-06-04) (confirm) — [src](companies/youdo/knowledge/log/2026-06-04-automation-services-prod-selectel-gitlab-runner-docker3-b2b.md)

### yandex-cloud / Terraform

- [ ] `yandex-tf/.gitlab-ci.yml`: `workflow:rules` for MR and default branch only (deferred by the user 2026-09-23) — [src](companies/youdo/knowledge/log/2026-09-23-yandex-cloud-yandex-tf-network-ansible-job.md)
- [ ] Ansible for `ipsec`/`balancers_test` is manual; nothing re-applies config after VM changes (2026-09-23) — [src](companies/youdo/knowledge/log/2026-09-23-yandex-cloud-yandex-tf-network-ansible-job.md)
- [ ] test-k8s: choose K8s version and upgrade chain, pin module source, fix `template_name`/default zone, re-plan; review SG egress and audit logging (2026-08-11) — [src](companies/youdo/knowledge/log/2026-08-11-yandex-cloud-yandex-tf-test-k8s-audit.md)
- [ ] K8s sizing for Nomad migration: 10-14 days of metrics, folder quotas, `maxPods`/pod CIDR, autoscaler 14-16 nodes (2026-08-11) — [src](companies/youdo/knowledge/log/2026-08-11-yandex-cloud-k8s-nomad-sizing.md)
- [ ] Temporal dev: review plan and apply in a change window; PVC backup policy; maintained PostgreSQL 16 image before prod — [src](companies/youdo/knowledge/systems/temporal.md)

### selectel

- [ ] `prod-dbaas-grants` CI apply: `-parallelism=1` or a dependency chain; retry and confirm an empty plan (2026-09-21) — [src](companies/youdo/knowledge/log/2026-09-21-selectel-tf-job-3163660-postgresql-acl-race.md)

### youdo-mcp

- [ ] Apply the port/health-check correction to production before the first prod deploy (2026-09-18) — [src](companies/youdo/knowledge/log/2026-09-18-youdo-mcp-test-nomad-healthcheck.md)
- [ ] Upload OpenIddict replacement PFX values to Vault, delete the temporary handoff directory after verification (2026-09-21) — [src](companies/youdo/knowledge/log/2026-09-21-youdo-mcp-openiddict-vault-pfx.md)
- [ ] Data Protection keys unencrypted at rest (security hardening) (2026-09-18) — [src](companies/youdo/knowledge/log/2026-09-18-youdo-mcp-test-nomad-healthcheck.md)

### ios-ci

- [ ] Check fastlane version/installation on `idcn-10`; after 2.240.0 update Gemfile.lock and drop the git pin; move lanes from Apple-ID session to App Store Connect API key (2026-09-14) — [src](companies/youdo/knowledge/log/2026-09-14-ios-ci-fastlane-spaceauth-service-key.md)
- [ ] Runner `idcn-10`: disk cleanup routine (DerivedData, Archives, stale workspaces); SwiftPM cache / Git HTTP/1.1 if GitHub HTTP/2 failures recur (confirm) — [src](companies/youdo/knowledge/log/2026-07-20-ios-ci-runner-dns-rubygems.md), [src](companies/youdo/knowledge/log/2026-08-31-ios-ci-job-3102258-github-http2-failure.md)
- [ ] Nexus consumers switch to `.ipa` URLs; check `Build development` on the macOS runner (2026-08-04) (confirm) — [src](companies/youdo/knowledge/log/2026-08-04-ios-ci-build-dev-ipa.md)

### android-farm

- [ ] Restore `/opt/adb/adb_pkg.sh` on both Appium nodes or fix the CI contract; drop `|| true` masking; reconcile `EMULATORS="emulator_1 emulator_2"` with per-host inventory; fail fast on helper/IME errors (2026-09-08) — [src](companies/youdo/knowledge/log/2026-09-08-android-farm-android-dig-job-3121092.md), [src](companies/youdo/knowledge/systems/android-farm/system-map.md)
- [ ] Samsung A55 on M-K0057: reproduce create -> quit -> create race on port `15903` before changing timeouts (2026-09-08) — [src](companies/youdo/knowledge/log/2026-09-08-android-farm-android-dig-job-3121092.md)
- [ ] Validate `FailedTestSuite.xml` download (HTTP status, XML check) before Gradle (2026-09-07) — [src](companies/youdo/knowledge/log/2026-09-07-android-farm-android-dig-job-3120554.md)
- [ ] Restore the Loki read route for the collector and Grafana (`/loki/api/v1/labels` returned 404) (2026-09-07) — [src](companies/youdo/knowledge/log/2026-09-07-android-farm-android-dig-job-3120554.md)
- [ ] Trend memory pressure on M-K0057/M-K0058 and the M-K0057 iowait spike (2026-09-07) — [src](companies/youdo/knowledge/log/2026-09-07-android-farm-android-dig-job-3120554.md)
- [ ] Appium watchdog beyond `/status`; pre-session reset for MIUI/HyperOS overlays; staged Appium 1.22.3 upgrade with a canary (2026-08-12) — [src](companies/youdo/knowledge/log/2026-08-12-android-farm-appium-147-148.md)
- [ ] Hotfix pipeline fix on `DevOps-833-fix-hotfix`: merge and verify with a real hotfix build; protected environments for store jobs; pin images by digest (2026-08) — [src](companies/youdo/knowledge/systems/android-farm/ci-cd.md)
- [ ] CI suites: `InfoMessagesTestSuite` option is broken (XML and class absent); `MindBoxTestSuite` has zero enabled tests — [src](companies/youdo/knowledge/systems/android-farm/ci-suites.md)
- [ ] M-K0056: monitor Selenium Grid on `4444` in Zabbix; check active-checks timeout to `172.24.0.107:10051` (2026-08-13) — [src](companies/youdo/knowledge/log/2026-08-13-android-farm-selenium-hub-zabbix.md)
- [ ] Host `192.168.50.17`: backup, NVMe replacement (Percentage Used 222%), kernel log alerts, reduce `emulator_1` log verbosity (2026-08-03) (confirm) — [src](companies/youdo/knowledge/log/2026-08-03-android-farm-ssh-192-168-50-17-connection-reset.md)
- [ ] android-dig: confirm `instance` label values for M-K0057/M-K0058 on the first real diagnosis (2026-08-20) — [src](companies/youdo/knowledge/log/2026-08-20-android-farm-global-skill-android-dig.md)

### Other systems

- [ ] Elasticsearch msk3-elastic-cls02: analyze heap dump `/data/data-es6/java_pid1.hprof` (sensitive, 16 GB), heap/GC alerts, plan upgrade from 6.8.23 (2026-07-31) — [src](companies/youdo/knowledge/log/2026-07-31-elasticsearch-msk3-elastic-cls02-restart.md)
- [ ] MSSQL `RecreateDBProcedures`: check backup readability before drop, `TRY/CATCH`, `sqlcmd -b` in Ansible; confirm file server `10.16.26.4` vs `172.26.0.115` (2026-08-02) (confirm) — [src](companies/youdo/knowledge/log/2026-08-02-mssql-yandex-mssql-restore-youdo.md)
- [ ] sc-except: restart policy/alert for the stopped container; MSSQL memory limits (2026-06-13) (confirm) — [src](companies/youdo/knowledge/log/2026-06-13-sc-except-mssql-unavailable.md)
- [ ] RabbitMQ (sorm): delete old Mnesia `rabbit@spb2-rabbit01*` after application-level check (2026-09-22) — [src](companies/youdo/knowledge/log/2026-09-22-rabbitmq-config-migration.md)
- [ ] pg-b2b-test `10.16.26.27`: drop/archive unused `test*` DBs, Hangfire retention (2026-06-23) (confirm) — [src](companies/youdo/knowledge/log/2026-06-23-postgresql-pg-b2b-test-10-16-26-27-data-space.md)
- [ ] sc-mta-01 postfix: correlate mass-mailing bursts, check SMTP egress/NAT limits, consider transport rate limits — [src](companies/youdo/knowledge/systems/mail/sc-mta-01-postfix.md)
- [ ] gitlab-ci Nomad canary rollback: unsafe with concurrent deployments (`nomad job promote` targets the latest one) — [src](companies/youdo/knowledge/systems/gitlab-ci/nomad-canary-rollback.md)
- [ ] youdo.business dotnet tests: lower concurrency on runner 108 or a dedicated runner; timing sections (2026-09-03) (confirm) — [src](companies/youdo/knowledge/log/2026-09-03-youdo-business-dotnet-tests-duration.md)
- [ ] Base images: LibreOffice PPA via explicit key + `signed-by`; buster archive sources for other .NET 3.1 images (2026-06-26) (confirm) — [src](companies/youdo/knowledge/log/2026-06-26-base-images-docker-libreoffice-ppa-gpg-timeout.md), [src](companies/youdo/knowledge/log/2026-06-26-base-images-dotnet-aspnet-3-1-buster-archive.md)
- [ ] team-copilot: `ANTHROPIC_BASE_URL` in `secret/dotnet/team-copilot` if needed (2026-06-11) (confirm) — [src](companies/youdo/knowledge/log/2026-06-11-team-copilot-deploy-gitlab-ci.md)
- [ ] rp: open follow-ups — Tinkoff notifications IP access (DevOps-812), iOS physical-phone task (DevOps-810) (2026-07-22) (confirm) — [src](companies/youdo/knowledge/log/2026-07-22-rp-devops-sprint-185-reports.md)

Application-side findings handed to developers, not tracked as DevOps work: geocoder
suggest HTTP 500, docvalidation passport mapping, escrow Tinkoff 502, `lead_companies`
schema drift, tracing of `YouDo.Web.MvcApplication`. See the respective logs.

---

## Personal

- [ ] Home network phase 1: TV and Lampa via Media Station X, C64 backup, device list, tunnel speed test (2026-09-26) — [src](personal/knowledge/log/2026-09-26-home-network-initial-plan.md)
- [ ] Bench tests: podkop fail-open on `ifdown tun0`, FakeIP DNS with AdGuard Home DoT upstream, VPS public IP from inside the tunnel (2026-09-26) — [src](personal/knowledge/log/2026-09-26-home-network-initial-plan.md)
- [ ] `home-infra`: choose where to host the git repo; move the router password out of the plaintext inventory once Vault is ready (2026-09-26) — [src](personal/knowledge/log/2026-09-26-home-network-initial-plan.md)

---

## Knowledge base

- [ ] Staleness review. Add `build_index.py --stale <days>` (or an INDEX section) listing
      system maps whose `checked` is older than the threshold, then review monthly: confirm,
      update, or set `status: outdated`. Include the `hypothesis` recipes in `general/`.
      (proposed 2026-09-23)
- [ ] Feed `knowledge/log/` and this file into the `rp` skill as sources for daily and
      sprint reports, next to Mattermost and YouTrack. (proposed 2026-09-23)
- [ ] Observe agent behaviour for two weeks: do daily sync commits have a non-empty
      "Work recorded by agents" section when "Files" is non-empty? Do agents add new open
      items here instead of only in notes? If not, tighten AGENTS.md or move the rule into
      a skill. (proposed 2026-09-23, extended 2026-09-28)
- [ ] `companies/youdo/.env`: there is also an empty line; remove it. (proposed 2026-09-23)
- [ ] Review the Claude per-project memory directories under `~/.claude/projects/*/memory`
      (automation-services, sorm, youdo-mcp, home) and move anything durable into `~/ai`.
      (proposed 2026-09-23)
- [ ] Read `companies/youdo/CONTEXT.md` once and correct the inferred stack and conventions.
      (proposed 2026-09-23)
- [ ] Keep `AGENTS.md` at or below about 5 KB; move anything domain-specific to
      `general/knowledge/README.md` or `CONTEXT.md`. Check quarterly. (proposed 2026-09-23)
- [ ] Decide whether to link the team skills repository `~/git/ai-skills/skills/*` into
      `companies/youdo/skills/` via symlinks. (proposed 2026-09-23)
- [ ] Walk through the `(confirm)` items above with the user. (proposed 2026-09-28)

### Token cost optimization (proposed 2026-09-23)

- [ ] AGENTS.md rule: a sequence of three or more commands run twice becomes a script in
      `scripts/`; check `scripts/` before improvising. Scripts print a compact summary,
      not raw output (`--summary`, `--quiet`).
- [ ] `general/scripts/kb_find.py <keywords>`: search the knowledge base and return only
      title, system, checked date and matching lines per note, instead of reading INDEX.md
      and whole maps. AGENTS.md rule: read long maps in parts (first 40 lines, then the
      needed section), not whole.
- [ ] Notes over ~8 KB start with a `## Summary` of 10-15 lines; `kb_lint.py` warns when a
      long note has none. Add summaries to the existing large maps (dev-deployment overview,
      gitlab-ci deploy-dev, jenkins deploy-dev-b2b, test-k8s, android system map).
- [ ] AGENTS.md rule: reading more than three files or a long log is delegated to a
      subagent that returns a few lines of conclusions.
- [ ] Mark the recommended model tier in each prompt under `general/prompts/`; use a cheaper
      model for translation, migration, frontmatter fixes and template-based recipes.
- [ ] Habit: one session per task; the knowledge base carries context between sessions.
- [ ] Output discipline in AGENTS.md: never print whole files when one line is needed
      (`head`, `grep -c`, `wc -l`, script `--quiet`).
- [ ] Measure weekly (`/cost` in Claude Code, Codex usage stats); note expensive tasks and
      why in the log.

---

## Done

- [x] `companies/youdo/.env`: renamed `ZABBIZ_DEV_TOKEN` to `ZABBIX_DEV_TOKEN` (done 2026-09-23).
- [x] dev-deployment TKB: memory fix `aa4d083` deployed (pipeline 138096, job 3120801, 2026-09-07); smoke 3120883 and regression 3120884 172/174 each, same 2 failures; peak memory not recorded (checked 2026-09-28) — [src](companies/youdo/knowledge/systems/dev-deployment/post-deploy-autotests.md)
- [x] dev-deployment: real `auto_stop_in: 7 days` expiry: `3 delete dev` 3120803 started 2026-09-14 23:24, 7 days after deploy 3120801, uninstalled release and deleted `dev-devops-832` (checked 2026-09-28) — [src](companies/youdo/knowledge/systems/dev-deployment/post-deploy-autotests.md)
- [x] DevOps-832 Tochka/TKB/Billing merged: test projects (!85, !16, !64, 01:11) with `publish-maven` + `update latests`; services !237 (01:18), !63 (01:31), !97 (01:38), master CI without pins, master pipelines green; namespace `dev-devops-832` deleted, all three environments stopped; TKB repeat deploy (Jenkins 169) done (2026-09-29) — [src](companies/youdo/knowledge/systems/dev-deployment/post-deploy-autotests.md)
- [x] dev-deployment: templates `DevOps-832-dev-autotests` merged to `master` (`12b72c9`, then `76347cd` with the suffix fix `29734d7`); test projects pushed with `DEV_HOST_SUFFIX` (tochka `d6cb806`, tkb `71ead24`, billing `b76bb67`) (done 2026-09-29)
- [x] DevOps-846 follow-ups closed by the user: concurrent case accepted as verified (test_signals), `oldest_first` not needed for now, manual prod templates need no lock, `test_signals` ref not important (done 2026-09-28) — [src](companies/youdo/knowledge/log/2026-09-28-gitlab-ci-devops-846-prod-deploy-lock-rollout.md)
- [x] DevOps-846: MR !82 and youdo.business replica jobs merged, pipeline 139705 OK (done 2026-09-28) — [src](companies/youdo/knowledge/log/2026-09-28-gitlab-ci-devops-846-prod-deploy-lock-rollout.md)
- [x] DevOps-846: linted all 23 auto-template consumers against the lock, only youdo.business affected (done 2026-09-28) — [src](companies/youdo/knowledge/systems/gitlab-ci/resource-groups.md)
- [x] Consolidated open items from all notes into this file (done 2026-09-28).
