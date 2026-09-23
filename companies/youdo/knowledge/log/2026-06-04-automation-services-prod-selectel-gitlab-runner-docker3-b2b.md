---
system: automation-services
status: verified
checked: 2026-06-04
tags: [gitlab-runner, prod_selectel, inventory, host_vars, s3-cache, b2b, docker-clean]
---
# prod_selectel gitlab-runner docker3 b2b config

## Task

Add b2b GitLab Runner configuration for gitlab-runner-docker3 in prod_selectel inventory.

## Context

- Project: automation-services
- Repository: /home/slnnk/git/automation-services
- Area: prod_selectel gitlab runner inventory
- Date: 2026-06-04

## Actions and changes

- Updated file: inventories/prod_selectel/host_vars/gitlab-runner-docker-3.yml.
- Change: added/normalized b2b docker runner entry with name template `{{ ansible_hostname }} b2b ({{ ansible_host }})`, GitLab URL, docker executor, `docker:24.0.5-cli`, tag `b2b`, S3 cache settings, docker socket/cache volumes, and dind-related settings.
- Validation: YAML parsed successfully with Ruby YAML.load_file.
- Validation: ansible-inventory with static `inventories/prod_selectel/hosts` works when `ANSIBLE_LOCAL_TEMP` is redirected to /tmp; static hosts use `gitlab-runner-dind03.youdo.corp`, while host_vars config file is `gitlab-runner-docker-3.yml` as requested/existing convention.
- Security: secrets/tokens were not recorded here; refer to the repository inventory/secret storage workflow for actual values.

Next steps:
- Apply relevant gitlab-runner playbook against the docker3 host/terraform inventory when ready.

### 2026-06-04 gitlab-runner docker clean cron

- Context: automation-services, role `roles/gitlab-runner`.
- Change: restored old docker cleanup cron schedule in `roles/gitlab-runner/templates/cron-docker-clean.j2`.
- Effective schedule: container prune hourly at minute 10, image prune hourly at minute 20, volume prune hourly at minute 30.
- Validation: checked template diff manually; no secrets recorded.

### 2026-06-04 terraform inventory ansible_host fallback

- Context: prod_selectel Terraform inventory for GitLab docker runner 03.
- Issue: gitlab-runner role failed during runner registration because runner names referenced `ansible_host`, but Terraform inventory host `gitlab-docker-runner-03` did not define it.
- Change: updated `inventories/prod_selectel/host_vars/gitlab-docker-runner-03.yml` runner display names to use `ansible_host | default(ansible_ssh_host | default(inventory_hostname))`.
- Validation: YAML parsed successfully. Local Ansible smoke test requires `/tmp` temp override due read-only `~/.ansible/tmp` in sandbox.
- Security: no secrets recorded.

### 2026-06-04 terraform inventory host_vars for docker runners 01/02

- Context: prod_selectel Terraform inventory for GitLab docker runners 01 and 02.
- Change: renamed host_vars files to match Terraform inventory hostnames: `gitlab-docker-runner-01.yml` and `gitlab-docker-runner-02.yml`.
- Change: updated runner display names in 01/02 to use `ansible_host | default(ansible_ssh_host | default(inventory_hostname))`, matching docker runner 03 behavior.
- Validation: YAML parsed successfully for 01/02/03 host_vars. Terraform inventory was not queried with real Consul token in this note to avoid recording/exposing secrets.
- Security: no secrets recorded.

### 2026-06-04 b2b runner config for docker runners 01/02

- Context: prod_selectel GitLab docker runners 01 and 02.
- Change: normalized b2b runner blocks in `inventories/prod_selectel/host_vars/gitlab-docker-runner-01.yml` and `gitlab-docker-runner-02.yml` to match docker runner 03.
- Details: replaced test runner name with templated b2b name using ansible_host/ansible_ssh_host/inventory_hostname fallback, removed explicit registration token field, added `b2b` tag and `HEALTHCHECK_TCP_PORT=2375` env var.
- Validation: YAML parsed successfully for docker runner 01/02/03 host_vars.
- Security: no secrets recorded.

## Findings

### 2026-06-04 S3 cache 403 on ordinary docker runner 03

- Context: prod_selectel GitLab docker runners 01/02/03.
- Issue: ordinary docker runner 03 failed cache upload to object storage with HTTP 403 Forbidden.
- Finding: b2b runner blocks used one S3 credential set, while ordinary/autotest/integration runner blocks still used an older S3 credential set. A 403 during cache upload is consistent with missing/invalid PutObject permissions for that credential set.
- Change: unified S3 cache credentials across all runner blocks in `gitlab-docker-runner-01.yml`, `gitlab-docker-runner-02.yml`, and `gitlab-docker-runner-03.yml`.
- Validation: YAML parsed successfully; each docker runner host_vars file now has one unique cache access key across its runner blocks.
- Security: no secret values recorded.

### 2026-06-04 manual S3 cache credentials update on runner hosts

- Context: prod_selectel GitLab docker runner hosts 172.28.0.171-172.28.0.173.
- Action: manually backed up `/etc/gitlab-runner/config.toml` on each host, replaced all S3 cache AccessKey/SecretKey lines with the unified credential set from inventory, and restarted `gitlab-runner`.
- Result: replacements made on all hosts; 172.28.0.171 had 4 cache credential sections, 172.28.0.172 and 172.28.0.173 had 3 each.
- Validation: old S3 credential strings no longer present in config.toml; AccessKey/SecretKey line counts match on each host; gitlab-runner service is active on all three hosts.
- Security: no secret values recorded.

## Open items

- Apply the gitlab-runner playbook against the docker3 host/terraform inventory when ready.

## Portable lesson

none
