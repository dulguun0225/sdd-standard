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
     section 4.
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
   the ban enforced by an architecture test. A 2026-07-22 research
   pass recorded each domain's predicate, toolchain, and traps, and
   set aside a one-body always-on model (section 3).
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

## 3. The other exactness domains (2026-07-22 research pass)

Assumption 2 names three exactness domains beside money — physical
quantities, legal time, security-critical values. A verified research
pass on 2026-07-22 asked whether all four should become one always-on
body of rules: value-property-triggered disciplines in a single Java
pack, each binding wherever a value has the property and silent
otherwise. The model was set aside; these three stay candidates here,
for an adopting repo to pick up. Why:

- Only money survived as a verified, gate-ready discipline. The other
  three came back convention-strength — defensible practice, not
  independently confirmed rules.
- Their enforcement is bespoke or partial (below), so "always on"
  would read as turnkey when it is not.
- No repo drives them; only money has one. That is assumption 2's own
  rule.
- One pack carrying four always-on families is the bloated seed text
  D-17 exists to prevent.

If a repo does pick one up, the shape that fits is
value-property-triggered: define the property once as an open
enumeration, then bind each rule as "where a value is X, … ; silent
otherwise." Name it *value*-property-triggered to keep it distinct
from D-16, whose triggers are properties of a change, not of a value.
The wire half of each domain is technology-free and could sit in the
profile as a silence-default, the way the money wire rule already
does — a separate, optional question, not pursued here.

Markers below are the 2026-07-22 pass's verdicts (three refutation
votes per claim, the packs' bar): confirmed, convention, or uncertain.
Re-verify at adoption.

### Physical quantities

- **Predicate** (needs scoping): a value is a dimensioned quantity
  when its unit carries a physical dimension — re-expressible in
  another unit of the same kind by a fixed factor (metres to feet),
  and addable only to same-kind values. Dimensionless counts and
  same-kind ratios (%, ppm) fall outside; currency fails the test and
  stays money.
- **Wire**: {value, explicit unit code, code system}, never a bare
  number; default the code system to UCUM (confirmed; FHIR-preferred).
- **Type discipline**: JSR-385 `unit-api` 2.2 with the Indriya 2.2.3
  reference implementation gives compile-time dimension safety for
  add, subtract, convert, and scalar scaling — a mass added to a
  volume fails to compile (confirmed). Limit: products and quotients
  are checked only at runtime, so derived-quantity math always needs
  test coverage.
- **Enforcement gap**: no off-the-shelf "raw arithmetic banned"
  check. ArchUnit cannot see operator-level `a + b` on primitives;
  the ban needs a custom Error Prone check, authored and
  false-positive-tuned (convention). The Checker Framework Units
  Checker is an all-compile-time alternative with a heavy annotation
  burden and a thin training corpus (uncertain).
- **Pin**: Indriya 2.2.3 — newest on Maven Central; the GitHub 2.2.4
  tag is not published there.

### Legal time

- **Predicate** (needs scoping): a time value is legal-time when a
  statute, regulation, or contract computes a right or obligation from
  the value itself — wrong by a day, and a named legal consequence
  follows. Retention start/end, limitation periods, legally fixed
  deadlines, and legal-state-change dates qualify. Ordinary event time
  (`created_at` for sort, logs, TTL) does not.
- **Wire**: UTC ISO-8601 `*_at` / `*_date` already cover ordinary
  time. A future legal deadline is the exception: store local
  wall-time plus the governing `ZoneId`, not a frozen UTC instant, and
  resolve the instant at evaluation time — zone rules can change
  before the date arrives (confirmed).
- **Type discipline**: `java.time` only (ban `Date` / `Calendar` /
  `Timestamp`). A wrapper such as `LegalDeadline(LocalDateTime
  wallTime, ZoneId governingZone)` with no bare-instant constructor
  forces every deadline to name its zone. Injected `Clock` and the
  wall-clock-read ban are rules the packs already carry.
- **Holiday / business-day math**: `de.focus-shift:jollyday-core` 2.x,
  the maintained fork (confirmed). ThreeTen-Extra 1.10.0 adds
  `PeriodDuration` and `Interval`; `Interval` is instant-based and
  zone-free, so a zoned retention window is a pair of `LegalDeadline`s.
- **Retention is two-sided**, not one number: a legal floor (verify at
  adoption — e.g. SOX ~7y, HIPAA 6y, BSA 5y, SEC 17a-4) and the GDPR
  Art. 5(1)(e) storage-limitation ceiling. The two can conflict, so a
  single default retention number is wrong by construction.
- tzdb ships inside the JDK and updates on the quarterly release, so
  two JVMs on different patch levels can resolve the same future
  deadline differently. Out-of-band updaters exist but were not
  confirmed against primary sources (uncertain); treat JDK patching as
  the primary path.

### Security-critical values

