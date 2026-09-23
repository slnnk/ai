---
system: evaluation-service
status: verified
checked: 2026-09-11
tags: [evaluation-service, postgresql, data-map, sql, assessments]
---
# YouDo Evaluation Service

Last checked: 2026-09-11.

## Purpose and repository

- Employee evaluation service.
- Local repository: `/home/slnnk/git/youdo-evaluation-service`.
- Safe origin: `git@gitlab.youdo.sg:youdo/processes/youdo-evaluation-service.git`.
- Current branch at check time: `master` (snapshot, not a permanent property).

## PostgreSQL data map

- Local database name documented by the repository: `youdo_evaluation_service`.
- Production database name in CI configuration: `youdo_evaluation`.
- `persons`: employees; relevant columns are `id`, `full_name`, `email`, `position`, `is_active`, `manager_id`.
- `assessments`: evaluation sheets; `subject_person_id` references the evaluated employee, `evaluator_person_id` references the evaluator. Relevant result columns are `total_score`, `rank`, `status`, `period_id`; rows with `deleted_at IS NOT NULL` are soft-deleted.
- `assessment_scores`: per-criterion values; joins to `assessments` using `assessment_id`, with `criterion_id`, nullable `level` (1 through 4), and `note`.
- Basic employee/result query: join `assessments.subject_person_id` to `persons.id` and exclude `assessments.deleted_at IS NOT NULL`.

## Diagnostics and configuration

- Entity mappings: `src/YouDo.Evaluation.Infrastructure/Configurations/`.
- EF Core migrations: `src/YouDo.Evaluation.Infrastructure/Migrations/`.
- Local database setup and migrations: repository `README.md` and `Makefile`.
- Deployment database name and CI variables: `.gitlab-ci.yml`; access secrets are obtained through the configured deployment secret path and are not recorded here.

## Work log

### 2026-08-19 — SQL for employee names and evaluations

Confirmed the actual table and column names from entity configurations and migrations. For final scores, select `persons.full_name` and `assessments.total_score`, joining on the evaluated person and filtering out soft-deleted assessment sheets. For criterion-level values, additionally join `assessment_scores` on `assessment_id`.

### 2026-08-19 — Interpretation of total score and rank

- `total_score` is the sum of the configured weight for every selected criterion level, not an average of raw levels. The active `youdo-v2` schema has 10 criteria; a fully completed sheet ranges from 4.00 (all level 1) to 16.00 (all level 4).
- `rank` is calculated only when every criterion has a selected level; otherwise it is `NULL` while `total_score` remains a partial running sum.
- The seeded inclusive upper thresholds are: rank 1 `<=6`, rank 2 `<=7`, rank 3 `<=8`, rank 4 `<=9`, rank 5 `<=10`, rank 6 `<=11`, rank 7 `<=12`, rank 8 `<=13`, rank 9 `<=14`, rank 10 `<=16.01`. Thresholds belong to a criteria set, so operational SQL should join `rank_bands` by `criteria_set_id` instead of assuming they never change.
- The repository defines the calculation and calls `rank` a "разряд" (grade), but does not define its business meaning or whether it maps to compensation/grade; a product review explicitly records this as missing documentation.

### 2026-09-11 — Manual check for new employee assessments

- Production access was not revalidated because the user chose to run the SQL manually.
- For a reliable check, join `assessments` to `persons`, `periods`, and evaluator `persons`; include `created_at` and `updated_at`, and exclude soft-deleted assessments.
- The previous investigation baseline is 2026-08-19; filtering `created_at` or `updated_at` after that date isolates newly created or subsequently changed sheets.
