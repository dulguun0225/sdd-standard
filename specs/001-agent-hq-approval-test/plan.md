# Design — agent-hq-approval-test

**Status: DRAFT**

<!-- Present only to keep the test's CI signal meaningful. Because this
     design document exists while spec.md is still a draft, the structure
     check reports a gate-order violation (design before approved
     requirements) and CI is red. Approving spec.md clears it. This
     document stays DRAFT throughout — the test stops at the design gate. -->

| Field        | Value                          |
| ------------ | ------------------------------ |
| Feature      | `001-agent-hq-approval-test`   |
| Authored     | 2026-07-09                     |
| Requirements | [spec.md](spec.md)             |

## 1. Summary

Nothing is designed here. This document exists to demonstrate that the
design gate stays shut until the requirements gate passes [R-2].

## 2. Notes

Once a human approves `spec.md` in the browser, the check stops flagging
this file and CI goes green [R-1].
