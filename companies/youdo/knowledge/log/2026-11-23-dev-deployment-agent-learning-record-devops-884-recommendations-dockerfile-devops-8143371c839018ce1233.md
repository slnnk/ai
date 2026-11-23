---
system: dev-deployment
status: verified
checked: 2026-11-23
tags: [agents, learning]
---
# Agent learning: devops-884-recommendations-dockerfile-devops

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-23T18:02:52.533427+00:00",
  "decisions": [],
  "evaluations": [
    {
      "at": "2026-11-23T18:14:22.872936+00:00",
      "cause": "",
      "event_id": "devops-884-recommendations-published-20261123",
      "expected": "For the recommendations-mock DevOps-884 MR, use the shared v3 templates and put the local Python Dockerfile under devops; a dedicated build job may invoke it with the repository root as context.",
      "outcome": "pass",
      "revision": 2,
      "rule_loaded": "yes",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-19-dev-deployment-devops-884-all-services-plan.md#recommendations-mock-v3-ci-mr-published-2026-11-23",
      "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-19-dev-deployment-devops-884-all-services-plan.md#recommendations-mock-ci-template-and-dockerfile-layout-preview-2026-11-23"
    }
  ],
  "expected": "For the recommendations-mock DevOps-884 MR, use the shared v3 templates and put the local Python Dockerfile under devops; a dedicated build job may invoke it with the repository root as context.",
  "key": "devops-884-recommendations-dockerfile-devops",
  "kind": "task",
  "layer": "current",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-23T18:02:52.533427+00:00",
      "cause": "",
      "event_id": "devops-884-recommendations-dockerfile-devops-20261123",
      "expected": "For the recommendations-mock DevOps-884 MR, use the shared v3 templates and put the local Python Dockerfile under devops; a dedicated build job may invoke it with the repository root as context.",
      "source": "User direction in the DevOps-884 discussion on 2026-11-23",
      "summary": "User chose shared CI templates with a separate Python build job and a local Dockerfile under devops for recommendations mock."
    }
  ],
  "repo": "",
  "revision": 2,
  "scope": "current",
  "summary": "User chose shared CI templates with a separate Python build job and a local Dockerfile under devops for recommendations mock.",
  "system": "dev-deployment",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-19-dev-deployment-devops-884-all-services-plan.md#recommendations-mock-ci-template-and-dockerfile-layout-preview-2026-11-23",
  "task_id": "DevOps-884",
  "updated": "2026-11-23T18:14:22.872936+00:00",
  "version": 1
}
```
