---
system: nexus
status: verified
checked: 2026-10-20
tags: [nexus, usage, ci, cache]
---
# Nexus CE request limit: measured traffic and CI causes

## Task

User requested live read-only analysis of Nexus CE usage after screenshots showed 117,340 requests against the 100,000 rolling-24-hour limit and enforcement starting 2026-11-13. Analysis only; no CI, repository, Nexus, host or external tracker modifications authorized or performed.

## Context

Nexus 3.96.4 on `10.18.24.233`, [system map](../systems/nexus.md). Existing admin credential remains solely `NEXUS_ADMIN_PASSWORD` in `~/ai/current/.env`. Existing SSH access and MSS relay were reused. Current components metric is 10,107, safely below 40,000. SSH/API network access required sandbox escalation. Sync returned no output or reminders.

## Actions

- Aggregated all retained Nexus request logs, 2026-10-11 through 2026-10-20 around 12:23 MSK: 763,181 parsed requests, zero unmatched lines. No raw log copies retained locally. Remote Python was supplied on stdin and performed only log reads; aggregation outputs are local.
- Read repository inventory, authenticated `GET /service/rest/metrics/data`, usage history and monthly metrics. No package downloads or write/API operations.
- Matched the metric window exactly: 2026-10-19 09:00 UTC through 2026-10-20 09:00 UTC (12:00 MSK to 12:00 MSK). Summed `/repository/*` requests equal **117,340**, exactly matching the UI and `nexus.analytics.content_request_count.value.last_24h`.
- Read nginx logging configuration to assess client attribution. All Nexus requests record the bridge gateway `172.18.0.1`; nginx default server has `access_log off`, and its access file is empty. Therefore original client IP/job attribution cannot be recovered from these local access logs.
- Inspected existing local CI/source checkouts without mutations. Read-only GitLab GET confirms current monolith master `c06afbf11383a66d276b65a9cc126e75dbae2a37` and measured-window build job3236355 commit `ae4b098dd1f900953e7afcedc4374a7bfbc98e61` have the same four relevant files as the inspected local checkout. Job3236355 successfully extracted its configured cache; runner106. No raw trace copies or credentials persisted.

## Findings

### Exact rolling-24-hour breakdown

| Repository | Requests | Share |
| --- | ---: | ---: |
| nuget | 60,084 | 51.2% |
| npm | 36,798 | 31.4% |
| docker + docker-hosted | 17,210 | 14.7% |
| Maven + PyPI | 3,248 | 2.8% |
| Total | 117,340 | 100% |

### NuGet

- 13,911 requests concern workload manifests and their packages: 11,727 metadata and 2,184 `.nupkg` requests. This classification uses `.manifest-` package names across paths. Includes Android, iOS, MAUI, tvOS, Mac Catalyst, Mono and Emscripten. SDK8.0.400 registration paths each returned404 414 times; SDK8.0.100 registration paths returned200 209 times.
- Likely background advertising-manifest refreshes: Microsoft documents that build/restore/publish trigger these downloads and `DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE=true` disables background advertising downloads. The exact SDK8 caller and whether any explicit workload operations contribute are not established by existing logs. Do not treat all 13,911 as guaranteed savings before testing.
- Remaining NuGet requests: 25,827 package binaries and 20,346 package index requests. Legacy client `NuGet Command Line/6.5.0` and SDK8/NuGet6.11.2 dominate.
- Monolith `devops/cake/build.cake:5` pins NuGet.CommandLine6.5.0; line54 sets `NoCache=true`. Its CI performs an additional restore and multiple publish commands without `--no-restore` (`.gitlab-ci.yml:88` and release equivalent). Cache semantics, target OS/RID requirements and savings must be checked before changing these commands.

### npm

