---
system: automation-services
status: verified
checked: 2026-11-11
tags: [agents, learning]
---
# Agent learning: automation-services-vault-all-secrets

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-11T19:54:41.603147+00:00",
  "decisions": [],
  "evaluations": [],
  "expected": "Store all real automation-services service, runner and cache secrets in HashiCorp Vault and reference them through inventory secret fetching; no literal or base64 secret values, new encrypted secret files or application-secret environment fallback. Migrate legacy values within reviewed scope, preserving consumers and external-change approvals.",
  "key": "automation-services-vault-all-secrets",
  "kind": "explicit",
  "layer": "current",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-11T19:54:41.603147+00:00",
      "cause": "",
      "event_id": "2026-11-11-automation-services-all-secrets-vault",
      "expected": "Store all real automation-services service, runner and cache secrets in HashiCorp Vault and reference them through inventory secret fetching; no literal or base64 secret values, new encrypted secret files or application-secret environment fallback. Migrate legacy values within reviewed scope, preserving consumers and external-change approvals.",
      "source": "User statement in current session, 2026-11-11: all secrets in this repository must be in Vault.",
      "summary": "User requires all secrets in automation-services to be stored in Vault, not only current Nexus credentials."
    }
  ],
  "repo": "/home/slnnk/git/automation-services",
  "revision": 1,
  "scope": "repo",
  "summary": "User requires all secrets in automation-services to be stored in Vault, not only current Nexus credentials.",
  "system": "automation-services",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/systems/automation-services/local-vault-ansible-access.md",
  "task_id": "",
  "updated": "2026-11-11T19:54:41.603147+00:00",
  "version": 1
}
```
