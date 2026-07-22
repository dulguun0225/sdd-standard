#!/usr/bin/env python3
"""Merge gate: spec folders exist and are well-formed.

    uv run ci/check_spec_structure.py --repo <product-repo-path>
    uv run ci/check_spec_structure.py --self

Checks every feature folder (`specs/*/`; with --self also `examples/*/`):

  * spec.md exists in every feature folder
  * artifact order holds by presence (SDD-STANDARD §3.1): no tasks.md
    without plan.md (a missing spec.md is already a violation on its own)
  * R-ids are unique within spec.md
  * every task in tasks.md carries at least one [R-n] that exists in spec.md
  * every local `contracts/...` path referenced from plan.md exists in the
    feature folder (URLs and registry references are out of scope)
  * filenames are lowercase-kebab-case (universal conventions README.md,
    CODEOWNERS, LICENSE are allowed)
  * text files use LF line endings

With --self it additionally asserts layer congruence: the plan-template's
contract-table headers match the backend-services profile's column lists —
redundant spec layers help only while they agree; drifted layers hurt.

Advisory (WARNING lines, never merge-blocking): vague wording in spec.md
requirement bullets ("quickly", "appropriate", …) — lexical vagueness
survives well-formed EARS; replace the word with a number and a unit, or
leave it with a stated reason.

Non-zero exit on any violation; each violation names its file. Runs the
same locally and on CI, on all three OS — stdlib + pathlib only.
The product-repo merge gate of SDD-STANDARD §8.1.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RID_DEF_RE = re.compile(r"^\s*-\s+\*\*(R-\d+)\*\*", re.MULTILINE)
TASK_START_RE = re.compile(r"^\s*-\s+\[[ xX]\]\s+\*\*(T-\d+)\*\*", re.MULTILINE)
RID_REF_RE = re.compile(r"\[(R-\d+)\]")
KEBAB_RE = re.compile(r"^[a-z0-9][a-z0-9.-]*$")
KEBAB_EXCEPTIONS = {"README.md", "CODEOWNERS", "LICENSE"}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yml", ".yaml", ".py", ".toml"}
# Local contract paths only: a `contracts/…` token not preceded by a path,
# URL, or registry-reference character. Schema-registry refs and URLs
# (`…/contracts/…`, `registry:contracts/…`) are deliberately not checked.
CONTRACT_PATH_RE = re.compile(r"(?<![\w/:.@-])contracts/[A-Za-z0-9][A-Za-z0-9._/-]*")
# Vague words that survive well-formed EARS phrasing ("respond quickly" is
# valid EARS) and leave the implementer to pick the number. Advisory only.
VAGUE_WORD_RE = re.compile(
    r"\b(quickly|soon|eventually|fast|timely|promptly|appropriate(?:ly)?|"
    r"reasonable|reasonably|adequate(?:ly)?|sufficient(?:ly)?|"
    r"efficient(?:ly)?|robust|seamless(?:ly)?|gracefully|properly|"
    r"user-friendly|intuitive|flexible|optimal|simple|easy)\b",
    re.IGNORECASE)
RID_BULLET_RE = re.compile(r"^\s*-\s+\*\*(R-\d+)\*\*")

violations: list[str] = []
warnings: list[str] = []


def violation(path: Path, message: str) -> None:
    violations.append(f"{path.as_posix()}: {message}")


def warning(path: Path, message: str) -> None:
    warnings.append(f"{path.as_posix()}: {message}")


def check_feature(feature: Path) -> None:
    spec = feature / "spec.md"
    plan = feature / "plan.md"
    tasks = feature / "tasks.md"

    if not spec.is_file():
        violation(feature, "spec.md missing - every feature folder needs one")
        return

    rids = RID_DEF_RE.findall(spec.read_text(encoding="utf-8", errors="replace"))
    seen: set[str] = set()
    for rid in rids:
        if rid in seen:
            violation(spec, f"duplicate requirement id {rid} - R-ids are "
                            "never reused")
        seen.add(rid)

    check_vague_words(spec)

    if plan.is_file():
        check_contract_links(plan, feature)

    if tasks.is_file():
        if not plan.is_file():
            violation(tasks, "tasks.md exists but plan.md is missing - the "
                             "Design Document comes before the Task List "
                             "(SDD-STANDARD §3.1)")
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


def check_contract_links(plan: Path, feature: Path) -> None:
    """Every local contracts/… path plan.md references must exist."""
    text = plan.read_text(encoding="utf-8", errors="replace")
    checked: set[str] = set()
    for match in CONTRACT_PATH_RE.finditer(text):
        ref = match.group(0).rstrip(".,;:")
        if ref in checked:
            continue
        checked.add(ref)
        if not (feature / ref).is_file():
            violation(plan, f"references {ref}, which does not exist - "
                            f"create {(feature / ref).as_posix()} or fix "
                            "the reference (a schema link must point at a "
                            "real file)")


def check_vague_words(spec: Path) -> None:
    """Advisory: vague wording inside requirement bullets. Never blocks."""
    current_rid: str | None = None
    for line in spec.read_text(encoding="utf-8", errors="replace").splitlines():
        started = RID_BULLET_RE.match(line)
        if started:
            current_rid = started.group(1)
        elif current_rid and not line.startswith("  "):
            current_rid = None  # a bullet ends where its continuation does
        if current_rid:
            for word in VAGUE_WORD_RE.findall(line):
                warning(spec, f'{current_rid} says "{word.lower()}" - '
                              "replace it with a number and a unit; "
                              "advisory, never merge-blocking")


def section_lines(text: str, heading: str) -> list[str]:
    """The lines of one `## …` section, heading excluded."""
    lines: list[str] = []
    active = False
    for line in text.splitlines():
        if line.strip() == heading:
            active = True
            continue
        if active and line.startswith("## "):
            break
        if active:
            lines.append(line)
    return lines


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def profile_columns(lines: list[str]) -> list[str]:
    """First-column values of the profile's `| Column | Content |` table."""
    columns: list[str] = []
    in_table = False
    for line in lines:
        if not line.strip().startswith("|"):
            if in_table:
                break
            continue
        cells = table_cells(line)
        if not in_table:
            if cells and cells[0] == "Column":
                in_table = True
            continue
        if set(cells[0]) <= set("-: "):
            continue  # the header separator row
        columns.append(cells[0])
    return columns


