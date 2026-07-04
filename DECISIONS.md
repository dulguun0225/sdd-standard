# Decision registry

**Informative.** This file is an index over decision records, not a home
for them: each row points at where the decision and its rationale actually
live (a CHANGELOG entry, an SDD-STANDARD section, this file's notes). It
exists so decisions stay findable and citable across document rewrites and
repo moves. It records; it never legislates — in any conflict, the linked
record wins.

Rules (mirroring the R-id discipline of SDD-STANDARD §4):

- **D-ids are stable**: never renumbered, never reused. Superseded or
  withdrawn decisions stay listed with their state changed and a dated
  note — rows are never deleted.
- A row's Decision, Date, and Authority cells are never edited after the
  fact; only State and Record pointers change, with a dated note below.
- A PR that settles, supersedes, or withdraws a decision updates this
  index in the same PR as its CHANGELOG entry.
- The column is named **State**, not Status — "Status" stays reserved for
  the gate-approval lines of SDD-STANDARD §3.2.
- ⚠ marks the standard's starting defaults (SDD-STANDARD preamble): the
  standard owner amends them by reviewed PR as real usage teaches.

## Index

Founding decisions, made during the convention's development and recorded
at the creation of this repository.

| ID | Decision | Date | Authority | State | Record |
| -- | -------- | ---- | --------- | ----- | ------ |
| D-1 | GitHub Spec Kit is the current implementation of the standard. Rejected: Kiro, OpenSpec-as-primary, BMAD, Superpowers | 2026-07-04 | Repo owner (founding) | Settled | [SDD-STANDARD §9](standard/SDD-STANDARD.md) |
| D-2 | Exit triggers pre-declared; the exit is a tested capability (converter + CI round-trip), never an intention | 2026-07-04 | Repo owner (founding) | Settled | [migration/PLAYBOOK.md](migration/PLAYBOOK.md) (operative wording); [SDD-STANDARD §9.4](standard/SDD-STANDARD.md) |
| D-3 | The convention is a versioned shared library: semver, CHANGELOG, releases stay 0.x until the standard owner declares 1.0 | 2026-07-04 | Repo owner (founding) | Settled | [SDD-STANDARD §13](standard/SDD-STANDARD.md) |
| D-4 | Specs live in each product repo next to the code they govern; no central specs repository | 2026-07-04 | Repo owner (founding) | Settled | [SDD-STANDARD §2](standard/SDD-STANDARD.md) |
| D-5 | Stack profiles are subordinate to the standard: defaults and vocabulary only — never gates, approval steps, or artifact types | 2026-07-04 | Repo owner (founding) | Settled | [SDD-STANDARD §7](standard/SDD-STANDARD.md) |
| D-6 | All repo tooling is one cross-platform Python implementation (stdlib + pathlib, `uv run`); never `.sh`/`.ps1` twins | 2026-07-04 | Repo owner (founding) | Settled | [CHANGELOG](CHANGELOG.md) "Decided" |
| D-7 | Working language: specs are authored in English; GLOSSARY.md carries Mongolian translations of key terms | 2026-07-04 | Repo owner (founding) | Starting default ⚠ — see note | [SDD-STANDARD §11](standard/SDD-STANDARD.md) |
| D-8 | The spec is the source of truth for requirements detail; work-tracker items carry a summary and a link, never duplicated acceptance criteria | 2026-07-04 | Repo owner (founding) | Starting default ⚠ — see note | [SDD-STANDARD §4](standard/SDD-STANDARD.md) |
| D-9 | Artifact filenames follow stock Spec Kit naming (`spec.md`, `plan.md`, `tasks.md`); the standard's vocabulary lives inside the documents | 2026-07-04 | Repo owner (founding) | Settled — premise on record, see note | [CHANGELOG](CHANGELOG.md) "Decided" |
| D-10 | Scaffold script variant: bash (`sh`), for all adopting repos, all three OS | 2026-07-04 | Repo owner (founding) | Settled — see note | [SDD-STANDARD §10](standard/SDD-STANDARD.md) (binding record); [CHANGELOG](CHANGELOG.md) "Decided" |
| D-11 | Validation happens on demo projects; introduction to an organization is a separate, later decision with its own approval | 2026-07-04 | Repo owner (founding) | Settled | [CHANGELOG](CHANGELOG.md) "Decided" |
| D-12 | Decisions are indexed in this single-file registry with stable D-ids; sparse per-file records only if a future decision has no natural home | 2026-07-04 | Repo owner (founding) | Settled — see note | This file; [CHANGELOG](CHANGELOG.md) "Decided" |
| D-13 | The repository is organization-neutral: it contains only the standard, its tooling, and processes — no organization names, governance bodies, org structure, personnel, or org-infrastructure facts. Organization-specific bindings (standard-owner designation, approver names, policies, hosting) happen at adoption | 2026-07-04 | Repo owner (founding) | Settled | [SDD-STANDARD §13](standard/SDD-STANDARD.md); [CHANGELOG](CHANGELOG.md) "Decided" |
| D-14 | Exit-trigger reviews weigh two pre-declared plan-B candidates: OpenSpec (the tested exit) and chartering an in-house implementation of the standard (spec'd at review time, never pre-built). Trigger 5 covers upstream retiring or breaking the supported override points | 2026-07-04 | Repo owner (founding) | Settled — see note | [migration/PLAYBOOK.md](migration/PLAYBOOK.md) §1 (operative wording); [CHANGELOG](CHANGELOG.md) "Decided" |

## Notes

- **D-7, D-8**: starting defaults ⚠ pending explicit confirmation.
  Confirmation comes from demo-project usage (D-11), amended by the
  standard owner per the ⚠ rule. Nothing else tracks that these are
  unconfirmed — these rows are the tracker.
- **D-9**: premise on record — the decision is justified by the exit
  being a *tested* capability (D-2). If `migration/` rots, the premise
  fails and the decision must be revisited.
- **D-10**: the pinned Spec Kit (v0.12.4) ships a `py` script type;
  evaluated 2026-07-04 and not adopted — it is one release old with no
  maturity evidence, has no cells in the verification matrix, and its
  interpreter resolution can bake the Windows Store `python3` stub (LW-1)
  into scaffolded commands. Grounds in SDD-STANDARD §10.4's note; watch
  at future pin-forwards.
- **D-12**: evaluated against external practice: small standards repos
  keep rationale in the spec text and history in a changelog; per-file
  ADR directories stall at 1–5 files in roughly half of observed
  adoptions (Buchgeher et al. 2023); the load-bearing properties of every
  strong scheme are never-edit-after-approval and never-renumber, which a
  registry row honors as well as a file. Trigger to revisit: decision
  volume or rationale length outgrowing one file.
- **D-14**: the convention's only hard coupling to Spec Kit is the
  supported override points (preset template overrides, extension hooks);
  if upstream retires them, the "patch at our layer" review outcome stops
  existing, so their retirement is exit trigger 5. The in-house candidate
  is deliberately **not** built in advance: the convention, not the
  tooling, is the product, and building early would front-load solo
  maintenance into commodity machinery (agent-integration churn,
  scaffolding) that upstream currently absorbs. It becomes rational only
  if a trigger fires or demo validation shows a thin actually-used tool
  surface — so during validation, pin-forward pain and which Spec Kit
  features get exercised are noted informally (CHANGELOG observations,
  not pilot machinery).
