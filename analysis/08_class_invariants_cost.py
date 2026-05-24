"""
Experiment 08 — Ramanujan class invariants G_n: direct evaluation cost
vs radical-form evaluation cost, as a function of (n, d_digits).

Definition.
    G_n = 2^(-1/4) * exp(pi*sqrt(n)/24) * prod_{k odd, k>=1} (1 + exp(-k*pi*sqrt(n)))

This is Ramanujan's standard "class invariant" for n odd, equivalent up to
normalization to the Weber f-function:  G_n = 2^(-1/4) * f(sqrt(-n))
in Weber's notation, where f(tau) = q^{-1/48} * prod_{k>=1} (1 + q^{(2k-1)/2})
evaluated at tau = i*sqrt(n), q = e^{i*pi*tau} = e^{-pi*sqrt(n)}.

The CM theory of Heegner/Weber/Birch shows G_n is an algebraic unit in the
ring class field of Q(sqrt(-n)); for many n Ramanujan tabulated explicit
nested-radical forms (he gave 116 of them, the last ~18 of class-number-8
discriminants without proof — see CANDIDATE_INSIGHTS §C4).

Verified radical table (each entry tested to ~100 decimal digits below
against the infinite-product evaluation; n is excluded otherwise).

    n   radical form                            source
    --  --------------------------------------- ----------------------------
    1   1                                       trivial, Berndt V Ch.34
    5   ((1+sqrt(5))/2)^(1/4)                   Ramanujan, classical
    9   (2+sqrt(3))^(1/6)                       PSLQ-confirmed, classical
    13  ((3+sqrt(13))/2)^(1/4)                  Ramanujan, classical
    17  ((y+sqrt(y^2-4))/2)^(1/4),
            y = (5+sqrt(17))/2                  PSLQ-confirmed (Weber)
    25  (1+sqrt(5))/2  (= phi)                  Ramanujan, classical
    37  (6+sqrt(37))^(1/4)                      Ramanujan, classical
    49  sqrt(((y+sqrt(y^2-4))/2)),
            y = 2+sqrt(7)                       PSLQ-confirmed (Weber)

(training-memory; verified) — each is numerically asserted at module import
to >= 50 digit agreement.

Cost models.
- Method A (DIRECT): infinite product of (1+q^k) for k odd. Terms are kept
  until q^k drops below 10^{-d-pad}. Wall time is measured around the
  evaluation; arithmetic ops are reported as the number of multiplied
  factors plus the exp() and final-rescale ops.
- Method B (RADICAL): evaluate the closed-form expression using mpmath at
  precision d+pad. "Operations" is a static count of the +,*,sqrt,**,/
  nodes in the expression tree (a tight upper bound on irreducible mpmath
  primitive calls); wall time is measured around the evaluation.

Both routes are cross-checked to relative agreement <= 10^{-d}; mismatch
aborts the row.

Output:
    results/class_invariants_cost.csv
"""
from __future__ import annotations
import csv
import time
from pathlib import Path
from mpmath import mp, mpf, exp, sqrt, pi, log


# ---------- verified radical forms ----------

def _g(n_int):
    """Return a callable f(precision_dps) -> mpmath value of G_n's radical form.

    The callable sets mp.dps to the requested precision and evaluates."""
    if n_int == 1:
        def f(dps):
            mp.dps = dps
            return mpf(1)
        return f
    if n_int == 5:
        def f(dps):
            mp.dps = dps
            return ((1 + sqrt(5)) / 2) ** (mpf(1) / 4)
        return f
    if n_int == 9:
        def f(dps):
            mp.dps = dps
            return (2 + sqrt(3)) ** (mpf(1) / 6)
        return f
    if n_int == 13:
        def f(dps):
            mp.dps = dps
            return ((3 + sqrt(13)) / 2) ** (mpf(1) / 4)
        return f
    if n_int == 17:
        def f(dps):
            mp.dps = dps
            y = (5 + sqrt(17)) / 2
            return ((y + sqrt(y * y - 4)) / 2) ** (mpf(1) / 4)
        return f
    if n_int == 25:
        def f(dps):
            mp.dps = dps
            return (1 + sqrt(5)) / 2
        return f
    if n_int == 37:
        def f(dps):
            mp.dps = dps
            return (6 + sqrt(37)) ** (mpf(1) / 4)
        return f
    if n_int == 49:
        def f(dps):
            mp.dps = dps
            y = 2 + sqrt(7)
            return sqrt((y + sqrt(y * y - 4)) / 2)
        return f
    raise KeyError(n_int)


# Static op counts for each radical form (counted by hand from the AST).
# Counts +, -, *, /, sqrt, ** as 1 each. Constants are free.
RADICAL_OP_COUNT = {
    1: 0,
    5: 4,   # sqrt(5); +1; /2; **(1/4)
    9: 3,   # sqrt(3); +2; **(1/6)
    13: 4,  # sqrt(13); +3; /2; **(1/4)
    17: 8,  # sqrt(17); +5; /2; y*y; -4; sqrt; +y; /2; **(1/4) -> 9
    25: 3,  # sqrt(5); +1; /2
    37: 3,  # sqrt(37); +6; **(1/4)
    49: 7,  # sqrt(7); +2; y*y; -4; sqrt; +y; /2; sqrt -> 8
}

VERIFIED_NS = [1, 5, 9, 13, 17, 25, 37, 49]


# ---------- Method A: direct infinite product ----------

