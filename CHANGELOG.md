# Changelog

All notable changes to the SDD convention are documented here.
The convention is semantically versioned; Spec Kit is pinned separately in
`speckit/PINNED-VERSION`.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- The teaching corpus: `docs/` now covers every seat of the lifecycle
  (informative throughout; org-neutrality D-13 intact — the cast is
  fictional, extending the teaching example's own names).
  - `docs/feature-walkthrough.md` — "who does what, when": the teaching
    example replayed as a team runs it — roles bound to a cast, a
    gates-onto-PRs shape, a requirements-gate rejection, a
    mid-implementation same-PR amendment, the review phase feeding the
    Review gate, hotfix/exempt/spike variations, and a one-page
    who/what/how/when table. It also names, honestly, the one mechanic
    the standard leaves to the team's working agreement: which file
    carries the Review gate's Status line.
  - `docs/writing-requirements.md` — the author's guide to `spec.md`: a
    realistic agent draft carrying the standard defects (smuggled
    "and", judgment words, triggers the system never observes,
    undefined terms smuggling features, happy-path bias) shaped move by
    move into the approved teaching example; choosing the EARS pattern;
    the testable-not-prophetic bar; a pre-gate checklist mirroring the
    approver's.
  - `docs/writing-design.md` — the author's guide to `plan.md`:
    contract rows readable from the caller's seat, stable error codes
    traced to IF/THEN requirements, the stated-or-default silence rule
    applied at authoring time (silence as a deliberate claim; the
    Idempotency cell never silent), schema links that must resolve,
    decisions carrying their rejected alternative, the phase plan as
    the Task List's skeleton.
  - `docs/writing-tasks.md` — the author's guide to `tasks.md`: slicing
    to one-sitting-verifiable tasks, `[R-n]` coverage walked both
    directions, evidence designed at authoring time (with a bad→good
    evidence table), explicit dependencies, stable T-ids.
  - `docs/README.md` — the guide index: a "you want to… → read" table
    and reading paths per seat (everyone, authors, approvers, team
    leads).
  Cross-linked throughout: the README lifecycle section points at the
  index; the quickstart, feature-walkthrough, and adopting-a-repo point
  at the writing guides at the step where each applies; each
  reviewing-specs gate section points at its author-side guide.

### Changed

- `docs/adopting-a-repo.md` — the prerequisites section becomes "What
  you need, and why": the convention's requirements listed as
  capabilities with their rationale (a git host with a review flow —
  approvals are commits, the same-PR rule needs the PR unit; one CI job
  on push/PR — the §8.1 merge gate; merge blocking where the plan has
  it, with §8.1's honest fallback; uv + git per machine — one Python
  implementation, pinned Spec Kit via `uv tool run`; the pinned
  sdd-standard clone — one dialect at a known version; any tracker —
  summary + link only), plus what is deliberately not required (no
  specific CI vendor, agent, IDE, central specs repo, or approval bot).
  The CI-gate section gains a Jenkins example alongside GitHub Actions
  and GitLab CE, with the run-vs-block distinction spelled out.
- Editorial readability pass, no normative or behavioral change. The
  informative guides (quickstart, reviewing-specs, adopting-a-repo,
  evolving-requirements) and the README are rewritten for fast
  comprehension: short sentences, everyday words, concrete wording.
  SDD-STANDARD gets punctuation-level splits only (§4.1,
  §8.1, §8.2, §13 — long clauses broken at existing dashes and
  semicolons, wording untouched). The §10 decision records and all
  dated amendment notes remain verbatim.
- Second editorial pass, same rules, no normative or behavioral change.
  The README lifecycle section, `docs/feature-walkthrough.md`, and
  `docs/faq.md` get their remaining long stacked sentences split. The
  distributed prose is included this time: the preset README, the
  `speckit.sdd.review` command text, and the guidance prose of the four
  seeded templates. The constitution template's drift-checked "Shared
  principles" block stays byte-identical; only its intro is reworded.
  The approved teaching example (`examples/sample-feature`) is left
  verbatim — approved artifacts are never silently edited.

## [0.3.0-draft] - 2026-07-20

The pin-forward release: Spec Kit v0.12.4 → v0.13.0 through the full
tri-OS matrix, with the pinned-version facts re-verified against source.
LW-1's scaffold-runtime leg is fixed upstream, so §10.3 relaxes from a
preflight-enforced gate to a recommendation — the one normative change.
Also: the glossary's Mongolian translations are native-reviewed.

### Changed

- Spec Kit pin v0.12.4 → v0.13.0 (per SDD-STANDARD §9.3: reviewed PR
  plus the full tri-OS matrix). Pinned-version facts re-verified against
  the v0.13.0 source: `specify init` now seeds the constitution *after*
  preset install from the preset's own constitution-template (upstream
  #3276) — bootstrap's `seed_constitution` remains as the
  placeholder-filling overwrite; scaffold template resolution is now
  layered and manifest-aware, degrading to path-convention replace-only
  without a working python3 + PyYAML — the preset stays all-replace
  deliberately; `--integration generic` still requires `--commands-dir`.
  LW-1's scaffold-runtime leg is fixed upstream (spec-kit#3304 via
  #3312/#3320, in by v0.12.9): the scripts fall through to grep/sed/awk
  on parser failure, so bootstrap's Windows JSON-parser preflight
  downgrades from a hard failure to a warning and SDD-STANDARD §10.3 is
  amended from a preflight-enforced gate ("shall") to a recommendation
  (dated amendment in §10.3). The §10.4 `py` script-type record is
  re-evaluated (D-10 note): matured upstream (#3385 fixed the
  stub-baking interpreter resolution) yet still not adopted — no
  verification-matrix cells, single-variant rule. Preset 0.3.1 and
  review extension 0.2.1: `requires.speckit_version` widened to
  `<0.14.0`, which the previous bound excluded.
- GLOSSARY.md: the Mongolian translations are native-reviewed and
  approved (2026-07-20). The machine-draft caveat is resolved — the
  provenance note now records the review, and the "(ноорог)" draft
  markers on the Mongolian term columns are removed. This closes the
  "machine-drafted MN pending native review" note from the 0.1.0-draft
  entry; the note's earlier 2026-07-05 review date was premature and is
  corrected.

## [0.2.0-draft] - 2026-07-20

Developed during demo validation (D-11). Two threads: vendor-neutrality
abandoned for simplicity — GitHub Spec Kit is the sole implementation of
the standard (D-18) — and research-grounded hardening against
AI-implementer failure modes: the backend-services profile's
stated-or-default contract reading, the review extension's
silence-conformance step, deterministic structure checks, point-of-use
template nudges, and the profile's full text shipped into product repos.

### Added

- `ci/check_spec_structure.py` grows two merge-blocking checks and one
  advisory: **contract-link existence** (every local `contracts/…` path a
  feature's plan.md references must exist in that feature's spec folder;
  URLs and registry references are out of scope) — hallucinated schema
  links are the measured API-knowledge-conflict defect class, ~20–26% of
  hallucinations (ACM TOSEM 10.1145/3728894; arXiv:2404.00971);
  **layer congruence** (`--self` only: the plan-template's contract-table
  headers must match the backend-services profile's column lists —
  multi-layer redundant specs help only while the layers agree; drifted
  layers actively hurt, arXiv:2604.24712); and a **vague-word WARNING**
  (never merge-blocking) on spec.md requirement bullets ("quickly",
  "appropriate", …) — lexical vagueness survives well-formed EARS, and a
  deterministic grep beats LLM ambiguity-flagging's ~50% precision
  (arXiv:2604.21505); advisory output for the human Requirements
  approver. Extending the merge gate's scope is standard-adjacent: this
  entry plus standard-owner PR approval is its record.
- `examples/sample-feature/contracts/` — the two event schemas the
  example's plan.md always referenced now exist, teaching the profile's
  default schema location (and satisfying the new contract-link check).
- Review extension 0.2.0: the review command's contract check gains a
  **silence-conformance** step — where a contract cell is silent, it
  verifies the code implements the profile default (cursor pagination,
  compare-and-set, durable dedup on `event_id`, dead-letter never drop,
  atomic publish-with-state-change, existence-safe not-entitled) rather
  than a guess, and flags every mutating operation whose Idempotency cell
  is empty (no safe default — profile §2) as a named question. Findings
  land in review-notes.md; zero new gates — the command still only
  informs the human Review approver and never writes Status lines.
  Ground: agents violate explicit constraints in 40.4% of confirmed
  real-world failures (arXiv:2605.30777) — verification, not document
  volume, secures compliance.
- Preset 0.3.0 — point-of-use nudges (the D-17 pattern): the
  spec-template's §3 comment sends the drafting agent through the
  profile's standard failure cases for the IF/THEN rows (missing corner
  cases are the #2 LLM bug pattern at 15.27%, #1 for the strongest model
  studied — arXiv:2403.08937); the tasks-template favors many small,
  independently verifiable tasks over few large ones (per-step errors
  compound; smallest-verifiable-subtask decomposition with independent
  verification approaches zero error at scale — arXiv:2511.09030).
  `docs/reviewing-specs.md` (informative) gains the Requirements
  approver's ambiguity checklist — ambiguity is removed upstream by
  humans or nowhere (arXiv:2604.21505; arXiv:2607.00711).
