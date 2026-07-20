# Adopting a repo — the team-lead guide

**Informative.** This guide explains how adoption works; the binding rules
live in [SDD-STANDARD.md](../standard/SDD-STANDARD.md). In any conflict,
the standard wins.

The convention is pre-1.0 and still being validated on demo projects.
Coordinate with the standard owner (SDD-STANDARD §13) before adopting a
real repo, so pre-1.0 changes do not surprise you.

## 1. What you need, and why

The convention requires **capabilities, not vendors**. Anything
providing these six works — GitHub, GitLab (SaaS or self-hosted CE),
Bitbucket, or Jenkins-backed setups included:

- **A git repository per product, on a host with a review flow
  (PRs/MRs).** Approvals are commits: a gate is passed by the approver
  adding the Status line in their own change (§3.2). So git history
  shows who approved what, and when. No approval bot, app, or side
  database. The same-PR rule (§5.2) needs the PR/MR unit to exist —
  spec update and code change merge together or not at all. And the
  Review gate needs an assignable reviewer who is not the implementer
  (§3.3).
- **One CI job on every push/PR.** This is the merge gate (§8.1).
  `check_spec_structure.py --repo .` turns the pipeline red when an
  artifact outruns its gate — a `plan.md` next to a DRAFT `spec.md` —
  before a human has to catch it. `check_convention_version.py` reports
  when the repo falls behind the pinned convention, or when the seeded
  constitution/profile copies were edited locally (§8.2). The job is
  one Linux container or shell with git and uv. Stdlib Python, no
  services, seconds to run. Any runner works: GitHub Actions,
  GitLab CI (on CE one runner is enough, and a project Maintainer can
  register it), Jenkins, Azure Pipelines. §3 below shows three.
- **Merge blocking, where your plan has it.** Red must mean "does not
  merge". Turn on the platform's mechanism where it exists: required
  status checks, "pipelines must succeed". Where it does not exist
  (branch protection on free-plan private GitHub repos, CODEOWNERS
  approval on GitLab CE), the check still runs. A red pipeline is then
  a merge-blocker by convention, recorded in the team agreement. That
  fallback is §8.1's own wording.
- **uv and git on every developer machine.** All convention tooling is
  one cross-platform Python implementation run via `uv run`. No local
  Python to manage, no `.sh`/`.ps1` twins to drift apart. Bootstrap
  installs the pinned Spec Kit itself via `uv tool run` — nobody ever
  installs Spec Kit by hand (§9.2). On Windows, Git Bash ships with Git
  for Windows (the scaffold scripts' single variant, §10.1). The
  one-time `python3` fix in the
  [README per-OS notes](../README.md#per-os-setup-notes) is
  recommended. The bootstrap preflight checks all of this and prints
  the exact command when something is missing.
- **A clone of sdd-standard at the pinned release tag.** Bootstrap, the
  templates, and both CI checks come from it. That is how every
  adopting repo speaks one dialect at a known version, instead of
  hand-copied templates quietly diverging (§9.2, §9.3). CI clones it
  too — the first line of every snippet in §3.
- **A work tracker — any.** Items carry a summary and a link to the
  spec folder, nothing more (§4.3). Acceptance criteria live in the
  spec alone, so the tracker never disagrees with the spec. No
  integration required; a link is all it takes.

Deliberately **not** required: a specific CI vendor; a specific AI
agent or IDE (§1 scopes the choice out — bootstrap wires whichever you
pass to `--integration`, or `generic` for none); a central specs
repository (§2.3 — there deliberately is none); any platform bot or app
for approvals (an approval is a plain commit).

## 2. Bootstrap

Clone this repo **at the pinned release tag** (not main), then from
the clone:

```
uv run bootstrap/init.py <path-to-your-repo> --integration <your-agent> --profile backend-services
```

- `--integration` is your team's coding agent (mandatory — there is no
  default on purpose; `generic` if you use none or several).
- `--profile` binds your Design Documents' contract vocabulary. v1.0 ships
  one profile: `backend-services`.
- The target can be a fresh directory or an existing repo. Existing
  specs and code are untouched; the scaffold adds `.specify/` and agent
  command files.

Commit the scaffold as its own commit before anything else. Never copy
templates between repos by hand. That is how divergent dialects start,
and the standard prohibits it.

## 3. Wire the CI gate

The merge gate is one Linux job running `check_spec_structure.py` against
your repo. Copy the script's invocation, not the script — it lives in
sdd-standard and comes along when you clone at the pin.

### GitHub Actions

```yaml
# .github/workflows/spec-gate.yml
name: spec-gate
on: [push, pull_request]
jobs:
  spec-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - name: Get the convention at the pinned release
        # use your organization's sdd-standard fork/home
        run: git clone --depth 1 --branch <PINNED-RELEASE-TAG> https://example.com/sdd-standard sdd-standard
      - name: Spec structure gate
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
spec-gate:
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
- **CODEOWNERS approval enforcement is a Premium feature — on CE the file
  is informational only.** Reviewer discipline has to carry what the
  platform won't; say so in your team working agreement rather than
  pretending the gate exists.

### Jenkins

Any Linux agent with git and uv on PATH (or a container that has both,
via the Docker plugin):

```groovy
// Jenkinsfile
pipeline {
  agent { label 'linux' }
  stages {
    stage('spec-gate') {
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
- `check_convention_version.py` in your CI tells you when your repo is
  behind the convention release. It also tells you when the seeded
  constitution's shared-principles block was edited: SDD-STANDARD §8.2
  compares it byte-for-byte against the pinned template. Repo-specific
  principles go under "Repo principles".
- Bootstrap also installs your profile's full text at
  `.specify/memory/profile.md`, so its contract defaults are in the
  repo your agents actually read. The same CI check compares that copy
  against the standard's profile at the pinned release. A profile
  change lands upstream by PR to sdd-standard, never by editing the
  copy.

## 5. Roles before you start

Bind the four gate-approver roles (SDD-STANDARD §3.3) to named people and
record them in your repo (README or team agreement): requirements — product
authority; design and tasks — technical authority; review — a reviewer who
is never the implementer. Approvers read
[reviewing-specs.md](reviewing-specs.md) before their first gate.
[feature-walkthrough.md](feature-walkthrough.md) shows the whole team
around one feature: who acts at each step, in which PR, on which day.
