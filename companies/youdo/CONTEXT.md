# YouDo: working context

Read at the start of every task. Update when the stack or priorities change.

## Role and priorities

DevOps engineer. In system maps and long-lived notes prioritize infrastructure and CI/CD:
runners, build images, registries, artifacts, secret stores, pipelines and jobs, launch,
publish and deploy rules, environments, network dependencies, monitoring, logs, operations
and recovery. Describe product architecture only where it affects build, delivery, launch
and diagnostics.

## Stack (derived from existing notes, verify on first contact)

- Source and CI: GitLab (pipelines, dynamic Kubernetes runners, CI templates repo), Jenkins
  (legacy pipelines, dev deployments).
- Runtime: Nomad + Consul (test and prod clusters), Kubernetes (dev, Yandex Managed K8s),
  Helm charts repo for dev environments.
- Cloud and hosting: Yandex Cloud (Terraform), Selectel (Terraform), on-prem hosts in the
  corporate network.
- Config management: Ansible, AWX, Vault for secrets.
- Registries: Nexus (`msk3-nexus.youdo.corp`), container registry `registry.youdo.sg`.
- Observability: Zabbix, Loki with Alloy agents, Elasticsearch.
- Product: .NET services and base images, MSSQL and PostgreSQL, iOS and Android apps.
- Test infrastructure: Android device farm (Selenium Grid, Appium, ADB, emulators and
  physical devices), iOS runners with fastlane, autotest repositories per product.
- Tracking and chat: YouTrack (tickets like `DEVOPS-832`), Mattermost.

## Conventions

- Environment names carry meaning: `prod`/`production` is sensitive, `test` and `dev`
  are shared stands. Treat anything named prod as change-controlled.
- Company skills live in `~/ai/current/skills/`: `rp` (daily and sprint reports from
  Mattermost and YouTrack), `android-dig` (Android CI infrastructure diagnosis). Team
  skills repository: `~/git/ai-skills`.
- Secrets for tooling are in `~/ai/current/.env` (GitLab, YouTrack, Jenkins, Nomad,
  Consul, Zabbix tokens). Never copy values elsewhere.
- Android farm maps follow the extended template in `general/knowledge/README.md`.

## Where to look first

- `knowledge/INDEX.md`, then `knowledge/systems/<system>.md`.
- `knowledge/repos.md` for local clones under `~/git` and `~/mygit`.
