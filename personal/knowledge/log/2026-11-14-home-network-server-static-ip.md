---
system: home-network
status: verified
checked: 2026-11-14
tags: [netplan, home-server]
---
# Home server: persistent static LAN address

## Task
Change the newly installed home server from DHCP IPv4 `192.168.168.180` to persistent static `192.168.168.2`.

## Context
[Home network](../systems/home-network.md). Host `home`, Ubuntu 26.04.1 LTS, interface `enp1s0`, MAC `d8:bb:c1:a7:5e:83`; systemd-networkd via Netplan. Router DHCP pool was previously verified as `.100` through `.249`. Target address returned no ping or ARP response during preflight; this is not proof against an offline address holder.

## Actions
Read-only preflight established `/24`, gateway/DNS `192.168.168.1`, DHCPv4 and DHCPv6 enabled. Prepared local YAML, presented the exact address/gateway/DNS and backup proposal; user explicitly approved. One SSH mutation backed up and updated Netplan, validated with `netplan generate`, and launched `netplan apply` through a transient systemd unit to survive SSH interruption.

## Findings
SSH to `192.168.168.2` verified the existing server host key using `HostKeyAlias=192.168.168.180`. Runtime IPv4 is `192.168.168.2/24`, default route is static via `192.168.168.1`, gateway ping passed 2/2, and `getent ahostsv4 example.com` resolved successfully. Netplan apply journal records successful deactivation; transient unit was collected.

## Changes
Remote `/etc/netplan/00-installer-config.yaml`: disable DHCPv4, set static IPv4, default route and router DNS; retain DHCPv6 and MAC/name matching. Original configuration retained at `/etc/netplan/00-installer-config.yaml.before-static-20261114`. Local proposal at `/home/slnnk/ai-data/home-server/00-installer-config.yaml`.

## Status and risks
Completed and runtime verified. Configuration is persistent; reboot was not requested or performed. No background task remains. No new follow-up is needed; the separate existing home-server media planning backlog remains unchanged and unauthorized for implementation.

## Portable lesson
none
