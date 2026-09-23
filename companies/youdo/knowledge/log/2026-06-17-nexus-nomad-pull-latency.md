---
system: nexus
status: verified
checked: 2026-06-17
tags: [nexus, docker-registry, nomad-test, image-pull, nginx, pmtu, sc-lb-pub01, incident]
---
# Nexus / Nomad image pull diagnostics

## Task

Find why Docker image pulls from Nexus are slow on the test Nomad cluster, and diagnose a
related failing job (`youdo-business-tochka-proxy-test6`) reported the same day.

## Context

- Date: 2026-06-17 Europe/Moscow
- Context: Nexus in Docker on root@msk3-nexus.youdo.corp / nexus-prod-01.ru-central1.internal, test Nomad node root@10.16.26.33 / nomad-agent-test-06.ru-central1.internal.

## Findings

- Nexus container: nexus-nexus-1, image sonatype/nexus3:3.70.4-java11-ubi, up ~11 months, ports 3000/3003/8081.
- Nexus data mount: /data/nexus/nexus-data -> /nexus-data, filesystem /dev/vdb ext4 167G total, 90G used, 69G free, inode usage 4%.
- Container memory high but not exhausted during check: about 11.75GiB / 15.61GiB, JVM options Xms/Xmx/MaxDirectMemorySize 6144m.
- Nexus logs currently contain repeated OrientDB errors: No space left on device in analytics DB flush/commit. Host df did not show actual /data full, so likely Nexus/Orient state needs separate follow-up/restart/DB check, but this is not the main pull latency cause found on Nomad.
- Test node 10.16.26.33 resolves nexus.youdo.com to external 92.53.80.147/148/149, while msk3-nexus.youdo.corp resolves to internal 10.16.24.23.
- Docker daemon on test node only lists msk3-nexus.youdo.corp, msk3-nexus.youdo.corp:3000 and :3003 in insecure-registries; nexus.youdo.com is pulled via external HTTPS path.
- HTTP timing from test node: https://nexus.youdo.com/v2/ about 165ms to 401 via remote 92.53.80.148; http://msk3-nexus.youdo.corp/v2/ about 10ms to 401 via 10.16.24.23.
- Image check after cache warm: nexus.youdo.com/youdo/microservices/youdo.business/migrations:site-25047-shift-notifications-133887 took 1.57s; same image via msk3-nexus.youdo.corp took 0.09s.
- Cold-ish pull via nexus.youdo.com on 10.16.26.33 for that image took 2:39.62 even though many base layers were already present.
- Diagnostic pull via nexus.youdo.com from the Nexus host itself did not finish after several minutes and was interrupted.
- Nomad logs also show repeated failures for missing tag nexus.youdo.com/youdo/microservices/youdo.content/api:2.5.4 with manifest unknown; these retries look like a separate deployment/tag issue, not slow downloading.

### Conclusion

Primary cause for slow test-cluster pulls appears to be use of external nexus.youdo.com from internal Nomad nodes. Internal registry address msk3-nexus.youdo.corp reaches the Nexus host directly and is much faster.

### Next steps

- Prefer msk3-nexus.youdo.corp in Nomad job image references for internal clusters, or change internal DNS/split-horizon for nexus.youdo.com to resolve to 10.16.24.23 where appropriate.
- If nexus.youdo.com must remain in image refs, investigate external 92.53.80.147/148/149 proxy/LB path and why large blob transfer stalls.
- Separately investigate Nexus OrientDB No space left on device errors and consider controlled Nexus restart/repair after checking scheduled tasks and backups.

### LB sc-lb-pub01 findings

- Checked root@172.28.0.141 / sc-lb-pub01.youdo.corp, external IP 92.53.80.147, nginx + consul-template.
- nginx vhost /etc/nginx/conf.d/nexus.youdo.com.conf proxies /v2 to http://msk3-nexus.youdo.corp with Host $host. No explicit proxy_buffering off in the Docker location.
- LB to backend timings: http://10.16.24.23:3000/v2/ about 126ms; http://10.16.24.23:8081/repository/docker/v2/ about 1.15s in one sample; public self https://nexus.youdo.com/v2/ about 143ms.
- Access log shows slow Docker blob transfers through nexus.youdo.com, e.g. 18MB in 467.9s, 41.7MB in 299.2s, 23.8MB in 299.6s. For these requests upstream header/connect times are small, while total/upstream response time is large.
- No obvious Nexus-specific nginx error log warnings for temporary file buffering found in the sampled tail; /data/nginx cache is tiny, root FS 65% used.
- Current evidence points to the external LB/public path or client path via it being the bottleneck. Internal msk3-nexus.youdo.corp remains the preferred path for Nomad nodes.

### Nexus host nginx check

