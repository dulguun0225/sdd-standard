# Evolving requirements — the spec → build → learn loop

**Informative.** This guide explains and demonstrates; the rules live in
[SDD-STANDARD.md](../standard/SDD-STANDARD.md). In any conflict, the
standard wins.

Nobody writes airtight requirements. The standard does not ask for
them. The bar is **testable** (§4.1), not airtight. A requirement is
testable when a reader can tell whether an implementation satisfies it.
It can still be narrow, incomplete, or later proven wrong. A spec is
the team's *current intent in checkable form*. The machinery around
it — stable R-ids, amendments, the same-PR rule — exists precisely
because intent changes.

## The cycle this replaces

Vague requirement → implement → "that's not what I meant" → refine →
re-implement. That loop exists under every methodology. The damage is
not the iteration; it is the **silence**. Each turn churns code while
the document, if one exists, quietly rots. Eventually the spec is
fiction, and the third iteration starts from what people remember of
the first two.

The standard keeps the loop and removes the silence.

## The loop

The whole shape is one diagram: the
[README's lifecycle diagram](../README.md#the-lifecycle-in-a-product-repo).
Gates run down the solid spine. Dashed edges appear everywhere the
lifecycle bends back on itself. Three of those dashed edges are this
guide's subject:

- **spec ⇢ spike ⇢ spec** — what you cannot yet state as testable
  behavior, you prototype first, exempt from ceremony (§6.1);
- **gate ⇢ artifact** — rejection: revised and resubmitted (§3.4),
  before any code is written;
- **Done ⇢ Work item** — reality teaches. The learning re-enters as
  the next work item. Where it changes behavior an approved spec
  covers, the amendment rides the same PR as the code (§5.2).

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
Not: will this survive contact with reality unchanged. Rejection is
normal and cheap (§3.4, [reviewing-specs.md](reviewing-specs.md)). So
is amendment. A team whose specs never change is not writing great
specs; it has stopped updating them.

**Build against the approved artifacts.** The solid spine of the
diagram — gates before implementation, the review phase after.

**Learn.** The review notes, the failing contract test, the user who
did the thing nobody predicted. Three exits. The behavior matches
intent: done, and the record is true. The intent changed: amend. The
next slice is now visible: spec it and go around again. The last two
are the same dashed edge out of Done.

**Amend in the same PR as the code it explains.** This edge is the
whole trick, and it is binding (§5.2). A change that alters behavior
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
there. Everything here is fictitious. Each step answers who, what,
when, where, why, and how.

One timing difference matters before the steps. In the walkthrough,
the learning arrived mid-implementation (Day 5), so the amendment rode
the implementation PR — §5.2's same-PR rule doing its job. Here the
learning arrives after Done, so the turn starts at the gates: the
amendment passes the Requirements gate **before** any code (§3.1).
Same mechanics, different entry point. The team keeps the
one-PR-per-artifact shape it used in the walkthrough, so this turn is
four small PRs: spec, plan, tasks, implementation.

### Step 1 — learn

- **When:** 2026-07-17, nine days after transfer-limit-alerts merged.
- **Who:** a payroll client, then support, then Nara — product owner
  of the alerts domain, holder of the Requirements gate.
- **What:** the client's payroll run submitted 40 transfers in one
  minute. Each bounced off the limit, each fired an event, and the
  client got 40 identical sms — then turned the alert off and told
  support why.
- **Where:** a support ticket, checked against the `delivery_log`
  table — the data R-5's success criterion is measured over.
- **How:** Nara queries the log for the account: 40 deliveries in one
  minute, every one within R-5's 60 seconds. No defect anywhere.
- **Why this is spec work:** the service does exactly what the
  approved spec says, so no bug report can carry the problem. The
  intent is what changed: from "notify on every event" to "one
  notification per burst".

### Step 2 — re-enter as a work item

- **When:** the same day, 2026-07-17.
- **Who:** Nara. Changing intent is the product owner's call.
- **What:** a tracker item carrying a summary and a link, nothing
  else:

  > Payroll bursts fire one sms per transfer; clients disable the
  > alert. Coalesce notifications per alert.
  > → `specs/007-transfer-limit-alerts/`

- **Where:** the team's work tracker, pointing at the **existing**
  spec folder. Coalescing changes how the alerts capability behaves;
  it is not a new capability, so no new `008-` folder is created.
- **Why so short:** acceptance criteria live in the Requirements
  Document and nowhere else (§4.3). The tracker never holds a second
  copy that can drift.
- **How:** summary plus link is the whole item.

### Step 3 — qualify

- **When:** 2026-07-18, the moment Bilguun picks the item up.
- **Who:** Bilguun, the implementer. The qualification call is the
  developer's (walkthrough, Day 1).
- **What:** the §6.1 call — does the change match a trigger?
- **Where:** noted on the tracker item.
- **How:** judgment against the §6.1 trigger list. The triggers are
  properties of the change itself; nothing is estimated.
- **Why it qualifies:** it alters externally observable behavior —
  events that today produce a notification will deliberately produce
  none. And it is not exempt: not a bugfix, because current behavior
  is exactly what R-5 specifies. A change of intent is never a
  bugfix.

### Step 4 — amend the spec (PR 1 of 4)

- **When:** 2026-07-18.
- **Who:** Bilguun and the agent draft. The agent may edit
  requirement text; it never touches a Status line (§3.2).
- **Where:** a PR touching `specs/007-transfer-limit-alerts/spec.md`
  — the approved, merged original. No copy, no v2 file: an amendment
  is a diff to the document itself.
- **What:** two of §4.2's three moves, in one diff.

  *Supersede R-5 in place.* The id keeps its number; the text
  changes:

  > **R-5** WHEN the alerts service consumes a
  > `transfer-limit-exceeded` event for an account with an active
  > matching alert **and no notification for that alert was delivered
  > in the preceding 10 minutes**, the alerts service shall deliver a
  > notification on the configured channel within 60 seconds.

  *Append R-10.* The suppressed case is new behavior, so it gets a
  new id:

  > **R-10** WHEN the alerts service consumes a
  > `transfer-limit-exceeded` event for an account with an active
  > matching alert whose most recent delivery is less than 10 minutes
  > old, the alerts service shall record the event in the delivery
  > log and shall not deliver a notification.

  Bilguun makes the matching edit to the R-5 success criterion: 99%
  within 60 seconds now measures the first event in each window. And
  because `Status: APPROVED — Nara (PO), 2026-07-05` is now a stale
  claim, he adds a dated amendment note under the Status line:

  > **Amendment 2026-07-18 (pending re-approval):** R-5 superseded —
  > delivery now applies only outside a 10-minute window; R-10
  > appended (suppression). Re-approve to clear this note.

- **How:** edit the superseded requirement's text in place; append
  the new id after the highest ever used; add the note. Bilguun does
  not touch the Status line itself. He never does.
- **Why R-10, not R-9:** R-9 is taken — the unsupported-channel case
  appended mid-implementation (walkthrough, Day 5). Ids are never
  reused (§4.2).
- **Why nothing renumbers:** R-1–R-4 and R-6–R-8 keep their ids, so
  every `[R-n]` in `plan.md`, `tasks.md`, and merged history still
  points where it pointed yesterday.

### Step 5 — the Requirements gate, again (still PR 1)

- **When:** 2026-07-19.
- **Who:** Nara — the same gate, the same approver as the original
  document.
- **What:** a re-approval read as a diff: two requirements and one
  criterion, not a 70-line document.
- **Where:** inside PR 1, in a change she authors herself (§3.2) — a
  suggestion she writes or a commit she pushes.
- **How:** she removes the amendment note and rewrites the Status
  line to `Status: APPROVED — Nara (PO), 2026-07-19`. PR 1 merges.
- **Why a human, again:** the gate's two questions, scoped to the
  diff — testable, and wanted today? She pushes back once: does
  suppression hide a second, larger breach inside the window? R-10
  keeps suppressed events in the delivery log, so they stay visible;
  she accepts. A document nobody re-agreed to is not an agreement.
  Minutes, not a ceremony.

### Step 6 — amend design and tasks (PRs 2 and 3)

- **When:** 2026-07-19, after PR 1 merges — gates pass in order
  (§3.1).
- **Who:** Bilguun and the agent draft; Tulga — tech lead, holder of
  the Design and Tasks gates — approves each in his own change.
- **What, in `plan.md`:** one new clause in §2's delivery flow —
  before calling notification-service, check `delivery_log` for a
  delivery under 10 minutes old — cited as `[R-10]`. Same
  amendment-note mechanics as the spec.
- **What, in `tasks.md`:** an appended task; T-ids are as stable as
  R-ids:

  > **T-7** Suppress delivery when the alert's most recent delivery
  > is under 10 minutes old; record the suppressed event in
  > `delivery_log`. Depends: T-5. [R-5] [R-10]
  > *Evidence: burst-replay test — 40 events in one minute produce 40
  > delivery-log rows and exactly one notification.*

- **Where:** PR 2 touches `plan.md`; PR 3 touches `tasks.md`.
- **How:** direct edits. No `/speckit.*` command amends: each one
  drafts a whole document, so re-running one over an approved
  artifact would replace it wholesale — the amendment note and the
  ticked, stable T-ids with it. The agent re-checks R-id coverage in
  both directions.
- **Why:** implementation may not start before the Tasks gate passes
  (§3.1). Tulga checks what he always checks: every task carries an
  `[R-n]` (§5.1), states its evidence, and names its dependencies.

### Step 7 — implement (PR 4)

- **When:** 2026-07-20 to 2026-07-21.
- **Who:** Bilguun and the agent, task by task.
- **What:** the window check in the delivery path, the
  suppressed-event log write, and the burst-replay test named by
  T-7's evidence line.
- **Where:** PR 4 — alerts-service code and tests.
- **How:** `/speckit.implement`; T-7's box is ticked when the
  burst-replay evidence exists, not before.
- **Why §5.2 still matters:** passing the gates first does not
  suspend the same-PR rule. If implementation surfaces another
  unspecified case, that amendment rides this same PR — the
  walkthrough's Day-5 move.

### Step 8 — the Review gate, and done (still PR 4)

- **When:** 2026-07-22.
- **Who:** the agent writes the notes; Sarnai — who implemented none
  of this — holds the gate (§3.3).
- **What:** `review-notes.md`, rewritten by `speckit.sdd.review`
  after implementation: a verdict per R-id, contract and
  task-evidence checks, and a drift section that comes back empty for
  the right reason — the behavior change went through the spec, not
  around it.
- **Where:** the feature folder, inside PR 4.
- **How:** Sarnai spot-checks the R-5 and R-10 verdicts into code and
  tests, then passes the gate in her own change, at the top of
  `review-notes.md` per the team's working agreement:
  `Status: APPROVED — Sarnai (reviewer), 2026-07-22`. PR 4 merges.
- **Why:** the notes inform the gate; they cannot pass it. A human
  who is not the implementer does (§3.2, §3.3).

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
R-11, not a recycled R-10. Deletion would strand T-7's `[R-10]` and
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

- **When:** 2026-08-03, twelve days after the coalescing turn merged.
- **Who:** treasury clients holding dozens of accounts, their account
  managers, then Nara.
- **What:** an ask for a new thing, not a complaint about an existing
  one: a single daily email summarizing limit events across all of a
  client's accounts. Per-event alerts stay wanted where they fit —
  payroll accounts keep them.
- **Where:** account-manager feedback, checked against the delivery
  log: one client's accounts fired 60 separate notifications in a
  week.
- **How:** Nara reads the feedback against the delivery log's volume
  numbers, the same instrumentation the amendment turn used.
- **Why this is not an amendment:** nothing 007 covers changes.
  Every R-id in 007 stays true word for word, and 007 §1's purpose —
  register an alert on an account, get notified per event — does not
  cover a cross-account daily summary. That is §6.1's fourth
  trigger: a new capability.

### Step 2 — the folder call

- **When:** 2026-08-04, when Bilguun picks the item up.
- **Who:** Bilguun — the same developer judgment as the
  qualification call.
- **What:** two decisions. The item qualifies (new capability, new
  externally observable output). And it opens a new spec folder
  instead of amending 007.
- **Where:** noted on the tracker item.
- **How:** ask the boundary question of the approved spec: does the
  change alter or extend behavior this document covers? R-9 and
  R-10 did — new cases of the same capability — so they amended 007.
  The digest does not, so it gets its own folder.
- **Why the call matters both ways:** crammed into 007, one spec
  carries two capabilities, and every future approval re-reads both.
  Split out when covered behavior *did* change, 007 keeps claiming
  behavior that is no longer true — the silent drift the standard
  exists to prevent.

### Step 3 — scaffold with the command

- **When:** 2026-08-04.
- **Who:** Bilguun and the agent.
- **What:** a new feature branch and folder,
  `specs/008-limit-event-digest/`, holding a drafted `spec.md` with
  `Status: DRAFT`.
- **Where:** the product repo; the command creates the branch and
  numbers the folder.
- **How:**

  ```
  /speckit.specify daily digest email of transfer-limit events across all of a client's accounts, sent once per day at a client-chosen hour
  ```

  Numbering, branch, folder, template — scaffolding is what the
  commands are for, and none of it exists in an amendment. This is
  the case where the command is the right tool.
- **Why R-ids restart:** the 008 draft opens at its own R-1. R-ids
  are scoped to their document (§4.1); 008's R-1 has nothing to do
  with 007's. A spec that must reference another names the folder:
  "007's R-5".

### Step 4 — the normal lifecycle, plus one cross-reference

- **When:** 2026-08-04 onward.
- **Who:** the full cast; the same four gates.
- **What:** from here, 008 is an ordinary new feature — draft,
  Requirements gate, plan, tasks, implementation, Review.
  [feature-walkthrough.md](feature-walkthrough.md) is that story.
- **Where:** 008 §1 states the boundary in writing: "Out of scope:
  per-event alert behavior (`specs/007-transfer-limit-alerts/`)."
- **How:** the same commands as the walkthrough — `/speckit.plan`,
  `/speckit.tasks`, `/speckit.implement` — because everything in 008
  is a first draft, not an amendment.
- **Why 007 can still be amended by this work:** if implementing the
  digest alters behavior 007 covers — say the digest sender changes
  the retry policy that per-event delivery also uses — that PR
  amends 007's spec too, in the same PR (§5.2). The rule binds the
  change, not the folder the developer happens to be working in.

The two turns are the same loop with different entry points:
learning that changes covered behavior re-enters its own spec;
learning that adds a capability enters a new one.

## When you cannot even spec a slice

Prototype first. A spike with no externally observable effect matches
no qualifying trigger, so §6.1 exempts it from all ceremony. Keep it
throwaway by intent. Spec-driven does not mean spec-first-always. It
means the qualifying change that **ships** is spec'd. Learn from the
prototype. Write the requirements from what it taught you. Then walk
the loop with them.

## If every PR amends the spec

That is a signal, not a sin — usually one of two:

- **Wrong altitude.** The spec pins internals that should stay free:
  algorithms, data shapes, module layout. The §6.1 triggers name what
  a spec is for — contracts, externally observable behavior,
  boundaries, hard-to-reverse steps. Those are the things other people
  depend on. They are also the things teams *can* commit to. Pin the
  contract surface. Leave everything underneath undecided; design
  freedom belongs to `plan.md`, at most.
- **Slice too thick.** If the requirements will not hold still, the
  item is usually too big. Spec a slice thin enough to be sure of,
  ship it, learn, spec the next one. The loop turns faster and each
  turn costs less.
