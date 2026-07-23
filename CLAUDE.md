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
story points (D-16, ⚠), the thin seeded constitution whose shared
block is drift-checked by `ci/check_convention_version.py` (D-17), and
no human approval gates (D-19 — no `Status:` lines, no approver roles,
no human Review gate; artifact order by presence, review phase as agent
self-review; don't propose reintroducing approvals).
Decision records live
in CHANGELOG.md and SDD-STANDARD sections (e.g. §4.1, §6, §10), indexed
with stable D-ids in
DECISIONS.md — a PR that settles, supersedes, or withdraws a decision
updates the index in the same PR.

## Rules that bind you here (the repo dogfoods its own standard)

- A change that alters behavior covered by a spec must update
  that spec **in the same PR**. Normative documents are never silently
  edited — a substantive change to SDD-STANDARD or a profile carries a
  dated amendment note or CHANGELOG entry in the same PR; git history
  keeps the trail. There are no approval `Status:` lines anywhere —
  human gates were removed (D-19); don't add Status machinery back.
- R-ids and T-ids are stable: never renumbered, never reused; withdrawn
  entries stay listed as `WITHDRAWN`. Every task carries at least one
  `[R-n]`. Tick a task only when its stated evidence exists (run link,
  passing check, artifact).
- Binding language (shall/MUST) lives **only** in
  `standard/SDD-STANDARD.md` and `standard/profiles/`. Everything in
  `docs/` is informative and must never legislate. Profiles provide
  defaults and vocabulary only — never gates, approval steps, or artifact
  types (§7.3 keeps that prohibition so nothing reintroduces approvals
  at the profile level).
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
red on a task with no [R-n] reference. The full grid is variant-decision
evidence; never add `fail-fast`.

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
  `after_implement` hook. It writes findings to review-notes.md; findings
  are resolved (fix, same-PR amendment, or explicit accepted-with-reason
  note) before the item is done. No command or script overrides — only
  supported upstream override
  points, which is what keeps pin-forwards cheap.
- `examples/sample-feature` never falls out of date: `ci/check_spec_structure.py --self`
  gates it on every push (it keys on `- **R-n**` requirement bullets), so any
  edit must keep that check green.

## Pinned-version facts (re-verify at every pin-forward)

Verified against Spec Kit v0.13.4 source; each one shapes code here:

1. `specify init` seeds `.specify/memory/constitution.md` *after* the
   preset installs, from the preset's own constitution-template when one
   exists (`ensure_constitution_from_template`, upstream #3276) —
   `bootstrap/init.py::seed_constitution` still overwrites it afterwards
   to fill the placeholders and append the stack-profile block.
2. The scaffolded workflow scripts — bash and, since v0.13.2 (#3386), the
   Python ports — resolve templates by path convention only
   (`common.sh`/`common.py` `resolve_template`): they pick the first
   matching `presets/<id>/templates/<name>.md` and copy it, so template
   resolution is replace-only at scaffold time, unconditionally.
   Composition strategies exist in Spec Kit but run in the preset resolver
   at preset-resolve time (`PresetResolver.resolve_content`), never in the
   scaffold scripts (`resolve_template_content` is defined but has no call
   site) — which is why every preset override stays `replace`: it is the
   only strategy honored where the scaffold consumes templates.
3. `--integration generic` requires `--integration-options
   --commands-dir …`; bootstrap defaults it to `.agent/commands`
   (unchanged since v0.12.4).
4. The `py` script type is still shipped (sh/ps/py) and matured —
   upstream #3385 fixed the Store-stub interpreter resolution, and v0.13.2
   (#3386) completed the Python ports of the core scaffold scripts — but
   remains not adopted (SDD-STANDARD §10.4, re-evaluated 2026-07-23: no
   verification-matrix cells, single-variant rule). Watch again at the
   next pin-forward.

A pin change lands only as a reviewed PR that passes the full tri-OS matrix
(SDD-STANDARD §9.3); never install Spec Kit by hand or bump the pin
casually.

## Platform pitfalls with prior art

- **LW-1 (Windows):** stock Windows has a Microsoft-Store `python3` stub in
  Git Bash that *exists but fails at runtime*. At the v0.13.4 pin the
  scaffold scripts survive it (spec-kit#3304 fixed upstream by v0.12.9 —
  they fall through to text parsing), so bootstrap's preflight WARNS
  instead of failing; it still *executes* the parser rather than locating
  it. Recommended fix stays: `uv python install --default`.
- **pwsh CI steps:** invoking a `.ps1` via `&` does not reset
  `$LASTEXITCODE`; guards reading it see stale state from earlier native
  commands. Reset it explicitly (see `Run-Json` in verify-tri-os.yml).

## Status and governance

The standard is complete at 0.4.1-draft and being validated on demo projects
(separate repos, bootstrapped from this one). Owner: the standard owner —
the repo maintainer(s), a role defined in SDD-STANDARD §13; an adopting
organization designates its own owner at adoption. Convention changes
get a CHANGELOG entry; releases stay 0.x until the standard owner declares
1.0.
