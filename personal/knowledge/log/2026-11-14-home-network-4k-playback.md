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

## Backward and forward sequence installed; TV test deferred by user

User explicitly requested installing the short one-backward-seek test but said TV
testing would be later. That version was installed with backup
/opt/lampa/diag-backups/seek-control-20261114T211147Z/start.json, delivered hash679c4d4a5e1ebfa27bd82605c296be83ae9ebee4ed94d10a99029f9df25925c4.
No TV launch or background capture started. User then discussed forward versus
backward behavior; discussion alone did not authorize an intermediate forward-only
change. Finally user explicitly requested combined sequence:1min watch,back30s,
3min watch,forward30min,5min watch. This supersedes short one-backward version.

Implemented locally seek-sequence.js,seek-sequence.html.in,seek-sequence-diag.js and
install_seek_sequence.py. Playback stage durations use actual advancing media time,
excluding paused/seeking/waiting/insufficient-ready periods; seek jumps do not count
as viewing. From near60s seek to30s, then after180s more seek from about210s to2010s,
then300s viewing, automatic pause/completion around38:30 media time. About540s of
actual watching plus initial loading/rebuffers. Hard20min wall-time timeout. Separate
copied observer at /playback-seek-control/diag.js has20min bound; shared original
playback-diag.js unchanged. Stage markers include stage,played time,from/target
numbers in same local access log; no URLs,keys or media content in telemetry.

Meaningful local JS checks passed: zero initial seek, exactly-30 then+1800s, stage
thresholds60/180/300, paused/waiting time excluded, correct automatic completion;
observer remains active after10min and stops after20min. Python compile and remote
read-only preflight passed. Executed one user-requested update with baseline hash
checks and backups: /opt/lampa/diag-backups/seek-sequence-20261114T212052Z contains
old index.html and startup JSON. Updated existing test index, new private diag.js,
and MSX version/action. PageSHA256
920aef537c26449d7911ef270c9eefa9c607c361a86a07056f77cc7de6dd450d;
private observerSHA25647d2c186a58b66fc7831d86b4395fea56320301f084f1e3232d7184dca757b50.
Current action link:http://192.168.168.2:8080/playback-seek-control/?v=920aef537c26.

Post-install HTTP startup/page/private observer200,CORS*,exact hashes and schedule
verified. RAM readback4294967296 bytes,UseDiskfalse,PreloadCache10,ReaderReadAHead95.
No service/container/image/network changes, no clip encoding or cache-mode changes.
Actual TV sequence not run or claimed working: user will test later. No scheduled
job, automation or background sampler left. Before user later starts, launch bounded
cache/stat/TCP observation; browser observer begins only when page opens. Current MSX
redirect and all temporary pages/media/scripts still await approved restoration/
cleanup after diagnostic work. Original Lampa startup backup remains
/opt/lampa/diag-backups/plain-test-20261114T195322Z/start.json. Parent diagnosis and
separate DV7 startup error remain unresolved; only requested test setup completed.

## Seek sequence observation started 2026-11-15

User is ready to launch the TV and asked whether attendance is needed. Live HTTP200 and exact installed page/observer hashes verified; MSX still selects the approved combined sequence. Read-only SSH collection started10:01:47UTC for1500s (expected end10:26:47UTC), local exec session5560. Local runner ai-data/home-media-diagnostics/run_seek_observation.py reads cache/stat, TorrServer TCP and Lampa diagnostic events; files seek-cache/tcp/events-20261115T100147Z.jsonl. Initial cache/TCP samples present without stderr; HEAD observer_probe round trip confirmed in parsed local events. No remote files/settings changed. Actual TV test events not yet observed at this checkpoint. User may leave after playback starts; telemetry detects waits/errors/progress, but cannot certify subjective picture/audio quality. Keep TV/MSX/server/collecting PC running. Browser/test hard limit20min; capture25min. Parent diagnosis remains open. Check local capture files and exec session5560; stop runner with Ctrl-C via that session if requested.

## Combined seek sequence completed with three post-seek stalls

2026-11-15: user reported picture/audio running at launch, then TV displayed completion.
Parsed local browser trace confirms test_done reason completed at10:12:30UTC,
media2310.533169s; all three actual-watch stages60/180/300s completed.
First playing10:03:19UTC; first minute had no post-start waiting.
Backward seek60.178271 ->30.178271 took about0.438s until playing;
forward seek210.422244 ->2010.422244 took about0.309s. These expected seek waits
are separate from three later non-seek waits (browser elapsed times):

- At media91.224558s,10:05:22UTC:3.634s waiting. Current server piece complete,
  approximately3184MiB contiguous ready; about3.97MB unsent TCP queue,
  acknowledged bytes stopped over two consecutive samples and rwnd_limited increased.
- At media137.429s,10:06:12UTC:2.733s waiting. Current piece complete,
  3888MiB contiguous ready; about4.15MB unsent queue, flat acknowledged bytes
  and increasing receiver-window limited time, resuming before playing returned.
  Retransmissions occurred elsewhere in capture; do not claim no packet loss globally.
- At media2096.761s (34m56.761s),10:08:55UTC:0.918s waiting. Current piece complete,
  about2552MiB contiguous ready. Adjacent TCP samples show queued bytes and resumed
  transfer; do not claim a whole-stall zero-window proof from one-second sampling.

No media error/stalled event recorded. Buffered reports22/24s ahead during first
two waits do not prove every audio/video track was ready. After far seek, currentTime
was about2010s while buffered ranges remained near~250s and subsequently progressed
on the prior timeline; ahead_s0 cannot be interpreted as an empty actual buffer.
The timeline mismatch is reproducible evidence, not a demonstrated root cause.

