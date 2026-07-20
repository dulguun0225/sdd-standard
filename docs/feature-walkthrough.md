# One feature, end to end — who does what, when

**Informative.** This guide explains and demonstrates; the rules live in
[SDD-STANDARD.md](../standard/SDD-STANDARD.md). In any conflict, the
standard takes precedence.

The [quickstart](quickstart.md) guides *you* through the artifacts,
alone in a scratch repo. This guide replays the same feature the way it
happens in an adopted product repo. Four people, one agent, four pull
requests, about a week. The feature is the teaching example,
[transfer-limit-alerts](../examples/sample-feature/spec.md). Those
files show the finished documents. This guide shows what the files
cannot: the people, the rejection, the timing — laid out step by step
in the table below.

## The people

Fictional, like everything about the feature. The gate roles (§3.3)
were bound to named people at adoption and recorded in the team's
README. That binding is step 5 of
[adopting-a-repo.md](adopting-a-repo.md).

| Who | Team role | In this lifecycle |
| --- | --------- | ----------------- |
| Nara | product owner of the alerts domain | **Requirements approver** |
| Tulga | tech lead | **Design approver** and **Tasks approver** (§3.3 allows one person both) |
| Bilguun | backend developer | the **implementer** — drives the agent, holds no gate |
| Sarnai | senior engineer | **Review approver** — never the implementer (§3.3) |
| 🤖 | the coding agent the team wired at bootstrap | drafts artifacts, implements tasks, prepares review notes — approves nothing, ever (§3.2) |

One person may hold several roles. Two rules never bend. Every gate is
passed by a human, in a change that human authors (§3.2). And the
Review approver is never the implementer of the item under review
(§3.3).

## Gates and PRs — this team's shape

The standard binds the order: Requirements → Design → Tasks before
implementation, Review after it (§3.1). It binds the approval mechanics
(§3.2). It deliberately does not bind PR granularity. This team opens
**one PR per artifact**, all from the feature branch the scaffold
created, merged in sequence. Each gate is passed inside its PR, before
merge. A single long-running feature PR is just as legal. The same
caution applies either way. The merge-blocking structure check (§8.1)
goes red the moment a pushed branch holds an artifact whose
predecessor is not approved yet. A `plan.md` next to a `spec.md` still in DRAFT is a
violation, whatever the PR shape.

## The lifecycle, step by step

One row per phase across the week. The six fields — when, who, what,
where, how, why — are the columns. The people are the four above, plus
the agent (🤖).

