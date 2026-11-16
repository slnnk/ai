---
system: home-network
status: verified
checked: 2026-11-15
tags: [ansible, radarr, qbittorrent, minidlna]
---
# Home Radarr roles and diagnostic cleanup preparation

## Task and authorization

User selected Radarr on the existing home server, retained Lampa/TorrServer for
a possible later firmware retry, requested removal of diagnostic scripts and
downloaded test media and restoration of normal Lampa settings. User explicitly
approved working on existing master instead of a new feature/home-radarr branch,
requested a separate MiniDLNA role and chose /data/minidlna for torrent data.
This is local preparation authorization; per-command remote-change approval and
publication approval remain required. No commit, push, deployment or cleanup ran.

## Changes

Existing checkout /home/slnnk/mygit/ansible preserved, including deleted tracked
README.md and preexisting untracked configuration. Added separate radarr and
qbittorrent Docker roles and native-package minidlna role to home.yml. Shared
media group, setgid directories, umask002 and one /data bind mount preserve
same-filesystem hardlinks. Host root /data/minidlna contains downloads/incomplete,
downloads/complete and movies; only movies is scanned by MiniDLNA, with a
read-only service mount. LAN UIs 7878/8081; MiniDLNA uses enp1s0,8200/1900.
Pinned upstream LSIO release tags verified through official GitHub API:
Radarr6.4.4.10685-ls326, qBittorrent5.3.0_v2.1.2-ls487. Package minidlna uses
state:latest. Existing Lampa/TorrServer roles and runtime settings retained.
Documented required first-login credentials and authenticated Radarr download
client/indexer setup; no account/password invented or application link claimed.
Updated role READMEs, home group vars, project AGENTS.md and media checks.

## Verification

Home playbook syntax check passed using the repo-local environment. Seven media
tests passed, including native Docker Compose rendering, common mount and group,
LAN bindings and exclusion of incomplete downloads from the DLNA tree. Bootstrap
tag task listing contains only ansible-user tasks. git diff --check passed but
does not cover the preexisting untracked configuration. Instruction lint checked
10 files:0errors,1warning CDX-AG-005 in project AGENTS.md:59; report-only.

Read-only SSH verified home-01 available,175GiB free before cleanup, existing
media containers running, test tv-dlna-test active, /data/minidlna absent.
Prepared /tmp/home-media-cleanup.py, default read-only. Remote dry run passed:
original Lampa index matches current minus exactly the diagnostic injection;
original MSX action is link:http://192.168.168.2:8080. Test container has expected
read-only single-file mount and AutoRemove. Exact known targets total39040187037
bytes: playback-diag.js, playback-test, container-test, playback-from-start,
playback-seek-control, playback-http-control under active Lampa release; scratch
/opt/torrserver/data/container-test-20261114T203921Z and /opt/lampa/diag-backups.
The script restores original index/startup before stopping tv-dlna-test, removing
these targets and creating /data/minidlna. No server mutation performed.

## Cleanup executed after approval

User explicitly approved the exact cleanup command. It completed with exit0:
normal Lampa index and MSX startup restored, diagnostic single-file DLNA stopped
and auto-removed, known diagnostic pages/scripts/backups and test MKV/clips
removed (39040187037bytes), /data/minidlna created. No new services deployed.
Independent read-only SSH verification passed: root and MSX startup HTTP200 with
allow-origin*, expected ordinary startup action and bootstrap script, no diagnostic
index reference; all six diagnostic HTTP paths404; scratch/backups absent; test
container absent and all four original media containers running. Root free space
now212GiB (was175GiB). No background task operation remains.

## Checkpoint and remaining work

Requested roles, cleanup and directory creation are complete. Subsequent user
request to execute deployment and authenticated linkage completed as recorded
below. Basic real download/import/hardlink/native-TV playback subsequently passed
as recorded below; central TODO is reconciled to that acceptance. No background task commands or agents remain. No Plex, firmware,
router, automatic download or media-deletion change was made.

## Portable lesson

None.

