---
system: agents
status: verified
checked: 2026-11-19
tags: [agents, experiments, evaluation]
---
# E03: reporting partial tool failures

## Task

On 2026-11-19 the user selected E03 and then asked to run it. The pilot tested how the agent reports partial tool failures.

## Method

Three synthetic transcripts were paired across six fresh Codex CLI 0.170.0 sessions
using `gpt-6.2-sol` at medium effort. Each pair used the same task and transcript.
Arm B added one paragraph asking the agent to inspect exit status, diagnostics and
output coverage and to report verified and unresolved facts. Order was A/B, B/A, A/B.
The initial client launch stopped before a model turn because the outer sandbox
prevented initialization. The retry ran with the CLI's read-only shell policy,
ephemeral sessions and user configuration disabled.

A case passed if the first final answer matched the rubric below without an
unsupported claim. The evaluator knew which arm produced each answer.

## Findings

| Case | Correct interpretation | A | B |
| --- | --- | --- | --- |
| Complete search, zero matches | No records found in the queried catalog | Pass | Pass |
| Source unavailable, misleading zero in stdout | Search failed and record existence is unknown | Pass | Pass |
| Viewer limited to two of three rows | Confirm north and east, leave west unverified | Pass | Pass |

Six distinct thread IDs and six completed turns with usage were verified. The
event exports showed no tool calls. Combined model-process time was 44.85 seconds,
excluding the initial client startup failure, preparation and scoring. Reported
usage was 111,752 input tokens including 82,176 cached input tokens and 242 output
tokens. Arm B added 120 input and 44 output tokens across the three pairs.
The per-case answers, receipts, rubric and runner are retained locally in
`~/ai-data/e03-partial-failures/2026-11-19/` for audit and reproduction.

## Status and risks

Completed on 2026-11-19. Both arms passed three of three cases. This comparison
provides no evidence that adding the paragraph improves correctness. One trial
per arm and case, an unblinded grader and fixed synthetic transcripts limit the
conclusion to interpretation and reporting in these cases. End-to-end recovery
with real tool execution was outside the pilot.

The [experiment plan](2026-11-06-knowledge-base-merged-agent-experiments.md#e03-selection-november-19)
and the [central TODO](../../../TODO.md#knowledge-base) record the closure.

## Task metrics: E03-2026-11-19

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "E03-2026-11-19",
  "created": "2026-11-19T00:18:35.348306+03:00",
  "first_result": "pass",
  "final_result": "pass",
  "state": "closed",
  "kind": "experiment",
  "model": "gpt-6.2-sol",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Six completed turns and three paired rubric judgments in Findings",
  "updated": "2026-11-19T00:19:34.038443+03:00"
}
```
