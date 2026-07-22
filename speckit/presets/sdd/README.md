# SDD preset

This preset layers the SDD convention over stock Spec Kit. It uses only
the supported preset mechanism: four template overrides, no command or
script overrides. `bootstrap/init.py` installs it into product repos —
never install it by hand (SDD-STANDARD §9.2).

| Override | Strategy | Provides |
| -------- | -------- | -------- |
| `constitution-template` | replace | Shared constitution — non-negotiable principles, repo-append section, profile slot |
| `spec-template` | replace | Requirements Document — EARS + stable R-ids |
| `plan-template` | replace | Design Document — sync/async contract sections (profile slots) |
| `tasks-template` | replace | Task List — `[R-n]` traceability |

`tasks-template` is a full replace, not the originally designed append
addendum. Reason: the scaffolded workflow scripts honor composition
strategies only when a working python3 + PyYAML exist at scaffold time.
Without them, the scripts fall back to path-convention resolution, which
supports replace only (verified in the v0.13.0 source, common.sh
`resolve_template`). On such a machine an append-strategy file would
silently vanish. All-replace behaves identically at every degradation
level.

The review phase lives in the companion extension at
`speckit/extensions/sdd/`.
