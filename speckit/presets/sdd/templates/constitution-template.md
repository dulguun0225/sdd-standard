# Constitution — [PROJECT NAME]

Seeded from the SDD convention, version [CONVENTION VERSION] (the
sdd-standard repository). `standard/SDD-STANDARD.md` at the pinned
release is the normative text. In any conflict the standard prevails and
this file gets fixed. The shared principles below are non-negotiable. A
repo may append to this file, never remove or weaken them (§2.4).
`ci/check_convention_version.py` checks the seeded block against the
pinned template.

## Shared principles (seeded — do not edit)

1. **Spec before code.** A qualifying work item (§6) has its
   Requirements Document, Design Document, and Task List in place, in
   that order, before implementation starts (§3.1). The review phase
   runs after implementation; its findings are resolved — fix, same-PR
   amendment, or explicit accepted-with-reason note — before the item
   is marked done (§3.2).
2. **No silent drift.** Every task carries at least one `[R-n]` reference
   to a requirement it implements. A change that alters behavior covered by
   a spec does not merge unless the same PR/MR updates that spec
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
