---
system: home-network
status: verified
checked: 2026-11-13
tags: [agents, learning]
---
# Agent learning: home-network-public-dot

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-13T20:06:38.602405+00:00",
  "decisions": [],
  "evaluations": [
    {
      "at": "2026-11-13T20:21:20.119455+00:00",
      "cause": "",
      "event_id": "2026-11-13-dns-role-first-applicable-attempt",
      "expected": "Allow DoT on TCP 853 from any client IP without IP/CIDR/ASN allowlists. Keep plain DNS and administration private; preserve the implementation pause and separate deployment approval.",
      "outcome": "pass",
      "revision": 1,
      "rule_loaded": "yes",
      "source": "/home/slnnk/ai/personal/knowledge/log/2026-11-13-home-network-ansible-dns-role.md",
      "target": "/home/slnnk/ai/personal/knowledge/systems/home-network.md"
    }
  ],
  "expected": "Allow DoT on TCP 853 from any client IP without IP/CIDR/ASN allowlists. Keep plain DNS and administration private; preserve the implementation pause and separate deployment approval.",
  "key": "home-network-public-dot",
  "kind": "explicit",
  "layer": "personal",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-13T20:06:38.602405+00:00",
      "cause": "",
      "event_id": "2026-11-13-user-unrestricted-dns-clients",
      "expected": "Allow DoT on TCP 853 from any client IP without IP/CIDR/ASN allowlists. Keep plain DNS and administration private; preserve the implementation pause and separate deployment approval.",
      "source": "User decision in the 2026-11-13 single-VPS DNS discussion: no access restrictions.",
      "summary": "User chose unrestricted client access to the planned VPS encrypted DNS endpoint."
    }
  ],
  "repo": "",
  "revision": 1,
  "scope": "personal",
  "summary": "User chose unrestricted client access to the planned VPS encrypted DNS endpoint.",
  "system": "home-network",
  "target": "/home/slnnk/ai/personal/knowledge/systems/home-network.md",
  "task_id": "",
  "updated": "2026-11-13T20:21:20.119455+00:00",
  "version": 1
}
```
