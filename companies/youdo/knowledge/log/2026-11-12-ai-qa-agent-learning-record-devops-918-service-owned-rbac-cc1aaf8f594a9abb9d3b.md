---
system: ai-qa
status: verified
checked: 2026-11-12
tags: [agents, learning]
---
# Agent learning: devops-918-service-owned-rbac

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-12T13:14:09.642031+00:00",
  "decisions": [
    {
      "at": "2026-11-12T13:50:48.218371+00:00",
      "decision": "adopted",
      "expected": "Retain KUBE_CONFIG env and current VK Keystone helper for this task. Do not add separate ServiceAccounts, native-token access, generic/service-specific RBAC or Jenkins binding changes. If RBAC is revisited in a future authorized scope, preserve the prior generic service-owned lifecycle preference.",
      "revision": 2,
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md",
      "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md"
    }
  ],
  "evaluations": [],
  "expected": "Retain KUBE_CONFIG env and current VK Keystone helper for this task. Do not add separate ServiceAccounts, native-token access, generic/service-specific RBAC or Jenkins binding changes. If RBAC is revisited in a future authorized scope, preserve the prior generic service-owned lifecycle preference.",
  "key": "devops-918-service-owned-rbac",
  "kind": "task",
  "layer": "current",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-12T13:14:09.642031+00:00",
      "cause": "",
      "event_id": "devops-918-user-rejects-scattered-rbac-20261112",
      "expected": "Design generic declarative RBAC owned by the service release; avoid hardcoded ai-qa platform/Jenkins settings and per-service cross-repository edits. Handle dynamic namespace access and cleanup explicitly without implying native RBAC supports namespace selectors.",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md",
      "summary": "User rejected ai-qa-specific SA/RBAC split across infrastructure and Jenkins because new services and retirement would require edits everywhere."
    }
  ],
  "repo": "",
  "revision": 2,
  "scope": "current",
  "summary": "User chose to retain kubeconfig; separate SA and RBAC/Jenkins implementation proposals are superseded for DevOps-918.",
  "system": "ai-qa",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md",
  "task_id": "DevOps-918",
  "updated": "2026-11-12T13:50:48.218371+00:00",
  "version": 1
}
```
