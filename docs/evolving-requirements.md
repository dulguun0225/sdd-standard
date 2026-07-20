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

### Step 1 — learn

On **2026-07-17**, nine days after transfer-limit-alerts merged, a
payroll client's run submitted 40 transfers in one minute. Each was
rejected by the limit, each fired an event, and the client got 40
identical sms — then turned the alert off and told support why. The
ticket reaches **Nara**, product owner of the alerts domain and holder
of the Requirements gate. She checks it against the `delivery_log`
table — the data R-5's success criterion is measured over — and finds
40 deliveries in one minute, every one inside R-5's 60 seconds. **No
defect anywhere.** The service does exactly what the approved spec
says, so no bug report can capture the problem. The intent is what
changed: from "notify on every event" to "one notification per burst".

### Step 2 — re-enter as a work item

The same day, **Nara** files a work item — changing intent is the
product owner's call. It carries a summary and a link, nothing else:

> Payroll bursts fire one sms per transfer; clients disable the
> alert. Coalesce notifications per alert.
> → `specs/007-transfer-limit-alerts/`

The link points at the **existing** spec folder. Coalescing changes
how the alerts capability behaves; it is not a new capability, so no
new `008-` folder is created. Summary plus link is the whole item,
because acceptance criteria live in the Requirements Document and
nowhere else (§4.3) — the tracker never holds a second copy that can
drift.

### Step 3 — qualify

On **2026-07-18**, **Bilguun** picks the item up and makes the §6.1
qualification call — the developer's, as in the walkthrough (Day 1).
He judges the change against the §6.1 trigger list, noted on the
tracker item; the triggers are properties of the change itself, so
nothing is estimated. It qualifies: it alters externally observable
behavior — events that today produce a notification will deliberately
produce none. And it is not exempt — not a bugfix, because current
behavior is exactly what R-5 specifies. **A change of intent is never
a bugfix.**

### Step 4 — amend the spec (PR 1 of 4)

Still **2026-07-18**. **Bilguun** and the agent draft the amendment in
a PR touching `specs/007-transfer-limit-alerts/spec.md` — the
approved, merged original. No copy, no v2 file: an amendment is a diff
to the document itself. The agent may edit requirement text; it never
touches a Status line (§3.2).

The diff makes two of §4.2's three moves. First it **supersedes R-5 in
place** — the id keeps its number, the text changes:

> **R-5** WHEN the alerts service consumes a `transfer-limit-exceeded`
> event for an account with an active matching alert **and no
> notification for that alert was delivered in the preceding 10
> minutes**, the alerts service shall deliver a notification on the
> configured channel within 60 seconds.

Then it **appends R-10** — the suppressed case is new behavior, so it
gets a new id:

> **R-10** WHEN the alerts service consumes a `transfer-limit-exceeded`
> event for an account with an active matching alert whose most recent
> delivery is less than 10 minutes old, the alerts service shall record
> the event in the delivery log and shall not deliver a notification.

Bilguun makes the matching edit to the R-5 success criterion: 99%
within 60 seconds now measures the first event in each window. And
because `Status: APPROVED — Nara (PO), 2026-07-05` is now a stale
claim, he adds a dated amendment note under the Status line:

> **Amendment 2026-07-18 (pending re-approval):** R-5 superseded —
> delivery now applies only outside a 10-minute window; R-10 appended
> (suppression). Re-approve to clear this note.

He edits the superseded text in place, appends the new id after the
highest ever used, and adds the note — but he does not touch the
Status line itself. He never does. **Why R-10, not R-9:** R-9 is
taken, the unsupported-channel case appended mid-implementation
(walkthrough, Day 5), and ids are never reused (§4.2). And nothing
renumbers: R-1–R-4 and R-6–R-8 keep their ids, so every `[R-n]` in
`plan.md`, `tasks.md`, and merged history still points where it
pointed yesterday.

### Step 5 — the Requirements gate, again (still PR 1)

