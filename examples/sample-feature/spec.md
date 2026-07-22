# Requirements — transfer-limit-alerts

| Field    | Value                                                        |
| -------- | ------------------------------------------------------------ |
| Feature  | `007-transfer-limit-alerts` (shown here as `examples/sample-feature`) |
| Authored | 2026-07-02                                                    |
| Input    | User description: "alert clients when a transfer is rejected by their daily limit, so they can raise it before the payroll run fails" |

This is the **Requirements Document** of the convention's teaching example —
a complete spec the shape a real qualifying work item produces.
`ci/check_spec_structure.py --self` checks it on every push, so CI keeps it
current. Everything about the feature is fictitious.

## 1. Purpose and scope

Clients whose transfers are rejected by the daily-limit check today find out
from support tickets. This feature lets a client register an alert on an
account and get notified when a transfer is rejected for exceeding the limit, so they can
act before the next payroll run fails. Out of scope: changing limits,
approving limit-raise requests, and any channel beyond the two the
notification service already offers (sms, email).

## 2. Requirements

- **R-1** WHEN a client submits a create-alert request with an account id,
  a threshold amount, and a notification channel, the alerts service shall
  persist the alert and return `201` with the new alert's id.
- **R-2** IF the threshold amount is not a positive amount in the account's
  currency, THEN the alerts service shall reject the request with `400
  VALIDATION_FAILED`.
- **R-3** IF an alert with the same account id, threshold, and channel
  already exists, THEN the alerts service shall reject the request with
  `409 ALERT_EXISTS`.
- **R-4** IF the account does not exist or the caller is not entitled to
  it, THEN the alerts service shall reject the request with `404
  ACCOUNT_NOT_FOUND`.
- **R-5** WHEN the alerts service consumes a `transfer-limit-exceeded`
  event for an account with an active matching alert, the alerts service
  shall deliver a notification on the configured channel within 60 seconds.
- **R-6** The alerts service shall process `transfer-limit-exceeded` events
  idempotently by `event_id` — at-least-once delivery shall never produce a
  duplicate notification.
- **R-7** IF a notification delivery attempt fails, THEN the alerts service
  shall retry per the channel's retry policy and record every attempt in
  the delivery log.
- **R-8** The alerts service shall record every alert state transition
  (created, triggered, delivered, failed) in the audit log.

## 3. Success criteria

- Create-alert p95 latency ≤ 300 ms at the alerts service boundary.
- 99% of notifications delivered within 60 seconds of the triggering event
  (R-5), measured over a rolling two-week window.
- Zero duplicate notifications in the at-least-once replay test (R-6),
  which redelivers a day's events against a copy of production state.

## 4. Traceability

`tasks.md` references these requirements as `[R-n]`. A change that alters
behavior covered by this document updates it in the same PR/MR.

---

**Order (SDD-STANDARD §3.1):** the Design Document ([plan.md](plan.md)) is
drafted only after this document exists — requirements first, design
second.
