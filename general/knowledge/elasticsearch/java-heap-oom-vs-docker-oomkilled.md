---
system: elasticsearch
status: verified
checked: 2026-07-31
tags: [jvm, heap, OutOfMemoryError, docker, gc, heap-dump, exit-code-127]
---
# Elasticsearch container restarted: telling a Java heap OOM from a kernel/cgroup OOM kill

## Symptom

A Dockerized Elasticsearch node restarts by itself. `docker inspect` shows
`RestartCount` incremented, exit code `127` and `OOMKilled=false`; the host did
not reboot and `journalctl -u docker` says `manualRestart=false`. Nobody
touched it.

## Cause

Exit code 127 with `OOMKilled=false` is not the kernel OOM killer (that gives
137/`OOMKilled=true`). It is the JVM terminating itself: Elasticsearch's
`ElasticsearchUncaughtExceptionHandler` exits the process on
`java.lang.OutOfMemoryError: Java heap space`. The heap (`-Xmx`) was exhausted
inside the process while the container had plenty of RAM. With G1, a large
share of the retained heap is often *humongous* regions (objects > half a
region, i.e. big request/response buffers or aggregations), which the final
Full GCs cannot reclaim.

## Fix

Confirm and collect evidence in this order:

```bash
docker inspect elasticsearch | grep -E 'ExitCode|OOMKilled|RestartCount|FinishedAt'
journalctl -k | grep -iE 'oom|killed process'          # must be empty for a JVM OOM
docker logs --timestamps elasticsearch | grep -n 'OutOfMemoryError'
tail -n 200 /path/to/gc.log*                            # Full GC storm, heap ~= Xmx, "humongous"
ls -lh /path/to/data/java_pid*.hprof                    # heap dump if HeapDumpOnOutOfMemoryError is on
curl -s localhost:9200/_cluster/health
curl -s 'localhost:9200/_nodes/_local/stats/jvm,breaker,thread_pool'
```

Then:

- keep the `.hprof` (it is the only artifact that names the retaining object
  graph) and analyze it with Eclipse MAT (Leak Suspects, dominator tree) on a
  machine with RAM >= dump size; treat it as sensitive, it contains documents;
- correlate the minute before the first `OutOfMemoryError` with request logs
  and monitoring (heavy aggregations, large bulk requests, huge `size`);
- alert on sustained old-gen occupancy / GC overhead, and review circuit
  breaker limits (`indices.breaker.*`) so the request is rejected instead of
  killing the node.

## Limits

- Verified on Elasticsearch 6.8 with G1 and a 16 GiB heap; newer versions
  have a real-memory circuit breaker that usually prevents this.
- `restart: always` masks the failure as a short blip; without it the node
  stays down, so pair it with alerting on `RestartCount`.
- Heap dump generation pauses the JVM for tens of seconds and needs free disk
  equal to the heap size on the data volume.
