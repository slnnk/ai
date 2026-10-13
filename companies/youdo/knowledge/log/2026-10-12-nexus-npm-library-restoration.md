---
system: nexus
status: verified
checked: 2026-10-12
tags: [nexus, npm, recovery, gitlab-ci]
---
# npm libraries restored through CI and historical local builds

## Summary

User explicitly approved supplemental authentication, existing UI/ESLint/Prettier jobs, UI latest restoration, and local build/publication when jobs are unavailable. Auth file variable applied and verified. Prettier0.0.1 CI publication completed; historical ESLint1.2.5 and cursor-extension0.0.3 locally built and published with metadata verification. UI0.17.5 and ESLint2.1.0 jobs completed after waiting for shared runners. Local rebuilt integrity differs from existing consumer lockfiles; package presence alone does not prove npm ci compatibility.

## Context and authorization

Follow-up to [original job executions and diagnosis](2026-10-12-nexus-npm-library-retry-plan.md). User instruction authorizes planned supplemental actions and local build/publication without further prompts. Existing service/producer checkout and Git history remain untouched. Scratch builds and sanitized scripts/results in ~/ai-data/nexus-recovery.

## Actions

Created project496 file variable NPM_CONFIG_USERCONFIG: scope*, rawtrue, protectedfalse/maskedfalse, secret-free value references existing NPM_TOKEN at npm-private auth scope. POST/GET validated payload; credentials not copied into scripts/logs. Helper continue_npm_recovery.py.

Started retry2640279->3219467 (UI0.17.5), retry3043068->3219468 (ESLint2.1.0), play3213529 (Prettier0.0.1). Prettier job succeeded27.26s, actual npm success line and hosted metadata verified. UI/ESLint initially pending with docker tag, eligible instance runners105/106 online/active but all slots occupied by NuGet restoration jobs. No runner reconfiguration or other-job cancellation.

Local ESLint1.2.5 from historical SHA924dacb3f08e09e17b462682e88ea30557c5bef8: original version preserved, plain index.js config requires no build dependencies. Packed artifact npm-local-build/artifacts/youdo-eslint-config-1.2.5.tgz, SHA256737e3d5c81c65dec5009adcce5d2af0c4c224c95eb2bb85a802b6a0c48b1a432.

Local cursor-extension0.0.3 from pinned GitLab archive SHAba81439efca9e2fccad6516b074bd6626041100e. Original source/version/lock untouched. Isolated public-npm toolchain pins direct build/runtime dependency versions from historical lock; transitive dependencies separately resolved. Dependency lifecycle scripts disabled, explicit TypeScript compile/esbuild/VSIX prepack succeeded, IDE postinstall never executed. Packed artifact npm-local-build/artifacts/youdo-cursor-css-vars-extension-0.0.3.tgz, SHA256d3092deba64bca36599a8168d4d7c629097d13066bad3717368320fb18e9224e. Parent verified main dist/extension.js, dist/install/postinstall.js and embedded artifacts/youdo-css-vars.vsix with extension identity0.0.3 and18ZIP entries.

Published both approved tarballs using publish_local_npm.py with strict name/version guard, npm publish --ignore-scripts, npm-private scoped auth via runtime env and a credential-reference userconfig. Actual secrets only in current/.env or runtime env, not helper/userconfig/records. Hosted metadata confirms both exact versions. Existing versions are never overwritten. Verification downloaded no published tarballs.

## Integrity verification and limits

Read-only npm metadata integrity comparison against local consumer lockfile inventory finds rebuilt ESLint1.2.5 and cursor0.0.3 have different SHA512integrity than locked historical artifacts. Evidence npm-rebuilt-integrity-check.json. This is a byte-identity mismatch; successful version publication is not proof of restoring installations that enforce old lock integrity. A separately reviewed lock refresh or original artifact restoration is needed before claiming npm ci compatibility. No consumer lockfile modified, no service install/build performed.

## Changes and evidence

GitLab auth file variable, three approved supplemental job starts, two npm hosted publications; local artifacts/helpers/sanitized metadata results; KB records. npm-supplemental-runs.json, npm-local-publications.json, npm-local-build/npm-local-build-results.json, npm-rebuilt-integrity-check.json. No Git mutations, source edits, Storybook S3 deployment, runner changes, package verification downloads or IDE installation.

## Portable lesson

None.

## Final publication results

All six requested version pairs are present via hosted metadata GET: UI0.17.5/0.39.0, ESLint1.2.5/2.1.0, Prettier0.0.1, cursor-extension0.0.3. Supplemental UI3219467 succeeded88.24s and ESLint3219468 succeeded19.12s; actual publish traces confirm names/versions and old UI auth file variable worked. No queued job was canceled. UI0.17.5/ESLint2.1.0 backup artifacts were prepared/entry-point-checked while waiting but not published; use CI results instead.

Final metadata integrity matches old locks for ESLint2.1.0 and Prettier0.0.1. Actual mismatches, with integrity field present, are UI0.17.5/0.39.0, ESLint1.2.5 and cursor0.0.3. No claim of npm ci compatibility for those old locks. Evidence npm-final-metadata-verification.json.

## Remaining UI latest limitation and concrete proposal

Current UI latest=0.17.5 after the historical CI publication. Direct tag API and stock npm dist-tag add both return400 Unable to update latest tag. Nexus logs do not prove deployment policy is the cause; do not present that as a verified explanation. No policy change or extra republish performed.

Prepared separate workaround proposal: preserve the exact already-published UI0.39.0 tarball bytes, temporarily change only npm-private writePolicy from ALLOW_ONCE to ALLOW, republish those same bytes with latest, and restore ALLOW_ONCE in a finally block. This wider repository policy mutation/republication requires explicit additional approval. Preparation downloaded the existing tarball ONLY for byte-preserving republish, not package-availability verification. SHA1/SHA512 match current metadata, package identity checked;2647522bytes, SHA2561bd5c35fb7e22c4340800881a80918013863bffaaa391e4ff729ded4fe169486. Proposal ui-latest-republish/plan.json, local helper ui_latest_republish.py (no writes unless --apply). Guard checks current policy/latest/artifact digest, preserves all existing versions and compares post-publication integrity.

## Approved UI latest workaround applied

User explicitly approved temporary npm-private ALLOW, identical UI0.39.0 republish, and immediate ALLOW_ONCE restoration. Ran ui_latest_republish.py --apply, exit0. Initial metadata/artifact checks passed; ALLOW PUT/GET verified, npm publish original unchanged2647522byte archive succeeded, finally block restored ALLOW_ONCE and GET-verified it. Final metadata latest=0.39.0, published SHA512integrity unchanged, all prior UI versions retained. Evidence ui-latest-republish/result.json. No package rebuilt, no version deleted, no other repository policy changed. This closes the earlier latest limitation; old consumer lock integrity mismatch remains separate unfinished work.
