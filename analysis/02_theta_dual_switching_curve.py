"""
Experiment 02 — theta-dual switching curve.

Quantity:  Z(beta) = sum_{n in Z} exp(-beta n^2)
Two representations:
  (D)irect       Z = 1 + 2 sum_{n>=1} exp(-beta n^2)
  (T)heta-dual   Z = sqrt(pi/beta) * [1 + 2 sum_{n>=1} exp(-pi^2 n^2 / beta)]
                 (Poisson summation / Jacobi theta functional equation)

For each beta we measure the minimum number of nonnegative-n terms each
representation needs so that the next-term magnitude drops below the target
absolute tolerance tol; that term count is a stand-in for arithmetic work.
We also sanity-check that both routes agree to ~tol.

This turns ChatGPT's single point (beta=1e-6 -> 11871 vs 1) into a curve over
beta in [1e-8, 1e8] x tol in {1e-6, 1e-12, 1e-30, 1e-100}.

Output: CSV at analysis/results/theta_dual_curve.csv, plus a console summary.
"""
from __future__ import annotations
import csv
import math
import os
from pathlib import Path
from mpmath import mp, mpf, exp, sqrt, pi, log, ceil


def terms_needed_direct(beta: mpf, tol: mpf) -> int:
    """Smallest N s.t. exp(-beta * (N+1)^2) <= tol. Term count is N+1 (n=0..N)."""
    # solve beta * x^2 >= -log(tol)
    if tol <= 0:
        return 0
    rhs = -log(tol)
    if rhs <= 0:
        return 1
    x = sqrt(rhs / beta)
    return int(ceil(x)) + 1


def terms_needed_dual(beta: mpf, tol_dual: mpf) -> int:
    """For the dual sum sum_{n>=0} exp(-pi^2 n^2 / beta). After multiplying by
    the prefactor sqrt(pi/beta) and the leading 1, the tolerance carried into
    the inner sum is tol_dual = tol / (2*sqrt(pi/beta))."""
    if tol_dual <= 0:
        return 0
    alpha = pi * pi / beta
    rhs = -log(tol_dual)
    if rhs <= 0:
        return 1
    x = sqrt(rhs / alpha)
    return int(ceil(x)) + 1


def Z_direct(beta: mpf, tol: mpf) -> tuple[mpf, int]:
    N = terms_needed_direct(beta, tol)
    s = mpf(0)
    for n in range(1, N + 1):
        s += exp(-beta * n * n)
    return 1 + 2 * s, N + 1  # term count including n=0


def Z_dual(beta: mpf, tol: mpf) -> tuple[mpf, int]:
    pref = sqrt(pi / beta)
    # tolerance carried into inner sum
    inner_tol = tol / (2 * pref) if pref > 0 else tol
    N = terms_needed_dual(beta, inner_tol)
    s = mpf(0)
    alpha = pi * pi / beta
    for n in range(1, N + 1):
        s += exp(-alpha * n * n)
    return pref * (1 + 2 * s), N + 1


def main():
    out_path = Path(__file__).parent / "results" / "theta_dual_curve.csv"
    out_path.parent.mkdir(exist_ok=True)

    betas = [mpf(10) ** k for k in range(-8, 9)]
    tols = [mpf(10) ** -k for k in (6, 12, 30, 100)]

    rows = []
    print(f"{'beta':>10} {'tol':>10} {'direct_terms':>14} {'dual_terms':>12} {'gain':>10} {'cheap_route':>12} {'rel_diff':>14}")
    print("-" * 90)
    for tol in tols:
        # need enough working precision to actually certify
        dps_needed = max(50, int(-float(log(tol)) / math.log(10)) + 20)
        mp.dps = dps_needed
        for beta in betas:
            zd, nd = Z_direct(beta, tol)
            zt, nt = Z_dual(beta, tol)
            rel = abs(zd - zt) / (abs(zd) + mpf("1e-300"))
            gain = nd / nt if nt > 0 else float("inf")
            route = "T" if nt < nd else "D"
            print(f"{float(beta):>10.1e} {float(tol):>10.0e} {nd:>14d} {nt:>12d} {float(gain):>10.2g} {route:>12} {float(rel):>14.2e}")
            rows.append(
                dict(beta=float(beta), tol=float(tol),
                     direct_terms=nd, dual_terms=nt, gain_ratio=float(gain),
                     cheap_route=route, rel_difference=float(rel),
                     dps_used=dps_needed)
            )
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
