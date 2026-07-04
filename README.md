# sdd-standard

A spec-driven development (SDD) convention for an engineering
organization — versioned, reviewed, and distributed from this repository.

The convention itself is the product here. It is treated like a shared
library: semantic versioning on the convention, a changelog, code owners, and
changes by PR review. Product repos consume it via a bootstrap wrapper; specs
always live in each product repo next to the code they govern — there is
deliberately no central specs repository.

[GitHub Spec Kit](https://github.com/github/spec-kit) is the *current
implementation* of the standard — it is not the standard itself. The
approved version is pinned in `speckit/PINNED-VERSION`; upgrades are
tested in this repo first. A tested migration path to
[OpenSpec](https://github.com/Fission-AI/OpenSpec) ships with v1.0, not
later.

## Why not stock Spec Kit?

Stock Spec Kit is a workflow tool: it walks an AI agent from spec through
plan and tasks to implementation. Nothing in it says who approves an
artifact, how requirement ids stay stable over time, or what happens when
code drifts from an approved spec. The convention layers those rules on top —
through Spec Kit's supported preset and extension mechanisms, no forks —
and keeps the tool replaceable. What it adds
([SDD-STANDARD](standard/SDD-STANDARD.md), § references below):

- **Human gates.** Artifacts pass Requirements → Design → Tasks gates
  before implementation and a Review gate after. Only a human approver
  passes a gate, by adding the `Status: APPROVED` line in their own
  change — agents never write Status lines, and the Review approver is
  never the implementer (§3).
- **Requirements that stay put.** Every requirement is one testable EARS
  behavior with a stable R-id — never renumbered, never reused; withdrawn
  ones stay listed. Acceptance criteria live in the spec alone; tracker
  items carry a summary and a link (§4).
- **Traceability with teeth.** Every task carries at least one `[R-n]`
  reference, and a change that alters spec-covered behavior updates that
  spec in the same PR. `ci/check_spec_structure.py` enforces the
  structure as merge-blocking CI — an artifact that outruns its approvals
  (a plan without an APPROVED spec, tasks without an APPROVED plan, a
  missing Status line) turns the pipeline red (§5, §8).
- **One dialect, not one per team.** Repos adopt only via
  `bootstrap/init.py` at the pinned, tri-OS-tested version: shared
  constitution seeded (repos append principles, never weaken them), stack
  profile appended, no hand-copied templates quietly diverging (§2.4, §7,
  §9).
- **A review phase.** After implementation, the review
  extension (`speckit.sdd.review`) compares what was built against
  the approved artifacts and writes notes for the human Review approver —
  input to the Review gate (§3), never a pass of it.
- **A pressure valve.** Below the size threshold there is no spec
  ceremony, and emergency hotfixes ship first and update the spec after —
  the ceremony binds where it pays, not everywhere (§6).
- **A tested exit.** CI round-trips the example spec through the OpenSpec
  converter on every push, so leaving Spec Kit remains a capability, not
  a rewrite (§9.4).

## Status

**Pre-1.0 (0.1.0-draft), complete and usable.** This repository is the standard
and its tooling — nothing else. It is being validated on demo projects;
adoption of the convention by real teams is a separate, later decision with
its own approval. Settled decisions are indexed with stable D-ids in
[DECISIONS.md](DECISIONS.md).

**Standard owner:** the maintainer(s) of this repository — a role, never a
person, defined in
[SDD-STANDARD §13](standard/SDD-STANDARD.md#13-ownership-and-versioning-of-this-standard).
An organization adopting the standard designates its own standard owner at
adoption. v1.0 is declared by the standard owner when real usage has earned
it.

## Layout

| Path         | Purpose                                                        |
| ------------ | -------------------------------------------------------------- |
| `standard/`  | The normative documents: SDD-STANDARD.md, stack profiles, glossary |
| `speckit/`   | Version pin, the standard's preset, extensions (current implementation layer) |
| `bootstrap/` | `init.py` — how a product repo adopts the convention (run via `uv run`) |
| `ci/`        | Structure and version checks — same scripts locally and on CI  |
| `docs/`      | Informative guides only — they explain, never legislate        |
| `examples/`  | Complete exemplary spec; doubles as the converter's CI fixture |
| `migration/` | Plan-B playbook and artifact converter (Spec Kit → OpenSpec)   |

## Per-OS setup notes

The single scaffold script variant is **bash (`sh`)** on all three OS —
decided from the tri-OS matrix evidence, recorded in
[SDD-STANDARD §10](standard/SDD-STANDARD.md#10-scaffold-script-variant--binding-record).
Every OS needs [uv](https://docs.astral.sh/uv/) and git; Spec Kit itself is
installed pinned by `bootstrap/init.py` — never install it by hand.

- **Windows**: Git Bash ships with Git for Windows — no extra shell needed.
  One pitfall: the scaffold scripts need a **working** `python3` or `jq` in
  Git Bash, and stock Windows only has the Microsoft-Store `python3` stub,
  which breaks them silently
  ([spec-kit#3304](https://github.com/github/spec-kit/issues/3304)). Fix
  once per machine: `uv python install --default` (or install jq, or disable
  the `python3` App Execution Alias and put a real Python on PATH).
  Bootstrap's preflight checks this and tells you exactly what to run.
- **macOS**: nothing extra — the scripts run on the system bash 3.2
  (verified on the matrix's macOS runners).
- **Linux**: nothing extra.

## Hosting note

Where the hosting plan cannot enforce merge gates (branch protection and
rulesets are unavailable on free-plan private GitHub repos; CODEOWNERS
approval is a GitLab Premium feature), the checks still run and a red
pipeline is a merge-blocker by convention — recorded honestly, per
SDD-STANDARD §8.1. Self-hosted GitLab CE can run product-repo spec gates
with a single Linux runner — registerable by a project Maintainer, no
instance admin needed. Setup notes live in `docs/adopting-a-repo.md`.
