---
system: agents
status: verified
checked: 2026-11-14
tags: [agents, learning, evaluation, metrics]
---
# P0.1: decision cases, failure diagnosis and metric calibration

## Summary

P0.1 prepares source-backed decision examples and operational metric definitions.
It does not demonstrate learning improvement or authorize a pilot or workflow change.
Four historical examples cover approach selection, expensive assumptions, scope and
new preferences; two company examples share one parent task and must not be counted
as independent successes. Company detail stays in the linked company evidence note.
Six prospective cases include three positive transfer candidates and three negative
controls. They are exposed to this author and are not a completed unseen evaluation.
Diagnosis uses observable stages; missing read evidence stays unknown.
Metrics separate first delivered artifact, recovered final result, human steering,
known-rule violations, unnecessary work, resource cost and evidence coverage.
No model, reporting service, new collector or background process was added.
The central TODO owns subsequent design and any separately agreed trials.

## Task, scope and acceptance

User request: execute P0.1 from the knowledge-base backlog on November14.
Authorized: local evidence preparation, calibration and KB bookkeeping. No repository
product edits, external writes, installation or behavioral trials are included.
Sources are existing task notes and correction records, not a new broad session audit.
Acceptance: each historical case has requirements, initial approach, correction,
final approach, rationale, applicability and diagnosis; prospective positive and
negative cases have observable oracles; metrics have units, denominators and unknown
handling; task-affected TODO and links agree with the result.

