#!/usr/bin/env python3
"""Convert a standard feature spec folder to OpenSpec change structure, and back.

    uv run migration/convert.py <feature-dir> <out-dir>              # forward
    uv run migration/convert.py --reverse <change-dir> <out-dir>     # back
    uv run migration/convert.py --round-trip <feature-dir>           # CI gate

Forward mapping (per migration/PLAYBOOK.md):

    spec.md   -> openspec/changes/<slug>/specs/<slug>/spec.md
                 (requirement bullets become OpenSpec `### Requirement:`
                 blocks) + a generated proposal.md
    plan.md   -> openspec/changes/<slug>/design.md   (verbatim — a Design
                 Document is valid freeform OpenSpec design)
    tasks.md  -> openspec/changes/<slug>/tasks.md    (verbatim — checkbox
                 markdown either way)

Standard-specific metadata (title, Status line, field table, intro prose) has
no OpenSpec home; it is preserved in a ```sdd-preamble fenced block
at the top of the converted spec so the conversion loses nothing and
--reverse reconstructs the original exactly. proposal.md is derived output;
--reverse ignores it.

Constitution/profile content is out of scope by design: profile material is
plain prose inside design sections and migrates untouched (the
migration-isolation rule, PLAYBOOK §2); the constitution mapping is a human
step in the playbook.

--round-trip converts forward then back into temp dirs and fails unless the
reconstruction is normalized-identical (trailing whitespace and blank-run
collapse only). Wired into checks.yml and the tri-OS matrix on every
push/PR — the exit stays a *tested* capability (SDD-STANDARD §9.4).

Stdlib + pathlib only.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
import tempfile
from pathlib import Path

PREAMBLE_FENCE = "sdd-preamble"
REQ_BULLET_RE = re.compile(r"^- \*\*(R-\d+)\*\* ?(.*)$")
REQ_BLOCK_RE = re.compile(r"^### Requirement: (R-\d+)$")
SECTION_RE = re.compile(r"^## ", re.MULTILINE)
ARTIFACTS = ("spec.md", "plan.md", "tasks.md")


def die(message: str) -> "NoReturn":  # noqa: F821
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(2)


def read(path: Path) -> str:
    if not path.is_file():
        die(f"{path.as_posix()} missing")
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def split_sections(text: str) -> tuple[str, list[str]]:
    """Preamble (before the first `## `) and the `## `-led sections."""
    matches = list(SECTION_RE.finditer(text))
    if not matches:
        return text, []
    preamble = text[: matches[0].start()]
    sections = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append(text[match.start():end])
    return preamble, sections


def feature_title(spec_text: str) -> str:
    match = re.search(r"^# Requirements — (.+)$", spec_text, re.MULTILINE)
    return match.group(1).strip() if match else "converted-feature"


# -- spec.md: standard -> OpenSpec -----------------------------------------


def requirements_to_openspec(section: str) -> str:
    """`- **R-n** ...` bullets (2-space continuations) -> Requirement blocks."""
    lines = section.splitlines()
    heading = lines[0]
    blocks: list[list[str]] = []
    current: list[str] | None = None
    for line in lines[1:]:
        bullet = REQ_BULLET_RE.match(line)
        if bullet:
            current = [f"### Requirement: {bullet.group(1)}", "", bullet.group(2)]
            blocks.append(current)
        elif line.startswith("  ") and current is not None:
            current.append(line[2:])
        elif line.strip() == "":
            current = None
        else:
            die(f"unexpected line in requirements section: {line!r} "
                "(the converter expects `- **R-n**` bullets with two-space "
                "continuations)")
    out = [heading, ""]
    for block in blocks:
        out.extend(block)
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def openspec_to_requirements(section: str) -> str:
    """Requirement blocks -> `- **R-n**` bullets with 2-space continuations."""
    lines = section.splitlines()
    heading = lines[0]
    out = [heading, ""]
    rid: str | None = None
    body: list[str] = []

    def flush() -> None:
        nonlocal rid, body
        if rid is None:
            return
        while body and body[-1] == "":
            body.pop()
        while body and body[0] == "":
            body.pop(0)
        first, *rest = body or [""]
        out.append(f"- **{rid}** {first}")
        out.extend(f"  {line}" if line else "" for line in rest)
        rid, body = None, []

    for line in lines[1:]:
        block = REQ_BLOCK_RE.match(line)
        if block:
            flush()
            rid = block.group(1)
        elif rid is not None:
            body.append(line)
    flush()
    return "\n".join(out).rstrip() + "\n"


def spec_forward(spec_text: str) -> str:
    preamble, sections = split_sections(spec_text)
    title = feature_title(spec_text)
    out = [
        f"# {title} Specification",
        "",
        f"```{PREAMBLE_FENCE}",
        preamble.rstrip(),
        "```",
        "",
    ]
    for section in sections:
        heading = section.splitlines()[0]
        if "Requirements" in heading:
            out.append(requirements_to_openspec(section))
        else:
            out.append(section.rstrip() + "\n")
    return "\n".join(out)


def spec_reverse(openspec_text: str) -> str:
    fence_re = re.compile(
        rf"^```{PREAMBLE_FENCE}\n(.*?)\n```$", re.MULTILINE | re.DOTALL
    )
    fence = fence_re.search(openspec_text)
    if not fence:
        die(f"no {PREAMBLE_FENCE} block found - was this produced by "
            "convert.py? Hand-authored OpenSpec specs are migrated per the "
            "playbook, not mechanically reversed")
    preamble = fence.group(1) + "\n\n"
    _, sections = split_sections(openspec_text)
    out = [preamble]
    for section in sections:
        heading = section.splitlines()[0]
        if "Requirements" in heading and "### Requirement:" in section:
            out.append(openspec_to_requirements(section))
        else:
            out.append(section.rstrip() + "\n")
    return "\n".join(out)


# -- change-level conversion ----------------------------------------------


def proposal_for(title: str, slug: str, spec_text: str) -> str:
    _, sections = split_sections(spec_text)
    why = ""
    for section in sections:
        heading = section.splitlines()[0]
        if "Purpose" in heading:
            body = "\n".join(section.splitlines()[1:]).strip()
            why = body.split("\n\n")[0]
            break
    return (
        f"# Change: {title}\n\n"
        f"## Why\n\n{why or 'See the converted specification.'}\n\n"
        "## What Changes\n\n"
        f"- Adds the `{title}` capability - full requirements in "
        f"`specs/{slug}/spec.md`, design in `design.md`, work plan in "
        "`tasks.md`.\n\n"
        "## Source\n\n"
        "Converted from an SDD feature folder by "
        "`migration/convert.py`; this file is derived output and is not "
        "used by the reverse conversion.\n"
    )


def forward(feature_dir: Path, out_dir: Path) -> Path:
    slug = feature_dir.resolve().name
    spec_text = read(feature_dir / "spec.md")
    change_dir = out_dir / "openspec" / "changes" / slug
    write(change_dir / "specs" / slug / "spec.md", spec_forward(spec_text))
    write(change_dir / "design.md", read(feature_dir / "plan.md"))
    write(change_dir / "tasks.md", read(feature_dir / "tasks.md"))
    write(change_dir / "proposal.md",
          proposal_for(feature_title(spec_text), slug, spec_text))
    print(f"forward: {feature_dir.as_posix()} -> {change_dir.as_posix()}")
    return change_dir


def reverse(change_dir: Path, out_dir: Path) -> Path:
    slug = change_dir.resolve().name
    spec_candidates = sorted((change_dir / "specs").glob("*/spec.md")) \
        if (change_dir / "specs").is_dir() else []
    if not spec_candidates:
        die(f"no specs/*/spec.md under {change_dir.as_posix()}")
    out_feature = out_dir / slug
    write(out_feature / "spec.md", spec_reverse(read(spec_candidates[0])))
    write(out_feature / "plan.md", read(change_dir / "design.md"))
    write(out_feature / "tasks.md", read(change_dir / "tasks.md"))
    print(f"reverse: {change_dir.as_posix()} -> {out_feature.as_posix()}")
    return out_feature


# -- round-trip gate --------------------------------------------------------


def normalize(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines()]
    out: list[str] = []
    for line in lines:
        if line == "" and out and out[-1] == "":
            continue
        out.append(line)
    while out and out[0] == "":
        out.pop(0)
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out) + "\n"


def round_trip(feature_dir: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="sdd-roundtrip-") as tmp:
        tmp_path = Path(tmp)
        change_dir = forward(feature_dir, tmp_path / "fwd")
        restored = reverse(change_dir, tmp_path / "rev")
        failed = False
        for name in ARTIFACTS:
            original = normalize(read(feature_dir / name))
            returned = normalize(read(restored / name))
            if original != returned:
                failed = True
                print(f"\nDIVERGENCE in {name}:", file=sys.stderr)
                sys.stderr.writelines(difflib.unified_diff(
                    original.splitlines(keepends=True),
                    returned.splitlines(keepends=True),
                    fromfile=f"original/{name}", tofile=f"round-trip/{name}",
                ))
        if failed:
            print("\nFAIL: the exit is not currently a tested capability - "
                  "fix convert.py (or the fixture) before merging (SDD-STANDARD §9.4)",
                  file=sys.stderr)
            sys.exit(1)
    print(f"round-trip OK: {', '.join(ARTIFACTS)} reconstruct "
          "normalized-identical")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--reverse", action="store_true",
                       help="convert an OpenSpec change dir back to a "
                            "standard feature folder")
    group.add_argument("--round-trip", action="store_true",
                       help="forward + reverse into temp dirs; fail on any "
                            "normalized divergence (the CI gate)")
    parser.add_argument("source", help="feature dir (forward/round-trip) or "
                                       "change dir (--reverse)")
    parser.add_argument("out", nargs="?",
                        help="output dir (not used with --round-trip)")
    args = parser.parse_args()

    source = Path(args.source)
    if not source.is_dir():
        die(f"{source.as_posix()} is not a directory")

    if args.round_trip:
        round_trip(source)
    elif args.reverse:
        if not args.out:
            die("--reverse needs an output directory")
        reverse(source, Path(args.out))
    else:
        if not args.out:
            die("forward conversion needs an output directory")
        forward(source, Path(args.out))


if __name__ == "__main__":
    main()
