"""Analysis 38 -- Adversarial verification of ChatGPT-Pro's 30-digit Brusselator
period claim (diary 67) and the Lambert-W conservative-cousin period formula.

System (Brusselator at A=1, B=3):
    x' = 1 - 4x + x^2 y
    y' = 3x - x^2 y

ChatGPT-Pro reports (via Poincare shooting at section x=1, dx/dt > 0):
    y_0* = 4.46889305620907548510997570325262400661836...
    T    = 7.15691992117987981979986960576635244970738...
    rho  = 2.51637579988970937917961166298e-4   (Poincare multiplier)

Verification protocol:
  Claim 1 (Brusselator period + multiplier):
    1. Implement Brusselator ODE in mpmath at dps>=40.
    2. Use mp.odefun (Taylor-series arbitrary-precision integrator) as the
       inner solver. Implementing DOPRI5 at high dps was tried in
       rkc/dynamics/rk45.py but mp.odefun is dramatically faster for this
       use case (per-step cost grows much more slowly with dps).
    3. Find a point on the section (x=1, y > 3) on the limit cycle, then
       iterate the Poincare return map. Because the cycle is strongly
       attracting (|rho| < 3e-4), simple fixed-point iteration converges
       quadratically.
    4. Compute the multiplier rho by central finite difference at small eps.
    5. Compare to ChatGPT digit-by-digit; verdict by the rubric.

  Claim 2 (Lambert-W conservative cousin):
    1. Verify u_-(E), u_+(E) satisfy u - log u = E for E in {1.1, 2, 5, 10, 100}.
    2. Tabulate T_0(E) and compare to direct ODE integration of u'' + 1 - 1/u = 0
       at the same energies.
    3. Plot/tabulate T_0(E) to show log-growth in E.
    4. Search for an E with T_0(E) = 7.157 (the true Brusselator period).
       If unique, report; otherwise report the gap.

Outputs:
  - analysis/results/38_brusselator_verification.csv
  - diary/68_brusselator_lambert_w_cousin_verification.md   (the writeup)
"""
from __future__ import annotations

import csv
import os
import time
from pathlib import Path

import mpmath as mp

from rkc.dynamics import (
    turning_points,
    period_cousin,
    period_cousin_ode,
    hamiltonian,
)


# ChatGPT-Pro reference values (diary 67)
CHATGPT_Y0  = "4.46889305620907548510997570325262400661836"
CHATGPT_T   = "7.15691992117987981979986960576635244970738"
CHATGPT_RHO = "2.51637579988970937917961166298e-4"


# ---------------------------------------------------------------------------
# Brusselator at A=1, B=3
# ---------------------------------------------------------------------------

A_PARAM = mp.mpf(1)
B_PARAM = mp.mpf(3)


def brusselator_rhs(t, y):
    x, yy = y[0], y[1]
    return [A_PARAM - (B_PARAM + 1) * x + x * x * yy,
            B_PARAM * x - x * x * yy]


def brusselator_x_dot(x, yy):
    return A_PARAM - (B_PARAM + 1) * x + x * x * yy


# ---------------------------------------------------------------------------
# Poincare return map at section Sigma = {x = 1, x_dot > 0}
# ---------------------------------------------------------------------------

def _bracket_return(sol, t_samples):
    """Walk through t_samples; find the first adjacent pair where x crosses 1
    from below (x_prev < 1, x >= 1)."""
    prev_t, prev_x = t_samples[0], sol(mp.mpf(t_samples[0]))[0]
    for t in t_samples[1:]:
        x = sol(mp.mpf(t))[0]
        if prev_x < 1 and x >= 1:
            return mp.mpf(prev_t), mp.mpf(t)
        prev_t, prev_x = t, x
    raise RuntimeError("no return crossing found in sample window")


def _refine_crossing(sol, a, b, dps_tol_margin=5):
    """Bisect on x(t) - 1 for t in [a, b]. Returns (t_cross, y_cross)."""
    tol = mp.mpf("10") ** (-(mp.mp.dps - dps_tol_margin))
    for _ in range(2000):
        m = (a + b) / 2
        x_m = sol(m)[0]
        if abs(x_m - 1) < tol:
            return m, sol(m)
        if x_m < 1:
            a = m
        else:
            b = m
    return m, sol(m)


