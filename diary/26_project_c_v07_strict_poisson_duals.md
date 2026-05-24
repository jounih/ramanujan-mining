# Diary 26 — Project C v0.7: half-shifted + weighted Gaussian Poisson duals

**Date:** 2026-05-24
**Source:** Extension of `rkc/search/basis.py::_mellin_inversion_apply`
(originally v0.4, diary 14b commit `945e01f`). Strict-bar numerical
verification via `rkc/search/verifiers.py::MpmathVerifier`. New tests
in `rkc/tests/test_cli.py`; new seeds in `rkc/search/seeds.py`.
**Status:** SHIPPED. 73/73 tests passing (67 v0.6 baseline + 6 new
v0.7 tests). 2 new identity classes operational end-to-end through the
six-step engine; 2 strategically-deferred to v0.8 with rationale in
[`DID_NOT_PAN_OUT §R17`](../insights/DID_NOT_PAN_OUT.md).

## Setup

Project C v0.4 shipped the **first** concrete operator transformation —
the keystone Poisson summation on a pure Gaussian:

```
exp(-β n²)  →  √(π/β) · exp(-π² n²/β)
```

acceptably end-to-end through the verifier + cost gate at small β
(54× speedup at β=1/100). v0.5 added master-theorem on Integral
expressions; v0.6 added the parallel sweep harness across a 15-seed
library.

**The brief for v0.7** (per project notes) was to extend
`_mellin_inversion_apply` to one or two additional kernel families.
The natural candidates from rkc's existing routing layer
(`rkc/registry.py::_route_bose_einstein` and `_route_lambert`) are:

1. **Bose-Einstein partition** `1/(1 - exp(-β n))` summand
2. **Lambert/divisor** `n·q^n/(1-q^n)` summand

both with documented dual-β formulas in rkc's cost model
(`dual_beta = 4π²/β` and `q' = exp(-4π²/-log q)` respectively).

## What I did

### Strategy decision — strict-bar discipline blocks the obvious path

The Bose-Einstein and Lambert sums are **one-sided** (n ≥ 1), and their
modular transformation laws carry essential **additive scalar
correction terms**:

```
Σ_{n≥1} 1/(e^{βn}-1)   =  π²/(6β) - 1/2 - (1/2)log(β/2π) + O(exp(-4π²/β))
Σ_{n≥1} n q^n/(1-q^n)  =  E_2-related; quasi-modular law has additive 6iτ/π
```

Neither admits a clean `Σ_n f(n) = Σ_n g(n)` term-by-term identity at
the dual parameter. The MpmathVerifier (`_sum_evaluate` at
`rkc/search/verifiers.py:149`) compares full `mpmath.nsum`-evaluated
sums; any naive "emit dual summand and verify" would fail by exactly the
additive correction term.

The current `Operator.apply_fn(expr, n) → expr | None` API can return
ONE new summand and nothing else — it cannot emit a separate scalar
correction that gets folded into the comparison. Capturing that
structure cleanly requires a richer operator class
(`modular_transform_with_correction`) with `apply_fn` returning
`(new_summand, additive_scalar)`, plus a verifier extension that
subtracts the additive correction from the before-side sum before
comparing. **That is a v0.8 scope** — the data model change has
downstream effects on `OperatorApplication`, the engine's verification
step, and the registry serialisation.

For v0.7 I chose the **Strategy D path from the brief**: ship two
genuinely-new identity classes that ARE clean strict double-sided
Poisson identities and fit the existing API unchanged. This preserves
the strict-bar discipline (no "approximate identity passes if you squint
at small β" — every accepted identity holds to numerical zero across
the test sweep).

### Case A — half-integer-shifted Gaussian (theta₂ / theta₄ partner)

**Identity.**

```
Σ_{n ∈ Z} exp(-β (n + 1/2)²)  =  √(π/β) · Σ_{k ∈ Z} (-1)^k · exp(-π² k²/β)
```

