"""
Experiment 09 — Kernel-Fingerprint Recognizer v0.

Answers Gemini's "next step" question: how do we programmatically detect that
an arbitrary user-defined energy function matches a known dual kernel?

This v0 is intentionally tiny but real: it walks a sympy expression tree
representing an energy summand E(n, params), extracts structural fingerprints,
and matches against a small registry of canonical kernels. For each match it
returns:
  - registry name
  - the dual identity it knows (string form)
  - the cost predictor for both direct and dual routes
  - the certified tail bound function

Registry entries supported in v0:
  * "gaussian_quadratic"     E(n) = beta * n^2
  * "bose_einstein_geometric" E(n) = -log(1 - exp(-beta n))    (additive in log)
  * "lambert_divisor"        f(q) = sum q^n / (1 - q^n)        (kernel q^n/(1-q^n))
  * "fermi_dirac_geometric"  E(n) = -log(1 + exp(-beta n))    (mock counterpart)
  * "dedekind_eta_log"       E(n) = -log(1 - exp(2 pi i n tau))

Each entry carries:
  match(expr, dummy) -> dict or None    (returns extracted parameters if match)
  cost_direct(params, tol) -> int
  cost_dual(params, tol)   -> int

Usage demo (`main()`):
  - constructs a few test expressions
  - prints (recognized_kernel, recognized_params, cost_direct, cost_dual, recommended_route)
"""
from __future__ import annotations
import sympy as sp
from dataclasses import dataclass
from typing import Callable, Optional
from mpmath import mp, mpf, exp, sqrt, pi, log, erfc, ceil


@dataclass
class RegistryEntry:
    name: str
    match: Callable          # (sympy_expr, summation_var) -> Optional[dict]
    cost_direct: Callable    # (params, tol) -> int
    cost_dual: Callable      # (params, tol) -> int or None
    dual_identity: str       # human-readable


# ---------- match helpers ----------

def _match_gaussian(expr, n):
    """E = beta * n^2 (we then look for outer exp). Returns {'beta': ...} or None."""
    # the expression we're given is the summand, which we expect to look like exp(-beta * n^2)
    # try: expr = exp(-beta * n^2)
    if not isinstance(expr, sp.exp.__class__) and not (expr.func == sp.exp):
        # also accept E^(-x) parsed differently
        return None
    arg = expr.args[0]
    # arg should be -beta * n^2
    coeff_n2 = arg.coeff(n, 2)
    coeff_n1 = arg.coeff(n, 1)
    coeff_n0 = arg.coeff(n, 0)
    if coeff_n2 is not sp.S.Zero and coeff_n1 == 0 and coeff_n0 == 0:
        if coeff_n2.is_negative:
            return {"beta": -coeff_n2}
    return None


def _match_bose_einstein(expr, n):
    """Summand for log Z = -sum_n log(1 - exp(-beta n)). Take expr = -log(1 - exp(-beta n)) or its
    exponentiated/product form 1/(1 - exp(-beta n))."""
    # Try the 1/(1 - exp(-beta n)) form:
    if expr.func == sp.Pow and expr.args[1] == -1:
        inner = expr.args[0]
        # inner should be 1 - exp(-beta n)
        if inner.func == sp.Add and len(inner.args) == 2:
            a, b = inner.args
            for one_term, exp_term in [(a, b), (b, a)]:
                if one_term == 1 and exp_term.func == sp.Mul and len(exp_term.args) == 2:
                    sign, exp_part = exp_term.args
                    if sign == -1 and exp_part.func == sp.exp:
                        coeff_n = exp_part.args[0].coeff(n, 1)
                        if coeff_n.is_negative:
                            return {"beta": -coeff_n}
    # Try the logarithmic summand
    if expr.func == sp.Mul and -1 in expr.args:
        rest = sp.Mul(*[a for a in expr.args if a != -1])
        if rest.func == sp.log:
            inner = rest.args[0]
            if inner.func == sp.Add and len(inner.args) == 2:
                a, b = inner.args
                for one_term, exp_term in [(a, b), (b, a)]:
                    if one_term == 1:
                        if exp_term.func == sp.Mul and -1 in exp_term.args:
                            other = sp.Mul(*[x for x in exp_term.args if x != -1])
                            if other.func == sp.exp:
                                coeff_n = other.args[0].coeff(n, 1)
                                if coeff_n.is_negative:
                                    return {"beta": -coeff_n}
    return None


