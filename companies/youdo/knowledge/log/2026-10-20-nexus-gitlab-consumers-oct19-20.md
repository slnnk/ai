---
system: nexus
status: verified
checked: 2026-10-20
tags: [nexus, gitlab, usage, cache, DevOps-904]
---
# Nexus consumers: GitLab comparison for October 19 and 20

## Task

User requested a comparative read-only analysis of Nexus traffic and GitLab jobs for October19and20 under DevOps-904. October20is incomplete, so compare completed00:00–13:00MSK windows for both days and report October19full-day separately. No infrastructure, repository, tracker or CI execution changes authorized/performed.

## Context

[Initial request-limit analysis](2026-10-20-nexus-ce-request-limit-analysis.md), [Nexus map](../systems/nexus.md). Existing Nexus/GitLab credentials remain only in current/.env. Aggregates/scripts in `~/ai-data/nexus-usage/oct19-20/`. SSH existing MSS relay reused; remote script supplied on stdin reads request logs only. Network commands used approved sandbox escalation. Sync returned no reminders.

## Actions and coverage

- Aggregated `/repository/*` Nexus requests by minute, repository, client family and request kind; zero unmatched log lines. Excluded search/UI/admin APIs from counted traffic.
- Enumerated all10restored runners and their job history, 1,008jobs overlapping Oct19 00:00 through Oct20 13:00MSK, across31projects. Included failed/retried jobs as separate executions. Time comparison uses started-at timestamps, not job creation or pipeline date.
- Cross-checked an active-project inventory (683jobs/20projects). This alone missed schedule/retry activity in13other projects; one private project returned403. Complete runner enumeration supplied the final execution inventory without errors. Never use last project activity as the sole CI census.
- Streamed42representative CI traces (~50.6MB) and20targeted traces (~12.2MB) covering all internal-api executions and current DevOps-904 build attempts. No raw traces saved; persisted only counters and sanitized version/cache evidence. None truncated or unavailable.
- Compared Nexus per-minute User-Agent families to job intervals. Shared gateway IP and anonymous clients prevent direct authenticated per-project attribution; temporal overlaps are evidence of association, not a unique client identity. HTTP GET lines in traces independently confirm specific job request counts.

## Comparable periods

| Metric | Oct19 00:00–13:00 MSK | Oct20 00:00–13:00 MSK |
| --- | ---: | ---: |
| Nexus requests | 53,048 | 15,303 |
| NuGet | 21,562 | 7,018 |
| npm | 28,319 | 2,843 |
| Docker + hosted | 3,048 | 4,049 |
| Maven | 119 | 1,393 |
| Started GitLab jobs | 196 | 174 |
| Monolith build/build_release attempts | 10 | 2 |
| Business all jobs | 26 | 34 |
| Static prepare-npm jobs | 7 | 2 |

Full October19:146,536requests and834startedjobs. October20only174jobs started before13:00, so 1,008executions total. Business SDK8 requests rose from3,464to4,556in the comparable window despite lower overall requests. Overall job count is not a proxy for Nexus consumption; job type and cache behavior matter.

## Main consumer: monolith youdo

October19had19build/release jobs (15build,4build_release). Every one of53,757legacy npm requests and32,114NuGetCLI6.5requests lies within their execution intervals:85,871requests,58.6%of all Nexus traffic that day. Seventeen isolated npm bursts each contain2,820–2,854requests, about2,829perbuild overall. Legacy NuGet averages1,690perbuild. Existing Cake NoCache setting explains why NuGet HTTP traffic persists despite restored nuget-packages cache.

Trace corroboration:

- [3232849](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3232849),07:35–07:47MSK:1,605Nexus GET/OK pairs; same job interval contains2,854legacy npm requests.
- [3236355](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3236355),22:59–23:11MSK:1,685Nexus GET/OK pairs and2,828legacy npm requests.

These are much stronger than an attribution from Node version alone, but total monolith share remains a temporal/User-Agent inference because Nexus lacks original source identity.

## Confirmed NuGet cache exception: business-internal-api

