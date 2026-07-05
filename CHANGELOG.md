# Changelog

All notable changes to the SDD convention are documented here.
The convention is semantically versioned; Spec Kit (the current
implementation) is pinned separately in `speckit/PINNED-VERSION`.
Exit-trigger reviews are logged here regardless of outcome.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

Founding content of the convention at 0.1.0-draft. It was developed and
validated before this repository was created — full tri-OS consumption
matrix, a live LW-1 catch on a real Windows workstation — and is being
validated further on demo projects (D-11). Decisions carry stable D-ids
in `DECISIONS.md`.

### Added

- `standard/SDD-STANDARD.md` 0.1.0-draft — the normative standard:
  vocabulary/artifacts, gates & approver roles, EARS/R-id rules (with the
  §4.1 structured fallback, D-15),
  traceability & drift, qualifying-item triggers (⚠, D-16), profile MAY/MAY-NOT,
  compliance checks, current-implementation clauses, the scaffold-variant
  binding record (§10), working language, data classification, and the
  standard-owner role definition (§13). With `standard/GLOSSARY.md`
  (EARS patterns, artifact vocabulary, EN + machine-drafted MN pending
  native review).
- Profiles: `standard/profiles/_TEMPLATE.md` and
  `standard/profiles/backend-services/` 0.1.0-draft (thin: sync + async
  contract table shapes, worked examples). Profiles provide defaults and
  vocabulary only — never gates.
- Spec Kit pin `v0.12.4` (`speckit/PINNED-VERSION`), the standard's preset
  `speckit/presets/sdd/` 0.1.0 (four template overrides, all strategy
  **replace**; no command or script overrides), and the review extension
  `speckit/extensions/sdd/` 0.1.0 (`speckit.sdd.review`,
  `after_implement` hook, non-optional, hard-forbidden from writing
  Status lines).
- `bootstrap/init.py` — the only supported adoption path: preflight that
  *executes* the JSON parser instead of locating it (LW-1: fails loud with
  the exact remediation), pinned `specify init` via `uv tool run`, preset +
  review-extension install, shared-constitution repair with the chosen
  profile appended, and the `.specify/sdd.json` consumption marker.
- CI gates: `ci/check_spec_structure.py` (`--self`/`--repo` — Status lines
  with `—` or `-` accepted, gate order, R-id uniqueness, `[R-n]` validity,
  kebab-case filenames, LF endings) and `ci/check_convention_version.py`
  (convention currency vs an sdd-standard checkout, plus the seeded
  constitution's shared-principles block diffed against the pinned
  template — §2.4 machine-checked, D-17 — remediation on
  mismatch). Workflows: `checks.yml` (structure check + converter
  round-trip on every push/PR) and `verify-tri-os.yml` (full consumption
  flow on all 6 {ubuntu, windows, macos} × {sh, ps} cells, including a
  negative probe asserting the gate goes red on a skipped approval).
- `examples/sample-feature` — transfer-limit-alerts: the teaching example
  (8 EARS requirements, both profile contract sections exercised, all
  statuses APPROVED) and the converter's CI fixture.
- The tested exit: `migration/PLAYBOOK.md` (trigger→review→decision flow
  for the five pre-declared exit triggers, Spec Kit→OpenSpec mapping,
  execution steps, rollback — written while calm) and
  `migration/convert.py` (feature folder ↔ OpenSpec change structure,
  lossless via an `sdd-preamble` fence; `--reverse` and `--round-trip`
  gated in CI).
- Docs (informative, never binding): `docs/quickstart.md`,
  `docs/reviewing-specs.md`, `docs/adopting-a-repo.md`, `docs/faq.md`
  scaffold.
- `DECISIONS.md` — the decision registry: stable D-ids (never renumbered,
  never reused), supersessions tracked in place with dated notes; rows
  point at where each decision's record and rationale live.

### Decided

The registry indexes all decisions with stable D-ids; those whose record
lives in this changelog (rather than in a standard section) are recorded
below.

- **All repo tooling is one cross-platform Python implementation** (D-6):
  stdlib + pathlib only, run via `uv run` — never `.sh`/`.ps1` twins;
  every failure message carries the exact remediation command.
- **Artifact filenames follow stock Spec Kit naming** (D-9: `spec.md`,
  `plan.md`, `tasks.md`); the standard's vocabulary lives inside the
  documents via preset template overrides and the glossary's mapping
  table. **Premise on record:** justified by the exit being a *tested*
  capability (D-2); if `migration/` rots, the premise fails and the
  decision must be revisited.
- **Scaffold script variant: bash (`sh`), for all adopting repos, all
  three OS** (D-10) — per the pre-declared rule (bash unless it fails
  where PowerShell passes; no such cell in the matrix). Binding record,
  including the evaluation of the pinned version's `py` script type
  (not adopted), in SDD-STANDARD §10.
- **Validation happens on demo projects** (D-11); introduction to an
  organization is a separate, later decision with its own approval.
- **A single-file decision registry, not an ADR directory** (D-12):
  settled decisions get stable D-ids in `DECISIONS.md`; sparse per-file
  records only if a future decision has no natural home. Rationale in the
  D-12 note.
- **The repository is organization-neutral** (D-13): no organization
  names, governance bodies, org structure, personnel, or
  org-infrastructure facts live in this repo; organization-specific
  bindings (standard-owner designation, approver names, policies,
  hosting) happen at adoption.
- **The plan-B slot holds two pre-declared candidates** (D-14): OpenSpec
  (the tested exit: converter + CI round-trip) and chartering an in-house
  implementation of the standard, spec'd at review time and never
  pre-built. Exit trigger 5 covers upstream retiring or breaking the
  supported override points. Operative wording in `migration/PLAYBOOK.md`
  §1; rationale in the D-14 note.
- **EARS is the requirements notation** (D-15): §4.1 binds one testable
  behavior + a stable R-id, phrased in EARS, with a narrow
  structured-fallback escape hatch (mathematical content, >3
  preconditions). Rejected: stock Spec Kit user stories + Given/When/Then,
  Gherkin-as-primary, plain ISO-29148 shall statements, Planguage, FRET.
  Evidence, the recorded evidence gap on LLM codegen, and revisit triggers
  in the D-15 note.
- **Qualifying work items are defined by property triggers, not estimated
  size** (D-16, ⚠ starting default): spec ceremony binds WHEN a change
  creates or alters externally observable behavior or a contract, crosses a
  repo/service/team boundary, contains a hard-to-reverse step, or
  introduces a new capability — the "3 story points" threshold is
  withdrawn (story points are undefined for non-estimating teams and
  self-reported; §1 scopes estimation ceremonies out). The D-16 row is the
  ⚠ tracker.
- **The seeded constitution is thin context, not enforcement** (D-17): a
  version-stamped pointer to the standard plus the generation-time
  principles (gates are human, no silent drift, spec hygiene/language),
  replacing the 7-principle restatement of the standard;
  `ci/check_convention_version.py` diffs the seeded shared block against
  the pinned template, making §2.4 machine-checkable. Rationale and
  upstream evidence in the D-17 note.
