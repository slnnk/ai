---
system: home-network
status: verified
checked: 2026-11-14
tags: [agents, learning]
---
# Agent learning: home-lampa-msx-cors

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-14T17:05:03.832522+00:00",
  "decisions": [],
  "evaluations": [],
  "expected": "Lampa MSX startup requires allow-origin headers; verify response headers as well as HTTP status.",
  "key": "home-lampa-msx-cors",
  "kind": "fact",
  "layer": "personal",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-14T17:05:03.832522+00:00",
      "cause": "",
      "event_id": "home-lampa-tv-status0-20261114",
      "expected": "Lampa MSX startup requires allow-origin headers; verify response headers as well as HTTP status.",
      "source": "personal/knowledge/log/2026-11-14-home-network-lampa-cors-bootstrap.md#findings",
      "summary": "TV MSX rejected startup JSON without CORS despite HTTP200; original role checks missed required cross-origin headers."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "personal",
  "summary": "TV MSX rejected startup JSON without CORS despite HTTP200; original role checks missed required cross-origin headers.",
  "system": "home-network",
  "target": "/home/slnnk/ai/personal/knowledge/systems/home-network.md",
  "task_id": "",
  "updated": "2026-11-14T17:05:03.832522+00:00",
  "version": 1
}
```
