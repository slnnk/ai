---
system: knowledge-base
status: verified
checked: 2026-11-09
tags: [agents, experiments, evaluation, model-routing, planning]
---
# Merged agent-methodology experiment proposals

## Summary

The user requested additional experiment ideas merged with earlier proposals.
This plan combines old optional steps 4/5/7/8/9, the current dialogue's methodology
recommendations and three focused additions: instruction scope/provenance, partial
failure handling, and shared-state concurrency. Fourteen experiment families have
explicit comparisons and acceptance evidence. Cheaper-model delegation is first;
total accepted-task cost includes the coordinator, retries and verification.
Old completed steps 1/2/3/6 and the F1 fix stay completed, and the Claude-specific
extension stays cancelled. Technical defects already established by reproduction
remain ordinary fixes, not questions of whether to tolerate them for lower cost.
At the planning checkpoint no experiment, model invocation, install or permanent rule
change was authorized or performed. On 2026-11-09 the user-selected bounded E01 pilot
was completed; see the [measured outcome](2026-11-09-knowledge-base-e01-model-delegation-pilot.md).
E02–E14 remain proposals. Central TODO remains the sole live action list; this is its
design evidence.

The user later authorized the [second E01 stage](../../../current/knowledge/log/2026-11-09-knowledge-base-e01-stage2-comparison.md), completed on 2026-11-09 with 36 historical-task attempts and 114 invocations. Raw cost fell with Luna helpers, but equal quality was not demonstrated; no model-default change was adopted. Method/rubric limits are recorded with that outcome. The user subsequently retained one Sol agent and closed E01 follow-ups without further runs; E02–E14 remain proposals.

## ECC follow-up recorded November 12

The user requested retaining the [ECC recommendations](2026-11-12-agents-ecc-local-approaches.md) for future pilots. Map compact resumption state to E08, behavioral regression cases to E02/E03/E05, and one targeted supported lifecycle hook to E12. Preserve the existing experiment IDs and central TODO entry; this records future candidates without authorizing a run, installation or configuration change. The suggested E08-first order remains an engineering recommendation, not a user-selected execution order.

## Task and context

Prepare a consolidated experiment selection plan within this dialogue. Sources:

