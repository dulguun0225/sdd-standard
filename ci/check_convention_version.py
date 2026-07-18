#!/usr/bin/env python3
"""Convention currency check: is this repo on the standard's current version?

    uv run ci/check_convention_version.py --repo <product-repo> --standard <sdd-standard checkout>

Compares the repo's `.specify/sdd.json` (written by
`bootstrap/init.py`) against a local sdd-standard checkout — its
SDD-STANDARD.md version and speckit/PINNED-VERSION — the seeded
constitution's shared-principles block against the checkout's template
(SDD-STANDARD §2.4: seeded principles are never removed or weakened), and
the profile copy installed by bootstrap (`.specify/memory/profile.md`)
against the checkout's profile (SDD-STANDARD §8.2: profile changes land
upstream by PR, never by editing the copy).

Non-zero exit with remediation on any mismatch. Stdlib only.
SDD-STANDARD §8.2.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def fail(problem: str, remediation: str) -> "NoReturn":  # noqa: F821
    print(f"FAIL: {problem}", file=sys.stderr)
    print(f"\nFix:\n  {remediation}", file=sys.stderr)
    sys.exit(1)


SHARED_HEADING = "## Shared principles"


def shared_block(text: str) -> str | None:
    """The shared-principles block: its heading up to the next `## ` heading.

    Returns None when the heading is absent. The block carries no bootstrap
    placeholders by construction ([PROJECT NAME] and [CONVENTION VERSION]
    live in the template's intro), so seeded copies compare byte-for-byte.
    """
    lines = text.splitlines()
    start = next(
        (i for i, line in enumerate(lines) if line.startswith(SHARED_HEADING)),
        None,
    )
    if start is None:
        return None
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")),
        len(lines),
    )
    return "\n".join(lines[start:end]).strip()


def standard_version(standard: Path) -> str:
    doc = standard / "standard" / "SDD-STANDARD.md"
    try:
        match = re.search(r"\*\*Version:\s*([^*\s]+)\*\*",
                          doc.read_text(encoding="utf-8"))
    except OSError:
        match = None
    if not match:
        fail(f"cannot read the convention version from {doc}",
             "point --standard at a complete sdd-standard checkout")
    return match.group(1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", default=".", metavar="PATH",
                        help="product repo to check (default: .)")
    parser.add_argument("--standard", required=True, metavar="PATH",
                        help="local sdd-standard checkout at the standard's "
                             "current release")
    args = parser.parse_args()

    repo = Path(args.repo)
    standard = Path(args.standard)

    marker_path = repo / ".specify" / "sdd.json"
    if not marker_path.is_file():
        fail(f"{marker_path.as_posix()} missing - this repo was not "
             "bootstrapped onto the convention",
             "uv run bootstrap/init.py <target> --integration <agent> "
             "--profile <profile>   (from the sdd-standard checkout; "
             "manual template copying is prohibited, SDD-STANDARD §9.2)")

    try:
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as err:
        fail(f"{marker_path.as_posix()} unreadable: {err}",
             "re-run bootstrap/init.py to regenerate it")

    expected_version = standard_version(standard)
    expected_pin_file = standard / "speckit" / "PINNED-VERSION"
    expected_pin = expected_pin_file.read_text(encoding="utf-8").strip() \
        if expected_pin_file.is_file() else None
    if expected_pin is None:
        fail(f"{expected_pin_file.as_posix()} missing",
             "point --standard at a complete sdd-standard checkout")

    problems = []
    if marker.get("convention_version") != expected_version:
        problems.append(
            f"convention_version is {marker.get('convention_version')!r}, "
            f"current release is {expected_version!r}")
    if marker.get("speckit_pin") != expected_pin:
        problems.append(
            f"speckit_pin is {marker.get('speckit_pin')!r}, the standard's "
            f"pin is {expected_pin!r}")

    template_path = (standard / "speckit" / "presets" / "sdd" / "templates"
                     / "constitution-template.md")
    try:
        expected_block = shared_block(
            template_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError):
        expected_block = None
    if expected_block is None:
        fail(f"{template_path.as_posix()} missing or lacks the "
             f"'{SHARED_HEADING}' block",
             "point --standard at a complete sdd-standard checkout")

    constitution_path = repo / ".specify" / "memory" / "constitution.md"
    if not constitution_path.is_file():
        problems.append(
            f"{constitution_path.as_posix()} missing - the seeded "
            "constitution was removed")
    else:
        try:
            constitution_text = constitution_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as err:
            constitution_text = None
            problems.append(
                f"{constitution_path.as_posix()} unreadable as UTF-8 "
                f"({err}) - re-save it as UTF-8 with LF endings")
        if constitution_text is not None:
            found_block = shared_block(constitution_text)
            if found_block is None:
                problems.append(
                    f"constitution.md lacks the '{SHARED_HEADING}' block "
                    "seeded by bootstrap")
            elif found_block != expected_block:
                problems.append(
                    "constitution.md's shared-principles block differs from "
                    "the pinned template (SDD-STANDARD §8.2/§2.4: the seeded "
                    "block is compared byte-for-byte; seeded principles are "
                    "never removed or weakened)")

    profile_name = marker.get("profile")
    if not isinstance(profile_name, str) or not profile_name:
        problems.append(
            f"{marker_path.as_posix()} lacks a 'profile' entry - "
            "re-run bootstrap/init.py to regenerate it")
    else:
        source_path = (standard / "standard" / "profiles" / profile_name
                       / "profile.md")
        try:
            expected_profile = source_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            expected_profile = None
        if expected_profile is None:
            fail(f"{source_path.as_posix()} missing - the checkout has no "
                 f"{profile_name!r} profile",
                 "point --standard at a complete sdd-standard checkout at "
                 "the standard's current release")
        copy_path = repo / ".specify" / "memory" / "profile.md"
        if not copy_path.is_file():
            problems.append(
                f"{copy_path.as_posix()} missing - the profile copy "
                "installed by bootstrap was removed, or this repo was "
                "bootstrapped before the standard shipped profile copies")
        else:
            try:
                found_profile = copy_path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as err:
                found_profile = None
                problems.append(
                    f"{copy_path.as_posix()} unreadable as UTF-8 ({err}) - "
                    "re-save it as UTF-8 with LF endings")
            if found_profile is not None and found_profile != expected_profile:
                problems.append(
                    f"profile.md differs from the standard's {profile_name!r} "
                    "profile (SDD-STANDARD §8.2: the copy is compared "
                    "byte-for-byte; profile changes land upstream by PR, "
                    "never by editing the copy)")

    if problems:
        profile_hint = profile_name if isinstance(profile_name, str) \
            and profile_name else "<profile>"
        fail("; ".join(problems),
             "follow the convention upgrade steps in docs/adopting-a-repo.md "
             "of the sdd-standard repository (upgrades land as reviewed PRs, "
             "never by hand-editing .specify/). For a drifted constitution, "
             "restore the '## Shared principles' block from "
             "speckit/presets/sdd/templates/constitution-template.md at the "
             "pinned release - repo-specific principles belong under "
             "'## Repo principles'. For a drifted or missing profile copy, "
             "restore .specify/memory/profile.md from "
             f"standard/profiles/{profile_hint}/profile.md at the pinned "
             "release")

    print(f"OK: convention {expected_version}, Spec Kit pin {expected_pin}, "
          f"profile {marker.get('profile')!r}, variant "
          f"{marker.get('variant')!r}, constitution shared block and "
          f"profile copy intact")


if __name__ == "__main__":
    main()
