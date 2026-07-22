# Writing requirements — the author's guide

**Informative.** This guide teaches the craft. The rules live in
[SDD-STANDARD.md](../standard/SDD-STANDARD.md) §4. In any conflict, the
standard takes precedence.

You are the author when you draft a Requirements Document and shape it
into a spec that design, tasks, and implementation can build on. On most
teams that is a developer working with an agent.
[reviewing-specs.md](reviewing-specs.md) turns the same craft into a
critique checklist — for an agent, a teammate, or your own second pass.
Write so the critique finds nothing.

Every requirement is one EARS sentence. The common shape is
`WHEN <trigger>, the <system> shall <response>`; there are five patterns
in all, and [GLOSSARY §1](../standard/GLOSSARY.md#1-ears-requirement-patterns)
shows each with an example. "Choosing the pattern" below picks between
them.

## The raw material

`/speckit.specify` turns a one-line intent into a drafted `spec.md`.
That draft is raw material, not a spec. Agents fail at requirements in
known ways. They favor the happy path and skip the failure cases. When
they don't know a detail, they write vague filler instead of flagging
the gap. And they pack several behaviors into one sentence.

Here is a realistic draft for the teaching example's intent — "alert
clients when a transfer is rejected by their daily limit". Every one of
those failures is in it:

> - **R-1** The system shall allow clients to create transfer-limit
>   alerts and receive notifications when a transfer exceeds their
>   daily limit.
> - **R-2** The alerts service shall validate create-alert requests and
>   handle invalid input appropriately.
> - **R-3** WHEN a transfer exceeds the daily limit, the system shall
>   notify the client quickly on their preferred channel.
> - **R-4** The system shall be robust against duplicate events.
> - **R-5** The alerts service shall log alert activity.

Five plausible lines. None survives the shaping pass below. The rest of
this guide turns them into the teaching example's
[sample spec](../examples/sample-feature/spec.md).

## The shaping moves

**1. Split what "and" hides.** Draft R-1 holds three behaviors: create
an alert, match an event, deliver a notification. Each needs its own
R-id. Each gets its own test, its own tasks (`[R-n]`), and its own
amendments later (§4.2). The rule is *one testable behavior*, not zero
"and"s. The final R-1 says "persist the alert and return `201`". That
is one behavior seen from two sides: the state change and its response.
One test checks both. "Create alerts and receive notifications" is
different — two separate features in different parts of the system.

**2. Name the system; state a response.** "The system shall allow X"
cannot fail a test. *Allow* is not observable. *The system* names
nobody. Name the bound party in the `<system>` slot (GLOSSARY §1) and
state the observable response. Result: WHEN a client submits a
create-alert request with an account id, a threshold amount, and a
notification channel, **the alerts service** shall **persist the alert
and return `201` with the new alert's id**.

**3. A number and a unit for every judgment word.** "Quickly",
"appropriately", "robust". Each one leaves a decision to whoever
implements, without saying so. A human implementer guesses. An AI
implementer fills the gap with the most common pattern in its training
data — not with your intent. "Quickly" becomes **within 60 seconds**.
The structure check warns on these words. The warning is advisory,
never merge-blocking — treat each hit as a defect anyway, or defend the
word. "Robust against duplicate events" becomes an outcome a test can
check: at-least-once delivery shall **never produce a duplicate
notification**, de-duplicated by `event_id` (final R-6).

**4. Write the trigger the system actually observes.** Draft R-3 fires
"WHEN a transfer exceeds the daily limit". But the alerts service never
sees a transfer. It consumes a `transfer-limit-exceeded` event. If the
system cannot observe the trigger, no test at that system's boundary
can fire it. Rewriting it (final R-5) also surfaces the real contract
question: which event, from which producer? That question belongs in
`plan.md`'s asynchronous contracts table.

**5. Watch undefined terms — they conceal unplanned features.** Draft R-3 says
"preferred channel". That quietly assumes a client preference store
nobody planned to build. The actual design: a channel chosen per alert,
at registration. Define the terms your requirements lean on (the
template's §2 Definitions) or use plain ones. Anything else is
ambiguous, and every reader fills it in differently. A requirement is
only as precise as the definitions it uses.

**6. Write the IF/THEN rows the draft never has.** The draft has zero
unwanted-behavior requirements. Skipping failure cases is the most
common drafting mistake, by humans and agents alike. For every happy
path, ask what arrives malformed, duplicate, missing, unentitled, or
failing. The profile's standard failure cases
(`.specify/memory/profile.md` §4) are the checklist; the
spec-template's comment points there. Ask that question of draft R-1
and R-2 and you get the final spec's R-2 (invalid threshold →
`400 VALIDATION_FAILED`), R-3 (duplicate registration →
`409 ALERT_EXISTS`), R-4 (missing or unentitled account →
`404 ACCOUNT_NOT_FOUND`), and R-7 (delivery failure → retry, every
attempt logged). A spec with only WHEN rows is incomplete.

**7. Vague nouns are as ambiguous as vague adverbs.** "Log alert activity."
Which activity? Into which log? The shaped version names both: every
alert state transition (created, triggered, delivered, failed), in the
audit log (final R-8).

The whole pass, in one table:

| Draft line | Defect | Shaped into |
| ---------- | ------ | ----------- |
| R-1 "allow … and receive …" | hidden "and"; "allow" untestable | R-1, R-5 |
| R-2 "validate … appropriately" | judgment words; failure behavior unstated | R-2 |
| R-3 "quickly … preferred channel" | no number; trigger the system never observes; undefined term hiding a feature | R-5 |
| R-4 "robust against duplicates" | no testable outcome | R-6 |
| R-5 "log alert activity" | vague noun | R-8 |
| *(nothing)* | happy path only — no unwanted-behavior rows | R-3, R-4, R-7 |

## Choosing the pattern

Five questions, one per EARS pattern (templates and worked examples in
[GLOSSARY §1](../standard/GLOSSARY.md#1-ears-requirement-patterns)):

- Always true, with no trigger at all? → **Ubiquitous**.
- Fires at the moment something happens? → **WHEN** (event-driven).
- Holds for as long as a condition lasts? → **WHILE** (state-driven).
- A response to something that should not happen? → **IF … THEN**.
- Exists only where a feature is enabled? → **WHERE**.

Two quick checks. Unsure between WHEN and WHILE? Decide whether the
cause is an instant or a duration. Everything landing in Ubiquitous?
The triggers are missing, and with them the failure cases. Patterns
combine (Complex) but still state one behavior. Where an EARS sentence
would distort the meaning — mathematical content, more than three
preconditions — §4.1 permits a structured list or table under the same
R-id, with a one-line rationale.

## The bar is testable, not complete and unambiguous

A requirement is testable when a reader can tell whether an
implementation satisfies it. The practical test: could you write the
failing test from the sentence alone? Testable but later proven wrong
is fine. That is what amendments are for;
[evolving-requirements.md](evolving-requirements.md) covers that loop.
What you do not yet know, leave out. A missing requirement is honest; a
vague one is not. When the answer arrives, it takes the next free R-id
(§4.2 makes appending safe — no other id changes).

## What does not belong

- **Design.** Requirements state observable behavior at the system's
  boundary. Algorithms, storage layouts, and module shapes belong in
  `plan.md`. A requirement that pins internals is at the wrong level of
  detail — [evolving-requirements.md](evolving-requirements.md) has
  the diagnostic.
- **Acceptance criteria anywhere else.** They live here and only here.
  The tracker item carries a summary and a link (§4.3).
- **Success criteria that restate requirements.** The template's §4
  wants outcomes measurable after shipping. The sample spec says "99%
  of notifications within 60 seconds over a rolling two-week window" —
  not "notifications shall be delivered".
- **Unstated scope.** Say what is out. The sentence you leave out is
  the one that costs weeks later.

## The pre-implementation checklist

Run this pass before design and implementation build on the draft —
yourself, or point an agent at it
([reviewing-specs.md](reviewing-specs.md) is the same list from the
critic's side):

- every R-id states one testable behavior, in an EARS pattern or the
  §4.1 fallback with its rationale;
- the structure check ran locally (quickstart §6 has the command) —
  its vague-word warning is advisory, but treat each hit as a defect
  or defend the word;
- the IF/THEN rows cover the profile failure cases that apply;
- every essential term is defined or plain;
- scope says what is out; success criteria are measurable after
  shipping;
- new requirements took the next free R-id; nothing was renumbered.

A draft that survives this list is ready to build on. What slips
through surfaces later — in a teammate's PR comments, or in the review
phase after implementation (§3.2) — where each defect costs a round
trip instead of minutes. The checklist keeps that loop short.

## The author's turn, step by step

The moves above, placed on the walkthrough's timeline.
[feature-walkthrough.md](feature-walkthrough.md) tells the whole week;
this table replays its opening days from the author's chair. The
people are the walkthrough's; everything is fictitious. Each row is
one step. The six fields — when, who, what, where, how, why — are the
columns.

| When | Who | What | Where | How | Why |
| ---- | --- | ---- | ----- | --- | --- |
| **Day 1, afternoon** | **Bilguun** (developer, the author) + agent | The raw material: the five-line draft this guide opened with | The feature branch and folder the scaffold created | `/speckit.specify alert clients when a transfer is rejected by their daily limit, so they can raise it before the payroll run fails` | The draft is not a spec. The known failures — happy path only, vague filler, packed "and"s — are all in it |
| **Day 1, afternoon** | **Bilguun** + agent | The shaping pass, in one sitting: draft R-1 split three ways; "the system" named as the alerts service, every response made observable; IF/THEN rows written for the profile's failure cases; the trigger rewritten to the event the service consumes; "preferred channel" replaced by a channel chosen per alert; "log alert activity" pinned to named transitions in the audit log | `spec.md`, edited directly | Moves 1–7; the defect table above is this step's summary | Write so the critique finds nothing — a defect caught here costs minutes; the same defect found later costs a round trip |
| **Day 1, before pushing** | **Bilguun** | The author's checks: the structure check locally, then the checklist above. One finding stands — R-5 still says "quickly" | The local checkout, then a PR | Quickstart §6's command; the vague-word warning is advisory, never merge-blocking | The warning is for the author first. What survives his pass, a second reader catches |
| **Day 2** | **Nara** (product owner of the alerts domain) | Three comments: "quickly" is not a number (60 s or 6?); what happens when the same alert is registered twice; does scope cover *changing* limits? | The same PR | Ordinary PR review — the team's own practice, outside the standard's scope (§1) | Even a careful author's pass leaves defects. A second reader is the cheapest net there is |
| **Day 2, same day** | **Bilguun** + agent | The revision: R-5 gets "within 60 seconds"; a new R-3 covers the duplicate (`409 ALERT_EXISTS`); §1 gains its out-list — changing limits, limit-raise approvals, channels beyond sms and email | The same PR, revised | Each comment answered in the document, not in the comment thread | If the document does not say it, it is not agreed |
| **Day 3, morning** | **Bilguun** | The PR merges; `spec.md` exists in the feature folder | The feature folder on the branch | Nothing to flip, nothing to sign — the order is presence (§3.1): `plan.md` may exist only next to `spec.md`, and the structure check (§8.1) enforces it | The next artifact can start — [writing-design.md](writing-design.md) continues from here |