- msk3-nexus.youdo.corp also runs nginx on port 80. Docker /v2 is rewritten to /docker-pull or /docker-push; pull proxies to localhost:3000, push to localhost:3003.
- No active limit_rate, limit_req, limit_conn, geo/map based throttling found in /etc/nginx.
- The nginx locations do not set proxy_buffering off or proxy_request_buffering off, so default nginx buffering applies. proxy temp/client temp live under /var/cache/nginx on the small root filesystem /dev/vda2, currently 9.8G total, 6.9G used, 2.5G free.
- Historical nginx errors on this host show pwrite/pwritev No space left on device in /var/cache/nginx/proxy_temp and /var/cache/nginx/client_temp for Docker blob GET/PUT requests. Current /var/cache/nginx is small/empty, so this is not active right now but is a known failure mode.
- Conclusion: no evidence that msk3-nexus nginx intentionally throttles external clients. However, both LB nginx and Nexus-host nginx should likely disable proxy buffering/request buffering for Docker registry paths to avoid temp-file buffering and root FS pressure.

### Network-path isolation

- User noted the path used to be fast, so this is likely a regression rather than intended architecture.
- Large blob sha256:4b48b477... from 172.28.0.141 to 10.16.24.23:3000 timed out after 120s after only ~4.7-6.0MB, about 39-50KB/s.
- The same large blob from 10.16.26.33 directly to 10.16.24.23:3000 completed in 0.186s (~173MB/s). Locally on Nexus via 127.0.0.1:3000 completed in 0.034s.
- Therefore Nexus application/storage and nomad-to-nexus internal path are fast; the slow segment is specific to sc-lb-pub01 / 172.28.0.141 toward 10.16.24.23.
- TCP ss during slow LB download: mss 1298, pmtu 1414, rtt ~61ms, delivery_rate ~166Kbit/s, bytes_received grows slowly. This points to network/PMTU/tunnel/QoS/path issue, not nginx application throttling.
- PMTU checks: LB -> 10.16.24.23 route cache mtu 1414, DF ping size 1400 fails, 1322 succeeds; Nexus -> LB tracepath reports pmtu 1350. Nomad 10.16.26.33 -> Nexus has pmtu 1500 and DF ping 1472 succeeds.
- Recommended next owner/check: network path/gateway between 172.28.0.0/24 and 10.16.x.x, especially 172.28.0.1 / 172.24.0.1 / tunnel MTU and MSS clamping. Also compare other public LB nodes for the same PMTU and throughput.

### Nomad job youdo-business-tochka-proxy-test6

- Date: 2026-06-17 Europe/Moscow.
- Checked read-only via Nomad yandex-test API.
- Job youdo-business-tochka-proxy-test6 submitted at 2026-06-17T17:04:50+03:00, image tag master-1725, deployment f2e9982d failed due to progress deadline, job status dead.
- All recent allocations landed on node nomad-agent-test-010 / node id 24384c4e and failed. Pulls completed; pre/post migrations exited 0.
- The allocation is marked unhealthy because task youdo-business-tochka-proxy-proxy-worker-test6 exits. Sibling webapp/mock tasks are then killed by Nomad, often with exit 137 due to sibling failure, not as primary root cause.
- proxy-worker logs show fatal startup failure in Hangfire.PostgreSql/Npgsql: SocketException Name or service not known while opening PostgreSQL connection. Logs also show MassTransit/RabbitMQ connection warnings using rabbitmq.service.yandex-test.consul with port 0.
- Host and an existing Docker container on the same node can resolve postgres-b2b.service.yandex-test.consul and rabbitmq.service.yandex-test.consul; TCP checks to postgres-b2b:5433 and rabbitmq:5672 succeeded from the node.
- Compared with running youdo-business-tochka-proxy-test10: DB/Rabbit env shape is effectively the same, but test10 uses image tag master-1724 while failing test6 uses master-1725.
- Current conclusion: not an image pull issue and not a general node DNS outage. Most likely regression/config handling problem in image/code master-1725, causing worker startup DNS/config failures; RabbitMQ port becoming 0 is a concrete symptom to inspect in application config binding.
- Later status check: youdo-business-tochka-proxy-test6 recovered and is running again, which fits a transient infrastructure/network/bootstrap failure during today's incident better than a persistent deployment regression.
- Reproduced locally on nomad-agent-test-06 by running the exact migration image `msk3-nexus.youdo.corp/youdo/microservices/youdo-business-tochka-proxy/migrations:master-1725` with the pre-migrations env (`M_TAG=Pre`, `CON_STR`, `ConnectionStrings__default`). The container completed all migrations and exited 0. This means the current image/env/DB path is healthy now; the earlier failure was transient and not reproducible at the time of this check.
- Same reproduction on `10.16.26.48` (`nomad-agent-test-010`) failed immediately at `TRYING CREATE DATABASE` with `Name or service not known` / `SocketException` while resolving `postgres-b2b.service.yandex-test.consul`. That points to node-specific DNS/service-discovery instability rather than a universal image or database problem.

## Open items

- Switch internal Nomad image references (or split-horizon DNS) to `msk3-nexus.youdo.corp`.
- Hand the `172.28.0.0/24` -> `10.16.x.x` PMTU/MSS problem to the network path owner.
- Disable nginx proxy/request buffering for Docker registry paths on both LB and Nexus-host nginx.
- Follow up on Nexus OrientDB "No space left on device" errors.
- Investigate node-specific Consul DNS instability on `nomad-agent-test-010`.

## Portable lesson

none
