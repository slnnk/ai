---
system: rabbitmq
status: verified
checked: 2026-10-07
tags: [rabbitmq, masstransit, test-stands, test5]
---
# test5: validateemailcode slow due to youdo.user.signin exchange auto_delete mismatch

## Summary

On test5, `POST /api/signin/validateemailcode/` took ~8–10 s (test1 < 1 s). Cause: publishing
`UserSignedInEvent` to exchange `youdo.user.signin` in vhost `test5` fails with AMQP 406
`PRECONDITION_FAILED - inequivalent arg 'auto_delete' ... received 'true' but current is 'false'`.
The publisher (MassTransit route `ExchangeAutoDelete: True`) retries topology setup
(`HostConfigurationRetryExtensions.Retry`) for ~8 s inside the request, then logs
"Unable to publish" and returns. The event is lost on test5. Fix: recreate the exchange with
`auto_delete=true` (delete it in vhost `test5`; the next publish redeclares it).

## Task

Reported: validateemailcode on test5 ~10 s, test1 < 1 s; a Sentry/log error about publishing
`UserSignedInEvent` was attached.

## Context

- Nomad job `youdo-test5`, task `youdo-test5-web-mvcapplication`; RabbitMQ
  `rabbitmq.service.yandex-test.consul` (10.16.26.17), vhost per stand (`/test5`, `/test1`).
- RabbitMQ settings of mvcapplication are identical on test1 and test5 (`RabbitMqConnectionTimeout` 10,
  `RabbitMqPublishTimeout` 30, `RabbitMqRecoveryInterval` 3); only the vhost differs.

## Actions

- Read Nomad job specs via API (`/v1/job/youdo-test5`, `/v1/job/youdo-test1`), grep RabbitMQ settings.
- Management API `:15672` GET with the app credential from the job template: `not_authorised`
  (`Not management user`), so exchange properties could not be read directly.
- Checked `sorm` (a `youdo.user.signin` consumer): its `ExchangeDeclareAsync` is commented out in
  `BaseConsumer.cs` since at least 2026-04-13, so current sorm builds do not declare the exchange.

## Findings

- Timeline matches: request `X-Timestamp` 15:43:06, error logged 15:43:14 (= Chrome "Waiting for
  server response" 8.21 s).
- In vhost `test5` the exchange exists with `auto_delete=false`; the monolith declares `true`.
  Verified over AMQP (passive declare, then equivalence probes with pika; no state change):
  test1 `durable=true, auto_delete=true`; test5 `durable=true, auto_delete=false`.
- Who created it with `auto_delete=false` on test5 is unknown (hypothesis: manual creation,
  definitions import, or an old/other-branch consumer build).

## Changes

Resolved 2026-10-07 by the team: the RabbitMQ object in vhost `test5` was deleted (reported as "the queue")
and the publisher redeclared the exchange. Re-probe confirmed `youdo.user.signin` in `test5` is now
`durable=true, auto_delete=true`, same as test1.

## Open items

- Delete exchange `youdo.user.signin` in vhost `test5` with a management/admin account (needs user
  approval); check its bindings first and that the bound queues' consumers survive the rebind.
- Check other exchanges in `test5` for the same mismatch (other "Unable to publish" errors).
