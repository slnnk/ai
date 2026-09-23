---
system: escrow-tinkoff
status: hypothesis
checked: 2026-07-20
tags: [escrow-tinkoff, e2c, 502, refit, test7, tinkoff, outbound]
---
# Escrow.Tinkoff: 502 on E2C AddCustomer

Translated from Russian.

## Context

- Date: 2026-07-20, environment: test7, repository: /home/slnnk/git/escrow.tinkoff.

## Task

Symptom: `GET /api/card/request/add` for executor fails with `Refit.ApiException: 502 Bad Gateway`.

## Findings

- Call chain: `CardController.GetAddCardRequestAsync` -> `EscrowService.GetAddCardRequestAsync` -> `CardsService.GetAddCardUrlAsync` -> `CustomerService.GetOrCreateBeneficiaryAsync` -> `TinkoffE2CClient.AddCustomerAsync`.
- External call: `POST {Tinkoff__E2c__Endpoint}/e2c/AddCustomer`; on test environments the endpoint from devops/config.yml is `https://rest-api-test.tinkoff.ru`.
- Conclusion: the 502 is returned by the upstream E2C/bank gateway or a network proxy on the outbound call, not by the inbound nginx of escrow-tinkoff-api. It happens when a new beneficiary is created; if the beneficiary already exists in the DB, AddCustomer is not called.
- Risk/hypothesis from the data: the phone in requests has the form `71111...` without `+`; the model comments the format as `+71234567890`, but business validation should normally return JSON with an error, not HTTP 502.

## Open items

What to check next: find the outbound error log by trace/request id around 2026-07-20 12:12:01 and 12:15:07 MSK; check the 502 response body, reachability of `rest-api-test.tinkoff.ru/e2c/AddCustomer` from the test7 container/alloc, DNS/TLS/proxy; compare success of eacq/e2c and other E2C methods; if widespread, escalate to T-Bank with the time and the request payload without the token.

## Portable lesson

none
