"""Analysis 34 — Verify + benchmark the annular Poisson Green modular kernel.

Tests
-----
1. AGREEMENT at the diary-51 test cell
   (theta_q=0.171, y_q=0.025, theta_s=0.170, y_s=0.024, L=0.05) between
   the Fourier-series form (large M) and the modular one-image form at
   dps=80. Diary claim: matches to >40 digits.

2. CONVERGENCE PROFILE for the Fourier series as a function of M, at the
   same (small-L, near-source) cell. Confirms the slow form really is
   slow there.

3. WALL-CLOCK BENCHMARK at three thicknesses L in {0.05, 0.1, 0.5} at
   dps=80, modular form vs Fourier-form-truncated-to-converged-precision.

4. EDGE CASE: at large L = 1.0 (annulus is not thin), the modular form's
   omitted-image error grows. Confirm the modular form still gives a
   sensible value relative to a high-M Fourier reference.

Outputs
-------
analysis/results/34_annular_green.csv
"""
from __future__ import annotations

import csv
import time
from pathlib import Path

import mpmath as mp

from rkc.pde.annular_green import annular_green_fourier, annular_green_modular


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


def case_agreement_diary_cell():
    """Diary 51 test cell at dps=80, M=100000 vs modular."""
    print("\n== Agreement @ diary-51 cell (L=0.05, dps=80) ==")
    args = dict(theta=0.171, y=0.025, phi=0.170, eta=0.024, L=0.05)

    mp.mp.dps = 80

    # Modular reference
    t0 = time.perf_counter()
    g_mod = annular_green_modular(**args)
    t_mod = time.perf_counter() - t0

    # Fourier with successively larger M, to see how slow it converges
    rows = []
    for M in [100, 1000, 10_000, 100_000]:
        t0 = time.perf_counter()
        g_f = annular_green_fourier(**args, M=M)
        t_f = time.perf_counter() - t0
        delta = mp.fabs(g_f - g_mod)
        agree_digits = -mp.log10(delta) if delta > 0 else mp.mpf("inf")
        print(f"  M={M:7}: |delta|={delta!s:<35}"
              f" agree_digits={float(agree_digits):.1f}"
              f" t_f={t_f:.3f}s")
        rows.append({
            "M": M,
            "abs_diff": float(delta),
            "agree_digits": float(agree_digits) if delta > 0 else 999.0,
            "t_fourier_s": t_f,
        })

    print(f"  modular ref:  G = {g_mod!s}")
    print(f"  modular time: {t_mod*1e3:.3f} ms")
    return g_mod, t_mod, rows


def case_benchmark_thicknesses():
    """Wall-clock at L = 0.05, 0.1, 0.5 at dps=80."""
    print("\n== Wall-clock benchmark @ dps=80, varying L ==")
    mp.mp.dps = 80

    cells = [
        # (L, theta_q, y_q, theta_s, y_s, M_fair_for_30dig)
        # For L=0.05 (thin), 30 digits needs roughly ~30/log10(e^{-y_<})
        # terms but really the limiter is e^{-delta*m} and delta~10^{-3},
        # so it's huge. We do M=100000 as a 'fair' baseline that already
        # gives ~50 digits per diary 51.
        (0.05, 0.171, 0.025, 0.170, 0.024, 100_000),
        # For L=0.1, the convergence is faster; M=50000 suffices.
        (0.1,  0.171, 0.05,  0.170, 0.04, 50_000),
        # For L=0.5, M=200 gives well-converged answers.
        (0.5,  0.171, 0.25,  0.170, 0.24, 500),
    ]
    rows = []
    for L, tq, yq, ts, ys, M in cells:
        # modular
        t_med_mod, _, _, g_mod = median_timing(
            annular_green_modular,
            (),
            dict(theta=tq, y=yq, phi=ts, eta=ys, L=L),
            repeats=5,
        )
        # fourier (1 run only when M is huge -- it's slow)
        repeats = 1 if M >= 10_000 else 3
        t_med_f, _, _, g_f = median_timing(
            annular_green_fourier,
            (),
            dict(theta=tq, y=yq, phi=ts, eta=ys, L=L, M=M),
            repeats=repeats,
        )
        delta = mp.fabs(g_mod - g_f)
        agree = -mp.log10(delta) if delta > 0 else mp.mpf("inf")
        speedup = t_med_f / t_med_mod
        print(f"  L={L:>4}: t_mod={t_med_mod*1e3:>8.3f} ms "
              f" t_f(M={M})={t_med_f*1e3:>10.2f} ms "
              f" speedup={speedup:>10.1f}x"
              f"  agree_digits={float(agree):.1f}")
        rows.append({
            "L": L, "M_fourier": M,
            "t_modular_s": t_med_mod,
            "t_fourier_s": t_med_f,
            "speedup": speedup,
            "abs_diff": float(delta),
            "agree_digits": float(agree) if delta > 0 else 999.0,
        })
    return rows


