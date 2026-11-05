---
system: nexus
status: verified
checked: 2026-11-04
tags: [usage, gitlab, cache, read-only]
---
# Nexus October 29–31: CI jobs and cache revisions

## Task

Attribute heavy Nexus requests during October 29–31, Moscow time, to CI jobs and determine whether exact job revisions contain our cache changes. Include October 28 only as necessary to explain rolling-24-hour peaks.

## Context and method

[Nexus map](../systems/nexus.md), [weekly totals](2026-11-04-nexus-weekly-limits.md). Existing local checkouts inspected read-only for fix baselines. Authenticated GETs collected 2,166 retained overlapping jobs across all ten listed runners for October 28–31, 1,174 primary traces (one transient GET failure subsequently succeeded), 61 gate traces, 119 exact CI source revisions across three projects, and MR metadata. Primary traces: 1,173 first-pass successes plus the retried Android3265982. No remote state changed.

Artifacts: `~/ai-data/nexus-usage/oct29-31/`. Key files: `runner-jobs.json`, `nexus.json`, `seconds.json`, `trace-sources.json`, `trace-gates.json`, `trace-focused.json`, `exact-sources.json`, `gate-attribution.json`. Zero Nexus parse failures. Request totals count all methods/statuses under `/repository/*`, using Moscow log timestamps. Second-resolution aggregates refine minute correlations.

Source attribution combines User-Agent versions, exact job execution intervals, trace commands and revision-specific CI files. All request IPs share a gateway; simultaneous jobs using the same client cannot always be separated. A job-window count is not independently attributable when other compatible jobs overlap. Runner inventory covers listed/retained runners; extremely old manual jobs can fall outside the created-date pagination boundary. The identified npm client groups have full temporal coverage.

## Findings

### Monolith: old branches still lack the npm patch

Twelve build/build_release jobs started October 29–31. Eight have none of the three patch markers (`npm-node8`, `npm_config_prefer_offline`, `build/cache/npm/`); four contain all three and successfully restore both NuGet and npm caches. Fix MR10113 was merged October20 as `55ff066a0e1d2bb84b878faf3f4ec65a00e00592`; this did not update previously diverged branches.

| Job | Moscow date | Source branch | Exact SHA | npm patch | npm requests in compatible window |
| --- | --- | --- | --- | --- | ---: |
| [3258956](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3258956) | 2026-10-29 | `transactional-monetization-pilot` | `bd8e91dabfa2` | no | 2,822 |
| [3258961](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3258961) | 2026-10-29 | `Site-25766-payment-block` | `8a6038afa807` | yes | shared 3,751 with 3259092 |
| [3259092](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3259092) | 2026-10-29 | `transactional-monetization-pilot` | `a2fc795257bc` | no | shared 3,751 with 3258961 |
| [3259224](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3259224) | 2026-10-29 | `transactional-monetization-pilot` | `e3ae53382c8b` | no | 2,827 |
| [3260145](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3260145) | 2026-10-29 | `transactional-monetization-pilot` | `90b60b3cd292` | no | 2,828 |
| [3261199](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3261199) | 2026-10-29 | `transactional-monetization-pilot` | `ba5fef8f23ad` | no | 2,832 |
| [3263183](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3263183) | 2026-10-30 | `feat/Site-25859-flexible-form` | `b0e61de51afd` | yes | 924 |
| [3264922](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3264922) | 2026-10-30 | `25672-inactive-hold-after-restore` | `9a9a66a6343b` | no | 2,834 |
| [3265060](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3265060) | 2026-10-30 | `transactional-monetization-pilot` | `8e64a955693b` | no | 2,821 |
| [3265588](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3265588) | 2026-10-30 | `transactional-monetization-pilot` | `4c2329db25f4` | no | 2,828 |
| [3266241](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3266241) | 2026-10-30 | `master` | `c08ccc9decd1` | yes | 924 |
| [3269299](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3269299) | 2026-10-31 | `codex/Site-25776-unified-phone-owner` | `1ce7e95537bb` | yes | 924 |

Legacy npm total: **26,315**. Seven isolated old-build windows sum19,792; three isolated patched windows sum2,772 (924each). Shared window3259092/3258961 contains3,751 requests. Pattern-based split2,827old+924patched is plausible, but cannot be claimed as exact job attribution. Patched jobs still make residual package downloads; the optimization did not promise zero traffic. Independent legacy NuGet6.5 client requests total20,087, matching monolith build windows. The npm-only change did not optimize these NuGet/Cake restores.

### Business: the internal API patch is present; npm gates are separate

All70 internal-api jobs started October29–31 use `.dotnet-build-docker-b2b-backend` in their exact CI revision. Across the expanded October28–31 inventory all80jobs/78distinct SHAs have this marker. Runtime traces show cache mounts/CACHED build layers (for example3268244); this is not a missing-branch-patch case. Fresh MR3863 GET confirms merged2026-10-20 14:25Moscow as `30ef8f2425955257dd90d22b53dd391440c99852`, superseding the prior unverified-merge limitation.

Node26/npm12 CI clients made **23,150** requests, all tarball downloads. Every one falls within the first60seconds of exactly one compatible Business gate pipeline's `step_script`, where traces run `npm ci --cache .npm --prefer-offline --no-audit`. Concurrent business/employee gates in the same pipeline remain grouped rather than receiving duplicate request counts. Some jobs were retried; table links include retries belonging to that pipeline.

During October29–31,58gate jobs executed:24failed to extract cache,34succeeded. Selected failed traces explicitly say `WARNING: file does not exist`; this demonstrates an absent archive at that key, not a proven storage/network fault. Some cache-restoring runs also downloaded packages, so extraction success alone does not prove the cache contains all required tarballs. Lock-hash/protected partitioning and archive completeness were not diagnosed. Our internal-api patch did not target these npm jobs.

