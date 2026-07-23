# How it works — bootstrap, preset, extension, and the diff from stock Spec Kit

**Informative.** This guide explains the machinery; the binding rules live
in [SDD-STANDARD.md](../standard/SDD-STANDARD.md) and the stack profiles. In
any conflict, the standard takes precedence and this guide gets fixed.

It describes the machinery at the current pin — **Spec Kit v0.13.4**,
convention version **0.4.1-draft**, profile **backend-services
0.2.1-draft**. The file paths and the scaffold inventory below are
pin-specific and are re-verified at every pin-forward; the source of truth is
the code (`bootstrap/init.py`, `speckit/`, `ci/`) and the standard.

## 1. The core idea

This repo is a convention, distributed as a versioned library. It does **not**
fork Spec Kit. It sits on top of stock [GitHub Spec
Kit](https://github.com/github/spec-kit), pinned in
`speckit/PINNED-VERSION`, and changes its behavior through Spec Kit's own
supported extension points plus a thin Python wrapper. Nothing upstream is
patched. That is deliberate: touching only supported override points is what
keeps moving the pin forward cheap.

Three source pieces do the work, plus two checks and the normative text:

| Piece | What it is | Where it lives |
| ----- | ---------- | -------------- |
| Preset | Replaces 4 core templates | `speckit/presets/sdd/` |
| Extension | Adds 1 review command on a hook | `speckit/extensions/sdd/` |
| Bootstrapper | Wraps `specify init`, repairs files, writes a marker | `bootstrap/init.py` |
| Checks | Enforce the convention in an adopting repo's CI | `ci/check_spec_structure.py`, `ci/check_convention_version.py` |
| Normative text | The rules themselves | `standard/SDD-STANDARD.md`, `standard/profiles/` |

## 2. The consumption chain

```
speckit/PINNED-VERSION (v0.13.4)
        |
        v
bootstrap/init.py --uv tool run--> stock `specify init` (pinned; never a global install)
        |                                     |
        |  passes: --preset speckit/presets/sdd   --> installs SDD preset (4 template replaces)
        |          --integration generic
        |          --commands-dir .agent/commands
        |
        |--> `specify extension add speckit/extensions/sdd --dev`  --> installs review extension
        |--> seed_constitution()  --> overwrites .specify/memory/constitution.md (fills placeholders + profile block)
        |--> install_profile()    --> copies standard/profiles/backend-services -> .specify/memory/profile.md
        `--> write_marker()       --> writes .specify/sdd.json

Then, in the adopting repo's own CI:
   ci/check_spec_structure.py --repo .                            (structure + [R-n] traceability gate)
   ci/check_convention_version.py --repo . --standard <checkout>  (drift gate)
```

## 3. How the customization is implemented

Each layer uses exactly one mechanism. The first two are bootstrap wrapping
choices, the middle two are Spec Kit's own extension points, the last is the
adopting repo's CI.

| # | Layer | Mechanism | Effect |
| - | ----- | --------- | ------ |
| 1 | Pin enforcement | `bootstrap/init.py::specify()` always runs `uv tool run --from git+…spec-kit.git@v0.13.4 specify …` | Spec Kit runs at the exact pin, never a global `specify`. A mismatched global `specify` on PATH is a hard preflight failure. |
| 2 | Integration choice | bootstrap makes `--integration` required; for `generic` it adds `--integration-options "--commands-dir .agent/commands"` | Stock would silently default to `copilot`. bootstrap forces an explicit, agent-neutral choice. |
| 3 | Template overrides | Spec Kit **preset** (`preset.yml`, `provides.templates`) | Replaces the 4 core templates (constitution / spec / plan / tasks) with SDD versions. |
| 4 | Review phase | Spec Kit **extension** (`extension.yml`): one new command + `after_implement` hook | Adds an agent self-review step that writes `review-notes.md`. |
| 5 | File repair and marker | plain file writes in `bootstrap/init.py` | Fills the constitution, copies the profile, writes `.specify/sdd.json`. |
| 6 | Enforcement | `ci/check_*.py` in the adopting repo's CI — not a Spec Kit mechanism, not wired by bootstrap | Turns the conventions into a merge gate. |

Two implementation facts matter most.

**The preset uses full replace for all four templates.** Each override is
declared by a bare `replaces:` key naming the stock template; Spec Kit has no
`strategy:` field, so `replaces:` means "first match in the resolution stack
wins entirely". Replace is chosen on purpose. At this pin the scaffold scripts
that actually consume templates — `common.sh`/`common.py` `resolve_template`,
used by the bash scripts and the Python ports added in v0.13.2 — resolve by
path convention only: the first matching `presets/<id>/templates/<name>.md`
wins and is copied. That is replace-only. Spec Kit's other composition
strategies (prepend / append / wrap) exist, but they run in the preset
resolver at preset-resolve time (`PresetResolver.resolve_content`), not in the
scaffold scripts, so a non-replace template strategy would be silently ignored
where the templates are consumed. Replace is therefore the only strategy that
is honored.

**The extension only adds.** It registers a new command
(`speckit.sdd.review`) and attaches it to the documented `after_implement`
hook. It overrides nothing. That is why pin-forwards stay cheap — there is no
forked command or template to reconcile against upstream edits.

## 4. What `bootstrap/init.py` does, in order

Running `uv run bootstrap/init.py <target> --integration generic --profile
backend-services` executes this sequence:

1. **Reconfigure stdout/stderr** to `errors="replace"` so a legacy Windows
   codepage cannot crash it on `§` characters.
2. **Discover profiles** — the `--profile` choices are the non-`_`
   subdirectories of `standard/profiles/` (today: only `backend-services`).
3. **Parse args.** `--integration` and `--profile` are required. `--script`
   defaults to `sh` (choices `sh`/`ps`; `ps` is verification-matrix only and
   only warns). `--integration-options` and `--ignore-agent-tools` pass
   through.
4. **Assert the checkout is complete** — `preset.yml` and `extension.yml` must
   exist, else fail with "re-clone at the pinned release tag".
5. **Read the pin** from `speckit/PINNED-VERSION`.
6. **Preflight.** Check `uv` and `git`; hard-fail if a global `specify`
   version differs from the pin; on Windows with `sh`, locate Git Bash
   (rejecting WSL's `system32\bash.exe`) and run a `jq`/`python3` probe — a
   failing probe is a warning, not a gate (see LW-1 in the repo README).
7. **`specify init`** via `uv tool run`, passing `--preset <absolute path to
   speckit/presets/sdd>`; for `generic`, injects `--commands-dir
   .agent/commands`.
8. **Assert the preset landed** (`.specify/presets/sdd/preset.yml` exists) —
   because `specify init` downgrades preset failures to warnings.
9. **`specify extension add … --dev`**, run with `cwd=target`; then assert
   `.specify/extensions/sdd/extension.yml` exists.
10. **`seed_constitution()`** — overwrite `.specify/memory/constitution.md`:
    fill `[PROJECT NAME]` with the target directory name, `[CONVENTION
    VERSION]` with the standard's version, and replace the `## Stack profile`
    placeholder comment with the profile block.
11. **`install_profile()`** — copy `standard/profiles/backend-services/profile.md`
    verbatim to `.specify/memory/profile.md`.
12. **`write_marker()`** — write `.specify/sdd.json`.
13. Print next steps.

Every failure prints the exact remediation command. All target files are
written with LF line endings, even on Windows.

## 5. What a bootstrapped repo contains

A bootstrap with `--integration generic --profile backend-services` produces
the tree below. Each entry is marked by origin.

**SDD-specific — do not exist in stock at all:**

| File in the product repo | Written by | What it is |
| ------------------------ | ---------- | ---------- |
| `.specify/sdd.json` | `write_marker()` | The convention marker: `{convention_version, profile, variant, speckit_pin, bootstrapped}`. Read only by `check_convention_version.py`; its presence is that check's first gate. The key `variant` takes its value from `--script`. |
| `.specify/memory/profile.md` | `install_profile()` | Verbatim copy of the backend-services profile. Gives the implementing agent the profile's silence-as-default contract rules locally. Drift-checked byte-for-byte. |
| `.specify/presets/sdd/preset.yml` | `specify init --preset` | The SDD preset manifest, copied in so it can override at resolution time. |
| `.specify/presets/sdd/README.md` | `specify init --preset` | Copied in alongside the manifest. |
| `.specify/presets/sdd/templates/{constitution,spec,plan,tasks}-template.md` | `specify init --preset` | The 4 SDD templates. They outrank the stock core templates in the resolution stack (presets > core), so they are what actually shapes agent output. |
| `.specify/extensions/sdd/extension.yml` | `specify extension add` | The review-phase manifest. |
| `.specify/extensions/sdd/commands/review.md` | `specify extension add` | The `speckit.sdd.review` command prompt. It is not copied into `.agent/commands/`; it is invoked through the hook registry. |

**Repaired stock seed** (SDD content, but the file also exists in stock):

| File | What happened |
| ---- | ------------- |
| `.specify/memory/constitution.md` | `specify init` seeds it from the SDD preset's constitution-template (Spec Kit's `ensure_constitution_from_template` resolves through the preset; the sibling `.specify/memory/.constitution-template.json` records `"source": "sdd v0.4.0"`). So the file is SDD text from the first write, with placeholders unfilled. `seed_constitution()` then overwrites it to fill the project name, the convention version, and the `## Stack profile` block. The frozen `## Shared principles (seeded — do not edit)` block is preserved and drift-checked byte-for-byte. |