On **2026-07-19**, **Nara** re-approves — the same gate, the same
approver as the original document. She reads it as a diff: two
requirements and one criterion, not a 70-line document. The gate's two
questions, scoped to the diff: is each line testable, and is it wanted
today? She pushes back once — does suppression hide a second, larger
breach inside the window? R-10 keeps suppressed events in the delivery
log, so they stay visible; she accepts. Then, in a change she authors
herself (§3.2) — a suggestion she writes or a commit she pushes — she
removes the amendment note and rewrites the Status line to `Status:
APPROVED — Nara (PO), 2026-07-19`. PR 1 merges. A document nobody
re-agreed to is not an agreement. Minutes, not a ceremony.

### Step 6 — amend design and tasks (PRs 2 and 3)

Later on **2026-07-19**, after PR 1 merges — gates pass in order
(§3.1) — **Bilguun** and the agent amend the design and the task list.
**Tulga**, tech lead and holder of both the Design and Tasks gates,
approves each in his own change. In `plan.md` (PR 2), one new clause in
§2's delivery flow: before calling notification-service, check
`delivery_log` for a delivery under 10 minutes old, cited as `[R-10]`.
The amendment-note mechanics are the same as the spec's. In `tasks.md`
(PR 3), an appended task — T-ids are as stable as R-ids:

> **T-8** Suppress delivery when the alert's most recent delivery is
> under 10 minutes old; record the suppressed event in `delivery_log`.
> Depends: T-5. [R-5] [R-10]
> *Evidence: burst-replay test — 40 events in one minute produce 40
> delivery-log rows and exactly one notification.*

Both are direct edits. **No `/speckit.*` command amends:** each one
drafts a whole document, so re-running one over an approved artifact
would replace it wholesale — the amendment note and the ticked, stable
T-ids with it. The agent re-checks R-id coverage in both directions,
and Tulga checks what he always checks: every task carries an `[R-n]`
(§5.1), states its evidence, and names its dependencies. Implementation
may not start before this gate passes (§3.1). **Why T-8, not T-7:**
T-7 is taken, appended in the walkthrough's R-9 turn for the
unsupported-channel rejection. T-ids take the next free number and are
never reused, like R-ids: the frozen snapshot ended at T-6, R-9 added
T-7, coalescing adds T-8.

### Step 7 — implement (PR 4)

On **2026-07-20** to **2026-07-21**, **Bilguun** and the agent
implement task by task in PR 4 — alerts-service code and tests. The
work is the window check in the delivery path, the suppressed-event
log write, and the burst-replay test named by T-8's evidence line.
They run `/speckit.implement`; T-8's box is ticked when the
burst-replay evidence exists, not before. Passing the gates first does
not suspend §5.2: if implementation surfaces another unspecified case,
that amendment is included in this same PR — the walkthrough's Day-5
move.

### Step 8 — the Review gate, and done (still PR 4)

