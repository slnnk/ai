---
system: knowledge-base
status: verified
checked: 2026-11-09
tags: [agents, evaluation, cost, delegation]
---
# E01: bounded model delegation and whole-task cost pilot

## Summary

Completed 18 pack-runs, 42 calls and two repeats on six synthetic tasks.
Compared Sol alone, Sol helpers and Luna helpers at medium reasoning effort.
All participants finished normally; no tools, external actions or canary leaks occurred.
Solo was cheapest and fastest on these short inline tasks.
Luna helpers cost less than Sol helpers but did not beat solo, including without cache discounts.
One strict next-action label mismatch is retained with a documented rubric ambiguity.
All worker and final coordinator usage is counted; research setup costs are separate.
Actual subscription charges and the complete research monetary cost are unknown.
No permanent routing/configuration change was made; E02–E14 remain proposals.
Read Findings for measurements and grading limits, and Status and risks for applicability.

## Task

Run selected experiment E01 from the [merged plan](2026-11-06-knowledge-base-merged-agent-experiments.md#merged-experiments): compare a capable model alone, the same coordinator with same-model helpers, and the same coordinator with cheaper helpers. The user authorized this experiment explicitly. This does not authorize permanent model-routing changes or other experiments.

## Context

The [central backlog](../../../TODO.md#knowledge-base) retains all other proposals.
Generated fixtures, frozen protocol, harness, per-call prompts/events/results, per-pack grading and summaries live in `~/ai-data/e01-delegation/2026-11-08/`. Preparation started November 8; execution and completion are dated November 9, Moscow time. Artifacts are outside Git and contain synthetic evidence only.

Official sources inspected before model selection:

- [Models](https://learn.chatgpt.com/docs/models): Luna is positioned for focused repeatable tasks.
- [API pricing](https://developers.openai.com/api/docs/pricing): observed Standard short-context rates per million input/cached-input/output tokens were USD 2/0.10/10 for GPT-6.1 Sol and USD 0.10/0.01/0.50 for GPT-6 Luna. These are API-equivalent estimates, not measured subscription debits.

## Actions

Used Codex CLI 0.167.0 with requested `service_tier=default`, `model_reasoning_effort=medium`, ephemeral sessions and read-only child sandboxes. No permanent config was edited. Models received inline synthetic evidence and a no-tools contract. The outer startup, sync and rule retrieval were performed once by the parent rather than repeated by helpers.

Before measured runs, fixed three packs of two independent tasks each: log diagnosis/counting; instruction cancellation and evidence freshness; publication receipts and scanner failures. The first pack is the development set; the other two are held out. No prompt tuning after their outcomes is allowed. Each arm runs twice: 18 pack-runs and 42 model calls, with zero retries and a 100-second per-call timeout. Helper calls run in parallel; the final coordinator receives both original tasks and helper drafts and verifies the answers. Decomposition is fixed by the harness; there is no separate model planner.

Validated grading before freezing: three positive packs and 45 negative mutations passed the controls. Acceptance requires exact requested JSON fields, types and values, successful tool completion, no tool invocation and no canary disclosure by any participant. All participants, including failed calls with available usage, contribute to cost. A missing usage record makes the comparison incomplete. The predeclared usefulness threshold is at least 15% lower total cost or wall time versus solo with no correctness/constraint regression.

Balanced arm order across six blocks; recorded uncached/cached input, output and reasoning counts, subprocess return codes, elapsed time and worker/coordinator shares. Reasoning tokens are reported as a subset of output, not added a second time. Also calculate a no-cache sensitivity estimate. Full inherited Codex context is included in the native token totals.

Preflight initially failed on an invalid CLI option position and then the outer sandbox's read-only filesystem. Corrected option placement and obtained execution approval outside the outer sandbox while preserving read-only child sandboxes. These are setup failures, not model-quality failures. The subsequent Luna preflight returned the requested readiness JSON. Setup traces are retained separately.

## Findings

All 18 pack-runs and 42 model calls finished normally, with complete usage, no retries, no tool invocations, no canary disclosures and zero cache-write tokens. Whole-run wall time was approximately 244 seconds. The comparison below sums the same six pack-runs per arm; helper parallelism is already reflected in pack wall time.

| Arm | Strict accepted packs | Model calls | Total pack time | Median pack time | API-equivalent USD | No-cache USD |
| --- | --- | --- | --- | --- | --- | --- |
| Sol alone | 6/6 | 6 | 51.382 s | 8.545 s | 0.062504 | 0.193832 |
| Sol + two Sol helpers | 6/6 | 18 | 98.934 s | 16.219 s | 0.346492 | 0.577532 |
| Sol + two Luna helpers | 5/6 | 18 | 93.869 s | 14.941 s | 0.078189 | 0.202354 |

Total measured model-call estimate across all three arms: USD 0.487185. This includes all helper calls and final coordinator verification. It excludes experiment development, reporting and preflight; it is not the complete monetary cost of conducting the research or the actual subscription charge.

Replacing Sol helpers with Luna reduced the delegated policy's estimated cost by 77.43% with observed caching, or 64.96% under the no-cache sensitivity calculation. However, compared with Sol alone, the Luna policy cost 25.09% more with observed caching, or 4.40% more without cache discounts, and took 82.69% more total pack time. The coordinator accounts for 84.02% of the Luna policy's observed estimate. Neither delegated policy meets the predeclared usefulness threshold against solo. The result supports avoiding delegation overhead for these short inline tasks; it does not establish the best policy for larger independent workloads.

### Strict mismatch and grading limitation

In `logs-r2-cheap`, the Grid helper selected `report_observed_limits` instead of the frozen expected `request_recovery_approval`. The Sol coordinator retained that choice despite having the original evidence. Every other field in that pack was correct. Helper grading shows one mismatching helper answer out of 24 helper invocations; no forbidden action was executed or allowed.

The question requested a next action but did not explicitly require asking for recovery approval rather than merely reporting diagnostic limits. Both enum labels remain compatible with read-only diagnosis. Therefore retain the original strict 5/6 result, but do not characterize this isolated mismatch as an established safety or substantive correctness regression. The narrow rubric cannot justify a general reliability comparison. This limitation was identified during inspection and the frozen fixture, prompts and scoring were not changed or rerun to improve the result. The cost/time rejection relative to solo does not depend on treating this label mismatch as a real defect.

### Verification

Grader controls passed before freezing: three positive packs and 45 negative mutations. Independent post-run checks confirmed unchanged script/fixture SHA-256 values, 18 unique expected pack-runs, 42 successful participant calls, complete usage, no tools/canary leakage, valid token relationships and independently recomputed per-call and aggregate costs. Evidence is in `verification.json`; native traces and grading remain alongside each call. The runner returned exit 0, `status.json` says `finished`, and its process no longer exists.

Task-affected note/TODO reconciliation is complete: E01 selection is closed, remaining E02–E14 selection is open, and the broader context/coordination proposal records only its completed pilot subpart. The two affected Russian display titles render under Knowledge base. Full KB lint completed with zero errors and zero warnings.

## Changes

Created generated experiment artifacts and this work log; linked the completed bounded E01 outcome from the merged plan and central TODO, retaining E02–E14 and all other unfinished proposals. No application repository, skill, instruction, model default or external system was changed by the experiment.

The daily authorized sync independently failed its GitFlic push with `failed to lock`; its local state is retained for a later normal retry. This is unrelated to experiment correctness.

## Status and risks

The bounded E01 pilot is complete. No experiment command or child model process remains running. The parent owns all KB/TODO/index changes; child agents had no bookkeeping role. No permanent routing change is recommended from this sample. Remaining experiments and broader context/coordination proposals are still open in the central backlog, without authorization to execute them.

On 2026-11-09 the user requested preparation and subsequently authorized launch of a second stage. The [prepared historical corpus](../../../current/knowledge/log/2026-11-09-knowledge-base-e01-stage2-preparation.md) and [completed comparison](../../../current/knowledge/log/2026-11-09-knowledge-base-e01-stage2-comparison.md) are separate from this synthetic pilot. Stage 2 completed 36 attempts/114 invocations with complete accounting and blind review: Luna reduced raw operational cost but equal quality was not established. No permanent routing change was adopted. The user subsequently chose one Sol agent and closed E01 continuation; helpers require explicit task authorization.

This is a bounded pilot of six short synthetic tasks, not evidence for arbitrary development work, long code searches, production diagnosis, tool-heavy tasks or the best available decomposition. Both delegated arms retain full original evidence at the coordinator, so verification is charged rather than assumed free. Startup/routing changes belong to separate proposals. Cache state cannot be reset; balanced order and uncached sensitivity do not provide a fully controlled cold-cache latency comparison.

The cost of building and reporting the experiment is separate from the measured per-task policy cost. An outer-session token checkpoint is retained in `outer-checkpoint.json`; it is a lower bound through that checkpoint, not a completed bill. Actual subscription debits and the final outer-session monetary total are unavailable. No general savings claim is justified by cheaper helper rates alone.

## Portable lesson

none
