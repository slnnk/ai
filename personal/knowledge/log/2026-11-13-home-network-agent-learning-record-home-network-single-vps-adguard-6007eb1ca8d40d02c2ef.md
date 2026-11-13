---
system: home-network
status: verified
checked: 2026-11-13
tags: [agents, learning]
---
# Agent learning: home-network-single-vps-adguard

## Summary

Correction evidence and scoped application history. Canonical instructions remain authoritative.

```agent-learning-json
{
  "created": "2026-11-13T20:05:45.618860+00:00",
  "decisions": [
    {
      "at": "2026-11-13T20:21:19.778197+00:00",
      "decision": "adopted",
      "expected": "Use one VPS AdGuard Home on it-garage-de-02 at d.slnnk.com, without Unbound or home AdGuard, with Cloudflare and AdGuard Unfiltered DoH. Serve dynamic home/mobile clients; prepare locally when requested and require separate deployment approval.",
      "revision": 2,
      "source": "/home/slnnk/ai/personal/knowledge/log/2026-11-13-home-network-ansible-dns-role.md",
      "target": "/home/slnnk/ai/personal/knowledge/systems/home-network.md"
    }
  ],
  "evaluations": [],
  "expected": "Use one VPS AdGuard Home on it-garage-de-02 at d.slnnk.com, without Unbound or home AdGuard, with Cloudflare and AdGuard Unfiltered DoH. Serve dynamic home/mobile clients; prepare locally when requested and require separate deployment approval.",
  "key": "home-network-single-vps-adguard",
  "kind": "explicit",
  "layer": "personal",
  "occurrences": [
    {
      "agent": "codex",
      "at": "2026-11-13T20:05:45.618860+00:00",
      "cause": "",
      "event_id": "2026-11-13-user-single-vps-adguard-mobile",
      "expected": "Plan one AdGuard Home with Unbound on it-garage-de-02 at d.slnnk.com; omit home AdGuard and account for dynamic mobile clients. Preserve the implementation pause.",
      "source": "User decision in the 2026-11-13 DNS-role discussion after pausing implementation.",
      "summary": "User chose a single VPS AdGuard Home and explicitly needs access from phones on mobile networks."
    }
  ],
  "repo": "",
  "revision": 2,
  "scope": "personal",
  "summary": "User retained one VPS AdGuard Home and accepted external encrypted upstreams without Unbound.",
  "system": "home-network",
  "target": "/home/slnnk/ai/personal/knowledge/systems/home-network.md",
  "task_id": "",
  "updated": "2026-11-13T20:21:19.778197+00:00",
  "version": 1
}
```
