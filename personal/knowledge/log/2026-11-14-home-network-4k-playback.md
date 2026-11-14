---
system: home-network
status: verified
checked: 2026-11-15
tags: [lampa, torrserver, ethernet, performance]
---
# 4K playback buffering and home server patch-cord replacement

## Task

User confirmed local Lampa/MSX setup works, but a roughly40GB 4K movie pauses
with buffering. TV is connected by Ethernet. Diagnose playback without changing
router policy, running active speed tests or tuning settings without approval.

## Observations before cable replacement

Read-only SSH: Ubuntu home-01 had load0.05, about14GB available RAM, no swap
usage; TorrServer about44 percent of one CPU and146MiB RAM. enp1s0 negotiated
100Mb/s full duplex, despite both adapter and link partner advertising1000Base-T.
TorrServer uses its default64MiB RAM cache, preload50 percent/read-ahead95;
no configured download/upload rate limit. No tuning was performed.

Read-only POST /torrents action=list returned one active41.33GB torrent.
One snapshot had download26.67Mb/s,11 connected seeders and12 active peers.
Ten-second passive NIC counters averaged RX36.31/TX30.35Mb/s, with zero error
or drop increments. Later samples showed0 download and about49.4MiB cached;
without the player's state this does not establish starvation versus idle/full
buffer behavior. Torrent names, hashes, media URLs and peer IPs were not printed.
Neither NIC saturation nor a single root cause was proven. For a two-hour40GB
file, average encoded payload is about44Mb/s; actual duration/peaks were unknown.

## Patch-cord change

User reported replacing the patch cord. Read-only follow-up confirmed enp1s0
now negotiates1000Mb/s full duplex. Five-second passive traffic averaged
RX23.99/TX17.58Mb/s, zero NIC error increments. The100Mb/s negotiation issue
is resolved; no claim that buffering is resolved until the user retries the film.
No service restart, cache change, source download, speedtest or router mutation.

## Checkpoint and next observation

Expected result: same4K stream plays without repeated buffering after link repair.
User confirmed buffering remains after the cable replacement. If buffering remains,
continue with current torrent download/buffer statistics and the actual file's
bitrate/TV link constraints before proposing targeted cache or network changes.
Earlier cancellation of general speed tests remains; passive counters only were used.
All task diagnostic commands have exited. Intended media services remain running;
no task background operations remain. Central TODO tracks the ongoing playback
check and the separately unapproved broader PC-data migration.

## Portable lesson

none

