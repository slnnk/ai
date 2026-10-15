---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [b2b, preflight, gitlab, nomad]
---
# DevOps-898 Billing MobileID TKB Tochka repository readiness

## Task

User requested repository-change audit of next4services after Landings: Billing,MobileID,TKB,Tochka. Read-only investigation; no build/deploy authorization. No superpowers skills used. Preserve user sequence Landings→Billing→MobileID→TKB→Tochka→Business and service-specific recreate_db behavior.

## Context

Existing repositories checked clean, branches preserved; fetched origins read-only. Delegated multiple-file reviews per user instruction. GitLab/Nomad evidence `/home/slnnk/ai-data/DevOps-898/{billing,mobile-id,tkb,tochka}-preflight.json`, checked2026-10-15 20:06UTC.

| Service | Project | Latest master/release | Pipeline | Builds |
|---|---:|---|---:|---|
| Billing |491|55fc06b/master-705|139750|2of2success|
| Mobile ID |551|e11644d/master-57|137489|1of1success|
| TKB |535|d9b7505/master-264|139748|5of5success|
| Tochka |492|551265a/master-1764|140299|5of5success|

## Actions

Reviewed current origin/master CI/build files, per-stand config, common Nomad/Ansible migration support, dynamic routing and dependencies. Queried latest master pipelines/builds/manualjobs and Nomad jobs. No HTTP/Consul/business probes or source edits.

## Findings

No mandatory repository changes identified for any of the4services. All use shared v3per-stand deployment without project-level overrides losing VK settings; latest builds successful, all target VK Nomad jobs absent. Existing pipelines predate VK template adaptation, so recommend fresh master pipelines to capture current merged templates. All4auto-mode pipelines include automatic production deployment/release; disclose and obtain action approval before creation.

- Billing: .NET8 webapp+migrations, B2B PostgreSQL/auto stand DB, recreate=true/pre+post migrations with image entrypoint, dynamic RabbitMQ/vhost. devops/config.yml4–9/18–25/31/39–42; .gitlab-ci.yml10/21–27. webEx_check=false retained; no claim of HTTP/business checks from Nomad acceptance.
- Mobile ID: web+external operator mock mobile1d/test-mno:v1.0.6 on8013, no PG/migrations. Redis/Rabbit/provider URLs/callbacks parameterized per stand/DC, supported by common external template. devops/config.yml4–17/27–33/48–50. External image pullability remains runtime prerequisite, not evidence requiring code changes.
- TKB: stand composition mock-api+worker-mock+migrations matches dev catalog. B2B PG with one DB/recreate=true; pre/post migrations use image entrypoint (config19–20). CI additionally builds production web+worker. Dynamic internal routes/Rabbit; no custom deployment adaptation required.
- Tochka:4proxy/mock web+worker workloads, two B2B databases via db_count2 and both migration sets. Base entrypoint flags (config42–43) apply correctly to secondary migration templates; ConnectionStrings overrides use intended DB and port. Dynamic Rabbit/Billing/Notifications routes, existing bank sandbox/S3 dependencies preserved. Audit uses latest master551265a; local task branch differs, so do not build/deploy that checkout as master.

Ordinary historical manual test10–test15 jobs: Billing3190653–3190658,MobileID3097251–3097256,TKB3190558–3190563,Tochka3210152–3210157. Not played; do not assume immutable old pipelines contain later template corrections.

## Changes

Read-only Git refs, local sanitized audit artifacts, existing helper --brief output option, KB records only. No repository files modified, branches switched, commits/tags/pipelines/deployments created.

## Limits

Static source checks and historical successful jobs do not guarantee fresh build/runtime or business integration success. No optional source cleanup/hardening introduced. Existing dependency credentials remain in their original source/secret locations; no values printed/copied. Open work tracked centrally in ~/ai/TODO.md.

## User-approved fresh pipelines

After automatic production/release effects disclosed, user requested "Запусти свежие пайплайны на этих 4 сервисах". Validated all4current master SHAs still matched audit before first mutation. Created exactly one pipeline per service concurrently2026-10-15 20:10:07UTC, no CI overrides/source edits:

| Service | New pipeline | IID / expected image tag | SHA |
|---|---:|---|---|
| Billing |141010|707/master-707|55fc06b|
| Mobile ID |141008|58/master-58|e11644d|
| TKB |141009|267/master-267|d9b7505|
| Tochka |141011|1767/master-1767|551265a|

Initial GET confirms all4running/refmaster/pinnedSHAs. Preparation jobs running/pending, builds/tests created, production bridges/release jobs created without downstream IDs yet. No build/test/release/production success claimed. No stand deploy jobs played. Helper `/home/slnnk/ai-data/DevOps-898/four-b2b-pipelines.py create|status`; durable per-service receipts and status in `four-b2b-builds/`. Pipeline creation approval does not authorize later stand deployment/retry.

Subsequent Mobile ID user deployment independently verified2026-10-15 20:26UTC: master-58/pipeline141008 SUCCESS, all6ordinary stand jobs3229736–3229741 SUCCESS, Nomad test10–test15 running/healthy/restarts0. Agent did not play these jobs. [Acceptance](2026-10-15-nomad-test-devops-898-mobile-id-user-rollout.md).

## Portable lesson

none
