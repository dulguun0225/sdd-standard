#!/usr/bin/env python3
"""Bootstrap a product repo onto the SDD convention.

    uv run bootstrap/init.py TARGET --integration <agent> --profile <profile>

Wraps `specify init` (pinned to speckit/PINNED-VERSION, invoked through
`uv tool run` so the pin holds by construction), layers the SDD
preset and review extension from this checkout, seeds the shared constitution
with the chosen stack profile, installs the profile's full text next to it
(`.specify/memory/profile.md`), and records the consumed convention version
in `.specify/sdd.json`.

This is the ONLY supported way to adopt the convention (SDD-STANDARD §9.2).
One implementation for Windows, macOS, and Linux — stdlib + pathlib only.

Every failure prints the exact remediation command.
"""

from __future__ import annotations

import argparse
import datetime
import json
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PIN_FILE = REPO_ROOT / "speckit" / "PINNED-VERSION"
PRESET_DIR = REPO_ROOT / "speckit" / "presets" / "sdd"
EXTENSION_DIR = REPO_ROOT / "speckit" / "extensions" / "sdd"
PROFILES_DIR = REPO_ROOT / "standard" / "profiles"
STANDARD_FILE = REPO_ROOT / "standard" / "SDD-STANDARD.md"

SPECKIT_GIT = "git+https://github.com/github/spec-kit.git"

# The standard's scaffold variant is bash (SDD-STANDARD §10.1). `ps` exists
# for the verification matrix only and is not supported for adoption.
STANDARD_VARIANT = "sh"


def fail(problem: str, remediation: str) -> "NoReturn":  # noqa: F821
    print(f"\nERROR: {problem}", file=sys.stderr)
    print(f"\nFix:\n  {remediation}\n", file=sys.stderr)
    sys.exit(1)


def read_pin() -> str:
    if not PIN_FILE.is_file():
        fail(
            f"pin file missing: {PIN_FILE}",
            "restore speckit/PINNED-VERSION from the sdd-standard repository "
            "(your checkout is incomplete)",
        )
    return PIN_FILE.read_text(encoding="utf-8").strip()


def read_convention_version() -> str:
    """The convention version, parsed from SDD-STANDARD.md's Version line."""
    try:
        text = STANDARD_FILE.read_text(encoding="utf-8")
    except OSError:
        text = ""
    match = re.search(r"\*\*Version:\s*([^*\s]+)\*\*", text)
    if match is None:
        fail(
            f"cannot parse the convention version from {STANDARD_FILE}",
            "re-clone the sdd-standard repository at the pinned release tag "
            "(your checkout is incomplete, or SDD-STANDARD.md's Version line "
            "changed shape)",
        )
    return match.group(1)


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    """Run a command, echoing it first. Never uses shell=True."""
    print(f"$ {' '.join(str(c) for c in cmd)}")
    return subprocess.run([str(c) for c in cmd], **kwargs)


