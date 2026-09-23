---
system: youdo-business
status: verified
checked: 2026-09-03
tags: [gitlab-ci, dotnet-unit-tests, integration-test, merge-request, marketplace]
---
# youdo.business job 3109318: marketplace onboarding integration test

Last verified: 2026-09-03

## Task

Find out why job `3109318` (`dotnet-unit-tests`) of MR `!3727` failed.

## Context

- Repository: `/home/slnnk/git/youdo.business`
- Origin: `git@gitlab.youdo.sg:youdo/microservices/youdo.business.git`
- MR: `!3727`, `Site-25463-marketplace-integration` -> `Site-25456-MarketPlace`
- Pipeline: `137916`
- Job: `3109318`, `dotnet-unit-tests`
- Tested SHA: `32f6a4e67f4549deb7066818ac9e3cb6099f08f4`
- Runner: `gitlab-runner-docker-1 integrations-tests (172.28.0.171)`

## Findings

### Result

The build and all 379 unit tests succeeded. Integration tests had one failure out of 634 (632 passed, 1 skipped):

`MarketplaceContractPublishTests.OnboardingState_ForNonMarketplaceContractTask_Fails`

The assertion at `MarketplaceContractPublishTests.cs:299` expected `response.IsSuccess == false`, but got `true`.

### Root cause

Commit `5651753517ff6e27a606f7c33a5fc822cc95eba3` (`contract?.ProjectId`) changed `EmployeeOnboardingByYouDoUserRequest.GetProjectIdByTaskAsync` from:

```csharp
return contract is { IsMarketplace: true } ? contract.ProjectId : null;
```

to:

```csharp
return contract?.ProjectId;
```

This removes the `IsMarketplace` guard. The failing test creates a marketplace contract, updates `IsMarketplace` to `false`, and expects the onboarding lookup to reject it. The changed handler still obtains the project, then returns `Result.Ok` for the unknown employee, so the assertion fails deterministically.

The bad commit was merged into the MR head by merge commit `32f6a4e67`. The current remote target branch `origin/Site-25456-MarketPlace` points at `81c6dbf36` and has the original guarded expression again; it no longer contains commit `565175351`. The MR head still contains the bad commit. Earlier MR pipeline `137911` on SHA `c305d9378` succeeded; no newer pipeline than `137916` existed at verification time.

Cache extraction/NuGet source warnings at the start of the trace are non-fatal and unrelated. Artifacts uploaded successfully; the missing `coverage.json` warning is also not the job failure.

## Open items

Resolution: restore the `IsMarketplace` guard in the MR source branch (or rebuild/rebase the source branch cleanly on the corrected target without retaining commit `565175351`) and rerun the pipeline. A normal merge from the target may not remove the already-merged bad commit, so verify the resulting line explicitly.

## Portable lesson

none
