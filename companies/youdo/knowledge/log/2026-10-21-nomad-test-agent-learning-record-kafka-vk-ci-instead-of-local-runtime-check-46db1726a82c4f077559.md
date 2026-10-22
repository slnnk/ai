---
system: nomad-test
status: verified
checked: 2026-10-21
tags: [agents, learning]
---
# Agent learning: kafka-vk-ci-instead-of-local-runtime-check

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-10-21T15:44:19.692004+00:00",
  "decisions": [],
  "evaluations": [],
  "expected": "For this Kafka task stop local runtime checks, publish requested minimal VK changes, use kafka-vk-test with a separate broker name, and retain explicit merge/deployment boundaries; do not generalize waiver to other projects.",
  "key": "kafka-vk-ci-instead-of-local-runtime-check",
  "kind": "task",
  "layer": "current",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-10-21T15:44:19.692004+00:00",
      "cause": "",
      "event_id": "20261021-kafka-waive-local-checks",
      "expected": "For this Kafka task stop local runtime checks, publish requested minimal VK changes, use kafka-vk-test with a separate broker name, and retain explicit merge/deployment boundaries; do not generalize waiver to other projects.",
      "source": "Current Kafka task user: Не нужно проверять, пушь изменения и запускай через ci; Только поменяй job name, чтобы не было конфликта с уже запущенной kafka",
      "summary": "User selected full separate Kafka stack, then waived further local tests and explicitly requested push and CI execution with a distinct Nomad job name."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "current",
  "summary": "User selected full separate Kafka stack, then waived further local tests and explicitly requested push and CI execution with a distinct Nomad job name.",
  "system": "nomad-test",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-10-21-nomad-test-kafka-vk-full-job.md",
  "task_id": "kafka-vk-20261021",
  "updated": "2026-10-21T15:44:19.692004+00:00",
  "version": 1
}
```