Correction to the earlier general statement that Business caches NuGet: its own `devops/Dockerfile` and `devops/Dockerfile.backend` have BuildKit cache mounts, but `build-business-internal-api` extends shared `.dotnet-build-docker`, not `.dotnet-build-docker-b2b-backend`.

At exact job3233025revision `6c192959135c9fb08a9c067bd23d7421639b8567`, `.gitlab-ci.yml` confirms this inheritance and `.dockerignore` excludes `nuget-packages/`. The shared template starts DinD and uses `v3/files/dotnet.Dockerfile`, which copies the build context and restores to `$NUGET_CACHE` without cache mounts. GitLab restores the directory outside the Docker build, but .dockerignore prevents copying it in. No source fix performed.

All16internal-api traces for October19were inspected:15executed1,377–1,427Nexus GETs each; one had none. Total **21,073GET requests**,28.8%of that day's NuGet traffic. Every trace reported successful GitLab cache extraction, proving that extraction alone does not prove Docker-side cache reuse. Examples: [3233025](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3233025)1,412GETs; [3235977](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3235977)1,403GETs. Today's two internal-api executions made1,385and1,416GETs,2,801total.

Monolith-associated85,871plus independently counted internal-api21,073requests account for106,944or73.0%of October19traffic. They are disjoint client families; this excludes background workload traffic not represented by those trace GETs.

Proposed next implementation candidate: migrate this one job to the established cache-enabled backend path after checking build arguments/paths and runtime equivalence. Repository/publication approvals are still required.

## Other consumers and workload traffic

October19NuGet SDK8 family:35,861requests. Of these31,291occur while Business is the only active project among selected .NET build/test candidates. Within that project several jobs run concurrently: do not attribute all requests to unit tests. Five isolated Business test jobs produce only65SDK8requests each, all workload requests; their regular package caches look effective. Internal-api Docker traces provide the concrete bulk-download evidence.

Other isolated SDK8 candidate-project windows: tickets1,876requests, giveaway-bot1,329; overlapping Business+tickets856and tickets+loopplugin509remain ambiguous. These are candidates, not exact per-project totals.

Workload manifests and related packages generated15,764requests on October19. This is a request-kind dimension overlapping client/project counts above; never add it to those totals. Advertising refresh remains a separate proposed optimization, with explicit workload operations distinguished before implementation.

Static ran19prepare-npm jobs on October19. Its sampled jobs3232875and3236514successfully extracted npm cache and used prefer-offline. Only41of53,798npm requests that day came from clients outside the legacy monolith User-Agent family, consistent with effective Static/Business npm caches. The41requests are an upper bound shared by all other clients, not a unique Static count.

Docker contributed17,464requests on October19. Numerous deployment jobs, including migration-image pulls across test stands, explain why jobs with no dependency restore still generate registry traffic. These pulls are a secondary contributor and are not classified as waste without a separate assessment.

## DevOps-904 warm-cache verification limit

October20MR10113pipeline141244 build3236889failed on runner105 before dependency requests; automatic retry3236896succeeded on runner106at12:56:31MSK. The retry logged npm cache miss,1,644Nexus NuGet GETs and a matching2,835legacy npm requests. It was the first successful cache-fill build. No second successful warm-cache build existed before13:00, so the current lower total cannot be claimed as DevOps-904savings. No pipeline retry/play, merge or deployment was initiated by this analysis.

## Changes and status

Read-only comparison complete. Scripts and derived artifacts: `nexus_remote.py`, `collect_jobs.py`, `collect_runners.py`, `scan_traces.py`, `correlate.py`, `nexus-through13.json`, `runner-jobs.json`, `trace-evidence.json`, `trace-internal-api-and-devops904.json`, `internal-api-source-evidence.json`, `comparison-final.json`. Shared template source read from current master; exact historical clone SHA is unavailable, but executed restore behavior is independently visible in traces. Updated Nexus map and task-related TODO only. No external writes. Remaining implementation and warm-cache verification stay in central TODO; analysis does not authorize changes.

## Portable lesson

none

## User-approved YouTrack analysis comment published (2026-10-20)

