---
system: nexus
status: verified
checked: 2026-11-05
tags: [nexus, gitlab-ci, npm, cache]
---
# Business gates: latest pipeline cache restore and shared-key collision

## Task
Check whether npm caching works in the latest Business frontend gates, as a read-only follow-up to DevOps-904.

## Context
Project `youdo/microservices/youdo.business` (423). Existing checkout `/home/slnnk/git/youdo.business` was inspected; no repository edits. Exact latest sampled CI revision `2e21469a4efd4421c3ed6bc1c705161dd57d5f5e` was inspected using git show.

## Actions
Queried GitLab GET endpoints for latest MR/push pipelines and all job pages, including retries; selected the latest three pipelines containing gates among the latest ten candidates. Collected sanitized cache excerpts in `~/ai-data/nexus-usage/recent-business-gates.json` using `check_recent_business_gates.py` in the same directory. No raw traces or credentials saved.

## Findings
All six gate jobs on November 5 succeeded, restored a remote archive (`Successfully extracted cache`) and uploaded an archive (`Created cache`). All ran on runner 108; cross-runner reuse is untested in this sample.

| Pipeline | Business job / npm ci | Employee job / npm ci |
| --- | --- | --- |
| 142350 | 3276834 / 19s | 3276835 / 15s |
| 142349 | 3276706 / 17s | 3276707 / 13s |
| 142347 | 3276556 / 18s | 3276557 / 19s |

Every job checks and writes the identical effective cache key `0_YouDo-1f83f2f9319d9627fb7afaa62f5b9dfe4f4da81b-1-non_protected` in project 423. Business archives only `YouDo.Business.Web/spa/.npm`; employee archives only `YouDo.Business.EmployeeSpace.Infrastructure.Web/spa/.npm`. Logs confirm distinct contents (approximately 3300 versus 3016 matching entries) and changing ETags at the same object path. The shared destination and different configured archive paths are verified. Inference: the jobs overwrite one another with archives that may lack the other gate cache; extraction success alone therefore does not establish useful npm reuse. Why distinct lock-file definitions produce this effective key is not diagnosed.

The traces do not enable npm HTTP logging. Package counts printed by npm ci (713 Business, 654 employee) are installed packages, not verified network-download counts. Nexus request counts were not measured in this follow-up; zero downloads cannot be claimed.

Evidence: [latest Business job](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3276834), [latest employee job](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3276835), [pipeline142349](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/pipelines/142349), [pipeline142347](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/pipelines/142347).

## Changes
Knowledge-base evidence only. No repository, CI configuration, pipeline, cache object or remote service was changed.

## Status and risks
The cache transport works in the sample, but shared-key archive interference remains. DevOps-904 Business gates optimization in `~/ai/TODO.md` remains open. A distinct prefix per gate is a proposed minimal isolation change, subject to repository/publication approvals; it is not implemented. Further verification should measure actual npm/Nexus requests and cross-runner reuse. All diagnostic commands completed; no background operations remain.

## Approved local implementation (2026-11-05)

After the diagnostic, the user requested separating the npm caches. First-gate proposal: repository `youdo/microservices/youdo.business`, new branch `DevOps-904-split-business-gates-npm-cache`, base `origin/master` (`e174f972f`). User explicitly approved this proposal with `Да`. The existing checkout was clean before switching; no worktree was created.

Applied exactly two additions to `.gitlab-ci.yml`: `cache.key.prefix: business-web-npm` for `business-web-gates`, and `cache.key.prefix: employee-space-web-npm` for `employee-space-web-gates`. Existing lock-based key inputs, cache paths and job execution remain unchanged. `git diff --check` passed. Local YAML parsing and structural comparison against HEAD confirmed that only these two prefixes differ. No GitLab CI Lint API call or runtime pipeline verification was performed.

Result: the requested separation is prepared locally, uncommitted and unpublished. No commit, push, MR, merge, cache manipulation, pipeline trigger or deployment was performed. The DevOps-904 Business gates action in `~/ai/TODO.md` remains open pending reviewed publication and runtime verification; the historical diagnostic limitations above still apply. Publication still requires the second supervised approval with actual diff, checks, names and CI effects. All task commands completed; no background operations remain.

## Publication proposal prepared (2026-11-05)

The user requested preparing an MR. Reviewed the complete tracked diff and index: only two added prefix lines in `.gitlab-ci.yml`, no staged or unrelated changes. Local YAML structural comparison and diff whitespace checks pass. Fresh GitLab CI Lint returns `valid=true`, empty errors/warnings; this was validation only, not a pipeline execution. GitLab inspection found no existing MR for the proposed branch; default target is `master`, squash default on, source deletion enabled, assignee `a.solonenko`.

