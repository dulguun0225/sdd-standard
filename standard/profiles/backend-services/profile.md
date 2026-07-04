# Profile: backend-services

| Field | Value |
| ----- | ----- |
| Profile version | `0.1.0-draft` |
| Requires | `SDD-STANDARD >= 0.1` |
| Owning team | TBD — named when adoption creates one; CODEOWNERS entry added then |
| Outside reviewer | Every change needs ≥ 1 reviewer from outside the owning team (SDD-STANDARD §7.4) |
| Stack family | Backend microservices: synchronous APIs and asynchronous messaging |

> **Authority banner — do not remove.** Per SDD-STANDARD §7: this profile
> provides **defaults, vocabulary, and worked examples only**. It shall not
> add gates, approval steps, artifact types, or workflow steps, and shall
> not override the standard. If something here appears to conflict with
> SDD-STANDARD.md, the standard wins and this profile gets fixed.

## 1. Scope

Applies to backend service repos adopting this standard — services exposing synchronous
APIs (HTTP/RPC) and/or exchanging asynchronous messages. It binds the Design
Document's two contract sections to a common shape so reviewers read every
service's design the same way. It deliberately does not name technologies
(broker, framework, serialization) — those are repo decisions; only the
*documentation shape* is standardized here.

## 2. Synchronous contract defaults

The Design Document's **Synchronous contracts** section is a table, one row
per operation:

| Column | Content |
| ------ | ------- |
| Operation | Short verb-noun name (`create-transfer`) |
| Method & path | `POST /transfers` (or RPC method name) |
| Auth | Required principal/scope, or `none` with a reason |
| Request | Body/params summary, link to schema if one exists |
| Responses | Success statuses with body summaries |
| Errors | Every business error as a **stable error code** (`LIMIT_EXCEEDED`), with its status |
| Idempotency | Stated for every mutating operation (key, natural, or `not idempotent` + why that is safe) |

Defaults: error codes are SCREAMING_SNAKE_CASE and never renumbered/reused
(same discipline as R-ids); a mutating operation with an empty Idempotency
cell is a review question, not a formatting choice.

## 3. Asynchronous contract defaults

The **Asynchronous contracts** section is a table, one row per message:

| Column | Content |
| ------ | ------- |
| Event | Past-tense name (`transfer-limit-exceeded`) |
| Subject/topic | Default naming: `<domain>.<entity>.<event>` (e.g. `payments.transfer.limit-exceeded`) |
| Schema | Link/path to the schema; default location is `contracts/` inside the feature's spec folder, or the team's schema-registry reference |
| Producer | Owning service |
| Delivery | Semantics as consumed: default assumption is **at-least-once → consumers de-duplicate**; anything else stated explicitly |
| Consumers | Known consumers at design time, or `open` |

Defaults: an event is a fact, not a command — commands go through the sync
section; a message row without stated delivery semantics is a review
question.

## 4. Worked examples

Synchronous:

| Operation | Method & path | Auth | Request | Responses | Errors | Idempotency |
| --------- | ------------- | ---- | ------- | --------- | ------ | ----------- |
| create-transfer-limit-alert | `POST /transfer-limit-alerts` | `alerts:write` | `{account_id, threshold, channel}` | `201` created alert | `400 VALIDATION_FAILED`, `404 ACCOUNT_NOT_FOUND`, `409 ALERT_EXISTS` | Idempotency key: `(account_id, threshold, channel)` |

Asynchronous:

| Event | Subject/topic | Schema | Producer | Delivery | Consumers |
| ----- | ------------- | ------ | -------- | -------- | --------- |
| transfer-limit-exceeded | `payments.transfer.limit-exceeded` | `contracts/transfer-limit-exceeded.schema.json` | transfer-service | at-least-once; consumers de-duplicate on `event_id` | alerts-service, `open` |

## 5. Profile changelog

| Version | Date | Change |
| ------- | ---- | ------ |
| 0.1.0-draft | 2026-07-02 | Initial thin version |