def _match_lambert_divisor(expr, n):
    """f_summand(n) = q^n / (1 - q^n) for variable q in (0,1). Return {'q': q} or None."""
    if expr.func == sp.Mul and len(expr.args) == 2:
        a, b = expr.args
        for num, den in [(a, b), (b, a)]:
            if den.func == sp.Pow and den.args[1] == -1:
                inner = den.args[0]
                if num.func == sp.Pow and num.args[1] == n:
                    q = num.args[0]
                    if inner == 1 - q ** n:
                        return {"q": q}
    return None


# ---------- cost models ----------

def _cost_gauss_direct(params, tol):
    beta = mpf(params["beta"])
    rhs = mpf(tol) * sqrt(beta / pi)
    if rhs >= 2:
        return 1
    lo, hi = mpf(0), mpf(10)
    while erfc(hi) > rhs:
        hi *= 2
        if hi > mpf(1e30):
            break
    for _ in range(200):
        mid = (lo + hi) / 2
        if erfc(mid) > rhs:
            lo = mid
        else:
            hi = mid
        if hi - lo < mpf(1e-20):
            break
    return int(ceil(hi / sqrt(beta))) + 1


def _cost_gauss_dual(params, tol):
    beta = mpf(params["beta"])
    alpha = pi * pi / beta
    pref = sqrt(pi / beta)
    inner_tol = mpf(tol) / (2 * pref)
    return _cost_gauss_direct({"beta": alpha}, inner_tol)


def _cost_bose_direct(params, tol):
    """K s.t. e^(-beta(K+1)) / (1 - e^(-beta)) < tol."""
    beta = mpf(params["beta"])
    inv_factor = 1 - exp(-beta)
    rhs = -log(mpf(tol) * inv_factor)
    if rhs <= 0:
        return 1
    return int(ceil(rhs / beta))


def _cost_bose_dual(params, tol):
    beta = mpf(params["beta"])
    a = 4 * pi * pi / beta
    inv_factor = 1 - exp(-a)
    rhs = -log(mpf(tol) * inv_factor)
    if rhs <= 0:
        return 1
    return int(ceil(rhs / a))


def _cost_lambert_direct(params, tol):
    """f_summand(n) = q^n / (1 - q^n); for n large dominated by q^n / 1 since q^n -> 0.
    Tail bound: sum_{n>K} q^n/(1-q^n) <= q^(K+1) / ((1-q)(1-q^(K+1))). Solve."""
    q = mpf(params["q"])
    if q >= 1:
        return -1  # divergent
    # q^(K+1) / (1 - q) < tol  -> K+1 > log(tol*(1-q)) / log(q)
    rhs = log(mpf(tol) * (1 - q)) / log(q)
    return int(ceil(rhs))


def _cost_lambert_dual(params, tol):
    """Use Eisenstein modular S-transform. With q = e^(2 pi i tau), tau = i y, q = e^(-2 pi y),
    the modular companion uses tau' = -1/tau = i/y, so q' = e^(-2 pi / y) = e^(-2 pi / (-log q / (2pi)))
    = e^(-4 pi^2 / -log q). So the dual q' is much smaller than q when -log q is small (q near 1).
    Tail bound similar:  q'^(K+1) / (1 - q') < tol."""
    q = mpf(params["q"])
    if q >= 1 or q <= 0:
        return -1
    neg_log_q = -log(q)
    q_prime = exp(-4 * pi * pi / neg_log_q)
    if q_prime <= 0 or q_prime >= 1:
        return -1
    rhs = log(mpf(tol) * (1 - q_prime)) / log(q_prime)
    return int(ceil(rhs))


