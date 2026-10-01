# YouDo: working context

Read at the start of every task. Update when the stack or priorities change.

## Role and priorities

DevOps engineer. In system maps and long-lived notes prioritize infrastructure and CI/CD:
runners, build images, registries, artifacts, secret stores, pipelines and jobs, launch,
publish and deploy rules, environments, network dependencies, monitoring, logs, operations
and recovery. Describe product architecture only where it affects build, delivery, launch
and diagnostics.

## Stack (reviewed with the user 2026-09-30)

- Source and CI: GitLab (pipelines, dynamic Kubernetes runners, CI templates repo). Jenkins
  is active only for test and dev stands: deploys to Nomad test stands, web autotest runs,
  and the ephemeral dev deploy to Kubernetes (job `test`, DevOps-832).
- Runtime: Nomad + Consul for test stands and prod; Kubernetes (Yandex Managed K8s) for
  ephemeral dev environments, with the Helm charts repo. Direction: dev environments replace
  the Nomad test stands, then services migrate from Nomad to Kubernetes.
- Cloud and hosting: Yandex Cloud (Terraform), Selectel (Terraform, DBaaS), on-prem hosts
  in the corporate network.
- Config management: Ansible, AWX (`awx-ee` execution image), Vault for secrets.
- Registries and storage: Nexus (`msk3-nexus.youdo.corp`), container registry
  `registry.youdo.sg`, Yandex Object Storage for reports and artifacts.
- Observability: Zabbix; VictoriaMetrics with vmagent and Grafana; Loki with Alloy agents
  (Loki runs in the dev cluster, `loki.dev.youdo.corp`); Sentry; Jaeger tracing;
  Elasticsearch.
- Product: .NET services and base images; MSSQL and PostgreSQL; RabbitMQ, Redis, Hangfire
  (on PostgreSQL); Temporal (dev, in progress); iOS and Android apps.
- Test infrastructure: Android device farm (Selenium Grid, Appium, ADB, emulators and
  physical devices), iOS runners with fastlane, autotest repositories per product.
- Tracking and chat: YouTrack (DevOps tickets `DevOps-832`, product tickets like
  `Site-24856`, knowledge-base articles `DevOps-A-50`), Mattermost.

## Out of scope

- sorm (incl. its RabbitMQ) is handed over to another engineer (2026-09-30). Do not work on
  it without the user's explicit request.

## Conventions

- Environment names carry meaning: `prod`/`production` is sensitive, `test` and `dev`
  are shared stands. Treat anything named prod as change-controlled.
- Company skills live in `~/ai/current/skills/`: `rp` (daily and sprint reports from
  Mattermost and YouTrack), `android-dig` (Android CI infrastructure diagnosis).
- Secrets for tooling are in `~/ai/current/.env` (GitLab, YouTrack, Jenkins, Nomad,
  Consul, Zabbix tokens). Never copy values elsewhere.
- Android farm maps follow the extended template in `general/knowledge/README.md`.

## Where to look first

- `knowledge/INDEX.md`, then `knowledge/systems/<system>.md`.
- `knowledge/repos.md` for local clones under `~/git` and `~/mygit`.
