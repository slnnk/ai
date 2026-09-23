---
system: ansible
status: verified
checked: 2026-08-13
tags: [get_url, uri, ansible-core, python, pip, user-install]
---
# get_url/uri fail with "CustomHTTPSConnection object has no attribute cert_file"

## Symptom

Any module that uses `ansible.module_utils.urls` (`get_url`, `uri`, `apt_key`
with a URL) fails on the target with:

```text
'CustomHTTPSConnection' object has no attribute 'cert_file'
```

while `curl` to the same URL works. Upgrading within the same ansible-core
major/minor line (2.13.2 -> 2.13.13) does not help.

## Cause

Old `ansible-core` (2.13 and earlier) subclasses `http.client.HTTPSConnection`
and reads `self.cert_file`/`self.key_file`, attributes that newer Python
`ssl`/`http.client` builds no longer set. The interpreter that matters is the
one executing the module, which for `connection: local` or `delegate_to:
localhost` tasks is the controller's own Python. The mismatch typically appears
on controllers with a pip `--user` Ansible install on a system Python (3.8)
that received a security backport.

## Fix

Install a current ansible-core on a newer interpreter without touching the
distribution's `/usr/bin/python3`:

```bash
/usr/bin/python3.9 -m pip install --user --upgrade 'ansible==8.7.0' 'ansible-core==2.15.13'
ansible-playbook --version   # must show core 2.15.x, python 3.9, ~/.local/lib/python3.9/site-packages
head -1 ~/.local/bin/ansible-playbook   # shebang must be the new interpreter
```

Then re-run the failing play. If `~/.ansible/tmp` is read-only (sandboxes),
set `ANSIBLE_LOCAL_TEMP=/tmp/ansible-local` for the run.

## Limits

- Distribution apt packages of Ansible may still be installed in parallel;
  `PATH` order decides which `ansible-playbook` runs, so always check
  `--version`.
- ansible-core 2.15 requires Python >= 3.9 on the controller; targets may keep
  older interpreters.
- Exact cause is inferred from the fix (verified) rather than from a traceback
  bisect (hypothesis).
