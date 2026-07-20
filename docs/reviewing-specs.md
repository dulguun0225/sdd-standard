# Reviewing specs — the approver's guide

**Informative.** This guide shows what a good artifact is at each gate.
The binding rules live in [SDD-STANDARD.md](../standard/SDD-STANDARD.md)
§3. In any conflict, the standard takes precedence.

You are a gate approver if your team bound one of the §3.3 roles to
you. Read this before your first approval.
[feature-walkthrough.md](feature-walkthrough.md) shows your gate in
context: one feature through all four gates, PR by PR.

## Mechanics, common to every gate

- An artifact passes a gate only when **you** replace its Status line
  with `Status: APPROVED — <your name>, <date>`. That happens **in
  your own change**: a commit or suggestion you author. Em dash or
  plain hyphen both count. An agent writing that line is a rule
  violation, not a convenience.
- Rejection is normal and cheap. Comment what must change and leave
  the Status line alone. A stalled gate blocks real work from
  starting. Review within a couple of working days, or hand off
  explicitly.
- You are approving the *document*, not the person. If the document
  does not say it, it is not agreed.

## Requirements gate (product authority)

The author's side of this gate is
[writing-requirements.md](writing-requirements.md): the same defects,
caught while writing.

Approve when:

- Every requirement is **one testable behavior** in an EARS pattern.
  The §4.1 fallback (mathematical content, more than three
  preconditions) permits a structured list or table instead, with its
  stated rationale. Watch for a hidden "and" — "validates and persists
  and notifies" is three requirements under one R-id.
- R-ids are permanent: never renumbered, never reused. Anything
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
  terms the spec uses but §2 never defines. The structure check warns
  on the common vague words. The judgment call stays yours.
- Success criteria are measurable after shipping, not restatements of
  the requirements.
- Scope says what is **out**. The missing sentence is the one that
  costs weeks later.
- Acceptance criteria live here, not in the tracker item. The ticket
  carries a summary and a link, nothing more.

## Design gate (technical authority)

The author's side of this gate is
[writing-design.md](writing-design.md).

Approve when:

- Every design element cites the requirement it satisfies as `[R-n]`,
  and every R-id is somewhere satisfied. Check the list; it takes two
  minutes.
- The contract sections follow the repo's stack profile shapes.
  Mutating sync operations state their idempotency. Every business
  error has a stable code. Every message states its delivery semantics
  and schema location. An empty idempotency or delivery cell is a
  question you ask now, not in the incident review.
- Decisions carry rationale including what was rejected. "We chose X"
  with no alternative considered is a preference, not a decision.
- The constitution check is done honestly — tension named, not dismissed.

## Tasks gate (technical authority)

The author's side of this gate is
[writing-tasks.md](writing-tasks.md).

Approve when:

- Every task carries at least one valid `[R-n]`, and collectively the
  tasks cover every R-id. An uncovered requirement is an unbuilt
  requirement.
- Each task states its **evidence**: what will exist when it is
  truthfully done (a passing check, a run link, an artifact).
- Dependencies are explicit, and phases match the design's phase plan.

## Review gate (a reviewer who is not the implementer)

The review phase produces `review-notes.md`: requirement-by-requirement
verdicts, contract checks, and spec-drift findings. Those notes inform
you; they approve nothing.

Approve when:

- Every R-id verdict is *implemented*, with evidence you
  spot-checked — or the deviation went back through the spec (a
  same-PR update), not around it.
- No spec drift: nothing in the delta changes behavior the approved
  spec covers without the spec changing in the same PR. This finding
  matters most. Drift is how specs stop matching the code.
- Done tasks have their stated evidence.

You must not be the implementer of the item under review. If the team
is small enough that this is hard to staff, that is a staffing conversation,
not a rule to waive.
