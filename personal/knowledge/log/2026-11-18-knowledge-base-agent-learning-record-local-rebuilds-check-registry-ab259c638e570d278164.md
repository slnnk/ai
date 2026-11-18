---
system: knowledge-base
status: verified
checked: 2026-11-18
tags: [agents, learning]
---
# Agent learning: local-rebuilds-check-registry

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-18T20:50:25.617256+00:00",
  "decisions": [],
  "evaluations": [],
  "expected": "Use fresh dependency state and the configured registries for repeated local builds under ai-data, honor pinned versions and lockfiles, and surface unavailable packages. Discard build-only caches and keep distinct runtime or recovery artifacts.",
  "key": "local-rebuilds-check-registry",
  "kind": "explicit",
  "layer": "personal",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-18T20:50:25.617256+00:00",
      "cause": "",
      "event_id": "p22-2026-11-18-fresh-registry",
      "expected": "Use fresh dependency state and the configured registries for repeated local builds under ai-data, honor pinned versions and lockfiles, and surface unavailable packages. Discard build-only caches and keep distinct runtime or recovery artifacts.",
      "source": "P2.2 ai-data retention conversation, user clarification on 2026-11-18",
      "summary": "For repeated local builds, the user wants fresh registry-backed dependency resolution rather than retained package caches."
    }
  ],
  "repo": "",
  "revision": 2,
  "scope": "global",
  "summary": "For repeated local builds, the user wants fresh registry-backed dependency resolution rather than retained package caches.",
  "system": "knowledge-base",
  "target": "/home/slnnk/ai/general/knowledge/README.md#dependency-sources-for-repeated-builds",
  "task_id": "",
  "updated": "2026-11-18T20:50:25.725566+00:00",
  "version": 1
}
```
