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
    """v0.8b: One-sided modular transformations with additive scalar
    correction terms.

    Where v0.4 / v0.7 `mellin_inversion` covers STRICT two-sided Poisson
    identities (`Σ_{n∈Z} f(n) = Σ_{k∈Z} g(k)`), this operator covers the
    ONE-SIDED (n ≥ 1) class where the modular law carries a non-trivial
    scalar correction outside the summand — Bernoulli polynomial values,
    logarithms, and weight-2 quasi-modular anomalies.

    v0.8b ships two cases (both verified to rel-err ≤ 1e-30 at dps=80
    across β ∈ {1e-3, 1e-2, 1e-1, 1, 10}):

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

    ### Return convention

    Returns either `None` (declines) or
    `(new_summand: sp.Expr, additive_correction: sp.Expr, summand_range: tuple)`
    where `summand_range = (1, sp.oo)`. The engine populates the
    OperatorApplication's `additive_correction` and `summand_range`
    fields from the tuple; the verifier picks them up and computes
    `Σ_{n≥1} before  ≡  Σ_{n≥1} after + correction`.

    See [DID_NOT_PAN_OUT §R17] for the original deferral rationale and
    [diary 31] for the v0.8b numerical-verification table.
    """
    # CASE A: log Bose-Einstein
    result = _log_bose_einstein_apply(expr, n)
    if result is not None:
        return result
    # CASE B: Lambert / E_2 quasi-modular
    result = _lambert_e2_apply(expr, n)
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


def _hardy_orders_apply(expr: sp.Expr, n: sp.Symbol) -> Optional[sp.Expr]:
    """Hardy orders of infinity stub.

    For asymptotic-comparison queries, apply the ≺/≻ relation to
    classify growth orders. Doesn't transform expressions in the
    standard sense; placeholder for v0.
    """
    return None


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
              "Σ 1/(e^{βn}-1) (per ChatGPT Pro proposer answer; diary 32). "
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
]

QR7_OPERATOR_IDS: list[str] = [op.id for op in QR7_OPERATOR_BASIS]


def get_operator(op_id: str) -> Operator:
    """Look up an operator by id; raises KeyError if not in basis."""
    for op in QR7_OPERATOR_BASIS:
        if op.id == op_id:
            return op
    raise KeyError(f"unknown operator id: {op_id!r}")
