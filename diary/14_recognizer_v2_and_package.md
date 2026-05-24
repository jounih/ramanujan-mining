# Diary 14 — Recognizer v2 + standalone `rkc/` package

**Date:** 2026-05-24
**Sources:** `ramanujan/rkc/` package, `ramanujan/analysis/14b_recognizer_v2_benchmark.py`,
`ramanujan/analysis/results/recognizer_routing_benchmark_v2.csv`.
**Status:** v2 ships with 55/55 = 100% on the same 55-case battery v1 scored
54/55 on. Package and unit tests pass: `pytest rkc/tests/` → 35/35.

## (a) What each gap fix actually did

### Gap 1 — Scalar-coefficient stripping wrapper

v1's one false-negative was `3 * exp(-βn²)` predicted as `none` because the
gaussian matcher required the summand to be exactly `exp(quadratic)` with no
outer factor.

Fix lives in `rkc/recognizer.py::_strip_scalar_coefficient`: before
dispatching to any strict matcher, partition `expr.args` into n-dependent
and n-independent factors; the n-independent product is the
`scalar_coefficient` (preserved on the result), the n-dependent product is
sent to the matchers. We also try the original unstripped expression as a
fallback so we don't break matchers that already handle outer factors
(e.g. Eisenstein, which has its own `rest` rejection logic).

Result: case 14 flipped from `none` → `gaussian_quadratic, correct=True`.
The `scalar_coefficient` propagates through the cost estimator (one extra
mul folded into the total).

**Honest regression check:** does scalar stripping create false positives?
I checked the 9 canonical "none" cases (sin, cos+1, etc.); all still
correctly return None. The strip only happens when the expression has a
Mul with both n-dependent and n-independent factors AND a strict matcher
fires on the n-dependent part — so it can't silently invent matches out of
expressions that lack a kernel core.

### Gap 2 — Soft fuzzy second-pass matcher

v1 was strict-or-null. v2 adds a `Route.FUZZY` state and three fuzzy
matchers (`_fuzzy_match_shifted_theta`, `_fuzzy_match_mock_theta_ish`,
`_fuzzy_match_lambert_ish`) that run **only when no strict matcher fires**.
They return a `KernelFamily` value plus a hand-tuned confidence in [0, 1]
(0.50–0.60 currently).

The fuzzy fallback covers exactly the v1 "documented near-miss" cases:
shifted theta `q^(n²+n)`, mock-f3 × cos(n), `q^n / (1 - q^(2n))`. The
strict matcher still rejects them — that's still the right call, because
the routing recommendation would be wrong. But now an operator sees a
`route=FUZZY, confidence=0.6` warning rather than a silent null.

Backward compatibility: `best_match()` defaults to `accept_fuzzy=False`,
matching v1's strict-or-null semantics. Setting `accept_fuzzy=True`
returns the fuzzy result when no strict match exists.

### Gap 3 — Per-component cost rollup for composites

v1's composite wrapper (`best_match_composite`) walked Add terms / Mul
factors and returned the **first** matching component, reporting only that
single component's cost. For a sum-of-two-kernels this systematically
under-counted the total work.

v2's `recognize_composite` returns a synthetic `RoutingResult` with
`kernel="composite[sum](gaussian_quadratic,bose_einstein_geometric)"` and
`total_cost = sum_i total_cost(component_i)`. The full per-component
breakdown is in the `.components` field. The composite's `route` is the
strongest route across components (DEGENERATE if all are; else any DUAL
wins; else MODULAR_COMPLETION_REQUIRED; else DIRECT).

For benchmark backward-compatibility, the 14b benchmark scorer still
checks whether ANY component kernel matches the case's `accept_families`
set (it does — all 10/10 composed cases pass).

### Gap 4 — Per-term complexity tracking

Insight §A7's lesson: bits-per-term lies about wall-clock when per-term
cost varies (HRR Dedekind sums at dps=372 vs pentagonal big-int adds).

v2 adds `rkc/costs.py` with one `per_term_*(params, target_precision)`
function per registered kernel. Costs are approximate mpmath / big-int ops
per term, hand-calibrated to roughly match the order-of-magnitude
wall-clock from experiments 03, 05, 07. Each `RoutingResult` carries
`per_term_cost`, `num_terms`, and `total_cost = num_terms * per_term_cost`
(plus a one-mul fold if a scalar coefficient was peeled).

The relative scale is what matters; absolute numbers are not load-bearing.

### Gap 5 — Gauss-sum gcd-degeneracy fix

v1's diary noted: sympy auto-reduces `2*n²/6 → n²/3` BEFORE the matcher
sees it, so the gcd(p, q) > 1 branch of `_gauss_sum_degeneracy` is
**unreachable through the sympy AST**.