Proposed commit `split npm caches for business gates`; ready MR title `DevOps-904 split npm caches for business gates`; source `DevOps-904-split-business-gates-npm-cache`, target `master`. Exact Russian description, proposal and immutable state snapshot are stored under `~/ai-data/gitlab-workflow/DevOps-904/youdo.business/gates-cache/`. Snapshot comparison initially encountered an older record in the parent directory and safely refused to overwrite it; a separate gates-specific record was then captured successfully.

CI effects inspected: refreshed shared templates `origin/master` to `ef12833`; relevant rule/build/release files have no differences from the inspected local versions. MR runs the two gates (CI file matches their change rules), .NET tests and standard service-image builds/pushes to the project registry. Dev/test deployment and autotests stay manual. Production deployment/release rules require master/tag context and do not apply to this MR. New prefix keys initially create cold caches. Preparation grants no merge or deployment permission.

Second publication approval is pending. Nothing staged, committed, pushed or created remotely. DevOps-904 remains open for publication and runtime validation. No background operations remain.

## Approved publication completed (2026-11-05)

The user explicitly approved the presented publication bundle with `Да`: task-only staging, commit, branch push and ready MR creation, including the disclosed CI image-build/push effects. Snapshot check matched before staging. Inspected the complete staged patch: exactly two prefix additions, no other files. Created commit `05580fcf342639830a957c182a461776ee0ddfdd` (`split npm caches for business gates`) and verified its diff against the reviewed change. Pushed the source branch without force.

Published ready [MR3918](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/merge_requests/3918), title `DevOps-904 split npm caches for business gates`, source `DevOps-904-split-business-gates-npm-cache`, target `master`, assignee `a.solonenko`, squash on and source deletion on merge enabled. The agreed description and full commit SHA were independently verified. No merge, manual job execution, release or deployment performed. Worktree/index are clean.

Sandbox DNS prevented the first push and API attempt. Retried the push with approved network access; before retrying MR creation, read-only verification confirmed that no open MR existed. Creation then returned `write_state=created`, `verified=true`; an independent verify returned `write_state=not_requested`, `verified=true`. No duplicate MR was created.

Latest observed [pipeline142389](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/pipelines/142389) is `running`. Pipeline success, distinct runtime keys, cold/warm behavior and Nexus savings remain unverified. The existing DevOps-904 Business gates TODO remains open with publication progress recorded. Publication work is complete; all local task commands finished. Remote GitLab CI continues and can be checked or canceled through the linked pipeline; no automatic cancellation or additional infrastructure action is authorized.

## Pipeline verification (2026-11-05)

User requested checking pipeline jobs and the next plan. Read-only GET of pipeline142389 and every jobs page (including retries) shows `success`: 13successful jobs (9builds, .NET unit tests, both frontend gates, set-variables), 113manual jobs and2skipped jobs; zero failed/running jobs. MR3918 is still `opened`, `mergeable`, not merged. Sanitized aggregate: `~/ai-data/nexus-usage/business-gates-142389.json`.

Runtime key separation is now verified: [Business3278028](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3278028) checks/creates `business-web-npm-1f83f2f9319d9627fb7afaa62f5b9dfe4f4da81b-1-non_protected`; [Employee3278029](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3278029) checks/creates `employee-space-web-npm-1f83f2f9319d9627fb7afaa62f5b9dfe4f4da81b-1-non_protected`. Both first lookups report `WARNING: file does not exist` and `Failed to extract cache`, consistent with new keys. Both then upload their separate archives and report `Created cache`. npm ci takes17seconds/713installed packages for Business,13seconds/654installed packages for Employee; those package counts do not measure downloads. Both jobs use runner108. Earlier running/key-unverified statuses above are superseded by these observations.

Next proposed validation is a separately authorized retry of only these two gates with unchanged inputs, checking exact key matches, successful extraction and preservation of separate archives. Actual Nexus requests must be measured separately before claiming savings. Cross-runner reuse is still untested. After warm validation, merge remains a separate user decision; this project automatically deploys production from master, so merging requires explicit approval covering that effect. Protected master caches use a separate partition and may initially be cold. Central DevOps-904 remains open pending these verifications. No jobs retried, MR merged or external state changed during this check. All task commands finished; pipeline142389 has no running jobs and no task background operations remain.

## User-authorized warm retries started (2026-11-05)

