---
system: nexus
status: verified
checked: 2026-10-12
tags: [nexus, nuget, recovery, gitlab]
---
# NuGet library recovery after Coworking and RabbitHole

## Summary

User requested continuing publication recovery through the master dependency inventory. Retry existing historical publish jobs first; investigate actual failures afterward. Verify only Nexus version metadata, without downloading published packages. All 143 required package/version pairs across 52 package IDs are now present in final public Nexus metadata (allHTTP200). Service restore and exhaustive transitive checks remain deferred by the user. Latest machine-readable inventory is under `~/ai-data/nexus-recovery/nuget-inventory/`.

## Context and authorization

The original inventory contains 143 required package/version pairs across 52 libraries. Six RabbitHole/Coworking pairs were already restored. The user explicitly authorized publication of ten prepared fallback packages, cancellation of four unserviceable pending jobs, two additional Fluent1.8.1 packages, and a subsequent eight-package Chronos/Contracts/CQRS/Microservices batch. These approvals cover those exact artifacts only. Historical publication retries are within the user's request; new pipelines, role changes, unrelated cancellations or fallback uploads still require explicit approval.

## Actions and evidence

- Audited exact historical source SHA, package identity and CI version rules. Remaining queue has 62 candidate jobs covering125 required pairs; `remaining-job-targets.json` and `remaining-job-evidence.json` hold evidence. Auth job selection corrected: `prepare-nuget` only prepares environment; actual publication is `build-libs`. Retried exact-version jobs2448220 and3165482 as3219465/3219466; NBGV versions verified on their selected SHAs.
- DocXToPdfConverter1.1.0-youdo job3219134 and FluentMigratorCore.Consolisator1.9.1 job3219133 succeeded; public metadata confirms both.
- Published the approved ten-package fallback batch using `publish_library_batch.py --manifest fallback-publication-batch.json --publish`: FluentMigratorCore.Consolisator0.3.11/1.1.0/1.7.0, required Core/Runner/Extensions0.3.11 dependencies, Kaiena1.0.8, Serilog.Sinks.Exceptional1.0.2/1.0.4, YouDo.Serilog.Sinks.Exceptional1.0.5. Every push returned Created and public metadata presence was verified.
- Canceled approved jobs3219129,3219130,3219131,3219136; API confirmed canceled.
- Published separately approved FluentMigratorCore.Consolisator1.8.1 and FluentMigratorCore.Extensions1.8.1 after actual BaGet publish timeout. Public metadata confirms both. All requested Fluent versions are now present.
- Second approved fallback batch manifest `fallback-publication-batch-2.json`: all eight Chronos/Configuration/Contracts/CQRS/Microservices packages published with Created and public metadata presence confirmed.
- Separately approved and published ten Extensions packages from exact tags1.8.1/1.9.2, including necessary Net1.9.2 and MessageBus1.8.1 dependencies; `fluent/extensions-ready-manifest.json`, all metadata verified.
- Separately approved and published23 ServiceCore packages: Application0.3.1; Application/Configuration0.4.1; Common/Configuration/DistributedLock/Metrics/RabbitMq/Testing/Tracing/Validation1.0.14 and1.0.15; Common/DistributedLock/Testing/Validation1.0.16. Historical sources unchanged, net6.0 SDK6 / net8.0 SDK8 preserved. All public metadata verified. Eight remaining ServiceCore pairs originally failed when public NuGet substituted2.0.0 for private Serilog.Enrichers.Sensitive1.8.0. Exact fork project549/tag1.8.0 was rebuilt with native historical version flags, then used through a credential-free local feed. All eight previously failing ServiceCore packages now build unchanged; separately approved final nine-package publication completed and public metadata confirmed. A batch interruption was resumed safely; already-present versions were metadata-verified and skipped. All requested ServiceCore pairs are now present.
- Private Serilog.Enrichers.Sensitive1.8.0 provenance confirmed: project549 exacttag1.8.0 SHA bf6f9a0083f1a6dbe705a00c9c57b073b0af4e73 contains expected MaskPropertyCollection. Historical publication2254599 retried as3219469; queued with eligible Docker runners. This is an actual missing dependency from ServiceCore errors, not an upstream API shim.
- Separately approved nine-package Caching/Data/Disposables/Push batch uses historical build configuration and version flags (Caching assembly2.2.2.0 retained for package2.2.4). Manifest `pending-plus-push-ready-manifest.json`; includes necessary Data.Common2.5.4. All nine pushes returned Created; public metadata confirmed.
- Separately approved and published eight-package batch3: Chronos.Configuration.Extensions1.0.0, four requested Extensions1.9.1 packages plus Hosting/Net1.9.1 dependencies, Mailer1.0.3. All public metadata confirmed. Mailer needed already restored RabbitHole/Contracts/Common dependencies; source unchanged.
- Separately approved TextValidation.Contracts0.0.8 fallback published after CI BaGet timeout; public metadata confirmed, exact Kaiena1.0.8 dependency retained.
- Local builds of remaining queued/slow-restore versions were prepared concurrently after long CI resource delay to prioritize recovery. This does not authorize new external uploads; exact artifact batches still require explicit consent and existing Nexus versions are skipped on verified metadata.
- Auth0.0.31 Shared/Client/Lib separately approved, published and metadata-verified from exactSHA499ecbc0 with native assembly0.0.10.0 preserved. Auth0.0.37 Client/Lib already appeared through CI and local builds were skipped.
- Final32 separately approved historical packages published: remaining Microservices/Common/Core/Hosting (including deletedtag4.0.1 proof), Caching2.4.2, old Extensions versions and Mailer prerelease. `final-32-publication-batch.json` is the reviewed manifest; every version metadata-verified. Additional Common3.0.7 is a direct prerequisite. Mailer preserves declaredContract>=1.9.3; restore selectedavailable1.9.4, warning explicitly disclosed beforeapproval.
- Final full check `inventory-metadata-final.json` confirms143of143requiredpairs across 52packageIDs, allmetadataHTTP200. No packages downloaded for presence verification. Restoration CSVs/summary updated and central backlog separated into completed publication and deferred service restore/transitive work.
- User separately approved final cancellation of 26 own retry jobs after all required versions were restored. `cancellation-plan-reviewed.json` freezes exact project/job IDs; API cancel applied only to still-active own retries. Fresh GET verification `cancellation-final-status.json` confirms all 26 canceled and no pending/running/canceling states. Original/unrelated jobs were excluded.
- Existing checked source snapshots and rebuilt artifacts reside only under `~/ai-data/nexus-recovery/`; credentials remain runtime-only, never in manifests/config files. Generic upload uses existing `nuget` identity and Basic authentication; symbol archives are not uploaded.

