# Spec-Driven Development Standard

**Version: 0.1.0-draft** (pre-release — binding for a repository from the
moment that repository adopts the convention) · Owner: the **standard
owner** — a role, not a person, defined in §13 · Changes land by reviewed
PR and a CHANGELOG entry.

> **Normative status.** This document and the profiles under
> `standard/profiles/` are the ONLY normative sources of the SDD
> convention. Everything in `docs/` is informative — it explains and
> demonstrates, never legislates. In any conflict, this standard wins and the
> guide gets fixed. Requirements language: **shall** = binding; **may** =
> explicitly permitted. Parameters marked ⚠ are starting defaults — the
> standard owner amends them by reviewed PR as real usage teaches.

---

## 1. Scope

This standard governs how features are specified, approved, and traced in
adopting product repositories. It does **not** govern coding style,
architecture review, CI/CD pipelines beyond the checks in §8, choice of AI
agent or IDE, or the team's process ceremonies. Adjacent standardization
gets its own home.

## 2. Vocabulary and artifacts

2.1 The standard names the documents; the current implementation (§9) names
the files:

| Standard term | File | Contains |
| ------------- | ---- | -------- |
| Requirements Document | `spec.md` | EARS requirements with stable R-ids; acceptance criteria |
| Design Document | `plan.md` | Architecture and contracts — sync endpoints and/or async messages; profiles (§7) fill the stack vocabulary |
| Task List | `tasks.md` | Implementation tasks, each carrying `[R-n]` references |
| Constitution | `.specify/memory/constitution.md` | The repo's non-negotiable principles, seeded from the shared constitution |

Term definitions live in [GLOSSARY.md](GLOSSARY.md) (reference material).

2.2 Each spec'd feature shall live in its product repo at
`specs/<NNN>-<kebab-slug>/` with sequential numbering. Filenames throughout
spec folders shall be lowercase-kebab-case; all text files shall use LF line
endings.

2.3 Specs shall live in the repository whose code they govern. There shall
be **no central specs repository**. (Spec change and implementation land in
the same PR; co-location prevents drift; any vendor's agent gets the spec in
its working directory for free.)

2.4 A repo may append repo-specific principles to its constitution; it shall
not remove or weaken the seeded shared principles.

## 3. Workflow and gates

3.1 For every qualifying work item (§6), the artifacts shall pass their
gates in order — **Requirements → Design → Tasks** — before implementation
starts, and the **Review** gate after implementation completes, before the
item is marked done.

3.2 An artifact passes a gate only when a human approver adds
`Status: APPROVED — <name>, <date>` to it in that same change (an em-dash or
plain hyphen is accepted). AI agents shall not write or modify approval
Status lines.

3.3 Gate approver roles — each adopting team binds these to named people at
adoption (`docs/adopting-a-repo.md` shows how, informatively):

| Gate | Approver role |
| ---- | ------------- |
| Requirements | The repo's product authority (e.g. a product owner, or an explicit delegate) |
| Design | The repo's technical authority (tech lead or architect) |
| Tasks | The technical authority (may be the Design approver) |
| Review | A code reviewer who is **not** the implementer |

One person may hold several roles; the Review approver shall never be the
implementer of the item under review.

3.4 A rejected artifact is revised and resubmitted.

## 4. Requirements rules

4.1 Every requirement in a Requirements Document shall express **one
testable behavior** and carry a stable R-id. Requirements shall be phrased
in an EARS pattern (patterns illustrated in GLOSSARY §1). Where an EARS
sentence would distort a requirement's meaning — mathematical content, or
more than three preconditions — the requirement may instead carry a
structured list or table under its R-id, with a one-line rationale; it
still expresses one testable behavior. (Decision record: D-15.)

4.2 R-ids shall never be renumbered or reused. Amendments supersede a
requirement in place or append a new one; deleted requirements remain listed
as `WITHDRAWN`.

4.3 Acceptance criteria shall exist solely in the Requirements Document.
Work-tracker items for spec'd features shall carry only a summary and a link
to the spec folder. ⚠

## 5. Traceability and drift

5.1 Every task in a Task List shall carry at least one `[R-n]` reference to
a requirement it implements.

5.2 A change that alters behavior covered by an approved spec shall not
merge unless the same PR/MR updates that spec. A merged violation is a
spec-drift incident.

## 6. Qualifying work items — the pressure valve

6.1 A work item **qualifies** (full gated workflow, §3.1) WHEN it does any
of the following ⚠:

- creates or alters externally observable behavior or a contract (API,
  CLI, schema, message, protocol);
- crosses a repo, service, or team boundary;
- contains a hard-to-reverse step (a data migration, a protocol or
  data-model change);
- introduces a new capability, rather than a localized change to an
  existing one.

A work item that does none of these requires no spec ceremony. Explicitly
exempt, even where a trigger appears to match: bugfixes restoring
already-specified behavior, refactorings and strict internal improvements,
and changes with no externally observable effect. Teams may use whatever
lightweight planning they prefer for exempt items. The triggers are
properties of the change itself, so they bind without requiring any
estimation practice. (Decision record: D-16.)

6.2 An emergency hotfix may be implemented immediately. WHEN a hotfix alters
behavior covered by an approved spec, the team shall update that spec within
5 working days of the fix shipping.

## 7. Stack profiles

