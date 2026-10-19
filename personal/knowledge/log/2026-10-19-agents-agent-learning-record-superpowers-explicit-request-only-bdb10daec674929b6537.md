---
system: agents
status: verified
checked: 2026-10-19
tags: [agents, learning]
---
# Agent learning: superpowers-explicit-request-only

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-10-19T18:02:37.849515+00:00",
  "decisions": [],
  "evaluations": [],
  "expected": "Do not automatically invoke any superpowers skill, including using-superpowers; use them only when explicitly requested for the current task.",
  "key": "superpowers-explicit-request-only",
  "kind": "explicit",
  "layer": "personal",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-10-19T18:02:37.849515+00:00",
      "cause": "",
      "event_id": "user-2026-10-19-superpowers-opt-in",
      "expected": "Do not automatically invoke any superpowers skill, including using-superpowers; use them only when explicitly requested for the current task.",
      "source": "User request in Codex on 2026-10-19: add a global rule that superpowers skills are used only on demand.",
      "summary": "Use superpowers skills only on explicit user request."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "global",
  "summary": "Use superpowers skills only on explicit user request.",
  "system": "agents",
  "target": "/home/slnnk/ai/AGENTS.md",
  "task_id": "",
  "updated": "2026-10-19T18:02:37.849515+00:00",
  "version": 1
}
```
