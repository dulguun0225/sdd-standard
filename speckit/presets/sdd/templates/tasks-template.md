# Tasks — [FEATURE NAME]

| Field        | Value                                        |
| ------------ | -------------------------------------------- |
| Feature      | `[###-feature-name]`                          |
| Authored     | [DATE]                                        |
| Requirements | [spec.md](spec.md)                            |
| Design       | [plan.md](plan.md)                            |

This is the **Task List**. Every task carries at least one `[R-n]`
reference to a requirement it implements. A task that maps to no
requirement is either missing a requirement or not needed. T-ids are
stable like R-ids: never renumbered, never reused. Withdrawn tasks stay
listed as `WITHDRAWN`. Phases come from plan.md §9. A task is done when
its evidence exists. Prefer many small, independently verifiable tasks
over few large ones. Each task should be completable and checkable in
a single work session. Per-step errors compound across a long task.
Be precise first, simple second: say exactly what is true, no
ambiguity. Keep technical terms when the everyday word is less exact.
Within that: short sentences, everyday words, one idea per sentence.
No business-speak or figurative filler.
The style limits wording, not coverage: stay complete, keep every
edge case.

---

## Phase 1 — [phase name]

- [ ] **T-1** [What gets built, concretely — name the files/components.]
  [R-1] *Evidence: [what proves it done — a passing check, a run link, an
  artifact that exists].*
- [ ] **T-2** [Next task. Note dependencies explicitly: Depends: T-1.]
  [R-2] [R-3]

## Phase 2 — [phase name]

- [ ] **T-3** [...] [R-3]

---

**Order (SDD-STANDARD §3.1):** implementation starts only after this list
exists; the review phase follows implementation, and its findings are
resolved before the item is marked done (§3.2).
