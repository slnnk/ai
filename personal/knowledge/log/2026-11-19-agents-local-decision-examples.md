---
system: agents
status: verified
checked: 2026-11-19
tags: [agents, learning, rules]
---
# Apply decision examples through agent-learning

## Task

The user asked to retain Codex and use practical Letta and Hermes ideas in local rules.
They authorized implementation after discussing linked examples for recurring mistakes
and placing proven procedures in existing skills.

## Context

[P0.2](2026-11-14-agents-p02-learning-search-comparison.md#recommended-bounded-design)
prepared this approach. The [P1.5 decision](2026-11-18-agents-p15-adoption-decision.md)
declined the previously tested paragraph after tied first-attempt results and greater
token use. This change is limited to linked examples for specific choices.

## Actions

Placed the read trigger in the existing scoped lookup step and the capture trigger
in the recurring-error step. Reused the capability-inspection example already written
in P0.1. Linked it from the existing simplest-sufficient-solution evidence record.
Updated the learning CLI to preserve notes below the data block when rewriting a record.
The regression test reproduced a lost link on evaluation, then verified preservation
across both evaluation and occurrence updates.

## Findings

The example records the rejected tool acquisition path, ordinary checkout with
available tools, and the missing-tool or immutable-revision conditions that can
justify another approach. It illustrates one documented loaded-rule failure.

## Changes

The [agent-learning skill](../../../general/skills/agent-learning/SKILL.md#before-related-work)
now calls for consulting a linked example before making the relevant choice.
The [repeated-error procedure](../../../general/skills/agent-learning/SKILL.md#if-the-error-repeats)
uses existing records and existing skills. The [first link](2026-11-12-agents-agent-learning-record-simplest-sufficient-solution-4cedeecedfca84d648d0.md#decision-example)
reuses historical evidence. Git and canonical Markdown provide revision history.

## P3.1 closure

On November 19, backlog reconciliation closed the conditional runtime pilot
without running it. P0.2 documented the mechanisms and found no established
benefit that required changing runtimes. P1.5 found no persistent limitation
requiring a different runtime in the four historical pairs. The user chose to
retain Codex and apply the selected practices locally. Future behavioral
outcomes can be evaluated under the existing rule-task process. A new comparison
would require a concrete recurring gap that smaller changes cannot address.

## Portable lesson

[Correction learning](../../../general/knowledge/agents/correction-learning.md).

## Task metrics: agents-local-decision-examples-20261119

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "agents-local-decision-examples-20261119",
  "created": "2026-11-19T00:06:15.929033+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "skills",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Runtime skill lookup and the first linked example verified; all 18 learning tests passed, including preservation across evaluation and occurrence updates; future decision quality remains unmeasured.",
  "updated": "2026-11-19T00:06:15.929081+03:00"
}
```