**Stock registry file with an SDD entry inside it:**

| File | Detail |
| ---- | ------ |
| `.specify/extensions.yml` | Stock extension registry, now listing `installed: [sdd]` and wiring `hooks.after_implement -> {extension: sdd, command: speckit.sdd.review, optional: false, priority: 10}`. This is how the review runs without a command file in `.agent/commands`. |

**Stock, unchanged** (the rest of the scaffold):

- `.agent/commands/speckit.{specify,plan,tasks,clarify,analyze,checklist,constitution,implement,converge,taskstoissues}.md`
  — the 10 stock slash-command files. The agent-neutral location is the only
  SDD choice here; there is no `review` command file among them.
- `.specify/templates/{spec,plan,tasks,constitution,checklist}-template.md` —
  the 5 stock core templates, present but inert (outranked by the preset
  copies).
- `.specify/scripts/bash/{check-prerequisites,common,create-new-feature,setup-plan,setup-tasks}.sh`
  — stock scaffold scripts. Only the variant choice (`sh` for all operating
  systems) is convention-bound.
- Bookkeeping: `.specify/init-options.json`, `.specify/integration.json`,
  `.specify/integrations/{generic,speckit}.manifest.json`,
  `.specify/memory/.constitution-template.json`, `.specify/presets/.registry`,
  `.specify/extensions/.registry`, `.specify/workflows/speckit/workflow.yml`,
  `.specify/workflows/workflow-registry.json`.

