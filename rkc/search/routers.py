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
        # extract β from params; FUZZY shape uses 'a2' = -β
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
            # rkc's cost_direct is term count (NOT multiplied by per_term_cost);
            # match that convention so comparisons are like-for-like.
            num_terms = max(1, math.ceil(math.sqrt(28.0 / beta_f)))
            return float(num_terms)
        except Exception:
            return None
    return None


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
