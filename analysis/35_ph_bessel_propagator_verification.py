"""Analysis 35 -- Verify + benchmark the PH Bessel-image propagator.

Tests
-----
1. EXACTNESS AT SMALL N, t. At N=8, t=2 (so 2*c*t=4), compare the Bessel-image
   propagator's predicted (q_n, p_n) for n = 0..N-1 against (a) Verlet
   integration with very small dt, and (b) the DFT modal-baseline (which is
   exact). The Bessel form should match DFT to ~1e-12 in double precision
   and Verlet to ~1e-4 with dt = 1e-4.

2. DIARY-53 TEST CELL. At N=2048, t=100, n=37, check the published value
   q_{37}(100) approx -0.04954556973216... (which equals J_74(200) for a
   single-image cell because the nearest omitted image has order |2*(37 + 2048)|
   = 4170 with J_4170(200) far below double-precision floor). Verify against
   J_74(200) directly (single-term truncation is the whole answer here).

3. ENERGY CONSERVATION. At various (n, t), construct the full chain state and
   compute H(t). For the linear chain the propagator is energy-conserving
   exactly. We confirm |H(t) - H(0)| is small (machine epsilon, since DFT
   is the spectral truth and the Bessel form agrees with it).

4. WALL-CLOCK BENCHMARK FOR SPARSE-OUTPUT QUERIES.  At N=2048, asking for
   one site at one time:
     - direct Verlet integration:  O(N * t/dt) work to walk to time t.
     - exact DFT modal evaluation: O(N log N) FFT (returns ALL sites).
     - Bessel-image one-cell:      O(L) where L is the Bessel truncation
                                    radius (a small constant when 2*c*t < N).
   The brief asks specifically for sparse-output benchmarking, so we time
   the case of "one site, one time" with all three.

Outputs
-------
analysis/results/35_ph_bessel_propagator.csv
"""
from __future__ import annotations

import csv
import math
import time
from pathlib import Path

import mpmath as mp
import numpy as np
import scipy.special as sp

from rkc.ph.bessel_image_propagator import (
    propagator_bessel,
    propagator_verlet,
    propagator_dft,
    chain_energy,
)


