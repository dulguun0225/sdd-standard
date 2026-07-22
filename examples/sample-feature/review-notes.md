# Review notes — transfer-limit-alerts

Prepared by: the team's coding agent, 2026-07-08.
Every finding below is resolved before the item is marked done
(SDD-STANDARD §3.2): fix, same-PR amendment, or an explicit acceptance
with a reason recorded here.

This is the review phase's output of the teaching example — what
`speckit.sdd.review` writes into the feature folder after implementation
completes. Everything about the feature is fictitious, and this folder
stays frozen at R-1…R-8 — the amendments the guides tell on top of it
(R-9 and later) live in `docs/` only.

## Artifact check

| Artifact | Present |
| -------- | ------- |
| spec.md  | yes — authored 2026-07-02, before plan.md |
| plan.md  | yes — authored before tasks.md |
| tasks.md | yes — the branch's first implementation commit postdates it |

The artifact order held (§3.1): requirements, design, tasks, then
implementation.

## Requirements coverage

| R-id | Verdict | Evidence |
| ---- | ------- | -------- |
| R-1 | implemented | `POST /transfer-limit-alerts` persists the alert and returns `201` with the id; contract test `create-alert-201` (T-2 evidence run) |
| R-2 | implemented | non-positive and wrong-currency thresholds rejected with `400 VALIDATION_FAILED`; contract test `create-alert-400` |
| R-3 | implemented | natural-key duplicate rejected with `409 ALERT_EXISTS`, backed by the unique constraint; contract test `create-alert-409` |
| R-4 | implemented | missing and not-entitled accounts both answer `404 ACCOUNT_NOT_FOUND` — existence-safe; contract tests `create-alert-404`, `list-alerts-404` |
| R-5 | implemented | consume→deliver path holds the 60-second budget — slowest delivery 41 s in the integration run (T-5 evidence); the rolling two-week criterion (spec §3) starts measuring at release |
| R-6 | implemented | unique index on `delivery_log.event_id`; the at-least-once replay test delivers exactly once (T-4 evidence) |
| R-7 | implemented | failed attempts retried per channel policy through notification-service; every attempt recorded — failed-attempt rows asserted (T-5 evidence) |
| R-8 | implemented | audit entries for created, triggered, delivered, failed asserted in the integration run (T-6 evidence) |

## Contract check

Synchronous (plan.md §3): both declared operations implemented as
declared — methods, paths, `alerts:write`/`alerts:read`, success
statuses, and all error codes match. Nothing implemented but
undeclared: the API surface is exactly the two rows.

Asynchronous (plan.md §4): `payments.transfer.limit-exceeded` consumed
from the declared subject; `alerts.notification.delivered` produced on
the declared subject. Both payloads validate against the schema files
in `contracts/` (asserted in the integration run).

### Silence-conformance (profile defaults)

| Silent dimension | Verdict |
| ---------------- | ------- |
| List operation, no page statement (plan.md §3) | default honored — cursor pagination, `limit` default 50 cap 200, response `{items, next_cursor}` |
| Poison message, no dead-letter statement (plan.md §4) | default honored — schema-invalid events parked on the dead-letter subject with their error |
| Produced event vs. state change, no atomicity statement (plan.md §4) | default honored — publish goes through a transactional outbox; the mechanism is unstated in the plan, flagged under open questions |
| Ordering, unstated | default honored — the consumer assumes none; matching is per event |
| Update concurrency | not applicable — this feature has no update operation |

### Idempotency cells left empty

None. The one mutating operation states its natural key
`(account_id, threshold, channel)`.

## Task evidence

| T-id | Ticked | Evidence spot-check |
| ---- | ------ | ------------------- |
| T-1 | yes | migration applied in CI run `alerts-service#412`; repository round-trip test green in the same run |
| T-2 | yes | contract tests cover 201/400/404/409 per plan.md §3 — run `alerts-service#415` |
| T-3 | yes | list contract test green — run `alerts-service#415` |
| T-4 | yes | at-least-once replay test delivers exactly once — run `alerts-service#418` |
| T-5 | yes | delivery within 60 s in the integration run; failed-attempt rows visible — run `alerts-service#418` |
| T-6 | yes | audit entries asserted in the integration run — run `alerts-service#418` |

Every task carries `[R-n]`; no incomplete tasks remain.

## Spec-drift findings

None. The delta is confined to alerts-service and implements R-1…R-8;
nothing in it changes behavior a spec covers without that
spec. The empty section is a checked result, not an unchecked one: the
diff was read file by file against spec.md and plan.md.

## Open questions

1. plan.md §4 does not state the atomic-publish mechanism for
   `alert-notification-delivered`; the code uses a transactional outbox,
   which is the profile default. Behavior conforms — accepted with this
   note; state the mechanism in the plan at its next amendment, so the
   table says what the code does.
