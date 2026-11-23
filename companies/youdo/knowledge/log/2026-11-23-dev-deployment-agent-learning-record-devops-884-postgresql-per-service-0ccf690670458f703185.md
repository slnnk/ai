---
system: dev-deployment
status: verified
checked: 2026-11-23
tags: [agents, learning]
---
# Agent learning: devops-884-postgresql-per-service

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-23T18:26:05.275689+00:00",
  "decisions": [],
  "evaluations": [
    {
      "at": "2026-11-23T18:35:28.078378+00:00",
      "cause": "",
      "event_id": "devops-884-textvalidation-local-database-20261123",
      "expected": "For DevOps-884 use the B2B chart pattern to create a separate PostgreSQL alongside each service that needs it, owning its own StatefulSet, Service and PVC in that service release.",
      "outcome": "pass",
      "revision": 2,
      "rule_loaded": "yes",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-19-dev-deployment-devops-884-all-services-plan.md#textvalidation-dev-single-mr-published-2026-11-23",
      "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-19-dev-deployment-devops-884-all-services-plan.md#per-service-postgresql-for-dev-single-2026-11-23"
    }
  ],
  "expected": "For DevOps-884 use the B2B chart pattern to create a separate PostgreSQL alongside each service that needs it, owning its own StatefulSet, Service and PVC in that service release.",
  "key": "devops-884-postgresql-per-service",
  "kind": "task",
  "layer": "current",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-23T18:26:05.275689+00:00",
      "cause": "",
      "event_id": "devops-884-postgresql-per-service-20261123",
      "expected": "For DevOps-884 use the B2B chart pattern to create a separate PostgreSQL alongside each service that needs it, owning its own StatefulSet, Service and PVC in that service release.",
      "source": "User decision in the DevOps-884 discussion on 2026-11-23",
      "summary": "User chose a per-service PostgreSQL instance for services in the dev-single rollout using the B2B pattern."
    }
  ],
  "repo": "",
  "revision": 2,
  "scope": "current",
  "summary": "User chose a per-service PostgreSQL instance for services in the dev-single rollout using the B2B pattern.",
  "system": "dev-deployment",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-19-dev-deployment-devops-884-all-services-plan.md#per-service-postgresql-for-dev-single-2026-11-23",
  "task_id": "DevOps-884",
  "updated": "2026-11-23T18:35:28.078378+00:00",
  "version": 1
}
```
