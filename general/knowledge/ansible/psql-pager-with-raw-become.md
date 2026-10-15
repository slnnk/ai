---
system: ansible
status: verified
checked: 2026-10-15
tags: [ansible, postgresql, ssh]
---
# Disable psql pager for Ansible raw tasks with become

## Summary

Noninteractive PostgreSQL automation can wait indefinitely after changing an Ansible task from shell/command to raw with become. SSH may allocate a TTY, allowing psql to launch its interactive pager. Add -P pager=off to each psql invocation.

## Symptom

Ansible remains at a database task while the database has no active statement. Remote process ancestry shows sshd, sudo, psql and pager; psql waits for its pager child, which waits for terminal input.

## Cause and fix

The raw SSH/become execution path can expose a terminal to psql. A result larger than one screen triggers the pager. Keep existing SQL and execution identity, and add the command-line setting:

```yaml
raw: psql -P pager=off -U postgres -c "SELECT 1"
become: true
become_user: postgres
```

Apply it to every invocation, including multiple commands in a shell pipeline. This changes client output behavior rather than database state.

## Verification and limits

Inspect process names and database wait states without dumping SQL or credentials. Run a read-only result larger than one screen under the same SSH TTY path with the flag and confirm a bounded successful exit. In the observed regression, a 200-row SELECT completed in about one second. A local non-TTY check alone can miss this failure. Do not infer pager involvement when active SQL is waiting on locks or I/O; diagnose those independently. Cancelling CI may require separate approval and does not replace fixing the command.
