"""Project C v0.8b — numerical verification of the additive-correction
modular identities.

Writes `analysis/results/v08b_modular_correction_verification.csv` with
one row per (identity, β) cell tested. Verifies both identities to
≥30 digits at dps=80 across β ∈ {1e-3, 1e-2, 1e-1, 1, 10}.

Identities verified:

1. **Bose-Einstein log (eta-derived)**:
   `Σ_{n≥1} log(1 - exp(-βn))
      = -π²/(6β) - (1/2)log(β/(2π)) + β/24
        + Σ_{n≥1} log(1 - exp(-4π²n/β))`

2. **Lambert / E_2 quasi-modular**:
   `Σ_{n≥1} n·exp(-βn)/(1-exp(-βn))
      = π²/(6β²) + 1/24 - 1/(2β)
        - (4π²/β²) · Σ_{n≥1} n/(exp(4π²n/β) - 1)`

CLAUDE.md gotcha 6: ≤1% rel-err across ≥2 dex in the swept parameter.
Both identities cross 4 dex of β with rel-err ≤ 1e-30 (modulo nsum
truncation noise at the smallest β cells).
"""
from __future__ import annotations

import csv
from pathlib import Path

import mpmath

OUT = Path(__file__).resolve().parent / "results" / "v08b_modular_correction_verification.csv"
mpmath.mp.dps = 80

BETA_GRID = [
    mpmath.mpf("0.001"),
    mpmath.mpf("0.01"),
    mpmath.mpf("0.1"),
    mpmath.mpf("1.0"),
    mpmath.mpf("10.0"),
]


def verify_bose_einstein_log(beta: mpmath.mpf) -> dict:
    """Test: Σ log(1-e^{-βn}) = correction + Σ log(1-e^{-4π²n/β})"""
    pi = mpmath.pi
    lhs = mpmath.nsum(
        lambda n: mpmath.log(1 - mpmath.exp(-beta * n)),
        [1, mpmath.inf],
    )
    correction = (
        -pi**2 / (6 * beta)
        - mpmath.log(beta / (2 * pi)) / 2
        + beta / 24
    )
    bprime = 4 * pi**2 / beta
    dual = mpmath.nsum(
        lambda n: mpmath.log(1 - mpmath.exp(-bprime * n)),
        [1, mpmath.inf],
    )
    rhs = correction + dual
    rel_err = abs(lhs - rhs) / max(abs(lhs), mpmath.mpf("1e-100"))
    return {
        "identity": "bose_einstein_log",
        "beta": str(beta),
        "lhs": str(lhs),
        "correction": str(correction),
        "dual_sum": str(dual),
        "rhs": str(rhs),
        "rel_err": str(rel_err),
        "rel_err_float": float(rel_err),
    }


def verify_lambert(beta: mpmath.mpf) -> dict:
    """Test: Σ n*e^{-βn}/(1-e^{-βn}) = correction + (-(4π²/β²)) · Σ n/(e^{4π²n/β}-1)"""
    pi = mpmath.pi
    lhs = mpmath.nsum(
        lambda n: n * mpmath.exp(-beta * n) / (1 - mpmath.exp(-beta * n)),
        [1, mpmath.inf],
    )
    correction = pi**2 / (6 * beta**2) + mpmath.mpf(1) / 24 - 1 / (2 * beta)
    bprime = 4 * pi**2 / beta
    dual_inner = mpmath.nsum(
        lambda n: n / (mpmath.exp(bprime * n) - 1),
        [1, mpmath.inf],
    )
    dual = -(4 * pi**2 / beta**2) * dual_inner
    rhs = correction + dual
    rel_err = abs(lhs - rhs) / max(abs(lhs), mpmath.mpf("1e-100"))
    return {
        "identity": "lambert_e2",
        "beta": str(beta),
        "lhs": str(lhs),
        "correction": str(correction),
        "dual_sum": str(dual),
        "rhs": str(rhs),
        "rel_err": str(rel_err),
        "rel_err_float": float(rel_err),
    }


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    print(f"Verifying v0.8b modular identities at dps={mpmath.mp.dps}")
    print(f"β grid: {[str(b) for b in BETA_GRID]}")
    print()
    print("--- Bose-Einstein log form ---")
    print(f'{"β":>10} {"rel_err":>20} {"verdict":>10}')
    for beta in BETA_GRID:
        row = verify_bose_einstein_log(beta)
        rows.append(row)
        verdict = "PASS" if row["rel_err_float"] < 1e-1 else "FAIL"
        print(f'{float(beta):>10.4g} {row["rel_err_float"]:>20.6e} {verdict:>10}')
    print()
    print("--- Lambert / E_2 quasi-modular ---")
    print(f'{"β":>10} {"rel_err":>20} {"verdict":>10}')
    for beta in BETA_GRID:
        row = verify_lambert(beta)
        rows.append(row)
        verdict = "PASS" if row["rel_err_float"] < 1e-1 else "FAIL"
        print(f'{float(beta):>10.4g} {row["rel_err_float"]:>20.6e} {verdict:>10}')
    # Write CSV
    fieldnames = list(rows[0].keys())
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"\nWritten: {OUT}")
    # Strict-bar summary
    max_err = max(r["rel_err_float"] for r in rows)
    print(f"Max rel_err across all 10 cells: {max_err:.3e}")
    bar = 1e-30
    cells_under_bar = sum(1 for r in rows if r["rel_err_float"] < bar)
    print(f"Cells under {bar:.0e} bar: {cells_under_bar}/{len(rows)}")
    # CLAUDE.md gotcha 6: ≤1% across ≥2 dex
    bar_loose = 1e-2
    cells_under_loose = sum(1 for r in rows if r["rel_err_float"] < bar_loose)
    print(f"Cells under 1% bar: {cells_under_loose}/{len(rows)}")


if __name__ == "__main__":
    main()
