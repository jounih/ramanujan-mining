"""rkc.search.routers — RkcRouter + RkcCostModel.

Both wrap the existing `rkc.recognize` layer (already shipped v0.3.0).
These are the per-instance plug-ins for the Ramanujan side; the ARC side
(future) would have its own Router (DSL canonicalisation) and CostModel
(budget-aware tournament metric).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sympy as sp

from .core import CostEstimate, CostModel, Router, SearchState

from .. import recognize as _recognize_best  # we import best_match below
from ..recognizer import best_match
from ..routing import Route


_NUMERIC_CONSTS = {
    sp.pi: sp.Float(sp.pi.evalf(15)),
    sp.E: sp.Float(sp.E.evalf(15)),
    sp.EulerGamma: sp.Float(sp.EulerGamma.evalf(15)),
}


def _numerified_for_rkc(e: sp.Expr) -> sp.Expr:
    """Push symbolic π / e / γ → Float so rkc cost routines (which need
    mpf-convertible params) don't return DEGENERATE on operator outputs
    that legitimately contain symbolic constants."""
    try:
        return e.xreplace(_NUMERIC_CONSTS)
    except Exception:
        return e


@dataclass
class RkcRouter:
    """Classify the post-transformation expression via rkc.best_match.

    Returns `(route_label, payload_dict)` where route_label is the
    `Route.value` from rkc (DIRECT / DUAL / MODULAR_COMPLETION_REQUIRED /
    DEGENERATE / FUZZY / "UNKNOWN") and payload_dict carries:
      - kernel: the kernel id
      - family: the kernel family
      - confidence: rkc match confidence
      - notes: degeneracy reason, modular completion status, etc.

    The router numerifies symbolic π / e / γ before classification so that
    operator outputs containing those constants (like the Poisson-summation
    dual `√(π/β) · exp(-π² n² / β)`) classify cleanly instead of triggering
    the `mpf(symbolic_constant)` DEGENERATE path.
    """
    accept_fuzzy: bool = False

    def route(self, state_after: SearchState) -> tuple[str, dict[str, Any]]:
        expr = _numerified_for_rkc(state_after.payload)
        # iteration variable is in metadata; fall back to a fresh integer Symbol n
        var = state_after.metadata.get("var")
        if var is None:
            # try to recover from free symbols
            int_syms = [s for s in expr.free_symbols
                        if s.assumptions0.get("integer", False)]
            var = int_syms[0] if int_syms else sp.Symbol("n", integer=True, positive=True)
        result = best_match(expr, var, accept_fuzzy=self.accept_fuzzy)
        if result is None:
            return "UNKNOWN", {
                "kernel": None,
                "family": None,
                "confidence": 0.0,
                "notes": "no match (neither strict nor fuzzy)",
            }
        return result.route.value, {
            "kernel": result.kernel,
            "family": result.family,
            "confidence": result.confidence,
            "degenerate": result.degenerate,
            "reason": result.reason,
            "notes": result.notes,
        }


def _manual_cost_estimate(bm) -> float | None:
    """Closed-form cost estimate for known families when rkc declines to
    compute (FUZZY / DEGENERATE on symbolic params). Returns approximate
    direct-evaluation term count at default ~1e-12 precision.

    Currently handles: gaussian_quadratic (theta-like family) — most
    relevant for the v0.4 Poisson-summation flow.
    """
    if bm is None:
        return None
    # Gaussian: Σ exp(-β n²) needs num_terms ~ sqrt(-ln(tol)/β) before
    # exp(-β n²) < tol. Use tol=1e-12 (28 nats).
    if bm.family == "theta-like":
        beta = bm.params.get("beta")
        if beta is None:
            a2 = bm.params.get("a2")
            if a2 is not None:
                try:
                    beta = -float(a2)
                except Exception:
                    return None
        if beta is None:
            return None
        try:
            beta_f = float(beta)
            if beta_f <= 0:
                return None
            import math
            num_terms = max(1, math.ceil(math.sqrt(28.0 / beta_f)))
            return float(num_terms)
        except Exception:
            return None
    return None


def _gaussian_family_cost(expr: sp.Expr, var: sp.Symbol) -> float | None:
    """Cost estimate for `polynomial(n) · exp(quadratic_in_n)` summands.

    v0.7: rkc's strict gaussian matcher refuses any non-pure form (linear
    term, polynomial prefactor); fuzzy matcher catches some cases but not
    weighted forms like `n² · exp(-β n²)`. This helper recognises the
    structural class and computes the same `sqrt(28/β)`-style term-count
    estimate as `_manual_cost_estimate` for the theta-like family.

    The polynomial prefactor doesn't change the gaussian tail bound by
    more than a constant; the term count to reach 1e-12 absolute tolerance
    is dominated by the exponential decay rate β. Treats the prefactor as
    O(1) per-term cost (consistent with rkc's per-term-cost convention).

    Returns None if `expr` isn't structurally `polynomial(n) · exp(deg-2)`
    with negative leading coefficient — the caller falls back to
    `_structural_cost`.
    """
    if var is None:
        return None
    scalar, n_dep = expr.as_independent(var, as_Add=False)
    # n_dep must be a product of [a poly-in-n] × [exp(deg-2-in-n)] OR just
    # the exp factor (which is the pure gaussian case rkc handles, but we
    # still want to cost it here when the strict matcher refused due to
    # linear coefficient).
    polynomial_part = sp.Integer(1)
    exp_part = None
    if n_dep.func == sp.exp:
        exp_part = n_dep
    elif n_dep.func == sp.Pow and n_dep.args[0] == sp.E:
        exp_part = n_dep
    elif n_dep.func == sp.Mul:
        for f in n_dep.args:
            if (f.func == sp.exp
                    or (f.func == sp.Pow and f.args[0] == sp.E)):
                if exp_part is not None:
                    return None  # multiple exp factors — not the shape
                exp_part = f
            else:
                polynomial_part = polynomial_part * f
        if exp_part is None:
            return None
    else:
        return None
    # Parse exp argument as polynomial in var; degree must be exactly 2,
    # leading coefficient must be a negative number.
    if exp_part.func == sp.exp:
        arg = exp_part.args[0]
    else:
        arg = exp_part.args[1]
    if not arg.has(var):
        return None
    try:
        poly = sp.Poly(sp.expand(arg), var)
    except sp.PolynomialError:
        return None
    if poly.degree() != 2:
        return None
    a2 = poly.nth(2)
    try:
        beta_f = -float(a2)
    except (TypeError, ValueError):
        return None
    if beta_f <= 0:
        return None
    # Term-count estimate: same as _manual_cost_estimate for theta-like.
    import math
    return float(max(1, math.ceil(math.sqrt(28.0 / beta_f))))


def _one_sided_exponential_family_cost(
    expr: sp.Expr, var: sp.Symbol,
) -> float | None:
    """v0.8b cost estimate for one-sided modular families: log-Bose-Einstein
    (`c · log(1 - exp(-β n))`) and Lambert (`c · n / (R^n - 1)`).

    Both have exponential decay with rate β = log(R) or β directly, so the
    term-count to reach 1e-12 tolerance is `~log(1/tol)/β`. Mirrors
    `_route_bose_einstein` / `_route_lambert` in `rkc/registry.py`.

    Returns None if `expr` doesn't structurally match either form.

    Used by the cost model to give meaningful improvement ratios when
    `modular_transform_with_correction` fires on a small-β input and
    produces a large-β dual.
    """
    if var is None:
        return None
    scalar, n_dep = expr.as_independent(var, as_Add=False)
    # Form 1: log(1 - exp(-β n)) (Bose-Einstein log)
    beta = _try_extract_log_bose_einstein_beta(n_dep, var)
    # Form 2: n / (R^n - 1) (Lambert canonical form after sp.together)
    if beta is None:
        beta = _try_extract_lambert_form_beta(sp.together(n_dep), var)
    if beta is None:
        return None
    # Convert β to a float; if it has unevaluated π / log, use evalf
    try:
        beta_f = float(beta.evalf() if hasattr(beta, 'evalf') else beta)
    except (TypeError, ValueError):
        return None
    if beta_f <= 0:
        return None
    # Term count for ~1e-12 tol: log(10^12) / β = 28 / β (same constant as
    # the gaussian-family cost helper for consistency in cost units).
    import math
    return float(max(1, math.ceil(28.0 / beta_f)))


def _try_extract_log_bose_einstein_beta(
    expr: sp.Expr, var: sp.Symbol,
) -> sp.Expr | None:
    """Recognise `log(1 - exp(-β var))`; return β or None."""
    if expr.func != sp.log:
        return None
    arg = expr.args[0]
    if not arg.has(var):
        return None
    diff = sp.simplify(arg - 1)
    neg_exp = -diff
    if neg_exp.func != sp.exp:
        return None
    exp_arg = neg_exp.args[0]
    try:
        poly = sp.Poly(sp.expand(exp_arg), var)
    except sp.PolynomialError:
        return None
    if poly.degree() != 1:
        return None
    a1 = poly.nth(1)
    a0 = poly.nth(0)
    if a0 != 0:
        return None
    # a1 should be negative
    try:
        a1_f = float(a1.evalf() if hasattr(a1, 'evalf') else a1)
    except (TypeError, ValueError):
        return None
    if a1_f >= 0:
        return None
    return -a1


def _try_extract_lambert_form_beta(
    expr: sp.Expr, var: sp.Symbol,
) -> sp.Expr | None:
    """Recognise `var / (R^var - 1)` (canonical Lambert form for q ∈ (0,1));
    return β = log(R) or None."""
    num, den = sp.fraction(expr)
    if sp.simplify(num - var) != 0:
        return None
    den_p1 = sp.simplify(den + 1)
    if den_p1.func != sp.Pow:
        return None
    base, exponent = den_p1.args
    if sp.simplify(exponent - var) != 0:
        return None
    if not base.is_number:
        return None
    try:
        base_f = float(base)
    except (TypeError, ValueError):
        return None
    if base_f <= 1:
        return None
    return sp.log(base)


def _structural_cost(expr: sp.Expr) -> float:
    """Cost estimate based on expression structure when rkc can't recognise
    it (typical for v0.5+ Integral inputs and closed-form outputs).

    Conventions (matched to rkc's term-count units):
    - sp.Integral with finite or infinite limits → 100 (adaptive-quad iters)
    - sp.Sum / sp.Product with infinite upper limit → 100
    - Closed-form (no Sum/Integral/Product, finite operation count) → 1
    - Otherwise → None (signal "can't estimate")
    """
    if expr is None:
        return None
    if isinstance(expr, sp.Integral):
        return 100.0
    if isinstance(expr, (sp.Sum, sp.Product)):
        # if any limit is infinite, treat as aggregate cost
        for lim in expr.limits:
            if any(b is sp.oo or b is -sp.oo for b in lim[1:]):
                return 100.0
        return 50.0
    # has nested Sum/Integral/Product?
    if expr.has(sp.Integral, sp.Sum, sp.Product):
        return 100.0
    # closed form (Γ, sin, π, etc. evaluable in O(1))
    return 1.0


@dataclass
class RkcCostModel:
    """Estimate the cost-direct vs cost-reduced ratio via rkc.best_match.

    Compares the **direct-evaluation cost** of state_before vs state_after.
    The transformation is a win when the post-transformation expression
    has a smaller direct-evaluation cost than the pre-transformation one
    (which is the Pass A β\* = c·π crossover phenomenon expressed as a
    routing decision).

    Concretely for Poisson summation on a Gaussian:
      - expr_before = exp(-β n²) at small β → direct sum needs many terms
      - expr_after = √(π/β) exp(-π² n² / β) → β_effective = π²/β large
        → direct sum on the dual converges fast → cost_after << cost_before

    improvement_ratio > 1 ⇒ transformation is cheaper.
    """

    def cost(self, state_before: SearchState,
             state_after: SearchState) -> CostEstimate:
        expr_before = state_before.payload
        expr_after = state_after.payload
        var = state_before.metadata.get("var") or sp.Symbol("n", integer=True, positive=True)

        # Push symbolic π / e / γ → Float so rkc cost routines (which need
        # mpf-convertible params) don't return DEGENERATE on operator outputs
        # that legitimately contain symbolic constants. Same helper as the
        # router uses; keeps before/after units comparable.
        bm_before = best_match(_numerified_for_rkc(expr_before), var, accept_fuzzy=True)
        bm_after = best_match(_numerified_for_rkc(expr_after), var, accept_fuzzy=True)

        # Use rkc's cost_direct (the direct-evaluation cost of THIS expression
        # form). If cost_direct is -1 sentinel (e.g. DEGENERATE or FUZZY where
        # rkc doesn't compute cost), fall back to (a) total_cost; (b) manual
        # closed-form estimate from the matcher params; (c) float('inf').
        def _direct_cost(bm):
            if bm is None:
                return float("inf")
            if bm.cost_direct > 0:
                return float(bm.cost_direct)
            if bm.total_cost > 0:
                return float(bm.total_cost)
            if bm.num_terms > 0 and bm.per_term_cost > 0:
                return float(bm.num_terms * bm.per_term_cost)
            # Manual fallback for known families when rkc declined to cost
            # (typical for FUZZY matches or DEGENERATE-on-symbolic-params)
            manual = _manual_cost_estimate(bm)
            if manual is not None:
                return manual
            return float("inf")

        cost_before = _direct_cost(bm_before)
        cost_after = _direct_cost(bm_after)

        # v0.7 fallback: gaussian-family with polynomial prefactor or
        # linear-in-n offset (shifted theta, weighted theta) — rkc's
        # strict matcher refuses these but they are gaussian-cost-bounded.
        # This path catches the BEFORE side of half-shift / weighted
        # gaussian seeds; the AFTER side has a Float-numerified scalar
        # from the operator output and falls back to _structural_cost.
        if cost_before == float("inf"):
            gc = _gaussian_family_cost(expr_before, var)
            if gc is not None:
                cost_before = gc
        if cost_after == float("inf"):
            gc = _gaussian_family_cost(expr_after, var)
            if gc is not None:
                cost_after = gc

        # v0.8b fallback: one-sided exponential family (log-Bose-Einstein,
        # Lambert). rkc's strict matcher doesn't recognise these in our
        # current registry; the helper computes the same ~log(1/tol)/β
        # term-count estimate the rkc routing layer uses for the same
        # kernels (`_route_bose_einstein` / `_route_lambert` in
        # rkc/registry.py). The result: an honest improvement_ratio for
        # the modular_transform_with_correction operator's outputs.
        if cost_before == float("inf"):
            oc = _one_sided_exponential_family_cost(expr_before, var)
            if oc is not None:
                cost_before = oc
        if cost_after == float("inf"):
            oc = _one_sided_exponential_family_cost(expr_after, var)
            if oc is not None:
                cost_after = oc

        # Fallback: structural cost when rkc doesn't recognise. This is the
        # path Integrals and closed-form outputs (like Γ(s)) take in v0.5+.
        if cost_before == float("inf"):
            sc = _structural_cost(expr_before)
            if sc is not None:
                cost_before = sc
        if cost_after == float("inf"):
            sc = _structural_cost(expr_after)
            if sc is not None:
                cost_after = sc

        if cost_after == float("inf") and cost_before == float("inf"):
            ratio = 0.0
            notes = "both sides unrecognised — cannot decide"
        elif cost_after == float("inf"):
            ratio = 0.0
            notes = "post-transformation expression unrecognised by rkc"
        elif cost_before == float("inf"):
            ratio = float("inf")
            notes = "baseline expression unrecognised; any recognised result is an improvement"
        else:
            ratio = cost_before / max(cost_after, 1.0)
            notes = (f"cost_direct(before)={cost_before:.1f}, "
                     f"cost_direct(after)={cost_after:.1f}, "
                     f"ratio={ratio:.2f}× "
                     f"({'cheaper' if ratio > 1 else 'not improved'})")

        return CostEstimate(
            direct_cost=cost_before if cost_before != float("inf") else -1.0,
            reduced_cost=cost_after if cost_after != float("inf") else -1.0,
            improvement_ratio=ratio,
            notes=notes,
        )


# Protocol sanity checks
assert isinstance(RkcRouter(), Router)
assert isinstance(RkcCostModel(), CostModel)
