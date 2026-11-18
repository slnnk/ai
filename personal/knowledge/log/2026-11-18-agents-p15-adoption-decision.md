---
system: agents
status: verified
checked: 2026-11-18
tags: [agents, learning, evaluation, pilot]
---
# P1.5 learning pilot adoption decision

## Summary

Retain the current agent-learning workflow and decline the tested replacement
paragraph. The selected pilot showed equal first-delivery performance and human
steering in four historical replay pairs. The treatment consumed more input tokens.
The pilot supports a decision about this candidate, with limited evidence about
transfer on future work.

## Task and context

Decide adoption using the [P1.4 result](2026-11-14-agents-p14-transfer-protocol.md#final-pilot-result-on-november-18)
and the [P1.5 criterion](2026-11-14-agents-personalized-learning-backlog.md#prioritized-design).
The comparison tested one paragraph from the
[P1.3 design](2026-11-14-agents-p13-canonical-reconciliation.md).
A successful decision accounts for first-attempt quality, human steering, observed
resource use, maintenance and limits of the comparison.

## Findings

- Both arms passed 4/4 first attempts, including both applicable cases and both
  controls. Both needed zero human corrections. There were zero observed critical
  events. The additional verified Git finding in B did not change the frozen
  first-delivery score.
- The pilot totals receipt confirms 602,039 input tokens for A and 672,088 for B.
  B used 70,049 more input tokens (+11.6%), 231 fewer output tokens and two fewer
  seconds of measured process time. These figures exclude preflight for the arm
  comparison. Cached input is a subset. End-to-end labor and monetary costs are
  unknown. Unnecessary actions were not independently scored.
- The candidate would replace one paragraph in the existing skill, with the same
  owner and no new service or dependency. The extra decision instructions and
  observed input volume have no demonstrated primary benefit to justify adoption.
- The assessment covered four historical replays at one setting with one attempt
  per arm per task. The pilot author scored labeled artifacts. Prospective transfer,
  generalization and other parts of the P1.3 patch remain unmeasured.

## Changes and status

The P1.5 decision was recorded in the central TODO and linked to the research
record. The existing agent-learning skill and knowledge base continue to own the
workflow. The pilot and candidate files remain available as historical evidence.
P2.1 and P3.1 remain conditional because this pilot established neither a lifecycle
timing bottleneck nor a persistent limitation requiring a different runtime.
Reconsider adoption if real work exposes a concrete recurring gap and a bounded
change demonstrates a first-attempt or human-steering improvement without an
unacceptable correctness, scope, or cost tradeoff.

## P2.1 closure

On November 18 the user closed P2.1 because the pilot found no need for lifecycle
automation. The proposal was closed without a hook trial or workflow changes.

## Portable lesson

[Correction learning](../../../general/knowledge/agents/correction-learning.md).

## Task metrics: kb-p15-20261118

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "kb-p15-20261118",
  "created": "2026-11-18T23:14:37.675180+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "decision",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "P1.5 adoption decision and reconciled TODO based on P1.4 criteria, measured arm totals and evidence limits.",
  "updated": "2026-11-18T23:14:37.675231+03:00"
}
```