def case_edge_large_L():
    """At L=1, the omitted-image correction in the modular form is
    visible. Quantify."""
    print("\n== Edge case @ L=1 (NOT thin) ==")
    mp.mp.dps = 50
    args = dict(theta=0.5, y=0.5, phi=0.3, eta=0.4, L=1.0)
    g_mod = annular_green_modular(**args)
    g_f = annular_green_fourier(**args, M=300)
    delta = mp.fabs(g_f - g_mod)
    agree = -mp.log10(delta) if delta > 0 else mp.mpf("inf")
    print(f"  modular = {g_mod!s}")
    print(f"  fourier(M=300) = {g_f!s}")
    print(f"  |delta| = {delta!s}    agree_digits = {float(agree):.2f}")
    return {
        "L": 1.0, "M": 300,
        "abs_diff": float(delta),
        "agree_digits": float(agree),
    }


def main():
    here = Path(__file__).resolve().parent
    out_csv = here / "results" / "34_annular_green.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    g_mod, t_mod, agree_rows = case_agreement_diary_cell()
    bench_rows = case_benchmark_thicknesses()
    edge_row = case_edge_large_L()

    # Diary 51 claim: at L=0.05 with M=100000 the Fourier form takes
    # ~8.11 s and the modular form 1.14e-4 s, agreement 4e-47 digits.
    # We check (a) modular form agrees to >40 digits at L=0.05 vs the
    # converged Fourier reference and (b) modular is at least 100x faster.
    agree_target = 40
    speedup_target = 100

    best_agree = max(r["agree_digits"] for r in agree_rows)
    target_cell = next(r for r in bench_rows if abs(r["L"] - 0.05) < 1e-9)
    speedup_at_005 = target_cell["speedup"]

    exactness_ok = best_agree >= agree_target
    speedup_ok = speedup_at_005 >= speedup_target

    verdict = "CONFIRMED" if (exactness_ok and speedup_ok) else (
        "PARTIAL" if (exactness_ok or speedup_ok) else "FAILED"
    )

    # ----- write CSV -----
    header = [
        "case", "L", "M",
        "t_modular_s", "t_fourier_s",
        "speedup", "abs_diff", "agree_digits",
        "note",
    ]
    rows = []
    for r in agree_rows:
        rows.append({
            "case": "agreement_diary_cell", "L": 0.05, "M": r["M"],
            "t_modular_s": t_mod, "t_fourier_s": r["t_fourier_s"],
            "speedup": r["t_fourier_s"] / t_mod if t_mod > 0 else None,
            "abs_diff": r["abs_diff"], "agree_digits": r["agree_digits"],
            "note": "Fourier vs modular at L=0.05 diary cell",
        })
    for r in bench_rows:
        rows.append({
            "case": f"benchmark_L{r['L']}", "L": r["L"], "M": r["M_fourier"],
            "t_modular_s": r["t_modular_s"], "t_fourier_s": r["t_fourier_s"],
            "speedup": r["speedup"], "abs_diff": r["abs_diff"],
            "agree_digits": r["agree_digits"],
            "note": f"benchmark dps=80, L={r['L']}",
        })
    rows.append({
        "case": "edge_large_L", "L": edge_row["L"], "M": edge_row["M"],
        "t_modular_s": None, "t_fourier_s": None,
        "speedup": None, "abs_diff": edge_row["abs_diff"],
        "agree_digits": edge_row["agree_digits"],
        "note": "L=1 not-thin: modular drops accuracy",
    })

    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        for r in rows:
            w.writerow({h: r.get(h, "") for h in header})

    print()
    print("=" * 60)
    print(f"VERDICT (accelerator b, annular Green): {verdict}")
    print(f"  best agreement (Fourier-vs-modular @ L=0.05): {best_agree:.1f} digits")
    print(f"  speedup @ L=0.05 (modular vs Fourier M=100000): {speedup_at_005:.1f}x")
    print(f"  diary 51 claimed: ~7.1e4x speedup, ~46 digits agreement")
    print(f"  edge case L=1.0: only {edge_row['agree_digits']:.2f} digits agreement (expected)")
    print(f"  results -> {out_csv.relative_to(here.parent)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
