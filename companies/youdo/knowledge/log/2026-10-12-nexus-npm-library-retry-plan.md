---
system: nexus
status: verified
checked: 2026-10-12
tags: [nexus, npm, gitlab-ci, recovery]
---
# npm library restoration through existing GitLab jobs

## Summary

User identified youdo/microservices/youdo-core-frontend-tools as the library source and proposed retrying GitLab jobs. Read-only investigation prepares exact npm job retries; no publication/retry is authorized or performed yet. Current CI credential is already restored. Existing npm publication job is deploy lib; job named publish uploads Storybook to S3 and is outside library-only scope.

## Task and context

Restore the four internal package families at versions requested by current Business and Business landings master. Sources and prior Nexus configuration: [npm plan](2026-10-12-nexus-npm-recovery-plan.md), [applied infrastructure and CI token](2026-10-12-nexus-npm-recovery-applied.md). User prefers retrying existing jobs first, investigating actual failures and checking package metadata without tarball downloads.

## Actions and findings

Read-only project496 API GETs enumerate existing jobs and tags. No tags exist. Scanner ~/ai-data/nexus-recovery/inspect_npm_publish_jobs.py fetched12pages/1200job records, filtering634 deploy lib/publish jobs, including39successful master deploy lib jobs from2025-12-17 through2026-10-07. Sanitized list npm-publish-jobs.json. Latest npm job3213538 belongs to pipeline140392, SHA27f5e03c13ab1817b6f2f6191459d8901ab15c84. No raw trace stored. Latest trace GET200 contains zero bytes, so trace cannot verify historically published versions.

Local checkout remains clean on existing branch; stale origin/master is insufficient for selecting current-version jobs. Source package manifests at pinned pipeline commits are needed to map jobs to requested versions. deploy lib builds npm libraries and publishes workspaces; unrelated publish job performs Storybook S3 upload. Avoid whole-pipeline retry.

## Execution boundary and changes

Read-only investigation, sanitized local helper/results and this log. No repository edits, branch changes, npm install, library publish, CI retry, S3 write or deployment. Concrete job selection will be presented before API POST retry as required by user AGENTS.md. No secrets persisted in evidence. Backlog remains in ~/ai/TODO.md.

## Portable lesson

None.

## Initial pinned-source job matches

Successful master deploy lib job3197313/pipeline139919/SHA56839068af528419a799f1fb2c87d5516b7bb3ea contains UI0.39.0, eslint2.1.0, prettier0.0.1 and cursor-extension1.0.0 in pinned workspace manifests. Job2775626/SHAba81439e (full SHA in sanitized evidence) contains UI0.23.3, eslint2.0.14, prettier0.0.1 and cursor-extension0.0.3. Repeating these jobs includes their sibling workspace versions, not only one missing library. Optional older local Business references can map to job3135243 for UI0.34.0 and3064679 for UI0.30.1; these are outside the current-master priority.

All39examined master deploy lib traces returned200 with zero bytes. Versions above are pinned source versions, not inferred from empty traces. Evidence ~/ai-data/nexus-recovery/npm-deploy-job-versions.json. Older job search is needed for Business landings UI0.17.5/eslint1.2.5.

## Concrete existing-job execution proposal

Extended read-only inventory24pages through2025-04-22:1060filtered jobs,39successful master deploy lib,22failed,39manual,1canceled,1skipped. No successful master job in inspected history carries UI0.17.5/eslint1.2.5. Existing manual job2640279 at SHA924dacb3f08e09e17b462682e88ea30557c5bef8/pipeline126026 contains both versions. It needs play (first execution), not retry. Minimal current-master recovery proposal in oldest-to-newest order:

| Action | Existing job | Pinned package versions |
| --- | --- | --- |
| play |2640279| UI0.17.5 and eslint1.2.5 |
| retry |2775626| UI0.23.3, eslint2.0.14, prettier0.0.1, cursor-extension0.0.3 |
| retry |3197313| UI0.39.0, eslint2.1.0, prettier0.0.1, cursor-extension1.0.0 |

Both retries are historical successful master deploy lib jobs; no S3 Storybook publication is requested. Selected pinned CI has dependencies:[] and performs its own install/build, no expired artifact dependency. Old manual2640279 CI has no explicit npm login/auth directive;2775626 legacy npm-cli-adduser uses NPM_NEXUS_USER/NPM_NEXUS_PASS whereas3197313 uses NPM_TOKEN. Variables used by legacy jobs need actual execution/failure inspection; compatibility is not assumed from the new token alone. Retry-first remains user preference, do not rebuild or edit CI in anticipation of failures.

