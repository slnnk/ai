---
system: nexus
status: verified
checked: 2026-10-15
tags: [nexus, npm, gitlab-ci, recovery]
---
# UI 0.26.0 and 0.25.4 CI recovery inspection

## Summary

Both requested `@youdo/ui` versions are now locally rebuilt from pinned historical sources and published after explicit user authorization. Independent final Nexus metadata GET confirms0.25.4 and0.26.0 present, latest0.40.1 unchanged and recovery0.26.0. Earlier GitLab retries remain failed because current npm rejected implicit latest publication. No repository source change, policy change or package verification download occurred.

## Task

Assess whether missing `@youdo/ui@0.26.0` and `@youdo/ui@0.25.4` can be rebuilt through GitLab CI after Nexus recovery.

## Context

Producer: GitLab project 496, `youdo/microservices/youdo-core-frontend-tools`; local checkout `/home/slnnk/git/youdo-core-frontend-tools`. Prior recovery credentials and `NPM_CONFIG_USERCONFIG` variable were restored; see [previous recovery](2026-10-12-nexus-npm-library-restoration.md).

## Actions

Initial inspection read previous recovery maps/logs and sanitized job/source inventories. Queried current npm-private metadata and historical GitLab jobs, pinned UI manifests and CI definitions using GET requests only. Relevant existing helpers/evidence are `~/ai-data/nexus-recovery/inspect_npm_publish_jobs.py`, `npm-deploy-job-versions.py`, `npm-publish-jobs.json` and `npm-deploy-job-versions.json`. Later authorized retries are recorded below. No repository edit, install or Git mutation occurred.

## Findings

Current hosted metadata contains UI versions 0.17.5, 0.23.3, 0.39.0 and 0.40.1, with latest 0.40.1. Both requested versions are absent.

