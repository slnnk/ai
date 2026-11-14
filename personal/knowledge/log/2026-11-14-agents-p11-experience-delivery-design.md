---
system: agents
status: verified
checked: 2026-11-14
tags: [agents, learning, retrieval, design]
---
# P1.1: scoped experience delivery as knowledge grows

## Summary

P1.1 completes a design, not implementation or measured behavioral improvement.
Retain Markdown, agent-learning and the completed search fixes. The smallest proposed
change is a short addition at the existing pre-action retrieval step of agent-learning:
select relevant decision-example sections and state their applicability to the choice.
Keep mandatory instructions independent of topical ranking; examples are evidence.
Retrieve current state/procedures separately from historical rationale. Start with at
most two example sections; expand when exceptions, sources or decisions are incomplete.
Report coverage and unknowns instead of treating a short page as complete evidence.
No new index, store, hook, package, worker or automatic rule promotion is needed now.
P1.3 owns the selected canonical diff; P1.4/P1.5 own trials and adoption. Expected benefit
is a hypothesis: C01/C03 show that rules can already be loaded and still be violated.

## Task, authorization and acceptance

User request: execute P1.1, preparing applicable experience delivery with KB growth.
The [central TODO](../../../TODO.md#knowledge-base) explicitly defines a design deliverable;
implementation follows selection of the design. Authorized work here is local source
inspection, design and bookkeeping. No permanent instruction, runtime or search change
and no fresh-agent trial is included. One main agent performed the work.

Acceptance criteria established before writing:

- Justify the smallest change using P0.1/P0.2 and current retrieval capabilities.
- Specify timing, scope, sources, rationale, exception handling and bounded expansion.
- Separate mandatory rules, current state/procedures and historical decision evidence.
- Preserve task isolation, explicit/inferred distinctions and cancellations under growth.
- Give concrete examples and a falsifiable later verification plan, without claiming transfer.
- Reconcile this task's status with existing owners; create no parallel backlog or store.

## Sources and supported gap

Read [P0.1 cases and failure stages](2026-11-14-agents-p01-decision-cases-metrics.md#historical-learning-examples),
[P0.2 bounded design](2026-11-14-agents-p02-learning-search-comparison.md#recommended-bounded-design),
[growth requirements](2026-11-14-agents-personalized-learning-backlog.md#knowledge-growth-assessment),
[completed retrieval fixes](2026-11-14-knowledge-base-rules-retrieval-stability.md#verification-and-status),
[canonical learning workflow](../../../general/skills/agent-learning/SKILL.md), its
[query contract](../../../general/skills/agent-learning/references/operations.md#retrieval-and-verification),
and [KB retrieval](../../../general/knowledge/README.md#knowledge-retrieval).
The active global rule targets were read, including simplicity, scope and permissions.
Company evidence remains linked from P0.1 in its company layer; this design copies no
company infrastructure details. No new public-product capability assessment was needed.

C01 and C03 establish violations despite loaded instructions. C02 supports exposing a
constraint that causes a workaround; its precise prior rule-read state is unknown.
C04 establishes that new task-specific preferences must not become global instructions.
Therefore more search results alone cannot establish a remedy. Proposed benefit comes
from connecting an applicable precedent, including its exception, to the impending choice.
That connection is an engineering hypothesis until later transfer evaluation.

## Proposed delivery contract

This section is a proposed design, not an active agent instruction or required new form.
Use the existing main-agent workflow; no extra model call, approval gate or collector.

### Timing and retrieval roles

At the existing before-related-work step, before committing to an implementation
approach, identify the task/layer/repository/task ID and the specific engineering choice.
Revisit retrieval when a consequential new action type or materially different constraint
appears. Reuse current instruction text already fully loaded; do not reread it for ceremony.

| Role | Canonical source and selection | What it can establish |
| --- | --- | --- |
| Mandatory operating rules | Shared/project instructions, triggered README sections, scoped learning lookup; independent of example relevance | Permissions, prohibitions, exact task/repo boundaries; never omitted to satisfy an example quota |
| Current state | Existing system map, current repository/configuration or authoritative live observation when needed and authorized | What exists now; old logs are clues, not proof of installed tools or current credentials |
| Reusable procedure | Existing skill or portable recipe, with scope/status/date and needed section | Supported method and limits; a historical successful command grants no current execution permission |
| Decision evidence | P0.1 example section, linked original correction/final decision and canonical rule | Why a choice changed and when that rationale applies; not a replacement for current facts |

Run existing agent_learning.py query with the actual scope, repository and task ID when
applicable. Review applicable canonical targets, not just labels. Scope/task exclusions
precede relevance. Background global obligations remain discoverable even when they do
not match the choice. Follow continuation or increase the limit for applicable records;
record incomplete coverage if unable to finish. This does not require untriggered details
for every unrelated global topic. A page limit cannot relax a known obligation.

Use prepared English technical terms and unchanged identifiers with kb_find.py. Pick
layers by the task and metadata system only when known. For judgment questions search
specific choice terms, not broad words such as scope/correction alone. An already known
P0.1 section link can be followed directly; do not add a second manually maintained
example registry. For operational questions establish current state first; use history
when explaining a decision or investigating a contradiction. Ranking is a candidate
heuristic, not an authority hierarchy or verification of factual freshness.

### Compact context and expansion

Initial working context contains the relevant current rule/constraint references and
zero to two applicable example sections. Two is a proposed initial example budget from
P0.2, not a global cap on rules or evidence. Zero is valid when no applicable precedent
exists. Keep this in the existing task reasoning/log where useful; no mandatory public
template, parallel evidence store or transcript copy.

For each selected precedent retain: source section; rule or decision scope/state/date;
original rejected and final approach; rationale; matching present condition; exception
that would justify the rejected approach. Mark examples as historical evidence and
unconfirmed generalizations as proposals. Link the canonical rule rather than restating
it as a newly adopted instruction. A source update, not similarity score, resolves an
explicit superseding/cancellation decision within its actual scope.

Use kb_find's note/section references, line numbers and coverage. Read the full selected
example section when its rationale, exception, source or decision is absent from the
excerpt. Expand to linked original evidence only for unresolved conflict, missing context
or uncertain scope; do not load the entire source log by default. Check decision metadata
and its referenced decision section, including when query words omit that decision.
A restricted subtopic does not cancel unrelated completed results in a mixed note.

Bound reading by relevance and staged expansion, not by silently clipping safeguards.
Use existing default search budgets (15 notes/five excerpt lines) as candidate pages;
they are not answer-completeness guarantees. Follow next_command for a conclusion that
depends on omitted candidates. After the existing at-most-two empty-result reformulations,
state the gap and preserve uncertainty. Tool errors/corrupt metadata require handling;
they are not normal zero matches. A missing example does not block ordinary authorized
work; missing material facts or unresolved permission conflicts use existing rules.

The coverage statement distinguishes candidates found/shown, source sections actually
read, rule lookup completeness and unresolved facts. It can be one brief task-log line;
no mandatory recurring user-facing checklist. Search term visibility is not completeness
of obligations, understanding or successful application. If source files change during
pagination, restart lookup; do not combine pages as a stable snapshot.

### Connection to the choice

The useful addition is a brief rationale in the existing decision: which present fact
makes the precedent applicable, which exception was checked, and what approach follows.
When it changes the proposal, show that reason naturally in the proposal. Ordinary choices
remain autonomous. Material assumptions and approvals retain their current triggers.
P1.2 owns necessity/alternative handling; this design supplies evidence, not a duplicate
necessity checklist. Outcome bookkeeping reuses agent_learning and agent_metrics and
preserves first-attempt failure separately from recovery.

## Concrete documentary examples

These are interpretations of known historical cases, not fresh-agent tests or new
outcome scores. No prospective fixture was executed or exposed to another agent.

| Choice | Delivered context and applicability | Required boundary |
| --- | --- | --- |
| C01: repository acquisition | Simplicity rule plus P0.1 C01: the previous downloader was unnecessary because the base image supplied tools; inspect the present base image and authentication/revision needs | If a pinned binary is required and absent, C01 does not ban a verified download; current capabilities remain to be checked |
| C02: deployment ordering | P0.1 C02: identify whether the chosen credential source causes the dependency; source records a user-selected compatible alternative | Historical approval does not authorize changing this task's credential source; retained isolation may require ordering logic |
| C03: dialogue-only direction | P0.1 C03 plus original restricted decision: retain task evidence without promoting a standing proposal-recording rule | The restriction concerns that inferred rule; it does not prohibit genuinely explicit durable preferences |
| C04: issue formatting | P0.1 C04 explains a task-specific formatting correction and its recovery | A different issue's explicit format wins; do not export dedicated-field-only formatting as a global rule |

Compact C01 example after reading its full section: historical reason = supplied tools
made acquisition code redundant; present applicability = tools and supported authenticated
checkout actually verified; exception = missing/pinned-tool requirement; decision = reuse
checkout if those facts hold. If facts are not inspected, label applicability unresolved,
rather than asserting that the current image contains the tools.

## Growth, ownership and escalation

Markdown stays canonical, with one rule and linked evidence. New incidents extend an
existing scoped record/example when appropriate; inferred patterns do not become active
through frequency, age or silence. Do not consolidate the whole KB or expire explicit
rules. Preserve historical rationale, exceptions and superseding decisions while updating
touched current maps. Existing maintenance and P1.3 own consolidation.

The November14 inventory is a dated size observation, not a latency or context-cost
measurement. Growth alone selects no backend. Existing coverage/pagination and section
expansion address bounded reading now. FTS5 is conditional on measured lexical scan/rank
cost or gaps; hybrid/QMD on source-backed paraphrase/cross-language failures after query
preparation. Any index would be regenerable from Markdown, honor filters/decisions and
remain a non-authoritative reader. A missed delivery trigger can instead motivate the
existing conditional P2.1 owner; it is not evidence that a search backend is required.

Smallest future change: one concise addition to the existing agent-learning
Before related work step, using the existing P0.1 links and retrieval contract. P1.3
should merge actual overlap with existing canonical prose rather than append another
workflow. No AGENTS.md growth, new script/schema/store or hook is proposed for this
first change. P1.2 contributes its necessity design before P1.3 prepares the combined
diff. Selection and ordinary permissions govern implementation; P1.4 runs only an agreed
bounded pilot and P1.5 decides adoption. Rollback would restore only the selected hunk;
retain all canonical sources, decisions and measurements. Nothing runtime-related was
installed here and no runtime rollback is currently needed.

## Verification and limits

Read-only observations on the unchanged retrieval implementation:

- kb_find.py -l personal -s agents -m 3 capabilities acquisition returned two notes;
  C01 was first. Its excerpt omitted applicability/exception content; the complete C01
  section was read. This supports staged expansion, not complete-answer claims.
- An exact simplest-sufficient-solution learning query ranked that rule first, while
  reporting one topical and 22 background global records and continuation. Earlier
  scoped lookup with --limit 40 showed/read all 23 returned rule references and their
  relevant canonical policy; the short exact page was not counted as full coverage.
- kb_find.py -l personal -m 2 scope correction returned 57 candidates with unrelated
  results on the first page. No absence/completeness inference was made. The known P0.1
  C03 link and original restricted source were read instead of scanning all 57 notes.

These are observed examples, not a corpus benchmark or an unseen-transfer score.
Search code, output and active query-preparation instructions remain unchanged, so no
new search regression run is required. Saved 72-condition results remain historical
mechanics evidence. This proposal is not an active instruction change.

Later verification belongs to P1.4: freeze rules/examples/model/effort/fixtures and
separate training evidence from unseen positive/negative tasks using P0.1's contract.
Observe delivery before approach selection, canonical reads, actual applicability and
first delivered artifact; assess correctness, human corrections, inappropriate transfer,
unnecessary work and complete reading/model/retry/evaluator cost with unknown coverage.
Keep C01/C03 loaded-but-violated outcomes visible if delivery still fails to help.

For selected E06 growth cases, add irrelevant history without leaking held-out solutions;
check relevant evidence/decision visibility, mandatory-rule retention, exact task exclusion,
current-versus-history conflict, cancelled/restricted scope, negative applicability,
clipping/continuation and output/read volume. These are case dimensions, not an authorized
run/count/budget or a reopened startup/resumption evaluation. If search or actual query
instructions change later, run the existing synthetic and immutable-baseline real suite.
Improved retrieval alone cannot pass transfer; correctness/scope regression or critical
permission/false-completion events cannot be traded for a lower average cost.

## Changes and final status

Created this design; linked its completion in the existing parent backlog note and
closed only P1.1 under Knowledge base. P1.2/P1.3/P1.4/P1.5 retain existing ownership;
no additional task or approval request was created. Acceptance was reviewed against the
sections above. This is author-checked documentary completion, not independent evidence
of behavioral benefit. First delivery and attributable tokens/time remain unassessed.
Checks: all 22 local links/anchors in this note and its affected parent note passed;
the design acceptance inventory passed; KB lint reported zero errors/warnings; learning
store validation passed (69 records); indexes rebuilt without missing frontmatter.
TODO ancestry is Knowledge base and P1.1 is closed. Filtered rendering retains only
P1.3's reference to P1.1; no affected open title changed or needed a cache refresh.
Applicable planning-scope and expected-result rule outcomes were recorded once against
this evidence. No agent instruction/skill resource/settings changed, so agent lint was
not triggered. All task commands completed synchronously; no background commands or
agents remain. No external state change was performed beyond the authorized daily sync.

## Portable lesson

Reuse [correction-learning](../../../general/knowledge/agents/correction-learning.md).

## Task metrics: kb-p11-20261114

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "kb-p11-20261114",
  "created": "2026-11-14T03:19:24.388489+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "design",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Author-checked P1.1 design acceptance in this note; source-backed examples and scoped delivery contract complete. Behavioral benefit and first delivery independently unassessed; attributable usage/time unknown.",
  "updated": "2026-11-14T03:19:24.388567+03:00"
}
```
