---
system: dev-deployment
status: verified
checked: 2026-11-19
tags: [agents, learning]
---
# Agent learning: devops-884-public-image-for-all-namespaces

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-19T11:51:58.358792+00:00",
  "decisions": [],
  "evaluations": [
    {
      "at": "2026-11-19T11:56:36.371573+00:00",
      "cause": "",
      "event_id": "devops-884-uniform-public-image-prepared-20261119",
      "expected": "Use APP_IMAGE_PUBLIC_NAME in the shared Helm application deploy for every namespace and migrate ai-qa publication to Nexus in its own repository.",
      "outcome": "pass",
      "revision": 1,
      "rule_loaded": "yes",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-19-dev-deployment-devops-884-all-services-plan.md#uniform-image-template-prepared",
      "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-19-dev-deployment-devops-884-all-services-plan.md#uniform-public-image-name-direction"
    }
  ],
  "expected": "Use APP_IMAGE_PUBLIC_NAME in the shared Helm application deploy for every namespace and migrate ai-qa publication to Nexus in its own repository.",
  "key": "devops-884-public-image-for-all-namespaces",
  "kind": "task",
  "layer": "current",
  "occurrences": [
    {
      "agent": "unknown",
      "at": "2026-11-19T11:51:58.358792+00:00",
      "cause": "",
      "event_id": "devops-884-uniform-public-image-user-20261119",
      "expected": "Use APP_IMAGE_PUBLIC_NAME in the shared Helm application deploy for every namespace and migrate ai-qa publication to Nexus in its own repository.",
      "source": "DevOps-884 user decision on 2026-11-19 following comparison with ai-qa and Jenkins B2B",
      "summary": "User selected Nexus publication for ai-qa and uniform public deploy image names."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "current",
  "summary": "User selected Nexus publication for ai-qa and uniform public deploy image names.",
  "system": "dev-deployment",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-19-dev-deployment-devops-884-all-services-plan.md#uniform-public-image-name-direction",
  "task_id": "DevOps-884",
  "updated": "2026-11-19T11:56:36.371573+00:00",
  "version": 1
}
```