- **Predicate** (needs scoping): a value is security-critical when
  reading it alone lets an unauthorized party authenticate, authorize,
  decrypt, or impersonate — its confidentiality is the control. Key
  material, access-granting tokens, credentials, and pure secrets
  qualify; classify by capability, not opacity (a decodable JWT
  qualifies). PII and cardholder data are a different property with a
  different regime — a secret is zero-reveal, PCI permits a partial PAN
  reveal, PII returns to its subject — so do not fold them in.
- **Wire / log** (greenfield — no precedent profile line): a secret is
  write-only; never returned in a body, header, URL, or error message;
  never logged; never sent in cleartext. Grounded in OWASP ASVS
  v5.0.0.
- **Constant-time compare**: `MessageDigest.isEqual` is the stdlib
  answer (confirmed; real CVEs were fixed by switching to it). Scope it
  to fixed-length comparands, or hash both sides first.
- **Redaction as a type property**: wrap the value in a type whose
  `toString()` is overridden to mask, plus Jackson `@JsonIgnoreType` or
  a masking serializer — always-on redaction of the two dominant leak
  paths, SLF4J and JSON (confirmed). Trap: a Java record's
  auto-generated `toString` leaks the fields; override it.
- **Enforcement gap** (the predicted stress point, real): a
  build-failing "do not log this type" gate has no off-the-shelf check
  as of 2026. ArchUnit cannot do it — it sees the logger's erased
  `Object...` signature, not the argument's static type. It needs a
  custom Error Prone check (convention) or the Checker Framework
  Tainting Checker (uncertain, heaviest burden). The wire/redaction
  default is real and always-on; the gate is bespoke, not shipped.
- **Repo-side half**: CI secret scanning — gitleaks / TruffleHog
  (confirmed) — orthogonal to the in-JVM discipline. Transient
  credentials as `char[]` cleared after use shrink the exposure window
  but do not hide from a live heap dump; the String-pool memory
  argument is a myth.

### Cross-cutting traps (the highest-value finding)

An AI implementer building any of these steps on the same landmines,
because they dominate the training corpus. Whoever writes one of these
packs should ban them by name:

- **jqwik ≥ 1.10** — 1.10.0 shipped a hidden prompt injection (pulled
  from Maven Central); 1.10.1 prints an "ignore all results" anti-AI
  clause into test stdout that an implementing agent reads. Keep the
  ≤ 1.9.3 pin as a safety control, not just version hygiene (already
  the money pack's rule; now with a sharper reason).
- **Dead `de.jollyday:jollyday`** (last release 0.5.10, 2019) — the
  default reach; use `de.focus-shift` instead.
- **"Just store UTC"** for a future legal deadline — loses correctness
  when the zone's rules change; store wall-time plus zone.
- **ArchUnit for non-loggability** — structurally the wrong tool; it
  needs Error Prone.
- **Withdrawn units APIs** (JSR-275, JScience) and the **`char[]`
  string-pool myth** — both common, both wrong.

## 4. Recorded finding, pending amendment (2026-07-21)

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

## 5. Open research questions

Carried from the 2026-07-21 run:

- Property-testing replacement: jqwik is a maintenance dead end even
  at the clause-free 1.9.x pin. Evaluate successors before the next
  pack that needs property tests.
- Wire practice beyond the verified pair: Stripe and major
  bank/open-banking APIs (string decimal versus integer minor
  units), and what OpenAPI toolchains do with each.
- Rounding mandates not yet surveyed: US tax (IRS), IFRS/GAAP,
  interest-accrual conventions — a mandate anywhere would force a
  per-operation rounding table in the money pack.
- Precedent for opt-in, technology-naming defaults beside a
  technology-free standard — **addressed 2026-07-22**: golden-path
  programs (Spotify, Netflix) ship opinionated defaults that stay
  optional and win by being the path of least resistance; Google
  separates tooling-enforced rules from editable guidance; the
  Thoughtworks Radar is a versioned, revisable snapshot. The shape to
  copy: guardrail scope, golden-path governance, enforcement by
  tooling in the adopting repo, divergence recorded rather than gated.

From the 2026-07-22 pass:

- Physical quantities: JSR-385/Indriya versus hand-rolled records, and
  the false-positive cost of a custom Error Prone operator-ban versus
  the Checker Framework Units Checker.
- Security: whether any off-the-shelf "do not log" Error Prone pattern
  exists, and the annotation burden of the Checker Framework Tainting
  Checker on a real Spring Boot + jOOQ codebase.
- Whether the security wire predicate belongs in the profile at all —
  it is greenfield, and secrets are arguably more a runtime/type
  property than a wire-shape one.
- Legal time: verify MiFID II retention against EUR-Lex; the
  floor-versus-ceiling resolution pattern (legal hold,
  pseudonymization, purpose-scoped deletion); which jurisdictions'
  holiday calendars ship versus stay adopter-bound; and whether to
  record the tzdb version at capture.
