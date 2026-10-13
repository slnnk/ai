---
system: nexus
status: verified
checked: 2026-10-12
tags: [nexus, docker, gitlab-ci]
---
# SORM runner image pull requires Docker credentials

## Summary

Job3219124 fails during Docker executor preparation: `no basic auth credentials` pulling `nexus.youdo.com/youdo/microservices/sorm/migrations:0.0.22`. The image exists and current GitLab group8 Nexus Docker credentials return HTTP200 on its manifest HEAD. Anonymous HEAD returns401 BASIC. No new user is needed.

## Task and context

User asked whether Nexus recovery omitted a user, then requested inspection of runner Docker configuration. Job is `step 2 - pre migrations`, tag0.0.22, project567, runner105 on172.28.0.171. No runtime modifications authorized.

## Actions and findings

Read GitLab job/trace and CI templates via GET. Nexus REST GET confirms anonymous enabled and DockerToken active, but docker group3000 and docker-hosted3003 have forceBasicAuth=true. Authenticated public `/v2/` and manifest HEAD200; anonymous401. No image downloaded.

Read-only SSH `root@172.28.0.171`: gitlab-runner process runs as root. `/etc/gitlab-runner/config.toml` contains four runners, all with DOCKER_AUTH_CONFIG containing only registry.youdo.sg, user technical. No nexus.youdo.com entry. `/root/.docker/config.json`, `/home/gitlab-runner/.docker/config.json`, `/etc/gitlab-runner/.docker/config.json` absent. Credentials decoded in memory only to print username. Thus the runner has no configured Nexus pull identity in inspected sources. Runtime job-level overrides were not exhaustively inspected.

## Changes and risks

Knowledge bookkeeping only; no repository/runtime/API mutations, CI retry or deployment. Configure runner image-pull authentication before executor starts, or separately approve anonymous Docker read policy. Passwords/tokens not recorded.

## Evidence