- D-11 note (2026-07-18): three research-informed demo-validation
  observables — silence-conformance, review-notes catches, lexical
  vagueness. D-15 note (2026-07-18): the honest evidence gap narrows
  (spec misinterpretation confirmed as the dominant LLM defect class
  across four peer-reviewed taxonomies), not closes — no controlled
  study isolating EARS itself yet.
- D-11 note (2026-07-20): observable (5) of the 2026-07-05 note — one
  converter `--round-trip` on a real demo feature — recorded as lapsed
  with D-18, which withdrew `migration/` and the converter but did not
  amend the observable list. Observables (1)–(4) and (6)–(8) stand.

- README section "The lifecycle in a product repo" — the end-to-end map
  of the normative rules in an adopting repo: the qualification
  decision, the gate diagram with who-does-what markers, the approver
  table, and the enforcement rules underneath. The diagram draws the
  whole loop in one picture: alongside the hotfix bypass and
  gate-rejection edges, a spike/prototype detour off `spec.md` (§6.1)
  and a learning edge from Done back to the next work item (§5.2, §4.2).
- `docs/evolving-requirements.md` — informative guide to the
  spec → build → learn loop: testable-not-airtight (§4.1), amendments in
  the same PR (§5.2, §4.2), spiking under the §6.1 exemption, and the
  wrong-altitude / too-thick diagnostics. It walks the README diagram
  rather than carrying its own. Linked from the quickstart; the question
  that prompted it is seeded as the first FAQ entry.