def median_timing(fn, args, kwargs, repeats=5):
    times = []
    last = None
    for _ in range(repeats):
        t0 = time.perf_counter()
        last = fn(*args, **kwargs)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    times.sort()
    return times[len(times) // 2], times[0], times[-1], last


def case_exactness_small():
    """N=8, t=2 -- compare Bessel form against Verlet (small dt) and DFT modal."""
    print("\n== Exactness @ small (N=8, t=2) ==")
    N, t, k, m = 8, 2.0, 1.0, 1.0

    # DFT modal -- exact for linear system
    q_dft, p_dft = propagator_dft(t, N, k, m)

    # Verlet at very fine dt
    q_v, p_v = propagator_verlet(t, N, k, m, dt=1e-4)

    # Bessel-image per site
    q_b = np.zeros(N)
    p_b = np.zeros(N)
    for n in range(N):
        q_b[n], p_b[n] = propagator_bessel(n, t, N, k, m, abs_tol=1e-30)

    max_diff_dft = float(np.max(np.abs(q_b - q_dft) + np.abs(p_b - p_dft)))
    max_diff_verlet = float(np.max(np.abs(q_b - q_v) + np.abs(p_b - p_v)))

    print(f"  bessel vs DFT:    max|q,p delta| = {max_diff_dft:.3e}")
    print(f"  bessel vs Verlet: max|q,p delta| = {max_diff_verlet:.3e} (dt=1e-4)")
    # Print the per-site q values
    for n in range(N):
        print(f"    n={n}: q_b={q_b[n]:+.6f}  q_dft={q_dft[n]:+.6f}  q_v={q_v[n]:+.6f}")
    return max_diff_dft, max_diff_verlet


def case_diary_cell():
    """Diary 53 cell: N=2048, t=100, n=37. Bessel form claims J_74(200)."""
    print("\n== Diary 53 cell (N=2048, t=100, n=37) ==")
    N, t, n = 2048, 100.0, 37

    # Direct: J_74(200)  (since 2*n = 74 and nearest image is order 4170)
    j74 = float(sp.jv(74, 200.0))
    j73 = float(sp.jv(73, 200.0))
    j75 = float(sp.jv(75, 200.0))
    p_direct = (j73 - j75)
    print(f"  direct J_74(200) = {j74!r}")
    print(f"  direct (J_73 - J_75)(200) = {p_direct!r}")
    print(f"  diary 53 claim:  q_{n}(100) ~ -0.04954556973216079712...")

    q_b, p_b = propagator_bessel(n, t, N, k=1.0, m=1.0, abs_tol=1e-50)
    print(f"  bessel form:    q = {q_b!r}")
    print(f"  bessel form:    p = {p_b!r}")

    # Cross-check with mpmath at higher precision (50 digits)
    mp.mp.dps = 50
    q_mp, p_mp = propagator_bessel(n, t, N, k=1.0, m=1.0, abs_tol=mp.mpf("1e-50"), use_mpmath=True)
    print(f"  bessel @ dps=50 q = {q_mp!s}")
    print(f"  bessel @ dps=50 p = {p_mp!s}")

    # Cross-check with DFT modal -- this is independent
    qdft, pdft = propagator_dft(t, N, k=1.0, m=1.0)
    q_d, p_d = qdft[n], pdft[n]
    print(f"  DFT modal:      q = {q_d!r}")
    print(f"  DFT modal:      p = {p_d!r}")

    diff_q = abs(q_b - q_d)
    diff_p = abs(p_b - p_d)
    print(f"  bessel vs DFT:  |dq|={diff_q:.3e}  |dp|={diff_p:.3e}")

    return {
        "q_bessel": q_b, "p_bessel": p_b,
        "q_dft": q_d, "p_dft": p_d,
        "diff_q": diff_q, "diff_p": diff_p,
        "diff_vs_diary_q": abs(q_b - (-0.0495455697321607971201928832022)),
    }


def case_energy_conservation():
    """Verify the full chain state at several times satisfies H(t) = H(0)."""
    print("\n== Energy conservation (N=64) ==")
    N, k, m = 64, 1.0, 1.0
    # H(0): only q[0] = 1, rest zero -> potential = (k/2) * 2 = k
    H0 = chain_energy(np.array([1.0] + [0.0] * (N - 1)), np.zeros(N), k, m)
    print(f"  H(0) = {H0!r}")
    rows = []
    for t in [0.5, 1.0, 5.0, 10.0]:
        q = np.zeros(N); p = np.zeros(N)
        for n in range(N):
            q[n], p[n] = propagator_bessel(n, t, N, k, m, abs_tol=1e-30)
        H = chain_energy(q, p, k, m)
        drift = abs(H - H0)
        print(f"  t={t:>5}: H(t)={H!r}  drift={drift:.3e}")
        rows.append({"t": t, "H": H, "H0": H0, "drift": drift})
    return rows


def case_benchmark_sparse():
    """Sparse-output benchmark: one site, one time, N=2048."""
    print("\n== Wall-clock benchmark (sparse: one site, one time) ==")
    N, t, n = 2048, 100.0, 37
    k, m = 1.0, 1.0

    # Bessel-image for the single site -- using scipy in double precision
    def fn_bessel():
        return propagator_bessel(n, t, N, k, m, abs_tol=1e-15)

    # DFT modal for all sites (then index n)
    def fn_dft():
        qall, pall = propagator_dft(t, N, k, m)
        return qall[n], pall[n]

    # Verlet to time t at dt = 0.01 / omega_max (small but realistic)
    def fn_verlet():
        return propagator_verlet(t, N, k, m, dt=0.01)[0][n]

    t_b_med, _, _, _ = median_timing(fn_bessel, (), {}, repeats=20)
    t_d_med, _, _, _ = median_timing(fn_dft, (), {}, repeats=20)
    # Verlet is expensive at large t; only 3 runs
    t_v_med, _, _, _ = median_timing(fn_verlet, (), {}, repeats=3)

    print(f"  bessel-image:     {t_b_med*1e6:8.1f} us")
    print(f"  dft (all sites):  {t_d_med*1e6:8.1f} us")
    print(f"  verlet (full int):{t_v_med*1e6:10.1f} us")
    print(f"  bessel vs DFT speedup:    {t_d_med / t_b_med:7.2f}x")
    print(f"  bessel vs Verlet speedup: {t_v_med / t_b_med:7.2f}x")

    return {
        "N": N, "t": t, "n": n,
        "t_bessel_s": t_b_med, "t_dft_s": t_d_med, "t_verlet_s": t_v_med,
        "speedup_vs_dft": t_d_med / t_b_med,
        "speedup_vs_verlet": t_v_med / t_b_med,
    }


def main():
    here = Path(__file__).resolve().parent
    out_csv = here / "results" / "35_ph_bessel_propagator.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    small_dft, small_v = case_exactness_small()
    diary = case_diary_cell()
    energy_rows = case_energy_conservation()
    bench = case_benchmark_sparse()

    # Verdict
    exactness_ok = (small_dft < 1e-10)
    diary_match_ok = (diary["diff_vs_diary_q"] < 1e-12) and (diary["diff_q"] < 1e-10)
    energy_ok = all(r["drift"] < 1e-10 for r in energy_rows)
    # The brief specifies "sparse-output queries" -- the speedup against DFT
    # should be substantial because DFT computes all N sites.
    speedup_ok = bench["speedup_vs_dft"] > 1.0  # any speedup at all

    if exactness_ok and diary_match_ok and energy_ok:
        verdict = "CONFIRMED"
    elif exactness_ok and energy_ok:
        verdict = "PARTIAL"
    else:
        verdict = "FAILED"

    header = [
        "case", "N", "n", "t",
        "metric", "value", "note",
    ]
    rows = [
        {"case": "exactness_small", "N": 8, "n": "all", "t": 2,
         "metric": "max_diff_bessel_vs_dft", "value": small_dft, "note": "should be ~1e-15"},
        {"case": "exactness_small", "N": 8, "n": "all", "t": 2,
         "metric": "max_diff_bessel_vs_verlet_dt1e-4", "value": small_v,
         "note": "Verlet sanity, ~1e-4 dt^2"},
        {"case": "diary_cell", "N": 2048, "n": 37, "t": 100,
         "metric": "q_bessel", "value": diary["q_bessel"], "note": ""},
        {"case": "diary_cell", "N": 2048, "n": 37, "t": 100,
         "metric": "q_dft", "value": diary["q_dft"], "note": ""},
        {"case": "diary_cell", "N": 2048, "n": 37, "t": 100,
         "metric": "diff_q_vs_diary", "value": diary["diff_vs_diary_q"],
         "note": "diary 53 published value"},
        {"case": "diary_cell", "N": 2048, "n": 37, "t": 100,
         "metric": "diff_q_bessel_vs_dft", "value": diary["diff_q"], "note": ""},
    ]
    for r in energy_rows:
        rows.append({
            "case": "energy_conservation", "N": 64, "n": "all", "t": r["t"],
            "metric": "energy_drift", "value": r["drift"], "note": f"H(t)={r['H']}",
        })
    rows.append({
        "case": "benchmark_sparse_N2048", "N": 2048, "n": 37, "t": 100,
        "metric": "t_bessel_s", "value": bench["t_bessel_s"], "note": "",
    })
    rows.append({
        "case": "benchmark_sparse_N2048", "N": 2048, "n": 37, "t": 100,
        "metric": "t_dft_s", "value": bench["t_dft_s"], "note": "",
    })
    rows.append({
        "case": "benchmark_sparse_N2048", "N": 2048, "n": 37, "t": 100,
        "metric": "t_verlet_s", "value": bench["t_verlet_s"], "note": "dt=0.01",
    })
    rows.append({
        "case": "benchmark_sparse_N2048", "N": 2048, "n": 37, "t": 100,
        "metric": "speedup_vs_dft", "value": bench["speedup_vs_dft"], "note": "",
    })
    rows.append({
        "case": "benchmark_sparse_N2048", "N": 2048, "n": 37, "t": 100,
        "metric": "speedup_vs_verlet_dt0.01", "value": bench["speedup_vs_verlet"], "note": "",
    })
    rows.append({
        "case": "verdict", "N": "", "n": "", "t": "",
        "metric": "overall", "value": verdict,
        "note": "exact={} diary={} energy={} speedup>1={}".format(
            exactness_ok, diary_match_ok, energy_ok, speedup_ok),
    })

    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        for r in rows:
            w.writerow({h: r.get(h, "") for h in header})

    print()
    print("=" * 60)
    print(f"VERDICT (accelerator c, PH Bessel propagator): {verdict}")
    print(f"  exactness @ N=8, t=2: bessel-vs-DFT = {small_dft:.2e}")
    print(f"  diary cell (N=2048, t=100, n=37) bessel-vs-diary  = {diary['diff_vs_diary_q']:.2e}")
    print(f"  energy drift: max = {max(r['drift'] for r in energy_rows):.2e}")
    print(f"  sparse-output speedup: bessel vs DFT = {bench['speedup_vs_dft']:.2f}x;"
          f"  vs Verlet = {bench['speedup_vs_verlet']:.2f}x")
    print(f"  diary 53 claim: ~95x vs DFT")
    print(f"  results -> {out_csv.relative_to(here.parent)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