On **2026-07-22**, the agent writes `review-notes.md`, rewritten by
`speckit.sdd.review` after implementation: a verdict per R-id,
contract and task-evidence checks, and a drift section that comes back
empty for the right reason — the behavior change went through the
spec, not around it. Then **Sarnai**, who implemented none of this,
holds the gate (§3.3). She spot-checks the R-5 and R-10 verdicts into
code and tests, then passes the gate in her own change, at the top of
`review-notes.md` per the team's working agreement: `Status: APPROVED
— Sarnai (reviewer), 2026-07-22`. PR 4 merges. The notes inform the
gate; they cannot pass it. A human who is not the implementer does
(§3.2, §3.3).

**What the record now shows.** A reader opening `spec.md` sees
current intent: R-5 with its window, R-9's unsupported-channel
rejection, R-10's suppression. Git shows what changed, when, and who
agreed. The item is done — and the delivery log is already collecting
the data for the next turn. Turn N+1 starts from this record, not
from what anyone remembers.

### The amendment turn, in one page

| When | Who | Does what | How | Rule |
| ---- | --- | --------- | --- | ---- |
| 2026-07-17 | Nara | sees the alert misfire on a payroll burst — no defect, intent changed | reads the ticket against `delivery_log` | §4.1 |
| 2026-07-17 | Nara | files the work item: coalesce per alert | summary + link to the existing 007 folder | §4.3 |
| 2026-07-18 | Bilguun | qualifies the change — alters observable behavior, not a bugfix | the §6.1 trigger list | §6.1 |
| 2026-07-18 | Bilguun + agent | amend `spec.md` (PR 1): supersede R-5, append R-10, add the note | a direct diff to the approved file | §4.2, §5.2 |
| 2026-07-19 | Nara | re-approves the diff | own change flips the Status line | §3.2 |
| 2026-07-19 | Bilguun + agent, then Tulga | amend `plan.md` (PR 2) and `tasks.md` (PR 3); Tulga approves each | direct edits, never `/speckit.*` | §3.1, §5.1 |
| 2026-07-20–21 | Bilguun + agent | implement suppression + the burst-replay test (PR 4) | `/speckit.implement`; tick T-8 on evidence | §3.1 |
| 2026-07-22 | Sarnai | Review gate: spot-check verdicts, approve | own change; notes inform, never pass | §3.2, §3.3 |

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

### Step 1 — learn

On **2026-08-03**, twelve days after the coalescing turn merged,
treasury clients holding dozens of accounts — through their account
managers — ask **Nara** for a new thing, not a complaint about an
existing one: a single daily email summarizing limit events across all
of a client's accounts. Per-event alerts stay wanted where they fit;
payroll accounts keep them. Nara reads the feedback against the
delivery log's volume numbers, the same instrumentation the amendment
turn used: one client's accounts fired 60 separate notifications in a
week. This is not an amendment. Nothing 007 covers changes — every
R-id in 007 stays true word for word, and 007 §1's purpose, register
an alert on an account and get notified per event, does not cover a
cross-account daily summary. That is §6.1's fourth trigger: a new
capability.

### Step 2 — the folder call

On **2026-08-04**, **Bilguun** picks the item up — the same developer
judgment as the qualification call — and makes two decisions, noted on
the tracker item. The item qualifies: a new capability, a new
externally observable output. And it opens a new spec folder instead
of amending 007. He asks the boundary question of the approved spec:
does the change alter or extend behavior this document covers? R-9 and
R-10 did — new cases of the same capability — so they amended 007. The
digest does not, so it gets its own folder. The call matters both
ways. Combined into 007, one spec would carry two capabilities, and
every future approval would re-read both. Split out when covered
behavior *did* change, and 007 would keep claiming behavior that is no
longer true — the silent drift the standard exists to prevent.

### Step 3 — scaffold with the command

Still **2026-08-04**. **Bilguun** and the agent scaffold a new feature
branch and folder, `specs/008-limit-event-digest/`, holding a drafted
`spec.md` with `Status: DRAFT`. The command creates the branch and
numbers the folder:

```
/speckit.specify daily digest email of transfer-limit events across all of a client's accounts, sent once per day at a client-chosen hour
```

Numbering, branch, folder, template — scaffolding is what the commands
are for, and none of it exists in an amendment. This is the case where
the command is the right tool. The 008 draft opens at its own R-1:
R-ids are scoped to their document (§4.1), so 008's R-1 has nothing to
do with 007's. A spec that must reference another names the folder —
"007's R-5".

### Step 4 — the normal lifecycle, plus one cross-reference

From **2026-08-04** onward, the full cast runs 008 through the same
four gates. It is an ordinary new feature — draft, Requirements gate,
plan, tasks, implementation, Review — and
[feature-walkthrough.md](feature-walkthrough.md) is that story. The
same commands apply, `/speckit.plan`, `/speckit.tasks`,
`/speckit.implement`, because everything in 008 is a first draft, not
an amendment. 008 §1 states the boundary in writing: "Out of scope:
per-event alert behavior (`specs/007-transfer-limit-alerts/`)." And 007
can still be amended by this work: if implementing the digest alters
behavior 007 covers — say the digest sender changes the retry policy
that per-event delivery also uses — that PR amends 007's spec too, in
the same PR (§5.2). The rule binds the change, not the folder the
developer happens to be working in.

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
