# Tasks — transfer-limit-alerts

**Status: APPROVED — Tulga (tech lead), 2026-07-05**

> **Amendment 2026-07-20 (pending re-approval):** the Requirements and
> Design cross-reference dates below are corrected to 2026-07-05 to match
> the `spec.md` and `plan.md` approvals. Re-approve to clear this note.

| Field        | Value                                    |
| ------------ | ---------------------------------------- |
| Feature      | `007-transfer-limit-alerts`               |
| Authored     | 2026-07-02                                |
| Requirements | [spec.md](spec.md) — approved 2026-07-05  |
| Design       | [plan.md](plan.md) — approved 2026-07-05  |
| Approver     | Tasks gate: alerts-service technical authority |

This is the **Task List** of the teaching example. Every task carries at
least one `[R-n]`; T-ids are stable; a task is done when its evidence
exists. Phases come from plan.md §9.

## Phase 1 — alert registration API

- [ ] **T-1** Create the `alerts` table migration and repository
  (id, account_id, threshold, channel, state). [R-1]
  *Evidence: migration applied in CI; repository round-trip test green.*
- [ ] **T-2** Implement `POST /transfer-limit-alerts`: entitlement check,
  currency-aware threshold validation, natural-key conflict handling.
  Depends: T-1. [R-1] [R-2] [R-3] [R-4]
  *Evidence: contract tests cover 201/400/404/409 per plan.md §3.*
- [ ] **T-3** Implement `GET /transfer-limit-alerts?account_id=`.
  Depends: T-1. [R-1]
  *Evidence: contract test green.*

## Phase 2 — event consumption and delivery

- [ ] **T-4** Consume `payments.transfer.limit-exceeded`: match active
  alerts, unique-index dedup on `event_id` in `delivery_log`.
  Depends: T-1. [R-5] [R-6]
  *Evidence: at-least-once replay test delivers exactly once.*
- [ ] **T-5** Deliver through notification-service with per-channel retry;
  record every attempt in `delivery_log`; publish
  `alerts.notification.delivered`. Depends: T-4. [R-5] [R-7] [R-8]
  *Evidence: delivery within 60 s in the integration run; failed-attempt
  rows visible.*
- [ ] **T-6** Audit every alert state transition (created, triggered,
  delivered, failed). Depends: T-2, T-5. [R-8]
  *Evidence: audit entries asserted in the integration run.*

---

**Approval protocol:** the approver reviews, then replaces the Status line
at the top with `Status: APPROVED — <name>, <date>` in their own change.
Implementation starts only after that; the review phase follows
implementation before the item is marked done.
