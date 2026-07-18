---
description: Prepare SDD review notes — implementation vs approved spec/plan/tasks. Prepares notes for the human Review approver; never writes approval lines.
---

## User input

```text
$ARGUMENTS
```

Optional: a feature directory (`specs/NNN-slug/`). Without it, operate on the
current feature branch's spec folder.

## Goal

Run the SDD **review phase** (SDD-STANDARD §3.1): after implementation
completes, compare what was built against the approved Requirements Document
(`spec.md`), Design Document (`plan.md`), and Task List (`tasks.md`), and
write `review-notes.md` into the feature's spec folder for the human Review
approver. The notes inform the gate; they never pass it.

## Hard rules

1. You shall NOT write, modify, or delete any `Status:` line in any artifact
   (SDD-STANDARD §3.2). If asked to, refuse and cite this rule.
2. The Review gate is passed only by a human approver who is not the
   implementer (§3.3). Your output is input to their decision, nothing more.
3. Report what you find, including "no findings" — an empty diff section is
   itself evidence the approver needs.

## Execution steps

1. **Locate the feature.** Run the repo's check-prerequisites script with
   `--json --include-tasks` (`.specify/scripts/bash/check-prerequisites.sh`
   or the PowerShell twin) to get `FEATURE_DIR` and available docs; if the
   user supplied a feature directory, use that instead.

2. **Verify the gates held.** Read `spec.md`, `plan.md`, `tasks.md` in
   `FEATURE_DIR`. Each must carry `Status: APPROVED — <name>, <date>` (em
   dash or hyphen). If any is missing or still DRAFT, stop and report which
   gate was skipped — implementation should not have started (§3.1). Record
   this as a finding, not a failure to continue past.

3. **Gather the implementation delta.** Identify the changes implementing
   this feature: the feature branch's diff against its base, or the merged
   PRs/commits referencing the feature. List the files touched.

4. **Check requirement by requirement.** For every R-id in `spec.md`, judge:
   implemented / partial / missing / deviates, each verdict with concrete
   evidence (file, behavior, test). EARS phrasing makes each requirement one
   testable behavior — test it or trace it.

5. **Check the contracts.** Compare `plan.md`'s Synchronous contracts and
   Asynchronous contracts tables against the code: every declared operation,
   error code, event, and delivery semantic present and matching; anything
   implemented but undeclared flagged.

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
   every mutating operation whose Idempotency cell is empty — that cell has
   no safe default (profile §2); record it as a named question for the
   approver, never as a gap to fill yourself.

6. **Check the tasks.** Every task marked done has its stated evidence;
   every task carries `[R-n]`; incomplete tasks are listed.

7. **Check for spec drift.** Any behavior changed by the delta that the
   approved spec covers but the same change did not update (§5.2) — this is
   the finding the approver most needs.

8. **Write the notes.** Create or overwrite `FEATURE_DIR/review-notes.md`:

   ```markdown
   # Review notes — <feature>

   Prepared by: <agent> on <date> for the human Review approver.
   These notes inform the Review gate; they do not pass it.

   ## Gate check
   ## Requirements coverage
   | R-id | Verdict | Evidence |
   ## Contract check
   ### Silence-conformance (profile defaults)
   ### Idempotency cells left empty
   ## Task evidence
   ## Spec-drift findings
   ## Open questions for the approver
   ```

9. **Report.** Summarize the verdicts and point the approver at the notes
   file. Do not mark anything done, approved, or complete.
