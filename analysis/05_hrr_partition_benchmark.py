"""
Experiment 05 — bits-per-term benchmark for the integer partition function p(n).

Two representations of the SAME number p(n):

Method A (PENTAGONAL): Euler's pentagonal-number recurrence.
    p(n) = sum_{k>=1} (-1)^(k+1) [p(n - g_k) + p(n - g_{-k})]
    where g_k  = k(3k-1)/2 and g_{-k} = k(3k+1)/2.
    Pure integer arithmetic, no precision concerns. The cost metric is the
    total number of recurrence summands evaluated while building the table
    p(0), p(1), ..., p(n). Per-n work is O(sqrt(n)) summands (only k with
    g_k <= n contribute), so building the whole table costs O(n^{3/2}).

Method B (HRR): Hardy-Ramanujan-Rademacher exact series.
    p(n) = (1/(pi sqrt(2))) sum_{k=1}^infty sqrt(k) A_k(n) d/dn [sinh(C lambda_n / k)/lambda_n]
    where lambda_n = sqrt(n - 1/24), C = pi sqrt(2/3),
    and A_k(n) = sum_{0<=h<k, gcd(h,k)=1} exp(pi i s(h,k) - 2 pi i h n / k)
    is a Kloosterman-type sum (s(h,k) the classical Dedekind sum).
    Truncate at N s.t. the rigorous Rademacher tail bound below is < 0.5,
    so rounding to the nearest integer recovers p(n) exactly. N = O(sqrt(n)).

Rigorous Rademacher tail bound used (Rademacher 1937; see Calkin &
Johansson, Lehmer 1938; convenient form used by Johansson arXiv:1410.1672
section 5):
    |R_N(n)| <= (44 pi^2)/(225 sqrt(3)) * N^{-1/2}
              + (pi sqrt(2)/75) * sqrt(N/(n-1)) * sinh(pi sqrt(2 n / 3) / N).

The two methods produce the same INTEGER p(n); the *work* to get there is
totally different.

For each n in {10, 100, 1000, 10000, 100000} we record:
  - terms summed
  - bits_per_term = log2(p(n)) / terms   (information content per summand)
  - total_bits    = log2(p(n))           (size of the output)
  - wall_seconds  (rough, single-shot)

Both methods are wall-clock-measured.  Per the task we cross-check at every n
that the HRR integer equals the pentagonal integer (the latter is exact by
construction in Python integers).

Notes on the asymmetry:
  * pentagonal cost is integer-arithmetic ops on numbers of size O(log p(n));
    bignum work per add grows. HRR cost is mpmath floating ops at precision
    dps ~ log10(p(n)) + safety. Each "term" in HRR is far more expensive than
    a pentagonal-recurrence add, but there are exponentially fewer of them
    (sqrt(n)/log(n) vs n^{3/2} summands total). The "bits-per-term" metric
    isolates representation density and ignores per-term cost; the
    wall-seconds column exposes the per-term-cost asymmetry.
"""
from __future__ import annotations
import csv
import time
from math import gcd
from pathlib import Path

from mpmath import (
    mp, mpf, mpc, exp, sqrt, pi, log, cosh, sinh, nint,
)


# -------- Method A: Euler's pentagonal recurrence (exact integer) --------

def pentagonal_partitions(N: int) -> tuple[list[int], int]:
    """Build p(0..N) via Euler's pentagonal recurrence.

    Returns (table, total_terms_summed_across_all_n).
    Each iteration adds one recurrence term to the running n-sum; total_terms
    counts those adds across n=1..N. p(0)=1 is free (zero adds).
    """
    p = [0] * (N + 1)
    p[0] = 1
    total_terms = 0
    for n in range(1, N + 1):
        s = 0
        k = 1
        while True:
            g_pos = k * (3 * k - 1) // 2   # pentagonal number for +k
            g_neg = k * (3 * k + 1) // 2   # pentagonal number for -k
            if g_pos > n:
                break
            sign = 1 if (k % 2 == 1) else -1
            s += sign * p[n - g_pos]
            total_terms += 1
            if g_neg <= n:
                s += sign * p[n - g_neg]
                total_terms += 1
            k += 1
        p[n] = s
    return p, total_terms