**A fresh bootstrap has no `specs/` folder and no feature artifacts.** There is
no `spec.md`, `plan.md`, `tasks.md`, `review-notes.md`, or
`.specify/feature.json` yet — those appear only after an agent authors a
feature. The [`examples/sample-feature/`](../examples/sample-feature/spec.md)
folder in this repo is a teaching example of that end state, not something
bootstrap writes.

## 6. How the four replaced templates differ from stock

This is the substance of the difference: what an agent is told to produce.

| Artifact | Stock Spec Kit | SDD replacement |
| -------- | -------------- | --------------- |
| Requirements (`spec.md`) | Priority-ranked user stories (P1/P2/P3) with Given/When/Then acceptance; functional requirements numbered `FR-001` as MUST statements; `[NEEDS CLARIFICATION]` markers. | Every requirement is an EARS sentence as a `- **R-n**` bullet. R-ids are stable — never renumbered, never reused; withdrawn ones stay listed as `WITHDRAWN`. A narrow fallback (§4.1) allows a structured list or table only for mathematical content or more than three preconditions. A Traceability section. |
| Design (`plan.md`) | Technical Context, Constitution Check, Complexity Tracking. No contract sections, no profile. | Design elements cite `[R-n]`. Two profile-driven contract tables — Synchronous (Operation / Method & path / Auth / Request / Responses / Errors / Idempotency) and Asynchronous (Event / Subject / Schema / Producer / Delivery / Consumers) — with silence-conformance defaults from the profile. A phase plan whose "Satisfies" column holds `[R-n]` and feeds tasks. |
| Tasks (`tasks.md`) | `T001`-style sequential IDs, `[P]` parallel marker, `[US#]` story tag. No requirement traceability. | Every task is `- [ ] **T-n**` carrying at least one `[R-n]` and an italic `*Evidence:*` clause. T-ids stable like R-ids. A task is done when its evidence exists. |
| Constitution | Five named principle slots plus Governance; ships human-approval language ("Amendments require documentation, approval, migration plan"). | Thin: three non-negotiable seeded principles, a `## Repo principles` append slot (tighten, never loosen), a `## Stack profile` slot. The seeded block is drift-checked byte-for-byte. No approval language. |

The three content templates also embed the repo's writing-style directive
verbatim, so agent-authored documents inherit it.

## 7. The review phase (the extension)

Stock Spec Kit has no review phase. The extension adds one on the
`after_implement` hook (`optional: false`). `speckit.sdd.review` tells an agent
to: locate the feature; verify `spec.md`, `plan.md`, and `tasks.md` exist;
gather the implementation delta; give each R-id a verdict (implemented /
partial / missing / deviates) with evidence; check the contract tables against
the code, including silence-conformance against the profile; confirm every done
task has evidence and an `[R-n]`; and flag spec drift (the most important
finding class). It writes `review-notes.md`.

