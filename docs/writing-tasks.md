# Writing the task list — the author's guide

**Informative.** This guide teaches the craft. The rules live in
[SDD-STANDARD.md](../standard/SDD-STANDARD.md) §5. In any conflict, the
standard wins.

You are the author when you draft the Task List, after the design gate
passed (§3.1). The Task List is the bridge from approved intent to
evidence. It is the implementer's work order — often an agent's. After
implementation it becomes the Review approver's record of what "done"
claimed. The approver's side is
[reviewing-specs.md](reviewing-specs.md).

## The raw material

`/speckit.tasks` materializes `tasks.md` from the approved plan. A
realistic weak draft:

> - [ ] **T-1** Implement the alerts API. [R-1]
> - [ ] **T-2** Add event consumption and notification delivery.
> - [ ] **T-3** Testing and cleanup. [R-1] [R-5]

Three lines, three distinct failures. The shaping pass turns them into
the approved [sample task list](../examples/sample-feature/tasks.md).

## The shaping moves

**1. Slice until one sitting can verify it.** Draft T-1 is a phase
wearing a T-id. "The alerts API" is a migration, a repository, two
endpoints, validation, and conflict handling. Days of work, and nothing
can check it until all of it exists. The tasks-template
states the rule at the point of use: prefer many small, independently
verifiable tasks over few large ones. Each is completable and checkable
in one sitting; per-step errors compound across a long task. Draft T-1
becomes the sample's T-1 (migration + repository, round-trip test),
T-2 (the POST endpoint, contract tests), and T-3 (the GET endpoint,
contract test). Each has its own check that can fail.

**2. Every task cites `[R-n]`, and every R-id is covered.** Draft T-2
carries no reference. The merge gate goes red on exactly this
(`T-2 carries no [R-n] reference`). The mapping is the point, not the
formatting. A task that maps to no requirement is either not needed —
or it just discovered a missing requirement. In that case amend
`spec.md` first (next free R-id, §4.2), then cite it. Then walk the
other direction. An R-id no task implements is an unbuilt requirement,
and the tasks gate checklist looks for it.

**3. Design the evidence at authoring time; never claim it at
completion.** Draft T-3 treats verification as a phase at the end. The
convention treats it as a property of every task: *a task is done when
its stated evidence exists.* Write the Evidence line before any code.
That is where you decide what "truthfully done" will mean:

| Evidence line | Verdict |
| ------------- | ------- |
| "code complete" | a claim — nothing to check |
| "works locally" | nobody else can check it |
| "contract tests cover 201/400/404/409 per plan.md §3" | a check anyone can run |
| "at-least-once replay test delivers exactly once" | the requirement's own success criterion, executable |

The Review approver later spot-checks these lines
([reviewing-specs.md](reviewing-specs.md)). Write them so the
spot-check is a click, not a dig through history. And "cleanup" maps
to no requirement: internal tidying with no observable effect needs no
task here at all (§6.1).

**4. Dependencies explicit; phases from the plan.** `Depends: T-1` is
written out, never implied by ordering. Phases mirror `plan.md` §9, so
each phase lands an increment satisfying named R-ids. If the phases and
the plan disagree, one of them is wrong. The gate is where that gets
caught.

**5. T-ids are stable, like R-ids.** Never renumbered, never reused. A
task that is no longer needed stays listed as `WITHDRAWN`. Work
discovered mid-implementation appends the next free T-id. When that
work changes behavior the approved spec covers, the spec amendment
rides the same PR (§5.2).

The whole pass, in one table:

| Draft line | Defect | Shaped into |
| ---------- | ------ | ----------- |
| T-1 "implement the alerts API" | a phase wearing a T-id — nothing can verify it in one sitting | T-1, T-2, T-3, each with its own evidence |
| T-2 no `[R-n]` | unmapped work; the merge gate goes red | T-4, T-5 citing [R-5] [R-6] [R-7] [R-8] |
| T-3 "testing and cleanup" | evidence smuggled into a bucket task; "cleanup" maps to no requirement | dissolved — every task carries its own evidence; exempt tidying needs no task (§6.1) |

## Before you request the gate

The author's pass over the approver's checklist
([reviewing-specs.md](reviewing-specs.md)):

- every task states one verifiable outcome, sized to a sitting;
- every task carries at least one `[R-n]`; every R-id is covered by at
  least one task;
- every task has an Evidence line naming a check, a run link, or an
  artifact that will exist;
- dependencies are explicit; phases match `plan.md` §9;
- T-ids take the next free number; nothing renumbered, nothing reused.

After the gate, the list is live. Tick a box only when its evidence
exists. Append new T-ids as reality adds work. And remember the
same-PR rule: the Task List is the first place spec drift shows, one
unticked box at a time.
