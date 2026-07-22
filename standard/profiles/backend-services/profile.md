# Profile: backend-services

| Field | Value |
| ----- | ----- |
| Profile version | `0.2.1-draft` |
| Requires | `SDD-STANDARD >= 0.1` |
| Owning team | TBD — named when adoption creates one; CODEOWNERS entry added then |
| Outside reviewer | Every change needs ≥ 1 reviewer from outside the owning team (SDD-STANDARD §7.4) |
| Stack family | Backend services — synchronous APIs and asynchronous messaging, in any deployment shape (separate services or modules of one deployable) |

> **Authority banner — do not remove.** Per SDD-STANDARD §7: this profile
> provides **defaults, vocabulary, and worked examples only**. It shall not
> add gates, approval steps, artifact types, or workflow steps, and shall
> not override the standard. If something here appears to conflict with
> SDD-STANDARD.md, the standard takes precedence and this profile gets fixed.

## 1. Scope

Applies to backend service repos adopting this standard — code exposing
synchronous APIs (HTTP/RPC) and/or exchanging asynchronous messages,
whether deployed as separate services or as modules of one deployable. It
binds the Design Document's two contract sections to a common shape so
every reader reads every design the same way. It deliberately does not name
technologies (broker, framework, serialization) — those are repo
decisions; only the *documentation shape* is standardized here.

**The reading rule.** A contract table has two consumers: the reviewing
reader — the review phase, or a human reading the PR — and the
implementer, increasingly an AI agent. The documented
failure mode of AI implementers is not syntax; it is quietly filling each
unstated detail with the most common pattern in their training data,
without flagging the gap. This profile therefore gives every contract
dimension a **stated-or-default** reading: what the Design Document
states takes precedence; where it is silent, the defaults below are the reading; and
where no safe default can exist (§2, idempotency of a mutating
operation), silence is a named review question. Under this profile,
silence is never the implementer's choice.

## 2. Synchronous contract defaults

The Design Document's **Synchronous contracts** section is a table, one row
per operation:

