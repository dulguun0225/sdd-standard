#!/usr/bin/env python3
"""Convention currency check: is this repo on the standard's current version?

    uv run ci/check_convention_version.py --repo <product-repo> --standard <sdd-standard checkout>

Compares the repo's `.specify/sdd.json` (written by
`bootstrap/init.py`) against a local sdd-standard checkout — its
SDD-STANDARD.md version and speckit/PINNED-VERSION.

Non-zero exit with remediation on any mismatch. Stdlib only.
SDD-STANDARD §8.2.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def fail(problem: str, remediation: str) -> None:
    print(f"FAIL: {problem}", file=sys.stderr)
    print(f"\nFix:\n  {remediation}", file=sys.stderr)
    sys.exit(1)


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

    if problems:
        fail("; ".join(problems),
             "follow the convention upgrade steps in docs/adopting-a-repo.md "
             "of the sdd-standard repository (upgrades land as reviewed PRs, "
             "never by hand-editing .specify/)")

    print(f"OK: convention {expected_version}, Spec Kit pin {expected_pin}, "
          f"profile {marker.get('profile')!r}, variant "
          f"{marker.get('variant')!r}")


if __name__ == "__main__":
    main()
