---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [b2b, planning, nomad]
---
# B2B test10-test15 deployment planning

## Task

Prepare an action plan for deploying the services used by B2B dev deployment to test10–test15 under DevOps-898. User explicitly excluded superpowers skills. Planning only; no runtime changes authorized. User subsequently clarified that youdo-sms-service, docvalidation and fns are also required on C2C stands.

## Context

Existing maps: [dev deployment](../systems/dev-deployment/overview.md), [Nomad test](../systems/nomad-test.md). Local repository and dated KB inspection; no live runtime inventory in this task.

## Actions

Ran ai-sync.sh (no reminder output), read company context/backlog, searched KB with kb_find.py, and inspected Jenkins catalog plus relevant CI/Ansible configuration. Delegated long/multiple-file reads as required by global instructions. No superpowers skills used.

## Findings

- Jenkins loads `jenkins-pipelines/config/deploy-dev-b2b.groovy`, matching local `origin/master`: 13 services. Neighboring YAML has 16 but is not loaded.
- Catalog: youdo-business, youdo-business-auth-service, youdo-business-billing-service, youdo-business-doc-generator, youdo-business-landings, youdo-business-mobile-id, youdo-business-tkb-proxy, youdo-business-tochka-proxy, youdo-kitcut, youdo-notifications, youdo-sms-service, docvalidation, fns. Tickets/Sber/CryptoPro are outside this catalog.
- Catalog dependencies describe selection/routing; business and docvalidation have reciprocal dependencies. They do not define a valid startup order.
- `youdo.business/.gitlab-ci.yml:278` calls `automation-test-yandex/playbooks/deploy/docker/youdo_business.yml`; its tasks stop/purge the stand job and recreate main/mock databases (dropdb tags). Normal CI invocation has no skip-tags. Data policy and explicit runtime authorization must precede execution.
- Correction after user feedback: doc-generator was already deployed under DevOps-898 as a shared service, image master-137, GitLab deployment job3226189/pipeline140895, passing Consul and HTTP200. Reuse and verify the shared endpoint from the target stands. Its disabled per-stand deployment is intentional existing topology, not a blocker requiring six instances. Evidence: [DevOps-898 implementation](2026-10-14-nomad-test-devops-898-implementation.md).
- Dated platform evidence: ES/MSSQL were deployed for test10–test15, FeatureToggle DBs cloned from test5, Cerberus accepted. BuildAPI catalog entries alone do not prove service runtime. Current B2B pool capacity and every stand route remain preflight checks.

Proposed sequence: inventory service/ref/image/workloads/DB/vhost/routes for six stands; determine DB/seed policy and minimal required CI changes; validate configuration and image availability; deploy test10 pilot by dependency groups; verify migrations/health/integration; deploy identical versions to test11–test15 with concurrency based on measured capacity; record all six outcomes and rollback refs. Migrations need their own recovery path because image rollback cannot reverse schema changes.

Scope correction: continue all work under DevOps-898. Reuse shared doc-generator rather than adding per-stand instances. Deploy/verify SMS, DocValidation and Fns on both B2B test10–test15 and active C2C stands (working scope test/test1–test7; test8/test9 previously excluded). SMS already has accepted C2C deployment evidence, so inspect versions/health before proposing a repeat deployment. B2B database pool selection remains service-specific even when the consumer stand is C2C.

## Changes

Order correction after initial5stand-service completions and shared doc-generator acceptance: user explicitly selected Kitcut → Landings → Billing → MobileID → TKB → Tochka → Business. Supersedes previous next-Business proposal. External actions still need per-action authorization.

KB planning record and links only. No repository edits, git mutations, CI launches, infrastructure changes, or external API writes.

## Limits

The plan is not deployment acceptance or authorization. Repository adaptations require supervised branch approval; runtime changes require explicit approval. Detailed task tracking is in ~/ai/TODO.md.

## Portable lesson

none
