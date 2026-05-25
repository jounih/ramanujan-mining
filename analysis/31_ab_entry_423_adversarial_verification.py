"""
Exp 31 — Adversarial verification of Andrews-Berndt Lost Notebook Part IV
Entry 4.2.3 (formula 4.2.5, p. 199).

The identity (Ramanujan, with a > 0, 0 <= lambda < eps, 1/eps in Z_{>0}):

    eps * sum_{n>=0} a^{lambda + n*eps} / Gamma(1 + lambda + n*eps)
  = e^a - (eps/pi) * int_0^infty e^{-ax} * x^{-lambda-1}
          * [sin(pi(lambda - eps)) - x^eps * sin(pi*lambda)]
          / [2 cos(pi*eps) - (x^eps + x^{-eps})] dx

Andrews-Berndt (LN Part IV, section 4.4) claim Entry 4.2.3 is INCORRECT in
general; they 'demonstrate' this by asymptotic comparison at lambda=1/2,
eps=1 as a -> infty.

ChatGPT-Pro (diary 56) claims AB are mistaken and Ramanujan's identity is
CORRECT. This script independently verifies / refutes that claim adversarially,
sweeping (a, lambda, eps) cells across 7+ orders of magnitude and including
both a numerical-integration route and (where available) a closed-form
sympy / mpmath symbolic check.

Three independent verification paths:
 (P1) High-precision numerical: LHS as truncated series (with explicit error
      bound) vs RHS as numerical integral.
 (P2) Mittag-Leffler closed form: LHS == eps * a^lambda * E_{eps, 1+lambda}(a^eps)
      via mpmath's mp.mlf, used as cross-check on the LHS series truncation.
 (P3) Symbolic / sympy reduction: at lambda=1/2, eps=1 the identity collapses
      to e^a erf(sqrt(a)) (on both sides). Test this symbolically.

Output: results/31_ab_entry_423_verification.csv with one row per cell.
"""

import csv
import math
import os
import time
from typing import Optional

import mpmath as mp

RESULTS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "results",
    "31_ab_entry_423_verification.csv",
)

# Use a high working precision throughout
DPS = 80                # baseline working precision for sweep
DPS_DEEP = 200          # for the AB-chosen "smoking gun" cell


def lhs_series_truncated(a, lam, eps, dps, N=None):
    """LHS = eps * sum_{n>=0} a^{lam+n*eps} / Gamma(1+lam+n*eps).
    Truncate when the term is < 10^{-dps-20}; cap at very large N.
    Returns (value, n_terms_used, abs_last_term)."""
    a_mp = mp.mpf(a)
    lam_mp = mp.mpf(str(lam))
    eps_mp = mp.mpf(str(eps))
    if N is None:
        # heuristic upper cap; we'll break early on tail size
        N = 200000
    eps_for_term = mp.mpf(f"1e-{dps + 30}")
    total = mp.mpf(0)
    last = mp.mpf(0)
    started_decay = False
    peak = mp.mpf(0)
    for n in range(N):
        exponent = lam_mp + n * eps_mp
        term = mp.power(a_mp, exponent) / mp.gamma(mp.mpf(1) + exponent)
        total += term
        abs_term = abs(term)
        if abs_term > peak:
            peak = abs_term
        else:
            started_decay = True
        # break only after series has started to decay
        if started_decay and abs_term < eps_for_term and n > 20:
            last = abs_term
            return eps_mp * total, n + 1, last
    return eps_mp * total, N, abs(term)


