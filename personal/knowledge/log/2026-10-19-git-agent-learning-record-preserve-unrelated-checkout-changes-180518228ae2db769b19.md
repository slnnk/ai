---
system: git
status: verified
checked: 2026-11-11
tags: [agents, learning]
---
# Agent learning: preserve-unrelated-checkout-changes

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-10-19T17:58:36.513462+00:00",
  "decisions": [],
  "evaluations": [
    {
      "at": "2026-11-11T17:45:50.357601+00:00",
      "cause": "Existing task log records stopping a conflicting branch switch, obtaining approval for a revised base, preserving 16 unrelated paths and using the existing checkout. Historical instruction-read evidence is unavailable.",
      "event_id": "retrospective-devops916-checkout-preservation-20261110",
      "expected": "Work in the existing repository; create a worktree only on explicit request and never discard unrelated changes.",
      "outcome": "pass",
      "revision": 1,
      "rule_loaded": "unknown",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-10-nomad-test-devops-916-call-masking-config.md",
      "target": "/home/slnnk/ai/AGENTS.md"
    },
    {
      "at": "2026-11-11T19:36:59.299563+00:00",
      "cause": "",
      "event_id": "2026-11-11-sync-jenkins-publication",
      "expected": "Work in the existing repository; create a worktree only on explicit request and never discard unrelated changes.",
      "outcome": "pass",
      "revision": 1,
      "rule_loaded": "yes",
      "source": "Sync Jenkins publication: complete staged and committed diff contained exactly seven approved Jenkins paths; all nine runner worktree hashes matched before branch switch and after publication, index empty. Evidence current/knowledge/log/2026-11-11-automation-services-local-changes-audit.md section Sync Jenkins publication approved and completed.",
      "target": "/home/slnnk/ai/AGENTS.md"
    }
  ],
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
  "updated": "2026-11-11T19:36:59.299563+00:00",
  "version": 1
}
```
