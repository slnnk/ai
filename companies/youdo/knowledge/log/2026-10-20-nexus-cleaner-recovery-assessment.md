---
system: nexus
status: verified
checked: 2026-10-20
tags: [nexus, cleaner, nomad, recovery]
---
# Nexus cleaner credential recovery assessment

## Task

Assess whether creating a Nexus user is sufficient to restore nexus-cleaner. Investigation only; no user creation, secret update, job trigger or repository edits authorized or performed.

## Context

Local checkout /home/slnnk/git/nexus-cleaner at ba922e38f8905e5464ac22a38eafcdc84b6f917b; cached origin/master matches, remote revision not refreshed. Existing untracked t.go preserved. Prior October14 exclusion was task-specific; the user now requested this assessment.

## Actions and findings

Read-only authenticated Nomad and Nexus GETs on October20 verified:
- Nexus user lookup for cleaner returns an empty list (HTTP200).
- Existing nx-docker role includes Docker browse/read/delete and docker-hosted add/edit/browse/read/delete privileges. Reuse this role according to current company convention.
- docker-hosted is online, Basic Auth enabled, HTTP connector3003. Admin GET /v2/ on that connector returns200; REST search returns200 with50items and continuation token. These checks do not prove cleaner authentication or worker network access.
- Nomad periodic parent nexus-cleaner remains enabled, batch, running; cron 0 1 * * * UTC (04:00 Moscow), prohibit overlap. Retained child nexus-cleaner/periodic-1791680400 is reported running; parent allocations list is empty. Neither observation proves a successful cleaner run.
- Live template reads secret/admin/nexus-cleaner and supplies NEXUS_ADDR, NEXUS_USER, NEXUS_PASS, IMAGE_KEEP_REGEXP, IMAGE_KEEP_COUNT and IMAGE_AGE_DAYS. Production Vault secret values were not read; only a test Vault token is available in current/.env.

Code searches docker-hosted through REST and deletes manifests through NEXUS_ADDR plus :3003. One Basic Auth credential pair covers both. Restoring cleaner with the password already stored in Vault may suffice without rebuilding or redeploying, provided address and retention settings remain correct. If a different password is chosen, the corresponding Vault secret must also change. Do not claim verified recovery until authenticated GET checks and an authorized subsequent run are observed.

Code scopes images to the youdo prefix, excludes youdo/base-images and latest tags, applies regex/count and age retention. It has no dry-run; deletion is by manifest digest, so shared-digest tags require care. Search does not validate HTTP status and can misreport an unauthorized empty response as success. Historical October14 audit identified cached image bytes different from the restored registry tag; actual currently running image implementation remains unverified.

## Changes

This note, the existing Nexus map, indexes and sync note only. No infrastructure changes or repository edits.

## Status and risks

Assessment complete. Credential restoration, address/retention confirmation and controlled execution remain under the existing cleaner item in ~/ai/TODO.md (Nexus section); no duplicate backlog entry. Credentials are the confirmed blocker, but sufficiency is conditional on the unverified production Vault values and runtime image. Creating the account may enable deletion on an existing retry or future periodic execution without a separate manual trigger.

## Portable lesson

none

## Production Vault access follow-up

On October20 the user asked whether production Vault read access is available. Existing ~/.vault-token was found through the documented local Ansible access route. GET http://vault.service.consul:8200/v1/auth/token/lookup-self and GET /v1/secret/admin/nexus-cleaner both return403 with that token. Thus production secret read access is currently unavailable through this route; no secret values were printed or stored. A fresh approved production token or user login is required before dependent configuration checks. Existing test token does not establish production access. No login or external change attempted. This is a limitation within the existing cleaner TODO, not a separate restoration task.

## Approved user creation

User supplied VK_PROD_NEXUS_CLEANER_USER and VK_PROD_NEXUS_CLEANER_PASSWORD in current/.env and explicitly requested account creation. The per-command approval described active cleaner creation, existing nx-docker role, password source and possible resumed deletion by existing scheduled work; execution was approved. POST /service/rest/v1/security/users returned200. Independent admin GET confirmed user cleaner active with sole role nx-docker. No Vault mutation or cleaner trigger performed.

Immediate authenticated REST search and Docker connector GET checks both returned429; connector response supplied Retry-After30. This verifies creation, not successful cleaner authentication or service recovery. Existing rate-limit follow-up in the Nexus TODO remains open. No password values stored outside current/.env or printed.

## HTTP429 cause verified

Follow-up read-only diagnostics on October20: identical REST search returns429 for cleaner with Retry-After30 and response text `Too many authentication attempts`, while admin receives200. This is authentication-attempt throttling for the cleaner principal, not the Community Edition aggregate repository-request quota. Latest request.log records Go-http-client/1.1 search attempts every6–9seconds through13:53MSK, all429. Historical logs identified the rate-limit key user::cleaner. The ongoing client loop is consistent with continued throttling; present password mismatch and exact lockout renewal behavior are not independently proved. To verify recovery, first pause the retrying client with explicit approval, allow cooldown, then authenticate using the supplied credentials and check the deployed credential source if needed. No pause, credential change or configuration mutation performed. Existing cleaner TODO already covers this remaining work.

## Nomad status verified at 13:55 Moscow

Parent nexus-cleaner is running/enabled, periodic01:00UTC, ProhibitOverlap=true. Only retained child nexus-cleaner/periodic-1791680400 was submitted October11 at04:00Moscow and remains running. Its allocation6ec3c948-7e7d-07f4-6e23-56c85a06b01a on msk3-nomad02.youdo.corp (172.24.0.12) reports pending during restart backoff, desired run, task restart counter114693. Repeated exit1 events followed by5–6second backoff and task starts confirm a continuous crash loop, not successful execution. ProhibitOverlap means this active child blocks later overlapping scheduled runs.

