# Quickstart — your first spec'd feature

**Informative.** This guide explains and demonstrates; the rules live in
[SDD-STANDARD.md](../standard/SDD-STANDARD.md). In any conflict, the
standard wins.

Time: ~20 minutes. Works identically on Windows (Git Bash), macOS, and
Linux — every shell command below is verified by this repo's tri-OS CI
matrix. Shell commands run in **Git Bash** on Windows and any shell on
macOS/Linux.

## 0. Prerequisites, once per machine

[uv](https://docs.astral.sh/uv/) and git. On Windows also make sure Git
Bash has a working `python3` or `jq` — stock Windows has a broken
Microsoft-Store `python3` stub, and the fix is one command:

```
uv python install --default
```

Don't worry about getting this right: the bootstrap preflight below checks
all of it and prints the exact fix if something is missing. Never install
Spec Kit by hand — the tooling brings the pinned version itself.

## 1. Get a playground

Your team's real repos are adopted by your team lead
([adopting-a-repo.md](adopting-a-repo.md)). For this walkthrough, make a
scratch repo. From a clone of `sdd-standard`:

```
uv run bootstrap/init.py ../my-playground --integration generic --profile backend-services
cd ../my-playground
git init -b main .
git add -A
git commit -m "bootstrap"
```

(`--integration generic` keeps this agent-neutral; in a real repo your team
passes its own agent — the choice is yours, that is the point. With
`generic` no agent commands are wired, so run each step's underlying
script from its footnote instead — on Windows, in Git Bash.)

## 2. Start a feature — the Requirements Document

Start the feature from its one-line intent:

```
/speckit.specify alert clients when a transfer bounces off their daily limit
```

Your agent scaffolds the feature folder and drafts the Requirements
Document. Open `specs/001-limit-alerts/spec.md`:
phrase each requirement in an EARS pattern with a stable R-id. Look at
[examples/sample-feature/spec.md](../examples/sample-feature/spec.md) to
see a finished one — same template, filled in.

**The gate:** when the requirements are ready, your product authority
reviews and — in their own change — replaces the `Status: DRAFT` line with
`Status: APPROVED — <name>, <date>`. You never write that line yourself,
and your agent must never write it at all. Nothing further is drafted
until the approval lands.

**What runs underneath.** `/speckit.specify` first runs a scaffold script —
mechanical setup only: create the feature folder, copy the template, report
paths as JSON — then the agent drafts the content. The same step by hand:

```
bash .specify/scripts/bash/create-new-feature.sh --json --short-name limit-alerts "alert clients when a transfer bounces off their daily limit"
```

## 3. The Design Document

After the requirements gate, run `/speckit.plan`.

Fill `specs/001-limit-alerts/plan.md`: the architecture, and the two
contract sections in your stack profile's table shapes (the sample feature
shows both — one sync operation table, one async message table). Cite
requirements as `[R-n]`. Gate: your technical authority approves the same
way.

**What runs underneath.** `bash .specify/scripts/bash/setup-plan.sh --json`
creates `plan.md` from the template and reports the paths as JSON; the agent
(or you, by hand) fills it.

## 4. The Task List

After the design gate, run `/speckit.tasks` — the agent materializes
`tasks.md` from the tasks template. Every task carries at least
one `[R-n]` — a task that maps to no requirement is either missing a
requirement or not needed. Gate: technical authority approves;
implementation starts only after that.

**What runs underneath.**

```
bash .specify/scripts/bash/check-prerequisites.sh --json
bash .specify/scripts/bash/setup-tasks.sh --json
```

The first script verifies the preceding gates; the second reports the
tasks-template path to materialize `tasks.md` from.

## 5. Implement, then the review phase

Implement task by task with `/speckit.implement`. When implementation
completes, the review phase runs automatically (`speckit.sdd.review`
is hooked after implement) or on demand — it compares the code against the
approved spec/plan/tasks and writes `review-notes.md` for the human Review
approver, who must not be the implementer. The approver — not the notes,
not the agent — passes the Review gate.

One rule to internalize now: **if your change alters behavior an approved
spec covers, the same PR updates that spec.** The CI gate
(`check_spec_structure.py`) and PR review both look for exactly this.

## 6. Check yourself

The same check CI runs, locally (from your sdd-standard clone):

```
uv run ci/check_spec_structure.py --repo ../my-playground
```

It verifies Status lines, gate order, R-id uniqueness, `[R-n]`
traceability, kebab-case filenames, and LF endings — with file-by-file
messages when something is off. Run it right now, mid-walkthrough, and it
correctly goes red: your plan.md exists while spec.md is still DRAFT —
that is the requirements gate working, not a bug. It goes green once the
approvals from §2–§4 are in place.

## Where to go next

- Too small to spec? Items under the size threshold need no ceremony —
  SDD-STANDARD §6, the pressure valve.
- Reviewing someone's spec? [reviewing-specs.md](reviewing-specs.md).
- Questions? Ask the standard owner; answers that help
  everyone land in [faq.md](faq.md).