Result: scripted completion is not a clean playback pass. These three waits were
not caused by unavailable current torrent pieces in sampled server cache. Two align
with TV receiver backpressure. Prior from-zero/no-seek9m42s control was smooth;
seek-related player/demux behavior is strengthened as a hypothesis, still not causal
proof without a repeatable matched control. Distinct earlier incomplete-piece and
DV7 startup events remain separate unresolved cases. No settings/files changed on
server. Temporary redirect/pages remain pending approved restoration/cleanup.

Raw numerical evidence: ai-data/home-media-diagnostics/seek-events/cache/tcp-20261115T100147Z.jsonl.
Local collection session5560 remains bounded to10:26:47UTC (13:26:47 Moscow),
with browser observer ending20min after page load (~10:23:02UTC). Check/stop via
local session5560; no unattended scheduler installed. Parent diagnostic remains open.

## Full unchanged MKV HTTP control prepared; installation awaiting approval

User requested preparation of the proposed full-file HTTP test. Prepared local
ai-data/home-media-diagnostics/prepare_full_http_test.py, generated
install_full_http_test.py, and run_full_http_observation.py. No remote writes made.
Read-only sudo SSH preflight verified current startup/source test hashes, destination
absence and209.5GiB free on the Lampa release filesystem. Expected source37390284387
bytes (~34.82GiB); require6GiB additional free reserve.

Proposed single reviewed installer operation: create
/opt/lampa/releases/lampa-5d135cd2ed2d0ed4650e0b185fc2107d47c9c6bc/playback-http-control,
copy full original TorrServer response byte-for-byte to source.mkv.part, with45s
socket timeout and90min overall download bound; verify status200/Content-Length
and exact byte count, stream SHA256, fsync and rename to source.mkv. No ffmpeg,
remux, track removal, codec/settings/cache/network/container change. Partial failures
retain temporary evidence; old MSX redirect remains until all preparatory checks pass.
Validate Apache206/Content-Range/CORS and exact local bytes at start/middle/end.
Install same seek-sequence page and same20min diagnostic script, first audio,
60s watch ->back30s ->180s watch ->forward1800s ->300s watch. Only media URL and
diagnostic script path differ from last test. Save startup backup/source manifest
under /opt/lampa/diag-backups/full-http-<UTC>, then atomic temporary MSX redirect.

Expected delivered pageSHA256d8c3d949bd476a4b131578f79e21cb2161e4159e266052b4a13031ffa6e2c284;
observerSHA25647d2c186a58b66fc7831d86b4395fea56320301f084f1e3232d7184dca757b50.
Action /playback-http-control/?v=d8c3d949bd47. Local compile/guard/order checks
passed; template equality preserves already tested seek logic. Read-only remote
preflight passed. Actual download, static media Range delivery and TV behavior
remain unverified until approved execution. Observer prepared for25min Apache TCP
and browser events, not launched. Current old seek capture session5560 still active
at this checkpoint, bounded to10:26:47UTC; no new background operation.

Before running installer --apply obtain explicit approval for these remote writes
under user AGENTS External changes. This diagnostic static copy is not the declined
TorrServer disk-cache experiment. Interpretation: successful HTTP control would
implicate differences in the TorrServer/live source path, not prove one exact bug;
repeated waiting would narrow toward the shared media/player/network path, not
prove a decoder defect alone. Parent diagnosis and cleanup remain open.

## Full HTTP installation approved and copying

User explicitly approved the reviewed single installer operation. Started
install_full_http_test.py --apply on home-01 over sudo SSH, local exec session99654,
2026-11-15 around10:22UTC. Preflight passed209.5GiB free, exact source/startup hashes;
first copy progress0.45GiB/1.3 percent confirmed. Source37390284387bytes, same raw MKV,
20min seek scenario and paths as reviewed. Do not run --apply again while session
active; target now exists and partial file is expected. Check output through
session99654; stopping the SSH process may not prove remote termination, inspect
before cleanup/retry. No MSX redirect until full copy and checks finish. Existing
old observer5560 remains bounded until10:26:47UTC; HTTP observer not yet launched.

## Full copy timed out; verified resumable retry awaits approval

Approved installer session99654 exited1 with TimeoutError during response.read:
source sent691011584bytes (~659MiB), then no next block within45s. Partial remains
at playback-http-control/source.mkv.part. Read-only inspection verified startup
SHA25633ad279999e826318f080b5845f53c0be58739506dab41b12de9e65c10ce1e6c
unchanged; no HTTP page/observer or new redirect installed. Directory contains only
source.mkv.part. SHA25665d70cd16c8633902943c67f20c5345445bc4b4f52798eb12274b9bc5f784a56.
Later read-only torrents list empty; do not infer the cause of this transfer timeout
from that later state. Initial partial-copy response had expected200 and exact
Content-Length; download is incomplete, no full-source test is ready.

Prepared local prepare_full_http_resume.py ->resume_full_http_test.py. Guard exact
inspected partial size/checksum; same page/hash/target and same final HTTP checks.
One proposed retry command resumes with HTTP Range from saved offset,180s socket
timeout, at most10 connections/retries and90min overall download bound. Preserve
partial and old startup on failure. No source re-encoding/settings/cache change.
Default read-only remote preflight passed208.9GiB free, exact prefix and startup.
Local compile/guard/bound checks passed. Re-execution is a new external-write
command and requires explicit approval under user AGENTS; not run automatically.

