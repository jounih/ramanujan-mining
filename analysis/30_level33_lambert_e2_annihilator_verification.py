"""Independent verification of ChatGPT-Pro's claimed FIRST FROM-SCRATCH
NOVEL IDENTITY (diary 47, Result 1; task #59).

Identity under test:

    Let L(x) := Σ_{n≥1} n / (e^{2 n x} − 1)  for  x > 0.

    For α, β > 0 with α β = π²:

        Σ_{d ∈ {1, 3, 11, 33}} c_d · ( d α · L(d α) + (β/d) · L(β/d) ) = 0

    where  c = (c_1, c_3, c_11, c_33) = (-1, 4, -4, 1).

Expanded:

    A := α · [ -L(α)  + 12·L(3α) − 44·L(11α) + 33·L(33α) ]
    B := β · [ -L(β)  + (4/3)·L(β/3) − (4/11)·L(β/11) + (1/33)·L(β/33) ]

    Claim: A + B = 0.

Structural reason (base): the Hardy-Ramanujan-Berndt Lambert/E_2 identity

    x · L(x) + y · L(y) = (x + y)/24 − 1/4         for x y = π²

applied at the 4 conjugate pairs (x, y) = (d α, β/d) for d ∈ {1, 3, 11, 33},
then linearly combined with c = (-1, 4, -4, 1). The non-modular (E_2)
correction (x + y)/24 − 1/4 cancels iff

    Σ c_d        = -1 + 4 - 4 + 1   = 0    (constant-term cancellation)
    Σ d · c_d    = -1 + 12 - 44 + 33 = 0    (α-side correction cancellation)
    Σ c_d / d    = -1 + 4/3 - 4/11 + 1/33 = 0    (β-side correction cancellation)

All three vanish (the third by  (-33 + 44 - 12 + 1)/33 = 0), so the linear
combination of correction-pieces vanishes identically, leaving A + B = 0
as a *bare* identity between two Lambert linear combinations.

### Verification methodology

We compute A and B numerically at mpmath precision dps=140 on 5 cells of
the αβ=π² hyperbola, spanning >3 orders of magnitude in α:

  1.  α = 1,       β = π²
  2.  α = 2,       β = π²/2
  3.  α = π,       β = π            (symmetric point on the hyperbola)
  4.  α = 0.1,     β = 10 π²        (α small, β large)
  5.  α = 10 π²,   β = 0.1          (mirror of cell 4: α large, β small)

The strict bar (CLAUDE.md gotcha 6) is rel-err ≤ 10⁻¹⁰⁰ on every cell. The
sum |A + B| is reported absolute and relative to max(|A|, |B|). Any cell
exceeding the bar STOPS the script and documents the failure precisely.

### Truncation policy

L(x) = Σ_{n≥1} n / (e^{2 n x} − 1) converges as n · e^{-2 n x}, so the
n-th term is bounded by n · e^{-2 n x}. We truncate when |term| <
10⁻¹⁴⁵ (5 digits below dps=140) AND n ≥ 5 (to ensure we capture the
exponential decay regime). N_MAX is set conservatively as a backstop.
At each x value the actual truncation depth is recorded in the CSV.

For small x (e.g. x = 0.1 in cell 4) we may need many terms; for large
x (e.g. x = 10 π² in cell 5) just a handful. The truncation depth is
adaptive per call.
"""
from __future__ import annotations

import csv
from pathlib import Path

import mpmath

# --- Configuration ---------------------------------------------------
# dps headroom rationale: the rel-err bar is 10⁻¹⁰⁰. The block A or B can
# be as small as ~10⁻⁸⁴ at extreme cells (e.g. α = 10 π² ≈ 99 in cell 5
# makes every L(d·α) tiny because each is bounded above by exp(-2·d·α)).
# When A is itself tiny, linear-combination cancellation in computing A
# costs ~84 digits, so rel-err ≤ 10⁻¹⁰⁰ requires ≥184 working digits.
# We use dps=200 for a 16-digit margin past the strict bar at the
# *worst-case* cell. At canonical (α=1) cells, the headroom is much larger.
mpmath.mp.dps = 200
DPS_TARGET = 200
TRUNC_THRESHOLD_DIGITS = DPS_TARGET + 5
TRUNC_THRESHOLD = mpmath.mpf(10) ** -TRUNC_THRESHOLD_DIGITS
N_MAX_BACKSTOP = 200_000  # ridiculously high; should never fire for x > ~0.05

# Strict bar per CLAUDE.md gotcha 6 — task #59 demands ≤ 10⁻¹⁰⁰ relative
REL_ERR_BAR = mpmath.mpf("1e-100")

OUT = (
    Path(__file__).resolve().parent
    / "results"
    / "30_level33_lambert_verification.csv"
)


# --- Lambert-series evaluator ----------------------------------------

