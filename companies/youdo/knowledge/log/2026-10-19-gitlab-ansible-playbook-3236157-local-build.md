---
system: gitlab
status: verified
checked: 2026-10-19
tags: [docker, ansible, registry]
---
# Ansible 5.10.0 local image recovery for job 3236157

## Summary

Local rebuild requested for [job 3236157](https://gitlab.youdo.sg/sysadmins/ansible-playbook/-/jobs/3236157), with publication to its registry tag and no additional tests. Build and requested registry push completed successfully.

## Context and authorization

User explicitly requested local build and registry push, speed, no extra checks, and no superpowers skill. Source project363, tag `ansible_5.10.0`, commit `90176a8094ef23d25955199b27eb01c10915b31d`. CI uses the ref slug: `registry.youdo.sg/sysadmins/ansible-playbook:ansible-5-10-0`.

## Actions and changed files

- Read job metadata, failure trace, Dockerfile and CI configuration through GitLab GET requests.
- Downloaded commit archive into `/home/slnnk/ai-data/ansible-playbook-3236157/`; no repository checkout or branch changes.
- Locally replaced Alpine package installation with Ubuntu apt equivalents, retained Ansible5.10.0, Python dependencies, entrypoint and environment.
- Started `docker build --tag registry.youdo.sg/sysadmins/ansible-playbook:ansible-5-10-0 /home/slnnk/ai-data/ansible-playbook-3236157`.

## Findings and limits

CI failed at `apk: not found`: the historical Alpine recipe now inherits Ubuntu22.04 from `sysadmins/nomad:master`. The parent image is a mutable tag. Runtime and extra registry checks are intentionally omitted per user instruction. Local recipe adaptations are outside Git and are not a permanent upstream CI repair.

## Result

- Local build exit0; image ID `sha256:8453ddaab804f8aa7da8d106ef7b1f6e95efbe36767e7a66f84efce6c5e68d2f`.
- Requested `docker push registry.youdo.sg/sysadmins/ansible-playbook:ansible-5-10-0` exit0.
- Push-reported manifest digest: `sha256:a399762c28ebe8001f80a8838a869fd28385735fd4c8a50e9f7c03379a1e0dd5`.
- No runtime tests, registry reinspection, CI rerun, deployment, Git commits or upstream changes.