Old observation session5560 has now finished: cache/TCP exited0, bounded logs
exited124 as expected from timeout1500. Preflight22012/32908 exited0. Installer
99654 exited1; all task commands ended, no task background collector or download
remains. Browser observer's20min window has also elapsed. Parent diagnosis and
full-file HTTP preparation remain open; source copy and pending retry are evidence.

## Resumable full copy approved and running

User explicitly approved the reviewed resumable command. Started
resume_full_http_test.py --apply, exec session53254,2026-11-15~10:47UTC. Exact prefix
checksum/startup checks passed; resumed connection1 progressed beyond prior offset,
2.71GiB/7.8percent by10:48UTC. Same agreed paths/source/page and final redirect;
180s socket timeout,10 connections,90min bound, no settings changes. Do not rerun
while active. Read-only source-hash-matched cache sampler32316 started for600s,
local full-copy-cache-20261115T1047.jsonl; no remote files written by sampler.
Snapshot10:48:15UTC showed485.9Mb/s download and urgent piece447 missing64KiB;
this is a live transfer sample, not proof of a playback stall. Current startup
remains old seek control until all full-file verification completes.

## Full unchanged MKV HTTP control installed and verified

Approved resumable installer session53254 exited0. Resumed from the inspected
691011584byte prefix, completed on connection1 without a new timeout/reconnect.
Installed2026-11-15T10:56:04UTC. Source copied byte-for-byte,37390284387bytes,
SHA256be7ed164f446f498685c29325ee1f53469a4815d7faaf3aa683af97cac60032f.
No remux, encoding, track removal, TorrServer settings, service/network/container
change. Media now served by Apache from playback-http-control/source.mkv,
independent of live torrent delivery during the TV control.

Installer validated exact source count/full-stream SHA, static206 Content-Range,
CORS* and byte identity at first/middle/last4KiB, then page/observer delivery hashes,
then backed up prior MSX startup and atomically redirected. Backup and source
manifest: /opt/lampa/diag-backups/full-http-20261115T105604Z.
Current action http://192.168.168.2:8080/playback-http-control/?v=d8c3d949bd47.
StartupSHA25656e648530807bde89f1dfdfda48918c535f45422f1116b2638f7b5dabb6b3323.
Same seek script60/180/300s actual viewing,back30s,forward1800s,first audio,
20min test/observer bounds. Source URL and observer path are the controlled changes.

Independent verify_full_http_test.py read-only SSH exited0: current action correct,
HTTP200 page and observer exact hashes, media HEAD200 exact37390284387 length,
video/x-matroska, Accept-Ranges bytes; GET bytes0-15 returned206 and EBML header.
Probe full_http_observer_probe observed in local parsed event log. These checks
verify delivery/preparation, not TV playback or elimination of stalls.

Started run_full_http_observation.py session52696 at11:03:09UTC for1500s;
local full-http-tcp/events-20261115T110309Z.jsonl. Initial TCP samples and probe
present, stderr0. Reads Apache namespace TCP and browser events, local writes only.
Expected capture end11:28:09UTC (14:28:09 Moscow); browser observer/test starts on
TV page load and bounds itself20min. To check/stop current local observer use
exec session52696; if session control unavailable inspect the local process
run_full_http_observation.py before acting. Do not claim background termination
without checking it. Old full-copy cache sampler32316 exited0; installer53254,
independent verification and all older observers finished. No download running.

Prepared test is ready: user should close/reopen MSX, start with OK/Play if needed,
leave TV/MSX/PC on and allow the sequence to finish. Actual TV launch/results not
observed yet. Current full HTTP action and source supersede prior seek-test redirect,
not historical evidence. Parent playback diagnosis, separate DV7 startup error and
later approved cleanup/restoration remain open; source static copy uses~34.82GiB.

## Full HTTP sequence also reproduces fixed-position waits

User confirmed picture/audio at launch and later reported completion. Full static
HTTP browser trace has300 records, first playing11:05:23UTC, test_done completed
11:14:32UTC at media2310.697023s. All actual-watch stages60/180/300s completed.
First minute had no post-start waits; expected seek waits about0.422s backward
and0.274s forward, excluded from non-seek stalls. No media error/stalled event.

Four later non-seek waits measured from browser elapsed_ms (network log receipt
delay differs, so do not use receipt-time differences for exact duration):

| Media position | TorrServer control | Static full HTTP control |
| --- | --- | --- |
| ~91s |91.224558s /3.634s wait |91.466s /2.899s wait |
| ~137s |137.429s /2.733s wait |137.429s /0.642s wait |
| ~2093s |none recorded |2093.049s /1.201s wait |
| ~2097s |2096.761s /0.918s wait |2096.844s /1.553s wait |

These waits occur with a complete local unchanged source through Apache, no live
TorrServer source dependency. Thus insufficient torrent/cache data or TorrServer
HTTP implementation is not necessary for these fixed-position waits. This does
not resolve the distinct earlier urgent-piece66.655s stall or DV7 startup error.
Shared TV/player/MKV/HTTP/LAN path remains; no exact decoder, subtitle or firmware
root cause proven. CurrentTime/buffered mismatch also recurs after far seek with
static source (currentTime~2090s,buffered~330s); ahead_s0 is not empty-buffer proof.
Apache TCP samples show queued media bytes and increasing rwnd_limited during
first two waits, with flat acknowledged counters then recovery. This supports TV
receiver backpressure, not a claim of source starvation or universal network health.

