"""rkc.costs — per-term complexity tracking (insight §A7).

The v1 recognizer reported a single `cost_direct` and `cost_dual` (a *term
count*). Insight §A7 makes the case that bits-per-term is misleading when
per-term cost varies wildly. For example:

  - HRR partition: each term costs O(prec * sqrt(n)) bits-of-work via
    Dedekind sums at mpmath dps=372.
  - Pentagonal recurrence: each term is one big-int add.
  - Mock-theta f3 truncation: each term is one rational-power + a partial
    product (cost grows with n).
  - Gauss sum: each term is one complex exp; trivially cheap.

v2 carries a `per_term_cost(params, target_precision)` function per
registry entry. The total work for a route is `num_terms * per_term_cost`.

We measure "cost" in approximate mpmath / big-int ops. Constants are
hand-calibrated to roughly match the order-of-magnitude wall-clock from
experiments 03, 05, 07. The absolute numbers are NOT load-bearing — what
matters is RELATIVE comparison between routes / kernels.
"""
from __future__ import annotations

import math
from typing import Any


def _prec_bits(target_precision: float) -> float:
    """Convert tolerance (e.g. 1e-12) to working precision in bits."""
    if target_precision <= 0:
        return 64.0
    return max(64.0, math.log2(1.0 / target_precision) + 16.0)


# ---------- per-kernel per-term cost models ----------
# Each takes (params, target_precision) and returns a float "ops per term".

def per_term_gaussian(params: dict, target_precision: float) -> float:
    """exp(-beta n^2): one mpmath exp at working precision."""
    bits = _prec_bits(target_precision)
    return float(bits)  # ~1 exp ~ O(bits) with FFT-based mpmath


def per_term_bose(params: dict, target_precision: float) -> float:
    """1 / (1 - exp(-beta n)): one exp + one div."""
    bits = _prec_bits(target_precision)
    return 2.0 * bits


def per_term_lambert(params: dict, target_precision: float) -> float:
    """q^n / (1 - q^n): one pow + one div + one sub."""
    bits = _prec_bits(target_precision)
    return 3.0 * bits


def per_term_mock_theta(params: dict, target_precision: float) -> float:
    """q^(n^2) / Π_{k=1..n} (1 + q^k)^[1 or 2].

    Cost grows with n because the partial product has n factors. Conservative:
    average term up to N costs ~N/2 multiplications at working precision. We
    return the AVERAGE per-term cost (so total cost = num_terms * this).
    """
    bits = _prec_bits(target_precision)
    # Average over n in [1, N]: avg cost ~ N/2 mul + pow
    # Without N we use a reference N=20 (typical truncation for q < 0.5)
    N_ref = 20
    return float(bits) * (N_ref / 2.0 + 2.0)


def per_term_partial_theta(params: dict, target_precision: float) -> float:
    """(-1)^n q^(n(n+1)/2): one pow."""
    bits = _prec_bits(target_precision)
    return float(bits)


def per_term_q_pochhammer(params: dict, target_precision: float) -> float:
    """Each factor (1 - a q^k): one pow + one sub + one mul (into running prod)."""
    bits = _prec_bits(target_precision)
    return 3.0 * bits


def per_term_eisenstein(params: dict, target_precision: float) -> float:
    """sigma_{2k-1}(n) q^n: divisor sum costs O(sqrt(n)) at integer precision
    plus a pow at working precision."""
    bits = _prec_bits(target_precision)
    # ref n=20: sqrt(20) ~ 4.5 divisor lookups, each cheap (integer); pow at bits
    return 5.0 + float(bits)


def per_term_dirichlet(params: dict, target_precision: float) -> float:
    """chi(n) * n^(-s): one char lookup (cheap) + one pow at bits."""
    bits = _prec_bits(target_precision)
    return 1.0 + float(bits)


def per_term_gauss_sum(params: dict, target_precision: float) -> float:
    """exp(2 pi i p n^2 / q): one complex exp; trivially cheap at low prec."""
    bits = _prec_bits(target_precision)
    return float(bits)


# Default (fuzzy / unknown) per-term cost
def per_term_default(params: dict, target_precision: float) -> float:
    bits = _prec_bits(target_precision)
    return float(bits)


# ---------- aggregator ----------

def total_cost(num_terms: int, per_term: float, scalar_coefficient: Any = 1) -> float:
    """Total ops = num_terms * per_term + 1 multiply for the outer scalar."""
    if num_terms <= 0 or per_term <= 0:
        return -1.0
    base = float(num_terms) * float(per_term)
    if scalar_coefficient is None or scalar_coefficient == 1:
        return base
    # one extra mul to fold the scalar in at the end
    return base + per_term


def composite_total_cost(component_results: list[dict]) -> float:
    """Sum total_cost across components of a composite (sum or product)."""
    s = 0.0
    for c in component_results:
        tc = c.get("total_cost", -1)
        if tc is not None and tc > 0:
            s += float(tc)
    return s if s > 0 else -1.0