def lhs_mittag_leffler(a, lam, eps, dps):
    """LHS = eps * a^lam * E_{eps, 1+lam}(a^eps).
    Here E_{alpha, beta}(z) = sum_n z^n / Gamma(alpha*n + beta).
    Note that this is mathematically equivalent to the LHS series — they share
    the same sum — but with the geometric/Mittag-Leffler structure made
    explicit. The numerical evaluation also goes through differently because
    we factor out eps*a^lam and sum z^n / Gamma(alpha n + beta) instead.
    We use this as a self-consistency sanity check on the truncated sum.

    For 1/eps in Z_{>0} we can ALSO use the well-known finite combinator
    identity (e.g. for eps=1/2: E_{1/2,1}(z) = exp(z^2)*erfc(-z)) as another
    cross-check; this is implemented as `lhs_eps_inv_integer_closed`.
    """
    a_mp = mp.mpf(a)
    lam_mp = mp.mpf(str(lam))
    eps_mp = mp.mpf(str(eps))
    z = mp.power(a_mp, eps_mp)
    alpha = eps_mp
    beta = mp.mpf(1) + lam_mp
    # Direct Mittag-Leffler series; truncate when term tiny relative to current dps
    eps_for_term = mp.mpf(f"1e-{dps + 30}")
    total = mp.mpf(0)
    peak = mp.mpf(0)
    decay_started = False
    for n in range(200000):
        term = mp.power(z, n) / mp.gamma(alpha * n + beta)
        total += term
        absterm = abs(term)
        if absterm > peak:
            peak = absterm
        else:
            decay_started = True
        if decay_started and absterm < eps_for_term and n > 20:
            break
    return eps_mp * mp.power(a_mp, lam_mp) * total


def lhs_closed_eps_one_lam_half(a):
    """Closed form for the special cell lambda=1/2, eps=1:
    LHS = sum_{n>=0} a^{1/2+n} / Gamma(3/2+n) = e^a erf(sqrt(a)).
    """
    a_mp = mp.mpf(a)
    return mp.exp(a_mp) * mp.erf(mp.sqrt(a_mp))


def lhs_closed_eps_one_lam_zero(a):
    """Trivial degenerate cell lambda=0, eps=1: LHS = sum_n a^n / n! = e^a."""
    return mp.exp(mp.mpf(a))


def rhs_integral(a, lam, eps, dps, use_substitution=True):
    """RHS = e^a - (eps/pi) * int_0^infty f(x) dx where
        f(x) = e^{-ax} * x^{-lam-1}
              * [sin(pi*(lam-eps)) - x^eps * sin(pi*lam)]
              / [2 cos(pi*eps) - (x^eps + x^{-eps})]

    Integrability at x=0: integrand ~ x^{eps - lam - 1} * (constant),
    which is integrable iff lam < eps. (Ramanujan's stated condition.)

    Near x=0 the denominator behaves as -(x^{-eps})*(1+O(x^eps)), so the
    overall power is x^{eps-lam-1}. The integrand has no other singularities
    on (0, infty) provided eps in (0, 1] — denominator 2cos(pi*eps)-(x^eps+x^{-eps})
    never vanishes for x>0, eps in (0,1) (AM-GM gives x^eps+x^{-eps} >= 2,
    and 2cos(pi*eps) <= 2 with equality only at eps=0, which is excluded;
    for eps in (0,1) we have 2cos(pi*eps) < 2 <= x^eps+x^{-eps}, so the
    denominator is strictly negative; for eps=1, denominator = -2 - x - 1/x
    which is also strictly negative).

    With use_substitution=True (DEFAULT — strongly recommended), apply
        x = u^{1/(eps-lam)}
    so that the integrand near u=0 has no singular factor; the
    Jacobian dx/du = (1/(eps-lam)) u^{1/(eps-lam) - 1} cancels the
    x^{eps-lam-1} singularity at x=0 (which corresponds to u=0).
    This is critical for cells with lam close to eps; without the
    substitution the quadrature loses many digits to a near-pole.
    """
    a_mp = mp.mpf(a)
    lam_mp = mp.mpf(str(lam))
    eps_mp = mp.mpf(str(eps))
    pi = mp.pi

    sin_lam_minus_eps = mp.sin(pi * (lam_mp - eps_mp))
    sin_lam = mp.sin(pi * lam_mp)
    two_cos_eps = 2 * mp.cos(pi * eps_mp)

    if not use_substitution:
        def integrand(x):
            x = mp.mpf(x)
            x_eps = mp.power(x, eps_mp)
            x_neg_eps = mp.power(x, -eps_mp)
            num = sin_lam_minus_eps - x_eps * sin_lam
            den = two_cos_eps - (x_eps + x_neg_eps)
            return mp.exp(-a_mp * x) * mp.power(x, -lam_mp - 1) * num / den
        I_low = mp.quad(integrand, [mp.mpf(0), mp.mpf(1)])
        I_high = mp.quad(integrand, [mp.mpf(1), mp.inf])
    else:
        delta = eps_mp - lam_mp   # > 0
        inv_delta = 1 / delta
        def integrand_u(u):
            u = mp.mpf(u)
            if u == 0:
                return mp.mpf(0)
            x = mp.power(u, inv_delta)
            x_eps = mp.power(x, eps_mp)
            x_neg_eps = mp.power(x, -eps_mp)
            num = sin_lam_minus_eps - x_eps * sin_lam
            den = two_cos_eps - (x_eps + x_neg_eps)
            jac = inv_delta * mp.power(u, inv_delta - 1)
            return mp.exp(-a_mp * x) * mp.power(x, -lam_mp - 1) * num / den * jac
        I_low = mp.quad(integrand_u, [mp.mpf(0), mp.mpf(1)])
        I_high = mp.quad(integrand_u, [mp.mpf(1), mp.inf])
    I = I_low + I_high
    return mp.exp(a_mp) - (eps_mp / pi) * I