Read-only docker exec ffprobe over static HTTP read intervals88%+10,134%+10,
2090%+12, exited0; saved technical-only stream/packet fields to local
ai-data/home-media-diagnostics/full-http-packets-stall-windows.json (12309 packets).
Removed unnecessary title/language/tag metadata from the local artifact.
Full source has mainHEVC DV8 video,11 audio tracks,19 SubRip tracks and one attached
MJPEG cover (32 streams total). Selected stream1 is E-AC-3 5.1. Within sampled
windows, primary-video DTS increments41/42ms, selected-audio DTS exactly32ms;
no detected decode-timestamp gap in those windows. This does not establish all
codec payloads or whole-file timestamps are defect-free. Subtitle packet times
near stalls are observations, not proven causation.

Next proposed matched control: use the already saved full original to remux a
full-length MKV containing only main video and first audio, both stream-copy,
then same HTTP/seek sequence. Preserve codecs/DV8/audio and full length; remove
extra audio/subtitle/cover streams and rebuild container. This is a proposal,
not authorized remote creation/redirect; prepare reviewable command before any
external-write approval. Success would implicate packaging/stream-set differences,
not identify one exact faulty track by itself. No remux or remote changes performed
in this result turn. Avoid repetitive manual track switching or cache changes.

Collector52696 still active at checkpoint, bounded until11:28:09UTC/14:28Moscow;
TCP/event numeric files remain full-http-*-20261115T110309Z.jsonl. All metadata
commands completed; no download/transcode running. Check/stop collector via local
session52696; browser observer expires~11:25:19UTC. Temporary current HTTP redirect,
34.82GiB source and diagnostic files await later approved cleanup. Parent diagnosis
and separate DV7 startup issue remain open.

## Codec and browser replacement options researched

User asked whether codecs can be installed or the browser replaced on this TV.
Discussion only; no TV changes, firmware update, app installation or DLNA service
authorized. Official Hisense55U7S PRO product page lists HEVC/Dolby Vision support:
https://ru.hisense.com/catalog/tvs/55U7SPRO/ . Current successful HEVC/E-AC-3 playback
also makes a simple missing-codec explanation weak; no exact decoder defect proven.

Official VIDAA support documents firmware updates through System Settings > Support
> System Upgrade > Check Firmware Upgrade: https://www.vidaa.com/support/ .
No confirmed user-installable codec pack or independent Chrome/Firefox engine
replacement found for this exact model. Absence of a documented route is not proof
that every unofficial native modification is impossible. Official VIDAA partner FAQ
says platform supports native Linux and HTML5 apps; avoid claiming all VIDAA apps
are web-only: https://www.vidaa.com/is-ortaklari/ . Older WebApp development guide
explains platform browser engines but is not model-specific U9.5 evidence:
https://www.vidaa.com/wp-content/uploads/2020/12/WebApp_Development_Guide_for_VIDAA.pdf .

Official Hisense regional VIDAA U9 manual (generic, not the exact55U7S PRO manual)
describes App Store installation, warns downloaded APK files may not install, and
supports media/content sharing. Therefore Android APK installation is not a confirmed
supported route for this model. Do not assert a particular unsupported browser engine
version from third-party SEO pages or the old developer guide.
Manual: https://www.hisense.com.my/wp-content/uploads/2025/08/93041_9603VIDAA_U9_EUEMCO_E-Manual_eng_202502%E5%AE%8C%E6%95%B4%E6%9F%A5%E7%9C%8B%E7%89%88.pdf .

Candidate diagnostic alternative discussed: play same saved full source using TV's
built-in media player via USB or a local DLNA server, to compare a path outside
MSX browser playback. This is a proposal, not a confirmed fix or DLNA installation
approval. Previously proposed full two-track stream-copy MKV test remains unexecuted;
no user cancellation/supersession inferred. Check existing diagnostic TODO before
selecting or implementing next control.

## Single-file DLNA control prepared; server launch awaiting approval

User has no USB drive and asked how to use DLNA. Read-only home-01 checks:
no minidlnad/installed minidlna found, no listeners1900/udp or8200/tcp;
enp1s0 UP192.168.168.2, source.mkv exact37390284387bytes; only existing media images.
No DLNA server has been started. Docker image documentation verified at
https://hub.docker.com/r/vladgh/minidlna/ : host networking for SSDP discovery,
MINIDLNA_ configuration, V,/media scan filtering and notify interval30.
Source: https://github.com/vladgh/docker_base_images/tree/main/minidlna .

Prepared local start_dlna_test.py, default read-only preflight passed remotely.
Proposed single docker run: image vladgh/minidlna:latest (pull if absent), ephemeral
container tv-dlna-test, --rm, --restart=no, --network=host; bind only existing
source.mkv ->/media/test.mkv read-only, media_dirV,/media, friendly name
Home TV Test, network_interfaceenp1s0, port8200, SSDP1900/udp, notify30s,inotifyno.
No film copy/transcode, MSX redirect, router/firewall or existing service change.
Default preflight checks complete source and absence of container name; --apply
is gated by explicit per-command external-change approval. After launch, planned
read-only checks: descriptionXML friendlyName, running state, readonly single
media mount, host network, restartno. Does not prove TV discovery/playback.
Shutdown command after separate approval: sudo docker stop tv-dlna-test; --rm
removes ephemeral container/anonymous volumes, downloaded image remains.

