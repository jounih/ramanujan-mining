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
              "inverse via Bromwich contour. The substrate of the Master Theorem.",
        apply_fn=_mellin_inversion_apply,
        family_tag="analytic",
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
