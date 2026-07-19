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
append addendum: the scaffolded workflow scripts honor composition
strategies only when a working python3 + PyYAML are present at scaffold
time and fall back to path-convention replace-only resolution without
them (verified in the v0.13.0 source, common.sh resolve_template), so an
append-strategy file would silently vanish on degraded machines.
All-replace behaves identically at every degradation level.

The review phase lives in the companion extension at
`speckit/extensions/sdd/`.
