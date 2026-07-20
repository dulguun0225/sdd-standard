# Requirements — [FEATURE NAME]

**Status: DRAFT**
<!-- The gate is passed only when a HUMAN approver replaces the line above
     with `Status: APPROVED — <name>, <date>` in their own change.
     AI agents shall not write or modify Status lines (SDD-STANDARD §3.2). -->

| Field    | Value                                                     |
| -------- | --------------------------------------------------------- |
| Feature  | `[###-feature-name]`                                       |
| Authored | [DATE]                                                     |
| Approver | Requirements gate: [product authority or explicit delegate] |
| Input    | User description: "$ARGUMENTS"                             |

This is the **Requirements Document** (SDD convention). Every
requirement is phrased in an EARS pattern and carries a stable R-id.
R-ids are never renumbered and never reused. Withdrawn requirements stay
listed as `WITHDRAWN`. Acceptance criteria live here and only here. The
tracker item carries a summary and a link to this folder, nothing more.

---

## 1. Purpose and scope

[What this feature is for, in 2–5 sentences. State what is explicitly out
of scope — skipping that costs weeks of misunderstanding later.]

## 2. Definitions

[Terms the requirements depend on, each defined measurably. Delete the
section if plain language covers it. A requirement may only be as precise as
the definitions it uses.]

## 3. Requirements

<!-- EARS patterns (keywords stay in English):
     Ubiquitous:        The <system> shall <response>.
     Event-driven:      WHEN <trigger>, the <system> shall <response>.
     State-driven:      WHILE <state>, the <system> shall <response>.
     Unwanted behavior: IF <condition>, THEN the <system> shall <response>.
     Optional feature:  WHERE <feature is included>, the <system> shall <response>.
     Patterns combine when needed (Complex). One requirement = one testable
     behavior. Sometimes an EARS sentence would distort the meaning
     (mathematical content, more than three preconditions). SDD-STANDARD
     §4.1 then permits a structured list or table under the same R-id
     bullet, with a one-line rationale. Keep it inside the bullet's
     two-space continuation lines.
     A spec with only WHEN happy paths is incomplete. Walk the profile's
     standard failure cases (.specify/memory/profile.md §4: duplicate,
     replay, stale update, not-entitled, timeout, partial failure, …).
     Write the IF/THEN unwanted-behavior rows that apply. -->

- **R-1** WHEN [trigger], the [system] shall [response].
- **R-2** The [system] shall [response].
- **R-3** IF [undesired condition], THEN the [system] shall [response].

[Group requirements under §3.x subsections when the list grows past ~10.
New requirements take the next free R-id regardless of section.]

## 4. Success criteria

[How we will know the feature works in production — measurable outcomes, not
implementation claims. Delete only with a stated reason.]

## 5. Open items

| ID   | Item | Blocks | Owner / due |
| ---- | ---- | ------ | ----------- |
| OI-1 | [unknown or unconfirmed input] | [what it blocks] | [who resolves it, by when] |

## 6. Traceability

`tasks.md` shall reference these requirements as `[R-n]`. A change that
alters behavior covered by this document after approval shall update it in
the same PR/MR.

---

**Approval protocol:** the approver reviews, then replaces the Status line at
the top with `Status: APPROVED — <name>, <date>` in their own change. The
Design Document is drafted only after that.