| Column | Content |
| ------ | ------- |
| Operation | Short verb-noun name (`create-transfer`); one operation per row |
| Method & path | `POST /transfers` (or RPC method name) |
| Auth | The named permission/scope, or `none` with a reason |
| Request | Body/params summary, link to schema if one exists (default location: `contracts/` inside the feature's spec folder); a collection operation names its page parameters |
| Responses | Every success status with body summary; a collection response names its page shape |
| Errors | Every business error as a **stable error code** (`LIMIT_EXCEEDED`), with its status; the §4 failure cases are the ones that commonly apply |
| Idempotency | Stated for every mutating operation: `key: <field>` (client-supplied), natural key (request-content identity), or `not idempotent` + why that is safe |

Column conventions:

- Error codes are SCREAMING_SNAKE_CASE and never renumbered or reused
  (the R-id discipline); one code per cause a caller can act on.
- An idempotent retry returns the first execution's outcome — recording
  that outcome is part of the operation's effect, not an optimization
  (the classic gap: effect committed, outcome not recorded, a retry
  duplicates the effect).
- Wire shapes: timestamps are UTC ISO-8601 and named `*_at`; calendar
  dates are named `*_date`; money and other exact decimals travel as
  strings with an explicit currency or unit — a bare float on a money
  field is a defect, not a style choice.
- Time is numeric: a stated timeout, latency budget, retry count, or
  delivery window carries a number and a unit. "Quickly", "soon", and
  "eventually" are not contract language — they survive even
  well-formed EARS phrasing and leave the implementer to pick the
  number.

How silence reads (the §1 reading rule applied to this table):

- **Empty Auth cell** → the operation requires authentication and a named
  permission; `none` is always written out. Where a caller can be
  authenticated but not entitled to the specific resource, the default
  response is **existence-safe**: indistinguishable from "does not
  exist".
- **Empty Idempotency cell on a mutating operation** → a review question,
  never a formatting choice. There is no safe default; an unstated
  choice here is exactly where an implementer guesses.
- **Collection operation with no page statement** → cursor pagination:
  opaque `cursor` + `limit` (default 50, cap 200), response
  `{items, next_cursor}`. Offset pagination is a stated deviation (it
  skips and repeats items under concurrent writes).
- **Update with no concurrency statement**, where the resource carries a
  version → compare-and-set: stale writes rejected with a stable
  conflict code. Last-write-wins is a stated deviation.
- **Unknown request fields** → rejected with the validation error;
  tolerant reading is a stated deviation.
- **A mutating operation touching more than one store or downstream** →
  all-or-nothing (one atomic step); anything weaker states what holds
  when a part fails (§4, partial failure).

## 3. Asynchronous contract defaults

The **Asynchronous contracts** section is a table, one row per message:

| Column | Content |
| ------ | ------- |
| Event | Past-tense name (`transfer-limit-exceeded`) — an event is a fact; commands go through §2 |
| Subject/topic | Default naming: `<domain>.<entity>.<event>` (e.g. `payments.transfer.limit-exceeded`) |
| Schema | Link/path to the schema; default location is `contracts/` inside the feature's spec folder, or the team's schema-registry reference |
| Producer | Owning service or module |
| Delivery | Semantics as consumed: delivery guarantee, de-duplication key, ordering scope |
| Consumers | Known consumers at design time, or `open` |

Column conventions:

- Every event envelope carries at least `event_id` (the de-duplication
  key), `occurred_at`, and the correlation id of the change that caused
  it.
- Schema changes are additive-compatible by default (new optional fields
  only); a breaking change is a new subject or an explicit version in
  the row.

How silence reads:

- **Unstated delivery** → at-least-once, and consumers de-duplicate on
  `event_id` with **durable** state (survives restart and scale-out —
  a unique index or dedup table, not process memory).
- **Unstated ordering** → none, not even per producer. A consumer that
  needs order states its ordering scope (e.g. per `account_id`) and the
  design says how it is achieved.
- **Message that cannot be processed** (schema-invalid, or retries
  exhausted) → parked on a dead-letter destination together with its
  error, never silently dropped; the row or the repo default names the
  destination.
- **Event produced as the effect of a state change** → publish and state
  change are atomic (the design names the mechanism — e.g. a
  transactional outbox). Publishing "after commit" with no such
  mechanism loses events on a crash and is a stated deviation.

## 4. Contract vocabulary

Names, so every design and review says the same thing the same way.

| Term | Meaning |
| ---- | ------- |
| Idempotent operation | Repeating it with the same input produces the effect once and returns the first outcome |
| Idempotency key | Client-supplied identifier the service stores to recognize a repeat |
| Natural key | Repeat-identity derived from request content, e.g. `(account_id, threshold, channel)` |
| At-least-once | Delivery may repeat a message; processing must tolerate repeats |
| Effectively-once | At-least-once delivery plus durable de-duplication: the *effect* happens once |
| Durable de-duplication | Dedup state that survives restart and scale-out (unique index, dedup table) — not process memory |
| Ordering scope | The key within which a consumer may assume order; default none |
| Dead-letter | Destination where unprocessable messages are parked with their error — never dropped |
| Transactional outbox | Mechanism making "state changed" and "event published" one atomic step |
| Compatible schema change | Additive/optional-only; consumers of the old schema keep working |
| Stable error code | SCREAMING_SNAKE_CASE, never renumbered or reused; one code per actionable cause |
| Compare-and-set | A write valid only against the version the caller read; stale writes rejected |
| Cursor pagination | Pages identified by an opaque cursor; stable under concurrent writes (offset is not) |
| Existence-safe response | Not-entitled and nonexistent are indistinguishable to the caller |

**Standard failure cases.** The corner cases every backend contract
meets; main-path-only designs are where implementers silently omit them.
Which ones apply is the design's call — these are the names to state it
with:

| Failure case | What the design states |
| ------------ | ---------------------- |
| Duplicate request | The Idempotency cell: key, natural key, or why-safe |
| Replayed message | Delivery cell: dedup key and its durability |
| Out-of-order message | Delivery cell: ordering scope, or tolerance of disorder |
| Poison message | Delivery cell or repo default: the dead-letter destination |
| Stale update | Errors cell: the conflict code; the concurrency choice |
| Not-entitled access | Errors cell: existence-safe response, or explicit denial |
| Downstream timeout | The caller's state when it gave up mid-call — did the effect happen? |
| Partial failure | What holds when one of several effects fails (default: all-or-nothing) |
| Oversized or malformed input | The validation error; size bounds stated where they matter |
| Burst | Rate-limit behavior and its error code, where a limit exists |

## 5. Worked examples

Synchronous — a create (natural-key idempotency), an update
(compare-and-set), and a list (cursor pages):

| Operation | Method & path | Auth | Request | Responses | Errors | Idempotency |
| --------- | ------------- | ---- | ------- | --------- | ------ | ----------- |
| create-transfer-limit-alert | `POST /transfer-limit-alerts` | `alerts:write` | `{account_id, threshold, channel}` | `201` created alert | `400 VALIDATION_FAILED`, `404 ACCOUNT_NOT_FOUND` (also not-entitled), `409 ALERT_EXISTS` | Natural key `(account_id, threshold, channel)`; a retry returns the first outcome |
| update-transfer-limit-alert | `PUT /transfer-limit-alerts/{alert_id}` | `alerts:write` | Full alert body + the `version` read | `200` updated alert | `400 VALIDATION_FAILED`, `404 ALERT_NOT_FOUND` (also not-entitled), `409 STALE_VERSION` | Compare-and-set on `version` — a replay is rejected stale, no duplicate effect |
| list-transfer-limit-alerts | `GET /transfer-limit-alerts?account_id=` | `alerts:read` | `account_id`; page: `cursor`, `limit` (50, cap 200) | `200 {items, next_cursor}` | `404 ACCOUNT_NOT_FOUND` | Read — idempotent |

Asynchronous — one consumed and one produced event:

| Event | Subject/topic | Schema | Producer | Delivery | Consumers |
| ----- | ------------- | ------ | -------- | -------- | --------- |
| transfer-limit-exceeded | `payments.transfer.limit-exceeded` | `contracts/transfer-limit-exceeded.schema.json` | transfer-service | at-least-once; durable dedup on `event_id`; unordered; poison → dead-letter | alerts-service, `open` |
| alert-notification-delivered | `alerts.notification.delivered` | `contracts/alert-notification-delivered.schema.json` | alerts-service | at-least-once via transactional outbox; consumers de-duplicate on `delivery_id` | audit pipeline, `open` |

## 6. Profile changelog

| Version | Date | Change |
| ------- | ---- | ------ |
| 0.2.1-draft | 2026-07-22 | Wording only, no defaults changed: the reading rule's "human reviewer" becomes the reviewing reader (review phase or a human reading the PR) — the standard's human approval gates were removed (D-19, convention 0.4.0-draft) |
| 0.2.0-draft | 2026-07-18 | The stated-or-default reading rule (§1); silence defaults for auth, pagination, concurrency, atomicity, delivery, ordering, dead-lettering, and schema evolution; contract vocabulary and the standard failure cases (§4); worked examples extended. Grounds recorded in the convention CHANGELOG entry |
| 0.1.0-draft | 2026-07-02 | Initial thin version |
