---
system: terraform
status: verified
checked: 2026-09-14
tags: [terraform, destroy, depends_on, managed-kubernetes, iam, FailedPrecondition]
---
# Terraform destroy of a managed Kubernetes cluster stops half-way (IAM bindings gone, cluster left)

## Symptom

`terraform apply <saved destroy plan>` for a managed Kubernetes root deletes the service account's
IAM bindings and a few security-group rules, then fails on the node group with the cloud API error
`FailedPrecondition` (for example `operation is not permitted because the cluster is stopped` or
`deletion is not permitted while cluster ... is stopped`). Afterwards the state holds only the
cluster, node group and service account; the bindings are gone. A retry of the saved plan is
refused as stale, and starting the cluster manually returns `PermissionDenied` because the cluster
service account lost its roles.

## Cause

Two independent problems combine:

1. The API refuses to delete a node group (and therefore the cluster) while the cluster is in the
   `STOPPED` state. Terraform does not know this precondition and tries anyway.
2. Terraform derives destroy order from resource references only. The cluster references the
   service account ID, not the `folder_iam_member` / `*_iam_binding` resources, so those bindings
   have no dependents and are destroyed in the first wave. The cluster then has no permissions to
   act, and even the manual `start` needed to unblock deletion fails.

Terraform persists state after each successfully destroyed resource, so a failed run leaves a
partially destroyed graph, and the previously saved plan no longer matches the state.

## Fix

Recover:

1. Restore the bindings with a targeted plan built from the normal configuration
   (`terraform plan -target=<each binding>` -> expected `N to add, 0 to change, 0 to destroy`),
   apply it after review.
2. Start the cluster with the cloud CLI using a credential that has the right roles, wait for
   `RUNNING`, then create a **fresh** destroy plan. Never re-apply the stale one.

Prevent it in configuration by making the cluster depend explicitly on its bindings so they are
destroyed last:

```hcl
resource "yandex_kubernetes_cluster" "this" {
  # ...
  depends_on = [
    yandex_resourcemanager_folder_iam_member.k8s_agent,
    yandex_resourcemanager_folder_iam_member.vpc_public_admin,
    yandex_resourcemanager_folder_iam_member.images_puller,
    # every binding the cluster or node service account needs
  ]
}
```

With this the destroy order becomes node group -> cluster -> bindings -> service account. Verify in
the plan JSON (`terraform show -json plan | jq '.configuration'`) that the dependencies are present.

Also run destroys with the lock on, and keep a pre-destroy state backup:
`terraform state pull > pre-destroy.tfstate` (mode `0600`, delete when done).

## Limits

- Observed on Yandex Managed Kubernetes with the Yandex provider 0.169; other clouds have similar
  "cluster must be running" preconditions, but the exact error text differs.
- `depends_on` on the cluster also delays cluster *creation* until the bindings exist, which is
  usually what you want anyway.
- If the saved destroy plan came from a module that fails during planning (for example a missing
  `template_name` key in `node_groups_defaults`), fix the configuration first; you cannot destroy
  through a configuration that does not plan.
- Deleting the local working directory or the cloud folder by hand does not remove the state in a
  remote backend; only a successful destroy (or a deliberate `removed`/`state rm`) does.