[Job3219124](https://gitlab.youdo.sg/youdo/microservices/sorm/-/jobs/3219124).

## Follow-up: previous operation and CI templates

User states Docker Nexus previously required authentication and these migrations worked. Historical June notes confirm anonymous /v2/401; old forceBasicAuth not recorded. Successful migrations3199808/3199560 on same runner105 October2 found, but recovered GitLab trace GET200 bodies are empty; historical credential source remains unresolved. Thus current missing credentials is established, but cannot yet explain the historical change.

Live master templates: .ci-scripts.yml defines .docker-login-nexus with NEXUS_USER/NEXUS_PASS/NEXUS_ADDR; .main-vars.yml maps group Nexus variables. Local full include-chain review confirms .dotnet-build.yml invokes login during build scripts. .deploy-prod-migrations only declares service image, always pull, and DB connection setup; no login/image-pull auth. .main.yml set-variables dotenv contains only three image-name/tag fields. Complete paginated project567/group158/group8 variable GET (0/3/52 variables) finds no DOCKER_AUTH_CONFIG. Templates contain no such variable either. These checks supersede the earlier incomplete first-page collection check. No mutations.

## Approved runner credential change

User explicitly requested adding Nexus to DOCKER_AUTH_CONFIG on171 and172. Applied only /etc/gitlab-runner/config.toml on172.28.0.171 (four runner entries) and172.28.0.172 (three). Added nexus.youdo.com auth for gitlab using existing group8 NEXUS_DOCKER_USER/PASSWORD fetched in memory. Existing registry.youdo.sg technical identity and all other fields preserved; atomic replacement retained ownership and mode0600. Helper ~/ai-data/nexus-recovery/add_runner_nexus_auth.py defaults to preflight, --apply mutates only approved hosts; no secret values embedded or printed.

Checks: authenticated public /v2/200 before application; read-back exact match; second preflight changed=false on both hosts. Both gitlab-runner systemd services active; each journal contains one Configuration loaded event within five minutes and zero configuration parse error markers. No restart, docker pull or CI retry executed. Runtime-only change is not persisted in Ansible repository; later configuration management may overwrite it. Local repository untouched.

## User-reported CI verification

User retried the failed job and reported success after the runner DOCKER_AUTH_CONFIG change. This confirms recovery from the original image-pull failure according to the user; retry job ID was not provided and no independent API verification was performed.

## Nomad host inspection requested by user

User reported analogous service image pull failure for nexus.youdo.com/youdo/microservices/sorm/service:0.0.22 and requested Docker configuration on172.24.0.12. Read-only SSH identifies msk3-nomad02.youdo.corp. /etc/nomad.d/client.hcl Docker plugin auth.config points to /root/.docker/config.json. That JSON contains only registry.youdo.sg, username nomad, with credential present; no credsStore or credHelpers and no Nexus entry. No configuration changes or Nomad job operations executed. This establishes absence of Nexus credentials in the configured driver auth file; task-level job auth was not inspected.

## Historical docker identity search

User suspects an old Nexus user named docker. Bounded KB/recovery/local repository searches, including hidden files and history of the Nomad auth template, found no confirmation; this does not establish that the user never existed. nx-docker/ci-docker are role names associated with gitlab. Current/deprecated runner stored registry auth identities are technical; Nomad inventory identity is nomad. Complete paginated GET of group8 (youdo) checks52 CI variables: NEXUS_DOCKER_USER=gitlab, NEXUS_DOCKER_PASSWORD exists, NEXUS_HOST=msk3-nexus.youdo.corp and NEXUS_PUBLIC_HOST=nexus.youdo.com. No literal docker variable value or Docker auth configuration found. Passwords not printed or recorded. Historical deleted/changed GitLab variable values remain unknown; no global Git history audit performed.

## Approved dedicated Docker pull account

User explicitly requested creation of Nexus user docker, password sourced from current/.env NEXUS_DOCKER_PASSWORD. Preflight GET confirmed user absent and existing nx-docker includes hosted add/edit. Created minimal role nx-docker-read (same ID/name), with direct privileges nx-repository-view-docker-docker-browse/read and nx-repository-view-docker-docker-hosted-browse/read; no inherited roles or write privileges. Created active docker assigned only nx-docker-read. GET verified exact role privileges and user status/sole role. Authenticated public /v2/ and SORM service0.0.22 manifest HEAD both200 using the new account. No package/image downloaded. No change to existing users/roles, anonymous policy, client configs or Nomad jobs. No credential value printed or embedded in scripts.

Helper ~/ai-data/nexus-recovery/create_docker_reader.py defaults to preflight, --apply performs the approved creation; refuses existing user/conflicting role. Account metadata Docker Clients/docker@youdo.com. New account password location current/.env NEXUS_DOCKER_PASSWORD; admin authentication current/.env NEXUS_ADMIN_PASSWORD. Client configuration remains a separately authorized step.

## User correction: shared Docker role with deletion

User requested full Docker content access, then explicitly corrected the proposed separate nx-docker-full role: modify existing nx-docker and include delete. Initial nx-docker-full creation succeeded, but user assignment PUT failed400; no assignment occurred. Following correction, existing nx-docker gained docker group and docker-hosted delete privileges, preserving its prior six privileges/inheritance. User docker now assigned sole nx-docker; password unchanged. gitlab still has nx-nuget+nx-docker and inherits the new delete rights as disclosed to the user. Unused nx-docker-full deleted after checking no user or role references. GET verifies exact eight privileges, active docker/sole nx-docker and nx-docker-full404; authenticated SORM service0.0.22 manifest HEAD200. No actual image push/delete or Nomad/client changes. nx-docker-read remains unused, not assigned to docker.

Nexus user update PUT requires source as returned by GET, in addition to userId/metadata/status/roles; missing source was the explicit400 validation cause, corrected without password changes. User preference: reuse/modify nx-docker for Docker content access, including deletion, rather than introduce a separate full-access role.

## Approved Nomad client172.24.0.12 Docker auth change

User explicitly requested applying the Nexus client auth change on172.24.0.12. Preflight confirmed /etc/nomad.d/client.hcl uses /root/.docker/config.json; existing JSON contains registry.youdo.sg/nomad only and file mode0640. Added nexus.youdo.com auth for docker using current/.env NEXUS_DOCKER_PASSWORD sent over SSH stdin, with no secret output or embedded values. Atomic file replacement preserved ownership, mode0640 and all other JSON fields/registry entries.

Authenticated HEAD from the node to SORM service0.0.22 manifest returned200 before mutation and again using credentials read from the saved config afterward. Exact JSON read-back verified. Helper ~/ai-data/nexus-recovery/add_nomad_nexus_auth.py --host HOST defaults to preflight; --apply changes only the explicitly approved host. No docker pull, Docker/Nomad restart, allocation restart or Nomad job update performed. Runtime change remains to be persisted separately in configuration management; other client nodes untouched.

## Remaining requested Nomad clients applied

User explicitly requested the same change on172.24.0.11 and172.24.0.13. Read-only preflight identifies msk3-nomad01.youdo.corp and msk3-nomad03.youdo.corp; both Docker drivers reference /root/.docker/config.json, initially registry.youdo.sg/nomad only, mode0640. Executed add_nomad_nexus_auth.py --host HOST --apply sequentially for each requested host. Added nexus.youdo.com/docker using current/.env NEXUS_DOCKER_PASSWORD; preserved ownership, mode0640, existing registry entry and all other settings. Both node-side precheck and saved-credential SORM service0.0.22 manifest HEAD return200, JSON read-back exact. All three explicitly requested clients11/12/13 now configured. No service/job/allocation restart, image pull or Ansible repository edit.
