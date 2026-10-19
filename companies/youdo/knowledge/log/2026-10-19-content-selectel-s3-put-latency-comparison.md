---
system: content
status: verified
checked: 2026-10-19
tags: [content, production, selectel, s3, tempo, latency]
---
# Historical sampled traces confirm slow Selectel S3 PUT requests

## Summary

The incident was closed by the user on 2026-10-19, with the Selectel incident confirmed as the cause. Historical investigation and limits follow; the final closure is recorded below.

Existing production Tempo traces demonstrate slow successful HTTP PUT requests from Content to Selectel bucket `youdo-photos` on2026-10-19. In one sampled photo upload at11:09Moscow, S3 calls consumed24.246s of24.559saction time (98.73%), while JPEG conversion took273ms and non-overlapping outer SQL spans totalled20.447ms. A sampled Max1600PUT took10.918s today versus0.957–2.210s in three retained Friday examples. Similar current object sizes support the comparison. This establishes latency at the S3 HTTP-client boundary; it does not by itself distinguish provider processing from network/connection delays or establish the exact stage split of the earlier unsampled Shift248 request.

## Task and context

User asked whether existing traces, beyond Shift248, show increased S3 upload latency and possible Selectel problems. This follows [Content and Business incident investigation](2026-10-19-content-s3-thumbnail-conflicts.md). No production writes, replay, deployment or tracing changes were performed.

Production Tempo: `http://tempo.infra.youdo.corp`, mks-infra namespace monitoring, service tempo port3100. Query API2.6.1 works without tenant/auth. Configured retention168h. Distinct Activity/W3C and Jaeger contexts must be considered; only the Jaeger ID identifies custom OpenTracing traces in the observed source stack.

## Actions and query coverage

Validated a selector against a known retained positive control, then searched19October early/incident periods and16/18October comparison windows, followed by full UTC-day photo-bucket searches for16/18October and00:00–10:55UTC19October. All searches returned fewer than limit100 and their completedJobs matched totalJobs. This avoids limit truncation but not sampling bias or missing telemetry.

```traceql
{ span.http.method = "PUT" && span.peer.hostname =~ ".*selcloud.ru" }
```

Narrow photo-bucket selector:

```traceql
{ span.http.method = "PUT" && span.peer.hostname = "youdo-photos.s3.storage.selcloud.ru" }
```

Downloaded35unique traces and extracted39unique S3 PUT spans after deduplicating by traceID/spanID. All extracted PUTs were from service `back/content/api`;36HTTP200,3HTTP409. Split by bucket, object stage and success/failure; fast409responses must not be mixed into successful-write latency. Raw signed/request URLs and payloads were not copied into notes.

## Findings: successful PUT comparison

The following are medians in seconds with sample counts. Dates are UTC; queries cover full days16/18October and the available morning19October for photo-bucket comparisons. Small samples and differing object sizes mean these are diagnostic examples, not fleet p95/SLA measurements.

| Photo object stage | 2026-10-16 | 2026-10-18 | 2026-10-19 |
| --- | --- | --- | --- |
| Original | 0.297(n=2) | 4.227(n=1) | 18.683(n=1) |
| OrigSize | 1.039(n=2) | 1.706(n=1) | 5.563(n=1) |
| Max1600 | 1.045(n=3) | 1.753(n=1) | 10.918(n=1) |

Original-size comparability is not established for historical samples; the19October original is9.45MB. The stronger evidence is direct stage attribution and reasonably similar-sized thumbnail examples below. Three sampled19October409responses took42–51ms, separately from the slow successful PUTs.

## Sampled upload: trace148ae312ae4a95

Moscow11:09:39–11:10:04 (UTC08:09:39–08:10:04): inbound Content `HTTP POST`24.628730s; upload action24.558959s.

- Original `HTTP PUT`:18.683297s; enclosing StorageUploadFile18.684416s.
- OrigSize `HTTP PUT`:5.563115s; enclosing StorageUploadFile5.564178s.
- Sum of S3 HTTP PUT spans24.246412s,98.73%ofaction.
- UploadManager.GetJpeg273.046ms (includes limiter wait).
- Outer SQL wrappers10.700+0.988+8.269+0.490=20.447ms. Nested SqlClient spans represent the same calls and are not summed again.
- Both PUTs200. No explicit retry event/tag was found; this does not exclude hidden AWS SDK retry/connection handling. Client HTTP span duration includes the client/network/server interaction and is not server processing time alone.
- Loki exact-Jaeger-ID query found the same completion, application timer24557ms, multipart Content-Length9,446,566bytes. The original object HEAD is9,446,384bytes; multipart overhead explains the small difference.

