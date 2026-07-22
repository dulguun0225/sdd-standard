# Reviewing specs — the reader's guide

**Informative.** This guide shows what a good artifact is, read from
the other side of the page: the same defects the writing guides teach
authors to avoid, as a checklist for whoever reads the artifact next.
The binding rules live in
[SDD-STANDARD.md](../standard/SDD-STANDARD.md) §3–§5. In any conflict,
the standard takes precedence.

The standard defines no approval gates (§3.3, D-19). Nothing here is a
sign-off, and whether humans review changes at all is the team's own
practice, outside the standard's scope (§1). Reviewing a spec is
optional practice that catches defects while they are cheap: a defect
found in the artifact costs minutes; the same defect found after
implementation costs a rework cycle; found in production, an incident.

The checklists below serve two moments:

- **Before implementation starts** — whoever reads an artifact: a
  teammate on the PR, an agent asked to critique the draft, or the
  author on a last pass before pushing.
- **After implementation** — the automated review phase (§3.2)
  compares what was built against these same artifacts. A defect that
  survives into implementation comes back then as a finding — or, if
  the artifact was too vague to check against, does not come back at
  all. That silence is the worst outcome; the checklists exist to keep
  the artifacts checkable.

[feature-walkthrough.md](feature-walkthrough.md) shows these reads in
context: one feature end to end, PR by PR.

## Two habits, common to every artifact

- Read the document, not the author. If the document does not say it,
  it is not agreed. The implementer — human or AI — gets only the
  text.
- Fixes land in the document, not the comment thread. Ask for the
  number and the unit, the missing `IF … THEN` row, the empty cell's
  answer — and check that the artifact's next revision says it.

## Requirements Document (`spec.md`)

The author's side is
[writing-requirements.md](writing-requirements.md): the same defects,
caught while writing.

Look for:

- Every requirement is **one testable behavior** in an EARS pattern.
  The §4.1 fallback (mathematical content, more than three
  preconditions) permits a structured list or table instead, with its
  stated rationale. Watch for a hidden "and" — "validates and persists
  and notifies" is three requirements under one R-id.
- R-ids are permanent: never renumbered, never reused (§4.2). Anything
  removed is listed `WITHDRAWN`, not deleted.
- The unwanted-behavior cases exist (`IF … THEN …`). A spec with only
  happy-path `WHEN`s is incomplete. Ask what happens on the
  duplicate, the missing account, the failed delivery.
- Ambiguity is removed here or nowhere. Implementers, human or AI,
  cannot be relied on to catch it downstream. An AI implementer fills
  each ambiguous spot with a silent guess. A quick checklist:
  unbounded quantities ("large", "many", "several"); time bounds
  without a number and a unit ("quickly", "soon", "eventually"); vague
  adverbs and adjectives ("appropriately", "gracefully", "efficient");
  terms the spec uses but its §2 (Definitions) never defines. The
  structure check (§8.1) warns on the common vague words — an advisory
  WARNING, never merge-blocking. The judgment call stays with the
  reader.
- Success criteria are measurable after shipping, not restatements of
  the requirements.
- Scope says what is **out**. The missing sentence is the one that
  costs weeks later.
- Acceptance criteria live here, not in the tracker item (§4.3). The
  ticket carries a summary and a link, nothing more.

## Design Document (`plan.md`)

The author's side is [writing-design.md](writing-design.md).

Look for:

- Every design element cites the requirement it satisfies as `[R-n]`,
  and every R-id is somewhere satisfied. Check the list both ways; it
  takes two minutes.
- The contract sections follow the repo's stack profile shapes. Every
  business error has a stable code. Every message states its delivery
  semantics and schema location. Under the profile's stated-or-default
  reading rule, a silent cell is not the implementer's free choice —
  the profile default *is* the contract — so silence is right only
  when the author means the default and the design makes it real.
- Idempotency on a mutating operation is the one cell with no safe
  default (profile §2). Empty, it is a review question to ask now, not
  in the incident review; the review phase later records exactly this
  as an open question.
- Decisions carry rationale including what was rejected. "We chose X"
  with no alternative considered is a preference, not a decision.
- The constitution check is done honestly — tension named, not
  dismissed.

## Task List (`tasks.md`)

The author's side is [writing-tasks.md](writing-tasks.md).

Look for:

- Every task carries at least one valid `[R-n]` (§5.1), and
  collectively the tasks cover every R-id. An uncovered requirement is
  an unbuilt requirement. The structure check goes red on a task with
  no `[R-n]`; the other direction — every R-id reached by some task —
  stays a reader's check.
- Each task states its **evidence**: what will exist when it is
  truthfully done (a passing check, a run link, an artifact).
- Dependencies are explicit, and phases match the design's phase plan.

## After implementation — the review phase

The checklists above are also the bar the review phase checks against.
After implementation completes, the review command
(`speckit.sdd.review`) compares what was built against the three
artifacts and writes `review-notes.md` into the feature folder (§3.2):
requirement-by-requirement verdicts with evidence, contract checks
including profile-default conformance, task evidence, spec-drift
findings, and open questions. A filled example:
[examples/sample-feature/review-notes.md](../examples/sample-feature/review-notes.md).

Before the item is marked done, every finding is resolved one of three
ways (§3.2): fix the implementation, amend the artifact in the same
PR/MR (§5.2), or record an explicit acceptance with a reason in the
notes. Whoever resolves the notes — usually the implementer, with the
PR's readers watching — weighs the findings in this order:

- **Spec drift first.** The delta changes behavior the spec covers,
  and the same PR did not update that spec (§5.2). This finding
  matters most: drift is how specs stop matching the code. Resolve it
  by amending the spec in the PR, never by ignoring it.
- **A verdict other than *implemented*.** A deviation goes back
  through the spec — a same-PR amendment — not around it.
- **A done task without its stated evidence.** Untick it, or produce
  the evidence.
- **Open questions** — an empty idempotency cell, an unstated
  mechanism the code chose. Answer them in the artifact, or accept
  them with a reason in the notes.

An empty findings section is itself evidence: the notes say what was
checked, so "none" is a checked result, not an unchecked one.
