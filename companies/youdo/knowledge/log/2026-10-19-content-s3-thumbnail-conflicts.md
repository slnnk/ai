---
system: content
status: verified
checked: 2026-10-19
tags: [content, production, s3, selectel, logreader, diagnosis]
---
# Production Content S3 thumbnail persistence errors

## Summary

The incident was closed by the user on 2026-10-19, with the Selectel incident confirmed as the cause. Historical investigation and limits follow; the final closure is recorded below.

Read-only investigation of production LogReader event `b46ada2e-8439-48f2-9cd7-5b96082275d7` found an S3 PUT HTTP 409 Conflict while persisting a generated thumbnail. The exact reason for the storage conflict remains unresolved. A broader sample contains similar failures for multiple objects and thumbnail sizes across both observed service containers; it does not establish a single-object race as the cause.

## Task and context

The user requested diagnosis and supplied LogReader access variables in `~/ai/current/.env`. No repository modifications, deployment, S3 writes or external configuration changes were authorized or performed for this investigation.

## Evidence

- Reported event: `/get.content?ContentId=21498041&size=Max1600`, bucket `youdo-photos`, key `Max1600/2026.10.19/21498041.jpeg`.
- S3 error text: HTTP 409 Conflict with no further service error information. The exception recorded by LogReader is a Serilog message exception from the application's fallback logger, not proof of an unhandled request failure.
- Latest UI list sample: 200 rows, 78 Content records, distributed across containers `a6f61e731fda` (44) and `475c98719b9d` (34).
- Eight inspected recent Content records: seven S3 HTTP409 conflicts on different keys and sizes (`Max384`, `Max1600`, `H206W280`); one `TaskCanceledException` during S3 connection establishment.
- These UI samples are not a complete time-window incident count; event rows may represent rolled-up duplicates.

## Source findings

- `src/YouDo.Content.ImageService/Gallery/ContentManager.cs:61-114`: a failed target-thumbnail read causes original-image fetch, resize and PUT. After disk fallback returns, the generated image stream is returned successfully to the caller.
- `ContentManager.cs:97-111`: the process-local semaphore covers resize only, releases before PUT, and provides no lock per object or coordination between replicas. Concurrent same-key PUT is possible, but is only a hypothesis for this incident.
- `src/YouDo.Content.ImageService/Storage/AbstractStorage.cs:121-132`: `OnlyS3` uploads fall back to disk on unsuccessful S3 result, then log an error.
- `AbstractStorage.cs:74-79`: `OnlyS3` reads exclusively from S3; they do not read the local fallback file. Missing persisted thumbnails can therefore trigger repeated regeneration.
- `src/YouDo.Content.Storage.Disk/DiskStorage.cs:114-136`: disk upload returns Success or throws. An IOException is suppressed whenever the destination file exists, without validating completeness; the success log alone is not an integrity check.
- `devops/production.hcl`: two replicas; AWS profile `s3selectel`, endpoint `https://s3.storage.selcloud.ru`, `ForcePathStyle=false`. Read-only Nomad GET confirmed job `youdo-content`, datacenter `selectel`, release `2.5.11`, two running allocations on `msk3-nomad01.youdo.corp`, with 2 and 1 historical restarts respectively. Job templates confirm the endpoint, profile and Windows-style base path; the task has no configured Docker volumes or mounts. This does not independently verify the rendered configuration inside each process.
- The configured Windows-style fallback base path `C:\youdo\storage\` is relative on Linux. With image `WORKDIR /app`, its likely location is under `/app/C:\youdo\storage\/...`; no persistent fallback mount was identified in the checked template.
- A PDB stack line differing from the current logger line does not establish a version mismatch because async sequence points can refer to the end of a block.

## Access routes and commands

- Public `https://logreader.youdo.com/login` returned WAF403 before application authentication in the investigation environment.
- Checked nginx template maps public LogReader to `http://logreader-new.proxy-sel.youdo.local`; application authentication uses a cookie login form.
- Production Nomad API: `http://nomad.service.consul:4646`; token variable `SELECTEL_PROD_NOMAD_TOKEN` in `~/ai/current/.env`, passed as `X-Nomad-Token`. Existing read-only example: `~/ai-data/nexus-pypi-recovery/nomad_periodic_version_probe.py`.
- Older established exception-store access: SSH `root@172.28.0.156`, web UI port9900; SQL database `YouDoLogsExceptions.dbo.Exceptions` in `data-mssql-1`. Read-only SQL procedure documented in `~/git/claude-code-config-infra/skills/logreader/SKILL.md`. This historical route was not needed to identify the reported event.

## Changes and risks