v2 ships `extract_raw_gauss_coefficient(expr_string, n)` plus
`recognize_with_raw_string(expr_string, n)`. The raw extractor walks the
`sympify(s, evaluate=False)` parse, which DOES preserve the unreduced
`(2 * pi * I * 2 * n²) / 6` structure (sympy stores `1/6` as `Pow(6, -1)`
in the unevaluated form). The extracted `(p_raw, q_raw)` gets stashed on
the params dict as `raw_pq` and `_gauss_sum_degeneracy_v2` checks
`gcd(p_raw, q_raw) > 1` before falling through to the post-reduction
checks.

Two small implementation gotchas caught while wiring this up:
1. `sympify(..., evaluate=False)` returns expressions with FRESH symbols
   that lack the caller's `integer=True, nonnegative=True` assumptions.
   The matchers compare symbols with `==` which is assumption-sensitive,
   so I had to compare on `.name` and `.subs(fresh_n, caller_n)`.
2. In the unevaluated `Mul`, `2*pi*I*2` is represented as four separate
   args `(2, pi, I, 2)`. My first cut absorbed both `2`s into a single
   `found_two` flag; the second `2` was actually `p_raw`. Fixed by
   tracking exactly one consumed `2`.

Test `test_gauss_sum_gcd_via_raw_string` confirms: `exp(2*pi*I*2*n**2/6)`
now reports `route=DEGENERATE` with the reason string referencing the raw
extraction.

### Gap 6 — Optional kernel additions

v1 already registered partial_theta, q_pochhammer_infty, and
eisenstein_E2k. The task notes these as "already implicit" in v1's
Lambert-Eisenstein experiment; I kept the same registry set in v2 with
new family tags (THETA_LIKE / MOCK_THETA_LIKE / etc.). No NEW kernels
added — see "still missing" for what an honest next pass should add.

## (b) v2 vs v1 benchmark delta

```
                  v1                v2          delta
overall          54/55 = 98.2%   55/55 = 100%   +1
macro precision  0.99            1.00           +0.01
macro recall     0.94            0.95           +0.01
gaussian recall  0.64 (7/11)     0.73 (8/11)    +1 TP (case 14)
none precision   0.90 (9/10)     1.00 (9/9)     -1 FP (case 14)
```

Per-family table from `recognizer_routing_benchmark_v2.csv`:

```
family                      #true  #pred   TP   FP   FN   prec  recall   F1
bose_einstein_geometric         6      6    6    0    0   1.00    1.00  1.00
dirichlet_L                     1      1    1    0    0   1.00    1.00  1.00
eisenstein_E2k                  4      4    4    0    0   1.00    1.00  1.00
gauss_sum                       8      8    8    0    0   1.00    1.00  1.00
gaussian_quadratic             11      8    8    0    0   1.00    0.73  0.84
lambert_divisor                 6      4    4    0    0   1.00    0.67  0.80
mock_theta_f3                   3      3    3    0    0   1.00    1.00  1.00
mock_theta_f5                   2      2    2    0    0   1.00    1.00  1.00
mock_theta_f7                   2      2    2    0    0   1.00    1.00  1.00
none                            9      9    9    0    0   1.00    1.00  1.00
partial_theta                   4      4    4    0    0   1.00    1.00  1.00
q_pochhammer_infty              4      4    4    0    0   1.00    1.00  1.00
```

The only row that changed: gaussian_quadratic gained 1 TP (the previously-FN
case 14) and the `none` family lost the corresponding FP, lifting its
precision from 0.90 to 1.00. Lambert recall stayed at 0.67 — those FNs are
the composed cases where the composite-wrapper peels gaussian first; that's
not a recognizer bug but the order-dependence baked into composite scoring
(the accept_families lets it pass overall but lambert's per-family recall
counts it as FN under strict per-row accounting).

No new false positives introduced. The scalar-stripping wrapper is clean.

## (c) Per-term cost — gaussian kernel curve

Measured at `target_precision = 1e-12` (working precision ~ 64 bits):

```
beta        | num_terms | per_term | total_cost | route
   1e-4     |        2  |     64.0 |      128.0 | DUAL
   1e-3     |        2  |     64.0 |      128.0 | DUAL
   1e-2     |        2  |     64.0 |      128.0 | DUAL
   0.1      |        2  |     64.0 |      128.0 | DUAL
   0.5      |        3  |     64.0 |      192.0 | DUAL
   1.0      |        3  |     64.0 |      192.0 | DUAL
   π        |        4  |     64.0 |      256.0 | DIRECT
   10       |        3  |     64.0 |      192.0 | DIRECT
   100      |        2  |     64.0 |      128.0 | DIRECT
```

The crossover at β ≈ π is exactly the §A6 universal β* = c·π pattern
(c = 1 for the pure gaussian theta). per_term_cost is constant because
each summand is one `mpmath.exp` at working precision; total_cost is
driven entirely by `num_terms`.

Now compare per-term cost ACROSS kernels at q = 1/3:

