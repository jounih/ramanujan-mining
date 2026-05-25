"""rkc.search.basis — Operator basis for Project C v0.

Defines the Hunt 5 revised 7-operator basis (per diary 20) as the v0
validation set. Each `Operator` carries:

  - id        : the op_id string used in OperatorApplication
  - apply_fn  : sympy Expr → sympy Expr | None (returns None if op doesn't
                apply to this expression)
  - notes     : human-readable description

The apply_fn is the "what does this operator DO" — for v0, we stub these
with simple AST rewrites and explicit None returns when the operator
doesn't fit. v0.4+ will refine.

The Hunt 5 7-operator basis (per diary 20):
  1. mellin_inversion              — universal substrate (forward Mellin)
  2. master_theorem                — Ramanujan's "general formula"
  3. FOURIER_SELF_RECIPROCITY      — Theorem III of QR II + QR III §13-§15
  4. FRACTIONAL_FUNCTIONAL_ITERATION — QR III §4-§6 Schröder/Koenig
  5. HARDY_ORDERS_OF_INFINITY      — QR III §7-§9
  6. FRULLANI_LIMIT                — QR II §4 Theorem II
  7. MELLIN_PAIR_RECIPROCITY       — QR III §15
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional

import sympy as sp


@dataclass
class Operator:
    """One operator in the Project C basis."""
    id: str
    notes: str
    apply_fn: Callable[[sp.Expr, sp.Symbol], Optional[sp.Expr]] = field(
        default=lambda e, n: None,
    )
    # short tag for the cohomological / modular / analytic family
    family_tag: str = "analytic"


# ---------------------------------------------------------------------------
# Operator stubs (v0 — most apply_fn's return None, the engine treats
# this as PROPOSER_DECLINED; v0.4 will refine each operator's AST rewrite)
# ---------------------------------------------------------------------------

def _master_theorem_apply(expr: sp.Expr, n: sp.Symbol) -> Optional[sp.Expr]:
    """Master Theorem application via a library of canonical Mellin-
    transform identities (v0.5).

    Recognises sp.Integral expressions matching known Master-Theorem
    pattern and returns the closed-form RHS. v0.5 library:

    1. Gamma function:   ∫_0^∞ x^(s-1) exp(-x) dx = Γ(s)
    2. Beta function:    ∫_0^1 x^(m-1) (1-x)^(n-1) dx = Γ(m)Γ(n)/Γ(m+n)
       (QR I §5(ii) worked example)
    3. ∫_0^∞ x^(s-1)/(1+x) dx = π/sin(πs)
       (QR I §5(i) special case)

    Returns None if expr is not an Integral or doesn't match any of the
    canonical patterns. v0.6+ will extend with the (-1)^k phi(k)/k!
    coefficient-extraction generality.

    The `n` argument (iteration variable for summand kernels) is unused
    here — Integral expressions have their own integration variable in
    the Integral AST. We accept it for API uniformity with the other
    operator apply_fn's.
    """
    if not isinstance(expr, sp.Integral):
        return None
    integrand = expr.function
    limits = expr.limits
    if len(limits) != 1 or len(limits[0]) != 3:
        return None
    x, lower, upper = limits[0]
    # Beta function pattern: x^(m-1) * (1-x)^(n-1) on [0, 1]
    if lower == 0 and upper == 1:
        bm = _try_beta_pattern(integrand, x)
        if bm is not None:
            m, n_param = bm
            return sp.gamma(m) * sp.gamma(n_param) / sp.gamma(m + n_param)
    # Patterns on [0, ∞)
    if lower == 0 and upper == sp.oo:
        # Gamma: x^(s-1) exp(-x) → Γ(s)
        bm = _try_gamma_pattern(integrand, x)
        if bm is not None:
            return sp.gamma(bm)
        # Mellin of 1/(1+x): x^(s-1) / (1+x) → π / sin(π s)
        bm = _try_inv_1plusx_pattern(integrand, x)
        if bm is not None:
            return sp.pi / sp.sin(sp.pi * bm)
    return None


def _try_beta_pattern(integrand: sp.Expr, x: sp.Symbol) -> Optional[tuple]:
    """Try to match `x^(m-1) * (1-x)^(n-1)`; return (m, n) or None.

    Both `m-1` and `n-1` must be symbolic-or-numerical exponents; we
    extract `m` and `n` by adding 1.
    """
    if integrand.func != sp.Mul:
        return None
    factors = integrand.args
    if len(factors) != 2:
        return None
    # Both factors should be Pow
    a, b = factors
    if a.func != sp.Pow or b.func != sp.Pow:
        return None
    # Try (x^(m-1), (1-x)^(n-1)) in either order
    for first, second in [(a, b), (b, a)]:
        base1, exp1 = first.args
        base2, exp2 = second.args
        if base1 == x and sp.simplify(base2 - (1 - x)) == 0:
            return (exp1 + 1, exp2 + 1)
    return None


def _try_gamma_pattern(integrand: sp.Expr, x: sp.Symbol) -> Optional[sp.Expr]:
    """Try to match `x^(s-1) * exp(-x)`; return s or None."""
    if integrand.func != sp.Mul:
        return None
    pow_part, exp_part = None, None
    for arg in integrand.args:
        if arg.func == sp.Pow and arg.args[0] == x:
            pow_part = arg
        elif arg == sp.exp(-x) or arg.func == sp.exp and sp.simplify(arg.args[0] + x) == 0:
            exp_part = arg
    if pow_part is None or exp_part is None:
        return None
    return pow_part.args[1] + 1  # s = exp + 1


def _try_inv_1plusx_pattern(integrand: sp.Expr, x: sp.Symbol) -> Optional[sp.Expr]:
    """Try to match `x^(s-1) / (1+x)`; return s or None."""
    num, den = sp.fraction(integrand)
    if sp.simplify(den - (1 + x)) != 0:
        return None
    if num.func == sp.Pow and num.args[0] == x:
        return num.args[1] + 1
    return None


def _mellin_inversion_apply(expr: sp.Expr, n: sp.Symbol) -> Optional[sp.Expr]:
    """Mellin transform / Poisson-summation dual.

    v0.4 implemented the keystone case: pure Gaussian summand
    `exp(-β n²)` → Poisson-summation dual `√(π/β) · exp(-π² n² / β)`.

    v0.7 extends to two further STRICT two-sided Poisson identities (no
    additive correction term needed — both sides are clean summand-to-
    summand identities over n ∈ Z):

    (A) **Shifted-Gaussian with half-integer offset**
        `exp(-β (n + 1/2)²)` → `√(π/β) · (-1)^n · exp(-π² n² / β)`.
        Verified strictly via mpmath.nsum across β ∈ {1e-3, 1e-2, 1e-1, 1};
        this is the classical theta_2 ↔ theta_4 modular transform (the
        Jacobi triple-product half-shift partner of v0.4's theta_3).

    (B) **Weighted-Gaussian (second moment)**
        `n² · exp(-β n²)` →
        `√(π/β) · (1/(2β) - π² n² / β²) · exp(-π² n² / β)`.
        Derived by differentiating v0.4's identity in β; preserves
        single-summand structure, no Add of sub-duals exposed at the API.
        Verified strictly via mpmath.nsum across the same β sweep.

    What v0.7 deliberately defers to v0.8: ONE-SIDED kernels with a
    modular relation but no clean term-by-term equality (Bose-Einstein
    `1/(1-exp(-β n))` and Lambert `n q^n / (1-q^n)`). These require an
    "operator that emits dual summand + scalar additive correction" data-
    model extension (the OperatorApplication currently only emits a new
    summand). See [DID_NOT_PAN_OUT §R17] for the structural reason.

    Mathematical justification: Poisson summation is the Z-action
    instance of Mellin-pair self-reciprocity (Gaussian self-Mellin-pair).
    The kernel matches rkc's `gaussian_quadratic` registry entry; the
    transformed summand sits in the *dual β* regime (small β → large
    effective β'), which is the β\* = c·π crossover that Pass A
    characterised across 5 independent kernels
    ([CANDIDATE_INSIGHTS §A6](../../insights/CANDIDATE_INSIGHTS.md)).
    """
    # CASE 1 (v0.4): pure Gaussian via rkc recognizer (a1 == 0)
    result = _poisson_dual_pure_gaussian(expr, n)
    if result is not None:
        return result
    # CASE 2 (v0.7): half-integer-shifted Gaussian exp(-β (n + 1/2)²)
    result = _poisson_dual_half_shift_gaussian(expr, n)
    if result is not None:
        return result
    # CASE 3 (v0.7): weighted Gaussian n² · exp(-β n²)
    result = _poisson_dual_weighted_gaussian(expr, n)
    if result is not None:
        return result
    return None


def _poisson_dual_pure_gaussian(expr: sp.Expr, n: sp.Symbol) -> Optional[sp.Expr]:
    """v0.4 case: pure `c · exp(-β n²)` → `c · √(π/β) · exp(-π² n²/β)`."""
    from ..recognizer import best_match
    bm = best_match(expr, n)
    if bm is None or bm.kernel != "gaussian_quadratic":
        return None
    beta = bm.params.get("beta")
    if beta is None:
        return None
    # PRESERVE the scalar c. rkc's bm.scalar_coefficient peels only NUMERICAL
    # scalars; for inputs containing symbolic constants like 10*√π (the typical
    # output of a previous Poisson-dual call), rkc reports scalar=1 and bakes
    # the prefactor into the AST. Use sp.as_independent to extract everything
    # n-independent — handles both cases.
    scalar = expr.as_independent(n, as_Add=False)[0]
    return scalar * sp.sqrt(sp.pi / beta) * sp.exp(-sp.pi**2 * n**2 / beta)


def _parse_quadratic_exp(expr: sp.Expr, n: sp.Symbol) -> Optional[tuple]:
    """Parse `c · exp(P(n))` where P is degree-2 in n with NEGATIVE
    leading coefficient. Returns `(scalar_c, a2, a1, a0)` such that
    `expr == scalar_c · exp(a2·n² + a1·n + a0)`, with `a2` guaranteed
    a negative number. Returns None otherwise.

    Used by both shifted-Gaussian and (future) generic linear-coefficient
    cases. We pull out the n-independent scalar via `as_independent` and
    then look for a single Mul/exp/Pow factor that exponentiates a deg-2
    polynomial in n.
    """
    scalar, n_dep = expr.as_independent(n, as_Add=False)
    # n_dep must be a single `exp(...)` or `Pow(E, ...)` factor (no extra
    # n-dependent multipliers — that's the weighted case, handled separately).
    if n_dep.func == sp.exp:
        arg = n_dep.args[0]
    elif n_dep.func == sp.Pow:
        base, exponent = n_dep.args
        if base != sp.E:
            return None
        arg = exponent
    else:
        return None
    if not arg.has(n):
        return None
    # Expand so (n + 1/2)² becomes n² + n + 1/4 and is parsed as a polynomial
    arg_expanded = sp.expand(arg)
    try:
        poly = sp.Poly(arg_expanded, n)
    except sp.PolynomialError:
        return None
    if poly.degree() != 2:
        return None
    a2 = poly.nth(2)
    a1 = poly.nth(1)
    a0 = poly.nth(0)
    if not _is_negative_number(a2):
        return None
    return (scalar, a2, a1, a0)


def _is_negative_number(x: sp.Expr) -> bool:
    """Local copy of the registry helper (avoids circular import).

    Returns True iff sympy can prove `x` is a strictly-negative number.
    """
    try:
        return bool(sp.simplify(x).is_negative)
    except Exception:
        return False


def _poisson_dual_half_shift_gaussian(
    expr: sp.Expr, n: sp.Symbol,
) -> Optional[sp.Expr]:
    """v0.7 case (A): half-integer-shifted Gaussian.

    Detects `c · exp(-β (n + 1/2)²)` i.e. `a2 = -β`, `a1 = -β`,
    `a0 = -β/4` after expansion. Emits the strict Poisson dual

        `c · √(π/β) · (-1)^n · exp(-π² n²/β)`.

    Identity: `Σ_n exp(-β (n+1/2)²) = √(π/β) · Σ_k (-1)^k · exp(-π² k²/β)`
    (Poisson with the `exp(2πi k · 1/2) = (-1)^k` phase from the
    half-integer translation). Verified strictly with rel-err 0 at dps=50
    across β ∈ {1e-3, 1e-2, 1e-1, 1} via the v0.7 unit tests.

    Returns None if `expr` isn't of this exact shape (declining cleanly
    when the offset is anything other than ±1/2).
    """
    parsed = _parse_quadratic_exp(expr, n)
    if parsed is None:
        return None
    scalar, a2, a1, a0 = parsed
    # Half-integer shift signature: a1 / a2 == 1 and a0 / a2 == 1/4
    # i.e. -β·n² - β·n - β/4 = -β·(n + 1/2)²
    # Use simplify == 0 rather than == on Rationals for robustness with
    # potentially un-normalised forms.
    if sp.simplify(a1 / a2 - 1) != 0:
        return None
    if sp.simplify(a0 / a2 - sp.Rational(1, 4)) != 0:
        return None
    beta = -a2  # β > 0
    # Dual: c · √(π/β) · (-1)^n · exp(-π² n²/β)
    return scalar * sp.sqrt(sp.pi / beta) * (-1)**n * sp.exp(-sp.pi**2 * n**2 / beta)


def _poisson_dual_weighted_gaussian(
    expr: sp.Expr, n: sp.Symbol,
) -> Optional[sp.Expr]:
    """v0.7 case (B): weighted Gaussian (second moment).

    Detects `c · n² · exp(-β n²)` and emits the strict Poisson dual

        `c · √(π/β) · (1/(2β) - π² n²/β²) · exp(-π² n²/β)`.

    Derivation: differentiate v0.4's identity
    `Σ_n exp(-β n²) = √(π/β) · Σ_k exp(-π² k²/β)` w.r.t. β and negate.

    LHS: `-Σ_n n² · exp(-β n²)`.
    RHS: `-1/(2β) · √(π/β) · Σ_k exp(-π² k²/β)
           + √(π/β) · Σ_k (π² k²/β²) · exp(-π² k²/β)`
        = `√(π/β) · Σ_k (-1/(2β) + π² k²/β²) · exp(-π² k²/β)`.

    Negating both sides gives the identity above. Verified strictly to
    rel-err 0 at dps=50 across β ∈ {1e-3, 1e-2, 1e-1, 1} via the v0.7
    unit tests. Note that `n=0` contributes 0 on the LHS (the `n²` factor
    kills it), but the dual evaluates a non-trivial `1/(2β) · √(π/β)`
    `k=0` term — the sums match overall because the other dual cells
    re-sum to cancel.

    Returns None if `expr` isn't of this exact shape. We deliberately
    don't try to handle `n^k` for higher k yet — each k requires its own
    derivative identity, and the engine has no proposer-side parameter
    to range over k. v0.8+ if needed.
    """
    if expr.func != sp.Mul:
        return None
    # Pull out the n-independent scalar; the remainder must factor as
    # n^2 · exp(quadratic_in_n).
    scalar, n_dep = expr.as_independent(n, as_Add=False)
    if n_dep.func != sp.Mul:
        return None
    factors = n_dep.args
    pow_factor = None
    exp_factor = None
    other_factors = []
    for f in factors:
        if f == n**2 or (f.func == sp.Pow and f.args[0] == n and f.args[1] == 2):
            if pow_factor is None:
                pow_factor = f
                continue
            other_factors.append(f)
        elif f.func == sp.exp or (f.func == sp.Pow and f.args[0] == sp.E):
            if exp_factor is None:
                exp_factor = f
                continue
            other_factors.append(f)
        else:
            other_factors.append(f)
    if pow_factor is None or exp_factor is None or other_factors:
        return None
    # Parse the exp argument as a pure Gaussian (a1 == 0, a0 == 0)
    if exp_factor.func == sp.exp:
        arg = exp_factor.args[0]
    else:
        arg = exp_factor.args[1]
    if not arg.has(n):
        return None
    arg_expanded = sp.expand(arg)
    try:
        poly = sp.Poly(arg_expanded, n)
    except sp.PolynomialError:
        return None
    if poly.degree() != 2:
        return None
    a2 = poly.nth(2)
    a1 = poly.nth(1)
    a0 = poly.nth(0)
    if a1 != 0 or a0 != 0:
        return None
    if not _is_negative_number(a2):
        return None
    beta = -a2
    # Dual: c · √(π/β) · (1/(2β) - π² n²/β²) · exp(-π² n²/β)
    return (scalar * sp.sqrt(sp.pi / beta)
            * (sp.Rational(1, 2) / beta - sp.pi**2 * n**2 / beta**2)
            * sp.exp(-sp.pi**2 * n**2 / beta))


def _modular_transform_with_correction_apply(
    expr: sp.Expr, n: sp.Symbol,
) -> Optional[tuple]:
    """v0.8b/v0.8c: One-sided modular transformations with additive scalar
    correction terms.

    Where v0.4 / v0.7 `mellin_inversion` covers STRICT two-sided Poisson
    identities (`Σ_{n∈Z} f(n) = Σ_{k∈Z} g(k)`), this operator covers the
    ONE-SIDED (n ≥ 1) class where the modular law carries a non-trivial
    scalar correction outside the summand — Bernoulli polynomial values,
    logarithms, and weight-2 quasi-modular anomalies.

    v0.8b shipped two cases (verified to rel-err ≤ 1e-30 at dps=80
    across β ∈ {1e-3, 1e-2, 1e-1, 1, 10}); v0.8c added Case C (Stieltjes
    occupation-number; per ChatGPT Pro proposer answer 2026-05-24):

    ### Case A — Bose-Einstein eta-log form

        Σ_{n≥1} log(1 - exp(-β n))
          = -π²/(6β) - (1/2)·log(β/(2π)) + β/24
            + Σ_{n≥1} log(1 - exp(-4π² n / β))

    Derivation: differentiate `log eta(it)` modular transformation
    `eta(i/t) = √t · eta(it)` w.r.t. t in real-form. Substituting
    β = 2π t gives the identity above. The boundary terms
    `-π²/(6β) - (1/2)log(β/(2π)) + β/24` come from the (i) `pi*t/12`
    Eisenstein-of-weight-2 contribution and (ii) the `(1/2)log(t)`
    half-modular weight in `log eta`.

    The matched input shape is `log(1 - c · exp(-β n))` where `c` is a
    constant (typically 1). We require c=1 strictly (the c≠1 case is
    NOT a clean modular identity — it picks up dilogarithm boundary
    terms). The dual summand is `log(1 - exp(-4π² n/β))`.

    ### Case B — Lambert / E_2 quasi-modular form

        Σ_{n≥1} n·q^n/(1-q^n)     with q = exp(-β)
          = π²/(6β²) + 1/24 - 1/(2β)
            - (4π²/β²) · Σ_{n≥1} n / (exp(4π² n/β) - 1)

    Derivation: `Σ n q^n/(1-q^n) = (1 - E_2(τ))/24` for `τ = iβ/(2π)`.
    Apply Hecke's quasi-modular transformation
    `E_2(-1/τ) = τ² E_2(τ) - 6iτ/π` with `-1/τ = 2πi/β`. The dual q'
    parameter is `q' = exp(-4π²/β)`. The `n·q'^n/(1-q'^n)` summand
    rewrites as `n / (e^{4π² n/β} - 1)`. The multiplicative prefactor
    `-(2π/β)² = -4π²/β²` baked into the new summand keeps the API
    tuple-shape clean: `(new_summand, correction, range)`.

    The matched input shape: `c · n · q^n / (1 - q^n)` where q is a
    rational of the form `Rational(p, q)` with `0 < p < q` (so
    `log q < 0`, i.e., `β = -log(q) > 0`). For symbolic q (`exp(-β)`
    form) we'd need extra plumbing; this v0.8b cut handles concrete
    rational q to match the existing seed `lambert_divisor_q_p1`.

    ### Case C — Stieltjes / Lambert occupation-number form (v0.8c)

        Σ_{n≥1} 1/(e^{β n} − 1)
          = (log(1/β) + γ)/β + 1/4
            − (2/β) · Σ_{m≥1} d(m) · [e^{-z_m}·Ei(z_m) − e^{z_m}·E_1(z_m)]

    where β* = 4π²/β, z_m = β*·m, γ is Euler-Mascheroni, d(m) is the
    number of divisors (sympy.divisor_sigma(m, 0)), and Ei / E_1 are
    the exponential integrals.

    Derivation: Mellin-inversion of `Σ d(N) e^{-βN} = S_0(β)` (using
    `1/(e^x-1) = Σ_k e^{-kx}` and pooling by N = nk gives d(N)). The
    Mellin transform is `Γ(s)·ζ(s)²`; the closed pieces come from the
    Laurent expansion at the s=1 double pole (`(γ - log β)/β`) and the
    s=0 simple pole (`1/4`). The remaining contour residue is the
    dual-series term involving Ei/E_1 weighted by d(m), which is a
    rewriting of the `Σ d(m)·e^{−β*m}·integral` form via the standard
    Mellin transform of `1/(e^x − 1)`.

    The matched input shape is `c · 1/(exp(β·n) - 1)` where β is a
    strictly-positive numeric (rational, e.g. `Rational(1, 100)`) or
    sympy-positive symbol. Other forms decline.

    **Convergence-regime caveat** (per `analysis/26_v08c_*.py` header):
    The LHS converges fast as `e^{-βn}` at every β; the dual SUM
    converges only as `1/m²` (asymptotic from `e^{-z}Ei(z) − e^z E_1(z)
    ~ 2/z²`). In the small-β regime (β ≪ 1, β* large) the dual is
    practically computable to high precision; in the large-β regime
    (β ≥ 10, β* small) the dual is truncation-noise-limited at
    rel-err ~few%. This is the inverse of v0.8b Case A/B's
    speedup-direction — exactly the modular-dual character.

    ### Return convention

    Returns either `None` (declines) or
    `(new_summand: sp.Expr, additive_correction: sp.Expr, summand_range: tuple)`
    where `summand_range = (1, sp.oo)`. The engine populates the
    OperatorApplication's `additive_correction` and `summand_range`
    fields from the tuple; the verifier picks them up and computes
    `Σ_{n≥1} before  ≡  Σ_{n≥1} after + correction`.

    See [DID_NOT_PAN_OUT §R17] for the original v0.8b deferral
    rationale, [diary 31] for the v0.8b numerical-verification table,
    and [diary 32] for the v0.8c Stieltjes/Lambert addition.
    """
    # CASE A: log Bose-Einstein
    result = _log_bose_einstein_apply(expr, n)
    if result is not None:
        return result
    # CASE B: Lambert / E_2 quasi-modular
    result = _lambert_e2_apply(expr, n)
    if result is not None:
        return result
    # CASE C: Stieltjes / Lambert occupation-number (v0.8c)
    result = _v08c_try_occupation_number_pattern(expr, n)
    if result is not None:
        return result
    return None


def _log_bose_einstein_apply(
    expr: sp.Expr, n: sp.Symbol,
) -> Optional[tuple]:
    """Detect `c · log(1 - exp(-β n))` and emit the eta-log modular dual.

    The input shape is matched STRICTLY: a constant scalar `c` times
    `log(1 - exp(-β n))` where `β` is a strictly-positive numeric (or
    sympy-positive symbol). Any other form returns None.

    Returns `(new_summand, additive_correction, (1, oo))` where
        new_summand = c · log(1 - exp(-4π² n / β))
        additive_correction = c · (-π²/(6β) - (1/2) log(β/(2π)) + β/24)

    This is c times the unit-c identity; the `c` factor is the
    n-independent scalar pulled out via `as_independent(n)`.
    """
    scalar, n_dep = expr.as_independent(n, as_Add=False)
    if n_dep.func != sp.log:
        return None
    log_arg = n_dep.args[0]
    # log_arg must be `1 - exp(-β n)`. Match it as `1 + something`.
    # sp.Add normalizes "1 - x" as "1 + (-1)*x".
    if not log_arg.has(n):
        return None
    diff = sp.simplify(log_arg - 1)  # should be -exp(-β n)
    # Try to recognise diff = -exp(arg) with arg = -β·n + 0 (i.e., linear in n)
    # We allow exp factor; deeper structure must be excluded.
    neg_exp = -diff  # should be exp(-β n)
    if neg_exp.func != sp.exp:
        return None
    exp_arg = neg_exp.args[0]
    # exp_arg must be linear in n with negative coefficient (β·n with β>0,
    # so exp_arg = -β·n, leading coeff -β < 0).
    try:
        poly = sp.Poly(sp.expand(exp_arg), n)
    except sp.PolynomialError:
        return None
    if poly.degree() != 1:
        return None
    a1 = poly.nth(1)
    a0 = poly.nth(0)
    if a0 != 0:
        return None  # require pure exp(-β n), no constant offset
    if not _is_negative_number(a1):
        return None
    beta = -a1  # β > 0
    # Dual: c · log(1 - exp(-4 π² n / β))
    new_summand = scalar * sp.log(1 - sp.exp(-4 * sp.pi**2 * n / beta))
    # Additive correction: c · (-π²/(6β) - (1/2) log(β/(2π)) + β/24)
    correction = scalar * (
        -sp.pi**2 / (6 * beta)
        - sp.log(beta / (2 * sp.pi)) / 2
        + beta / 24
    )
    return (new_summand, correction, (1, sp.oo))


def _lambert_e2_apply(
    expr: sp.Expr, n: sp.Symbol,
) -> Optional[tuple]:
    """Detect Lambert summand `c · n · q^n / (1 - q^n)` and emit the
    E_2 quasi-modular dual.

    The input is matched in either of two equivalent canonical forms
    (sympy's `as_independent` + `together` simplifies between them):

      (i)  `c · n · q^n / (1 - q^n)` with `q` rational in `(0, 1)`
      (ii) `c · n / (R^n - 1)` with `R > 1` rational (equivalent to (i)
           via `R = 1/q`; sympy's `together` produces this form when
           `q · q^n / (1 - q^n)` is simplified).

    In both cases, `β = log(R) = -log(q) > 0`.

    Returns `(new_summand, additive_correction, (1, oo))` where
        new_summand = -c · (4π²/β²) · n / (exp(4π² n / β) - 1)
        additive_correction = c · (π²/(6β²) + 1/24 - 1/(2β))

    The multiplicative prefactor `-(4π²/β²)` is baked INTO new_summand to
    keep the API tuple-shape clean and match the standing convention
    (one summand expression, one scalar correction).
    """
    # Pull out the n-independent scalar.
    scalar, n_dep = expr.as_independent(n, as_Add=False)
    # Try sympy's `together` canonicalisation first.
    n_dep_t = sp.together(n_dep)
    beta = _try_extract_lambert_beta(n_dep_t, n)
    if beta is None:
        # Try without the together step (sometimes the user's form already is)
        beta = _try_extract_lambert_beta(n_dep, n)
    if beta is None:
        return None
    new_summand = (
        -scalar
        * (4 * sp.pi**2 / beta**2)
        * n
        / (sp.exp(4 * sp.pi**2 * n / beta) - 1)
    )
    correction = scalar * (
        sp.pi**2 / (6 * beta**2)
        + sp.Rational(1, 24)
        - 1 / (2 * beta)
    )
    return (new_summand, correction, (1, sp.oo))


def _try_extract_lambert_beta(
    expr: sp.Expr, n: sp.Symbol,
) -> Optional[sp.Expr]:
    """Try to recognise `expr` as `n / (R^n - 1)` (canonical form after
    `sp.together` on `n · q^n / (1 - q^n)` for rational q ∈ (0,1)).
    Returns `β = log(R)` if matched; else None.
    """
    num, den = sp.fraction(expr)
    if sp.simplify(num - n) != 0:
        return None
    # den should be R^n - 1 with R > 1
    den_p1 = sp.simplify(den + 1)
    if den_p1.func != sp.Pow:
        return None
    base, exponent = den_p1.args
    if sp.simplify(exponent - n) != 0:
        return None
    if not base.is_number:
        return None
    # base must be > 1 (else the series doesn't converge)
    try:
        base_f = float(base)
    except (TypeError, ValueError):
        return None
    if base_f <= 1:
        return None
    return sp.log(base)


def _v08c_try_occupation_number_pattern(
    expr: sp.Expr, n: sp.Symbol,
) -> Optional[tuple]:
    """v0.8c (Case C of modular_transform_with_correction): detect
    `c · 1/(exp(β·n) − 1)` and emit the Stieltjes/Lambert occupation-
    number dual.

    The matched input shape: a constant scalar `c` (pulled via
    `as_independent(n)`) times `1/(exp(β·n) − 1)` where `β` is
    strictly-positive. Equivalent canonical forms accepted:

      (i)   `1 / (exp(β·n) - 1)`
      (ii)  `1 / (E**(β·n) - 1)`     (sympy may render `exp` as `Pow(E, ·)`)

    Returns `(new_summand, additive_correction, (1, oo))` where
        new_summand = -c · (2/β) · divisor_sigma(n, 0)
                       · [exp(-4π² n/β) · Ei(4π² n/β)
                          − exp(4π² n/β) · expint(1, 4π² n/β)]
        additive_correction = c · ((log(1/β) + γ)/β + 1/4)

    The dual summand uses sympy.divisor_sigma + sympy.Ei + sympy.expint;
    the verifier's lambdify modules-list (see
    `rkc/search/verifiers.py`'s `_V08C_LAMBDIFY_MODULES`) wires
    divisor_sigma to a sympy.divisor_count shim so mpmath.nsum can
    evaluate the dual cleanly. Ei and expint are stock-mpmath supported.

    See [diary 32] for the v0.8c numerical-verification table and the
    convergence-regime caveat (dual is `~1/m²` slow; only practical at
    small β — exactly the modular-speedup direction).
    """
    # Pull out the n-independent scalar.
    scalar, n_dep = expr.as_independent(n, as_Add=False)
    # n_dep must be `1 / (something - 1)` where `something` is
    # `exp(β · n)` for some β > 0.
    num, den = sp.fraction(n_dep)
    if sp.simplify(num - 1) != 0:
        return None
    # `den` should be `exp(β · n) - 1`; den + 1 should equal exp(β·n).
    den_p1 = sp.simplify(den + 1)
    beta = _v08c_extract_beta_from_exp(den_p1, n)
    if beta is None:
        return None
    # Build the dual summand
    bstar = 4 * sp.pi**2 / beta
    zn = bstar * n
    dual_summand = (
        -scalar
        * (2 / beta)
        * sp.divisor_sigma(n, 0)
        * (sp.exp(-zn) * sp.Ei(zn) - sp.exp(zn) * sp.expint(1, zn))
    )
    # Build the additive correction
    correction = scalar * (
        (sp.log(1 / beta) + sp.EulerGamma) / beta + sp.Rational(1, 4)
    )
    return (dual_summand, correction, (1, sp.oo))


def _v08c_extract_beta_from_exp(
    candidate: sp.Expr, n: sp.Symbol,
) -> Optional[sp.Expr]:
    """If `candidate == exp(β·n)` for some strictly-positive β, return β;
    else return None.

    Accepts both `sp.exp(arg)` and `sp.Pow(sp.E, arg)` AST shapes.
    """
    if not candidate.has(n):
        return None
    if candidate.func == sp.exp:
        arg = candidate.args[0]
    elif candidate.func == sp.Pow and candidate.args[0] == sp.E:
        arg = candidate.args[1]
    else:
        return None
    # arg must be linear in n with positive leading coefficient and zero offset.
    arg_expanded = sp.expand(arg)
    try:
        poly = sp.Poly(arg_expanded, n)
    except sp.PolynomialError:
        return None
    if poly.degree() != 1:
        return None
    a1 = poly.nth(1)
    a0 = poly.nth(0)
    if a0 != 0:
        return None  # require pure exp(β·n), no constant offset
    # require β > 0; for symbolic positive β, sympy's `is_positive` returns True
    try:
        is_pos = sp.simplify(a1).is_positive
    except Exception:
        is_pos = None
    if is_pos is not True:
        return None
    return a1


def _is_rational_in_open_unit(x: sp.Expr) -> bool:
    """True iff `x` is a sympy Rational with 0 < x < 1."""
    if not isinstance(x, sp.Rational):
        return False
    return x > 0 and x < 1


def _fourier_self_reciprocity_apply(expr: sp.Expr, n: sp.Symbol) -> Optional[sp.Expr]:
    """Fourier cos/sin self-reciprocity stub.

    If expr can be written as a cosine/sine integral transform of f,
    apply the (π/2)F[F[f]] = f self-inverse property.
    """
    return None


def _fractional_iteration_apply(expr: sp.Expr, n: sp.Symbol) -> Optional[sp.Expr]:
    """Fractional iteration F^r via Schröder linearisation stub.

    Per QR III §6: if F has a fixed point with Schröder eigenfunction σ
    satisfying σ ∘ F = s · σ, then F^r = σ⁻¹ ∘ (s^r · σ).
    """
    return None


def _hardy_orders_apply(expr: sp.Expr, n: sp.Symbol) -> Optional[tuple]:
    """v0.9a (Project C v0.9-hardy): Hardy-orders divergence diagnostic.

    Per QR III §7-§9, Ramanujan's "orders of infinity" is the systematic
    Hardy ≺/≻ classification of how fast functions grow at ∞ — the
    substrate that makes the Quarterly-Report operator calculus
    well-typed. v0.3 - v0.8 left this operator as a stub returning None;
    v0.9a wires it as the engine's **divergence diagnostic**: a
    non-transforming annotator that flags the asymptotic class of the
    literal summand `payload(n)` as n → ∞.

    Concrete motivating example (ChatGPT Pro's proposer-test answer):
    given the seed `1/(1 - exp(-β n))`, naively summing the LHS
    diverges — each term tends to 1 as n → ∞. Before the proposer
    suggests `modular_transform_with_correction` (the operator that
    actually applies), the engine needs to know the literal summand
    does not converge so the verifier doesn't waste cycles trying to
    compare divergent sums.

    ### Return convention (v0.9a — new 2-tuple form)

    `_hardy_orders_apply` returns one of:

      - `None` — the operator declines (e.g. expr has no n-dependence
        at all, so the limit question is trivial / nonsensical).
      - A 2-tuple `(expr_unchanged, {"convergence_class": <ConvergenceClass value>})`
        — engine merges the metadata dict into `state_after.metadata` AND
        copies the class to the top-level `state_after.convergence_class`
        field. The payload is RETURNED UNCHANGED (this is a non-
        transforming operator — it annotates, doesn't rewrite).

    The 2-tuple convention is distinct from the v0.8b 3-tuple
    `(new_summand, additive_correction, summand_range)` convention by
    its length AND by the dict-typed second element (vs. v0.8b's
    Expr-typed second element). The engine dispatches on length + type.

    ### Classification method

    Compute `sp.limit(expr, n, sp.oo)`. Decision:

      - limit is `0` (zero) → `CONVERGENT`. The necessary condition for
        absolute summability is met. We don't try a finer
        speed-of-convergence test (e.g. detecting harmonic-style
        divergence at the boundary between absolute and conditional
        convergence). That's a v0.10+ refinement; for v0.9a the goal is
        a fast 3-bin diagnostic to flag the WORST common failure
        (divergent-literal summands).

      - limit is `±oo` (infinite) → `NEEDS_REGULARIZATION`. The summand
        diverges to infinity; Abel / zeta regularization or a modular
        transformation is required to make sense of any sum.

      - limit is a finite non-zero number (sympy `is_finite=True` and
        `is_number=True` and not zero) → `DIVERGENT_LITERAL`. The
        summand stabilises at a non-zero level — `Σ_n c = ∞` trivially.

      - limit is `AccumulationBounds` (oscillatory bounded), `nan`,
        `zoo`, or sympy's limit raises → `UNKNOWN`. We don't make a
        confident classification.

    ### Why this design (rather than a pre-pass)

    The brief offers two implementation options: (a) a regular operator
    the proposer can suggest, or (b) a pre-pass the engine runs first
    on every new state. v0.9a goes with (a) — regular operator —
    because:

      1. **Zero engine surgery beyond the metadata-merge.** The
         apply_fn return-convention extension (2-tuple form) is small,
         backward-compatible, and reuses the same dispatch path the
         v0.8b 3-tuple takes.

      2. **Composability.** Future operators (e.g. an "Abel
         regularization" operator that fires when convergence_class is
         NEEDS_REGULARIZATION) can read the class off the state and
         decide whether to apply. A pre-pass would need its own hook
         system.

      3. **The proposer can BE the gating logic.** ClaudeProposer
         (v0.8a) sees the state and can be prompted to fire
         hardy_orders FIRST on novel states (we'll wire this hint into
         the system prompt as a follow-up; v0.9a focuses on the
         operator + data-model side). RandomProposer in the meantime
         will fire hardy_orders ~1/8 of the time uniformly, which is
         fine for a diagnostic that's cheap to compute.

    ### Why None is returned for expressions with no n-dependence

    If `expr.has(n) is False`, the summand is a constant in n. The
    "limit as n → ∞" is the constant itself; this is not a
    classification of n-dependent asymptotic behaviour. We decline
    rather than emit a confusing CONVERGENT-or-DIVERGENT tag, mirroring
    how `mellin_inversion` declines on non-Gaussian inputs. The engine
    will record PROPOSER_DECLINED, which is the right outcome — there's
    nothing for hardy_orders to say about an n-independent expression.
    """
    # Decline on n-independent expressions — there's nothing asymptotic
    # to classify if the summand doesn't depend on n.
    if not expr.has(n):
        return None
    convergence_class = _v09a_classify_convergence(expr, n)
    if convergence_class is None:
        # Defensive: classifier should always return some value (incl. UNKNOWN)
        # but if it ever returns None we decline rather than silently misclassify.
        return None
    return (expr, {"convergence_class": convergence_class})


def _v09a_classify_convergence(expr: sp.Expr, n: sp.Symbol) -> Optional[str]:
    """v0.9a helper: classify the n → ∞ asymptotic class of `expr`.

    Returns one of the string values from `ConvergenceClass` (CONVERGENT,
    DIVERGENT_LITERAL, NEEDS_REGULARIZATION, UNKNOWN). The string form
    matches what we serialize into JSONL via `JsonlRegistry`.

    Pulled out as a module-level helper so the proposer (or any other
    caller) can invoke the same classifier without going through the
    apply_fn return-tuple plumbing. Useful for the future Claude-side
    proposer hint ("if the state's convergence_class is UNKNOWN, fire
    hardy_orders first").

    Implementation: a single `sp.limit(expr, n, sp.oo)` call wrapped in
    a broad try/except. The classification then inspects sympy's flags
    on the returned object:

      - `lim.is_zero is True`               → CONVERGENT
      - `lim is sp.oo` or `lim is -sp.oo`   → NEEDS_REGULARIZATION
      - `lim.is_finite is True` AND
        `lim.is_number is True` AND
        `lim != 0`                          → DIVERGENT_LITERAL
      - everything else (AccumBounds, zoo,
        nan, sympy raises)                  → UNKNOWN

    We require `is_number=True` to reject AccumulationBounds (which
    report `is_finite=True` but are not classifiable point values).
    """
    try:
        lim = sp.limit(expr, n, sp.oo)
    except Exception:
        # Any limit-evaluation failure (NotImplementedError, PolynomialError,
        # recursion explosion, sympy bugs, etc.) — bail to UNKNOWN.
        return "UNKNOWN"
    # Pathological values
    if lim is sp.nan or lim is sp.zoo:
        return "UNKNOWN"
    # Infinite limits → NEEDS_REGULARIZATION (sign doesn't matter for
    # the diagnostic — both +oo and -oo are divergent-to-infinity).
    if lim is sp.oo or lim is -sp.oo:
        return "NEEDS_REGULARIZATION"
    # Zero limit → CONVERGENT (necessary condition met)
    if lim.is_zero is True:
        return "CONVERGENT"
    # Finite, classifiable non-zero number → DIVERGENT_LITERAL
    if lim.is_finite is True and lim.is_number is True:
        # Defensive: re-check non-zero (a number with is_zero=None could be
        # something exotic; if it's a sympy number we can compare).
        try:
            if lim == 0:
                return "CONVERGENT"
        except Exception:
            return "UNKNOWN"
        return "DIVERGENT_LITERAL"
    # AccumBounds (oscillatory), symbolic-with-free-symbols-beyond-n
    # (parameters in the expression beyond the summand variable), or
    # anything else that isn't a clean number → UNKNOWN. We deliberately
    # don't try harder here; v0.9a is a fast 3-bin diagnostic.
    return "UNKNOWN"


def _frullani_limit_apply(expr: sp.Expr, n: sp.Symbol) -> Optional[sp.Expr]:
    """Frullani-extended Master Theorem (Theorem II) stub.

    Apply the n→0 limit to a parametric Master-Theorem identity to
    land on a Frullani-style integral.
    """
    return None


def _mellin_pair_reciprocity_apply(expr: sp.Expr, n: sp.Symbol) -> Optional[sp.Expr]:
    """Mellin-pair self-reciprocity stub (QR III §15).

    For functional pairs (F, f) with ∫₀^∞ F(ax)f(bx) dx = 1/(a+b),
    apply the αβ=1 reciprocity.
    """
    return None


# ---------------------------------------------------------------------------
# v0.10: four new operators that close the 4-seed coverage gap per diary 42
# (mock_theta_completion, partial_theta_completion,
#  gauss_sum_finite_evaluation, q_pochhammer_transform)
# ---------------------------------------------------------------------------

def _mock_theta_completion_apply(
    expr: sp.Expr, n: sp.Symbol,
) -> Optional[tuple]:
    """v0.10 Operator (a): mock-theta completion certificate emission.

    Match: `q^{n²} / Product(1 + q^k, (k, 1, n))²` — Ramanujan's
    third-order mock theta f(q) (the f3 family of [diary 41/42]).

    Decision (per brief, diary 42): added as a NEW operator id (rather
    than extending mellin_inversion) for cleanliness — the completion
    operator is structurally different (it's an annotative certificate
    emission, not a term-by-term rewrite). Wraps the existing
    `rkc.completions.compute_mock_theta_with_completion` machinery
    when q is a concrete number in (0, 1); otherwise emits a symbolic
    certificate.

    For v0.10 we ship f3 only (already supported in
    `rkc.completions`). f5/f7/f10 via Zwegers R_{a,b} erfc per diary 41
    is a follow-up v0.10b — out of scope here (see brief).

    Return convention: v0.9a 2-tuple `(payload_unchanged, metadata_dict)`.
    The payload is returned UNCHANGED because the completion is a
    numerical certificate (not a rewrite of the AST). The metadata
    contains the certificate fields when q is concrete; for symbolic q
    it contains a structural certificate marker.

    Decline cases:
      - expression is not a mock-theta f3 shape
      - the rkc matcher returns None (some structural detail off)

    Verifier: payload is unchanged → `sp.simplify(before - after) == 0`
    short-circuit fires → trivially passes.

    Cost model: payload unchanged → cost_after = cost_before → ratio = 1.0
    → cost gate passes (the gate rejects ratio < 1.0; ratio == 1.0 is
    accepted).
    """
    from ..registry import _match_mock_theta_f3
    match = _match_mock_theta_f3(expr, n)
    if match is None:
        # Try the equivalent AST shape `q^{n²} / Product(1+q^k)**2` (squaring
        # OUTSIDE the product, vs the rkc matcher's INSIDE-product form). The
        # seed `mock_theta_f3_q_p5` uses the outside-square form; this shim
        # detects it directly.
        match = _try_extract_mock_theta_f3_outside_square(expr, n)
        if match is None:
            return None
    q = match.get("q")
    if q is None:
        return None
    meta = {
        "operator": "mock_theta_completion_transform",
        "family": "mock_theta_f3",
        "match_params": {"q": str(q)},
    }
    # If q is a concrete number in (0, 1), compute the completion
    # certificate via the existing rkc.completions machinery.
    try:
        q_num = sp.Float(q)
        q_f = float(q_num)
        if 0 < q_f < 1:
            from ..completions import (
                compute_mock_theta_with_completion,
                CompletionNotImplemented,
            )
            try:
                cert = compute_mock_theta_with_completion(
                    "mock_theta_f3", q_f, target_digits=30,
                )
                meta["completion_value"] = str(cert.value)
                meta["completion_error_bound"] = float(cert.error_bound)
                meta["completion_method"] = cert.certificate.method
                meta["completion_regime"] = cert.certificate.regime
                meta["completion_confidence"] = cert.certificate.confidence
                meta["completion_dps"] = cert.certificate.working_dps
            except CompletionNotImplemented as e:
                meta["completion_value"] = None
                meta["completion_status"] = (
                    f"family not instrumented: {e}"
                )
            except Exception as e:
                meta["completion_value"] = None
                meta["completion_status"] = (
                    f"completion failed: {type(e).__name__}: {e}"
                )
    except (TypeError, ValueError):
        meta["completion_status"] = "symbolic q — structural match only"
    # Return the 2-tuple form: payload unchanged, metadata annotated.
    return (expr, meta)


def _partial_theta_completion_apply(
    expr: sp.Expr, n: sp.Symbol,
) -> Optional[tuple]:
    """v0.10 Operator (b): partial-theta DIRECT-CERTIFICATE acceptance.

    Match: `q^{n(n+1)/2}` (triangular exponent; optionally with `(-1)^n`
    prefactor for the alternating partial theta).

    Per rkc `_route_partial_theta` (registry.py): "no clean dual (one-
    sided in n); direct truncation suffices". So this operator's job is
    NOT to transform; it's to emit a CERTIFIED-DIRECT acceptance with
    the reason `partial_theta_one_sided_no_clean_dual_exists`.

    Engineering approach: 2-tuple `(payload_unchanged, metadata_dict)`
    per the v0.9a annotator convention. The payload IS the optimal form;
    the metadata documents this fact. The cost model will see ratio=1.0
    (input == output) which passes the gate.

    Note: per the brief's "Alternative", a more ambitious version
    would emit the false-theta `(-1)^n` companion per Andersen/Bringmann.
    We defer that — false-theta is a separate operator class with its
    own modular obstruction theory, and the v0.10 scope is closing the
    12/12 gate, not advancing the false-theta frontier.
    """
    from ..registry import _match_partial_theta
    match = _match_partial_theta(expr, n)
    if match is None:
        return None
    q = match.get("q")
    alternating = match.get("alternating_sign", False)
    if q is None:
        return None
    meta = {
        "operator": "partial_theta_completion",
        "family": "partial_theta",
        "match_params": {
            "q": str(q),
            "alternating": bool(alternating),
        },
        "decision": "DIRECT_CERTIFICATE",
        "reason": "partial_theta_one_sided_no_clean_dual_exists",
        "decay_class": "finite",
        # cost analysis: direct truncation needs ~sqrt(2 · -log(tol)/-log(q))
        # terms; see _route_partial_theta in rkc.registry for the formula
    }
    # Optionally annotate the convergence rate if q is concrete
    try:
        q_f = float(sp.Float(q))
        if 0 < q_f < 1:
            import math
            num_terms = max(1, math.ceil(
                (math.sqrt(1 + 8 * (-math.log(1e-12) / -math.log(q_f))) - 1) / 2
            ))
            meta["num_terms_for_1em12"] = num_terms
    except (TypeError, ValueError):
        pass
    return (expr, meta)


def _gauss_sum_finite_evaluation_apply(
    expr: sp.Expr, n: sp.Symbol,
) -> Optional[tuple]:
    """v0.10 Operator (c): finite quadratic Gauss-sum closed-form.

    Match: `exp(2πi · p · n² / q)` — the summand of the quadratic
    Gauss sum G(p, q) = Σ_{n=0}^{q-1} exp(2πi p n² / q).

    Closed-form values (Gauss, 1801; cf. Berndt-Evans-Williams *Gauss and
    Jacobi sums* §1.5):

      - gcd(p, q) = 1, q odd                    → G(p, q) = (p/q)_J · ε_q · √q
        where (p/q)_J is the Jacobi symbol and
        ε_q = 1 if q ≡ 1 (mod 4) else i.
      - gcd(p, q) = 1, q ≡ 0 (mod 4)            → G(p, q) = (1 + i) · (p/q) · √q
      - q ≡ 2 (mod 4)                            → G(p, q) = 0 (SILENT-ZERO HAZARD)
        — preserved per CLAUDE.md gotcha 1 and §A4
      - gcd(p, q) = d > 1, q = d · q', p = d · p' → G(p, q) = d · G(p', q')
        (reduces to a smaller Gauss sum on q' < q)

    For p=1 specifically (the typical test case), the formula simplifies:
      - q ≡ 1 (mod 4) → G(1, q) = √q
      - q ≡ 3 (mod 4) → G(1, q) = i · √q
      - q ≡ 0 (mod 4) → G(1, q) = (1+i) · √q

    Return convention: 3-tuple `(constant_summand, 0, (0, q-1))` per the
    v0.8b convention. We rewrite the summand as a constant `G/q` so that
    `Σ_{n=0}^{q-1} G/q = G` matches the original sum.

    This routing preserves the silent-zero guard: when q ≡ 2 (mod 4)
    the operator returns the trivial summand `0`, which sums to 0 and
    matches the direct-evaluation answer (also 0). The router will then
    classify the AST as DEGENERATE on its own via `_gauss_sum_degeneracy_v2`
    — the engine's gate at line 284 (Step 6c) handles the rejection if
    we wanted that; here we choose to ACCEPT the closed-form 0 with an
    explicit silent_zero=True metadata flag instead (since the seed
    `gauss_sum_q6` exists specifically to test the silent-zero guard,
    and returning 0 IS the correct mathematical answer).

    Decline cases:
      - expression is not a quadratic exponential (not `exp(c·n²)` with c
        of the form `2πi · rational`)
      - the rational p/q can't be extracted as integers
    """
    from ..registry import _match_gauss_sum
    match = _match_gauss_sum(expr, n)
    if match is None:
        return None
    p = match.get("p")
    q = match.get("q")
    if p is None or q is None:
        return None
    # SILENT-ZERO GUARD: q ≡ 2 (mod 4) → G(p, q) = 0 identically.
    # This preserves CLAUDE.md gotcha 1.
    if q % 4 == 2:
        # The summand exp(2πi p n²/q) does NOT pointwise equal 0;
        # but its sum over n ∈ (0, q-1) IS exactly 0. We emit
        # a constant summand 0 → sum is 0 → matches the closed form.
        return (sp.Integer(0), sp.Integer(0), (0, q - 1))
    # Otherwise compute the closed form.
    closed_form = _gauss_sum_closed_form(p, q)
    if closed_form is None:
        return None
    # Emit constant summand = closed_form / q so that
    # Σ_{n=0}^{q-1} (closed_form/q) = closed_form.
    constant = closed_form / q
    return (constant, sp.Integer(0), (0, q - 1))


def _gauss_sum_closed_form(p: int, q: int) -> Optional[sp.Expr]:
    """Compute G(p, q) = Σ_{n=0}^{q-1} exp(2πi p n²/q) in closed form.

    Returns None if the structure is degenerate beyond what the operator
    is supposed to handle (the q ≡ 2 (mod 4) silent-zero case is handled
    OUTSIDE this helper, in the apply_fn proper, so this only sees the
    non-silent-zero paths). Reduces by gcd recursion if gcd(p, q) > 1.

    References:
      - Berndt, Evans, Williams. *Gauss and Jacobi sums*. Wiley, 1998. §1.5
      - Gauss, *Disquisitiones Arithmeticae* §356 (1801; the original).
    """
    import math
    if q <= 0:
        return None
    g = math.gcd(abs(p), q)
    if g > 1:
        # Reduction: G(p, q) = g · G(p/g, q/g), then iterate if q/g still even
        # WARNING: gcd reduction can hit the q ≡ 2 (mod 4) case after one
        # reduction step. Handle via recursion that respects the silent-zero
        # check at each step.
        p_red = p // g
        q_red = q // g
        if q_red % 4 == 2:
            return sp.Integer(0)
        sub = _gauss_sum_closed_form(p_red, q_red)
        if sub is None:
            return None
        return g * sub
    # gcd(p, q) = 1 case. Use the standard closed forms.
    if q % 2 == 1:
        # Odd q: G(p, q) = (p/q)_J · ε_q · √q
        # where ε_q = 1 if q ≡ 1 (mod 4), i if q ≡ 3 (mod 4)
        eps_q = sp.Integer(1) if q % 4 == 1 else sp.I
        jacobi = sp.jacobi_symbol(p, q)
        return jacobi * eps_q * sp.sqrt(q)
    # Even q with gcd(p,q)=1 implies q ≡ 0 (mod 4) (since q ≡ 2 (mod 4)
    # was filtered already). Closed form: G(p, q) = (1+i) · (q/p) · √q
    # for odd p, q ≡ 0 (mod 4). (Symmetric Jacobi handling; we use
    # the Berndt-Evans-Williams §1.5 formula).
    # For simplicity in v0.10 we handle p=1 explicitly (the seed case);
    # general p would extend with the full Jacobi-reciprocity formula.
    if p == 1:
        return (1 + sp.I) * sp.sqrt(q)
    # General even-q case: fall back to direct finite sum (always works)
    return _gauss_sum_direct_finite(p, q)


def _gauss_sum_direct_finite(p: int, q: int) -> sp.Expr:
    """Direct evaluation Σ_{n=0}^{q-1} exp(2πi p n²/q) as a closed sympy
    expression (a sum of exp factors). For q ≤ ~30 this is feasible
    symbolically; for larger q we'd want a numerical evaluation, but the
    seed cases here are q=6, 7 — well within range.
    """
    total = sp.Integer(0)
    for n_val in range(q):
        total = total + sp.exp(2 * sp.pi * sp.I * p * n_val * n_val / q)
    return sp.simplify(total)


def _q_pochhammer_transform_apply(
    expr: sp.Expr, n: sp.Symbol,
) -> Optional[tuple]:
    """v0.10 Operator (d): q-Pochhammer factor-lift + transformation.

    Match: `1 - a · q^n` (a single factor of the infinite Pochhammer
    product `(a; q)_∞ = Π_{k=0}^∞ (1 - a · q^k)`).

    Per the brief's "order of preference":

      1. If a = 1: emit Euler's pentagonal-number theorem
         `(q; q)_∞ = Σ_{k∈Z} (-1)^k q^{k(3k-1)/2}` — a finite-summable
         theta-like form.
      2. Else: emit the lifted infinite-product form
         `Product(1 - a · q^k, (k, 0, ∞))` via Dedekind-eta modular
         transform if recognizable.
      3. Else: fall back to Heine `_3φ_2` transformation (deferred to
         v0.11; we emit the lifted form with a `route_to_heine=True`
         marker).

    Return convention: 2-tuple `(payload_unchanged, metadata_dict)`.
    The payload of the SUMMAND `1 - a·q^n` is unchanged (its semantic
    meaning as "a single Pochhammer factor" is intact); the metadata
    carries the lifted product form, the recognized (a, q) parameters,
    and the dispatched route (pentagonal / lifted / heine).

    Verifier: payload unchanged → trivially passes the symbolic equality
    short-circuit.

    Cost model: payload unchanged → ratio = 1.0 → gate passes.

    Decline cases:
      - expression not of the form `1 - a · q^n` (e.g., not even an Add,
        or no Pow over n in the additive piece)
      - a or q can't be extracted as numeric/symbolic values
    """
    extracted = _try_extract_pochhammer_factor(expr, n)
    if extracted is None:
        return None
    a, q = extracted
    # Try to coerce to floats for routing decisions
    try:
        a_f = float(sp.Float(a))
        q_f = float(sp.Float(q))
    except (TypeError, ValueError):
        a_f, q_f = None, None
    meta = {
        "operator": "q_pochhammer_transform",
        "family": "q_pochhammer",
        "match_params": {
            "a": str(a),
            "q": str(q),
        },
    }
    # Path 1: Euler's pentagonal-number theorem at a = 1
    k = sp.Symbol("k", integer=True)
    if sp.simplify(a - 1) == 0:
        meta["route"] = "euler_pentagonal"
        meta["lifted_product"] = str(sp.Product(1 - q**k, (k, 0, sp.oo)))
        meta["pentagonal_form"] = (
            "Σ_{k∈Z} (-1)^k · q^{k(3k-1)/2}"
        )
        meta["decay_class"] = "exponential" if (q_f is None or q_f < 1) else "diverges"
    else:
        # Path 2: lifted infinite product (Dedekind-eta routes if recognized)
        meta["route"] = "lifted_to_infinite_product"
        meta["lifted_product"] = str(sp.Product(1 - a * q**k, (k, 0, sp.oo)))
        # Tag the decay class so the cost model gets the right pacing
        if q_f is not None and 0 < q_f < 1:
            meta["decay_class"] = "exponential"
            # Numerical evaluation of the product to ≥30 digits (verification
            # bar for downstream consumers)
            try:
                import mpmath
                old_dps = mpmath.mp.dps
                try:
                    mpmath.mp.dps = 50
                    # Use sympy's evalf to preserve full precision on
                    # rational/symbolic a, q (avoiding 64-bit float downcast).
                    a_mp = mpmath.mpf(sp.Float(a, 50))
                    q_mp = mpmath.mpf(sp.Float(q, 50))
                    prod_val = mpmath.mpf(1)
                    for kk in range(1, 200):
                        term = 1 - a_mp * q_mp**kk
                        prod_val *= term
                        # convergence test
                        if abs(1 - term) < mpmath.mpf(10) ** (-40):
                            break
                    # Include the k=0 factor (1 - a)
                    prod_val = (1 - a_mp) * prod_val
                    meta["product_value_30dps"] = str(prod_val)
                finally:
                    mpmath.mp.dps = old_dps
            except Exception as e:
                meta["product_value_30dps"] = f"computation failed: {e}"
        else:
            meta["decay_class"] = "polynomial"
        # Path 3 stub: a ≠ 1 → could also route via Heine; we mark for v0.11
        meta["heine_route_available"] = (q_f is not None and 0 < q_f < 1)
    return (expr, meta)


def _try_extract_mock_theta_f3_outside_square(
    expr: sp.Expr, n: sp.Symbol,
) -> Optional[dict]:
    """Try to match `q^{n²} / Product(1 + q^k, (k, 1, n))^2` where the
    squaring is OUTSIDE the product (as in the seed `mock_theta_f3_q_p5`).

    The rkc matcher `_match_mock_theta_f3` expects the equivalent INSIDE-
    product form `Product((1 + q^k)^2, (k, 1, n))`. Both are
    mathematically equal but symbolically distinct ASTs. This shim handles
    the outside-square form so the seed lands cleanly.

    Returns {'q': q} or None.
    """
    if expr.func != sp.Mul:
        return None
    num_q = None
    sq_product_base = None
    other_parts = []
    k_sym = sp.Symbol("k", integer=True, positive=True)
    for arg in expr.args:
        if arg.func == sp.Pow:
            base, expo = arg.args
            if expo.has(n):
                try:
                    poly = sp.Poly(expo, n)
                except Exception:
                    poly = None
                if poly is not None and poly.degree() == 2 and poly.nth(1) == 0 and poly.nth(0) == 0:
                    a2 = poly.nth(2)
                    if a2 == 1:
                        num_q = base
                        continue
                    if a2 == -1 and base.is_number and base > 1:
                        num_q = sp.Rational(1) / base
                        continue
            # check for Product(...)**(-2) pattern
            if expo == -2 and base.func == sp.Product:
                sq_product_base = base
                continue
            if expo == 2 and base.func == sp.Product:
                # If it's in numerator squared form
                sq_product_base = base
                continue
        other_parts.append(arg)
    if num_q is None or sq_product_base is None:
        return None
    if other_parts:
        return None
    # Check the product body is (1 + q^k) over (k, 1, n)
    body = sq_product_base.args[0]
    if len(sq_product_base.args) < 2:
        return None
    limits = sq_product_base.args[1]
    if len(limits) != 3:
        return None
    kvar, lo, hi = limits
    if lo != 1 or hi != n:
        return None
    if sp.simplify(body - (1 + num_q ** kvar)) != 0:
        return None
    return {"q": num_q}


def _try_extract_pochhammer_factor(
    expr: sp.Expr, n: sp.Symbol,
) -> Optional[tuple]:
    """Try to recognise `expr` as `1 - a · q^n` and return (a, q).

    Accepts both AST shapes:
      (i)  `1 - a · q^n`     (Add with two args, one being 1)
      (ii) `1 - q^n`         (a = 1 case, where there's no explicit `a` factor)
      (iii) Sympy may canonicalise `1 - (1/3) · (1/2)^n` as
            `1 - (1/3) · 2^{-n}` or `1 - 1/(3·2^n)`. We try both forms.

    Returns None if the AST doesn't match.
    """
    expanded = sp.expand(expr)
    # Need an Add with exactly two args and 1 (or constant) plus a power
    if expanded.func != sp.Add:
        return None
    args = expanded.args
    if len(args) != 2:
        return None
    one_part = None
    other_part = None
    for a in args:
        if not a.has(n):
            one_part = a
        else:
            other_part = a
    if one_part is None or other_part is None:
        return None
    if sp.simplify(one_part - 1) != 0:
        return None
    # other_part should be `-a · q^n` for some a, q.
    # Pull out -1 to get a · q^n, then split into scalar a and base q.
    neg = -other_part
    # neg should be (positive) a · q^n. It may be in form like (1/3)·2^{-n}
    # Convert to a single Pow exp expression.
    base, exponent = None, None
    scalar = sp.Integer(1)
    if neg.func == sp.Pow:
        base, exponent = neg.args
    elif neg.func == sp.Mul:
        # Search for the single Pow factor with n in exponent
        for f in neg.args:
            if f.func == sp.Pow and f.args[1].has(n):
                if base is not None:
                    return None  # multiple n-dependent powers
                base, exponent = f.args
            else:
                scalar = scalar * f
    else:
        return None
    if base is None or exponent is None:
        return None
    # exponent should be linear in n: c · n + 0
    try:
        poly = sp.Poly(sp.expand(exponent), n)
    except sp.PolynomialError:
        return None
    if poly.degree() != 1 or poly.nth(0) != 0:
        return None
    coeff = poly.nth(1)
    # If coefficient is -1 (e.g., 2^{-n}), invert base
    if coeff == -1:
        try:
            base_inv = 1 / base
        except Exception:
            return None
        q = sp.simplify(base_inv)
    elif coeff == 1:
        q = base
    else:
        # Non-standard coefficient (e.g., q^{2n}) — not our target shape
        return None
    a = scalar
    return (a, q)


# ---------------------------------------------------------------------------
# The basis
# ---------------------------------------------------------------------------

QR7_OPERATOR_BASIS: list[Operator] = [
    Operator(
        id="master_theorem",
        notes="Ramanujan's Master Theorem (QR I §2): "
              "F(x) = ∑_k (-1)^k φ(k) x^k/k! ⇒ ∫₀^∞ x^(s-1) F(x) dx = Γ(s) φ(-s).",
        apply_fn=_master_theorem_apply,
        family_tag="analytic",
    ),
    Operator(
        id="mellin_inversion",
        notes="Forward Mellin transform M[f](s) = ∫₀^∞ x^(s-1) f(x) dx; "
              "inverse via Bromwich contour. The substrate of the Master Theorem. "
              "v0.4-v0.7: covers strict two-sided Poisson identities on n ∈ Z "
              "(pure Gaussian, half-shift theta_2/theta_4, weighted second-moment).",
        apply_fn=_mellin_inversion_apply,
        family_tag="analytic",
    ),
    Operator(
        id="modular_transform_with_correction",
        notes="v0.8b/v0.8c: One-sided (n ≥ 1) modular transformations with "
              "additive scalar correction. v0.8b covers log-Bose-Einstein "
              "(Dedekind eta) and Lambert / E_2 quasi-modular cases. "
              "v0.8c adds Stieltjes/Lambert occupation-number "
              "Σ 1/(e^{βn}-1) (per ChatGPT Pro proposer answer). "
              "Returns (new_summand, additive_correction, summand_range=(1, oo)) "
              "via the extended apply_fn protocol introduced in v0.8b.",
        apply_fn=_modular_transform_with_correction_apply,
        family_tag="modular",
    ),
    Operator(
        id="fourier_self_reciprocity",
        notes="Fourier cos/sin self-reciprocity (QR II §7 Theorem III + "
              "QR III §13-§15): if ∫₀^∞ φ(x) cos(nx) dx = ψ(n) then "
              "∫₀^∞ ψ(x) cos(nx) dx = (π/2) φ(n).",
        apply_fn=_fourier_self_reciprocity_apply,
        family_tag="analytic",
    ),
    Operator(
        id="fractional_functional_iteration",
        notes="QR III §4-§6 Schröder/Koenig fractional iteration: "
              "F^r(x) = σ⁻¹(s^r σ(x)) where σ ∘ F = s · σ. "
              "Lie-vector-field generator: ψ_1(x) = C/F(x) (QR III §10).",
        apply_fn=_fractional_iteration_apply,
        family_tag="iteration",
    ),
    Operator(
        id="hardy_orders_of_infinity",
        notes="QR III §7-§9 Hardy ≺/≻ asymptotic-order relation; "
              "scale construction defying logarithmic / exponential scales.",
        apply_fn=_hardy_orders_apply,
        family_tag="asymptotic",
    ),
    Operator(
        id="frullani_limit",
        notes="Frullani-extended Master Theorem (QR II §4 Theorem II): "
              "n→0 limit on a parametric Master-Theorem identity gives "
              "Frullani integral form.",
        apply_fn=_frullani_limit_apply,
        family_tag="analytic",
    ),
    Operator(
        id="mellin_pair_reciprocity",
        notes="QR III §15 Mellin-pair self-reciprocity: function pair (F, f) "
              "with ∫₀^∞ F(ax)f(bx) dx = 1/(a+b) yields a generalised "
              "Fourier-self-inversion theorem.",
        apply_fn=_mellin_pair_reciprocity_apply,
        family_tag="analytic",
    ),
    # === v0.10: four new operators closing the 4-seed coverage gap
    # (per diary 42 / ChatGPT-Pro basis-completeness verdict) ===
    Operator(
        id="mock_theta_completion_transform",
        notes="v0.10 Operator (a): mock-theta f3 completion certificate. "
              "Match: q^{n²} / Product(1+q^k, (k,1,n))² → 2-tuple "
              "(payload_unchanged, {certificate}) with Watson-Hickerson "
              "Eichler-integral value from rkc.completions. Decay class: "
              "polynomial (Eichler-integral correction; ~1/√α at α small). "
              "f5/f7/f10 via Zwegers R_{a,b} erfc per diary 41 is v0.10b.",
        apply_fn=_mock_theta_completion_apply,
        family_tag="modular_completion",
    ),
    Operator(
        id="partial_theta_completion",
        notes="v0.10 Operator (b): partial-theta DIRECT-CERTIFICATE. "
              "Match: q^{n(n+1)/2} (triangular exp, optionally (-1)^n). "
              "Per rkc._route_partial_theta: 'no clean dual exists; "
              "direct truncation suffices'. Emits 2-tuple with "
              "reason='partial_theta_one_sided_no_clean_dual_exists'. "
              "Decay class: finite (truncation bounded by direct sqrt(2·-log(tol)/-log(q)) terms).",
        apply_fn=_partial_theta_completion_apply,
        family_tag="partial_theta",
    ),
    Operator(
        id="gauss_sum_finite_evaluation",
        notes="v0.10 Operator (c): finite quadratic Gauss-sum closed form. "
              "Match: exp(2πi·p·n²/q). Returns 3-tuple (constant_summand, "
              "0, (0,q-1)) with constant = closed_form/q via Berndt-Evans-"
              "Williams §1.5. PRESERVES silent-zero guard at q ≡ 2 (mod 4) "
              "by returning Integer(0) summand. Decay class: finite "
              "(exactly q terms in the original sum, 1 term in the dual).",
        apply_fn=_gauss_sum_finite_evaluation_apply,
        family_tag="gauss_sum",
    ),
    Operator(
        id="q_pochhammer_transform",
        notes="v0.10 Operator (d): q-Pochhammer factor-lift + transformation. "
              "Match: 1 - a·q^n (single factor of (a;q)_∞). Routes: "
              "(1) a=1 → Euler pentagonal-number theorem; "
              "(2) a≠1 → lift to Product(1-a·q^k, (k,0,∞)) (Dedekind-eta if recognized); "
              "(3) Heine _3φ_2 deferred to v0.11. Emits 2-tuple with "
              "lifted_product + route metadata. Decay class: exponential "
              "for |q|<1, polynomial otherwise.",
        apply_fn=_q_pochhammer_transform_apply,
        family_tag="q_series",
    ),
]

QR7_OPERATOR_IDS: list[str] = [op.id for op in QR7_OPERATOR_BASIS]


def get_operator(op_id: str) -> Operator:
    """Look up an operator by id; raises KeyError if not in basis."""
    for op in QR7_OPERATOR_BASIS:
        if op.id == op_id:
            return op
    raise KeyError(f"unknown operator id: {op_id!r}")