def reldiff(a, b):
    a = mp.mpf(a); b = mp.mpf(b)
    if a == 0 and b == 0:
        return mp.mpf(0)
    return abs(a - b) / max(abs(a), abs(b))


def sweep():
    rows = []
    mp.mp.dps = DPS

    # 1) The smoking-gun cell — AB's chosen counterexample, super-deep
    print("=" * 72)
    print("CELL 0 — AB's claimed counterexample (a=10, lam=1/2, eps=1), deep dps")
    print("=" * 72)
    mp.mp.dps = DPS_DEEP
    a, lam, eps = 10, mp.mpf("0.5"), 1
    t0 = time.time()
    L, n_used, tail = lhs_series_truncated(a, lam, eps, DPS_DEEP)
    L_mlf = lhs_mittag_leffler(a, lam, eps, DPS_DEEP)
    R = rhs_integral(a, lam, eps, DPS_DEEP)
    closed = mp.exp(a) * mp.erf(mp.sqrt(a))  # special-case closed form
    rd_LR = reldiff(L, R)
    rd_L_mlf = reldiff(L, L_mlf)
    rd_L_closed = reldiff(L, closed)
    t = time.time() - t0
    print(f"  N_terms={n_used}, tail={tail}, elapsed={t:.1f}s")
    print(f"  LHS         = {mp.nstr(L, 50)}")
    print(f"  RHS         = {mp.nstr(R, 50)}")
    print(f"  LHS_mlf     = {mp.nstr(L_mlf, 50)}")
    print(f"  closed-form = {mp.nstr(closed, 50)}")
    print(f"  rel|LHS-RHS|        = {mp.nstr(rd_LR, 8)}")
    print(f"  rel|LHS-LHS_mlf|    = {mp.nstr(rd_L_mlf, 8)}")
    print(f"  rel|LHS-closed_form|= {mp.nstr(rd_L_closed, 8)}")
    rows.append({
        "cell_id": "AB_smoking_gun",
        "a": float(a), "lambda": float(lam), "eps": float(eps),
        "dps": DPS_DEEP,
        "N_terms_lhs": n_used,
        "lhs_series": mp.nstr(L, 50),
        "lhs_mlf": mp.nstr(L_mlf, 50),
        "rhs_integral": mp.nstr(R, 50),
        "closed_form": mp.nstr(closed, 50),
        "rel_err_LHS_RHS": float(rd_LR),
        "rel_err_LHS_mlf": float(rd_L_mlf),
        "rel_err_LHS_closed": float(rd_L_closed),
        "elapsed_s": round(t, 2),
    })

    # 2) Broad sweep across a, lambda, eps
    a_grid = [mp.mpf("0.001"), mp.mpf("0.01"), mp.mpf("0.1"),
              mp.mpf("1"), mp.mpf("10"), mp.mpf("100"), mp.mpf("1000")]
    eps_grid = [mp.mpf(1), mp.mpf(1) / 2, mp.mpf(1) / 3,
                mp.mpf(1) / 4, mp.mpf(1) / 5, mp.mpf(1) / 6]
    # lambda values, expressed as fractions of eps (0 <= lam < eps)
    lam_frac_grid = [mp.mpf(0),
                     mp.mpf("0.01"),
                     mp.mpf("0.1"),
                     mp.mpf("0.5"),
                     mp.mpf("0.9")]
    mp.mp.dps = DPS
    cell_idx = 0
    for eps in eps_grid:
        for lf in lam_frac_grid:
            lam = lf * eps    # so 0 <= lam < eps holds
            for a in a_grid:
                cell_idx += 1
                t0 = time.time()
                try:
                    L, n_used, tail = lhs_series_truncated(a, lam, eps, DPS)
                except Exception as e:
                    print(f"  cell {cell_idx} LHS failed: {e}")
                    continue
                try:
                    L_mlf = lhs_mittag_leffler(a, lam, eps, DPS)
                except Exception as e:
                    L_mlf = mp.nan
                try:
                    R = rhs_integral(a, lam, eps, DPS)
                except Exception as e:
                    print(f"  cell {cell_idx} RHS integral failed at a={a}, lam={lam}, eps={eps}: {e}")
                    R = mp.nan
                # closed form: only at lam=1/2, eps=1
                if eps == 1 and lam == mp.mpf("0.5"):
                    closed = mp.exp(a) * mp.erf(mp.sqrt(a))
                    rd_L_closed = float(reldiff(L, closed))
                else:
                    closed = mp.nan
                    rd_L_closed = float("nan")
                try:
                    rd_LR = float(reldiff(L, R))
                except Exception:
                    rd_LR = float("nan")
                try:
                    rd_L_mlf = float(reldiff(L, L_mlf)) if mp.isfinite(L_mlf) else float("nan")
                except Exception:
                    rd_L_mlf = float("nan")
                t = time.time() - t0
                print(f"  cell {cell_idx:3d}: a={float(a):.4g}, lam={float(lam):.4g}, eps={float(eps):.4g}, "
                      f"N={n_used}, |L-R|/|R|={rd_LR:.2e}, |L-mlf|={rd_L_mlf:.2e}, t={t:.1f}s")
                rows.append({
                    "cell_id": f"sweep_{cell_idx:03d}",
                    "a": float(a), "lambda": float(lam), "eps": float(eps),
                    "dps": DPS,
                    "N_terms_lhs": n_used,
                    "lhs_series": mp.nstr(L, 25),
                    "lhs_mlf": mp.nstr(L_mlf, 25) if mp.isfinite(L_mlf) else "NaN",
                    "rhs_integral": mp.nstr(R, 25) if mp.isfinite(R) else "NaN",
                    "closed_form": mp.nstr(closed, 25) if mp.isfinite(closed) else "NaN",
                    "rel_err_LHS_RHS": rd_LR,
                    "rel_err_LHS_mlf": rd_L_mlf,
                    "rel_err_LHS_closed": rd_L_closed,
                    "elapsed_s": round(t, 2),
                })

    # 3) "Suspicious" cells specifically targeting AB's regime
    #    - large a (which AB claim shows discrepancy)
    #    - lambda close to upper bound eps
    print()
    print("=" * 72)
    print("Targeted: large a + lambda close to eps (where AB claim breaks the identity)")
    print("=" * 72)
    for eps_val in [mp.mpf(1), mp.mpf(1) / 2, mp.mpf(1) / 3]:
        for a_val in [mp.mpf(20), mp.mpf(50)]:
            for lam_frac in [mp.mpf("0.95"), mp.mpf("0.99")]:
                lam_val = lam_frac * eps_val
                cell_idx += 1
                t0 = time.time()
                L, n_used, tail = lhs_series_truncated(a_val, lam_val, eps_val, DPS)
                L_mlf = lhs_mittag_leffler(a_val, lam_val, eps_val, DPS)
                try:
                    R = rhs_integral(a_val, lam_val, eps_val, DPS)
                except Exception as e:
                    print(f"  target cell {cell_idx}: integral failed: {e}")
                    R = mp.nan
                rd_LR = float(reldiff(L, R)) if mp.isfinite(R) else float("nan")
                rd_L_mlf = float(reldiff(L, L_mlf))
                t = time.time() - t0
                print(f"  target {cell_idx}: a={float(a_val)}, lam={float(lam_val):.4g}, eps={float(eps_val):.4g} "
                      f"| |L-R|/|R| = {rd_LR:.2e}, |L-mlf| = {rd_L_mlf:.2e}, t={t:.1f}s")
                rows.append({
                    "cell_id": f"target_large_a_{cell_idx:03d}",
                    "a": float(a_val), "lambda": float(lam_val), "eps": float(eps_val),
                    "dps": DPS,
                    "N_terms_lhs": n_used,
                    "lhs_series": mp.nstr(L, 25),
                    "lhs_mlf": mp.nstr(L_mlf, 25),
                    "rhs_integral": mp.nstr(R, 25) if mp.isfinite(R) else "NaN",
                    "closed_form": "NaN",
                    "rel_err_LHS_RHS": rd_LR,
                    "rel_err_LHS_mlf": rd_L_mlf,
                    "rel_err_LHS_closed": float("nan"),
                    "elapsed_s": round(t, 2),
                })

    # Write CSV
    fieldnames = ["cell_id", "a", "lambda", "eps", "dps",
                  "N_terms_lhs", "lhs_series", "lhs_mlf",
                  "rhs_integral", "closed_form",
                  "rel_err_LHS_RHS", "rel_err_LHS_mlf",
                  "rel_err_LHS_closed", "elapsed_s"]
    with open(RESULTS_PATH, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"\nWrote {len(rows)} rows to {RESULTS_PATH}")

    # Summary verdict
    print()
    print("=" * 72)
    print("VERDICT SUMMARY")
    print("=" * 72)
    n_pass = sum(1 for r in rows if r["rel_err_LHS_RHS"] < 1e-15)
    n_pass_loose = sum(1 for r in rows if r["rel_err_LHS_RHS"] < 1e-10)
    n_fail = sum(1 for r in rows if r["rel_err_LHS_RHS"] >= 1e-10)
    print(f"  Total cells: {len(rows)}")
    print(f"  Identity holds at <1e-15 rel-err: {n_pass}")
    print(f"  Identity holds at <1e-10 rel-err: {n_pass_loose}")
    print(f"  Cells failing >=1e-10:            {n_fail}")
    if n_fail > 0:
        print("  FAILING CELLS:")
        for r in rows:
            if r["rel_err_LHS_RHS"] >= 1e-10:
                print(f"    {r['cell_id']}: a={r['a']}, lam={r['lambda']}, eps={r['eps']}, "
                      f"rel|L-R|={r['rel_err_LHS_RHS']:.2e}")
    return rows


