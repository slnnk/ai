---
system: yandex-cloud
status: verified
checked: 2026-09-23
tags: [terraform, yandex-tf, network, base-image, ansible-provider, nlb]
---
# Yandex Terraform: network

Last verified: 2026-09-17.

## Scope and access

- Repository: `/home/slnnk/git/yandex-tf`; safe origin: `git@gitlab.youdo.sg:sysadmins/yandex/yandex-tf.git`.
- Terraform root: `/home/slnnk/git/yandex-tf/network`.
- Remote state: Consul at `consul.service.selectel.consul:8500`, datacenter `selectel`, path `terraform/yandex-network`.
- The root manages shared networking plus gateway, balancer, Postfix, IPsec, and NAT MSSQL compute resources. The Yandex provider authenticates with ignored `network/key.json`; CI copies the key from GitLab Secure Files.
- CI jobs: `validate:network` runs `tflint`, `plan:network` initializes and creates a plan, and manual `apply:network` runs on `master` for changes under `network/**`.
- TODO (repo-wide): `.gitlab-ci.yml` has no `workflow:rules`, so the first push of a new branch runs every `plan:*` (including `prod`) alongside the MR pipeline. See the DevOps-866 [log](../../log/2026-09-23-yandex-cloud-yandex-tf-network-ansible-job.md).
- Since `DevOps-866` (2026-09-23, MR `!229`, applied in job `3170875`): Terraform no longer runs playbooks and there is no CI Ansible job; only `ansible_host` inventory resources remain, and playbooks are run manually from `automation-services/inventories/yandex`. The `time` provider was removed. Reason: Terraform-run Ansible had no Vault creds, so `/etc/ipsec.secrets` was rendered empty. Details: [log](../../log/2026-09-23-yandex-cloud-yandex-tf-network-ansible-job.md). Sections below about `ansible_playbook` resources describe the state before this change.

## Shared Ubuntu 22.04 base-image overwrite mitigation (2026-09-17)

- Replaced hard-coded image ID `fd8tpn447q9l6en2gqvi` with lookup by stable name `yc-base-image-ubuntu-22-04` for six active image data sources: public-test balancer, test balancer, prod gateway, NAT MSSQL, test Postfix, and `postfix-prod04` (`youdo-in`).
- All active lookups use `var.folder_id`, the default folder containing the shared image. `postfix-prod04` previously specified the net-folder ID; lookup by name failed there, so its data source was corrected to the image-owning default folder. Current image ID resolved by all six sources is `fd8ot9ko30559cfp1p0o`.
- Added `ignore_changes = [image_id, snapshot_id]` to the six corresponding standalone boot-disk resources.
- NAT MSSQL also declares its actual VM boot disk inline under `yandex_compute_instance.nat_mssql.boot_disk.initialize_params`; added a narrow instance lifecycle ignore for `boot_disk[0].initialize_params[0].image_id`. The separately declared `yandex_compute_disk.boot-nat_mssql` remains protected as well, although the VM configuration currently initializes its own disk rather than attaching that resource.
- Updated the commented image data-source example in `compute-gateway.tf` to use the stable name; its existing disk has no configured `image_id`, so no lifecycle change was needed there.
- `terraform validate` succeeds with provider `yandex-cloud/yandex` 0.136.0.
- Read-only verification command: `terraform plan -refresh=false -lock=false -detailed-exitcode -no-color -compact-warnings`. Result: `0 to add, 9 to change, 17 to destroy`; no image-driven disk or VM replacements are present.
- The 17 unrelated destroys are existing retirement drift for the old production balancer/Postfix stack and associated load balancer, target group, and external addresses. The nine in-place changes include metadata updates plus snapshot-schedule cleanup. Review this destructive scope separately before apply.
- Operational caveat: ignored `image_id` preserves existing disks/VMs when the named image is rebuilt. Re-imaging requires a separately reviewed controlled recreation or temporary removal of the ignore rule.

## Current plan breakdown (2026-09-17)

