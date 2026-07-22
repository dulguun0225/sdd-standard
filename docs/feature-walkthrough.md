# One feature, end to end — who does what, when

**Informative.** This guide explains and demonstrates; the rules live in
[SDD-STANDARD.md](../standard/SDD-STANDARD.md). In any conflict, the
standard takes precedence.

The [quickstart](quickstart.md) guides *you* through the artifacts,
alone in a scratch repo. This guide replays the same feature the way it
happens in an adopted product repo. Three people, one agent, four pull
requests, about a week. The feature is the teaching example,
[transfer-limit-alerts](../examples/sample-feature/spec.md). Those
files show the finished documents. This guide shows what the files
cannot: the people, the revision, the timing — laid out step by step
in the table below.

## The people

Fictional, like everything about the feature. The standard assigns
none of them a role — it defines no human approval gates (§3.3). It
binds which artifacts exist and in what order (§3.1) and the same-PR
spec-update rule (§5.2); who reads whose work is the team's own
practice, outside the standard's scope (§1). This team's practice:
every PR gets a teammate's read before it merges.

| Who | Team role | In this lifecycle |
| --- | --------- | ----------------- |
| Bilguun | backend developer | drives the agent — the qualification call, the drafting, the implementation, resolving the review findings |
| Nara | product owner of the alerts domain | knows what the behavior must be — refines the spec, reads the spec PRs |
| Tulga | tech lead | reads the design and task PRs; asks the empty-cell questions |
| 🤖 | the coding agent the team wired at bootstrap | drafts artifacts, implements tasks, runs the review phase and writes `review-notes.md` |

The human decisions that remain are judgment, not sign-off: whether
the item qualifies (§6.1), what the behavior must be, and how each
review finding is resolved (§3.2).

## PRs — this team's shape

The standard binds the order by presence: Requirements → Design →
Tasks before implementation, the review phase after it (§3.1). It
deliberately does not bind PR granularity, and it does not require
human PR review (§1). This team opens **one PR per artifact**, all
from the feature branch the scaffold created, merged in sequence, each
read by a teammate — their own habit, not a rule of the standard. A
single long-running feature PR is just as legal. The same caution
applies either way. The merge-blocking structure check (§8.1) goes red
the moment a pushed branch holds an artifact without its predecessor
beside it — a `tasks.md` with no `plan.md`, a feature folder with no
`spec.md`, a task with no `[R-n]` — whatever the PR shape.

## The lifecycle, step by step

One row per phase across the week. The six fields — when, who, what,
where, how, why — are the columns. The people are the three above,
plus the agent (🤖).

| When | Who | What | Where | How | Why |
| ---- | --- | ---- | ----- | --- | --- |
| **Day 1** | **Bilguun** (developer) | Picks up the tracker item — *"Clients discover rejected transfers from support tickets — alert them instead. → `specs/007-transfer-limit-alerts/`"* — and makes the qualification call | The work tracker; the new feature folder | §6.1 judgment — new capability + new API + consumed event (three triggers, and one is enough) → it qualifies, the artifact workflow binds | A bugfix restoring specified behavior would need no ceremony; the call is human judgment, and genuinely unclear cases land in [faq.md](faq.md) so they are asked once |
| **Day 1, afternoon** | **Bilguun** + agent | Draft `spec.md`, then shape it — one testable EARS behavior per R-id (§4.1), the `IF … THEN …` cases the draft missed, the out-of-scope sentence | The feature branch/folder the scaffold created; a PR the team's practice routes to Nara | `/speckit.specify alert clients when a transfer is rejected by their daily limit …`, then human shaping ([writing-requirements.md](writing-requirements.md)) | The draft is raw material. CI is green with one advisory WARNING — R-5 says "quickly", replace it with a number and a unit (advisory, never merge-blocking) |
| **Day 2** | **Nara** (product owner) | Three PR comments — "quickly" is not a number (60 s or 6?); what happens when the same alert is registered twice; does scope cover *changing* limits? The spec goes back for a rewrite before anything downstream is drafted | The same PR — revise and resubmit | Her comments are this team's own review practice, not a gate of the standard (§1). Bilguun + agent revise: R-5 gets "within 60 seconds"; a new R-3 covers the duplicate (`409 ALERT_EXISTS`); §1 gains its out-list. The PR merges once her questions have answers in the text | Revision is normal and cheap — one comment cycle, not a meeting. Catching "quickly" here costs a comment; catching it in the review phase costs a finding; catching it in production costs an incident |
| **Day 3** | **Bilguun** + agent draft; **Tulga** (tech lead) reads the PR | `plan.md` — every element cites `[R-n]` and every R-id is satisfied; two contract tables in the profile shapes; the `contracts/` schema files exist; empty cells assert the profile default; Idempotency on a mutating operation is never empty | The PR touching `plan.md` | `/speckit.plan`, then judgment where the agent cannot be trusted alone ([writing-design.md](writing-design.md)). Tulga checks R-id coverage both ways, asks the empty-cell questions, pushes for D1's rejected alternative | An empty cell is a *statement* (the profile default), not a blank. A human asking about it now is cheaper than the review phase flagging it later — and far cheaper than an outage |
| **Day 4** | **Bilguun** + agent | `tasks.md` — every task carries ≥ 1 `[R-n]`, together covering R-1…R-8; each states its evidence; dependencies are explicit; phases match the plan | The PR touching `tasks.md` | `/speckit.tasks`, then shaping — slicing, evidence lines ([writing-tasks.md](writing-tasks.md)) | The lightest artifact of the three; the plan it traces is only a day old. Implementation may now start (§3.1), and not before — a `tasks.md` pushed with no `plan.md` beside it is a red build on every push (§8.1) |
| **Days 4–6** (Day 5, an unspecified case) | **Bilguun** + agent, task by task | Implement; tick a task only when its stated evidence exists. Day 5: an unsupported `channel` value has no specified behavior → append **R-9** (never renumber) and **T-7**; the spec diff lands in the same PR (§5.2), where Nara reads it — team practice again | The implementation PR — code, tests, the amended spec, the ticked tasks | `/speckit.implement`; §5.2 — the PR that ships the behavior must also update the spec, or it does not merge | That bundle is what "no silent drift" means in practice; T-4's box stays open until the at-least-once replay test delivers exactly once |
| **Day 6** | The agent writes the notes; **Bilguun** resolves the findings | `speckit.sdd.review` writes `review-notes.md` — artifact check, a verdict per R-id with evidence, contract + silence-conformance check, task evidence, drift findings, open questions | The feature folder, inside the implementation PR | The run reports one finding: the plan never states the atomic-publish mechanism the code uses (a transactional outbox — the profile default). Bilguun records an explicit acceptance with a reason in the notes; a finding that needed a code fix would send him back to implementation instead | Every finding is resolved before the item is done (§3.2) — fix, same-PR amendment, or a recorded acceptance. The notes never mark anything done; the resolutions are their own visible changes. The PR merges; the item is done |

