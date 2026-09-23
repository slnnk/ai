---
system: dotnet
status: verified
checked: 2026-09-18
tags: [aspnet, docker, ASPNETCORE_HTTP_PORTS, ASPNETCORE_URLS, port-8080, healthcheck, base-image]
---
# Health check on port 80 fails after moving to a .NET 8+ ASP.NET image

## Symptom

A service migrated to `mcr.microsoft.com/dotnet/aspnet:8.0` (or 9.0/10.0, or a corporate
image built on them) starts cleanly, logs show hosted services running, but the
orchestrator's HTTP check on container port 80 stays unhealthy with `connection refused`. The
same manifest worked with .NET 6/7 images.

## Cause

Since .NET 8 the official ASP.NET images set `ASPNETCORE_HTTP_PORTS=8080` and run as the
non-root `app` user (`APP_UID=1654`); Kestrel therefore listens on **8080**, not 80. Older
images defaulted to `ASPNETCORE_URLS=http://+:80`. If an intermediate corporate base image used
to pin the old defaults and the new one does not, every consumer silently changes port.
Application-level port settings read by a custom host builder (for example a
`Core:Port` option) are ignored when the app uses plain `WebApplication.CreateBuilder`.

## Fix

Verify inside the container without dumping the whole environment:

```bash
env | grep -E '^ASPNETCORE_(HTTP_PORTS|URLS)='
curl -sv --max-time 2 http://127.0.0.1:80/health
curl -sv --max-time 2 http://127.0.0.1:8080/health
```

Then choose one contract and apply it consistently:

- Service-scoped: set `ASPNETCORE_HTTP_PORTS=80` (or `ASPNETCORE_URLS=http://+:80`) in the
  deployment environment, or change the check/port mapping to 8080. Note that Microsoft moved
  to 8080 so the image can run as the unprivileged `app` user; if your Dockerfile switches to
  `USER app`/`USER $APP_UID`, binding to 80 needs root or `CAP_NET_BIND_SERVICE`, so prefer
  mapping the check to 8080 in that case.
- Platform-scoped: if you maintain a shared base image, decide explicitly whether it restores
  `ASPNETCORE_HTTP_PORTS=80` for compatibility; document it, because the choice affects every
  consumer.
- Code-scoped: configure Kestrel from your own option (`builder.WebHost.ConfigureKestrel` /
  `UseUrls`) if the app must honour a custom port setting.

## Inverse case: CrashLoopBackOff with `SocketException (13): Permission denied` on `http://*:80`

The mirror image of the symptom above: a corporate base image still pins
`ASPNETCORE_URLS=http://*:80` (and `ASPNETCORE_HTTP_PORTS=80`), the Kubernetes chart runs the
container as non-root and expects port 8080, and every pod crash-loops at startup with

```text
System.Net.Sockets.SocketException (13): Permission denied
```

while trying to bind `http://*:80`. Setting an application-level option such as
`App__Core__Port=8080` / `Core:Port` in the ConfigMap does not help when the service does
not wire that option into Kestrel; the env var is rendered but the listen port stays 80.

Fix in the deployment values (not in the image):

```yaml
env:
  ASPNETCORE_URLS: "http://*:8080"
  # optional, keep consistent; URLS wins if both are set
  HTTP_PORTS: "8080"
```

Verify with `helm template` that the ConfigMap contains `ASPNETCORE_URLS` and that
`containerPort`/probes target 8080, then confirm in pod logs that Kestrel reports
`Now listening on: http://[::]:8080`. Checked with .NET services on Kubernetes, 2026-06.

## Limits

- `ASPNETCORE_URLS` overrides `ASPNETCORE_HTTP_PORTS`; do not set both to different values.
- A missing listen-port override shows up as *both* failed probes on 8080 and a crash on 80;
  read the container log rather than trusting the probe error alone.
- The `No XML encryptor configured` Data Protection warning seen in the same logs is
  unrelated to the health check.
- Verified on the 8.0 and 10.0 official image defaults; check `docker inspect` of your exact
  tag for the environment.