### Changed

- `bootstrap/init.py` installs the chosen profile's full text into the
  product repo (`.specify/memory/profile.md`, next to the constitution),
  and the constitution's stack-profile block now points at that local
  copy. This closes the gap noted in the preset 0.2.0 entry below — the
  profile file itself was absent from product repos, so its silence
  defaults never reached an implementing agent's context beyond the
  compressed template comments; embedding the relevant knowledge in the
  generation context is the strongest measured hallucination mitigation
  (arXiv:2404.00971). `ci/check_convention_version.py` keeps the copy
  honest: compared byte-for-byte against the standard's profile at the
  pinned release, same mechanism as the constitution's shared-block
  check (D-17 precedent) — profile changes land upstream by PR, never by
  editing the copy. SDD-STANDARD §8.2 amended accordingly; the tri-OS
  matrix gains a drifted-profile-copy negative probe. Preset 0.2.1: the
  plan-template's contract-slot comments point at the local profile copy.
- `backend-services` profile 0.2.0-draft — from thin table shapes to a
  full default set. New: the **stated-or-default reading rule** (silence
  in a Design Document contract reads as the profile default, never as
  implementer's choice); silence defaults for auth, pagination,
  concurrency, atomicity, delivery semantics, ordering, dead-lettering,
  and schema evolution; a contract vocabulary; the ten standard failure
  cases; extended worked examples; stack-family wording widened from
  "microservices" to any deployment shape. Grounds — adversarially
  verified findings on AI-implementer failure modes: misreading the spec
  and missing corner cases dominate LLM-generated bugs, models fill
  unstated detail with the statistically common training-data pattern
  rather than flagging the gap, and explicit contract tables target the
  measured API-misuse defect class (arXiv:2403.08937; ACM TOSEM
  10.1145/3728894; arXiv:2407.06153) — plus contract conventions
  observed in a production backend codebase. `_TEMPLATE.md` gains the
  optional "Contract vocabulary" section the profile now uses.
- Preset 0.2.0: the plan-template's two contract-slot comments now carry
  the profile's silence defaults at point of use (the D-17
  point-of-use pattern — the profile file itself is not present in
  product repos, the seeded template is).
- SDD-STANDARD §9 renamed "Current implementation" → "Implementation":
  GitHub Spec Kit is now stated as *the* implementation of the standard,
  not one swappable option. §9.1's tool-independence claim and §9.4 (the
  tested-exit requirement) are removed (D-18).

### Removed

- The vendor-neutrality / exit apparatus (D-18): `migration/` (the OpenSpec
  converter `convert.py` and the plan-B `PLAYBOOK.md`), the pre-declared
  exit triggers, and the converter round-trip CI step in `checks.yml` and
  `verify-tri-os.yml`. `examples/sample-feature` stays the teaching example,
  no longer doubling as the converter fixture — it is kept fresh by
  `check_spec_structure.py --self`. Org-neutrality (D-13) is unaffected.

### Decided

- **Vendor-neutrality abandoned for simplicity and ease** (D-18): GitHub
  Spec Kit is the sole implementation of the standard. The tested exit
  (converter + CI round-trip), the plan-B candidates (OpenSpec, in-house),
  and the pre-declared exit triggers are withdrawn — superseding D-2 and
  D-14 and simplifying D-1 and D-9's premise. The trade is explicit: no
  tested escape hatch remains; if Spec Kit or its supported override points
  fail, an exit is rebuilt then, not kept warm. Org-neutrality (D-13) is
  retained. Rationale in the D-18 note.

## [0.1.0-draft] - 2026-07-05

Founding content of the convention. It was developed and
validated before this repository was created — full tri-OS consumption
matrix, a live LW-1 catch on a real Windows workstation — and is being
validated further on demo projects (D-11, pre-declared observables in the
D-11 note). Decisions carry stable D-ids
in `DECISIONS.md`. Includes the founding amendment (#1): D-15 (EARS
notation with the §4.1 structured fallback), D-16 (property-trigger
qualifying rules), D-17 (thin seeded constitution with the shared-block
drift check).

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
