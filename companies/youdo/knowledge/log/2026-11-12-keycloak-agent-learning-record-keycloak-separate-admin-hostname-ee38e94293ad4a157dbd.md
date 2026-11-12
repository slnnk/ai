---
system: keycloak
status: verified
checked: 2026-11-12
tags: [agents, learning]
---
# Agent learning: keycloak-separate-admin-hostname

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-12T17:40:59.557004+00:00",
  "decisions": [],
  "evaluations": [],
  "expected": "Use https://auth-tech-admin.youdo.com/admin/ for Keycloak administration; public OIDC issuer remains https://auth-tech.youdo.com/realms/youdo.",
  "key": "keycloak-separate-admin-hostname",
  "kind": "fact",
  "layer": "current",
  "occurrences": [
    {
      "agent": "unknown",
      "at": "2026-11-12T17:40:59.557004+00:00",
      "cause": "",
      "event_id": "ai-qa-20261112-keycloak-admin-404",
      "expected": "Use https://auth-tech-admin.youdo.com/admin/ for Keycloak administration; public OIDC issuer remains https://auth-tech.youdo.com/realms/youdo.",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md",
      "summary": "Public OIDC hostname returned nginx404 for admin path; configuration declares a separate administrative hostname."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "current",
  "summary": "Public OIDC hostname returned nginx404 for admin path; configuration declares a separate administrative hostname.",
  "system": "keycloak",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md",
  "task_id": "",
  "updated": "2026-11-12T17:40:59.557004+00:00",
  "version": 1
}
```
