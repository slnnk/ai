---
system: ai-qa
status: verified
checked: 2026-11-12
tags: [agents, learning]
---
# Agent learning: devops-918-dev-postgres-credentials

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-12T20:00:53.348176+00:00",
  "decisions": [],
  "evaluations": [],
  "expected": "For ai-qa dev Helm use the chart defaults for PostgreSQL and app PGPASSWORD; no dedicated PG Vault mapping/passwordSecretRef. Keep integration secrets in Vault and deploy both charts normally without CI VSO bootstrap. This is a dev task-specific decision, not a global secret-policy change.",
  "key": "devops-918-dev-postgres-credentials",
  "kind": "task",
  "layer": "current",
  "occurrences": [
    {
      "agent": "unknown",
      "at": "2026-11-12T20:00:53.348176+00:00",
      "cause": "",
      "event_id": "ai-qa-20261112-standard-dev-postgres",
      "expected": "For ai-qa dev Helm use the chart defaults for PostgreSQL and app PGPASSWORD; no dedicated PG Vault mapping/passwordSecretRef. Keep integration secrets in Vault and deploy both charts normally without CI VSO bootstrap. This is a dev task-specific decision, not a global secret-policy change.",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md",
      "summary": "User chose the same standard dev PostgreSQL credentials as other services instead of a separate ai-qa Vault password."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "current",
  "summary": "User chose the same standard dev PostgreSQL credentials as other services instead of a separate ai-qa Vault password.",
  "system": "ai-qa",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md",
  "task_id": "DevOps-918",
  "updated": "2026-11-12T20:00:53.348176+00:00",
  "version": 1
}
```
