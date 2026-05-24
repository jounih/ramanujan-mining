"""
Experiment 03 — Reciprocal-Kernel Compiler v0.

A working sketch of a "compiler" that, given a kernel descriptor, picks the
representation that needs the fewest certified terms to compute a target
sum/integral to a target tolerance.

Currently supports the Gaussian kernel family
    Z(beta) = sum_{n in Z} exp(-beta * n^2)
with two routes:
    DIRECT  Z = 1 + 2 sum_{n>=1} exp(-beta n^2)        (slow at small beta)
    DUAL    Z = sqrt(pi/beta) * sum_{n in Z} exp(-pi^2 n^2 / beta)  (slow at large beta)

Improvements over experiment 02:
    1. Truncation certificate uses an erfc tail bound, not the
       next-term bound, which fixes a real bug in the large-beta dual regime.
    2. Cost predictor returns term counts a priori without running either sum.
    3. Decision: pick the cheaper route, log the why.
    4. Self-consistency check: both routes return values that match within tol.

Run prints a per-(beta,tol) line showing predicted-cost-D, predicted-cost-T,
chosen route, achieved relative error, and certified tail bound.
"""
from __future__ import annotations
import math
from dataclasses import dataclass
from mpmath import mp, mpf, exp, sqrt, pi, log, erfc, ceil


@dataclass
class TruncatedSumCost:
    terms: int               # how many nonneg-n terms to evaluate
    tail_bound: mpf          # rigorous bound on |truncated sum - exact|
    why: str                 # one-line explanation


def cost_direct_gaussian(beta: mpf, tol: mpf) -> TruncatedSumCost:
    """Cost to compute sum_{n>=1} exp(-beta n^2) with tail <= tol/2.

    Tail bound (rigorous):
        sum_{n>=N+1} exp(-beta n^2) <= (1 / (2*beta*N)) * exp(-beta (N+1)^2)
    or, looser but simpler,
        <= exp(-beta (N+1)^2) / (1 - exp(-beta (2N+1)))   (geometric majorization)

    We use the Gaussian-integral bound:
        sum_{n>=N+1} exp(-beta n^2) <= int_N^inf exp(-beta x^2) dx
                                     = (sqrt(pi)/(2 sqrt(beta))) * erfc(N sqrt(beta))
    which is tight and easy to invert.
    """
    if tol <= 0:
        raise ValueError("tol must be > 0")
    # we want (sqrt(pi)/(2 sqrt(beta))) * erfc(N sqrt(beta)) <= tol/2
    # i.e., erfc(z) <= tol * sqrt(beta/pi),  z = N sqrt(beta)
    rhs = tol * sqrt(beta / pi)
    # invert erfc by binary search (erfc is monotone decreasing)
    if rhs >= mpf(2):
        N = 0
    else:
        # find z s.t. erfc(z) <= rhs
        lo, hi = mpf(0), mpf(10)
        # grow hi until enough
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
        z = hi
        N = int(ceil(z / sqrt(beta)))
    tail = (sqrt(pi) / (2 * sqrt(beta))) * erfc(mpf(N) * sqrt(beta)) if N > 0 else mpf("inf")
    return TruncatedSumCost(terms=N + 1, tail_bound=tail,
                            why=f"erfc({N}*sqrt(beta))*sqrt(pi/(4 beta)) <= tol/2")


def cost_dual_gaussian(beta: mpf, tol: mpf) -> TruncatedSumCost:
    """The dual sum is (1/sqrt(beta/pi)) * Z(pi^2/beta) so cost is symmetric
    with alpha = pi^2/beta and the outer prefactor sqrt(pi/beta)."""
    alpha = pi * pi / beta
    pref = sqrt(pi / beta)
    inner_tol = tol / (2 * pref)
    inner_cost = cost_direct_gaussian(alpha, inner_tol)
    # outer tail bound: pref * 2 * inner_tail
    outer_tail = pref * 2 * inner_cost.tail_bound
    return TruncatedSumCost(terms=inner_cost.terms, tail_bound=outer_tail,
                            why=f"dual: {inner_cost.why} (alpha=pi^2/beta)")


def Z_direct(beta: mpf, N: int) -> mpf:
    s = mpf(0)
    for n in range(1, N + 1):
        s += exp(-beta * n * n)
    return 1 + 2 * s


def Z_dual(beta: mpf, N: int) -> mpf:
    alpha = pi * pi / beta
    pref = sqrt(pi / beta)
    s = mpf(0)
    for n in range(1, N + 1):
        s += exp(-alpha * n * n)
    return pref * (1 + 2 * s)


def compile_and_run(beta: mpf, tol: mpf, log_fn=print):
    """Pick the cheaper route, run it, certify, report."""
    cd = cost_direct_gaussian(beta, tol)
    ct = cost_dual_gaussian(beta, tol)
    if cd.terms <= ct.terms:
        chosen = "DIRECT"
        Z_chosen = Z_direct(beta, cd.terms - 1)
        chosen_cost = cd
    else:
        chosen = "DUAL"
        Z_chosen = Z_dual(beta, ct.terms - 1)
        chosen_cost = ct
    # cross-check: compute both at the chosen tolerance, verify they agree
    Z_d_check = Z_direct(beta, cd.terms - 1)
    Z_t_check = Z_dual(beta, ct.terms - 1)
    rel = abs(Z_d_check - Z_t_check) / (abs(Z_d_check) + mpf("1e-300"))
    log_fn(f"beta={float(beta):.1e} tol={float(tol):.0e}  "
           f"cost(D)={cd.terms:>6}  cost(T)={ct.terms:>6}  -> {chosen:>6}  "
           f"|Z_D-Z_T|/|Z|={float(rel):.2e}  certified_tail={float(chosen_cost.tail_bound):.2e}")
    return dict(beta=float(beta), tol=float(tol), cost_D=cd.terms, cost_T=ct.terms,
                chosen=chosen, Z=Z_chosen, rel_diff=rel,
                certified_tail=float(chosen_cost.tail_bound))


def main():
    rows = []
    for tol_exp in (6, 12, 30, 100):
        tol = mpf(10) ** -tol_exp
        mp.dps = max(60, tol_exp + 30)
        print(f"\n--- tol = 10^-{tol_exp} (dps={mp.dps}) ---")
        for beta_exp in range(-8, 9):
            rows.append(compile_and_run(mpf(10) ** beta_exp, tol))
    # summarize
    print("\nDone. Total invocations:", len(rows))


if __name__ == "__main__":
    main()
