"""Verification — Project C improvements on Warnaar 1.7 (a=1) and AB 1.6.6.

Per diary 42 (the 7th-8th Erdős-style ChatGPT-Pro cycle), Project C's
`modular_transform_with_correction` operator is claimed to improve two
recorded Ramanujan identities by 1-3 orders of magnitude in mpmath
wall-clock at q→1⁻:

    1. Lost Notebook p. 29 / Warnaar (1.7) at a=1
       Claim: 15× at β=10⁻¹, 62× at β=10⁻², 272× at β=10⁻³

    2. Andrews-Berndt Entry 1.6.6 (LN p. 35), ψ(q)
       Claim: 9×-35× vs triangular sum; hundreds-to-thousands× vs the
       product spelling near q→1⁻

This script independently benchmarks 6 forms across β ∈ {1e-3, 1e-2,
1e-1, 1.0} in our mpmath 1.3 / Python 3.12 environment at dps=80:

    IDENTITY 1 (Warnaar 1.7 at a=1):
      A. LHS triangular sum  Σ_{n=0}^∞ [(q;q²)_n · q^{2n}] / [(q²;q²)_n²]
      B. RHS recorded form   [(q;q²)_∞ / (q²;q²)_∞²] · false-θ tail
      C. RHS Project C form  modularly-transformed eta prefactor · same
                             false-θ tail (with q → e^{-β}, Q = e^{-2π²/β})

    IDENTITY 2 (AB 1.6.6):
      D. L triangular sum    Σ_{n=0}^∞ [(-1)^n q^{n²+n}] / [(q²;q²)_n (1-q^{2n+1})]
      E. ψ product           (q²;q²)_∞² / (q;q)_∞
      F. ψ Project C form    √(π/(2β)) · e^{β/8} · (1 + 2 Σ (-1)^m e^{-2π²m²/β})

For each form at each β we measure (median of TIMING_TRIALS runs)
wall-clock and report speedup vs the slowest "recorded" form.

Cross-check: at β=0.1 all three Identity-1 forms must agree to within
1e-30 rel-err (likewise all three Identity-2 forms).

NUMERICAL CAVEAT (matches diary 42's observation):
  At β ≤ 0.01 the triangular sums for both identities (A, D) suffer
  catastrophic intermediate-term cancellation — individual terms reach
  ~10^177 at β=0.001 while the true sum is ~40. mp.dps=80 working
  precision is insufficient to recover the true value at these β,
  producing garbage output despite the form being mathematically
  correct.

  ChatGPT Pro's claimed timings appear to be reported at the SAME 80
  dps without numerical validity check — i.e. the "recorded" timings
  represent wall-clock for the work the naive evaluator would do,
  independent of whether the answer is correct. We follow the same
  convention so the speedup ratios are apples-to-apples with ChatGPT,
  but we ALSO carry a `numerically_valid` column (True iff this form's
  result agrees with form C/F to ≤1e-30 rel-err). This honestly
  separates the cost claim (ratio of wall-clock at fixed dps) from
  the correctness story (the transformed form is the ONLY one usable
  at this dps in the small-β regime — a stronger result than mere
  speedup).

Implementation notes:
  - All Pochhammer-bearing series use INCREMENTAL Pochhammer evaluation
    `P_{n+1} = P_n · (1 - a·q^n)` to avoid the O(n²) blow-up of naive
    `mpmath.qp(a, q, n)` recomputation. This is the standard fair
    implementation any q-series user would write — same operation count
    as ChatGPT's measurement.
  - Infinite Pochhammers (∞-product spellings) delegate to mpmath.qp
    which truncates internally at machine precision.
  - Truncation policy: each series terminates when |next_term| < 1e-70.
  - Print is unbuffered (`flush=True`) so progress is visible during
    the long β=10⁻³ run.

Output:
  analysis/results/29_warnaar_17_ab_166_cost_verification.csv

Verdict tag per identity:
  CONFIRMED   if measured speedup ≥ 0.5 × claimed (within 2× of claim)
  PARTIAL     if measured speedup ≥ 2× but < 0.5 × claimed
  REFUTED     if measured speedup < 2× (no meaningful win)
"""
from __future__ import annotations

import csv
import time
from pathlib import Path
from typing import Callable

import mpmath
from mpmath import mp, mpf, exp, sqrt, pi, qp

OUT = Path(__file__).resolve().parent / "results" / "29_warnaar_17_ab_166_cost_verification.csv"
mp.dps = 80


