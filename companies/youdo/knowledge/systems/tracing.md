---
system: tracing
status: verified
checked: 2026-06-10
tags: [tracing, jaeger, tempo, youdo, Tracing:Hosts, nomad, consul]
---
# YouDo tracing configuration

Date: 2026-06-10
Project: /home/slnnk/git/youdo
Context: investigation of `Tracing:Hosts` for `YouDo.Web.MvcApplication`.

## How `Tracing:Hosts` works

- `Tracing:Hosts` keys are matched against application name resolved by `HostAppInfoResolver.Resolve()`, not HTTP request host.
- Matching is implemented in `YouDo.Bootstrapping/Tracing/TracingContainerBuilderExtensions.cs`.
- The selected config sets global `TracingSwitch.Enabled`; ASP.NET Core middleware checks only this switch at request time.
- `YouDo.Web.MvcApplication` has assembly name `YouDo.Web.MvcApplication`, so it should match `*.Web.*`.
- `YouDo.Web.Moderation` is explicitly disabled and wins over `*.Web.*` because exact keys are ordered first.
- MVC app has tracing middleware/filter wired in `YouDo.Web.MvcApplication/Startup.cs`: `mvcOptions.AddYouDoTracing()` and `app.UseYouDoTracing()`.
- Local repo `YouDo.Configuration/environment.json` currently has `*.Web.*` rate `1` and Jaeger UDP endpoint configured under `Tracing:Jaeger`.

## Debug checklist

- Confirm runtime uses the same `environment.json`/environment config version that was edited.
- Check startup logs for `YouDo.Bootstrapping.Tracing`: `Tracing enabled=... rate=... conf=...`.
- For `YouDo.Web.MvcApplication`, expected log is enabled true, rate 1, conf `*.Web.*`.
- If startup is correct and there are no traces, check UDP delivery to Jaeger agent and service name `back/youdo/youdo.web.mvcapplication` in Jaeger.
- If another tracer is registered first in the same process, `TracingInitializationTask` does not replace `GlobalTracer`.

## Probe URLs for `YouDo.Web.MvcApplication`

- `GET /api/auto/makers` maps to `AutoController.Makers`; read-only API endpoint, no auth attribute in controller.
- `GET /api/suggestion/city?query=москва` maps to `SuggestionController.City`; read-only suggestion endpoint.
- `GET /Robots.txt` maps to `ServiceController.Robots`; read-only static-ish file response.
- `GET /x/Service/NewGuid` maps via ajax route `x/{controller}/{action}` to `ServiceController.NewGuid`; returns a GUID.
- Query string can include `trace_probe=<unique>` and be searched by `http.url` in Tempo.

## Delivery path (test1, verified 2026-06-10)

- Nomad job: `youdo-test1`, allocation `youdo-test1.youdo-test1-web[0]`, task `youdo-test1-web-mvcapplication` on node `nomad-agent-test-03`.
- Runtime `environment.json` for web-mvcapplication has `Tracing.Hosts[*.Web.*].Enabled=true` and `Rate=1`.
- Runtime `Tracing.Jaeger` for test1 is `Host=tempo.service.consul`, `Port=14250`.
- Application code uses Jaeger `UdpSender(host, port, ...)`, so it sends Jaeger compact thrift over UDP.
- `tempo.service.consul:14250` is Jaeger gRPC/TCP receiver, not UDP compact. This explains missing spans despite tracing enabled.
- `jaeger-agent` system job exposes compact UDP port `6831` on all Nomad nodes and forwards to `tempo.service.consul:14250` over gRPC.
- Likely fix: point app `Tracing.Jaeger` to `jaeger-agent.service.consul:6831` (or another valid Jaeger compact UDP endpoint), not Tempo gRPC port.

## Related log entries

- [`../log/2026-06-09-tracing-web-mvcapplication-health-only.md`](../log/2026-06-09-tracing-web-mvcapplication-health-only.md): only `/health/live` traces visible in Tempo (sampler rate, search limit).

## Portable lesson

[`~/ai/general/knowledge/jaeger/udp-sender-pointed-at-grpc-port-no-spans.md`](../../../../general/knowledge/jaeger/udp-sender-pointed-at-grpc-port-no-spans.md)