npm publish --workspaces includes sibling versions in table. Both retry jobs include prettier0.0.1, so ALLOW_ONCE may reject duplicate publication; actual metadata must determine recovered targets even if a job exits nonzero. Use oldest-to-newest order to reduce latest-tag downgrade, and verify final relevant metadata/dist-tags rather than claiming source manifests prove published availability. No package downloads. No job retry/play performed; explicit execution approval required under AGENTS.md external-write rule. Evidence files npm-publish-jobs.json, npm-deploy-job-versions.json and agent-generated pinned manifest mappings under ~/ai-data/nexus-recovery/.

## Explicit execution approval and first launch

User approved the reviewed three-action plan: play2640279, retry2775626, retry3197313, oldest-to-newest, library-only scope. Local helper run_npm_recovery_jobs.py guards exact job/name/master identity and duplicate launch, persists only sanitized returned job IDs, and GET-checks hosted metadata without tarball downloads. POST /projects/496/jobs/2640279/play returned201; job2640279 entered running. Initial metadata shows all six requested version pairs absent. Remaining two approved retries will follow after terminal status; no separate retry scope or full pipeline/Storybook trigger is inferred.

## Actual execution results and corrected publication scope

All three approved actions executed in the agreed sequence. Manual2640279 failed after98.56s: npm install/build:lib passed, npm publish --workspaces returned ENEEDAUTH because pinned CI has no npm authorization setup. No reusable build archive exists. Retry2775626 created3219284, success61.97s, published only @youdo/ui0.23.3. Retry3197313 created3219285, success45.08s, published only @youdo/ui0.39.0.

Important correction to the proposed scope: both historical deploy lib jobs cd into packages/ui before npm publish --workspaces. Actual traces contain only UI publication; the earlier assumption that these jobs publish all workspace siblings was wrong. Source manifests alone are not evidence of the effective publication working directory. New job successes do not restore cursor/config packages. Earlier all-workspaces/duplicate-prettier warnings were based on that incorrect scope and do not describe these actual jobs.

Final hosted metadata GETs verify UI0.39.0 (and incidental UI0.23.3). Remaining requested pairs absent: UI0.17.5, eslint1.2.5/2.1.0, prettier0.0.1, cursor-extension0.0.3. No tarball downloaded. Evidence npm-recovery-job-runs.json, npm-recovery-version-status.json and npm-recovery-diagnostics.json under ~/ai-data/nexus-recovery; no raw traces or credentials persisted. Dedicated package publishing jobs and a minimal old-job auth fix need read-only identification and separate approval before more external writes/retries.

## Follow-up authentication and dedicated-job proposal

Prepared secret-free npm-userconfig-plan.json: project496 file variable NPM_CONFIG_USERCONFIG, scope*, rawtrue, protectedfalse/maskedfalse, containing a registry-scoped _authToken=${NPM_TOKEN} reference for npm-private. Project variable is absent. This would provide authorization to old2640279 without source edits; a new variable creation and additional retry require explicit approval. Old UI publication would change latest, so restoring UI latest to0.39.0 must be included in any execution approval. Nothing applied.

Read-only search of1200projectjobs found84dedicated config jobs and no cursor/extension jobs. ESLint2.1.0 has existing successful master job3043068/pipeline136023/SHA54c3b56d (full source SHA in npm-config-job-candidates.json) as possible additional retry. Prettier0.0.1 source jobs in inspected range are MR refs; publication versioning must be checked before treating them as stable0.0.1 restoration candidates. This updates the earlier conclusion that no existing config jobs are available: the three selected UI pipelines have none, but other pipelines do. No extra job was started.

## Dedicated-job verification complete

Retry3043068 is confirmed master ESLint2.1.0. Manual3213529 (MR178) can publish stable Prettier0.0.1: its three package blobs README/index.js/package.json match the inspected master snapshot, and package deployment script preserves package.json version, choosing alpha only when version contains a hyphen. No automatic branch prerelease mutation exists in this job. These two actions, auth-file variable creation, retry2640279 and restoring UI latest0.39.0 are a concrete follow-up proposal awaiting approval. ESLint1.2.5/cursor0.0.3 remain historical-source publication gaps, with no existing dedicated job identified in inspected scope. No follow-up action performed.
