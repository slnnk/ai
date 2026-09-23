---
system: gitlab-ci
status: verified
checked: 2026-09-03
tags: [runner, concurrent, performance, junit, contention, docker-executor]
---
# A CI job doubled in duration: separate runner contention from real growth

## Symptom

A test job that used to take ~7 minutes now takes ~12. The suite did grow, so the slowdown
is blamed on "more tests". Reruns sometimes finish fast, sometimes slow.

## Cause

On a Docker-executor runner with `concurrent > 1`, several heavyweight jobs (build + tests +
database containers) share the host's CPU, disk and memory. Contention shows up as a
**uniform slowdown of everything**: checkout, package restore, compile, unit tests and
integration tests all get slower by a similar factor, including test cases whose code did not
change. Real workload growth, by contrast, adds time only where cases were added.

## Fix

Diagnose with three artifacts of the runner and the JUnit reports; no access to the runner
host is needed.

1. Pick three jobs: an old fast one, the slow one, and a **control** job of the same size that
   ran alone on the same runner near the same time.
2. From the job traces, compare per-phase timings (checkout, restore, build, unit, integration).
   A slowdown in checkout and restore already points at the host, not the tests.
3. List what else the runner executed during the slow job:

   ```bash
   curl -s --header "PRIVATE-TOKEN: $TOKEN" \
     "$CI_API_V4_URL/runners/<runner_id>/jobs?status=success&per_page=100" \
     | jq -r '.[] | "\(.started_at) \(.finished_at) \(.id) \(.name) \(.project.path_with_namespace)"'
   ```

   Overlapping intervals with the slow job = concurrent load. The executor name in the trace
   (`...concurrent-N`) also tells how many slots were in use.
4. Compare the JUnit reports of the control and the slow job on the **intersection of
   identical test-case names**. If the cumulative time of unchanged cases grows 2-3x, the
   environment is the cause; if only new cases are slow, the suite is.

   ```bash
   # sum of <testcase time> per name, then join on name
   python3 - <<'PY'
   import sys, xml.etree.ElementTree as ET
   def load(p):
       return {f"{c.get('classname')}.{c.get('name')}": float(c.get('time') or 0)
               for c in ET.parse(p).iter('testcase')}
   a, b = load(sys.argv[1]), load(sys.argv[2])
   common = a.keys() & b.keys()
   print(len(common), sum(a[k] for k in common), sum(b[k] for k in common))
   PY
   ```

Remedies, in order of preference:

- lower `concurrent`/`limit` for the heavy job's runner, or give heavy jobs a dedicated tag
  and runner with known CPU/RAM;
- if concurrency must stay, cap in-process test parallelism (for xUnit
  `maxParallelThreads`) and measure; it reduces thrashing but can raise isolated wall time;
- wrap each phase in `section_start`/`section_end` markers and keep JUnit artifacts so the
  next regression is attributable in minutes.

## Limits

- A cache miss (for example a NuGet cache) that is present in both old and new jobs is not the
  regression; compare cache hit/miss lines before blaming it.
- The method needs JUnit (or similar per-case timing) reports from both jobs; without them,
  only phase-level comparison is possible.
