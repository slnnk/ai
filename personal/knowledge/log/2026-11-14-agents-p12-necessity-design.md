---
system: agents
status: verified
checked: 2026-11-14
tags: [agents, simplicity, design]
---
# P1.2: necessity checking before implementation

## Task

Execute knowledge-base P1.2: prepare the smallest necessity check before adding
configuration or helpers. Authorized work is this design and local bookkeeping;
active instruction edits belong to P1.3 and any transfer trial to P1.4.
The user requested preparation, not installation, a new approval gate or enforcement.

Acceptance: connect existing analogues, actual tool capabilities and constraints to
the implementation choice; justify deviations; surface assumptions causing workarounds
early; retain ordinary autonomy and necessary complexity. Verify by documentary
walkthroughs of positive and negative P0.1 cases and a scope/link review. These checks
establish design coverage, not fresh-agent activation or measured improvement.

## Context and evidence

- [P0.1 cases](2026-11-14-agents-p01-decision-cases-metrics.md#historical-learning-examples):
  C01 missed inherited tools despite a loaded simplicity rule; C02's credential choice
  caused ordering work, but changing that choice needed a user decision. C03/C04 show
  why task preferences must not become universal prohibitions.
- [P0.2 design](2026-11-14-agents-p02-learning-search-comparison.md#rejected-alternatives-and-conditional-escalation):
  no sound textual oracle for engineering necessity; retain existing workflow rather
  than add a blocker, observer, product or duplicate writer.
- [P1.1 delivery](2026-11-14-agents-p11-experience-delivery-design.md#connection-to-the-choice):
  supplies applicable current constraints and scoped historical rationale before the
  choice. P1.2 consumes that evidence; it does not add another retrieval registry.
- Existing [Simplicity](../../../general/knowledge/README.md#simplicity),
  [Affected flow](../../../general/knowledge/README.md#affected-flow) and
  [Material assumptions](../../../general/knowledge/README.md#material-assumptions)
  already own solution order, consumer inspection and consequential clarification.

The gap is application at the choice, not evidence that another generic rule is missing.
The design below is a proposal; none of its wording becomes an active instruction here.

## Proposed necessity check

### Timing and bounded inspection

Use the existing approach-selection step, before writing the proposed configuration,
helper, dependency or compatibility branch. Revisit only if a new constraint changes
that choice. A direct reuse or ordinary reversible edit can proceed without a public
form or user confirmation. Do not turn every command into a checkpoint.

Inspect the nearest relevant established consumer/helper and its actual execution
environment. Check the specific capability the proposed addition would duplicate:
inherited image tools and versions, authenticated acquisition routes, supported input
formats, platform behavior or dependency ordering as applicable. A visible customization
alone does not establish what the base environment supplies. Use local code/manifests
and existing scripts first; use a proportionate read-only capability check when needed
and available. Unknown availability stays unknown, not an assumed missing dependency.
Do not crawl unrelated repositories or install a tool merely to investigate it.

Follow the existing selection order: established project solution, platform/standard
capability, installed dependency, then minimal new code. An analogue is evidence of a
candidate, not permission to copy credentials, stale assumptions or incompatible behavior.
Compare its relevant guarantees with the current request and affected consumers.

### Reason attached to the choice

For each consequential addition, tie the mechanism to a concrete requirement or observed
constraint and explain why the nearest simpler candidate fails that requirement.
Keep this rationale in the existing proposal/task record when review is useful; no new
schema, mandatory template or duplicate decision log. A natural example is:
"The base manifest supplies the required tool and checkout supports the requested
revision, so reuse checkout." For a justified deviation: "The tool is absent and
installation is unavailable; the pinned verified artifact is required, so use the
existing verified acquisition helper, or the smallest supported acquisition path."

Test necessity by removing the proposed mechanism conceptually: if required behavior
and safeguards remain, omit it. If removal breaks an evidenced requirement, retain it
or choose a simpler compatible method. Do not implement competing solutions merely
to compare them. Speculative future formats, retries or extension points are not
requirements; explicit supported formats and demonstrated failure modes can be.

### Assumptions that create a workaround

When an assumption creates a chain of ordering, bootstrap, ownership, readiness or
compatibility logic, examine that assumption before optimizing each link. Establish
whether it is an explicit requirement, a verified system constraint or an agent guess.
Expose the causal tradeoff early in the existing proposal: retaining X requires Y;
the established alternative Z removes Y but changes the stated behavior or guarantee.
State the relevant difference, evidence and remaining uncertainty, not just line savings.

If the simpler alternative changes a material requirement, credential/security property,
scope or permission, preserve current semantics and clarify under existing rules before
acting on that choice. Continue independent authorized work while awaiting the answer.
If the choice is routine, reversible and satisfies all known constraints, decide it
autonomously. No new approval is required merely because a solution has extra steps.
An unresolved material fact can block the dependent choice; lack of a historical example
alone cannot. Any necessary scope expansion keeps its existing approval requirements.

### Review and ownership

Before presenting the resulting change, reuse the existing simplicity review: each
remaining consequential addition has a requirement and simpler-candidate comparison;
required safeguards and affected behavior still hold. Uncertainty is reported explicitly.
Use behavior/constraint evidence rather than line count, abstraction count or a model's
self-score. A small script can violate requirements; longer ordering logic can be required.

P1.3 should first assess a minimal replacement/clarification in the existing README
Simplicity section, reusing Material assumptions and Affected flow by reference. Do not
add parallel AGENTS/skill/prompt checklists. P1.1 supplies the evidence delivery and this
design supplies its connection to the choice. Whether any wording change is needed and
the actual canonical diff remain P1.3 decisions. No helper, hook, schema or settings
change is justified by this preparation. P1.6 retains separate helper-inventory ownership.

## Documentary walkthrough and verification contract

These are design checks against the existing specifications, not executed fixtures,
new rule-task pass scores or unseen transfer evidence.

| Case | Expected application and review oracle |
| --- | --- |
| C01 / T01 | Inspect base and customization; required installed tools and supported checkout remove the acquisition need. Reject downloader/checksum/PATH machinery without a remaining concrete requirement. |
| N01 | Missing tool, unavailable installation and pinned verified binary requirement justify bounded verified acquisition. Reject blindly forbidding downloads or weakening integrity. |
| C02 / T02 | Trace secret ordering to the selected credential mechanism; show the compatible established alternative and its changed guarantee before constructing the workaround. Preserve credentials pending the decision. |
| N02 | Explicit isolation remains mandatory; retain it and choose minimal supported ordering/phase handling. Reject silently copying the simpler credential pattern. |
| C03 / T03 | Discussion-only direction remains task-scoped; reuse evidence without adding permanent policy. Reject a new universal necessity checklist derived from this task. |
| C04 / N03 | Follow the current issue's explicit format and existing approvals. Reject importing another issue's dedicated-field preference or treating fewer sentences as correctness. |
| Ordinary reuse | Reuse a verified compatible existing helper without a new confirmation/form. Reject a new gate or broad environment audit when the capability and constraints are already known. |
| Speculative format support | With one requested format and no additional consumer requirement, omit alternate parser/configuration branches. Retain them when actual required consumers demonstrate the need. |

Walkthrough result: each row has an action and a falsifiable failure boundary; the
same historical lesson permits opposite choices when the verified constraints differ.
No fresh client/model trial was run. Future selected P1.4 evaluation uses P0.1's
first-delivery correctness, substantive corrections, unnecessary work, critical events,
whole-task cost and per-measure coverage; preserve unknowns and recovered failures.
Reuse its frozen-state/exposure/negative-case requirements rather than create another
pilot. A retrieved rationale or green lint alone does not establish behavioral success.

## Changes and status

Prepared this design, linked it from the existing prioritized map and closed P1.2 in
the central TODO. P1.3 remains the existing owner of a coherent proposed canonical diff;
no additional action item or instruction layer is introduced. Benefit remains a design
hypothesis until separately selected behavioral evaluation. Unrelated working-tree
changes are preserved.

Verification: eight documentary case rows and the required timing, capability,
deviation, assumption and autonomy boundaries passed content assertions. TODO ancestry
confirmed P1.2 closed under Knowledge base; P1.3 stays open as the existing owner.
The filtered TODO rendering has a current cached title for that remaining owner.
KB lint completed with zero errors and warnings; indexes were rebuilt. No instructions,
skills/resources or settings changed, so no new agent-lint run is triggered by this task.
Existing discussion-only and verifiable-results rules were evaluated against observed
scope and verification behavior, not scored as evidence of necessity-check transfer.
New design generalizations remain proposals; no new durable user preference is inferred.
All task commands finished; no background operations or agents remain.

## Portable lesson

Reuse [correction-learning](../../../general/knowledge/agents/correction-learning.md).

## Task metrics: p12-necessity-design-20261114

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "p12-necessity-design-20261114",
  "created": "2026-11-14T03:23:08.291319+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "analysis",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Eight documentary cases and scope/TODO content assertions passed; KB lint zero findings; design only, no behavioral transfer claim",
  "updated": "2026-11-14T03:23:38.646559+03:00"
}
```
