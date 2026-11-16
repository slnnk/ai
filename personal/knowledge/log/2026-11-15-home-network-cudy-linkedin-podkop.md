---
system: home-network
status: verified
checked: 2026-11-15
tags: [podkop, linkedin, cudy]
---
# Cudy: LinkedIn domains added to podkop

## Task

Add the user-specified [v2fly LinkedIn list](https://github.com/v2fly/domain-list-community/blob/master/data/linkedin)
to the home Cudy router VPN routing.

## Context

[Home network](../systems/home-network.md). Existing dynamic manual list in
podkop.main on Cudy192.168.168.1; sing-box routes listed destinations through
the existing main selector and TrustTunnel.

## Actions

Read source and existing router configuration. Proposed all12 literal domains,
including conversion of three full-prefixed entries to suffix matching as used by
the existing manual list. User explicitly approved this concrete change.
Ran the existing local add_domains.py helper once with label linkedin and --apply.
It saved a private backup, added12 domains, committed UCI and reloaded podkop.
The reload returned exit9 without diagnostics, so helper verification did not run.
Independent read-only checks then verified the resulting state successfully.
A first verification attempt failed locally before SSH due to unsupported Python
str.removeprefix; the compatible retry passed.

## Findings

All12 source names are present and return FakeIP198.18/15 through router DNS.
All previous manual domains remain. UCI exports excluding manual domain entries
have identical SHA256 before/after, confirming other settings were preserved.
Generated sing-box configuration passes sing-box check; service instance is running.
Failover selected trusttunnel-out with zero failures; router egress probe returned
152.234.226.70. Podkop logs reported successful list update despite reload exit9;
the precise nonzero return cause remains unverified. No repeat reload was needed.

## Changes

Remote /etc/config/podkop main user_domains:12 appended domain suffixes.
Backup: /root/cudy-before-v2fly-linkedin/podkop.
Local source and verification: /home/slnnk/ai-data/cudy/linkedin-domains/.
No repository, firewall, DNS upstream or failover configuration changes.

## Status and risks

Completed2026-11-15. Routing/DNS and running service verified; interactive LinkedIn
login was not tested. Three original full matches also cover subdomains, as disclosed
and approved. Compared task records with central TODO: no matching open item or new
required action. All task commands exited; no task background operation remains.

## Portable lesson

none
