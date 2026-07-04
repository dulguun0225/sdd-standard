# Reviewing specs — the approver's guide

**Informative.** This guide explains what good looks like at each gate; the
binding rules live in [SDD-STANDARD.md](../standard/SDD-STANDARD.md) §3. In
any conflict, the standard wins.

You are a gate approver if your team bound one of the §3.3 roles to you.
Read this before your first approval.

## Mechanics, common to every gate

- An artifact passes a gate only when **you** replace its Status line with
  `Status: APPROVED — <your name>, <date>` **in your own change** (commit
  or suggestion you author). Em dash or plain hyphen both count. An agent
  writing that line is a rule violation, not a convenience.
- Rejection is normal and cheap: comment what must change and leave the
  Status line alone. A stalled gate blocks implementation start for real
  work — review within a couple of working days or hand off explicitly.
- You are approving the *document*, not the person. If the document does
  not say it, it is not agreed.

## Requirements gate (product authority)

Approve when:

- Every requirement is **one testable behavior** in an EARS pattern. Watch
  for smuggled "and" — "validates and persists and notifies" is three
  requirements wearing one R-id.
- R-ids are bare facts: never renumbered, never reused; anything removed is
  listed `WITHDRAWN`, not deleted.
- The unwanted-behavior cases exist (`IF … THEN …`). A spec with only
  happy-path `WHEN`s is half a spec — ask what happens on the duplicate,
  the missing account, the failed delivery.
- Success criteria are measurable after shipping, not restatements of the
  requirements.
- Scope says what is **out**. The absent sentence is the expensive one.
- Acceptance criteria live here, not in the tracker item. The ticket
  carries a summary and a link, nothing more.

## Design gate (technical authority)

Approve when:

- Every design element cites the requirement it satisfies as `[R-n]`, and
  every R-id is somewhere satisfied — walk the list, it takes two minutes.
- The contract sections follow the repo's stack profile shapes: mutating
  sync operations state their idempotency; every business error has a
  stable code; every message states its delivery semantics and schema
  location. An empty idempotency or delivery cell is a question you ask
  now, not in the incident review.
- Decisions carry rationale including what was rejected. "We chose X" with
  no alternative considered is a preference, not a decision.
- The constitution check is done honestly — tension named, not waved off.

## Tasks gate (technical authority)

Approve when:

- Every task carries at least one valid `[R-n]`, and collectively the tasks
  cover every R-id — uncovered requirements are unbuilt requirements.
- Each task states its **evidence**: what will exist when it is truthfully
  done (a passing check, a run link, an artifact).
- Dependencies are explicit, and phases match the design's phase plan.

## Review gate (a reviewer who is not the implementer)

The review phase produces `review-notes.md` — requirement-by-requirement
verdicts, contract checks, and spec-drift findings. Those notes inform you;
they approve nothing.

Approve when:

- Every R-id verdict is *implemented* with evidence you spot-checked — or
  the deviation went back through the spec (same-PR update), not around it.
- No spec drift: nothing in the delta changes behavior the approved spec
  covers without the spec changing in the same PR. This is the finding that
  matters most — drift is how specs die.
- Done tasks have their stated evidence.

You must not be the implementer of the item under review. If the team is
small enough that this pinches, that is a staffing conversation for the
team, not a rule to bend.