No application or infrastructure changes were made. No secrets or request personal data are included here. The exact S3 conflict cause and current object persistence require further evidence; the active job metadata/templates were read from Nomad, but actual image digests and process configuration were not inspected. Avoid regenerating thumbnails via public GET during diagnosis: the application GET may perform S3 PUT and database writes.

## Verification and next evidence

The reported error occurred at 2026-10-19 11:29:58 as displayed by LogReader; request header timestamp was 11:29:53+03:00. Seven sampled newer 409 events span displayed times 12:58:45–13:02:55. The eighth sample is a connection timeout in `S3Storage.GetFileStreamAsync`, not a PUT conflict. Subsequent S3 HEAD/Range GET checks are recorded below; no API query of account-level quotas was performed.

A race between concurrent thumbnail requests is possible in source, but is not established as the cause of the mass conflicts. Selectel conditional-write documentation describes 409 for changed/deleted objects, but the inspected application `PutObjectRequest` contains no explicit conditional headers; that explanation cannot be applied without the actual request/response. Capture provider request ID, response body/headers, bucket/account limits and correlate with provider logs before choosing a fix.

## Follow-up: authenticated production S3 checks

The user supplied a screenshot showing no configured bucket limits for storage volume or object count and unlimited lifetime. This is UI evidence; account/project limits were not independently queried.

Local AWS credentials profile `s3selectelprod` (location `~/.aws/credentials`) successfully authenticated read-only requests to `https://s3.storage.selcloud.ru`. No credential values were printed or copied. HeadBucket200 and GetBucketLocation200 identify bucket `youdo-photos`, location `ru-1`.

All eight exact keys from the previously inspected PUT409 events returned HeadObject200 with nonzero ContentLength. This does not establish content integrity. Original reported key `Max1600/2026.10.19/21498041.jpeg`: 311125 bytes, LastModified `2026-10-19T08:30:25Z` (11:30:25 Moscow, 27 seconds after displayed error time), ETag `9c06e60f7636a422de9f07e9e8f337da`. Range GET0–31 returned206 and JPEG magic; exact-prefix ListObjectsV2 returned the object. Successful later persistence is confirmed; it does not identify the reason for the earlier409.

A distinct sampled key is anomalous: `Max384/2026.10.19/21498533.jpeg`:

- HeadObject200, length34538, LastModified `2026-10-19T09:58:17Z`, ETag empty string.
- Range GET0–31 twice returned206, with `application/octet-stream`, empty ETag, and a zero-filled prefix (first24 bytes explicitly inspected); it is not a valid JPEG header.
- Exact-prefix ListObjectsV2 (`MaxKeys=1`) twice returned200 with no object entries, despite successful HEAD/GET.
- First Range response at `2026-10-19T10:10:43Z`: request ID `be38a340-e2f1-40f4-8b46-76750a19725b`.
- Repeat at `2026-10-19T10:16:01Z`: request ID `61d4eb9c-fd57-4005-a575-b1a81cf7892f`.
- Storage-policy headers report `Policy-0`, index0.

This is confirmed anomalous object/read/list behavior at the S3 API boundary, independently of application fallback. Whether it is caused by storage-side partial-write handling, an incomplete/concurrent application upload, gateway behavior or another mechanism remains unresolved. Do not label ordinary same-key concurrency as the proven cause of409. Provider support can correlate the read request IDs and historical failed PUT window. No PUT, DELETE, object repair or public image GET was issued.

## Related Business timeout: possible dependency, unproven event correlation

User supplied production Business error at `2026-10-19T10:23:36.1047405+03:00`, ShiftId248, TraceId `abaebdf3a9760781769ffbf774f5f330`, method `IYouDoApiClient.CreateShiftTaskAsync`. HttpClient reports configured30s timeout while waiting for initial HTTP response data. Socket cancellation125 is nested under cancellation caused by this deadline; it alone does not establish an independent network fault.

Checkout source confirms a conditional synchronous dependency:

1. `youdo.business/YouDo.Business.Managers/Handlers/Shifts/CreateShiftC2CTask.cs:54-61` prepares photo attachments before invoking C2C. `YouDo.Api.Client/IYouDoApiClient.cs:57-75` sends multipart `POST /v1/tasks/shifts` including binary images.
2. `youdo/API/YouDo.API/Managers/ShiftTaskApiManager.cs:106-131` awaits each photo upload sequentially before task creation, when Images.Count>0.
3. `youdo/YouDo.Managers/Contents/ContentsManager.cs:397-408` awaits `_contentApi.UploadImagesAsync` using temporary gallery type. Thus slow Content/S3 writes may exhaust the Business request deadline.
4. `youdo.business/YouDo.Api.Client/YouDoApiModule.cs:23-26,44` configures timeout30s; retry policy handles HttpRequestException/service-not-registered, not every timeout. Total deadline is not proof that all30s were spent in Content.
5. `RequestLoggingDelegatingHandler.cs:105-118` only logs call information after awaited SendAsync returns; exceptions can bypass URL/body response logging.

