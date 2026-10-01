---
system: helm
status: verified
checked: 2026-09-30
tags: [helm, sprig, templates]
---
# Helm/Sprig: default true turns an explicit false into true

## Symptom

A chart has a boolean that should default to on, and setting `enabled: false` in values has
no effect: the resource is still rendered.

```yaml
{{- if ne (.Values.service.enabled | default true) false }}
kind: Service
...
```

`helm template` with `service.enabled: false` still outputs the Service.

## Cause

Sprig `default` returns the default when the value is "empty", and `false` counts as empty
(like `0`, `""`, `nil`, empty list/map). So `false | default true` evaluates to `true`.

## Fix

Test for the key instead of the value:

```yaml
{{- if or (not (hasKey .Values.service "enabled")) .Values.service.enabled }}
```

or compare the string form, which keeps `false` distinct from "unset":

```yaml
{{- if ne (toString .Values.service.enabled) "false" }}
```

`toString nil` is `"<nil>"`, so an unset key renders the resource. Add a template test with
`enabled: false`, `enabled: true` and the key absent.

## Limits

- The same trap applies to any `| default <non-empty>` over a boolean or numeric `0`.
- For nested maps that may be absent, guard the parent first (`dig`, or `hasKey` on each
  level), otherwise `hasKey` fails on `nil`.
