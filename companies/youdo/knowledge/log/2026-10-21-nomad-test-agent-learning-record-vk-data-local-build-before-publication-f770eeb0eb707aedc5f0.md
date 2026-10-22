---
system: nomad-test
status: verified
checked: 2026-10-21
tags: [agents, learning]
---
# Agent learning: vk-data-local-build-before-publication

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-10-21T14:22:22.297646+00:00",
  "decisions": [],
  "evaluations": [],
  "expected": "For current VK Data-service recovery, build candidate images locally and validate relevant behavior before further publication; retain minimal scope and existing external approval gates.",
  "key": "vk-data-local-build-before-publication",
  "kind": "task",
  "layer": "current",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-10-21T14:22:22.297646+00:00",
      "cause": "",
      "event_id": "20261021-user-local-build-before-push",
      "expected": "For current VK Data-service recovery, build candidate images locally and validate relevant behavior before further publication; retain minimal scope and existing external approval gates.",
      "source": "Current user message: Прежде чем отправлять изменения проверь сборку локально",
      "summary": "User required local image build before sending further recovery changes after repeated CI build failures."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "current",
  "summary": "User required local image build before sending further recovery changes after repeated CI build failures.",
  "system": "nomad-test",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-10-21-nomad-test-subcategory-predictor-vk.md",
  "task_id": "vk-data-services-20261021",
  "updated": "2026-10-21T14:22:22.297646+00:00",
  "version": 1
}
```