## Task metrics: home-4k-playback-20261114

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "home-4k-playback-20261114",
  "created": "2026-11-14T20:14:02.708041+03:00",
  "first_result": "unknown",
  "final_result": "unknown",
  "state": "open",
  "kind": "operations",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "4GiB RAM cache and swap disable verified; same-movie playback retest remains pending",
  "updated": "2026-11-14T20:27:04.426530+03:00"
}
```

## Continued diagnostics after gigabit repair

User gave film duration2h30m. The active41.33GB file implies about36.74Mb/s
average payload; instantaneous bitrate remains unknown. Five samples over16s
showed downloads12.52/15.27/11.31/34.45/31.16Mb/s with7-10 connected seeders,
about41-43MiB cached and useful bytes increasing by40.2MiB (about21Mb/s average).
This short, demand-driven sample does not independently establish a swarm ceiling.

Later read-only /cache action=get showed configured capacity64MiB, filled about
70MiB, one active reader and a read-ahead window32 two-MiB pieces. A full cache
can pause demand-driven fetching, so do not infer permanent peer starvation from
low or zero download_speed alone. No single remaining root cause proven.

Official MatriX.150 code was inspected: /settings action=get returns complete
BTSets; action=set replaces it. Preserve unrelated fields with read-merge-write.
SetSettings drops active torrents and reconnects the torrent client, so any cache
trial interrupts the current stream and requires explicitly approved change.
Sources: https://github.com/YouROK/TorrServer/blob/MatriX.150/server/web/api/settings.go
and https://github.com/YouROK/TorrServer/blob/MatriX.150/server/torr/apihelper.go.

Concrete proposed trial, not applied: CacheSize from67108864 to1073741824 bytes
(64MiB to1GiB), PreloadCache from50 to10 percent; keep RAM storage and all other
settings. This gives more room for intermittent throughput but cannot compensate
for a sustained source speed below the file's bitrate. User approval pending.
All new passive diagnostics exited; no task background operations remain.

## User-approved RAM cache and swap changes

User replaced the proposed1GiB cache with `RAM 4 Gb сделай`, authorizing4GiB
RAM cache with the previously proposed10 percent preload. Described the stream
interruption, then applied a read-preserve-write through the official API after
execution approval. Actual values: CacheSize4294967296, PreloadCache10,
UseDiskfalse; all other settings compared equal after the operation. Protected
backup: /opt/torrserver/settings-before-cache-20261114T171929Z.json (mode0600).
Independent SSH read verified persisted BitTorr values in
/opt/torrserver/data/config/settings.json, /echo200, container running/restarts0.
No application restart or image/configuration change was required; the API reset
active torrents as expected. Earlier1GiB proposal is superseded, not executed.

User then explicitly requested disabling swap. Read-only preflight found one
unused4GiB /swap.img file enabled by one /etc/fstab entry and generated
swap.img.swap unit; about14GiB RAM remained available before the operation.
Described runtime/persistent disable, then executed with approval: backup fstab,
swapoff /swap.img, comment only its fstab entry, systemctl daemon-reload.
Backup /etc/fstab.before-swap-disable-20261114T172144Z retained mode0600;
the actual /swap.img file was not deleted. findmnt --verify passed, /proc/swaps
empty. Independent follow-up free showed Swap0/0/0 and no active swap units.
No reboot was performed; persistent fstab configuration was verified directly.

Final snapshot after cache adjustment: about5.3GiB used RAM,10GiB available,
swap0. Persisted4GiB RAM cache and10 percent preload reconfirmed. This does
not establish whether the movie now plays without buffering; same-film retry
remains pending. Broader PC-data migration remains separately unapproved.
All mutation/verification processes finished; no task background commands remain.
No repository changes were made for these runtime requests; current roles
preserve TorrServer settings and do not enable swap.

## Buffering persists with a full cache

User reported buffering still occurs with4GiB cache and swap disabled. Read-only
follow-up: server gigabit link remains, about10GiB RAM available, negligible
TorrServer CPU during the stall, no swap. Four /cache samples over15s showed
about4107MiB filled and3890MiB of continuously complete pieces ahead of the
same reader position361. Download_speed0 is expected with a full demand-driven
cache here and does not imply slow peers. The stalled interval is not explained
by an empty upstream torrent buffer.

TCP inspected inside the TorrServer network namespace: TV192.168.168.160 stream
had3668664 bytes queued/not sent and receiver-window-limited time98.9-99.4 percent.
Two samples5s apart showed identical byte counters; another connection continued
control requests and had earlier delivery samples around95Mb/s. User confirmed
the TV was still displaying loading, not intentionally paused/exited. This localizes
the observed stall to receiving/consuming the stream at the TV side, without proving
an exact codec/player/network defect. Cudy port inspection found only lan2 up at
1000Mb/s; TV's own negotiated Ethernet rate was not established.

Read only2MiB of already-cached initial media with HTTP206 Range, passed in memory
to container ffprobe; no sample file or movie identity saved. Initial1s probe was
too short, repeated probe with10s analysis recognized HEVC Main10 3840x1606,
10-bit level5, multiple AC3/E-AC3 tracks and one AAC-LC2-channel track. Container
duration9948s, so earlier user-provided2h30m/37Mb/s estimate was approximate;
actual file average is about33.24Mb/s. No specific codec incompatibility proven.
Proposed user test: AAC2.0 with subtitles off. No TV track settings changed.

## Requested TV connection

Instead of the manual test, user asked whether the agent could connect to the TV.
Bounded targeted port check found only36669 among tested control ports. TLS1.3
handshake worked; web/debug ports including9222 were not reachable. Read maintainer
docs at https://github.com/tombabolewski/vidaa-control. Installed vidaa-control1.1.0
and dependencies in /tmp/home-vidaa-remote-venv, leaving Ansible environment unchanged.

Described normal VIDAA pairing/read-state action and executed after approval.
Temporary helper /tmp/home-vidaa-pair.py used library dynamic authentication,
local neighbor MAC only in memory, suppressed credential logs and a TokenStorage
adapter storing any certificate pin/tokens only as VIDAA_REMOTE_TOKENS in
personal/.env (mode0600). MQTT connected and TV state was returned without needing
a PIN. No remote keys, app launch, playback or settings commands sent.
Helper disconnected in finally and exited0. This interface provides remote-control
commands/state, not a picture of the TV screen or browser DOM; no screen visibility
was established. Temporary client can be recreated after /tmp cleanup.

Buffering remains unresolved. All probes, samplers and TV connection processes
have exited; no task background operations remain. User-assisted AAC/no-subtitle
test remains pending; further remote UI actions require their own authorization.

## Reproduced PIPELINE_ERROR_NETWORK on another torrent

User selected another torrent, reported code2 / PIPELINE_ERROR_NETWORK after
long initial loading, then explicitly repeated it while passive observation ran.
This file is74.46GB, not the earlier41.33GB file. No runtime settings changed.

Before retry: no active torrents, about14GiB RAM available, swap0; container had
restarts0/OOMfalse with original startup timestamp. Kernel memory-event counts
were zero for15min; Docker/file log scans found no recognized preload/read/error
events. The absence of a matching log line does not prove no request error.

Two bounded read-only samplers caught metadata acquisition and initial peers,
then preload target409.6MiB from4GiB cache/10 percent. Speed rose to100-164Mb/s
with about23 connected seeders. At17:47:10UTC preload completed; reader opened
near piece5 with392MiB continuously ready ahead. At17:47:12UTC reader disappeared,
with443MiB still cached. User confirmed the same NETWORK error immediately after
preloading. This attempt did not fail due to an empty torrent buffer or a measured
source-rate shortage. Earlier hypothesis of waiting for410MiB before a player
timeout was not established; the error followed successful preload completion.

Read2MiB of already cached data with Range and Origin headers and no saved media.
HTTP206, Content-Length2097152, correct Content-Range total74463514940,
Accept-Rangesbytes, Access-Control-Allow-Origin*, Content-Typevideo/x-matroska,
Connectionclose, no Content-Encoding. ffprobe recognized Matroska, HEVC Main10
3840x2160 level5.1, Dolby Vision profile7 with BL/EL/RPU present, multiple
AC3/E-AC3 tracks and one8-channel TrueHD/Atmos track. Duration9949s. Default
audio track actually chosen on TV was not observed; presence of TrueHD alone
does not establish that it caused the failure.

Compatibility hypothesis: browser playback/container/Dolby profile handling.
VIDAA WebApp Development Technical Guide section4.6 lists ISO-BMFF/MP4 and
MPEG2-TS with the supported browser codecs; this older general document is not
proof that this particular TV cannot play any MKV. Dolby documents profile7 as
dual-layer UHD Blu-ray. No exact model-specific limitation or decoder failure
was proven by the generic NETWORK error or the controller's successful HTTP test.

Sources:
- https://www.vidaa.com/wp-content/uploads/2020/12/WebApp_Development_Guide_for_VIDAA.pdf
- https://ott.dolby.com/OnDelKits/Dolby_Vision_Online_Delivery_Kit/v1/Documentation/Specs/Visio_Profiles/help_files/topics/c_dovi_profiles_public.html
- Official TorrServer MatriX.150 preload/API and stream source inspected under
  https://github.com/YouROK/TorrServer/tree/MatriX.150/server

Next controlled test proposed: MP4 with H.264/AVC and AAC, e.g.1080p without
Dolby Vision, to separate basic delivery from the failing MKV/DV path. Earlier
AAC/no-subtitle experiment remains unperformed; this test includes AAC while
also establishing a documented baseline container. No new player/transcoding,
codec conversion, remote key, router or server setting was applied. All probes
and bounded sampler processes exited; no background work remains.

## Alternative player research in response to user proposal

User proposed installing another player and connecting it through MSX. Research
only; no app installation, MSX startup change or TV key commands performed.
MSX official Android Player documentation describes external VLC/MX application
handoff for Android/FireTV (also a different URL-based variant for iOS), not a
confirmed generic VIDAA installation/handoff path:
https://www.msx.benzac.de/wiki/index.php?title=Android_Player.

MSX video/audio plugins are HTML pages in iframes according to the official API;
adding such a plugin does not by itself establish new native codec support:
https://msx.benzac.de/wiki/index.php?title=Video/Audio_Plugin.

Maintainer documentation confirms MSXPlayer has a direct TorrServer client and
uses start parameter msxplayer.ru or v4.msxplayer.ru. A reasonable optional
comparison path is opening the same TorrServer file through that client with
server URL http://192.168.168.2:8090, while the local Lampa frontend remains
available at192.168.168.2:8080. No claim of tested MSXPlayer compatibility with
this TV, DolbyVision7/TrueHD or automatic Lampa-to-MSXPlayer handoff. Reverting
MSX startup to192.168.168.2:8080 restores the current launcher route.
Sources: https://msxplayer.ru/ and
https://msxplayer.ru/docs/launcher/torrserver.html.

This is an option within the existing unresolved TV playback task, not separate
permission to install/change anything. All research tools finished; no background
operations remain. MP4/H264/AAC control remains an unperformed alternative test.

## Additional external player portals rejected

User explicitly stated they do not want to connect to additional external services
while discussing the proposed MSXPlayer route. Scope: home-media playback solution.
Do not redirect MSX startup to msxplayer.ru or another external player portal or
add new external playback-service dependencies without a new user instruction.
This does not cancel existing MSX, tracker/catalog/VPN/DNS services or authorize
installing an alternative local solution. The previous external MSXPlayer proposal
is rejected; preserve its research as historical evidence.

A local alternative was checked against MSX Start Object and Internal Actions
specifications: home-01 can serve a JSON menu/content page containing video:URL
items pointing directly to its TorrServer streams. This uses the already installed
MSX player without an extra external portal or third-party runtime script. A local
same-stream comparison page is a proposed diagnostic path, not an implemented
new player or a confirmed DolbyVision7/TrueHD fix. Automatic handoff from the
current Lampa frontend would be a separate integration to verify.
Sources: https://msx.benzac.de/wiki/index.php?title=Start_Object and
https://msx.benzac.de/wiki/index.php?title=Internal_Actions.
No repo, server or TV changes made in this discussion; all tools finished.

## Restarted diagnosis and working MKV control

User restarted diagnosis from first principles: establish the cause before choosing
solutions. No tuning, new player or external playback service was authorized.
The selection UI exposes size, quality and seeds, so asking the user to select exact
codecs is impractical; inspect candidate media server-side after selection.

A new observed attempt on the 74463514940-byte torrent reproduced
`code [2] details [PIPELINE_ERROR_NETWORK]` immediately after the displayed
409.6 MiB preload. Five-second samples showed a reader at 18:03:15 UTC and none
at 18:03:20 UTC; 450793788 bytes remained cached. The container was running,
OOMKilled false, restart count zero; its last-five-minute Docker log was empty.
This localizes the failure to the transition into playback but does not prove a
codec, HTTP or network cause. Samples do not establish exact HTTP request timing.

User then selected a 4832966955-byte MKV and confirmed playback without delays.
The same 409.6 MiB preload threshold completed; an active reader progressed while
about 1.4 GB remained cached. Read only the first 2 MiB over HTTP Range (206),
passed directly in memory into the existing container ffprobe; no media file saved.
Probe exit 0: H.264 High, level 4.1, yuv420p 8-bit, 1152x482; three AC-3 5.1
tracks and SubRip subtitles; Matroska duration 9948.032 seconds. Selected audio
track was not observed; all enumerated audio tracks use AC-3. This is not a 1080p
control despite the requested UI selection guidance.

Verified conclusion: the current MSX/Lampa/TorrServer route can play at least this
MKV/H.264/AC-3 file; a universal MKV incompatibility and universal preload failure
are contradicted. The failing large file previously probed as 4K HEVC 10-bit with
Dolby Vision profile 7 differs in codec, resolution, dynamic-range metadata and
bitrate. None of those differences is individually established as causal.
A further candidate must be probed to choose a useful comparison. Existing central
TODO remains open; no resolution or additional implementation is claimed.

## Jackett-selected comparison candidate

User identified the film as Dune: Part Two (2024) and asked the agent to find a
suitable release through Jackett instead of delegating selection to the TV UI.
Read-only Jackett GET search used its target-local API key in memory only; no key,
magnet or authenticated URL was printed or saved. Query `Дюна 2` was noisy; full
`Дюна Часть вторая` and `Dune Part Two` searches returned the relevant film releases.
Exact-size matches identify the failed 74463514940-byte UHD BDRemux HDR10/Dolby
Vision release and the successful 4832966955-byte WEB-DL-AVC release on RuTracker.

Selected next candidate: RuTracker `Dune: Part Two [2024, WEB-DL 2160p, SDR]`,
25064810791 bytes (23.34 GiB), 125 seeders at query time. Full title continues
`Dub (Bravo Records Georgia, RHS, Jaskier, HDrezka) + MVO (LostFilm, TVShows, Jaskier) + AVO + Original (Eng) + Sub (Rus, Eng)`.
2160p/SDR are release-title claims, not independently probed metadata. This candidate
can test a 4K SDR path, but differences in bitrate, encoding and audio still prevent
isolating Dolby Vision alone. No torrent added, playback started, remote key sent
or setting changed. Both prior four-minute samplers and Jackett searches exited.
Existing diagnostic TODO remains open. Next playback still needs user selection
and a coordinated observation; no successful 4K result is claimed.

## Confirmed working 4K HEVC 8-bit control

User selected the Jackett candidate and confirmed playback without stalls. Read-only
API confirmed exact torrent size 25064810791 bytes. Five-second samples caught
successful 409.6 MiB preload and continued reader progression after 18:14:29 UTC;
cache filled to approximately 4 GB while playback continued. Reader positions also
jumped; no user intent or seek cause was inferred from these alone.

A bounded 2 MiB HTTP Range read returned 206 and video/x-matroska; in-memory
ffprobe exit 0 identified HEVC Main, 3840x1600, yuv420p 8-bit, level 150,
Matroska duration 10016.215 seconds. No HDR/Dolby Vision side data was reported
by this bounded probe, consistent with the release-title SDR claim. Audio tracks
include E-AC-3 5.1, AC-3 5.1/stereo and AAC-LC stereo; actual TV-selected track
remains unknown. No media sample saved or runtime setting changed.

Conclusion: 4K/HEVC/MKV playback is demonstrated for this file and observed interval,
not for every profile or sustained bitrate. The failing 74.46 GB release differs
in 10-bit profile, HDR/Dolby Vision 7, bitrate and audio options. No single cause
is established. Next proposed comparison is 4K HEVC HDR10 without Dolby Vision;
existing Jackett results contain NoNaMe Club 22861622885-byte release titled
`Дюна: Часть вторая / Dune: Part Two (2024) UHD BDRip [H.265/2160p] [4K, HDR, 10-bit]`
with 5 seeders at search time. Actual HDR format, absence of DV and audio must be
verified after selection; the title alone does not prove HDR10-only metadata.
Central diagnostic TODO remains open, with no implementation decision made.

## HDR10 candidate starts but stalls with limited ready data

User selected the 22861622885-byte candidate and confirmed it plays with intermittent
loading pauses. Exact size verified. In-memory 2 MiB HTTP206 probe, ffprobe exit0:
Matroska, HEVC Main10, 3840x1608, yuv420p10le, level186 (HEVC6.2), BT.2020/PQ,
mastering-display and content-light metadata consistent with HDR10. No Dolby Vision
side data reported in this bounded probe. One E-AC-3 5.1 audio track, SubRip,
attached MJPEG; duration9949.023s. Level field is an observed header value, not
proof of actual decoder resource requirements or an established failure cause.

Sampler showed initial download roughly9-20MB/s, later roughly0.1-0.5MB/s with
1-3 connected seeders while the reader advanced slowly. Cache total grew, but
total filled bytes alone do not show data available at the requested position.
Three focused samples at18:23:08/13/18UTC showed:
- position1119: current8MiB piece only7421952 bytes, Completedfalse;
- position1122: current8MiB piece only6258688 bytes, Completedfalse;
- position1124: two completed pieces including current,16MiB total before gap1126.
TCP TV stream had Send-Q0 in the first two samples; acknowledged bytes increased
from181458021 to204477541 in5s. Third sample had about2.76MB queued and a short
receiver-window-limited period. Thus missing ready data at the reader was observed;
this is not the earlier fully buffered long TV receive stall. Exact screen events
were not timestamped, so not every user-reported pause is assigned a proven cause.
Neither a universal 10-bit/HDR startup incompatibility nor a single cause covering
all releases is established. More stable upstream data is needed to assess this
file's decoder/player behavior. A pause-and-refill comparison without seeking or
settings changes is the proposed next diagnostic step, not yet executed.
Both bounded samplers/probe and the focused three-sample command exited; no task
background operations remain. Existing central playback TODO remains open.

## HDR10 playback stabilized without changes

After the pause/refill proposal, user reported playback had already stopped stalling.
Agent withdrew the pause instruction and requested continued playback without seeking
or changes. User subsequently confirmed no further problems. Exact observation duration
was not supplied; no claim of full-film verification. Pause/refill was not executed and
is superseded by this natural continuation, not a pending diagnostic requirement.

Together with incomplete current pieces and ongoing TCP reception observed earlier,
this supports transient torrent-side ready-data shortage as an explanation for the
initial stalls on the21.29GiB HDR10 candidate. It does not establish the cause of the
separate immediate NETWORK error on the69.35GiB Dolby Vision7 release. Current setup
has demonstrated sustained user-observed playback of this MKV/4K HEVC Main10 HDR10
file, without new player, cache, network or audio-setting changes.

Next proposed comparison: RuTracker WEB-DL2160p HDR10+/Dolby Vision,
37390284387 bytes (34.82GiB),430 seeders in the earlier Jackett search. Actual DV
profile and media parameters still need probing; title alone is insufficient. This
comparison varies encoding, audio and bitrate too, so it cannot isolate DV alone.
No new playback or observation command started; no background work remains.
The existing central task remains open because the original large-release startup
failure is unresolved. No infrastructure solution has been selected or implemented.

## Dolby Vision profile 8 file plays

User reported one loading episode followed by generally normal playback of the
37390284387-byte WEB-DL. Exact torrent size verified. Four-minute passive sampler
exited0; preload completed and reader progressed with growing cache. Later focused
snapshot showed4105.8MiB filled and3880MiB continuously complete including the
current reader piece, with download55.91Mb/s. The single user-reported loading
episode was not precisely timestamped; its cause remains unassigned.

In-memory2MiB HTTP206 probe, ffprobe exit0: MKV, HEVC Main10,3840x1606,
yuv420p10le, level150 (5.0), BT.2020/PQ. DOVI configuration dv_profile8,
dv_level6, BL1/EL0/RPU1, compatibility_id1; this is profile8.1 metadata.
Audio options include E-AC-3/AC-3/AAC, no TrueHD in enumerated tracks. Duration
9948.064s. TV-selected audio and actual displayed HDR/Dolby Vision mode unknown;
playback of this DV-tagged file does not establish that the TV used DV instead of
HDR10-compatible base-layer playback. No media saved, settings or playback changed.

Working controls now cover H.264 MKV,4K HEVC8-bit SDR,4K HEVC10-bit HDR10 and a
4K HEVC10-bit DV8.1-tagged file. Immediate NETWORK error remains specific to the
tested74.46GB UHD BDRemux with DV7 among these candidates. Profile7/enhancement
layer handling, remux structure, bitrate and selected audio remain hypotheses,
not independently isolated causes. Next potentially useful same-file comparison
is selecting AC-3/AAC audio with subtitles off on the original release if the UI
permits pre-playback selection; availability not yet established, no action taken.
All samplers and probes exited; no task background commands remain. Existing
central playback TODO remains open; no fix or full-film validation claimed.

## Repeated DV8 buffering with ready data and receiver backpressure

User reported repeated brief loading episodes on34.82GiB DV8 candidate, including
one around3s. Ten-minute passive sampler started18:39:38UTC (scheduled finish
approximately18:49:38UTC), sampling cache and TCP each second. User then reported
two further episodes during collection. No exact TV playback timestamp or frame
capture, so alignment is approximate to user messages, not proven frame-level.

Received samples around18:42:38-18:43:48UTC showed current pieces complete and
3848-3896MiB continuously cached including current piece. One stream TCP connection
had roughly2.7-4.2MB queued, with multiple intervals where sent/acked byte counters
were unchanged while receiver-window-limited time increased. At18:43:19-22UTC,
bytes_sent/acked2630001985 remained fixed, queued4150352 bytes; position2326,
3888MiB continuous ready data. Sending resumed18:43:23UTC. Similar intermittent
pauses also occur elsewhere in the samples. No bytes_retrans field was emitted for
the media connection by ss; this is not a packet-capture proof of no loss.

Conclusion: torrent starvation does not explain these sampled intervals; data was
ready and server faced receiver backpressure. Receiver-window stalls also occur in
normal buffered playback, so cannot alone establish a decoder/player defect or
exclude every network path issue. Need a controlled same-file test and actual TV
track selection before attributing cause. Current audio/subtitle selections unknown.
The next step is inspect the active audio selection; no settings/UI action applied.

Output retrieval clipped an earlier interval around18:40:27-18:42:37UTC; do not
claim complete reviewed ten-minute coverage. Collector continues as session79330
until its bounded timeout; can be checked through that session or stopped on request.
All one-shot commands have exited. Existing central task remains open; no fix chosen.

## Same-file audio comparison: fourth then first track

Read-only ffprobe audio-tag inspection confirmed11 audio streams in file order:
1 rus E-AC-3 5.1 `Дубляж (Bravo Records Georgia / Movie Dubbing)` (default flag1),
2 rus AC-3 5.1 `Дубляж (Red Head Sound)`,3 rus AC-3 stereo `Дубляж (Jaskier)`,
4 rus AAC-LC stereo `Дубляж (HDRezka Studio)`; remaining streams include Russian
MVO/AVO/VO, Ukrainian AC-3 and English E-AC-3 Atmos. User clarified TV shows9
Russian tracks plus1 Ukrainian and1 English, all numbered without codec titles.
Agent guided selection by matching file order, which is plausible but not verified
through TV instrumentation; actual selected codec remains inferred from numbering.
Initial audio selection before testing remains unknown.

User switched to fourth Russian track and confirmed no loading pauses during the
five-minute observation. Collector session53836 exited0;59 subsequent samples
18:48:24-18:53:14UTC had min3840MiB continuous ready data and no incomplete current
piece, with reader advancing2472->2602. No video/server setting changes or seeking
were requested. Then user switched to first Russian track as a controlled comparison
and reported a loading pause. Collector30741 running:33 received samples
18:53:44-18:56:24UTC, min3864MiB continuous ready data, no incomplete current piece.
The reported pause therefore occurred in an observation interval with ready torrent
data, unlike the earlier underfed HDR10 torrent.

Interpretation: same-file track-dependent behavior supports an audio/playback-path
hypothesis; it does not prove that E-AC-3 generally is unsupported, and different
scenes/bitrate plus unobserved TV codec selection remain confounders. A return to
fourth track for another observed interval is the next confirmation step; not yet
performed. Original70GiB-class remux startup failure has not been retested with AAC,
so must not attribute that separate error to audio on this evidence alone.
Session30741 remains bounded to about18:58:39UTC; earlier collectors have exited.
No runtime settings changed, no fix declared; central diagnostic task remains open.

## Fourth-first-fourth audio result

User returned to fourth Russian track and again reported no playback problems.
Repeat collector63494 started18:58:12UTC and exited0 after19:03:08UTC.
All59 subsequent samples were reviewed across two retrievals: min3856MiB
continuous ready data and no incomplete current pieces. Reader advanced through
the observation. The full five-minute repeat completed. Previous collector30741
also exited0; all task commands have exited, no background work remains.
No server settings changed.

Same-file observed sequence: fourth track no pauses in first five-minute interval;
first track user-reported loading pause with at least3864MiB ready; fourth track
again no problems in repeat interval with at least3856MiB ready. This strengthens
a track-dependent TV playback-path hypothesis, rather than source starvation for
the observed DV8 trial. Number mapping to file order implies AAC-LC stereo on
fourth and E-AC-3 5.1 on first; TV actual selected codec has not been instrumented.
Confounders remain different scenes/bitrate, track-specific encoding or timestamps,
and player state after switching. Do not claim universal E-AC-3 incompatibility,
confirmed decoder defect or root cause of the unretested DV7 remux startup error.

A second Russian track comparison (file-order AC-3 5.1) can distinguish broader
multichannel handling from the first E-AC-3 track path, while preserving video and
server settings. This is proposed only, not selected or launched. Existing central
playback diagnostic TODO remains open; no implementation decision made.

## Second AC-3 5.1 track also pauses

User selected second Russian track and reported a loading pause. File-order metadata
maps this to AC-3 5.1, while first is E-AC-3 5.1 and fourth is AAC stereo. Collector
27875 started19:04:22UTC;18 received subsequent samples19:04:27-19:05:52UTC had
min3864MiB continuously complete data and zero incomplete current pieces. Thus
sampled source availability remained healthy during this second-track interval.
Actual TV codec selection is still inferred from numbered order, not instrumented.

This contradicts an E-AC-3-only explanation. Both tested5.1 tracks paused, while
AAC stereo twice ran without user-reported pauses. AC-3/E-AC-3 processing versus
multichannel processing remain confounded. Next proposed comparison is third Russian
track, AC-3 stereo in file order, preserving codec family but reducing channel count.
Not yet selected. No general codec incompatibility or cause of the separate DV7
startup failure established. Collector27875 remains bounded to about19:09:17UTC;
all prior collectors exited. No server setting changes; central TODO remains open.

## AC-3 stereo comparison has no user-reported pauses

User selected third Russian track (AC-3 stereo by file-order mapping) and reported
no playback problems. Collector97458 started19:06:59UTC;42 subsequent samples
19:07:04-19:10:29UTC reviewed, min3848MiB continuously ready including current piece,
zero incomplete current pieces, reader2974->3071. Approximately3.5min observed
at this checkpoint; do not claim full five-minute completion yet. Collector remains
bounded to about19:11:54UTC. Previous collector27875 exited0; all older commands
finished. Server settings unchanged.

Current same-file comparisons: first E-AC-3 5.1 pauses; second AC-3 5.1 pauses;
third AC-3 stereo no pauses so far; fourth AAC stereo no pauses in two complete
five-minute runs. All identified comparison intervals had substantial contiguous
ready data. This strengthens association with the two tested5.1 tracks and weakens
an AC-3-family-wide explanation. It does not isolate a universal channel-count
limitation: specific track encoding, timestamps, scene bitrate, player state and
actual TV-selected stream remain potential confounders. Original DV7 remux immediate
NETWORK error remains separate and unresolved.

Next missing context: actual audio output route (TV speakers, HDMI ARC/eARC
soundbar/receiver, optical, Bluetooth) to distinguish TV decoding/downmix from an
external audio chain. No output-mode change or implementation authorized/performed.
Existing central diagnostic task remains open.

## TV speakers confirmed

User confirmed audio comes from the TV speakers, not an external soundbar/receiver,
optical or Bluetooth route. External audio equipment is outside the observed path.
This supports focusing on the TV/player audio handling and stereo conversion path,
but does not identify a decoder or downmix defect by itself. No TV sound settings
changed. Comparisons used different sequential scenes, so scene-dependent bitrate
and playback state remain confounders. Next stronger comparison should replay the
same short fragment with first/second5.1 and third stereo audio, rather than claim
channel count is conclusively causal. TV playback time is not available through
TorrServer; it requires user observation. Separate DV7 startup error still unresolved.

## Stereo AC-3 also paused; channel-count hypothesis withdrawn

User reported another loading episode, then clarified `Дорожка 3` and
`Не переключал`: they had remained on third track, rather than executing the
proposed switch to first. Thus this episode belongs to third Russian audio
(file-order AC-3 stereo), not first E-AC-3 5.1. Whether the proposed seek to1:55:20
was actually performed is unknown; do not label this a completed same-fragment test.
Agent had narrowed too early toward channel count and explicitly withdrew the
5.1-only hypothesis after the clarification. Earlier successful stereo intervals
are retained as observations, not proof that stereo AC-3 is always stable.

Sampler81518 received16 samples19:13:49-19:14:19UTC,
min3848MiB continuous ready data, no incomplete current pieces. The reported event
occurred during a well-buffered observation interval; exact screen timestamp unknown.
AAC stereo twice had no user-reported pauses in five-minute runs, while AC-3 stereo
and AC-3/E-AC-3 5.1 now all have reported pauses. This keeps codec/track/player-path
hypotheses open but does not establish an AC-3-family decoder defect or rule out
scene/player-state effects. No confirmed same-fragment A/B result exists yet.
Need clarify whether the seek was performed and whether loading followed it
immediately before assigning the latest event to normal steady-state playback.
No runtime changes; original DV7 startup error remains separate and unresolved.

## User stopped repetitive track switching; independent checks

User clarified no seek had occurred during the third-track loading event. This was
normal continued viewing, not seek buffering; proposed same-fragment A/B was not
executed. User then stated fatigue with repeated switching and requested other
checks. Stop this manual switching sequence; no further user track trials assumed.

Read-only checks: server enp1s0 1000Mb/s full duplex, RX errors/drops0, TX errors0
and cumulative TX drops4; TorrServer running, OOMfalse, restarts0. Cudy LAN2 only
active LAN carrier,1000F, CRC/link errors0, cumulative RX drops56; other LAN ports
no carrier. Those cumulative nonzero drops were not interval-correlated and are
not established as causal. Last physical TV link still unknown; Cudy may see a
shared downstream uplink. Target TV ARP reachable. Router bridge/od utilities
unavailable, so no final TV bridge-port association was established; nothing installed.

Actual deployed app.min.js read directly. Generic player uses HTML video element
outside explicit Tizen/Orsay paths. HTML video waiting event toggles loader; error
handler forwards video.error.code/message into displayed code/details. Thus generic
NETWORK text is browser-media error evidence, not an independently established
transport failure. Audio menu obtains native audioTracks for this direct-file path;
no explicit VIDAA/MSX-specific override found in the searched bundle. Read relevant
selection and loaded-data paths, found no demonstrated switching defect. TV runtime
selected/enabled streams remain uninstrumented; do not claim exact codec selection.

Official Russian Hisense55U7S PRO page lists HEVC/Dolby Vision/HDR support, but
this does not prove support of every file/profile in an embedded browser:
https://ru.hisense.com/catalog/tvs/55U7SPRO/ . No model-specific browser limitation
established. Old VIDAA guide alone is insufficient to diagnose this TV.

Prepared only locally /home/slnnk/ai-data/home-media-diagnostics/playback-diag.js;
node --check exit0. Ten-minute bounded browser diagnostic: every2s while playing,
and on waiting/playing/error/stalled/seeking/seeked/pause, collect currentTime,
paused/seeking, readyState/networkState, buffered ranges/ahead seconds, available
frame/drop counters, enabled audio-track indices, numeric media error code. Send
numeric/state JSON via same-origin HEAD /msx/start.json query to existing Apache
access log. No film URLs/titles, API keys or media content collected. Automatic
stop removes listeners and stops timer; diagnostic is not installed or browser-tested.

Concrete proposed installation, requiring explicit external-change approval: back up
current index outside document root, add temporary playback-diag.js to the active
Lampa release and one script reference in index.html; user reopens Lampa once to
capture the actual client buffer during normal viewing. No repository edits proposed.
Subsequent cleanup also needs the normal external-command approval. Distinguish
prepared local artifact from installed/working telemetry. All samplers including
81518 exited0; no task background commands remain. Original startup error and
repeated buffering remain open in the existing central diagnostic TODO.

## Temporary browser diagnostics installed with approval

User explicitly approved the previously described temporary installation. Read-only
preflight confirmed current index hash and no existing diagnostic file/reference.
One authorized SSH operation installed playback-diag.js in active Lampa release and
one deferred script tag in index.html; no service restart or repository change.
Backup outside web root: /opt/lampa/diag-backups/20261114T192419Z/index.html.
Original index SHA256 b3cee44fadb483eff0de104d3e2453bc2dfe25e83db65e30f45b565c6a0ef1eb;
installed index749f4fe670ab16c642fbd8a776fbc79e00b3c04d901f8ade2d61dbbaf17ef6c5;
script510e340ba6c918b5d8f0511f2ec503954989d086eeea61021fd18ca2f23ee933.

Verification: node --check passed; in-memory browser-stub checks passed for buffered
ahead calculation, selected audio indices, waiting/error events, automatic ten-minute
stop/listener cleanup and suppression of error text. Real LAN GET index/script200,
exact script hash matched; probe HEAD /msx/start.json200 was visible in Apache log.
This verifies delivery/log transport, not TV execution or an observed buffer event.
User must reopen Lampa once, then view normally; no more manual track switching.
Capture TV telemetry before diagnosing the exact player mechanism. No new external
service, media export or saved film content. This approval covers installation only;
cleanup is a later external action requiring the normal explicit approval.

After page load, browser collection stops automatically after ten minutes; installed
script/reference remain until cleanup. No task SSH sampler or local background process
remains. No browser session has yet been observed executing the script. The main
playback diagnosis stays open; central TODO updated to capture and cleanup status.

## TV telemetry captured actual non-seek waiting; thermal check

User reopened Lampa, selected first track and reported loading. Real telemetry
confirmed audioTracks enabled index0,3840x1606 video, increasing decoded frames.
At19:29:42UTC (browser elapsed253525ms), video currentTime7678.671s (2:07:58.671),
waiting occurred with pausedfalse,seekingfalse,readyState2,networkState2. CurrentTime
and decoded frames2965 froze; playing resumed at elapsed256210ms, a2685ms pause.
No media error or dropped-frame increments recorded around the event.
Synchronized TorrServer19:29:42UTC: current piece3468 complete,3048MiB continuous
ready including current piece, download310.17Mb/s; at19:29:44UTC still3176MiB ready.
This actual pause is not explained by missing torrent data at its current reader.

Important measurement limit: during successful playback, TV reports currentTime
around7600s while buffered ranges are around[70.9,71] or[152.9,153]. Computed
ahead_s0 is therefore not reliable evidence of an empty real browser buffer. Do not
infer zero buffered seconds from mismatched timelines. readyState transition is a
separate direct observation. Exact client receive/demux/decode cause still unknown.

User then observed CPU cooler stopping/restarting and finally stopped. Prioritized
read-only thermal checks without stress tests or fan configuration. CPU Intel Core
i3-10105; three readings19:31:36/41/46UTC package53/46/46C, cores41-53C, exported
max80C/crit100C, CPU busy1.9/0.8percent in two5s intervals. Core/package throttle
counters all0; no recent30min kernel thermal/throttling events. No RPM sensors
exported. No observed overheating/throttling explanation for playback, but fan
health or intentional zero-RPM policy is not verified by absent RPM telemetry.

Independent passive TCP capture92561 started19:32:30UTC for150s, numeric records
saved in ai-data/home-media-diagnostics/tcp-<UTC>.jsonl. Server cache collector74883
continues bounded until about19:35:40UTC. Browser telemetry runs until roughly
19:35:28UTC (ten minutes from page load), no track switching requested. Capture/log
read operations are read-only; no new runtime changes. Main task remains open,
including cleanup requiring a separate external-command approval.

## Second waiting event correlated with TCP receiver backpressure

Second spontaneous loading event observed by user and telemetry at19:34:42UTC,
currentTime7976.885s (2:12:56.885). waiting elapsed554157ms, pausedfalse,
seekingfalse,readyState2; playing elapsed557827ms:3670ms pause. Active audio index0.
TorrServer samples19:34:42/44/46UTC all current piece3598 complete with3888MiB
continuous ready data. TCP connection43102 at19:34:41-45UTC had sent/acked bytes
fixed1612294064, Send-Q/notsent3471008, while rwnd_limited increased each second.
Sending resumed19:34:46UTC;19:34:47 acked1623324112. This correlates the actual
TV waiting interval with receiver backpressure while data was ready, rather than
with source starvation. Missing snd_wnd field was not independently verified by
packet capture; use reported rwnd_limited and counters, not an invented window value.

Full150s TCP capture193230-193459UTC:150 records, average acknowledged27.65Mb/s,
no bytes_retrans increase observed. Pauses also occurred outside waiting events,
so backpressure alone is not a decoder-defect diagnosis. Captures saved in
ai-data/home-media-diagnostics/tcp-20261114T193229Z.jsonl and
ai-data/home-media-diagnostics/tv-events-20261114.jsonl (parsed numerical/state data,
no raw access log or film content). Counters in browser were not perfectly monotonic
(e.g. total frames10136 before waiting then10123 at waiting), so precise dropped-frame
or decoder-throughput conclusions are not justified from those counters alone.

Read-only packet probe attempted45s near2:12:35 but returned only about1.5s of media,
so it did not cover the waiting time and supplied no usable peak-bitrate result.
Repeat video-packet read2:12:50 for20s exited0 without warnings,480 packets spanning
7969.920-7989.898s, covering the waiting position. Thus another client could read that
part of the stream; no full decoder validation or measured bitrate ceiling claimed.
No film sample saved, no server or TV settings changed by these probes.

Confirmed localization for this DV8 event: receiver/media-consumption side at TV,
with sufficient ready data at server. Exact browser buffering, MKV demux/track
interleaving or decoder mechanism not isolated. Do not label AAC as a proven fix
or apply this finding automatically to the separate DV7 startup NETWORK error.
All cache/TCP/probe commands exited0. Browser diagnostic collection is configured
to stop after600000ms; the temporary installed file and index tag remain pending
explicitly approved cleanup. No more manual switching requested. Central task
updated to correlated evidence; original diagnosis remains open.

## First isolation test prepared; external installation pending

User said `Давай начнем` after the proposed plain-player then same-fragment container
comparison plan. Proceeded with local preparation/read-only preflight, not remote
installation. Scope: same37.39GB release, first audio track, simple HTML video page
without Lampa application code, served by existing local Apache inside current MSX
browser runtime. Initial position7940s (2:12:20), before captured waiting at2:12:56.885.
This isolates Lampa UI/application effects; it does not replace the VIDAA media engine.

Read deployed Lampa stream URL builder: /stream/<encoded basename>?link=<hash>&index=<id>&play
(after preload conversion). Plain page uses the same path pattern, active torrent
and numeric file index, selected dynamically in the installer without printing hash,
filename or stream URL. Lampa can drop the active torrent on close; upstream
MatriX.150 stream handler parses hash/magnet and adds absent runtime torrents.
No explicit drop/add/save API mutation performed. No source/key copied into Git.

Prepared local artifacts under ai-data/home-media-diagnostics:
plain-player.html.in and install_plain_test.py (read-only default, --apply required).
Page has one native video element, existing approved playback-diag.js, first audio
selection, one initial seek, native controls/OK playback and small status/error text.
No app.min.js or new service. Installer backs up current msx/start.json outside web
root, creates playback-test/index.html and replaces startup action to local test URL.
It aborts on startup hash drift, existing test directory, missing diagnostic script
or missing/ambiguous expected release; rollback of partial new files is included.

Validation: installer Python compile and JS syntax/behavior stub checks passed for
source assignment, first audio selection, one seek only, play/error behavior.
Remote read-only preflight passed: current startupSHA256
c731d84aa098cedb03a55c8a5d5cce2a8e154f0c9e3336ed5b4505028d059582;
expected release/file37390284387 bytes present; test directory absent; original
startup still points to Lampa. Proposed pageSHA256
f626c56cf291de8c1a4e0cf151e31048cb9902e499339479b50da32581c07c20.
Proposed startup action link:http://192.168.168.2:8080/playback-test/?v=f626c56cf291;
parameter remains current msx/start.json, version playback-test-f626c56cf291.
No actual runtime test, HTTP delivery check or TV success claimed yet. No repository
changes or running background commands. Obtain explicit approval for this concrete
remote installation before executing --apply, then verify HTTP and coordinate one
MSX reopen. Later restoration/cleanup remains separately approval-gated.

## Plain-player test installed after explicit approval

User explicitly approved the reviewed page installation and temporary MSX startup
redirect. Applied prepared install_plain_test.py --apply in one SSH command.
Created playback-test/index.html in active Lampa release and replaced msx/start.json.
Startup backup outside document root:
/opt/lampa/diag-backups/plain-test-20261114T195322Z/start.json.
Installed startupSHA25696a10f6af3e6b55a3186b43b3f97665f89fa5e40825c0cc16a1e17b56be7b0cd;
pageSHA256f626c56cf291de8c1a4e0cf151e31048cb9902e499339479b50da32581c07c20.
No service restart, repository change, transcoding or audio/server settings mutation.

HTTP verification: startup/page/diagnostic JS200 with allow-origin*, expected startup
action; page exactly matches rendered hash, one video, no Lampa app.min.js and no
unrendered placeholder. Existing playback-diag.js hash matched. Bounded1024-byte
read of configured same stream returned206, correct total37390284387, Matroska MIME,
CORS*. Start7940s. Delivery is verified; actual TV execution/playback still pending.

User instructions: fully close/reopen existing MSX once; same configured server
address, page should autoplay same release from2:12:20 with first audio index0.
If autoplay blocked, page supports OK/Play. No track switching requested. Native
media engine remains VIDAA; comparison isolates Lampa UI/application overhead.
Ten-minute read-only cache capture started with raw numeric JSONL saved under
ai-data/home-media-diagnostics/plain-test-cache-<UTC>.jsonl; browser collector also
bounded ten minutes from page load. Check active cache capture status before final
closeout. Existing runtime diagnostic and startup redirect must be restored/removed
only with a later explicit external-change approval. Main root cause remains open.

## Plain-player stall traced to incomplete urgent piece; disk-cache proposal

TV successfully opened plain page without app.min.js, active audio index0 confirmed.
At19:55:53UTC currentTime7998.323s (2:13:18.323), spontaneous waiting, readyState2,
not paused or seeking. It continued until19:57:00UTC; playing elapsed134238ms minus
waiting67583ms =66655ms stall. This time backend starvation was observed:
cache reader3603 incomplete from19:55:43 through19:56:59, continuous ready0;
nearby pieces3600-3602 and3604-3610 completed. At19:56:59 piece3603 Size8355840
of8388608, missing32768 bytes, Priority5. Total cache4240619107 of4294967296 bytes,
25 seeders, aggregate139.16Mb/s. TCP Send-Q0; old HTTP connection CLOSE-WAIT,
retry connection accepted but no sent-body bytes. At19:57:01 reader advanced3606
with1720MiB continuous ready; at19:57:03/07 progressed3609/3612 with TCP sending.
This supplies a concrete cause of this long plain-player event: missing current
piece data, not Lampa UI or an established codec error. It does not retroactively
explain prior short events with continuous ready data and receiver backpressure.
Why the last32KiB remained unavailable despite high priority/healthy aggregate
speed is not established: peer request completion and cache/scheduler behavior
remain candidates. Priority was nonzero, so do not claim a proven cleared-priority bug.

Runtime image ghcr.io/yourok/torrserver:MatriX.150,
sha256:2d02152b804946848f032dcca94fa0f096c8840cff3d37e1ba5400c30f70e16b,
OCI revision0c48c9ac78de2864f5fc9341e8caf89d355a4850, created2026-11-06.
Official source for this revision copied under ai-data/home-media-diagnostics/
torrserver-source/deployed-0c48c9ac78de. Cache/piece/mempiece match previously read
tag files; source includes priority watchdog and partial-RAM accounting safeguards.
Missing string markers in binary are not proof of missing code (packing/stripping
not investigated); use OCI revision, no claimed installed-source mismatch.
Upstream issue845 concerns older stream request race and was fixed before this
build; do not present its historical report as the confirmed current fault.

User proposed disk-backed storage instead of only RAM; discussion, not implementation.
Read-only preflight: current UseDiskfalse, CacheSize4294967296, TorrentsSavePathempty,
RemoveCacheOnDropfalse, ReaderReadAHead95, PreloadCache10, ConnectionsLimit25.
Host SSD Apacer AS350256, root233GiB with212GiB available; writable bind mount
/opt/torrserver/data -> /opt/ts. Source selects MemPiece OR DiskPiece via UseDisk;
this is not a combined two-level application cache or automatic full-film download.
Disk cache remains budgeted/evicted; incomplete current data is not magically filled
by choosing SSD. Source NewDiskPiece reconstructs completion from on-disk file size,
so persistence semantics are not equivalent to a verified whole-file archive.

Proposed controlled experiment: change only UseDisktrue and path /opt/ts/cache
(host /opt/torrserver/data/cache), preserve4GiB capacity,10percent preload and all
other settings; protected settings backup, read-preserve-write API and independent
verification required. Settings apply interrupts active torrent stream. No settings,
directory, container or repository changes performed for this proposal. Requires
explicit approval of the concrete remote change; do not treat the user's question
as approval. Temporary MSX plain-page redirect/diagnostic still need restoration/
cleanup after approval; original DV7 startup error still unresolved.

## Disk-cache trial declined; RAM retained

User clarified the disk-storage question was discussion only and explicitly rejected
switching to disk: `Нет, оставим RAM, это был просто вопрос, не вижу смысла в переключении на диск.`
Decision scope: this playback diagnosis and proposed SSD experiment only. Withdraw
that proposal; keep existing4GiB RAM cache,10percent preload and other current
settings. No disk cache directory, settings mutation or trial was performed. Earlier
proposal/preflight remain historical evidence, not pending permission or execution.
This does not cancel the broader playback diagnosis, authorize other changes or
resolve why urgent piece3603 lacked32KiB. Future work remains read-only investigation
of missing-block delivery/cache scheduling and separate short client-side pauses;
new runtime changes need their own explicit approval. Temporary plain-page/MSX
redirect and browser diagnostic remain installed; restoration/cleanup still require
approval. All task samplers/probes have exited; no background operations remain.

## Read-only request analysis and next container test preparation

User requested continued diagnosis, retaining RAM and declining SSD cache. Confirmed
ResponsiveModetrue, EnableDebugfalse, ConnectionsLimit25,4GiB RAM; Docker log empty.
Read exact OCI-revision go.mod: anacrolix/torrent v1.59.1 replaced with
https://github.com/tsynik/torrent/tree/v1.2.34 . Library source uses strategy3 with
1s duplicateRequestTimeout; high-priority piece3603 therefore cannot be explained
merely by an intentional one-minute duplicate-request delay. This is source-level
behavior, not proof of which peer/request stalled in the past.

Discovered native GET /stat via deployed server/web/pages/route.go; no debug toggle
needed. It exposes piece-state runs, reader ranges, peer queue counts, next pieces,
choke/interest flags and last-message/helpful ages. Raw output includes peer
identifiers, addresses and an announce key, so inspect only in memory and persist
whitelisted/pseudonymized fields. New local watch_block_requests.py collected300s
cache/stat snapshots, logging per-peer salted pseudonyms without addresses/IDs.
Capture: ai-data/home-media-diagnostics/block-requests-20261114T201138Z.jsonl.
Collector70988 exited0. No new incomplete-current-piece episode caught in that
interval. At20:10:24UTC tail piece4456 was partial/queued;20:15:27/32 it had completed
and peer queues were empty. Cannot retroactively assign the earlier delay to a peer.

User reported more short pauses on plain player. At20:18:07/10UTC current4164/4165
complete with2352/2344MiB continuous ready through the final piece; TCP had about
3.1-3.4MB queued, receiver limited, same64160 cumulative retransmitted bytes across
those two snapshots (not zero over connection lifetime). TV-side ten-minute
telemetry had expired, so these short episodes lack exact client-event correlation.
Native ports9222/9223/9226 closed; no debugger enabled or TV setting changed.
No new proof that all pauses share the missing-block cause. User may stop the
plain test; repeated track switching remains withdrawn.

User asked whether Docker was suspected. Clarified no positive Docker-specific
failure evidence, not completely excluded. Proposed matched MKV/MP4 clips will be
served by the same Apache container, preserving that aspect of the environment.
Compared outcomes can implicate format handling; do not claim the test generally
rules Docker out. User said `Продолжи`, authorizing continued preparation, not an
unreviewed remote mutation.

Prepared locally container-player.html and install_container_test.py under
ai-data/home-media-diagnostics. Plan: extract120s from2:12:20, copy HEVC/DV8 video
and first E-AC-3 5.1 without re-encoding into MKV; remux that clip into MP4; verify
both carry3840x1606,yuv420p10le,DV8,E-AC-3 5.1 and matching~120s duration before
publishing. Existing FFmpeg8.1.3 available in TorrServer container. Store temporary
clips under existing /opt/torrserver/data mount, serve copies from /container-test/,
automatically play MKV then MP4 on one page with phase markers; preserve4GiB RAM
cache. This is temporary test media, not enabling SSD cache. Proposed startup
redirect, clip creation and page installation still require explicit approval.

Local Python compile and JS syntax/behavior checks passed: one video element,
automatic MKV->MP4 sequence, first audio, phase markers and bounded two-clip end.
Initial local opening-tag regex assertion was replaced by an explicit opening-tag
count; no remote mutation was attempted. Source/codec-copy behavior and actual
playback remain unverified until clip creation. Remote read-only preflight failed
with SSH No route to host; no clips or new test page/startup changes installed.

## Server intentionally unavailable

Controller route to home-01 remains LAN192.168.168.2; ARP failed and one ping lost.
Cudy reachable; TV neighbor reachable, server neighbor stale. User explicitly
confirmed they switched off/disconnected the server. Do not classify this as a
new service/network fault, independently restart it, or infer relation to fan.
Continue remote preparation only after user restores power/network. Prepared local
artifacts retained. Previously approved plain-page redirect and diagnostic are still
on persistent files, with restoration/cleanup approval pending. All agent commands
and collectors exited; no task background processes remain. Main playback diagnosis
and original DV7 startup error remain unresolved in the existing central task.

## Server returned; container comparison preflight ready

User said server was starting. Read-only SSH succeeded20:35:41UTC, uptime under1min;
Lampa, Jackett, FlareSolverr and TorrServer containers all up31s. Read-only container
test preflight first stopped because expected active torrent was absent after restart.
No remote writes or torrent add occurred. Updated local install_container_test.py
with a strictly validated saved-source fallback: original plain-player page must
match previously verified SHA256f626c56cf291de8c1a4e0cf151e31048cb9902e499339479b50da32581c07c20;
extract its config stream and require expected local8090 origin, /stream/ path,
40hex infohash,index1,play flag. Do not print/store the actual URL in KB.

Python compile and actual remote read-only preflight passed. Startup hash still
matches expected plain-test redirect; container-test directory absent; disk space
sufficient. Source will reopen via the saved stream only during approved clip creation.
Prepared plan:120s starting2:12:20, same HEVC Main10/DV8 and first E-AC-3 5.1 via
codec copy, MKV then MP4 automatically; clips must pass metadata assertions before
publishing. RAM stays4GiB; no disk-cache experiment. Installer/HTML locally ready,
no clips/page/startup changes for this second test applied. Explicit approval needed
for creating temporary clips and redirecting MSX startup to /container-test/.
All readiness/preflight processes exited; no background commands remain. Earlier
server-unavailable checkpoint superseded by this user-restored availability.

## Matched MKV/MP4 clips created and comparison installed

User explicitly approved creating temporary clips and the MSX comparison redirect.
Ran prepared install_container_test.py --apply in one authorized SSH operation.
Source restored from verified saved plain-page URL after user reboot; no cache/settings
API mutation. FFmpeg8.1.3 stream-copied120s starting2:12:20, mapping original HEVC
video and first E-AC-3 5.1 audio into MKV, then remuxed that same clip into MP4.
No video/audio re-encoding. Both probes passed assertions: exactly two streams,
3840x1606,yuv420p10le,HEVC,DV8,E-AC-3 six channels. MKV122.997s/412444824 bytes;
MP4122.788s/412486240 bytes. Extra preroll is keyframe/timestamp alignment; clip
duration difference0.209s, within reviewed1s limit. Profiles preserved, not a full
bit-exact decoded-frame validation.

Scratch originals /opt/torrserver/data/container-test-20261114T203921Z; served copies
in active Lampa release /container-test/clip.mkv and clip.mp4 with index.html. Backup
of prior plain-test startup /opt/lampa/diag-backups/container-test-20261114T203921Z/start.json.
Current MSX action link:http://192.168.168.2:8080/container-test/?v=a1d448223736.
Original Lampa startup backup remains earlier plain-test-20261114T195322Z/start.json;
final restoration must choose intended original, not blindly restore latest backup.
PageSHA256a1d448223736912a8a43095049e4eaef497a0415b50f337b5c11172d8a7d07c2.

Verification: startup/page200, allow-origin*, correct action and page hash; one video
and no app.min.js. Both media Range0-1023 returned206 with exact totals, bytes
Accept-Ranges, MKV video/x-matroska and MP4 video/mp4. Cache readback confirmed
UseDiskfalse,CacheSize4294967296,PreloadCache10,ReaderReadAHead95. No service restart,
Docker network/image change or repository edits. Temporary files are test media,
not a disk-cache experiment. Both formats served by same Apache container; source
is now a ready static clip, so P2P is removed during playback. Comparison with the
full original also changes stream count/packaging/start timeline, so two smooth
clips alone cannot prove a sole full-file container defect.

Prepared page auto-plays MKV then MP4 using same video element and first audio,
sends phase0/1 markers to existing local diagnostic log; total about four minutes.
User needs one MSX reopen, no track switching. Actual TV comparison execution still
pending. Existing browser collector runs10min after page load. Passive Apache-namespace
TCP capture started for420s, stored as ai-data/home-media-diagnostics/container-test-tcp-<UTC>.jsonl.
All installation/verification commands exited; only bounded TCP collector running.
Main diagnosis, separate DV7 startup failure and future cleanup/restoration remain open.

## Both static clips played normally; from-start control prepared

User confirmed video/audio normal through both automatic clips. Browser log verified
MKV phase0 at20:42:20UTC, first playing20:42:21;62 active samples through122.398s.
MP4 phase1 at20:44:25UTC, first playing20:44:27;63 active samples through122.824s.
Neither phase had non-seek waiting after first playing or a media error. Enabled audio
index0 both. Positive calculated buffer ahead approximately1.6-13.6s MKV and1.2-13.2s
MP4 (near end naturally diminishes). Some adjacent buffered-range starts were a few
milliseconds ahead of currentTime; isolated computed0 values are not starvation proof.
Frame counters reported0 even during observed playback; do not infer decoder FPS from
these unsupported/inconsistent counters. Parsed events saved locally in
ai-data/home-media-diagnostics/container-test-events-20261114.jsonl.

Apache TCP capture96912 exited0 after420s, file
ai-data/home-media-diagnostics/container-test-tcp-20261114T204158Z.jsonl. Media connections
sent about412MB each with no reported retransmitted bytes. Both static formats can
play this HEVC Main10/DV8/E-AC-3 5.1 fragment on this TV. This contradicts a universal
format/5.1 incompatibility, but does not prove all long streams are supported or
exclude every Docker/network issue. Relative to original, clips also have two tracks,
rebased timestamps, smaller files and Apache delivery instead of live torrent stream.
No sole cause established by two successful clips.

Next prepared control: same full37.39GB source and first audio, plain page from0,
no automatic currentTime assignment/seek. Original large-stream tests resumed or
sought to a nonzero position and showed mismatched currentTime/buffered timelines;
static from-zero clips had coherent timelines. This motivates testing resume/seek
path; it is a hypothesis, not a demonstrated VIDAA seek defect.
Prepared ai-data/home-media-diagnostics/install_from_start_test.py; default read-only,
--apply gated. New page /playback-from-start/index.html, temporary MSX action redirect;
backup before replacement. Source read from exact hash-verified original plain page,
all tracks retained in full source, no remux/settings/cache changes. Startup expected
SHA25619475a8fcf04815a3c21438a66ba05deae0bdec9912641217ce4554cd9af5b44;
new rendered pageSHA256b7d774fb70752cb7badbad7f57efbeacf2a5053eaf5248707b9412ba07312f25.
Python compile, JS behavior check proving zero currentTime setter calls and actual
remote read-only preflight passed. No next-test page/startup modification applied;
requires explicit approval. All server samplers/commands exited; browser diagnostic
has bounded10min lifetime after page load. Temporary test files/redirects remain
pending approved cleanup. Central diagnostic task remains open, including DV7 error.

## Original full-file from-start control installed with approval

User explicitly approved the reviewed from-zero/no-seek page and startup redirect.
Applied install_from_start_test.py --apply. New /playback-from-start/index.html uses
same full37.39GB TorrServer URL, all original tracks, selects first audio and makes
no currentTime assignment at start0. No remux, Docker image/network or settings
changes. Backup of container-comparison startup:
/opt/lampa/diag-backups/from-start-20261114T205251Z/start.json.
Current action link:http://192.168.168.2:8080/playback-from-start/?v=b7d774fb7075.

Verified startup/page200, CORS*, expected SHA256
b7d774fb70752cb7badbad7f57efbeacf2a5053eaf5248707b9412ba07312f25, config.start0,
positive-start guard before seek, no Lampa bundle. Cache readback4GiB RAM,
UseDiskfalse,PreloadCache10. Actual TV startup/absence of seeking still requires
browser events after user reopens MSX. Observe about five minutes without controls;
initial loading is separate from post-playing stalls. Read-only cache/stat and
TorrServer-namespace TCP captures started for420s, numerical/pseudonymized files
under ai-data/home-media-diagnostics/from-start-cache-<UTC>.jsonl and
from-start-tcp-<UTC>.jsonl. Browser diagnostic bounded10min after page load.
Only bounded capture runner remains; install/HTTP/setting checks exited0.
Main diagnosis and separate DV7 startup error unresolved; temporary pages/media,
startup redirect and original diagnostic still require approved cleanup/restoration.

## Full original from zero stable for 9m42s; one-seek control prepared

User reported no problems. Browser trace confirmed first playing20:56:01UTC at0.152s,
first audio index0; no seeking/seeked, no post-start waiting, no errors through last
sample21:05:43UTC, currentTime582.038s (9m42s). Page elapsed598000ms; subsequent
collector expiry is expected. Original full37.39GB file, all original tracks and
TorrServer HTTP delivery retained; no remux. This weakens a universal original-file,
Docker or5.1 incompatibility explanation. It supports investigating nonzero-start/
seek behavior, but starting scene/bitrate differs, so a seek defect remains unproven.
Parsed browser records saved from-start-events-20261114.jsonl (301 events).

Combined cache/stat/TCP collector45300 exited0, both420s captures saved under
from-start-cache/tcp-20261114T205451Z.jsonl. Ten incomplete-current samples over the
whole capture must not be called playback stalls; these include initial loading and
need time alignment. Later reader150/151 had about3888/3880MiB ready. Actual browser
record supplied the absence of post-start stalls, not a green unrelated metric.
All agent commands/captures finished; installed browser script reached its bounded
10min window. Temporary runtime files/redirects remain pending approved cleanup.

Prepared next narrow control locally: install_seek_control.py and seek-control.html.in.
Same full original source/first audio: start0 without initial seek, after60s of real
playing seek back30s exactly once, then pause with completion message at180s.
Purpose: compare a brief nearby backward seek with no-seek playback while reducing
scene differences and avoiding user manual controls. Source ready-data must still be
observed around the seek before interpreting a stall. Not a proven fix or a guarantee
that nearby seeking reproduces far-seek behavior.

Python compile, JS behavior checks (no initial currentTime write, one60s timer,
exact30s backward jump, no repeated seek on playing,180s stop) and actual remote
read-only preflight passed. New pageSHA256
679c4d4a5e1ebfa27bd82605c296be83ae9ebee4ed94d10a99029f9df25925c4;
proposed MSX action /playback-seek-control/?v=679c4d4a5e1e. Page and redirect are
not installed; explicit approval required. Existing /playback-from-start remains
current MSX action. Main diagnostic TODO and separate DV7 startup error remain open.