TV instructions from official generic VIDAA U9 manual, not exact model UI labels:
Settings > Connection > Multimedia Device Connection > Content Sharing ON,
then Media > Content Sharing(device name), select Home TV Test and movie.
Some VIDAA versions put sharing under System > Application Settings per official
https://www.vidaa.com/customer_support/what-should-i-do-if-the-vidaa-app-media-function-isnt-working/ .
No TV setting has been changed by agent. Native media player has no installed
browser observer or automatic seek scenario: server can observe transfers, but
cannot claim browser waiting telemetry/automatic native controls. User should
observe a short playback/seek comparison; no repeated track switching proposed.

Full HTTP observer52696 now finished (TCP0,bounded logs124), browser expired.
All task commands complete, no download/capture/server-launch running. Current
MSX HTTP control remains installed. Parent diagnosis, optional two-track remux
and approved cleanup remain open. USB unavailable is a task constraint, not a
universal preference or a cancellation of other previously proposed controls.

## Native DLNA playback accepted smooth including seeking

User approved the reviewed single DLNA launch operation. start_dlna_test.py --apply
session25717 exited0; container tv-dlna-test running, ID3843744b18e37ca3cecaed1a9e796c107745e20fc934de4023e4bd992fbabe79.
Pulled image vladgh/minidlna:latest digest
sha256:cdfa0ed2bc9482b350c387d793ec6e2d41749cdafd9b69a4fe3579c0995469ef.
Verified HTTP200 rootDesc.xml friendlyName Home TV Test, readonly bind of sole
source.mkv into /media/test.mkv, host network and restartno. Source unchanged.
SSDP1900/udp and media8200/tcp configured on enp1s0. No existing service/MSX
redirect/configuration/router change. --rm container; image remains after stopping.

User already found DLNA server and started native TV picture/audio. Catalog
verification initially counted two resources; read-only follow-up proved one
37390284387byte video resource /MediaItems/24.mkv and its embedded JPEG artwork
/AlbumArt/1-24.jpg, exposed through several virtual folder references to same item.
This is one film, not two movies or another host directory exposure. Range0-15
returned206, correct Content-Range total and MKV EBML header. All catalog/probe
commands finished; no fix/config change was needed for the verification assertion.

User later explicitly reported extended viewing without problems, then clarified
that this includes seeking. Treat as user-observed native-player success, not
instrumented proof of exact matching seek positions/duration/audio-track index.
No native browser waiting/error telemetry exists. TCP independently confirms
active media delivery; it cannot certify smooth picture/audio. The earlier raw
HTTP/MSX full-file test reproduced waits near same media positions as TorrServer.
This strongly shifts diagnosis to browser-based MSX/HTML5 playback versus native
DLNA playback. Native path also changes HTTP server/headers/control behavior;
do not claim the exact Chromium/demux/decoder bug is proven, all LAN issues are
universally excluded, or a new codec installation is required.

Practical currently accepted playback path: existing saved full source ->MiniDLNA
->native TV player, including manual seeking. Current MiniDLNA shares this one
saved file; it is not an implemented Lampa/TorrServer-to-native-player integration
and does not automatically publish arbitrary torrents. Do not replace that scope
with a promised working live-torrent workflow. Native smoothness does not close
the separate DV7 startup error or prior urgent-piece download issue. No next remux,
firmware/browser change or permanent DLNA deployment authorized by this report.
Keep currently working container active for viewing until user requests otherwise;
later stop/removal remains subject to external-change approval.

Read-only native host TCP sampler95644 active for600s from12:06:37UTC, expected
end12:16:37UTC/15:16:37Moscow; local dlna-tcp-20261115.jsonl. It filters source8200
and TV192.168.168.160 and saves numerical transport data only. Check/stop using
exec session95644. Container tv-dlna-test intentionally remains serving film;
check sudo docker ps --filter name=tv-dlna-test, stop sudo docker stop tv-dlna-test
only after approval. Installer, all catalog/range checks and previous observers
finished; no download/transcode running. Existing temporary HTTP/MSX pages,
34.82GiB source and diagnostic redirects still require later approved cleanup.

## Stremio VIDAA issue and linked Reddit discussion match the failure class

User supplied https://github.com/Stremio/stremio-bugs/issues/2055 and
https://www.reddit.com/r/Stremio/comments/1pn840i/does_anybody_know_if_the_vidaa_problem_is_getting/ .
Read issue body, visible Reddit comments and all119 GitHub comments via public API
(100+19, no next page). Local source snapshots stremio-2055-comments-page1/2.json.
Issue remains open. Reddit includes the issue author's link to2055, so these are
connected discussions, not fully independent confirmations.

Matching pattern: VIDAA browser/app MKV playback stalls across source paths while
same source plays via native DLNA. Our pauses are usually transient, versus many
reports of indefinite buffering; exact same defect not proven. Original reporter
uses U7Q Pro/9.02, our known model55U7S PRO differs; actual full firmware string
not yet supplied. Async request for full V0000... version sent, answer pending.

Key evidence (technical claims paraphrased; no support contact made):
- Maintainer jaruba reproduced platform issue on43E7Q and32A5NQ, found short/high
  bitrate trailers could work, and questioned a universal16MB buffer explanation:
  https://github.com/Stremio/stremio-bugs/issues/2055#issuecomment-4343092617
  https://github.com/Stremio/stremio-bugs/issues/2055#issuecomment-4327804474 .
