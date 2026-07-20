# Evolving requirements — the spec → build → learn loop

**Informative.** This guide explains and demonstrates; the rules live in
[SDD-STANDARD.md](../standard/SDD-STANDARD.md). In any conflict, the
standard takes precedence.

Nobody writes complete, unambiguous requirements. The standard does not ask for
them. The bar is **testable** (§4.1), not complete and unambiguous. A requirement is
testable when a reader can tell whether an implementation satisfies it.
It can still be narrow, incomplete, or later proven wrong. A spec is
the team's *current intent in checkable form*. The rules around
it — stable R-ids, amendments, the same-PR rule — exist precisely
because intent changes.

**In short.** When you learn something after approval, you change the
spec and the code together, in the same PR (§5.2). Three moves keep the
record honest: supersede a requirement in place, append a new R-id, or
mark a dead one `WITHDRAWN` — never renumber, never delete (§4.2). The
rest of this guide walks the loop stage by stage, then two full worked
turns. Read a worked turn when you reach it; you do not need both on a
first pass.

## The cycle this replaces

Vague requirement → implement → "that's not what I meant" → refine →
re-implement. That loop exists under every methodology. The damage is
not the iteration; it is the **silence**. Each turn rewrites code while
the document, if one exists, quietly goes out of date. Eventually the spec no longer matches the code, and the third iteration starts from what people remember of
the first two.

The standard keeps the loop and removes the silence.

## The loop

