---
system: home-network
status: verified
checked: 2026-11-10
tags: [lampa, jackett, indexers]
---
# Home network: public Jackett indexers for Lampa

## Task

The user explicitly requested adding about three popular torrent indexers through Jackett's `Add indexer` workflow.

## Context

[Jackett](2026-11-10-home-network-pc-jackett.md) runs on the Linux PC at `http://192.168.192.107:9117`. Lampa needs search sources in addition to the already deployed TorrServer.

## Actions

Read Jackett's current indexer list and the upstream definitions. Initially selected public sources requiring no account: RuTor (`rutor`), 1337x (`1337x`), The Pirate Bay (`thepiratebay`). Announced the selected sources. Used the same configuration API as the UI: GET `/api/v2.0/indexers/{id}/config`, followed by POST of the default form to the same path. All three saves returned HTTP 204.

Tested each with POST `/api/v2.0/indexers/{id}/test`. RuTor and The Pirate Bay passed (HTTP 204). 1337x failed HTTP 500 with `Challenge detected but FlareSolverr is not configured`. Announced replacement within the requested three-indexer scope; added public YTS (`yts`) with its default configuration and verified its test returned HTTP 204. Removed only the failed 1337x configuration created in this task (DELETE returned HTTP 200). No FlareSolverr or other service was installed.

Local helper: `/home/slnnk/ai-data/jackett/indexers.py` (`list`, `config`, `add`, `test`, `remove`). It uses the service's browser cookies in memory and does not print API keys, cookies, torrent titles or download links. No credentials were copied into notes or command output. No source repository edits or Git publication.

## Findings

Final GET of configured indexers returned exactly RuTor, The Pirate Bay and YTS, all `configured: true`. All three passed Jackett's built-in Test. RuTor supplies Russian-language releases; the other two are English-language sources, and YTS specialises in movies. No user download or playback was started.

## Changes

Three tested public indexer configurations in the existing Jackett service: RuTor, The Pirate Bay, YTS. No firewall, VPN, router or container changes.

## Status and risks

Requested indexer addition and verification completed; all task commands finished. Jackett and TorrServer remain intentionally active as previously deployed. Their check/stop commands are recorded in the deployment notes. The existing home-network phase 1 item in [central TODO](../../../TODO.md) continues to cover Lampa integration and playback verification. Availability of public trackers can change; successful backend tests do not prove TV-side playback.

## Portable lesson

none

## Russian-language sources selected

The user confirmed the setup now works after the CORS fix, then requested Russian-language sources, naming RuTracker and RuTor. This is a home-media source preference, not a global rule. Read current forms and upstream definitions: NoNaMe Club (`noname-club`, NNM-Club) is a Russian public source requiring no account in Jackett; RuTracker.org (`rutracker`) requires username/password and may display a captcha. The separately listed `rutracker-ru` is not the selected RuTracker.org source. Byrutor currently points to a games-focused site and was not selected for TV/movie use.

Added `noname-club`: configuration save and Test both returned HTTP 204. Announced removal of the two English-language sources and deleted only `thepiratebay` and `yts` (HTTP 200 each). Final configured list is exactly `noname-club` and `rutor`, both `ru-RU`. This supersedes the earlier three-source set; the earlier actions and test results remain historical evidence.

The user confirmed having a RuTracker.org account and chose to enter credentials in the local Jackett UI. No credentials were requested in chat, read, copied or submitted by the agent. Provide manual steps: open Jackett, `Add indexer`, select `RuTracker.org`, enter username/password, complete captcha if shown, save and test. RuTracker is not yet configured; awaiting the user's manual credential entry is the only remaining source-setup step. The existing home-network phase 1 item in [central TODO](../../../TODO.md) remains open for the broader router/network work. User-confirmed working Lampa integration does not independently prove a particular movie's audio/seek behavior. All commands finished; only the intentionally deployed services remain active.

## RuTracker Cloudflare prerequisite

The user's attempted RuTracker save returned `Challenge detected but FlareSolverr is not configured`. This supersedes the assumption that manual credential entry alone is sufficient for this endpoint. No credentials were shared or inspected. Official Jackett documentation describes FlareSolverr integration for Cloudflare-protected indexers: https://github.com/Jackett/Jackett#configuring-flaresolverr. Official image/setup: https://github.com/FlareSolverr/FlareSolverr.

Read-only checks: no `flaresolverr` container, TCP 8191 free, about 11 GB available RAM; Jackett uses Docker's default bridge. Docker network name `home-media` is unused. Proposed implementation: create `home-media`, connect existing Jackett to it while preserving its existing published port, start official `ghcr.io/flaresolverr/flaresolverr:latest` there with restart `unless-stopped` and no host port publication, then set Jackett's FlareSolverr URL to `http://flaresolverr:8191`. Keep its existing timeout unless testing shows a reason to change it. This API configuration may restart Jackett's web host. The browser-containing image needs downloading and the prior registry transfer was slow.

Await explicit approval for this new service/network/configuration change. No install, Docker network change, Jackett settings write or browser challenge was executed. All read-only checks finished. Existing RuTor/NNM-Club remain the working configured sources; RuTracker retry remains within the existing phase 1 backlog item.

## FlareSolverr installed and RuTracker verified

The user explicitly approved installation and integration. FlareSolverr 3.5.2 is now deployed on private Docker network `home-media` with restart `unless-stopped` and no published host port. Jackett uses `http://flaresolverr:8191`, timeout 55000 ms and CORS true. Container-to-container health and a public RuTracker login-page challenge both passed; the latter returned `Challenge solved!` and HTTP 200. Jackett lists exactly RuTor, NNM-Club and RuTracker.org configured, and RuTracker's built-in Test returned HTTP 204. This supersedes the earlier pending solver approval and manual source-setup blocker. No credentials were read or printed. See [deployment and checks](2026-11-10-home-network-pc-flaresolverr.md). TV-side playback with RuTracker remains untested; all installer/check commands are finished and the intended services remain active.