- The nine in-place changes are seven standalone VM metadata updates (`balancer-test01`, `balancer-test02`, `gate-vm`, `ipsec_vm`, `nat_mssql`, `postfix-test`, and `postfix-prod04`) plus the daily and weekly snapshot schedules. The VM drift originates from commit `b202bb5`, which changed the rendered SSH `user-data` input to `local.vm_ssh_key`. The schedule configuration excludes the old balancer-prod disks.
- The 17 destroys originate from commit `2807179`, not from the base-image fix. That commit renamed `compute-balancer-prod.tf` and `compute-postfix-prod.tf` to `.tf.off`, commented out the Postfix load balancer resources, and removed the old external-address groups from `terraform.tfvars`.
- Exact destroy set: two `yandex_compute_disk.boot_balancer_prod` disks, two `yandex_compute_instance.balancer-prod` VMs, three `yandex_compute_disk.boot_postfix` disks, three `yandex_compute_instance.postfix` VMs, `yandex_lb_network_load_balancer.youdo-postfix`, `yandex_lb_target_group.youdo-postfix`, two balancer external addresses, and three SMTP external addresses.
- The former configuration set deletion protection on the Postfix load balancer and both balancer external addresses. Even though Terraform displays destroy actions, an apply may be rejected by the API until protection is deliberately disabled. Do not apply the network plan unless retirement of this complete 17-object set is confirmed and protection/backup/traffic migration are handled.

## Excessive GitLab plan log: job 3153985 (2026-09-17)

- GitLab job `3153985` (`plan:network`, pipeline `138954`, MR `!224`, commit `9cbc7a39`) succeeded but produced about 4.2 MB / 6429 lines of trace output.
- The output size is not caused by `tf-summarize`; its tree accounts for only about 1 KB. The main source is Terraform rendering complete historical Ansible CLI logs stored in `ansible_playbook_stdout`.
- All six `ansible_playbook` resources in `ansible-gateway.tf` and `ansible-balancer-test.tf` use `replayable = true`. Provider 1.3.0 defines this as recreating/running the playbook on every apply. During refresh/plan these resources appear deleted/recreatable, and Terraform prints their old computed stdout in the external-change report.
- Root outputs `ansible_stdout` and `ansible_stdout_balancer_test01` expose the full stdout values. The first plan printed about 1.52 MB just in `Changes to Outputs`; the preceding refresh/external-change and resource-plan section printed another roughly 1.59 MB.
- The CI command `terraform apply -input=false --target=ansible_playbook.playbook_check_mode -auto-approve` targets an address that does not exist in current configuration (actual check-mode resources are `playbook_gateway_check_mode` and `playbook_balancer-test01_check_mode`). It applies nothing but Terraform still prints every root output, adding about 1.09 MB of duplicated Ansible logs.
- Likely remediation: stop exporting raw playbook stdout/stderr as ordinary root outputs, or mark those outputs sensitive to suppress CLI rendering; then decide whether replayable playbooks belong in Terraform plan/apply at all. Separately remove or correct the stale targeted apply command. These are behavior changes and were not implemented during this diagnosis.

### Actual action set in job 3153985

- The refresh-enabled GitLab plan result is `6 to add, 8 to change, 7 to destroy`. This differs from the earlier local `-refresh=false` plan because live refresh confirmed that the two old balancer-prod VMs, three old Postfix VMs, and their five boot disks are already absent from Yandex Cloud. They appear only in Terraform's `Objects have changed outside of Terraform` report, not as pending destroy actions.
- The six adds are all replayable `ansible_playbook` pseudo-resources, not VMs, disks, or network resources.
- Seven in-place VM changes affect the currently existing machines `balancer-test01`, `balancer-test02`, `ipsec-vm`, `nat-mssql`, `postfix-prod04`, `gate-vm-prod`, and `postfix-test`; each is the previously documented SSH `metadata.user-data` change. The plan does not replace or destroy these VMs.
- The eighth in-place change is `yandex_vpc_route_table.selectel_prod`. Although the set-style diff redraws most routes, the net change is removal of live route `192.168.30.0/24 -> 10.16.20.3`, which is absent from current `network/vpc.tf`. Treat this as potentially impactful unmanaged drift and confirm its owner/purpose before apply.
- The seven pending destroys are only the old Postfix network load balancer, its target group, two `balancer-prod-*` external addresses, and three `smtp-ip-a1/a2/a3` external addresses. No currently visible VM from the 2026-09-17 console screenshot is in the destroy set.
- Console screenshot verification on 2026-09-17: the seven remaining VMs listed above exist; all shown are running except `nat-mssql`, which is stopped.
- After the user confirmed that route `192.168.30.0/24 -> 10.16.20.3` is required, it was added explicitly to `yandex_vpc_route_table.selectel_prod` in `network/vpc.tf`. `terraform validate` succeeds. A refresh-enabled read-only plan now reports `6 to add, 7 to change, 7 to destroy`, and JSON inspection confirms zero pending changes for the route table; the previous eighth in-place change is eliminated.

