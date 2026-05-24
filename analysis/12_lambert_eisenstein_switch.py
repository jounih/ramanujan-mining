"""
Experiment 12 — Lambert-series <-> Eisenstein modular switching curve.

Quantity (for odd k in {3, 5, 7}):

    L_k(q) = sum_{n>=1} n^k q^n / (1 - q^n)
           = sum_{n>=1} sigma_k(n) q^n               (divisor-sum form)

For odd k >= 3 the Lambert series equals a normalized Eisenstein series:

    E_{k+1}(tau) = 1 - (2(k+1)/B_{k+1}) sum_{n>=1} sigma_k(n) q^n,
                              q = e^{2 pi i tau}.

So

    L_k(q) = c_k * (E_{k+1}(tau) - 1),     c_k = -B_{k+1}/(2(k+1)).

We use q = e^{-beta}, i.e. tau = i beta / (2 pi). The Eisenstein S-transform
    E_{k+1}(-1/tau) = tau^{k+1} E_{k+1}(tau)     (k+1 even >= 4)
gives a fast-converging dual when beta is small. With tau = i beta/(2 pi),
    -1/tau = 2 pi i / beta,   q' = e^{-4 pi^2 / beta},
    tau^{-(k+1)} = i^{-(k+1)} (2 pi / beta)^{k+1}
                 = (-1)^{(k+1)/2} (2 pi / beta)^{k+1}   (k+1 even).

So the MODULAR-side identity is:

    E_{k+1}(tau) = (-1)^{(k+1)/2} (2 pi / beta)^{k+1} * E_{k+1}(2 pi i / beta).

That gives the modular evaluator:

    L_k(q)  =  c_k * ( (-1)^{(k+1)/2} (2 pi / beta)^{k+1}
                       * [1 - (2(k+1)/B_{k+1}) * S(q')]
                       - 1 ),

where S(q') = sum_{n>=1} sigma_k(n) q'^n with q' = e^{-4 pi^2 / beta}.

Methods compared:
    DIRECT     -- truncate sum_{n=1..N} sigma_k(n) q^n with
                  term-bound  sigma_k(n) q^n <= zeta(k) * n^k * e^{-beta n} < tol.
    MODULAR    -- truncate sum_{n=1..N'} sigma_k(n) q'^n with the same shape,
                  using beta' = 4 pi^2 / beta and a tolerance scaled by the
                  outer prefactor c_k * (2(k+1)/B_{k+1}) * (2 pi/beta)^{k+1}.

Cross-validation: at one (k, beta) cell both routes must agree to >= 40 digits
before any benchmark cell is written.

Sweep:
    k    in {3, 5, 7}
    beta in {1e-4, 1e-3, 1e-2, 1e-1, 1, pi, 10, pi^2, 100}     (log-ish)
    tol  in {1e-10, 1e-30, 1e-60}

Outputs:
    ramanujan/analysis/results/lambert_eisenstein_switch.csv
"""
from __future__ import annotations
import csv
import math
import time
from pathlib import Path
from mpmath import mp, mpf, exp, pi, log, ceil, bernoulli, zeta


# ---------------------------------------------------------------------------
# arithmetic helpers
# ---------------------------------------------------------------------------

def sigma_k(k: int, n: int) -> mpf:
    """Divisor sum sigma_k(n) = sum_{d|n} d^k, returned as mpf."""
    s = mpf(0)
    d = 1
    while d * d <= n:
        if n % d == 0:
            s += mpf(d) ** k
            other = n // d
            if other != d:
                s += mpf(other) ** k
        d += 1
    return s


# ---------------------------------------------------------------------------
# term-count certificates
#
# Both sides have the same structural truncation: a sum sum_{n>=1} sigma_k(n) x^n
# with x = e^{-b} for some positive b. Use the elementary bound
#     sigma_k(n)/n^k = sum_{d|n} 1/d^k <= zeta(k)    (k > 1)
# So term_n <= zeta(k) * n^k * e^{-b n}. Solve n^k e^{-b n} < tol / zeta(k):
#     b*n - k*ln(n) > ln(zeta(k)/tol).
# We invert this with a few Newton steps starting from n = ln(zeta(k)/tol)/b.
# ---------------------------------------------------------------------------