This is the classical theta₂ ↔ theta₄ modular S-transform — the
half-shift partner of v0.4's theta₃ keystone case. Derivation: Poisson
summation with the phase `exp(2πi k · 1/2) = (-1)^k` from the
half-integer translation.

**Implementation.** Add `_poisson_dual_half_shift_gaussian(expr, n)` to
`rkc/search/basis.py`. AST inspection: parse `c · exp(arg)` with `arg`
a degree-2 polynomial in `n` whose coefficient signature is
`a2 = a1 = -β`, `a0 = -β/4`. Decline cleanly on any other offset
(`(n + 1/3)` etc.) — the dual becomes complex-valued for non-half
rational shifts and we don't yet have summand-complex-comparison logic.

**Numerical evidence (strict bar).** Verified via `mpmath.nsum` at
dps=50 over the symmetric range `(-∞, +∞)`:

| β | LHS (Σ_n exp(-β(n+1/2)²)) | Relative error vs RHS |
|---|---|---|
| 1e-4 | 177.245... | 4.85e-38 |
| 1e-3 | 56.0499... | 0 |
| 1e-2 | 17.7245... | 0 |
| 1e-1 | 5.60499... | 0 |
| 1    | 1.77227... | 0 |
| 5    | 0.57303... | 0 |

The single 1e-38 residual at β=1e-4 is the truncation tail at dps=50,
not an identity defect — the sum has ~530 effectively-contributing
terms at that β.

### Case B — weighted Gaussian (second moment, derivative of v0.4)

**Identity.**

```
Σ_{n ∈ Z} n² · exp(-β n²)  =  √(π/β) · Σ_{k ∈ Z} (1/(2β) - π² k²/β²) · exp(-π² k²/β)
```

Derivation: differentiate v0.4's identity in β and rearrange. Stays a
single-summand transformation (no Add of two sub-duals visible at the
API), which is the key API-fit property.

**Implementation.** Add `_poisson_dual_weighted_gaussian(expr, n)` to
the same file. AST inspection: parse the input as `c · n² · exp(arg)`
where `arg` is a pure deg-2 polynomial in n (a1 = a0 = 0). Declines on
`n^3` (no third-moment identity wired) and on `n² · exp(linear in n)`
(would be a different family).

**Numerical evidence (strict bar).** Same sweep, dps=50, two-sided
sum:

| β | LHS (Σ_n n²·exp(-β n²)) | Relative error vs RHS |
|---|---|---|
| 1e-4 | 886226.9... | 1.16e-34 |
| 1e-3 | 28024.96... | 0 |
| 1e-2 | 886.227... | 0 |
| 1e-1 | 28.0249... | 0 |
| 1    | 0.884509... | 0 |
| 5    | 0.013476... | 0 |

Same 1e-34 truncation-residual at the extreme β=1e-4; numerical zero
elsewhere. Six orders of magnitude in β with strict agreement.

### Cost-model wiring

The half-shift and weighted forms don't match rkc's strict
`gaussian_quadratic` matcher (which refuses any non-pure form). For the
half-shift, the existing fuzzy matcher catches the theta-like
signature; `_manual_cost_estimate` then computes the `sqrt(28/β)` term
count from the `a2` coefficient. For the weighted form (which rkc's
fuzzy matcher also declines, because of the polynomial prefactor), I
added `_gaussian_family_cost(expr, var)` in
`rkc/search/routers.py` — a structural-cost helper that recognises
`polynomial(n) · exp(quadratic in n)` and computes the same theta-tail
term-count estimate.

With this in place the engine reports the expected cost ratios:

- Half-shift β=1/100: 53× cheaper after Poisson dual ✓
- Weighted β=1/100: 53× cheaper after Poisson dual ✓
- Weighted β=5 (anti-test): 0.75× — fails the cost gate cleanly ✓

The anti-test confirms the cost model isn't just rubber-stamping
mellin_inversion outputs — at large β the direct sum is genuinely
faster and the dual gets rejected with `COST_NOT_IMPROVED`.

