---
system: knowledge-base
status: verified
checked: 2026-11-09
tags: [agents, evaluation, cost, comparison]
decision_state: restricted
decision_scope: E01 follow-ups and default model delegation
decision_summary: The user retained one Sol agent and closed E01 follow-ups; completed results are preserved.
decision_date: 2026-11-09
decision_source: #single-sol-decision
---
# E01 stage 2: approved model-delegation comparison

## Summary

Completed all 36 case attempts using 114 invocations in 1,927.351 seconds.
Observed usage was complete; native tools, infrastructure failures and timeouts were zero.
Operational API-equivalent cost: solo USD 1.262120, Sol helpers 1.910173, Luna helpers 0.758135.
The two preflights cost another 0.0263355; total measured estimate 3.95676266.
Luna reduced attempted-work cost 39.93% versus solo, but total time increased 36.28%.
Independent blinded review did not establish equal quality under the frozen protocol.
Strict full acceptance was 7/12 solo,7/12 Sol helpers and 3/12 Luna helpers.
A disputed composite rubric criterion penalized all C03 answers; symmetric sensitivity is retained.
Six corrections only normalized already-correct upload-number objects to scalars.
No task class met both the cost and quality adoption conditions; model defaults stay unchanged.
Read Findings for costs, per-case scores, grading limitations and the bounded recommendation.

## Task

The user explicitly authorized running the [prepared second stage](2026-11-09-knowledge-base-e01-stage2-preparation.md). Compare Sol alone, Sol with Sol helpers and Sol with Luna helpers on four historical tasks, three repeats, with a maximum of 134 agent invocations, 45 minutes of execution wall time and a USD 10 observed API-equivalent soft stop. Already-running invocations may overshoot the cost stop. This is not a subscription-billing cap and does not authorize changes to model defaults or live infrastructure.

## Context

Generated material: `~/ai-data/e01-delegation/2026-11-09-stage2/`. The first synthetic pilot remains [separately recorded](../../../../personal/knowledge/log/2026-11-09-knowledge-base-e01-model-delegation-pilot.md). The prepared corpus contains four cases and thirteen files, including two sanitized timing partitions; private source provenance and rubrics are not supplied as agent task input. Operational task cost includes helpers, final coordination, source verification, correction and failed/incomplete attempts with available usage. Research preparation, independent grading and reporting are disclosed separately.

## Actions