# -------- Method B: Hardy-Ramanujan-Rademacher exact series ---------------

def dedekind_sum(h: int, k: int) -> mpf:
    """Classical Dedekind sum s(h, k) = sum_{r=1..k-1} ((r/k))((hr/k)),
    where ((x)) = x - floor(x) - 1/2 for x non-integer, 0 otherwise."""
    if k == 1:
        return mpf(0)
    s = mpf(0)
    inv_k = mpf(1) / k
    for r in range(1, k):
        a = (r * h) % k
        if a == 0:
            continue
        s += (r * inv_k - mpf("0.5")) * (a * inv_k - mpf("0.5"))
    return s


def A_k(k: int, n: int) -> mpc:
    """Rademacher Kloosterman-like sum
        A_k(n) = sum_{0<=h<k, gcd(h,k)=1} exp(pi i s(h,k) - 2 pi i h n / k).
    Returns an mpc whose imaginary part cancels across k after summation.
    """
    if k == 1:
        return mpc(1)
    s = mpc(0)
    two_pi_i = 2 * pi * mpc(0, 1)
    pi_i = pi * mpc(0, 1)
    for h in range(1, k):
        if gcd(h, k) != 1:
            continue
        sh = dedekind_sum(h, k)
        s += exp(pi_i * sh - two_pi_i * h * n / k)
    return s


def hrr_term(k: int, n: int) -> mpc:
    """Single Rademacher summand T_k(n).

    Decompose: p(n) = (1/(pi sqrt(2))) sum_k sqrt(k) A_k(n) df/dn,
    where  f(n) = sinh(C lambda_n / k) / lambda_n,  C = pi sqrt(2/3),
    lambda_n = sqrt(n - 1/24).  Direct chain rule gives
        df/dn = mu cosh(mu lambda) / (2 lambda^2) - sinh(mu lambda)/(2 lambda^3),
    with mu = C/k. (No Bessel call required; the derivative is closed form.)
    """
    C = pi * sqrt(mpf(2) / 3)
    lam = sqrt(mpf(n) - mpf(1) / 24)
    mu = C / k
    arg = mu * lam
    dfdn = (mu * cosh(arg)) / (2 * lam * lam) - sinh(arg) / (2 * lam * lam * lam)
    return (sqrt(mpf(k)) * A_k(k, n) * dfdn) / (pi * sqrt(mpf(2)))


def rademacher_tail_bound(N: int, n: int) -> mpf:
    """Rigorous bound on |p(n) - sum_{k=1}^N T_k(n)|.

    Form used in Johansson arXiv:1410.1672 sec 5 (Calkin-Johansson lemma,
    originally due to Rademacher 1937 / Lehmer 1938).
    """
    N_mp = mpf(N); n_mp = mpf(n)
    t1 = (mpf(44) * pi**2) / (mpf(225) * sqrt(mpf(3))) * N_mp ** (mpf(-1) / 2)
    t2 = (pi * sqrt(mpf(2)) / 75) * sqrt(N_mp / (n_mp - 1)) \
         * sinh(pi * sqrt(mpf(2) * n_mp / 3) / N_mp)
    return t1 + t2


def find_N_hrr(n: int, tol: mpf = mpf("0.5")) -> int:
    """Smallest N such that the Rademacher tail bound is < tol.
    With tol=0.5 the integer round of the partial sum recovers p(n) exactly.
    """
    hi = 2
    while rademacher_tail_bound(hi, n) >= tol:
        hi *= 2
        if hi > 10**8:
            raise RuntimeError("Rademacher bound did not reach tol")
    lo = 1
    while lo < hi:
        mid = (lo + hi) // 2
        if rademacher_tail_bound(mid, n) < tol:
            hi = mid
        else:
            lo = mid + 1
    return lo


