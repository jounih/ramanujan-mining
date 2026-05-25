"""ADVERSARIAL VERIFICATION of the INFINITE FAMILY of E_2 Lambert
annihilator identities at squarefree composite levels (diary 55,
commit `4150472`).

The family (from ChatGPT-Pro, paraphrased):

    For Lambert series  L(x) = Σ_{n≥1} n / (e^{2 n x} − 1)  and the
    "conjugate-pair block"
        T_d(α, β) := d·α·L(d·α) + (β/d)·L(β/d)
    with the constraint  α·β = π²,

    For every squarefree N = p·q with primes  p < q, there is a UNIQUE
    (up to scale) non-trivial 4-divisor annihilator

        Σ_{d | pq}  c_d · T_d(α, β)  =  0

    with closed-form integer coefficients

        (c_1, c_p, c_q, c_pq) = (−δ, m, −m, δ)
        where  g = gcd(p·q − 1, q − p),
                δ = (q − p)/g,
                m = (p·q − 1)/g.

Diary 48 (commit `ba13b38`) verified Level 33 = 3·11 to rel-err ≤ 10⁻¹⁰⁰
at dps=200.  ChatGPT-Pro then verified 7 NEW levels {35, 51, 65, 77, 87,
95, 115} to rel-err ≤ 10⁻¹⁰⁰ at dps=120 in their own environment.  This
script's job is to:

  (1) INDEPENDENTLY VERIFY the 7 new levels in OUR env at dps=200, 5
      cells each, rel-err ≤ 10⁻¹⁰⁰ bar.

  (2) ADVERSARIAL EDGE CASES:
        - Twin primes:           N ∈ {35=5·7, 143=11·13, 323=17·19}
        - Far-apart primes:      N ∈ {95=5·19, 187=11·17, 391=17·23}
        - p = 2 (small prime):   N ∈ {6=2·3, 10=2·5, 14=2·7, 22=2·11}
      For each, compute the closed-form coefficients and verify
      numerically at 5 cells.  If any fail the strict bar, the family
      claim is broken.

  (3) STRUCTURAL EXTENSIONS (most likely to break):

        (a) 3-prime squarefree  N = p·q·r:  8 divisors, 3 linear
            constraints  ⇒  5-DIMENSIONAL annihilator space.  Compute
            the rational nullspace basis and verify the lowest-height
            integer annihilator that uses ALL 8 divisors numerically.
            Tested:  N ∈ {30=2·3·5, 105=3·5·7, 165=3·5·11}.

        (b) Prime power  N = p²:  3 divisors, 3 linear constraints  ⇒
            generically 0-dimensional annihilator space.  Tested:
            N ∈ {49=7², 121=11²}.  Expected verdict: NO ANNIHILATOR;
            the family does NOT extend.

        (c) Composite with repeated prime  N = p²·q:  6 divisors, 3
            linear constraints  ⇒  3-DIMENSIONAL annihilator space.
            Tested:  N ∈ {18=3²·2, 45=3²·5}.  Verify any
            full-divisor-support annihilator numerically.

  (4) LITERATURE DIFF — see companion diary 58 for full search log.
      (PDF grep + arxiv WebFetch run separately; results recorded in
      diary entry, not in this script's CSV.)

  (5) MULTI-TOOL TRIANGULATION — the Hardy-Ramanujan-Berndt base
      identity is verified IN THE SCRIPT first, so that if it fails
      we KNOW the whole construction is bogus before testing
      anything downstream.

Verdict rule per cell:  rel-err ≤ 10⁻¹⁰⁰.

Output CSV at  analysis/results/32_level_pq_family_verification.csv.
"""
from __future__ import annotations

import csv
from fractions import Fraction
from functools import reduce
from math import gcd
from pathlib import Path

import mpmath
import sympy as sp

# ----------------------- Configuration ------------------------------

