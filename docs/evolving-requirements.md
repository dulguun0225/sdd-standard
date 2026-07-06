# Evolving requirements — the spec → build → learn loop

**Informative.** This guide explains and demonstrates; the rules live in
[SDD-STANDARD.md](../standard/SDD-STANDARD.md). In any conflict, the
standard wins.

Nobody writes airtight requirements. The standard does not ask for them:
the bar is **testable** (§4.1), not prophetic. A requirement is testable
when a reader can tell whether an implementation satisfies it — it can
still be narrow, incomplete, or later proven wrong. A spec is the team's
*current intent in checkable form*, and the machinery around it — stable
R-ids, amendments, the same-PR rule — exists precisely because intent
changes.

## The cycle this replaces

Vague requirement → implement → "that's not what I meant" → refine →
re-implement. That loop exists under every methodology; the damage is not
the iteration, it is the **silence**: each turn churns code while the
document (if one exists) quietly rots, until the spec is fiction and the
third iteration starts from tribal memory of the first two.

The standard keeps the loop and removes the silence.

## The loop

The whole shape is one diagram — the
[README's lifecycle diagram](../README.md#the-lifecycle-in-a-product-repo):
gates down the solid spine, dashed edges everywhere the lifecycle bends
back on itself. Three of those dashed edges are this guide's subject:

- **spec ⇢ spike ⇢ spec** — what you cannot yet state as testable
  behavior, you prototype first, exempt from ceremony (§6.1);
- **gate ⇢ artifact** — rejection: revised and resubmitted (§3.4),
  before reality is even consulted;
- **Done ⇢ Work item** — reality teaches; the learning re-enters as the
  next work item, and where it changes behavior an approved spec covers,
  the amendment rides the same PR as the code (§5.2).

Read around the circle and it says: spec → build → learn → spec. The
rest of this guide walks those legs.

## Walking the legs

**Spec the slice you know.** One testable behavior per R-id (§4.1) means
you can write down only what you are sure of and *omit* the rest — an
absent requirement is honest, a vague one is not. When you learn the
answer, append a new R-id; §4.2 makes appending safe, because ids are
never renumbered and nothing downstream shifts.

**Gates approve current intent.** The Requirements approver answers two
questions: is each line testable, and is this what we want *today*? Not:
will this survive contact with reality unchanged. Rejection is normal and
cheap (§3.4, [reviewing-specs.md](reviewing-specs.md)) — and so is
amendment. A team whose specs never change is not writing great specs; it
has stopped updating them.

**Build against the approved artifacts.** The solid spine of the
diagram — gates before implementation, the review phase after.

**Learn.** The review notes, the failing contract test, the user who did
the thing nobody predicted. Three exits: the behavior matches intent —
done, and the record is true; the intent changed — amend; the next slice
is now visible — spec it and go around again. The last two are the same
dashed edge out of Done.

**Amend in the same PR as the code it explains.** This edge is the whole
trick, and it is binding (§5.2): a change that alters behavior an
approved spec covers does not merge unless the same PR updates that spec.
Mechanics per §4.2: supersede the requirement in place, append a new
R-id, or mark a dead one `WITHDRAWN` — never renumber, never delete. The
amended spec goes back before its approver as a diff — minutes, not a
ceremony — because a document nobody re-agreed to is not an agreement.
The re-implementation was going to happen anyway; the amendment is the
one extra step, and it is what makes turn N+1 start from a record instead
of from memory.

## When you cannot even spec a slice

Prototype first. A spike with no externally observable effect matches no
qualifying trigger — §6.1 exempts it from all ceremony; keep it
throwaway by intent. Spec-driven does not mean spec-first-always; it
means the qualifying change that **ships** is spec'd. Learn from the
prototype, write the requirements from what it taught you, then walk the
loop with them.

## If every PR amends the spec

That is a signal, not a sin — usually one of two:

- **Wrong altitude.** The spec pins internals — algorithms, data shapes,
  module layout — that should stay free. The §6.1 triggers name what a
  spec is for: contracts, externally observable behavior, boundaries,
  hard-to-reverse steps. Those are the things other people depend on, and
  they are also the things teams *can* commit to. Pin the contract
  surface; leave everything underneath undecided (design freedom belongs
  to `plan.md`, at most).
- **Slice too thick.** If the requirements will not hold still, the item
  is usually too big. Spec a slice thin enough to be sure of, ship it,
  learn, spec the next one. The loop turns faster and each turn costs
  less.
