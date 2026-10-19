---
system: gitlab-ci
status: verified
checked: 2026-10-19
tags: [agents, learning]
---
# Agent learning: release-base-images-from-master

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-10-19T17:58:36.678655+00:00",
  "decisions": [],
  "evaluations": [],
  "expected": "Release tags must point to master after merge; tagging and rebuilding still require explicit runtime authorization.",
  "key": "release-base-images-from-master",
  "kind": "explicit",
  "layer": "current",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-10-19T17:58:36.678655+00:00",
      "cause": "",
      "event_id": "policy-import-20261019-release-base-images-from-master",
      "expected": "Release tags must point to master after merge; tagging and rebuilding still require explicit runtime authorization.",
      "source": "current/CONTEXT.md Conventions, user correction 2026-10-14.",
      "summary": "Release base images from merged master commits."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "current",
  "summary": "Release base images from merged master commits.",
  "system": "gitlab-ci",
  "target": "/home/slnnk/ai/companies/youdo/CONTEXT.md",
  "task_id": "",
  "updated": "2026-10-19T17:58:36.678655+00:00",
  "version": 1
}
```
