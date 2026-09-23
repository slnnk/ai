---
system: tracing
status: verified
checked: 2026-06-09
tags: [tracing, tempo, jaeger, youdo, web-mvcapplication, sampler, health-check]
---
# YouDo web.mvcapplication tracing: only /health visible in Tempo

## Context

- Date: 2026-06-09
- Project/repo: /home/slnnk/git/youdo
- Context: Grafana Tempo search for service `back/youdo/youdo.web.mvcapplication` shows latest traces as `asp::get::/health/live`.

## Task

Explain why only health-check traces are visible for `YouDo.Web.MvcApplication` in Tempo.

## Findings

- `YouDo.Web.MvcApplication` registers MVC tracing filter via `mvcOptions.AddYouDoTracing()` and middleware via `UseYouDoTracing()`.
- `UseYouDoTracing()` creates a server span for every request when `TracingSwitch.Enabled` is true. Initial operation name is `asp::{method}::{path}`; MVC actions may later rename it to `asp::{controller}.{action}` via `TracingActionFilter`.
- Health checks are endpoint-routed, not MVC actions, so their operation name remains path-based: `asp::get::/health/live`.
- Tracing enablement is based on `HostAppInfoResolver.Resolve()` matched against `Tracing:Hosts`; `YouDo.Web.MvcApplication` should match `*.Web.*`.
- Sampler is `ProbabilisticSampler`; provided production snippet uses rate `0.05`, so only about 5% of root traces are reported.
- Tempo screenshot shows Search Options `Limit: 20`; health checks arrive every few seconds, so the newest 20 traces can all be health checks even if non-health traces exist deeper in the result set.

## Open items

Recommended checks:

- In Tempo, increase trace search limit and/or filter out health checks.
- Search by operation/span name for expected MVC action names (`asp::<controller>.<action>`) rather than URL paths for MVC endpoints.
- Temporarily raise sampler rate to `1` for `YouDo.Web.MvcApplication` during a controlled test, then generate a known request and check for a trace.
- Check startup logs from `YouDo.Bootstrapping.Tracing` for `Tracing enabled=true rate=... conf=*.Web.*`.
- If non-health requests still do not appear with sampler `1`, inspect middleware short-circuiting before MVC and Jaeger UDP export path to `10.16.26.62:6831`.

Follow-up investigation (2026-06-10) and the general tracing configuration map: [`../systems/tracing.md`](../systems/tracing.md).

## Portable lesson

[`~/ai/general/knowledge/jaeger/udp-sender-pointed-at-grpc-port-no-spans.md`](../../../../general/knowledge/jaeger/udp-sender-pointed-at-grpc-port-no-spans.md)
