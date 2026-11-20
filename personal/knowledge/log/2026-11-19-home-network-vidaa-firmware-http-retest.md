---
system: home-network
status: verified
checked: 2026-11-19
tags: [vidaa, msx, http]
---
# Home network: VIDAA firmware HTTP retest

## Task

Prepare a Media Station X playback retest after the user reported a new TV firmware.

## Context

The [previous static HTTP control](2026-11-14-home-network-4k-playback.md#full-http-sequence-also-reproduces-fixed-position-waits) reproduced four playback waits. The byte-identical source was removed in [approved cleanup](2026-11-15-home-network-radarr-roles.md#cleanup-executed-after-approval).
The local fallback is the complete 20351317548-byte Resident Evil 4K HEVC MKV,
5632.8 seconds long. This can detect playback problems on the fallback source but
cannot establish whether the exact previous pauses disappeared.

## Actions

Reused the previous HTML player and diagnostic observer. The program watches
60 seconds, seeks back 30 seconds, watches 180 seconds, seeks forward 1800
seconds and watches 300 seconds. Maximum runtime is 20 minutes. Both scripts
passed Node.js syntax checks. Read-only server preflight confirmed the complete
file, shared filesystem for the hardlink, existing normal MSX startup and CORS.

## Changes

Local prepared payload: `/tmp/msx-firmware-20261119.TpYRLQ/deploy.py`.
Default invocation is read-only. Its SHA-256 is
`581042c6ac005efbf005bcc2118f9b2404f45d8416b466037f689f1749da3d02`.

## Status and risks

The user explicitly approved placement. Deployment session 85122 exited 0.
The normal MSX start file is saved at
`/opt/lampa/msx-start-before-firmware-test-20261119.json`.
The live startup points to `http://192.168.168.2:8080/vidaa-firmware-test/?v=65468737e23d`.
The static media link shares the source device and inode. The installer checked
three byte ranges, CORS and MIME. An independent LAN check verified the start
file, page and observer contents, MKV signature via HTTP 206 and a diagnostic
probe in Apache logs. No installer or observer commands are running. The test
will start when the user reopens Media Station X. TV playback, comparison and
later restoration of the normal startup remain in central TODO.

## OTA visible but blocked by network error

The TV screenshot shows installed build `V01.09.50W.Q0312`, offered build
`V0000.09.62M.Q0921`, package size 1000 MB and `Сеть недоступна`.
Cudy recorded DHCPACK for the TV's known LAN address at 20:20:29 MSK.
WAN is up, router DNS resolves, and home-01 reached Hisense and VIDAA
public HTTPS sites. There was no ping response from the TV and its OTA
endpoint was not identified. These checks cannot establish TV Internet or
OTA reachability. The MSX test page remains configured. No test-page hits
or diagnostic events from the known TV address were recorded in the
checked 20-minute window. No external change or background command remains.

## TV network check passed

The TV reported successful network connectivity, 40.224 ms latency and a
100 Mbps connection. Cudy's sing-box log showed the OTA host
`ota-tv-ru.vidaahub.com` had returned `read response: EOF` for an A query
at 20:25:04 MSK. During follow-up, Cudy, Google and Cloudflare resolved the
same CNAME and address. A verified TLS request from home-01 to the original
OTA hostname reached HTTP 404 at the root path. This checks DNS and transport
from the home server. The actual firmware request needs a TV-side retry and
its outcome remains unconfirmed. No network settings were changed.

## TV link rate and follow-up

The user repeated the check and reported the same result with slightly
different latency. The TV displayed 100 Mbps. The official Hisense model
page lists Ethernet without a rate. A firsthand model review reports
100 Mbps as the wired maximum. Cudy learned the TV MAC through lan2,
which is itself linked at 1 Gbps. The router port rate does not establish
the final link rate if a switch is in between. The bounded connection
samples on Cudy showed TV DNS activity and no flow to the resolved OTA
address, and no new matching DNS error was logged. A short connection
could have fallen between polls. Both samplers exited; OTA and MSX playback
remain pending. No network settings were changed.

## Podkop single-host trial proposed

The user asked about testing the OTA hostname through Podkop. Read-only
preflight found Podkop's existing DNS upstream is DoT, the OTA hostname is
absent from the manual VPN list, Cudy returns its current public DNS answer,
and tun0 is up. The existing helper validated a one-line domain source
at `/tmp/vidaa-ota-podkop.qCqirl/domains.txt` with label
`vidaa-ota-20261119`. Proposed external action: back up Podkop, add
`ota-tv-ru.vidaahub.com` to the main VPN list and reload once, then verify
FakeIP and LAN-side TLS before asking for the TV OTA retry. No router changes
have been made. Awaiting explicit approval for this test within the current
central VIDAA task.

## Podkop single-host trial applied

The user explicitly authorized the single-host change. The helper committed
the new entry and invoked reload once. It exited 9 during reload, so the
independent checks were run without another reload. The backup at
`/root/cudy-before-v2fly-vidaa-ota-20261119/podkop` matches the active file
byte-for-byte after removing the single added domain line. The active
sing-box config passed validation, tun0 was up and the existing VPN probe
returned HTTP 200. Cudy DNS and home-01 both resolved the OTA name to
FakeIP `198.18.7.131`. HTTPS from home-01 reached that peer with valid TLS
and HTTP 404 at the bare root. The firmware download itself still needs the
TV retry. No diagnostic or deployment process remains.

## OTA UI reached download state

The TV screenshot after the rule change showed `Выполняется загрузка... 0%`
for `V0000.09.62M.Q0921`. It says installation will occur at power-off.
Cudy observed TV HTTPS to the new FakeIP and a reply, confirming that the
TV used the rule. Brief snapshots at 20:49 MSK showed only small HTTPS
flows, with no sustained transfer in the checked interval. Package download
and installation remain unconfirmed. No further external change was made.

## OTA returned to network error

The user reported `Сеть недоступна` after the 0% download screen. The
first OTA hostname still resolved to FakeIP and answered via valid TLS from
home-01. Read-only AdGuard query-log API inspection found
`ota-dl.vidaahub.com` at 20:51:33 MSK resolving to 89.222.125.6, an address
also seen in TV HTTPS flows and shared with some other VIDAA names. The
timing and hostname identify it as a candidate download host, not proof
of the exact package request or failure. The download hostname's bare
root responds to HTTP and HTTPS from home-01 over the existing routing.
The actual package path was not observed. Proposed separate test: add
only `ota-dl.vidaahub.com` to Podkop. Validated local source:
`/tmp/vidaa-ota-download-podkop.yKR4Ht/domains.txt`. Await explicit
approval before making this additional change. No background jobs remain.

## OTA download hostname VPN rule applied

The user approved the second exact hostname. The helper committed
`ota-dl.vidaahub.com` and invoked reload once. Reload returned exit 9.
Independent verification confirmed the prior rule and all other settings
were preserved against backup
`/root/cudy-before-v2fly-vidaa-ota-download-20261119/podkop`.
The generated sing-box configuration passed validation and tun0 remained up.
Cudy returned FakeIP `198.18.7.136` for the new hostname and
`198.18.7.131` for the first. Home-01 HTTPS reached the new FakeIP with
validated TLS and HTTP 200 at the root. The existing VPN probe returned 200.
No background operations remain. The actual TV firmware payload requires
a fresh TV retry and remains unverified.

## OTA transfer confirmed through the second rule

The user reported 27% after the second rule was applied. At 20:55:13 MSK,
Cudy conntrack showed the TV's established HTTPS connection to the
`ota-dl.vidaahub.com` FakeIP with 109081019 reply bytes on that connection.
The user-visible progress and TV traffic confirm package transfer through
the rule. Download completion, installation and MSX playback remain pending.

## Firmware installed according to user

The user confirmed the TV updated after switching it off with the remote.
The exact installed build was not independently checked. LAN verification
confirmed the prepared MSX action and test page HTTP 200. No test requests
from the TV were observed in the preceding 12 minutes. Post-update TV
playback remains pending. No background operations remain.

## Post-update MSX playback passed on Resident Evil

The user launched the test after confirming the firmware update. The TV
observer recorded first playback at 21:04:32 MSK and `test_done` with reason
`completed` at 21:13:34 MSK. All three actual-watch stages completed
(60, 180 and 300 seconds). The video was 3840 by 2160 and the observer
showed zero dropped frames at the end. There were no media errors,
`stalled` events or non-seek waits during playback. The only waits were
initial startup (1.008 seconds), the backward seek (0.198 seconds) and
the forward seek (0.191 seconds). The observer saw the first audio track
selected. It cannot establish the audible output.

The [older HTTP control](2026-11-14-home-network-4k-playback.md#full-http-sequence-also-reproduces-fixed-position-waits)
recorded four non-seek waits. The exact original file was removed earlier;
this run confirms smooth playback for the replacement 4K HEVC MKV on the
updated TV, without a matched before-and-after conclusion for the old file.
The TV playback test and log checks completed. The server still delivers
the temporary MSX startup; restoring the normal page remains an external
change that needs explicit approval. No background observer command remains.

## Ordinary Lampa startup restored

The user explicitly requested ordinary Lampa back. The restore (session
19151, exit 0) validated both the normal backup and active test action,
then atomically restored the saved MSX startup. HTTP content and CORS
matched the saved file. An independent LAN check verified the normal MSX
action and app root HTTP 200. No background operation remains. Only the
startup restoration was requested; diagnostic assets were left in place.

## Portable lesson

none