| UI version | Historical deploy lib job | Pipeline | Ref/status | Pinned SHA |
| --- | --- | --- | --- | --- |
| 0.26.0 | [3010368](https://gitlab.youdo.sg/youdo/microservices/youdo-core-frontend-tools/-/jobs/3010368) | 135015 | master/success | acde6a70e50237d994f2ca20ec3dab4b671bc25f |
| 0.25.4 | [2981316](https://gitlab.youdo.sg/youdo/microservices/youdo-core-frontend-tools/-/jobs/2981316) | 134326 | master/failed | 78dedc7f3f4469a85a2e9371ba44099910887150 |

Pinned `packages/ui/package.json` verifies the requested version at each SHA. Both CI definitions use fresh `npm install`, `build:lib`, `dependencies: []` and `npm publish --workspaces` with default latest. Job2981316 trace GET returns HTTP200 with zero bytes, so its original failure cause is unavailable. Current builds remain untested; a retry is not guaranteed to succeed. Retry only individual `deploy lib` jobs: the separate `publish` job uploads Storybook to S3.

Historical source rebuilds may differ from original tarball bytes, as observed for prior restored UI versions; a published version does not prove compatibility with existing lockfile integrity. Historical default-latest publication can replace latest 0.40.1 with an older version. Prior direct dist-tag updates failed with HTTP400; any latest restoration workaround requires its own reviewed scope. Current latest must be rechecked before execution.

## Changes

Local changes: this log, a minimal update to the existing Nexus map, generated current index, sanitized helper/evidence and sync notes. External changes: only the two explicitly authorized job retries recorded below; no latest write or runner change.

## Execution boundary

Initial investigation performed no external writes. The user subsequently explicitly instructed: “Перезапусти, ты сможешь потом latest переключить обратно?” This authorized the two job retries; the latest restoration question was not treated as separate authorization for further external mutations.

## Authorized retries and queue state

POST `/projects/496/jobs/3010368/retry` created job3228457 for UI0.26.0; POST `/projects/496/jobs/2981316/retry` created job3228458 for UI0.25.4. Both remain pending after approximately100seconds, runner null, tags `docker`. Project runners105/106 are online and unpaused, tagged `docker,dind`, access_level `not_protected`. No missing eligible tag was demonstrated; the queue cause remains unknown. No runner or queue intervention was authorized or performed.

The latest metadata GET still has latest0.40.1 and neither requested version. This is a queued recovery attempt, not a completed library restoration. Local helper `~/ai-data/nexus-recovery/ui_0260_0254.py` provides `--retry ORIGINAL_ID` and status operations; sanitized evidence is `ui-0260-0254-before.json` and `ui-0260-0254-runs.json` in the same directory.

## Latest restoration options and limits

No0.40.1 archive exists among inspected recovery artifacts (files through depth3). Existing UI archives are original0.39.0 and rebuilt0.17.5. Prior HTTP400 failure affected the internal hosted endpoint `/repository/npm-private/-/package/@youdo%2Fui/dist-tags/latest` and stock `npm dist-tag add`; an alternate public URL is not an established fix. This evidence does not prove universal failure for every Nexus endpoint or version.

After jobs terminate, recheck metadata first. If latest remains0.40.1 no restoration is required. A metadata-only `npm dist-tag add @youdo/ui@0.40.1 latest` against hosted would require explicit write approval and may fail as before. The proven prior workaround uses identical package bytes, temporary ALLOW, republish and ALLOW_ONCE restoration, but0.40.1 bytes are unavailable locally. Obtaining them would require an explicitly approved exception to the user's metadata-only/no-package-download preference. Rebuilding and overwriting0.40.1 could change existing integrity and is not an equivalent safe restoration. No latest write or package download performed.

## Terminal retry results

On the user's subsequent status-check request, live GETs show job3228457 failed `script_failure` after64.56seconds and job3228458 failed `script_failure` after39.94seconds. Both reached npm packing (516files) and then failed with the same publication guard:

```text
Cannot implicitly apply the "latest" tag because previously published version0.40.1 is higher than new version0.26.0/0.25.4. You must specify a tag using --tag.
```

The version strings above combine the equivalent errors from the two jobs. Hosted metadata confirms neither requested version exists and latest remains0.40.1. This supersedes the earlier risk assumption that these exact retries would necessarily downgrade latest: the currently used npm client blocks their implicit latest assignment before publication. The recovery is unsuccessful; the build reached packing, but publication did not complete.

A concrete next correction is an explicit non-latest publication tag such as `--tag recovery`. No repository/CI edit, new retry or tag mutation has been made or authorized for this correction. No latest restoration is currently needed. No new backlog item was created for the status-only request.

## Approved local rebuild and publication completed

The user subsequently explicitly requested local build and publication of both versions. Scratch sources from archives pinned to the SHAs above are under `~/ai-data/nexus-recovery/ui-local-0260-0254/{0.26.0,0.25.4}`. Local helpers `ui_local_recovery.py` and `ui_local_run.py` prepare sources and perform install/build/pack/publication. The repository checkout and Git state were untouched.

Build container `node:24.13.0`, npm11.6.2, user1001 used the Nexus npm group for `npm install --ignore-scripts --no-audit --no-fund`, matching CI's install rather than imposing npm ci. Original `build:lib` command `tsc && vite build && node scripts/build-codemods.mjs` exited0 for both, with no TypeScript diagnostics. Comparison with original source archives confirms only scratch `package-lock.json` changed during npm install; all other original source files remained unchanged.

Both packed archives contain516files. Main, module, types and codemod entry points were checked, along with absence of `.npmrc`, `.env` and key filenames.

| Version | Packed bytes | SHA256 |
| --- | --- | --- |
| 0.25.4 | 2419434 | 2d4a504e4e29d6b5be8553407c72212f434564c328a419ebbbf2b1b0df37380a |
| 0.26.0 | 2420644 | e373a9d35857c04830f00aeae785e144192d150d71a23b16ccbe222d2c55f987 |

Published0.25.4 first, then0.26.0, with explicit `--tag recovery --ignore-scripts` and guards refusing version overwrite. Each publication's metadata SHA512 matches its local archive, and prior versions' dist metadata remains unchanged. Evidence files `{version}-published.json` are in the scratch root. An independent final metadata GET confirms both versions present, latest0.40.1 preserved and recovery0.26.0.

No latest restoration or repository write-policy mutation was needed. No package was downloaded for verification; old GitLab jobs remain failed and were not retried again. Historical consumer lockfile integrity has not been checked, so these rebuilds are not claimed byte-identical to the lost historical packages. No hypothetical consumer-failure TODO was added.

Final independent metadata GET verification confirms both versions and matching local SHA512 through both `npm-private` and the `npm` group, with latest0.40.1 in each; sanitized evidence is `~/ai-data/nexus-recovery/ui-local-0260-0254/final-verification.json`.

## Requested recovery task comment update

The user explicitly requested updating the Nexus recovery task comment. DevOps-890 comment74-124640 was updated by replacing only its npm bullet; all other text was preserved. The npm bullet now includes0.25.4/0.26.0, local builds from original sources with typecheck/Vite/codemods, hosted/group metadata SHA512verification, latest0.40.1 and recovery0.26.0, the failed CI implicit-latest cause and the unverified historical consumer lock integrity. POST succeeded and an independent GET verified exact comment text. Evidence in `~/ai-data/nexus-recovery/ui-local-0260-0254/`: `youtrack-comment-before.json`, `youtrack-comment-proposed.txt` and `youtrack-comment-result.json`. No additional external writes were performed.

## Portable lesson

none
