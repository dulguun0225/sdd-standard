# Adopting a repo — the team-lead guide

**Informative.** This guide explains how adoption works; the binding rules
live in [SDD-STANDARD.md](../standard/SDD-STANDARD.md). In any conflict,
the standard wins.

The convention is pre-1.0 and still being validated on demo projects —
coordinate with the standard owner (SDD-STANDARD §13) before adopting a
real repo, so you are not surprised by pre-1.0 changes.

## 1. Prerequisites

Every developer machine: uv and git, per the per-OS notes in the
[README](../README.md#per-os-setup-notes). Windows machines need the
one-time `python3` fix described there — the bootstrap preflight checks it
and prints the exact command if it is missing.

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
- The target can be a fresh directory or an existing repo — existing specs
  and code are untouched; the scaffold adds `.specify/` and agent command
  files.

Commit the scaffold as its own commit before anything else. Never copy
templates between repos by hand — that is how divergent dialects start, and
the standard prohibits it.

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

One Linux runner is enough, and a project **Maintainer** can register it —
no instance admin needed (Settings → CI/CD → Runners → registration token,
then `gitlab-runner register` on any Linux box with the `docker` or `shell`
executor).

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

## 4. Living with the pin

- The Spec Kit version is pinned for all adopting repos
  (`speckit/PINNED-VERSION`).
  Bootstrap always installs the pin; a different `specify` on a developer's
  PATH fails the preflight with the fix.
- Never upgrade Spec Kit locally. Pin changes land in sdd-standard as
  reviewed PRs that pass the full tri-OS matrix first; your repo picks them
  up by re-cloning at the new release tag when a new release is tagged.
- `check_convention_version.py` in your CI tells you when your repo is
  behind the convention release — and when the seeded constitution's
  shared-principles block was edited (SDD-STANDARD §8.2 compares it
  byte-for-byte against the pinned template; repo-specific principles go
  under "Repo principles").

## 5. Roles before you start

Bind the four gate-approver roles (SDD-STANDARD §3.3) to named people and
record them in your repo (README or team agreement): requirements — product
authority; design and tasks — technical authority; review — a reviewer who
is never the implementer. Approvers read
[reviewing-specs.md](reviewing-specs.md) before their first gate.