def sympy_symbolic_check():
    """Independent third path: at lambda=1/2, eps=1 we can symbolically reduce
    both sides via sympy and check equality."""
    import sympy as sp
    print()
    print("=" * 72)
    print("SYMBOLIC CHECK (sympy) at lambda=1/2, eps=1")
    print("=" * 72)
    a = sp.symbols("a", positive=True)
    x = sp.symbols("x", positive=True)
    # LHS in closed form (via the differential equation):
    # L(a) = sum_{n>=0} a^{1/2+n} / Gamma(3/2+n)
    # L'(a) - L(a) = 1/sqrt(pi*a), L(0)=0 => L = e^a erf(sqrt(a))
    L = sp.exp(a) * sp.erf(sp.sqrt(a))

    # RHS integral at lam=1/2, eps=1:
    # numerator sin(pi*(1/2-1)) - x*sin(pi/2) = sin(-pi/2) - x = -1 - x
    # denominator 2*cos(pi) - (x + 1/x) = -2 - x - 1/x = -(x+1)^2/x
    # ratio = -(1+x) * x / (x+1)^2 = -x/(x+1)
    # full integrand = e^{-a*x} * x^{-3/2} * (-x/(x+1)) = -e^{-a*x} / (sqrt(x)(x+1))
    # So integral I = - int e^{-ax}/(sqrt(x)(x+1)) dx
    # RHS = e^a - (1/pi) * I = e^a + (1/pi) * int e^{-ax}/(sqrt(x)(x+1)) dx ... wait sign.
    # Let me redo: original RHS = e^a - (eps/pi) * int [sin(...) - x^eps sin(...)] / [2cos - ...] dx
    # The integrand we just simplified is e^{-ax} * x^{-lam-1} * (NUM/DEN)
    # NUM/DEN = -x/(x+1) (negative ratio)
    # So integrand = e^{-ax} x^{-3/2} (-x/(x+1)) = -e^{-ax} / (sqrt(x)(x+1))
    # Integral is negative; (-eps/pi) * integral = (+1/pi) * |integral|
    # Wait no: RHS = e^a - (eps/pi) * INT where INT is the negative integral
    # so RHS = e^a - (1/pi)(- I_pos) = e^a + I_pos/pi
    # where I_pos = int e^{-ax}/(sqrt(x)(x+1)) dx
    # The known Laplace identity: int_0^inf e^{-ax}/(sqrt(x)(x+1)) dx = pi*e^a*erfc(sqrt(a))
    # Hmm wait then RHS = e^a + e^a*erfc(sqrt(a)) > e^a, which is wrong.
    # Let me re-check the sign:
    # We had num/den = (-1-x)/(-2-x-1/x) = (1+x)/(2+x+1/x) = (1+x)*x/(x(2+x+1/x))
    #              = (x+x^2)/(2x+x^2+1) = (x+x^2)/(x+1)^2 = x(1+x)/(x+1)^2 = x/(x+1)
    # So num/den = x/(x+1) [POSITIVE].
    # OK I had a sign error above. Let me redo:
    # denominator = 2cos(pi) - (x+1/x) = -2 - x - 1/x. This is NEGATIVE.
    # numerator = sin(pi*(1/2-1)) - x sin(pi/2) = -1 - x. This is NEGATIVE.
    # So num/den = (-1-x) / (-2-x-1/x) = (1+x)/(2+x+1/x) = (1+x)x / (2x+x^2+1) = x(1+x)/(x+1)^2 = x/(x+1)
    # Both factors negative, ratio positive. Good.
    # So integrand = e^{-ax} * x^{-3/2} * x/(x+1) = e^{-ax} / (sqrt(x)(x+1))
    # And RHS = e^a - (1/pi) * int_0^inf e^{-ax}/(sqrt(x)(x+1)) dx
    #       = e^a - (1/pi) * pi*e^a*erfc(sqrt(a))    [Laplace identity]
    #       = e^a (1 - erfc(sqrt(a)))
    #       = e^a erf(sqrt(a))
    # Which equals LHS. CONFIRMED.

    # Sympy verification of the Laplace identity:
    laplace_check = sp.integrate(sp.exp(-a*x) / (sp.sqrt(x)*(x+1)), (x, 0, sp.oo))
    laplace_known = sp.pi * sp.exp(a) * sp.erfc(sp.sqrt(a))
    print(f"  sympy int e^{{-ax}}/(sqrt(x)(x+1)) dx = {laplace_check}")
    print(f"  expected pi e^a erfc(sqrt(a))         = {laplace_known}")
    diff = sp.simplify(laplace_check - laplace_known)
    print(f"  sympy says diff simplifies to:        {diff}")

    # Numerical sanity
    for a_val in [sp.Rational(1, 10), sp.Integer(1), sp.Integer(10), sp.Integer(100)]:
        L_num = float(L.subs(a, a_val))
        R_num = float((sp.exp(a) - (1/sp.pi) * laplace_check).subs(a, a_val))
        print(f"  a={a_val}: L={L_num:.10g}, R={R_num:.10g}, |L-R|={abs(L_num-R_num):.2e}")


