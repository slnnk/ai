---
system: dotnet
status: verified
checked: 2026-06-26
tags: [dotnet-tool, NU1202, dotnet-trace, dotnet-counters, dotnet-dump, dotnet-gcdump, dotnet-monitor, dockerfile]
---
# `dotnet tool install dotnet-trace` fails with NU1202 in an old SDK image

## Symptom

A Dockerfile that has built for years suddenly fails in the SDK stage:

```text
error NU1202: Package dotnet-trace 9.0.661903 is not compatible with net6.0 ...
```

The tool line is `dotnet tool install --tool-path /tools dotnet-trace` with no `--version`.
Later stages appear as `CANCELED` in BuildKit output; that is a consequence, not a second
error.

## Cause

Without `--version`, `dotnet tool install` resolves the **latest** package on the feed. The
diagnostics tools (`dotnet-trace`, `dotnet-counters`, `dotnet-dump`, `dotnet-gcdump`,
`dotnet-monitor`) periodically raise their minimum target framework; once the latest build
targets `net8.0`, a `sdk:6.0` build stage cannot restore it. The Dockerfile was never
reproducible; it only worked while the feed happened to be compatible.

## Fix

Find the newest version line compatible with the SDK from the flat-container index (no
auth needed):

```bash
for t in dotnet-trace dotnet-counters dotnet-dump dotnet-gcdump; do
  curl -s https://api.nuget.org/v3-flatcontainer/$t/index.json | jq -r '.versions[]' | grep '^6\.' | tail -1
done
```

Then pin through one ARG so every tool moves together:

```dockerfile
ARG DOTNET_DIAGNOSTIC_TOOLS_VERSION=6.0.351802
RUN dotnet tool install --tool-path /tools --version $DOTNET_DIAGNOSTIC_TOOLS_VERSION dotnet-trace \
 && dotnet tool install --tool-path /tools --version $DOTNET_DIAGNOSTIC_TOOLS_VERSION dotnet-counters \
 && dotnet tool install --tool-path /tools --version $DOTNET_DIAGNOSTIC_TOOLS_VERSION dotnet-dump \
 && dotnet tool install --tool-path /tools --version $DOTNET_DIAGNOSTIC_TOOLS_VERSION dotnet-gcdump
```

Alternative: install the tools with a newer SDK stage and copy them into the runtime image;
this only works if the tool's own runtime requirement is satisfied by the final image.

## Limits

- `dotnet-monitor` does not share the diagnostics version line; an exact `6.0.351802` was not
  found and NuGet installed the "approximate best match" `6.1.0` with a warning. Pin it
  separately.
- The same unpinned pattern usually exists in sibling Dockerfiles (`-focal`, `-alpine`
  variants); fix them together.
