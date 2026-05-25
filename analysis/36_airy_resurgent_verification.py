"""Analysis 36 -- Verify + benchmark the Airy Tricomi-U closed form.

Tests
-----
1. ACCURACY vs mp.airyai(-x) at x in {5, 10, 20, 50, 100} at dps=70.
   Diary 56 claims all cells should match to 30+ digits; we expect
   close to dps precision (~70 digits).

2. WALL-CLOCK BENCHMARK at the same cells, Tricomi-U vs:
   - mp.airyai(-x) itself (the "industry standard" baseline)
   - Borel-Pade [10/10] with numerical Laplace quadrature
     (the "current resurgent practice" baseline)

3. EDGE CASES:
   - small x (x = 0.1, 0.5): Tricomi form is meant for x large enough
     that the WKB-asymptotic representation makes sense. Quantify how
     accuracy degrades.
   - very large x (x = 1000, 10000): does it still work?

Outputs
-------
analysis/results/36_airy_resurgent.csv
"""
from __future__ import annotations

import csv
import time
from pathlib import Path

import mpmath as mp

from rkc.special.airy_resurgent import (
    airy_ai_neg_tricomi,
    airy_ai_neg_borel_pade,
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


def case_accuracy_table():
    """Per-x accuracy + timing summary, dps=70."""
    print("\n== Accuracy + timing, dps=70 ==")
    mp.mp.dps = 70
    cells = [5, 10, 20, 50, 100]
    rows = []
    for x in cells:
        ref = mp.airyai(-x)

        # Tricomi form
        t_tri_med, _, _, val_tri = median_timing(
            airy_ai_neg_tricomi, (x,), {}, repeats=10
        )
        diff_tri = abs(val_tri - ref)
        digits_tri = float(-mp.log10(diff_tri)) if diff_tri > 0 else 999.0

        # mp.airyai baseline
        t_ref_med, _, _, _ = median_timing(
            mp.airyai, (-x,), {}, repeats=10
        )

        # Borel-Pade baseline
        t_bp_med, _, _, val_bp = median_timing(
            airy_ai_neg_borel_pade, (x,), dict(n_coefs=21, pade_order=10), repeats=3
        )
        diff_bp = abs(val_bp - ref)
        digits_bp = float(-mp.log10(diff_bp)) if diff_bp > 0 else 999.0

        speedup_vs_bp = t_bp_med / t_tri_med if t_tri_med > 0 else None
        speedup_vs_ref = t_ref_med / t_tri_med if t_tri_med > 0 else None
        print(
            f"  x={x:>5}: "
            f"tri={t_tri_med*1e3:>8.2f} ms ({digits_tri:>5.1f} digits)  "
            f"bp={t_bp_med*1e3:>8.2f} ms ({digits_bp:>5.1f} digits)  "
            f"mp.airyai={t_ref_med*1e3:>8.2f} ms  "
            f"vs_bp={speedup_vs_bp:>6.2f}x  vs_ref={speedup_vs_ref:>6.2f}x"
        )
        rows.append({
            "x": x,
            "t_tricomi_ms": t_tri_med * 1e3,
            "t_borel_pade_ms": t_bp_med * 1e3,
            "t_mp_airyai_ms": t_ref_med * 1e3,
            "digits_tricomi": digits_tri,
            "digits_borel_pade": digits_bp,
            "speedup_tricomi_vs_borel_pade": speedup_vs_bp,
            "speedup_tricomi_vs_mp_airyai": speedup_vs_ref,
        })
    return rows


def case_edge_small_x():
    """Small x: WKB-asymptotic representation is poorly conditioned."""
    print("\n== Edge case: small x (sub-WKB regime) ==")
    mp.mp.dps = 50
    rows = []
    for x in [0.1, 0.5, 1.0, 2.0]:
        ref = mp.airyai(-x)
        try:
            val = airy_ai_neg_tricomi(x)
            diff = abs(val - ref)
            digits = float(-mp.log10(diff)) if diff > 0 else 999.0
            print(f"  x={x}: agree_digits={digits:.2f}")
        except Exception as e:
            digits = -999.0
            print(f"  x={x}: FAILED with {e!r}")
        rows.append({"x": x, "digits": digits})
    return rows


def case_edge_very_large_x():
    """Very large x: confirm robustness."""
    print("\n== Edge case: very large x ==")
    mp.mp.dps = 70
    rows = []
    for x in [1000, 10_000]:
        ref = mp.airyai(-x)
        val = airy_ai_neg_tricomi(x)
        diff = abs(val - ref)
        digits = float(-mp.log10(diff)) if diff > 0 else 999.0
        print(f"  x={x}: agree_digits={digits:.2f}")
        rows.append({"x": x, "digits": digits})
    return rows


def main():
    here = Path(__file__).resolve().parent
    out_csv = here / "results" / "36_airy_resurgent.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    table_rows = case_accuracy_table()
    small_x_rows = case_edge_small_x()
    large_x_rows = case_edge_very_large_x()

    # Verdict criteria
    # diary 56 claim: 30+ digits at all cells, 50-113x faster than Borel-Pade
    digits_ok = all(r["digits_tricomi"] >= 30 for r in table_rows)
    speedup_ok = any(r["speedup_tricomi_vs_borel_pade"] >= 10 for r in table_rows)
    if digits_ok and speedup_ok:
        verdict = "CONFIRMED"
    elif digits_ok:
        verdict = "PARTIAL"
    else:
        verdict = "FAILED"

    header = [
        "case", "x", "dps",
        "t_tricomi_ms", "t_borel_pade_ms", "t_mp_airyai_ms",
        "digits_tricomi", "digits_borel_pade",
        "speedup_vs_borel_pade", "speedup_vs_mp_airyai",
        "note",
    ]
    rows = []
    for r in table_rows:
        rows.append({
            "case": "accuracy_main", "x": r["x"], "dps": 70,
            "t_tricomi_ms": r["t_tricomi_ms"],
            "t_borel_pade_ms": r["t_borel_pade_ms"],
            "t_mp_airyai_ms": r["t_mp_airyai_ms"],
            "digits_tricomi": r["digits_tricomi"],
            "digits_borel_pade": r["digits_borel_pade"],
            "speedup_vs_borel_pade": r["speedup_tricomi_vs_borel_pade"],
            "speedup_vs_mp_airyai": r["speedup_tricomi_vs_mp_airyai"],
            "note": "",
        })
    for r in small_x_rows:
        rows.append({
            "case": "edge_small_x", "x": r["x"], "dps": 50,
            "t_tricomi_ms": None, "t_borel_pade_ms": None, "t_mp_airyai_ms": None,
            "digits_tricomi": r["digits"],
            "digits_borel_pade": None,
            "speedup_vs_borel_pade": None, "speedup_vs_mp_airyai": None,
            "note": "small x; sub-WKB",
        })
    for r in large_x_rows:
        rows.append({
            "case": "edge_large_x", "x": r["x"], "dps": 70,
            "t_tricomi_ms": None, "t_borel_pade_ms": None, "t_mp_airyai_ms": None,
            "digits_tricomi": r["digits"],
            "digits_borel_pade": None,
            "speedup_vs_borel_pade": None, "speedup_vs_mp_airyai": None,
            "note": "very large x",
        })
    rows.append({
        "case": "verdict", "x": "", "dps": "",
        "t_tricomi_ms": None, "t_borel_pade_ms": None, "t_mp_airyai_ms": None,
        "digits_tricomi": None, "digits_borel_pade": None,
        "speedup_vs_borel_pade": None, "speedup_vs_mp_airyai": None,
        "note": verdict,
    })
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        for r in rows:
            w.writerow({h: r.get(h, "") for h in header})

    min_digits = min(r["digits_tricomi"] for r in table_rows)
    max_speedup = max(
        (r["speedup_tricomi_vs_borel_pade"] for r in table_rows
         if r["speedup_tricomi_vs_borel_pade"] is not None),
        default=None,
    )
    print()
    print("=" * 60)
    print(f"VERDICT (accelerator d, Airy Tricomi-U): {verdict}")
    print(f"  min digits across {{5,10,20,50,100}}: {min_digits:.1f} (target: 30+)")
    print(f"  max speedup vs Borel-Pade:           {max_speedup:.2f}x (claimed 50-113x)")
    print(f"  small-x edge: digits at x=0.1 = {small_x_rows[0]['digits']:.2f}")
    print(f"  large-x edge: digits at x=10000 = {large_x_rows[-1]['digits']:.2f}")
    print(f"  results -> {out_csv.relative_to(here.parent)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
