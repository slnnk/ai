---
system: youdo-mcp
status: hypothesis
checked: 2026-09-18
tags: [nomad, yandex-test, healthcheck, aspnet, port-8080, base-images, kestrel]
---
# youdo-mcp: test Nomad health check does not reach the application

Date: 2026-09-18

Status: root-cause hypothesis is strongly supported by repository configuration; confirm on a live allocation with loopback curls to ports 80 and 8080.

## Task

Explain why the Nomad HTTP check for `/_/healthcheck` of the youdo-mcp test deployment stays unhealthy although the application starts.

## Context

- Service repository: `/home/slnnk/git/youdo-mcp` (`origin/master` inspected at `77ba31b`).
- Test deployment: per-stand GitLab job `deploy-yandex-test N/17` renders a Nomad job from `automation-test-yandex` (`a240575`).
- Runtime image: `registry.youdo.sg/youdo/base-images/microsoft/aspnet:10.0`, source in `/home/slnnk/git/base-images` (`eddc5ac`).
- Symptom: the service process starts and `KnownClientsSeeder` creates the predefined OAuth clients, but the Nomad HTTP check for `/_/healthcheck` stays unhealthy.

## Findings

1. The Data Protection message `No XML encryptor configured` is a non-fatal warning. The keys are persisted by the application to PostgreSQL; lack of an XML encryptor does not prevent Kestrel from starting or make the health endpoint unhealthy.
2. Successful messages from `KnownClientsSeeder` show that startup reached the hosted service and that the database/schema were usable.
3. `devops/config.yml` configures `webEx_check_path=/_/healthcheck` and exports `YouDo__Core__Port=80`.
4. The `automation-test-yandex` template `playbooks/deploy/docker/files/deploy_microservices/deploy_microservices.j2` maps `webEx_port` to container port 80, and `web_ex.j2` executes the HTTP check through that port.
5. `src/YouDo.Mcp.Web/Program.cs` uses `WebApplication.CreateBuilder`. It does not use ServiceCore `ServiceHostBuilder`, which is the component that reads `YouDo:Core:Port` and calls `Kestrel.Listen`.
6. The shared .NET 8 runtime image explicitly set `ASPNETCORE_HTTP_PORTS=80` and `ASPNETCORE_URLS=http://*:80`; the new .NET 10 image does not. Therefore the upstream ASP.NET container default (port 8080) remains in effect, while Nomad checks container port 80.

### Root-cause hypothesis

Port mismatch: Kestrel listens on container port 8080, but Nomad forwards/checks container port 80. `YouDo__Core__Port=80` looks correct in the rendered environment but is ignored by this application's hosting path.

### Safe live verification

Run inside the web task, without dumping all environment variables:

```bash
env | grep -E '^(ASPNETCORE_(HTTP_PORTS|URLS)|YouDo__Core__Port)='
curl -sv --max-time 2 http://127.0.0.1:80/_/healthcheck
curl -sv --max-time 2 http://127.0.0.1:8080/_/healthcheck
```

Expected evidence: port 80 refuses the connection and port 8080 returns HTTP 200 with `Healthy`.

Also inspect `nomad alloc status <alloc-id>` for the service check error; `connection refused` supports the port mismatch, while HTTP 404/500 would require a different branch of investigation.

### Remediation options

- Minimal service-scoped correction: add `ASPNETCORE_URLS = "http://+:80"` (or `ASPNETCORE_HTTP_PORTS = 80`) to both test `webEx_env` and production Nomad environment.
- Code-level correction: explicitly configure Kestrel from `YouDo:Core:Port` in the minimal-hosting setup, or migrate to ServiceCore `ServiceHostBuilder` if compatible with the endpoint setup.
- Platform correction: restore the port-80 environment defaults in the shared `aspnet:10.0` base image. This has the widest blast radius and requires checking all .NET 10 consumers.

Preferred immediate scope is the service configuration; afterwards decide whether the shared base image should retain the .NET 8 compatibility contract.

## Open items

Remaining checks / risks:

- Confirm the live listener with the two loopback curls before changing configuration.
- Apply the same correction to production before the first production deployment; its Nomad job also maps `web_port` to container port 80 and only sets `YouDo__Core__Port=80`.
- The unencrypted Data Protection key-at-rest warning is a separate security-hardening item, not the health-check incident.

## Portable lesson

[`~/ai/general/knowledge/dotnet/aspnet-container-default-port-8080-healthcheck.md`](../../../../general/knowledge/dotnet/aspnet-container-default-port-8080-healthcheck.md)
