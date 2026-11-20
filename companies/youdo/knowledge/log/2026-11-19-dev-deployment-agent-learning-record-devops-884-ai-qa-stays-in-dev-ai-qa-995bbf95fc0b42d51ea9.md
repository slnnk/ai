---
system: dev-deployment
status: verified
checked: 2026-11-19
tags: [agents, learning]
---
# Agent learning: devops-884-ai-qa-stays-in-dev-ai-qa

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-19T15:53:58.163150+00:00",
  "decisions": [],
  "evaluations": [],
  "expected": "Keep ai-qa in dev-ai-qa. The 18-service dev-single rollout excludes ai-qa; its Nexus image-publication change retains the dedicated namespace.",
  "key": "devops-884-ai-qa-stays-in-dev-ai-qa",
  "kind": "task",
  "layer": "current",
  "occurrences": [
    {
      "agent": "unknown",
      "at": "2026-11-19T15:53:58.163150+00:00",
      "cause": "",
      "event_id": "devops-884-ai-qa-namespace-20261119",
      "expected": "Keep ai-qa in dev-ai-qa. The 18-service dev-single rollout excludes ai-qa; its Nexus image-publication change retains the dedicated namespace.",
      "source": "DevOps-884 user correction after the prepared service count on 2026-11-19",
      "summary": "User clarified that ai-qa stays in its own namespace."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "current",
  "summary": "User clarified that ai-qa stays in its own namespace.",
  "system": "dev-deployment",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-19-dev-deployment-devops-884-all-services-plan.md#ai-qa-namespace-scope",
  "task_id": "DevOps-884",
  "updated": "2026-11-19T15:53:58.163150+00:00",
  "version": 1
}
```
