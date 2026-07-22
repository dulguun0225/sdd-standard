# Quickstart — your first spec'd feature

**Informative.** This guide explains and demonstrates; the rules live in
[SDD-STANDARD.md](../standard/SDD-STANDARD.md). In any conflict, the
standard takes precedence.

Time: ~20 minutes. The scaffold scripts and checks below run identically
on Windows (Git Bash), macOS, and Linux — this repo's tri-OS CI matrix
verifies them on all three. Shell commands run in **Git Bash** on Windows
and any shell on macOS/Linux; the `/speckit.*` commands run inside your
coding agent.

## The shape, before you start

```
spec.md → plan.md → tasks.md → implement → review-notes.md → findings resolved → done
```

The artifact order is structural: plan.md is drafted only once spec.md
exists, tasks.md only once plan.md exists, and implementation starts
only once all three are there (SDD-STANDARD §3.1). No one signs an
artifact off — the CI check reads which files exist, not who approved
them. After implementation, the review phase compares the code against
the three artifacts and writes `review-notes.md`; every finding is
resolved before the item is done (§3.2). The full picture — including
the loops back when requirements change — is the
[README's lifecycle diagram](../README.md#the-lifecycle-in-a-product-repo).

Two terms recur below:

- **review phase** — the automated step after implementation: the
  review command compares the code against the three artifacts and
  writes `review-notes.md` into the feature folder.
- **profile** — your stack's contract vocabulary; this guide uses
  `backend-services`, installed into the repo at bootstrap.

[GLOSSARY §3](../standard/GLOSSARY.md#3-terms) defines the rest.

## 0. Prerequisites, once per machine

[uv](https://docs.astral.sh/uv/) and git. On Windows, a working
`python3` or `jq` in Git Bash is recommended. Stock Windows has a
broken Microsoft-Store `python3` stub. The scaffold still works with it at the
pinned Spec Kit version, but installing a real parser takes one command:

```
uv python install --default
```

Don't worry about getting this right. The bootstrap preflight below
checks all of it and prints the exact fix if something is missing.
Never install Spec Kit by hand; the tooling brings the pinned version
itself.

## 1. Get a scratch repo

Your team's real repos are adopted by your team lead
([adopting-a-repo.md](adopting-a-repo.md)). For this walkthrough, make a
scratch repo. From a clone of `sdd-standard`:

```
uv run bootstrap/init.py ../my-scratch --integration claude --profile backend-services
cd ../my-scratch
git init -b main .
git add -A
git commit -m "bootstrap"
```

(`--integration claude` wires the `/speckit.*` slash commands this guide
uses below, for Claude Code. Your team's agent is a free choice — pass its
name instead if you use a different one, that is the point. No coding
agent, or want the agent-neutral path this repo's CI verifies? Pass
`--integration generic`: no slash commands are wired, and you run each
scaffold step yourself — steps 2–4 below each show the exact script, in
Git Bash on Windows.)

## 2. Start a feature — the Requirements Document

Start the feature from its one-line intent:

```
/speckit.specify alert clients when a transfer is rejected by their daily limit
```

Your agent scaffolds the feature folder and drafts the Requirements
Document. Open `specs/001-limit-alerts/spec.md`:
phrase each requirement in an EARS pattern with a stable R-id. An EARS
requirement reads `WHEN <trigger>, the <system> shall <response>` — one of
five patterns ([GLOSSARY §1](../standard/GLOSSARY.md#1-ears-requirement-patterns)
shows all five with examples). Look at
[examples/sample-feature/spec.md](../examples/sample-feature/spec.md) to
see a finished one — same template, filled in.
[writing-requirements.md](writing-requirements.md) shows how to get
from the agent's raw draft to that finished shape.

**When to move on:** when every requirement states one testable
behavior under a stable R-id, draft the design next. There is no
sign-off step — the order holds because the files exist in order:
plan.md comes only after spec.md exists (SDD-STANDARD §3.1). Whether a
teammate reads the spec before you continue is your team's own
practice, outside the standard (§1).

**What the command does mechanically.** `/speckit.specify` first runs a scaffold
script. The script is mechanical setup only: create the feature folder,
copy the template, report paths as JSON. Then the agent drafts the
content. The same step by hand:

```
bash .specify/scripts/bash/create-new-feature.sh --json --short-name limit-alerts "alert clients when a transfer is rejected by their daily limit"
```

## 3. The Design Document

With spec.md in place, run `/speckit.plan`.

Fill `specs/001-limit-alerts/plan.md`: the architecture, and the two
contract sections in your stack profile's table shapes (the sample feature
shows both — one sync operation table, one async message table). Cite
requirements as `[R-n]`. How to fill the contract rows well is
[writing-design.md](writing-design.md).

**What the command does mechanically.** `bash .specify/scripts/bash/setup-plan.sh --json`
creates `plan.md` from the template and reports the paths as JSON. The
agent — or you, by hand — fills it.

## 4. The Task List

With plan.md in place, run `/speckit.tasks` — the agent materializes
`tasks.md` from the tasks template. Every task carries at least
one `[R-n]` — a task that maps to no requirement is either missing a
requirement or not needed. Implementation starts once tasks.md exists,
the last of the three artifacts (SDD-STANDARD §3.1). Slicing tasks and
writing their evidence lines is [writing-tasks.md](writing-tasks.md).

**What the commands do mechanically.**

```
bash .specify/scripts/bash/check-prerequisites.sh --json
bash .specify/scripts/bash/setup-tasks.sh --json
```

The first script verifies the preceding artifacts exist; the second
reports the tasks-template path to materialize `tasks.md` from.

## 5. Implement, then the review phase

Implement task by task with `/speckit.implement`. When implementation
completes, the review phase runs automatically (`speckit.sdd.review`
is hooked after implement) or on demand. It compares the code against
spec.md, plan.md, and tasks.md and writes `review-notes.md` into the
feature folder: a verdict per requirement, the contract check, task
evidence, spec drift, and open questions. Before the item is marked
done, every finding is resolved one of three ways (SDD-STANDARD §3.2):
fix the implementation, amend the artifact in the same PR, or record
an explicit acceptance with a reason in the notes.
[examples/sample-feature/review-notes.md](../examples/sample-feature/review-notes.md)
shows a filled one.

One rule to internalize now: **if your change alters behavior a spec
covers, the same PR updates that spec** (SDD-STANDARD §5.2). The review
phase's spec-drift section looks for exactly this.

## 6. Check yourself

The same check CI runs, locally (from your sdd-standard clone):

```
uv run ci/check_spec_structure.py --repo ../my-scratch
```

It goes red — non-zero exit, one message per file — on any of these:
a feature folder with no spec.md, tasks.md present without plan.md
beside it (the artifact order, read from presence), a task with no
`[R-n]`, a task citing an R-id that spec.md does not define, a
duplicate R-id or T-id, a `contracts/` path in plan.md that points at
no file, a filename that is not lowercase-kebab-case, or CRLF line
endings. One finding is advisory,
never merge-blocking: a vague word inside a requirement bullet
("quickly", "appropriate", …) prints as a WARNING — replace it with a
number and a unit, or keep it with a stated reason.

If you followed steps 2–4 in order, the check is green now. To watch
it catch the order, move plan.md aside and run it again: red —
tasks.md exists but its Design Document is missing. Put plan.md back.

## Where to go next

- Who does all this on a real team, in which PR?
  [feature-walkthrough.md](feature-walkthrough.md) replays this same
  feature as a team runs it, PR by PR.
- Too small to spec? An item matching none of the qualifying triggers
  needs no ceremony — SDD-STANDARD §6, the exemption for small changes.
- Requirements keep changing? That is normal —
  [evolving-requirements.md](evolving-requirements.md), the
  spec → build → learn loop.
- Reviewing someone's spec? [reviewing-specs.md](reviewing-specs.md).
- Questions? Ask the standard owner; answers that help
  everyone land in [faq.md](faq.md).