- [Historical experiments](2026-10-19-knowledge-base-agent-capabilities-research.md#proposed-trial-order-user-requested-plan-not-implementation).
- [Current findings](2026-11-05-knowledge-base-agent-methodology-review.md).
- [Developer guidance and dialogue-only scope](2026-11-05-knowledge-base-developer-best-practices-research.md).
- [Twenty ranked recommendations and model-selection follow-up](2026-11-05-knowledge-base-prioritized-agent-tools.md).
- [Central TODO](../../../TODO.md).

Experiment IDs below are new and must not be confused with the historical step
numbers or the twenty-item recommendation ranking. They describe candidate
comparisons, not standing instructions for every task.

## Actions

Read the original plan, completed/cancelled outcomes and current proposals. An
independent read-only review checked coverage and suggested shared-state concurrency
as a distinct missing experiment. Consolidated overlapping ideas and added criteria;
no runtime agent used an experimental model configuration for this planning task.

## Common proposed protocol

The starting setup should be small and shared across selected experiments:

- Use representative sanitized cases and identical initial fixtures in each arm;
  split development examples from a small held-out set to avoid tuning only to known
  failures. A pilot might start with 10–15 cases and three repeats per arm, scaled to
  the selected question and an agreed budget. These numbers are suggestions, not a
  statistical guarantee or an instruction to launch all comparisons.
- Define success before running: final artifact correctness, required constraints,
  recoverable failures and useful evidence. Record uncached/cached token usage when
  available, all participating agents, retries, elapsed time and human correction
  work. Convert to currency only with the applicable billing basis; do not equate
  raw token totals with actual charged cost.
- Treat unauthorized writes, lost unrelated edits, disclosure of fake test secrets
  and false completion claims as failures, not tradeoffs compensated by lower cost.
  Zero observed failures in a small sample is not a general safety guarantee.
- Keep source cases, tool/client versions, model/effort settings and output budgets
  stable within a comparison. Vary one factor where possible; when comparing complete
  policies, label the result as a policy comparison rather than attributing it solely
  to the model. Balance run order and document cache conditions.
- Use disposable copies, mock external systems and synthetic access values. Model
  evaluations, hooks or selected tool installation require their own implementation
  decision. Do not connect tests to live publication/deployment paths.
- Retain traces and generated artifacts in `~/ai-data/`; keep reusable sanitized
  checks near existing tests. Do not introduce a second backlog or replace an accepted
  retrieval baseline with a failed run.

These proposals adapt the distinction between traces/outcomes and repeated trials in
[Anthropic's evaluation guidance](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)
and positive/negative skill cases in
[OpenAI's skill-eval guidance](https://developers.openai.com/blog/eval-skills).
The local scenarios and priority judgments below are our own design proposals.

## Merged experiments

| ID | Experiment | Controlled comparison | Evidence of value / rejection |
| --- | --- | --- | --- |
| E01 | Cheaper-model delegation and total cost | A capable agent alone; the same coordinator with same-model helpers; then comparable helpers on a cheaper model. Keep delegation/context constant when changing the helper model. Test reasoning effort separately. | Correct accepted outcomes and no constraint regression; lower whole-task cost or meaningful speed improvement after coordinator work, retries and verification. Reject routes that merely shift work back to the coordinator. |
| E02 | Instruction scope and provenance | Paired prompts specifying only this dialogue versus an explicit future preference; add quoted document instructions, cancelled decisions and a fresh follow-up session. | Dialogue-only directions do not become permanent rules; genuine explicit durable directions are saved correctly; source text is not promoted to user authority. Inspect persisted files and subsequent behavior. |
| E03 | Partial tool failures and truthful completion | Existing versus improved response contracts under empty results, unavailable roots, truncated logs, malformed output, checker crashes and partially successful operations. | Agent distinguishes no matches from incomplete inspection, requests only needed evidence and reports actual partial state; never claims a skipped check or unpublished result completed. Use mock tools. |
| E04 | Shared-state concurrency and ownership | Sequential work versus two workers in disposable copies, with controlled user edits after reads, unrelated staged changes and duplicate correction evidence. | No lost changes/double bookkeeping; stale diff detected; unrelated index content preserved; completed and still-running workers reported correctly. Start with deterministic race reproduction. |
| E05 | Skill activation and useful execution | Current skill versus a candidate revision on new explicit, implicit, adjacent-negative and conflicting-context cases. Include cli-creator/security workflow samples only if selected. | Correct activation/rejection and useful final artifacts; no unrequested process expansion. This extends earlier pilot2 with new coverage rather than declaring it unfinished. |
| E06 | Real-agent retrieval and decision use | Fixed-script benchmark plus fresh agents asked natural task questions; vary added distractor logs, paraphrases and cancelled/superseded evidence in fixtures. | The agent finds and applies the current relevant answer/decision with bounded reading, not merely a target file in top5. Preserve old measured results and separately score ranking and query preparation. |
| E07 | Startup context and output budgets | Current loading versus task-scoped references; separately compare verbose and bounded tool output with continuation links. | Fewer unnecessary reads/tokens/time without missing required constraints or answers. Vary context selection and tool output in separate rounds to identify their contributions. |
| E08 | Resumption after interruption or compaction | Reconstruct state from full task history versus a compact existing task record, then introduce a benign source-state change before resumption. | Agent retains goal, authorized scope, cancellations and evidence; rechecks changed state, avoids repeating completed actions and performs the next permitted step. |
| E09 | Independent review and reviewer context | Author self-check versus an independent reviewer; compare reviewer access to the implementation narrative against a concise task/diff/evidence brief. | More confirmed defects caught with bounded false positives and cost. Review only the task diff, without fixes/publication. This preserves historical step4 and adds a context-bias comparison. |
| E10 | One focused DevOps skill | Same saved LogQL tasks without/with a selected skill; if a different concrete need is chosen, use a separate Terraform plan/mock or GitLab CI case set. | Fewer query/configuration mistakes at unchanged scope and reasonable cost. Preserve deployed syntax/pinned versions; no automatic apply, provider upgrade or real deployment. Historical step5. |
| E11 | Targeted static checkers | Existing checks versus one added checker at a time: Gitleaks, ShellCheck or Lychee, using seeded known faults and clean controls. | Additional real fault coverage, acceptable false positives, clear failure status and reasonable overhead. Check partial staging and output handling; an intentional protective failure is not a flaky result. |
| E12 | One nonblocking lifecycle hook | Existing reminder/check delivery versus one supported hook in a test client, with relevant and irrelevant events. | Fewer missed required checks without duplicate executions, loops, approval changes or disproportionate delay. Verify runtime support before building; historical step7. |
| E13 | Coupled-edit detection with BlockWatch | A few genuinely coupled fixtures, correct coordinated edits and deliberately omitted companion edits, compared with current checks. | Detect useful missing co-edits with low noise. Do not treat textual coupling as proof of semantic TODO consistency; skip if no real coupling need exists. Historical step8. |
| E14 | Selected documentation/navigation/interface/export tool | Choose one: Context7 vs official-doc search; Serena vs current code navigation; Playwright vs an uncovered interface workflow; Repomix vs current context handoff. Compare only tasks in that tool's scope. | Better correctness or less time/context with understood data flow and setup cost. Never install/run all candidates as one confounded comparison. Historical step9 plus current candidates. |

## New focused experiments

E02 isolates a demonstrated scope failure from this dialogue rather than adding a new
global instruction. It includes the opposite case, where the user really does ask
for a permanent rule, so a blanket refusal to remember anything cannot pass.

E03 injects partial failures to test end-to-end interpretation and final reporting.
It does not repeat only the completed F1 script test and does not delay repairing
the already confirmed missing-root defect.

E04 separately tests coordination correctness. Cheap helpers (E01), useful independent
review (E09) and correct error reporting (E03) do not establish safe concurrent writes.
The synthetic user changes and staged content remain within disposable fixtures.

## Coverage and dependency mapping

| Prior item | Current home |
| --- | --- |
| Historical step4: independent review | E09 |
| Historical step5: one DevOps skill | E10 |
| Historical step7: lifecycle hooks | E12 |
| Historical step8: BlockWatch | E13 |
| Historical step9: convenience tools | E14; token accounting cross-check is part of E01 measurement |
| Current model selection/delegation proposal | E01; concurrent-state correctness separately E04 |
| Existing-skill and retrieval improvements | E05–E06, extending completed bounded pilots |
| Context selection, bounded output and resumption | E07–E08 |
| New concrete static tools | E11 |
| Promptfoo | Optional measurement/reporting infrastructure if native runner is insufficient, not a required experiment |

The completed historical 1/2/3/6 and F1 remain completed. The prior small skill pilot
did not establish incremental quality gains; this plan makes no contrary claim.
Cancelled Claude work is not revived. Actual observed F2–F7 defects remain in their
existing central fix/proposal records: experiments assess candidate approaches and
new coverage, not permission to leave verified defects unresolved indefinitely.

Suggested first bounded selection: share a small fixture/evidence format, then choose
E01 for economics and E02/E05 for scope and activation. E03/E04 need their own failure
and concurrency fixtures. Later tool-specific families are selected only for a concrete
workload. No recommendation means all fourteen should run at once.

## Changes

Created this proposal design and linked it from the earlier plans and relevant central
TODO entries, preserving source history. Refreshed affected display-cache titles and
indexes. No scripts, skill definitions, global instructions, model configuration or
external systems were changed. No benchmark or experiment was executed.

## Status and risks

Plan prepared on 2026-11-06; all E01–E14 were proposals at that checkpoint. The user
subsequently selected E01. Its [bounded pilot](2026-11-09-knowledge-base-e01-model-delegation-pilot.md)
finished on 2026-11-09: 42 calls, full participant usage and verification, no permanent
model-routing changes. Luna helpers reduced delegated cost but did not beat solo on
the tested short tasks; one strict next-action mismatch has a documented rubric
ambiguity. E02–E14 remain proposals referenced from central TODO. No background
research or experiment remains running.

## Portable lesson

none
