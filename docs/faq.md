# FAQ

**Informative.** Seeded from real questions and their answers: whoever
resolves a question records it here, newest at the top of its section.
Deliberately empty until someone asks something — pre-written FAQs answer
questions nobody has.

Format per entry:

```markdown
### <the question, as asked>
<the answer that resolved it, with links to the standard/guides>
*(asked <YYYY-MM-DD>, answered by <role>)*
```

## Workflow

### Nobody can write airtight requirements — won't we just loop vague requirement → implement → refine → re-implement? How do we work?

The bar is **testable**, not airtight (SDD-STANDARD §4.1), and the loop
is the expected shape of the work, not a failure of it. The standard's
job is to make each turn recorded instead of silent: amend the spec in
the same PR as the code change (§5.2), superseding in place, appending a
new R-id, or marking `WITHDRAWN` (§4.2). Too uncertain to spec at all?
Spike first under the §6.1 exemption, then spec what the spike taught
you. The loop is drawn in the README's lifecycle diagram (the dashed
edges); the full explanation is
[evolving-requirements.md](evolving-requirements.md).
*(asked 2026-07-06, answered by the standard owner)*

## Tooling

*(no questions yet)*

## Gates and roles

*(no questions yet)*
