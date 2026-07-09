# Requirements — agent-hq-approval-test

**Status: DRAFT**

<!-- Throwaway feature for testing the Agent HQ browser-approval flow.
     Do not merge.

     The drafting agent wrote `Status: DRAFT` above — allowed by §3.2
     (only the APPROVED flip is reserved for a human). A human reviewer
     flips DRAFT -> APPROVED in a browser commit, with no local clone.

     A DRAFT spec alone is valid (green). The sibling plan.md (also DRAFT)
     is what makes CI red until this spec is approved: the design gate
     stays shut until the requirements gate passes. Approving this spec
     opens it. -->

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
  flips the draft to an approval line in a browser commit, the structure
  check shall treat the requirements gate as passed and stop blocking the
  sibling design document.
- **R-2** WHILE this document remains a draft, the structure check shall
  block any sibling `plan.md` — the design gate stays shut until the
  requirements gate passes.

## 3. Success criteria

- `uv run ci/check_spec_structure.py --self` goes from red (plan present,
  spec not approved) to green (spec approved) with only a browser commit in
  between.

## 4. Traceability

`plan.md` in this folder depends on this document being approved first. No
`tasks.md` — the test stops at the design gate.
