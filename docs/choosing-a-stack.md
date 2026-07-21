# Choosing a stack — the team-lead guide

**Informative.** No normative text names a technology for your code:
the standard ([SDD-STANDARD.md](../standard/SDD-STANDARD.md)) governs
how features are specified, approved, and traced (§1), and the
[backend-services profile](../standard/profiles/backend-services/profile.md)
deliberately names no technologies (profile §1).
The tech stack — language, framework, storage, messaging, the build
and test toolchain — is a repo decision. This guide helps you make it
well for spec-driven work. Nothing here binds; in any conflict, the
standard takes precedence.

The choice is real mainly when the repo is new. Adoption never touches
existing code ([adopting-a-repo.md](adopting-a-repo.md) §2) — a repo
that has a stack keeps it, and the convention adapts to it. The
chooser is the repo's technical authority, the same role that holds
the Design gate (§3.3). Discard one assumption first: that spec-driven
development has a best stack. It does not; it changes the weights on a
few ordinary criteria, and it gives the decision a place to be
recorded. Both are below.

## 1. What the convention settles, and what stays yours

- **The profile is not the stack.** `--profile backend-services`
  binds how contracts are *documented* — the table shapes, the
  silence defaults. It deliberately names no broker, framework, or
  serialization (profile §1). Choosing a profile and choosing a stack
  are different acts; every candidate in the worked example below
  uses the same profile.
- **The decision's home is the constitution.** Repo-wide stack rules
  — the chosen platform, a ban list, a pinned toolchain — go under
  the constitution's *Repo principles*, appended by PR. They may
  tighten the seeded shared principles, never loosen them (§2.4).
  For two common backend outcomes, pre-written seed text for that PR
  exists ([stack packs](stack-packs/README.md)) — a starting text
  for the record, never a substitute for the decision.
- **Per-feature technical choices live in `plan.md`.** Each cites its
  `[R-n]` and names its rejected alternative
  ([writing-design.md](writing-design.md), moves 6–7). The stack
  decision deserves the same discipline, one level up — the worked
  example shows the record.
- **Changing the stack later is real work.** Where a migration alters
  a contract, carries a data migration, or contains any other
  hard-to-reverse step, it qualifies for the full gated workflow
  (§6.1) — and most migrations meet at least one of these. The
  cheap moment to choose well is before the first feature.

## 2. What the stack has to make cheap

Capabilities, not brand names — the same rule adoption applies to
infrastructure ([adopting-a-repo.md](adopting-a-repo.md) §1). Six,
each tied to the convention mechanism that makes it matter:

1. **Machine evidence.** A task is done only when its stated evidence
   exists — a check anyone can run, not a claim
   ([writing-tasks.md](writing-tasks.md), move 3). The stack sets the
   price of those checks: a first-class test framework, integration
   tests against real dependencies (a containerized store or broker),
   and — where the agent writes both the code and the tests — tooling
   that tests the tests, mutation testing above all. A stack where
   good evidence is expensive turns evidence lines back into claims.
2. **Contracts as files in the diff.** The Design Document links
   schemas under `contracts/`, and the same-PR rule merges spec
   change and code change together (§5.2). Both work best when the
   stack renders its contracts as committed artifacts — schema files,
   database migrations, an API description, generated code that is
   committed and diffed. What exists only at runtime cannot appear in
   a PR.
3. **Exact numbers where the domain is exact.** The profile's wire
   rule: money and other exact decimals travel as strings; a bare
   float on a money field is a defect (profile §2). The runtime has
   to honor what the wire promises — an exact decimal type in the
   language or its standard idiom. A stack that reaches for floating
   point by default fights that rule on every feature.
