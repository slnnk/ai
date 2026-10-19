---
system: content
status: verified
checked: 2026-10-19
tags: [content, production, s3, selectel, nomad]
---
# Content production storage and diagnostics

## Summary

Production job `youdo-content` in Nomad datacenter `selectel` serves generated image thumbnails. On 2026-10-19 job metadata reports release `2.5.11`, with two running allocations on `msk3-nomad01.youdo.corp`. The user confirmed the Selectel incident as the cause of the upload latency/thumbnail PUT409 incident on 2026-10-19 and closed all three related diagnostics items. Historical evidence and measurement limits below are retained; they do not reopen the incident.

## Components and access

- Repository: `~/git/youdo.content`; registry entry in `../repos.md`.
- Nomad API: `http://nomad.service.consul:4646`; read-only GET `/v1/job/youdo-content` and `/v1/job/youdo-content/allocations`. Access token location: `~/ai/current/.env`, variable `SELECTEL_PROD_NOMAD_TOKEN`, header `X-Nomad-Token`.
- Job image metadata: `nexus.youdo.com/youdo/microservices/youdo.content`, version `2.5.11`; configured image `${NOMAD_META_IMAGE}/api:${NOMAD_META_VERSION}`. Image digest unverified.
- S3 endpoint in active job template: `https://s3.storage.selcloud.ru`, AWS profile `s3selectel`, `ForcePathStyle=false`, credential mount target `/nonroot/.aws/credentials`. Never record credential contents.
- Thumbnail bucket: `youdo-photos`; keys include size/date/content ID.
- Public logs: `https://logreader.youdo.com`; nginx backend `http://logreader-new.proxy-sel.youdo.local`. Cookie form login uses `.env` variables `SELECTEL_PROD_LOGREADER_USER` and `SELECTEL_PROD_LOGREADER_PASSQORD` (spelling retained). Public login returned WAF403 from the investigation environment; internal backend login succeeded.

## Storage behavior and operational limits

`ContentManager.GetThumbnailAsync` regenerates a thumbnail after unsuccessful target read and persists it using `S3Storage.PutObjectAsync`. In `OnlyS3`, a failed PUT falls back to disk and logs an error, while the caller can still receive the generated image. Later reads use S3 exclusively. Thus a disk fallback does not repair the S3 copy or serve subsequent reads.

The active job template sets Windows-style base path `C:\youdo\storage\`. On Linux this is relative; no persistent Docker mount for fallback data was present in the active task configuration. File existence/integrity and actual rendered paths were not checked.

## Diagnostic boundaries

Do not reproduce by calling public `/get.content` without reviewing effects: a GET may trigger thumbnail generation, S3 PUT and database changes. Read the exception detail and existing service/S3 records first. No production changes were made during this investigation.

## Evidence

[2026-10-19 S3 thumbnail conflict investigation](../log/2026-10-19-content-s3-thumbnail-conflicts.md).

## S3 access and anomalous object (2026-10-19)

Local AWS profile `s3selectelprod` in `~/.aws/credentials` has verified read access to bucket `youdo-photos` in `ru-1`. User UI screenshot shows bucket volume/object-count limits disabled. All eight sampled failed-PUT keys later returned HEAD200; the original reported thumbnail also passed Range JPEG-header and ListObjects checks.

One sampled thumbnail `Max384/2026.10.19/21498533.jpeg` repeatedly returns a zero-filled prefix, empty ETag, and application/octet-stream via Range GET, while exact-prefix listing returns no entries. HEAD/GET success alone is therefore insufficient to establish thumbnail validity. Provider root cause remains unverified. Read request IDs and timestamps are in the linked investigation log; do not repair/delete without explicit authorization.

## Business shift creation dependency (source inspected 2026-10-19)

When a Business shift has TaskPhoto attachments, multipart `POST /v1/tasks/shifts` to the C2C monolith synchronously uploads each image through Content before task creation (`ShiftTaskApiManager.cs:106-131` -> `ContentsManager.UploadTempImageAsync`). Business configures a30s HttpClient timeout. Content/S3 delays can therefore propagate as a Business timeout. This conditional dependency is verified in local source; Loki later confirmed Shift248 timeout at10:23:36Moscow occurred during a sequence of seven successful Content uploads totalling37.729s; linkage to S3409 remains unproven. See the investigation log for evidence and missing correlation data.

## Historical incident timing

Direct exception-store queries on2026-10-19 found S3 PUT409 as early as10:16Moscow, on both containers at10:21:57, and a checksum mismatch at10:26:38. Exact10:23:06–10:23:36.105Moscow window has no Content exception by CreationDate or LastLogDate, including soft-deleted rows. All seven entries in expanded10:15–10:30window concern `/get.content`; no upload-route exception was found. This does not rule out slow uploads without an exception. See linked log for GUIDs and limits.

## Confirmed Business timeout and production Loki

Production Loki is accessible at `http://loki.infra.youdo.corp` in Kubernetes `mks-infra`, namespace `loki`, context `admin@mks-infra`. Query API works without auth/tenant header. Relevant selectors: `{job_name="youdo-content"}`, `{job_name="youdo-business"}`, `{job_name="youdo-web",task_name="web-api"}`. Use exact trace ID across jobs; warn/error-only exception storage misses successful slow uploads.