def _terms_for_geom(k: int, b: mpf, tol: mpf) -> int:
    """Smallest N s.t. N^k exp(-b N) < tol / zeta(k). Returns N (>= 1)."""
    if tol <= 0:
        return 1
    zk = zeta(k)
    rhs = log(zk / tol)
    if rhs <= 0:
        return 1
    # initial guess: ignore the k log n term
    n = rhs / b
    # 4 Newton steps on f(n) = b n - k log n - rhs
    for _ in range(40):
        if n <= k:  # avoid log(<=0)
            n = mpf(k) + 1
        f = b * n - k * log(n) - rhs
        fp = b - mpf(k) / n
        if fp == 0:
            break
        n_new = n - f / fp
        if n_new <= 0:
            n_new = n / 2
        if abs(n_new - n) < mpf("1e-3"):
            n = n_new
            break
        n = n_new
    # round up and verify
    N = int(ceil(n)) + 1
    while mpf(N) ** k * exp(-b * N) >= tol / zk and N < 10 ** 8:
        N += max(1, N // 32)
    return max(N, 1)


def terms_direct(k: int, beta: mpf, tol: mpf) -> int:
    """Truncation for sum sigma_k(n) e^{-beta n} < tol."""
    return _terms_for_geom(k, beta, tol)


def terms_modular(k: int, beta: mpf, tol: mpf) -> int:
    """Truncation for the modular sum sigma_k(n) (q')^n with q' = e^{-4 pi^2/beta}.

    The modular sum sits inside the chain
        L_k(q) = c_k * ( sign * (2 pi/beta)^{k+1}
                         * [1 - (2(k+1)/B_{k+1}) * S(q')] - 1 ).
    The outer linear factor multiplying S(q') is
        A = |c_k| * (2(k+1)/|B_{k+1}|) * (2 pi/beta)^{k+1}
          = (2 pi/beta)^{k+1}          (since |c_k|*(2(k+1)/|B_{k+1}|) = 1).
    So a tolerance tol on L_k corresponds to tol/A on the inner sum.
    """
    inner_tol = tol * (beta / (2 * pi)) ** (k + 1)
    if inner_tol <= 0:
        inner_tol = mpf("1e-1000")
    b = 4 * pi * pi / beta
    return _terms_for_geom(k, b, inner_tol)


# ---------------------------------------------------------------------------
# evaluators
# ---------------------------------------------------------------------------

def L_direct(k: int, beta: mpf, N: int) -> mpf:
    """Direct evaluation L_k(q) = sum_{n=1..N} sigma_k(n) e^{-beta n}."""
    s = mpf(0)
    qn = exp(-beta)             # q^1
    q1 = qn
    for n in range(1, N + 1):
        s += sigma_k(k, n) * qn
        qn *= q1
    return s


def L_modular(k: int, beta: mpf, Nprime: int) -> mpf:
    """Modular-side evaluation of L_k(q) using
       E_{k+1}(tau) = sign * (2 pi/beta)^{k+1} * E_{k+1}(2 pi i / beta),
       q' = e^{-4 pi^2 / beta}.
       L_k(q) = c_k * (E_{k+1}(tau) - 1).
    """
    Bkp1 = bernoulli(k + 1)
    c_k = -Bkp1 / (2 * (k + 1))
    sign = mpf(-1) ** ((k + 1) // 2)
    factor = sign * (2 * pi / beta) ** (k + 1)
    qp = exp(-4 * pi * pi / beta)
    s = mpf(0)
    qn = qp
    for n in range(1, Nprime + 1):
        s += sigma_k(k, n) * qn
        qn *= qp
    E_at_minus_inv = 1 - (2 * (k + 1) / Bkp1) * s
    E_tau = factor * E_at_minus_inv
    return c_k * (E_tau - 1)


# ---------------------------------------------------------------------------
# cross-validation (mandatory before benchmarking)
# ---------------------------------------------------------------------------

def cross_validate(k: int, beta_str: str, digits: int = 60) -> mpf:
    """At (k, beta), evaluate both methods to ~digits precision and
    return the number of agreeing leading digits."""
    save_dps = mp.dps
    mp.dps = digits + 30
    beta = mpf(beta_str)
    tol = mpf(10) ** -(digits + 5)
    Nd = terms_direct(k, beta, tol)
    Nm = terms_modular(k, beta, tol)
    Ld = L_direct(k, beta, Nd)
    Lm = L_modular(k, beta, Nm)
    rel = abs(Ld - Lm) / (abs(Ld) + mpf(10) ** -(digits + 10))
    if rel == 0:
        agree_digits = mpf("inf")
    else:
        agree_digits = -log(rel) / log(10)
    mp.dps = save_dps
    return Ld, Lm, rel, agree_digits, Nd, Nm


# ---------------------------------------------------------------------------
# main sweep
# ---------------------------------------------------------------------------

CAP = 200_000  # don't actually evaluate if a route demands more than this


def main():
    out_path = Path(__file__).parent / "results" / "lambert_eisenstein_switch.csv"
    out_path.parent.mkdir(exist_ok=True)

    # ---- mandatory cross-validation gate ----
    mp.dps = 100
    print("Cross-validation (mandatory): both methods must agree to >= 40 digits")
    print(f"{'k':>3} {'beta':>10} {'agree_digits':>14} {'Nd':>8} {'Nm':>8}")
    for k_, beta_str in [(3, "1.0"), (5, "0.5"), (7, "2.0")]:
        Ld, Lm, rel, ad, Nd, Nm = cross_validate(k_, beta_str, digits=60)
        agree_str = "inf" if ad == mpf("inf") else f"{float(ad):.1f}"
        print(f"{k_:>3} {beta_str:>10} {agree_str:>14} {Nd:>8} {Nm:>8}")
        if not (ad == mpf("inf") or float(ad) >= 40):
            raise SystemExit(
                f"ABORT: methods disagree at k={k_}, beta={beta_str}: "
                f"rel={float(rel):.3e}, agree_digits={float(ad):.2f}. "
                "Suspected normalization bug; DO NOT paper over."
            )
    print("Cross-validation PASSED.\n")

    # ---- sweep ----
    betas = [mpf("1e-4"), mpf("1e-3"), mpf("1e-2"), mpf("0.1"),
             mpf(1), pi, mpf(10), pi * pi, mpf(100)]
    beta_labels = ["1e-4", "1e-3", "1e-2", "0.1", "1", "pi",
                   "10", "pi^2", "100"]
    tols = [mpf("1e-10"), mpf("1e-30"), mpf("1e-60")]
    ks = [3, 5, 7]

    rows = []
    print(f"{'k':>2} {'beta':>10} {'tol':>8} {'Nd':>10} {'Nm':>10} {'gain':>10} "
          f"{'route':>6} {'t_dir':>9} {'t_mod':>9} {'check':>10}")
    print("-" * 100)

    for tol in tols:
        # working precision: need to certify to tol, plus headroom for the
        # modular prefactor and any cancellation when L_k is exponentially
        # tiny. At large beta the modular formula is
        #     L_k = c_k * ((2pi/beta)^{k+1} * E_{k+1}(2pi i/beta) - 1)
        # whose RHS is the difference of a finite quantity from 1; if L_k
        # itself is O(e^{-beta}), cancellation eats ~ beta/log(10) digits.
        # We provision for it explicitly.
        for beta, blabel in zip(betas, beta_labels):
            cancellation_pad = max(0, int(float(beta) / math.log(10)) + 5)
            dps = max(80,
                      int(-float(log(tol)) / math.log(10)) + 40
                      + cancellation_pad)
            mp.dps = dps
            for k in ks:
                Nd_full = terms_direct(k, beta, tol)
                Nm_full = terms_modular(k, beta, tol)

                # Wall-clock the cheap route always; only run the expensive route
                # if its size is under CAP (otherwise we trust the certificate).
                # We still try to compute the value_check using whichever route
                # actually ran.
                Nd_eval = Nd_full if Nd_full <= CAP else None
                Nm_eval = Nm_full if Nm_full <= CAP else None

                # Time direct
                if Nd_eval is not None:
                    t0 = time.perf_counter()
                    Ld = L_direct(k, beta, Nd_eval)
                    t_direct = time.perf_counter() - t0
                else:
                    Ld = None
                    t_direct = float("nan")

                # Time modular
                if Nm_eval is not None:
                    t0 = time.perf_counter()
                    Lm = L_modular(k, beta, Nm_eval)
                    t_modular = time.perf_counter() - t0
                else:
                    Lm = None
                    t_modular = float("nan")

                # value_check = rel difference when both available, else nan
                if Ld is not None and Lm is not None:
                    val_check = float(abs(Ld - Lm) /
                                      (abs(Ld) + mpf(10) ** -(dps - 5)))
                else:
                    val_check = float("nan")

                gain = Nd_full / Nm_full if Nm_full > 0 else float("inf")
                route = "MOD" if Nm_full < Nd_full else "DIR"

                print(f"{k:>2} {blabel:>10} {float(tol):>8.0e} "
                      f"{Nd_full:>10d} {Nm_full:>10d} {float(gain):>10.3g} "
                      f"{route:>6} {t_direct:>9.3g} {t_modular:>9.3g} "
                      f"{val_check:>10.2e}")

                rows.append(dict(k=k, beta=float(beta),
                                 tol=float(tol), method="DIRECT",
                                 terms=Nd_full, wall_seconds=t_direct,
                                 value_check=val_check))
                rows.append(dict(k=k, beta=float(beta),
                                 tol=float(tol), method="MODULAR",
                                 terms=Nm_full, wall_seconds=t_modular,
                                 value_check=val_check))

    # ---- write csv ----
    fields = ["k", "beta", "tol", "method", "terms",
              "wall_seconds", "value_check"]
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
