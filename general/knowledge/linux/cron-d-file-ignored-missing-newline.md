---
system: linux
status: verified
checked: 2026-06-03
tags: [cron, cron.d, newline, ansible, template, docker-prune]
---
# A /etc/cron.d file without a trailing newline is silently ignored

## Symptom

A scheduled job (for example the hourly `docker image prune`/`docker volume prune` on a CI runner)
never runs, disk usage grows, but the cron file is present, readable and looks correct. Nothing in
the job's own logs, because it never starts. `journalctl -u cron` / syslog contains:

```
cron[...]: (*system*dockerclean) ERROR (Missing newline before EOF, this crontab file will be ignored)
```

## Cause

Vixie/ISC cron requires every crontab, including files in `/etc/cron.d/`, to end with a newline
character. A file whose last line has no `\n` is rejected as a whole; cron logs one error at load
time and then stays quiet. Files generated from templates are the usual culprit: the template
engine (Jinja2 in Ansible, by default `trim_blocks`/strip of the final newline in some setups) or an
editor that strips the trailing newline produces a valid-looking file that cron discards.

## Fix

1. Confirm: `tail -c1 /etc/cron.d/<file> | xxd` must show `0a`. Or `grep -c '' file` vs `wc -l`.
2. Add the newline and reload cron:

   ```bash
   printf '\n' >> /etc/cron.d/dockerclean
   systemctl restart cron
   grep -i 'cron.d\|crontab' /var/log/syslog | tail
   ```

3. Fix the generator so it cannot regress: end the Jinja2 template file with a blank line, or in
   Ansible use `template:` with `validate:` (there is no crontab validator for cron.d files, so a
   `lineinfile`/`assert` on the trailing newline, or simply a trailing newline in the template,
   is the pragmatic option). Alternatively manage the entry with the `cron` module, which writes a
   correct file.
4. Run the missed commands once by hand and check the effect (`docker system df`).

## Limits

- `docker container/image/volume prune` does not touch BuildKit build cache; add
  `docker builder prune --force --filter until=...` if build cache is the growing part.
- systemd timers do not have this requirement; the trap is specific to cron.
- Verified with Debian/Ubuntu `cron` 3.0pl1; other cron implementations (cronie) show a similar
  "premature EOF" message.