# ---------- registry ----------

REGISTRY = [
    RegistryEntry(
        name="gaussian_quadratic",
        match=_match_gaussian,
        cost_direct=_cost_gauss_direct,
        cost_dual=_cost_gauss_dual,
        dual_identity="theta_3(0; q) = sqrt(pi/(-log q)) * theta_3(0; e^(-pi^2/(-log q)))",
    ),
    RegistryEntry(
        name="bose_einstein_geometric",
        match=_match_bose_einstein,
        cost_direct=_cost_bose_direct,
        cost_dual=_cost_bose_dual,
        dual_identity="eta(-1/tau) = sqrt(-i tau) eta(tau); for Z=1/prod(1-q^n), q=exp(-beta), the S-dual gives a fast-converging product at q'=exp(-4 pi^2/beta).",
    ),
    RegistryEntry(
        name="lambert_divisor",
        match=_match_lambert_divisor,
        cost_direct=_cost_lambert_direct,
        cost_dual=_cost_lambert_dual,
        dual_identity="sum n q^n/(1-q^n) ~ Eisenstein-style. Modular S-transform sends q -> e^(-4 pi^2/(-log q)), making the dual sum convergent fast when q is near 1.",
    ),
]


def recognize_and_route(expr_summand, n, tol=mpf("1e-12")) -> dict:
    """Walk the registry, find all matches, predict costs, recommend the cheap route."""
    results = []
    for entry in REGISTRY:
        params = entry.match(expr_summand, n)
        if params is None:
            continue
        cd = entry.cost_direct(params, tol)
        cdual = entry.cost_dual(params, tol)
        chosen = "DIRECT" if cd <= cdual else "DUAL"
        results.append({
            "kernel": entry.name,
            "params": {k: float(v) for k, v in params.items()},
            "cost_direct": cd,
            "cost_dual": cdual,
            "recommended": chosen,
            "gain_if_dual": (cd / cdual) if cdual > 0 else float("inf"),
            "dual_identity": entry.dual_identity,
        })
    return results


def main():
    n = sp.symbols("n", positive=True)
    beta, q = sp.symbols("beta q", positive=True)

    test_cases = [
        ("Gaussian theta at beta=1e-4",  sp.exp(-mpf("1e-4") * n ** 2)),
        ("Gaussian theta at beta=1.0",   sp.exp(-1 * n ** 2)),
        ("Gaussian theta at beta=1e4",   sp.exp(-mpf("1e4") * n ** 2)),
        ("Bose-Einstein 1/(1-e^(-0.01 n))", 1 / (1 - sp.exp(-mpf("0.01") * n))),
        ("Bose-Einstein 1/(1-e^(-10 n))",   1 / (1 - sp.exp(-10 * n))),
        ("Lambert q^n/(1-q^n), q=0.99", (mpf("0.99")) ** n / (1 - (mpf("0.99")) ** n)),
        ("Lambert q^n/(1-q^n), q=0.5",  (mpf("0.5"))  ** n / (1 - (mpf("0.5"))  ** n)),
        ("Unknown kernel: sin(beta*n)",  sp.sin(0.1 * n)),
    ]
    print(f"\n{'description':<46} {'kernel':<26} {'cost_D':>8} {'cost_T':>8} {'route':>8} {'gain':>10}")
    print("-" * 110)
    for desc, expr in test_cases:
        matches = recognize_and_route(expr, n, tol=mpf("1e-12"))
        if not matches:
            print(f"{desc:<46} {'<none>':<26} {'-':>8} {'-':>8} {'-':>8} {'-':>10}")
        for m in matches:
            print(f"{desc:<46} {m['kernel']:<26} {m['cost_direct']:>8} {m['cost_dual']:>8} {m['recommended']:>8} {m['gain_if_dual']:>10.2g}")


if __name__ == "__main__":
    main()
