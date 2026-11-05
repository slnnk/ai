---
system: knowledge-base
status: verified
checked: 2026-11-04
tags: [knowledge-base, staleness, monthly-review]
---
# Knowledge base: November 2026 staleness review

## Task

The user explicitly requested starting the offered monthly review. The initial
`build_index.py --stale 30` result contained 29 notes. This review reconciles
documentary evidence and available local configuration; it is not a live audit
of every server or deployment.

## Context

The 29-note candidate set and pre-existing local changes were captured before
editing. Existing VPN work and unrelated TODO changes were preserved. Read-only
review was delegated by subject as required by the KB economical-tool-use rule.
No infrastructure changes, repository code edits, manual commits or deployments
were performed. The initial sandbox failure to access agent-lint state was
resolved by repeating the authorized daily sync with filesystem access.

## Findings and changes

Each reviewed note contains a dated assessment and evidence where available.
Current configuration is distinguished from deployed runtime. Historical
observations, cancelled tasks and untested hypotheses retain their limitations;
dates are not renewed solely to remove a note from the stale list.

| Note | Resulting status | Evidence/check date | Assessment |
| --- | --- | --- | --- |
| [current/knowledge/systems/yandex-cloud/base-image.md](../systems/yandex-cloud/base-image.md) | verified | 2026-09-17 | Builder source contradicts claimed current Ubuntu22.04; preserve historical runtime date. |
| [current/knowledge/systems/yandex-cloud/terraform-prod.md](../systems/yandex-cloud/terraform-prod.md) | verified | 2026-09-17 | Source API partly confirmed; live state and old plan/apply status unresolved, preserve date. |
| [current/knowledge/systems/yandex-cloud/terraform-public-test.md](../systems/yandex-cloud/terraform-public-test.md) | verified | 2026-09-17 | Source API partly confirmed; live state and old plan/apply status unresolved, preserve date. |
| [current/knowledge/systems/yandex-cloud/terraform-network.md](../systems/yandex-cloud/terraform-network.md) | verified | 2026-09-23 | Source API partly confirmed; live state and old plan/apply status unresolved, preserve date. |
| [current/knowledge/systems/dev-deployment/gitlab-ci-deploy-dev.md](../systems/dev-deployment/gitlab-ci-deploy-dev.md) | verified | 2026-08-31 | Retain dated component/runtime evidence; remove internally contradicted unresolved claims. |
| [current/knowledge/systems/dev-deployment/jenkins-deploy-dev-b2b.md](../systems/dev-deployment/jenkins-deploy-dev-b2b.md) | verified | 2026-08-31 | Confirmed TTL drift; preserve runtime verification date. |
| [current/knowledge/systems/dev-deployment/post-deploy-autotests.md](../systems/dev-deployment/post-deploy-autotests.md) | verified | 2026-09-29 | Contract partly reconfirmed; functional/runtime risks require separate verification. |
| [current/knowledge/systems/team-config-repo.md](../systems/team-config-repo.md) | verified | 2026-11-04 | Index identity confirmed; scope explicitly local. |
| [current/knowledge/systems/sentry.md](../systems/sentry.md) | verified | 2026-10-02 | Source desired version newer than runtime note; do not misstate current deployment. |
| [current/knowledge/systems/sorm.md](../systems/sorm.md) | excluded | 2026-09-22 | Handed over; excluded under the explicit current context restriction. |
| [current/knowledge/systems/android-farm/ci-suites.md](../systems/android-farm/ci-suites.md) | verified | 2026-08-12 | Documentary reconciliation only; no fresh infrastructure or remote-revision check. |
| [current/knowledge/systems/android-farm/ci-cd.md](../systems/android-farm/ci-cd.md) | verified | 2026-08-19 | Documentary reconciliation only; no fresh infrastructure or remote-revision check. |
| [current/knowledge/systems/gitlab-ci/nomad-canary-rollback.md](../systems/gitlab-ci/nomad-canary-rollback.md) | verified | 2026-08-20 | Documentary reconciliation only; no fresh infrastructure or remote-revision check. |
| [current/knowledge/systems/gitlab-ci/android-youdo4-dynamic-runner.md](../systems/gitlab-ci/android-youdo4-dynamic-runner.md) | hypothesis | 2026-09-16 | Documentary reconciliation only; no fresh infrastructure or remote-revision check. |
| [current/knowledge/systems/gitlab-ci/resource-groups.md](../systems/gitlab-ci/resource-groups.md) | verified | 2026-09-28 | Documentary reconciliation only; no fresh infrastructure or remote-revision check. |
| [current/knowledge/systems/gitlab-ci/dynamic-kubernetes-runners.md](../systems/gitlab-ci/dynamic-kubernetes-runners.md) | hypothesis | 2026-10-10 | Documentary reconciliation only; no fresh infrastructure or remote-revision check. |
| [current/knowledge/systems/automation-services/nginx-business-youdo-routing.md](../systems/automation-services/nginx-business-youdo-routing.md) | verified | 2026-06-05 | Documentary reconciliation only; no fresh infrastructure or remote-revision check. |
| [current/knowledge/systems/automation-services/awx-collection-dependencies.md](../systems/automation-services/awx-collection-dependencies.md) | verified | 2026-09-01 | Documentary reconciliation only; no fresh infrastructure or remote-revision check. |
| [current/knowledge/systems/automation-services/local-vault-ansible-access.md](../systems/automation-services/local-vault-ansible-access.md) | verified | 2026-09-18 | Documentary reconciliation only; no fresh infrastructure or remote-revision check. |
| [current/knowledge/systems/mail/sc-mta-01-postfix.md](../systems/mail/sc-mta-01-postfix.md) | outdated | 2026-11-04 | Documentary reconciliation only; no fresh infrastructure or remote-revision check. |
| [current/knowledge/systems/workstation/apt-repositories.md](../systems/workstation/apt-repositories.md) | verified | 2026-09-08 | Documentary reconciliation only; no fresh infrastructure or remote-revision check. |
| [current/knowledge/systems/temporal.md](../systems/temporal.md) | hypothesis | 2026-09-08 | Documentary reconciliation only; no fresh infrastructure or remote-revision check. |
| [current/knowledge/systems/evaluation-service.md](../systems/evaluation-service.md) | verified | 2026-09-11 | Documentary reconciliation only; no fresh infrastructure or remote-revision check. |
| [personal/knowledge/systems/vpn-gateway.md](../../../../personal/knowledge/systems/vpn-gateway.md) | outdated | 2026-07-30 | Current verified status misleading for old gateway; new recorded SSH refusal and expired historical certificate window. Preserve checked as last actual old-gateway verification. Do not reopen user-cancelled IKEv2 testing. |
| [personal/knowledge/systems/trusttunnel-de.md](../../../../personal/knowledge/systems/trusttunnel-de.md) | verified | 2026-11-04 | Same-day recorded host checks and current local configuration corroborate current role; replace opening September-only provenance with dated review and change delivery command to modern venv. Historical StrongSwan sections already clearly superseded. |
| [personal/knowledge/systems/home-network.md](../../../../personal/knowledge/systems/home-network.md) | hypothesis | 2026-10-13 | Correct existing map drift versus its planning source without promoting unimplemented design or claiming fresh hardware/router verification. Checked remains original. |
| [general/knowledge/docker/add-apt-repository-gpg-key-timeout.md](../../../../general/knowledge/docker/add-apt-repository-gpg-key-timeout.md) | outdated | 2026-11-04 | Concrete broken executable example; mark outdated and add prominent warning above Fix, rather than silently refreshing hypothesis. Do not store company evidence in general note. |
| [general/knowledge/gitlab-ci/kubernetes-executor-scale-to-zero-node-group.md](../../../../general/knowledge/gitlab-ci/kubernetes-executor-scale-to-zero-node-group.md) | hypothesis | 2026-09-16 | Docs corroborate design primitives; operational implementation and cold start still unconfirmed. Preserve checked for untested design, soften absolute PVC claim. |
| [general/knowledge/ssh/vpn-packet-size-handshake-stall.md](../../../../general/knowledge/ssh/vpn-packet-size-handshake-stall.md) | hypothesis | 2026-10-11 | No new mechanism evidence; corporate-specific closure must stay outside portable recipe. No request to revive closed network diagnostics. |