| When | Who | What | Where | How | Why |
| ---- | --- | ---- | ----- | --- | --- |
| **Day 1** | **Bilguun** (developer) | Picks up the tracker item — *"Clients discover rejected transfers from support tickets — alert them instead. → `specs/007-transfer-limit-alerts/`"* — and makes the qualification call | The work tracker; the new feature folder | §6.1 judgment — new capability + new API + consumed event (three triggers, and one is enough) → it qualifies, the gated workflow binds | A bugfix restoring specified behavior would need no ceremony; the call is human judgment, and genuinely unclear cases land in [faq.md](faq.md) so they are asked once |
| **Day 1, afternoon** | **Bilguun** + agent | Draft `spec.md`, then shape it — one testable EARS behavior per R-id (§4.1), the `IF … THEN …` cases the draft missed, the out-of-scope sentence. `Status: DRAFT` stays as scaffolded | The feature branch/folder the scaffold created; a PR requesting Nara's review | `/speckit.specify alert clients when a transfer is rejected by their daily limit …`, then human shaping ([writing-requirements.md](writing-requirements.md)) | The draft is raw material. CI is green (DRAFT is allowed) with one advisory finding — R-5 says "quickly", replace it with a number and a unit (never merge-blocking) |
| **Day 2** | **Nara** (Requirements approver) | Three comments — "quickly" is not a number (60 s or 6?); what happens when the same alert is registered twice; does scope cover *changing* limits? She leaves the Status line alone | The same PR — revise and resubmit | Comments, no flip (§3.4). Bilguun + agent revise: R-5 gets "within 60 seconds"; a new R-3 covers the duplicate (`409 ALERT_EXISTS`); §1 gains its out-list | Rejection is normal and cheap — one review cycle, not a meeting |
| **Day 3, morning** | **Nara** | Passes the Requirements gate: `Status: APPROVED — Nara (PO), <date>`. The PR merges | Inside the PR, in her own change (a suggestion she writes or a commit she pushes) | Re-reads the diff, then flips the Status line (§3.2; em dash or plain hyphen both count). Bilguun never writes it; the agent is hard-forbidden from it | Nothing downstream is drafted yet — a `plan.md` pushed next to a DRAFT spec is a red build on every push (§8.1) |
| **Day 3** | **Bilguun** + agent draft; **Tulga** (tech lead) holds the gate | `plan.md` — every element cites `[R-n]` and every R-id is satisfied; two contract tables in the profile shapes; the `contracts/` schema files exist; empty cells assert the profile default; Idempotency on a mutating operation is never empty | The PR touching `plan.md` | `/speckit.plan`, then judgment where the agent cannot be trusted alone ([writing-design.md](writing-design.md)). Tulga checks R-id coverage both ways, asks the empty-cell questions, pushes for D1's rejected alternative, then approves: `Status: APPROVED — Tulga (tech lead), <date>` | An empty cell is a *statement* (the profile default), not a blank; the design gate is where the reviewer asks about them — cheaper now than during an outage |
| **Day 4** | **Bilguun** + agent draft; **Tulga** holds this gate too (§3.3) | `tasks.md` — every task carries ≥ 1 `[R-n]`, together covering R-1…R-8; each states its evidence; dependencies are explicit; phases match the plan | The PR touching `tasks.md` | `/speckit.tasks`, then shaping — slicing, evidence lines ([writing-tasks.md](writing-tasks.md)). Tulga approves in his own change | The fastest gate of the four; the plan it traces is only a day old. Implementation may now start (§3.1), and not before |
| **Days 4–6** (Day 5, an unspecified case) | **Bilguun** + agent, task by task | Implement; tick a task only when its evidence exists. Day 5: an unsupported `channel` value has no specified behavior → append **R-9** (never renumber) and **T-7**; the spec diff goes back to **Nara**, re-approved as a diff inside this PR | The implementation PR — code, tests, the amended spec, the ticked tasks, Nara's re-approval commit | `/speckit.implement`; §5.2 — the PR that ships the behavior must also update the spec, or it does not merge | That bundle is what "no silent drift" means in practice; T-4's box stays open until the at-least-once replay test delivers exactly once |
| **Day 6** | The agent writes the notes; **Sarnai** (never the implementer, §3.3) holds the gate | `speckit.sdd.review` writes `review-notes.md` (gate check, a verdict per R-id with evidence, contract + silence-conformance check, task evidence, drift findings). Sarnai spot-checks two verdicts, the drift section, and the done tasks' evidence | The feature folder; this team puts the Review Status line at the top of `review-notes.md` | `Status: APPROVED — Sarnai (reviewer), <date>`; she approves the PR; it merges | The notes inform the gate; they never pass it (the extension never touches a Status line). The item is done |

## After Done

Done is a dashed edge, not an end point (the
[README's lifecycle diagram](../README.md#the-lifecycle-in-a-product-repo)).
The delivery log starts to show: which channels fail, whether
60 seconds was the right number. What it shows re-enters as the next
work item. [evolving-requirements.md](evolving-requirements.md) covers
that loop.

## Variations

- **Emergency hotfix** (§6.2): production is down; the implementer
  ships the fix immediately, no gate first. If it altered behavior an
  approved spec covers, the spec amendment lands within 5 working days
  of shipping, approved the normal way. A missed window is a spec-drift
  incident (§5.2).
- **Nothing qualifies** (§6.1): an error-message reword, a refactor, a
  bugfix restoring specified behavior. No spec ceremony; the team's own
  lightweight planning. Nobody creates spec folders for these.
- **Too uncertain to spec** (§6.1): spike first — throwaway by intent,
  exempt from ceremony. Then spec what the spike taught you and enter
  the walkthrough at Day 1.
