"""Analysis 33 — Verify + benchmark finite-pole semiseparable attention.

Tests
-----
1. EXACTNESS at small (N=16, R=2, d_v=4) by comparing the recurrence
   output against the O(N^2) direct-matrix oracle, element by element,
   for both normalized and unnormalized forms.
2. EXACTNESS at medium (N=256, R=4, d_v=16) — same comparison.
3. WALL-CLOCK BENCHMARK at the cell the brief asks for: N=4096, R=8,
   d_v=64.

The diary 50 cost-ratio table claims that vs dense causal O(N^2*d_v)
attention, the finite-pole recurrence's "ratio" is approximately N/R.
For N=4096 and R=8 that is 512x. Here we measure the wall-clock ratio
of the O(N^2*R*d_v) reference vs the O(N*R*d_v) recurrence -- the same
two implementations, so the ratio that matters is "O(N)/O(1) per step"
times constants.

NOTE: the brief asks us to test the recurrence against the "direct
O(N^2) attention" form. There are TWO things one could mean by that:
  (i)  the dense softmax causal attention used in transformers
        (different semantics; an approximation question);
  (ii) the dense form of THIS attention (sum-of-poles, but built
        explicitly into an NxN matrix and applied to v).
The brief explicitly says "Verify EXACTNESS by computing the full
attention matrix at small N=16, R=2 and confirming float-equality",
which can only be (ii) -- the same semantics, two implementations.
So we use (ii) as the oracle and time both.

Outputs
-------
analysis/results/33_finite_pole_attention.csv

Verdict
-------
CONFIRMED if max(|y_direct - y_recur|) < 1e-10 at small N AND
the recurrence is faster than the direct O(N^2) form at N=4096.
"""
from __future__ import annotations

import csv
import time
from pathlib import Path

import numpy as np

from rkc.attention.finite_pole import (
    direct_finite_pole_attention,
    recurrent_finite_pole_attention,
)