def log(msg: str = "") -> None:
    """Unbuffered print so the long benchmark shows live progress."""
    print(msg, flush=True)


BETA_GRID = [
    mpf("0.001"),
    mpf("0.01"),
    mpf("0.1"),
    mpf("1.0"),
]
# Truncation threshold: 40 digits below dps=80 working precision so the
# final summed value has ≥30 reliable digits even after cancellation.
TRUNC_THRESHOLD = mpf(10) ** -70
N_MAX = 1_000_000     # safety cap; we also rely on threshold (form A at β=0.001 needs ~490k)
TIMING_TRIALS = 5     # median of 5 runs

# ChatGPT-Pro claimed speedups (diary 42) — for verdict assignment.
WARNAAR_CLAIM = {  # claimed transformed/recorded speedup
    mpf("0.1"): 15.2,
    mpf("0.01"): 62.2,
    mpf("0.001"): 272.0,
}
AB166_CLAIM_VS_TRIANG = {  # claimed transformed/triangular speedup, "9-35×"
    mpf("0.1"): 9.0,       # 1.0/0.12 ≈ 8.3 → use claim 9
    mpf("0.01"): 14.5,     # 1.6/0.11 ≈ 14.5
    mpf("0.001"): 34.2,    # 4.1/0.12 ≈ 34.2
}
AB166_CLAIM_VS_PROD = {  # claimed transformed/product speedup ("hundreds-thousands×")
    mpf("0.1"): 316.0,     # 38/0.12
    mpf("0.01"): 3360.0,   # 370/0.11
    mpf("0.001"): 31_600.0,  # 3800/0.12
}


# -------- Identity 1 (Warnaar 1.7 at a=1) ---------------------------------

def warnaar_lhs_triangular(beta: mpf) -> tuple[mpf, int]:
    """A. Σ_{n=0}^∞ [(q;q²)_n · q^{2n}] / [(q²;q²)_n²] (incremental Pochhammer)."""
    q = exp(-beta)
    q2 = q * q
    # numerator Pochhammer:   P1_n = (q;q²)_n   = Π_{k=0..n-1} (1 - q · q²^k) = Π (1 - q^{2k+1})
    # denominator Pochhammer: P2_n = (q²;q²)_n  = Π_{k=0..n-1} (1 - q²^{k+1})
    P1 = mpf(1)        # (q;q²)_0 = 1
    P2 = mpf(1)        # (q²;q²)_0 = 1
    q_pow_2n = mpf(1)  # q^{2*0} = 1
    s = mpf(0)
    n = 0
    while True:
        term = P1 * q_pow_2n / (P2 * P2)
        s += term
        if n > 0 and abs(term) < TRUNC_THRESHOLD:
            break
        # advance to n+1:
        P1 *= (1 - q ** (2 * n + 1))       # next factor of (q;q²)_n
        P2 *= (1 - q2 ** (n + 1))          # next factor of (q²;q²)_n
        q_pow_2n *= q2                     # q^{2(n+1)} = q^{2n} · q²
        n += 1
        if n > N_MAX:
            raise RuntimeError(f"warnaar_lhs hit N_MAX={N_MAX} at β={beta}")
    return s, n + 1


def warnaar_rhs_recorded(beta: mpf) -> tuple[mpf, int]:
    """B. [(q;q²)_∞ / (q²;q²)_∞²] · Σ_{n=0}^∞ (-1)^n q^{n(3n+2)}(1+q^{2n+1}).

    "recorded" = Ramanujan's RHS form with the original q-Pochhammers,
    NOT modularly transformed. Pochhammer prefactor via mpmath.qp(a,q)
    (no n argument → infinite product, truncated at machine precision).
    """
    q = exp(-beta)
    q2 = q * q
    # maxterms bumped past default (50·prec) so qp converges at β=0.001
    # where (q;q²)_∞ needs ~138k factors to drop below 10^-80.
    prefactor = qp(q, q2, maxterms=10_000_000) / qp(q2, q2, maxterms=10_000_000) ** 2
    s = mpf(0)
    n = 0
    while True:
        term = (-1) ** n * q ** (n * (3 * n + 2)) * (1 + q ** (2 * n + 1))
        s += term
        if n > 0 and abs(term) < TRUNC_THRESHOLD:
            break
        n += 1
        if n > N_MAX:
            raise RuntimeError(f"warnaar_rhs_recorded hit N_MAX={N_MAX} at β={beta}")
    return prefactor * s, n + 1