## Master plan verification: job 3154029 (2026-09-17)

- GitLab pipeline `138961`, job `3154029` (`plan:network`), merge commit `7e712f93`, succeeded with `6 to add, 7 to change, 7 to destroy`.
- The required route `192.168.30.0/24 -> 10.16.20.3` produces no pending route-table action after refresh, confirming that live infrastructure/state already matches the committed configuration.
- The six additions are replayable Ansible pseudo-resources: gateway and balancer normal/check-mode playbooks plus two authorized-keys playbooks. A full apply can execute these playbooks; they are not cloud infrastructure additions.
- The seven updates are the known in-place VM metadata changes for `balancer-test01`, `balancer-test02`, `gate-vm`, `ipsec_vm`, `nat_mssql`, `postfix-prod04`, and `postfix-test`. `postfix-prod04` also removes metadata key `serial-port-enable = 1`. There are no VM or disk replacements.
- The seven destroys remain: internal NLB `youdo-mta-balancer`, target group `youdo-mta`, balancer IPs `51.250.78.57` and `51.250.89.128`, and direct-SMTP IPs `37.230.174.141`, `37.230.174.4`, and `37.230.174.198`. Refresh reported all five IPs as unused, but the NLB and two balancer IPs have deletion protection. Concurrent apply may still delete unprotected resources before failing on protected ones, so protection is not a safe guard against a partial apply.
- The CI job's final targeted command still references nonexistent `ansible_playbook.playbook_check_mode`; it applied nothing and printed the standard target/incomplete-apply warnings. `network/terraform.tfvars` also retains the non-fatal undeclared `subnets` warning.
- Operational decision remains: do not start `apply:network` until retirement of the NLB, target group, and all five public IPs is explicitly confirmed and deletion protection is handled deliberately.

## Failed apply:network job 3154707 (2026-09-17)

- Pipeline `138961`, job `3154707`, merge commit `7e712f93`, failed when Terraform attempted to destroy protected NLB `youdo-mta-balancer` (`enp6sft3t08f0q8j5lc7`). Yandex Cloud returned `FailedPrecondition: Resource is protected from deletion` and explicitly required changing `deletion_protection` first.
- Before the failure, in-place metadata updates completed successfully for `yandex_compute_instance.nat_mssql` and `yandex_compute_instance.postfix-test`. No destroy operation completed and no Ansible pseudo-resource creation started according to the trace.
- A fresh refresh-enabled read-only plan after the failure (`-lock=false`) reports `6 to add, 5 to change, 7 to destroy`, confirming the two VM updates were persisted while all seven intended destroys remain pending.
- A direct retry without preparation will fail on the same NLB. If retirement is intended, disable deletion protection first on all three protected pending resources: NLB `youdo-mta-balancer` and external addresses `51.250.78.57` / `51.250.89.128`. Otherwise a later retry can again partially delete the unprotected target group and SMTP addresses before stopping on a protected address. If retirement is not intended, restore all seven resources to configuration instead of retrying.
- Exact YC CLI operations for an approved retirement: `yc load-balancer network-load-balancer update enp6sft3t08f0q8j5lc7 --deletion-protection=false`, `yc vpc address update e9bfmqa9uimru8fdts5e --deletion-protection=false`, and `yc vpc address update e9bmd9jaie9jb7gn7i8p --deletion-protection=false`. Verify each object reports `deletion_protection: false` before rerunning Terraform. These updates do not delete resources by themselves; the subsequent Terraform apply will attempt all seven pending destroys.
- Before retry, direct read-only YC API checks confirmed the NLB and both protected addresses now omit `deletion_protection` in JSON (proto default `false`), so protection is disabled on all three live objects. A simultaneous refresh-enabled Terraform plan still shows the old `true` values in the destroy-side state representation, but its action set is unchanged at `6 add, 5 change, 7 destroy`; the direct cloud reads are authoritative for the deletion guard.