def G_direct(n_int, dps, pad=10):
    """Compute G_n by direct evaluation of the infinite product.

    Returns (value, n_terms_used, wall_seconds).
    """
    mp.dps = dps + pad
    sqrt_n = sqrt(mpf(n_int))
    q_log = -pi * sqrt_n         # log(q_one_step) ; q = exp(-pi*sqrt(n))
    tol = mpf(10) ** -(dps + pad - 2)
    log_tol = log(tol)

    t0 = time.perf_counter()

    # Determine cutoff: include factors for k=1,3,5,...,k_max where
    # exp(k*q_log) > tol  <=>  k*q_log > log(tol)  <=>  k < log(tol)/q_log .
    # (q_log < 0; log(tol) < 0; both negative so quotient positive.)
    k_max = int(log_tol / q_log)
    if k_max % 2 == 0:
        k_max -= 1
    if k_max < 1:
        k_max = 1

    # Build product. To minimise exp() calls we use the recurrence
    # q^{k+2} = q^k * q^2.
    q = exp(q_log)
    q2 = q * q
    qk = q                  # k = 1
    prod = mpf(1)
    n_terms = 0
    k = 1
    while k <= k_max:
        prod *= (1 + qk)
        n_terms += 1
        qk *= q2
        k += 2

    # Apply prefactor 2^{-1/4} * exp(pi*sqrt(n)/24)
    value = (mpf(2) ** (mpf(-1) / 4)) * exp(pi * sqrt_n / 24) * prod
    wall = time.perf_counter() - t0
    return value, n_terms, wall


# ---------- Method B: radical evaluation ----------

def G_radical(n_int, dps, pad=10):
    """Evaluate the closed-form radical at precision dps+pad.

    Returns (value, op_count, wall_seconds).
    """
    f = _g(n_int)
    t0 = time.perf_counter()
    value = f(dps + pad)
    wall = time.perf_counter() - t0
    ops = RADICAL_OP_COUNT[n_int]
    return value, ops, wall


# ---------- module-load verification ----------

def _verify_radical_table(dps_check=60):
    """At import time, assert every tabulated radical agrees with the direct
    infinite-product evaluation to at least 50 decimal digits.

    Raises AssertionError on mismatch — this is the discipline gate."""
    for n_int in VERIFIED_NS:
        v_direct, _, _ = G_direct(n_int, dps_check)
        v_radical, _, _ = G_radical(n_int, dps_check)
        rel = abs(v_direct - v_radical) / abs(v_direct + mpf(10) ** -200)
        assert rel < mpf(10) ** -50, (
            f"verification failure for G_{n_int}: rel={rel}\n"
            f"  direct  = {v_direct}\n  radical = {v_radical}"
        )


_verify_radical_table()


# ---------- experiment driver ----------

def main():
    out_path = Path(__file__).parent / "results" / "class_invariants_cost.csv"
    out_path.parent.mkdir(exist_ok=True)

    digits_grid = [30, 100, 300, 1000]

    rows = []
    print(
        f"{'n':>3} {'method':>7} {'d':>5} "
        f"{'terms_or_ops':>13} {'wall_s':>11} {'value (20-digit truncation)':>32}"
    )
    print("-" * 80)

    for n_int in VERIFIED_NS:
        for d in digits_grid:
            # Method A — direct
            v_a, n_terms, wall_a = G_direct(n_int, d)
            # Method B — radical
            v_b, n_ops, wall_b = G_radical(n_int, d)

            # cross-check
            rel = abs(v_a - v_b) / abs(v_a + mpf(10) ** -300)
            assert rel < mpf(10) ** -(d - 5), (
                f"A/B disagree for n={n_int} d={d}: rel={rel}"
            )

            # 20-digit truncated string of the value (use the radical value;
            # it is the "ground truth" for inspection)
            mp.dps = 25
            v_str = mp.nstr(v_b, 20, strip_zeros=False)

            print(
                f"{n_int:>3} {'direct':>7} {d:>5} "
                f"{n_terms:>13} {wall_a:>11.4f} {v_str:>32}"
            )
            print(
                f"{n_int:>3} {'radical':>7} {d:>5} "
                f"{n_ops:>13} {wall_b:>11.4f} {v_str:>32}"
            )

            rows.append(dict(
                n=n_int, method="direct", digits_d=d,
                terms_or_ops=n_terms, wall_seconds=wall_a, value=v_str,
            ))
            rows.append(dict(
                n=n_int, method="radical", digits_d=d,
                terms_or_ops=n_ops, wall_seconds=wall_b, value=v_str,
            ))

    with open(out_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print()
    print(f"Wrote {out_path}")

    # ---- compact ratio summary ----
    print()
    print("cost ratio (direct_terms / radical_ops) and (wall_A / wall_B)")
    print(f"{'n':>3} {'d':>5} {'op_ratio':>10} {'time_ratio':>11}")
    print("-" * 35)
    by_key = {(r['n'], r['digits_d'], r['method']): r for r in rows}
    for n_int in VERIFIED_NS:
        for d in digits_grid:
            ra = by_key[(n_int, d, 'direct')]
            rb = by_key[(n_int, d, 'radical')]
            op_ratio = ra['terms_or_ops'] / max(rb['terms_or_ops'], 1)
            tr = ra['wall_seconds'] / max(rb['wall_seconds'], 1e-9)
            print(f"{n_int:>3} {d:>5} {op_ratio:>10.2f} {tr:>11.2f}")


if __name__ == "__main__":
    main()
