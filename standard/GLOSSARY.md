# Glossary

**Reference material — informative.** This document defines terms and shows
EARS patterns; it never adds rules. If anything here appears to conflict with
SDD-STANDARD.md or a profile, the standard wins and this file gets fixed.

> **Монгол орчуулгын тухай / About the Mongolian column:** орчуулгыг
> AI ноороглож, эх хэлтэй хянагч 2026-07-05-нд хянасан.
> The Mongolian translations were machine-drafted and native-reviewed on
> 2026-07-05. Improvements land by PR like any other change.

---

## 1. EARS requirement patterns

EARS (Easy Approach to Requirements Syntax) phrases every requirement in one
of five patterns. The keywords (`WHEN`, `WHILE`, `IF … THEN`, `WHERE`,
`shall`) always stay in English — specs are authored in English; this table
explains each pattern's meaning in both languages.

| Pattern | Template | Example |
| ------- | -------- | ------- |
| **Ubiquitous** — always true, no trigger. *Үргэлж биелэх шаардлага.* | The `<system>` shall `<response>`. | The payment service shall record every state transition of a payment in the audit log. |
| **Event-driven** — fires on a trigger. *Тодорхой үйл явдлаар өдөөгдөх шаардлага.* | WHEN `<trigger>`, the `<system>` shall `<response>`. | WHEN a transfer request exceeds the client's daily limit, the transfer service shall reject it with error code `LIMIT_EXCEEDED`. |
| **State-driven** — holds while a state persists. *Тодорхой төлөв үргэлжлэх хугацаанд биелэх шаардлага.* | WHILE `<state>`, the `<system>` shall `<response>`. | WHILE the market-data feed is disconnected, the pricing service shall serve the last received quote marked as stale. |
| **Unwanted behavior** — response to a condition that should not happen. *Хүсээгүй нөхцөлд үзүүлэх хариу үйлдэл.* | IF `<undesired condition>`, THEN the `<system>` shall `<response>`. | IF a consumed message fails schema validation, THEN the consumer shall route it to the dead-letter subject without acknowledging success. |
| **Optional feature** — applies only where a feature exists. *Тухайн боломж идэвхтэй үед л хамаарах шаардлага.* | WHERE `<feature is included>`, the `<system>` shall `<response>`. | WHERE a deployment enables two-factor authentication, the login service shall require a second factor for every session. |

Patterns combine when needed — the **Complex** pattern (e.g. `WHILE
<state>, WHEN <trigger>, the <system> shall <response>`); a requirement
still expresses **one** testable behavior. Where an EARS sentence would
distort a requirement's meaning (mathematical content, more than three
preconditions), SDD-STANDARD §4.1 permits a structured list or table under
the same R-id instead, with a one-line rationale. The `<system>` slot names
whoever is bound — a service, a team, a CI pipeline, a reviewer, a
document, a PR, a tracker item.

## 2. Artifact vocabulary

The standard names the *documents*; GitHub Spec Kit (pinned in
`speckit/PINNED-VERSION`) names the *files*. Decided 2026-07-02: stock
filenames, the standard's vocabulary inside the documents.

| Standard term | File on disk | Contains |
| ------------- | ------------ | -------- |
| Requirements Document | `spec.md` | EARS requirements with stable R-ids; acceptance criteria |
| Design Document | `plan.md` | Architecture and contracts: sync API endpoints and/or async message subjects & schemas (profile fills stack specifics) |
| Task List | `tasks.md` | Implementation tasks, each carrying `[R-n]` references |
| Constitution | `.specify/memory/constitution.md` | The repo's non-negotiable principles, seeded from the shared constitution template |

## 3. Terms

### SDD core

| Term (EN) | Definition | Монгол (ноорог) |
| --------- | ---------- | ---------------- |
| Spec-driven development (SDD) | Working method where an approved specification precedes and governs implementation | Тодорхойлолтод суурилсан хөгжүүлэлт |
| Specification (spec) | The set of artifacts (requirements, design, tasks) governing one feature | Техникийн тодорхойлолт (спек) |
| Requirement | A single testable statement of expected behavior, phrased in EARS | Шаардлага |
| R-id | A requirement's stable identifier (`R-7`); never renumbered, never reused — withdrawn requirements stay listed as WITHDRAWN | Шаардлагын тогтмол дугаар |
| Traceability | The property that every task and change links back to a requirement (`[R-n]`) | Мөшгих боломж |
| Gate | A human approval checkpoint on an artifact; passed only via an explicit Status line | Шалгах цэг (гейт) |
| Approval | A human adding `Status: APPROVED — <name>, <date>` to an artifact; agents never write it | Баталгаажуулалт |
| Spec drift | A merged change altering behavior covered by an approved spec without updating that spec in the same PR/MR | Тодорхойлолтын зөрүү |
| Qualifying triggers | The §6.1 list of change properties (externally observable behavior or contract, boundary-crossing, hard-to-reverse step, new capability) that require spec ceremony; items matching none are exempt (the pressure valve) | Болзол хангах шалгуурууд |
| Qualifying work item | A work item matching at least one §6.1 trigger — full gated workflow applies | Болзол хангасан ажил |
| Emergency hotfix | A change shipped outside the normal spec workflow to restore service; implemented first, spec updated after | Яаралтай засвар |

### Governance & tooling

| Term (EN) | Definition | Монгол (ноорог) |
| --------- | ---------- | ---------------- |
| Standard owner | The named **role** (not person) that approves normative changes, pin-forwards, and new profiles (SDD-STANDARD §13) | Стандарт эзэмшигч (үүрэг) |
| Normative | Binding language (shall/MUST, gates) — lives only in SDD-STANDARD.md and profiles | Заавал мөрдөх |
| Informative | Explains and demonstrates, never legislates — everything in `docs/` | Танилцуулах, мэдээллийн |
| Stack profile | A subordinate document binding the standard's abstract slots to one stack; defaults and vocabulary only — never gates, approvals, or artifact types | Технологийн профайл |
| Version pin | The single pinned Spec Kit version (`speckit/PINNED-VERSION`); upgrades are tested in this repo first | Бэхэлсэн хувилбар |
| Preset | Spec Kit's supported mechanism for layering the standard's templates and terminology over stock behavior | Пресет (урьдчилсан багц) |
| Extension | Spec Kit's supported mechanism for adding commands and workflow hooks (e.g. the review phase) | Өргөтгөл |
| Constitution | The non-negotiable principles a repo's specs must respect | Үндсэн дүрэм |
