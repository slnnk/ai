---
system: docker
status: verified
checked: 2026-10-13
tags: [docker, git, jenkins, build-context]
---
# Copied build Git metadata disables credential prompts in application images

## Symptom

A fresh application container cannot list remote Git branches with stored username/password credentials: askpass reports inability to obtain a password. Removing credential.interactive=never from a local Git config repairs the running container, but recreation brings the failure back.

## Cause

A Dockerfile using ADD/COPY of the entire context without a .dockerignore can copy build-checkout .git metadata into the runtime image. CI-generated local credential configuration then affects runtime Git commands launched from that directory. The copied config and its effect can be verified separately; do not infer the identity of the writer without evidence.

## Fix

Add .git to .dockerignore so repository metadata is excluded before context transfer. Verify the build-context archive excludes .git while retaining required payload files. Build a fresh image and inspect that it contains no copied repository metadata or unwanted credential setting. Recreate a test/application container from the verified new digest, preserving its persistent data, and repeat credentialed branch lookup without manually unsetting the key.

## Limits

A restart of an already patched container does not prove an image fix. Test context filtering without exposing Git configuration or credentials. A global/system credential setting or deliberate metadata dependency needs separate diagnosis; excluding .git addresses this copied-context cause. Keep deployment configuration aligned with the verified image so a later automation run cannot restore the defective image.
