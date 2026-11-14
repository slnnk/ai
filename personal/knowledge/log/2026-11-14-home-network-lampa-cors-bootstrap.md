---
system: home-network
status: verified
checked: 2026-11-14
tags: [lampa, msx, cors, bootstrap, ansible]
---
# Lampa MSX CORS repair and automatic media settings

## Task and scope

User reported `server responded with status 0` after entering the home frontend
address in Media Station X. They then requested preconfigured TorrServer and
Jackett so no manual backend/key entry is needed on the TV. Existing authorized
ansible master checkout reused; no staging, publication or unrelated changes.

## Findings

Apache logs showed TV192.168.168.160 successfully requested /msx/start.json twice
with HTTP200. Independent HTTP checks found no Access-Control-Allow-Origin header.
Official MSX documentation requires CORS and lists missing headers as a common
status0 cause: https://msx.benzac.de/wiki/index.php?title=Tips_%26_Tricks.
The original role's HTTP-only readiness checks missed this cross-origin requirement;
the previous deployment checks did not prove MSX could consume its JSON.

## Changes and approvals

- Apache command in the Lampa Compose template now sets allow-origin * and
  Origin/Content-Type/Accept allowed headers. Role readiness requires HTTP200
  and the CORS header. Native Apache syntax and Compose tests passed.
- Described and applied lampa-config only after execution approval: ok7,
  changed2, failed0/unreachable0. Independent LAN checks confirmed header * on
  root and startup JSON. Log: ~/ai-data/home-media-lampa-cors-20261114.log.
- Added optional structured lampa_media mapping in role defaults/home group vars:
  backend URLs and target Jackett ServerConfig path. No API key in inventory/Git.
- Home playbook now runs TorrServer and Jackett before Lampa. The role slurps
  only target runtime config with no_log, renders runtime home-media.js with
  no_log/diff suppression and loads it before upstream application scripts.
- Browser bootstrap enables Jackett parser, chooses primary backend links,
  sets TorrServer/Jackett URLs and target API key once per settings fingerprint.
  Later manual changes survive reload; backend/key changes update media settings.
  Favorites/history are untouched. Disabling the optional mapping removes the
  role-owned script/tag, retaining browser settings. Runtime key is delivered
  to trusted LAN clients as required for their Jackett requests.
- Updated role README and project AGENTS; five tests passed, including script
  execution, manual-choice retention and key rotation. Standalone empty mapping
  was separately checked. Syntax-check passed. Agent lint: zero errors, existing
  CDX-AG-005 warning for generic defaults/main.yml reference; no auto-fix.
- Described and applied lampa-config bootstrap after execution approval: ok13,
  changed2, failed0/unreachable0. Log:
  ~/ai-data/home-media-lampa-bootstrap-20261114.log. No backend/container data
  changes or tracker/key regeneration; existing CORS correction retained.

## Verification

Independent LAN fetch verified the bootstrap loads before upstream Lampa scripts
and is served with CORS. Executed its live bytes in a Node browser-storage stub;
verified both URLs, parser enabled and key presence without printing/saving key.
Torznab caps returned200 with that key and CORS; cookie-aware UI query confirmed
exactly noname-club/rutor/rutracker configured. Initial diagnostic attempted the
UI indexer-list API without its browser cookie and received an HTTP error; the
correct Torznab key test and cookie-aware list query passed without product changes.

## Status and risks

Both fixes deployed and server-side verification complete. Actual MSX relaunch
and TV playback still require user confirmation. All Ansible and diagnostic
processes exited; no task background commands remain. Lampa and backends remain
intentionally running. No user credentials, API key or frontend script containing
it were copied into Git or notes. TV now needs only the MSX startup parameter
192.168.168.2:8080 and a full application restart. Earlier manual backend/API-key
instructions in prior logs describe the superseded configuration stage.

## Portable lesson

none

## Task metrics: lampa-cors-bootstrap-20261114

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "lampa-cors-bootstrap-20261114",
  "created": "2026-11-14T20:05:03.928753+03:00",
  "first_result": "pass",
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
  "evidence": "Native config, five tests and deployed CORS/bootstrap/Torznab verification passed; TV end-to-end retry unconfirmed",
  "updated": "2026-11-14T20:05:03.928802+03:00"
}
```
