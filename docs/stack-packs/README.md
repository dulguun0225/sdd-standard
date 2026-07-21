# Stack packs — seed text for a repo's stack rules

**Informative.** A stack pack is pre-written seed text for the one
place technology rules live: the *Repo principles* section of an
adopting repo's constitution (§2.4). Packs name technologies on
purpose — that is their job. Nothing in a pack binds anyone until a
repo's team lands the text, edited, in its own constitution by PR.
The standard and the profiles stay technology-free
([choosing-a-stack.md](../choosing-a-stack.md) §1); in any conflict,
the standard takes precedence and the pack gets fixed.

## What a pack is, and is not

- A pack is the starting text for the Repo-principles PR that
  [choosing-a-stack.md](../choosing-a-stack.md) §5 shows landing the
  Monday after the stack decision. It saves the writing, not the
  decision.
- A pack presumes the decision already passed the dominant criterion:
  the team can run this stack in production
  ([choosing-a-stack.md](../choosing-a-stack.md) §3). A pack is never
  a reason to adopt a stack the team cannot operate.
- A pack is not a profile. The profile binds how contracts are
  *documented* and deliberately names no technologies; a pack names
  technologies and rules for the *code*. `--profile backend-services`
  serves every pack here unchanged.
- Edit before landing. Delete rules your situation does not need,
  tighten the ones it does. An unedited pack in a constitution is a
  sign nobody read it — the same failure the thin-constitution
  decision (D-17) exists to avoid.

## The review model packs assume

Both packs assume no human reads the generated code line by line.
Agents implement; code volume outruns human reading; the packs treat
that as the normal case, not the extreme one
([choosing-a-stack.md](../choosing-a-stack.md) §3). Two consequences:

- Machine evidence substitutes for code review, so the evidence
  rules are gates, not advice. Weakening one is a stated deviation
  for a repo where a human actually reads the code — that repo is
  the exception and carries the burden of saying so.
- Human review does not disappear; it moves up the stack. The
  standard's four gates are humans reading artifacts and evidence,
  and the Review approver judges behavior against the spec (§3.3).
  That human semantic backstop is why the packs stop at
  deterministic gates and do not import the heavier apparatus a
  fully human-free repo needs.

## How to use one

1. Bootstrap the repo ([adopting-a-repo.md](../adopting-a-repo.md) §6).
2. Open the Repo-principles PR with the pack's seed text, edited.
3. Wire the pack's enforcement the same week: a ban without its
   ArchUnit or Error Prone rule is a wish, not a rule.

## The packs

| Pack | For repos where… | File |
| ---- | ---------------- | ---- |
| Java backend, money-grade | money is moved or accounted — payments, billing, ledgers, lending | [java-backend-money.md](java-backend-money.md) |
| Java backend, general | no field carries money; exactness pressure is ordinary | [java-backend-general.md](java-backend-general.md) |

Both packs share one platform family (Java, Spring Boot MVC, jOOQ,
PostgreSQL). They differ where the domain differs: the money pack
carries the exact-numbers discipline end to end; the general pack
replaces it with a lighter numeric discipline and a tripwire for the
day the first money field appears.

## Freshness

Version facts and tool verdicts in the packs were verified
2026-07-21 (adversarial web research; sources cited in each pack).
Re-verify pins at adoption and at every dependency review — the packs
date their claims so staleness is visible, not silent.
