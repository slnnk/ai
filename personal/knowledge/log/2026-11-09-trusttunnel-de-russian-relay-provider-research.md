---
system: trusttunnel-de
status: verified
checked: 2026-11-09
tags: [vpn, hosting, private-network]
---
# Russian relay: cross-country private network provider research

## Task
Find a provider offering VMs in Russia and abroad with a private network between countries for a personal VPN relay.

## Context
Discussion only; existing [TrustTunnel system](../systems/trusttunnel-de.md) remains unchanged. Proposed topology: client to Russian nginx stream relay to a foreign TrustTunnel endpoint.

## Actions
Reviewed official public product documentation. No provider was contacted and no purchase, deployment or network test was performed.

## Findings
- [Timeweb Cloud VPC](https://timeweb.cloud/services/vpc): standard cloud VPC is within one location. Its custom routed-network service explicitly describes connecting cloud and dedicated servers across regions and countries using own backbones and operator partners. Russia, Netherlands and Germany appear on the page. This is the strongest documented candidate; eligibility and price for two 1 GB VMs, specific country pairs and physical transport remain unconfirmed. No standard low-cost cross-country SKU was verified.
- [Selectel global router](https://selectel.ru/services/additional/local-network/): explicitly excludes private networks between countries, including Moscow to Tashkent.
- [Serverspace private subnet](https://serverspace.kz/support/help/kak-sozdat-chastnuyu-podset/): documented scope is servers in one data center; does not establish cross-country support.
- [Melbicom vMesh](https://www.melbicom.net/vmesh/) describes intra-DC connectivity; [launch announcement](https://www.melbicom.net/news/vmesh-scalable-private-networks-for-vps-everywhere/) requires instances in the same region. Availability in multiple locations does not prove connectivity between them.
- [HOSTKEY VLAN](https://hostkey.ru/services/servers-communication/) applies to custom-configuration servers and describes rack/server switching; it does not establish the requested small-VM cross-country service.

## Changes
Research note and a link in the existing system map only.

## Status and risks
Research complete. No provider is verified by an actual connection test. Custom Timeweb applicability and cost are unknown. No procurement, support outreach or implementation requested; no new execution backlog or background operations.

## Portable lesson

none