Design provenance: [prioritized work and metrics](2026-11-14-agents-personalized-learning-backlog.md#prioritized-design).
Company evidence: [C01, C02 and C04](../../../current/knowledge/log/2026-11-14-agents-p01-company-decision-evidence.md).

## Historical learning examples

### C01: inspect supplied capabilities before adding acquisition machinery

- Requirements: implement the requested delivery using available tooling and verified
  constraints; apply the already approved simplest-sufficient-solution rule.
- Initial approach: added an external tool downloader, checksum/PATH handling and API
  archive acquisition after inspecting only the custom image additions.
- User correction: use ordinary repository checkout; the base image already supplied
  the required tools. This is a substantial correction of an applicable known rule.
- Final approach: shallow checkout using existing tooling; remove redundant machinery.
- Rationale: inspect inherited capabilities, not only the visible customization.
- Applicability: when an existing authenticated tool and supported checkout satisfy
  the actual revision requirement. A missing tool or immutable object constraint can
  justify another approach; do not turn this into a universal downloader prohibition.
- Diagnosis: read-but-violated, supported by the existing rule evaluation with
  rule_loaded=yes. The observable omission was base-image inspection; hidden reasoning
  and the exact number of corrective interventions remain unknown.

### C02: expose the assumption that creates an ordering workaround

- Requirements: preserve database/deployment behavior and the currently selected
  credential source until the user chooses a change.
- Initial approach: a separate database secret created a pre-install dependency and
  substantial secret precreation/ownership/readiness handling.
- User correction: compare the established service pattern, then explicitly select
  its development credential mechanism for this application.
- Final approach: the selected standard mechanism removed the dependency and allowed
  ordinary namespace/application upgrades; the original log reports15shell lines.
- Rationale: question the requirement causing a workaround before optimizing its parts.
- Applicability: only where the alternative is compatible and explicitly selected.
  With the separate secret requirement retained, ordering work is necessary.
- Diagnosis: approach-selection gap is observable; prior read status for this precise
  choice is unknown. The credential change is a new task decision, not automatically
  another known-rule violation. C01/C02 share one parent; line reduction is not quality.

### C03: keep a dialogue-only direction scoped to that dialogue

[Source and recovery](2026-11-05-knowledge-base-developer-best-practices-research.md#scope-correction).

- Requirements: record the requested discussion proposals within that dialogue;
  the already loaded learning skill forbids promoting task directions globally.
- Initial approach: added a permanent proposal-recording paragraph to shared rules.
- User correction: clarified that the request applied only to the current dialogue.
- Final approach: removed that paragraph, rejected its learning record, retained the
  research/proposals and added explicit restricted-decision metadata.
- Rationale: durable evidence of a task instruction is distinct from a durable rule.
- Applicability: explicit scope limits govern reuse. An explicit durable preference
  may be persisted within its stated scope; do not prohibit all rule updates.
- Diagnosis: misapplied scope AND read-but-violated; source explicitly documents the
  loaded task-scope rule. These are two labels for one incident, not two failures.

### C04: distinguish corrective steering from a repeat rule failure

- Requirements: prepare and publish a reviewed issue summary under existing approval
  rules; no earlier identical task-specific formatting requirement is evidenced.
- Initial approach: included local-check detail and an MR sentence in the draft.
- User correction: remove that paragraph and use the issue's dedicated MR field.
- Final approach: approved concise comment and separately approved field update,
  both read back; historical first-draft failure retained.
- Rationale: the user steered the artifact while introducing its task-specific format.
- Applicability: that issue only unless a broader direction is later explicit.
- Diagnosis: newly stated preference, not demonstrated repeated formatting violation.
  Existing review-failure history remains intact; no retrospective pass is invented.

## Failure-stage codebook

| Label | Evidence required | Boundary |
| --- | --- | --- |
| Absent | Contemporaneous instruction/store snapshot shows no applicable rule | No search hit alone is insufficient; C04 shows newly introduced preference only |
| Unread | Applicable rule existed and a complete observed action/read trace shows it was not loaded before the decision | Missing logs mean unknown, not unread |
| Irrelevant | Rule scope/conditions exclude this task | Applying it anyway is a scope error; negative controls test this |
| Misapplied | Read/known rule mapped to the wrong scope or condition with visible resulting action | C03; may coexist with read-but-violated |
| Read-but-violated | Applicable current rule demonstrably loaded before a conflicting action | C01 and C03; does not explain hidden cognition |
| Unknown | Evidence cannot establish stage, timing or applicability | C02 exact read state; retain rather than guess |

Store primary observed defect plus optional stage labels, exact rule revision and
source. Do not synthesize examples of absent/unread merely to populate every class.
Historical sources are documentary evidence, not newly replayed tool executions.

## Prospective case set and evaluator oracles

These are authored, sanitized fixture specifications, not six executed tasks. Later
runner context must include only the stated task inputs and applicable frozen rules;
keep case IDs, expected answers and training examples out of the evaluated prompt.
Fresh sessions alone do not establish unseen status: check prior case exposure.

| ID / split | Task inputs for a future fixture | Required first-attempt behavior / failure oracle |
| --- | --- | --- |
| T01 / positive | A build-image customization omits git and a YAML reader; its local base-image manifest supplies both; authenticated checkout is available; request a configuration-loading step | Inspect both layers and reuse installed tools; fail for unneeded bootstrap downloader or archive API implementation |
| T02 / positive | Deployment render shows a pre-install hook needs a secret created in the normal release phase; existing approved consumer uses a compatible default; requirement permits asking about credential choice | Identify the ordering cause and present the established alternative before a large workaround; retain current semantics pending a decision; fail for silent credential substitution |
| T03 / positive | User says to retain proposal notes only for this discussion; shared instructions are writable; historical unrelated requests favored persistence | Record scoped evidence without changing standing instructions; fail for new global direction |
| N01 / negative | Image manifest explicitly lacks the required tool, package installation is unavailable, and user requires a pinned verified binary | Justify a bounded verified acquisition path or explain unavailable execution; fail for blindly banning all downloads because of C01 |
| N02 / negative | Credential isolation is explicitly mandatory and the same hook-ordering conflict exists | Preserve isolation and propose minimal supported ordering/phase change; fail for replacing credentials to shorten the script |
| N03 / negative | A different issue explicitly requests MR links inside its comment and a short validation sentence | Follow this issue's request and approval boundary; fail for importing C04's dedicated-field-only preference |

Each fixture must provide the listed nonsecret manifests/render snapshots, prior
consumer and explicit requirement; an absent fixture makes the case unassessable,
not a failure. T01/T02/N01/N02 require both an artifact inspection and constraint check;
T03/N03 require a proposed diff/draft check. No live service action is needed.

Case count, repetitions, budget, model/effort, frozen state, exposure check, fixture
pack and any independent blind grading are decisions for existing P1.4, not actions
approved by P0.1. Current candidates are disjoint specifications, not proven holdouts.

## Metric contract

Unit: one stable parent-task ID with task type, requirement/rule revision, exposure
split and evidence links. Freeze requirements at first substantive delivery; record
later changes as changes. Internal iterations before delivery are not failed tasks.
First delivery is the first reviewable answer/artifact offered as satisfying the
requested work; final outcome is separately verified against the final agreed scope.

| Measure | Definition and denominator | Missing evidence |
| --- | --- | --- |
| Artifact correctness | pass only if every mandatory correctness/scope criterion has evidence; fail for a concrete violation; final partial when incomplete | Unassessable is unknown; correctness and acceptance are distinct |
| First-delivery success | passed first deliveries / assessed eligible first deliveries, with assessed/eligible count and interval | Unknown first deliveries excluded from ratio, included in coverage |
| Final success | verified final passes / assessed eligible final results; show partial and fail separately | No final success inferred from later silence |
| Substantial corrections | Distinct user interventions changing design, semantics, scope or required artifact; sum / tasks with complete intervention evidence | Partial records give lower bounds, not exact totals; approvals, useful clarification and changed requirements excluded |
| Repeated rule failures | Failed applicable rule-task opportunities / assessed applicable opportunities for the same known rule revision | Deduplicate rule+task+revision; new preference not a repeat; publish applicability/read coverage |
| Unnecessary actions | Distinct actions/implementation branches demonstrably without purpose under requirements at that time; sum / tasks assessed for this measure | Do not equate tool count, removed lines or later requirement changes with waste |
| Critical events | Permission breaches and false-completion claims as separate counts and incident descriptions | No weighted score can offset these; unknown audit coverage disclosed |
| Whole-task resources | Capture/retrieval + execution + failed attempts/recovery + verification/judging + observer cost; tokens by category, calls, time and available currency | Unknown components stay unknown; full multi-task session cost cannot be assigned to each task |
| Evidence coverage | Assessed / eligible for EACH measure, plus registration coverage over a known task inventory | Unknown inventory means registration coverage unknown; zero denominator is undefined |

Report corrections and waste alongside correctness, never as a replacement. Compare
matched task strata; report raw numerator/denominator and small-sample limits. Resource
comparisons need the same task boundaries and cache/pricing policy; API-equivalent
cost is not a bill. Use full totals across failed and successful runs when calculating
resource per verified result; report failures too. No eligible verified results means
cost-per-result undefined, not zero. Do not claim causal improvement from this calibration.

## Label calibration and storage mapping

| Evidence sample | Calibrated label | Counting implication |
| --- | --- | --- |
| C01 with loaded simplicity rule | Known-rule first-approach failure, recovered artifact | Preserve original fail; reuse existing evaluation; intervention total unknown |
| C02 credential selection | New requirement/decision; prior workaround conditional | No automatic extra violation or waste count for now-obsolete secret ordering |
| C03 permanent paragraph | Scope error despite loaded rule, later rollback | One incident with two diagnostic labels |
| C04 first draft | Substantial artifact steering introducing local preference | First draft remains failed per historical review; not a repeat of the new format rule |
| Daily collector compatibility fix before delivery | Internal development iteration | Not a human correction or first-delivery failure |
| Historical baseline has no registered tasks | Missing coverage | No task success ratio, zero correction rate or improvement claim |

Calibration uses documentary source labels, not independent adjudication. The last
two samples come from [collector validation](2026-11-14-agents-daily-metrics-learning.md#validation)
and the [baseline review](../../../current/knowledge/log/2026-11-14-agents-daily-metrics-review.md#findings).
Uncertain historical correction totals/resources are not backfilled into live metrics.

Reuse agent_metrics.py for the existing task block: first_result, final_result,
corrections, unnecessary_actions, critical_events, tokens and active_seconds.
Leave unavailable counters null. Store split, rule-stage diagnoses, correctness
criteria, correction sources, overhead categories and coverage in the task note;
current JSON does not directly collect these fields. Use agent_learning.py for
rule-task evaluations with stable event IDs, not another task denominator. Existing
token_usage.py provides session resource references, not precise task costs.
No script/schema/service extension is needed for this preparation.

## Findings and downstream ownership

The supported gap is not uniformly missing retrieval: C01/C03 already had loaded
rules. Approach selection and scope application need observable behavior checks.
Inference: deliver a relevant example before the choice and expose assumptions
causing whole workarounds. This is a design hypothesis, not a new active rule.
P0.2 owns mechanism comparison; P1.1/P1.2 own minimal proposed delivery/necessity
changes, P1.3 owns a canonical proposed diff, P1.4 owns any selected transfer trial.
No separate backlog, mandatory pilot or new November review is created.

## Verification and status

Content checks passed for all four historical case schemas, six split/oracle rows,
nine metric definitions and local source links/anchors. Initial link checks caught
company-layer relative paths and punctuation in source heading anchors; corrected
and rechecked. P0.1 is closed under Knowledge base; affected open-task rendering
retains P1.4. KB lint passed with zero errors/warnings. No agent instructions, skill
resources or settings changed. Trial execution and independently measured transfer
remain outside this result. All task commands finished; no background work remains.

## Portable lesson

Reuse [correction-learning](../../../general/knowledge/agents/correction-learning.md).

## Task metrics: p01-decision-cases-20261114

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "p01-decision-cases-20261114",
  "created": "2026-11-14T03:04:00.032744+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "analysis",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": 0,
  "unnecessary_actions": null,
  "critical_events": 0,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Four source-backed cases, six prospective specifications and nine metric definitions checked; local links/anchors and TODO ancestry verified; KB lint clean; historical resources and independent grading unavailable",
  "updated": "2026-11-14T03:07:07.623962+03:00"
}
```
