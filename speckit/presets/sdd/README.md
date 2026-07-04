# SDD preset

The SDD convention layered over stock Spec Kit through its supported preset
mechanism: four template overrides, no command or script overrides. Installed
into product repos by `bootstrap/init.py` (never by hand — see
SDD-STANDARD §9.2).

| Override | Strategy | Provides |
| -------- | -------- | -------- |
| `constitution-template` | replace | Shared constitution — non-negotiable principles, repo-append section, profile slot |
| `spec-template` | replace | Requirements Document — EARS + stable R-ids, requirements gate |
| `plan-template` | replace | Design Document — sync/async contract sections (profile slots), design gate |
| `tasks-template` | replace | Task List — `[R-n]` traceability, tasks gate |

`tasks-template` is a full replace rather than the originally designed
append addendum: at Spec Kit v0.12.4 the scaffolded workflow scripts resolve
templates by path convention and never apply composition strategies, so an
append-strategy file would be invisible to the agent workflow (verified
in the v0.12.4 source).

The review phase lives in the companion extension at
`speckit/extensions/sdd/`.
