---
system: home-network
status: verified
checked: 2026-11-14
tags: [jackett, migration, lampa, tv]
---
# Home Jackett indexer migration and TV cutover instructions

## Task and approval

User requested transferring the previously configured indexers and instructions
for the TV. Scope is the three source configurations, associated decryption keys,
verification and TV guidance; no old-PC shutdown or other media-data migration.
The transfer, protected backup and brief target Jackett stop/start were described
before execution and the execution approval covered that command. Tracker Test
requests and the RuTor retry were also described in their execution approvals.

## Context

Source PC Docker container jackett mounts ~/ai-data/jackett at /config. Source
configuration has exactly rutor, noname-club and rutracker, plus DataProtection
keys. Target is home-01 /192.168.168.2, new Jackett in /opt/jackett, with an
initially empty/missing Indexers directory and its own protection key. Target
server configuration and runtime API key must remain unchanged.

## Actions

Transferred the three current .json indexer files and one source protection-key
XML as opaque bytes in memory over authenticated SSH. No source credential/key
values were printed or written to another controller artifact. Target existing
protection keys were retained; source key was added so encrypted source account
settings remain readable. No ServerConfig.json, API key, .bak indexer files,
logs or unrelated source settings were copied. Runtime configs are outside Git.

Before target changes, copied its existing DataProtection directory to private
/opt/jackett/migration-backup-20261114T164258Z. Backup directory mode0700,
files0600. Briefly stopped only target jackett service, wrote configs/keys with
service ownership and private permissions, verified byte hashes and unchanged
ServerConfig hash, then started it. Failure handling would restore affected files
from the backup and restart the service. Transfer helper was
/tmp/migrate-home-jackett-indexers.py, containing no embedded secret values.

## Verification

Target API lists exactly noname-club, rutor and rutracker configured. NNM-Club
and RuTracker built-in Test returned HTTP204. RuTor first Test failed with TLS
connection reset; read-only container DNS resolved rutor.info to router FakeIP
198.18.2.147 and HTTPS GET returned200, then repeated Test returned204 without
changing indexer, DNS, router or VPN settings. All three final tests passed.
Account login, sessions and any challenge data stayed inside the services.
Tests do not prove playback on the TV.

## TV instructions

Media Station X startup parameter:192.168.168.2:8080, then restart MSX.
Local Lampa URL is http://192.168.168.2:8080. In Lampa settings set TorrServer
primary URL to http://192.168.168.2:8090. Enable parser, select Jackett and set
URL http://192.168.168.2:9117. Copy the API key from the new Jackett dashboard
at that URL into the Lampa API-key field; it was deliberately not copied from
the PC or printed here. Restart Lampa, search a title and verify playback.
Frontend/browser storage is per-origin, so settings may need re-entry for this
new local frontend. No tracker account re-entry is needed after passing Tests.

## Status and risks

Requested migration complete. All migration and test processes exited; no task
background operations remain. Both old PC services and the intended home Docker
services remain running; no shutdown was requested. No repository changes.
TV cutover/playback and any broader PC media-data migration remain unperformed
and are tracked in the existing central TODO. Server configuration/API key was
preserved; user obtains the new key directly from the target UI.

## Portable lesson

none

## Task metrics: home-indexer-migration-20261114

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "home-indexer-migration-20261114",
  "created": "2026-11-14T19:45:35.733338+03:00",
  "first_result": "pass",
  "final_result": "pass",
  "state": "closed",
  "kind": "operations",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Three opaque configs and protection key copied, target settings preserved, all final tracker Tests204; TV instructions documented",
  "updated": "2026-11-14T19:45:35.733385+03:00"
}
```
