# Writing the design — the author's guide

**Informative.** This guide teaches the craft. The rules live in
[SDD-STANDARD.md](../standard/SDD-STANDARD.md) and the table shapes in
your repo's stack profile (`.specify/memory/profile.md`). In any
conflict, they win.

You are the author when you draft a Design Document, after the
Requirements Document exists (§3.1). On most teams that is a developer
working with an agent. [reviewing-specs.md](reviewing-specs.md) turns
the same craft into a critique checklist — for an agent, a teammate, or
your own second pass. A Design Document has two readers who cannot ask
you questions: whoever reviews it next, and the implementer —
increasingly an AI agent. The implementer will take every cell literally
and fill every gap with *something*. Write for both.

## The raw material

`/speckit.plan` drafts `plan.md` from the requirements. The
architecture prose is usually serviceable. The contract tables are
where drafts fail, because they fail quietly. A realistic draft row for
the teaching example:

> | Operation | Method & path | Auth | Request | Responses | Errors | Idempotency |
> | --------- | ------------- | ---- | ------- | --------- | ------ | ----------- |
> | create alert | `POST /alerts` | | alert JSON | `200 OK` | `400` on bad input | |

and a consumed event:

> | Event | Subject/topic | Schema | Producer | Delivery | Consumers |
> | ----- | ------------- | ------ | -------- | -------- | --------- |
> | limit exceeded | transfers | (schema in the registry) | | | |

Nothing here is *wrong* yet. It is vague, which is worse. A vague row
does not fail the build. It becomes somebody else's silent guess. The
shaping pass turns these into the
[sample plan](../examples/sample-feature/plan.md). The profile's §5
worked examples show the same shapes on a create, an update, and a
list.

## The shaping moves

**1. Fill each row like its caller.** "Alert JSON" is not a request; a
caller cannot code against it. Name the fields:
`{account_id, threshold, channel}`. Link the schema where one exists. A
create returns `201` with the new resource's id, not `200 OK`. Every
success status appears with its body summary. The test for a finished
row: could someone implement the *client* from the row alone?

**2. Every business error is a stable code.** "`400` on bad input"
names no cause a caller can act on. One SCREAMING_SNAKE_CASE code per
actionable cause, never renumbered or reused — the R-id discipline
applied to errors: `400 VALIDATION_FAILED`, `404 ACCOUNT_NOT_FOUND`,
`409 ALERT_EXISTS`. The codes are not made up while filling the table.
They come from the spec's IF/THEN rows, and each cites its requirement:
`[R-2]`, `[R-4]`, `[R-3]`. Note the profile's existence-safe default:
not-entitled reads the same as "does not exist". That is why the
not-entitled case is `404`, not `403`.

**3. An empty cell is a statement — make it on purpose.** Under the
profile's stated-or-default rule (profile §1), every cell you leave
empty *means* the profile default. The reviewer reads it that way. So
does the implementer. The draft's empty Delivery cell therefore says:
at-least-once, durable de-duplication on `event_id`, no ordering,
poison messages dead-lettered. Leave it empty only when that is your
design. And the design still has to make the default real: the dedup
lands in §5 Data and storage (a unique index), and later in a task.
One cell must never be empty: **Idempotency on a mutating operation**.
It has no safe default (profile §2). The draft's blank cell becomes:
natural key `(account_id, threshold, channel)`; a retry returns the
first outcome.

**4. Name what the default cannot know.** An empty Auth cell reads as
"authenticated, with a named permission" — but no default can supply
the name. Write it: `alerts:write`. Same for the event row. The subject
follows the naming default: `payments.transfer.limit-exceeded`. The
event name is a past-tense fact: `transfer-limit-exceeded`, not "limit
exceeded". The producer is a named service.

**5. Schema links must resolve.** "(Schema in the registry)" is a
link that resolves to nothing. Local schemas live at `contracts/` inside the
feature folder. The structure check verifies every local `contracts/…`
path the plan references. Agents are known to invent schema links; that
is why the check exists. Registry references and URLs are fine too —
they just have to be real.

**6. Cite `[R-n]` in both directions.** Every design element cites the
requirement it satisfies. Then check the list the other way. An R-id no
element satisfies is a gap in the design. A reader does this check in two
minutes ([reviewing-specs.md](reviewing-specs.md)). Do it first.

**7. Decisions carry the rejected alternative.** "D1: dedup by unique
index" is a preference until it names what was rejected and why. The
sample's D1 does both: the decision line rejects an in-memory cache, and
the rationale says why the index wins — it survives restarts and
scale-out. Decisions with alternatives survive re-reading months later.
Preferences get argued again.

**8. Be honest in the constitution check; make the phase plan drive the
tasks.** Name the tension with the repo constitution if one exists. An
automatic "no conflicts" makes the section useless. Write §9 so each
phase delivers a working increment covering named R-ids. The Task List
is built from it, phase by phase.

