---
system: nomad-test
status: verified
checked: 2026-10-21
tags: [agents, learning]
---
# Agent learning: daily-compilations-preserve-deploy-variables

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-10-21T11:06:42.433098+00:00",
  "decisions": [],
  "evaluations": [],
  "expected": "For this restoration preserve deployment-supplied dc/proxy via NOMAD_VAR variables; do not hardcode them into staging.nomad defaults.",
  "key": "daily-compilations-preserve-deploy-variables",
  "kind": "task",
  "layer": "current",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-10-21T11:06:42.433098+00:00",
      "cause": "",
      "event_id": "20261021-daily-compilations-dc-proxy",
      "expected": "For this restoration preserve deployment-supplied dc/proxy via NOMAD_VAR variables; do not hardcode them into staging.nomad defaults.",
      "source": "Current conversation 2026-10-21: user correction about dc and proxy injection",
      "summary": "User questioned unnecessary dc/proxy repository defaults because deployment already injects them."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "current",
  "summary": "User questioned unnecessary dc/proxy repository defaults because deployment already injects them.",
  "system": "nomad-test",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-10-21-nomad-test-daily-compilations-missing.md",
  "task_id": "daily-compilations-vk-20261021",
  "updated": "2026-10-21T11:06:42.433098+00:00",
  "version": 1
}
```
