---
system: knowledge-base
status: verified
checked: 2026-11-09
tags: [agents, evaluation, cost, preparation]
---
# E01 stage 2: historical corpus, evaluation criteria and proposed budget

## Summary

Prepared four historical tasks with two independent evidence shards each.
The largest case contains 1,590 sanitized timing rows and related diagnosis notes.
Fixed source hashes, questions, numeric oracles and semantic/citation criteria are retained.
The proposed comparison has three arms, three repeats and 84 base agent invocations.
Shared reserves raise the absolute invocation ceiling to 134, with a 45-minute ceiling.
The uncached base planning estimate is USD 4.1–5.1; USD 10 is a soft usage stop.
Actual subscription charges and a hard account spending cap are not observable here.
Thirteen offline evidence-adapter checks passed at the preparation checkpoint.
The user subsequently approved execution; the separate comparison record holds its completed outcome.
Read Findings for assignments, scoring and budget; Status and risks records the scope.

## Task

Prepare the second E01 model-delegation comparison after the user requested preparation only. Deliver concrete historical assignments, sanitized local snapshots, acceptance criteria and a proposed execution budget. Comparative model runs remain pending approval of this package; preparation does not authorize infrastructure diagnostics, deployment or changes to model defaults.

## Context

The [first pilot](../../../../personal/knowledge/log/2026-11-09-knowledge-base-e01-model-delegation-pilot.md) found that delegation did not beat solo on six short synthetic tasks. Its strict next-action mismatch also exposed an ambiguous rubric. Stage 2 therefore uses substantial retained evidence, arithmetic checked independently, and fact/citation grading that accepts valid semantic alternatives.

Company source provenance belongs in this layer. Generated material is in `~/ai-data/e01-delegation/2026-11-09-stage2/`: `prepared/`, `manifest.json`, `rubrics.private.json`, `source-provenance.private.json`, `protocol.json`, the preparation script and an offline allowlisted evidence adapter. Private provenance, answer keys and alias mappings are not part of agent input. The old `prepared-attempt1/` folder is an excluded preparation attempt, not an additional case or measurement.

## Actions

One read-only preparation assistant inspected candidate source sections and verified exact answer anchors; the parent retained all writes. No comparative Sol/Luna run or external service access was performed. Existing full logs were not mined: the 115 MB Jenkins console was excluded. The retained timing table supplies the substantial structured-data case.

Created line-preserving snapshots of eleven historical notes and two partitions of 1,590 timing rows. Removed timing free-text names/descriptions, replaced hostnames, IPs, paths, organizational/ticket/object identifiers and identified assignee values, while preserving numeric data, dates, versions and equality relationships. Targeted checks passed; this is bounded sanitization rather than proof of general secret/PII detection. Do not import the original publisher configuration warned about in the Selenium note.

An initial private-IP check incorrectly matched partial decimal/date strings; corrected it to require complete IPv4 addresses, retained the first attempt separately and reran preparation successfully. No benchmark score was affected.

## Findings

### Prepared assignments

| Case | Retained corpus | Size | Independent helper work and acceptance evidence |
| --- | --- | --- | --- |
| C01: upload latency | Two Content S3 notes | 32,882 bytes | Seven-upload timeline versus separately sampled PUT/provider evidence; check counts, 37.729 s total, 30 s deadline, sample values and explicit final closure without overstating causal/onset proof. |
| C02: Selenium recovery | Three failure/recovery notes | 16,290 bytes | Earlier registration/DNS/retry failures versus later manual and demand-driven capacity evidence; distinguish requested from Ready workers and retain unknown historical root cause. |
| C03: test duration | Four diagnosis notes plus two timing partitions | 101,430 bytes | Independent timing partitions plus latency/autoscaling/causal evidence; recompute 1,590 rows, status totals and 180,661 s, and reconcile the later RabbitMQ diagnosis with earlier uncertainty. |
| C04: CI target audit | Two mock-service recovery notes | 35,396 bytes | Initial inherited-variable conflict versus independent correction/acceptance; explicit Nomad address/token references, conflicting-placeholder test and final accepted versions, preserving unrelated build behavior. |

Sources are historical snapshots, not current operational checks. C01 is a development case; C02–C04 are held out from later tuning. C02 deliberately retains a realistic smaller documentary task rather than adding irrelevant filler. C03 is the volume case. The exact eleven source paths, hashes, original sizes, aliases, shard membership and answer ranges are retained in the preparation artifacts.

Representative canonical sources: [Content comparison](2026-10-19-content-selectel-s3-put-latency-comparison.md), [Selenium recovery](2026-10-19-jenkins-selenium-vk-scale-observation.md), [duration attribution](2026-10-20-web-autotests-jenkins-2006-duration-api-latency.md), [subsequent messaging diagnosis](2026-10-20-nomad-test-test1-monolith-rabbitmq-exchange-latency.md), [Nomad target audit](2026-10-16-nomad-test-devops-898-houstonv2mock-vk-assessment.md) and [later mock acceptance](2026-10-21-nomad-test-recommendations-mock-vk.md).

### Proposed comparison and scoring

Keep GPT-6.1 Sol as solo/coordinator, with either two Sol helpers or two GPT-6 Luna helpers; medium reasoning and requested default service tier in all arms. Fixed two-shard assignments and identical prompts isolate the helper-model substitution between the two delegated arms. Solo versus delegation compares complete policies, including context distribution. No separate model planner is assumed free: decomposition is predetermined for these narrow tasks, and this limit must be reported.

