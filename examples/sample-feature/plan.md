# Design — transfer-limit-alerts

**Status: APPROVED — Tulga (tech lead), 2026-07-02**

| Field        | Value                                         |
| ------------ | --------------------------------------------- |
| Feature      | `007-transfer-limit-alerts`                    |
| Authored     | 2026-07-02                                     |
| Requirements | [spec.md](spec.md) — approved 2026-07-02       |
| Approver     | Design gate: alerts-service technical authority |

This is the **Design Document** of the teaching example. Its two contract
sections follow the `backend-services` profile — this is what the profile's
table shapes look like on a real feature (one synchronous operation family,
one consumed and one produced event).

## 1. Summary

A new `alerts-service` capability: a small CRUD surface for alert
registration, a consumer on the payments limit-exceeded subject, and
delivery through the existing notification service. State lives in the
service's own store; idempotency rides the producer's `event_id`.

## 2. Architecture overview

transfer-service (existing) publishes `transfer-limit-exceeded`.
alerts-service (this feature) consumes it, matches active alerts, and calls
notification-service (existing) for delivery; every attempt lands in the
delivery log. Alert registration is a synchronous API on alerts-service.

## 3. Synchronous contracts

| Operation | Method & path | Auth | Request | Responses | Errors | Idempotency |
| --------- | ------------- | ---- | ------- | --------- | ------ | ----------- |
| create-transfer-limit-alert | `POST /transfer-limit-alerts` | `alerts:write` | `{account_id, threshold, channel}` | `201` created alert | `400 VALIDATION_FAILED` [R-2], `404 ACCOUNT_NOT_FOUND` [R-4], `409 ALERT_EXISTS` [R-3] | Natural key `(account_id, threshold, channel)` [R-3] |
| list-transfer-limit-alerts | `GET /transfer-limit-alerts?account_id=` | `alerts:read` | query by account | `200` alert list | `404 ACCOUNT_NOT_FOUND` | Read — idempotent |

## 4. Asynchronous contracts

| Event | Subject/topic | Schema | Producer | Delivery | Consumers |
| ----- | ------------- | ------ | -------- | -------- | --------- |
| transfer-limit-exceeded | `payments.transfer.limit-exceeded` | `contracts/transfer-limit-exceeded.schema.json` | transfer-service | at-least-once; consumers de-duplicate on `event_id` [R-6] | alerts-service (this feature), `open` |
| alert-notification-delivered | `alerts.notification.delivered` | `contracts/alert-notification-delivered.schema.json` | alerts-service | at-least-once; consumers de-duplicate on `delivery_id` | audit pipeline [R-8], `open` |

## 5. Data and storage

Two tables owned by alerts-service: `alerts` (id, account_id, threshold,
channel, state) and `delivery_log` (delivery_id, alert_id, event_id,
attempt, outcome, at) [R-7] [R-8]. Consumed `event_id`s are unique-indexed
in `delivery_log` — that index IS the R-6 dedup.

## 6. Design decisions

| ID | Decision | Rationale |
| -- | -------- | --------- |
| D1 | Dedup by unique index on `event_id`, not an in-memory cache | Survives restarts and horizontal scaling; the at-least-once replay test (spec §3) verifies it |
| D2 | Delivery through the existing notification service | Channel retry policy already lives there (R-7); no second retry stack |

## 7. Risks

Notification-service latency spikes eat into the 60-second budget (R-5) —
the delivery log's timestamps give the measurement; the sprint metric in
spec §3 watches it.

## 8. Constitution check

Honors the repo constitution: contracts documented in profile shape, no new
gates invented, no secrets in spec content, audit on every state
transition.

## 9. Phase plan

| Phase | Delivers | Satisfies |
| ----- | -------- | --------- |
| 1     | Alert registration API | R-1, R-2, R-3, R-4 |
| 2     | Event consumption and delivery | R-5, R-6, R-7, R-8 |

---

**Approval protocol:** the approver reviews, then replaces the Status line
at the top with `Status: APPROVED — <name>, <date>` in their own change.
The Task List is drafted only after that.
