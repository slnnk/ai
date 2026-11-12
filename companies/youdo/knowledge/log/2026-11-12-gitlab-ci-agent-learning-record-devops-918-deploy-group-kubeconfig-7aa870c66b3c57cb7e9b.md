---
system: gitlab-ci
status: verified
checked: 2026-11-12
tags: [agents, learning]
---
# Agent learning: devops-918-deploy-group-kubeconfig

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-12T19:25:38.515790+00:00",
  "decisions": [
    {
      "at": "2026-11-12T19:44:52.891542+00:00",
      "decision": "adopted",
      "expected": "For DevOps-918 use group KUBECONFIG_DEV as raw kubeconfig YAML; its type is fixed. Write directly to the standard config location without format-detection branching; preserve native authentication, with no project kubeconfig or Keystone variables.",
      "revision": 2,
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md",
      "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md"
    }
  ],
  "evaluations": [],
  "expected": "For DevOps-918 use group KUBECONFIG_DEV as raw kubeconfig YAML; its type is fixed. Write directly to the standard config location without format-detection branching; preserve native authentication, with no project kubeconfig or Keystone variables.",
  "key": "devops-918-deploy-group-kubeconfig",
  "kind": "task",
  "layer": "current",
  "occurrences": [
    {
      "agent": "unknown",
      "at": "2026-11-12T19:25:38.515790+00:00",
      "cause": "",
      "event_id": "ai-qa-20261112-group-kubeconfig",
      "expected": "Use group KUBECONFIG_DEV in shared deployment templates; preserve its native authentication settings instead of requiring project-specific kubeconfig or Keystone files. Support raw content and GitLab file variables without printing credentials.",
      "source": "/home/slnnk/ai/current/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md",
      "summary": "User selected the existing YouDo group KUBECONFIG_DEV as the deployment credential source."
    }
  ],
  "repo": "/home/slnnk/git/gitlab-ci-templates",
  "revision": 2,
  "scope": "repo",
  "summary": "User fixed KUBECONFIG_DEV as an env_var containing YAML and rejected a file/content compatibility branch.",
  "system": "gitlab-ci",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-12-ai-qa-devops-918-vk-helm-deployment-plan.md",
  "task_id": "DevOps-918",
  "updated": "2026-11-12T19:44:52.891542+00:00",
  "version": 1
}
```
