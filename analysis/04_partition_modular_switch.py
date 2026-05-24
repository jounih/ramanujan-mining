"""
Experiment 04 — partition-function Z(beta) modular switch.

Physically meaningful kernel: 1D free-bosonic gas / Bose statistics.
    Z(beta) = sum_{n>=0} p(n) e^(-beta n) = 1 / prod_{k>=1} (1 - e^(-beta k))
             = e^(beta/24) / eta(i beta / (2 pi))

Two routes:
    DIRECT product  Z = 1 / prod_{k=1..K} (1 - e^(-beta k))     -- slow at small beta
    MODULAR S-transform via eta(-1/tau) = sqrt(-i tau) eta(tau):
            Z = e^(beta/24) / [ sqrt(beta/(2pi)) * eta(2*pi*i / beta * i) * e^(-(2pi)^2 / (24 beta)) ]
       wait, let me derive cleanly. Let tau = i beta / (2 pi). Then -1/tau = 2 pi i / beta = i (2pi/beta).
       eta(-1/tau) = sqrt(-i tau) * eta(tau).
       sqrt(-i tau) = sqrt(beta / (2 pi)).
       So eta(i beta/(2 pi)) = (1/sqrt(beta/(2 pi))) * eta(i 2pi/beta) = sqrt(2 pi / beta) * eta(i 2pi/beta).
       eta(i*y) for large y is dominated by e^(-pi y / 12) * (1 - e^(-2 pi y) - ...).
       So with beta small, 2pi/beta is large, eta(i 2pi/beta) is essentially e^(-pi (2pi/beta) / 12) = e^(-pi^2/(6 beta)).
       Z = e^(beta/24) / [sqrt(2pi/beta) * eta(i 2pi/beta)]
         = e^(beta/24) * sqrt(beta/(2pi)) / eta(i 2pi/beta)
         = e^(beta/24) * sqrt(beta/(2pi)) * e^(pi^2/(6 beta)) / (1 - e^(-4 pi^2/beta) - ...)

  This is the famous Hardy-Ramanujan asymptotic for Z(beta).

Compare term counts:
    DIRECT product: K terms s.t. (1 - e^(-beta K)) factor contributes < tol-equivalent
    MODULAR product: K' terms s.t. (1 - e^(-(2pi/beta) k * 2pi)) factor contributes < tol
                      (since eta(iy) = e^(-pi y/12) * prod (1 - e^(-2 pi k y))  with y = 2pi/beta)

Output: CSV of (beta, tol, K_direct, K_modular, Z_direct, Z_modular, rel_diff).
"""
from __future__ import annotations
import csv
import math
from pathlib import Path
from mpmath import mp, mpf, exp, sqrt, pi, log, ceil


def Z_direct(beta: mpf, K: int) -> mpf:
    """Z(beta) = 1 / prod_{k=1..K} (1 - e^(-beta k))."""
    prod = mpf(1)
    for k in range(1, K + 1):
        prod *= 1 - exp(-beta * k)
    return 1 / prod


def K_direct_needed(beta: mpf, tol: mpf) -> int:
    """Want the missing tail factors prod_{k>K}(1 - e^(-beta k)) close to 1 within tol.
    Tail logarithm: -sum_{k>K} log(1 - e^(-beta k)) ~ sum_{k>K} e^(-beta k) = e^(-beta (K+1)) / (1 - e^(-beta)).
    Want this < tol.
    """
    # solve e^(-beta(K+1)) / (1 - e^(-beta)) < tol
    # K+1 > -log(tol * (1 - e^(-beta))) / beta
    inv_factor = 1 - exp(-beta)
    if inv_factor <= 0:
        return 1
    rhs = -log(tol * inv_factor)
    if rhs <= 0:
        return 1
    return int(ceil(rhs / beta))


def Z_modular(beta: mpf, K: int) -> mpf:
    """Derivation:
        Z(beta) = sum p(n) e^(-beta n) = prod_{n>=1} (1 - e^(-beta n))^-1.
        eta(tau) = q^(1/24) prod (1 - q^n), q = exp(2 pi i tau).
        Set tau = i beta / (2 pi); then q = e^(-beta) and
            eta(i beta / (2 pi)) = e^(-beta/24) prod (1 - e^(-beta n)).
        So Z = e^(-beta/24) / eta(i beta / (2 pi)).
        Modular S-transform: eta(-1/tau) = sqrt(-i tau) eta(tau)
            => eta(i beta / (2 pi)) = sqrt(2 pi / beta) eta(i 2 pi / beta).
        And eta(i 2 pi / beta) = e^(-pi^2 / (6 beta)) prod (1 - e^(-4 pi^2 n / beta)).
        Combine:
            Z(beta) = e^(-beta/24) sqrt(beta/(2 pi)) e^(pi^2/(6 beta)) / prod_{n>=1} (1 - e^(-4 pi^2 n / beta)).
    """
    pref = exp(-beta / 24) * sqrt(beta / (2 * pi)) * exp(pi * pi / (6 * beta))
    a = 4 * pi * pi / beta
    prod = mpf(1)
    for k in range(1, K + 1):
        prod *= 1 - exp(-a * k)
    return pref / prod


def K_modular_needed(beta: mpf, tol: mpf) -> int:
    a = 4 * pi * pi / beta
    inv_factor = 1 - exp(-a)
    if inv_factor <= 0:
        return 1
    rhs = -log(tol * inv_factor)
    if rhs <= 0:
        return 1
    return int(ceil(rhs / a))


CAP = 2000  # skip actual evaluation if a route asks for > CAP terms, but still report cost


def main():
    out_path = Path(__file__).parent / "results" / "partition_modular_switch.csv"
    out_path.parent.mkdir(exist_ok=True)
    rows = []
    print(f"{'beta':>10} {'tol':>10} {'K_direct':>12} {'K_modular':>12} {'gain':>8} {'route':>8} {'rel_diff':>14}")
    print("-" * 90)
    for tol_exp in (12, 30, 60):
        tol = mpf(10) ** -tol_exp
        mp.dps = max(50, tol_exp + 20)
        for beta_exp in range(-3, 5):  # 1e-3 .. 1e4
            beta = mpf(10) ** beta_exp
            Kd = K_direct_needed(beta, tol)
            Km = K_modular_needed(beta, tol)
            # actual evaluation only if both routes are cheap enough; else rely on certificate
            if max(Kd, Km) <= CAP:
                Zd = Z_direct(beta, Kd)
                Zm = Z_modular(beta, Km)
                rel = abs(Zd - Zm) / (abs(Zd) + mpf("1e-300"))
                rel_str = f"{float(rel):.2e}"
            else:
                # evaluate only the cheap route, skip cross-check
                cheap_K = min(Kd, Km)
                if Kd <= Km:
                    Z_cheap = Z_direct(beta, Kd)
                else:
                    Z_cheap = Z_modular(beta, Km)
                rel = float("nan")
                rel_str = "skipped (cap)"
            gain = Kd / Km if Km > 0 else float("inf")
            route = "MOD" if Km < Kd else "DIR"
            print(f"{float(beta):>10.1e} {float(tol):>10.0e} {Kd:>12d} {Km:>12d} {float(gain):>8.2g} {route:>8} {rel_str:>14}")
            rows.append(dict(beta=float(beta), tol=float(tol), K_direct=Kd, K_modular=Km,
                             gain_ratio=float(gain), cheap_route=route, rel_difference=rel))
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