After the explicit proposal to retry only the two gates, the user instructed `Запусти повторно`, authorizing both job retries. Preflight GET verified pipeline142389SHA05580fcf342639830a957c182a461776ee0ddfdd and that the latest matching gate jobs were the previously successful3278028/3278029. Performed exactly two POSTs to their retry endpoints, with no automatic retries.

Created [Business3278746](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3278746) and [Employee3278747](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3278747). Both were initially pending; independent GET then confirmed both running on runner108. At that observation their traces had not reached cache restoration. Pipeline142389 is running again due to these retries; the previous13successful jobs remain historical evidence. MR3918 remains open and mergeable. No other jobs were triggered and no merge/deployment performed.

Receipt: `~/ai-data/nexus-usage/business-gates-142389-retry-receipt.json`; observed state: `~/ai-data/nexus-usage/business-gates-142389-after-retry.json`. Warm-cache extraction and completion remain pending. Local commands completed; the two remote GitLab jobs continue. Their linked job pages show status and offer cancellation; this check does not authorize cancellation or another retry. DevOps-904 remains open.

## Warm retry results verified (2026-11-05)

Read-only follow-up confirms both retries successful: Business3278746 and Employee3278747 each report `Successfully extracted cache`, then upload their distinct prefix archive and report `Created cache`. Business npm ci is10seconds versus17seconds in the initial cold run; Employee7seconds versus13seconds. Both use runner108, unchanged inputs and the separate keys recorded above. Warm extraction and separate archive persistence are verified on this runner; no exact Nexus download counts or cross-runner reuse were measured. Evidence: `~/ai-data/nexus-usage/business-gates-142389-warm-result.json`.

Pipeline142389 is SUCCESS again; its include-retried inventory has15successful job records,113manual and2skipped, with no running/failed jobs. MR3918 remains open/mergeable and was not merged. This supersedes pending/running warm-retry observations above. Central DevOps-904 retains cross-runner verification, measured Nexus savings and merge decision as remaining actions. All task commands finished; no task background operations remain.

## Nexus request counts verified (2026-11-05)

User requested measuring Nexus requests. Read GitLab trace section epochs for the initial jobs3278028/3278029 and warm retries3278746/3278747, then ran a read-only SSH counter on Nexus10.18.24.233 against `/data/nexus/nexus-data/log/request*log*`. Counter keeps both gates grouped because their installs overlap. No per-job division is claimed.

Initial install union `[17:53:38,17:54:44)` Moscow: **1367 npm requests**, all `GET200` tarball downloads, agent `npm/12.0.2 node/v26.9.0 linux x64 workspaces/false ci/gitlab-ci`. These occur only17:53:42–17:53:51. There are853distinct method/path/status combinations and514repeats, consistent with overlapping dependencies downloaded into the two independent cold caches. This is a combined time-window/client measurement; the shared gateway prevents an independent server-side job identifier. The two job install summaries total1367packages (713+654), corroborating the cold-window attribution without treating those summaries as network measurements themselves.

Warm first-minute union `[19:37:04,19:38:04)` has **zero npm requests**. More strongly, the complete combined warm script interval `[19:37:04,19:48:14)` has **zero requests to any npm repository, from any client**. Other repositories receive328requests in that full interval (maven-public316, raw10, raw-private2), so this does not mean Nexus was idle. Full cold script window contains unrelated legacy Node8npm traffic and other clients, which are excluded from the initial-install comparison.

Logging completeness was explicitly checked: zero parse failures; the known disk-full log interruption is between18:52:58 and19:16:41, outside both measurement intervals. All warm minutes contain server records, and the latest retained record is20:44:16. Zero warm npm is therefore supported by functioning server logging, not inferred from the earlier log gap. Raw request rows/credentials were not saved.

Artifacts under `~/ai-data/nexus-usage/`: `business-gates-nexus-windows.json`, `business_gate_windows.py`, `business_gate_count_remote.py`, `business-gates-nexus-counts.json`. Result: warm reuse eliminated1367npm requests versus the measured initial installation window (100percent reduction for this cold/warm pair). This does not establish sustained busy-day savings or cross-runner behavior. MR3918 remains open in the latest prior observation; no merge, deployment or further retry performed. Central DevOps-904 retains cross-runner verification, merge decision and longer-term measurement. SSH/API commands finished; delegated method review completed; no task background operations remain.

## Task comment draft prepared (2026-11-05)

