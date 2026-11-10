---
system: home-network
status: verified
checked: 2026-11-10
tags: [tv, lampa, torrserver, docker]
---
# Home network: TorrServer on the Linux PC

## Task

Continue home-network phase 1: the user installed Media Station X, confirmed Lampa opens, and chose the current Linux PC for TorrServer.

## Context

The [home-network map](../systems/home-network.md) originally planned TorrServer on a future mini PC. The user now selected this PC, connected to the home router. Ubuntu 20.04.6, x86_64, Docker Engine 27.2.0; LAN interface `wlp0s20f3`, address `192.168.192.107/24`.

## Actions

Read-only checks confirmed Docker works, TCP 8090 has no listener and no container named `torrserver` exists. Upstream Docker instructions: https://github.com/YouROK/TorrServer.

Proposed the official image, LAN-bound port 8090, persistent data and Docker restart policy. The user explicitly approved with `Да`. Executed:

```bash
docker run -d --name torrserver --restart unless-stopped -p 192.168.192.107:8090:8090 -v /home/slnnk/ai-data/torrserver:/opt/ts ghcr.io/yourok/torrserver:latest
```

## Findings

Lampa startup via Media Station X is confirmed by the user. Image download completed with digest `sha256:2d02152b804946848f032dcca94fa0f096c8840cff3d37e1ba5400c30f70e16b`. Docker inspection reports `running`, restart policy `unless-stopped`, and TCP 8090 published only on `192.168.192.107`. GET `http://192.168.192.107:8090/echo` returned HTTP 200 and `MatriX.150`. Startup log confirms configuration, logs and torrents under `/opt/ts`.

## Changes

Approved local Docker deployment and data directory above. No router, firewall, VPN or repository changes.

## Status and risks

Deployment and host-side HTTP verification completed. No installation command remains running. The persistent `torrserver` container is intentionally active; check with `docker ps --filter name=torrserver`, stop with `docker stop torrserver` if requested. TV access and video playback remain unverified. The PC must stay on while viewing. Its current LAN address may change with DHCP. The existing home-network phase 1 item in [central TODO](../../../TODO.md) remains open and covers the remaining setup and playback check.

## Portable lesson

none

## Cache configuration inspected

Read-only inspection of `/home/slnnk/ai-data/torrserver/config/settings.json`, under `BitTorr`, found `CacheSize: 67108864` (64 MiB), `UseDisk: false`, `PreloadCache: 50`, `ReaderReadAHead: 95`, `RemoveCacheOnDrop: false`. Only nonsecret cache fields were printed. The current persisted configuration therefore uses a bounded RAM cache, not disk storage for downloaded video pieces. Upstream cache code supports either RAM or disk and evicts eligible pieces above capacity; it is not necessary to keep an entire film in memory. RAM content does not survive process restart. No settings or runtime changes, playback, downloads, or background commands were started for this inspection.
