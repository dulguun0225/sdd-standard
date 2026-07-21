# Stack packs — candidates and boundaries (working notes)

**Informative.** These notes record why future packs would exist and
which candidates are on the table, so the reasoning is not re-derived
each time. Nothing here binds, and nothing here is a commitment to
build. A candidate becomes a pack the way the first two did: its own
verified research pass, dated evidence notes, and confirmed-versus-
convention markers ([README.md](README.md), Freshness).

## 1. When a different pack is warranted

The two existing packs quietly assume four things. A requirement
warrants a *new* pack when it breaks one of the assumptions. Anything
less is an edit to the seed text — which the packs invite — or a
variant of an existing pack.

1. **The platform is right.** Broken by:
   - *Latency as correctness* — "too late is wrong" (trading,
     control, telephony-class deadlines). A GC pause becomes a
     defect; performance gates become gates, not ratchets; the
     platform pin itself is in question.
   - *A runtime you don't control* — mobile, embedded, plugins in
     someone else's process. No production of your own to run
     standing invariants in; rollback is not yours; backward
     compatibility with deployed clients becomes the top rule.
   - Recorded correction (2026-07-21): massive concurrent I/O no
     longer breaks this assumption. Virtual threads carry the packs'
     blocking style to high concurrency on the same servlet stack;
     the reactive ban stands. Details and the pending amendment:
     section 3.
2. **Money is the exactness domain.** Money is one instance of "a
   wrong value has a victim." Other instances need other type
   disciplines, and each is a pack-sized change:
   - *Physical quantities* — units-of-measure discipline: a
     milligram added to a milliliter must not compile.
   - *Legal time* — deadlines, retention, statutes: jurisdiction
     calendars and timezone law, beyond the business-date rule.
   - *Security-critical values* — key material, tokens:
     constant-time comparison, non-loggability as a type property.
   The pattern transfers even where the content does not: one value
   type, arithmetic only through it, raw arithmetic banned outside,
   the ban enforced by an architecture test.
3. **Evidence is deterministic tests.** Broken by:
   - *A stochastic component in the product* — LLM or ML calls.
     Pass/fail becomes statistical: evals, golden transcripts,
     gated model pins. The deepest break: "tests are the code
     review" stops being well-defined.
   - *Untrusted input at the core* — parsers, file ingestion,
     protocol endpoints: fuzzing becomes the primary evidence.
   - *Regulator-prescribed evidence* — the auditor dictates the
     evidence format and toolchain qualification; the evidence
     section stops being the repo's call.
4. **The artifact is a running service.** Broken by:
   - *Batch and data pipelines* — correctness is reconciliation to a
     source of truth and idempotent reruns over historical data;
     schema evolution over years of stored rows replaces API
     compatibility.
   - *Stream processors* — event-time windows, replay-deterministic
     reprocessing.
   - *Libraries and SDKs* — no production to observe; API-
     compatibility gates and semver discipline replace standing
     invariants.

**Not a new pack:** more throughput, more modules, multi-tenancy, a
different broker or cloud, stricter thresholds — those are seed-text
edits or `plan.md` decisions. A persistence preference (JPA over
jOOQ) is a *variant* of the same pack, not a new kind.

**The tripwire marker.** Each break has a "first X" moment — the
first LLM call, the first hard deadline, the first shipped SDK, the
first regulated audit, the first pipeline that must reconcile. The
spec introducing X is the signal that the repo has left the existing
packs' coverage; that PR is the cheap moment to say so, exactly as
the general pack's money tripwire works.

## 2. Candidate roster

Same shape, other languages:

| Candidate | Money-grade viable? | The distinct discipline it would carry |
| --------- | ------------------- | -------------------------------------- |
| dotnet-backend | Yes — strongest candidate | `decimal` is a language primitive, so the money rules simplify. Compile wall: nullable reference types + warnings-as-errors + analyzers. Evidence: Stryker.NET (mature mutation testing). Ban-list flavor: the ORM's silent parts — lazy-loading proxies, change tracking |
| typescript-node-backend | A different shape | Types erase at runtime, so the spine is runtime validation at every boundary, schemas committed as the contract. Honest money is integer minor units — no decimal type exists. Stryker and fast-check are mature. Bans: `any`, implicit coercion, decorator-DI reflection |
| python-backend | Riskier | All discipline is runtime discipline: strict type checking + boundary validation as the compile-wall substitute. `Decimal` is stdlib. Standout: Hypothesis, the strongest property-testing tool of any family here. Weak spot: mutation tooling |
| go-backend | No — general only | Explicitness is native; the ban list is short; exhaustiveness comes from linters, not the compiler. No stdlib decimal and silent zero values, so its money tripwire differs: the first money field triggers a platform decision, not rule adoption. Mutation tooling effectively absent — the pack must say so |
| rust-backend | Yes | The compiler is most of the review: no nulls, exhaustive matching, compile-checked SQL as contracts-in-the-diff. Active mutation tooling. Dated caveat: corpus depth, the capability that matters most when agents implement |

Kotlin: a note on the Java packs (same JVM, same rules, one dated
fact on mutation-tooling maturity), not a pack.

Different kinds:

- **typescript-frontend** (deferred for now) — strict-compiler wall,
  boundary and dead-code gates, browser-level evidence. Its money
  rule completes the money pack's wire promise: the frontend never
  does money arithmetic — amounts stay strings from wire to display,
  formatted, never parsed to float.
- **llm-service** — services containing model calls. Evals as the
  machine evidence, golden transcripts as the characterization-replay
  analogue, prompts committed and diffed like contracts, stated
  determinism handling, cost and latency budgets as numeric contract
  terms, model pins with eval-gated pin-forwards. Assumption 3's
  break, so research must precede drafting.
- **data-pipeline** — committed SQL models as contract files, schema
  and freshness tests, idempotent backfills, and reconciliation:
  aggregate totals tie back to the source ledger exactly; floating
  point never touches a money aggregate.
- **iac** — the plan diff is the contract in the PR, policy checks as
  the ban list, pinned providers, state discipline, drift detection
  as the standing invariant.
- **supply-chain** — cross-cutting; composes with every pack above:
  SHA-pinned CI actions, SBOM and CVE scanning gating on exit codes,
  secrets scanning, provenance attestation.

Suggested draft order: dotnet-backend first (a second type system
tests which money rules are portable and which were Java-shaped),
llm-service second (highest strategic value, least settled ground).
The rest wait for a real repo decision to land on them.

## 3. Recorded finding, pending amendment (2026-07-21)

Virtual threads and the concurrency rules — discussed, not yet
research-verified; verify the version facts before amending the
packs:

- Virtual threads (final since Java 21) carry the blocking style to
  massive concurrent I/O on the servlet stack. They do not violate
  the visible-behavior rule: the scheduler is runtime machinery like
  the GC, not behavioral wiring hidden in program text. The reactive
  ban is strengthened, not challenged.
- Cheap threads remove an accidental safety limit: platform-thread
  scarcity used to throttle concurrency implicitly. Proposed seed
  rule for both packs' Platform section: every concurrency limit is
  explicit and numbered (bounded executors or semaphores) — the
  limit the old platform imposed silently must appear in program
  text. The practical bottleneck moves to the resources behind the
  threads, above all the connection pool.
- Structured concurrency was still a preview API at Java 25 (JEP
  505, fifth preview — re-verify). Production use means
  `--enable-preview`: a stated constitution-level decision, never
  drift. The synchronized-pinning problem was fixed in JDK 24 —
  re-verify alongside.

## 4. Open research questions (carried from the 2026-07-21 run)

- Property-testing replacement: jqwik is a maintenance dead end even
  at the clause-free 1.9.x pin. Evaluate successors before the next
  pack that needs property tests.
- Wire practice beyond the verified pair: Stripe and major
  bank/open-banking APIs (string decimal versus integer minor
  units), and what OpenAPI toolchains do with each.
- Rounding mandates not yet surveyed: US tax (IRS), IFRS/GAAP,
  interest-accrual conventions — a mandate anywhere would force a
  per-operation rounding table in the money pack.
- Precedent: golden-path/paved-road programs that ship opt-in,
  technology-naming defaults beside a technology-free standard, and
  how they keep them informative rather than binding.