7.1 A profile fills the Design Document's abstract contract slots with one
stack family's vocabulary and defaults. Profiles live under
`standard/profiles/`, one directory per profile, shaped by
[`_TEMPLATE.md`](profiles/_TEMPLATE.md).

7.2 Profiles **may** provide: defaults, vocabulary, and worked examples for
design-document sections.

7.3 Profiles shall **not** add gates, approval steps, artifact types, or
workflow steps, and shall not override this standard. That authority belongs
to this document alone.

7.4 Each profile is owned by the team closest to that stack (its own
CODEOWNERS entry). Every profile change shall have at least one reviewer
from outside the owning team.

7.5 Profiles carry their own semver and shall declare compatibility
(`requires SDD-STANDARD >= X.Y`). Core and profiles release independently.

7.6 A new profile shall cover a stack *family*, never a single team, and
requires standard-owner approval. v1.0 ships exactly one profile:
`backend-services`.

## 8. Compliance checks

8.1 Product repos shall run `ci/check_spec_structure.py` as merge-blocking
CI, using the hosting platform's enforcement mechanism where available
(e.g. required status checks, "pipelines must succeed") — where hard
enforcement is unavailable, the check still runs and a red pipeline is
treated as a blocker by convention.

8.2 Repos shall record their consumed convention version
(`.specify/sdd.json`, written by bootstrap); currency is checked by
`ci/check_convention_version.py`. The same check compares the
constitution's seeded shared-principles block byte-for-byte against the
pinned template (§2.4): any change to the shared block lands upstream by
PR to the standard; repo-specific tightening belongs under the
constitution's repo-principles section.

## 9. Current implementation

9.1 This standard is tool-independent. **GitHub Spec Kit**, pinned to the
exact version in `speckit/PINNED-VERSION`, is the *current implementation*
of the standard — it is not the standard.

9.2 Repos shall adopt the convention only via `bootstrap/init.py`. Manual
copying of templates into repos is prohibited — it creates divergent
dialects.

9.3 A pin change shall land as a reviewed PR to this repository that passes
the full tri-OS verification matrix before any product repo consumes it.

9.4 The exit shall remain a tested capability: CI round-trips
`examples/sample-feature` through `migration/convert.py` on every push. The
round-trip proves structural reversibility of the artifacts; known
conversion gaps against the plan-B tool's own validator are recorded in the
playbook and close as part of executing it. Exit
triggers and the migration procedure are defined in `migration/PLAYBOOK.md`;
trigger reviews are logged in CHANGELOG.md regardless of outcome. The
playbook is the sole operative source of the exit triggers; their
pre-declaration is recorded in DECISIONS.md D-2.

## 10. Scaffold script variant — binding record

10.1 The single scaffold script variant, for all adopting repos, is
**bash (`sh`)**, on all three OS. Bootstrap shall always pass `--script sh` explicitly; relying on
the implementation's OS-dependent default is prohibited (it silently
diverges per OS, and the scaffolded command files hard-code one variant's
paths into the committed repo).

10.2 Decision evidence (gathered 2026-07-02 during development, at Spec
Kit v0.12.3), per the pre-declared rule *"bash unless it fails somewhere
PowerShell passes"* — no such cell exists: a full tri-OS matrix run (6/6
cells green, both variants; the `verify-tri-os.yml` workflow reproduces
it on demand) plus a real-workstation Windows/Git Bash leg.

10.3 Windows workstations shall have a **working** `python3` or `jq`
available in Git Bash before scaffold use (finding LW-1: the WindowsApps
`python3` stub defeats the implementation's JSON parser chain — upstream
[github/spec-kit#3304](https://github.com/github/spec-kit/issues/3304)).
Bootstrap's preflight enforces this; remediation rides the existing uv
prerequisite (see README per-OS notes).

10.4 This record shall be re-evaluated at any pin-forward that materially
changes the script-type offering. *(The pinned v0.12.4 ships a `py`
script type; evaluated 2026-07-04 and **not adopted**. Grounds: `py` is
one release old with no maturity evidence and no cells in the
verification matrix, and its interpreter resolution can select the
Windows Store `python3` stub at scaffold time — the LW-1 failure §10.3
exists to prevent. Watch `py` at future pin-forwards; adopt it only by
amending this record with matrix evidence.)*

## 11. Working language

Specs shall be authored in English. GLOSSARY.md carries Mongolian
translations of key terms. Team ceremonies and discussion remain whatever
the team speaks. ⚠

## 12. Data classification and AI usage

Specs shall contain no credentials, secrets, or personal data. Spec content
inherits its repository's data classification. Agent access to spec content
shall follow the adopting organization's AI usage policy (reference named
by the standard owner at adoption).

## 13. Ownership and versioning of this standard

**The standard owner** is the maintainer or maintainers of the repository
that hosts this standard — a role, never a person. An organization adopting
the standard designates its own standard owner at adoption and records the
binding in its own space; this repository carries no organization-specific
governance. The standard owner: approves changes to this document and to
profiles (§7.6), approves version-pin changes (§9.3), decides exit-trigger
reviews within 5 working days of a fired trigger (§9.4,
`migration/PLAYBOOK.md`), and arbitrates standard-vs-guide conflicts (the
standard wins and the guide gets fixed).

The convention is semantically versioned; every release has a CHANGELOG
entry. Releases shall be 0.x pre-versions until the standard owner declares
the convention stable at 1.0. Changes to this document and to profiles land
by reviewed PR, approved by the standard owner. This section is the sole
definition of the standard-owner role.