4. **Behavior visible in the program text.** The profile's reading
   rule exists because AI implementers fill unstated details with the
   most common pattern in their training data (profile §1). Code has
   the same failure mode: framework behavior that never appears in
   the text — hidden proxies, reflection-driven wiring,
   auto-configuration the team cannot enumerate — is behavior the agent
   guesses at, and it guesses the common case, not yours. Prefer
   explicit. A large framework can still be the right answer *as a
   subset*: keep the loud parts, ban the silent ones, and write the
   ban down (section 1's constitution home).
5. **A compiler that carries review weight.** Exhaustive case
   matching, null-safety, checked units where they exist — each is a
   class of spec violations caught before any human reads the diff.
   How much weight to put here is set by your review model
   (section 3).
6. **A corpus the agent knows.** Where agents implement — on these
   guides' fictitious team they do — output quality tracks how much
   of a stack's idiom the model saw in training. Boring, stable, and
   widely written beats novel and elegant. The newest framework is at
   its worst exactly where the agent needs it most.

## 3. What sets the weights

Four questions, answered before any candidate is named:

- **Who implements?** Agents → capabilities 4 and 6 rise. Humans
  only → both barely matter.
- **Who reviews?** Where tests are effectively the only review —
  agent-written code at a volume no human reads line by line —
  capabilities 1 and 5 become most of the decision. Ordinary human
  review relaxes both to normal weight.
- **What breaks if it is wrong?** Money movement or another
  irreversible effect → capability 3 is non-negotiable and the
  evidence bar rises. An internal tool that can be wrong for a day →
  most weights drop.
- **What can the team run?** The dominant criterion, and it is not on
  the list because spec-driven development did not change it: a stack
  the team cannot operate in production fails everything at once. The
  capabilities are tiebreakers among stacks the team can run. They
  never justify adopting one it cannot.

## 4. What a better stack does not buy

When specs and code drift apart, the cause is almost never the stack.
It is a skipped gate, a spec not amended in the PR that shipped the
change, a task ticked without its evidence — process failures, each
with its own net: the merge gate catches the skipped gate (§8.1), the
same-PR rule forbids merging without the spec amendment (§5.2), and
the Review approver spot-checks the evidence
([reviewing-specs.md](reviewing-specs.md)). No stack prevents any of
it. If the convention keeps breaking in your repo, look at the gates
before the toolchain. The converse follows: do not migrate a working
stack chasing spec-driven fitness. The migration is itself real work,
usually gated (section 1), and capabilities 1–6 alone rarely justify
its cost.

## 5. One stack choice, step by step

The sections above, on one fictitious decision. The cast is the
walkthrough's ([feature-walkthrough.md](feature-walkthrough.md)); the
setting is the week before an adoption morning like the one
[adopting-a-repo.md](adopting-a-repo.md) §6 shows. The team is
starting a new repo — statements-service: monthly account statements
from the transaction stream, one consumed event, a small API, money
amounts on every line. The technologies named are worked-example
material, chosen by fictitious people under fictitious constraints —
not recommendations. Each row is one step. The six fields — when, who,
what, where, how, why — are the columns.

| When | Who | What | Where | How | Why |
| ---- | --- | ---- | ----- | --- | --- |
| **Thursday, 09:30** | **Tulga** (tech lead) | Writes the situation down before any candidate is named: the agent will implement most tasks; Sarnai reviews every PR but will not read agent output line by line; statement lines carry money amounts; the team runs two JVM services and is on call for them | A one-page decision note | Section 3's four questions, answered in order | The weights come from the situation, not from the technologies. Candidates named first turn the meeting into a brand debate |
| **Thursday, 10:00** | **Tulga** + **Bilguun** (developer) | The shortlist, by operability alone: Java (what they run today), Kotlin (same JVM, same operations), Go (Bilguun's case — one static binary, fast builds). A serverless-rewrite pitch falls off: nobody on the team has operated one | The decision note | Section 3's dominant criterion, applied first | The capabilities are tiebreakers among stacks the team can run; a stack the team cannot operate stays out |
| **Thursday, afternoon** | **Tulga** + agent | The capability pass, one finding per cell. Exact numbers (capability 3): Go's standard library has no decimal type, and a missed field silently reads as zero — on statement lines, the wrong gap to patch with a library and discipline. Evidence (1): the agent writes the tests too, so mutation testing counts; their check finds it mature on Java bytecode, commercial-or-noisy on Kotlin's. Corpus (6): deepest on Java | The decision note — one row per candidate per capability, findings dated | Section 2, checked against the domain and row 1's weights | The findings are this team's, on this day, in this domain — and they age. A team with no money fields, or with humans writing the tests, lands elsewhere from the same table |
| **Thursday, late** | **Tulga** | The subset decision: Java and its usual framework, minus the runtime-silent parts. What never shows in program text — hidden proxying, auto-configuration the team cannot enumerate — goes on a written ban list; loud, visible wiring stays | The decision note; the ban list marked for the constitution | Capability 4: what the text does not show, the agent guesses | A stack is not only chosen; it is subsetted. An unwritten ban does not survive; a constitution entry does — every `plan.md`'s constitution check reads it |
| **Friday** | **Tulga**; **Nara** and **Sarnai** read it | The record: the decision with its rejected alternatives — Go (no exact decimal type, silent zero values, on a money domain), Kotlin (mutation tooling commercial-or-noisy at decision time; re-check at the next major choice) | The decision note, final — kept where the team plans work until the repo exists | [writing-design.md](writing-design.md) move 7's discipline, one level up: a decision names what it rejected and why | Decisions with alternatives survive re-reading months later. Preferences get argued again |
| **Monday, 09:00** | **Tulga** | Adoption begins — [adopting-a-repo.md](adopting-a-repo.md) §6's morning, replayed on the new repo. `--profile backend-services` is passed regardless of Thursday's outcome; the ban list lands under *Repo principles* in a follow-up PR to the scaffold commit | The new statements-service repo | `uv run bootstrap/init.py ../statements-service --integration claude --profile backend-services`, then the Repo-principles PR | The profile binds documentation shape, not technologies — it would have served Go or Kotlin unchanged. The convention is the same whichever candidate won; that is what stack-agnostic means |
