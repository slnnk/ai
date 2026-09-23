---
system: jaeger
status: verified
checked: 2026-06-10
tags: [jaeger, tempo, udp, 6831, 14250, grpc, thrift-compact, tracing, sampling]
---
# Tracing is enabled but no spans arrive: Jaeger UDP sender configured with a gRPC/TCP port

## Symptom

Startup logs confirm tracing is on (`Tracing enabled=true rate=1`), the service name shows
up nowhere in Jaeger/Tempo, or only a few unrelated spans appear. No error is logged by the
application.

## Cause

Jaeger client libraries have two reporter transports that use different ports and protocols:

| Transport | Protocol | Typical port | Receiver |
|---|---|---|---|
| `UdpSender` (thrift compact) | UDP | 6831 | `jaeger-agent`, or Tempo/OTel collector `jaeger.thrift_compact` receiver |
| `HttpSender` / gRPC | TCP | 14268 (HTTP), 14250 (gRPC) | `jaeger-collector`, Tempo `jaeger.grpc` receiver |

Pointing a `UdpSender` at `tempo:14250` sends UDP datagrams to a port that only listens on TCP.
UDP is fire-and-forget: nothing answers, nothing fails, the client just keeps "reporting".
Typical way in: the tracing config exposes only `Host`/`Port`, someone fills in the collector
address, and the code silently constructs a UDP sender.

## Fix

- Check what the code builds (`new UdpSender(host, port, maxPacketSize)` vs an HTTP/gRPC
  sender) and match the endpoint: UDP sender -> agent/collector compact-thrift port `6831`;
  collector gRPC `14250` only for a gRPC sender.
- If a `jaeger-agent` (or OTel collector) runs as a system/daemon job on every node with
  `6831/udp` exposed, point the application at that local agent, not at the central Tempo.
- Verify the receiver actually listens on UDP: `ss -lun | grep 6831` on the target, and from
  the application host `echo | nc -u -w1 <host> 6831` (no error proves nothing; check the
  receiver's metrics/logs for received spans).
- Send a probe request with a unique marker, e.g. `?trace_probe=<uuid>`, and search by
  `http.url` in Tempo/Jaeger.

Two related pitfalls when the endpoint is right:

- A probabilistic sampler at `0.05` drops 95% of traces; temporarily set the rate to `1` for
  the service under test.
- Health-check endpoints traced every few seconds fill the "latest N traces" list (Tempo
  search `Limit: 20` by default). Raise the limit or search by the operation name of a real
  endpoint; endpoint-routed health checks keep a path-based span name
  (`asp::get::/health/live`), while MVC actions are renamed to `controller.action`.

## Limits

- UDP compact thrift has a ~65 KB datagram limit; huge spans are dropped silently as well.
- If another tracer registered `GlobalTracer` first in the same process, the configured one
  is ignored; check initialization order before blaming transport.