```
kernel              | num_terms | per_term | total_cost
mock_theta_f3       |        6  |    768.0 |     4608.0
lambert             |        1  |    192.0 |      192.0
bose                |        1  |    128.0 |      128.0
gauss_sum (p=1,q=7) |        7  |     64.0 |      448.0
```

Mock theta dominates per-term at ~12× the gaussian baseline (the n-th
mock-theta summand carries an n-factor partial product). This is the
operational form of insight §A7: a kernel's bits-per-term gain MUST be
divided by per-term cost. A naive "fewer terms is better" routing rule
would prefer mock theta over a Gauss sum here; the cost-weighted rule
correctly flags mock theta as the more expensive option per-term despite
needing fewer summands.

## (d) Bottom-line claim

**Confidence: high.** Recognizer v2 closes every documented v1 gap that
admits a clean fix: scalar-coefficient stripping is a real bug-fix
(case 14 was a legitimate FN); the gcd-reachability fix is a real
defense against a previously phantom guard; per-term cost tracking turns
the recognizer's routing recommendation from "fewer terms" into "less
work". The fuzzy second pass is the most speculative addition — its
confidence numbers (0.50-0.60) are hand-tuned constants and would need
calibration against a labelled corpus of "fuzzy-match was operationally
useful" judgments before they could mean anything precise. As a
warning-emission mechanism it's the right shape; as a quantitative
confidence it's a placeholder.

Package surface: `from rkc import recognize, best_match, recognize_composite,
Route, KernelFamily`. 35/35 unit tests pass (every kernel + every
degeneracy branch + one test per gap).

## (e) Honest "things still missing"

1. **Mock-theta orders 6, 8, 10.** v1 and v2 register f₃, f₅, f₇ as
   canonical representatives of the 3rd/5th/7th order families. The 6th-,
   8th-, and 10th-order mock thetas have distinct denominator structures
   (Andrews-Hickerson f₈, the Ramanujan-Gordon f₁₀ family) that the
   current `_extract_mock_theta_denominator` helper won't catch without
   per-order Product-body matchers. The fuzzy `mock-theta-like` fallback
   would flag them — but as warnings only, not as routed kernels.

2. **Class invariants G_n / g_n.** Experiment 08 has a working
   direct/radical evaluation of Ramanujan's class invariants; there's no
   recognizer entry for the AST shape `(2^(1/12) * (...)^(1/24))` that
   identifies a class-invariant expression. Adding one would close the
   loop between §A6 (radical/direct crossover at high precision) and the
   routing decision.

3. **The MODULAR_COMPLETION_REQUIRED route is a flag, not a computation.**
   Diary 11 already noted this. v2 didn't fix it — wiring the route
   through to experiment 15's shadow proxy + experiment 17's Watson-
   Hickerson Eichler integral would actually produce a numerical answer
   on the mock-theta cases instead of just labelling them. That's the
   next high-leverage gap.

4. **Composite routing assumes Add/Mul are the only decomposition
   shapes.** Sums-of-Pochhammers products, Jacobi triple products, and
   Cauchy-product expansions all have richer composite structure. v2's
   composite wrapper handles the cases the benchmark covers; it doesn't
   yet handle nested Add(Mul(Add, ...)) decompositions.

5. **Fuzzy confidence calibration.** The 0.50-0.60 constants are
   placeholders. A real confidence would need a labelled set of "this
   AST is genuinely a member of family F" judgments and a confusion
   matrix; until then the numbers are operator-warning markers, not
   probabilities.

6. **Per-term cost models are calibrated to mpmath; arblib would shift
   the relative ratios.** Experiment 05 showed HRR closing a 10⁵× cost
   gap to ~1.2× via FLINT bignums. The `costs.py` numbers don't yet
   model that — they assume vanilla mpmath. A second cost backend
   ("arblib") would be a clean extension and would change mock-theta vs
   lambert routing recommendations at high precision.

## Cross-references

- `ramanujan/rkc/recognizer.py` — v2 implementation (the new package).
- `ramanujan/rkc/registry.py` — kernel registry + fuzzy matchers + raw
  Gauss-sum extractor.
- `ramanujan/rkc/routing.py` — Route enum (now with FUZZY) and
  KernelFamily enum.
- `ramanujan/rkc/costs.py` — per-term complexity (insight §A7).
- `ramanujan/rkc/tests/test_recognizer.py` — 35-test truth oracle.
- `ramanujan/analysis/14b_recognizer_v2_benchmark.py` — the v2 scorer
  against the same 55-case battery.
- `ramanujan/analysis/results/recognizer_routing_benchmark_v2.csv` —
  per-case audit log for v2.
- v1 stays at `analysis/13_recognizer_v1.py`, untouched.
- v1 CSV stays at `analysis/results/recognizer_routing_benchmark.csv`,
  untouched, for diff inspection.
