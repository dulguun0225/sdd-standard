# Guides — start here

**Informative.** Everything in `docs/` explains and demonstrates; the
binding rules live in [SDD-STANDARD.md](../standard/SDD-STANDARD.md)
and the stack profiles. In any conflict, the standard takes precedence and the
guide gets fixed.

| You want to… | Read |
| ------------ | ---- |
| understand what this convention is, and why | the [repo README](../README.md) — its lifecycle section is the overview |
| run your first spec'd feature yourself | [quickstart.md](quickstart.md) (~20 minutes, scratch repo) |
| see who does what, when, on a real team | [feature-walkthrough.md](feature-walkthrough.md) |
| write a Requirements Document that passes its gate | [writing-requirements.md](writing-requirements.md) |
| write a Design Document | [writing-design.md](writing-design.md) |
| write a Task List | [writing-tasks.md](writing-tasks.md) |
| approve at a gate — any of the four | [reviewing-specs.md](reviewing-specs.md) |
| change requirements after approval; spike; amend | [evolving-requirements.md](evolving-requirements.md) |
| know what infrastructure this needs — hosting, CI, tracker — and why | [adopting-a-repo.md](adopting-a-repo.md) §1 — capabilities, not vendors |
| choose the tech stack for a new repo | [choosing-a-stack.md](choosing-a-stack.md) — capabilities, not brand names |
| adopt the convention in a repo | [adopting-a-repo.md](adopting-a-repo.md) |
| ask a question | [faq.md](faq.md) — real questions and answers collect there |

Reading paths, by role:

- **Everyone, once:** the README's lifecycle section, then the
  quickstart done yourself.
- **Authors** (usually a developer working with an agent): the three
  writing guides, in artifact order. Each takes a realistic weak draft
  and shapes it into the approved
  [teaching example](../examples/sample-feature/spec.md). Add
  [evolving-requirements.md](evolving-requirements.md) for when requirements
  change, and the walkthrough to see the whole week of work.
- **Approvers:** [reviewing-specs.md](reviewing-specs.md) before your
  first gate, plus the writing guide of the artifact you approve — it
  is your checklist, read from the author's side.
- **Team leads:** [choosing-a-stack.md](choosing-a-stack.md) when the
  repo is new, [adopting-a-repo.md](adopting-a-repo.md), then
  everything your team reads.

Reference material lives outside `docs/`: the normative standard and
profiles (`standard/`), the glossary with the EARS patterns
([GLOSSARY.md](../standard/GLOSSARY.md)), and the finished example
artifacts ([examples/sample-feature](../examples/sample-feature/)).
