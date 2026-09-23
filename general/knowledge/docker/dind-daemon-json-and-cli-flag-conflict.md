---
system: docker
status: verified
checked: 2026-06-03
tags: [docker, dind, daemon.json, insecure-registry, gitlab-runner, healthcheck]
---
# docker:dind service never comes up when daemon.json and dockerd flags set the same option

## Symptom

In a GitLab CI job using the `docker:dind` service:

- the service healthcheck prints `FATAL: No HOST or PORT found` (or the job waits for the service
  and times out), even with `HEALTHCHECK_TCP_PORT=2375` set;
- the build cannot reach `tcp://docker:2375`, `after_script` fails with
  "Cannot connect to the Docker daemon";
- running the same image by hand shows `dockerd` exiting immediately with an error like
  `unable to configure the Docker daemon with file /etc/docker/daemon.json: the following directives are specified both as a flag and in the configuration file: insecure-registries`.

## Cause

`dockerd` refuses to start when an option is provided both in `/etc/docker/daemon.json` and on the
command line. The runner mounted a host `daemon.json` into the service container
(`/data/daemon.json:/etc/docker/daemon.json:ro`) that already lists `insecure-registries`, and the
runner's `[runners.docker]` section (or the job's `services:` entry) additionally passed
`command: ["--insecure-registry=..."]`. Both were added at different times as "belt and braces";
together they are fatal. The healthcheck message is misleading: the daemon never listened, so the
port probe has nothing to report.

## Fix

Keep a single source of truth. Either:

- mount `daemon.json` and remove every `--insecure-registry`, `--dns`, `--storage-driver` ... flag
  from `command` (runner `config.toml` and Ansible/host_vars that generate it), or
- drop the mount and pass everything as flags.

Verify by hand on the runner host:

```bash
docker run --rm --privileged -d --name dind-test \
  -v /data/daemon.json:/etc/docker/daemon.json:ro \
  -e DOCKER_TLS_CERTDIR= docker:dind
sleep 20
docker exec dind-test docker info | grep -A5 'Insecure Registries'
```

Port `2375` becomes reachable roughly 15 seconds after start when the config is consistent.

## Limits

- After editing `config.toml` by hand, run `gitlab-runner verify` and restart the service; a
  configuration management run later must not reintroduce the flags.
- A registry hostname given to `docker login` without a port defaults to `443`. If the registry
  only serves plain HTTP on `80`/`3000`, `insecure-registries` alone does not help when `443` is
  closed at the network level; fix the endpoint variable (`host:3000` or `http://host`) as well.
- Checked with Docker 28.x/29.x dind images and GitLab Runner 17.9.
