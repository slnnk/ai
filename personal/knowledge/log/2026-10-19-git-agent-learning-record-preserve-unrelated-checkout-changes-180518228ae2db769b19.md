---
system: git
status: verified
checked: 2026-10-19
tags: [agents, learning]
---
# Agent learning: preserve-unrelated-checkout-changes

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-10-19T17:58:36.513462+00:00",
  "decisions": [],
  "evaluations": [],
  "expected": "Work in the existing repository; create a worktree only on explicit request and never discard unrelated changes.",
  "key": "preserve-unrelated-checkout-changes",
  "kind": "explicit",
  "layer": "personal",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-10-19T17:58:36.513462+00:00",
      "cause": "",
      "event_id": "policy-import-20261019-preserve-unrelated-checkout-changes",
      "expected": "Work in the existing repository; create a worktree only on explicit request and never discard unrelated changes.",
      "source": "User-provided AGENTS.md, 2026-10-19, Git section.",
      "summary": "Use the existing checkout and preserve unrelated local changes."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "global",
  "summary": "Use the existing checkout and preserve unrelated local changes.",
  "system": "git",
  "target": "/home/slnnk/ai/AGENTS.md",
  "task_id": "",
  "updated": "2026-10-19T17:58:36.513462+00:00",
  "version": 1
}
```
