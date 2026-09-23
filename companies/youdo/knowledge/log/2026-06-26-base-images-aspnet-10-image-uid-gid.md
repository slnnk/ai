---
system: base-images
status: verified
checked: 2026-06-26
tags: [base-images, aspnet-10, uid, gid, groupadd, useradd, gitlab-ci-templates, dotnet.Dockerfile]
---
# registry.youdo.sg aspnet:10.0 UID/GID check

Date: 2026-06-26
Project/repository: `/home/slnnk/git/youdo.dengage`
Image: `registry.youdo.sg/youdo/base-images/microsoft/aspnet:10.0`
Digest observed: `sha256:0b85a1f04398b7c2f1d8311e7b7fed73addd910330b090e2c1d8e05e3f6b5544`

## Context

Build failed on a Dockerfile step similar to:

```sh
groupadd -g 1000 nonroot && useradd -u 1000 -g 1000 -r -m nonroot
```

Error:

```text
groupadd: GID '1000' already exists
```

## Findings

Inside the image, UID/GID `1000` are already occupied by the `ubuntu` user and group:

```text
ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
ubuntu:x:1000:
```

The image also already contains the .NET non-root application user/group:

```text
app:x:1654:1654::/home/app:/bin/sh
app:x:1654:
```

Image env includes:

```text
APP_UID=1654
ASPNETCORE_HTTP_PORTS=8080
DOTNET_RUNNING_IN_CONTAINER=true
DOTNET_VERSION=10.0.9
ASPNET_VERSION=10.0.9
```

### Conclusion

Creating a new `nonroot` group/user with UID/GID `1000` is not valid for this image. Prefer using the existing `app` user (`USER app` or `USER $APP_UID`) or choose an unused UID/GID. If UID/GID `1000` is mandatory, use the existing `ubuntu` identity instead of creating another user/group with the same IDs.

### Related local context

Search in the repository only found a similar Alpine-style user creation in `devops/migrations.Dockerfile`; the reported failing command uses Debian/Ubuntu `groupadd/useradd` and was not found verbatim in this repo at the time of check.

### Template compatibility proposal

For `/home/slnnk/git/gitlab-ci-templates/v3/files/dotnet.Dockerfile`, the least invasive compatible approach is:

- keep default `USERNAME=nonroot`, `USER_UID=1000`, `USER_GID=1000` for old images;
- create group/user only when the numeric GID/UID are not already present;
- use numeric ownership and runtime user (`1000:1000`) in `chown`, `COPY --chown`, and `USER`.

This was checked on:

- `registry.youdo.sg/youdo/base-images/microsoft/aspnet:6.0`: UID/GID 1000 absent, `nonroot` is created;
- `registry.youdo.sg/youdo/base-images/microsoft/aspnet:10.0`: UID/GID 1000 already belong to `ubuntu`, creation is skipped and numeric ownership still works.

Avoid `groupadd ... || true`: it does not handle `useradd` conflicts and leaves `COPY --chown=nonroot:nonroot` / `USER nonroot:nonroot` broken when the name does not exist.

## Changes

Applied template change: updated `/home/slnnk/git/gitlab-ci-templates/v3/files/dotnet.Dockerfile` so the user creation step falls back from `USER_UID=1000` / `USER_GID=1000` to `1001:1001` when UID `1000` already exists in the base image.

Validated shell fragment behavior:

- `aspnet:6.0`: creates `nonroot:x:1000:1000`;
- `aspnet:10.0`: detects existing UID `1000` (`ubuntu`) and creates `nonroot:x:1001:1001`.

## Portable lesson

[`~/ai/general/knowledge/docker/groupadd-gid-already-exists-in-base-image.md`](../../../../general/knowledge/docker/groupadd-gid-already-exists-in-base-image.md)
