# One feature, end to end — who does what, when

**Informative.** This guide explains and demonstrates; the rules live in
[SDD-STANDARD.md](../standard/SDD-STANDARD.md). In any conflict, the
standard wins.

The [quickstart](quickstart.md) walks *you* through the artifacts,
alone in a scratch repo. This guide replays the same feature the way it
happens in an adopted product repo. Four people, one agent, four pull
requests, about a week. The feature is the teaching example,
[transfer-limit-alerts](../examples/sample-feature/spec.md). Those
files show the finished documents. This guide shows what the files
cannot: the people, the rejection, the clock. In a hurry? Read
[the one-page version](#the-one-page-version) at the end.

## The cast

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
caution applies either way: the merge-blocking structure check (§8.1)
goes red the moment an artifact outruns its predecessor's gate on a
pushed branch. A `plan.md` next to a `spec.md` still in DRAFT is a
violation, whatever the PR shape.

## Day 1 — the work item, and the qualification call

The tracker item reads, in full:

> Clients discover bounced transfers from support tickets — alert them
> instead. → `specs/007-transfer-limit-alerts/`

A summary and a link, nothing more. The acceptance criteria will live
in the spec and nowhere else (§4.3).

**Bilguun** picks it up. Before anything else, he makes the
qualification call (§6.1). This item creates a new capability, a new
API, and a consumed event — three triggers, and one is enough. It
qualifies; the gated workflow binds. Compare: "make the limit check
reject at the boundary, as already spec'd" is a bugfix restoring
specified behavior. No ceremony, whatever its size. The call is human
judgment. When it is genuinely unclear, ask — the answer lands in
[faq.md](faq.md) so it is asked once.

## Day 1, afternoon — drafting the Requirements Document

**Who:** Bilguun and the agent. **How:**

```
/speckit.specify alert clients when a transfer bounces off their daily limit, so they can raise it before the payroll run fails
```

The agent scaffolds the feature branch and folder, then drafts
`spec.md` (what runs underneath: quickstart §2). The draft is a draft.
Bilguun shapes it: one testable EARS behavior per R-id (§4.1), the
unwanted-behavior `IF … THEN …` cases the draft missed, the
out-of-scope sentence. The shaping moves, demonstrated on this very
draft, are [writing-requirements.md](writing-requirements.md).
`Status: DRAFT` stays exactly as scaffolded. He opens the PR and
requests Nara's review.

**What CI says:** green — DRAFT is allowed. Plus one advisory line the
humans will use tomorrow:

```
WARNING: spec.md: R-5 says "quickly" - replace it with a number and a
unit; advisory for the Requirements approver, never merge-blocking
```

## Day 2 — rejection, the normal kind

**Nara** reads the rendered document against her gate checklist
([reviewing-specs.md](reviewing-specs.md)). Three comments. R-5's
"quickly" is not a number — 60 seconds or 6? What happens when the same
alert is registered twice? And scope does not say whether *changing*
limits is in. She **leaves the Status line alone**. That is what
rejection looks like (§3.4): comments, no flip, revise and resubmit. It
costs one review cycle, not a meeting.

Bilguun and the agent revise in the same PR. R-5 gets "within
60 seconds". A new R-3 covers the duplicate (`409 ALERT_EXISTS`). §1
gains its out-list.

## Day 3, morning — the Requirements gate

**Nara** re-reads the diff and passes the gate **in her own change** —
a suggestion she authors, or a commit she pushes herself. She replaces
the line with `Status: APPROVED — Nara (PO), <date>` (§3.2; em dash or
plain hyphen both count). Bilguun never writes that line. The agent is
hard-forbidden from it. The PR merges. The finished document is
[the example's spec.md](../examples/sample-feature/spec.md).

**When matters here:** nothing downstream has been drafted yet. That
is not discipline; the pipeline enforces it. A `plan.md` pushed now,
next to a DRAFT spec, is a red build on every push (§8.1).

## Day 3 — the Design Document

**Who:** Bilguun and the agent draft; **Tulga** holds the gate.
**How:** `/speckit.plan`, then judgment where the agent cannot be
trusted alone:

- every design element cites the requirement it satisfies as `[R-n]`,
  and every R-id is somewhere satisfied;
- the two contract tables follow the repo's stack profile shapes
  ([the example's plan.md](../examples/sample-feature/plan.md) §3–4
  shows both);
- the schema files under `contracts/` actually exist — the structure
  check verifies every local `contracts/…` path the plan references;
- under the profile's stated-or-default rule, an empty cell is a
  *statement*, not a blank. Leaving Delivery empty says "profile
  default" (at-least-once with durable dedup), not "TBD". One cell is
  never left empty: Idempotency on a mutating operation. It has no
  safe default (profile §2).

The full authoring pass, demonstrated on this feature's contract rows,
is [writing-design.md](writing-design.md).

**Tulga** walks the R-id list in both directions — two minutes. He asks
the empty-cell questions now, not in an incident review. One push on
rationale: decision D1 says *what*, so he asks for the rejected
alternative before approving. Then his own change:
`Status: APPROVED — Tulga (tech lead), <date>`. Merge.

## Day 4 — the Task List

**Who:** the same pair drafts with `/speckit.tasks` (the authoring
pass — slicing, evidence lines — is
[writing-tasks.md](writing-tasks.md)). **Tulga** holds this gate too,
wearing the other hat (§3.3 allows it). He checks three things. Every
task carries at least one `[R-n]`, and together the tasks cover all of
R-1…R-8 — an uncovered requirement is an unbuilt requirement. Every
task states its **evidence**: what will exist when it is truthfully
done. Dependencies are explicit, and phases match the plan's phase
plan. He approves in his own change. This is the fastest gate of the
four; the plan it traces is only a day old.

Implementation may now start (§3.1) — and not before. A `tasks.md`
pushed next to an unapproved plan is another red build.

## Days 4–6 — implementation

**Who:** Bilguun and the agent, task by task, with
`/speckit.implement`. A task is ticked only when its stated evidence
exists. T-4's box stays open until the at-least-once replay test
actually delivers exactly once — not when the code "looks done".

**Day 5, reality arrives.** The create-alert endpoint accepts a
`channel` value. Nothing in the approved spec says what happens when it
is one the notification service does not offer. That is new externally
observable behavior, so §5.2 applies: the PR that ships the behavior
updates the spec, same PR, or it does not merge. Bilguun appends
**R-9** — never renumber, never reuse (§4.2). The agent updates code
and tests. The spec diff goes back before **Nara**, who re-approves it
as a diff inside this PR. Minutes, not a ceremony —
[evolving-requirements.md](evolving-requirements.md) is the long form
of this move. *(The example's frozen snapshot ends at R-8; the R-9 turn
here is the story continuing past it.)*

The implementation PR now carries code, tests, the amended spec, the
ticked tasks, and Nara's re-approval commit. That bundle is what "no
silent drift" means in practice.

## Day 6 — the review phase, then the Review gate

**First the agent.** When implementation completes, the review
extension runs (`speckit.sdd.review`, hooked after implement; it also
runs on demand). It writes `review-notes.md` into the feature folder: a
gate check, a verdict per R-id with evidence, the contract check, task
evidence, and spec-drift findings. The contract check includes
silence-conformance: for every dimension the tables left unstated, did
the code implement the profile default — or a guess? The notes
**inform** the gate. They cannot pass it; the extension's first hard
rule is that it never touches a Status line.

**Then Sarnai**, who wrote none of this code. She spot-checks rather
than re-reviews: two R-id verdicts traced into code and tests; the
drift section (empty for the right reason — R-9 went *through* the
spec, not around it); the done tasks' evidence links. Then she passes
the Review gate the same human-only way. The standard fixes the who
(not the implementer) and the how (a Status line in her own change,
§3.2). Which file carries the Review gate's line is the team's working
agreement. This team puts it at the top of `review-notes.md`:
`Status: APPROVED — Sarnai (reviewer), <date>`. She approves the PR. It
merges. The item is done.

## After Done

Done is a dashed edge, not a wall (the
[README's lifecycle diagram](../README.md#the-lifecycle-in-a-product-repo)).
The delivery log starts teaching: which channels fail, whether
60 seconds was the right number. What it teaches re-enters as the next
work item. [evolving-requirements.md](evolving-requirements.md) walks
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

## The one-page version

| When | Who | Does what | How | Rule |
| ---- | --- | --------- | --- | ---- |
| Item picked up | the developer | qualification call — do any §6.1 triggers match? | judgment, noted on the ticket; tracker carries summary + link only | §6.1, §4.3 |
| Before anything else | developer + agent | draft `spec.md`: EARS, stable R-ids, unwanted-behavior cases, out-of-scope | `/speckit.specify`, then human shaping; Status stays DRAFT | §4.1–4.3 |
| Requirements gate | product authority | approve — or reject with comments, Status untouched | own commit or suggestion flips Status to APPROVED | §3.2–3.4 |
| After that gate | developer + agent | draft `plan.md`: contracts in profile shapes, every element cites `[R-n]` | `/speckit.plan`; silent cells assert profile defaults; always fill Idempotency | §7 + profile |
| Design gate | technical authority | walk R-id coverage both ways, ask the empty-cell questions, approve | own change | §3.2–3.3 |
| After that gate | developer + agent | draft `tasks.md`: every task ≥ 1 `[R-n]`, evidence stated | `/speckit.tasks` | §5.1 |
| Tasks gate | technical authority (may be the same person) | check coverage and evidence, approve | own change | §3.2–3.3 |
| After that gate | developer + agent | implement; tick a task only when its evidence exists | `/speckit.implement`, task by task | §3.1 |
| The moment a change alters spec-covered behavior | developer, then the artifact's approver | amend the spec **in the same PR**; re-approve as a diff | append / supersede in place / mark WITHDRAWN — never renumber | §5.2, §4.2 |
| Implementation complete | 🤖 | write `review-notes.md`: verdicts, silence-conformance, drift findings | `speckit.sdd.review` (auto after implement) — informs, never passes | §3.1 |
| Review gate | a reviewer who is not the implementer | spot-check the notes, pass the gate, approve the PR | own change; the notes' file location per team agreement | §3.2–3.3 |
| Production emergency, any moment | the implementer | ship first; spec updated within 5 working days if covered behavior changed | normal amendment + approval, on a deadline | §6.2 |