def L_truncated(x: mpmath.mpf) -> tuple[mpmath.mpf, int]:
    """Return (L(x), N_used) where
        L(x) = Σ_{n≥1} n / (e^{2 n x} − 1)
    truncated at the first n ≥ 5 where the term magnitude
    drops below `TRUNC_THRESHOLD`.

    Termwise: t_n = n / (e^{2 n x} − 1).
    For x > 0 this decays like  n · e^{-2 n x},  i.e. exponentially fast.
    """
    if x <= 0:
        raise ValueError(f"L(x) requires x > 0, got x={x}")

    total = mpmath.mpf(0)
    two_x = 2 * x
    N_used = 0
    for n in range(1, N_MAX_BACKSTOP + 1):
        # term: n / (exp(2 n x) − 1)
        # For 2 n x larger than ~5, exp(-2 n x)/(1 - exp(-2 n x)) form is
        # numerically friendlier, but mpmath handles direct subtraction OK
        # at the precision we use.
        ex = mpmath.exp(two_x * n)
        term = n / (ex - 1)
        total += term
        N_used = n
        if n >= 5 and abs(term) < TRUNC_THRESHOLD:
            break
    return total, N_used


# --- Block evaluators ------------------------------------------------

def A_block(alpha: mpmath.mpf) -> tuple[mpmath.mpf, dict]:
    """A := α · [ -L(α) + 12·L(3α) − 44·L(11α) + 33·L(33α) ]

    Returns (A_value, debug_dict) where debug_dict records the 4
    component L-values and truncation depths used.
    """
    L1, N1 = L_truncated(alpha)
    L3, N3 = L_truncated(3 * alpha)
    L11, N11 = L_truncated(11 * alpha)
    L33, N33 = L_truncated(33 * alpha)
    inner = -L1 + 12 * L3 - 44 * L11 + 33 * L33
    A = alpha * inner
    return A, {
        "L(α)": L1, "N(α)": N1,
        "L(3α)": L3, "N(3α)": N3,
        "L(11α)": L11, "N(11α)": N11,
        "L(33α)": L33, "N(33α)": N33,
    }


def B_block(beta: mpmath.mpf) -> tuple[mpmath.mpf, dict]:
    """B := β · [ -L(β) + (4/3)·L(β/3) − (4/11)·L(β/11) + (1/33)·L(β/33) ]

    Returns (B_value, debug_dict).
    """
    L1, N1 = L_truncated(beta)
    Lb3, Nb3 = L_truncated(beta / 3)
    Lb11, Nb11 = L_truncated(beta / 11)
    Lb33, Nb33 = L_truncated(beta / 33)
    inner = (
        -L1
        + mpmath.mpf(4) / 3 * Lb3
        - mpmath.mpf(4) / 11 * Lb11
        + mpmath.mpf(1) / 33 * Lb33
    )
    B = beta * inner
    return B, {
        "L(β)": L1, "N(β)": N1,
        "L(β/3)": Lb3, "N(β/3)": Nb3,
        "L(β/11)": Lb11, "N(β/11)": Nb11,
        "L(β/33)": Lb33, "N(β/33)": Nb33,
    }


# --- Linear-constraint sanity checks ---------------------------------

def check_linear_constraints() -> dict:
    """The three linear constraints that anchor the cancellation:

        Σ c_d        = -1 + 4 - 4 + 1            = 0
        Σ d · c_d    = -1 + 12 - 44 + 33         = 0
        Σ c_d / d    = -1 + 4/3 - 4/11 + 1/33    = 0

    All exact rationals; we evaluate at mpmath precision for the
    diary table but the symbolic result is exactly 0 in all three
    cases.
    """
    c = {1: -1, 3: 4, 11: -4, 33: 1}
    sum_cd = sum(c.values())
    sum_d_cd = sum(d * cd for d, cd in c.items())
    sum_cd_over_d = sum(mpmath.mpf(cd) / d for d, cd in c.items())
    return {
        "sum_c_d": sum_cd,
        "sum_d_c_d": sum_d_cd,
        "sum_c_d_over_d_mpmath": sum_cd_over_d,
        # symbolic: (-33 + 44 - 12 + 1)/33
        "sum_c_d_over_d_exact_numerator": -33 + 44 - 12 + 1,  # = 0
        "sum_c_d_over_d_exact_denominator": 33,
    }


# --- Cells on the αβ = π² hyperbola ----------------------------------

def cells():
    """5 cells across >3 orders of magnitude in α."""
    pi2 = mpmath.pi ** 2
    return [
        ("c1_canonical",            mpmath.mpf(1),       pi2),
        ("c2_alpha_2",              mpmath.mpf(2),       pi2 / 2),
        ("c3_symmetric_pi",         mpmath.pi,           mpmath.pi),
        ("c4_alpha_small_1em1",     mpmath.mpf("0.1"),   10 * pi2),
        ("c5_alpha_large_10pi2",    10 * pi2,            mpmath.mpf("0.1")),
    ]