Its hard rules: it must not silently edit `spec.md`, `plan.md`, or `tasks.md`
to match the code, and must not tick tasks or mark the item done in this phase.
Findings are resolved one of three ways — fix the implementation, amend the
artifact in the same PR/MR, or record an explicit acceptance with a reason.

## 8. The profile layer

A profile fills the Design Document's abstract contract slots with one stack
family's vocabulary and defaults. `backend-services` defines the
stated-or-default reading rule (what the design states wins; silence reads as
the profile default; where no safe default exists — for example the idempotency
of a mutating operation — silence is a named review question, never the
implementer's choice), plus the synchronous and asynchronous default tables,
contract vocabulary, worked examples, and a standard-failure-cases table. By
rule (§7.3) a profile provides defaults and vocabulary only; it never adds
gates, approval steps, or artifact types. Bootstrap copies it into the repo so
the agent has it locally; the constitution carries only a pointer.

## 9. What enforces the convention — and what does not

**Enforced by machine, merge-blocking:**

- `check_spec_structure.py`: the `- **R-n**` and `- [ ] **T-n**` shapes; every
  task carries `[R-n]`; unique, stable ids; artifact order by presence (a
  `tasks.md` with no `plan.md` beside it fails); local `contracts/…`
  references resolve to real files; lowercase-kebab filenames; LF line endings.
  Two modes: `--self` (gates this repo's `examples/`, plus a layer-congruence
  check that the plan template's contract columns match the profile's) and
  `--repo <path>` (what an adopting repo runs on its own `specs/`).
- `check_convention_version.py`: `.specify/sdd.json` present; `convention_version`
  and `speckit_pin` match the standard; the constitution's shared block matches
  the pinned template byte-for-byte; `.specify/memory/profile.md` matches the
  standard's profile byte-for-byte.

**Not enforced — authored discipline, stated honestly:**

- EARS phrasing is never machine-checked. The structure check keys on the `-
  **R-n**` bullet shape, not on EARS keywords. A poorly phrased requirement
  passes.
- Evidence truth is not checked. The task regex accepts `[ ]` and `[x]`
  equally; a ticked box with a fabricated `*Evidence:*` line passes. Ticking
  only when evidence exists is a human rule.
- Section names, the `review-notes.md` format, and whether humans review at all
  are conventions or out of scope.

## 10. The decisions behind the differences

The differences trace to settled decisions, indexed with stable D-ids in
[DECISIONS.md](../DECISIONS.md) and recorded in the standard. The main ones:
GitHub Spec Kit as the sole implementation (D-18); EARS notation with the §4.1
structured fallback (D-15); stable R-ids and T-ids, never reused, with
`WITHDRAWN` retained; `[R-n]` on every task and a same-PR spec update or it is a
drift incident (§5); property-trigger qualifying rules instead of story points
(D-16); the thin, drift-checked constitution (D-17); no human approval gates at
all (D-19 — no `Status:` lines, no approver roles, no human Review gate;
artifact order is by presence, and review means automated agent self-review);
organization-neutrality (D-13); one Python and stdlib toolchain via `uv`; one
`sh` scaffold variant (§10.1); and no central specs repository (§2.3).

## 11. Non-obvious facts worth carrying

- The constitution is written twice — Spec Kit seeds it from the SDD preset
  template, then bootstrap overwrites it to fill placeholders. Assuming
  `specify init` leaves it untouched misreads the flow. The
  `.constitution-template.json` `source: "sdd v0.4.0"` is direct evidence it
  came from the preset.
- A global `specify` at the wrong version is a hard preflight failure even
  though bootstrap never uses it — the guard protects the developer's own
  `/speckit` workflow, which would otherwise run at the wrong version.
- The Windows JSON probe executes `python3 -c 'print(0)'` in Git Bash (the
  Microsoft-Store `python3` stub exists on PATH but fails at runtime); at this
  pin a failure only warns, because the scaffold falls back to text parsing.
- The review command is wired through `.specify/extensions.yml` (the
  `after_implement` hook), not by a file in `.agent/commands/`.
- The preset must never gain command or script overrides, and the four
  templates must stay `replace` — both to keep pin-forwards cheap and the
  scaffold degradation-safe.
- The `repository:` field in `preset.yml` and `extension.yml` is the
  placeholder `https://example.com/sdd-standard`, kept deliberately for
  organization-neutrality (D-13); it is not a live location.
