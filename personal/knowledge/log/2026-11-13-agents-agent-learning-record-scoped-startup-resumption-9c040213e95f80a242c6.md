---
system: agents
status: verified
checked: 2026-11-25
tags: [agents, learning]
---
# Agent learning: scoped-startup-resumption

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-13T22:53:49.425699+00:00",
  "decisions": [],
  "evaluations": [
    {
      "at": "2026-11-13T22:59:54.596879+00:00",
      "cause": "Rule available in active context; README sections were unnecessarily reread at closure task entry.",
      "event_id": "scoped-startup-resumption-2026-11-14-closure-read",
      "expected": "Read detailed instructions at their task/action triggers; reuse fully available current rule text; retain sync, scoped learning queries and permissions; keep goal, scope, approvals, decisions, checks and next step in an existing long-task record.",
      "outcome": "fail",
      "revision": 1,
      "rule_loaded": "yes",
      "source": "personal/knowledge/log/2026-11-14-knowledge-base-scoped-startup-resumption.md#evaluation-decision; observable repeated README read in closure turn",
      "target": "/home/slnnk/ai/general/knowledge/README.md"
    },
    {
      "at": "2026-11-24T22:48:55.758553+00:00",
      "cause": "Unnecessary reread of current instruction text at follow-up entry; daily sync and scoped query were separate required steps.",
      "event_id": "2026-11-25-local-kb-rating-startup-follow-up",
      "expected": "Read detailed instructions at their task/action triggers; reuse fully available current rule text; retain sync, scoped learning queries and permissions; keep goal, scope, approvals, decisions, checks and next step in an existing long-task record.",
      "outcome": "fail",
      "revision": 1,
      "rule_loaded": "yes",
      "source": "November 25 follow-up to local KB rating about short-task startup overhead: first exec reread README lines 207-244 and 405-425, already fully visible from the preceding turn.",
      "target": "/home/slnnk/ai/general/knowledge/README.md"
    }
  ],
  "expected": "Read detailed instructions at their task/action triggers; reuse fully available current rule text; retain sync, scoped learning queries and permissions; keep goal, scope, approvals, decisions, checks and next step in an existing long-task record.",
  "key": "scoped-startup-resumption",
  "kind": "explicit",
  "layer": "personal",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-13T22:53:49.425699+00:00",
      "cause": "",
      "event_id": "context-simplification-2026-11-14-user-start",
      "expected": "Read detailed instructions at their task/action triggers; reuse fully available current rule text; retain sync, scoped learning queries and permissions; keep goal, scope, approvals, decisions, checks and next step in an existing long-task record.",
      "source": "personal/knowledge/log/2026-11-14-knowledge-base-scoped-startup-resumption.md#task; conversation user reply: Начинай",
      "summary": "User approved task-scoped startup reading and compact state in existing long-task records after a concrete proposal."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "global",
  "summary": "User approved task-scoped startup reading and compact state in existing long-task records after a concrete proposal.",
  "system": "agents",
  "target": "/home/slnnk/ai/general/knowledge/README.md",
  "task_id": "",
  "updated": "2026-11-24T22:48:55.758553+00:00",
  "version": 1
}
```

## Decision example

On November 25 the user approved a check at the point where the agent chooses to
reopen a source. In the follow-up about short-task overhead, the agent reread two
current README sections already available in the same session. Before a repeat
read, identify the excerpt needed and why the existing context is insufficient.
Reuse the excerpt for an explanation within the same scope. Read the relevant
source when the excerpt is missing, potentially stale, or needed for new scope.
See the [canonical example](../../../general/knowledge/README.md#task-context-selection).

At the next naturally occurring same-task follow-up in a fresh session where the
agent already read the relevant source, use the first tool calls as evidence and
record one applicable outcome under this key. Required sync and rule lookup are
outside the repeat-read check. Fresh-session evidence is pending.