## Ansible output clarification: plan job 3154716 (2026-09-17)

- Job `3154716` is a successful `plan:network`, not an Ansible/apply execution. Its final command targeted nonexistent `ansible_playbook.playbook_check_mode`, returned `No changes`, and did not run any playbook.
- The large `changed` sections are historical `ansible_playbook_stdout` values stored in Terraform state and exposed by root outputs. They are not changes made by job `3154716`; embedded timestamps and recaps correspond to earlier runs.
- Historical gateway (`ipsec`) recap: `ok=20 changed=8`; changes included StrongSwan repository/GRE configuration and restart/netplan handler, starting/enabling `restore-iptables`, updating two BIND config files, and restarting BIND.
- Historical balancer recap: `ok=29 changed=6`; changes included nginx systemd override, main/vhost configuration, nginx reload/restart, and systemd daemon re-exec.
- The plan still proposes creating/running six replayable resources on the next full apply: normal and check-mode gateway playbooks, gateway authorized-keys, normal and check-mode balancer playbooks, and balancer authorized-keys. This comes from `replayable = true`; it is separate from the historical stdout printed during plan.

## Successful apply with masked Ansible failure: job 3154717 (2026-09-17)

- `apply:network` job `3154717` completed with Terraform summary `6 added, 5 changed, 7 destroyed` and GitLab status `success`.
- All approved retirement resources were destroyed: NLB `youdo-mta-balancer`, target group `youdo-mta`, balancer addresses `51.250.78.57` / `51.250.89.128`, and SMTP addresses `37.230.174.141` / `37.230.174.4` / `37.230.174.198`.
- Metadata updates completed for the five remaining pending VMs: `balancer-test01`, `balancer-test02`, `ipsec_vm`, `gate-vm`, and `postfix-prod04`. Together with job `3154707`, all seven planned standalone VM metadata updates are now applied.
- All six replayable Ansible resources were marked created. Gateway normal/check runs overlapped. The normal gateway result succeeded (`ok=26 changed=8 failed=0`) and updated the StrongSwan repository cache, `/etc/ipsec.secrets`, GRE/netplan configuration, RPZ zone file, then ran `ipsec restart`, `ipsec secrets`, `netplan apply`, and restarted BIND. `netplan apply` emitted the non-fatal warning that `ovsdb-server.service` was not running.
- The normal balancer playbook actually failed at the start of `base_linux`: required variable `base_linux_login_user_password` was absent (`ok=1 changed=0 failed=1`). Terraform and GitLab still reported success because the resource sets `ignore_playbook_failure = true`. Therefore nginx/balancer configuration was not reconciled in this run. The check-mode playbook and both authorized-keys resources were marked complete, but their detailed results are not exposed as root outputs.
- Follow-up: supply `base_linux_login_user_password` through the approved Vault/inventory path (record only the variable/source, never its value), then rerun the balancer playbook deliberately. Remove `ignore_playbook_failure = true` or otherwise propagate Ansible failure to CI; also avoid parallel normal/check-mode execution for the same host.
- Gateway rollback assessment: the persistent files changed by the successful normal run were `/etc/ipsec.secrets`, `/etc/netplan/00-gre-gre_kz.yaml`, and `/etc/bind/db.rpz.local`; handlers reloaded IPsec secrets, ran `netplan apply`, and restarted IPsec/BIND. The Ansible template tasks do not enable `backup`, so there is no automatic pre-run copy from this job. The identifiable `gre_kz` delta is automation-services commit `98911e7a`, which adds main-table link route `10.128.0.200/32` for the KZ AWG panel. RPZ changes correspond to later inventory/template state and may include multiple August 2026 commits; `/etc/ipsec.secrets` must be restored only from the approved secret/inventory source, never copied into notes. An exact rollback therefore requires choosing a known automation-services baseline or recovering host/snapshot backups; do not blindly restore all three files from unrelated historical content.

## Related recipes

- [Rebuilt cloud image with the same name makes Terraform plan mass disk and VM replacements](../../../../../general/knowledge/terraform/image-rebuild-forces-disk-replacement.md)
- [Terraform ansible provider: multi-megabyte plan logs and green applies that hide failed playbooks](../../../../../general/knowledge/terraform/ansible-provider-replayable-playbooks-bloat-plan.md)
