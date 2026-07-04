#!/usr/bin/env python3
"""Merge gate: spec folders exist and are well-formed.

    uv run ci/check_spec_structure.py --repo <product-repo-path>
    uv run ci/check_spec_structure.py --self

Checks every feature folder (`specs/*/`; with --self also `examples/*/`):

  * spec.md exists and each present artifact carries a Status line
    (em dash or plain hyphen accepted in APPROVED lines)
  * gate order holds: no plan.md without an APPROVED spec.md, no tasks.md
    without an APPROVED plan.md
  * R-ids are unique within spec.md
  * every task in tasks.md carries at least one [R-n] that exists in spec.md
  * filenames are lowercase-kebab-case (universal conventions README.md,
    CODEOWNERS, LICENSE are allowed)
  * text files use LF line endings

Non-zero exit on any violation; each violation names its file. Runs the
same locally and on CI, on all three OS — stdlib + pathlib only.
The product-repo merge gate of SDD-STANDARD §8.1.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

STATUS_RE = re.compile(r"Status:\s*(.+?)\**\s*$")
APPROVED_RE = re.compile(r"^APPROVED\s*[—–-]\s*\S.*$")
RID_DEF_RE = re.compile(r"^\s*-\s+\*\*(R-\d+)\*\*", re.MULTILINE)
TASK_START_RE = re.compile(r"^\s*-\s+\[[ xX]\]\s+\*\*(T-\d+)\*\*", re.MULTILINE)
RID_REF_RE = re.compile(r"\[(R-\d+)\]")
KEBAB_RE = re.compile(r"^[a-z0-9][a-z0-9.-]*$")
KEBAB_EXCEPTIONS = {"README.md", "CODEOWNERS", "LICENSE"}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yml", ".yaml", ".py", ".toml"}

violations: list[str] = []


def violation(path: Path, message: str) -> None:
    violations.append(f"{path.as_posix()}: {message}")


def status_of(path: Path) -> str | None:
    """The artifact's Status value, or None when no Status line exists."""
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "Status:" in line:
            match = STATUS_RE.search(line)
            if match:
                return match.group(1).strip().rstrip("*").strip()
    return None


def is_approved(status: str | None) -> bool:
    return status is not None and APPROVED_RE.match(status) is not None


def check_feature(feature: Path) -> None:
    spec = feature / "spec.md"
    plan = feature / "plan.md"
    tasks = feature / "tasks.md"

    if not spec.is_file():
        violation(feature, "spec.md missing - every feature folder needs one")
        return

    spec_status = status_of(spec)
    if spec_status is None:
        violation(spec, "no Status line (expected `Status: DRAFT` or "
                        "`Status: APPROVED — <name>, <date>`)")

    rids = RID_DEF_RE.findall(spec.read_text(encoding="utf-8", errors="replace"))
    seen: set[str] = set()
    for rid in rids:
        if rid in seen:
            violation(spec, f"duplicate requirement id {rid} - R-ids are "
                            "never reused")
        seen.add(rid)

    plan_status = None
    if plan.is_file():
        plan_status = status_of(plan)
        if plan_status is None:
            violation(plan, "no Status line")
        if not is_approved(spec_status):
            violation(plan, "plan.md exists but spec.md is not APPROVED - "
                            "the requirements gate comes first")

    if tasks.is_file():
        tasks_status = status_of(tasks)
        if tasks_status is None:
            violation(tasks, "no Status line")
        if not plan.is_file() or not is_approved(plan_status):
            violation(tasks, "tasks.md exists but plan.md is missing or not "
                             "APPROVED - the design gate comes first")
        check_task_references(tasks, seen)

    check_filenames(feature)
    check_line_endings(feature)


def check_task_references(tasks: Path, valid_rids: set[str]) -> None:
    text = tasks.read_text(encoding="utf-8", errors="replace")
    starts = list(TASK_START_RE.finditer(text))
    if not starts:
        violation(tasks, "no tasks found (expected `- [ ] **T-n**` items)")
        return
    tids_seen: set[str] = set()
    for index, match in enumerate(starts):
        tid = match.group(1)
        if tid in tids_seen:
            violation(tasks, f"duplicate task id {tid} - T-ids are never reused")
        tids_seen.add(tid)
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        chunk = text[match.start():end]
        refs = RID_REF_RE.findall(chunk)
        if not refs:
            violation(tasks, f"{tid} carries no [R-n] reference")
        for rid in refs:
            if valid_rids and rid not in valid_rids:
                violation(tasks, f"{tid} references {rid}, which spec.md "
                                 "does not define")


def check_filenames(feature: Path) -> None:
    for path in feature.rglob("*"):
        name = path.name
        if name in KEBAB_EXCEPTIONS or name.startswith("."):
            continue  # dot-files are git plumbing, not spec artifacts
        if not KEBAB_RE.match(name):
            violation(path, "filename is not lowercase-kebab-case "
                            "(SDD-STANDARD §2.2)")


def check_line_endings(feature: Path) -> None:
    for path in feature.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if b"\r" in path.read_bytes():
            violation(path, "CRLF line endings - all text files are LF "
                            "(SDD-STANDARD §2.2; check .gitattributes)")


def scan_root(root: Path) -> int:
    """Check every feature folder under one root; return how many."""
    if not root.is_dir():
        return 0
    count = 0
    for feature in sorted(p for p in root.iterdir() if p.is_dir()):
        count += 1
        check_feature(feature)
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--repo", metavar="PATH",
                      help="product repo to check (its specs/ folders)")
    mode.add_argument("--self", dest="self_mode", action="store_true",
                      help="check this sdd-standard repo (specs/ and examples/)")
    args = parser.parse_args()

    if args.self_mode:
        base = Path(__file__).resolve().parent.parent
        roots = [base / "specs", base / "examples"]
    else:
        base = Path(args.repo)
        if not base.is_dir():
            print(f"ERROR: {base} is not a directory", file=sys.stderr)
            sys.exit(2)
        roots = [base / "specs"]

    total = sum(scan_root(root) for root in roots)

    if violations:
        print(f"FAIL: {len(violations)} violation(s) in {total} feature "
              f"folder(s):\n", file=sys.stderr)
        for entry in violations:
            print(f"  {entry}", file=sys.stderr)
        print("\nThe convention is defined in standard/SDD-STANDARD.md of "
              "the sdd-standard repository.", file=sys.stderr)
        sys.exit(1)

    print(f"OK: {total} feature folder(s) checked, no violations")


if __name__ == "__main__":
    main()
