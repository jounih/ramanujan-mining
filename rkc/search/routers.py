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
    """
    accept_fuzzy: bool = False

    def route(self, state_after: SearchState) -> tuple[str, dict[str, Any]]:
        expr = state_after.payload
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


@dataclass
class RkcCostModel:
    """Estimate the cost-direct vs cost-reduced ratio via rkc.best_match.

    For the Ramanujan side, "reduced" means cheapest route rkc identifies
    (dual / modular completion / direct if no better available). Returns
    improvement_ratio = cost_direct / cost_reduced; >1 means the proposed
    transformation is cheaper.
    """

    def cost(self, state_before: SearchState,
             state_after: SearchState) -> CostEstimate:
        expr_before = state_before.payload
        expr_after = state_after.payload
        var = state_before.metadata.get("var") or sp.Symbol("n", integer=True, positive=True)

        bm_before = best_match(expr_before, var, accept_fuzzy=True)
        bm_after = best_match(expr_after, var, accept_fuzzy=True)

        # extract per-side cost; fall back to -1 sentinel handling
        def _safe_cost(bm):
            if bm is None:
                return float("inf")  # unrecognised → very expensive (penalty)
            if bm.total_cost > 0:
                return bm.total_cost
            if bm.num_terms > 0 and bm.per_term_cost > 0:
                return bm.num_terms * bm.per_term_cost
            return float("inf")

        cost_before = _safe_cost(bm_before)
        cost_after = _safe_cost(bm_after)

        if cost_after == float("inf"):
            ratio = 0.0  # transformation made things unrecognisable
            notes = "post-transformation expression unrecognised by rkc"
        elif cost_before == float("inf"):
            ratio = float("inf")  # any recognised result beats unknown baseline
            notes = "baseline expression unrecognised by rkc"
        else:
            ratio = cost_before / max(cost_after, 1.0)
            notes = (f"cost_before={cost_before:.1f}, cost_after={cost_after:.1f}, "
                     f"ratio={ratio:.2f}× ({'cheaper' if ratio > 1 else 'not improved'})")

        return CostEstimate(
            direct_cost=cost_before if cost_before != float("inf") else -1.0,
            reduced_cost=cost_after if cost_after != float("inf") else -1.0,
            improvement_ratio=ratio,
            notes=notes,
        )


# Protocol sanity checks
assert isinstance(RkcRouter(), Router)
assert isinstance(RkcCostModel(), CostModel)