## Findings and limits

Legacy jobs fail on removed `microsoft/dotnet:2.1-sdk` / `2.2-sdk` images, unavailable runner tags, stale BaGet sources, or missing NexusPrivate source name. CQRS project448 is archived and rejects retry with403; no unarchive performed. Extensions1.8.1 encountered public dependency HTTP429 through Nexus. ServiceCore newer jobs also contain a concrete Logging compiler failure; exact errors are being investigated.

Rebuilds preserve historical source and target frameworks, including net47 where present, but use SDK6 when obsolete SDK images cannot run. No repository code, refs, tags or CI variables were changed. Presence verification does not claim service restore/build success or complete transitive coverage. Hosting4.0.1 provenance found in successful historical pipeline124885 (deleted ref4.0.1-extensions), exactSHAf175055b582daa5478c497c5f61e8eee1c7797db; job2588689 retried as3219470. No tag created.

## Changed files

Local recovery helpers and manifests under `~/ai-data/nexus-recovery/`; restoration CSV/summary; this log; existing Nexus system map and central TODO. No task edits in repository checkouts.

## Risks

Temporary Nexus anonymous access remains enabled by user request. Legacy CI sources/runner tags remain unchanged; package recovery does not repair them. Follow-up work is tracked only in `~/ai/TODO.md`.

## Portable lesson

none