User requested a task-comment draft following the latest DevOps-904 comment and covering earlier Business repository changes too. Read-only YouTrack GET found latest comment `74-125202`: three Russian bold labels for repository, changes and effect, describing Android MR1163. Prepared the same three-paragraph format for Business MR3863 and MR3918. Draft payload: `~/ai-data/gitlab-workflow/DevOps-904/youdo.business/gates-cache/youtrack-business-result-comment.json`.

The text covers the earlier internal-api backend-template/BuildKit NuGet change and current independent npm prefixes. Reports internal-api125.7to24.6seconds (80.4percent faster), zeroNuGet in its repeat interval, and combined frontend-gates1367to0npm requests for the measured warm comparison. Does not present the initial377NuGet requests as isolated internal-api traffic, because that window overlapped other builds. Does not claim sustained daily savings. Draft only: no YouTrack comment created/updated, no merge or pipeline action performed. Existing DevOps-904 implementation/validation remainder is unchanged. No task background operations remain.

## Task comment wording correction (2026-11-05)

User requested removing the earlier/later framing and build duration, retaining only request-count reduction as the effect. Updated the existing draft payload accordingly: describes both Business changes without chronology, reports combined frontend-gates1367to0npm requests (100percent reduction). No isolated internal-api cold count is invented. This task-specific wording supersedes the draft description above; no global rule inferred. No external comment write or background operation performed.

## Task comment request-count wording (2026-11-05)

User requested showing377to0for internal-api. Updated the existing unpublished draft to explicitly describe the internal-api build windows (377to0NuGet requests), alongside1367to0npm requests for both frontend gates. The377baseline remains an aggregate containing parallel builds; this wording does not establish isolated internal-api savings. Supersedes the prior draft wording without changing the measurement evidence, TODO scope or external permissions. No comment published; no background operations.

## Approved task comment published (2026-11-05)

After reviewing the final three-paragraph Markdown draft, the user explicitly requested adding the comment with the same Markdown formatting. Checked existing DevOps-904 comments for an exact duplicate, found none, then created comment `74-125203`. Independent readback exactly matched all490characters. Text covers Business MR3863/3918, describes the two cache changes without chronology/timing, reports377to0NuGet requests in internal-api build windows and1367to0npm requests for both gates, with100percent for each. The aggregate377baseline attribution limitation remains in the evidence above.

Receipt: `~/ai-data/gitlab-workflow/DevOps-904/youdo.business/gates-cache/youtrack-business-result-comment-receipt.json`. This supersedes the unpublished draft status above. Only the authorized comment was added; no issue fields, MR, pipeline or infrastructure changed. Central DevOps-904 implementation/verification remainder is unchanged; no new follow-up action created. All commands completed, no task background operations remain.

## MR links corrected in the last two comments (2026-11-05)

User identified plain-text MR numbers in the last two DevOps-904 comments and explicitly requested fixing both. Cause: the drafted repository paragraphs used bare MR numbers and the publication/readback check verified exact text rather than the presence of Markdown links. Applied the agent-learning workflow as a task-specific correction; this is not a new global permission or unrelated-content change.

Read both current comments and verified each MR through GitLab GET before updating existing YouTrack comment text in place. Comment74-125202now links [MR1163](https://gitlab.youdo.sg/youdo/Test/youdo-android-testing/-/merge_requests/1163); comment74-125203now links [MR3863](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/merge_requests/3863) and [MR3918](https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/merge_requests/3918). Only the MR-reference substrings changed; formatting and all other wording were preserved. Both independent readbacks exactly matched the prepared payloads. No new comments were created.

Evidence, before snapshots and per-comment verified receipts are under `~/ai-data/gitlab-workflow/DevOps-904/comment-mr-links/`; the Business local payload was refreshed to match the linked text. For these task comments, keep MR references as explicit Markdown links and verify their actual URLs as well as exact text. Implementation TODO remainder is unchanged; no merge, pipeline or issue-field changes. All commands finished; no task background operations remain.

## Portable lesson
None.

## User merge confirmed (2026-11-05)
User reported merging Business. Independent read-only GET confirms MR3918merged into master at21:06:43MSK by a.solonenko, source05580fcf3426, merge7efa6508a733a7e80320c2d16eacd037f7745af4, squash e2d91aae3a9df95e8bec9e27852f34cd1f86e85a. This supersedes earlier open/unmerged status. Post-merge pipeline GET timed out; completion/runtime not verified. Existing cross-runner/sustained effect remains open in central TODO; merge step is complete. Receipt `/home/slnnk/ai-data/nexus-usage/devops-904-merge-status.json`. No remote mutation/agent merge or background operation.
