"""Hunt 5 — Quarterly Reports operator tagging.

Loads the hand-tagged QR section index
(`corpora/transcriptions/quarterly_reports/qr_section_index.json`) and tests
the HUNT_MAP §5 prediction:

    "5-10 operators recur 80%+ of the time"

operationalized as: ≥80% of mathematical sections in the Berndt 2022 HRJ
reproduction of the QRs are tagged with at least one of the 6 predicted
operators (mellin_inversion, master_theorem, q_shift, modular_S_transform,
eisenstein_normal_ordering, class_field_galois_average).

The tagging itself is hand-judgment — see diary 23 for the methodology. This
script just tallies and writes `analysis/results/qr_operator_tags.csv` and
`analysis/results/qr_hunt5_verdict.csv`.

Run:
    python analysis/23_hunt5_qr_operator_tagging.py
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = REPO_ROOT / "corpora/transcriptions/quarterly_reports/qr_section_index.json"
RESULTS_DIR = REPO_ROOT / "analysis/results"
TAGS_CSV = RESULTS_DIR / "qr_operator_tags.csv"
VERDICT_CSV = RESULTS_DIR / "qr_hunt5_verdict.csv"


# The 6 predicted operators from HUNT_MAP §5
PREDICTED_OPERATORS = {
    "mellin_inversion",
    "master_theorem",
    "q_shift",
    "modular_S_transform",
    "eisenstein_normal_ordering",
    "class_field_galois_average",
}


def load_sections() -> list[dict]:
    """Return flat list of section dicts with report/section info attached."""
    with open(INDEX_PATH) as f:
        index = json.load(f)
    out = []
    for report in index["reports"]:
        for section in report["sections"]:
            out.append(
                {
                    "report_id": report["report_id"],
                    "date": report["date"],
                    "section_id": section["section_id"],
                    "title": section["title"],
                    "type": section["type"],
                    "line_range": section["line_range"],
                    "is_meta": section.get("is_meta", False),
                    "operators_predicted_basis": section["operators_predicted_basis"],
                    "operators_extra": section["operators_extra"],
                    "in_predicted_basis": section["in_predicted_basis"],
                    "note": section.get("note", ""),
                }
            )
    return out


def write_tags_csv(sections: list[dict]) -> None:
    RESULTS_DIR.mkdir(exist_ok=True, parents=True)
    with open(TAGS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "report_id",
                "date",
                "section_id",
                "title",
                "type",
                "is_meta",
                "line_start",
                "line_end",
                "operators_predicted_basis",
                "operators_extra",
                "in_predicted_basis",
                "note",
            ],
        )
        writer.writeheader()
        for s in sections:
            writer.writerow(
                {
                    "report_id": s["report_id"],
                    "date": s["date"],
                    "section_id": s["section_id"],
                    "title": s["title"],
                    "type": s["type"],
                    "is_meta": s["is_meta"],
                    "line_start": s["line_range"][0],
                    "line_end": s["line_range"][1],
                    "operators_predicted_basis": ";".join(s["operators_predicted_basis"]),
                    "operators_extra": ";".join(s["operators_extra"]),
                    "in_predicted_basis": s["in_predicted_basis"],
                    "note": s["note"],
                }
            )


def compute_verdict(sections: list[dict]) -> dict:
    """Per-report and overall verdict on the HUNT_MAP §5 prediction.

    The 80%-recurrence prediction is tested over MATH-CONTENT sections only:
    we exclude `is_meta` sections (validity discussions, foundational
    interpolation arguments) since these are about the operators rather than
    using them.
    """
    rows = []
    by_report = {}
    for s in sections:
        if s["is_meta"]:
            continue
        rid = s["report_id"]
        by_report.setdefault(rid, []).append(s)
    by_report["ALL"] = [s for s in sections if not s["is_meta"]]

    for rid, items in by_report.items():
        n_total = len(items)
        n_in = sum(1 for s in items if s["in_predicted_basis"])
        pct = (n_in / n_total) if n_total else 0.0

        # Operator-occurrence counts (one section can use multiple operators)
        op_counter: Counter = Counter()
        extra_counter: Counter = Counter()
        for s in items:
            for op in s["operators_predicted_basis"]:
                op_counter[op] += 1
            for op in s["operators_extra"]:
                extra_counter[op] += 1

        rows.append(
            {
                "scope": rid,
                "n_math_sections": n_total,
                "n_in_predicted_basis": n_in,
                "pct_in_predicted_basis": round(pct * 100, 1),
                "meets_80pct_prediction": pct >= 0.80,
                "predicted_operator_uses": dict(op_counter),
                "extra_operator_uses": dict(extra_counter),
            }
        )

    return rows


def write_verdict_csv(verdict_rows: list[dict]) -> None:
    RESULTS_DIR.mkdir(exist_ok=True, parents=True)
    with open(VERDICT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "scope",
                "n_math_sections",
                "n_in_predicted_basis",
                "pct_in_predicted_basis",
                "meets_80pct_prediction",
                "predicted_operator_uses",
                "extra_operator_uses",
            ],
        )
        writer.writeheader()
        for r in verdict_rows:
            writer.writerow(
                {
                    **r,
                    "predicted_operator_uses": json.dumps(r["predicted_operator_uses"]),
                    "extra_operator_uses": json.dumps(r["extra_operator_uses"]),
                }
            )


def main() -> None:
    sections = load_sections()
    write_tags_csv(sections)
    verdict = compute_verdict(sections)
    write_verdict_csv(verdict)

    print(f"Wrote {len(sections)} section tags to {TAGS_CSV.relative_to(REPO_ROOT)}")
    print(f"Wrote {len(verdict)} verdict rows  to {VERDICT_CSV.relative_to(REPO_ROOT)}")
    print()
    print(
        f"{'scope':<6} {'n_math':>7} {'n_in_basis':>11} {'pct':>7} {'meets ≥80%?':>13}"
    )
    print("-" * 50)
    for r in verdict:
        meets = "YES" if r["meets_80pct_prediction"] else "NO"
        print(
            f"{r['scope']:<6} {r['n_math_sections']:>7} {r['n_in_predicted_basis']:>11} "
            f"{r['pct_in_predicted_basis']:>6.1f}% {meets:>13}"
        )
    print()

    overall = next(r for r in verdict if r["scope"] == "ALL")
    print("Predicted-basis operator usage (across all math sections):")
    for op in sorted(PREDICTED_OPERATORS):
        n = overall["predicted_operator_uses"].get(op, 0)
        marker = "  " if n > 0 else " *"
        print(f"  {marker}{op:<32s} {n} sections")
    n_unfired = sum(
        1 for op in PREDICTED_OPERATORS if overall["predicted_operator_uses"].get(op, 0) == 0
    )
    print(f"  ({n_unfired} of 6 predicted operators NEVER fire — marked *)")
    print()
    print("Operators outside the predicted basis (the empirical correction):")
    for op, n in sorted(overall["extra_operator_uses"].items(), key=lambda kv: -kv[1]):
        print(f"  {op:<40s} {n} sections")


if __name__ == "__main__":
    main()