- 19,502 tarball requests and 17,296 metadata requests. Of tarball requests, **19,476 successful GETs cover only882 unique URLs**:18,594 requests repeat a URL already fetched during the same window. This is a cross-client deduplication opportunity, not a guaranteed achievable saving with separate per-job caches.
- Example `extend-shallow-2.0.1.tgz` downloaded156 times; `define-property-0.2.5.tgz` and `has-flag-3.0.0.tgz` each130 times.
- Almost all npm traffic uses `npm/6.13.4 node/v8.17.0 linux x64 ci/gitlab`.
- Strong monolith source match: `.gitlab-ci.yml:70` uses `6.0-nodejs-cake`; base-images `microsoft/dotnet-sdk/6.0-nodejs-cake/Dockerfile:4` installs Node8.17.0. Monolith GitLab cache at lines73-76 contains only `./nuget-packages`; npm caches are `build/cache/npm/<project>` in `YouDo.Web.Moderation/App_Build/npm.targets:11` and `YouDo.Web.Venus/YouDo.Web.Venus.csproj:65`, absent from the GitLab cache. Their install commands lack `--prefer-offline`. This cache-path omission is verified at the actual build SHA; all npm requests cannot be uniquely assigned to that job from the available Nexus logs.
- B2B already has BuildKit npm and NuGet cache mounts and npm `--prefer-offline --no-audit`; youdo.static/shared v3 templates also cache npm. These are not evidence of effective cross-runner reuse, but should not be blindly replaced.

### Daily pattern and other traffic

Calendar-day `/repository/*` totals in MSK: Oct12 53,538; Oct13 89,028; Oct14 128,798; Oct15 129,160; Oct16 87,482; Oct17 381; Oct18 242; Oct19 **146,536**. These calendar-day totals are not rolling peaks; the UI recorded153,169 as its highest rolling count. The workday/weekend difference supports CI-driven traffic rather than a constant repository-content load.

Oct19 npm had53,798 requests, including28,476 successful tarball GETs across882 URLs (27,594 repeats). Workload requests total15,764. Even an ideal removal of both categories would leave103,178 requests that day; stable compliance requires metadata/package cache reuse and measuring a busy day, not just removing advertising downloads.

Cleaner-like Go client made12,239 search requests returning429 in a near-contemporary moving24-hour window. They target `/service/rest/v1/search`, outside `/repository/*`, and do not explain the licence counter. This is the previously known cleaner credential/rate-limit issue; no cleaner changes or execution were performed. Docker401responses can be normal registry authentication challenges; do not label all as failures. PyPI contributes1,376requests, mostly404for public packages checked against the private index; it is a small secondary source.

### Decision basis and limits

Priorities for a separately approved implementation: disable background workload advertising in applicable server CI, persist the existing monolith npm cache with appropriate keys and prefer-offline, then assess Cake HTTP cache bypass and redundant restores with OS/RID compatibility preserved. Docker is a smaller contributor. Package cleanup does not solve this request limit. A target below 80,000 requests on busy days leaves headroom; existing evidence cannot guarantee that target before implementation and measurement.

