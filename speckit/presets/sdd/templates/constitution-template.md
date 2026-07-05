# Constitution — [PROJECT NAME]

Seeded from the SDD convention, version [CONVENTION VERSION] (the
sdd-standard repository). `standard/SDD-STANDARD.md` at the pinned release
is the normative text — in any conflict the standard prevails and this file
gets fixed. The shared principles below are non-negotiable: a repo may
append to this file, never remove or weaken them (§2.4); the seeded block
is checked against the pinned template by `ci/check_convention_version.py`.

## Shared principles (seeded — do not edit)

1. **Gates are human.** A qualifying work item (§6) passes the
   Requirements → Design → Tasks gates, in order, before implementation
   starts, and the Review gate after implementation (§3.1). An artifact
   passes a gate only when a human approver adds
   `Status: APPROVED — <name>, <date>` in their own change; AI agents never
   write or modify approval Status lines (§3.2). The Review approver is
   never the implementer (§3.3).
2. **No silent drift.** Every task carries at least one `[R-n]` reference
   to a requirement it implements. A change that alters behavior covered by
   an approved spec does not merge unless the same PR/MR updates that spec
   (§5).
3. **Specs are clean and English.** No credentials, secrets, or personal
   data in specs; spec content inherits the repo's data classification, and
   agent access follows the adopting organization's AI usage policy (§12).
   Specs are authored in English (§11).

Everything else the convention binds — EARS phrasing and stable R-ids (§4),
the qualifying-item triggers (§6), artifact structure — is carried by the
seeded templates and the review command at their point of use; the standard
at the pinned release is the single source.

## Repo principles

<!-- Repo-specific principles are appended here by PR, like any other
     change. They may tighten the shared principles, never loosen them
     (§2.4). -->

## Stack profile

<!-- bootstrap/init.py appends the repo's stack profile reference below.
     The profile provides defaults and vocabulary for the Design Document's
     contract sections; it never adds gates or artifact types (§7). -->
