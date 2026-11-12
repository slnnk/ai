---
system: ai-qa
status: verified
checked: 2026-11-12
tags: [agents, learning]
---
# Agent learning: devops-918-runtime-layout

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-12T11:30:00.255420+00:00",
  "decisions": [
    {
      "at": "2026-11-12T11:57:40.157200+00:00",
      "decision": "adopted",
      "expected": "Keep namespace ai-qa and adjacent chart PostgreSQL with retained PVC in the deployment plan. Implement only the approved ai-qa environment-secret MR on DevOps-918-secrets-from-env from origin/master; publication needs second approval, all other deployment/infrastructure work remains planning only.",
      "revision": 2,
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md",
      "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md"
    },
    {
      "at": "2026-11-12T12:29:34.353328+00:00",
      "decision": "adopted",
      "expected": "Target permanent namespace ai-qa with adjacent chart PostgreSQL/PVC for state, no dual SQLite target. Approved env-secret MR is published. User approved extending the same branch/MR with S3 artifacts; S3 settings are only bucket, URL, access key and secret key. S3 publication needs renewed second approval; infrastructure writes and other deployment changes remain unapproved.",
      "revision": 3,
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md",
      "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md"
    },
    {
      "at": "2026-11-12T14:49:58.656887+00:00",
      "decision": "adopted",
      "expected": "For DevOps-918, keep global.namespace ai-qa in service dev.yml; shared logic must honor an explicit service namespace and generate a stable Helm fallback when absent. Do not hardcode ai-qa namespace provisioning in infrastructure. Keep adjacent chart PostgreSQL/PVC target, S3 settings only bucket/URL/access keys, kubeconfig auth, and existing approval gates for any additional implementation/publication.",
      "revision": 4,
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md",
      "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md"
    },
    {
      "at": "2026-11-12T16:50:03.822373+00:00",
      "decision": "adopted",
      "expected": "For DevOps-918 set service dev.yml global.namespace to dev-ai-qa, keep it permanent without TTL/auto-stop despite dev- prefix. Preserve release/project/resource names ai-qa. Common namespace contract still honors explicit names and Helm fallback when absent; keep kubeconfig auth and all existing approval gates. No live namespace/Vault changes implied.",
      "revision": 5,
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md",
      "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md"
    }
  ],
  "evaluations": [],
  "expected": "For DevOps-918 set service dev.yml global.namespace to dev-ai-qa, keep it permanent without TTL/auto-stop despite dev- prefix. Preserve release/project/resource names ai-qa. Common namespace contract still honors explicit names and Helm fallback when absent; keep kubeconfig auth and all existing approval gates. No live namespace/Vault changes implied.",
  "key": "devops-918-runtime-layout",
  "kind": "task",
  "layer": "current",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-12T11:30:00.255420+00:00",
      "cause": "",
      "event_id": "devops-918-user-layout-20261112",
      "expected": "Plan namespace ai-qa in VK test Kubernetes, shared microservice chart with adjacent PostgreSQL and PVC reuse across deployments; do not implement during planning.",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md",
      "summary": "User specified namespace ai-qa and adjacent chart-managed PostgreSQL with retained PVC; planning only."
    }
  ],
  "repo": "",
  "revision": 5,
  "scope": "current",
  "summary": "User changed the explicit permanent namespace to dev-ai-qa to fit existing Vault dev-* eligibility.",
  "system": "ai-qa",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md",
  "task_id": "DevOps-918",
  "updated": "2026-11-12T16:50:03.822373+00:00",
  "version": 1
}
```