Read-only client fs logs confirm repeated requests to http://msk3-nexus.youdo.corp/service/rest/v1/search?repository=docker-hosted. Fatal error is `get images error - body unmarshal error: invalid character '<' looking for beginning of value`. This is consistent with parsing the previously verified HTML429 response as JSON. No stop/restart/trigger/update performed. Existing cleaner TODO remains open.

## Approved child job stop

User explicitly instructed stopping the stuck child after the concrete plan. DELETE /v1/job/nexus-cleaner/periodic-1791680400?purge=false returned200. Independent GET confirms child status dead and Stop=true; history preserved. Parent GET confirms Stop=false, Periodic.Enabled=true and schedule0 1 * * *UTC retained. No new child triggered, no credential/Vault change, no repository edits. Remaining credential/cooldown/retention/run checks remain covered by the existing cleaner TODO.

## Cooldown verification and corrected interpretation

User requested step2 after stopping the child. At10:58UTC, more than70seconds after the allocation finished at10:56:57UTC, both cleaner-authenticated search and connector still returned429, Retry-After30, `Too many authentication attempts`; allocation remained complete/dead. No successful credential verification claimed. User suggested a longer lockout; subsequent retries were suspended.

Official Sonatype3.96 release notes describe a known issue (affected version range3.94.0–3.96.3; fixed3.97.0): Retry-After30 may coexist with lockout up to900seconds, and attempts even with valid credentials can restart the timeout. Recommendation is15uninterrupted minutes after the last authentication attempt. Source: https://help.sonatype.com/en/sonatype-nexus-repository-3-96-0-release-notes.html . Our recorded version3.96.4 falls outside that explicitly listed affected range, so this is strong explanatory context, not proof of the exact installed-version timeout. No explicit rate-limit overrides found in nexus.properties/docker-compose.yml or matching main-log lines. Earlier30second recovery expectation is superseded: header alone does not establish full cooldown. Existing cleaner TODO covers verification after an uninterrupted cooldown; no new external changes.

## Reset options researched

Official authentication rate-limiting reference https://help.sonatype.com/en/authentication-attempt-rate-limiting.html specifies default max-delay-seconds900, state held in memory per node, and restart required after nexus.properties changes. Thus restarting the Nexus process is expected to clear in-memory throttling state (inference from documented storage); it interrupts all registry/package clients. Documented workaround nexus.auth.ratelimit.enabled=false disables protection globally and also needs restart. No documented per-user reset endpoint found in official API reference. Recommendation remains uninterrupted cooldown for this single cleaner account; no restart, property edit or reset performed. Existing TODO remains unchanged; these are options, not authorized work.

## Audit log cooldown evidence

At14:15:21Moscow read-only audit scan found7135security.auth.ratelimit events in current audit.log, all type blocked. No unblock/release event found. Exact last blocked event for cleaner is13:58:27.509Moscow, from the previous credential checks; no later rate-limit events. Therefore15minutes elapsed at14:13:27.509, correcting the previous approximate14:14estimate. No cleaner authentication was attempted during this audit inspection. Absence of unblock events does not establish whether in-memory cooldown expired; a subsequent successful GET is needed. Existing verification TODO unchanged.

## User verification after uninterrupted cooldown

User requested checking the account after15minutes elapsed. Admin GET confirms cleaner active with sole nx-docker role. Using current/.env VK_PROD_NEXUS_CLEANER_USER/PASSWORD, REST search for docker-hosted returns200 with50items and continuation token; Docker connector3003 GET /v2/ returns200. Authentication throttling has cleared and supplied credentials work for both read endpoints. No deletion performed, delete authorization not exercised, no job triggered. Production Vault/runtime credential agreement, retention and successful cleaner execution remain unverified under the existing cleaner TODO.

## User-triggered successful recovery run

User launched allocation ab7c7a54-71a2-729d-1378-93214ef80bce, child nexus-cleaner/periodic-1792494996. Read-only Nomad verification: complete, task dead/failed=false, zero restarts, started14:16:38.648Moscow and finished14:16:55.032, Terminated Exit Code0. Stderr empty. Stdout logs old master image deletions and stop cleaning images at14:16:43. Nexus request-log count for14:16:38–56Moscow confirms108DELETE requests, all HTTP202 (accepted), supporting actual server acceptance rather than only client log intentions. No deletion request was initiated by the agent. No individual image absence or physical blob-space reclamation claimed. Current deployed credentials are operationally sufficient; production Vault values were not directly read and retention policy was not reviewed. Existing cleaner credential/rate-limit TODO closed after successful run; earlier failure/stop records preserved. Parent schedule remains the previously verified04:00Moscow daily schedule; no agent runtime changes in this follow-up.

## YouTrack completion comment

User requested a short task comment. Read-only YouTrack search identified dedicated DevOps-905, `[Nexus] Восстановить работу cleaner`, with no existing description/comments. After displaying the concrete text and per-command approval, POST created comment74-124719 (HTTP200); independent GET verified exact text. Comment records account/role restoration, stuck-child stop and cooldown, user-run exit0/zero restarts,108DELETE responses202 and04:00Moscow schedule. Issue state not changed. Link: https://youtrack.youdo.com/issue/DevOps-905 . Existing cleaner recovery TODO already closed; no additional follow-up created.

## User-reported task closure

On2026-10-20 the user confirmed closing DevOps-905 after the verified successful cleaner run and completion comment. Treat restoration as accepted complete. This is user-reported closure; no agent issue-state mutation or independent state GET was performed. Existing cleaner TODO is already checked. Earlier Vault-value, retention-review and blob-space verification limits remain historical boundaries, not new actions or reasons to reopen the task.
