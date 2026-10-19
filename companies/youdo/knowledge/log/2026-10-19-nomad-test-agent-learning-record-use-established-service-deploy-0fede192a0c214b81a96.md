---
system: nomad-test
status: verified
checked: 2026-10-19
tags: [agents, learning]
---
# Agent learning: use-established-service-deploy

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-10-19T17:58:36.599484+00:00",
  "decisions": [],
  "evaluations": [],
  "expected": "Use established GitLab deploy jobs and preserve established database recreation behavior unless explicitly asked otherwise.",
  "key": "use-established-service-deploy",
  "kind": "explicit",
  "layer": "current",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-10-19T17:58:36.599484+00:00",
      "cause": "",
      "event_id": "policy-import-20261019-use-established-service-deploy",
      "expected": "Use established GitLab deploy jobs and preserve established database recreation behavior unless explicitly asked otherwise.",
      "source": "current/CONTEXT.md Conventions, user correction 2026-10-16; current/knowledge/log/2026-10-16-nomad-test-cerberus-standard-gitlab-rollout.md",
      "summary": "Use the established service deployment workflow."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "current",
  "summary": "Use the established service deployment workflow.",
  "system": "nomad-test",
  "target": "/home/slnnk/ai/companies/youdo/CONTEXT.md",
  "task_id": "",
  "updated": "2026-10-19T17:58:36.599484+00:00",
  "version": 1
}
```
