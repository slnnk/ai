---
system: nexus
status: verified
checked: 2026-10-22
tags: [nexus, usage, ci, cache]
---
# Nexus DevOps-904: October 22 request peak explained

## Task
Explain the user screenshot showing 164,373 requests per rolling day. Read-only diagnosis; no implementation or external writes requested.

## Context
Follow-up to [October 20 analysis](2026-10-20-nexus-ce-request-limit-analysis.md) and [consumer comparison](2026-10-20-nexus-gitlab-consumers-oct19-20.md). Access routes and credential variable names remain in those notes and the Nexus system map.

## Actions
Read existing Nexus request logs through the established SSH relay; GET metrics, usage history and monthly metrics. Reused aggregate/detail/API diagnostic scripts, with new local dated copies for the October 22 window. No package downloads, CI retries, repository changes or external writes.

## Findings
The API usage-history latest value is 164,373. Log aggregation exactly reproduces it over October 21 20:00 to October 22 20:00 MSK, with zero unmatched log lines.

| Repository family | Requests | Share |
| --- | ---: | ---: |
| npm including private | 73,539 | 44.7% |
| NuGet | 46,026 | 28.0% |
| Docker | 23,907 | 14.5% |
| Maven | 20,865 | 12.7% |
| PyPI | 36 | 0.02% |
| Total | 164,373 | 100% |

Modern npm11.6.2/Node24 CI agents generated 54,527 public npm requests; npm12/Node26 CI added 3,934. Legacy npm6/Node8, previously associated with monolith, generated 13,108. Modern CI npm therefore dominates this window; Exact projects were not attributed at this initial pass; the GitLab follow-up below supersedes that limit for the dominant agents. Successful public npm tarball GETs total 67,518 for 2,368 unique URLs (65,150 requests repeat a URL within the window). This establishes repeated downloads across clients/jobs, not the precise cache failure or an achievable saving. Vitest pretty-format and utils 4.1.7 tarballs each appear 390 times.

NuGet workload metadata/packages total 29,379 (24,922 metadata plus 4,457 binaries), 63.8% of NuGet and 17.9% of all counted requests. Ordinary NuGet package/index requests total 16,647. This classifies endpoint traffic; background advertising versus explicit workload commands and exact caller projects remain unproven.

Maven traffic is 20,865 versus 3,248 combined Maven/PyPI in the earlier October 20 window. Gradle8.13 accounts for 16,942 requests and Gradle8.7 Linux for 2,674; Project attribution was not established at this initial pass; see the GitLab follow-up below. Ordinary Gradle dependency paths dominate, with repeated package POM and snapshot metadata lookups.

Relative to the earlier 117,340 rolling window: npm including private +36,741; NuGet -14,058; Docker +6,697; Maven/PyPI +17,653; total +47,033. These are different workday windows, not a controlled before/after experiment. The previously observed 67.4% npm reduction concerned one monolith cold/warm pair; it never established a 67.4% reduction of total Nexus traffic. Even excluding all classified workload traffic leaves 134,994 requests, so workload suppression alone cannot bring this observed window below 100,000.

## GitLab source attribution completed (2026-10-22)

User requested identifying the source in GitLab jobs. Applied gitlab-workflow investigation stage and delegated bounded local CI source inspection under the KB economical-tool rule. Read-only inventory covers all10registered runners,883job executions in the exact screenshot window, zero runner-list/trace errors. Streamed49sample traces followed by106priority traces (83frontend-tools,15Android,8monolith); saved only counters and selected sanitized cache/version/command evidence. Exact CI files were GET-read at job SHAs after local source inspection; no repository/Git mutations or external writes.

### Primary npm source: frontend-tools

Project `youdo/microservices/youdo-core-frontend-tools` (496) ran83jobs across18pipelines. All68Node jobs execute `npm install`:18verify,18verify eslint-config,15build,13lib-stats,2deploy lib,2deploy eslint-config. The other15publish jobs use a different image. None of the68traces restores a GitLab cache; the exact CI files contain no cache or include declaration and use Node24. Both first sampled job3242582SHAcf99239d and latest3247583SHA820ddbb6confirm this behavior. Latest example pipeline141526runs separate verify3247583, build3247585andlib-stats3247586, each adding791packages. Earlier jobs add823packages. These independent installations explain repeated tarball downloads; do not equate an npm added summary alone with network traffic.