# dps headroom rationale: identical to analysis/30 — the rel-err bar is
# 10⁻¹⁰⁰; in some extreme cells the T_d-block can be as small as ~10⁻⁸⁴
# so the cancellation can cost ~84 digits.  dps=200 gives 16-digit
# margin at the worst case; canonical α=1 cells have much more headroom.
mpmath.mp.dps = 200
DPS_TARGET = 200
TRUNC_THRESHOLD_DIGITS = DPS_TARGET + 5
TRUNC_THRESHOLD = mpmath.mpf(10) ** -TRUNC_THRESHOLD_DIGITS
N_MAX_BACKSTOP = 500_000

# Strict bar per CLAUDE.md gotcha 6
REL_ERR_BAR = mpmath.mpf("1e-100")

OUT = (
    Path(__file__).resolve().parent
    / "results"
    / "32_level_pq_family_verification.csv"
)


# ----------------------- Lambert evaluator --------------------------

def L_truncated(x: mpmath.mpf) -> tuple[mpmath.mpf, int]:
    """L(x) = Σ_{n≥1} n / (e^{2nx} − 1), truncated when |term| < threshold."""
    if x <= 0:
        raise ValueError(f"L(x) requires x > 0, got x={x}")
    total = mpmath.mpf(0)
    two_x = 2 * x
    N_used = 0
    for n in range(1, N_MAX_BACKSTOP + 1):
        ex = mpmath.exp(two_x * n)
        term = n / (ex - 1)
        total += term
        N_used = n
        if n >= 5 and abs(term) < TRUNC_THRESHOLD:
            break
    return total, N_used


def T_block(d: int, alpha: mpmath.mpf, beta: mpmath.mpf) -> mpmath.mpf:
    """T_d(α, β) := d·α·L(d·α) + (β/d)·L(β/d).

    Note: the formula uses single-divisor d, not its complementary
    divisor — even when d > sqrt(N).  The complementarity is captured
    by α ↔ β/d^2 (modular inversion), not by d ↔ N/d.
    """
    xa = d * alpha
    xb = beta / d
    La, _ = L_truncated(xa)
    Lb, _ = L_truncated(xb)
    return xa * La + xb * Lb


# ----------------------- Coefficient formula ------------------------

def coefficients_pq(p: int, q: int) -> dict[int, int]:
    """Closed-form (c_1, c_p, c_q, c_pq) for squarefree N = p·q, p < q.

    Returns dict {divisor: coefficient}.
    """
    if not (p < q):
        raise ValueError(f"need p < q, got p={p}, q={q}")
    if gcd(p, q) != 1:
        raise ValueError(f"need gcd(p, q) = 1, got p={p}, q={q}")
    pq = p * q
    diff = q - p
    pqm1 = pq - 1
    g = gcd(pqm1, diff)
    delta = diff // g
    m = pqm1 // g
    return {1: -delta, p: m, q: -m, pq: delta}


def check_linear_constraints(coeffs: dict[int, int]) -> dict:
    """Return the three linear-constraint values + a boolean PASS flag.

    All three must vanish exactly for the family construction to work.
    """
    s_c = sum(coeffs.values())
    s_dc = sum(d * c for d, c in coeffs.items())
    s_cd_rational = sum(Fraction(c, d) for d, c in coeffs.items())
    return {
        "sum_c": s_c,
        "sum_d_c": s_dc,
        "sum_c_over_d": s_cd_rational,
        "passes": (s_c == 0 and s_dc == 0 and s_cd_rational == 0),
    }


# ------------------ Rational nullspace for extensions ---------------