| Pipeline | npm tarball requests | Gate extraction failures/jobs | Gate jobs |
| --- | ---: | ---: | --- |
| 141881 | 1,365 | 2/2 | [3260026](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3260026), [3260025](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3260025) |
| 141886 | 653 | 0/2 | [3260298](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3260298), [3260297](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3260297) |
| 141891 | 653 | 0/2 | [3260816](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3260816), [3260815](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3260815) |
| 141893 | 712 | 0/2 | [3260947](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3260947), [3260946](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3260946) |
| 141894 | 1,365 | 2/2 | [3261078](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3261078), [3261077](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3261077) |
| 141914 | 1,365 | 2/2 | [3261669](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3261669), [3261668](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3261668) |
| 141927 | 1,365 | 2/2 | [3262343](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3262343), [3262342](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3262342) |
| 141949 | 1,365 | 2/2 | [3262690](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3262690), [3262689](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3262689) |
| 141955 | 1,365 | 2/2 | [3262828](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3262828), [3262827](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3262827) |
| 141961 | 1,365 | 2/2 | [3262975](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3262975), [3262974](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3262974) |
| 142010 | 1,365 | 2/2 | [3264269](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3264269), [3264268](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3264268) |
| 142016 | 1,365 | 0/2 | [3264539](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3264539), [3264538](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3264538) |
| 142022 | 1,365 | 0/3 | [3264937](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3264937), [3265592](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3265592), [3264936](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3264936) |
| 142034 | 712 | 0/2 | [3265731](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3265731), [3265730](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3265730) |
| 142035 | 653 | 0/2 | [3265860](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3265860), [3265859](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3265859) |
| 142043 | 1,365 | 2/2 | [3266300](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3266300), [3266299](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3266299) |
| 142044 | 1,365 | 2/2 | [3266432](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3266432), [3266431](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3266431) |
| 142065 | 653 | 0/1 | [3267669](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3267669) |
| 142080 | 1,367 | 2/2 | [3268560](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3268560), [3268559](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3268559) |
| 142082 | 1,367 | 2/2 | [3268700](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3268700), [3268699](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3268699) |

Business Docker image paths account for37,393of47,258Docker requests across the three days. Largest paths: worker4,410; business-api4,348; business-internal-api4,318; migrations4,168. These identify image owners, not necessarily the individual process consuming them. Backend NuGet mounts do not eliminate Docker registry requests.

### Frontend-tools: cache is present and effective in this interval

All24 prepare-npm jobs started October29–31 include the single-writer `npm-node24` patch and successfully extract cache. All27expanded-window source revisions contain `prepare-npm`, `npm-node24` and `resource_group: npm-node24-cache`. MR183 was mergedOctober22 as `b1f0670ddf8b9b9fb0eef7020a8e570db94bd40e`. Matching Node24/npm11.6.2 CI traffic across October29–31 is only119requests (63/35/21 by day), rather than thousands. No missing-cache-extraction evidence in the frontend-tools traces.

### Android and the rolling peak

Gradle8.13 traffic across October29–31 totals9,167: feature3258950=2,531, browserstack3258951=473; feature3265981=2,596, browserstack3265982=485; feature3266281=2,597, browserstack3266282=485. All counts match non-overlapping compatible execution windows. Android cache implementation remained a proposal, not one of our applied patches. Gradle8.7 has3,352additional requests not attributable to listed CI jobs.

The October29 14:58:43 rolling peak105,806 includes Android Gradle8.13 requests23,878 from the preceding24hours, including October28afternoon/evening jobs; attributing the whole peak to October29jobs alone would be wrong. Peak breakdown: NuGet37,993, Maven-public24,700, npm23,386, Docker18,900, others827. October31 01:12:02 peak99,645 includes workload31,711, legacy npm10,331, Node26npm11,577 and Gradle8.13 6,163; peaks are not calendar-day totals.

### Remaining workload traffic

There are54,821workload manifest requests across October29–31 (20,649/29,435/4,737 by day), of which50,700use SDK8/NuGet6.11 and4,121other clients. Business SDK8 `dotnet-unit-tests` and backend builds are major overlapping candidates; unit-test traces restore `nuget` successfully and run dotnet restore, but background workload calls are separate from the optimized ordinary package cache. Shared gateway/parallel identical clients prevent exact assignment of all workload requests to individual jobs or exclusively to Business. Global disabling of workload advertising remains proposed in DevOps-904; it was not part of the three applied cache patches.

## Changes

Read-only infrastructure/GitLab investigation; local scripts/evidence and KB update only. No application checkout edits, external writes, CI retries, publication or deployment.

## Status and risks

Investigation complete; no task commands or agents remain running at final verification. Existing DevOps-904 backlog remains open and retains implementation approval requirements. Its measurement and Business merge status are updated; no whole-item completion inferred. Missing monolith patches, npm-gate misses and remaining workload traffic are observations under that existing task, not authorization to modify branches or CI. Exact attribution limitations above remain.

## Follow-up planning record (2026-11-04)

The user requested adding an optimization plan to TODO. The existing DevOps-904 entry in `~/ai/TODO.md` now contains six ordered phases, based on this investigation: workload advertising, existing monolith npm patch propagation, Business gate-cache diagnosis, proposed Android Gradle reuse, conditional residual-source reassessment, and seven-day rolling-limit validation. Existing completed cache work and deferred monolith NuGet scope remain distinguished. Only local backlog/documentation changed; no implementation, branch update or external operation was authorized or executed by this planning request. The live plan remains exclusively in central TODO.

## Portable lesson

none
