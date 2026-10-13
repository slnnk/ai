---
system: maven
status: verified
checked: 2026-10-12
tags: [maven, gradle, recovery, bootstrap]
---
# Recover mutually dependent Maven snapshots

## Summary

When a fresh artifact repository lacks mutually dependent snapshots, current-source shared classes can provide a temporary bootstrap jar. Validate dependent main jars locally, publish the bootstrap explicitly, publish dependent libraries, then immediately replace the bootstrap with the full artifact. Use one bounded final validation pass. Local main-jar validation, publication, full-artifact replacement and the bounded final build/publication pass have been verified. Full builds excluded test execution; runtime/deployment validation remains outside this recipe.

## Symptom

After artifact storage loss or migration to an empty repository, library A cannot build because library B is missing; library B cannot build because A is missing. Retrying the same publication jobs does not resolve this cycle.

## Cause

The libraries consume each other's previously published jars. Existing snapshots can allow routine builds, while an empty repository exposes a bootstrap problem. Treat the explanation that old artifacts masked the issue as an inference unless historical build evidence confirms it. Inspect main-source imports, build dependencies, publication tasks and the relevant source revisions before choosing a recovery method.

## Fix

1. Pin current source revisions. Identify the exact API used by dependent main sources and recursively collect its same-library dependency closure. Include required field types, interfaces, enums, superclass implementations, annotation processing and external libraries.
2. Compile those unchanged current sources into a reduced temporary jar outside source checkouts. Use the snapshot coordinate already consumed by the dependent libraries. Generate matching Maven metadata/POM locally and record provenance/checksum.
3. Force the bootstrap module to resolve exclusively from the isolated local Maven repository. Validate dependent `:jar` tasks locally; guard the task graph against test, precondition, report and publication tasks. Do not substitute a normal full build: its test compilation can require additional APIs absent from the reduced jar.
4. Explicitly publish the reviewed bootstrap artifact, then publish the dependent full main jars. Verify each action's outcome before taking dependent actions.
5. Immediately compile and publish the full original artifact against those restored dependent jars. Verify metadata now identifies the full snapshot rather than the bootstrap.
6. Perform one bounded final pass: rebuild/republish dependent libraries against the full artifact, then validate and publish the original library. Define required actions and success conditions beforehand; read-only status polling does not create new retries. Investigate new failures rather than repeating until convergence.

## Limits

- The reduced artifact is recovery-only. It lacks normal APIs and must not serve ordinary runtime, test or other full-library consumers. Keep the exposure brief and replace it with the full artifact before normal work resumes.
- Removing dependency declarations alone can fail because main sources import the other library. Older source revisions may lack current package names, methods or types even if they predate the dependency cycle.
- Plugin libraries, external dependencies, repository access, credentials, compiler versions and annotation processors must still resolve. A static closure audit is insufficient until actual local compilation succeeds.
- `:jar` ordinarily compiles main sources only, but inspect custom task dependencies and plugin behavior; a task-graph guard can fail closed if additional effects appear.
- Maven metadata checks establish published version selection. They do not independently verify downloaded jar contents or full transitive build compatibility. If verification is intentionally limited to metadata, report that limit and avoid downloading packages without need.
- Publishing artifacts or triggering CI changes external state; apply the session's explicit approval rules independently of local preparation.
- Extracting common APIs into a standalone shared library can remove the architectural cycle, but it is a separate optional task, not part of minimal recovery.
