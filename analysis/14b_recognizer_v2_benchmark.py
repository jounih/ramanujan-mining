"""Experiment 14b — v2 benchmark, same 55-case battery, scored against rkc/.

Reuses the test cases from experiment 14 (v1) verbatim; only the recognizer
implementation under test is swapped to the rkc.* package. Output goes to
analysis/results/recognizer_routing_benchmark_v2.csv — v1's CSV is left
untouched for diff inspection.
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from collections import Counter
from importlib import import_module

# include analysis/ for the v1 benchmark module, and ramanujan/ for rkc
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

import sympy as sp  # noqa: E402
from mpmath import mpf  # noqa: E402

bench_v1 = import_module("14_recognizer_routing_benchmark")
CASES = bench_v1.CASES
n = bench_v1.n

from rkc import best_match, recognize_composite, Route  # noqa: E402


OUT_CSV = Path(__file__).parent / "results" / "recognizer_routing_benchmark_v2.csv"
OUT_CSV.parent.mkdir(exist_ok=True)


def evaluate(case):
    if case["cohort"] == "composed":
        cm = recognize_composite(case["expr"], n, target_precision=1e-12)
        if cm is not None and "composite" in cm.kernel and cm.components:
            comp_kernels = [c["kernel"] for c in cm.components]
            # for backward-compat scoring: pick whichever component is
            # accepted (if any), else the primary
            for ck in comp_kernels:
                if ck in case["accept_families"]:
                    return ck, cm.route.value, False, True
            return comp_kernels[0], cm.route.value, False, comp_kernels[0] in case["accept_families"]
    bm = best_match(case["expr"], n, target_precision=1e-12)
    if bm is None:
        predicted = "none"
        route = "NONE"
        degen = False
    else:
        predicted = bm.kernel
        route = bm.route.value
        degen = bm.degenerate is not None
    if case["expect_degenerate"]:
        correct = (predicted == case["true_family"]) and degen
    else:
        accept = case.get("accept_families", [case["true_family"]])
        correct = predicted in accept
    return predicted, route, degen, correct


def run():
    rows = []
    for case in CASES:
        predicted, route, degen, correct = evaluate(case)
        rows.append({
            "case_id": case["case_id"],
            "cohort": case["cohort"],
            "true_family": case["true_family"],
            "predicted_family": predicted,
            "route": route,
            "degenerate_flag": degen,
            "correct": correct,
            "comment": case["comment"],
        })

    with open(OUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "case_id", "cohort", "true_family", "predicted_family",
            "route", "degenerate_flag", "correct", "comment",
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} cases to {OUT_CSV}")
    print()

    # per-family table
    families = sorted(set([r["true_family"] for r in rows]) |
                      set([r["predicted_family"] for r in rows]))
    tp = Counter()
    fp = Counter()
    fn = Counter()
    accept_lookup = {c["case_id"]: set(c["accept_families"]) for c in CASES}
    for r in rows:
        accept = accept_lookup[r["case_id"]]
        if r["predicted_family"] in accept:
            tp[r["predicted_family"]] += 1
        else:
            fp[r["predicted_family"]] += 1
            fn[r["true_family"]] += 1

    print(f"{'family':<26} {'#true':>6} {'#pred':>6} {'TP':>4} {'FP':>4} {'FN':>4} "
          f"{'prec':>6} {'recall':>7} {'F1':>6}")
    print("-" * 80)
    total_correct = sum(1 for r in rows if r["correct"])
    macro_prec = []
    macro_rec = []
    for fam in families:
        n_true = sum(1 for c in CASES if fam in c["accept_families"])
        n_pred = sum(1 for r in rows if r["predicted_family"] == fam)
        t = tp[fam]
        prec = t / n_pred if n_pred > 0 else float("nan")
        rec = t / n_true if n_true > 0 else float("nan")
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else float("nan")
        print(f"{fam:<26} {n_true:>6} {n_pred:>6} {t:>4} {fp[fam]:>4} {fn[fam]:>4} "
              f"{prec:>6.2f} {rec:>7.2f} {f1:>6.2f}")
        if not math.isnan(prec):
            macro_prec.append(prec)
        if not math.isnan(rec):
            macro_rec.append(rec)
    print("-" * 80)
    macro_p = sum(macro_prec) / len(macro_prec) if macro_prec else float("nan")
    macro_r = sum(macro_rec) / len(macro_rec) if macro_rec else float("nan")
    print(f"{'MACRO AVG':<26} {'':>6} {'':>6} {'':>4} {'':>4} {'':>4} "
          f"{macro_p:>6.2f} {macro_r:>7.2f}")
    print(f"Overall accuracy: {total_correct}/{len(rows)} = "
          f"{total_correct/len(rows):.2%}")

    print()
    print("Cases that changed from v1 -> v2:")
    # Load v1 CSV for comparison
    v1_csv = Path(__file__).parent / "results" / "recognizer_routing_benchmark.csv"
    if v1_csv.exists():
        with open(v1_csv) as f:
            v1_rows = list(csv.DictReader(f))
        v1_by_id = {int(r["case_id"]): r for r in v1_rows}
        any_change = False
        for r in rows:
            v1r = v1_by_id.get(r["case_id"])
            if v1r is None:
                continue
            if (v1r["predicted_family"] != r["predicted_family"] or
                v1r["correct"] != str(r["correct"])):
                any_change = True
                print(f"  case {r['case_id']:>2}: v1 pred={v1r['predicted_family']} "
                      f"correct={v1r['correct']} -> v2 pred={r['predicted_family']} "
                      f"correct={r['correct']}")
        if not any_change:
            print("  (none)")
    return rows


if __name__ == "__main__":
    run()