## After Done

Done is a dashed edge, not an end point (the
[README's lifecycle diagram](../README.md#the-lifecycle-in-a-product-repo)).
The delivery log starts to show: which channels fail, whether
60 seconds was the right number. What it shows re-enters as the next
work item. [evolving-requirements.md](evolving-requirements.md) covers
that loop.

## Variations

- **Emergency hotfix** (§6.2): production is down; the implementer
  ships the fix immediately, no artifacts first. If it altered behavior
  a spec covers, the spec amendment lands within 5 working days of
  shipping. A missed window is a spec-drift incident (§5.2).
- **Nothing qualifies** (§6.1): an error-message reword, a refactor, a
  bugfix restoring specified behavior. No spec ceremony; the team's own
  lightweight planning. Nobody creates spec folders for these.
- **Too uncertain to spec** (§6.1): spike first — throwaway by intent,
  exempt from ceremony. Then spec what the spike taught you and enter
  the walkthrough at Day 1.

## The qualification call, on harder items

Day 1's call was easy — three triggers matched. The §6.1 list is short.
A change qualifies when it creates or alters externally observable
behavior or a contract, crosses a repo, service, or team boundary,
contains a hard-to-reverse step, or introduces a new capability.
Explicitly exempt, even where a trigger appears to match: bugfixes
restoring already-specified behavior, refactorings and strict internal
improvements, and changes with no externally observable effect. The
same judgment applied to items where the call is less obvious — all on
the alerts service:

| Work item | Call | Why |
| --------- | ---- | --- |
| Reword the `400 VALIDATION_FAILED` error *message* | exempt | The stable code is the contract; the message prose is not something a caller may rely on. Changing the *code* would alter a contract — that qualifies |
| Add an optional `status=` filter to `GET /transfer-limit-alerts` | qualifies | Alters a contract — a compatible addition still changes what callers may rely on, and plan.md §3's row is where they read it |
| Extract the delivery retry loop into its own module, behavior identical | exempt | A refactoring, strictly internal — explicitly exempt |
| Notifications arrive after ~90 s because a retry timer misfires; fix it | exempt | A bugfix restoring already-specified behavior (R-5 says 60 s) — exempt even though delivery timing is externally observable |
| The service crashes on a `channel` value the spec never mentions; fix it | qualifies | There is no specified behavior to restore — the fix *decides* observable behavior, so the spec is amended in the same PR. Day 5 above is this case, caught mid-implementation |
| Split the `alerts.channel` column in two, with a backfill and a dropped column | qualifies | A hard-to-reverse step (data-model change and migration), even with every API unchanged |
| Change the delivery-log line format that the operations team's dashboards parse | qualifies | Crosses a team boundary: a consumer exists, so the format is a contract in practice, declared or not |
| Raise the event consumer's retry budget from 3 to 5 attempts | genuinely unclear | Downstream load and delivery timing shift, but no contract names them. Ask — the answer lands in [faq.md](faq.md), so it is asked once |