Trace `abaebdf3a9760781769ffbf774f5f330` proves seven sequential temporary-image uploads from10:23:06.137to10:23:43.911Moscow, total logged37.729s, all successful. Business expires its30s deadline during upload6 at10:23:36.1047405. Processing continues afterwards. This confirms cumulative Content-call latency caused the timeout; it does not prove S3409 caused the latency. Source-stage timing and final C2C task existence remain unchecked. Full timeline is in the linked investigation log.

At investigation time Nomad `youdo-web` release metadata `Release-2.1003` has10API replicas; stdout retains target10:23window in7/10. Prefer Loki for historical cross-service correlation over per-allocation stdout rotation.

## Stage-attribution limit and CPU checks (2026-10-19)

UploadController's timer starts after multipart/model binding. Seven request sizes were41–536KB, but durations3.9–7.8s are server processing time. Source path performs SQL operations, two storage writes and Vips progressive JPEG conversion under an upload limiter. No stage timing was recovered for the incident.

Both tracing contexts are unsampled: W3C abaebdf3a9760781769ffbf774f5f330(flags00), custom Jaeger450a530e4aeb1d75(flags0). Tempo queries of both IDs returned404; other trace retrieval succeeded. All19nearby upload completions in Loki also had Jaeger flags0. No source-level custom Prometheus stage histograms were found. Use production Tempo in mks-infra/monitoring at tempo.infra.youdo.corp for a future sampled trace; distinct Activity and Jaeger IDs must be checked.

Historical Nomad metrics10:15–10:30show zero recorded CPUthrottled_time/periods for both Content allocations. During upload interval the40core host averaged32.13%CPU in10second samples, peak host average34.85%; actual Content CPU use exceeded500MHz reservation. These do not establish CPU starvation, nor exclude conversion or short pauses. Aggregate cAdvisor CPUcounter increments21.886/22.345CPU-seconds per container in10:23–10:24 cannot be assigned to individual requests. Exact SQL/S3/Vips attribution remains unresolved without sampled per-stage evidence.

## Sampled S3 PUT evidence (2026-10-19)

Broader historical Tempo searches recovered sampled OTHERphoto uploads. Query actual client spans `span.http.method="PUT"` and `span.peer.hostname="youdo-photos.s3.storage.selcloud.ru"`; restricting to one hour or inbound POST had missed these. Trace148ae312ae4a95at11:09Moscow has24.246s in two successful S3PUTs of24.559s action(98.73%); JPEG273ms, outerSQL20.447ms. A similar-current-size Max1600example today339KB/10.918s versusFriday361KB/1.045s supports degradation on the S3HTTP path. Samples are small; file sizes and later rewrites limit comparison. ExactShift248 remains unsampled. Official Selectelincident406285reported slowS3uploads inru-1/ru-3 from18October20:53to19October05:47Moscow, but sampled slow11:09/11:29requests are after its published resolution. Provider-internal cause versus transport/client handling remains unproven. [Detailed comparison](../log/2026-10-19-content-selectel-s3-put-latency-comparison.md).

## Current provider status2026-10-19

Official [Selectel406434](https://selectel.live/incidents/406434), published13:57Moscow, confirms reduced S3uploadspeed/intermittent500 inru-1/ru-3 and explains immediate retries can amplify409/5xx. Bucketru-1 and observedslowPUT/409match. This strengthens storage-provider degradation as a leading diagnosis; earlier morning incidents require onset correlation because publication is later. No retry/runtime changes were made. Preserve distinction from earlier406285resolved05:47.

## User-confirmed incident closure (2026-10-19)

The user confirmed the Selectel incident as the cause and requested closure of the three Content/production S3 backlog items: provider correlation, Shift248/Business timeout follow-up, and PUT409/anomalous-thumbnail diagnostics. These items are closed by user decision; no further investigation, repair, runtime change or external tracker update was performed. Earlier measurement limits remain historical evidence, not requirements to reopen the incident. Final C2C task existence and object repair were not independently verified.

HoustonV2Mock Buildx compatibility is a separate Nomad-test CI proposal, unrelated to Content or production S3. Its accidental placement in the Content TODO section was corrected.
