# Stack pack: Java backend, general

**Informative.** Seed text for the *Repo principles* section of a
backend repo where no field carries money. How packs work, and
their authority: [README.md](README.md). This pack is the
money-grade pack minus the money discipline, plus a lighter numeric
discipline and a tripwire for the day the first money field
appears. Evidence: [section 3](#3-evidence-notes).

## 1. When this pack applies

Pick this pack when the repo's domain has no amounts that move or
account money — internal tools, catalogs, content services,
telemetry, scheduling. The weights change
([choosing-a-stack.md](../choosing-a-stack.md) §3): exactness stops
being non-negotiable. The review model does not change — no human
reads the generated code here either, so the machine-evidence rules
stay at full strength. What relaxes is only the money-stakes layer;
what stays is everything that was never about money — visible
behavior, null safety, real-database evidence, deterministic time.

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
- JSON is Jackson.

### Numbers

- Counts and identifiers are integer types. A quantity a user sees,
  or that must sum to an externally checked total, is an integer or
  an exact decimal — never `double`.
- `double` is acceptable for measurements, metrics, statistics, and
  scores: values already carrying measurement noise, where nothing
  reconciles to an exact total.
- Floating-point values are never compared for equality; comparisons
  state a tolerance.
- Durations and instants are `Duration` and `Instant`, not numeric
  seconds or millis in domain code — units live in types.
- Tripwire: the first money field re-classes the repo. A feature
  that introduces an amount which moves or accounts money adopts the
  money-grade pack's Money, rounding, storage, and wire rules in the
  same PR. The profile already treats a bare float on a money field
  as a defect; the cheap moment to adopt the rest is the first field,
  not the tenth.

### Time

- `Clock` is injected. Wall-clock reads in domain code
  (`Instant.now()`, `LocalDate.now()`, `new Date()`,
  `System.currentTimeMillis()`) are banned (ArchUnit rule).
- Timestamps are UTC `Instant`, stored as `timestamptz`; calendar
  dates are `LocalDate`. If the domain has a business day, it comes
  from an explicit source, never the wall clock.

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
- Mutation testing gates the packages that carry the domain's
  invariants (pitest ≥ 1.25.8) — the agent writes both the code and
  the tests, so something must test the tests. The threshold is
  this repo's call, stated here. Relaxing the gate to advisory is a
  stated deviation for a repo where a human actually reads the code.
- Property tests are recommended on pure domain logic.
  Property-testing library: see the jqwik caveat in the pack's
  evidence notes before pinning.
- Contract-conformance fuzzing is recommended: a generator
  (Schemathesis-class) attacks the running app from its committed
  API description. The same model writes the spec and the
  implementation from one mental model; only an outside generator
  probes where they diverge.
```

## 3. Evidence notes

Shared rules carry the money pack's evidence
([java-backend-money.md](java-backend-money.md) §3, verified
2026-07-21): JSpecify + NullAway confirmed mainstream (Spring Boot 4
deprecates Spring's own nullability annotations); pitest confirmed
active with Java 26 bytecode support and the 1.25.8 fix; the jqwik
anti-AI clause and maintenance-mode status confirmed — if you pin
jqwik, ≤ 1.9.x with a version-ceiling check.

Specific to this pack, stated honestly: **the Numbers section is
convention.** No independent evidence survived verification on
when `double` is acceptable outside money, on float-comparison
defect rates, or on decimal needs in non-financial backends. The
rules are kept because they are cheap, enforceable, and fail toward
safety; treat them as this pack's starting defaults, not cited
findings. The ban list, Testcontainers rule, injected-`Clock` rule,
and the contract-conformance-fuzzing recommendation are likewise
convention, shared with the money pack.