The normal startup sync returned successfully without output or reminders. Read applicable KB procedures and retrieved scoped rules. Rechecked the prepared evidence adapter (13 offline checks) and refreshed the [official API pricing](https://developers.openai.com/api/docs/pricing) through OpenAI Docs: Standard short-context Sol input/cached/output USD 2/0.10/10 and Luna USD 0.10/0.01/0.50 per million tokens, unchanged from preparation. Actual account charges are not observable.

Before any measured outcome, an independent read-only audit verified C01/C03 arithmetic and found two sanitation omissions: `.consul` hostnames and compact assignee values. Corrected these, retained original preparation artifacts and regenerated the corpus/manifest/package hashes. C04 now explicitly accepts the source-supported alternative of robust execution-shell rebinding after inherited environment, in addition to CLI flags. This is a pre-run clarification, not a response to observed arm performance. Global median calculation must use the full timing table or equivalent mergeable data; averaging partition medians is invalid.

Implementation and offline runner checks precede the two reserved preflight invocations. Measured roles use only supplied sanitized evidence and host-side allowlisted JSON evidence requests. Native shell/exec, browsing, apps/plugins, image/computer and nested-agent features are disabled per invocation without persistent configuration edits. Semantic answer review will hide arm, model, repetition, timing and costs until scoring is recorded.

Runner implementation and independent review completed before launch. The offline self-test passed numeric/citation mutations, concurrent quota reservation, cost/wall stopping and process-group cancellation. Review fixes made before measured calls include failed evidence receipts as protocol failures, required final-response type, interrupted unknown usage, end-of-run input integrity and isolation of local packet overflow from global stopping. All four question files and the runner are included in the frozen package hashes. Automatic citation checks validate ranges only; blind review must assess actual support for every numeric and semantic fact and critical evidence from both shards.

Launched the approved single `--execute` entry outside the outer filesystem sandbox because Codex CLI cannot initialize there; child invocations retained read-only sandboxes and disabled native tools. Both reserved preflights passed with no native tool items. The durable ledger, PIDs, exact prompts/events, role/case results and cost totals are under `execution/`. Read-only status command: `python3 ~/ai-data/e01-delegation/2026-11-09-stage2/monitor_stage2.py`. Execution is now finished with no active child entries and no runner process; no stop operation remains.

## Findings

### Completed execution and cost

The runner returned exit 0 after all 36 case attempts. It used 83 base invocations,23 evidence continuations,6 corrections and 2 preflights:114 total, within 134. One delegated attempt stopped before its coordinator because of the 30 KB packet limit, explaining 83 rather than 84 base calls. Execution wall time was 1,927.351 seconds (32.12 minutes), below 45 minutes. The observed API-equivalent total was USD 3.95676266, below the USD 10 soft stop. No limit was increased and no measured prompt/code was changed after launch.

| Policy | Case attempts | Invocations | Operational USD | No-cache sensitivity USD | Sum of attempt times | Median attempt time |
| --- | --- | --- | --- | --- | --- | --- |
| Sol alone | 12 | 18 | 1.262120 | 1.488782 | 502.837 s | 43.527 s |
| Sol + Sol helpers | 12 | 47 | 1.910173 | 2.650960 | 728.225 s | 63.989 s |
| Sol + Luna helpers | 12 | 47 | 0.758135 | 1.060622 | 685.272 s | 57.698 s |

All attempted work, including failed integration, verification and correction, is charged to its policy. Times include failed attempts and therefore are not latency conditioned on acceptance. Preflight cost USD 0.0263355 is outside the three policy totals. Preparation, independent review and reporting overhead are disclosed separately and not represented as a measured complete research bill or actual subscription debit.

Compared with solo, Luna helpers reduced observed attempted-work cost 39.93%, or28.76%without cache discounts, while increasing total attempt time 36.28%. Compared with Sol helpers, Luna reduced cost 60.31%. Sol helpers cost 51.35%more than solo. The Sol coordinator consumed 91.26%of the Luna policy's observed estimate, including verification/correction; making already-cheap workers cheaper is not the principal remaining cost opportunity.

### Blind quality and citation review

Four independent reviewers received case packets without arm, model, repetition, time or cost labels. C03/C04 review began once all nine attempts of each case were complete, while remaining measurement continued; source text was deduplicated and host receipts carried no origin labels. The C04 packet contained eight answers because one attempt produced none. First/final answer hashes were checked when opaque review IDs were joined with the execution mapping only after every review was complete. Original blind judgments remain unchanged.

All 35 available final answers passed the reviewers' scope, conclusion and critical-shard checks. This does not mean that every required fact and citation passed. Full acceptance combines native/protocol health, automatic checks and every mandatory blind fact/citation judgment; missing/uncertain/composite criteria remain visible.

| Case | Solo fully accepted | Sol helpers fully accepted | Luna helpers fully accepted |
| --- | --- | --- | --- |
| C01: S3 evidence | 3/3 | 3/3 | 1/3 |
| C02: Selenium chronology | 1/3 | 3/3 | 0/3 |
| C03: duration and later diagnosis | 0/3 | 0/3 | 0/3 |
| C04: CI target audit | 3/3 | 1/3 | 2/3 |
| Total | 7/12 | 7/12 | 3/12 |

First-pass full acceptance was 4/12 solo,7/12 Sol helpers and 2/12 Luna helpers. These small-sample counts measure this strict protocol, not general model accuracy, safety or statistical equivalence.

Observed exceptions:

- C01: all numeric values were factually correct, including the sixth upload. Six automatic corrections normalized a richer JSON object containing that correct ordinal to the required scalar 6; they were format work, not factual ordinal fixes. Their total observed cost was USD 0.2441416. The generic public response shape allowed objects while the common prompt requested numeric quantitative values, so this is a contract weakness. Keep original first-pass grades and actual cost rather than inventing a cheaper counterfactual. Two Luna answers lacked either the onset/publication limitation or citation support for it.
- C02: missing publisher retry-enqueue DNS detail or the limitation that Ready capacity does not prove all tests passed affected three Luna answers. Two solo answers rendered minute-only evidence as an ISO timestamp with zero seconds; the reviewer marked citation precision uncertain rather than asserting a contradiction. Sol helpers met the full criterion set in all three attempts.
- C03: all nine answers had combined-table computation receipts and correct arithmetic/diagnosis. The composite `attribution_limit` criterion additionally demanded explicit historical-peak and exchange-creator caveats not clearly asked in the question; its evidence range also excluded the peak-usage source line. Every answer missed part of that composite. The issue was recorded in `grading-disputes.pre-unblind.json` before label/score joining. Retain the primary 0/3 scores; excluding only this disputed criterion symmetrically gives 2/3 solo,2/3 Sol helpers and 1/3 Luna helpers. Other omissions, including explicit scale-down evidence, still count. Across all cases this sensitivity gives 9/12,9/12 and 4/12 respectively. It is not a replacement baseline or proof of equal quality.
- C04: one Sol-helper attempt overflowed the 30 KB evidence packet and returned no final answer. A different Sol-helper final answer incorrectly claimed no tools had been used despite local source-read receipts; historical findings otherwise passed. One Luna helper omitted the required final-response type; its coordinator's content passed automatic checks, but the fixed protocol correctly retained the helper contract failure. These are distinct integration/reporting issues, not proof that the historical diagnosis was wrong or that any external action occurred.

### Decision and limits

No case met both the predeclared 20%cost-saving and unchanged-quality condition. Luna saved 21.67%on C01 but lost full fact/citation acceptance; C02 saved only 0.15%and lost completeness; C04 cost 18.06%more and had a format failure. C03 saved 64.44%(53.79%without cache discounts), but the disputed rubric and remaining completeness differences prevent an equal-quality claim.

Under the original strict scores, cost per accepted result was USD 0.1803 solo,0.2729 Sol helpers and 0.2527 Luna helpers. The apparent 40%raw saving therefore did not yield a lower strict accepted-result cost. The rubric limitations mean these ratios must not be presented as universal production economics.

Keep Sol as the current default. The study supports a lower price for Luna workers when delegation is already appropriate; it does not support automatic wholesale delegation or claim that stronger coordination preserves all omitted evidence for free. Any later narrow routing proposal should use explicit typed output, a checklist matching the question, reliable evidence transfer and independent fact checks, then a separately reviewed evaluation. Do not deploy such a policy from this sample.

Solo versus delegation is a policy/context comparison; only the two delegated arms isolate the helper-model substitution. A solo policy that receives deterministic preaggregation before the first model prompt was not tested. Because C03 arithmetic is solved by a local tool, this comparison does not establish that LLM helpers are necessary for that task. Reasoning effort was held at medium; no effort or additional-model comparison was performed.

### Final verification

Independent recalculation confirmed 114 successful native invocations,36 unique attempts, complete input/cache/output usage, zero native tool items, zero infrastructure failures/timeouts, zero cache-write tokens, matching per-call/aggregate cost and all approved limits. Package, runner, question and corpus hashes matched at both ends. `execution/status.json` is `finished`, `active` is empty, and the runner PID no longer exists. All 35 available answers have complete independent review coverage; the packet-overflow attempt is explicitly unreviewable. Evidence: `independent-verification.json`, `comparison-final.json`, `sensitivity.json`, original blind judgments and pre-unblinding dispute records.

## Changes

Generated runner/artifacts and KB bookkeeping only. The existing central E01 stage-2 item is closed with the bounded result. The user subsequently retained single-agent Sol and closed the E01 follow-up proposal without implementation. No historical incident is reopened; no application repository, remote service or CI job is changed.

## Status and risks

The approved bounded comparison is complete, including all 36 attempts, independent blind review and accounting verification. One attempt had no final answer because of the packet limit; another failed a helper response contract. These limitations and rubric ambiguities remain in the result rather than being silently rerun or discarded. Task-affected KB/TODO statuses are reconciled: the authorized comparison is complete and the user closed the E01 follow-up without implementation. Research preparation/review/reporting overhead is separate from the operational arm estimates; no exact monetary total for the full research activity or actual subscription debit is asserted. No new baseline/run or automatic delegation is planned.

## Single Sol decision

On 2026-11-09 the user decided: `Оставляем Sol одну`. Retain one Sol agent as the default; same-model or cheaper helpers require explicit task authorization. The former automatic helper trigger based on file count or log length is superseded in the canonical economical-tool-use rules. Runtime model configuration is unchanged. Close the E01 refinement/further-run proposal as declined, not implemented; preserve all measured results and grading limits. Other proposed experiments and unrelated context/resumption improvements remain untouched.

## Portable lesson

none
