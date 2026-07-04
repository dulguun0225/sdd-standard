# Migration playbook — Spec Kit → OpenSpec

Written while calm, before any trigger has fired. The pre-declared, tested
plan B is **OpenSpec**
([Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec), MIT); a
trigger review also weighs a second pre-declared candidate — **chartering
an in-house implementation** of the standard (outcome 4 below; D-14). The
methodology (EARS, R-ids, human gates, co-located specs) is the standard;
only the current implementation (SDD-STANDARD §9) is being replaced, so
nothing in `standard/` changes in a migration.

`migration/convert.py` round-trips `examples/sample-feature` on every push
and PR (checks.yml and the tri-OS matrix) — if this playbook's tooling
rots, CI goes red long before anyone needs it (SDD-STANDARD §9.4).

## 1. Triggers → review → decision

Any trigger below **convenes** a migration review; it does not decide it.
The standard owner convenes within 5 working days of the trigger
being noticed, with representatives of the adopting repos' teams. The
review picks exactly one outcome and logs it in CHANGELOG.md **regardless
of outcome** — including "reviewed, staying put".

| # | Trigger | Typical first check |
| - | ------- | ------------------- |
| 1 | Upstream stall: no Spec Kit release or substantive commit for 2 consecutive months, or maintainer departure without named replacement | github.com/github/spec-kit commit graph and releases; the weekly verify-tri-os heartbeat failing on upstream fetch is an early hint |
| 2 | Blocking defect: critical bug in the pinned version unresolved 6+ weeks with no safe pin-forward | Issue tracker at the pin; the matrix run for every candidate pin-forward |
| 3 | Agent regression: a release drops/breaks an agent in active use by an adopting team with no fix within one release cycle | The affected team's repro; the adopting repos' teams say which agents are in active use |
| 4 | Usage verdict: real usage (demo projects or adopting repos) concludes the tool — not the methodology — is the obstacle | The users' concrete evidence: what the tool blocked, and why no preset/extension patch could fix it |
| 5 | Override-point retirement: an upstream release retires or breaks the supported customization mechanisms this layer depends on (preset template overrides, extension hooks) with no replacement | The pin-forward matrix run; upstream release notes and PRs touching presets/extensions; SDD-STANDARD §10.4's `py`-variant watch item is an early hint of script-layer churn |

Outcomes, in order of preference:

1. **Pin and wait** — the pin already isolates us; record the watch item
   and a re-review date.
2. **Patch via extension/preset** — fix at our layer using supported
   override points only; lands as a reviewed PR through the full matrix.
3. **Execute this playbook** — migrate to OpenSpec, §3 below.
4. **Charter an in-house implementation** — only ever a review outcome,
   never pre-built in anticipation: the convention, not the tooling, is
   the product. It starts as its own spec'd project under this standard
   (requirements gate first), sized against the tool surface real usage
   actually exercised — not against everything Spec Kit ships.

## 2. Artifact mapping

| Standard artifact (Spec Kit shape) | OpenSpec home | How |
| ---------------------------------- | ------------- | --- |
| `specs/NNN-slug/spec.md` (Requirements Document) | `openspec/changes/<slug>/specs/<slug>/spec.md` + generated `proposal.md` | `convert.py` — R-id bullets become `### Requirement:` blocks; standard metadata (Status line, field table) preserved in an `sdd-preamble` fence |
| `specs/NNN-slug/plan.md` (Design Document) | `openspec/changes/<slug>/design.md` | `convert.py` — verbatim; profile contract tables are plain prose and migrate untouched (migration-isolation rule) |
| `specs/NNN-slug/tasks.md` (Task List) | `openspec/changes/<slug>/tasks.md` | `convert.py` — verbatim; checkbox markdown either way |
| `.specify/memory/constitution.md` | `openspec/project.md` (conventions section) | Human step: shared principles are pasted into project conventions; they are tool-independent prose |
| Gates & Status lines | No OpenSpec equivalent | The standard's §3 still applies — approvals stay Status lines inside the artifacts (preserved by the converter); `ci/check_spec_structure.py` keeps enforcing them, it reads markdown, not Spec Kit |
| `.specify/scripts`, commands, preset, extension | Dropped | OpenSpec has its own CLI (`openspec`); the review phase becomes a documented step until an equivalent hook exists |

What is deliberately **not** migrated: completed/archived features stay as
plain markdown wherever they are — the exit-cost promise is that specs
remain readable documentation with no tooling at all.

## 3. Execution steps

Run on a branch in each affected repo; one repo end-to-end first (this
repo's `examples/sample-feature` is the rehearsal fixture, then one real
adopting repo), then fan out.

1. **Freeze**: announce the migration window (§4); merge or park open spec
   PRs in the repo being migrated.
2. **Convert** every active feature folder:
   `uv run migration/convert.py specs/NNN-slug <repo-root>` — outputs under
   `openspec/changes/`. Verify each with
   `uv run migration/convert.py --round-trip specs/NNN-slug` first.
3. **Constitution**: create `openspec/project.md`; paste the shared
   principles and repo principles from `.specify/memory/constitution.md`.
4. **Install OpenSpec** per its README at the version the standard owner
   pins (a new `PINNED-VERSION` under a new `openspec/` implementation dir
   in this repo — the pin discipline of SDD-STANDARD §9 is
   tool-independent).
5. **CI**: `ci/check_spec_structure.py` keeps running unchanged on the
   still-present markdown artifacts (it has no Spec Kit dependency);
   `check_convention_version.py` gets a follow-up for the new marker file.
6. **Remove** `.specify/` once the team's agent commands are re-pointed;
   archive, don't delete, on the migration branch.
7. **Verify**: the repo's spec CI gate green; one feature taken through
   requirements → review on the new tool by the repo's own team before the
   migration is declared done for that repo.

## 4. Communications

- The convened review's outcome goes to every adopting repo's team the same
  day, with the CHANGELOG entry linked.
- If outcome 3 is chosen: a migration window per repo (target: one sprint),
  the freeze rules above, and a named migration owner per adopting repo (or
  group of repos).
- `docs/faq.md` collects migration questions; the standard owner answers
  within 1 working day during the window.

## 5. Rollback

The migration branch is the rollback: `.specify/` is archived on it, not
deleted, and the pre-migration pin still lives in `speckit/PINNED-VERSION`
history. Rolling back a repo is `git revert` of the migration merge plus
re-running `bootstrap/init.py` on a scratch clone to confirm the old stack
still scaffolds (the matrix verifies this weekly regardless). Specs
themselves never need rolling back — both shapes are plain markdown and the
converter reverses losslessly (`--reverse`).