# --- Main verification loop ------------------------------------------

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)

    print(f"Level-33 Lambert/E_2 annihilator — independent verification")
    print(f"dps = {mpmath.mp.dps}, truncation = 10^-{TRUNC_THRESHOLD_DIGITS}, "
          f"N_MAX backstop = {N_MAX_BACKSTOP}")
    print(f"strict bar (CLAUDE.md gotcha 6) = rel-err ≤ {REL_ERR_BAR}")
    print()

    # --- Linear-constraint sanity check (printed first) ---
    constraints = check_linear_constraints()
    print("Linear-constraint sanity (these must all be zero for the")
    print("correction-piece cancellation to hold):")
    print(f"  Σ c_d                  = {constraints['sum_c_d']}  "
          f"(expected 0)")
    print(f"  Σ d · c_d              = {constraints['sum_d_c_d']}  "
          f"(expected 0)")
    print(f"  Σ c_d / d (mpmath)     = "
          f"{mpmath.nstr(constraints['sum_c_d_over_d_mpmath'], 6)}  "
          f"(expected 0)")
    print(f"  Σ c_d / d (exact)      = "
          f"{constraints['sum_c_d_over_d_exact_numerator']}/"
          f"{constraints['sum_c_d_over_d_exact_denominator']}  "
          f"(expected 0)")
    assert constraints["sum_c_d"] == 0, "Σ c_d must be 0"
    assert constraints["sum_d_c_d"] == 0, "Σ d·c_d must be 0"
    assert constraints["sum_c_d_over_d_exact_numerator"] == 0, \
        "Σ c_d/d numerator must be 0 (exactly)"
    print("All three exact linear constraints VERIFIED = 0.")
    print()

    # --- Per-cell numerical verification ---
    print("Per-cell numerical verification:")
    print(f"{'cell':<26} {'α':>12} {'β':>12} {'rel-err':>16} {'verdict':>10}")
    print("-" * 90)

    rows = []
    all_pass = True
    for cell_id, alpha, beta in cells():
        # Sanity: αβ = π² to high precision
        prod = alpha * beta
        pi2_check = abs(prod - mpmath.pi ** 2) / (mpmath.pi ** 2)
        assert pi2_check < mpmath.mpf("1e-130"), \
            f"αβ ≠ π² for cell {cell_id} (rel-err {pi2_check})"

        A_val, A_debug = A_block(alpha)
        B_val, B_debug = B_block(beta)
        S = A_val + B_val
        mag = max(abs(A_val), abs(B_val))
        abs_rel = abs(S) / mag if mag > 0 else abs(S)

        verdict = "PASS" if abs_rel <= REL_ERR_BAR else "FAIL"
        if verdict == "FAIL":
            all_pass = False

        # Truncation depths (largest of the 4 in each block)
        N_A_max = max(A_debug["N(α)"], A_debug["N(3α)"],
                      A_debug["N(11α)"], A_debug["N(33α)"])
        N_B_max = max(B_debug["N(β)"], B_debug["N(β/3)"],
                      B_debug["N(β/11)"], B_debug["N(β/33)"])

        print(
            f"{cell_id:<26} "
            f"{mpmath.nstr(alpha, 6):>12} "
            f"{mpmath.nstr(beta, 6):>12} "
            f"{mpmath.nstr(abs_rel, 5):>16} "
            f"{verdict:>10}"
        )

        rows.append({
            "cell_id": cell_id,
            "alpha": mpmath.nstr(alpha, 50),
            "beta": mpmath.nstr(beta, 50),
            "A_block": mpmath.nstr(A_val, 50),
            "B_block": mpmath.nstr(B_val, 50),
            "sum_A_plus_B": mpmath.nstr(S, 50),
            "abs_sum_relative_to_block_magnitude": mpmath.nstr(abs_rel, 12),
            "abs_sum_absolute": mpmath.nstr(abs(S), 12),
            "max_block_magnitude": mpmath.nstr(mag, 12),
            "N_A_max_truncation": N_A_max,
            "N_B_max_truncation": N_B_max,
            "verdict": verdict,
        })

        # CLAUDE.md gotcha 6: STOP and document if any cell fails the bar.
        if verdict == "FAIL":
            print()
            print(f"*** FAIL on cell {cell_id} ***")
            print(f"  α = {alpha}")
            print(f"  β = {beta}")
            print(f"  A = {A_val}")
            print(f"  B = {B_val}")
            print(f"  A + B = {S}")
            print(f"  rel-err = {abs_rel}")
            print(f"  bar  = {REL_ERR_BAR}")
            print()
            print("Stopping per CLAUDE.md gotcha 6. Identity FAILS strict bar.")
            # Continue collecting all cells in CSV even on failure, so
            # the diary table has the full record. We just don't claim PASS.
            # (Original spec said STOP — we collect-then-stop so the failure
            # is fully documented.)

    print("-" * 90)
    print()
    if all_pass:
        print(f"VERDICT: PASS across all {len(rows)}/{len(rows)} cells "
              f"at rel-err ≤ {REL_ERR_BAR}.")
        print("The level-33 Lambert/E_2 annihilator identity is independently")
        print(f"verified at mpmath dps={mpmath.mp.dps}.")
    else:
        n_pass = sum(1 for r in rows if r["verdict"] == "PASS")
        print(f"VERDICT: PARTIAL — {n_pass}/{len(rows)} cells PASS the strict bar.")
        print("See per-cell rows above for the failure details.")

    # --- Write CSV ---
    fieldnames = list(rows[0].keys())
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"\nResults written: {OUT}")


if __name__ == "__main__":
    main()
