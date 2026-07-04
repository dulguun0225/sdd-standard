# Constitution — [PROJECT NAME]

Seeded from the SDD convention (the sdd-standard repository; normative text
in `standard/SDD-STANDARD.md` — section references below point there). The
shared principles are non-negotiable: a repo may append to this file, never
remove or weaken them (§2.4).

## Shared principles (seeded — do not edit)

1. **Spec first.** A qualifying work item passes the Requirements → Design →
   Tasks gates, in order, before implementation starts, and the Review gate
   after implementation, before it is marked done (§3.1).
2. **Gates are human.** An artifact passes a gate only when a human approver
   adds `Status: APPROVED — <name>, <date>` in their own change. AI agents
   never write or modify approval Status lines (§3.2). The Review approver is
   never the implementer (§3.3).
3. **EARS with stable R-ids.** Every requirement is one testable behavior in
   an EARS pattern with an R-id that is never renumbered or reused (§4).
   Acceptance criteria live in the Requirements Document only — tracker items
   carry a summary and a link (§4.3).
4. **Traceability, no drift.** Every task carries at least one `[R-n]`
   reference. A change that alters behavior covered by an approved spec does
   not merge unless the same PR/MR updates that spec (§5).
5. **The pressure valve.** Below the size threshold, no spec ceremony.
   Emergency hotfixes ship immediately; when one alters spec-covered
   behavior, the spec is updated within 5 working days (§6).
6. **Specs are clean and English.** No credentials, secrets, or personal
   data in specs; spec content inherits the repo's data classification and
   agent access follows the adopting organization's AI usage policy (§12).
   Specs are authored in English; the glossary carries Mongolian
   translations (§11).
7. **The standard wins.** This file and everything informative explain;
   SDD-STANDARD.md and the stack profiles legislate. In any conflict, the
   standard prevails and this file gets fixed.

## Repo principles

<!-- Repo-specific principles are appended here by PR, like any other
     change. They may tighten the shared principles, never loosen them. -->

## Stack profile

<!-- bootstrap/init.py appends the repo's stack profile reference below.
     The profile provides defaults and vocabulary for the Design Document's
     contract sections; it never adds gates or artifact types (§7). -->
