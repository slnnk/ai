---
system: agents
status: verified
checked: 2026-11-14
tags: [agents, metrics, learning]
---
# Daily task metrics and evidence-based agent learning

## Task and decision

The user requested collecting agent effectiveness metrics and having an agent analyze
examples and record conclusions about once a day. They selected the first agent
interaction of the day, explicitly without a background model, in session
01a1d727-6401-7be0-ab41-a4ea664e6a74 (daily review timing answer). This authorizes local
implementation in the existing learning/sync flow, not a scheduler or external model
service. Existing standing permissions and unrelated changes are preserved.

## Expected result

One stable record per substantive task, first-attempt and final outcomes kept separate,
unknown counts not converted to zero/success, existing rule events not counted as
tasks. Normal sync prepares a snapshot even when Git already synced; read-only modes
remain read-only. The active agent analyzes and saves findings before acknowledgment.
A failed or unfinished review remains pending; another same-day call does not repeat
completed work. Days without active agents are covered on a later review rather than
being claimed as daily autonomous executions.

## Implementation

Added standard-library agent_metrics.py, reusing learning-store validation, locking
and atomic writes. Task JSON blocks live in existing log notes for durable KB sync;
updates reuse the task ID. Snapshots/receipts are generated under ai-data/agent-metrics.
The first snapshot covers seven completed days; later intervals start at the last
reviewed boundary and exclude the current day. An unfinished snapshot is immutable
until acknowledgment. The marker checks the snapshot hash and saved note sections;
it does not prove the semantic correctness of the agent's analysis.

Integrated prepare before ai-sync's same-day Git skip. Skill instructions cover task
registration/update and daily source review; README supplies the startup trigger and
operations reference supplies commands. No AGENTS.md growth, new skill, database,
package, model daemon or external timer. Resource reference reuses token_usage.py;
it is a rolling seven-day session cohort, not precise daily or task-level expenditure.
Task tokens/time remain unknown unless an attributable measurement is available.

## Validation

Eleven focused checks cover stable IDs, failure retention, unknown denominators,
intervals, duplicate/corrupt records, missing roots, pending review reuse, saved-evidence
requirements, modified snapshots, missed days and the same-day sync trigger.
The initial run exposed Python3.8 Path compatibility; replaced is_relative_to with
relative_to handling and all eleven passed. This is an internal test correction,
not a user correction or a failed first delivered task result.
Final verification:12 metrics tests and22 existing sync tests passed; agent lint reported0errors/warnings/info, learning-store check validated69records and KB lint reported0errors/warnings. Live prepare produced the baseline; a saved source-backed analysis was acknowledged and a second prepare emitted no reminder. Source confinement and malformed/null blocks were checked; unavailable resource collection remains explicit.

## Status and limits

Collection requires agents to register/update task outcomes as instructed. The script
does not infer correctness from silence or parse every conversation into tasks.
Coverage outside registered records is unknown. No historical task success rate is
fabricated. Comparable task trends need subsequent evidence; the existing November20
review remains open and independent. Metric conclusions do not authorize policy or
infrastructure changes. First live preparation/review and final checks follow below.

## Related design

[Metric definitions and prioritized work](2026-11-14-agents-personalized-learning-backlog.md#effectiveness-metrics-proposal).
The source task examples/design and behavioral pilots remain open; implementing
collection does not complete them.

## Portable lesson

See the existing [agent-learning workflow](../../../general/skills/agent-learning/SKILL.md#daily-metrics).

## Task metrics: 01a1d727-daily-metrics

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "01a1d727-daily-metrics",
  "created": "2026-11-14T02:50:07.691426+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "code",
  "model": "gpt-6-astra",
  "session_id": "01a1d727-6401-7be0-ab41-a4ea664e6a74",
  "corrections": 0,
  "unnecessary_actions": null,
  "critical_events": 0,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Expected behavior verified by 12 focused and 22 sync checks plus live prepare-review-complete flow; no user corrective intervention or external mutation; first-delivery acceptance and task resource attribution unknown",
  "updated": "2026-11-14T02:53:17.543759+03:00"
}
```

## Completion

The [first daily analysis](../../../current/knowledge/log/2026-11-14-agents-daily-metrics-review.md)
was saved and acknowledged. Live state has reviewed_on2026-11-14 and no pending
snapshot. It found missing historical task coverage and a label distinction between
new task preferences and repeated known-rule failures. Existing P0.1 and the November20
review retain those actions; other pilot tasks remain unchanged. No background process
or timer remains. Subsequent daily activation depends on agents invoking normal sync
and following the skill; this has not yet been observed on a later real day.

## Subsequent P0.1 preparation

The source case design and metric calibration previously left open above were
[completed locally on November14](2026-11-14-agents-p01-decision-cases-metrics.md).
Behavioral transfer trials remain separately proposed in P1.4; collecting metrics
and preparing examples are not evidence of improved transfer.
