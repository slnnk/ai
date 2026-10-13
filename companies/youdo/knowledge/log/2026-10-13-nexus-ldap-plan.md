---
system: nexus
status: verified
checked: 2026-10-13
tags: [nexus, ldap, recovery, selectel]
---
# Nexus LDAP configuration plan for DevOps-890

## Summary

Plan LDAP authentication and group authorization for the recovered Nexus 3.96.4 in DevOps-890. This plan was implemented on 2026-10-13; see [applied configuration and verification](2026-10-13-nexus-ldap-enabled.md). The implementation steps below preserve the original planning context. Configuration will use the existing Nexus REST API and runtime credentials from current/.env. No automation-services repository changes are needed for the proposed initial setup.

## Task

Configure LDAP login and map approved directory groups to Nexus permissions as part of Nexus recovery. Acceptance requires successful LDAP login, correct group roles, expected allowed and denied operations, and continued local CI authentication.

## Context

Recorded target: Nexus 3.96.4, host `10.18.24.233`, internal `http://msk3-nexus.youdo.corp`, public `https://nexus.youdo.com`. Persistent data is `/data/nexus/nexus-data`. See [system map](../systems/nexus.md). These deployment facts come from existing recovery notes; live state must be rechecked before applying.

`SELECTEL_PROD_LDAP_NEXUS_USER` and `SELECTEL_PROD_LDAP_NEXUS_PASSWORD` are nonempty in `~/ai/current/.env`. Their purpose is presumed to be the directory bind account and must be verified. Secret values were not printed or recorded. LDAP endpoint, search bases, schema and target group permissions remain to establish.

## FreeIPA group evidence

The user supplied a FreeIPA UI screenshot on 2026-10-13 showing `nexus-admins` and `nexus-users` in the group search on `https://ipa6.youdo.corp`. This confirms displayed group names, not directory membership, LDAP endpoint availability or the bind account search permissions. Treat `ipa6.youdo.corp` as a candidate LDAP server until connection checks establish its role.

Proposed admin mapping: `nexus-admins` to built-in `nx-admin`; administrator assignment remains to approve. On 2026-10-13 the user explicitly specified `nexus-users` read and publication access to all repositories. Proposed local role ID/name is `nx-ldap-users`, with exact repository-view privileges `nx-repository-view-*-*-browse`, `nx-repository-view-*-*-read`, `nx-repository-view-*-*-add`, and `nx-repository-view-*-*-edit`. Wildcards cover current and future repository formats and names. No delete or administrative privileges are included. Publication remains subject to repository type and write policy; proxy/group endpoints are not automatically upload targets. This permission requirement is agreed; applying the role or mapping still requires approval for the external mutation. Resolve each group's LDAP DN, membership attributes and effective membership through a scoped query. Inspect existing FreeIPA integration settings for user/group bases and schema instead of assuming Active Directory attributes.

## Implementation plan

1. Inspect current Nexus state with GET requests: LDAP connections, active/available realms, roles and local users. Reuse existing read-only inventory patterns in `~/ai-data/nexus-recovery/comment_inventory.py`. Capture a sanitized before snapshot under `~/ai-data/nexus-recovery/ldap/` and compare the cached `api-spec.json` with the running version. Recover historical LDAP settings from existing configuration evidence if available. Result: exact configuration baseline and available endpoints.
2. Establish directory parameters from existing LDAP integrations and a narrowly scoped directory query: hostname, port, supported secure transport, CA trust, bind identity format, base DN, user/group search bases, object classes, login/name/email attributes, membership attribute and group identifier. Verify network and TLS reachability from the Nexus host, then bind/search with the supplied account without exposing credentials. Check direct and nested membership behavior only as required by actual groups. Result: verified connection and mapping parameters; directory data is not changed.
3. Prepare an explicit table of LDAP group IDs and resulting Nexus privileges for user review, using the agreed `nexus-users` read/publication rights and the proposed `nx-ldap-users` role above. Recover previous mappings where evidence exists. Reuse existing roles only when their permissions match the approved need; `nx-docker` currently includes deletion rights and must not be assigned blindly. Grant administration only to an explicitly approved group. Identify a test user in an approved group and a user outside mapped groups. Result: agreed permission matrix and test identities.
4. Prepare a sanitized local `~/ai-data/nexus-recovery/ldap/plan.json` containing the exact connection settings, mapping fields, role changes, active realms before/after and rollback procedure. Inject bind credentials from current/.env only in runtime memory. Keep local authentication, existing token realms, CI identities and temporary anonymous settings unchanged. Present each state-changing API action with its effect and obtain explicit approval before that command, per global AGENTS.md. Nexus validation endpoints use POST: inspect whether they persist anything before classifying them as read-only checks. Result: concrete reviewable configuration proposal.
5. After approval for each mutation, configure or update the LDAP connection through `/service/rest/v1/security/ldap`, validate connection/user mapping/login, create the approved external role mappings through the roles API and add `LdapRealm` to the existing active realm list through `/service/rest/v1/security/realms/active`. Preserve existing realm order unless a reviewed precedence change is required. Verify every saved configuration with GET before proceeding. CA trust changes, if necessary, are a separate approved mutation. Result: LDAP configuration active with exact approved settings.
6. Verify actual UI/API login with a directory user, returned group/role membership, approved repository access, and denial of operations outside the permission matrix. Include invalid credentials, a user outside mapped groups, nested membership if used, and local administrator/CI regression checks. Temporary anonymous wildcard read means repository HTTP200 alone does not prove LDAP works or enforce private read restrictions; do not disable anonymous during this task. Publishing or deleting test content requires separate approval. Result: evidence of authentication and authorization with the anonymous-access limitation explicit.
7. Record sanitized before/after evidence, effective mappings, credential variable names and rollback instructions in the system map and work log. Close the LDAP item in `~/ai/TODO.md` only after acceptance checks pass. Update the recovery ticket only with separate approval for the external API write.

## Rollback and risks

Maintain an independent local administrator session. Restore the previous active realm list first to remove LDAP from authentication, then restore or remove only LDAP connections/role mappings introduced by this task; each rollback mutation needs explicit approval. A GET snapshot will not necessarily contain a reusable bind password, so restoration of an existing connection requires its credential access route to be confirmed beforehand.

Review login collisions between local and LDAP users, CA expiry/trust, unsupported nested groups, overly broad group mappings and LDAP cache effects after membership changes. LDAP login and group resolution do not constitute continuous provisioning/deprovisioning synchronization. Cache invalidation is a separate state-changing action if required.

## Actions and findings

Ran `ai-sync.sh` with no output or reminder. Reviewed Nexus recovery notes, existing backlog, supplied environment key presence, cached API paths and official Sonatype documentation. Cached schema exposes LDAP CRUD, verification, templates and cache APIs, plus active/available realm endpoints. Runtime endpoint and schema checks are planned, not performed.

Sources: [Sonatype LDAP](https://help.sonatype.com/en/ldap.html), [roles](https://help.sonatype.com/en/roles.html), [security management API](https://help.sonatype.com/en/security-management-api.html).

## Changed files

This work log, the existing Nexus system map, the LDAP backlog source link and generated indexes. No repository task files or external services changed.

## Portable lesson

none
