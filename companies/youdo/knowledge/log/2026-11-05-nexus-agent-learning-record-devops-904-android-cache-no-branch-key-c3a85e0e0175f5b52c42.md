---
system: nexus
status: verified
checked: 2026-11-05
tags: [agents, learning]
---
# Agent learning: devops-904-android-cache-no-branch-key

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-05T18:11:49.255124+00:00",
  "decisions": [
    {
      "at": "2026-11-05T18:13:10.904952+00:00",
      "decision": "adopted",
      "expected": "For DevOps-904 product Android dependency caching use exactly gradle-cache without branch or toolchain suffixes. This changes the discussed plan; existing repository and external-change approval gates remain.",
      "revision": 2,
      "source": "User correction on 2026-11-05: use exactly gradle-cache.",
      "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-05-nexus-agent-learning-record-devops-904-android-cache-no-branch-key-c3a85e0e0175f5b52c42.md"
    }
  ],
  "evaluations": [],
  "expected": "For DevOps-904 product Android dependency caching use exactly gradle-cache without branch or toolchain suffixes. This changes the discussed plan; existing repository and external-change approval gates remain.",
  "key": "devops-904-android-cache-no-branch-key",
  "kind": "task",
  "layer": "current",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-05T18:11:49.255124+00:00",
      "cause": "",
      "event_id": "devops-904-20261105-no-branch-key",
      "expected": "For DevOps-904 product Android dependency caching, propose a shared toolchain-versioned key such as android-deps-gradle813-jdk21-v1 without CI_COMMIT_REF_SLUG; this correction changes the plan only and grants no implementation or external-settings permission.",
      "source": "User correction on 2026-11-05 in DevOps-904 Android cache planning: item 3 must not split by branch.",
      "summary": "User rejected branch-specific keys in the product Android Gradle cache proposal."
    }
  ],
  "repo": "",
  "revision": 2,
  "scope": "current",
  "summary": "User selected the exact shared product Android Gradle cache key gradle-cache.",
  "system": "nexus",
  "target": "/home/slnnk/ai/companies/youdo/knowledge/log/2026-11-05-nexus-agent-learning-record-devops-904-android-cache-no-branch-key-c3a85e0e0175f5b52c42.md",
  "task_id": "DevOps-904",
  "updated": "2026-11-05T18:13:10.904952+00:00",
  "version": 1
}
```