## Task metrics: home-radarr-20261115

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "home-radarr-20261115",
  "created": "2026-11-15T16:56:02.521210+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "code",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "User confirms actual TV playback; real1554290370byte download imported, same device/inode and nlink2 prove hardlink, MiniDLNA1video and empty Radarr queue verified. Duplicate-add409 explains reported error without repair;4K/seeking not claimed.",
  "updated": "2026-11-15T17:25:31.140460+03:00"
}
```

## Plex addition discussed

User asked what adding Plex would provide; this is discussion, not permission
to implement or deploy. Plex would read the same imported movies library and
provide a TV/phone catalog with posters and resume/watch state. Radarr remains
responsible for acquisition/import, qBittorrent for downloads; MiniDLNA can
remain alongside Plex as the already proven native-TV playback route.

Official Plex support lists VIDAA U4+ support, but exact regional availability
on this unit and large HEVC/HDR playback have not been tested. Smart TV playback
uses manufacturer playback systems; app availability does not prove that Plex
bypasses the observed VIDAA browser/media failure. Direct Play preserves the
file; Direct Stream repackages streams; transcoding can convert incompatible
tracks and may be triggered by subtitles. Hardware acceleration generally needs
Plex Pass and supported hardware; no server4K-transcode capacity was assessed.
Sources: https://support.plex.tv/articles/204080173-which-smart-tv-models-are-supported-/ ,
https://support.plex.tv/articles/203810286-what-media-formats-are-supported/ ,
https://support.plex.tv/articles/200430303-streaming-overview/ ,
https://support.plex.tv/articles/115002178853-using-hardware-accelerated-streaming/ ,
https://support.plex.tv/articles/navigating-the-big-screen-apps/ .
No Plex choice, installation or additional external operation authorized. Existing
deployment proposal remains unchanged in central TODO; no new action created.

## Deployment and authenticated linkage completed

After the user deferred Plex and asked to execute items1and2 (deployment and
application links), ran home.yml limited to home-01 and tags
qbittorrent,radarr,minidlna. First run installed qBittorrent but Radarr image pull
timed out at lscr.io; retry timed out on another layer. Official LSIO FAQ verifies
lscr.io redirects to GHCR and supports pulling directly there. Changed only
radarr_image registry to ghcr.io/linuxserver/radarr with identical pinned
6.4.4.10685-ls326 tag, updated README and reran syntax/7media tests successfully.
Final radarr,minidlna run completed23ok,8changed,0failed. MiniDLNA is the native
package/systemd service, not a Docker replacement test container.

One-time local /tmp/configure-home-radarr.py executed over SSH stdin; no helper
script saved on home-01. Generated unique random admin passwords, saved only
in target /opt/radarr/.env (root0600), configured qBittorrent password through its
temporary first-session credential and Radarr form authentication through API.
No password, cookie value or API key was printed. qBittorrent5.3 differs from
older API wiki examples: bad credentials HTTP401, success HTTP204/empty body,
cookie QBT_SID_8081. Initial provisioning attempts incorrectly assumed Ok. and
SID; corrected after secret-safe live inspection and official current source.
Use a cookie jar plus an authenticated endpoint to verify login.

Configured qBittorrent paths /data/downloads/complete and
/data/downloads/incomplete, temporary paths enabled, category radarr, no
UPnP/NAT-PMP for peers or WebUI. Added accessible Radarr root /data/movies,
enabled copyUsingHardlinks and Completed Download Handling. Home qBittorrent
client uses192.168.168.2:8081, category radarr, permanent credentials; automatic
removal of completed/failed downloads disabled. Existing Jackett key and
indexer credentials retained. Separate Torznab entries for noname-club, rutor,
rutracker: all Radarr built-in Test calls passed. Interactive search enabled;
RSS and automatic search disabled to preserve manual release selection.

RuTor initially failed with successful query but no results in movie categories.
Live caps/search confirmed all results Other8000. Official Jackett rutor.yml
documents missing source categories and statically assigns Other. RuTor alone
now uses[2000,8000]; NNM-Club/RuTracker use[2000]. No Jackett indexer modified.
Added operational notes to radarr/qbittorrent READMEs.

Independent /tmp/verify-home-radarr.py over SSH passed: both APIs reject
unauthenticated requests; actual Radarr form login reaches/with RadarrAuth
cookie and saved credentials; Radarr API independently requires its key.
qBittorrent permanent login/preferences/category/empty torrent list verified.
Three indexers and download client persisted; movie root accessible; hardlinks
and completion handling enabled. Catalog lookup tmdb:603 returned one result.
Health has only two expected disabled-RSS/automatic-search notices. MiniDLNA
active+enabled, rootDesc friendlyName Home Movies, movies-only media_dir and
read-only service override verified. Six original/new Docker containers running,
all restart counts0. No movie added, torrent started or test media downloaded.
All local exec sessions exited, no task background operation remains.

User-facing entry points: Radarr http://192.168.168.2:7878 and qBittorrent
http://192.168.168.2:8081; username admin for both. Privately retrieve passwords
through sudo cat /opt/radarr/.env on home-01. The outstanding step is a real
download/import/hardlink and native-TV playback acceptance, not another deployment.
No commit or publication performed; master and unrelated checkout files retained.

Sources: https://docs.linuxserver.io/faq/ ,
https://github.com/linuxserver/docker-radarr/pkgs/container/radarr ,
https://raw.githubusercontent.com/qbittorrent/qBittorrent/master/src/webui/api/authcontroller.cpp ,
https://raw.githubusercontent.com/Jackett/Jackett/master/src/Jackett.Common/Definitions/rutor.yml .

## Real download, import and TV playback accepted

User reported Failed to connect to qbittorrent after clicking the same release
again. Read-only diagnostics verified both containers running with0restarts and
HTTP reachability. Radarr logged POST torrents/add409; qBittorrent log explicitly
reported attempts to add a duplicate. One selected film was already100percent
downloaded and seeding. No password/network/service change needed or performed.
Radarr API masks stored client passwords, so direct equality with the saved
password is not a valid authentication test; authenticated calls work.

User then explicitly confirmed the film plays on TV. Completed read-only check
verified Radarr hasFiletrue, file1554290370bytes, empty queue; completed download
and imported movie share device2050/inode1572871 and link count2, proving a
real hardlink with no second media copy. MiniDLNA database contains1video.
Thus real download/import/hardlink/catalog/native-TV playback accepted for this
file. Separate4K/HDR behavior and seeking were not established by this statement;
the original VIDAA browser bug is not fixed or newly diagnosed. No task background
operation remains, no repair or new torrent launched by the agent.

Source for misleading error class: https://github.com/qbittorrent/qBittorrent/issues/18361 .
The chosen Radarr pipeline now fulfills the requested basic workflow.
