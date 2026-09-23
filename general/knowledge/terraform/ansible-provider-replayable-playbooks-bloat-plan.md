---
system: terraform
status: verified
checked: 2026-09-17
tags: [terraform, ansible-provider, replayable, outputs, sensitive, ignore_playbook_failure, ci]
---
# Terraform ansible provider: multi-megabyte plan logs and green applies that hide failed playbooks

## Symptom

- A `terraform plan` job in CI succeeds but writes several MB / thousands of lines of trace. The
  bulk is old Ansible task output repeated in `Objects have changed outside of Terraform`,
  in the resource diff and again in `Changes to Outputs`.
- Every plan proposes to (re)create all `ansible_playbook` resources although nothing changed.
- An `apply` finishes with `Apply complete` and the CI job is green, yet one playbook actually
  failed on its first task (for example a missing required variable) and the host was never
  reconfigured.

## Cause

Provider `ansible/ansible` (`ansible_playbook` resource, checked with 1.3.0):

- `replayable = true` means "recreate and run the playbook on every apply". During refresh/plan
  the resource shows as deleted and to be recreated, so its stored computed attribute
  `ansible_playbook_stdout` (the complete previous run log) is printed in the external-change
  report.
- If root `output` blocks expose `ansible_playbook_stdout`/`stderr`, Terraform prints them again in
  `Changes to Outputs` and once more at the end of every apply, including a targeted apply that
  changes nothing.
- `ignore_playbook_failure = true` turns a non-zero `ansible-playbook` exit into a successful
  resource creation. Terraform, and therefore CI, report success.

A stale `terraform apply -target=ansible_playbook.<name-that-no-longer-exists>` step in CI does not
error out; it applies nothing, prints the targeting warnings and dumps all root outputs again.

## Fix

1. Stop exporting raw playbook logs as plain outputs. Either delete the outputs or mark them
   sensitive so the CLI does not render them:

   ```hcl
   output "ansible_stdout" {
     value     = ansible_playbook.gateway.ansible_playbook_stdout
     sensitive = true
   }
   ```

2. Decide whether the playbook should run on every apply at all. If not, set
   `replayable = false` and trigger reruns through a changing input (for example
   `extra_vars = { run_id = var.run_id }`) or run Ansible from a separate CI job.
3. Remove `ignore_playbook_failure = true`, or if a failure must not block Terraform, parse the
   recap (`failed=`) in a following CI step and fail the pipeline explicitly.
4. Do not run the normal and the `check_mode` playbook for the same host in parallel from one
   apply; add `depends_on` between them.
5. Remove or fix `-target=` commands that reference resource addresses no longer in configuration.

## Limits

- `sensitive = true` hides the value only in CLI output; it is still stored in plain text in the
  state file.
- The provider does not offer a way to keep replayable playbooks out of the external-change report;
  the only complete fix is not to store large stdout in state (i.e. do not use replayable for
  long-running playbooks).
- Ansible `template` tasks do not keep backups unless `backup: true` is set, so a playbook that
  partially applied cannot be rolled back from Terraform; treat the host configuration as
  reconcile-only.
