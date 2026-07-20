# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

The **convention is the product**: this repo defines and distributes a
spec-driven development standard — **and nothing else**. It is
treated like a shared library — semver on the convention itself
(CHANGELOG.md, 0.x pre-versions until the standard owner declares 1.0),
changes by reviewed PR. Product repos consume it via `bootstrap/init.py`
at a pinned release tag; specs always live in product repos next to their
code — there is deliberately **no central specs repository**. The standard
is being validated on demo projects; introduction to an organization is a
separate, later decision (D-11). There is deliberately no rollout program
in this repo — don't add pilot machinery, metrics scaffolding, or
org-trial planning here.

The repo is **organization-neutral** (D-13): no organization names,
governance bodies, org structure, personnel, or org-infrastructure facts
belong anywhere in it — organization-specific bindings (standard-owner
designation, approver names, policies, hosting) happen at adoption. Don't
reintroduce any.

Settled decisions — do not relitigate them: GitHub Spec Kit as the sole
implementation of the standard (vendor-neutrality abandoned for simplicity,
D-18 — no plan B, no exit triggers, no converter), stock artifact
filenames
(`spec.md`/`plan.md`/`tasks.md`), bash as the single scaffold variant,
the abstract standard-owner role (SDD-STANDARD §13),
org-neutrality (D-13), EARS as the requirements notation with the §4.1
structured fallback (D-15), property-trigger qualifying rules instead of
story points (D-16, ⚠), and the thin seeded constitution whose shared
block is drift-checked by `ci/check_convention_version.py` (D-17).
Decision records live
in CHANGELOG.md and SDD-STANDARD sections (e.g. §4.1, §6, §10), indexed
with stable D-ids in
DECISIONS.md — a PR that settles, supersedes, or withdraws a decision
updates the index in the same PR.

## Rules that bind you here (the repo dogfoods its own standard)

- **Never write or modify an approval `Status:` line** — the
  `APPROVED — <name>, <date>` line — in any artifact (SDD-STANDARD §3.2).
  Writing `Status: DRAFT` on an artifact you draft is fine and expected; it
  is the *approval* flip that is reserved for a human approver, added in
  their own change. This is the one rule that allows no exceptions.
- A change that alters behavior covered by an approved spec must update
  that spec **in the same PR**. Approved documents are never silently
  edited — add a dated amendment note and flag it for re-approval in the
  PR. The change that re-approves the document removes the note; git
  history keeps the trail.
- R-ids and T-ids are stable: never renumbered, never reused; withdrawn
  entries stay listed as `WITHDRAWN`. Every task carries at least one
  `[R-n]`. Tick a task only when its stated evidence exists (run link,
  passing check, artifact).
- Binding language (shall/MUST, gates) lives **only** in
  `standard/SDD-STANDARD.md` and `standard/profiles/`. Everything in
  `docs/` is informative and must never legislate. Profiles provide
  defaults and vocabulary only — never gates, approval steps, or artifact
  types.
- All tooling is one Python implementation, **stdlib + pathlib only**, run
  via `uv run` — never `.sh`/`.ps1` duplicates, never `shell=True`. Every
  failure message must include the exact remediation command.
- LF line endings everywhere (.gitattributes enforces); filenames in spec
  folders are lowercase-kebab-case (exceptions: README.md, CODEOWNERS,
  LICENSE, dot-files).

## Writing style

Be precise first, simple second: say exactly what is true, no
ambiguity. Keep technical terms when the everyday word is less exact.
Within that: short sentences, everyday words, one idea per sentence.
No business-speak or figurative filler.
The style limits wording, not coverage: stay complete, keep every
edge case.

This style applies to any text with a human reader — chat replies,
documents, specs, plans, comments, reports — even if agents read it
too. Only text no human reads (command definitions, agent
instructions) is exempt; there, repeat key constraints and list every
case when that helps reliability.

## Behavior

Push back when I'm wrong or my request doesn't make sense.
Don't just comply — say so first, then do it if I insist.

## Commands

There is no test framework; verification is these checks plus the CI
matrix. All commands are identical on Windows (Git Bash for the scaffold
scripts), macOS, and Linux.