def poincare_map(y_section, t_samples=None):
    """Take a point y on the section Sigma = {x=1, x_dot > 0} and return
    (T_return, P(y)) where P(y) is the y-value at the next intersection
    with Sigma (one cycle later).
    """
    if t_samples is None:
        # Brusselator period ~7.15; sample window safely around it
        t_samples = [4, 5, 6, 6.3, 6.7, 7, 7.3, 7.7, 8, 9]
    y0 = [mp.mpf(1), mp.mpf(y_section)]
    sol = mp.odefun(brusselator_rhs, mp.mpf(0), y0)
    a, b = _bracket_return(sol, t_samples)
    t_cross, y_cross = _refine_crossing(sol, a, b)
    # Verify x_dot > 0 at the crossing
    xdot = brusselator_x_dot(y_cross[0], y_cross[1])
    if xdot <= 0:
        raise RuntimeError("crossing direction wrong (xdot={})".format(mp.nstr(xdot, 5)))
    return t_cross, y_cross[1]


# ---------------------------------------------------------------------------
# Claim 1: full verification
# ---------------------------------------------------------------------------

def verify_brusselator(dps_target=35, max_iters=20, verbose=True):
    """Compute (y_0*, T*) at the given precision via fixed-point iteration
    of the Poincare return map, then compute rho by central finite diff.
    Returns a dict with all the numbers + agreement counts."""

    mp.mp.dps = dps_target

    # Initial guess from a low-precision scan
    y = mp.mpf("4.4688930562090759")  # ~15 sig digits, well within basin
    T = None

    if verbose:
        print(f"[brusselator] iterating return map at dps={dps_target}")
        print(f"[brusselator] initial y = {mp.nstr(y, 15)}")

    converged = False
    t_iter_start = time.time()
    for i in range(max_iters):
        t0 = time.time()
        T, y_next = poincare_map(y)
        dt = time.time() - t0
        delta = y_next - y
        if verbose:
            print(f"  iter {i}: T={mp.nstr(T, dps_target-3)}, |dy|={mp.nstr(abs(delta), 4)} ({dt:.1f}s)")
        y = y_next
        if abs(delta) < mp.mpf("10") ** (-(dps_target - 2)):
            converged = True
            break

    t_iter_total = time.time() - t_iter_start

    # Compute Poincare multiplier rho via central finite difference.
    # eps choice: with working dps ~ 60 we need eps such that quad term
    # ~ eps^2 * P'' is far below truncation but eps itself is well above
    # mp.mp.eps. Pick eps ~ 10^(-dps/2).
    rho_dps = max(dps_target * 2, 60)
    mp.mp.dps = rho_dps
    eps = mp.mpf("10") ** (-rho_dps // 2)
    y_hp = mp.mpf(y)
    t0 = time.time()
    _, P_plus = poincare_map(y_hp + eps)
    _, P_minus = poincare_map(y_hp - eps)
    rho = (P_plus - P_minus) / (2 * eps)
    rho_time = time.time() - t0

    if verbose:
        print(f"[brusselator] rho computed at working dps={rho_dps}, eps={mp.nstr(eps, 3)}, time {rho_time:.1f}s")

    # Compare to ChatGPT references
    chat_y0 = mp.mpf(CHATGPT_Y0)
    chat_T = mp.mpf(CHATGPT_T)
    chat_rho = mp.mpf(CHATGPT_RHO)

    err_y0 = abs(y - chat_y0)
    err_T = abs(T - chat_T)
    err_rho = abs(rho - chat_rho)
    rel_y0 = err_y0 / abs(chat_y0)
    rel_T = err_T / abs(chat_T)
    rel_rho = err_rho / abs(chat_rho)

    def _digit_count(rel):
        if rel == 0:
            return mp.mp.dps
        return int(-mp.log10(rel))

    return {
        "y0": y,
        "T": T,
        "rho": rho,
        "converged": converged,
        "iters_used": i + 1,
        "iter_time_s": t_iter_total,
        "rho_time_s": rho_time,
        "rho_eps": eps,
        "err_y0_rel": rel_y0,
        "err_T_rel": rel_T,
        "err_rho_rel": rel_rho,
        "digits_y0": _digit_count(rel_y0),
        "digits_T": _digit_count(rel_T),
        "digits_rho": _digit_count(rel_rho),
    }


# ---------------------------------------------------------------------------
# Claim 2: Lambert-W cousin
# ---------------------------------------------------------------------------

def verify_cousin(E_values=None, dps=40, verbose=True):
    """For each E:
       - check u_- - log u_- = E and u_+ - log u_+ = E.
       - compute T_0(E) by quadrature.
       - compute T_0(E) by direct ODE.
       - compare.
    Returns a list of dicts.
    """
    if E_values is None:
        E_values = [mp.mpf(s) for s in ["1.1", "2", "5", "10", "100", "1000"]]
    mp.mp.dps = dps
    rows = []
    for E in E_values:
        if verbose:
            print(f"[cousin] E={E}")
        u_minus, u_plus = turning_points(E)
        check_minus = u_minus - mp.log(u_minus) - E
        check_plus = u_plus - mp.log(u_plus) - E
        t0 = time.time()
        T_quad = period_cousin(E)
        t_quad = time.time() - t0
        # Direct ODE only at moderate E (it's slow + can be unstable for very large E)
        T_ode = None
        ode_time = None
        ode_match_digits = None
        if E <= mp.mpf(20):
            try:
                t0 = time.time()
                T_ode = period_cousin_ode(E, rk_dps=20)
                ode_time = time.time() - t0
                # rel digits
                rel = abs(T_ode - T_quad) / abs(T_quad)
                ode_match_digits = int(-mp.log10(rel + mp.mpf("1e-50")))
            except Exception as exc:
                if verbose:
                    print(f"  ODE failed: {exc}")
        rows.append({
            "E": E,
            "u_minus": u_minus,
            "u_plus": u_plus,
            "check_minus": check_minus,
            "check_plus": check_plus,
            "T_quad": T_quad,
            "T_quad_time_s": t_quad,
            "T_ode": T_ode,
            "T_ode_time_s": ode_time,
            "T_ode_match_digits": ode_match_digits,
        })
        if verbose:
            print(f"    u_-={mp.nstr(u_minus, 12)}, u_+={mp.nstr(u_plus, 12)}")
            print(f"    check_- = {mp.nstr(check_minus, 4)}, check_+ = {mp.nstr(check_plus, 4)}")
            print(f"    T_0(E) = {mp.nstr(T_quad, 15)}  ({t_quad:.2f}s)")
            if T_ode is not None:
                print(f"    T_ode  = {mp.nstr(T_ode, 15)}  ({ode_time:.1f}s, match ~{ode_match_digits} digits)")
    return rows


def search_E_giving_brusselator_period(rows, target_T=mp.mpf("7.157"),
                                       dps=40):
    """The cousin T_0(E) grows monotonically (from 2*pi at E=1+ to ~log(E) for
    E -> infty? actually sqrt-ish; see numerical results). Check whether the
    target Brusselator period 7.157 is hit by some E.
    """
    mp.mp.dps = dps
    target_T = mp.mpf(target_T)
    # Bracket: T_0(1.1) ~ 6.34 (just above 2pi); T_0(10) ~ 10.6 -> brackets 7.157.
    # Find E such that T_0(E) = 7.157.
    a, b = mp.mpf("1.1"), mp.mpf("10")
    Ta, Tb = period_cousin(a), period_cousin(b)
    if not (Ta < target_T < Tb or Tb < target_T < Ta):
        return None
    for _ in range(200):
        m = (a + b) / 2
        Tm = period_cousin(m)
        if abs(Tm - target_T) < mp.mpf("1e-30"):
            return m
        if (Tm < target_T) == (Ta < target_T):
            a, Ta = m, Tm
        else:
            b, Tb = m, Tm
    return m


# ---------------------------------------------------------------------------
# CSV writeout
# ---------------------------------------------------------------------------

def write_csv(claim1_result, claim2_rows, e_match, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["section", "field", "value"])
        # Claim 1
        w.writerow(["claim1", "y0_computed", mp.nstr(claim1_result["y0"], 36)])
        w.writerow(["claim1", "y0_chatgpt", CHATGPT_Y0])
        w.writerow(["claim1", "y0_relerr", mp.nstr(claim1_result["err_y0_rel"], 6)])
        w.writerow(["claim1", "y0_digits_match", claim1_result["digits_y0"]])
        w.writerow(["claim1", "T_computed", mp.nstr(claim1_result["T"], 36)])
        w.writerow(["claim1", "T_chatgpt", CHATGPT_T])
        w.writerow(["claim1", "T_relerr", mp.nstr(claim1_result["err_T_rel"], 6)])
        w.writerow(["claim1", "T_digits_match", claim1_result["digits_T"]])
        w.writerow(["claim1", "rho_computed", mp.nstr(claim1_result["rho"], 36)])
        w.writerow(["claim1", "rho_chatgpt", CHATGPT_RHO])
        w.writerow(["claim1", "rho_relerr", mp.nstr(claim1_result["err_rho_rel"], 6)])
        w.writerow(["claim1", "rho_digits_match", claim1_result["digits_rho"]])
        w.writerow(["claim1", "converged", claim1_result["converged"]])
        w.writerow(["claim1", "iter_time_s", "{:.2f}".format(claim1_result["iter_time_s"])])
        w.writerow(["claim1", "rho_time_s", "{:.2f}".format(claim1_result["rho_time_s"])])
        # Claim 2
        for row in claim2_rows:
            E = row["E"]
            tag = "E={}".format(mp.nstr(E, 6))
            w.writerow(["claim2", tag + ":u_minus", mp.nstr(row["u_minus"], 20)])
            w.writerow(["claim2", tag + ":u_plus", mp.nstr(row["u_plus"], 20)])
            w.writerow(["claim2", tag + ":check_minus", mp.nstr(row["check_minus"], 6)])
            w.writerow(["claim2", tag + ":check_plus", mp.nstr(row["check_plus"], 6)])
            w.writerow(["claim2", tag + ":T_quad", mp.nstr(row["T_quad"], 20)])
            if row["T_ode"] is not None:
                w.writerow(["claim2", tag + ":T_ode", mp.nstr(row["T_ode"], 20)])
                w.writerow(["claim2", tag + ":T_ode_match_digits", row["T_ode_match_digits"]])
        # Cousin search
        if e_match is not None:
            w.writerow(["claim2_search", "E_giving_T_7.157", mp.nstr(e_match, 20)])
            w.writerow(["claim2_search", "T_at_E_match",     mp.nstr(period_cousin(e_match), 20)])
        else:
            w.writerow(["claim2_search", "E_giving_T_7.157", "(none in [1.1, 10])"])
    return path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("Brusselator + Lambert-W cousin verification (analysis 38)")
    print("=" * 70)
    print()

    # Claim 1
    print(">>> Claim 1: Brusselator period at A=1, B=3 <<<")
    print()
    claim1 = verify_brusselator(dps_target=35, max_iters=20, verbose=True)
    print()
    print(f"  y_0  = {mp.nstr(claim1['y0'], 36)}")
    print(f"  y_0  | ChatGPT = {CHATGPT_Y0}")
    print(f"  digits match: {claim1['digits_y0']}")
    print()
    print(f"  T    = {mp.nstr(claim1['T'], 36)}")
    print(f"  T    | ChatGPT = {CHATGPT_T}")
    print(f"  digits match: {claim1['digits_T']}")
    print()
    print(f"  rho  = {mp.nstr(claim1['rho'], 36)}")
    print(f"  rho  | ChatGPT = {CHATGPT_RHO}")
    print(f"  digits match: {claim1['digits_rho']}")
    print()

    # Verdict for Claim 1
    digits_T = claim1["digits_T"]
    rho_rel = claim1["err_rho_rel"]
    if digits_T >= 25 and rho_rel < mp.mpf("0.01"):
        verdict1 = "CONFIRMED"
    elif digits_T >= 10:
        verdict1 = "PARTIAL"
    else:
        verdict1 = "REFUTED"
    print(f"  ==> Claim 1 verdict: {verdict1}")
    print()

    # Claim 2
    print(">>> Claim 2: Lambert-W conservative-cousin period formula <<<")
    print()
    claim2 = verify_cousin(dps=40, verbose=True)
    print()
    e_match = None
    try:
        e_match = search_E_giving_brusselator_period(claim2, target_T=mp.mpf("7.157"))
        if e_match is not None:
            T_at = period_cousin(e_match)
            print(f"  E giving T_0 = 7.157: E* = {mp.nstr(e_match, 20)}, T_0(E*) = {mp.nstr(T_at, 20)}")
        else:
            print("  No E in [1.1, 10] gives T_0 = 7.157.")
    except Exception as exc:
        print(f"  Cousin E-search failed: {exc}")

    # Verdict for Claim 2: all checks should be ~working precision
    cousin_ok = True
    for row in claim2:
        if abs(row["check_minus"]) > mp.mpf("1e-30"):
            cousin_ok = False
        if abs(row["check_plus"]) > mp.mpf("1e-30"):
            cousin_ok = False
        if row["T_ode"] is not None and row["T_ode_match_digits"] < 10:
            cousin_ok = False
    verdict2 = "CONFIRMED" if cousin_ok else "PARTIAL"
    print(f"\n  ==> Claim 2 verdict: {verdict2}")
    print()

    # Write CSV
    csv_path = Path(__file__).resolve().parent / "results" / "38_brusselator_verification.csv"
    write_csv(claim1, claim2, e_match, csv_path)
    print(f"Wrote {csv_path}")

    return {"claim1": claim1, "claim2": claim2, "verdict1": verdict1, "verdict2": verdict2, "e_match": e_match}


if __name__ == "__main__":
    main()