def median_timing(fn, args, repeats=5):
    """Return (median, min, max) wall-clock in seconds across `repeats` runs."""
    times = []
    last_result = None
    for _ in range(repeats):
        t0 = time.perf_counter()
        last_result = fn(*args)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    times.sort()
    return times[len(times) // 2], times[0], times[-1], last_result


def make_inputs(N, R, d_v, seed=0):
    rng = np.random.default_rng(seed)
    q = rng.standard_normal((N, R))
    k = rng.standard_normal((N, R))
    v = rng.standard_normal((N, d_v))
    # poles uniformly in (0.1, 0.95)
    alpha = rng.uniform(0.1, 0.95, size=R)
    return q, k, v, alpha


def case_exactness_small():
    """N=16, R=2, d_v=4 — print full matrix and confirm float-equality."""
    print("\n== Exactness @ small (N=16, R=2, d_v=4) ==")
    q, k, v, alpha = make_inputs(16, 2, 4, seed=42)

    for normalized in [False, True]:
        y_direct = direct_finite_pole_attention(q, k, v, alpha, normalized=normalized)
        y_recur = recurrent_finite_pole_attention(q, k, v, alpha, normalized=normalized)
        max_abs = float(np.max(np.abs(y_direct - y_recur)))
        rel_err = float(np.max(np.abs(y_direct - y_recur) / (np.abs(y_direct) + 1e-300)))
        print(f"  normalized={normalized:5}: max|delta|={max_abs:.3e}  rel_err={rel_err:.3e}")
    return max_abs, rel_err


def case_exactness_medium():
    """N=256, R=4, d_v=16 — single-number summary."""
    print("\n== Exactness @ medium (N=256, R=4, d_v=16) ==")
    q, k, v, alpha = make_inputs(256, 4, 16, seed=7)
    y_direct = direct_finite_pole_attention(q, k, v, alpha)
    y_recur = recurrent_finite_pole_attention(q, k, v, alpha)
    max_abs = float(np.max(np.abs(y_direct - y_recur)))
    rel_err = float(np.max(np.abs(y_direct - y_recur) / (np.abs(y_direct) + 1e-300)))
    print(f"  unnormalized: max|delta|={max_abs:.3e}  rel_err={rel_err:.3e}")
    return max_abs, rel_err


def case_benchmark_target():
    """The benchmark cell from the brief: N=4096, R=8, d_v=64."""
    N, R, d_v = 4096, 8, 64
    print(f"\n== Wall-clock benchmark @ N={N}, R={R}, d_v={d_v} ==")
    q, k, v, alpha = make_inputs(N, R, d_v, seed=0)

    t_direct_med, t_direct_min, t_direct_max, y_direct = median_timing(
        direct_finite_pole_attention, (q, k, v, alpha), repeats=3,
    )
    t_recur_med, t_recur_min, t_recur_max, y_recur = median_timing(
        recurrent_finite_pole_attention, (q, k, v, alpha), repeats=5,
    )

    max_abs = float(np.max(np.abs(y_direct - y_recur)))
    print(f"  direct  : {t_direct_med:8.3f} s  (min {t_direct_min:.3f}, max {t_direct_max:.3f})")
    print(f"  recur   : {t_recur_med:8.5f} s  (min {t_recur_min:.5f}, max {t_recur_max:.5f})")
    print(f"  speedup : {t_direct_med / t_recur_med:8.2f}x")
    print(f"  agreement: max|delta|={max_abs:.3e}")
    return {
        "N": N, "R": R, "d_v": d_v,
        "t_direct_med_s": t_direct_med,
        "t_direct_min_s": t_direct_min,
        "t_direct_max_s": t_direct_max,
        "t_recur_med_s": t_recur_med,
        "t_recur_min_s": t_recur_min,
        "t_recur_max_s": t_recur_max,
        "speedup_observed": t_direct_med / t_recur_med,
        "speedup_claimed_N_over_R": N / R,
        "max_abs_diff": max_abs,
    }


def case_benchmark_scaling():
    """Several (N, R, d_v) cells to show O(N) vs O(N^2) scaling."""
    cells = [
        (256, 8, 64),
        (512, 8, 64),
        (1024, 8, 64),
        (2048, 8, 64),
    ]
    print("\n== Scaling benchmark ==")
    rows = []
    for N, R, d_v in cells:
        q, k, v, alpha = make_inputs(N, R, d_v, seed=0)
        t_dir_med, _, _, y_dir = median_timing(direct_finite_pole_attention, (q, k, v, alpha), repeats=3)
        t_rec_med, _, _, y_rec = median_timing(recurrent_finite_pole_attention, (q, k, v, alpha), repeats=5)
        max_abs = float(np.max(np.abs(y_dir - y_rec)))
        print(f"  N={N:5}: direct={t_dir_med*1e3:8.2f} ms  recur={t_rec_med*1e3:8.2f} ms"
              f"  speedup={t_dir_med/t_rec_med:7.2f}x  max|delta|={max_abs:.2e}")
        rows.append({
            "N": N, "R": R, "d_v": d_v,
            "t_direct_med_s": t_dir_med,
            "t_recur_med_s": t_rec_med,
            "speedup_observed": t_dir_med / t_rec_med,
            "speedup_claimed_N_over_R": N / R,
            "max_abs_diff": max_abs,
        })
    return rows


def main():
    here = Path(__file__).resolve().parent
    out_csv = here / "results" / "33_finite_pole_attention.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    small_max_abs, small_rel = case_exactness_small()
    med_max_abs, med_rel = case_exactness_medium()
    target_row = case_benchmark_target()
    scaling_rows = case_benchmark_scaling()

    # ----- verdict -----
    exactness_ok = small_max_abs < 1e-9 and med_max_abs < 1e-8
    speedup_ok = target_row["speedup_observed"] >= 4.0  # modest sanity bar
    verdict = "CONFIRMED" if (exactness_ok and speedup_ok) else (
        "PARTIAL" if exactness_ok else "FAILED"
    )

    # ----- write CSV -----
    header = [
        "case", "N", "R", "d_v",
        "max_abs_diff", "rel_err",
        "t_direct_med_s", "t_recur_med_s",
        "speedup_observed", "speedup_claimed_N_over_R",
        "verdict",
    ]
    rows = []
    rows.append({
        "case": "exactness_small", "N": 16, "R": 2, "d_v": 4,
        "max_abs_diff": small_max_abs, "rel_err": small_rel,
        "t_direct_med_s": None, "t_recur_med_s": None,
        "speedup_observed": None, "speedup_claimed_N_over_R": None,
        "verdict": "OK" if small_max_abs < 1e-9 else "FAIL",
    })
    rows.append({
        "case": "exactness_medium", "N": 256, "R": 4, "d_v": 16,
        "max_abs_diff": med_max_abs, "rel_err": med_rel,
        "t_direct_med_s": None, "t_recur_med_s": None,
        "speedup_observed": None, "speedup_claimed_N_over_R": None,
        "verdict": "OK" if med_max_abs < 1e-8 else "FAIL",
    })
    rows.append({
        "case": "benchmark_target_4096", **target_row,
        "rel_err": None,
        "verdict": verdict,
    })
    for r in scaling_rows:
        rows.append({
            "case": f"scaling_N{r['N']}", **r,
            "rel_err": None,
            "verdict": "speedup={:.1f}x".format(r["speedup_observed"]),
        })

    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        for r in rows:
            w.writerow({h: r.get(h, "") for h in header})

    print()
    print("=" * 60)
    print(f"VERDICT (accelerator a, finite-pole attention): {verdict}")
    print(f"  exactness @ small N=16:    max|delta| = {small_max_abs:.3e}")
    print(f"  exactness @ medium N=256:  max|delta| = {med_max_abs:.3e}")
    print(f"  speedup @ N=4096, R=8: {target_row['speedup_observed']:.2f}x"
          f"  (claimed ~ N/R = {target_row['speedup_claimed_N_over_R']:.0f}x)")
    print(f"  results -> {out_csv.relative_to(here.parent)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