def warnaar_rhs_projectc(beta: mpf) -> tuple[mpf, int]:
    """C. (√2·β/π)·exp(π²/(12β) − 5β/24) · [(Q²;Q²)_∞/(Q;Q)_∞³] · false-θ tail

    Project C's modular_transform_with_correction applied twice (at t=β
    and t=2β) collapses the Pochhammer prefactor onto the (Q;Q) side
    where Q = e^{-2π²/β} ≪ 1, so the dual Pochhammers compute essentially
    for free at small β. The false-theta tail is the SAME as in form B
    (rewritten with exp(-β·…) instead of q^…).
    """
    Q = exp(-2 * pi ** 2 / beta)
    Q2 = Q * Q
    # qp here is trivially fast since |Q| ≪ 1; default maxterms is plenty
    prefactor_eta = qp(Q2, Q2) / qp(Q, Q) ** 3
    prefactor_scalar = (sqrt(2) * beta / pi) * exp(pi ** 2 / (12 * beta) - 5 * beta / 24)
    pref = prefactor_scalar * prefactor_eta
    s = mpf(0)
    n = 0
    while True:
        term = (-1) ** n * exp(-beta * n * (3 * n + 2)) * (1 + exp(-beta * (2 * n + 1)))
        s += term
        if n > 0 and abs(term) < TRUNC_THRESHOLD:
            break
        n += 1
        if n > N_MAX:
            raise RuntimeError(f"warnaar_rhs_projectc hit N_MAX={N_MAX} at β={beta}")
    return pref * s, n + 1


# -------- Identity 2 (AB 1.6.6) -------------------------------------------

def ab166_L_triangular(beta: mpf) -> tuple[mpf, int]:
    """D. L(q) = Σ_{n=0}^∞ [(-1)^n · q^{n²+n}] / [(q²;q²)_n · (1-q^{2n+1})]
    with incremental Pochhammer accumulation."""
    q = exp(-beta)
    q2 = q * q
    P = mpf(1)             # (q²;q²)_0 = 1
    s = mpf(0)
    n = 0
    while True:
        # q^{n²+n} = q^{n(n+1)}
        num = (-1) ** n * q ** (n * (n + 1))
        den = P * (1 - q ** (2 * n + 1))
        term = num / den
        s += term
        if n > 0 and abs(term) < TRUNC_THRESHOLD:
            break
        # advance: P_{n+1} = P_n · (1 - q²^{n+1})
        P *= (1 - q2 ** (n + 1))
        n += 1
        if n > N_MAX:
            raise RuntimeError(f"ab166_L_triang hit N_MAX={N_MAX} at β={beta}")
    return s, n + 1


def ab166_psi_product(beta: mpf) -> tuple[mpf, int]:
    """E. ψ(q) = (q²;q²)_∞² / (q;q)_∞ (the natural product spelling).

    "n_terms" returned as 0 — mpmath.qp handles internal truncation; we
    treat the whole call as one operation. maxterms bumped so qp
    converges at β=0.001."""
    q = exp(-beta)
    q2 = q * q
    return qp(q2, q2, maxterms=10_000_000) ** 2 / qp(q, q, maxterms=10_000_000), 0


def ab166_psi_projectc(beta: mpf) -> tuple[mpf, int]:
    """F. ψ(e^{-β}) = √(π/(2β)) · e^{β/8} · (1 + 2 Σ_{m=1}^∞ (-1)^m e^{-2π²m²/β}).

    Standard Jacobi-θ Poisson dual of ψ; in Project C this is
    modular_transform_with_correction applied to the Bose-Einstein
    log / eta side."""
    prefactor = sqrt(pi / (2 * beta)) * exp(beta / 8)
    s = mpf(1)
    m = 1
    while True:
        term = 2 * (-1) ** m * exp(-2 * pi ** 2 * m * m / beta)
        s += term
        if abs(term) < TRUNC_THRESHOLD:
            break
        m += 1
        if m > N_MAX:
            raise RuntimeError(f"ab166_psi_projectc hit N_MAX={N_MAX} at β={beta}")
    return prefactor * s, m


# -------- Timing harness --------------------------------------------------