```sh
# The merge gate — run before every push (checks examples/, and specs/ if
# this repo ever grows its own feature folders again)
uv run ci/check_spec_structure.py --self

# Full local consumption test: bootstrap a scratch repo end-to-end
uv run bootstrap/init.py ../scratch --integration generic --profile backend-services --ignore-agent-tools

# Check a product repo (what an adopting repo's CI runs)
uv run ci/check_spec_structure.py --repo <path>
uv run ci/check_convention_version.py --repo <path> --standard .
```

CI: `checks.yml` runs the structure self-check on every push/PR.
`verify-tri-os.yml` (PRs touching `bootstrap|speckit|ci`, weekly cron,
manual) runs
the full consumption flow on all 6 cells — {ubuntu, windows, macos} ×
{sh, ps} — including a negative probe asserting the structure check goes
red on a skipped approval. The full grid is variant-decision evidence;
never add `fail-fast`.

## Architecture — the consumption chain

```
speckit/PINNED-VERSION ──► bootstrap/init.py ──► product repo
speckit/presets/sdd/           (wraps pinned `specify init` via uv tool run,
speckit/extensions/sdd/         installs preset + review extension from this
standard/profiles/<profile>/    checkout, repairs the constitution, copies
                                the profile to .specify/memory/profile.md,
                                writes .specify/sdd.json)
ci/check_*.py — same scripts gate this repo (--self) and product repos (--repo)
examples/sample-feature — teaching example (kept fresh by check_spec_structure.py --self)
```

- The preset overrides four templates (all strategy **replace** — see
  below); the extension adds `speckit.sdd.review` on an
  `after_implement` hook. It prepares review notes and never writes Status
  lines. No command or script overrides — only supported upstream override
  points, which is what keeps pin-forwards cheap.
- `examples/sample-feature` never falls out of date: `ci/check_spec_structure.py --self`
  gates it on every push (it keys on `- **R-n**` requirement bullets), so any
  edit must keep that check green.

## Pinned-version facts (re-verify at every pin-forward)

Verified against Spec Kit v0.13.0 source; each one shapes code here:

1. `specify init` seeds `.specify/memory/constitution.md` *after* the
   preset installs, from the preset's own constitution-template when one
   exists (`ensure_constitution_from_template`, upstream #3276) —
   `bootstrap/init.py::seed_constitution` still overwrites it afterwards
   to fill the placeholders and append the stack-profile block.
2. The scaffolded shell scripts apply manifest-declared composition
   strategies only when a working python3 + PyYAML exist at scaffold
   time, and degrade to path-convention replace-only resolution
   (`presets/<id>/templates/<name>.md`) without them — which is why every
   preset override stays `replace`: identical behavior at every
   degradation level.
3. `--integration generic` requires `--integration-options
   --commands-dir …`; bootstrap defaults it to `.agent/commands`
   (unchanged since v0.12.4).
4. The `py` script type is still shipped (sh/ps/py) and matured —
   upstream #3385 fixed the Store-stub interpreter resolution — but
   remains not adopted (SDD-STANDARD §10.4, re-evaluated 2026-07-20: no
   verification-matrix cells, single-variant rule). Watch again at the
   next pin-forward.

A pin change lands only as a reviewed PR that passes the full tri-OS matrix
(SDD-STANDARD §9.3); never install Spec Kit by hand or bump the pin
casually.

## Platform pitfalls with prior art

- **LW-1 (Windows):** stock Windows has a Microsoft-Store `python3` stub in
  Git Bash that *exists but fails at runtime*. At the v0.13.0 pin the
  scaffold scripts survive it (spec-kit#3304 fixed upstream by v0.12.9 —
  they fall through to text parsing), so bootstrap's preflight WARNS
  instead of failing; it still *executes* the parser rather than locating
  it. Recommended fix stays: `uv python install --default`.
- **pwsh CI steps:** invoking a `.ps1` via `&` does not reset
  `$LASTEXITCODE`; guards reading it see stale state from earlier native
  commands. Reset it explicitly (see `Run-Json` in verify-tri-os.yml).
- Status lines accept both em dash and plain hyphen after APPROVED; the
  matrix deliberately exercises hyphen on sh cells and em dash on ps cells.

## Status and governance

The standard is complete at 0.3.0-draft and being validated on demo projects
(separate repos, bootstrapped from this one). Owner: the standard owner —
the repo maintainer(s), a role defined in SDD-STANDARD §13; an adopting
organization designates its own owner at adoption. Convention changes
get a CHANGELOG entry; releases stay 0.x until the standard owner declares
1.0.
