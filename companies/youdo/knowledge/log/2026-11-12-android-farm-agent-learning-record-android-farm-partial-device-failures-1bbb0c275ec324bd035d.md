---
system: android-farm
status: verified
checked: 2026-11-12
tags: [agents, learning]
---
# Agent learning: android-farm-partial-device-failures

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-12T16:45:24.501301+00:00",
  "decisions": [],
  "evaluations": [],
  "expected": "Preserve tests on remaining devices; report individual preparation errors and use actual per-host emulator services. Supersede blanket fail-fast/job-stop proposal; no implementation or quarantine authorized by this discussion.",
  "key": "android-farm-partial-device-failures",
  "kind": "task",
  "layer": "current",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-12T16:45:24.501301+00:00",
      "cause": "",
      "event_id": "android-farm-20261112-partial-preparation-correction",
      "expected": "Preserve tests on remaining devices; report individual preparation errors and use actual per-host emulator services. Supersede blanket fail-fast/job-stop proposal; no implementation or quarantine authorized by this discussion.",
      "source": "/home/slnnk/ai/current/knowledge/systems/android-farm/system-map.md#partial-device-failure-policy--2026-11-12",
      "summary": "User rejected stopping the whole autotest job when preparation fails on one device because other devices can run tests."
    },
    {
      "agent": "codex",
      "at": "2026-11-12T16:46:35.578677+00:00",
      "cause": "",
      "event_id": "android-farm-20261112-adb-loop-clarification",
      "expected": "Preserve tests on remaining devices; report individual preparation errors and use actual per-host emulator services. Supersede blanket fail-fast/job-stop proposal; no implementation or quarantine authorized by this discussion.",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-12-android-farm-backlog-relevance-audit.md#adbsh-device-loop-clarification--2026-11-12",
      "summary": "User rejected stopping the whole autotest job when preparation fails on one device because other devices can run tests."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "current",
  "summary": "User rejected stopping the whole autotest job when preparation fails on one device because other devices can run tests.",
  "system": "android-farm",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/systems/android-farm/system-map.md",
  "task_id": "android-farm-preparation",
  "updated": "2026-11-12T16:46:35.578677+00:00",
  "version": 1
}
```