Official references: [Sonatype usage counting](https://help.sonatype.com/en/usage-metrics.html), [metric API](https://help.sonatype.com/en/service-metrics-data-api.html), [Microsoft .NET environment variables](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-environment-variables), [npm6 prefer-offline](https://docs.npmjs.com/cli/v6/using-npm/config/).

## Changes

Local diagnostic scripts and sanitized aggregates in `~/ai-data/nexus-usage/`: `aggregate_remote.py`, `detail_remote.py`, `api_snapshot.py`, `gitlab_probe.py`, `verify_job_revision.py`, `request-summary-relay.json`, `request-detail-final.json`, `usage-metrics.json`, `gitlab-monolith.json`. Updated this log, existing Nexus map and central TODO proposal. No repository task edits, commits, CI runs, service restarts or external writes.

## Status and risks

Read-only analysis complete 2026-10-20. Remaining remediation is a proposal under the Nexus section in `~/ai/TODO.md`, requiring normal repository/publication and external-change approvals. The pre-existing cleaner backlog item remains open; this analysis does not change its status. Enforcement date 2026-11-13 is from the supplied UI screenshot, not a new live license expiry check. Exact per-job attribution remains unavailable because source IPs are lost and most clients are anonymous.

## Portable lesson

none

## DevOps-904 npm cache implementation proposal (2026-10-20)

User requested implementation of recommendation1only and supplied task DevOps-904. Current stage: first repository approval pending; no repository edits or branch switch performed. Scope excludes .NET workload and NuGet changes.

Read-only preflight: `/home/slnnk/git/youdo` is clean on master at e22695ea6fa9b4e5f34eee00768582bc7a0d55d8. GitLab master GET returns c06afbf11383a66d276b65a9cc126e75dbae2a37; earlier exact API comparison proves relevant files match this checkout. Proposed branch `DevOps-904-cache-monolith-npm` does not exist remotely (404); no open matching MR returned. No repo-local instruction files found.

Proposal: use existing checkout, create `DevOps-904-cache-monolith-npm` from fresh `origin/master` corresponding to verified remote master (refresh immediately before implementation). Change only `.gitlab-ci.yml`: retain existing NuGet cache key/path, add a separate npm cache for `build/cache/npm/`, and set `npm_config_prefer_offline=true` for `build` and `build_release`. Existing npm project paths consume that directory and npm environment configuration, so project XML edits are unnecessary. Preserve Node/npm versions, installation commands and dependency resolution mode. Validate YAML/cache structure and GitLab CI configuration before the separate publication approval. Runtime savings remain unverified until comparable builds run with a warm cache.

## DevOps-904 local implementation and publication proposal (2026-10-20)

First approval received: user replied `Да` to the concrete repo/branch/base proposal. Both fetch attempts ultimately completed; origin/master is c06afbf11383a66d276b65a9cc126e75dbae2a37, matching approval. Created `DevOps-904-cache-monolith-npm` in the existing clean checkout from origin/master. No unrelated changes existed.

Implemented only `.gitlab-ci.yml` for `build` and `build_release`: job variable `npm_config_prefer_offline: "true"`; existing NuGet cache dictionary retained as the first item of a cache list with identical key/path; second cache key `npm-node8`, path `build/cache/npm/`. No project XML, install command, Node version, NuGet or .NET workload changes.

Verification: `git diff --check` passed. GitLab CI Lint returned valid=true, no errors/warnings; the lint API validated content without creating a pipeline. Parsed before/after YAML comparison confirms only these two jobs' cache and variable blocks changed; original NuGet settings and all scripts/rules preserved. Runtime warm-cache behavior is not yet tested and savings are unverified. Net patch: one file,16insertions,6deletions. Index remains empty; no commit/push/MR performed.

Second approval proposal: commit `cache npm dependencies between monolith builds`; ready MR title `DevOps-904 Cache npm dependencies between monolith builds`; source `DevOps-904-cache-monolith-npm`, target `master`. Description is a short Russian paragraph plus DevOps-904 link in `~/ai-data/gitlab-workflow/DevOps-904/youdo/body.txt`. Actual diff, lint report, proposal and bound snapshot are in the same directory. Snapshot verification passed; it grants no permission. Publication approval remains pending.

CI effects inspected from current YAML and live include `monitoring/generate-slo-rules.yml` plus `partials/.rules-sets.yml`: standalone feature push is excluded by workflow; a ready MR to master automatically builds/tests, pushes project Docker images tagged by pipeline ID, then `publish` creates/pushes a CI Git tag and calls the established notification endpoint. User approval must explicitly cover those effects. Production deploy jobs require trigger/production-target manual actions and are not automatic here. SLO jobs have no matching MR-event rules, so monitoring deployment is not triggered by this MR. No manual job, merge, release or deployment is authorized. Target master merge later remains a separate user action.

## DevOps-904 publication completed (2026-10-20)

Second supervised approval received: user replied `Да` to the exact diff/checks, commit message, ready MR title/body, source/target and explicit automatic Docker push/CI tag/notification effects. This supersedes the earlier pending-publication status, without authorizing merge, manual jobs or deployment.

Bound snapshot check matched before staging. Staged only `.gitlab-ci.yml` and inspected the entire staged diff; no other staged/untracked changes. Commit `abc9c7ae1a5cc65509065be344abf20cb74a6810`, message `cache npm dependencies between monolith builds`, exactly matches the approved saved diff. Working tree clean. Pushed only `DevOps-904-cache-monolith-npm` to origin using verified SSH HostKeyAlias; no force or target push.

Created ready [MR !10113](https://gitlab.youdo.sg/youdo/youdo/-/merge_requests/10113), source `DevOps-904-cache-monolith-npm`, target `master`, title `DevOps-904 Cache npm dependencies between monolith builds`. Assignee `a.solonenko`, squash false, remove-source-on-merge true, matching project defaults. Publication and independent verify helpers both returned verified=true and exact expected SHA/body/identity. CI [pipeline141244](https://gitlab.youdo.sg/youdo/youdo/-/pipelines/141244) is running at final verification. This is not a passing-CI or runtime savings claim. No manual job, merge, production deployment or YouTrack write performed. Central TODO retains pipeline/merge/warm-cache effectiveness verification and separate optional optimizations.

## DevOps-904 description scope clarification (2026-10-20)

Task-specific user correction: DevOps-904 covers overall Nexus request-limit remediation and identification of other sources, not just the monolith npm cache change. The user requested a general issue description with concrete measured figures; monolith optimization is one contributor and first step. Implementation so far remains limited to the previously approved npm patch; this scope clarification does not authorize unrelated repository edits or external writes. Prepared a revised description payload in `~/ai-data/gitlab-workflow/DevOps-904/youdo/youtrack-description.json`, using the exact117,340rolling-window breakdown and UI peak153,169. YouTrack current description was GET-verified empty; no description update has been performed. Await confirmation for the concrete revised YouTrack write under the external-change rule.

## DevOps-904 YouTrack description saved (2026-10-20)

User explicitly approved the final full description after adding the old OSS versus CE behavior explanation. Pre-write GET confirmed description remained empty. Updated only the description of [DevOps-904](https://youtrack.youdo.com/youtrack/issue/DevOps-904), preserving title and other issue fields. Independent GET exactly matched the prepared 1,432-character payload. Description includes measured117,340request breakdown, peak153,169, Nov13enforcement, OSS3.70.4 advisory warnings versus CE3.96.4 enforced limits introduced with3.77.0, and overall remediation with monolith npm as first step. No new comment or issue-state change. Local verification receipt: `~/ai-data/gitlab-workflow/DevOps-904/youdo/youtrack-description-receipt.json`. This supersedes earlier description-write approval-pending status. Existing central TODO remains open for CI/cache effectiveness and other traffic sources; no remediation completion inferred from description publication.

## Description formatting correction prepared (2026-10-20)

User screenshot shows the saved description as plain paragraphs. The submitted payload omitted Markdown headings, bold emphasis and list syntax; exact text GET verification did not verify rendered formatting. Prepared `youtrack-description-formatted.json` beside the original payload with three headings, a four-item request breakdown, emphasized limits/dates and a named MR link. No external correction performed yet; the per-action external-change approval is pending. Content scope remains the general DevOps-904 problem and remediation.

## Description formatting correction applied (2026-10-20)

User approved the prepared formatting correction with `Да`. Pre-write GET matched the original description. Updated only the description of DevOps-904 to the prepared Markdown payload, with three headings, a four-item metric list, emphasis and a named MR link. Independent GET exactly matched the approved replacement. Receipt: `~/ai-data/gitlab-workflow/DevOps-904/youdo/youtrack-description-formatted-receipt.json`. This supersedes formatting approval-pending status. Rendered browser appearance was not inspected; API verification proves Markdown text preservation only. Remediation backlog unchanged.

## Consumer attribution refined by GitLab comparison (2026-10-20)

[October19/20 comparison](2026-10-20-nexus-gitlab-consumers-oct19-20.md) supplies job/trace evidence and supersedes the earlier broad Business NuGet caching statement: internal-api still uses the shared uncached Docker restore path. On October19 its traces contain21,073Nexus GETs. Monolith timing/UA association accounts for85,871requests. DevOps-904 first successful build was a cold cache fill, not evidence of savings. No external changes from this follow-up.