Three repeats across four cases and three arms produce 36 case-runs and 84 base agent invocations. Rotate arm order by Latin square and record cache usage. The coordinator receives helper results with original citation windows supplied by the harness, and verifies at least one critical fact from each shard. Additional allowlisted evidence requests and any final correction are charged fully, including failed or incomplete attempts with available usage.

The evidence adapter permits only fixed-corpus `read_source` and `aggregate_timings` operations. Reads require valid source hashes and exact allowed filenames/ranges; aggregation receives only the role's assigned timing files. All arms have the same arithmetic tool, so models are not expected to add 1,590 numbers mentally. Tool results, re-reads and continuations consume input tokens and wall time; this local work is not excluded from the cost of verification. No shell, browsing, plugins, live endpoints or original private paths are required in measured agent turns.

Score mandatory supported facts, arithmetic tolerances, valid citations and scope preservation; permit equivalent prose and multiple valid next steps. Semantic review should be blinded to arm identity. Preserve the frozen rubric and record disputed criteria with a symmetric sensitivity analysis rather than tuning after held-out results. Report first-pass acceptance separately from final corrected acceptance/cost. A task class qualifies for a routing proposal only with at least 20% lower total cost than solo, no fact/citation/scope regression and no material extra human correction; three repeats do not establish broad reliability or statistical equivalence.

### Proposed execution budget

- Base: 84 agent invocations. Shared reserves: 36 evidence/verification continuations, 12 final corrections and 2 preflights; absolute invocation ceiling 134. These are Codex invocations, not an assertion about invisible provider request counts.
- At most two helper invocations concurrently; 120-second timeout per invocation; 45-minute total wall-time ceiling. Stop and report incomplete results if limits are exhausted.
- Uncached base estimate: USD 4.114–5.046, using the first pilot's previously inspected Standard API rates, measured approximately 16k fixed native-context tokens, two byte/token heuristics, a 30 KB coordinator evidence envelope and 2,000 output tokens per base invocation. These are planning scenarios, not tokenizer measurements or confirmed account charges. Refresh rates before an approved run.
- Proposed stop threshold: USD 10 observed API-equivalent usage, checked after each invocation; stop launching further calls. Already-running calls may overshoot. The CLI does not provide an enforceable subscription-billing cap; do not present this threshold as a hard spending guarantee.
- Keep preparation, blinded evaluation/reporting overhead and actual subscription debits separate from operational per-task comparisons. Missing native usage makes the cost comparison incomplete; never assign an unknown failed call zero cost.

Rate basis: the earlier inspected [official API pricing](https://developers.openai.com/api/docs/pricing), Sol input/cached/output USD 2/0.10/10 and Luna USD 0.10/0.01/0.50 per million tokens. No fresh model-selection recommendation or changed account-price claim is made during preparation.

### Offline validation

Preparation checks passed: source hashes, exact/disjoint two-shard coverage, line-preserving sanitization, known identifier/private-path/private-IP checks, answer-range bounds, preserved timing fields/order/counts, recomputed arithmetic and a deliberately changed numeric fixture.

The evidence adapter passed 13 offline checks: whole-table oracle equality, partial aggregation reconciliation, cross-shard/path-traversal refusal, oversized/invalid range reporting, numbered read receipts with continuation, unknown/malformed requests, non-timing aggregation refusal, changed-source detection and missing-source failure reporting. These checks invoke no models and demonstrate local adapter behavior only.

Final package verification confirmed the preparation-script/package hashes, all 13 corpus-file hashes, 84/134 invocation arithmetic and absence of a benchmark output directory. Task-affected notes and TODO agree: preparation is finished, review/execution remains proposed. The affected display title renders under Knowledge base. Full KB lint passed with zero errors and zero warnings.

## Changes

Created local preparation artifacts and this company work log. Linked the prepared second stage from the first-pilot record and recorded pending approval/execution in the central TODO. No runtime agent configuration, repository code, infrastructure, external tracker or model routing was changed.

## Status and risks

At the preparation checkpoint, the proposed comparison had not started and stage-1 runner adaptation/preflight remained pending. That historical preparation status is retained here; the subsequent execution record below supersedes it.

Subsequent decision on 2026-11-09: the user authorized launch of the comparison. The [execution record](2026-11-09-knowledge-base-e01-stage2-comparison.md) now owns its implementation, preflight, measurement and final status. A pre-outcome independent audit required additional hostname/compact-assignee redactions and acceptance of a source-documented robust shell-rebinding alternative for C04; original preparation artifacts are retained and the amended package is hashed before measured calls. This does not reopen historical incidents or authorize changes to model defaults.

Final outcome on 2026-11-09: all 36 attempts completed within the approved limits using 114 invocations in 32.12 minutes. Four independent blind reviews and accounting/input-integrity checks finished. Luna lowered raw operational cost but did not establish equal quality; no routing change was adopted. The user subsequently retained one Sol agent and closed the E01 follow-up/refinement proposal without execution; other experiments remain proposals.

Historical decisions remain historical: closed incidents stay closed, later documented corrections supersede earlier pending steps, and no new infrastructure work is authorized. Generated snapshots and answer keys remain outside Git; approved execution must verify their hashes and preserve the separation of source evidence from expected answers. No comparative model run, background command or preparation assistant remains active at completion.

## Portable lesson

none
