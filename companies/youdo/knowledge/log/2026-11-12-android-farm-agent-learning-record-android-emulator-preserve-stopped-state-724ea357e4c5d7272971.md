---
system: android-farm
status: verified
checked: 2026-11-12
tags: [agents, learning]
---
# Agent learning: android-emulator-preserve-stopped-state

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-12T16:49:42.149659+00:00",
  "decisions": [],
  "evaluations": [],
  "expected": "Skip absent and stopped emulator services; restart running services only. Preserve partial-device operation and leave adb.sh unchanged within this proposal.",
  "key": "android-emulator-preserve-stopped-state",
  "kind": "task",
  "layer": "current",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-12T16:49:42.149659+00:00",
      "cause": "",
      "event_id": "android-emulator-20261112-stopped-state",
      "expected": "Skip absent and stopped emulator services; restart running services only. Preserve partial-device operation and leave adb.sh unchanged within this proposal.",
      "source": "/home/slnnk/ai/current/knowledge/systems/android-farm/system-map.md#emulator-preparation-preserves-stopped-services--2026-11-12",
      "summary": "User explicitly rejected restarting stopped emulator services during CI preparation."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "current",
  "summary": "User explicitly rejected restarting stopped emulator services during CI preparation.",
  "system": "android-farm",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/systems/android-farm/system-map.md",
  "task_id": "android-farm-preparation",
  "updated": "2026-11-12T16:49:42.149659+00:00",
  "version": 1
}
```
