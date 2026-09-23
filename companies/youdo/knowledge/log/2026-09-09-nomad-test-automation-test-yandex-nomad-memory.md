---
system: nomad-test
status: verified
checked: 2026-09-09
tags: [nomad, resources, memory, automation-test-yandex, jinja2, youdo-business]
---
# automation-test-yandex: Nomad resource adjustment

## Task

Lower the Nomad scheduling reservation of the legacy Yandex test deployment jobs: halve
the `memory` reservation of the microservice and monolith templates and drop `cpu`
reservations, while keeping `memory_max` unchanged.

## Context

- Date: 2026-09-09
- Repository: `/home/slnnk/git/automation-test-yandex`
- Area: legacy Yandex test deployment, Nomad microservice jobs
- Templates: `playbooks/deploy/docker/files/deploy_microservices/*.j2`
- Monolithic job template: `playbooks/deploy/docker/files/nomad_youdo-business/youdo-business.j2`

## Changes

All 21 dynamic `resources.memory` expressions in the microservice Nomad templates now render half of the configured `*_memory` value using integer division:

```jinja2
memory = {{ (<service>_memory | default("256", true) | int) // 2 }}
```

The corresponding `memory_max` expressions were intentionally left unchanged. Fixed memory values in migration-task templates were also left unchanged. This makes the configured service memory value continue to drive the maximum while lowering the Nomad scheduling reservation for dynamic microservice tasks.

All `resources.cpu` fields were also removed from the templates in this directory. Nomad therefore uses its default CPU reservation for these tasks; with the Docker driver's default soft limiting, allocations can still burst when host CPU is available.

The same adjustment was applied to all 11 resource blocks in `nomad_youdo-business/youdo-business.j2`: each fixed `memory` reservation was divided by two, every `cpu` field was removed, and all existing `memory_max` values were preserved.

## Findings (verification)

- Confirmed 21 dynamic `memory` expressions use `// 2`.
- Confirmed no dynamic or fixed `cpu` fields remain in `deploy_microservices` templates.
- Confirmed all 11 `nomad_youdo-business` memory reservations were halved and no `cpu` fields remain in that template.
- `git diff --check` completed successfully.
- Changes remain uncommitted as of this note.

## Open items

- Lower reservations permit denser placement. Monitor host memory pressure, allocation OOM/restarts, and application latency after deployment.

## Portable lesson

none
