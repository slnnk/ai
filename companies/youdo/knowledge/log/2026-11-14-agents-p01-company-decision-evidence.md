---
system: agents
status: verified
checked: 2026-11-14
tags: [agents, learning, evaluation]
---
# P0.1: company decision evidence and calibration

## Task and boundaries

Source excerpts for [P0.1 case design](../../../../personal/knowledge/log/2026-11-14-agents-p01-decision-cases-metrics.md).
Read-only documentary preparation; no current runtime verification, task reopening,
repository modification or external operation. Dates below belong to source events.

## C01: unnecessary tool acquisition

[Primary task section](2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md#before_script-simplified-to-git-clone-script-simplification-discussed).
DevOps-918 required a reusable GitLab Helm deployment. Initial CI implementation
added yq download/checksum/PATH and API archive retrieval after inspecting only custom
Dockerfile additions. User rejected that approach and requested git clone. Actual
cached kubectl1.35.6 image history showed git and yq already installed. Commit723ea3b
replaced the before_script with shallow clone of DEV_HELM_CHARTS_REF using CI_JOB_TOKEN.
Consumer CI lint was valid with0errors/warnings; this was not runtime acceptance.

[Existing rule evidence](../../../../personal/knowledge/log/2026-11-12-agents-agent-learning-record-simplest-sufficient-solution-4cedeecedfca84d648d0.md)
records fail, rule_loaded=yes, event devops-918-simplicity-first-attempt.
Do not add a second occurrence/evaluation for this case. Observable inspection gap
is base-image inheritance; hidden reasoning is unknown. Recovery does not erase failure.

## C02: dependency caused by a credential assumption

[Comparison](2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md#jenkins-deployment-comparison-from-local-code-and-refreshed-originmaster)
and [explicit user decision](2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md#user-selected-standard-dev-postgresql-credentials).
The ai-qa PostgreSQL pre-install hook required a Vault-derived Secret; ordinary
application VSO resources would only exist in the normal Helm phase. Extra bootstrap
logic was therefore necessary under that credential requirement. Other inspected
dev services used chart defaults without the same ordering conflict.

User explicitly selected that standard mechanism for ai-qa dev. Values then removed
database.passwordSecretRef and its Vault PG mapping, and used defaults.postgres.password.
Shared template82e4ad9 dropped app VSO precreation/ownership/readiness machinery and
retained ordinary namespace/app Helm upgrades and PG rollout; source reports15lines.
Rendered app/PG passwords agreed without printing them; CI lint passed. No live DB
change follows from this source subsection. This is scoped ai-qa dev behavior, not
a global secret-policy exception. The assumption should have been surfaced earlier,
but a silent credential substitution would have violated the task boundary.
C01/C02 belong to the same parent; no independent task-success count is inferred.

## C04: comment steering is not proof of repeated formatting violation

[Correction](2026-11-12-android-farm-devops-921-apk-http-errors.md#comment-format-correction-and-mr-field--2026-11-12)
and [verified publication](2026-11-12-android-farm-devops-921-apk-http-errors.md#approved-comment-and-mr-field-publication--2026-11-12).
Original DevOps-921 summary included local checks and an MR sentence. User removed
the checks and requested MR2926 in the dedicated field. Exact concise comment and
field change were approved before publication; GET readback verified both.
Existing first-draft review fail remains historical. This correction introduced the
issue-specific format: no earlier identical applicable formatting rule is evidenced.
Classify substantial steering separately from a repeated known-rule violation.
No task-specific formatting is promoted to a company-wide requirement.

## Status and risks

Source-backed case preparation only. Historical intervention totals, complete resource
use and unknown rule-read stages remain unknown. No transcript-wide audit or new
behavioral experiment was performed. Subsequent design/trials belong to existing
P0.2/P1 entries in [central TODO](../../../../TODO.md#knowledge-base).

## Portable lesson

Existing [correction-learning](../../../../general/knowledge/agents/correction-learning.md).
