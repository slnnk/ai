---
system: home-network
status: verified
checked: 2026-11-15
tags: [ansible, mediamanager, migration]
---
# Home MediaManager replacement through Ansible

## Task and approvals

User requested replacing Radarr with MediaManager through Ansible after finding
that MobLand is a TV show, unsupported by Radarr. Bazarr was ruled out because
it manages subtitles. User explicitly approved existing master at b857c7e in
/home/slnnk/mygit/ansible, without a new branch. Existing unrelated deletion of
tracked README.md and preexisting untracked repository content preserved.
User then explicitly approved one Ansible apply command:
`.ansible-venv/bin/ansible-playbook -i inventory/hosts playbooks/home.yml --limit home-01 --tags mediamanager,minidlna`.
This authorizes the reviewed replacement command, not publication, cleanup,
new downloads, router changes or additional mutations. No commit/push authorized.

## Implementation

Added mediamanager role, pinned official stable release1.12.3 (GitHub release
API checked), private PostgreSQL17 named volume, LAN UI8000. Shared /data/minidlna
mounted once at /data; movies and tv separate from downloads/complete/incomplete.
MiniDLNA now accepts explicit media directory list, includes movies and tv with
read-only service paths. Home playbook replaces Radarr role with MediaManager;
Radarr role remains available for reviewed rollback. Its runtime data and
/opt/radarr/.env qBittorrent credential source are retained.

Source inspection of release1.12.3 found upstream entrypoint recursively chowns
/data and creates default admin password. Managed runtime bypasses that entrypoint,
uses host UID/shared media GID and umask002. One unpublished Compose run applies
migrations and creates a random-password first administrator, preserving existing
users on reruns. Stable secrets remain in target /opt/mediamanager/.env0600;
existing Jackett key and qBittorrent credentials copied privately without output.
Configuration TOML contains only nonsecret settings. Existing torrent state and
library files are not automatically imported or deleted. Upstream existing-media
import renames source folders; use only after reviewing actual files and scope.
No requests or continuous downloads are created by provisioning.

## Verification

Ten media tests passed, including Compose rendering, shared mounts, unprivileged
UID/GID, private database, DLNA scans/read-only paths, secret stability/rotation
and literal dotenv credentials. home.yml syntax check passed; bootstrap-only task
list contains ansible-user tasks only. git diff --check passed but does not cover
preexisting untracked files. Instruction lint checked10files,0errors,1warning
CDX-AG-005 in project AGENTS.md line65 (report-only).
Read-only preflight found existing six media containers running,190GiB free,
one movie directory and no MediaManager. Remote Compose5.7.1; local2.29.2.

## Deployment and independent verification

First approved apply session64567 exited2: database and secure admin created,
but application startup failed because upstream's rotating logger writes to the
read-only configuration directory. Radarr was not stopped. This was an agent
configuration error, recovered in the same task. Added supported LOG_FILE env
pointing to /tmp/media_manager.log; Docker console logs remain rotated/persistent.
Restricted final reconciliation to application service only, preserving database.
Ten tests and syntax check passed again. User explicitly approved repeating the
same Ansible command; session53995 exited0: ok34,changed6,unreachable0,failed0.
No third apply or publication ran.

Authenticated independent API checks: health200, anonymous movies401, login200,
movie/TV library200. MobLand search200 with one matching title (1.29seconds);
Inception search200 with12results. qBittorrent login204 and authenticated version
200; existing2torrents, category radarr, unchanged. All three Jackett caps200,
each advertises movie and TV search. Runtime secret mode0600. No media videos
currently in movies/tv, so no existing-file import was necessary or executed.
The earlier Radarr-era movie directory remains; no files deleted by this task.

Final independent post-apply snapshot: MediaManager and PostgreSQL healthy;
Radarr Exited0; qBittorrent/Jackett/FlareSolverr/Lampa/TorrServer continue running.
MiniDLNA active, description HTTP200, configuration and systemd ReadOnlyPaths
include both movies and tv. Shared directory modes2770 root:media preserved.
Both /opt/radarr/.env and /opt/mediamanager/.env remain root:root0600.

User opened the new login page. Supplied admin@example.com and a targeted sudo
grep command to read only MEDIAMANAGER_BOOTSTRAP_PASSWORD from the target .env;
no password printed in chat or copied to KB. API login already independently
verified; user browser login confirmation is not inferred.

## Final status and limits

Requested Ansible replacement deployed and checked. No new download, automatic
request/series monitoring, retention cleanup, router change, commit or push.
Download/import/hardlinks and native TV playback through the new manager were
not exercised; no media download permission was inferred. No task execution
sessions or helper agents remain. Central TODO and system map reconciled to
completed replacement; original Radarr acceptance remains historical evidence.

## Portable lesson

None. Upstream startup specifics remain scoped to this version and migration.