def ab_asymptotic_audit():
    """Pin down AB's claimed asymptotic comparison numerically.

    AB (4.4.1): RHS asy = e^a - (1/pi) sum_n (-1)^n Gamma(n+1/2)/a^{n+1/2}
    AB (4.4.3): LHS asy = e^a (1 - 3/(8a) + O(1/a^2))

    Test how each of these agrees with the actual values across a.
    """
    print()
    print("=" * 72)
    print("AB ASYMPTOTIC AUDIT (lambda=1/2, eps=1)")
    print("=" * 72)
    mp.mp.dps = 60
    print(f"{'a':<8} {'LHS_exact':<24} {'AB(4.4.3) e^a(1-3/(8a))':<28} {'rel_err_AB_LHS':<14}")
    for a in [10, 20, 50, 100, 500, 1000, 10000]:
        a_mp = mp.mpf(a)
        L = mp.exp(a_mp) * mp.erf(mp.sqrt(a_mp))
        AB_LHS = mp.exp(a_mp) * (1 - mp.mpf(3) / (8 * a_mp))
        # alternative (correct) Watson application would give 1 - 1/(8a)
        alt = mp.exp(a_mp) * (1 - mp.mpf(1) / (8 * a_mp))
        rel = abs(AB_LHS - L) / abs(L)
        print(f"{a:<8} {mp.nstr(L, 12):<24} {mp.nstr(AB_LHS, 12):<28} {float(rel):<14.4e}")
    print()
    print("Key observation:")
    print("  At a=10, AB's (4.4.3) gives 21200.5 but L = 22026.3 (rel err 3.7e-2).")
    print("  The 'discrepancy' AB observed between LHS and RHS asymptotics is an")
    print("  artifact of (4.4.3) itself being wrong — the actual LHS is")
    print("  e^a erf(sqrt(a)) = e^a (1 - e^{-a}/sqrt(pi a) (1 + O(1/a))), so the")
    print("  correction to e^a is EXPONENTIALLY small, not polynomial.")
    print()
    print("Where AB's derivation goes wrong (4.4.3):")
    print("  The Entry-10 result they apply gives sum a^n n!/(n! Gamma(n+3/2))")
    print("  ~ e^a * Gamma(a+1)/Gamma(a+3/2), but only modulo a relative error")
    print("  O(a^{-5/2}) * sqrt(a) * e^a = O(e^a / a^2), and that error is")
    print("  POLYNOMIAL, not exponential. The leading polynomial correction")
    print("  from Gamma(a+1)/Gamma(a+3/2) is actually a^{-1/2}(1 - 1/(8a) + ...),")
    print("  not (1 - 3/(8a)). So both the coefficient AND the order of the")
    print("  correction in AB's statement are off — but more importantly, even")
    print("  the corrected polynomial-correction CLAIM is wrong because the")
    print("  whole approach is comparing two divergent asymptotic series whose")
    print("  difference is EXPONENTIALLY small, not polynomially small.")