def tool_version(exe: str) -> str | None:
    """`<exe> --version` first line, or None if the tool is unusable."""
    path = shutil.which(exe)
    if path is None:
        return None
    try:
        out = subprocess.run(
            [path, "--version"], capture_output=True, text=True, timeout=30
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0:
        return None
    return (out.stdout or out.stderr).strip().splitlines()[0]


def find_git_bash() -> Path | None:
    """Locate Git Bash on Windows without mistakenly selecting WSL's bash.exe."""
    git = shutil.which("git")
    if git is not None:
        # C:/Program Files/Git/cmd/git.exe -> C:/Program Files/Git/bin/bash.exe
        candidate = Path(git).resolve().parent.parent / "bin" / "bash.exe"
        if candidate.is_file():
            return candidate
    bash = shutil.which("bash")
    if bash is not None and "system32" not in bash.lower():
        return Path(bash)
    return None


def preflight(pin: str, variant: str) -> None:
    """Verify the workstation before touching anything."""
    print("== Preflight ==")
    print(f"   platform : {platform.platform()}")
    print(f"   python   : {platform.python_version()} ({sys.executable})")

    uv = tool_version("uv")
    if uv is None:
        fail(
            "uv is not on PATH (it is a Spec Kit prerequisite)",
            "install uv: https://docs.astral.sh/uv/getting-started/installation/",
        )
    print(f"   uv       : {uv}")

    git = tool_version("git")
    if git is None:
        fail(
            "git is not on PATH",
            "install Git (on Windows: Git for Windows, which also provides "
            "Git Bash): https://git-scm.com/downloads",
        )
    print(f"   git      : {git}")

    # A specify CLI installed on PATH at a version other than the pin
    # would run the developer's own /speckit workflow on a version other than the pin.
    # Bootstrap itself always invokes the pin via `uv tool run`.
    installed = tool_version("specify")
    if installed is not None:
        found = re.search(r"\d+\.\d+\.\d+", installed)
        if found and f"v{found.group(0)}" != pin:
            fail(
                f"specify on PATH is v{found.group(0)}, but the pinned "
                f"version is {pin} (speckit/PINNED-VERSION)",
                f'uv tool install --force --from "{SPECKIT_GIT}@{pin}" specify-cli',
            )
        print(f"   specify  : {installed} (matches pin {pin})")
    else:
        print(f"   specify  : not installed - using pinned {pin} via uv tool run")

    # Finding LW-1: on stock Windows, `python3` in Git Bash resolves to the
    # WindowsApps Store stub, which EXISTS but fails at RUNTIME — so the
    # probe *executes* the parser rather than locating it. At the pinned
    # version this no longer breaks the scaffold: upstream #3312/#3320
    # (fixing spec-kit#3304, in by v0.12.9) fall through to grep/sed/awk on
    # parse failure, and template resolution degrades to path-convention
    # replace-only — exactly what the all-replace SDD preset needs. A
    # working parser still provides manifest-aware template resolution and
    # robust JSON parsing, so the probe stays as a WARNING, not a gate.
    if variant == "sh" and platform.system() == "Windows":
        bash = find_git_bash()
        if bash is None:
            fail(
                "Git Bash not found (the standard's scaffold variant is "
                "bash, SDD-STANDARD §10.1)",
                "install Git for Windows: https://git-scm.com/downloads",
            )
        print(f"   bash     : {bash}")
        probe = (
            "command -v jq >/dev/null 2>&1"
            " || { command -v python3 >/dev/null 2>&1"
            " && python3 -c 'print(0)' >/dev/null 2>&1; }"
        )
        result = subprocess.run(
            [str(bash), "-c", probe], capture_output=True, timeout=60
        )
        if result.returncode != 0:
            print(
                "   json     : WARNING - no working jq or python3 in Git "
                "Bash (the spec-kit#3304 situation). The scaffold scripts "
                "fall back to text parsing at the pinned version, but a "
                "real parser is recommended:\n"
                "              uv python install --default   (or: install "
                "jq, or disable the python3 App Execution Alias and put a "
                "real Python on PATH)"
            )
        else:
            print("   json     : working jq or python3 available in Git Bash")

    print("preflight OK\n")


def specify(pin: str, args: list[str], cwd: Path | None = None) -> None:
    cmd = ["uv", "tool", "run", "--from", f"{SPECKIT_GIT}@{pin}", "specify"] + args
    result = run(cmd, cwd=cwd)
    if result.returncode != 0:
        fail(
            f"`specify {args[0]}` exited {result.returncode}",
            "read the output above; re-run after fixing the reported cause. "
            "If the failure is inside Spec Kit itself, report it with this "
            "transcript as an issue on the sdd-standard repository",
        )


def seed_constitution(target: Path, profile: str) -> None:
    """Overwrite the init-seeded constitution with the filled-in shared one.

    At the pinned version, `specify init` seeds
    .specify/memory/constitution.md AFTER the preset installs, from the
    preset's own constitution-template (verified in the v0.13.0 source:
    commands/init.py `ensure_constitution_from_template`, upstream #3276) —
    so the file already holds our template text, with its placeholders
    unfilled. This overwrite fills [PROJECT NAME] / [CONVENTION VERSION]
    and appends the stack-profile block, and stays correct even if a
    future version reverts to stock-first seeding. Re-verify at every
    pin-forward.
    """
    template = PRESET_DIR / "templates" / "constitution-template.md"
    memory = target / ".specify" / "memory" / "constitution.md"
    memory.parent.mkdir(parents=True, exist_ok=True)

    text = template.read_text(encoding="utf-8")
    text = text.replace("[PROJECT NAME]", target.resolve().name)
    text = text.replace("[CONVENTION VERSION]", read_convention_version())

    profile_doc = PROFILES_DIR / profile / "profile.md"
    profile_text = profile_doc.read_text(encoding="utf-8")
    version_match = re.search(r"Profile version \|\s*`([^`]+)`", profile_text)
    profile_version = version_match.group(1) if version_match else "unknown"

    profile_block = (
        f"This repo uses the **{profile}** stack profile "
        f"(version `{profile_version}` at bootstrap time). The Design "
        f"Document's contract sections follow its vocabulary and table "
        f"shapes; deviations carry a stated reason. The profile provides "
        f"defaults and vocabulary only — it never adds gates, approval "
        f"steps, or artifact types (SDD-STANDARD §7). Full text: "
        f"`.specify/memory/profile.md` — a verbatim copy of "
        f"`standard/profiles/{profile}/profile.md` at the pinned release, "
        f"installed by bootstrap and drift-checked by "
        f"`ci/check_convention_version.py`; profile changes land upstream "
        f"by PR, never by editing the copy.\n"
    )
    marker = "## Stack profile"
    head, sep, _ = text.partition(marker)
    if sep:
        # keep the heading, replace the placeholder comment below it
        text = head + marker + "\n\n" + profile_block
    else:
        text = text.rstrip() + f"\n\n{marker}\n\n" + profile_block

    memory.write_text(text, encoding="utf-8", newline="\n")
    print(f"constitution seeded: {memory} (Shared principles + {profile})")


def install_profile(target: Path, profile: str) -> None:
    """Copy the chosen profile's full text into the product repo.

    The constitution carries only a pointer (thin context, D-17); the
    profile's defaults can steer an implementing agent only if the full
    text is present in the repo the agent works in. The copy is verbatim —
    `ci/check_convention_version.py` compares it against the standard's
    profile at the pinned release, so edits to it land upstream by PR,
    never locally.
    """
    source = PROFILES_DIR / profile / "profile.md"
    dest = target / ".specify" / "memory" / "profile.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        source.read_text(encoding="utf-8"), encoding="utf-8", newline="\n"
    )
    print(f"profile installed: {dest} "
          f"(copy of standard/profiles/{profile}/profile.md)")


