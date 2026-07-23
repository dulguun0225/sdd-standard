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
addendum. Reason: the scaffolded workflow scripts resolve templates by
path convention only (verified in the v0.13.4 source, `common.sh` /
`common.py` `resolve_template`) — they pick the first matching
`presets/<id>/templates/<name>.md` and copy it, which is replace-only.
Spec Kit's composition strategies exist, but they run in the preset
resolver at preset-resolve time (`PresetResolver.resolve_content`), not in
these scaffold scripts, so a non-replace strategy would be silently
ignored where the templates are actually consumed. All-replace is the only
strategy that is honored, at every degradation level.

The review phase lives in the companion extension at
`speckit/extensions/sdd/`.
