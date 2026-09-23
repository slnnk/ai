---
system: youdo-business
status: verified
checked: 2026-09-10
tags: [gitlab-ci, build, cs0246, linq2db, generated-code, merge-request]
---
# youdo.business pipeline 138220 build failure

## Task

Determine why all build jobs of MR pipeline `138220` failed.

## Context

- Checked: 2026-09-10 (Europe/Moscow)
- Project: `youdo/microservices/youdo.business` (GitLab project ID 423)
- Pipeline: `138220`, MR pipeline for `refs/merge-requests/3741/head`
- MR: `!3741`, `Site-25489-c2c-onboarding` -> `master`
- Pipeline SHA: `7dc00d537ef1050b16504b90a8a227eee19d11a3` (`merge fix`)
- Local repository: `/home/slnnk/git/youdo.business`
- Safe origin: `git@gitlab.youdo.sg:youdo/microservices/youdo.business.git`

## Findings

### Symptom

All eight executed/retried build jobs failed with the same compiler error:

```text
YouDo.Business.Db/BusinessDb.Generated/Company.generated.cs(220,22):
error CS0246: The type or namespace name 'LeadCompany' could not be found
```

Affected jobs: `3128226` through `3128233` (`build-automation-web` including retry,
`build-business-api`, `build-business-internal-api`, `build-business-web`,
`build-mock-api`, `build-worker`, and `build-employee-web`). They ran on multiple
online B2B/DinD runners, so this is a source compilation defect rather than a
single-runner or registry failure. Later deploy and autotest jobs were skipped
because the build stage failed.

### Root cause

Commit `8cf4f02aae0389b45c3ee34aad441a8169bbdafe` (`db generated`, 2026-09-09)
reintroduced this association into
`YouDo.Business.Db/BusinessDb.Generated/Company.generated.cs`:

```csharp
[Association(ThisKey="Id", OtherKey="CompanyId", CanBeNull=true)]
public IEnumerable<LeadCompany> Leadcompanyidfks { get; set; }
```

The `LeadCompany` generated class is absent from the MR tree. The old lead domain
and `BusinessDb.Generated/LeadCompany.generated.cs` had previously been removed
by commit `ac66db8dc156900eee6e5685721c71f8ef310752` (`Site-25168`). Current
`origin/master` also has neither the stale association nor the generated class.

The likely mechanism is regeneration against a database/schema that still
contains the obsolete `public.lead_companies` foreign key, which restored only
the back-reference in `Company.generated.cs` while the corresponding generated
model remained deleted/excluded.

### Recommended correction

Remove the six-line `lead_companies_company_id_fk_BackReference` block from
`Company.generated.cs` (matching current `master`), commit it to
`Site-25489-c2c-onboarding`, and rerun the pipeline. Preferably also regenerate
against the current intended schema or adjust the generator source/filter so the
obsolete association is not reintroduced on the next DB generation.

## Actions

Checks performed:

- GitLab API: pipeline metadata, MR metadata, job list, and traces for all eight
  failed jobs.
- `git fetch origin refs/merge-requests/3741/head refs/heads/master` without
  switching or modifying the working tree.
- `git grep`/`git ls-tree`: stale `LeadCompany` reference exists at pipeline SHA,
  while no `LeadCompany` class/file exists.
- `git log -S 'IEnumerable<LeadCompany>'`: identified `8cf4f02aa` as the
  reintroduction commit.
- Compared the generated file with current `origin/master`, where the stale block
  is absent.

## Open items

Remaining risk: if the generator is run against the same stale schema, a manual deletion alone
will recur. Confirm whether `public.lead_companies` should still exist in the DB
used for generation and align that database or generator exclusions with the
repository model.

## Portable lesson

none