The timeout occurred approximately one hour before the initially reported Content409 at11:29:58Moscow. The available samples do not establish Content health at10:23. No shared correlation ID, Shift248 photo count, upstream access logs or downstream timings were retrieved. Other monolith dependencies (SQL, suggestions, geocoding) remain possible. Correlation requires exact outbound URL/upstream and timings near10:23:06–10:23:36Moscow (07:23:06–07:23:36UTC), whether Shift248 included photos, and corresponding Content upload logs. The inspected source path was not independently matched to production image commits.

A client timeout does not prove that task creation was rolled back or canceled on the monolith. Verify whether the C2C task was created before retrying. No retry or production mutation was performed.

## Historical Content window around Business Shift248 timeout

Read-only SQL on sc-except01 exception database confirmed the original GUID matches application `YouDo.Content`, machine475c98719b9d, CreationDate2026-10-19T08:29:58.977UTC. Thus the historical query uses the same store as the supplied public LogReader detail.

Exact Business request deadline window2026-10-19 10:23:06–10:23:36.105Moscow (07:23:06–07:23:36.105UTC): zero Content rows by CreationDate; an additional query matching either CreationDate or LastLogDate also returned no rows. No DeletionDate filter was applied, so soft-deleted rows were included. This establishes absence of recorded exceptions, not absence of slow requests.

Expanded10:15–10:30Moscow results, all URL `/get.content`:

| Moscow time | GUID | Finding |
| --- | --- | --- |
| 10:16:37.823 | D1FD9F8E-DEDE-4D3E-B8BD-C03ECEED90FD | S3 PUT409, Max1600/2026.10.19/21497771.jpeg, disk fallback |
| 10:17:29.380 | 45A3FAAF-64FA-4C26-8D9A-B92E27856968 | S3 PUT409, Max1600/2026.10.19/21497710.jpeg, disk fallback |
| 10:21:57.340 | 7E0F0DC1-14FE-45BB-8271-08C4003DD39F | S3 PUT409, Max1600/2026.10.19/21497785.jpeg, container475c98719b9d |
| 10:21:57.357 | 6CFC11D0-8F9E-43F8-90E3-6813FB7DF8F7 | S3 PUT409, Max1600/2026.10.19/21497784.jpeg, containera6f61e731fda |
| 10:26:38.500 | DAC25F81-F69E-45ED-8619-938C511BF996 | Amazon.Runtime.AmazonClientException: Expected hash not equal to calculated hash; HashStream.CalculateHash/Dispose stack |
| 10:26:38.517 | C32F777D-E342-4A79-9990-4B0968D4E25C | InvalidOperationException: StatusCode cannot be set because the response has already started |
| 10:29:12.740 | 0148D522-028D-4355-8C85-C9A12FBCCC7D | TaskCanceledException: The operation was canceled |

All seven rows had DuplicateCount1 and LastLogDateNULL. No Content upload-route exception was found in this15-minute sample. Content/S3 anomalies predated the previously inspected11:29event; however the historical records do not prove the Business timeout was caused by Content. Correlation still needs Shift248 attachment count and monolith/downstream request timings. The checksum error and following response-started error are17ms apart on the same container, consistent with a cascading response failure, but a shared request identifier was not retrieved to prove this.

## Confirmed Shift248 timeout correlation from production Loki

This supersedes the earlier unproven-correlation assessment. The user identified production Loki `http://loki.infra.youdo.corp`, deployed in Kubernetes `mks-infra` (local context `admin@mks-infra`, namespace `loki`). Read-only API queries worked without authentication/tenant header. GET labels identified `job_name` selectors `youdo-web`, `youdo-business`, `youdo-content` and `task_name` values `web-api`, `youdo-business-automation-web`, `youdo-content-api`.

Production Nomad job is `youdo-web`, metadata VERSION `Release-2.1003`. API has10allocations. At inspection7retained stdout covering10:23 and3had already rotated that window. Bounded stdout inspection found only informational records, no matching trace or shift route. Microsoft/HttpClient info suppression and post-response-only outbound logging limit interpretation; stdout absence was not evidence of no request.

Loki query for10:20–10:27Moscow (07:20–07:27UTC):

```logql
{job_name=~"youdo-web|youdo-business|youdo-content"} |= "abaebdf3a9760781769ffbf774f5f330"
```

