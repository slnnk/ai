---
system: nomad-test
status: verified
checked: 2026-10-20
tags: [nomad, monolith, rabbitmq, latency, autotests]
---
# test1 monolith latency from RabbitMQ exchange mismatch

## Task and context

Inspect Nomad test1/youdo after Jenkins two/2006 took267min and identical registration/signin workloads became15–41times slower than the previous Yandex Kubernetes baseline. Follow-up to [test timing analysis](2026-10-20-web-autotests-jenkins-2006-duration-api-latency.md). Read-only runtime inspection2026-10-20 14:25–14:27UTC (17:25–17:27Moscow).

## Actions

Used Nomad GET through http://nomad.service.vk-test.consul:4646 with current/.env VK_TEST_NOMAD_TOKEN. Read job metadata, allocations, task usage and bounded logs; parsed structured events in memory and retained only sanitized diagnostic fields. No job config, credentials, user payloads or raw HTTP bodies are retained in the final diagnostic excerpts. Generated evidence: /home/slnnk/ai-data/test1-monolith-diagnosis/.

## Findings

- Job youdo-test1 running/version26/images141210. Web allocation acecb7d8-12cb-b56d-6409-63f7233222cb, svc allocation197fe7e5-cca2-7ae0-eb57-119ac175feee. App tasks running/restarts0 since09:17UTC; migration tasks completed. No current container crash loop.
- MVC application usage sample:2.46GiB against3GiB max, CPU42.55percent, reported throttled periods/time0. Current resource sample does not establish historical peak usage.
- MVC and web-api logs report AMQP406: `PRECONDITION_FAILED - inequivalent arg 'auto_delete' for exchange 'youdo.user.signin' in vhost 'test1': received 'true' but current is 'false'`.
- UserSignedInEvent publishing retries through attempt9 at roughly1second intervals, then logs final inability to publish. Existing exchange properties conflict with the publisher topology; delay is in the application's event-publish path.
- Retained early MVC log already reports this mismatch at16:45:15Moscow, inside build2006(12:37–17:04Moscow). It continues during2007. The recent5MB MVC/web-api sample includes76mismatch records; this is a bounded-log count, not unique affected requests.
- Server-side MVC logging confirms the delay: POST /api/users/signin/17:26:34.090Moscow elapsed8312ms/status200;17:26:38.647 elapsed8352ms/status200;17:26:40.600 elapsed8467ms/status200. Registration17:26:31.335 elapsed9856ms/status200 and17:26:38.348 elapsed9307ms/status200. HTTP success therefore hides event-publication failure and latency.
- svc-users separately has the same auto_delete mismatch for exchange youdo.user.signout2 in vhost test1. Other event routes also report publication retries whose inner exception references signin; do not infer those routes have independent declaration mismatches without checking RabbitMQ.
- This matches the earlier [test5 signin exchange incident](2026-10-07-rabbitmq-test5-signin-exchange-auto-delete-mismatch.md), resolved by the team in October7. Current test1 is a new incident; no inference about the creator of its exchange is supported.

## Changes

Read-only diagnosis; no restarts, deployments, RabbitMQ object changes or application requests that create data. Added KB evidence and a scoped corrective proposal in the central TODO.

## Status and risks

Confirmed test1 monolith event-publication failure explains the observed~8second signin delay and slow data setup: RabbitMQ rejects conflicting exchange declarations, and synchronous retry consumes request time. Exact fraction of all267build minutes is not reconstructed. Who created incompatible exchanges remains unknown; RabbitMQ management properties and bindings were not independently fetched. Fix proposal is in [central TODO](~/ai/TODO.md): inspect current exchanges/bindings and prepare reconciliation, preserving bindings and consumers; runtime changes require separate explicit approval. Existing user-closed historical web-autotest tasks remain closed.

## Portable lesson

none

## Deployed code and RabbitMQ change history checked2026-10-20

- Nomad versions26/25 confirm current image141210 and previous image141203. Pipeline [141210](https://gitlab.youdo.sg/youdo/youdo/-/pipelines/141210) resolves to38b4812174a6e17c34655ee2bdf979bc83790140, built2026-10-19 19:42Moscow from refs/merge-requests/10099/head. [MR10099](https://gitlab.youdo.sg/youdo/youdo/-/merge_requests/10099) is feat/Site-25699-b2b-tasks-ranking, opened, target master. This is the running backend, despite tests selecting static master.
- Jenkins2006 and2007 checkout6a9ddd55ca09d88ff3b292d28a6defbf609e6bb0 of youdo.static. Distinguish test revision from backend image revision.
- Exact deployed38b4812 source has explicit ExchangeAutoDelete=true in YouDo.Entities/Users/UserSignedInEvent.cs and UserSignedOutEvent.cs. Both files are identical to previous pipeline141203/c06afbf11383a66d276b65a9cc126e75dbae2a37 (git diff empty).
- Source-branch four-commit diff against merge base contains B2B task ranking/migration/indexing changes; no change to these exchanges or RabbitMQ connection settings. TaskVisitProcessor consumer business logic changes, but not signin/signout declaration topology.
- Relevant independent change: [MR10103](https://gitlab.youdo.sg/youdo/youdo/-/merge_requests/10103), Site-25732, commitc1c22d7c95293713ad3bdd8597ca31b041f3ed0e datedOctober13, removes explicit ExchangeAutoDelete=true for both affected exchanges. Merged as7709afb2131 at2026-10-19 16:06Moscow. Reverted byf6d81d762ddbf65f4b3d2ffdb30c43fe2a090fb6 (18:33Moscow), merged asc06afbf1138 at18:59Moscow, restoring true.
- This establishes a code-history topology compatibility hazard when persistent broker objects are shared across versions. Current feature branch predates that change, and the immediately prior deployed backend already has true. It does not prove MR10103 or its build actually created the false exchanges in test1; broker object creator remains unknown. A claim that MR10099 newly changed these flags would be incorrect.
- Local checkout /home/slnnk/git/youdo remained clean on existing task branch atabc9c7ae1a5. Exact running/prior/history commits were already available locally; read with git show/diff/log, no checkout/fetch/mutations. Pipeline and MR identities obtained through authenticated GET. Current remote master55ff066a0e1d was identified through API; its tree was not read locally (object unavailable), so source findings are scoped to exact inspected commits.

The proposed broker reconciliation in central TODO remains pending, with no runtime changes authorized or performed. Source MR names containing another system identify historical changes only; no investigation or mutation of that handed-over system was performed.

## Management access confirmed2026-10-20

Existing verify.py performed read-only RabbitMQ management GET calls using credentials loaded in memory from VK Vault secret/resources/rabbitmq. Login succeeded;17expected vhosts accessible, including test1; configure/read/write permissions all unrestricted for the existing account, no missing vhosts or permissions. RabbitMQ3.8.34 at the recorded test management endpoint. This confirms technical access only, not authorization to change broker objects. No runtime changes.
