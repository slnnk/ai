---
system: agents
status: verified
checked: 2026-11-12
tags: [agents, learning]
---
# Agent learning: simplest-sufficient-solution

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-12T15:39:13.230892+00:00",
  "decisions": [],
  "evaluations": [
    {
      "at": "2026-11-12T19:16:48.325534+00:00",
      "cause": "Initial Helm CI implementation added yq download/checksum and API archive machinery despite existing image tools; user requested simple git clone. Recovered in723ea3b; retain original failure.",
      "event_id": "devops-918-simplicity-first-attempt",
      "expected": "Prefer the simplest solution meeting the request and verified constraints; add conditions, exceptions, configuration or abstractions only for concrete needs; remove unnecessary complications while preserving required behavior and safeguards.",
      "outcome": "fail",
      "revision": 1,
      "rule_loaded": "yes",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md",
      "target": "/home/slnnk/ai/general/knowledge/README.md"
    }
  ],
  "expected": "Prefer the simplest solution meeting the request and verified constraints; add conditions, exceptions, configuration or abstractions only for concrete needs; remove unnecessary complications while preserving required behavior and safeguards.",
  "key": "simplest-sufficient-solution",
  "kind": "explicit",
  "layer": "personal",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-12T15:39:13.230892+00:00",
      "cause": "",
      "event_id": "karpathy-simplicity-approved-20261112",
      "expected": "Prefer the simplest solution meeting the request and verified constraints; add conditions, exceptions, configuration or abstractions only for concrete needs; remove unnecessary complications while preserving required behavior and safeguards.",
      "source": "personal/knowledge/log/2026-11-12-knowledge-base-karpathy-guidelines-review.md#simplicity-wording-review; Codex session 01a1ced4-16da-7e60-9d0b-b58427e7f6e6: user approved simplicity adoption, resumed in recovery session.",
      "summary": "User approved the simplicity rule after reviewing the original and the local adaptation."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "global",
  "summary": "User approved the simplicity rule after reviewing the original and the local adaptation.",
  "system": "agents",
  "target": "/home/slnnk/ai/general/knowledge/README.md",
  "task_id": "",
  "updated": "2026-11-12T19:16:48.325534+00:00",
  "version": 1
}
```
