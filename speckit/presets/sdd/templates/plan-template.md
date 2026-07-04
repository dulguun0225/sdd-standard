# Design — [FEATURE NAME]

**Status: DRAFT**
<!-- The gate is passed only when a HUMAN approver replaces the line above
     with `Status: APPROVED — <name>, <date>` in their own change.
     AI agents shall not write or modify Status lines (SDD-STANDARD §3.2). -->

| Field        | Value                                                  |
| ------------ | ------------------------------------------------------ |
| Feature      | `[###-feature-name]`                                    |
| Authored     | [DATE]                                                  |
| Requirements | [spec.md](spec.md) — approved [date]                    |
| Approver     | Design gate: [technical authority — tech lead/architect] |

This is the **Design Document**: how the approved requirements get built.
Design elements cite the requirements they satisfy as `[R-n]`. The two
contract sections follow the repo's stack profile — the profile provides the
table shape and vocabulary; deviations carry a stated reason.

---

## 1. Summary

[The technical approach in one paragraph: what gets built, on what, and the
one or two decisions that shape everything else.]

## 2. Architecture overview

[Components and their relationships — a small diagram or tight prose. Name
what already exists vs. what this feature adds.]

## 3. Synchronous contracts

<!-- Profile slot. Table shape per the repo's stack profile (default:
     backend-services profile §2 — operation, method & path, auth, request,
     responses, errors with stable codes, idempotency).
     Delete this section only if the feature exposes no synchronous
     operations — deletion is a review question. -->

| Operation | Method & path | Auth | Request | Responses | Errors | Idempotency |
| --------- | ------------- | ---- | ------- | --------- | ------ | ----------- |
|           |               |      |         |           |        |             |

## 4. Asynchronous contracts

<!-- Profile slot. Table shape per the repo's stack profile (default:
     backend-services profile §3 — event, subject/topic, schema, producer,
     delivery semantics, consumers).
     Delete this section only if the feature produces and consumes no
     messages — deletion is a review question. -->

| Event | Subject/topic | Schema | Producer | Delivery | Consumers |
| ----- | ------------- | ------ | -------- | -------- | --------- |
|       |               |        |          |          |           |

## 5. Data and storage

[Entities, ownership, retention. Delete if the feature touches no data.]

## 6. Design decisions

| ID | Decision | Rationale |
| -- | -------- | --------- |
| D1 | [decision taken] | [why, and what was rejected] |

## 7. Risks

[What could invalidate this design, and what watches for it.]

## 8. Constitution check

[Confirm the design honors the repo constitution
(`.specify/memory/constitution.md`); justify any tension explicitly.]

## 9. Phase plan

| Phase | Delivers | Satisfies |
| ----- | -------- | --------- |
| 1     | [increment] | [R-n, R-m] |

[Becomes tasks.md at the tasks gate — each phase turns into tasks carrying
these `[R-n]` references.]

---

**Approval protocol:** the approver reviews, then replaces the Status line at
the top with `Status: APPROVED — <name>, <date>` in their own change. The
Task List is drafted only after that.