One more rule, carried over from the spec: pin only what others depend
on. A design that pins module layout it did not need to pin will need
amendments later
([evolving-requirements.md](evolving-requirements.md)).

The whole pass, in one table:

| Draft cell | Defect | Shaped into |
| ---------- | ------ | ----------- |
| Request "alert JSON" | caller cannot code against it | named fields, schema link |
| Responses "`200 OK`" | wrong status, no body | `201` created alert |
| Errors "`400` on bad input" | no stable code, no cause, no `[R-n]` | `400 VALIDATION_FAILED` [R-2], `404 ACCOUNT_NOT_FOUND` [R-4], `409 ALERT_EXISTS` [R-3] |
| Auth *(empty)* | the default cannot name the permission | `alerts:write` |
| Idempotency *(empty)* on a mutating row | the one cell with no safe default | natural key `(account_id, threshold, channel)` |
| Delivery *(empty)* | fine **only** if the profile default is the design — then make it real in §5 and a task | stated: at-least-once, dedup on `event_id` [R-6] |
| Schema "(in the registry)" | points at nothing | `contracts/transfer-limit-exceeded.schema.json` — a file that exists |

## The pre-implementation checklist

The author's pass over the reader's checklist
([reviewing-specs.md](reviewing-specs.md) is the same list from the
critic's side):

- every row is readable from the caller's perspective — statuses, field
  names, stable error codes;
- every mutating row's Idempotency cell is filled;
- every silent cell is deliberate: you mean the profile default, and
  the design makes it real;
- every local `contracts/…` path resolves — run the structure check
  (quickstart §6 has the command);
- `[R-n]` coverage checked in both directions;
- every decision names its rejected alternative; every risk names what
  mitigates or monitors it;
- the constitution check is honest; the phase plan's phases cover all
  R-ids between them.

A reader asks about the empty cells before implementation. Cheaper to answer them now than during an outage.

## The author's turn, step by step

The moves above, placed on the walkthrough's timeline.
[feature-walkthrough.md](feature-walkthrough.md) compresses this phase
into one Day 3 row; this table replays it step by step from the
author's chair. The people are the walkthrough's;
everything is fictitious. Each row is one step. The six fields — when,
who, what, where, how, why — are the columns.

| When | Who | What | Where | How | Why |
| ---- | --- | ---- | ----- | --- | --- |
| **Day 3**, after the spec PR merges | **Bilguun** (developer, the author) + agent | The raw material: a drafted `plan.md` — serviceable architecture prose, and the vague contract rows this guide opened with | A new PR touching `plan.md`, on the same feature branch | `/speckit.plan` | The order is binding (§3.1): a `plan.md` pushed with no `spec.md` beside it is a red build on every push (§8.1). That is why this step waits for the spec PR to merge |
| **Day 3** | **Bilguun** + agent | The synchronous row, filled like its caller: Request `{account_id, threshold, channel}`; Responses `201` created alert; Errors from the spec's IF/THEN rows as stable codes — `400 VALIDATION_FAILED` [R-2], `404 ACCOUNT_NOT_FOUND` [R-4], `409 ALERT_EXISTS` [R-3]; Auth `alerts:write`; Idempotency natural key `(account_id, threshold, channel)` | `plan.md` §3 | Moves 1–4 | Neither reader can ask questions. The finished-row test: the client could be implemented from the row alone |
| **Day 3** | **Bilguun** + agent | The asynchronous row: event `transfer-limit-exceeded`, subject `payments.transfer.limit-exceeded`, producer transfer-service; Delivery states the profile default — at-least-once, de-duplicate on `event_id` [R-6] — and §5 makes it real: consumed `event_id`s unique-indexed in `delivery_log` | `plan.md` §4 and §5; the schema file created at `contracts/transfer-limit-exceeded.schema.json` | Moves 3–5; the structure check verifies the `contracts/` path resolves | An empty Delivery cell would assert the same default (profile §1); either way the design has to make it real — the unique index IS the R-6 dedup |
| **Day 3** | **Bilguun** + agent | Coverage and decisions: every element cites `[R-n]`; the reverse pass finds each of R-1…R-8 satisfied somewhere; D1 written with its rejected alternative — dedup by unique index, not an in-memory cache, because the index survives restarts and scale-out | `plan.md` §6; the checklist above, as the author's pass | Moves 6–7 | An R-id no element satisfies is a gap found now, not by a reader later; a decision without a rejected alternative gets argued again |
| **Day 3** | **Tulga** (tech lead) reads the PR | `[R-n]` coverage checked both ways (two minutes), the empty-cell questions asked, a push for D1's rejected alternative — the PR merges once they have answers in the document | The same PR — the team's own review practice, outside the standard's scope (§1) | [reviewing-specs.md](reviewing-specs.md) is the reader's side | A reader asking about an empty cell now is cheaper than the review phase flagging it later — and far cheaper than an outage. Only with `plan.md` merged may `tasks.md` be drafted (§3.1) — [writing-tasks.md](writing-tasks.md) continues from here |