def template_header(lines: list[str]) -> list[str]:
    """Header cells of the first markdown table in a template section."""
    for line in lines:
        if line.strip().startswith("|"):
            return table_cells(line)
    return []


def check_layer_congruence(base: Path) -> None:
    """--self only: plan-template table headers match the profile columns.

    The template comments and the profile are redundant spec layers;
    redundancy helps only while the layers agree, so their table shapes
    are asserted equal here.
    """
    profile = base / "standard" / "profiles" / "backend-services" / "profile.md"
    template = (base / "speckit" / "presets" / "sdd" / "templates"
                / "plan-template.md")
    for path in (profile, template):
        if not path.is_file():
            violation(path, "missing - required for the layer-congruence "
                            "check (--self)")
            return
    profile_text = profile.read_text(encoding="utf-8", errors="replace")
    template_text = template.read_text(encoding="utf-8", errors="replace")
    pairs = [
        ("## 2. Synchronous contract defaults", "## 3. Synchronous contracts"),
        ("## 3. Asynchronous contract defaults", "## 4. Asynchronous contracts"),
    ]
    for profile_heading, template_heading in pairs:
        expected = profile_columns(section_lines(profile_text, profile_heading))
        found = template_header(section_lines(template_text, template_heading))
        if not expected:
            violation(profile, f'no "| Column | Content |" table under '
                               f'"{profile_heading}" - restore it or update '
                               "check_layer_congruence in this script")
        elif expected != found:
            violation(template, f'contract table under "{template_heading}" '
                                f"does not match the profile's "
                                f'"{profile_heading}" columns - expected '
                                f"{expected}, found {found}; align the "
                                "template with "
                                "standard/profiles/backend-services/profile.md "
                                "in the same PR (drifted layers actively "
                                "mislead implementers)")


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
        check_layer_congruence(base)
    else:
        base = Path(args.repo)
        if not base.is_dir():
            print(f"ERROR: {base} is not a directory", file=sys.stderr)
            sys.exit(2)
        roots = [base / "specs"]

    total = sum(scan_root(root) for root in roots)

    if warnings:
        print(f"WARNING: {len(warnings)} advisory finding(s) - "
              "never merge-blocking:\n")
        for entry in warnings:
            print(f"  {entry}")
        print()

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
