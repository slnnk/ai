---
system: nexus
status: verified
checked: 2026-10-12
tags: [nexus, npm, recovery]
---
# npm recovery inventory and action plan

## Summary

Read-only recovery investigation requested for all local clones under `~/git`, especially `youdo.static` and `youdo.business`, analogous to NuGet recovery. Live Nexus has no npm repositories, npm blob stores or npm service user. Implementation and publication remain proposed; no remote configuration changes, repository edits, Git mutations, installations or CI retries were performed.

## Context and verified Nexus state

Nexus3.96.4 on `10.18.24.233`, internal `http://msk3-nexus.youdo.corp`, public `https://nexus.youdo.com`. GET inspection authenticated as admin using `NEXUS_ADMIN_PASSWORD` in `~/ai/current/.env`; secrets stayed in memory. Inspector `~/ai-data/nexus-recovery/inspect_npm_state.py`, sanitized result `npm-state.json`. Seven existing File blob stores belong to default/Docker/Maven/NuGet; no npm stores exist. Users: admin, anonymous, gitlab, maven, nuget. Active realms: NexusAuthenticatingRealm and DockerToken. Available npm realm: NpmToken. Temporary anonymous read remains enabled per the separate recovery action; its eventual removal is already tracked.

Both key local clients configure `registry=http://msk3-nexus.youdo.corp/repository/npm/`. `youdo.static/package.json` and `youdo.business/YouDo.Business.Web/spa/package.json` declare private:true and are applications rather than npm publication candidates.

## Actions and evidence

Ran daily `ai-sync.sh` (no output), read company context/repository catalog/Nexus backlog and prior NuGet recovery plan. Delegated multi-file npm audit as required by AGENTS.md. Queried only Nexus GET endpoints for repositories, blob stores, users and realms. Public Sonatype and npm documentation was checked for repository grouping, authentication and publication behavior. Downloaded Nexus OpenAPI shows npm group `writableMember` is Pro-only, so the recovery plan uses direct hosted publication.

## Local clone inventory

Scanner `~/ai-data/nexus-recovery/scan_npm.py`, sanitized inventory `npm-inventory.json`: 164 local checkouts, tracked HEAD files plus differing local origin/master/master/main refs. These remote-tracking refs are snapshots, not automatically current GitLab master. Files are read without executing project code. Ignore node_modules, generated outputs and .git. Workspace package entries with no resolved URL are not counted as Nexus tarballs.

Confirmed direct consumers/producers: `youdo.static`, `youdo.business` (both Business and EmployeeSpace SPAs), `youdo`, `youdo.moderation`, `youdo.business.landings`, `youdo.landings`, `lenochka`, `unsubscribelinkgenerator`, `YouDo.Socket`, `youdo-business-test-metrcis`, `youdo-business-tests-data-generator`, `youdo-core-frontend-tools`. `pechkin` has npm Nexus configuration at HEAD but not at the inspected origin/master. Shared `gitlab-ci-templates` has npm registry overrides in b2b/.build-jobs.yml and v3/.nodejs-npm.yml. `test_signals` is an unrelated text match, not a demonstrated npm consumer. Package roots without registry URLs are not evidence of Nexus usage.

Default .npmrc registry: `http://msk3-nexus.youdo.corp/repository/npm/`; static/moderation CI and b2b templates also use `https://nexus.youdo.com/repository/npm/`. Library publishConfig: `http://msk3-nexus.youdo.corp/repository/npm-private/`. Live CI constructs `_authToken` from `NPM_TOKEN` (Bearer; earlier Basic interpretation corrected); client .npmrc files have no embedded authentication. Do not equate the variable name NPM_TOKEN to a Bearer token without inspecting its use.

Four publication candidates in `youdo-core-frontend-tools/packages/*`: `@youdo/ui`, `@youdo/eslint-config`, `@youdo/prettier-config`, `youdo-cursor-css-vars-extension`. Root `@youdo/core-tools-frontend@0.0.4` is the workspace container, not a confirmed published dependency. Applications with private:true must not be published as libraries.

| Package | Required by inspected origin/master lockfiles | Extra versions from existing local branches |
| --- | --- | --- |
| @youdo/ui | 0.39.0 (Business), 0.17.5 (Business landings) | 0.30.1 and 0.34.0 (local Business HEAD/master) |
| @youdo/eslint-config | 2.1.0 (Business), 1.2.5 (Business landings) | none additional |
| @youdo/prettier-config | 0.0.1 (Business) | none additional |
| youdo-cursor-css-vars-extension | 0.0.3 (Business) | none additional |

`youdo.static` has no @youdo dependencies in the inspected manifests/lockfiles; initial recovery is expected to need the npmjs proxy, subject to checking all locked upstream versions. Local producer snapshot contains @youdo/ui0.21.0 and eslint2.0.14, which do not match current requested versions. Local producer tags are absent. Rebuilding the local producer HEAD under another version is not a valid restoration of lost package bytes. Source selection must use live GitLab tags/commit history or original tarballs.

## Live GitLab and public npm verification

