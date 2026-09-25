---
system: yandex-cloud
status: verified
checked: 2026-09-23
tags: [yandex-tf, ansible, vault, gitlab-ci]
---
# yandex-tf: stop running Ansible from Terraform in network

## Task

YouTrack `DevOps-866` ("yandex-tf - запуск Terrafrom"): Ansible run by the Terraform `ansible` provider in `network/` gets no Vault credentials (`automation-services` playbooks now fetch secrets in `pre_tasks` via `playbooks/vault_fetch_tasks.yml`), so `/etc/ipsec.secrets` on `ipsec` is rendered empty. Decision: Terraform no longer runs playbooks, and there is no CI Ansible job for network either. A CI job `ansible:network` modelled on `ansible:test-infra` was drafted and then dropped at the user's request. Playbooks are run manually from `automation-services/inventories/yandex` (see its README).

## Context

- Repository `/home/slnnk/git/yandex-tf`, MR `!229` (branch `DevOps-866-disable-ansible`, commit `15194537`), merged to `master` as `09d88c45`.

## Actions

- `network/ansible-gateway.tf`, `network/ansible-balancer-test.tf`: removed `time_sleep.*`, all six `ansible_playbook` resources and the `ansible_stdout*`/`ansible_stderr*` outputs. `ansible_host` resources are kept: they are the inventory read by `cloud.terraform.terraform_provider` in `automation-services/inventories/yandex`.
- `.gitlab-ci.yml` `plan:network`: removed the stale `terraform apply --target=ansible_playbook.playbook_check_mode` (target never existed).
- `network/main.tf`: removed the `time` provider from `required_providers`; it only served the Ansible `time_sleep` resources.
- A broader cleanup of unrelated dead code (commented blocks, `.tf.off` files, unused `subnets` tfvar) was drafted and reverted at the user's request. Keep changes scoped to the task.

## Verification

- `terraform validate` succeeds.
- Read-only `terraform plan -lock=false` against Consul state: `0 to add, 0 to change, 2 to destroy`. The two destroys are only the `time_sleep.wait_60_seconds*` state entries. The `ansible_playbook` resources were already absent from state because `replayable = true` makes them drop out on refresh. The plan also removes the old stdout outputs. (Plan was run before the unrelated cleanup was reverted; the reverted part consisted only of comments, `.tf.off` files and the undeclared `subnets` tfvar, so the resource actions are unchanged.)
- `terraform init` works without `time` in `required_providers`: Terraform installs providers required by state automatically.

## Apply (2026-09-23)

- `apply:network` job `3170875` (pipeline `139287`, `master` `09d88c45`) succeeded: `0 added, 0 changed, 2 destroyed`. Only `time_sleep.wait_60_seconds` and `time_sleep.wait_60_seconds_balancer_test01` were destroyed, both state-only objects. The `ansible_stdout*`/`ansible_stderr*` outputs are gone. No VM, network or disk changes.

## Duplicate pipelines on MR !229

- A push to the new branch created pipeline `139285` (`source: push`, all 15 `validate:*`/`plan:*` jobs, because `rules: changes` is always true on a new branch's first push pipeline). Creating the MR 16 s later created pipeline `139286` (`merge_request_event`, only `validate:network`/`plan:network`, with `changes` compared to `master`). Cause: `.gitlab-ci.yml` has no `workflow:rules`. Pipeline `139285` was cancelled.

## Remaining risks / TODO

- [ ] `yandex-tf/.gitlab-ci.yml`: add `workflow:rules` so only MR and default-branch pipelines run (`$CI_PIPELINE_SOURCE == "merge_request_event"`, `$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH`). Trade-off: branches without an MR get no pipeline. `apply:*` rules are unaffected. Deferred by the user on 2026-09-23.
- Ansible for `ipsec`/`balancers_test` is manual now; nothing re-applies config after VM changes.
