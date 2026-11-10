---
system: home-network
status: verified
checked: 2026-11-10
tags: [lampa, jackett, flaresolverr, docker]
---
# Home network: FlareSolverr for Jackett RuTracker

## Task

Install and connect FlareSolverr to Jackett after the user's RuTracker.org setup hit `Challenge detected but FlareSolverr is not configured`.

## Context

The user confirmed Lampa now works after enabling CORS. Russian-language RuTor and NNM-Club are configured and tested; RuTracker.org needs its browser challenge handled. The user will enter account credentials directly in Jackett. See [source selection and prerequisite](2026-11-10-home-network-jackett-indexers.md#rutracker-cloudflare-prerequisite).

## Actions

Proposed official FlareSolverr container, private Docker network `home-media`, connecting existing Jackett, URL `http://flaresolverr:8191`, restart policy and no host port publication. The user explicitly approved with `Да`. Created `home-media`, connected Jackett, and started:

```bash
docker run -d --name flaresolverr --network home-media --restart unless-stopped --tmpfs /tmp:size=256M,mode=1777 -e LOG_LEVEL=info -e TZ=Europe/Moscow ghcr.io/flaresolverr/flaresolverr:latest
```

The official documentation recommends the browser-containing Docker image and optional RAM-backed browser temporary storage. Documentation: https://github.com/FlareSolverr/FlareSolverr and https://github.com/Jackett/Jackett#configuring-flaresolverr.

## Findings

Network creation/connection completed. Image download completed after an automatic retry of the largest layer: digest `sha256:c80ae007ce2ccdcd217a12426e4f039ef763ff90738c808d38810c3e59323767`. The amd64 image manifest totals 292,147,560 compressed bytes; the largest layer is 223,460,165 bytes. Docker reports roughly 735 MB unpacked.

From inside Jackett, GET `http://flaresolverr:8191/` returned ready status and version `3.5.2`, proving container DNS and service connectivity. Applied only Jackett's `flaresolverrurl` from null to `http://flaresolverr:8191`; save returned HTTP 200 and the service API applied its web-host restart. Read-back confirmed the URL, unchanged timeout 55000 ms and `cors: true`.

A FlareSolverr request for the public `https://rutracker.org/forum/login.php` with 55000 ms maximum timeout returned `status: ok`, `Challenge solved!`, page HTTP 200. Cookies and page contents were not printed. The configured-indexer list now contains exactly `noname-club`, `rutor`, `rutracker`; the user's earlier UI setup had saved RuTracker. Ran its built-in Test without reading credentials: HTTP 204. No account values were read, copied or submitted by the agent.

## Changes

Docker network `home-media`, Jackett network attachment, official FlareSolverr deployment and the approved Jackett URL setting. Local nonsecret-output helpers live in `/home/slnnk/ai-data/jackett/`; `flaresolverr_config.py --apply` changes only the FlareSolverr URL via a read-preserve-write of Jackett's settings, retaining CORS and the default timeout. Docker inspection confirms FlareSolverr is `running`, restart `unless-stopped`, connected to `home-media`, with no published host ports.

## Status and risks

Installation, configuration and verification completed, including a successful RuTracker Test. All download, manifest, configuration and test commands finished. FlareSolverr, Jackett and TorrServer remain intentionally active with Docker restart policies. Check FlareSolverr with `docker ps --filter name=flaresolverr`; stop only if requested with `docker stop flaresolverr` (protected-indexer requests then lose the solver). TV-side playback after adding RuTracker is not independently tested; the existing home-network phase 1 item in [central TODO](../../../TODO.md) remains open for broader network work.

During download diagnostics, Docker logs also showed earlier DNS timeouts for NNM-Club against a corporate resolver. No DNS, VPN or router changes were made, and no claim is made that NNM-Club was retested in this final turn. RuTracker's actual page and built-in Test both succeeded after the installation. If NNM-Club errors recur, diagnose that observed symptom separately rather than changing DNS preemptively.

## Portable lesson

none
