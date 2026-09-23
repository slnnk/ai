---
system: docker
status: verified
checked: 2026-06-26
tags: [dockerfile, groupadd, useradd, uid, gid, ubuntu, nonroot, aspnet, APP_UID]
---
# `groupadd: GID '1000' already exists` after switching to a newer base image

## Symptom

A shared Dockerfile template creates a non-root user:

```sh
groupadd -g 1000 nonroot && useradd -u 1000 -g 1000 -r -m nonroot
```

It worked on the old base image and fails on the new one with
`groupadd: GID '1000' already exists`.

## Cause

Ubuntu 24.04-based images (including `mcr.microsoft.com/dotnet/aspnet:10.0` variants built on
Ubuntu) ship a default `ubuntu:x:1000:1000` user and group. Debian-based images do not, so
UID/GID 1000 was free there. .NET 8+ images additionally ship `app:x:1654:1654` and export
`APP_UID=1654` for exactly this purpose. Check with:

```bash
docker run --rm <image> sh -c 'getent passwd 1000; getent group 1000; getent passwd app; env | grep APP_UID'
```

## Fix

Pick one:

- Use the identity the image already provides: `USER app` or `USER $APP_UID` (.NET images),
  and `COPY --chown=$APP_UID:$APP_UID`.
- In a template that must work on old and new bases, create the user only when the numeric
  IDs are free and fall back to other IDs, then use **numeric** ownership everywhere so it does
  not matter which name owns the IDs:

  ```dockerfile
  ARG USERNAME=nonroot USER_UID=1000 USER_GID=1000
  RUN set -eu; \
      if getent passwd "$USER_UID" >/dev/null || getent group "$USER_GID" >/dev/null; then \
        USER_UID=1001; USER_GID=1001; fi; \
      groupadd -g "$USER_GID" "$USERNAME" && useradd -u "$USER_UID" -g "$USER_GID" -r -m "$USERNAME"; \
      echo "$USER_UID:$USER_GID" > /etc/container-user
  COPY --chown=1000:1000 . /app
  USER 1000:1000
  ```

  (adjust the numeric literals to the chosen fallback, or resolve them from
  `/etc/container-user` in a later `RUN`).

Do **not** paper over it with `groupadd ... || true`: `useradd` still fails, and later
`COPY --chown=nonroot:nonroot` / `USER nonroot` break because the name never got created.

## Limits

- Volumes and bind mounts owned by 1000:1000 on the host will belong to `ubuntu` inside the
  new image if you switch to 1001; decide on the numeric contract per environment.
- `-r` (system account) plus `-m` is a legacy combination; it works but creates a home for a
  system user.
