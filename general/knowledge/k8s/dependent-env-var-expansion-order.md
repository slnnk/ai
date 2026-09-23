---
system: k8s
status: verified
checked: 2026-06-25
tags: [kubernetes, env, envFrom, variable-expansion, secrets, rabbitmq, configmap]
---
# `$(VAR)` in a container env value is passed literally (e.g. `amqp://$(USER):$(PASS)@host/`)

## Symptom

A service cannot authenticate to a dependency (RabbitMQ `ACCESS_REFUSED`, database auth
error) although the credentials Secret is correct. The dependency's log shows the **literal**
placeholder as the username:

```text
user '$(RabbitMq__Username)' ... access refused
```

The composed URL variable lives in a ConfigMap loaded with `envFrom`, while the username and
password come from a Secret via `env[].valueFrom.secretKeyRef`.

## Cause

Kubernetes expands `$(VAR)` in `env[].value` **only** against variables defined **earlier in
the same container's `env` list** (plus a few built-ins). It never expands references to
variables that arrive through `envFrom` (ConfigMap/Secret), and variables inside a ConfigMap
that is itself loaded via `envFrom` are not expanded at all. If the URL is in the ConfigMap
and the credentials are separate `env` entries, the placeholder is delivered verbatim.

## Fix

Define the dependent variable as an explicit `env` entry **after** the variables it
references, in the same container:

```yaml
env:
  - name: RabbitMq__Username
    valueFrom:
      secretKeyRef: { name: rabbitmq-auth, key: rabbitmq-app-username }
  - name: RabbitMq__Password
    valueFrom:
      secretKeyRef: { name: rabbitmq-auth, key: rabbitmq-app-password }
  - name: RabbitMq__Url
    value: "amqp://$(RabbitMq__Username):$(RabbitMq__Password)@rabbitmq/"
envFrom:
  - configMapRef: { name: app-env }     # must NOT contain RabbitMq__Url
```

In a Helm chart with a shared global `env` map, this means moving composed URLs from the
global ConfigMap into the per-service `env` block rendered after `envValueFrom`/secret
entries, or providing a chart helper that always renders credentials first and composed URLs
last. Verify with `helm template` that the order is correct, then in the pod:

```bash
kubectl exec <pod> -- sh -c 'echo "$RabbitMq__Url"'   # must show real values, not $(...)
```

## Limits

- Expansion is per container; an init container cannot see the app container's variables.
- A `$(VAR)` that cannot be resolved is left as-is; use `$$(VAR)` to emit a literal.
- If the application supports separate host/user/password settings, prefer those over a
  composed URL and avoid the ordering dependency entirely.
