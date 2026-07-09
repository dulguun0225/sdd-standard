# Requirements — agent-hq-approval-test

<!-- Throwaway feature for testing the Agent HQ browser-approval flow.
     Do not merge. This branch demonstrates a reviewer approving the
     spec via a GitHub browser commit, with no local clone.

     This document intentionally carries NO approval line: the agent that
     drafted it must not write one (CLAUDE.md / zero-tolerance rule).
     The human reviewer adds it in their own browser commit.

     NOTE: the body avoids the literal approval-line prefix so the
     structure check does not mistake requirement prose for a real
     approval line. -->

| Field    | Value                                                       |
| -------- | ----------------------------------------------------------- |
| Feature  | `001-agent-hq-approval-test`                                 |
| Authored | 2026-07-09                                                   |
| Input    | Exercise: can a reviewer approve spec.md from the GitHub PR UI, without cloning? |

## 1. Purpose and scope

A scratch feature that exists only to exercise the approval mechanics of
the standard through GitHub's browser editor. Out of scope: any real
behavior — nothing here ships.

## 2. Requirements

- **R-1** WHEN a reviewer opens this document in the GitHub web editor and
  adds an approval line in a browser commit, the structure check shall
  treat the requirements gate as passed.
- **R-2** IF this document carries no approval line, THEN the structure
  check shall report the feature as not approved.

## 3. Success criteria

- `uv run ci/check_spec_structure.py --self` goes from red (no approval
  line) to green (approval line present) with only a browser commit in
  between.

## 4. Traceability

No `tasks.md` in this scratch feature — the test stops at the requirements
gate.
