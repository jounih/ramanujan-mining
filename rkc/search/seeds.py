"""rkc.search.seeds — curated seed-expression library for Project C sweeps.

Each entry is a starting expression for `rkc.search.search()` to operate on.
Seeds are organized by kernel family + parameter regime so the sweep can
target specific operator-rediscovery cases.

The library is the input to the v0.6+ parallel sweep harness
(`rkc.search.sweep`) and is the operational embodiment of the
PROJECT_C_DESIGN.md controlled-validation case: at v0.7+ the engine
should recover ≥80% of the known rkc-registry identities by random
composition on the seeds below within budget=1000, max_depth ≤ 3.

Per-seed schema:
    id              : stable string identifier
    description     : short human-readable description
    expr_string     : python source for the sympy expression
                      (lambdified in build_seed() against the symbol set)
    var             : iteration variable name (default 'n')
    extra_symbols   : list of (symbol_name, assumptions_dict) tuples for
                      symbols beyond `var` that the expression uses
    kind            : 'summand' (default; Σ over var) or 'integral' (an
                      sp.Integral over var)
    expected_route  : the rkc route we expect to find via operator search
                      (for benchmark reporting; informational only)
    notes           : longer description of why this seed is included
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import sympy as sp


@dataclass
class Seed:
    id: str
    description: str
    expr_string: str
    var: str = "n"
    extra_symbols: list[tuple[str, dict[str, Any]]] = field(default_factory=list)
    kind: str = "summand"
    expected_route: str = "?"
    notes: str = ""


# ---------------------------------------------------------------------------
# The library (v0.6 starter set — 20 seeds across 6 kernel families)
# ---------------------------------------------------------------------------

SEED_LIBRARY: dict[str, Seed] = {

    # === Gaussian / theta-like (4 seeds across β regimes) ===
    "gaussian_beta_1em1": Seed(
        id="gaussian_beta_1em1",
        description="Gaussian Σ exp(-β n²) at β=1/10",
        expr_string="exp(-Rational(1, 10) * n**2)",
        kind="summand",
        expected_route="mellin_inversion → Poisson dual (~18x speedup)",
        notes="Mild β; dual is faster but margin smaller than at extreme small β",
    ),
    "gaussian_beta_1em2": Seed(
        id="gaussian_beta_1em2",
        description="Gaussian Σ exp(-β n²) at β=1/100",
        expr_string="exp(-Rational(1, 100) * n**2)",
        kind="summand",
        expected_route="mellin_inversion → Poisson dual (~54x speedup)",
        notes="Canonical v0.4 test case",
    ),
    "gaussian_beta_1em4": Seed(
        id="gaussian_beta_1em4",
        description="Gaussian Σ exp(-β n²) at β=1/10000",
        expr_string="exp(-Rational(1, 10000) * n**2)",
        kind="summand",
        expected_route="mellin_inversion → Poisson dual (~530x speedup)",
        notes="Extreme small β; dual is dramatically faster",
    ),
    "gaussian_beta_5": Seed(
        id="gaussian_beta_5",
        description="Gaussian Σ exp(-β n²) at β=5 (anti-test)",
        expr_string="exp(-5 * n**2)",
        kind="summand",
        expected_route="DIRECT preferred (mellin_inversion should NOT win)",
        notes="Large β; direct sum converges faster than the Poisson dual. Tests cost-model honesty",
    ),

    # === Master Theorem integral patterns (3 seeds, v0.5 territory) ===
    "beta_function_integral": Seed(
        id="beta_function_integral",
        description="Beta function: ∫₀^¹ x^(m-1) (1-x)^(n-1) dx",
        expr_string="Integral(x**(m-1) * (1-x)**(n-1), (x, 0, 1))",
        var="x",
        extra_symbols=[("m", {"positive": True}), ("n", {"positive": True})],
        kind="integral",
        expected_route="master_theorem → Γ(m)Γ(n)/Γ(m+n) (~100x)",
        notes="QR I §5(ii); canonical v0.5 test case",
    ),
    "gamma_function_integral": Seed(
        id="gamma_function_integral",
        description="Gamma function: ∫₀^∞ x^(s-1) exp(-x) dx",
        expr_string="Integral(x**(s-1) * exp(-x), (x, 0, oo))",
        var="x",
        extra_symbols=[("s", {"positive": True})],
        kind="integral",
        expected_route="master_theorem → Γ(s) (~100x)",
        notes="Eulerian integral; foundation of Ramanujan's QR I",
    ),
    "inv_1plus_x_integral": Seed(
        id="inv_1plus_x_integral",
        description="∫₀^∞ x^(s-1)/(1+x) dx",
        expr_string="Integral(x**(s-1) / (1+x), (x, 0, oo))",
        var="x",
        extra_symbols=[("s", {"positive": True})],
        kind="integral",
        expected_route="master_theorem → π/sin(πs) (~100x)",
        notes="QR I §5(i) reflection-like identity",
    ),

    # === Bose-Einstein partition (summand factor; v0.6+ target) ===
    "bose_einstein_beta_1em2": Seed(
        id="bose_einstein_beta_1em2",
        description="Bose factor 1/(1-exp(-βn)) at β=1/100",
        expr_string="1 / (1 - exp(-Rational(1, 100) * n))",
        kind="summand",
        expected_route="(v0.7+) mellin_inversion → Dedekind-eta dual",
        notes="Σ -log(1-q^n) → log of partition function; rkc DUAL route via η-modular",
    ),

    # === Lambert / divisor sum (summand; v0.6+ target) ===
    "lambert_divisor_q_p1": Seed(
        id="lambert_divisor_q_p1",
        description="Lambert summand n·q^n/(1-q^n) at q=1/10",
        expr_string="n * Rational(1, 10)**n / (1 - Rational(1, 10)**n)",
        kind="summand",
        expected_route="(v0.7+) mellin_inversion → Eisenstein-series dual",
        notes="Σ generates σ_1(k)·q^k; Eisenstein E_2 closed form",
    ),

    # === Mock theta f3 (summand; v0.7+ target with MCR completion) ===
    "mock_theta_f3_q_p5": Seed(
        id="mock_theta_f3_q_p5",
        description="Mock theta f(q) summand at q=1/2",
        expr_string="Rational(1, 2)**(n**2) / Product(1 + Rational(1, 2)**k, (k, 1, n))**2",
        kind="summand",
        expected_route="MODULAR_COMPLETION_REQUIRED (Watson-Hickerson)",
        notes="Per CANDIDATE_INSIGHTS §B; cohomological-irreducibility test case",
    ),

    # === Partial theta (summand; v0.7+) ===
    "partial_theta_q_p3": Seed(
        id="partial_theta_q_p3",
        description="Partial theta Σ_{n≥0} q^(n(n+1)/2) at q=1/3",
        expr_string="Rational(1, 3)**(n*(n+1)/2)",
        kind="summand",
        expected_route="DIRECT (no clean dual; one-sided)",
        notes="Tests the one-sided summation regime; expected DIRECT route only",
    ),

    # === Gauss sums (degeneracy detector test) ===
    "gauss_sum_q7": Seed(
        id="gauss_sum_q7",
        description="Gauss sum exp(2πi n²/q) at q=7 (safe)",
        expr_string="exp(2*pi*I * n**2 / 7)",
        kind="summand",
        expected_route="DIRECT (finite sum length 7)",
        notes="q=7 ≢ 2 (mod 4); no silent-zero hazard; should accept DIRECT route",
    ),
    "gauss_sum_q6": Seed(
        id="gauss_sum_q6",
        description="Gauss sum exp(2πi n²/q) at q=6 (DEGENERATE)",
        expr_string="exp(2*pi*I * n**2 / 6)",
        kind="summand",
        expected_route="DEGENERATE (silent-zero hazard at q ≡ 2 mod 4)",
        notes="§A4 silent-zero test; should refuse via degeneracy detector",
    ),

    # === q-Pochhammer (summand factor) ===
    "q_pochhammer_inf_p3": Seed(
        id="q_pochhammer_inf_p3",
        description="Single factor of (a;q)_∞ at a=1/3, q=1/2",
        expr_string="1 - Rational(1, 3) * Rational(1, 2)**n",
        kind="summand",
        expected_route="(future) q-shift / Heine transformation",
        notes="Factor of a q-Pochhammer; v0.8+ q_shift target",
    ),

    # === Composite test (multi-route, v0.6+ multi-step composition) ===
    "composite_gauss_x_lambert": Seed(
        id="composite_gauss_x_lambert",
        description="Composite: gaussian × Lambert factor",
        expr_string="exp(-Rational(1, 100) * n**2) * n / (1 - Rational(1, 10)**n)",
        kind="summand",
        expected_route="recognize_composite: per-component routing",
        notes="Tests composite recognition + per-component cost rollup",
    ),
}


def build_seed(seed: Seed) -> tuple[sp.Expr, sp.Symbol]:
    """Construct the sympy expression + iteration variable for a seed.

    Returns (expression, iteration_variable). Caller passes these into
    `rkc.search.SearchState(payload=expression, metadata={'var': var})`.
    """
    var = sp.Symbol(seed.var, integer=(seed.kind == "summand"), positive=True)
    locals_ = {seed.var: var}
    # always-available sympy constructs
    locals_.update({
        "exp": sp.exp, "log": sp.log, "sin": sp.sin, "cos": sp.cos,
        "sqrt": sp.sqrt, "pi": sp.pi, "I": sp.I, "oo": sp.oo,
        "Rational": sp.Rational, "Integer": sp.Integer,
        "Sum": sp.Sum, "Product": sp.Product, "Integral": sp.Integral,
        "gamma": sp.gamma, "k": sp.Symbol("k", integer=True, positive=True),
    })
    # extra symbols per seed
    for sym_name, assumptions in seed.extra_symbols:
        locals_[sym_name] = sp.Symbol(sym_name, **assumptions)
    expr = sp.sympify(seed.expr_string, locals=locals_)
    return expr, var
