# Adopting a repo — the team-lead guide

**Informative.** This guide explains how adoption works; the binding rules
live in [SDD-STANDARD.md](../standard/SDD-STANDARD.md). In any conflict,
the standard takes precedence.

The convention is pre-1.0 and still being validated on demo projects.
Coordinate with the standard owner (SDD-STANDARD §13) before adopting a
real repo, so pre-1.0 changes do not surprise you.

## 1. What you need, and why

The convention requires **capabilities, not vendors**. Anything
providing these six works — GitHub, GitLab (SaaS or self-hosted CE),
Bitbucket, or Jenkins-backed setups included:

- **A git repository per product, on a host with a review flow
  (PRs/MRs).** The same-PR rule (§5.2) needs the PR/MR unit to exist —
  spec update and code change merge together or not at all.
- **One CI job on every push/PR.** This is the merge gate (§8.1).
  `check_spec_structure.py --repo .` turns the pipeline red when the
  structure breaks — a `tasks.md` with no `plan.md` beside it (§3.1),
  a task with no `[R-n]`, a duplicate R-id, a `contracts/` link that
  points at no file — before a human has to catch it. Vague wording in
  a requirement gets a WARNING line; that is advisory, never
  merge-blocking. `check_convention_version.py` reports
  when the repo is older than the pinned convention, or when the seeded
  constitution/profile copies were edited locally (§8.2). The job is
  one Linux container or shell with git and uv. Stdlib Python, no
  services, seconds to run. Any runner works: GitHub Actions,
  GitLab CI (on CE one runner is enough, and a project Maintainer can
  register it), Jenkins, Azure Pipelines. §3 below shows three.
- **Merge blocking, where your plan has it.** Red must mean "does not
  merge". Turn on the platform's mechanism where it exists: required
  status checks, "pipelines must succeed". Where it does not exist
  (branch protection on free-plan private GitHub repos), the check
  still runs. A red pipeline is then a merge-blocker by convention,
  recorded in the team agreement. That fallback is §8.1's own wording.