Current read-only S3 HEAD checks: original9,446,384bytes, LastModified08:09:58UTC; OrigSize425,151bytes, LastModified08:10:04UTC. Both nonempty ETags, HEAD200. These are current metadata observations, not historical request-body captures.

## Comparable Max1600 examples

- Friday16October09:22:20.995Moscow, trace87c97646cafc7: PUT1.044775s200; current HEAD361,302bytes, LastModified06:22:22UTC16October.
- Monday19October11:29:42.579Moscow, trace127cc1a1ed5770: PUT10.918329s200; current HEAD339,376bytes, LastModified08:30:05UTC19October. LastModified is later than this PUT span end, so later rewrites cannot be excluded; current size is a size-comparison proxy.
- Ratio of these two observed durations10.45x, at similar current sizes; this is one matched diagnostic pair, not an overall p95 or a normalized regression estimate.

Additional Friday OrigSize samples:243,099bytes/0.603486s and130,917bytes/1.475443s; Sunday OrigSize126,960bytes/1.705941s. Today OrigSize425,151bytes/5.563115s. Sizes differ, so these alone do not provide a controlled size-normalized comparison.

## Provider status evidence

Official Selectel incident [406285: S3 access problems](https://selectel.live/incidents/406285?lang=ru) reports reduced S3 upload speed and intermittent500errors in ru-1/ru-3, opened18October20:53Moscow and marked resolved19October05:47Moscow. Bucket location read earlier isru-1. Our observed slow PUTs11:09/11:29Moscow are later than the published resolution; the official incident supports asking Selectel to correlate the symptoms, but does not prove these later requests belong to the same incident or that409has the same cause. Current generic resource-capacity warnings on the status page were not treated as proof of S3 performance failure.

## Assessment and limits

Slow S3 writes, rather than SQL or JPEG, dominate at least one retained representative photo upload. This is stronger evidence than the earlier inference from total Content duration. It makes the storage/transport path a justified focus. It still does not prove the provider-internal cause, a sustained rate increase across all traffic, or that the seven unsampled Shift248 uploads had the same distribution. A provider investigation should correlate exact UTC times/bucket/object keys and client egress route; historical S3 PUT request IDs were not captured in the available spans. Existing later HEAD request IDs refer to different reads, not those writes.

## Changes and risks

Only local diagnostic artifacts and KB documentation changed. No application configuration, retry behavior, S3 objects or external tickets/messages changed. Per-object key details for the three slow writes remain in the local diagnostic artifact `/tmp/tempo-s3-study/slow-s3-keys.json`; no credentials or signed URLs are included here. Open follow-up is tracked in ~/ai/TODO.md.

## New current provider incident406434 supplied by user

User linked [Selectelincident406434](https://selectel.live/incidents/406434). Direct HTTPS read of the official page on2026-10-19 shortly after14:00Moscow succeeded; initial web-search/open cache did not yet have this new page. Public status is Minor incident/Problem, published19October13:57Moscow, affecting S3ru-1/ru-3 (includingru-1a/b/c andru-3a/b/c). Provider reports reduced upload speed and intermittent500errors. It explicitly says immediate retries amplify load and can produceHTTP409and5xxseries.

Our bucket isru-1 and observed symptoms include slow successfulPUTs and409, so the provider now explicitly confirms the same class of ongoing problems in the matching region. This strengthens provider-side S3 degradation as the leading explanation. Publication13:57is later than observed10:23Business,11:09slowPUT, and11:29slowthumbnail; the page alone does not establish the exact earlier onset or retrospectively prove every morning error is part of this incident. The earlier406285was markedresolved05:47; keep the two incident identities/timelines separate.

No retry/configuration change, upload replay, ticket or external message was issued. Existing client/SDK retry behavior has not been fully audited; avoid claiming immediate retries were the proven cause of an individual409. The provider's statement is a mechanism warning and reported current incident evidence.

## User-confirmed incident closure (2026-10-19)

The user confirmed the Selectel incident as the cause and requested closure of the three Content/production S3 backlog items: provider correlation, Shift248/Business timeout follow-up, and PUT409/anomalous-thumbnail diagnostics. These items are closed by user decision; no further investigation, repair, runtime change or external tracker update was performed. Earlier measurement limits remain historical evidence, not requirements to reopen the incident. Final C2C task existence and object repair were not independently verified.