def time_call(fn: Callable[[mpf], tuple[mpf, int]], beta: mpf) -> tuple[mpf, int, float]:
    """Return (value, n_terms, median wall-clock over TIMING_TRIALS runs)."""
    durations = []
    last_value = None
    last_terms = None
    for _ in range(TIMING_TRIALS):
        t0 = time.perf_counter()
        v, n = fn(beta)
        t1 = time.perf_counter()
        durations.append(t1 - t0)
        last_value = v
        last_terms = n
    durations.sort()
    median = durations[len(durations) // 2]
    return last_value, last_terms, median


# -------- Main ------------------------------------------------------------

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)

    log(f"Verification at mp.dps={mp.dps}, trunc=1e-70, timing trials={TIMING_TRIALS}")
    log(f"β grid: {[float(b) for b in BETA_GRID]}")
    log("")

    rows: list[dict] = []
    # --- Cross-check at β=0.1: all 3 Identity-1 forms agree, all 3 Identity-2 forms agree ---
    log("Cross-check (β=0.1) ...")
    beta_check = mpf("0.1")
    a_v, _ = warnaar_lhs_triangular(beta_check)
    b_v, _ = warnaar_rhs_recorded(beta_check)
    c_v, _ = warnaar_rhs_projectc(beta_check)
    d_v, _ = ab166_L_triangular(beta_check)
    e_v, _ = ab166_psi_product(beta_check)
    f_v, _ = ab166_psi_projectc(beta_check)
    rel_ab = abs(a_v - b_v) / abs(a_v)
    rel_ac = abs(a_v - c_v) / abs(a_v)
    rel_de = abs(d_v - e_v) / abs(d_v)
    rel_df = abs(d_v - f_v) / abs(d_v)
    log(f"  Warnaar  LHS vs RHS_recorded:  rel_err = {float(rel_ab):.3e}")
    log(f"  Warnaar  LHS vs RHS_projectc:  rel_err = {float(rel_ac):.3e}")
    log(f"  AB 1.6.6 L   vs ψ_product:     rel_err = {float(rel_de):.3e}")
    log(f"  AB 1.6.6 L   vs ψ_projectc:    rel_err = {float(rel_df):.3e}")
    if max(float(rel_ab), float(rel_ac), float(rel_de), float(rel_df)) > 1e-30:
        raise SystemExit(
            "FAIL: identities do not agree to 1e-30 at β=0.1 — aborting before benchmark."
        )
    log("  All four agree under 1e-30 (OK)\n")

    # --- Per-β benchmark loop ---
    for beta in BETA_GRID:
        log(f"--- β = {float(beta):g} ---  (running 5 trials per form)")
        t_start = time.perf_counter()

        # Identity 1
        log("  [A] warnaar LHS triangular ...")
        a_v, a_n, a_t = time_call(warnaar_lhs_triangular, beta)
        log(f"      {a_t * 1000:.3f} ms ({a_n} terms)")
        log("  [B] warnaar RHS recorded   ...")
        b_v, b_n, b_t = time_call(warnaar_rhs_recorded, beta)
        log(f"      {b_t * 1000:.3f} ms ({b_n} terms)")
        log("  [C] warnaar RHS projectc   ...")
        c_v, c_n, c_t = time_call(warnaar_rhs_projectc, beta)
        log(f"      {c_t * 1000:.3f} ms ({c_n} terms)")
        # Identity 2
        log("  [D] AB 1.6.6 L triangular  ...")
        d_v, d_n, d_t = time_call(ab166_L_triangular, beta)
        log(f"      {d_t * 1000:.3f} ms ({d_n} terms)")
        log("  [E] AB 1.6.6 psi product   ...")
        e_v, e_n, e_t = time_call(ab166_psi_product, beta)
        log(f"      {e_t * 1000:.3f} ms")
        log("  [F] AB 1.6.6 psi projectc  ...")
        f_v, f_n, f_t = time_call(ab166_psi_projectc, beta)
        log(f"      {f_t * 1000:.3f} ms ({f_n} terms)")

        rel_ab = float(abs(a_v - b_v) / abs(a_v))
        rel_ac = float(abs(a_v - c_v) / abs(a_v))
        rel_de = float(abs(d_v - e_v) / abs(d_v))
        rel_df = float(abs(d_v - f_v) / abs(d_v))

        warnaar_speedup_vs_triang = a_t / c_t
        warnaar_speedup_vs_recorded = b_t / c_t
        ab166_speedup_vs_triang = d_t / f_t
        ab166_speedup_vs_product = e_t / f_t

        # Treat the Project C form (C / F) as the numerical reference
        # since it's the only one without cancellation issues at small β.
        # Compute rel_err of each form vs the reference; flag valid if ≤1e-30.
        warnaar_ref = c_v
        ab166_ref = f_v
        rel_a_ref = float(abs(a_v - warnaar_ref) / abs(warnaar_ref))
        rel_b_ref = float(abs(b_v - warnaar_ref) / abs(warnaar_ref))
        rel_c_ref = 0.0  # is the reference
        rel_d_ref = float(abs(d_v - ab166_ref) / abs(ab166_ref))
        rel_e_ref = float(abs(e_v - ab166_ref) / abs(ab166_ref))
        rel_f_ref = 0.0  # is the reference

        common = {"beta": str(beta), "beta_float": float(beta)}
        rows.append({
            **common, "identity": "warnaar_17_a1", "form": "A_LHS_triangular",
            "value": str(a_v), "n_terms": a_n, "time_s": a_t,
            "rel_err_vs_ref": rel_a_ref,
            "numerically_valid": rel_a_ref < 1e-30,
            "speedup_C_over_self": c_t / a_t if a_t > 0 else float("inf"),
        })
        rows.append({
            **common, "identity": "warnaar_17_a1", "form": "B_RHS_recorded",
            "value": str(b_v), "n_terms": b_n, "time_s": b_t,
            "rel_err_vs_ref": rel_b_ref,
            "numerically_valid": rel_b_ref < 1e-30,
            "speedup_C_over_self": c_t / b_t if b_t > 0 else float("inf"),
        })
        rows.append({
            **common, "identity": "warnaar_17_a1", "form": "C_RHS_projectc",
            "value": str(c_v), "n_terms": c_n, "time_s": c_t,
            "rel_err_vs_ref": rel_c_ref,
            "numerically_valid": True,
            "speedup_C_over_self": 1.0,
        })
        rows.append({
            **common, "identity": "ab_166", "form": "D_L_triangular",
            "value": str(d_v), "n_terms": d_n, "time_s": d_t,
            "rel_err_vs_ref": rel_d_ref,
            "numerically_valid": rel_d_ref < 1e-30,
            "speedup_C_over_self": f_t / d_t if d_t > 0 else float("inf"),
        })
        rows.append({
            **common, "identity": "ab_166", "form": "E_psi_product",
            "value": str(e_v), "n_terms": e_n, "time_s": e_t,
            "rel_err_vs_ref": rel_e_ref,
            "numerically_valid": rel_e_ref < 1e-30,
            "speedup_C_over_self": f_t / e_t if e_t > 0 else float("inf"),
        })
        rows.append({
            **common, "identity": "ab_166", "form": "F_psi_projectc",
            "value": str(f_v), "n_terms": f_n, "time_s": f_t,
            "rel_err_vs_ref": rel_f_ref,
            "numerically_valid": True,
            "speedup_C_over_self": 1.0,
        })

        log(f"  rel_err (vs C ref): A={rel_a_ref:.2e}  B={rel_b_ref:.2e}    "
            f"rel_err (vs F ref): D={rel_d_ref:.2e}  E={rel_e_ref:.2e}")
        valid_str = (
            f"  numerically_valid: A={rel_a_ref < 1e-30}  B={rel_b_ref < 1e-30}  "
            f"D={rel_d_ref < 1e-30}  E={rel_e_ref < 1e-30}"
        )
        log(valid_str)
        log(f"  Warnaar speedup C vs A (triang): {warnaar_speedup_vs_triang:7.2f}x")
        log(f"  Warnaar speedup C vs B (RHS rec): {warnaar_speedup_vs_recorded:7.2f}x")
        if beta in WARNAAR_CLAIM:
            log(f"      (ChatGPT vs recorded claim: {WARNAAR_CLAIM[beta]:.1f}x; "
                f"ratio measured/claim = {warnaar_speedup_vs_recorded/WARNAAR_CLAIM[beta]:.2f})")
        log(f"  AB 1.6.6 speedup F vs D (triang) : {ab166_speedup_vs_triang:7.2f}x")
        log(f"  AB 1.6.6 speedup F vs E (product): {ab166_speedup_vs_product:7.2f}x")
        if beta in AB166_CLAIM_VS_TRIANG:
            log(f"      (ChatGPT vs triang claim:  {AB166_CLAIM_VS_TRIANG[beta]:.1f}x; "
                f"ratio = {ab166_speedup_vs_triang/AB166_CLAIM_VS_TRIANG[beta]:.2f})")
            log(f"      (ChatGPT vs product claim: {AB166_CLAIM_VS_PROD[beta]:.1f}x; "
                f"ratio = {ab166_speedup_vs_product/AB166_CLAIM_VS_PROD[beta]:.2f})")
        log(f"  β block wall-clock: {time.perf_counter() - t_start:.1f}s")
        log("")

    # --- Write CSV ---
    fieldnames = ["beta", "beta_float", "identity", "form", "value",
                  "n_terms", "time_s", "rel_err_vs_ref",
                  "numerically_valid", "speedup_C_over_self"]
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    log(f"Written: {OUT}")

    # --- Verdict summary ---
    log("")
    log("=" * 72)
    log("VERDICT SUMMARY")
    log("=" * 72)

    def _verdict(measured: float, claim: float) -> str:
        if measured < 2.0:
            return "REFUTED"
        if measured >= 0.5 * claim:
            return "CONFIRMED"
        return "PARTIAL"

    log("\nIdentity 1 — Warnaar 1.7 at a=1 (Project C C vs recorded B):")
    log(f"{'β':>8} {'measured':>12} {'claim':>10} {'verdict':>12}")
    warnaar_verdicts = []
    for beta in BETA_GRID:
        if beta not in WARNAAR_CLAIM:
            continue
        row_b = next(r for r in rows if r["form"] == "B_RHS_recorded" and r["beta"] == str(beta))
        row_c = next(r for r in rows if r["form"] == "C_RHS_projectc" and r["beta"] == str(beta))
        measured = row_b["time_s"] / row_c["time_s"]
        claim = WARNAAR_CLAIM[beta]
        v = _verdict(measured, claim)
        warnaar_verdicts.append(v)
        log(f"{float(beta):>8g} {measured:>10.2f}x {claim:>8.1f}x {v:>12}")

    log("\nIdentity 2 — AB 1.6.6 (Project C F vs L triangular D):")
    log(f"{'β':>8} {'measured':>12} {'claim':>10} {'verdict':>12}")
    ab166_t_verdicts = []
    for beta in BETA_GRID:
        if beta not in AB166_CLAIM_VS_TRIANG:
            continue
        row_d = next(r for r in rows if r["form"] == "D_L_triangular" and r["beta"] == str(beta))
        row_f = next(r for r in rows if r["form"] == "F_psi_projectc" and r["beta"] == str(beta))
        measured = row_d["time_s"] / row_f["time_s"]
        claim = AB166_CLAIM_VS_TRIANG[beta]
        v = _verdict(measured, claim)
        ab166_t_verdicts.append(v)
        log(f"{float(beta):>8g} {measured:>10.2f}x {claim:>8.1f}x {v:>12}")

    log("\nIdentity 2 — AB 1.6.6 (Project C F vs product E):")
    log(f"{'β':>8} {'measured':>12} {'claim':>10} {'verdict':>12}")
    ab166_p_verdicts = []
    for beta in BETA_GRID:
        if beta not in AB166_CLAIM_VS_PROD:
            continue
        row_e = next(r for r in rows if r["form"] == "E_psi_product" and r["beta"] == str(beta))
        row_f = next(r for r in rows if r["form"] == "F_psi_projectc" and r["beta"] == str(beta))
        measured = row_e["time_s"] / row_f["time_s"]
        claim = AB166_CLAIM_VS_PROD[beta]
        v = _verdict(measured, claim)
        ab166_p_verdicts.append(v)
        log(f"{float(beta):>8g} {measured:>10.2f}x {claim:>8.1f}x {v:>12}")

    def _final(verdicts: list[str]) -> str:
        if all(v == "CONFIRMED" for v in verdicts):
            return "CONFIRMED"
        if any(v == "REFUTED" for v in verdicts):
            if not any(v == "CONFIRMED" for v in verdicts):
                return "REFUTED"
        return "PARTIAL"

    log("")
    log(f"Final verdict — Identity 1 (Warnaar 1.7):              "
        f"{_final(warnaar_verdicts)}")
    log(f"Final verdict — Identity 2 (AB 1.6.6 vs L triangular): "
        f"{_final(ab166_t_verdicts)}")
    log(f"Final verdict — Identity 2 (AB 1.6.6 vs ψ product):    "
        f"{_final(ab166_p_verdicts)}")


if __name__ == "__main__":
    main()
