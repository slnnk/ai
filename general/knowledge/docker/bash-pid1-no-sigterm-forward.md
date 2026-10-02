---
system: docker
status: verified
checked: 2026-10-01
tags: [docker, nomad, signals, graceful-shutdown]
---
# Bash entrypoint as PID 1 does not forward SIGTERM

## Summary
A container whose ENTRYPOINT is a bash script that starts the app as a child (no `exec`, no
trap) never delivers SIGTERM to the app. Every `docker stop` / Nomad stop ends in SIGKILL after
the kill timeout (exit 137). Raising the kill timeout only makes stops slower.

## Symptom
- Stop always takes exactly the kill timeout; exit code 137; no graceful-shutdown log lines.
- The app's own shutdown timeouts (e.g. .NET `HostOptions.ShutdownTimeout`) have no effect.
- Crash traces show the app as a child of the script, e.g. `./entrypoint.sh: line N: 7 Aborted dotnet ...`.
- Side effects of hard kills: leftover DB-based locks, jobs stuck "fetched"/invisible until a timeout.

## Cause
PID 1 in a PID namespace ignores signals for which it has no handler. Bash running a script
installs no SIGTERM handler and does not forward signals to a foreground child it waits on.

Reproduce:
```bash
printf '#!/usr/local/bin/bash\nsh -c "trap \\"echo got TERM; exit 0\\" TERM; while :; do sleep 0.2; done"\n' > ep.sh; chmod +x ep.sh
docker run -d --name t --entrypoint /ep.sh -v $PWD/ep.sh:/ep.sh bash:5
docker stop -t 5 t; docker inspect -f '{{.State.ExitCode}}' t   # 137 after 5 s, no "got TERM"
```

## Fix
- Preferred: `exec app args` as the last command of the script (the app becomes PID 1).
- If the script must run something after the app exits (e.g. `sleep`), forward explicitly:
  ```bash
  app args & pid=$!
  trap 'kill -TERM "$pid" 2>/dev/null' TERM INT
  rc=0
  while kill -0 "$pid" 2>/dev/null; do wait "$pid"; rc=$?; done   # wait returns early on a trapped signal
  ```
- Forward SIGINT as SIGTERM: a non-interactive shell starts background jobs with SIGINT ignored,
  so `kill -INT` to the child does nothing (verified).
- Then align timeouts: app shutdown timeout < orchestrator kill timeout.

## Limits
- `docker run --init` / Nomad `init = true` (tini) forwards to its direct child only; if that
  child is the bash script the problem remains unless tini kills the process group (`-g`).
- Shell form `ENTRYPOINT cmd` (`/bin/sh -c`) has the same problem.
