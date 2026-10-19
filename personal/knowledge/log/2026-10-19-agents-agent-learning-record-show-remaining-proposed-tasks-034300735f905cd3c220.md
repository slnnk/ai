---
system: agents
status: verified
checked: 2026-10-19
tags: [agents, learning]
---
# Agent learning: show-remaining-proposed-tasks

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-10-19T18:42:39.188583+00:00",
  "decisions": [
    {
      "at": "2026-10-19T18:44:17.704042+00:00",
      "decision": "adopted",
      "expected": "After completing an item from an agent-proposed list, show remaining unfinished items using the original wording, order, numbering, grouping and formatting; remove only completed items. If none remain, say so.",
      "revision": 2,
      "source": "User clarification on 2026-10-19: display remaining tasks in the same form as initially, because the reformatted list had discrepancies.",
      "target": "/home/slnnk/ai/AGENTS.md"
    }
  ],
  "evaluations": [],
  "expected": "After completing an item from an agent-proposed list, show remaining unfinished items using the original wording, order, numbering, grouping and formatting; remove only completed items. If none remain, say so.",
  "key": "show-remaining-proposed-tasks",
  "kind": "explicit",
  "layer": "personal",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-10-19T18:42:39.188583+00:00",
      "cause": "",
      "event_id": "codex-20261019-remaining-proposed-tasks-1",
      "expected": "After completing a task from a list initially proposed to the user, show the remaining unfinished tasks in the final response; if none remain, say so.",
      "source": "User instruction in the local-agent TODO discussion on 2026-10-19, following implementation of nested Codex accounting.",
      "summary": "After completing the classifier task, the user requested showing remaining tasks from the originally proposed list after each completion."
    }
  ],
  "repo": "",
  "revision": 2,
  "scope": "global",
  "summary": "After completing the classifier task, the user requested showing remaining tasks from the originally proposed list after each completion.",
  "system": "agents",
  "target": "/home/slnnk/ai/AGENTS.md",
  "task_id": "",
  "updated": "2026-10-19T18:44:17.704042+00:00",
  "version": 1
}
```
