---
system: nexus
status: verified
checked: 2026-10-13
tags: [nexus, ldap, freeipa, recovery]
---
# Nexus FreeIPA LDAP enabled for DevOps-890

## Summary

LDAP is configured on the recovered Nexus 3.96.4. FreeIPA connection and user mapping verification passed from Nexus; the user confirmed LDAP login with administrator access and supplied a screenshot. Eleven final GET checks passed. Artifact publication using LDAP credentials was not exercised.

## Task and context

Implement the [LDAP plan](2026-10-13-nexus-ldap-plan.md) under DevOps-890. User specified `nexus-users` read and publication access in all repositories, instructed implementation, and retained personal login verification. Target: `http://msk3-nexus.youdo.corp`, host `10.18.24.233`; UI `https://nexus.youdo.com`.

## Applied configuration

Connection `FreeIPA`: `ipa6.youdo.corp` (`172.28.0.6`), LDAPS636, SIMPLE bind, `useTrustStore=true`, search base `dc=youdo,dc=corp`. Runtime bind credentials come from `SELECTEL_PROD_LDAP_NEXUS_USER` and `SELECTEL_PROD_LDAP_NEXUS_PASSWORD` in `~/ai/current/.env`; username is normalized to a full user DN if needed. Values were not copied into scripts, snapshots or notes.

Users: `cn=users,cn=accounts`, subtree false, `inetOrgPerson`, login `uid`, real name `cn`, email `mail`, empty password attribute (saved as null). Groups: STATIC, `cn=groups,cn=accounts`, subtree false, `groupOfNames`, group ID `cn`, member attribute `member`, member format `uid=${username},cn=users,cn=accounts,dc=youdo,dc=corp`. Scoped LDAPS searches confirmed both group DNs, direct user members (14 administrators and13 users), and no nested group members at observation time. Static mapping uses the verified direct member format; no nested-membership support claim is made.

Local role IDs and names match directory group IDs. `nexus-users` has exactly `nx-repository-view-*-*-browse`, `nx-repository-view-*-*-read`, `nx-repository-view-*-*-add`, `nx-repository-view-*-*-edit`; no inherited roles, deletion or administration. Wildcards cover current and future repositories. `nexus-admins` inherits `nx-admin`, with no additional direct privileges. This implements external role mapping by matching external group ID to local role ID, without an extra `nx-ldap-users` intermediary.

Active realms verified exactly: `NexusAuthenticatingRealm`, `DockerToken`, `NpmToken`, `LdapRealm`. Temporary anonymous access remains unchanged by user request.

## CA trust

Added the public FreeIPA CA to Nexus's built-in SSL truststore via `POST /service/rest/v1/security/ssl/truststore`. Certificate subject/issuer `O=YOUDO.CORP, CN=Certificate Authority`, valid until2039-01-17. SHA256 `98:9A:DB:0F:E4:F4:CB:FB:0D:56:3A:06:EE:37:52:4B:07:50:09:9C:9D:59:B0:A6:E9:D4:42:B4:23:C2:CA:7F`; Nexus returned truststore ID/SHA1 `03:B1:A1:9E:BB:BD:CE:7B:24:F3:32:C2:67:A8:DF:9F:4B:81:6B:3B`. Read-back certificate SHA256 matches the approved public CA. System and Java truststores were not modified; no restart was issued.

## Approvals and execution

The user separately approved each external mutation: CA addition after clarification of the built-in Nexus truststore; creation of the FreeIPA LDAP connection; creation of `nexus-users`; creation of `nexus-admins`; enabling `LdapRealm`. All approved POST mutations were followed by GET verification. Before the approved realm PUT, the baseline guard found that the desired four-realm list was already active; an independent GET confirmed the exact approved final order. No PUT was issued, and the cause/timing of prior activation was not established.

Diagnostic POST `/security/ldap/verify-connection` succeeded; `/security/ldap/verify-user-mapping` returned20 mapped users including both Nexus groups. These checks did not persist configuration changes. User instructed personal login testing and then confirmed successful administrator LDAP login with a screenshot.

## Verification and findings

Final `verify.py` exited0: exact saved LDAP fields (allowing the observed empty-to-null normalization), one LDAP connection, exact realms, unchanged anonymous settings, unchanged prior local roles, exact two new roles, CA fingerprint, active local admin, active local CI identities `gitlab`/`pypi`, and the tested LDAP user's administrator group all passed. LDAP membership appears in users API `externalRoles`; `roles` contains local per-user assignments. User lookup is a search, so the exact user ID was matched before asserting membership. No identity/profile data was stored in evidence.

Initial role guards stopped before mutation because GET `/security/roles` also enumerates external LDAP group roles with empty permissions. Corrected the guard to distinguish source `default` from source `LDAP`, then created the two approved local mappings. No existing roles were overwritten. Initial connection verification stopped after successful create because Nexus returns null for empty `userPasswordAttribute`; an independent GET established this sole difference. Creation was not replayed.

## Changed files and commands

Local helper and evidence directory: `~/ai-data/nexus-recovery/ldap/`. `inspect.py` and `probe.py` collect a GET baseline and scoped LDAPS evidence; `configure.py --help` documents one-action apply commands; `verify.py` performs GET-only final checks. Artifacts include `before.json`, `plan.json`, `connection-after.json`, two role snapshots, truststore before/after and `final-verification.json`. Public CA is `ipa-ca.crt`; local `deps/` holds ldap3. No automation-services repository changes, branches, commits or MRs were needed.

Updated the existing [Nexus system map](../systems/nexus.md), the plan outcome and the LDAP item in `~/ai/TODO.md`. The user subsequently requested an LDAP update to the recovery comment. Updated existing DevOps-890 comment 74-124640 via POST; preserved original content and added a dated LDAP section. Subsequent GET verified exact saved text. Evidence: ~/ai-data/nexus-recovery/ldap/youtrack-comment-update.md and youtrack-comment-result.json. Helper update_comment.py guards against concurrent text changes. The direct request authorized this single comment update; no issue fields or other comments changed.

## Risks and rollback

Anonymous wildcard reads remain enabled, so read access alone cannot prove LDAP authorization boundaries. Publication/delete attempts were not run. Current evidence covers configured permissions and user-confirmed administrator login, not publication by a regular LDAP user. Publishing is still subject to repository type and write policy.

Rollback requires approval for each mutation: restore the previous three-realm list; remove only the new local `nexus-users`/`nexus-admins` mappings and the `FreeIPA` connection if required; remove the added CA only if unused. Preserve pre-existing roles and local users. Keep bind secrets in current/.env. LDAP cache effects and future nested group changes require separate evaluation.

## Portable lesson

none