User requested a new project-analysis comment and explicitly approved the prepared Markdown text with `Да`. Pre-write GET found no existing exact comment. Created DevOps-904 comment `74-124716`, then independently GET-verified all 3,676 characters against the approved payload. Includes matched-window totals, monolith attribution, confirmed Business internal-api cache gap, Static cache evidence and remaining verification/implementation scope. Local payload/Markdown/receipt: `~/ai-data/gitlab-workflow/DevOps-904/youdo/youtrack-analysis-comment*`. Only this comment was created; issue description/state and repository/infrastructure settings were unchanged. Central DevOps-904 remediation backlog remains open.

## Pipeline and initial cache-fill verification (2026-10-20)

User asked whether build needs retry. Read-only GitLab GET confirms pipeline141244SUCCESS, including build3236896, test3236894, build_docker3236890andpublish3236891. Initial build/test failures were superseded by successful automatic retries. Build3236896missed `npm-node8-3-non_protected` at startup, then archived11,924matching files/directories under build/cache/npm/ and uploaded the cache to runner object storage. This proves cold-cache population/upload, not warm-cache reuse. A further build retry is useful for measuring reuse and traffic reduction, not required to recover the already successful pipeline. No retry initiated; explicit execution approval remains required.

## Warm npm-cache measurement completed (2026-10-20 after 13:00 MSK)

User reported the retry completed. Read-only GET verifies [build3236903](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3236903) SUCCESS,13:14:12–13:24:19MSK,runner105. Both NuGet and npm cache extraction succeeded. The cold build3236896ran on runner106; reuse therefore works across those two runners through shared object storage. No other monolith build/release overlapped the warm measurement window.

Nexus log aggregation over each job interval confirms:

| Metric | Cold build3236896 | Warm build3236903 |
| --- | ---: | ---: |
| Legacy npm requests | 2,835 | 924 |
| npm tarball requests | 1,502 | 922 |
| npm metadata requests | 1,331 | 0 |
| npm audit requests | 2 | 2 |
| Legacy NuGet requests | 1,644 | 1,683 |
| GitLab job duration | 795.18s | 607.51s |

npm traffic fell67.4%(1,911requests), with metadata traffic eliminated. The922tarball requests remain a separate diagnostic opportunity; do not claim full cache coverage. NuGet is unchanged in scale, as expected for npm-only scope. Build elapsed time decreased187.67s(13m15s→10m08s); different runners and other workload variation prevent attributing the entire speedup solely to cache. One warm/cold pair confirms this observed saving, not a guaranteed rate for all builds.

Artifacts: `warm-build.json`, `warm_nexus_remote.py`, `warm-nexus.json` in the comparison data directory. No retry or infrastructure mutation initiated by the agent; user initiated the successful retry. This supersedes the earlier warm-cache-unverified status. GitLab/Nexus GETs and SSH log reads only; no YouTrack update. Existing DevOps-904 TODO still covers remaining NuGet/cache sources and sustained busy-day measurement.

## Remaining npm requests classified (2026-10-20)

User asked what the924remaining npm requests were. Warm window has922tarball requests across505unique URLs plus2automatic `/repository/npm/-/npm/v1/security/audits/quick` requests. Every URL also appeared in the cold build; no new dependency URLs. Examples: extend-shallow2.0.1requested12times, has-flag3.0.0anddefine-property0.2.5each10times, object-assign4.1.1seven times. npm logs contain no cache permission or integrity warnings.

Joined package/version URLs with both monolith lockfileVersion1files at the inspected checkout: cold tarballs562SHA512-only,905SHA1-only,35versions represented with both algorithms across entries. Warm tarballs905SHA1-only and17dual-represented; zeroSHA512-only. All warm package versions therefore have SHA1integrity entries. This is a strong correlation with legacy npm6.13.4/cacache hash lookup behavior, not proof that SHA1itself prevents caching. The exact cache-index/read/write mechanism remains unverified. Read-only searches of known runner cache locations did not locate npm-node8 archive; no extraction, downloads or cache mutations were performed. Do not claim index inspection occurred.