## Task metrics: home-mediamanager-20261115

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "home-mediamanager-20261115",
  "created": "2026-11-15T20:01:15.346099+03:00",
  "first_result": "fail",
  "final_result": "pass",
  "state": "closed",
  "kind": "code",
  "model": "gpt-6",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Initial readonly-log startup failure; approved retry and final independent runtime checks in source",
  "updated": "2026-11-15T20:06:36.421728+03:00"
}
```

## MobLand metadata route and season search

User logged in and reported adding MobLand stuck at Loading. Logs traced the
add-show POST to a60second timeout receiving season metadata from
metadata-relay.dorninger.co. Successful name search did not verify adding a show.

Direct home-01 season1 response stalled after18102of222587bytes and season2 after
19113of49076bytes. Personal DNS VPS31.77.132.212 received complete season1 in0.203s.
SSH to VPN endpoint timed out; no successful control on that endpoint claimed.
Router had no relay suffix, real public DNS, valid sing-box and healthy VPN.

User proposed parent dorninger.co instead of the initially prepared relay-only
hostname. Updated single-domain source and obtained explicit approval for parent
suffix before applying existing add_domains.py once with --label mediamanager.
Session67378 returned9 during Podkop reload. Did not blindly repeat mutation.
Independent read-only checks verified dorninger.co present, all previous manual
domains preserved, sing-box check exit0, trusttunnel-out with failures0 and
relay FakeIP198.18.4.63. Backup /root/cudy-before-v2fly-mediamanager/podkop retained.
Complete post-change home-01 responses: season1 HTTP200,222587bytes,0.485s;
season2 HTTP200,49076bytes,0.287s. User instructed to refresh and retry Add.
No series/request/torrent added by diagnostics.

User next reported only season1 in torrent results. Independent read-only Jackett
search found season2 on all three configured indexers: noname-club5results,
rutracker5results and rutor8results (Russian query); title examples include S2E1-9
and S02E01-09. English rutor query returned HTTP400, Russian query succeeded;
do not describe every query as successful. No downloads started.

Release1.12.3 frontend download-season-dialog.svelte initializes
selectedSeasonNumber=1 and sends that season_number in Basic mode. User should
select2 and search. Advanced query override MobLand bypasses the default search
string, which otherwise includes the show's original year2025 and S02.
The original year may narrow season2 searches excessively (season2 releases2026);
this remains a hypothesis until exact query comparison, not a proven parser bug.
Source confirms backend additionally filters to the selected season; Advanced
mode uses a plain TV search instead. Actual user's selected input was not observed.
Official Paramount release announcement confirms season2 premiere2026-09-18.
No new Ansible apply or application-code change was made; README documents
metadata routing and complete-response verification. All diagnostic sessions
have finished. Browser follow-up remains user-side; no download/TV acceptance
claimed or new execution authorized.

## qBittorrent response and season parser recovery

User reported HTTP500 downloading show dd3e93e5-4704-4d01-ba44-7f3c277cdf28.
Logs showed the release1.12.3 adapter required the literal Ok. response while
qBittorrent5.3/API2.14 returned TorrentsAddedMetadata with failure_count0,
pending_count1. Read-only qBittorrent check confirmed MobLand.S02 was already
downloading, alongside the same2Radarr torrents; did not retry adding a torrent.
Current upstream adapter handles success/pending counters. Sources:
https://raw.githubusercontent.com/maxdorninger/MediaManager/master/media_manager/torrent/download_clients/qbittorrent.py
https://github.com/qbittorrent/qBittorrent/blob/master/WebAPI_Changelog.md

Selected result289ee558-f9d5-427b-8ba7-47d2fe6ce1e9 had an empty persisted season
list despite its title S2E1-9. Release1.12.3 uses a word boundary after season
digits, so episode-style titles are omitted. This confirms the parsing cause of
missing RuTracker/NoNaMe results, beyond the earlier default-season1 observation.
User asked how parsing works; explained Jackett HTML-to-Torznab conversion and
MediaManager's own title-based season/quality parsing. Source-confirmed search
also included show premiere year2025 for later season2026 releases.

Prepared managed run-mediamanager.py startup launcher: preserve legacy success,
accept structured zero-failure positive success/pending response, preserve actual
failures without add retries; extend season parsing to S01E01/S2E1-9 while keeping
standalone and ranges; pass title-only Jackett query with existing season/ID
parameters. Built-in TV service still filters parsed season. No downloader version,
password, category, media path or existing torrent state changed.

Sixteen media tests passed, including accepted/rejected add responses, exactly one
unchanged add call, episode/range title parsing and title-only structured season
search; syntax passed. User explicitly approved one mediamanager-config apply;
session67358 exited0: ok17,changed3,failed0,unreachable0. Only app recreated;
database and downloader preserved. User asked whether configuration uses Python;
clarified normal TOML/env/Compose settings versus secret/admin helpers and the
version-specific runtime compatibility bridge. No new global preference inferred.

Prepared exact-match /tmp/recover-mobland-record.py, read-only by default.
Initial dry-run safely refused because persisted seasons were empty. Corrected
preflight to accept exactly the observed empty-or-season2 metadata and require
the reviewed S2E1-9 title, real qBittorrent S02 name, matching save path, one hash
and no conflicting torrent/season-file record. Final dry-run passed; user then
explicitly approved --apply. Session85581 exited0: one transaction inserted torrent
and season-file association for season2 and corrected the stored indexer season.
No qBittorrent command, new add, pause, cleanup or file move was sent by recovery.
Progress was29.11percent at recovery. Repeating script would report already linked.

Independent authenticated API verification session32704 exited0:
show torrents HTTP200,count1,linked seasons[2],status downloading,imported false.
Basic season1 search HTTP200:32results (RuTor12,NoNaMe12,RuTracker8).
Basic season2 search HTTP200:10results (NoNaMe5,RuTracker5),all parsed season2.
No claim that RuTor season2 Basic worked; direct generic Russian search earlier
found it. Actual new add was not sent as a test. New-manager real import and TV
playback remain unverified until the current user-started download finishes.

Project AGENTS and role README document version compatibility/recovery. Instruction
lint:10files,0errors,1CDX-AG-005warning (report-only). No commit/push. All task
commands finished; the user-started torrent intentionally continues in qBittorrent.
Central TODO now tracks completion/import/TV acceptance; no extra mutation allowed.
