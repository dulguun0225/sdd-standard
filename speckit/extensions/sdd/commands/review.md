---
description: Run the SDD review phase — compare the implementation against spec/plan/tasks and write the findings to review-notes.md.
---

## User input

```text
$ARGUMENTS
```

Optional: a feature directory (`specs/NNN-slug/`). Without it, operate on the
current feature branch's spec folder.

## Goal

Run the SDD **review phase** (SDD-STANDARD §3.1–3.2). It runs after
implementation completes, before the item is marked done. Compare what
was built against the Requirements Document (`spec.md`), Design Document
(`plan.md`), and Task List (`tasks.md`). Write `review-notes.md` into
the feature's spec folder. Every finding is then resolved one of three
ways (§3.2): fix the implementation, amend the artifact in the same
PR/MR, or record an explicit acceptance with a reason in the notes.

## Hard rules

1. You shall NOT resolve a finding by silently editing `spec.md`,
   `plan.md`, or `tasks.md` to match the code. A deliberate spec change
   is its own visible change in the same PR/MR (SDD-STANDARD §5.2) —
   record the finding first, then amend openly if amending is the right
   resolution.
2. Report what you find, including "no findings" — an empty diff section
   is itself evidence.
3. In this phase you shall not tick tasks, mark the item done, or edit
   the implementation. Findings are resolved after the notes exist, as
   their own visible changes.

## Execution steps

1. **Locate the feature.** Run the repo's check-prerequisites script with
   `--json --include-tasks` to get `FEATURE_DIR` and the available docs.
   The script is `.specify/scripts/bash/check-prerequisites.sh` or its
   PowerShell twin. If the user supplied a feature directory, use that
   instead.

2. **Verify the artifacts exist.** Read `spec.md`, `plan.md`, `tasks.md`
   in `FEATURE_DIR`. All three must exist — the artifact order is
   Requirements → Design → Tasks before implementation (§3.1). If any is
   missing, record which one as a finding, not a failure to continue
   past.

3. **Gather the implementation delta.** Identify the changes implementing
   this feature: the feature branch's diff against its base, or the merged
   PRs/commits referencing the feature. List the files touched.

4. **Check requirement by requirement.** For every R-id in `spec.md`, give
   a verdict: implemented / partial / missing / deviates. Back each verdict
   with concrete evidence (file, behavior, test). EARS phrasing makes each
   requirement one testable behavior — test it or trace it.

5. **Check the contracts.** Compare `plan.md`'s Synchronous contracts and
   Asynchronous contracts tables against the code. Every declared
   operation, error code, event, and delivery semantic must be present and
   matching. Flag anything implemented but undeclared.

   Then check **silence-conformance** against the repo's stack profile
   (`.specify/memory/profile.md`). Under the profile's stated-or-default
   reading rule (profile §1), a silent contract cell is not the
   implementer's choice — the profile default *is* the contract. For every
   dimension the table leaves unstated, verify the code implements the
   default, not a guess:

   - collection operation, no page statement → cursor pagination: opaque
     `cursor` + `limit` (default 50, cap 200), response
     `{items, next_cursor}`;
   - update on a versioned resource, no concurrency statement →
     compare-and-set, stale writes rejected with a stable conflict code;
   - unstated delivery → at-least-once with **durable** de-duplication on
     `event_id` (unique index or dedup table — not process memory);
   - unprocessable message → parked on a dead-letter destination with its
     error, never silently dropped;
   - event produced as the effect of a state change → publish and state
     change atomic, with a named mechanism (e.g. transactional outbox);
   - authenticated-but-not-entitled access → existence-safe response
     (indistinguishable from "does not exist").

   Give each silent dimension a verdict: default honored / default violated
   (name what the code does instead) / not applicable. Separately, flag
   every mutating operation whose Idempotency cell is empty. That cell has
   no safe default (profile §2). Record it as a named open question,
   never as a gap to fill yourself.

6. **Check the tasks.** Every task marked done has its stated evidence;
   every task carries `[R-n]`; incomplete tasks are listed.

7. **Check for spec drift.** Find behavior the delta changed that the
   spec covers, where the same change did not also update the
   spec (§5.2). This is the most important finding class.

8. **Write the notes.** Create or overwrite `FEATURE_DIR/review-notes.md`:

   ```markdown
   # Review notes — <feature>

   Prepared by: <agent> on <date>.
   Every finding below is resolved before the item is marked done
   (SDD-STANDARD §3.2): fix, same-PR amendment, or an explicit
   acceptance with a reason recorded here.

   ## Artifact check
   ## Requirements coverage
   | R-id | Verdict | Evidence |
   ## Contract check
   ### Silence-conformance (profile defaults)
   ### Idempotency cells left empty
   ## Task evidence
   ## Spec-drift findings
   ## Open questions
   ```

9. **Report.** Summarize the verdicts and point at the notes file. Do
   not mark anything done or complete — findings are resolved after this
   phase, as their own visible changes (§3.2).
