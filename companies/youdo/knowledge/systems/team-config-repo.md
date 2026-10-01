---
system: team-config-repo
status: verified
checked: 2026-09-30
indexed_commit: 3d96ec6
tags: [claude-code-config-infra, sysadmins, index, runbooks, infra-docs]
---
# Team repo claude-code-config-infra: index

## Summary

Shared Claude Code config and infra knowledge of the YouDo sysadmins team.
Clone `/home/slnnk/git/claude-code-config-infra`, origin `git@gitlab.youdo.sg:sysadmins/claude-code-config-infra.git`,
branch `main` (in this clone `origin` is the team repo). Not installed into `~/.claude` here;
read files from the clone. This note is a findability index only: open the repo file for facts.
Indexed at commit `indexed_commit` above. Refresh: `~/ai/current/scripts/team_repo_changes.sh`
lists changed files since then; update the affected rows and `indexed_commit`.

Contribution rules (what goes where, git flow): see section "Contributing". Every addition is
shown to the user first; YouDo content only.

## docs/infra (topology, live vs decommissioned)

- `docs/infra/README.md` - environment map with LIVE/DECOMMISSIONED status - Selectel ru-2 prod, YC test, spb2 (decommissioned), msk3-*, office Gate / Gate_K, test_spb2, prod_servers_ru, automation-services, DEPLOY_PROD_MODE
- `docs/infra/1c.md` - prod 1C server in YC, LUKS /data unlocked by hand after reboot, PostgresPro, backups - prod-1c, 1c.youdo.local, 10.16.24.150, usr1cv8, sysadmins/dags_adm backup_1c.py, yandex-tf compute-snapshot.tf, AP-2139
- `docs/infra/awx.md` - AWX 24.6.1 in mks-infra since 2026-08-18, old VM stopped - awx.youdo.corp, awx-prod-01, awx-test01, infra-tf modules/awx, prod/awx.tf, apply:prod, Zabbix hostid 10555
- `docs/infra/backup-cluster.md` - bare-metal backup servers, RAID, contents, route to Selectel k8s, disk ageing - msk3-backup, msk3-backup02, /backup/sql/{prod,buh,buh-server,test}, mdadm, AP-2275, AP-2298, AP-2156
- `docs/infra/ci-cd.md` - GitLab, runner topology, stuck pickup, "merge to master = prod rollout" - gitlab.youdo.sg, sc-gitlab-runner-docker-1..3, sc-gitlab-runner-ds, sc-gitlab-runner-android (172.28.0.175), gitlab-runner-*-dind*.youdo.corp, stuck_or_timeout_failure, gitlab-ci-templates, DEPLOY_PROD_MODE auto, auto_revert
- `docs/infra/compute.md` - k8s (mks-infra, YC test), Nomad prod/test, Selectel VMs, Zabbix groups, inventories - mks-infra namespaces (monitoring, loki, victoriametrics, traefik, alloy, sentry, vault, consul, n8n, keycloak, kafka-ui), kube-test-temp, sc-hashi-selectel-master-01..03, sc-hashi-dc1-master-01..03, nomad-consul-master-test-01..03, nomad-agent-test-*, sc-mta-01..03, prod_selectel inventory
- `docs/infra/data.md` - Selectel DBaaS PG/Redis, MSSQL, Vertica, ClickHouse, Elasticsearch, RabbitMQ, Kafka - prod-cluster-c2c, prod-cluster-b2b, clickhouse.service.data.consul, youdo_cluster, msk3-rabbit-cls01..03, rabbit-cls.youdo.local, sc-rabbit01, msk3-verticaNN, AppMetrica
- `docs/infra/monitoring.md` - Grafana prod/test and FreeIPA role map, Loki, VictoriaMetrics, Mimir, Tempo, Zabbix, SLO - grafana.youdo.corp, grafana.infra.youdo.corp, grafana.yandex-test.youdo.local, loki.infra.youdo.corp, tempo-otlp.infra.youdo.corp, tempo-jaeger.infra.youdo.corp, traces.youdo.com, msk3-kibana.youdo.local
- `docs/infra/networking.md` - subnets per DC, IPsec/GRE mesh YC-Selectel-KZ, OpenVPN, RKN-bypass VPN, DNS suffixes - ipsec-vm, ipsec-kz, sc-gateway2, ne1260 (FortiGate), gate-vm-prod, vpn-kz, vpn-office, 172.31.0.0/16
- `docs/infra/office.md` - Moscow MikroTik Gate, VLANs, srv0-2, Kazan site with Android/Appium stands - Gate, Gate_K, srv0/srv1/srv2, jenkins-0, android-sel-hub, 192.168.30.30 grid, appium-1/2, 192.168.30.0/24, AP-2268, AP-2140
- `docs/infra/repositories.md` - how to find the repo behind a component, key sysadmins/* repos - sysadmins/terraform, sysadmins/ansible, devops-tools/{gitlab-ci-templates,k8s-manifests,nomad-jobs}, meta.GITLAB_PROJECT, meta.COMPONENT_TAG
- `docs/infra/sentry.md` - self-hosted Sentry 25.9.0 (prod helm on mks-infra, test compose on YC), retention, Celery to taskworker - sentry-sentry-cleanup, nodestore_node vacuum cronjob, kube-test, AP-2199, AP-2270
- `docs/infra/sql-report.md` - Windows VM in YC with SSRS 2016, DataLens migration context - sql-report.youdo.local, 10.16.24.21, SSRS_Login, AP-2323

## docs/operations (runbooks)

- `docs/operations/README.md` - runbook index, ansible secrets conventions
- `docs/operations/airflow.md` - DAG delivery git -> S3 -> cron syncdags, inspect runs - data/airflow, /opt/airflow/dags, /etc/cron.d/syncdags, dag_bag2_bi, dag_bag3_int
- `docs/operations/ansible-runbook.md` - ansible run order (cwd, env, check, apply), host_vars naming, Vault secrets in group_vars - automation-services, selectel-tf/prod, sc-mta-03
- `docs/operations/awx.md` - AWX content, EE, k8s pitfalls after move - quay.io/ansible/awx-ee:24.6.1, base_linux, ssh_lockdown
- `docs/operations/clickhouse-system-logs.md` - TTL on system.*_log via config.d without renamed copies - youdo_cluster, trace_log, text_log
- `docs/operations/consul-alerts-mute.md` - mute node/check in consul-alerts before maintenance - consul-alerts/checks/, blacklist/services, #alert-infra
- `docs/operations/dashboard-migration.md` - Tableau/SSRS to DataLens playbook - ReportServer ExecutionLog3, twb
- `docs/operations/datalens.md` - self-hosted DataLens in mks-infra, API object creation - namespace datalens, datalens.infra.youdo.corp
- `docs/operations/discovery-checklist.md` - periodic commands to keep the infra map current
- `docs/operations/dns-client-linux.md` - systemd-resolved traps with .local and routing domains - resolvectl, ~local, youdo.local
- `docs/operations/dns.md` - public DNS via sysadmins/dns and octoDNS - youdo.com, youdo.sg, deploy_selectel, deploy_nic_ru
- `docs/operations/dns-rpz.md` - RPZ routing of AI/GitHub/Telegram domains via KZ - rpzctl, nft-dnat-sync, bind:rpz, break-dnssec, ipsec-vm, sc-gateway2
- `docs/operations/host-access.md` - finding and reaching hosts by subnet/site, Consul, Zabbix - 172.28.x Selectel, 172.24.x msk3, 10.16.x YC, *.service.consul
- `docs/operations/kz-fortigate-tunnel.md` - FortiGate-KZ GRE-over-IPsec for raw-IP egress - ne1260, to_kz, kz-gre, gre_scgw, AP-2236
- `docs/operations/logreader.md` - prod .NET exceptions pipeline - sc-except01:9900, YouDoLogsExceptions, StackExchange.Exceptional
- `docs/operations/mikrotik-tunnels.md` - office MikroTik IPsec/GRE spokes, failure modes - Gate, Gate_K, ipsec-kz, sysadmins/runbooks
- `docs/operations/rabbitmq-clients-no-recovery.md` - apps without AMQP auto-recovery, need nomad alloc restart - mailer-dispatcher, socketChat, youdo-business-{api,internal-api,tkb-proxy,tochka-proxy}, auth-service, mobile-id, notifications
- `docs/operations/rabbitmq-cluster-drain.md` - draining RabbitMQ 3.8 nodes, pause_minority pitfalls - stop_app, forget_cluster_node, min-masters
- `docs/operations/sp-log-collector.md` - Servicepipe raw-log collector in mks-infra, key rotation - namespace monitoring, VaultStaticSecret, SERVICEPIPE_API_TOKEN
- `docs/operations/terraform.md` - infra-tf flow validate/plan/apply:prod, import, branch must be current - infra-tf, merge-base check
- `docs/operations/vault.md` - Vault access, VSO model for mks-infra - VaultStaticSecret, VaultAuth, <ns>-read, secret/admin/gitlab-registry, vault.service.consul:8200
- `docs/operations/vertica.md` - querying Vertica, mart copy to ClickHouse - msk3-verticaNN, vsql, DBADMIN_PASS
- `docs/operations/youtrack-scheduled-workflows.md` - server-side YouTrack workflows for recurring tickets - youdo-servicepipePaymentMonthly, AP-2210
- `docs/operations/zabbix-monitoring.md` - network device monitoring via Zabbix API, alert naming, channel map - zabbix-selectel.youdo.local, #alert-infra, #alert-infra-test, #alert-helpdesk, #alert-c2c

## docs/api (API references)

alertmanager (vmalertmanager.infra.youdo.corp), appmetrica (Vault secret/ds/extraform), firecrawl, freeipa (ipa6.youdo.corp, arecord gotcha), gitlab (glab, MR description gotchas), grafana (datasource proxy), loop (Mattermost v4 fork), n8n, oncall (Grafana OnCall), selectel (Keystone/IAM, VPC, dedicated), servicepipe, yandex-cloud (read-only profile claude-reader, yc-approved.sh), youtrack, zabbix (JSON-RPC, maintenance). Path: `docs/api/<name>.md`.

## docs/lessons-learned (incidents)

backup-silent-empty-dumps (AP-2298, msk3-backup), branch-switch-breaks-live-config, clickhouse-replacing-version-column (AP-2279), clickhouse-system-log-ttl-outage (AP-2271), dpi-tls-filter-localization (AP-2291), hooks-read-wrong-payload-key, html-scrape-status-gating, live-system-debugging-discipline, n8n-pipeline-debugging-lessons, nomad-template-unknown-function (AP-2283, youdo-antibot), review-gate-not-a-rule (AP-2300, Sentry), test-grafana-spb2-misidentification, vault-agent-injector-race (AP-2250), zabbix-oncall-loop-pipeline (sc-zabbix-01). Path: `docs/lessons-learned/<name>.md`.

## docs/adr, skills

- ADR: 0001 Cursor shares canonical skills; 0002 .env resolves via ~/.claude.
- Skills (`skills/<name>/SKILL.md`): ansible-diff-digest, ansible-dynamic-inventory (sc-mta-03, postfix tags), context-budget, debug-n8n, logreader, loop-ai, loop-alerts, loop-post, mssql-monitoring (c2c/b2b, listyoudo.youdo.local), orchestrator-workflow, plan-diagram, pr, rc-loop, refactor-workflow, rpz-domain, selectel-dedicated, selectel-tickets, servicepipe-operations, systematic-debugging, task-review, yandex-cloud-inventory, youtrack-backlog (AP project, agiles/87-98).
- `.env.example`: variable names for GitLab, YouTrack, Loop, Grafana/Loki/VM/Mimir/Tempo, Sentry, Zabbix, Consul/Nomad, k8s, Vault, Selectel, Servicepipe, MSSQL, PG DBaaS, Vertica, n8n, YC, FreeIPA/WinRM, Jenkins YC, MikroTik, Firecrawl, Tableau.

## Known discrepancies (as of indexed_commit)

Candidates for a team-repo fix; propose to the user, do not change silently.

- Test k8s: repo (`compute.md`, `infra/README.md`, yandex-cloud-inventory skill) calls kube-test-temp live; local `systems/yandex-cloud/terraform-test-k8s.md` (2026-09-30) says it is gone and kube-test is live. `sentry.md`, `awx.md` already use kube-test.
- YC test Nomad agents: repo says 10 (verified 2026-06-10); local log 2026-09-13 scaled down.
- Old AWX VM awx-prod-01: repo says stopped with one-command rollback; local `systems/yandex-cloud/terraform-prod.md` plans its removal.
- Test Loki moved to loki.dev.youdo.corp (local android-farm map); repo documents only prod Loki.
- Repo internal: README counts of skills/hooks/docs are stale; `docs/rules/workflow.md` mixes master (infra repos) and main (this repo); README says Android stands "moving" to Kazan, `office.md` says "moved"; SQL_REPORT_*, LOOP_BOT_TOKEN, LOOP_CHANNEL_ID, LOOP_BOT_USER_ID missing from `.env.example`.

## Contributing

- Placement per `docs/operating-model.md` "Capture protocol": topology to `docs/infra/`, runbook to `docs/operations/`, API to `docs/api/`, incident to `docs/lessons-learned/` + README row, decision to `docs/adr/`; update the matching index (`docs/infra/README.md`, `docs/operations/README.md`, `docs/README.md`, CLAUDE.md knowledge map).
- Style (`docs/rules/agent-output.md`): only short dash `-`, no Unicode arrows in prose, identifiers plain text; hook guard-typography checks `.md`.
- Git (`docs/rules/workflow.md`): branch `<TICKET>-slug` or `<area>/slug` from fresh origin/main in a separate worktree; `git fetch` and check behind-count before push and MR; MR description empty (or `Close <TICKET>`); commit without Co-Authored-By footer, detailed body allowed in this repo; corporate git identity.
- Never personal projects; show the diff to the user and wait for approval before commit and push.