### Engine-level acceptance

Added two new seeds to `rkc/search/seeds.py`:
- `gaussian_half_shift_beta_1em2`
- `gaussian_weighted_beta_1em2`

Both produce one acceptance each in a 30-budget search at depth 1,
with the expected ~53× cost-ratio improvement. Tested via the new
`test_v07_seeds_buildable_and_recover_identity` in
`rkc/tests/test_cli.py`.

## What I deferred and why

**Bose-Einstein and Lambert one-sided summands** — deferred to v0.8 per
the structural reason above. Their seeds remain in `seeds.py` (now
correctly labelled `(v0.8+)` in their `expected_route` strings rather
than the previous `(v0.7+)`), so they still surface in the sweep
harness as future targets. The structural blocker — operator-API can't
carry an additive correction — is now documented in
[`DID_NOT_PAN_OUT §R17`](../insights/DID_NOT_PAN_OUT.md) for the
methodological record.

**Higher-moment Gaussian weights** — `n^k · exp(-β n²)` for k ≥ 3 not
implemented. The k=2 case requires its own derivative identity; each
k > 2 would require a separate explicit formula (no recursive pattern
shared with the proposer-side parameter space). v0.8+ if a use case
materialises.

**Linear-coefficient Gaussian** — `exp(-β n² + α n)` for irrational α
gives complex-valued dual summands. Skipped for v0.7; tractable in a
later release once the verifier handles complex-summand comparison
cleanly.

## Tests

73/73 passing:
- 67 baseline (v0.6) preserved unchanged
- 6 new v0.7 tests:
  - `test_v07_mellin_inversion_half_shift_apply_fn_directly`
  - `test_v07_mellin_inversion_weighted_apply_fn_directly`
  - `test_v07_mellin_inversion_verifier_strict_agreement`
  - `test_v07_mellin_inversion_half_shift_accepted` (engine end-to-end)
  - `test_v07_mellin_inversion_weighted_accepted` (engine end-to-end)
  - `test_v07_seeds_buildable_and_recover_identity`

Recognizer benchmark `analysis/14b_recognizer_v2_benchmark.py` remains
55/55 = 100% (no regression).

## Bottom line

**One-line claim.** v0.7 extends the Project C operator basis with two
new strict Poisson identities (half-shifted theta₂/theta₄, weighted
Gaussian second-moment), both verified to numerical zero across six
orders of magnitude in β, both producing the expected ~53× cost ratio
at small β and correctly failing the cost gate at large β.
**Confidence: high** (strict-bar agreement on both identities; clean
behaviour on the anti-tests).

**What it changes operationally.** Project C's basis grows from one
concrete operator transformation (v0.4 pure Gaussian) to three (v0.7
adds half-shift + weighted), all in the same `mellin_inversion`
operator. The basis-coverage trajectory toward the controlled-validation
case (≥80% of rkc's 11 known kernel identities recovered by random
composition within budget=1000 compositions of length ≤3) inches
forward; the weighted case is particularly relevant for the partition
function / Bose-Einstein neighbourhood since `n²·exp(-β n²)` is the
natural "energy expectation value" summand.

**What stays unchanged.** The closed Pass D verdict (g* irreducibly
Eichler), the Hunt 5 / 5b QR-vs-Notebooks toolkit-split finding, and
the Pass A β\* = c·π crossover pattern across five kernels. v0.7 is a
basis-coverage extension, not a new substantive finding.

**Next step (v0.8).** Extend the OperatorApplication API to carry an
additive scalar correction; add `modular_transform_with_correction` as
a new operator id with apply_fn for Bose-Einstein and Lambert; re-wire
the verifier to fold the correction into the before-side residual
before comparing. This unblocks the two seeds still labelled
`(v0.8+)` and starts to bridge the v0.7 strict-Poisson side to the
modular-with-anomaly side that the toolkit-split finding placed in the
Notebooks (Ch. 32 + Ch. 36 + Ch. 34 modular_S_transform corpus).
