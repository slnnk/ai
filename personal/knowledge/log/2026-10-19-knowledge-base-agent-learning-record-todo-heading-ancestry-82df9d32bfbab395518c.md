---
system: knowledge-base
status: verified
checked: 2026-11-15
tags: [agents, learning]
---
# Agent learning: todo-heading-ancestry

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-10-19T21:35:30.749798+00:00",
  "decisions": [],
  "evaluations": [
    {
      "at": "2026-11-14T00:07:07.452510+00:00",
      "cause": "",
      "event_id": "p01-20261114-todo-ancestry",
      "expected": "Choose TODO section by task subject and source; inspect full Markdown heading ancestry before adding or moving; verify affected rendered heading path using todo.py, or source ancestry for closed entries.",
      "outcome": "pass",
      "revision": 2,
      "rule_loaded": "yes",
      "source": "personal/knowledge/log/2026-11-14-agents-p01-decision-cases-metrics.md#verification-and-status",
      "target": "/home/slnnk/ai/general/knowledge/README.md"
    },
    {
      "at": "2026-11-14T23:26:04.879207+00:00",
      "cause": "",
      "event_id": "todo-relevance-20261115-heading",
      "expected": "Choose TODO section by task subject and source; inspect full Markdown heading ancestry before adding or moving; verify affected rendered heading path using todo.py, or source ancestry for closed entries.",
      "outcome": "pass",
      "revision": 2,
      "rule_loaded": "yes",
      "source": "current/knowledge/log/2026-11-15-knowledge-base-todo-relevance-audit.md: Nomad heading corrected in place, home item retained under Personal/Home network, both affected sections rendered successfully.",
      "target": "/home/slnnk/ai/general/knowledge/README.md"
    }
  ],
  "expected": "Choose TODO section by task subject and source; inspect full Markdown heading ancestry before adding or moving; verify affected rendered heading path using todo.py, or source ancestry for closed entries.",
  "key": "todo-heading-ancestry",
  "kind": "explicit",
  "layer": "personal",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-10-19T21:35:30.749798+00:00",
      "cause": "",
      "event_id": "todo-grouping-20261020-user-second-misgrouping",
      "expected": "Choose TODO section by task subject and source; inspect full Markdown heading ancestry before adding or moving; verify affected rendered heading path using todo.py, or source ancestry for closed entries.",
      "source": "User correction in current conversation on 2026-10-20: second incorrect grouping; prevent future errors.",
      "summary": "User identified a second unrelated TODO grouping and requested prevention; entries had inherited the last Markdown section."
    }
  ],
  "repo": "",
  "revision": 2,
  "scope": "global",
  "summary": "User identified a second unrelated TODO grouping and requested prevention; entries had inherited the last Markdown section.",
  "system": "knowledge-base",
  "target": "/home/slnnk/ai/general/knowledge/README.md",
  "task_id": "",
  "updated": "2026-11-14T23:26:04.879207+00:00",
  "version": 1
}
```
