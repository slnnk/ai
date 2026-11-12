---
system: gitlab-ci
status: verified
checked: 2026-11-12
tags: [agents, learning]
---
# Agent learning: devops-918-helm-ci-contract

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-12T19:05:57.437322+00:00",
  "decisions": [],
  "evaluations": [],
  "expected": "For DevOps-918 the include creates deploy dev directly, configured by DEV_-prefixed deployment variables; manual rules only, resource_group dev, no interruptible, chart ref master, fixed environment name dev, chart-owned Vault address, inline profile env in dev.yml, no HELM_SET_FILES/HELM_REQUIRED_ENV or Helm test file.",
  "key": "devops-918-helm-ci-contract",
  "kind": "task",
  "layer": "current",
  "occurrences": [
    {
      "agent": "unknown",
      "at": "2026-11-12T19:05:57.437322+00:00",
      "cause": "",
      "event_id": "ai-qa-20261112-helm-review-contract",
      "expected": "For DevOps-918 the include creates deploy dev directly, configured by DEV_-prefixed deployment variables; manual rules only, resource_group dev, no interruptible, chart ref master, fixed environment name dev, chart-owned Vault address, inline profile env in dev.yml, no HELM_SET_FILES/HELM_REQUIRED_ENV or Helm test file.",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md",
      "summary": "User specified include-defined deploy dev and simplified public configuration during MR92 review."
    }
  ],
  "repo": "/home/slnnk/git/gitlab-ci-templates",
  "revision": 1,
  "scope": "repo",
  "summary": "User specified include-defined deploy dev and simplified public configuration during MR92 review.",
  "system": "gitlab-ci",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md",
  "task_id": "DevOps-918",
  "updated": "2026-11-12T19:05:57.437322+00:00",
  "version": 1
}
```
