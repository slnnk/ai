---
system: home-network
status: verified
checked: 2026-11-10
tags: [tv, lampa, jackett, docker]
---
# Home network: Jackett on the Linux PC

## Task

Continue the user's TV/Lampa setup after enabling the parser produced a missing Jackett URL error. Deploy Jackett on the existing Linux PC for local torrent search.

## Context

TorrServer MatriX.150 is already running at `http://192.168.192.107:8090`; see [deployment](2026-11-10-home-network-pc-torrserver.md). Torrent playback and torrent discovery are separate services. Read-only checks found no Jackett container and no listener on TCP 9117. Local user/group IDs are 1001.

## Actions

Proposed `lscr.io/linuxserver/jackett:latest`, LAN-bound TCP 9117, persistent settings in `/home/slnnk/ai-data/jackett`, and Docker restart policy. The user explicitly approved with `Да`. Executed:

```bash
docker run -d --name jackett --restart unless-stopped -e PUID=1001 -e PGID=1001 -e TZ=Europe/Moscow -p 192.168.192.107:9117:9117 -v /home/slnnk/ai-data/jackett:/config lscr.io/linuxserver/jackett:latest
```

Image documentation: https://github.com/linuxserver/docker-jackett. No indexers or external search accounts were configured under this approval.

## Findings

Image download completed: digest `sha256:4449c813592f6169dbb38bf0e966775e618905a267cd46538901060c6bb978d1`. The amd64 manifest lists 81,334,866 compressed bytes overall; the slow final layer is 68,962,791 bytes. Docker reports `running`, restart `unless-stopped`, and TCP 9117 published only on `192.168.192.107`. Startup log reports LinuxServer image version `v0.24.3042-ls32` and a listener on port 9117. A bare request to `/UI/Dashboard` returned HTTP 400 with `Cookies required`; a cookie-aware client opening `/` and then `/UI/Dashboard` received HTTP 200 for both. No configuration changes were needed for that response. API keys and session cookies were not printed or copied into notes.

## Changes

User-approved Docker deployment with data in `/home/slnnk/ai-data/jackett`. No router, firewall, VPN or repository changes. Do not copy generated API credentials into notes; use the service UI for manual Lampa entry, or the personal `.env` for authorized scripted access.

## Status and risks

Installation and browser-style HTTP verification completed. Installation and manifest-query commands have finished. The persistent `jackett` container remains intentionally active; check with `docker ps --filter name=jackett`, stop only when requested with `docker stop jackett`. Lampa integration, indexer selection and video playback remain pending under the existing home-network phase 1 item in [central TODO](../../../TODO.md). The PC must remain on and its DHCP address can change. Indexer configuration is a separate service-state change and requires confirmation before agent execution.

## Portable lesson

none

## Subsequent indexer setup

On 2026-11-10 the user requested three popular sources. RuTor, The Pirate Bay and YTS are now configured and passed Jackett Test; see the [follow-up result](2026-11-10-home-network-jackett-indexers.md). This supersedes only the earlier pending indexer-selection status; TV-side integration and playback remain unverified.

## Lampa parser connection diagnosis

The user subsequently reported the generic parser connection error and explicitly confirmed the configured base URL is `http://192.168.192.107:9117`. Read-only checks reconfirmed the PC LAN IP, running container, published/listening TCP 9117 and the three configured sources. An unauthenticated API request with `Origin: http://lampa.mx` returned HTTP 401 and no CORS headers; OPTIONS returned HTTP 405 and no CORS headers. A nonsecret-only configuration inspection found `AllowCORS: false`, `AllowExternal: true`, `Port: 9117`. Upstream `Startup.cs` enables CORS middleware only when `AllowCORS` is true, and Lampa makes a cross-origin JSON API request. CORS is a confirmed missing requirement and a likely cause of the TV-side error; no authenticated TV request was observed, so do not claim it is the sole cause. TV browser reachability and entered API-key status were asked but remain unconfirmed at this point.

Proposed changing only the service CORS setting to true, which requires a web-host restart according to upstream `ServerConfigurationController.cs`. No setting or runtime change was made during diagnosis. Await explicit approval before the service API write/restart; the existing home-network phase 1 backlog item covers completion. All diagnostic commands finished.

## CORS correction applied

The user explicitly approved the CORS change/restart with `Да`, then confirmed the Jackett UI opens in the TV browser and the Lampa API key is correct. This supersedes the earlier pending approval, TV reachability and user-key-status uncertainty. Retrieved the current settings through the cookie-authenticated service API, changed only `cors` from false to true and POSTed the preserved configuration to `/api/v2.0/server/config`. Save returned HTTP 200; Jackett's web-host restart is performed by this API when CORS changes. No separate container restart was needed.

Post-change GET confirmed `cors: true`. A cookie-authenticated API request for configured indexers with `Origin: http://lampa.mx` returned HTTP 200 and `Access-Control-Allow-Origin: *`; configured IDs remain exactly `rutor`, `thepiratebay`, `yts`. Docker inspection confirms the container is running, restart policy `unless-stopped`, port bound only to `192.168.192.107`. Keys, cookies and configuration response bodies containing secrets were not printed or persisted in notes. TV-side retry after restarting Lampa and actual playback remain unverified under the existing home-network phase 1 backlog item. All change and verification commands finished; only the intended Jackett/TorrServer services remain running.

The user subsequently confirmed the setup works. This resolves the pending TV-side parser retry above. At the user's request, sources were then changed to Russian-language RuTor and NNM-Club, with RuTracker.org awaiting manual user credential entry; see [current source selection](2026-11-10-home-network-jackett-indexers.md#russian-language-sources-selected).

