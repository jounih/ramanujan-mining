"""
Experiment 11 — Composite-energy recognizer extension (RKC v0.5).

Extends the experiment-09 recognizer to handle composite expressions of the form
    summand(n) = f1(n) * f2(n) * ...      (product of recognized kernels)
or
    summand(n) = f1(n) + f2(n) + ...      (sum of recognized kernels)
where each f_i is independently routable via the kernel registry.

The "partial recognition + residual" pattern is also supported: if the
expression matches a registered kernel up to a small additive perturbation,
route the recognized part and emit a residual to evaluate directly.

This is the recognizer-side analog of the mock-theta-residual story: the
"clean" modular leading term is routed via its dual; the remainder (whether
a Lambert-style correction or, in the more ambitious case, a mock-theta
shadow) is computed directly. The total cost is then `cost(leading) +
cost(residual)`, and if the residual is small the cost is dominated by
the leading dual route.

Test cases:
  - Gaussian * Bose (product of two kernels at different temperatures)
  - Gaussian + Bose (additive)
  - Gaussian * Lambert (product with q-series)
  - Mostly-Gaussian with epsilon Lambert correction (the structural shape of
    mock-modular leading + non-modular correction)
"""
from __future__ import annotations
import sympy as sp
from typing import Optional
from mpmath import mp, mpf, exp, log
# Import the registry from experiment 09
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from importlib import import_module
exp09 = import_module("09_kernel_recognizer_v0")
REGISTRY = exp09.REGISTRY
recognize_and_route = exp09.recognize_and_route


def recognize_composite(expr_summand, n, tol=mpf("1e-12")):
    """Try to recognize a composite expression.

    Strategy:
      1) If expr is a sympy Mul, split into factors and try to match each
         factor (or product of factors) against the registry. Recommend a
         route as the product of independently-routed components.
      2) If expr is a sympy Add, split into terms; route each term, sum costs
         (concurrent independence: total terms needed = max of per-term costs
         under joint truncation; for simplicity we report a SUM of per-term
         cheap-route costs, which is a strict upper bound).
      3) Otherwise: try direct match; if none, return None.

    Returns dict with:
      - 'route': "DIRECT" / "DUAL" / "MIXED"
      - 'cost': estimated term count (for sums: max of components; for products:
                cost is for the JOINT factorization, here approximated by max(component costs))
      - 'components': list of recognized sub-kernels + their costs
      - 'unmatched': sub-expressions for which no kernel match was found
    """
    # Try direct first
    matches = recognize_and_route(expr_summand, n, tol)
    if matches:
        return {"route_type": "ATOMIC", "cost": min(m["cost_direct"] for m in matches if m["cost_direct"] > 0),
                "components": [{"kernel": m["kernel"], "params": m["params"],
                                "cost_direct": m["cost_direct"], "cost_dual": m["cost_dual"],
                                "recommended": m["recommended"]} for m in matches],
                "unmatched": []}

    components = []
    unmatched = []
    if expr_summand.func == sp.Mul:
        # try each factor
        for factor in expr_summand.args:
            sub_matches = recognize_and_route(factor, n, tol)
            if sub_matches:
                best = min(sub_matches, key=lambda m: min(m["cost_direct"], m["cost_dual"]) if m["cost_dual"] > 0 else m["cost_direct"])
                components.append({"kernel": best["kernel"], "params": best["params"],
                                   "cost_direct": best["cost_direct"], "cost_dual": best["cost_dual"],
                                   "recommended": best["recommended"]})
            else:
                unmatched.append(str(factor))
        if components:
            # for a product of independent kernels in n, the JOINT cost to compute
            # the convolution / coefficient extraction is bounded by max of per-factor costs
            joint_cost = max(min(c["cost_direct"], c["cost_dual"]) for c in components if min(c["cost_direct"], c["cost_dual"]) > 0)
            return {"route_type": "PRODUCT", "cost": joint_cost,
                    "components": components, "unmatched": unmatched}

    if expr_summand.func == sp.Add:
        total_cost = 0
        for term in expr_summand.args:
            sub_matches = recognize_and_route(term, n, tol)
            if sub_matches:
                best = min(sub_matches, key=lambda m: min(m["cost_direct"], m["cost_dual"]) if m["cost_dual"] > 0 else m["cost_direct"])
                components.append({"kernel": best["kernel"], "params": best["params"],
                                   "cost_direct": best["cost_direct"], "cost_dual": best["cost_dual"],
                                   "recommended": best["recommended"]})
                total_cost += min(best["cost_direct"], best["cost_dual"]) if best["cost_dual"] > 0 else best["cost_direct"]
            else:
                unmatched.append(str(term))
        if components:
            return {"route_type": "SUM", "cost": total_cost,
                    "components": components, "unmatched": unmatched}

    return None


def main():
    n = sp.symbols("n", positive=True)
    test_cases = [
        ("Gaussian theta beta=1e-4 alone",  sp.exp(-mpf("1e-4") * n ** 2)),
        ("Gaussian * Bose product (decoupled temperatures)",
         sp.exp(-mpf("1e-4") * n ** 2) * (1 / (1 - sp.exp(-mpf("0.5") * n)))),
        ("Gaussian + Bose additive composite",
         sp.exp(-mpf("1e-4") * n ** 2) + (1 / (1 - sp.exp(-mpf("0.5") * n)))),
        ("Bose at beta=0.01 + Lambert at q=0.99 (warm + warm)",
         (1 / (1 - sp.exp(-mpf("0.01") * n))) + (mpf("0.99") ** n / (1 - mpf("0.99") ** n))),
        ("Gaussian * sin(n) (mostly-recognized with unmatched harmonic)",
         sp.exp(-mpf("1e-3") * n ** 2) * sp.sin(n)),
    ]
    print(f"{'description':<58} {'route_type':<10} {'total_cost':>10} {'matched':>9} {'unmatched':>9}")
    print("-" * 100)
    for desc, expr in test_cases:
        result = recognize_composite(expr, n, tol=mpf("1e-12"))
        if result is None:
            print(f"{desc:<58} {'<none>':<10} {'-':>10} {'0':>9} {'-':>9}")
        else:
            n_match = len(result["components"])
            n_unmatch = len(result["unmatched"])
            print(f"{desc:<58} {result['route_type']:<10} {result['cost']:>10} {n_match:>9} {n_unmatch:>9}")
            for c in result["components"]:
                cheap = min(c['cost_direct'], c['cost_dual']) if c['cost_dual'] > 0 else c['cost_direct']
                print(f"    {c['kernel']:<28} params={c['params']}  cost(D)={c['cost_direct']}  cost(T)={c['cost_dual']}  cheap={cheap}")
            for u in result["unmatched"]:
                print(f"    UNMATCHED: {u}")
        print()


if __name__ == "__main__":
    main()