def rational_nullspace_basis(divisors: list[int]) -> list[list[int]]:
    """Compute integer basis vectors for the kernel of the 3×n
    constraint matrix [[1...1], [d_1..d_n], [1/d_1..1/d_n]] using
    sympy exact rationals; each basis vector is rescaled to be
    integer with gcd = 1 (and orientation chosen so c_1 ≤ 0 if c_1 != 0).
    """
    A = sp.Matrix([
        [sp.Integer(1)] * len(divisors),
        [sp.Integer(d) for d in divisors],
        [sp.Rational(1, d) for d in divisors],
    ])
    ns = A.nullspace()
    out: list[list[int]] = []
    for v in ns:
        denoms = [c.q for c in v]
        common_denom = reduce(sp.lcm, denoms, sp.Integer(1))
        cleared = [int(c * common_denom) for c in v]
        g = reduce(gcd, [abs(c) for c in cleared if c != 0], 0)
        if g > 0:
            cleared = [c // g for c in cleared]
        # canonical sign: if c_1 > 0 flip
        if cleared[0] > 0:
            cleared = [-c for c in cleared]
        out.append(cleared)
    return out


def full_support_combination(
    basis: list[list[int]], divisors: list[int]
) -> tuple[list[int], list[int]]:
    """Return an integer linear combination of basis vectors that has
    NONZERO coefficient on EVERY divisor (i.e. uses all divisors).
    The combination coefficients are returned alongside the result.

    Strategy: try coefficients (1, 1, ..., 1) first; if that has zeros,
    perturb with (1, 2, 1, 1, ...) etc. until full support is achieved.
    """
    n_div = len(divisors)
    n_basis = len(basis)

    def combine(weights: list[int]) -> list[int]:
        return [
            sum(w * b[i] for w, b in zip(weights, basis))
            for i in range(n_div)
        ]

    # Try a few weight patterns
    candidates: list[list[int]] = []
    # uniform
    candidates.append([1] * n_basis)
    # bumps
    for i in range(n_basis):
        w = [1] * n_basis
        w[i] = 2
        candidates.append(w)
    for i in range(n_basis):
        w = [1] * n_basis
        w[i] = 3
        candidates.append(w)
    # primes
    for i in range(n_basis):
        w = [1] * n_basis
        w[i] = 5
        candidates.append(w)

    for w in candidates:
        combo = combine(w)
        if all(c != 0 for c in combo):
            # reduce by gcd
            g = reduce(gcd, [abs(c) for c in combo])
            if g > 0:
                combo = [c // g for c in combo]
            # canonical sign
            if combo[0] > 0:
                combo = [-c for c in combo]
            return combo, w

    # Fallback: return the first basis vector even if not full support
    return basis[0], [1] + [0] * (n_basis - 1)


# ------------------------ Cells (5 per level) -----------------------

def cells():
    """5 cells across >3 orders of magnitude in α."""
    pi2 = mpmath.pi ** 2
    return [
        ("c1_canonical",          mpmath.mpf(1),       pi2),
        ("c2_alpha_2",            mpmath.mpf(2),       pi2 / 2),
        ("c3_symmetric_pi",       mpmath.pi,           mpmath.pi),
        ("c4_alpha_small_1em1",   mpmath.mpf("0.1"),   10 * pi2),
        ("c5_alpha_large_10pi2",  10 * pi2,            mpmath.mpf("0.1")),
    ]


# ----------------- Verification of a coefficient set ----------------

def evaluate_at_cell(
    coeffs: dict[int, int], alpha: mpmath.mpf, beta: mpmath.mpf
) -> tuple[mpmath.mpf, mpmath.mpf]:
    """Return (S, max_block_magnitude) where
       S = Σ_{d} c_d · T_d(α, β)
       max_block_magnitude = max_{d} |c_d · T_d(α, β)|

    The relative error is reported as |S| / max_block_magnitude.
    """
    block_magnitudes: list[mpmath.mpf] = []
    S = mpmath.mpf(0)
    for d, c in coeffs.items():
        Td = T_block(d, alpha, beta)
        block = mpmath.mpf(c) * Td
        S += block
        block_magnitudes.append(abs(block))
    return S, max(block_magnitudes)


def verify_coefficient_set(
    label: str,
    coeffs: dict[int, int],
    rows_out: list,
    notes: str = "",
) -> dict:
    """Verify a coefficient set across all 5 cells.  Returns dict
    summary {label, passes_all_cells, worst_rel_err, n_pass, n_total}.
    Writes per-cell rows into rows_out.
    """
    n_pass = 0
    worst_rel_err = mpmath.mpf(0)
    cell_results = []
    for cell_id, alpha, beta in cells():
        # sanity: αβ = π²
        prod = alpha * beta
        assert abs(prod - mpmath.pi ** 2) / (mpmath.pi ** 2) < mpmath.mpf("1e-180"), (
            f"αβ ≠ π² for cell {cell_id}"
        )
        S, mag = evaluate_at_cell(coeffs, alpha, beta)
        rel = abs(S) / mag if mag > 0 else abs(S)
        verdict = "PASS" if rel <= REL_ERR_BAR else "FAIL"
        if verdict == "PASS":
            n_pass += 1
        if rel > worst_rel_err:
            worst_rel_err = rel
        rows_out.append({
            "test_label": label,
            "cell_id": cell_id,
            "alpha": mpmath.nstr(alpha, 30),
            "beta": mpmath.nstr(beta, 30),
            "n_divisors": len(coeffs),
            "coefficients": str(dict(sorted(coeffs.items()))),
            "abs_sum": mpmath.nstr(abs(S), 20),
            "max_block_magnitude": mpmath.nstr(mag, 20),
            "rel_err": mpmath.nstr(rel, 15),
            "verdict": verdict,
            "notes": notes,
        })
        cell_results.append((cell_id, rel, verdict))
    return {
        "label": label,
        "passes_all_cells": n_pass == 5,
        "worst_rel_err": worst_rel_err,
        "n_pass": n_pass,
        "n_total": 5,
        "cell_results": cell_results,
    }


# --------------------- Main ----------------------------------------

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows: list = []
    summaries: list = []

    print("=" * 80)
    print("ADVERSARIAL VERIFICATION of the Level-pq E_2 Lambert annihilator FAMILY")
    print(f"  dps = {mpmath.mp.dps}, rel-err bar = {REL_ERR_BAR}")
    print("=" * 80)
    print()

    # ----------- (5) Triangulation: H-R-B base identity -------------
    print("Phase 0: H-R-B base identity verification")
    print("  Claim: x·L(x) + y·L(y) = (x+y)/24 − 1/4  for  x·y = π²")
    print(f"  (this anchors the whole family; if it fails, everything else fails)")
    print()
    print(f"  {'x':>14} {'rel-err':>20} {'verdict':>10}")
    hrb_all_pass = True
    for x in [mpmath.mpf(1), mpmath.mpf(2), mpmath.pi,
              mpmath.mpf("0.5"), mpmath.mpf(7), mpmath.mpf("0.1")]:
        y = mpmath.pi ** 2 / x
        Lx, _ = L_truncated(x)
        Ly, _ = L_truncated(y)
        lhs = x * Lx + y * Ly
        rhs = (x + y) / 24 - mpmath.mpf(1) / 4
        rel = abs(lhs - rhs) / abs(rhs) if rhs != 0 else abs(lhs - rhs)
        verdict = "PASS" if rel <= REL_ERR_BAR else "FAIL"
        if verdict == "FAIL":
            hrb_all_pass = False
        print(f"  {mpmath.nstr(x,8):>14} {mpmath.nstr(rel,5):>20} {verdict:>10}")
        rows.append({
            "test_label": "phase0_HRB_base",
            "cell_id": f"x={mpmath.nstr(x,5)}",
            "alpha": mpmath.nstr(x, 30),
            "beta": mpmath.nstr(y, 30),
            "n_divisors": 1,
            "coefficients": "{1: 1}",
            "abs_sum": mpmath.nstr(abs(lhs - rhs), 20),
            "max_block_magnitude": mpmath.nstr(max(abs(lhs), abs(rhs)), 20),
            "rel_err": mpmath.nstr(rel, 15),
            "verdict": verdict,
            "notes": "H-R-B base identity x*L(x)+y*L(y)=(x+y)/24-1/4 for xy=pi^2",
        })
    assert hrb_all_pass, "H-R-B base identity failed — STOP, family is bogus"
    print(f"  H-R-B base identity VERIFIED at all cells.")
    print()

    # ----------- (1) Independent verification of 7 new levels -------
    print("=" * 80)
    print("Phase 1: Independent verification of 7 NEW levels (diary 55 claims)")
    print("=" * 80)
    print(f"  Each level uses closed-form formula at dps={mpmath.mp.dps}")
    print(f"  Strict bar: rel-err ≤ {REL_ERR_BAR}")
    print()

    new_levels = [
        (35, 5, 7),
        (51, 3, 17),
        (65, 5, 13),
        (77, 7, 11),
        (87, 3, 29),
        (95, 5, 19),
        (115, 5, 23),
    ]
    for N, p, q in new_levels:
        coeffs = coefficients_pq(p, q)
        # linear constraints (must be exactly 0)
        constr = check_linear_constraints(coeffs)
        assert constr["passes"], f"linear constraints fail for N={N}"
        summary = verify_coefficient_set(
            f"phase1_N{N}_p{p}q{q}", coeffs, rows,
            notes=f"diary 55 family: N={N}={p}*{q}; closed-form coeffs",
        )
        summaries.append(summary)
        c1, cp, cq, cN = coeffs[1], coeffs[p], coeffs[q], coeffs[p*q]
        verdict = "PASS" if summary["passes_all_cells"] else "FAIL"
        print(f"  N={N:3d}=({p:2d}*{q:2d})  c=({c1:+4d},{cp:+4d},{cq:+4d},{cN:+4d})  "
              f"{summary['n_pass']}/5 cells PASS  worst_rel_err={mpmath.nstr(summary['worst_rel_err'],5):>13}  {verdict}")
    print()

    # ----------- (2) Edge cases --------------------------------------
    print("=" * 80)
    print("Phase 2: ADVERSARIAL edge cases (trying to break the formula)")
    print("=" * 80)

    print("  Phase 2a: Twin primes (q − p = 2)")
    twin_primes = [
        (143, 11, 13),
        (323, 17, 19),
    ]
    for N, p, q in twin_primes:
        coeffs = coefficients_pq(p, q)
        summary = verify_coefficient_set(
            f"phase2a_twin_N{N}_p{p}q{q}", coeffs, rows,
            notes="twin primes q-p=2",
        )
        summaries.append(summary)
        c1, cp, cq, cN = coeffs[1], coeffs[p], coeffs[q], coeffs[p*q]
        verdict = "PASS" if summary["passes_all_cells"] else "FAIL"
        print(f"    N={N:4d}=({p:2d}*{q:2d})  c=({c1:+4d},{cp:+4d},{cq:+4d},{cN:+4d})  "
              f"{summary['n_pass']}/5  worst={mpmath.nstr(summary['worst_rel_err'],5):>13}  {verdict}")

    print()
    print("  Phase 2b: Far-apart primes")
    far_primes = [
        (187, 11, 17),
        (391, 17, 23),
    ]
    for N, p, q in far_primes:
        coeffs = coefficients_pq(p, q)
        summary = verify_coefficient_set(
            f"phase2b_far_N{N}_p{p}q{q}", coeffs, rows,
            notes="far-apart primes",
        )
        summaries.append(summary)
        c1, cp, cq, cN = coeffs[1], coeffs[p], coeffs[q], coeffs[p*q]
        verdict = "PASS" if summary["passes_all_cells"] else "FAIL"
        print(f"    N={N:4d}=({p:2d}*{q:2d})  c=({c1:+4d},{cp:+4d},{cq:+4d},{cN:+4d})  "
              f"{summary['n_pass']}/5  worst={mpmath.nstr(summary['worst_rel_err'],5):>13}  {verdict}")

    print()
    print("  Phase 2c: p = 2 (small even prime)")
    p2_levels = [
        (6, 2, 3),
        (10, 2, 5),
        (14, 2, 7),
        (22, 2, 11),
    ]
    for N, p, q in p2_levels:
        coeffs = coefficients_pq(p, q)
        summary = verify_coefficient_set(
            f"phase2c_p2_N{N}_p{p}q{q}", coeffs, rows,
            notes="p=2 (small even prime)",
        )
        summaries.append(summary)
        c1, cp, cq, cN = coeffs[1], coeffs[p], coeffs[q], coeffs[p*q]
        verdict = "PASS" if summary["passes_all_cells"] else "FAIL"
        print(f"    N={N:4d}=({p:2d}*{q:2d})  c=({c1:+4d},{cp:+4d},{cq:+4d},{cN:+4d})  "
              f"{summary['n_pass']}/5  worst={mpmath.nstr(summary['worst_rel_err'],5):>13}  {verdict}")
    print()

    # ----------- (3) Structural extensions ---------------------------
    print("=" * 80)
    print("Phase 3: STRUCTURAL EXTENSIONS (these should reveal the limits)")
    print("=" * 80)

    # (3a) 3-prime squarefree N = pqr
    print("  Phase 3a: 3-prime squarefree N = p·q·r (expect 5-D annihilator space)")
    pqr_cases = [
        (30, 2, 3, 5),
        (105, 3, 5, 7),
        (165, 3, 5, 11),
    ]
    for N, p, q, r in pqr_cases:
        divs = sorted({1, p, q, r, p*q, p*r, q*r, p*q*r})
        basis = rational_nullspace_basis(divs)
        print(f"    N={N}=({p}*{q}*{r}): divisors={divs}, kernel dim={len(basis)}")
        # Verify the lowest-height integer annihilator that uses ALL 8 divisors
        full_combo, weights = full_support_combination(basis, divs)
        coeffs = {d: c for d, c in zip(divs, full_combo)}
        # Linear constraints
        constr = check_linear_constraints(coeffs)
        if not constr["passes"]:
            print(f"      WARN: linear constraints failed for combo on N={N}")
            continue
        # Verify
        summary = verify_coefficient_set(
            f"phase3a_pqr_N{N}_fullsupport", coeffs, rows,
            notes=f"3-prime squarefree N={N}; basis combo weights={weights}; uses all 8 divisors",
        )
        summaries.append(summary)
        verdict = "PASS" if summary["passes_all_cells"] else "FAIL"
        print(f"      full-support combo c={list(coeffs.values())}  "
              f"{summary['n_pass']}/5  worst={mpmath.nstr(summary['worst_rel_err'],5)}  {verdict}")
        # Also verify the first basis vector (often a sub-divisor annihilator)
        coeffs0 = {d: c for d, c in zip(divs, basis[0])}
        constr0 = check_linear_constraints(coeffs0)
        if not constr0["passes"]:
            print(f"      WARN: linear constraints failed for basis[0] on N={N}")
            continue
        summary0 = verify_coefficient_set(
            f"phase3a_pqr_N{N}_basis0", coeffs0, rows,
            notes=f"3-prime N={N}; basis[0] (sub-divisor annihilator)",
        )
        summaries.append(summary0)
        verdict0 = "PASS" if summary0["passes_all_cells"] else "FAIL"
        print(f"      basis[0] sub-divisor c={list(coeffs0.values())}  "
              f"{summary0['n_pass']}/5  worst={mpmath.nstr(summary0['worst_rel_err'],5)}  {verdict0}")

    print()
    # (3b) Prime power N = p^2
    print("  Phase 3b: Prime power N = p² (expect 0-dim annihilator space)")
    pp_cases = [(49, 7), (121, 11)]
    for N, p in pp_cases:
        divs = [1, p, p*p]
        basis = rational_nullspace_basis(divs)
        print(f"    N={N}=({p}²): divisors={divs}, kernel dim={len(basis)}")
        if len(basis) == 0:
            print(f"      VERDICT: NO ANNIHILATOR — family does NOT extend to prime powers.")
            rows.append({
                "test_label": f"phase3b_psq_N{N}_p{p}",
                "cell_id": "no_annihilator",
                "alpha": "n/a", "beta": "n/a",
                "n_divisors": 3,
                "coefficients": "{}",
                "abs_sum": "n/a",
                "max_block_magnitude": "n/a",
                "rel_err": "n/a",
                "verdict": "NO_ANNIHILATOR",
                "notes": f"N={N}=p²; constraint matrix has full rank=3; family does NOT extend",
            })
        else:
            # Try to verify the first basis vector
            coeffs = {d: c for d, c in zip(divs, basis[0])}
            summary = verify_coefficient_set(
                f"phase3b_psq_N{N}_basis0", coeffs, rows,
                notes=f"prime power N={N}; basis[0]",
            )
            summaries.append(summary)
            verdict = "PASS" if summary["passes_all_cells"] else "FAIL"
            print(f"      basis[0] c={list(coeffs.values())}  "
                  f"{summary['n_pass']}/5  worst={mpmath.nstr(summary['worst_rel_err'],5)}  {verdict}")

    print()
    # (3c) Composite with repeated prime N = p^2 q
    print("  Phase 3c: N = p²·q (expect 3-D annihilator space)")
    psq_cases = [
        (18, 3, 2),
        (45, 3, 5),
    ]
    for N, p, q in psq_cases:
        divs = sorted({1, p, q, p*p, p*q, p*p*q})
        basis = rational_nullspace_basis(divs)
        print(f"    N={N}=({p}²*{q}): divisors={divs}, kernel dim={len(basis)}")
        # Full-support combination
        full_combo, weights = full_support_combination(basis, divs)
        coeffs = {d: c for d, c in zip(divs, full_combo)}
        constr = check_linear_constraints(coeffs)
        if not constr["passes"]:
            print(f"      WARN: constraints failed for combo")
            continue
        summary = verify_coefficient_set(
            f"phase3c_psqq_N{N}_fullsupport", coeffs, rows,
            notes=f"N={N}=p²q; basis combo weights={weights}; full-support",
        )
        summaries.append(summary)
        verdict = "PASS" if summary["passes_all_cells"] else "FAIL"
        print(f"      full-support combo c={list(coeffs.values())}  "
              f"{summary['n_pass']}/5  worst={mpmath.nstr(summary['worst_rel_err'],5)}  {verdict}")
        # basis[0] (often a sub-annihilator)
        coeffs0 = {d: c for d, c in zip(divs, basis[0])}
        constr0 = check_linear_constraints(coeffs0)
        if not constr0["passes"]:
            print(f"      WARN: constraints failed for basis[0]")
            continue
        summary0 = verify_coefficient_set(
            f"phase3c_psqq_N{N}_basis0", coeffs0, rows,
            notes=f"N={N}=p²q; basis[0]",
        )
        summaries.append(summary0)
        verdict0 = "PASS" if summary0["passes_all_cells"] else "FAIL"
        print(f"      basis[0]    c={list(coeffs0.values())}  "
              f"{summary0['n_pass']}/5  worst={mpmath.nstr(summary0['worst_rel_err'],5)}  {verdict0}")

    print()

    # ------------------ Write CSV --------------------------------
    fieldnames = [
        "test_label", "cell_id", "alpha", "beta",
        "n_divisors", "coefficients",
        "abs_sum", "max_block_magnitude", "rel_err",
        "verdict", "notes",
    ]
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # ------------------ Summary table ----------------------------
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    pass_n = sum(1 for s in summaries if s["passes_all_cells"])
    print(f"  Total annihilator tests run: {len(summaries)}")
    print(f"  PASSED all 5 cells:           {pass_n} / {len(summaries)}")
    print(f"  Worst rel-err across all:     "
          f"{mpmath.nstr(max(s['worst_rel_err'] for s in summaries), 5)}")
    print()
    print("  Per-label verdict:")
    for s in summaries:
        verdict = "PASS" if s["passes_all_cells"] else "FAIL"
        print(f"    {s['label']:<48} {s['n_pass']}/{s['n_total']}  "
              f"worst={mpmath.nstr(s['worst_rel_err'],5):>13}  {verdict}")
    print()
    print(f"CSV written: {OUT}")
    print()
    if pass_n == len(summaries):
        print("OVERALL VERDICT: ALL TESTS PASS — family + extensions verified.")
    else:
        print(f"OVERALL VERDICT: PARTIAL — {pass_n}/{len(summaries)} tests pass.")


if __name__ == "__main__":
    main()
