---
system: nexus
status: verified
checked: 2026-10-12
tags: [nexus, routing, dhcp]
---
# Nexus public LB routing verification

## Summary

Public LB now routes Nexus through its private gateway and direct status returns HTTP200. Its latest DHCP lease includes the destination subnet. No remote state was changed. User clarified172.24.0.0/24 remains current for physical production servers; lb pub is in172.28.0.0/24.

## Task and context

Compare local routes on balancers_hardware with lb pub and propose a recovery solution. Repository automation-services, current production LB sc-lb-pub01.youdo.corp172.28.0.141; Nexus10.18.24.233.

## Actions and findings

Read-only repository inspection found no persistent unicast route management for these balancer groups. yandex_routes in the nginx iptables template grants INPUT access only. Hardware inventory lists172.24.0.22/.23. User corrected the earlier statement:172.24.0.0/24 is current for physical production servers;172.28.0.0/24 is also used in production.

Read-only SSH to lb pub: `ip -4 route get 10.18.24.233` returns via172.28.0.1 deveth0 source172.28.0.141. Live route10.18.24.0/24 exists. Latest `/var/lib/dhcp/dhclient.eth0.leases` lease from172.28.0.3 includes RFC3442 option121 destination10.18.24.0/24 via172.28.0.1, alongside10.18.20.0/24 and10.18.26.0/24. No matching manually persisted route was found in inspected network/DHCP/systemd configuration. eth0 is DHCP via ifupdown in `/etc/network/interfaces.d/50-cloud-init.cfg`; that file warns of regeneration by cloud-init. Existing `/etc/network/if-up.d/99-default-metric` adjusts only default route metric200. DHCP route delivery is verified; reboot persistence was not tested.

Direct LB GET `http://10.18.24.233/service/rest/v1/status` returns200. Public unauthenticated cached Jivo POM URL now returns401 instead of timeout; public status path remains404. Authenticated public artifact download remains unverified. `nginx -T` still shows six hostname-based Nexus proxy destinations.

Direct SSH to historical hardware172.24.0.22 timed out; through LB it succeeded. Historical `/etc/netplan/01-balancer.yaml:29` contains10.18.24.0/24 via172.24.0.1 on bondaggi. This is a verified physical production route example; its gateway is specific to172.24.0.0/24 and must not be copied to lb pub.172.24.0.23 direct SSH timed out.

## Proposal and limits

No new route is needed to fix current Nexus reachability: the required subnet route is already present and DHCP-delivered. Do not apply the earlier temporary /32 proposal, restart networking, or copy historical hardware gateway. If explicitly requested to enforce routes locally regardless of DHCP, use a separate idempotent ifupdown hook on current LB for only10.18.24.0/24 via172.28.0.1 deveth0; do not introduce Netplan on this host or edit cloud-init-generated interface configuration. Implementation and remote application were not authorized or performed. Next evidence needed: authenticated public Maven download and public Docker check.

## Changed files and risks

Knowledge-base log, Nexus system map and live backlog only. No repository edits, git publication, DHCP mutation, route mutation or remote restart. Existing repository Nexus backend changes remain local. No hardware inventory correction is required on the basis of the earlier withdrawn statement.

## Public nginx Maven location verified

Read-only `nginx -T` on lb pub confirms `/etc/nginx/conf.d/nexus.youdo.com.conf`: HTTPS server contains prefix location `/repository/maven` with `proxy_pass http://msk3-nexus.youdo.corp`, preserving the request URI. It covers maven-public, maven-releases and maven-snapshots. HTTP redirects to HTTPS. No auth_basic or allow/deny restrictions appear in this location. Public POM401 is consistent with Nexus anonymous access being disabled. Public status404 is explained by the absence of a matching `/service/rest/` or catch-all proxy location in this vhost; it does not demonstrate a Maven failure. No nginx change performed.

## Authenticated public Maven verification

Read-only `/home/slnnk/ai-data/nexus-recovery/verify_public_maven.py` exited0. Existing GitLab group34 Maven credentials were used in memory only, with normal HTTPS certificate validation and no redirects followed. Public `https://nexus.youdo.com/repository/maven-public/` returned200 for Jivo2.6.0 POM (8839 bytes,0.14s), Jivo2.6.0 AAR (2187102 bytes,1.11s), and Google AGP8.13.2 POM (11773 bytes,0.10s). Both POMs parsed as XML project documents; AAR ZIP integrity and AndroidManifest.xml verified. Anonymous Jivo POM returns401 as expected. Selected public artifacts verified; full Gradle build/transitive dependencies and Cyberity remain unverified. No credential values printed or persisted.

## Local explicit-backend proposal withdrawn

User explicitly requested reverting the two prepared Nexus backend edits. Restored only `inventories/prod_selectel/group_vars/balancers_public` and `roles/nginx/templates/vhost/nexus.youdo.com.j2` to HEAD after verifying their exact diffs consisted solely of the known Nexus proposal. Scoped `git diff` is empty. Unrelated runner/Terraform local edits remain. No state-changing git commands or remote changes executed. Public nginx continues using `msk3-nexus.youdo.corp`; authenticated public Maven reads already passed with that configuration. Earlier statements that these two edits remain pending are superseded.
