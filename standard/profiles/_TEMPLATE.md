# Profile: <name>

| Field | Value |
| ----- | ----- |
| Profile version | `<semver>` |
| Requires | `SDD-STANDARD >= <X.Y>` |
| Owning team | `<team>` (CODEOWNERS entry required) |
| Outside reviewer | Every change needs ≥ 1 reviewer from outside the owning team (SDD-STANDARD §7.4) |
| Stack family | `<what this profile covers — a family, never a single team>` |

> **Authority banner — do not remove.** Per SDD-STANDARD §7: this profile
> provides **defaults, vocabulary, and worked examples only**. It shall not
> add gates, approval steps, artifact types, or workflow steps, and shall
> not override the standard. If something here appears to conflict with
> SDD-STANDARD.md, the standard wins and this profile gets fixed.

## 1. Scope

<Which repos/stacks this profile applies to, and what it deliberately leaves
open. Keep it one paragraph.>

## 2. Synchronous contract defaults

<How the Design Document's sync-API contract section is written under this
stack: the table shape, required columns, error-code conventions, idempotency
language — and what silence means (the stated-or-default reading: an absent
statement reads as the profile default, never as implementer's choice).
Defaults only — a team may deviate with a stated reason in the
Design Document.>

## 3. Asynchronous contract defaults

<How the Design Document's async-message contract section is written:
subject/topic naming default, where schemas live, how delivery semantics are
stated — and what silence means. Defaults only.>

## 4. Contract vocabulary

<Optional — delete if plain language covers the stack. Terms the contract
sections depend on, each defined in one line, plus the failure cases this
stack family routinely meets. Vocabulary only: names and meanings, never
obligations.>

## 5. Worked examples

<At least one filled-in example per contract section, small enough to read
in a minute.>

## 6. Profile changelog

| Version | Date | Change |
| ------- | ---- | ------ |
| `<semver>` | `<date>` | Initial version |