def write_marker(target: Path, profile: str, variant: str, pin: str) -> None:
    marker = target / ".specify" / "sdd.json"
    payload = {
        "convention_version": read_convention_version(),
        "profile": profile,
        "variant": variant,
        "speckit_pin": pin,
        "bootstrapped": datetime.datetime.now(datetime.timezone.utc)
        .replace(microsecond=0)
        .isoformat(),
    }
    marker.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"marker written: {marker}")
    print(json.dumps(payload, indent=2))


def main() -> None:
    # Windows consoles may run a legacy codepage that cannot print the
    # standard's § references; never let an encoding error kill bootstrap.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")

    profiles = sorted(
        p.name
        for p in PROFILES_DIR.iterdir()
        if p.is_dir() and not p.name.startswith("_")
    )

    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("target", help="directory to initialize (created if missing)")
    parser.add_argument(
        "--integration",
        required=True,
        help="the team's AI agent integration, passed to `specify init` "
        "(mandatory: Spec Kit's non-interactive default would silently pick "
        "copilot). Agent choice stays free — use `generic` for none.",
    )
    parser.add_argument(
        "--profile",
        required=True,
        choices=profiles,
        help="stack profile to bind into the constitution",
    )
    parser.add_argument(
        "--script",
        default=STANDARD_VARIANT,
        choices=["sh", "ps"],
        help="scaffold script variant. The standard's variant is `sh` "
        "(SDD-STANDARD §10.1); `ps` exists for the verification matrix only",
    )
    parser.add_argument(
        "--integration-options",
        default=None,
        help="passed through to `specify init --integration-options`",
    )
    parser.add_argument(
        "--ignore-agent-tools",
        action="store_true",
        help="passed through to `specify init` (CI runners have no agent CLIs)",
    )
    args = parser.parse_args()

    if args.script != STANDARD_VARIANT:
        print(
            f"WARNING: --script {args.script} is for the verification matrix "
            f"only; the standard's variant is `{STANDARD_VARIANT}` "
            f"(SDD-STANDARD §10.1)\n"
        )

    for path, name in [
        (PRESET_DIR / "preset.yml", "SDD preset"),
        (EXTENSION_DIR / "extension.yml", "SDD extension"),
    ]:
        if not path.is_file():
            fail(
                f"{name} missing at {path}",
                "your sdd-standard checkout is incomplete or too old - "
                "re-clone it at the pinned release tag",
            )

    pin = read_pin()
    preflight(pin, args.script)

    target = Path(args.target)

    print("== specify init (pinned) ==")
    init_args = [
        "init",
        str(target),
        "--integration",
        args.integration,
        "--script",
        args.script,
        "--preset",
        str(PRESET_DIR.resolve()),
    ]
    if args.integration == "generic" and not args.integration_options:
        # upstream makes --commands-dir mandatory for the generic
        # integration; .agent/commands is the standard's default (agent-neutral)
        args.integration_options = "--commands-dir .agent/commands"
        print(f"note: --integration generic defaults to "
              f'--integration-options "{args.integration_options}"\n')
    if args.integration_options:
        init_args += ["--integration-options", args.integration_options]
    if args.ignore_agent_tools:
        init_args += ["--ignore-agent-tools"]
    specify(pin, init_args)

    # `specify init` downgrades preset failures to warnings - assert it landed
    if not (target / ".specify" / "presets" / "sdd" / "preset.yml").is_file():
        fail(
            "the SDD preset did not install (specify init only warns "
            "on preset failures)",
            "read the `specify init` output above for the preset warning; "
            "fix its cause and re-run bootstrap on a fresh target",
        )

    print("\n== review extension ==")
    specify(
        pin,
        ["extension", "add", str(EXTENSION_DIR.resolve()), "--dev"],
        cwd=target,
    )
    if not (target / ".specify" / "extensions" / "sdd" / "extension.yml").is_file():
        fail(
            "the SDD extension did not install",
            "read the `specify extension add` output above; fix its cause "
            "and re-run bootstrap on a fresh target",
        )

    print("\n== constitution, profile, and marker ==")
    seed_constitution(target, args.profile)
    install_profile(target, args.profile)
    write_marker(target, args.profile, args.script, pin)

    print(
        "\nDone. Next steps:\n"
        f"  1. cd {target}\n"
        "  2. commit the scaffold before anything else\n"
        "  3. wire the spec CI check (docs/adopting-a-repo.md in sdd-standard)\n"
        "  4. first feature: docs/quickstart.md steps through it end to end\n"
        "Reminder: spec before code - the artifacts exist in order before "
        "implementation, and review-phase findings are resolved before done "
        "(SDD-STANDARD §3)."
    )


if __name__ == "__main__":
    main()