Read-only GitLab GETs in `check_npm_live.py`, sanitized evidence `npm-live.json`, verified current default master for Static, Business, Business landings and the library producer. Business master requests @youdo/ui0.39.0, eslint2.1.0, prettier0.0.1 and cursor-extension0.0.3; landings master requests UI0.17.5 and eslint1.2.5. Static master has no identified private library dependencies. Live master producer manifests are newer than the local clone: UI0.40.1, eslint2.1.0, prettier0.0.1, cursor-extension1.0.0 (producer lock UI0.40.0). Hence eslint/prettier have matching current-source versions, while UI/cursor require historical source or original tarballs. Exact historical source commits and original tarball availability were not yet audited. Sequential raw GETs used master refs; no claim of a transactionally pinned multi-file snapshot.

Public registry metadata GETs return404 for all four internal library names. Public application/workspace names also return404 but are not library restoration candidates. This is not an exhaustive exact-version check of all public transitive dependencies; that remains part of proxy/install verification. Nothing here claims restored package contents or successful installation.

## Planned Nexus layout

| Object | Name | Storage/behavior |
| --- | --- | --- |
| File blob store | npm-hosted | relative path npm-hosted, permanent private packages |
| File blob store | npm-cache | relative path npm-cache, refillable public cache |
| npm hosted | npm-private | npm-hosted, actual library publishConfig URL |
| npm proxy | npmjs-proxy (new proposed name) | npm-cache, https://registry.npmjs.org/ |
| npm group | npm | npm-cache, members npm-private then npmjs-proxy |
| role | nx-npm | browse/read required npm repos, add/edit npm-private only |
| service identity | npm (proposed, verify existing NPM_TOKEN principal) | preserve compatible existing CI authentication |

## Proposed infrastructure restoration

1. Preserve legacy client registry URLs and resolve every repository endpoint pinned in lockfiles before making changes. Re-read state and current API schemas immediately before implementation; do not delete or overwrite unrelated repositories.
2. Create separate File stores `npm-hosted` and `npm-cache` with relative paths under `/nexus-data/blobs` (host `/data/nexus/nexus-data/blobs` on existing data disk). Hosted content is irreplaceable; public cache can refill. No cleanup policy on restored hosted content. Proxy uses `https://registry.npmjs.org/`, strict content-type validation and ordinary metadata/negative cache settings.
3. Restore the legacy `npm` group URL, combining private hosted first and npmjs proxy second. Hosted name `npm-private` matches all four library publishConfig entries; new proxy name `npmjs-proxy` is proposed (no legacy direct proxy URL identified). Use npm-hosted storage for hosted, npm-cache for proxy/group. Hosted write policy ALLOW_ONCE, subject to checking actual publisher requirements.
4. Restore compatible existing npm identity and credential from client configuration or inherited CI variables, comparing credentials in memory; never copy secret values into evidence or payload files. Proposed service username `npm`, unless live publisher credential resolves to another existing identity that must be preserved. The actual NPM_TOKEN-to-identity mapping is an implementation preflight, not an assumption. Create one role `nx-npm`, browse/read for the required npm repositories and add/edit only for private hosted, no administration/delete. Existing gitlab user needs nx-npm only if an actual npm publisher uses it; preserve its other roles.
5. Live publisher uses Bearer `_authToken`, so enable NpmToken while preserving existing realms. Basic `_auth` would work without it but is not the observed flow. Old Bearer tokens cannot be assumed to survive a new instance. Modern npm requires registry-scoped auth; first verify with the actual Node/npm versions used by each CI job, avoiding an unrelated toolchain upgrade.
6. Validate public/internal metadata and tarball URLs, status, returned JSON and package identity/integrity. Prove credential validity with authenticated principal evidence, since anonymous HTTP200 does not establish authentication. A publication probe requires a separately agreed real package/version and explicit external-write authorization.

## Library restoration sequence

Use exact package names/versions and integrities from the inventory. Prefer original .tgz files from available backup, CI artifacts or npm caches. Verify package.json and lockfile integrity before recovery publication; publish directly to private hosted and restore required dist-tags only where actual consumers need them. If originals are absent, identify matching source tags/commits and Node/npm/build configuration, rebuild in a scratch directory, inspect the tarball before requesting publication authorization. Never claim a rebuild has the original integrity: if bytes differ, lockfile consumers can fail EINTEGRITY. Such packages require original artifacts or separately reviewed consumer lockfile updates.

After exact packages are available, perform isolated dependency checks with the project's actual CI Node/npm version and clean cache: use existing lockfile with npm ci (or the repository's existing install path when no lockfile exists); first disable lifecycle scripts for availability checks, then run separately reviewed full build checks. Keep actual service checkout files untouched. Distinguish registry/package recovery from unrelated Git dependencies, binary downloads and native toolchain failures.

## Changes and execution boundary

Local audit scripts/results and this note only. Backlog items belong to `~/ai/TODO.md`, not this note. Execution of Nexus API writes, publication and CI retries requires explicit approval under user AGENTS.md. No such approval was requested for this inspection-only task.

## Sources

- [Sonatype npm registry](https://help.sonatype.com/en/npm-registry.html)
- [Sonatype npm security](https://help.sonatype.com/en/npm-security.html)
- [Sonatype npm publishing](https://help.sonatype.com/en/publishing-npm-packages.html)
- [npm v10 npmrc authentication scoping](https://docs.npmjs.com/cli/v10/configuring-npm/npmrc/)

## Approved execution outcome

User requested steps1-3; Nexus resources applied and internal identity/metadata verified. Current npm user uses a newly issued Bearer token; old CI token401, public npm404 from absent LB npm location. GitLab variable replacement and public LB configuration await separate approval. Details: [applied steps and verification](2026-10-12-nexus-npm-recovery-applied.md).
