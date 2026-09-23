---
system: k8s
status: verified
checked: 2026-08-25
tags: [kubernetes, postgresql, pvc, statefulset, PGDATA, lost+found, initdb]
---
# PostgreSQL StatefulSet never becomes ready: `initdb` refuses a PVC containing `lost+found`

## Symptom

A PostgreSQL pod backed by a freshly provisioned PersistentVolumeClaim crash-loops at first
start; `helm install --wait` times out. The container log ends with:

```text
initdb: error: directory "/var/lib/postgresql/data" exists but is not empty
initdb: hint: If you want to create a new database system, either remove or empty the directory "/var/lib/postgresql/data" or run initdb with an argument other than "/var/lib/postgresql/data".
```

or the entrypoint prints that it found `lost+found` in the data directory.

## Cause

Block-storage CSI drivers format the volume with ext4, which creates a `lost+found` directory
at the filesystem root. The chart mounts the PVC directly at PostgreSQL's default `PGDATA`
(`/var/lib/postgresql/data`), so `initdb` sees a non-empty directory and aborts. The same
manifest works with `emptyDir` or hostPath, which is why it passes local tests.

## Fix

Point `PGDATA` at a subdirectory of the mount so the data directory itself starts empty:

```yaml
containers:
  - name: postgres
    image: postgres:16
    env:
      - name: PGDATA
        value: /var/lib/postgresql/data/pgdata
    volumeMounts:
      - name: data
        mountPath: /var/lib/postgresql/data
volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ReadWriteOnce]
      resources:
        requests:
          storage: 5Gi
```

Alternative: use `subPath: pgdata` on the volumeMount. Both keep `lost+found` outside
`PGDATA`. The official image documents this workaround.

## Limits

- Changing `PGDATA` on an existing populated volume moves the expected location; migrate the
  files or start from a fresh PVC.
- The Bitnami PostgreSQL chart already uses a subdirectory (`/bitnami/postgresql/data`); the
  issue is specific to hand-written manifests around the official `postgres` image.
- Also watch for a half-created release: with `helm --atomic`, pre-install hook resources
  (StatefulSet, PVC, Jobs) survive the rollback and must be cleaned manually (see
  `../helm/atomic-install-failure-leaves-hook-resources.md`).
