# Stack pack: Java backend, money-grade

**Informative.** Seed text for the *Repo principles* section of a
repo whose code moves or accounts money — payments, billing, ledgers,
lending, anything where a wrong cent is a defect with a victim. How
packs work, and their authority: [README.md](README.md). The
evidence behind each rule, with dates and honest gaps, is in
[section 3](#3-evidence-notes).

## 1. When this pack applies

Pick this pack when any feature will carry an amount of money as
data the system computes with. The profile already treats a bare
float on a money field as a defect (backend-services profile §2);
this pack carries that promise from the wire into the runtime, the
database, and the toolchain. If no field will carry money, use
[java-backend-general.md](java-backend-general.md) — it is this pack
minus the money discipline, plus the tripwire that brings you back
here.

## 2. The seed text

Copy the block below under *Repo principles*, then edit: delete what
your situation does not need, tighten what it does, and keep the
enforcement column honest — a ban is real only when a named check
fails the build on it.

```markdown
### Platform

- Java <version pinned in the build>, Spring Boot with the servlet
  Web MVC stack. Reactive/WebFlux is banned as a paradigm — one
  concurrency model in the repo.
- Persistence is jOOQ against PostgreSQL. No JPA, no Hibernate, no
  Spring Data: no entity lifecycle, no lazy loading, no query
  derivation. Generated jOOQ classes are committed and diff-gated.
- Schema changes are committed Flyway SQL migrations, applied in
  integration tests against real PostgreSQL.
- JSON is Jackson. DTO fields that carry money are required fields —
  a missing amount fails deserialization, never defaults.

### Money

- One `Money` value type: exact decimal amount plus ISO 4217
  currency, constructed only at the currency's minor-unit scale.
  Excess precision is rejected at construction
  (`RoundingMode.UNNECESSARY`), never silently rounded.
- All arithmetic on amounts goes through `Money`. Raw `BigDecimal`
  arithmetic outside the money package is banned (ArchUnit rule).
  `double`/`float` on money — field, column, or wire — is a defect.
- Cross-currency arithmetic fails loud. There is no implicit
  conversion.
- Rates, factors, and percentages are not `Money`: separate types,
  higher precision, rounded only at the moment they produce a
  payable amount.

### Rounding

- There is no repo-wide default rounding mode. Every rounding names
  its `RoundingMode` at the call site, and the operation's spec
  states the rule with a worked numeric example.
- Splitting a sum uses an allocation that conserves the total
  (largest-remainder or equivalent). Parts are never rounded
  independently.
- Where amounts can be negative, the spec states whether "round up"
  means away from zero (Java `HALF_UP`) or toward positive
  infinity — jurisdiction texts and Java disagree on negatives.

### Storage

- Money columns are `numeric` with explicit precision and scale;
  scale 4 covers every ISO 4217 currency. Never `real`/`double
  precision`, never the PostgreSQL `money` type. The currency lives
  in a column beside the amount.
- Rate and factor columns carry their own, higher precision. They
  are not money columns and do not take the minor-unit scale.

### Wire

- Money on the wire is a string decimal plus an explicit currency; a
  JSON number on a money field is rejected at parse. This is a
  chosen convention — the main alternative is integer minor units —
  and it holds repo-wide, stated in every contract.
- Converting to a counterparty's minor units uses the counterparty's
  published exponent table, never an ISO 4217 assumption — processor
  tables deviate from ISO for specific currencies.

### Time

- `Clock` is injected. Wall-clock reads in domain code
  (`Instant.now()`, `LocalDate.now()`, `new Date()`,
  `System.currentTimeMillis()`) are banned (ArchUnit rule).
- Business dates are their own concept — a `LocalDate` from an
  explicit business-date source, never derived from the wall clock.
  Timestamps are UTC `Instant`, stored as `timestamptz`.

### Null

- JSpecify annotations, checked by NullAway riding Error Prone, as
  compile errors. A nullness violation never reaches review.

### Ban list — runtime-silent behavior

Behavior that never appears in program text is behavior an
implementer guesses at. Banned, each with a named enforcing check:

- Field and setter injection — constructor injection only.
- `@Transactional` — transactions are explicit visible blocks behind
  one seam; SQL outside a transaction is unwritable.
- `@Scheduled`, `@Async` — scheduling and async work go through one
  explicit, named mechanism.
- `@Cacheable` and AOP aspects on domain code.
- Reflection-based dispatch and stringly-typed behavior lookups.
- Every ban names the check that enforces it (ArchUnit on bytecode,
  Error Prone on source). A meta-test keeps the list honest: each
  ban is either enforced by a named test or explicitly marked
  deferred with a reason.

### Evidence toolchain

Tests are the code review: no rule below assumes a human reads the
generated code line by line.

- Integration tests run against real PostgreSQL (Testcontainers),
  applying the real migrations. No in-memory substitute database.
- The ban list is an ArchUnit test class — executable, not prose.
- Mutation testing gates the money packages (pitest ≥ 1.25.8);
  coverage is the floor, mutation score is the ceiling. The
  threshold is this repo's call, stated here.
- Money math carries property tests: construction rejects excess
  precision, allocation conserves the total, rounding stays within
  one minor unit. Property-testing library: see the jqwik caveat in
  the pack's evidence notes before pinning.
- Every change to money math carries a worked numeric example in its
  spec and a golden test reproducing it.
- Contract conformance is fuzzed, not assumed: a generator
  (Schemathesis-class) attacks the running app — booted with
  Testcontainers — from its committed API description. The same
  model writes the spec and the implementation from one mental
  model; only an outside generator probes where they diverge.
- Money paths carry a characterization replay: a committed corpus
  of realistic inputs is recomputed end to end and the full output
  compared byte-for-byte against committed, approved output files.
  Any unapproved diff fails the build — every numeric change
  becomes a git-visible re-approval. Precondition, asserted in CI:
  generation is deterministic (injected clock, pinned locale,
  stable ordering) — regenerate twice, require byte-identical.
- The domain's standing invariants (the trial-balance-equals-zero
  class) run in production on a schedule; a breach — or a stale
  run — alerts. Tests gate what CI runs; invariants catch what only
  real data does.
```

## 3. Evidence notes

Each verdict below survived adversarial verification (three
independent votes per claim) on 2026-07-21, except where marked
**convention** — those rules are defensible practice the research
did not (or could not) confirm from independent sources. Dates make
staleness visible; re-verify at adoption.

- **Hand-rolled `Money` over a library — confirmed reasonable.**
  Joda-Money is maintained (v2.0.3, 2025-12-14) but deliberately
  ships no monetary algorithms — allocation and rounding policy stay
  hand-written either way. Moneta (JSR 354) self-describes as
  maintenance-mode, latest 1.4.5 (2025-03-22), Java 8 baseline.
  Sources: the JodaOrg/joda-money and JavaMoney/jsr354-ri
  repositories.
- **No universal banker's-rounding mandate — confirmed for the
  surveyed regimes.** EU euro-conversion law (Reg. 1103/97 Art. 5)
  mandates round-half-*up* at ties and minor-unit rounding only for
  amounts "to be paid or accounted for"; EU VAT law prescribes
  neither method nor level (ECJ C-302/07); HMRC's penny rule is
  arithmetic half-up with alternatives allowed (VATREC12030). That
  is the argument for per-operation explicit rounding rather than a
  repo default. Gap: no US-tax, IFRS/GAAP, or interest-accrual
  source survived verification — the per-operation rule is also the
  hedge against what those may require.
- **Scale 4 covers ISO 4217 — confirmed.** Minor-unit exponents run
  0 (JPY) to 3 (BHD-class); ISO 4217's maximum is 4 (CLF only).
  Caveat, also confirmed: processor exponent tables deviate from ISO
  (Adyen for CLP, IDR, ISK, CVE; PayPal for HUF) — hence the
  counterparty-table rule. No evidence survived on `numeric(20,4)`
  versus `numeric(19,4)` versus bigint minor units; the precision
  digits are the repo's call.
- **String-decimal wire format — a convention, not the industry
  standard.** Confirmed split: PayPal Orders v2 sends major-unit
  decimal strings; Adyen requires integer minor units. The pack
  keeps string-decimal because the profile's contract tables already
  document money that way; the rule is stated as chosen, with the
  alternative named. Stripe and bank-API practice did not survive
  verification — do not cite them.
- **pitest ≥ 1.25.8 — confirmed.** pitest supports bytecode through
  Java 26 and is actively maintained; a real Java 25 defect in the
  `BigDecimal`/`BigInteger` mutators — the mutators money code
  exercises — was fixed in 1.25.8 (2026-07-20).
- **jqwik caveat — confirmed.** From 1.10, jqwik emits an anti-AI
  clause into logs (1.10.0 shipped it as a hidden prompt injection
  and was removed from Maven Central; 1.10.1 made it overt). The
  project is single-author, in maintenance mode, and 1.10.1 is
  described by its maintainer as probably the last release on JUnit
  Platform 1.x. 1.9.3 (2026-06-07) is clause-free. If you pin
  jqwik: ≤ 1.9.x, with a version-ceiling check in CI, and treat the
  library as re-decidable at every dependency review.
- **JSpecify + NullAway — confirmed mainstream.** Spring Boot 4 /
  Framework 7 (GA 2025-11) ship JSpecify-annotated null-safe APIs
  across ~20 portfolio projects and deprecate Spring's own
  nullability annotations; Spring's build checks with NullAway.
- **Convention (no surviving external evidence):** the ban list's
  defect-source claim, the allocation/largest-remainder rule, the
  Testcontainers-over-in-memory rule, injected `Clock` and the
  business-date split, and the worked-example-plus-golden-test rule.
  Each is stated because it is enforceable and cheap to keep; none
  currently carries a citation.
- **Convention — the three semantic gates.** Contract-conformance
  fuzzing, characterization replay with its reproducible-generation
  precondition, and production invariants are the working practice
  of an AI-only reference implementation, not cited findings. They
  are in the seed because the standard defines no human approval
  gates (D-19): its review phase is automated (§3.2), and a model
  reviewing model output shares its blind spots. These gates are
  the deterministic outside checks for plausible-but-wrong
  output — the failure class no human catches by default anymore.
  They are also the expensive part of this pack — corpus
  maintenance, determinism preconditions, a production job — priced
  for repos where money moves.