- **uv and git on every developer machine.** All convention tooling is
  one cross-platform Python implementation run via `uv run`. No local
  Python to manage, no `.sh`/`.ps1` duplicates to drift apart. Bootstrap
  installs the pinned Spec Kit itself via `uv tool run` — nobody ever
  installs Spec Kit by hand (§9.2). On Windows, Git Bash ships with Git
  for Windows (the scaffold scripts' single variant, §10.1). The
  one-time `python3` fix in the
  [README per-OS notes](../README.md#per-os-setup-notes) is
  recommended. The bootstrap preflight checks all of this and prints
  the exact command when something is missing.
- **A clone of sdd-standard at the pinned release tag.** Bootstrap, the
  templates, and both CI checks come from it. That is how every
  adopting repo uses one set of templates at a known version, instead of
  hand-copied templates quietly diverging (§9.2, §9.3). CI clones it
  too — the first line of every snippet in §3.
- **A work tracker — any.** Items carry a summary and a link to the
  spec folder, nothing more (§4.3). Acceptance criteria live in the
  spec alone, so the tracker never disagrees with the spec. No
  integration required; a link is all it takes.

Deliberately **not** required: a specific CI vendor; a specific AI
agent or IDE (§1 scopes the choice out — bootstrap wires whichever you
pass to `--integration`, or `generic` for none); a central specs
repository (§2.3 — there deliberately is none); any human approval
step (the standard defines none, §3.3 — whether humans review PRs is
the team's own practice, §1).

## 2. Bootstrap

Clone this repo **at the pinned release tag** (not main), then from
the clone:

```
uv run bootstrap/init.py <path-to-your-repo> --integration <your-agent> --profile backend-services
```

- `--integration` is your team's coding agent (mandatory — there is no
  default on purpose; `generic` if you use none or several).
- `--profile` binds your Design Documents' contract vocabulary. v1.0 ships
  one profile: `backend-services`. The profile names no technologies;
  if the repo is new and the stack itself is still open,
  [choosing-a-stack.md](choosing-a-stack.md) comes first.
- The target can be a fresh directory or an existing repo. Existing
  specs and code are untouched; the scaffold adds `.specify/` and agent
  command files.

Commit the scaffold as its own commit before anything else. Never copy
templates between repos by hand. That is how divergent template copies start,
and the standard prohibits it.

## 3. Wire the CI gate

The merge gate is one Linux job running `check_spec_structure.py` against
your repo. Copy the script's invocation, not the script — it lives in
sdd-standard and comes along when you clone at the pin.

### GitHub Actions

```yaml
# .github/workflows/spec-checks.yml
name: spec-checks
on: [push, pull_request]
jobs:
  spec-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - name: Get the convention at the pinned release
        # use your organization's sdd-standard fork/home
        run: git clone --depth 1 --branch <PINNED-RELEASE-TAG> https://example.com/sdd-standard sdd-standard
      - name: Spec structure check
        run: uv run sdd-standard/ci/check_spec_structure.py --repo .
      - name: Convention currency
        run: uv run sdd-standard/ci/check_convention_version.py --repo . --standard sdd-standard
```

Then mark the job as a required status check on your default branch
(Settings → Branches), plan permitting.

### GitLab CE (self-hosted)

One Linux runner is enough, and a project **Maintainer** can register
it — no instance admin needed. (Settings → CI/CD → Runners →
registration token, then `gitlab-runner register` on any Linux box with
the `docker` or `shell` executor.)

```yaml
# .gitlab-ci.yml
spec-checks:
  image: ghcr.io/astral-sh/uv:python3.12-bookworm-slim
  script:
    - git clone --depth 1 --branch <PINNED-RELEASE-TAG> https://<your-mirror>/sdd-standard sdd-standard
    - uv run sdd-standard/ci/check_spec_structure.py --repo .
    - uv run sdd-standard/ci/check_convention_version.py --repo . --standard sdd-standard
```

Enforcement on CE, stated honestly:

- Turn on **Settings → Merge requests → Merge checks → "Pipelines must
  succeed"** — that makes the red job block merges.
- Protect the default branch (Settings → Repository → Protected branches)
  so pushes go through MRs at all.
- Human review of MRs is the team's own practice, outside the standard
  (§1). If your team requires it, know that **CODEOWNERS approval
  enforcement is a Premium feature — on CE the file is informational
  only.** Record the practice in the team working agreement rather
  than pretending the platform enforces it.

### Jenkins

Any Linux agent with git and uv on PATH (or a container that has both,
via the Docker plugin):

```groovy
// Jenkinsfile
pipeline {
  agent { label 'linux' }
  stages {
    stage('spec-checks') {
      steps {
        sh 'git clone --depth 1 --branch <PINNED-RELEASE-TAG> https://<your-mirror>/sdd-standard sdd-standard'
        sh 'uv run sdd-standard/ci/check_spec_structure.py --repo .'
        sh 'uv run sdd-standard/ci/check_convention_version.py --repo . --standard sdd-standard'
      }
    }
  }
}
```

Jenkins only *runs* the gate; the *blocking* lives on the hosting
platform. Report the build status back through your setup's plugin
(GitHub, GitLab, or Bitbucket), then mark it required there — a
required status check, a merge check. Where nothing can hard-block,
the §8.1 fallback applies: the check still runs, and red is a
merge-blocker by convention.

## 4. Living with the pin

- The Spec Kit version is pinned for all adopting repos
  (`speckit/PINNED-VERSION`).
  Bootstrap always installs the pin; a different `specify` on a developer's
  PATH fails the preflight with the fix.
- Never upgrade Spec Kit locally. Pin changes land in sdd-standard as
  reviewed PRs that pass the full tri-OS matrix first. Your repo picks
  them up by re-cloning at the new release tag.
- Upgrading the convention takes three steps: re-clone sdd-standard at
  the new release tag, point `<PINNED-RELEASE-TAG>` in your CI job at
  it, and restore the constitution's "## Shared principles" block from
  `speckit/presets/sdd/templates/constitution-template.md` at that tag.
  The restore is required, not optional: the shared block's text
  changes between releases — 0.4.0 changed principle 1 to "Spec before
  code" — and the byte-for-byte check below stays red until the block
  matches the new template. Repo-specific principles under
  "## Repo principles" are untouched by the restore. The same applies
  to the profile copy (`.specify/memory/profile.md`) when the profile
  changed between releases: restore it from
  `standard/profiles/<profile>/profile.md` at the new tag.
- `check_convention_version.py` in your CI tells you when your repo is
  older than the convention release. It also tells you when the seeded
  constitution's shared-principles block was edited: SDD-STANDARD §8.2
  compares it byte-for-byte against the pinned template. Repo-specific
  principles go under "Repo principles".
- Bootstrap also installs your profile's full text at
  `.specify/memory/profile.md`, so its contract defaults are in the
  repo your agents actually read. The same CI check compares that copy
  against the standard's profile at the pinned release. A profile
  change lands upstream by PR to sdd-standard, never by editing the
  copy.

## 5. One adoption, step by step

The steps above, on one fictitious morning. The cast is the
walkthrough's ([feature-walkthrough.md](feature-walkthrough.md)):
Tulga, the tech lead, adopts his team's service repo. The platform is
GitLab CE self-hosted — the least-enforcing platform this guide covers,
so the honest-fallback notes of §3 get exercised; on GitHub Actions or
Jenkins only the §3 snippet differs. Each row is one step. The six
fields — when, who, what, where, how, why — are the columns.

| When | Who | What | Where | How | Why |
| ---- | --- | ---- | ----- | --- | --- |
| **Monday, 09:00** | **Tulga** (tech lead) | Tells the standard owner his team is adopting, and gets the current release tag back | A message to the standard owner (§13's role, bound at his organization) | One question: "which tag do we pin?" | The convention is pre-1.0; coordinating first means pin-forwards do not surprise the repo (top of this guide) |
| **Monday, 09:15** | **Tulga** | Clones sdd-standard at that pinned tag and runs bootstrap against the team repo. The preflight checks uv, git, and the Git Bash parser, and prints the exact fix for anything missing | His workstation | `git clone --depth 1 --branch <PINNED-RELEASE-TAG> https://<the-org-mirror>/sdd-standard`, then `uv run bootstrap/init.py ../alerts-service --integration claude --profile backend-services` | Bootstrap is the only adoption path (§9.2) — hand-copied templates are how silent divergence starts |
| **Monday, 09:40** | **Tulga** | Commits the scaffold as its own commit and opens the adoption MR: `.specify/` (constitution, profile copy, scripts, `sdd.json`) and the agent command files, nothing else | The team repo, a fresh branch | One commit, no code mixed in | Existing code and specs are untouched by bootstrap; a clean scaffold commit is easy to review and easy to revert |
| **Monday, 10:00** | **Tulga** | Wires the merge gate: both checks on every push/MR, cloning sdd-standard at the same pin | `.gitlab-ci.yml`, from §3's CE snippet; one Linux runner a project Maintainer registered | `check_spec_structure.py --repo .` and `check_convention_version.py --repo . --standard sdd-standard` | The check goes red on a broken structure — a `tasks.md` with no `plan.md` beside it, a task with no `[R-n]` — before any human has to catch it (§8.1) |
| **Monday, 10:30** | **Tulga** | Turns on "Pipelines must succeed", protects the default branch, and records the CE gap honestly: the team's own MR-review practice — outside the standard (§1) — goes in the working agreement, because on CE CODEOWNERS approval is informational only | GitLab settings; the team working agreement | §3's CE notes, verbatim | Red has to mean "does not merge"; where the platform cannot hard-block, the fallback is named in writing (§8.1) rather than pretended away |
| **Monday, afternoon** | **Bilguun** (developer) | Picks up the team's next qualifying work item — the first feature under the convention | The work tracker; a new feature branch | The lifecycle [feature-walkthrough.md](feature-walkthrough.md) replays, from its Day 1 | Adoption ends where the walkthrough begins |
