---
system: dev-deployment
status: verified
checked: 2026-11-19
tags: [agents, learning]
---
# Agent learning: dev-kubernetes-cpu-chart-defaults

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-19T14:21:50.356027+00:00",
  "decisions": [],
  "evaluations": [
    {
      "at": "2026-11-19T15:02:31.437371+00:00",
      "cause": "",
      "event_id": "devops-884-chat-content-cpu-defaults-20261119",
      "expected": "Omit both services[].cpu and services[].cpuLimit in dev service values. Verify rendered CPU follows the chart defaults and keep resource dimensions outside this correction in scope.",
      "outcome": "pass",
      "revision": 1,
      "rule_loaded": "yes",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-19-dev-deployment-devops-884-all-services-plan.md#chat-content-configuration-prepared-and-vault-verified",
      "target": "/home/slnnk/ai/companies/youdo/knowledge/systems/dev-deployment/overview.md#kubernetes-and-shared-infrastructure"
    }
  ],
  "expected": "Omit both services[].cpu and services[].cpuLimit in dev service values. Verify rendered CPU follows the chart defaults and keep resource dimensions outside this correction in scope.",
  "key": "dev-kubernetes-cpu-chart-defaults",
  "kind": "explicit",
  "layer": "current",
  "occurrences": [
    {
      "agent": "unknown",
      "at": "2026-11-19T14:21:50.356027+00:00",
      "cause": "",
      "event_id": "devops-884-pechkin-cpu-defaults-user-20261119",
      "expected": "Omit both services[].cpu and services[].cpuLimit in dev service values. Verify rendered CPU follows the chart defaults and keep resource dimensions outside this correction in scope.",
      "source": "User corrections during Pechkin DevOps-884 review on 2026-11-19, covering CPU limits and requests",
      "summary": "User selected the chart defaults for CPU requests and limits in dev service values."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "current",
  "summary": "User selected the chart defaults for CPU requests and limits in dev service values.",
  "system": "dev-deployment",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/systems/dev-deployment/overview.md#kubernetes-and-shared-infrastructure",
  "task_id": "",
  "updated": "2026-11-19T15:02:31.437371+00:00",
  "version": 1
}
```