Primary references checked: [npm6 configuration](https://docs.npmjs.com/cli/v6/using-npm/config/) states prefer-offline skips freshness checks but still fetches missing data; [cacache](https://github.com/npm/cacache) supports multiple digest types, so SHA1 alone is not an inherent unsupported format. Next diagnostic candidate is comparing lock integrity to preserved cache content/index with the exact old npm version. Optional audit suppression is only two requests and should not replace normal vulnerability checking without a separate decision. No repository, cache or tracker change performed. Evidence: `npm-residual-analysis.json`, `npm-residual-trace-evidence.json` and earlier per-path aggregates in comparison artifact directory.

## Merge readiness and user deferral (2026-10-20)

User said monolith/npm work is enough for now and asked whether they may merge. Treat additional monolith and residual npm work as deferred for this task; do not resume on initiative. Read-only live MR10113GET confirms opened/ready, mergeable, no conflicts, blocking discussions resolved, exact reviewed SHAabc9c7ae1a5cc65509065be344abf20cb74a6810. Pipeline141244SUCCESS; current build3236903,test3236894,build_docker3236890,publish3236891allSUCCESS. Remote diff is still the approved single-file npm cache/prefer-offline change. GitLab diffs endpoint returned500; fallback changes endpoint verified the complete diff with overflow=false. Recommended user merge; no merge action taken. Previously measured npm reduction67.4%supports the accepted change. Task remains open for other Nexus sources, notably Business internal-api; deferred monolith/npm investigations remain explicit in central TODO.

## User merge and release timing (2026-10-20)

User reported MR10113merged and release date unknown; requested a brief task comment about monolith and measured effect. Read-only GitLab GET verifies merged at13:34:41MSK, merge commit55ff066a0e1d2bb84b878faf3f4ec65a00e00592. Prepared a short Markdown comment covering npm2,835→924(-67.4%),metadata1,331→0,cross-runner reuse,CI success,unchanged NuGet and unknown release date. Payload `~/ai-data/gitlab-workflow/DevOps-904/youdo/youtrack-monolith-result-comment.json`; external comment publication approval pending. No release/deployment or further monolith/npm investigation initiated.

User correction to the prepared monolith-result comment: omit the paragraph about unknown release date, unmeasured daily effect and deferred further work. Removed it from the comment payload; retain those operational facts in task records, not in this requested brief comment. Publication approval still pending.

## Brief monolith-result comment published (2026-10-20)

User approved the corrected two-paragraph comment with `Да`. Created DevOps-904 comment `74-124717`; independent GET exactly matches all387characters. Text records MR10113merged, npm2,835→924(-67.4%),metadata1,331→0,cross-runner cache reuse,CI success and substantially unchanged NuGet. Omitted release timing/daily-effect/deferral paragraph as requested. Only this comment was created; no issue state, repository or infrastructure changes. Receipt: `~/ai-data/gitlab-workflow/DevOps-904/youdo/youtrack-monolith-result-comment-receipt.json`. Earlier publication-pending status is superseded. Central TODO retains other Nexus sources and the user's monolith/npm deferral.

## Business internal-api implementation plan clarified (2026-10-20)

User asked for the concrete service change plan, not implementation. Live master4cb0ec79e42e8c44d691c88c0b49c4aadc1e556d confirms internal-api still extends `.dotnet-build-docker`; API/worker siblings use `.dotnet-build-docker-b2b-backend`. Proposed repository patch is one extends-line in `.gitlab-ci.yml`, reusing the existing backend template and Dockerfile. It switches internal-api from DinD/dind runners to host Docker on b2b runners, adds existing global-package/HTTP-cache mounts, removes ineffective GitLab archive restore for this job, and preserves existing service/project/DLL/.NET8arguments. Plan validation: merged CI/lint, effective job vars/needs/rules/entrypoint check, image build, then cold/warm internal-api request comparison against ~1,400GET baseline on the same runner host. Publication pipeline/deployment triggers must be inspected before approval. No branch proposal approval or repository changes performed; other service and monolith scope unchanged.

## Business internal-api first approval proposal (2026-10-20)

User requested implementation of the described single-line internal-api cache change. Read-only preflight: existing `/home/slnnk/git/youdo.business` checkout is clean on `DevOps-872-worker-kill-timeout`, HEADd0f2a40cd4abce7fb87f244fae1003cb653fcca1. Live master remains4cb0ec79e42e8c44d691c88c0b49c4aadc1e556d. Proposed branch `DevOps-904-cache-business-internal-api-nuget` does not exist remotely (404); no open matching task MR. Proposal: existing checkout, fresh `origin/master` base at verified4cb0ec79, new branch above, only internal-api extends-line in `.gitlab-ci.yml`. First supervised branch/base confirmation pending; no branch switch or repository edit performed. No repo-root instructions found; nested SPA instructions do not apply to root CI edit. CI effect inspection, validation and separate publication approval follow after this gate.

## Business internal-api local patch and second approval proposal (2026-10-20)

First supervised approval received: user replied `Да` to repo/branch/base proposal. Fetched origin, verified base4cb0ec79e42e8c44d691c88c0b49c4aadc1e556d, created `DevOps-904-cache-business-internal-api-nuget` in the clean existing checkout. Changed only `.gitlab-ci.yml`: internal-api extends shared `.dotnet-build-docker-b2b-backend` instead of `.dotnet-build-docker` (1insertion/1deletion). No other repository files changed, no staging or commit.

Checks: diff whitespace check passed; GitLab CI Lint valid=true, errors/warnings empty; full merged-YAML comparison verifies preserved service/project/DLL/build-command and rules/dependencies/needs/stage, target b2b runner, no DinD service or ineffective GitLab cache, expected backend Dockerfile and its package/HTTP cache mounts. Runtime final stage matches existing shared template. Initial runtime-base equality check identified a real pre-existing difference: backend Dockerfile lacks the shared template UID1000collision fallback to1001. Documented this difference and verified no other normalized base-stage difference; neighboring .NET8API/worker jobs already use this backend. No Dockerfile modification proposed; full internal-api image build remains to be verified by CI. A diagnostic assertion had a string-escaping typo during refinement, corrected and locally verified before final effective-CI check passed.

Publication proposal: commit `cache nuget packages for business internal api`; ready MR `DevOps-904 Cache NuGet packages for business internal API`; source `DevOps-904-cache-business-internal-api-nuget`, target `master`. Russian body and exact actual diff/check report/proposal/snapshot saved under `~/ai-data/gitlab-workflow/DevOps-904/youdo.business/`. Snapshot succeeded and grants no permission. Second publication confirmation pending.

CI effects from resolved current includes: MR runs existing build/test jobs and project-registry image pushes (all service build jobs), including frontend gates due CI-file change. Dev/test deploy and autotests remain manual; production, release and monitoring rules require master/tag context and do not run for this MR. A later merge into master can automatically deploy production because DEPLOY_PROD_MODE=auto; no merge/deployment/manual-job approval is granted here. After publication, assess image-build outcome and separately approve any extra warm-cache retry needed. Runtime traffic reduction is still unmeasured for this patch.

## Business internal-api publication completed (2026-10-20)

User explicitly approved the exact second-stage publication proposal with `Да`, including MR build/test/image-push effects. Snapshot check matched before staging; staged only `.gitlab-ci.yml`, inspected entire staged diff, committed `36ec7c61d46737c7ef1a34384c29ee6b2cc20f8b` with message `cache nuget packages for business internal api`. Exact commit diff equals approved saved patch; checkout clean. Pushed only approved source branch without force.

Created ready [MR !3863](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/merge_requests/3863), title `DevOps-904 Cache NuGet packages for business internal API`, source `DevOps-904-cache-business-internal-api-nuget`, target `master`. Assignee `a.solonenko`, squash true and source removal on merge true per project defaults. Creation helper and independent verify both confirmed exact SHA/body/title/source/target. [Pipeline141254](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/pipelines/141254) status created at final verification. This supersedes the publication-pending status; image build/cache effect remain unverified. No merge, production deployment, manual job or YouTrack write performed. Existing note about automatic production effects of a future master merge remains applicable. Receipt in the proposal directory `publication-result.json`.

## Business internal-api two user-run builds verified (2026-10-20)

User reported running the pipeline job twice. Read-only GitLab verification confirms first job3237183SUCCESS at13:54:27–13:56:32MSK,125.70s, and repeat3237312SUCCESS at14:01:12–14:01:36MSK,24.59s. Both used runner123, host172.28.0.172. First executed restore for34projects and successfully built/published the image. Repeat reused all restore/publish layers (BuildKit CACHED), reducing elapsed time80.4%(5.1times faster). This confirms complete Docker-layer reuse for identical inputs; it does not yet isolate NuGet cache-mount reuse when changed code invalidates a layer.

Nexus request-log windows rounded outward to seconds: first13:54:27–13:56:33 contained377NuGet requests (325metadata,52packages); repeat14:01:12–14:01:37 contained zero NuGet requests, only50Docker repository requests. Several other Business service builds overlapped the first window, so377is an aggregate upper bound, not internal-api attribution. Full128-job pipeline pagination confirms overlaps; initial first-page-only result was incomplete and superseded. Pipeline overall remains running (unit tests/web gates ongoing at observation), so do not claim full pipeline success or merge readiness yet. No retries, merge, deployment or YouTrack write initiated.

Artifacts: `~/ai-data/gitlab-workflow/DevOps-904/youdo.business/pipeline-141254-builds.json`, `pipeline-141254-overlap.json`; `~/ai-data/nexus-usage/oct19-20/business_warm_remote.py`, `business-warm-nexus.json`. Image-build and identical-input cache verification supersede earlier unverified status. Central DevOps-904 backlog retains changed-input restore/cache-mount validation and sustained daily measurement with applicable permissions; monolith/npm remain deferred.

## Brief Business-result comment published (2026-10-20)

User requested a brief task comment analogous to the monolith result and explicitly approved the displayed two-paragraph text with `Да`. Published DevOps-904 comment74-124718; independent GET exactly verifies all575characters. Comment covers prepared MR3863, existing backend cache template, two successful builds,126→25seconds(-80%), cached restore/publish, zeroNuGet requests during repeat versus historical~1,400requests per job, and changed-code cache verification still outstanding. No claim that MR is merged or full pipeline succeeded. Only this comment created; no merge, retry, deployment or issue-state change. Exact approved payload and verified receipt: `~/ai-data/gitlab-workflow/DevOps-904/youdo.business/youtrack-business-result-comment*.json`. Central DevOps-904 backlog remains open and consistent with the preceding build-verification record.

## Tickets and Giveaway NuGet investigation completed (2026-10-20)

User requested investigation of remaining NuGet consumers (plan item3), not implementation. Applied gitlab-workflow read-only stage; delegated source inspection under the KB economical-tool rule. No repository changes, retries, merges, deployments or tracker writes. Existing Tickets untracked `devops/dev.yml` preserved.

Combined existing and28new trace summaries:32Tickets jobs (all25image builds,5prepare jobs,2sampled tests) and12Giveaway jobs (all8image builds,2prepare,2tests) successfully extracted the NuGet cache:44/44, no observed extraction failures. Trace verbose GET counts were12and2respectively, but quiet subprocess network traffic is not represented in those counts. Generic CI stores `./nuget-packages` via project-key `nuget`; prepare pulls/pushes, consumers pull. Unlike Business internal-api, neither root Docker context excludes this directory; ordinary builds copy it into /build. Package caching is present and effective for initial restores, not absent.

Concrete repeated network bursts align with additional EF builds in custom migration images. Both Dockerfiles explicitly restore with `--packages $NUGET_CACHE`, build with `--no-restore`, then run `dotnet ef migrations script` without `--no-build`. Traces show initial restore/build succeeds and then a separate `Build started...`/`Build succeeded.`. Exact EF-phase timestamps reconstructed from SDK UTC clock + BuildKit offsets; Nexus windows widened2seconds for timestamp resolution. Tickets jobs3233192,3233260,3233423,3233994,3234081each have99ordinary package GETs +64metadata requests during that phase. Giveaway3235925,3236109each have232packages +139metadata. Package names repeat across corresponding jobs. Total959package +598metadata requests =1,557, excluding workload. Because Nexus clients share a gateway and SDK User-Agent, attribution is temporal/source corroboration, not a unique per-client identifier; fixed repeated counts across all seven jobs provide strong evidence.

Primary source [EF9.0.11 Project.Build](https://raw.githubusercontent.com/dotnet/efcore/v9.0.11/src/dotnet-ef/Project.cs) invokes `dotnet build` without `--no-restore`; [CLI documentation](https://learn.microsoft.com/ef/core/miscellaneous/cli/dotnet) confirms `--no-build` skips building. NUGET_CACHE is an ordinary build ARG passed only to explicit restore; inspected service Dockerfiles do not set NUGET_PACKAGES/RestorePackagesPath for subsequent EF build. A package-path mismatch on the implicit restore is the strongly supported mechanism; exact runtime package-directory writes were not inspected. Re-installation of dotnet-ef occurs earlier in each trace, so do not attribute the99/232late package bursts to tool installation.

Historical source validation: Tickets pipeline141125SHAe16e010e /141157SHAf922ca03 and Giveaway141205SHA48820278 /141209SHAb57ebf85 migrations.Dockerfile all exactly match local inspected content. Tickets root CI also matches; Giveaway historical CI differs from local (historical4image jobs including maxbot versus local3), so counts use executed job inventory. Shared include exact historical SHA remains unavailable; observed traces independently verify cache extraction and commands. Local source revisions recorded by the source subagent: TicketsHEAD4eb06056, GiveawayHEADb367fd3a, templatesHEAD126620d7, with relevant CI/Dockerfile content unchanged against locally cached origin/master.

Refined exact-second candidate-project coverage replaces earlier minute-based1,876Tickets estimate: isolated among selected SDK8candidate projects, Tickets2,160requests (1,495workload,396ordinary packages,269metadata); Giveaway1,329(585workload,465ordinary packages,279metadata). Shared Tickets+Business687, Tickets+Loopplugin225, Giveaway+Business65remain ambiguous. These are isolated candidate windows, not exact daily project totals. Initial isolated numbers varied because minute boundaries included overlapping candidates; do not compare them as a traffic trend. Workload overlaps project totals and remains separate optimization scope. Tickets Web floating8.* version explains observed repeated version metadata lookup, not all traffic; HTTP metadata cache is not persisted by the package-only GitLab archive.

Proposed minimal remediation, requiring applicable approvals: use one effective NuGet package path for all migration commands; explicitly restore/build the required startup project and configuration, then avoid the redundant EF build where safe. Giveaway explicitly builds Db while EF starts Bot, so blindly adding --no-build is unsafe. Verify generated SQL and compare Nexus ordinary/workload requests on controlled builds. No blanket backend-template switch is needed to establish this fix. Remaining work is represented in central DevOps-904 backlog.

Artifacts under `~/ai-data/nexus-usage/oct19-20/`: `trace-tickets-giveaway.json`, `service-migration-traces.json`, `service-migration-step-evidence.json`, `service-historical-source-check.json`, `services_nexus_remote.py`, `services-nexus.json`, `service-ef-time-windows.json`, `service_ef_remote.py`, `service-ef-nexus.json`. Scripts and evidence contain no secret values or raw complete traces/configuration.

## User-requested frontend job liveness check (2026-10-20 14:46 MSK)

User asked whether Business job3237342hangs. Read-only GitLab and runner checks: business-web-gates in master pipeline141262, SHA30ef8f2425955257dd90d22b53dd391440c99852, running since14:26:35MSK. Between14:45:54and14:46:45trace grew1,098,284→1,102,312bytes(+4,028), confirming output progress. Runner108online with fresh heartbeat. Corresponding19-minute project423container d0604d64d83a on172.28.0.171 runs npm test:coverage/node, CPU104.55%, memory840.2MiB of15.61GiB. These observations support active frontend test/coverage execution, not a stalled runner or dependency fetch. No process interruption, retry or CI edit performed; no new independent backlog action established. Artifacts job-3237342-status/progress.json in the Business publication data directory. Task backlog unchanged; earlier full-pipeline-running observations remain dated and are not a claim about current merge state.
