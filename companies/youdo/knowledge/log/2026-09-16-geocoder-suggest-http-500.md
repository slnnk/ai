---
system: geocoder
status: hypothesis
checked: 2026-09-16
tags: [http-500, yandex-suggest, dadata, exceptional, serilog, logging, nomad]
---
# GeoCoder `/api/geocoder/Suggest` HTTP 500 investigation

Date: 2026-09-16

## Task

Explain an HTTP 500 on `GET /api/geocoder/Suggest` reported through an Exceptional record.

## Context

- Repository: `/home/slnnk/git/geocoder`
- Safe origin: `git@gitlab.youdo.sg:youdo/microservices/geocoder.git`
- Checked snapshot: branch `Site-24027_add_metrics`, commit `6cce615`
- Observed request: `GET /api/geocoder/Suggest` through `geocoder.proxy.youdo.local`
- Observed result: HTTP 500 in 271 ms at 2026-09-16 13:44:47 MSK; Exceptional record ID shown as `415f8295007a`

## Findings

### Verified request path

1. `GeoCoderController.Suggest` constructs an optional `GeoPoint` and calls `GeoCoderManager.SuggestAsync`.
2. `GeoCoderManager` calls the configured primary geocoder and catches any exception; it then calls the secondary provider. With the default configuration, Yandex is primary and DaData is secondary.
3. Yandex calls `https://suggest-maps.yandex.ru/v1/suggest`; DaData fallback calls `/suggest/address` at its configured base URL.
4. A client-visible 500 therefore normally means that the Yandex attempt failed and the DaData fallback also failed, or that processing after the provider call failed.

### Logging limitation

The displayed `YouDo.Serilog.Sinks.Exceptional.ErrorLevels.ErrorMessageException` is a synthetic exception created by the Exceptional sink for an error log event. It is not the root exception.

`LoggingMiddleware` sees status 500 in `finally` and tries to read `IExceptionHandlerFeature`, but the downstream MVC exception handler no longer exposes the original exception there. It consequently logs `GET /api/geocoder/Suggest:` with an empty message and a null exception. The Exceptional page therefore cannot identify the actual failure.

The outgoing `RequestLoggingDelegatingHandler` logs provider request/response details only after `base.SendAsync` returns. DNS, connect, TLS, and timeout failures throw before that log statement and are not recorded by this handler.

### Configuration risk

The production Nomad template injects `GeoServices__Yandex__ApiKey` and `GeoServices__DaData__Token`, but does not inject `GeoServices__Yandex__SuggestApiKey`. Yandex Suggest therefore falls back to the value packaged in `appsettings.json`. Do not copy key/token values into notes. Verify the live allocation environment and the Vault item `secret/dotnet/geocoder`; add a dedicated `YANDEX_SUGGEST_API_KEY` mapping if that is the intended secret contract.

### Leading hypotheses (not yet proven)

- Missing/empty `text` or zero/missing `count` in the client query caused both providers to reject the request. The screenshot did not include the `Request.Query.*` rows.
- The packaged Yandex Suggest key is expired, revoked, or quota-limited, followed by a DaData failure.
- Network/DNS/TLS failure to both external providers.
- Provider returned an unexpected/empty payload and response mapping dereferenced a null value (for example `response.Results`).

## Open items

Next diagnostic steps:

1. In the Exceptional record, inspect `Request.Query.text` and `Request.Query.count`; a valid reproduction should include non-empty text and a positive count.
2. Correlate container stdout for 2026-09-16 10:44:47 UTC using `Request.Headers.X-Request-Id`, `traceparent`, or the visible allocation/container identity. Look for Refit `ApiException`, timeout, DNS/TLS errors, and outbound response bodies.
3. Inside the live Nomad allocation, verify only the presence/source of `GeoServices__Yandex__SuggestApiKey` (never print the secret), then test reachability and HTTP status for Yandex Suggest and DaData with safely sourced credentials.
4. Improve logging: preserve/log the caught original exception, log exceptions from `RequestLoggingDelegatingHandler`, and validate `text`/`count` at the controller boundary so bad input returns 400 rather than 500.

## Changes

No repository files or live infrastructure were changed during this diagnosis.

## Portable lesson

none