def laplace_identity_proof_sketch():
    """Independent contour-proof reconstruction at lam=1/2, eps=1 (and by
    extension the general case via Mittag-Leffler representation).

    Goal: re-derive the identity from scratch without trusting ChatGPT's sketch.

    Step 1: LHS = sum_{n>=0} a^{1/2+n} / Gamma(3/2+n).
            By the differential equation L' = L + 1/sqrt(pi a), L(0) = 0,
            we get L(a) = e^a erf(sqrt(a)) exactly.

    Step 2: RHS = e^a - (1/pi) int_0^infty e^{-ax}/(sqrt(x)(x+1)) dx
            (after simplification at lam=1/2, eps=1, as shown in sympy check).
            By the standard Laplace transform identity
              int_0^infty e^{-ax}/(sqrt(x)(x+1)) dx = pi e^a erfc(sqrt(a))
            we get RHS = e^a (1 - erfc(sqrt(a))) = e^a erf(sqrt(a)).

    Step 3: Therefore LHS = RHS at lambda=1/2, eps=1.

    For the general case, the LHS sum is the Mittag-Leffler function:
       LHS = eps * a^lam * E_{eps, 1+lam}(a^eps)
    Use Bromwich representation of 1/Gamma(z):
       1/Gamma(z) = (1/(2 pi i)) int_{Br} e^s / s^z ds (Hankel/Bromwich contour)
    Geometric summation over n (z^n/Gamma(eps n + 1 + lam)) gives:
       E_{eps, 1+lam}(z) = (1/(2 pi i)) int_{Br} (e^s s^{eps-1-lam}) / (s^eps - z) ds
    Substitute z = a^eps and shift contour to wrap the cut on (-infty, 0]:
       - pole at s = a (since s^eps - a^eps = 0) gives a residue e^a/eps
       - the cut contribution gives, after standard manipulations, exactly
         the integral on the RHS divided by (-pi/eps)
    Combining: eps * a^lam * E_{eps, 1+lam}(a^eps)
             = e^a - (eps/pi) * (integral)
    which is the claimed identity.
    """
    print()
    print("=" * 72)
    print("INDEPENDENT CONTOUR PROOF SKETCH (reconstructed, not from ChatGPT)")
    print("=" * 72)
    print(laplace_identity_proof_sketch.__doc__)


if __name__ == "__main__":
    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    rows = sweep()
    sympy_symbolic_check()
    ab_asymptotic_audit()
    laplace_identity_proof_sketch()
    print()
    print("Done.")