- User-posted support correspondence2026-06-04 says MKV support is stronger via
  USB/DLNA, acknowledges app/network playback bug and promises improvement in
  U9.6.1 after U9.6. It recommends supported streaming packaging (DASH/HLS).
  This is a forwarded support letter, not an independently verified release note:
  https://github.com/Stremio/stremio-bugs/issues/2055#issuecomment-4619857345 .
- Later users report firmware improvements, but2026-11-09 U7 report describes
  regression after updating. No universal fixed version for our model established:
  https://github.com/Stremio/stremio-bugs/issues/2055#issuecomment-6749111516 .

Implication: prioritize exact TV firmware/model/region comparison and retain working
native DLNA. Do not infer that latest firmware universally fixes it or install a
firmware from another model based on a shared9.6 label. No update/contact authorized.
The16MB/disabled-overlay explanation remains unverified, not a demonstrated cause.
If a further browser control is needed, full-length MP4 or HLS stream-copy packaging
is now a stronger proposed direction than arbitrary cache changes; DV/audio behavior
still requires verification. No new remux/HLS service authorized or implemented;
previous optional two-track MKV proposal remains history, not a pending command.
Current DLNA serves saved file only; live TorrServer handoff remains separate.

Background checkpoint: container tv-dlna-test intentionally active for viewing;
TCP sampler95644 still active around12:14:51UTC, bounded until12:16:37UTC.
All issue retrieval/check commands finished; no firmware/server state change in
this turn. Parent diagnosis remains open pending exact firmware and next decision.

## Exact TV firmware provided by screenshot

User supplied About-device screenshot. Observed software V01.09.50W.Q0312;
extended build W.Q0312.X0001.W01.Y01.J01.9.05.00. Record software identifiers only;
serial/device identifiers are not necessary for diagnosis and are not transcribed.
This answers the pending full-version question. Existing known model55U7S PRO.

Bounded public search found no exact-build changelog or verified firmware fix for
this specimen. First-hand review of another55U7S PRO explicitly states test firmware
V01.09.60W.Q0611:
https://club.dns-shop.ru/review/t-132-televizoryi/186425-obzor-hisense-55u7s-pro-prokachannyii-4k-televizor-s-mini-led-m/ .
This is primary observation of a review sample, not an official release note,
proof of OTA availability/compatibility for this unit or proof the MKV bug is fixed.
Official download page https://ru.hisense.com/support/downloads/ did not provide
a verified exact-unit newer build in retrieved public content. No unofficial
firmware package downloaded, no TV update or other external change performed.

Next user-side read-only check: Settings > Support > System Upgrade > Check Firmware
Upgrade (localized labels can differ), report whether newer software is offered
and its version before deciding any installation. Official path documented at
https://www.vidaa.com/support/ . Keep working native DLNA available. A09.60/09.61
number alone cannot establish the exact Stremio issue fix across model/region.
Original support-letter promiseU9.6.1 and mixed later reports retain their limits.

Native TCP sampler95644 has now exited0; all samplers/installers/probes finished.
Only intentionally running temporary service tv-dlna-test remains for viewing;
stop still requires approval. No download/transcode/firmware operation running.
Parent diagnosis and temporary diagnostic cleanup remain open.

## Built-in update check offers no newer firmware

User reports TV says it is already updated to the latest version after built-in
update check. Current observed firmware remains V01.09.50W.Q0312; no installation
or changed version reported. This is evidence that this TV's current OTA check
returns no update, not proof of globally latest firmware or absence of a fix for
other model/hardware/region cohorts. Review-sample09.60W.Q0611 availability and
support-letterU9.6.1 fix applicability to this unit remain unverified.

Next proposed vendor question: whether Hisense55U7S PRO on V01.09.50W.Q0312 in
user's market has a firmware fix for browser/app MKV stalls with same-file native
DLNA success (Stremio issue2055), and whether it can be delivered through OTA
without USB. User has no USB. No support message sent or contact authorized.
Keep currently accepted saved-file DLNA playback; no firmware sideload/recovery,
permanent architecture change or new MP4/HLS operation authorized. Optional full
MP4/HLS stream-copy control remains a separate decision if browser playback is
needed. Exact internal defect and live TorrServer-to-native integration unresolved.

Task background: all samplers/probes finished; only intentionally active temporary
tv-dlna-test remains serving the saved movie. Stop requires explicit approval;
status check sudo docker ps --filter name=tv-dlna-test. No download/transcode/update
running. This is an intermediate diagnostic decision, not parent-task completion.

## Official model-specific downloads checked for USB firmware

User asked whether official Hisense downloads offer firmware and USB installation.
Read raw official downloads HTML and resolved exact55U7S PRO selector ID9243.
Opened model-specific card:
https://ru.hisense.com/support/downloads/?ACTION=start&ID=9243&PARENT_SECTION=10 .
It publishes only20186350_55-65-75-85U7S_PRO_Rus PDF7.62MB, no downloadable
firmware package or software version. Generic page title/description says firmware
and instructions, but that alone is not evidence of a firmware download.
Exact linked manual (13-page PDF, read-only open):
https://cdn.hisense.ru/upload/file_tovar/Service/User%20Manuals/TV/U7S_PRO/20186350_55-65-75-85U7S_PRO_Rus.pdf .

Official generic regional VIDAA U9 e-manual page73 documents Settings > Support
> System Update > Update from USB, files at USB root,FAT32/MBR. This establishes
platform-level USB update route, not exact-unit package compatibility or confirmed
presence of this menu on55U7S PRO:
https://www.hisense.com.my/wp-content/uploads/2025/08/93041_9603VIDAA_U9_EUEMCO_E-Manual_eng_202502%E5%AE%8C%E6%95%B4%E6%9F%A5%E7%9C%8B%E7%89%88.pdf .