def compute_p_hrr(n: int) -> tuple[int, int, float]:
    """Compute p(n) via HRR with auto-precision and the rigorous truncation.

    Returns (p_value_as_int, N_terms_used, wall_seconds_for_the_sum).

    Working precision = ceil(log10(p(n))) + safety. We use the Hardy-Ramanujan
    asymptotic log p(n) ~ pi sqrt(2n/3) to size dps without circular reference.
    """
    # safety margin: enough to drown the Dedekind-sum cancellation noise
    log10_pn = float(pi * sqrt(mpf(2) * n / 3) / log(mpf(10)))
    dps_needed = max(50, int(log10_pn) + 30)
    mp.dps = dps_needed

    N = find_N_hrr(n)
    t0 = time.perf_counter()
    s = mpc(0)
    for k in range(1, N + 1):
        s += hrr_term(k, n)
    dt = time.perf_counter() - t0
    return int(nint(s.real)), N, dt


# -------- Driver / benchmark ----------------------------------------------

def main():
    out_path = Path(__file__).parent / "results" / "hrr_partition_benchmark.csv"
    out_path.parent.mkdir(exist_ok=True)

    ns = [10, 100, 1000, 10000, 100000]
    rows = []

    print(f"{'n':>8} {'method':<10} {'terms':>10} {'bits':>10} {'bits/term':>10} {'wall_s':>10} {'check':>8}")
    print("-" * 72)

    for n in ns:
        # ---- Method A: pentagonal recurrence (the table-builder cost) ----
        t0 = time.perf_counter()
        p_table, pent_terms = pentagonal_partitions(n)
        pent_time = time.perf_counter() - t0
        p_true = p_table[n]
        total_bits = p_true.bit_length()  # log2(p(n))
        bits_per_pent_term = total_bits / pent_terms if pent_terms else float("inf")
        rows.append(dict(
            n=n,
            method="pentagonal",
            terms=pent_terms,
            bits_per_term=bits_per_pent_term,
            total_bits=total_bits,
            wall_seconds=pent_time,
        ))
        print(f"{n:>8} {'pentagonal':<10} {pent_terms:>10d} {total_bits:>10d} "
              f"{bits_per_pent_term:>10.4f} {pent_time:>10.4f} {'-':>8}")

        # ---- Method B: HRR exact series with rigorous truncation ---------
        p_hrr, N_hrr, hrr_time = compute_p_hrr(n)
        match = (p_hrr == p_true)
        bits_per_hrr_term = total_bits / N_hrr if N_hrr else float("inf")
        rows.append(dict(
            n=n,
            method="hrr",
            terms=N_hrr,
            bits_per_term=bits_per_hrr_term,
            total_bits=total_bits,
            wall_seconds=hrr_time,
        ))
        print(f"{n:>8} {'hrr':<10} {N_hrr:>10d} {total_bits:>10d} "
              f"{bits_per_hrr_term:>10.4f} {hrr_time:>10.4f} {'OK' if match else 'FAIL':>8}")
        if not match:
            raise RuntimeError(
                f"HRR mismatch at n={n}: hrr={p_hrr} vs pent={p_true}"
            )

    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {out_path}")

    # Crossover analysis on bits/term and wall-time
    print("\nSummary: bits-per-term ratio (HRR / pentagonal) and wall ratio:")
    print(f"{'n':>8} {'bits/term ratio':>20} {'wall ratio':>15} {'terms ratio':>15}")
    by_n = {}
    for r in rows:
        by_n.setdefault(r["n"], {})[r["method"]] = r
    for n, both in by_n.items():
        pent = both["pentagonal"]; hrr = both["hrr"]
        bratio = hrr["bits_per_term"] / pent["bits_per_term"]
        tratio = hrr["wall_seconds"] / pent["wall_seconds"] if pent["wall_seconds"] > 0 else float("inf")
        nratio = pent["terms"] / hrr["terms"]
        print(f"{n:>8} {bratio:>20.2f} {tratio:>15.2f} {nratio:>15.2f}")
    print("\n  bits/term ratio > 1   -> HRR is more bit-dense per summand")
    print("  wall ratio      < 1   -> HRR is wall-clock faster")
    print("  terms ratio (pent/hrr) -> how many recurrence summands per HRR term")


if __name__ == "__main__":
    main()
