---
system: nexus
status: verified
checked: 2026-10-12
tags: [nexus, npm, recovery]
---
# Nexus npm steps 1-3 applied and verified

## Summary

User explicitly requested steps1-3 of the npm recovery plan. Two File stores, three npm repositories, consolidated nx-npm role, active npm user and NpmToken realm were created and GET-verified. New npm Bearer token identifies npm at internal group/hosted whoami endpoints; original CI token returns401. Public npm returns404 because the production LB vhost lacks an npm proxy location. No library publication, CI retry, GitLab variable update or LB configuration change was performed.

## Authorization and context

User instruction: execute steps1-3 of [npm recovery plan](2026-10-12-nexus-npm-recovery-plan.md). Scope is Nexus storage/repositories/identity. Separate GitLab variable and production LB writes remain outside that reviewed action. Nexus internal msk3-nexus.youdo.corp, recovery host10.18.24.233; public nexus.youdo.com through sc-lb-pub01 at172.28.0.141.

## Actions and findings

Read-only live GitLab GET identifies NPM_TOKEN in project496 youdo/microservices/youdo-core-frontend-tools, environment_scope*. Actual master .gitlab-ci.yml lines90/132 use _authToken, not _auth; token starts with NpmToken. The prior Basic-auth interpretation was incorrect and is corrected in the plan. No variable value was printed or persisted outside current/.env.

Local helper ~/ai-data/nexus-recovery/restore_npm.py prepares/rechecks settings and applies authorized Nexus writes. First apply created stores and repositories then stopped before role/user because privilege responses expose name rather than id. Corrected the parser, verified existing targets match every intended setting, and resumed; second apply exited0. No target deletion/overwrite or unrelated-role changes occurred.

Created File stores npm-hosted/npm-cache with same-named relative paths beneath /nexus-data/blobs (host /data/nexus/nexus-data/blobs). Created npm-private hosted on npm-hosted with ALLOW_ONCE and strict content validation; npmjs-proxy on npm-cache with remote https://registry.npmjs.org/, metadata/content1440min, negative-cache1440min, autoBlocktrue; npm group on npm-cache with npm-private then npmjs-proxy. No cleanup policy added.

Role nx-npm has npm wildcard browse/read plus npm-private add/edit, no delete/admin or inherited roles. Active npm user has only nx-npm. Added NpmToken after NexusAuthenticatingRealm and DockerToken, preserving both. Generated password and replacement Bearer token stored only as NEXUS_NPM_USER, NEXUS_NPM_PASSWORD and NEXUS_NPM_TOKEN in ~/ai/current/.env. Login PUT targeted npm-private; no library was uploaded.

## Verification and limits

Sanitized GET evidence: ~/ai-data/nexus-recovery/npm-verification.json and npm-apply-plan.json. Both internal npm/-/whoami and npm-private/-/whoami return200 with username npm using new token. Old project NPM_TOKEN returns401 at the same hosted endpoint. Internal npm/lodash metadata returns200 with name lodash and version4.17.21. Metadata only: no package tarballs downloaded.

Public npm and npm-private whoami and npm/lodash all return404. Read-only SSH of /etc/nginx/conf.d/nexus.youdo.com.conf on LB confirms no /repository/npm location. Existing template roles/nginx/templates/vhost/nexus.youdo.com.j2 likewise lacks npm; no route failure or repository failure inferred.

Prepared ~/ai-data/nexus-recovery/update_npm_ci_token.py (default GET-only; --apply requires separate authorization). It replaces only project496 NPM_TOKEN value from current/.env:NEXUS_NPM_TOKEN, preserving type/envscope/protected/masked/raw/description. Existing metadata: env_var, scope*, protectedfalse, maskedfalse, rawfalse, descriptionnull. Sanitized plan npm-ci-token-plan.json. No masking-policy change or pipeline retry proposed.

Prepared npm-public-location.conf outside the repository: add HTTPS location /repository/npm with proxy_pass http://msk3-nexus.youdo.corp, original Host and X-Forwarded-Proto. Requires separate repository branch approval if implemented canonically and explicit remote apply/reload approval. Do not claim public npm or existing CI compatibility until these follow-ups are approved/applied/verified.

## Changes

Local audit/apply/verify helpers and evidence, current/.env secret variables, Nexus remote npm resources above; knowledge log, existing Nexus map, TODO and sync notes. No repository code/config edits or Git mutations.

## Portable lesson

None.

## Approved CI token replacement completed

User explicitly requested replacing NPM_TOKEN. Ran update_npm_ci_token.py --apply: project496 variable PUT returned200 and subsequent GET verified exact equality to current/.env:NEXUS_NPM_TOKEN and unchanged metadata. Scope*, env_var, protectedfalse, maskedfalse, rawfalse and descriptionnull preserved. No secret values printed/logged, no pipeline/job retry, no public LB change or package publication. GitLab CI credential replacement is complete; public npm routing and private package contents remain separate unfinished recovery work.
