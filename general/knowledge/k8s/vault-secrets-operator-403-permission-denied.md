---
system: k8s
status: verified
checked: 2026-06-11
tags: [kubernetes, vault, vault-secrets-operator, VaultStaticSecret, VaultAuth, 403, policy]
---
# VaultStaticSecret never creates the Kubernetes Secret: Vault returns 403 permission denied

## Symptom

A new application's `VaultStaticSecret` is `Healthy=False`, `SecretSynced=False`; the target
Kubernetes Secret does not exist, so the deploy job waiting for it fails
(`secrets "<name>" not found`). Another `VaultStaticSecret` in the same namespace (e.g. the
registry pull secret) syncs fine. Events on the failing resource show:

```text
GET http://vault...:8200/v1/secret/<path>: 403 permission denied
```

## Cause

Vault Secrets Operator authenticates to Vault with the `VaultAuth` referenced by the
resource; when `spec.vaultAuthRef` is empty it falls back to the **default** `VaultAuth`
(operator namespace), which is bound to one Vault role and therefore one policy set. That
policy grants read on the paths the existing secrets use, not on the new application's path.
The working sibling secret proves auth and connectivity are fine; only authorization for the
new path is missing.

## Fix

Inspect first:

```bash
kubectl -n <ns> get vaultstaticsecret <name> -o jsonpath='{.spec.vaultAuthRef}{"\n"}{.status}'
kubectl -n <vso-ns> get vaultauth -o yaml | grep -E 'role:|mount:'
vault read auth/<mount>/role/<role>            # which policies the role carries
vault policy read <policy>
```

Then either:

1. Extend the policy behind the default role with the new path (`path "secret/<app>/*"
   { capabilities = ["read"] }` — for KV v2 the path includes `data/`), or
2. Preferred for isolation: create a dedicated Vault role + policy for the app, a `VaultAuth`
   in the app namespace pointing at that role, and set `spec.vaultAuthRef` on the
   `VaultStaticSecret`.

VSO retries on its own; within a minute the status flips to `SecretSynced=True` and the
Secret appears. Old 403 events remain in `kubectl describe` history and are not a sign of a
current problem.

## Limits

- A 403 can also come from the Kubernetes auth role's `bound_service_account_namespaces`
  not including the app namespace; the fix is on the role, not the policy. The error text is
  the same, so check both.
- KV v1 vs v2 path shapes differ (`secret/app` vs `secret/data/app`); a policy written for the
  wrong engine version also yields 403.