The whole shape is one diagram: the
[README's lifecycle diagram](../README.md#the-lifecycle-in-a-product-repo).
Gates run down the solid main path. Dashed edges appear everywhere the
lifecycle loops back on itself. Three of those dashed edges are this
guide's subject:

- **spec ⇢ spike ⇢ spec** — what you cannot yet state as testable
  behavior, you prototype first, exempt from ceremony (§6.1);
- **gate ⇢ artifact** — rejection: revised and resubmitted (§3.4),
  before any code is written;
- **Done ⇢ Work item** — you learn from what shipped. The learning re-enters as
  the next work item. Where it changes behavior an approved spec
  covers, the amendment is included in the same PR as the code (§5.2).

Read around the circle and it says: spec → build → learn → spec. The
rest of this guide covers those stages one by one, then two full
turns, step by step: [a turn that amends the
spec](#a-turn-that-amends-the-spec-step-by-step) and [a turn that
opens a new one](#a-turn-that-opens-a-new-spec-step-by-step).

## The loop, stage by stage

**Spec the slice you know.** One testable behavior per R-id (§4.1)
means you can write down only what you are sure of and *omit* the
rest. An absent requirement is honest; a vague one is not. When you
learn the answer, append a new R-id. §4.2 makes appending safe: ids
are never renumbered, so nothing downstream shifts.

**Gates approve current intent.** The Requirements approver answers
two questions. Is each line testable? Is this what we want *today*?
Not: will this stay correct once implemented. Rejection is
normal and cheap (§3.4, [reviewing-specs.md](reviewing-specs.md)). So
is amendment. A team whose specs never change is not writing great
specs; it has stopped updating them.

**Build against the approved artifacts.** The solid main path of the
diagram — gates before implementation, the review phase after.

**Learn.** The review notes, the failing contract test, the user who
did the thing nobody predicted. Three exits. The behavior matches
intent: done, and the record is true. The intent changed: amend. The
next slice is now visible: spec it and go around again. The last two
are the same dashed edge out of Done.

**Amend in the same PR as the code it explains.** This edge is the
key rule, and it is binding (§5.2). A change that alters behavior
an approved spec covers does not merge unless the same PR updates that
spec. Mechanics per §4.2: supersede the requirement in place, append a
new R-id, or mark a dead one `WITHDRAWN`. Never renumber, never
delete. The amended spec goes back before its approver as a diff —
minutes, not a ceremony. A document nobody re-agreed to is not an
agreement. The re-implementation was going to happen anyway. The
amendment is the one extra step, and it makes turn N+1 start from a
record instead of from memory.

## A turn that amends the spec, step by step

The stages above, applied to one concrete turn. The feature is the
teaching example, [transfer-limit-alerts](../examples/sample-feature/spec.md);
the people and gate bindings are the walkthrough's
([feature-walkthrough.md](feature-walkthrough.md)). Like the
walkthrough's R-9 turn, this continues the story past the example's
frozen snapshot — the files under `examples/` end at R-8 and stay
there. Everything here is fictitious.

One timing difference matters before the steps. In the walkthrough,
the learning arrived mid-implementation (Day 5), so the amendment was included in
the implementation PR — §5.2's same-PR rule applying as intended. Here the
learning arrives after Done, so the turn starts at the gates: the
amendment passes the Requirements gate **before** any code (§3.1).
Same mechanics, different entry point. The team keeps the
one-PR-per-artifact shape it used in the walkthrough, so this turn is
four small PRs: spec, plan, tasks, implementation.

Each row is one step. The six fields — when, who, what, where, how,
why — are the columns.

| When | Who | What | Where | How | Why |
| ---- | --- | ---- | ----- | --- | --- |
| **2026-07-17**, nine days after transfer-limit-alerts merged | A payroll client, then support, then **Nara** (PO, Requirements approver) | A payroll run fired 40 transfers in one minute; each was rejected, each fired an event; the client got 40 identical sms and disabled the alert | A support ticket, checked against the `delivery_log` table (the data R-5's success criterion is measured over) | Nara queries the log — 40 deliveries in one minute, every one within R-5's 60 seconds. No defect | The service does exactly what the approved spec says, so no bug report captures it. Intent changed: "notify on every event" → "one per burst" |
| **2026-07-17** (same day) | **Nara** — changing intent is the product owner's call | A tracker item, summary + link only: *"Payroll bursts fire one sms per transfer; clients disable the alert. Coalesce notifications per alert. → `specs/007-transfer-limit-alerts/`"* | The team tracker, pointing at the **existing** 007 folder — coalescing is not a new capability, so no `008-` folder | Summary plus link is the whole item | Acceptance criteria live in the Requirements Document and nowhere else (§4.3); the tracker never holds a second copy that can drift |
| **2026-07-18**, when Bilguun picks it up | **Bilguun**, the implementer — the qualification call is the developer's | The §6.1 call: does the change match a trigger? | Noted on the tracker item | Judgment against the §6.1 trigger list; the triggers are properties of the change, so nothing is estimated | It qualifies — it alters externally observable behavior (events that notify today will produce none). Not exempt: not a bugfix, since current behavior is exactly what R-5 specifies. **A change of intent is never a bugfix** |
| **2026-07-18** | **Bilguun** + agent draft — the agent may edit requirement text, never a Status line (§3.2) | Two of §4.2's moves in one diff.<br>**Supersede R-5 in place** — add the clause "and no notification for that alert was delivered in the preceding 10 minutes", so it delivers within 60 seconds only outside that window.<br>**Append R-10** (new id) — "…whose most recent delivery is less than 10 minutes old, … record the event in the delivery log and shall not deliver a notification."<br>Edit the R-5 success criterion (99% within 60 s now measures the first event per window).<br>Add a dated note under the Status line: *"Amendment 2026-07-18 (pending re-approval): R-5 superseded; R-10 appended. Re-approve to clear."* | A PR touching `specs/007-transfer-limit-alerts/spec.md` — the approved original. No copy, no v2 file: an amendment is a diff to the document | Edit the superseded text in place; append the new id after the highest ever used; add the note. Bilguun never touches the Status line | **R-10, not R-9** — R-9 is taken (unsupported-channel, walkthrough Day 5); ids are never reused (§4.2). **Nothing renumbers** — R-1–R-4 and R-6–R-8 keep their ids, so every `[R-n]` still resolves |
| **2026-07-19** | **Nara** — same gate, same approver as the original | A re-approval read as a diff: two requirements and one criterion, not a 70-line document | Inside PR 1, in a change she authors herself (§3.2) | She removes the amendment note and rewrites the Status line to `Status: APPROVED — Nara (PO), 2026-07-19`. PR 1 merges | The gate's two questions, scoped to the diff — testable, wanted today? She pushes back once (does suppression hide a second, larger breach?); R-10 keeps suppressed events in the log, so they stay visible; she accepts. A document nobody re-agreed to is not an agreement |
| **2026-07-19**, after PR 1 merges (gates pass in order, §3.1) | **Bilguun** + agent draft; **Tulga** (tech lead) approves Design and Tasks, each in his own change | `plan.md` (PR 2): one new clause in §2's delivery flow — before calling notification-service, check `delivery_log` for a delivery under 10 minutes old — cited `[R-10]`.<br>`tasks.md` (PR 3): append **T-8** — "Suppress delivery when the alert's most recent delivery is under 10 minutes old; record the suppressed event in `delivery_log`. Depends: T-5. [R-5] [R-10]." Evidence: burst-replay test — 40 events in one minute produce 40 delivery-log rows and exactly one notification | PR 2 touches `plan.md`; PR 3 touches `tasks.md` | Direct edits — **no `/speckit.*` command amends** (each drafts a whole document and would replace it wholesale). The agent re-checks R-id coverage both ways | Implementation may not start before the Tasks gate (§3.1). Tulga checks each task carries `[R-n]` (§5.1), states evidence, names dependencies. **T-8, not T-7** — T-7 is taken (walkthrough's R-9 turn); T-ids are never reused |
| **2026-07-20** to **2026-07-21** | **Bilguun** + agent, task by task | The window check in the delivery path, the suppressed-event log write, and the burst-replay test named by T-8's evidence line | PR 4 — alerts-service code and tests | `/speckit.implement`; T-8's box is ticked when the burst-replay evidence exists, not before | §5.2 still binds — passing the gates first does not suspend the same-PR rule; another unspecified case would be amended in this same PR |
| **2026-07-22** | The agent writes the notes; **Sarnai** (never the implementer, §3.3) holds the gate | `review-notes.md`, rewritten by `speckit.sdd.review` — a verdict per R-id, contract and task-evidence checks, and a drift section empty for the right reason (the change went through the spec) | The feature folder, inside PR 4 | Sarnai spot-checks the R-5 and R-10 verdicts into code and tests, then passes the gate in her own change at the top of `review-notes.md`: `Status: APPROVED — Sarnai (reviewer), 2026-07-22`. PR 4 merges | The notes inform the gate; they cannot pass it. A human who is not the implementer does (§3.2, §3.3) |

**What the record now shows.** A reader opening `spec.md` sees
current intent: R-5 with its window, R-9's unsupported-channel
rejection, R-10's suppression. Git shows what changed, when, and who
agreed. The item is done — and the delivery log is already collecting
the data for the next turn. Turn N+1 starts from this record, not
from what anyone remembers.

### The third move — withdrawing a requirement

Two of §4.2's moves appeared above; the third is for a requirement
that is removed. Suppose a later turn teaches the opposite lesson: a
suppressed event hid a genuine second breach, and intent flips back
to notify-on-every-event. That turn's amendment supersedes R-5 in
place again — the window clause comes out — and withdraws R-10:

> **R-10** WITHDRAWN 2026-08-28 — suppression removed; a suppressed
> event hid a genuine second limit breach.

The entry stays in the list, and the next appended requirement is
R-11, not a recycled R-10. Deletion would leave T-8's `[R-10]` unresolvable and
every reference in merged PRs; WITHDRAWN keeps them all resolvable.
The spec keeps the record of what was tried and abandoned — exactly
what the next person proposing suppression needs to find.

## A turn that opens a new spec, step by step

First, the rule the turn above used without stating it: **no
`/speckit.*` command amends.** Each command drafts a whole document,
so running one against an approved artifact would replace it
wholesale — the amendment note and the stable, ticked T-ids with it.
Amendments of any size are direct edits. The commands return when the
loop returns something that is not an amendment: a capability the
approved spec does not cover. That is this turn. Fictitious, like the
turn above.

| When | Who | What | Where | How | Why |
| ---- | --- | ---- | ----- | --- | --- |
| **2026-08-03**, twelve days after the coalescing turn merged | Treasury clients (dozens of accounts), their account managers, then **Nara** | An ask for a new thing: a single daily email summarizing limit events across all of a client's accounts. Per-event alerts stay where they fit (payroll accounts keep them) | Account-manager feedback, checked against the delivery log (one client's accounts fired 60 notifications in a week) | Nara reads the feedback against the delivery log's volume numbers | **Not an amendment** — nothing 007 covers changes; 007 §1's purpose (register an alert, get notified per event) does not cover a cross-account summary. §6.1's fourth trigger: a new capability |
| **2026-08-04**, when Bilguun picks it up | **Bilguun** — the same developer judgment as the qualification call | Two decisions: the item qualifies (new capability, new observable output); and it opens a new spec folder instead of amending 007 | Noted on the tracker item | Ask the boundary question — does the change alter or extend behavior 007 covers? R-9/R-10 did (same capability) → amended 007; the digest does not → its own folder | Combined into 007, one spec would carry two capabilities and every approval would re-read both; split out wrongly, 007 would claim behavior no longer true (silent drift) |
| **2026-08-04** | **Bilguun** + agent | A new feature branch and folder `specs/008-limit-event-digest/`, holding a drafted `spec.md` with `Status: DRAFT` | The product repo; the command creates the branch and numbers the folder | `/speckit.specify daily digest email of transfer-limit events across all of a client's accounts, sent once per day at a client-chosen hour`. Scaffolding is what the commands are for; none of it exists in an amendment | **R-ids restart** — the 008 draft opens at its own R-1 (scoped to its document, §4.1). A spec referencing another names the folder ("007's R-5") |
| **2026-08-04** onward | The full cast; the same four gates | 008 is an ordinary new feature — draft, Requirements gate, plan, tasks, implementation, Review ([feature-walkthrough.md](feature-walkthrough.md) is that story) | 008 §1 states the boundary: *"Out of scope: per-event alert behavior (`specs/007-transfer-limit-alerts/`)."* | The same commands — `/speckit.plan`, `/speckit.tasks`, `/speckit.implement` — because everything in 008 is a first draft | 007 can still be amended by this work — if implementing the digest alters behavior 007 covers, that PR amends 007 too (§5.2). The rule binds the change, not the folder |

The two turns are the same loop with different entry points:
learning that changes covered behavior re-enters its own spec;
learning that adds a capability enters a new one.

## When you cannot even spec a slice

Prototype first. A spike with no externally observable effect matches
no qualifying trigger, so §6.1 exempts it from all ceremony. Keep it
throwaway by intent. Spec-driven does not mean spec-first-always. It
means the qualifying change that **ships** is spec'd. Learn from the
prototype. Write the requirements from what it taught you. Then go through
the loop with them.

## If every PR amends the spec

That is a signal, not a failure — usually one of two:

- **Wrong level of detail.** The spec pins internals that should stay free:
  algorithms, data shapes, module layout. The §6.1 triggers name what
  a spec is for — contracts, externally observable behavior,
  boundaries, hard-to-reverse steps. Those are the things other people
  depend on. They are also the things teams *can* commit to. Pin the
  contract surface. Leave everything underneath undecided; design
  freedom belongs to `plan.md`, at most.
- **Slice too thick.** If the requirements keep changing, the
  item is usually too big. Spec a slice thin enough to be sure of,
  ship it, learn, spec the next one. The loop turns faster and each
  turn costs less.
