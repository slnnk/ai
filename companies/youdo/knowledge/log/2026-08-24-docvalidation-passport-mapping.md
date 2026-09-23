---
system: docvalidation
status: verified
checked: 2026-08-24
tags: [docvalidation, passport, mapping, ArgumentOutOfRangeException, sumsub, b2b]
---
# DocValidation: passport mapping crash caused by a short number

Date of check: 2026-08-24. Translated from Russian.

## Task

Explain the `ArgumentOutOfRangeException` from an event on `GET /api/v1/B2BRequests/{requestId}/passport`.

## Context

- Repository: `/home/slnnk/git/docvalidation`
- Origin: `git@gitlab.youdo.sg:youdo/microservices/docvalidation.git`
- Environment from the event: `Staging_test12`, host `doc-validation.test12.yandex-test.youdo.local`
- Request: `GET /api/v1/B2BRequests/{requestId}/passport`

## Findings

In `src/YouDo.DocValidation.API/Mappers/UserPassportProfile.cs` the mapping `DocumentInfo -> PassportInfoModel` parses `DocumentInfo.Number` as a string consisting of series and number:

- `Substring(0, 4)` is the series;
- `Substring(4, Number.Length - 4)` is the number.

The only check is for null/empty string. With `Number.Length` from 1 to 3, the second call receives `startIndex = 4`, which is greater than the string length, matching the `ArgumentOutOfRangeException` from the event. The B2B controller has no number-length check before the mapping.

The related code `DocumentInfoExtensions.CalculateHash` already treats a number shorter than 5 characters as invalid and returns null. This confirms the discrepancy: the API mapper accepts a too-short value right up to the crash.

## Open items

What to check next:

1. Find the original SumSub `DocumentInfo` for the request id from the event and check the length of `Number`, the document type and the country. Do not write the full number into logs; the length and a format flag are enough.
2. Check whether the model "4 characters of series + the rest as number" really applies to the selected `identityDoc`: B2B selects an identity document but returns it through the passport mapping.
3. Fix the contract for handling an invalid number: validate the format before mapping and return a controlled 4xx/domain error, or make the mapping safe. The conditions must be aligned with `CalculateHash` and with the supported document types/countries.
4. Add tests for null, empty string, length 1–3, length 4 and a valid number.

## Related diagnostic points

- Mapping: `src/YouDo.DocValidation.API/Mappers/UserPassportProfile.cs`
- B2B endpoint: `src/YouDo.DocValidation.API/Controllers/B2bRequestsController.cs`
- Length check for hashing: `src/YouDo.DocValidation.Domain/Helpers/DocumentInfoExtensions.cs`
- API logs: middleware `ErrorHandlingMiddleware`; the trace contains the `RequestId`/Sentry trace from the original event.

## Portable lesson

none
