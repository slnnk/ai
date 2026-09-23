---
system: dotnet
status: verified
checked: 2026-06-25
tags: [nuget, NU1605, package-downgrade, approximate-version, private-feed, dotnet-pack, nexus]
---
# Sudden NU1605 "package downgrade" without any code change

## Symptom

`dotnet restore` in CI starts failing with

```text
error NU1605: Detected package downgrade: FluentMigrator.Runner.Postgres from 6.2.0 to 3.2.1
```

although no `PackageReference` changed. The restore log also shows a line like
`... 1.7.0 was not found; approximate best match 1.9.0 was resolved`.

## Cause

An internal package version referenced by the project disappeared from the feed (an old
private NuGet server was decommissioned, or the package was pruned). NuGet does not fail on the
missing exact version: `PackageReference` versions are **minimums** (`>= 1.7.0`), so it picks
the lowest available version that satisfies the range, here `1.9.0`. That newer transitive
package pulls a newer dependency line (`FluentMigrator.Runner 6.2.0`), which conflicts with the
direct, lower, pinned reference `3.2.1`. Downgrade warnings are errors by default (NU1605).

## Fix

Choose one:

1. Move the direct reference up to the version the transitive graph now requires and validate
   runtime behaviour (here: upgrade `FluentMigrator.Runner.Postgres` to `6.2.0`).
2. Restore the missing version on the feed. Rebuild it from the tagged source and push:

   ```bash
   git archive 1.7.0 | tar -x -C /tmp/build
   cp NuGet.Config /tmp/build/           # if the tag predates the feed config
   docker run --rm -v /tmp/build:/src -w /src mcr.microsoft.com/dotnet/sdk:8.0 \
     dotnet pack Solution.sln -c Release -o ./artifacts /p:PackageVersion=1.7.0
   dotnet nuget push artifacts/*.1.7.0.nupkg --source <private-feed-url> --api-key "$NUGET_API_KEY"
   ```

   Pass the version explicitly: `Directory.Build.props` that derive it from a CI variable
   produce a wrong version when packed outside CI. Record the SHA-256 of the published
   `.nupkg` files.
3. Pin exact versions with `[1.7.0]` syntax so a missing version fails loudly instead of
   floating.

Verify with a clean restore in a container using only the repository's `NuGet.Config`:

```bash
docker run --rm --network host -v "$PWD":/src -w /src mcr.microsoft.com/dotnet/sdk:8.0 \
  dotnet restore Solution.sln --configfile NuGet.Config
```

## Limits

- Rebuilt historical packages carry their old vulnerable dependencies (NuGet warns); that is
  expected for a bit-for-bit replacement, not something to fix in the rebuild.
- `--network host` was needed because default Docker DNS could not resolve the internal feed;
  not a NuGet issue.
- `NETSDK1138` (out-of-support target framework) warnings are unrelated to NU1605.