Conclusion: a USB update is a potential route if Hisense supplies an exact-unit
compatible package/instructions; no official public download found on the exact
model card. Proposed support request should include model55U7S PRO, current
V01.09.50W.Q0312, no OTA offered, MKV browser stalls/native DLNA success and request
USB firmware containing the issue2055-related fix. No serial/device identifier sent,
no vendor message sent, binary downloaded or firmware applied. Do not substitute a
third-party package or a related-model build for compatibility confirmation.
User previously lacked USB; asking about this route does not prove possession or
cancel DLNA. Full MP4/HLS control remains an optional distinct proposal.

Task commands complete, no background download/sampler/update. Temporary
MiniDLNA tv-dlna-test intentionally remains active for current viewing; stop and
cleanup require approval. Parent diagnosis remains open.

## Proposed convenient torrent predownload and native DLNA workflow

User asked to think through DLNA alternative with convenient torrent selection
and predownload. Clarification: both TV and phone/PC interfaces are acceptable,
phone/PC only is sufficient. Task-scoped requirement, not deployment authorization.
Keep native DLNA playback that already works. No repository/server/service changes.

Primary-source comparison:
- qBittorrent +VueTorrent: torrent-oriented search/download management; VueTorrent
  documents mobile/PWA support, integrated search, selective download and queue
  controls: https://github.com/VueTorrent/VueTorrent . Reviewable mocked demo
  https://vuetorrent.github.io/demo (not a live downloader).
- Reuse existing Jackett/indexers rather than migrate them: official qBittorrent
  integration https://github.com/qbittorrent/search-plugins/wiki/How-to-configure-Jackett-plugin .
- Radarr +qBittorrent +existing Jackett: optional film-catalog/poster interface,
  manual release choice and quality/custom-format policies. Source https://radarr.video/ .
  It adds a library/import workflow; not required for basic chosen-torrent download.
  TV remote navigation support for these web UIs not verified and not required.

Initial recommendation (proposal only): qBittorrent with VueTorrent on home-01,
existing Jackett for search and MiniDLNA exposing only completed downloads. User
on phone/PC searches title, compares release name/size/seeders, selects file(s),
starts download and sees completion; TV uses native Media/DLNA to choose ready film.
No browser media playback or transcoding in this design. Current temporary
single-file DLNA is not yet this library and needs a separately approved permanent
configuration; do not silently widen its readonly mount or replace active service.

Separate incomplete/complete folders: qBittorrent documents temp_path_enabled and
 temp_path in https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-5.0) .
Proposed same-filesystem move on completion, no unnecessary second media copy;
MiniDLNA receives read-only completed directory only. Automatic discovery via
inotify=yes is documented at
https://manpages.debian.org/trixie/minidlna/minidlna.conf.5.en.html .
Actual end-to-end behavior must be tested before accepting deployment: incomplete
file hidden, complete file cataloged once, TV discovery/seeking/audio functional,
UI removal reflected in library, existing working media/VPN unaffected.

Storage budget, retention/deletion and seeding policy remain design choices,
not inferred auto-delete or auto-download permissions. Radarr is an alternative
if movie posters/discovery/quality automation matter more than direct torrent UI;
no need to add extra request/catalog services without that requirement. Film/series
scope not yet specified; do not add Sonarr automatically. No external portal or
third-party hosted playback proposed. All actual services would remain on home-01.
Parent diagnosis/firmware investigation stays open independently of this proposal.
All task research commands finished, no new background operation. Current
single-file tv-dlna-test remains intentionally active; stop requires approval.

## Radarr website podkop addition prepared

User supplied radarr.video Cloudflare block screenshot and requested adding it to
podkop. Target domain only, suffix matching covers subdomains; no unrelated CDN,
Servarr or tracker additions implied. Read-only router preflight: dynamic manual
list, no radarr match, DNS returned public addresses rather than FakeIP; current
selector trusttunnel-out, failures0, generated sing-box check exit0.

Prepared /home/slnnk/ai-data/cudy/radarr-domains/domains.txt with single radarr.video,
validated using existing /home/slnnk/ai-data/cudy/add_domains.py without --apply.
Reviewed proposed one apply operation: backup /root/cudy-before-v2fly-radarr/podkop,
append missing suffix to podkop.main.user_domains, commit UCI, reload podkop and
verify sing-box, old-domain preservation, FakeIP and VPN state. Existing helper
previously encountered reload exit9 on LinkedIn addition; do not blindly retry
mutations if return nonzero, inspect actual resulting state read-only first.
HTTP/Cloudflare success cannot be promised from routing alone. No router changes
yet; explicit per-command approval pending under user AGENTS External changes.
All current read/preflight commands completed, no new background operation.
Current temporary native DLNA container remains intentionally active for viewing.

## Radarr website VPN routing applied and independently verified

User explicitly approved the reviewed router change. Ran existing add_domains.py
with radarr single-domain source and --apply once, session1268 exited0. Added1
radarr.video suffix to podkop.main.user_domains, UCI committed and podkop reloaded.
Backup /root/cudy-before-v2fly-radarr/podkop. Helper verified FakeIP, previous
manual domains preserved, generated sing-box config valid and healthy VPN selector.
Independent read-only UCI exports before/after excluding user_domains have equal
SHA256, confirming other UCI settings preserved. Router DNS returns FakeIP for
radarr.video and www.radarr.video; sing-box check passed, failures0.

