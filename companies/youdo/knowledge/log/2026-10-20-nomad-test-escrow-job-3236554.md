---
system: nomad-test
status: verified
checked: 2026-10-20
tags: [gitlab-ci, mssql, dns]
---
# Escrow Tinkoff job3236554 MSSQL connection failure

## Task
Read-only investigation of [job3236554](https://gitlab.youdo.sg/youdo/microservices/escrow.tinkoff/-/jobs/3236554). No fixes or deployment requested.

## Context
Project422, pipeline140950, ref13.8.12, SHA eaa0d387bb21488f2077968d10def0b9450f0947. Runner105, gitlab-runner-docker-1 (172.28.0.171). Job `deploy-yandex-test 0/17` failed on2026-10-20 at11:01:24UTC. Existing clean checkout /home/slnnk/git/escrow.tinkoff inspected without switching branches; exact failed revision inspected through git show.

## Actions
Fetched job metadata and trace through read-only GitLab API. Inspected CI and devops/config.yml at the failed SHA. Artifacts stored under ~/ai-data/gitlab-review/job-3236554/; raw trace contains an unmasked SQL credential and must not be quoted wholesale.

## Findings
- Fatal task `Create mssql db if not exist`, deploy_microservices.yml:163, trace964–1013. sqlcmd cannot connect to vk-ms1-sql-test.mcs.local to create TinkoffEscrow. Errors: `Login timeout expired`, `TCP Provider: Error code 0x2AF9`, `Server is not found or not accessible`. Failed before migrations or application submission.
- Name resolution is the leading hypothesis; live DNS/SQL connectivity was not checked. Earlier October15 DNS recovery does not prove current resolution. See [earlier DNS investigation](2026-10-10-gitlab-ci-dynamic-inventory-consul-dns.md).
- Earlier ignored task `Stop nomad job`, playbook149, trace896–949: `Prefix "escrow-tinkoff-test" matched multiple jobs`. Exact unsuffixed job was absent from command results; numbered test instances matched. This was not the fatal task.
- Target inventory host test_docker, Nomad http://nomad.service.vk-test.consul:4646, unsuffixed SQL database TinkoffEscrow and Nomad job escrow-tinkoff-test. This attempt targets the common test instance.

## Changes
Knowledge-base bookkeeping only; no repository, GitLab, DNS, SQL or Nomad changes.

## Status and risks
Log review complete. DNS diagnosis remains a hypothesis until live checks. Subsequent runner diagnostics are recorded below; the DNS repair proposal is in [central backlog](../../../../TODO.md), under nomad-test / Consul. No job retry performed. Raw log exposes an SQL credential; credential values were excluded from notes and response.

## Portable lesson
none

## Runner access verification, follow-up2026-10-20
User requested checking access from the GitLab runner. Read-only SSH to runner105 /172.28.0.171 confirmed:
- Host libc resolves vk-ms1-sql-test.mcs.local to10.18.26.17. TCP1433 connects successfully by both hostname and IP. This verifies transport only, without SQL login.
- Host resolvers172.28.0.6/.7 each return NOERROR10.18.26.17.
- Docker daemon DNS is explicitly172.28.0.8/.9. DNS172.28.0.8 repeatedly returns NXDOMAIN/root SOA;172.28.0.9 returns NOERROR10.18.26.17. A valid NXDOMAIN response can prevent fallback to the second server.
- Runner Docker configuration contains no dns/dns_search/network_mode override. No running containers were available for in-container inspection; no container was created and no job retried.
- The configured primary Docker DNS failure is verified and consistent with TCP0x2AF9 in the failed job. Forwarding/cache root cause within172.28.0.8 was not inspected. Host DNS/TCP success must not be treated as proof of successful container or SQL authentication.
No remote changes performed. Earlier October15 successful resolver matrix is historical; this fresh query supersedes any assumption both Docker resolvers currently work. Runner clock reported08:07UTC despite job API timestamps11:01UTC on the same date; do not infer a reliable cross-system timeline from these observations.

## Conditional forwarding follow-up
User screenshots confirm direct queries from Windows to10.18.20.3 resolve10.18.26.17, while172.28.0.8 still returns NXDOMAIN after successful server-side dnscmd cache clear. dnscmd /zoneinfo on172.28.0.8 shows active DS-integrated forwarder zone mcs.local (type4), master10.18.20.3, timeout5, forwarder slave0.
Read-only18s tcpdump via youdo SSH/sudo on10.18.20.3 captured a unique generated DNS probe forwarded by172.28.0.9 and its mcs.local-SOA NXDOMAIN reply. The same unique probe through172.28.0.8 returned root-SOA NXDOMAIN; no traffic sourced from.8 reached the gateway during the capture. Existing SQL name remained NXDOMAIN via.8 and correct via.9/direct.3. Receipts: ai-data/gitlab-review/job-3236554/dns-forwarding-{queries,capture}.txt. This supports a fault in the.8 conditional forwarding path/runtime state; absence at the gateway alone does not distinguish no send from routing/filtering before arrival. No Windows DNS service restart or configuration change performed by agent.

## DNS recovery verified after user follow-up
After the suggested DNS-service restart, the user supplied nslookup output: first query eventually returned10.18.26.17 after timeouts, repeated query returned immediately. The screenshot does not show the restart command itself. Fresh read-only checks from runner105 confirm both Docker upstreams172.28.0.8/.9 now return NOERROR10.18.26.17 in4ms/0ms respectively. Host resolution returns the same IP and TCP1433 connects. The immediate resolver failure is resolved; precise Windows service/runtime cause and uncached-query stability remain unproven. No container/SQL authentication or GitLab retry performed. Central DNS repair proposal closed on this evidence; historical Nomad-prefix ambiguity remains a separate nonfatal observation.