## Status and risks

The documentary review covers all 29 candidates, including the explicit sorm
scope exclusion. Notes with insufficient evidence retain their previous dates
and hypotheses remain hypotheses. The monthly review's outstanding verification
is tracked in [the central backlog](../../../../TODO.md#knowledge-base); it is not
authorization to resume cancelled incidents or change infrastructure. The stale
list contains 24 notes after this pass: 23 retain verification limits or
untested hypotheses, plus the excluded sorm map. Two notes received supported
date renewals, and three were marked outdated. The outstanding factual rechecks
are deferred in the central backlog; no claim of full live verification is made.

## Verification

- Full `kb_lint.py`: zero errors and zero warnings after adding the required
  summary to the runner design note that crossed the size threshold.
- `git diff --check`: passed; pre-existing local edits preserved.
- All 28 in-scope notes have exactly one dated review; excluded sorm unchanged.
- `build_index.py --stale 30 --count`: 24, consistent with the five removals
  from the original 29-note candidate set.
- The follow-up renders under the Knowledge base heading in `todo.py`; its
  derived Russian title cache was refreshed. The original monthly entry is
  closed only for the completed documentary pass.
- No agent instructions, skills, resources or settings were changed.

## Portable lesson

An editorial review date does not substitute for evidence of runtime state.
