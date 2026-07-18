# Tasks — [FEATURE NAME]

**Status: DRAFT**
<!-- The gate is passed only when a HUMAN approver replaces the line above
     with `Status: APPROVED — <name>, <date>` in their own change.
     AI agents shall not write or modify Status lines (SDD-STANDARD §3.2). -->

| Field        | Value                                        |
| ------------ | -------------------------------------------- |
| Feature      | `[###-feature-name]`                          |
| Authored     | [DATE]                                        |
| Requirements | [spec.md](spec.md) — approved [date]          |
| Design       | [plan.md](plan.md) — approved [date]          |
| Approver     | Tasks gate: [technical authority]             |

This is the **Task List**. Every task carries at least one `[R-n]` reference
to a requirement it implements — a task that maps to no requirement is either
missing a requirement or not needed. T-ids are stable like R-ids: never
renumbered, never reused; withdrawn tasks stay listed as `WITHDRAWN`. Phases
come from plan.md §9; a task is done when its evidence exists. Prefer many
small, independently verifiable tasks over few large ones — each completable
and checkable in one sitting; per-step errors compound across a long task.

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

**Approval protocol:** the approver reviews, then replaces the Status line at
the top with `Status: APPROVED — <name>, <date>` in their own change.
Implementation starts only after that; the review phase follows
implementation before the item is marked done.
