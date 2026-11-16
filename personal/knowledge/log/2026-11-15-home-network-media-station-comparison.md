---
system: home-network
status: verified
checked: 2026-11-15
tags: [media, torrent, dlna, nas, android]
---
# 4K torrent media station comparison

## Task
Compare existing home-01, Synology NAS and Android HDMI box for convenient torrent discovery and 4K viewing. User explicitly excludes Uptime Kuma, Immich and Synology Photos from this comparison. This narrows this analysis only; no service removal or global cancellation is implied.

## Context
Existing server has Intel Core i3-10105 and approximately 16GB RAM based on previous diagnostics. Native TV playback of the saved full MKV, including seeking, was accepted smooth; browser playback stalls remain unresolved. See [playback evidence](2026-11-14-home-network-4k-playback.md#native-dlna-playback-accepted-smooth-including-seeking).

## Findings
- Existing server: qBittorrent + VueTorrent + existing Jackett, completed-download-only MiniDLNA is the lowest additional equipment cost proposal. Radarr is optional for movie catalog and release policies. No deployment or permanent library is claimed.
- Synology: Media Server provides DLNA; Download Station offers built-in/extensible BT search, but current Russian tracker compatibility was not tested. Container Manager on a supported model permits the same search/download stack as Linux. It does not improve TV-side decoding or bypass native TV codec limits. Video Station is unavailable from DSM7.2.2; do not sell it as a current built-in cinema interface.
- Android: native external player over HDMI bypasses VIDAA browser playback. Local TorrServer is possible, but memory is shared with Android/player; do not copy the existing server's4GiB cache onto a4GB box. Standalone local Jackett equivalent is not assumed. Reusing existing server-side Jackett/TorrServer with an HDMI box is a practical hybrid proposal.
- TorrServer has optional DLNA, including live torrent delivery; exact TV integration/seeking has not been tested. Saved-file success does not prove live-torrent success.
- Prefer server for saved-library workflow without new equipment, Android for couch-controlled on-demand viewing. NAS purchase is justified by storage organization/expansion rather than improved 4K playback alone. No prices, wattage or universal Dolby Vision compatibility asserted.

## Sources
- https://github.com/VueTorrent/VueTorrent
- https://github.com/qbittorrent/search-plugins/wiki/How-to-configure-Jackett-plugin
- https://radarr.video/
- https://www.synology.com/en-us/dsm/7.2/software_spec/media_server
- https://www.synology.com/en-global/dsm/7.2/software_spec/video_station
- https://kb.synology.com/en-us/DSM/help/DownloadStation/download_setup
- https://www.synology.com/en-global/dsm/packages/ContainerManager
- https://github.com/YouROK/TorrServer
- https://www.homatics.com/products/box-r-4k-plus

## Changes
Knowledge bookkeeping only; updated existing system map and comparison backlog scope. No infrastructure, repository task code, purchase or migration.

## Status and risks
Comparison complete2026-11-15; hardware choice and implementation remain undecided under existing central TODO media evaluation/workflow items. Exact model, firmware, DV profiles, audio passthrough and worst-case 4K seeking require validation before purchase acceptance. No new task background operations; existing temporary tv-dlna-test intentionally remains active according to prior accepted state, not live rechecked in this comparison.

## Portable lesson
none
