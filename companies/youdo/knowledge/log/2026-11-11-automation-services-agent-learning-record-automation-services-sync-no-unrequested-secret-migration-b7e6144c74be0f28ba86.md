---
system: automation-services
status: verified
checked: 2026-11-11
tags: [agents, learning]
---
# Agent learning: automation-services-sync-no-unrequested-secret-migration

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-11T20:09:32.197347+00:00",
  "decisions": [
    {
      "at": "2026-11-11T20:27:42.386406+00:00",
      "decision": "adopted",
      "expected": "For current sync runner work, Nexus auth uses docker and prod_selectel nexus_docker_password. User subsequently authorized replacing registry auth and S3 credentials only in the two uncommitted host_vars01/02 using exact Vault keys gitlab_runner_registry_auth, gitlab_runner_s3_access_key and gitlab_runner_s3_secret_key. Preserve all other fields/files; broader secret migration and external writes still require approval.",
      "revision": 2,
      "source": "User explicitly created gitlab_runner_s3_access_key, gitlab_runner_s3_secret_key and gitlab_runner_registry_auth and requested replacing only uncommitted files in the current session.",
      "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-11-automation-services-local-changes-audit.md"
    }
  ],
  "evaluations": [],
  "expected": "For current sync runner work, Nexus auth uses docker and prod_selectel nexus_docker_password. User subsequently authorized replacing registry auth and S3 credentials only in the two uncommitted host_vars01/02 using exact Vault keys gitlab_runner_registry_auth, gitlab_runner_s3_access_key and gitlab_runner_s3_secret_key. Preserve all other fields/files; broader secret migration and external writes still require approval.",
  "key": "automation-services-sync-no-unrequested-secret-migration",
  "kind": "task",
  "layer": "current",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-11T20:09:32.197347+00:00",
      "cause": "",
      "event_id": "2026-11-11-runner-nexus-scope-correction",
      "expected": "For the current sync runner Nexus task, add only Nexus docker auth using prod_selectel nexus_docker_password and its env-output protection. Preserve existing registry credentials, S3 and other runner settings. The repository-wide Vault requirement does not authorize migrating unrelated legacy secrets in this step.",
      "source": "User correction in current session: Why are you changing what I did not request? followed by reverting the unrequested migration.",
      "summary": "User rejected expanding Nexus auth work into migration of existing GitLab Registry and S3 credentials and unrelated logging changes."
    }
  ],
  "repo": "/home/slnnk/git/automation-services",
  "revision": 2,
  "scope": "repo",
  "summary": "User rejected expanding Nexus auth work into migration of existing GitLab Registry and S3 credentials and unrelated logging changes.",
  "system": "automation-services",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-11-automation-services-local-changes-audit.md",
  "task_id": "automation-services-sync-runner-nexus",
  "updated": "2026-11-11T20:27:42.386406+00:00",
  "version": 1
}
```
