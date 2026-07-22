# Tasks — transfer-limit-alerts

| Field        | Value                                    |
| ------------ | ---------------------------------------- |
| Feature      | `007-transfer-limit-alerts`               |
| Authored     | 2026-07-02                                |
| Requirements | [spec.md](spec.md)                        |
| Design       | [plan.md](plan.md)                        |

This is the **Task List** of the teaching example. Every task carries at
least one `[R-n]`; T-ids are stable; a task is done when its evidence
exists. Phases come from plan.md §9.

## Phase 1 — alert registration API

- [x] **T-1** Create the `alerts` table migration and repository
  (id, account_id, threshold, channel, state). [R-1]
  *Evidence: migration applied in CI; repository round-trip test green.*
- [x] **T-2** Implement `POST /transfer-limit-alerts`: entitlement check,
  currency-aware threshold validation, natural-key conflict handling.
  Depends: T-1. [R-1] [R-2] [R-3] [R-4]
  *Evidence: contract tests cover 201/400/404/409 per plan.md §3.*
- [x] **T-3** Implement `GET /transfer-limit-alerts?account_id=`.
  Depends: T-1. [R-1]
  *Evidence: contract test green.*

## Phase 2 — event consumption and delivery

- [x] **T-4** Consume `payments.transfer.limit-exceeded`: match active
  alerts, unique-index dedup on `event_id` in `delivery_log`.
  Depends: T-1. [R-5] [R-6]
  *Evidence: at-least-once replay test delivers exactly once.*
- [x] **T-5** Deliver through notification-service with per-channel retry;
  record every attempt in `delivery_log`; publish
  `alerts.notification.delivered`. Depends: T-4. [R-5] [R-7] [R-8]
  *Evidence: delivery within 60 s in the integration run; failed-attempt
  rows visible.*
- [x] **T-6** Audit every alert state transition (created, triggered,
  delivered, failed). Depends: T-2, T-5. [R-8]
  *Evidence: audit entries asserted in the integration run.*

---

**Order (SDD-STANDARD §3.1):** implementation starts only after this list
exists; the review phase follows implementation, and its findings are
resolved before the item is marked done (§3.2) — see
[review-notes.md](review-notes.md) beside this file.