Returned36records:35Content Debug/Verbose and the exact Business Error. All Content calls are `/content.contentUpload`, temporary gallery `95c8becc-61a9-4c62-a4c8-29eeca9eff4a`. Seven sequential uploads all report ResultTrue:

| Upload | Start Moscow | Finish Moscow | Logged duration seconds |
| --- | --- | --- | --- |
| 1 | 10:23:06.137 | 10:23:10.038 | 3.900 |
| 2 | 10:23:10.043 | 10:23:14.192 | 4.147 |
| 3 | 10:23:14.197 | 10:23:18.547 | 4.349 |
| 4 | 10:23:18.554 | 10:23:26.352 | 7.796 |
| 5 | 10:23:26.359 | 10:23:33.857 | 7.497 |
| 6 | 10:23:33.864 | 10:23:38.003 | 4.137 |
| 7 | 10:23:38.007 | 10:23:43.911 | 5.903 |

Sum of logged upload durations37.729s; end-to-end sequence approximately37.775s. Business30s deadline expired at10:23:36.1047405 while sixth upload was running. Sixth and seventh uploads finished after Business stopped waiting. Therefore cumulative synchronous Content upload latency is confirmed sufficient to cause the observed Business timeout for Shift248. No S3409 or other Content errors are present in this trace. The reason each upload takes3.9–7.8s remains undetermined; source UploadManager includes database operations, original/storage writes and image decoding/conversion, not only S3. Per-stage spans/timings are needed to distinguish those costs.

Broader Content query10:20–10:27 returned1709records (limit2000, no saturation); matching409events at10:21:57 belong to different traces and `/get.content`. Thus contemporaneous S3 faults are real, but causation of these successful slow uploads by409 is not established. Task creation after upload completion was not checked; do not blindly retry a non-idempotent create after client timeout.

Raw query outputs stayed in `/tmp`; only sanitized timing, IDs and diagnostic evidence are recorded here. No secrets or request payloads were copied into KB. No deployment/configuration/API mutation was performed.

## Deeper stage attribution investigation (2026-10-19)

Exact correlation is established by W3C trace `abaebdf3a9760781769ffbf774f5f330`. The monolith synchronously uploaded seven photos sequentially through Content as part of C2C task creation; final C2C task state was not checked. Content processed the sequence from10:23:06.137 to10:23:43.912MSK. Business hit its30-second HTTP deadline at10:23:36.105 while the sixth upload was running; Content continued processing after that cancellation. All seven Content completions report `Result: True`.

| Upload | Duration ms | Multipart request bytes |
|---|---:|---:|
| 1 | 3900 | 345101 |
| 2 | 4147 | 398366 |
| 3 | 4349 | 398046 |
| 4 | 7796 | 490475 |
| 5 | 7497 | 536362 |
| 6 | 4137 | 512053 |
| 7 | 5903 | 40898 |

Multipart lengths include form overhead; they are not original image pixel dimensions or decoded memory sizes. The smallest request still took5.903seconds, so transmission byte size alone does not explain the server processing delay.

### Measurement boundaries and code path

`UploadController.SiteUpload` starts its stopwatch inside the action after multipart/model binding (`src/YouDo.Content.Api/Controllers/Handlers/UploadController.cs:81-85`). It measures copying the bound file into memory (`:102-110`) plus `UploadManager.UploadAsync`, and logs before response serialization (`:112-123`). Thus the4-8second durations reflect server work after binding rather than only initial incoming body transmission.

Each upload performs gallery/content SQL operations, saves the original object, converts the image to JPEG while holding the upload limiter, saves the converted OrigSize object, and updates SQL IsBroken status (`src/YouDo.Content.ImageService/Gallery/UploadManager.cs:72-109`). The conversion span begins before limiter acquisition (`:117-124`). Vips uses optimized progressive JPEG (`src/YouDo.Content.Image.Vips/Processor.cs:109-119`). The observed source path contains two sequential storage writes per photo,14writes across seven photos; individual write durations were not logged.

The checked production template specifies Vips, concurrency1000 for upload/thumbnail processing, ClearMemoryAfter0, CPU reservation500MHz and memory6144MiB/max8192MiB. Runtime correspondence must be checked before attributing behavior to these template settings. CPU reservation is not a hard CPU quota.

### Historical CPU evidence

Nomad metrics from the production VictoriaMetrics backend contain four10-second samples at10:23:10,20,30,40MSK across the upload interval:

- Host40-core mean CPU utilization:29.74%,32.58%,34.85%,31.33%; overall mean32.13%, maximum per-sample host mean34.85%. One individual core sample reached98%.
- Content allocation `6fc52105`: reported cpu_total_percent mean30.351%, max88.116%; cpu_total_ticks mean910.531MHz, max2643.469MHz.
- Content allocation `9109cb90`: reported cpu_total_percent mean13.237%, max27.669%; cpu_total_ticks mean397.119MHz, max830.084MHz.
- Both allocations' `nomad_client_allocs_cpu_throttled_time` and `nomad_client_allocs_cpu_throttled_periods` remained0 at all four samples. Observed CPU use can exceed the500MHz reservation.

These samples show no recorded CFS throttling or global host CPU saturation. They do not exclude short pauses below the10-second resolution, a busy individual CPU, image-specific conversion cost or other per-request delays. Metric percentages are the exported Nomad metric values; they are not percentages of the500MHz reservation.

### Attribution limits

The exact request was unsampled in both W3C and legacy Jaeger contexts. No persisted per-stage timings were recovered; source search found no custom Prometheus histograms separating SQL, S3 and Vips processing. Successful Content uploads in this trace do not contain S3 409 errors. Nearby /get.content requests have409errors, but those are different traces and do not establish the cause of these upload durations.

Established cause of the Business deadline: synchronous sequential photo handling accumulated beyond30seconds. The precise reason individual Content uploads took3.9-7.8seconds, and the division between SQL, storage, limiter waiting and Vips, remain unresolved from retained historical evidence. No production writes or repeated upload experiments are needed to state this limit; none are proposed as already authorized.

### Additional counter and backend checks

Read-only cAdvisor query at10:24:00Moscow using increase(container_cpu_usage_seconds_total[1m]) for the two exact DockerIDs yielded21.886 and22.345CPU-seconds per container during10:23–10:24. These are aggregate container costs across all concurrent requests and extrapolated counter windows, not per-photo CPU timings; they cannot attribute this trace to CPU conversion or exclude it.

VictoriaMetrics query access is `http://vmauth.infra.youdo.corp/api/v1/query` and `/query_range`. Existing read-account credential location: `~/git/infra-tf/modules/victoriametrics/main.tf`, second `vmauth.config.users` object, whose route points to `/select/0/prometheus`. Credentials were parsed only in memory, never printed/copied. Relevant labels: exported_job=youdo-content, task=youdo-content-api, alloc_id, node=msk3-nomad01.youdo.corp.

Tempo2.6.1 answered build/search/trace read APIs; a different stored trace was successfully retrieved as a positive control. Specific W3C and actual Jaeger trace lookups returned404. TraceQL searches for StorageUploadFile and UploadManager.GetJpeg in the10:00–11:00window returned no records. Therefore missing detailed historical evidence is real for this investigation, not an established backend availability failure.

A conclusive split requires a sampled trace of a representative ordinary photo-upload request, with StorageUploadFile spans and UploadManager.GetJpeg, and timing around uncovered SQL/controller segments. Production replay of Shift248 is not authorized and may duplicate a C2C task; no replay or sampling/configuration change was performed.


## Follow-up superseding the lack of stage attribution for all uploads

A broader Tempo search found sampled OTHERphoto uploads. Trace148ae312ae4a95 proves S3PUTs consume24.246of24.559s(98.73%), JPEG273ms and outerSQL20.447ms. A Max1600PUT is10.918s today versus0.957–2.210s across three Friday examples. This does not reconstruct unsampledShift248 stages, but establishes a real S3write-path latency issue in retained representative traces. See [S3latency comparison](2026-10-19-content-selectel-s3-put-latency-comparison.md) for query coverage, sample counts, sizes and official Selectelincident406285timing.

## Provider confirms current S3 incident406434

User supplied https://selectel.live/incidents/406434; official page read directly2026-10-19: published13:57Moscow, current S3 slowupload/500incident inru-1/ru-3, warning instantretries mayproduce409/5xx. This matches bucketru-1 and localS3symptoms, strengthens providerdegradation hypothesis, but the publication timestamp does not independently prove onsetbefore morning10:23. See [latencycomparison](2026-10-19-content-selectel-s3-put-latency-comparison.md) for both406434and earlierresolved406285timelines.

## User-confirmed incident closure (2026-10-19)

The user confirmed the Selectel incident as the cause and requested closure of the three Content/production S3 backlog items: provider correlation, Shift248/Business timeout follow-up, and PUT409/anomalous-thumbnail diagnostics. These items are closed by user decision; no further investigation, repair, runtime change or external tracker update was performed. Earlier measurement limits remain historical evidence, not requirements to reopen the incident. Final C2C task existence and object repair were not independently verified.