Node24/npm11.6.2 CI makes54,534repository requests including7private npm requests,54,527public npm requests. All corresponding minute buckets overlap frontend-tools;29,818requests occur with frontend-tools as the only relevant project candidate,24,716overlap Business jobs. Business sampled current traces/configuration use Node26, providing additional version discrimination. Strong project attribution combines client version, exact CI source, repeated installation evidence and timing; shared Nexus gateway/logging still prevents unique per-job request identification in overlapping intervals. Do not present each broad job-window count as exact job consumption.

Examples: [verify3246218](https://gitlab.youdo.sg/youdo/microservices/youdo-core-frontend-tools/-/jobs/3246218), [verify3247583](https://gitlab.youdo.sg/youdo/microservices/youdo-core-frontend-tools/-/jobs/3247583), [build3247585](https://gitlab.youdo.sg/youdo/microservices/youdo-core-frontend-tools/-/jobs/3247585), [lib-stats3247586](https://gitlab.youdo.sg/youdo/microservices/youdo-core-frontend-tools/-/jobs/3247586). Minimal future remediation proposal is shared npm download caching or a prepare/artifact stage, with lock-aware behavior and project checks; implementation remains unrequested and requires repository approvals.

### Main Gradle source: Android

All16,942Gradle8.13repository requests coincide with `team-youdo-android/android-youdo4` (79); no other Android/test-project candidate overlaps those buckets. Seven feature executions (including failed/cancelled attempts) plus4feature_browserstack jobs use image `registry.youdo.sg/sysadmins/devops-tools/gradle:18`. Feature calls `gradle assembleBeta`; BrowserStack job also invokes Gradle through `:youdoapp:uploadBuildToBrowserstack`, causing another project/dependency resolution. Both are relevant consumers, not just the APK build.

Exact job3243538SHAe0a32918 and3245641SHA8c3c2c49CI confirm these commands and no GitLab cache/GRADLE_USER_HOME declaration; all11Gradle-image traces lack cache restoration. Local Gradle image source Dockerfile starts from gradle:8.13.0-jdk21. Direct system gradle invocation uses this image version, not the repository wrapper version. Examples: [feature3244183](https://gitlab.youdo.sg/team-youdo-android/android-youdo4/-/jobs/3244183), [feature3245641](https://gitlab.youdo.sg/team-youdo-android/android-youdo4/-/jobs/3245641), [feature_browserstack3240161](https://gitlab.youdo.sg/team-youdo-android/android-youdo4/-/jobs/3240161). A persisted Gradle dependency-cache proposal remains separate from implementation authorization. No builds were started by agents.

### Other established sources and limits

Node26/npm12CI contributes3,934requests, all in Business-only candidate windows; Business sampled gates restore their lock-keyed npm cache and use prefer-offline, and image builds expose BuildKit npm mounts. Do not label this a missing-cache configuration. Modern npm is therefore dominated by frontend-tools, not the already cache-enabled Business paths or Static. Static sampled jobs use Node20.14 and successfully restore `.npm` cache.

Legacy monolith npm contributes13,108requests in its8build/build_release windows. All8traces restore NuGet;5also restore npm-node8cache. Three build jobs3242836,3245379and3246194have no npm cache check/extraction and their nonoverlapping legacy-client windows account for8,488requests; the remaining5cached builds collectively account for4,620(consistent with924each, but overlapping full build intervals are not unique per-job attribution). This explains why merging the cache patch did not eliminate uncached builds of older branches. No further monolith remediation was performed; prior user deferral remains.

Approximately2,674Linux Gradle8.7requests (plus80Mac Gradle8.7requests) remain unattributed to a GitLab job in this10-runner inventory. Previously known autotest repos have matching tooling, but no matching jobs were observed in the window; this is not proof of a particular Jenkins job or user source. NuGet workload29,379andremaining Docker/other traffic were not uniquely mapped by this npm/Gradle-focused follow-up.

Artifacts: `~/ai-data/nexus-usage/oct22/runner-jobs.json`, `nexus.json`, `source-correlation.json`, `trace-sources.json`, `trace-priority-all.json`, `exact-source-files.json` and the associated bounded read-only collectors. All runner inventory and selected trace collection completed with zero errors/truncation. CI files are exact observed revisions, not cached-master assumptions. No jobs retried, configs edited, merges/deployments performed or tracker comments written.

## Changes
Local aggregates: `~/ai-data/nexus-usage/request-summary-oct22.json`, `request-detail-oct22.json`, `usage-metrics-oct22.json`; dated diagnostic script copies in the same directory. Updated Nexus map and existing central DevOps-904 backlog evidence.

## Status and risks
Explained the exact UI total and attributed dominant modern npm/Gradle traffic to frontend-tools/Android; remaining cache remediation proposals and Gradle8.7 attribution are tracked in [central TODO](../../../../TODO.md), Nexus recovery / DevOps-904. Project attribution is supported as above; per-job overlap limits and achievable cache savings remain unverified. Prior user deferral of additional monolith/npm investigation remains in force; modern CI npm agents are a different observed source. No fixes, retries, merges, deployment or tracker writes performed.

## Portable lesson
none

## Frontend-tools cache implementation: first approval proposed (2026-10-22)

User requested implementing frontend-tools caching. Existing `/home/slnnk/git/youdo-core-frontend-tools` checkout is clean on Site-24691-update-storybook-and-deps, HEADb64740f; no applicable repository/ancestor AGENTS found and Git identity is configured. Read-only GitLab GET confirms default/master8b0e6d3e94aa852f1b29488023002c66c2908303, six npm install commands and no cache/prefer-offline configuration. Proposed branch `DevOps-904-cache-frontend-tools-npm` is absent locally/remotely (remote404), with no open matching MR.

First supervised proposal: existing checkout, new branch above from freshly verified origin/master8b0e6d3, only CI npm download-cache/prefer-offline changes for the six Node jobs. Retain existing install/build/publication commands and behavior except the requested caching. Validate YAML/effective GitLab CI before the separate publication proposal. First branch/base confirmation pending; no fetch/branch switch/task edit/stage/commit/push/MR performed. Publication effects include existing Storybook S3 upload and possible library publication paths; inspect current rules in full before proposing publication. Preflight artifacts: `~/ai-data/gitlab-workflow/DevOps-904/youdo-core-frontend-tools/preflight.json`, `master.gitlab-ci.yml`.

## Frontend-tools local cache patch and second approval proposal (2026-10-22)

First supervised approval received: user replied `Да` to existing repo/new branch/base proposal. Fetched origin/master and verified exact8b0e6d3e94aa852f1b29488023002c66c2908303; created `DevOps-904-cache-frontend-tools-npm` in the clean existing checkout. Only `.gitlab-ci.yml` changed:20insertions/6deletions. Added hidden `.npm-cache` template, NPM_CONFIG_CACHE=$CI_PROJECT_DIR/.npm and fixed key npm-node24/path.npm/. Six existing install locations extend the template and add --prefer-offline. Seven executable jobs inherit it because two package deploy jobs share a template; Storybook publish job has no npm cache. No install-command replacement, audit suppression, source changes, staging or commit.

Fresh master introduces root AGENTS and .codex rules absent at the former checked-out revision. Root instructions and all10required rule files read by review delegate; no CI-only additional skill gate. Repo Site-* convention yields to the user's explicit approved DevOps-904branch. Root AGENTS unconditionally requires lint/type-check; both attempted using existing local dependencies. Lint exit127: oxlint missing. Type-check exit2/TS2688: node type definitions missing. Local Node22.17/npm10.9also falls below the repository Node24/npm11requirement. No dependency installation or unrelated source repair performed; these checks remain pending in CI. Conditional UI tests/public-API validate:ai not applicable to this CI-only patch. No active pre-push hook/core.hooksPath found in checkout.

Passed git diff --check, local parsed-YAML comparison (only requested semantics), GitLab CI Lint valid=true with no errors/warnings, before/after effective-CI validation of all7jobs and inherited PKG_DIR preservation. Rules/scripts/stages/artifact/publication behavior otherwise unchanged; review found no blockers. Project/group GETs found no overriding NPM_CONFIG_CACHE/prefer-offline variables. Concurrent cache writers can reduce cache completeness, not installation correctness; runtime reuse and traffic savings require actual CI measurement.

Second approval proposal saved under `~/ai-data/gitlab-workflow/DevOps-904/youdo-core-frontend-tools/`: proposal.json, body.txt, reviewed.patch, checks.json, ci-effective-check.json, ci-lint.json, publication-ci-preflight.json and snapshot.json. Snapshot matches approved repo/base, exact branch/diff/body; grants no consent. Commit message `cache npm packages for frontend tools`; MR title `Draft: DevOps-904 Cache npm packages for frontend-tools`, source as above/target master, draft due incomplete local lint/type checks. Russian one-paragraph body describes common download cache and prefer-offline, followed by DevOps-904 link. Project defaults squash off/source removal on merge true; no merge authorized.

CI effect review: source branch push has no matching jobs under existing rules; MR creation runs verify, verify eslint-config, build, lib-stats and automatic Storybook upload to existing youdo-b2b-storybook-test S3 bucket. MR library-publication jobs remain manual. Future merge into master auto-publishes UI library; neither merge nor manual publication is covered here. Explicit second approval must cover the automatic test-Storybook S3 write. Stage/commit/push/MR publication pending; no external writes or real pipeline run initiated. Central TODO retains this gate, runtime verification and separate Android/cache workload proposals.

## Cache upload concurrency correction implemented locally (2026-10-22)

User asked about simultaneous cache uploads. Official GitLab caching/cache:policy documentation confirms shared keys overwrite archives rather than merge them and recommends pull-only parallel consumers. Explained last-writer cache completeness/extra-upload effects and proposed one writer with resource_group; user explicitly requested `Сделай`. This is a task-specific authorized implementation revision within the existing approved repo/branch/base, not publication approval or a new global workflow instruction.

Updated only `.gitlab-ci.yml` on the same approved branch:40insertions/6deletions total against master. Added prepare stage and prepare-npm job with existing Node24image/dind runner/registry settings. It warms root workspace download cache using npm install --ignore-scripts --prefer-offline --no-audit; scripts/audit are skipped only in the new warming job to avoid duplicating lifecycle side effects/audit, while all existing installation commands retain normal behavior except prefer-offline. Existing root npm prepare script configures Git hooks; skipping lifecycle scripts in the warming job avoids running it there.

Hidden cache template now has policy pull. prepare-npm overrides only policy pull-push and uses resource_group npm-node24-cache, serializing the only cache writers across pipelines; key npm-node24 and absolute cache path remain. Seven existing executable consumers wait through normal stages, use pull only, and have no needs bypass. Two package deploy jobs still preserve PKG_DIR via deep-merge inheritance. Existing rules/scripts/artifact/publication settings preserved; preparation shares master/MR rules with verify. Parallel readers can reuse the last complete cache; missing entries still fetch normally. Cache is best-effort, and traffic savings remain to measure. No claim that every missing optional/lifecycle download is warmed.

Checks: diff whitespace PASS; CI Lint v2 valid=true/no errors/warnings; parsed YAML comparison and before/after effective-CI assertions PASS, confirming sole writer/resource_group/read-only consumers/stage order/existing-job semantics. Existing UI lint/type local dependency blocks remain unchanged and were not rerun without dependency changes. No staging, commit, push, MR, pipeline or external mutation.

Version2publication proposal/body/reviewed diff/snapshot saved as proposal-v2.json, body-v2.txt, reviewed-v2.patch, snapshot-v2.json beside earlier artifacts; matching snapshot grants no approval. Version1proposal remains historical and is superseded; never use it for publication. Commit/title/source/target unchanged: cache npm packages for frontend tools; Draft: DevOps-904 Cache npm packages for frontend-tools; DevOps-904-cache-frontend-tools-npm to master. New Russian MR body describes the serialized preparation writer and pull-only consumers, then task link. Updated effects include one additional prep job/possible resource-group queue before existing tests/builds, and existing automatic test-Storybook S3 upload. Second approval of the revised proposal remains pending.

## Frontend-tools approved publication completed (2026-10-22)

Second supervised approval received: user replied `Сделай` to the complete version2commit/push/Draft-MR proposal, explicitly including automatic test-Storybook S3 update. Snapshot-v2check matched before staging; entire index was empty. Staged only .gitlab-ci.yml and inspected full staged diff; assertion exactly matched reviewed-v2.patch and no other tracked/unstaged changes. Committed `8dccfc2aa52debbe2b26cb975a442f2d567a9ea3` with approved message `cache npm packages for frontend tools`; resulting commit patch exactly matches approval and checkout is clean. Pushed only the approved source branch, without force.

Created [Draft MR183](https://gitlab.youdo.sg/youdo/microservices/youdo-core-frontend-tools/-/merge_requests/183), exact approved title/body/source/target. Assigned a.solonenko, squash false and remove-source-on-merge true per actual project defaults; no source deletion or merge performed. Publication helper and separate read-only verify both confirmed exact SHA/title/body/source/target/draft/settings. Initial create receipt had no pipeline yet; later verification confirms [pipeline141529](https://gitlab.youdo.sg/youdo/microservices/youdo-core-frontend-tools/-/pipelines/141529) running.

Initial runtime GET shows prepare-npm3247598running: expected cold cache miss, npm install added792packages in9seconds, archive upload to shared runner object storage started. Downstream verify/build/publish jobs were waiting at that observation. This proves execution/start of upload, not completed cache publication/reuse or overall pipeline success. No manual job, merge, extra retry, direct S3 write or tracker update performed; normal pipeline effects were covered by approval. MR remains Draft with CI checks/runtime cache verification pending. Receipts: publication-result.json, verification-result.json, commit-result.json, pipeline-141529-initial.json in the proposal directory. Earlier second-approval-pending state is superseded.

## Initial CI checks pass; cache upload blocked by S3 timeouts (2026-10-22)

Further read-only checks supersede initial upload-start status. prepare-npm3247598on runner106/gitlab-runner-docker-2(172.28.0.172) completed SUCCESS in148.37seconds, but its cache publication failed: three PUT attempts to shared S3 object project/496/npm-node24-non_protected ended with `net/http: timeout awaiting response headers`, final `Failed to create cache`. Runner still marks the job success because cache upload failure is nonfatal. Archive found3,502matching files/directories; npm installation itself added792packages in9seconds. Do not claim a usable cache from the green job.

Downstream verify3247599SUCCESS and verify eslint-config3247600SUCCESS both logged `file does not exist` / `Failed to extract cache`, installed791/792packages again, and correctly logged `Not uploading cache ... due to policy`. Thus pull-only behavior and stage ordering work, but storage failure prevents the intended reuse. CI verify executes the previously local-blocked lint/type checks (and its other existing gates) successfully; the local missing-dependency limitation is now distinct from passing runtime checks. build3247601andlib-stats3247602were running and pipeline141529overall running at final observation. MR remains Draft as approved; no readiness change or manual action performed.

Read-only SSH to runner106confirms hostname and ordinary unauthenticated HTTPS GET to https://storage.yandexcloud.net/ returns200in0.12seconds (connect0.015/TLS0.100). This does not establish successful signed PUT/upload from the helper container, permission validity or a specific network cause. No cache test object PUT, runner setting change, service restart, cache mutation or job retry was initiated. Further S3 upload diagnosis/recovery and subsequent runtime warm-cache measurement remain open in central TODO; external fixes/retries need applicable approval.

Artifacts: prepare-npm-upload-status.json and pipeline-141529-final-observation.json in the publication directory (signed URL query parameters redacted); earlier pipeline-141529-verification.json retained masked diagnostics. Final outcome: approved code committed/pushed/MR created and checks pass so far; cache upload blocked, reuse and request reduction not achieved in this first run. No merge/deployment/tracker update. This supersedes both the publication-pending gate and any assumption that cache upload completed.

## User restart confirms cache upload and consumer reuse (2026-10-22)

User reported restarting and supplied [prepare-npm3247736](https://gitlab.youdo.sg/youdo/microservices/youdo-core-frontend-tools/-/jobs/3247736). Read-only job/trace/pipeline GETs confirm new MR pipeline141531at exact approved SHA8dccfc2aa52debbe2b26cb975a442f2d567a9ea3. No agent retry or external mutation performed.

prepare-npm3247736SUCCESS on the same runner106(172.28.0.172),21:55:44–21:56:25MSK/41.32seconds. Initial cache miss is expected after the prior failed publication; installed792packages in9seconds, successfully uploaded the shared S3 object, logged `Created cache` and `Job succeeded`, with no repeated-upload timeout in this trace. This supersedes the earlier currently-blocked upload status; the reason for the first transient failure remains unknown, not a proven infrastructure fix.

Downstream verify3247737andverify eslint-config3247738bothSUCCESS. Both logged `Successfully extracted cache` and `Not uploading cache ... due to policy`; their npm installs added791/792packages in8seconds. Thus persisted-cache download/consumer behavior is now demonstrated, including pull-only policy. Installation summaries do not by themselves prove zero Nexus traffic or a quantified request reduction. Build3247739andlib-stats3247740were running, overall pipeline141531running at final observation; no full-pipeline-success or MR-readiness claim. MR stays Draft as approved. Actual Nexus request savings and sustained reuse remain to measure; no infrastructure repair is needed solely on the previous failed attempt absent recurrence.

Sanitized evidence: `~/ai-data/gitlab-workflow/DevOps-904/youdo-core-frontend-tools/job-3247736-cache-verification.json`; reusable bounded read-only checker `check_cache_job.py` in that directory. Existing pending S3-recovery wording in map/TODO superseded by this result while the first failure is retained as history.

## Storybook publish3247741 failed on two S3 InternalError responses (2026-10-22)

User supplied [publish3247741](https://gitlab.youdo.sg/youdo/microservices/youdo-core-frontend-tools/-/jobs/3247741). Read-only GET confirms script_failure/exit1after207.11seconds, runner106; full pipeline141531FAILED. Exact SHA remains8dccfc2. Sanitized trace evidence has379successful upload lines and2failed upload lines. Both failed PutObject requests returned S3 `InternalError` after reaching max retries4: `We encountered an internal error, please try again.` Failed files are storybook/assets/Accordion.stories-Br5XW97Q.js and storybook/components/atoms/Icon/index.d.ts. Storybook upload therefore partially completed; do not claim a complete published site from the successful files.

prepare-npm3247736,verify3247737,verify eslint-config3247738,build3247739andlib-stats3247740allSUCCESS. All4downstream npm jobs explicitly restore the cache and skip upload due to pull policy. npm cache publication/reuse remains verified; the failing publish job has no npm cache and its AWS sync command is unchanged by the reviewed patch. The S3 service response distinguishes this failure from a cache configuration error; relationship to the earlier response-header timeout remains unproven. Manual library-publication jobs skipped; none played.

A separately authorized retry of publish alone is the concrete next recovery step; no need to restart cache preparation/tests/builds for this observed failure. User supplied URL authorizes diagnosis, not retry or infrastructure changes. No retry, code change, MR readiness change, merge, infrastructure mutation or tracker write performed. Full green pipeline and quantified Nexus savings remain open; approved Draft MR183is still the published artifact. Evidence: job-3247741-cache-verification.json and job-3247741-publish-evidence.json in the publication directory. This supersedes the earlier full-pipeline-running observation.

## User publish retry succeeded; automatic pipeline jobs complete (2026-10-22)

User said `Готово` after the publish-only retry suggestion. Read-only GET of pipeline141531including retried jobs confirms new [publish3248009](https://gitlab.youdo.sg/youdo/microservices/youdo-core-frontend-tools/-/jobs/3248009) SUCCESS,22:18:19–22:18:33MSK/13.44seconds. Original failed publish3247741remains historical and is superseded by the successful retry. No agent retry/external mutation performed.

All six automatic jobs now SUCCESS: prepare-npm3247736,verify3247737,verify eslint-config3247738,build3247739,lib-stats3247740,publish3248009. Cache publication and all4consumer restorations remain verified with pull-only/no-upload behavior. Pipeline overall status is `manual`, not failed/running or completed SUCCESS, because deploy lib3247742/deploy eslint-config3247743/deploy prettier-config3247744are manual under the existing rules. Do not play these jobs to make the pipeline green; their package-publication effects need separate explicit approval. MR183remains Draft unless user separately requests readiness change; no merge authorization.

Publish recovery item is resolved by observed user retry; no ongoing S3 repair inferred from the two earlier transient failures. Root cause remains unknown. Current functional outcome is common npm cache implemented/published and verified, all automatic CI checks/build/Storybook sync successful; quantified Nexus request reduction/sustained busy-day effect remains to measure. Central TODO reconciled to remove stale publish-retry action. Evidence: updated job-3247741-cache-verification.json includes complete retry inventory and current pipeline status.

## Frontend-tools Nexus request reduction measured (2026-10-22)

User explicitly requested measurement. Read-only GitLab GET and remote Nexus log aggregation compare pre-change pipeline141526with working-cache pipeline141531and same-SHA cache-miss control141529. No retries/pipeline creation, package downloads, repository changes, tracker writes or infrastructure mutations. Fresh inventory covers all10runners/73jobs in19:30–22:05MSK, zero collection errors. Exact job/trace windows rounded outward to seconds; simultaneous jobs are counted as union windows, not summed (per-job windows overlap and must not be added).

Pre-change141526SHA820ddbb6has four npm jobs19:43:06–19:45:37MSK; cache implementation141531SHA8dccfc2has cold prepare21:55:44–21:56:26and four consumers21:56:26–22:00:05. Exact GitLab raw-file hashes confirm root package-lock.json and package.json are byte-identical across these revisions (historical source SHA was unavailable in local Git objects, so used exact-revision GET fallback). New/baseline consumer jobs install the same791/792package counts. Cache-miss control141529uses the identical implementation SHA8dccfc2but its initial archive upload failed, giving five cold installs20:56:23–21:01:26. This control isolates reuse from code/dependency changes.

| Metric | Pre-change141526 | Working cache141531 |
| --- | ---: | ---: |
| Four consumer npm requests | 3,160 | 4 |
| Consumer successful package GETs | 3,156 | 0 |
| Consumer audit POSTs | 4 | 4 |
| Additional cold preparation requests | none | 789 |
| Total including preparation | 3,160 | 793 |

Observed net saving versus the previous pipeline is2,367requests,74.905%. Four consumer jobs alone drop99.873%; their only remaining requests are four POSTs to /repository/npm/-/npm/v1/security/advisories/bulk (HTTP400in both windows). Warm consumers make zero npm tarball/metadata requests. Cold preparation makes789successful tarball GETs across754unique URLs; repeated versions in the graph can cause more downloads than unique URLs, so do not equate package install count to GET count.

Same-SHA control141529makes3,949requests:789preparation+3,160consumers, compared with793for141531(-79.919%). Before-change/control consumer totals exactly match, independently supporting the measured74.9% net saving after allowing for the newly introduced preparation cost. Both preparers were cold; an already-warm preparer in a later pipeline has not been measured, so do not claim a fully warm pipeline makes only4requests yet.

Attribution/overlap: no other frontend-tools pipeline overlaps any measured group. Control window has no other GitLab project; baseline overlaps2Business jobs; working cache overlaps11Business jobs. Filtered modern frontend-tools agent npm11.6.2/Node24CI;713parallel npm requests from Node26Business agents are excluded from the working pipeline result (unfiltered npm would misleadingly be1,506). Aggregate used both public/private npm repo paths, zero unmatched Nexus log lines. Shared gateway prevents splitting the simultaneous same-agent consumers individually, but does not affect these project/group union counts given the observed version and inventory separation.

Observed installation wall times8–14seconds remain similar to earlier9–17seconds; build durations vary and the working jobs are not uniformly faster. The confirmed benefit is Nexus request reduction, not a guaranteed build speedup. Reuse also crosses runner106(preparer) to runner105(build/lib-stats) through shared object storage.

Artifacts: `~/ai-data/nexus-usage/frontend-tools-cache/` contains windows.json, aggregate_windows_remote.py, nexus-windows.json, runner-jobs.json, overlap-check.json, comparison.json, dependency-source-comparison.json; exact job/trace windows in `~/ai-data/gitlab-workflow/DevOps-904/youdo-core-frontend-tools/npm-measurement-jobs.json`. Verified one working-cache pipeline including cold population, not sustained daily savings. MR183remains Draft/unmerged; other branch pipelines may still use old CI. Central TODO updated with measured result and only remaining whole-day/MR integration/other-consumer scope; this measurement does not authorize merge, readiness changes or new test runs.

## User merge verified; master cache works, duplicate UI publication fails (2026-10-22)

User requested merge; agent started read-only preflight and confirmed unchanged reviewed SHA/diff/base, no conflicts and all automatic MR checks successful. Before any readiness/merge write, user interrupted the read-only policy check and reported already merging, supplying [master pipeline141536](https://gitlab.youdo.sg/youdo/microservices/youdo-core-frontend-tools/-/pipelines/141536). No agent readiness, merge, source deletion, manual job or deployment command was issued. User action supersedes pending agent merge work.

Independent MR GET confirms MR183MERGED, draft false,22:26:31MSK, merge commitb1f0670ddf8b9b9fb0eef7020a8e570db94bd40e, original source8dccfc2unchanged, no squash SHA. Pipeline141536is push/master at exactly that merge commit and currently FAILED. Cache prepare3248018SUCCESS on runner105, creates npm-node24-protected after expected cold miss (MR used separate non_protected key). verify3248019,verify eslint-config3248020,build3248021andStorybook publish3248022allSUCCESS. All npm consumers, including deploy lib, extract the protected cache; successful build/check consumers skip upload due to pull policy. Shared reuse works on master and across the105→106runner path.

Only failure is existing automatic deploy lib3248023(exit1/script_failure) after successful npm cache restoration/install and library build. npm reports `You cannot publish over the previously published versions: 0.40.3.` The job attempts publishing unchanged @youdo/ui0.40.3under the original unmodified master publication rules. This is distinct from earlier S3 failures/cache behavior. Retry without changing the duplicate-publication condition is not expected to resolve it. Do not bump a UI package version merely to publish this CI-only patch, republish/delete an existing version, change release rules or retry automatically.

Optional minimal correction proposal: give deploy lib an existing-version probe/no-op behavior analogous to .deploy package, or separately decide publication rules/versioning. No implementation requested/approved for that additional behavior yet; track proposal in central TODO. Frontend cache task is implemented/merged and measured; sustained daily Nexus effect and other DevOps-904 consumers remain open. The pipeline is not wholly green and no new package-release success is claimed. Detailed sanitized evidence and reusable read-only checker: master-pipeline-141536.json/check_master_pipeline.py in the publication directory. No GitLab/YouTrack changes were made by this verification.

## User scope clarification: caching only; publication proposal withdrawn (2026-10-22)

User questioned the unrelated publication change: `Нам же нужно было только кэширование добавить.` Treat this as task-specific scope clarification for the frontend-tools caching work, not a new global rule or authorization. The optional deploy-lib existing-version guard suggestion was unnecessary to complete caching and is withdrawn from active follow-ups. Existing global minimal-scope instructions already apply; no instruction/skill edits needed.

The approved/merged diff only adds cache preparation/serialization/read-only consumers and prefer-offline. It does not change the existing publication rules or npm publish command. Master cache preparation/restoration, checks/builds and Storybook sync succeeded; measured per-pipeline Nexus requests fell74.9%. Duplicate UI0.40.3publication failure is retained as an observed pre-existing command behavior, outside this cache task. No publication guard, version bump, release skip, retry, MR or infrastructure change performed/planned under this request. Frontend-tools cache implementation is complete. Broader DevOps-904 daily observation/other-consumer proposals retain their independent existing scope; they do not authorize more changes here.
