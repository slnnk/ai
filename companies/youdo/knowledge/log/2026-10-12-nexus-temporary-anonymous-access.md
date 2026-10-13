---
system: nexus
status: verified
checked: 2026-10-12
tags: [nexus, recovery, anonymous]
---
# Temporary Nexus anonymous access during recovery

## Summary

User explicitly requested enabling Nexus anonymous access to prioritize recovery and adding a backlog item to disable it later. Anonymous is now enabled; unauthenticated public Maven POM downloads are verified.

## Context and authorization

Fresh Nexus at10.18.24.233, public nexus.youdo.com. User instruction authorizes temporary anonymous enablement and local TODO update. This supersedes the earlier unapproved anonymous proposal. No publication, repository or user-role modification authorized or performed.

## Actions and key commands

Local `/home/slnnk/ai-data/nexus-recovery/enable_anonymous.py` reads anonymous settings and assigned role with existing admin credentials kept in memory, then PUTs only enabled=true while preserving userId=anonymous and realmName=NexusAuthorizingRealm. GET verifies the exact configuration. Initial PUT succeeded with HTTP200; script initially expected204 and stopped. Corrected response handling to accept200/204; rerun detected enabled=true, made no second PUT and completed verification with exit0.

## Findings

Existing nx-anonymous role grants nx-healthcheck-read, nx-search-read, nx-repository-view-*-*-read and nx-repository-view-*-*-browse; roles list is empty. Existing privileges were preserved. Temporary access therefore covers reading/browsing all repositories, not just Maven; it grants no add/edit/delete privileges.

Unauthenticated HTTPS GET through nexus.youdo.com/repository/maven-public returned200 for Jivo2.6.0 POM (8839 bytes) and Google AGP8.13.2 POM (11773 bytes). Both parsed as XML project documents. No full Gradle build executed; Cyberity connectivity remains unresolved.

## Changed files and risks

Nexus anonymous configuration enabled=true; no other remote configuration modified. Local execution helper, Nexus system map, TODO and this log updated. Reading hosted/private repository content anonymously is now permitted by existing wildcard read role; disable after recovery and consumer credentials setup. Live follow-up is in ~/ai/TODO.md.