Independent home-01 LAN-client HTTPS check resolved radarr.video through router
FakeIP and returned200, Radarr content present, Cloudflare blocked-page marker
absent. This verifies LAN request, not the user's exact browser/cache state.
User should reopen/refresh the site. No other suffix/CDN/Servarr domain added,
no repository, firewall, DNS upstream or failover setting changed. Apply/check/sync
commands finished, no new background operation. Existing temporary native DLNA
service remains intentionally active. Radarr web access is a resolved dependency
within the ongoing DLNA UI-design discussion; no deployment authorization implied.

## Synology considered as complete home-01 replacement

User asked whether Synology can run Radarr, Immich and Uptime Kuma, linked
https://synocommunity.com/packages and noted Jackett. Clarified target: replace
home-01, not an extra storage box alongside it. Budget is not allocated; compare
available options and decide later. These are task-scoped planning requirements,
not purchase, migration, deployment or permission to stop current services.

Verified primary catalog lists Radarr, Jackett, qBittorrent, Immich and Uptime Kuma.
Separate pages verified Jackett/qBittorrent/Kuma supported DSM/architectures:
https://synocommunity.com/package/jackett
https://synocommunity.com/package/qbittorrent
https://synocommunity.com/package/uptime-kuma
Immich package page retrieval failed, but catalog listing and upstream community
build recipe establish a native SPK path with Node/PostgreSQL/Redis/Python/FFmpeg
dependencies rather than a mandatory Docker wrapper:
https://raw.githubusercontent.com/SynoCommunity/spksrc/master/spk/immich/Makefile .
Exact package availability/features must still be checked for a selected model/DSM.
SynoCommunity packages are third-party, not Synology-maintained built-in apps.
Container Manager remains an alternative; compatibility model list:
https://www.synology.com/en-global/dsm/packages/ContainerManager .
Immich docs also include a Synology container guide marked community-supported:
https://docs.immich.app/install/synology/ .

Official Immich requirements current2026-11-11: minimum6GB/recommended8GB RAM,
minimum2/recommended4 CPU cores; local SSD recommended for PostgreSQL database,
not a network share. Source https://docs.immich.app/install/requirements/ .
Inference/recommendation for combined DSM/photo/download/library services: target
16GB upgradeable RAM, x86-64 platform and enough drive bays; not an official16GB
minimum or measured performance guarantee. Immich initial indexing/ML/video jobs
matter more than Radarr/Kuma idle resource use. Native DLNA direct play retains
successful TV path; photo-video processing is a separate CPU workload.
DSM7.3 specs list Media Server for DLNA:
https://www.synology.com/en-us/dsm/7.3/software_spec .

Two current reference classes, not final buying recommendations:
DS725+:2 bays,RyzenR1600/2 cores,4GB supplied,32GB max.
DS925+:4 bays,RyzenV1500B/4 cores,4GB supplied,32GB max.
Official sheets:
https://global.download.synology.com/download/Document/Hardware/DataSheet/DiskStation/25-year/DS725%2B/enu/Synology_DS725%2B_Data_Sheet_enu.pdf
https://global.download.synology.com/download/Document/Hardware/DataSheet/DiskStation/25-year/DS925%2B/enu/Synology_DS925%2B_Data_Sheet_enu.pdf .
No price/stock query or claims of cheapest/best model. Exact disk/RAM/SSD
compatibility, data/backup capacity and total ownership cost need assessment after
requirements narrow. Four bays provide growth flexibility; two bays suit smaller
capacity targets. DSM offers common package/storage administration; apps still
have separate interfaces and third-party maintenance. No all-app compatibility
claim for every model and no assumption all native packages equal upstream Docker.

Current home-01 and working temporary DLNA remain intact. All research commands
finished; no new background work or migration. Firmware issue separate; support
question was drafted but not sent by agent. Existing server not decommissioned.

## Synology evaluation replaces Immich with Synology Photos

User asked to exclude Immich because Synology has its own photo application.
For the Synology replacement comparison, use Synology Photos instead of Immich.
Task-scoped planning revision; no app installation/migration or global preference
against Immich. Historical Immich requirement/availability research remains valid
but no longer sets the active NAS memory/CPU baseline.

Official Synology Photos docs verify automatic iOS/Android photo/video backups,
folder/timeline views, albums/sharing, personal/shared spaces and face/object
organization on selected models:
https://www.synology.com/en-global/dsm/feature/photos
https://www.synology.com/en-global/dsm/7.3/software_spec/synology_photos .
Photos is Synology's own application, unlike third-party SynoCommunity apps.
Recognition is model-dependent; verify support list before model choice. Current
DSM docs note HEIC/HEVC additional previews may need Synology Image Assistant on
client devices; do not promise every format preview is processed on NAS alone.
No assertion that Photos is feature-identical to Immich or needs no indexing CPU.

Revised workload: Synology Photos, Radarr/Jackett/qBittorrent, DLNA Media Server,
Uptime Kuma. Previous16GB target was a recommendation driven by Immich; it is
superseded for this plan. Initial engineering target8GB, with4GB potentially
sufficient for light use and memory expansion preferred; not vendor-guaranteed
minimum/performance. Exact library size/users/recognition and torrent load still
unknown. Re-evaluate cheaper models as well as DS725+/DS925+ rather than keep a
four-core/16GB requirement without need. Disk bay count still depends on storage
growth, not removal of Immich. No final model or budget selected, no purchase or
migration authorized. Existing home-01/DLNA unchanged, no new background task.
