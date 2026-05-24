"""
Experiment 21 — path-measure shadow probes for the Eichler integral g*(tau).

CONTEXT (see diary 13 / Exp 16 and diary 15 / Exp 18):

Exp 16 falsified four standard info-theoretic candidates (MI, KL, Surprise,
Fisher); Exp 18 falsified eight bounded-at-cusp candidates (Renyi-alpha,
Bhattacharyya, Hellinger^2, entropic uncertainty). Both experiments share
a structural limitation: they probe MARGINAL distributions of the
lattice-gas measure at a single beta. The Eichler integral
    g*(tau) = (i/sqrt(2)) integral_{-tau_bar}^{i*infty} g(w) / sqrt(-i(w+tau)) dw
IS structurally a PATH MEASURE — an integral over a path in the upper
half-plane. So the structurally-most-promising next probe is a path-measure
functional defined over a one-parameter family of lattice-gas distributions.

CONSTRUCTION (per the task brief)

A "cooling trajectory" is a path through state space parameterized by
inverse temperature beta(t), t in [0, 1]:

    beta(t) = beta_start * (beta_end / beta_start)^t        (log interpolation)

with beta_start = 1e-5 (deep cusp) and beta_end in {1e-3, 1e-2, 0.1,
0.3, 1, 3, 10}. The lattice-gas distribution P_{beta(t)} evolves along
this path. Three candidate functionals are probed against g*(beta_end):

  1. PATH ENTROPY PRODUCTION:
        S_prod = integral_0^1 dt * (d beta / dt) * <E>_{beta(t)}
     Standard Clausius-style entropy production along the cooling path,
     where <E>_beta is the mean energy of the signed n-marginal.

  2. PATH KL DIVERGENCE (cumulative):
        D_path = integral_0^1 dt * D_KL(P_{beta(t)} || P_{beta(t+dt)})
     Cumulative "distinguishability" along the cooling path. Uses the
     n-marginal of the signed distribution (positive; convention (a) from
     diary 15).

  3. EICHLER-SHAPED PATH AVERAGE:
        I_eich = integral_0^1 dt * g_density(beta(t)) * K(t)
     where K(t) = 1 / sqrt(tau_end - tau(t)) matches the Eichler integral's
     sqrt(-(w-tau)) kernel, and g_density(beta) = g(i*beta/(2*pi)) is the
     unary-theta shadow evaluated on the imaginary axis (the natural choice
     for "shadow density as a function of beta"). The path through the
     upper half-plane: tau(t) = i*beta(t)/(2*pi).

     Concretely (substituting the parameterization):
        tau_end - tau(t) = i (beta_end - beta(t)) / (2*pi)
        sqrt(tau_end - tau(t)) = sqrt(i) * sqrt((beta_end - beta(t))/(2*pi))
                                = e^{i pi/4} * sqrt((beta_end-beta(t))/(2*pi))
        K(t) = 1 / sqrt(tau_end - tau(t))
             = e^{-i pi/4} * sqrt(2*pi / (beta_end - beta(t)))
     We take the REAL PART for the test (g*(beta_end) is real, so a real
     functional is the natural counterpart). We also report the absolute
     value as a sanity check.

CONJECTURE BEING TESTED (candidate 3): g*(beta_end) equals (up to a
universal constant) this Eichler-shaped path average over the cooling path
through the lattice gas.

If TRUE: a clean concrete identity tying the Eichler integral to a
partition-function path integral — significant. Derives constant in closed
form below.

If FALSE: the shadow is NOT a path average over the natural lattice-gas
Markov chain, pushing the Eichler-cocycle conjecture toward "the cocycle
structure is intrinsic to Gamma acting on the upper half-plane and does
NOT reduce to a partition-function path integral".

NUMERICAL HYGIENE:
  - mp.dps = 40 throughout (trapezoidal rule limits accuracy to ~3-4 digits,
    so higher dps is overkill; 40 leaves headroom for the cumulative product).
  - 100 trapezoidal-rule steps for the path integrals.
  - n_max for the marginal is adaptive to beta(t): max(50, min(800, 20/beta(t))).
  - For the KL between consecutive distributions, we use a small relative
    spacing dt and divide; the integrand is finite (Fisher-like) so the
    discretization is well-conditioned.

ACCEPTANCE BAR (per spec, identical to Exp 16 / 18):
  max |candidate/g* - median(candidate/g*)| / median <= 1% across >= 2 dex
  of beta_end. Anything else FAILS.

  CANDIDATE 3 IS THE STRUCTURALLY-MOST-LIKELY-TO-MATCH CANDIDATE IN THE
  WHOLE INVESTIGATION. Therefore the strictest discipline applies. If it
  passes, derive the closed-form constant. If it fails, articulate
  precisely why.
"""
from __future__ import annotations
import csv
import importlib.util
import sys
from pathlib import Path

from mpmath import mp, mpf, exp, log, pi, sqrt, nstr, mpc, cos, sin, fabs

mp.dps = 40
# Trapezoidal rule on ~50-100 path steps limits accuracy to ~3-4 digits; dps
# = 40 leaves ample headroom for cumulative-product evaluation. Exp 16's
# g_star_iy is still computed by mpmath quad which retains ~30 digits.

# ---------------------------------------------------------------------------
# Import helpers from Exp 16 (lattice gas) and Exp 17 (Watson-Hickerson Eichler
# integral, etc.).
# ---------------------------------------------------------------------------
_HERE = Path(__file__).parent

def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, _HERE / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

exp16 = _load("exp16", "16_fep_mock_modular_toy.py")
exp17 = _load("exp17", "17_mock_theta_residual_ebm_v1.py")

# exp17 raises mp.dps to 80 (for its modular cross-check at >=30 digits);
# we reset to our chosen 40 after the imports complete.
mp.dps = 40

# Lattice-gas helpers
g_star_iy = exp16.g_star_iy
g_shadow_at_iy = exp16.g_shadow_at_iy
# Eichler integral helper from Exp 17 (Watson-Mordell form). We use it as
# an independent cross-check on g*; the proportionality test below uses
# exp16.g_star_iy (the integrand-form g*), which is what Exp 16 / 18 used.
watson_mordell_integral = exp17.watson_mordell_integral


# Fast signed-marginal: cumulative product is O(n_max) rather than the
# O(n_max^2) form used in exp16.signed_marginal_n (which re-multiplies the
# full product for each n). This is mathematically identical and pays for
# the ~100-step path sweep at large n_max.
def signed_marginal_n_fast(q: mpf, n_max: int) -> tuple[list[mpf], mpf]:
    """w_signed(n) = q^(n^2) / prod_{k=1..n} (1+q^k)^2, normalized.

    Computes the running cumulative product so total cost is O(n_max).
    """
    weights = []
    prod = mpf(1)  # prod_{k=1..n} (1+q^k)^2 ; starts at 1 for n=0.
    for n in range(n_max + 1):
        if n > 0:
            prod *= (1 + q ** n) ** 2
        weights.append(q ** (n * n) / prod)
    Z = sum(weights)
    return [w / Z for w in weights], Z


# In-module alias so module-level code still reads "signed_marginal_n".
signed_marginal_n = signed_marginal_n_fast


# Adaptive g_shadow_at_iy: the unary theta g(iy) = sum_{n in Z} (-1)^n (6n+1)
# exp(-2*pi*y*(6n+1)^2/24) is alternating-sign and SLOW to converge at small
# y (the exponent only suppresses tails like exp(-pi*y*n^2/2), so nrange ~
# 10 * sqrt(dps / y) is needed). We size adaptively.
def g_shadow_adaptive(y: mpf) -> mpf:
    """Adaptive nrange for g_shadow_at_iy; ensures tail is below 1e-(dps-5)."""
    # tail term at n=N is ~ exp(-2*pi*y*N^2*36/24) = exp(-3*pi*y*N^2). For this
    # to be < 10^{-(dps-5)}, need N^2 > (dps-5) * log(10) / (3*pi*y), i.e.
    # N > sqrt((dps-5) * log(10) / (3*pi*y)).
    from math import sqrt as fsqrt, log as flog, pi as fpi, ceil
    yf = max(float(y), 1e-20)
    target = (mp.dps - 5) * flog(10)
    N = int(ceil(fsqrt(target / (3 * fpi * yf)))) + 20
    N = max(N, 200)
    # Cap to avoid runaway at extreme cusps.
    N = min(N, 200000)
    return g_shadow_at_iy(y, nrange=N)


# ---------------------------------------------------------------------------
# Lattice-gas mean energy <E>_beta under the SIGNED n-marginal.
#
# E(C) = n^2 + sum_{k=1..n} k*(a_k+b_k); we want the expectation over the full
# signed measure but reduced to n. The conditional expectation of the
# k*(a_k+b_k) part given n requires summing (a_k+b_k) under the per-site signed
# weight (-1)^{a_k+b_k} q^{k(a_k+b_k)}. With two species this is the second
# moment of the per-site occupation. The closed-form result:
#
#   <a_k + b_k>_signed_per_site = 2 * d/d(log q^k) [ -log(1 + q^k) ]
#                                = -2 * q^k / (1 + q^k)
#
# (two species, with sign cancellation giving the (-)-log derivative of the
# fermionic-flavor partition function 1/(1+q^k) per species.)
#
# Wait: each species contributes a per-site sum sum_{a>=0} (-q^k)^a = 1/(1+q^k).
# Its derivative with respect to log q gives sum a (-q^k)^a / 1 = q^k *
# d/dq^k of 1/(1+q^k) = -q^k/(1+q^k)^2 (this is sum_a (-1)^a a (q^k)^a *
# (the un-normalized signed expectation). The signed-conditional expectation
# is this divided by the partition factor 1/(1+q^k), giving:
#
#   E[a_k]_signed = -q^k/(1+q^k)
#
# (Note: this is NEGATIVE for q in (0,1) — a hallmark of signed-measure
# "expectations" not being honest probabilistic means; this is a feature, not
# a bug — the energy is a SIGNED EXPECTATION, the natural quantity in this
# context.) With two species:
#
#   E[a_k + b_k]_signed = -2 q^k / (1+q^k).
#
# And E[E(C) | n]_signed = n^2 + sum_{k=1..n} k * (-2 q^k / (1+q^k))
#                       = n^2 - 2 * sum_{k=1..n} k * q^k / (1+q^k).
#
# So the full signed-expectation of E:
#
#   <E>_signed = sum_n p_signed(n) * (n^2 - 2 * sum_{k=1..n} k*q^k/(1+q^k)).
#
# We compute it this way to avoid materialising the joint distribution.
# ---------------------------------------------------------------------------
def signed_mean_energy(beta: mpf, n_max: int) -> mpf:
    q = exp(-beta)
    ps, _ = signed_marginal_n(q, n_max=n_max)
    # Precompute cumulative inner sums S_n = sum_{k=1..n} k*q^k/(1+q^k).
    S = [mpf(0)] * (n_max + 1)
    running = mpf(0)
    for k in range(1, n_max + 1):
        qk = q ** k
        running += k * qk / (1 + qk)
        S[k] = running
    mean = mpf(0)
    for n in range(n_max + 1):
        E_cond = mpf(n) * mpf(n) - 2 * S[n]  # signed conditional <E | n>
        mean += ps[n] * E_cond
    return mean


# ---------------------------------------------------------------------------
# Adaptive n_max (matches Exp 16 / 18 policy).
# ---------------------------------------------------------------------------
def adaptive_nmax(beta: mpf) -> int:
    nm = max(50, int(20 / float(beta)) if beta > mpf("0.01") else 800)
    return min(nm, 800)


# ---------------------------------------------------------------------------
# Cooling path & integrands.
# ---------------------------------------------------------------------------
def beta_of_t(t: mpf, beta_start: mpf, beta_end: mpf) -> mpf:
    """beta(t) = beta_start * (beta_end / beta_start)^t."""
    return beta_start * (beta_end / beta_start) ** t


def dbeta_dt(t: mpf, beta_start: mpf, beta_end: mpf) -> mpf:
    """d beta / dt = beta(t) * log(beta_end / beta_start)."""
    return beta_of_t(t, beta_start, beta_end) * log(beta_end / beta_start)


# Candidate 1: entropy production
def candidate_entropy_production(beta_start: mpf, beta_end: mpf, n_steps: int = 100) -> mpf:
    """S_prod = integral_0^1 dt * (d beta/dt) * <E>_{beta(t)}, trapezoidal rule."""
    pts = []
    for i in range(n_steps + 1):
        t = mpf(i) / n_steps
        b = beta_of_t(t, beta_start, beta_end)
        nm = adaptive_nmax(b)
        E = signed_mean_energy(b, nm)
        db = dbeta_dt(t, beta_start, beta_end)
        pts.append(db * E)
    # Trapezoidal
    total = mpf(0)
    for i in range(n_steps):
        total += (pts[i] + pts[i + 1]) / 2 * (mpf(1) / n_steps)
    return total


# Candidate 2: cumulative path KL
def kl_two_marginals(beta_a: mpf, beta_b: mpf, n_max: int) -> mpf:
    """D_KL( P_{beta_a}(n) || P_{beta_b}(n) ) on the signed n-marginals."""
    q_a = exp(-beta_a)
    q_b = exp(-beta_b)
    p_a, _ = signed_marginal_n(q_a, n_max=n_max)
    p_b, _ = signed_marginal_n(q_b, n_max=n_max)
    kl = mpf(0)
    for pa, pb in zip(p_a, p_b):
        if pa <= 0 or pb <= 0:
            continue
        kl += pa * log(pa / pb)
    return kl


def candidate_path_kl(beta_start: mpf, beta_end: mpf, n_steps: int = 100) -> mpf:
    """D_path = sum_t D_KL(P_{beta(t)} || P_{beta(t+dt)}) over the discretized path.

    NOTE: since the spec calls this a cumulative "distinguishability" along
    the path, we sum the per-step KLs (not divide-by-dt — that would be a
    Fisher-information-density form which we already tested in Exp 16). This
    is the natural "info-theoretic length" of the path.
    """
    dt = mpf(1) / n_steps
    total = mpf(0)
    for i in range(n_steps):
        t0 = mpf(i) * dt
        t1 = mpf(i + 1) * dt
        b0 = beta_of_t(t0, beta_start, beta_end)
        b1 = beta_of_t(t1, beta_start, beta_end)
        nm = adaptive_nmax(min(b0, b1))
        total += kl_two_marginals(b0, b1, n_max=nm)
    return total


# Candidate 3: Eichler-shaped path average.
#
# Path through the upper half-plane: tau(t) = i * beta(t) / (2*pi).
# K(t) = 1 / sqrt(tau_end - tau(t))
#      = 1 / sqrt( i*(beta_end - beta(t)) / (2*pi) )
#      = sqrt(2*pi / (beta_end - beta(t))) * 1/sqrt(i)
#      = sqrt(2*pi / (beta_end - beta(t))) * e^{-i*pi/4}.
# g_density(beta) = g(i*beta/(2*pi))   (unary theta shadow on imag axis;
# real-valued for real beta).
#
# So the Eichler-shaped integrand g_density(beta(t)) * K(t) is COMPLEX. The
# real part is cos(pi/4) * g_density * sqrt(2*pi / (beta_end-beta(t))) =
# (1/sqrt(2)) * g_density * sqrt(2*pi/(beta_end-beta(t))), and the imag part
# is -sin(pi/4) times the same. We compute the COMPLEX path integral and
# then report
#
#   I_eich_real = Re(integral)         (the natural real counterpart to g*)
#   I_eich_abs  = |integral|           (cross-check; for sanity)
#
# The integrand has an integrable square-root singularity at t = 1, i.e.
# beta(t) -> beta_end. Trapezoidal rule undercounts near a sqrt singularity;
# we therefore use an endpoint-correction: skip the t = 1 endpoint and add
# a closed-form correction integral for the asymptotic singular behavior
# (g_density(beta_end) * sqrt(2*pi) * 2 * sqrt(dt_min) / log(b_e/b_s)
# scaling). For numerical hygiene, we also report the value WITHOUT the
# correction and verify the ratios are consistent — if the correction
# dominates the answer, the candidate is intrinsically singular and the
# trapezoidal sweep doesn't tell us anything robust.
#
# Specifically, near t = 1: beta(t) ~ beta_end (1 - (1-t) log(b_e/b_s) +
# O((1-t)^2)), so beta_end - beta(t) ~ beta_end * log(b_e/b_s) * (1 - t),
# and sqrt(2*pi/(beta_end-beta(t))) ~ sqrt(2*pi/(beta_end * log(b_e/b_s))) /
# sqrt(1-t). The "tail" from t = 1 - eps to t = 1 contributes (in the
# real part):
#
#   real_tail = (1/sqrt(2)) * g_density(beta_end) * sqrt(2*pi/(beta_end *
#               log(b_e/b_s))) * integral_{1-eps}^1 dt / sqrt(1-t)
#             = (1/sqrt(2)) * g_density(beta_end) * sqrt(2*pi/(beta_end *
#               log(b_e/b_s))) * 2 * sqrt(eps)
#
# i.e., the singularity is integrable and the tail vanishes like sqrt(eps);
# but discrete trapezoidal evaluation OVERESTIMATES the endpoint
# contribution by approximately f(1)*dt/2 instead of the correct
# integral_{1-dt}^1 f = O(sqrt(dt)). We therefore use the
# substitution u = sqrt(1 - t), which removes the singularity (du = -dt /
# (2*sqrt(1-t)), so dt = -2*u du, and the integrand in u becomes regular):
#
#   integral_0^1 f(t) dt = integral_0^1 f(1 - u^2) * 2*u du   (with u = sqrt(1-t))
#
# In u-coordinates the integrand is bounded and trapezoidal rule converges
# at O(n^{-2}). We use this u-substitution for candidate 3.
def candidate_eichler_path_avg(
    beta_start: mpf, beta_end: mpf, n_steps: int = 200
) -> dict:
    """Eichler-shaped path average; returns dict with .real, .imag, .abs."""
    # u-substitution: t = 1 - u^2, dt = -2u du. integral_0^1 f(t) dt =
    # integral_0^1 f(1 - u^2) * 2*u du. At u = 0 -> t = 1 (singular endpoint);
    # the 2*u factor exactly cancels the 1/sqrt(1-t) = 1/u singularity.
    pi_4 = pi / 4
    cos_pi4 = cos(pi_4)
    sin_pi4 = sin(pi_4)
    # We compute real and imag parts separately.
    def integrand_in_u(u: mpf) -> mpc:
        t = mpf(1) - u * u
        b = beta_of_t(t, beta_start, beta_end)
        # Tau path point and tau_end on imaginary axis.
        # K(t) = exp(-i*pi/4) * sqrt(2 pi / (beta_end - b)).
        # When u = 0 (t = 1), beta_end - b = 0 and K -> infty; but with the
        # 2*u Jacobian factor the product is finite — we compute the limit
        # explicitly.
        diff = beta_end - b
        if diff <= 0:
            # u = 0 limit: use Taylor expansion. b = beta_end - beta_end * log(b_e/b_s) * u^2 + ...
            # So beta_end - b ~ beta_end * log(b_e/b_s) * u^2.
            # sqrt(2*pi/(beta_end - b)) ~ sqrt(2*pi/(beta_end*log(b_e/b_s))) / u.
            # Multiplied by 2*u, the Jacobian gives:
            #   2*u * sqrt(2*pi/(beta_end*log(b_e/b_s))) / u
            # = 2 * sqrt(2*pi/(beta_end*log(b_e/b_s))).
            # g_density at u=0 is g(i*beta_end/(2*pi)).
            y_end = beta_end / (2 * pi)
            g_end = g_shadow_adaptive(y_end)
            mag = 2 * sqrt(2 * pi / (beta_end * log(beta_end / beta_start)))
            return mpc(cos_pi4 * g_end * mag, -sin_pi4 * g_end * mag)
        y = b / (2 * pi)
        g_val = g_shadow_adaptive(y)
        K_mag = sqrt(2 * pi / diff)
        # Multiply by Jacobian 2*u.
        prefactor = 2 * u * g_val * K_mag
        return mpc(cos_pi4 * prefactor, -sin_pi4 * prefactor)

    # Trapezoidal over u in [0, 1].
    real_total = mpf(0)
    imag_total = mpf(0)
    pts = []
    for i in range(n_steps + 1):
        u = mpf(i) / n_steps
        val = integrand_in_u(u)
        pts.append(val)
    for i in range(n_steps):
        avg = (pts[i] + pts[i + 1]) / 2
        real_total += avg.real / n_steps
        imag_total += avg.imag / n_steps
    z = mpc(real_total, imag_total)
    return {"real": real_total, "imag": imag_total, "abs": fabs(z)}


# ---------------------------------------------------------------------------
# Driver.
# ---------------------------------------------------------------------------
def main():
    out_path = _HERE / "results" / "path_measure_shadow.csv"
    out_path.parent.mkdir(exist_ok=True)

    # Standard beta_end grid (from the spec).
    beta_end_grid = [mpf("1e-3"), mpf("1e-2"), mpf("0.1"), mpf("0.3"),
                     mpf("1"), mpf("3"), mpf("10")]
    beta_start = mpf("1e-5")

    print("=" * 78)
    print("Experiment 21 — path-measure shadow probes.")
    print(f"  Cooling path: beta(t) = {float(beta_start):.0e} * (beta_end/{float(beta_start):.0e})^t,")
    print(f"                t in [0, 1], 100 steps trapezoidal (200 for cand 3).")
    print(f"  beta_end grid: {[float(b) for b in beta_end_grid]}")
    print(f"  mp.dps = {mp.dps}.")
    print("=" * 78)
    print()

    # Compute g* for each beta_end (the target).
    g_star_values: dict[mpf, mpf] = {}
    for be in beta_end_grid:
        y = be / (2 * pi)
        g_star_values[be] = g_star_iy(y)

    # Compute candidate 1 (entropy production) for each beta_end.
    print("Candidate 1: PATH ENTROPY PRODUCTION.")
    print(f"{'beta_end':>10}  {'S_prod':>16}  {'g*':>14}  {'ratio':>14}")
    print("-" * 60)
    c1_results = []
    for be in beta_end_grid:
        S = candidate_entropy_production(beta_start, be, n_steps=100)
        gs = g_star_values[be]
        ratio = S / gs if gs != 0 else mpf("nan")
        c1_results.append((be, S, gs, ratio))
        print(f"{float(be):>10.4g}  {float(S):>16.6g}  {float(gs):>14.6g}  {float(ratio):>14.6g}")

    # Compute candidate 2 (path KL) for each beta_end.
    print()
    print("Candidate 2: CUMULATIVE PATH KL DIVERGENCE.")
    print(f"{'beta_end':>10}  {'D_path':>16}  {'g*':>14}  {'ratio':>14}")
    print("-" * 60)
    c2_results = []
    for be in beta_end_grid:
        D = candidate_path_kl(beta_start, be, n_steps=100)
        gs = g_star_values[be]
        ratio = D / gs if gs != 0 else mpf("nan")
        c2_results.append((be, D, gs, ratio))
        print(f"{float(be):>10.4g}  {float(D):>16.6g}  {float(gs):>14.6g}  {float(ratio):>14.6g}")

    # Compute candidate 3 (Eichler-shaped path average) for each beta_end.
    print()
    print("Candidate 3: EICHLER-SHAPED PATH AVERAGE (the candidate most likely to match).")
    print(f"{'beta_end':>10}  {'I_eich.real':>16}  {'I_eich.abs':>14}  "
          f"{'g*':>10}  {'ratio_real':>12}  {'ratio_abs':>12}")
    print("-" * 90)
    c3_results = []
    for be in beta_end_grid:
        I = candidate_eichler_path_avg(beta_start, be, n_steps=200)
        gs = g_star_values[be]
        ratio_r = I["real"] / gs if gs != 0 else mpf("nan")
        ratio_a = I["abs"] / gs if gs != 0 else mpf("nan")
        c3_results.append((be, I["real"], I["imag"], I["abs"], gs, ratio_r, ratio_a))
        print(f"{float(be):>10.4g}  {float(I['real']):>16.6g}  {float(I['abs']):>14.6g}  "
              f"{float(gs):>10.6g}  {float(ratio_r):>12.6g}  {float(ratio_a):>12.6g}")

    # ---------- Proportionality tests ----------
    print()
    print("=" * 78)
    print("Proportionality tests (strict bar: max |ratio - median|/median <= 1%).")
    print()

    def evaluate(name: str, values_and_g_and_ratio: list):
        ratios = [r for (_, _, _, r) in values_and_g_and_ratio if r == r]  # drop NaN
        if not ratios:
            return name, mpf("nan"), mpf("nan"), "SKIP"
        med = sorted(ratios)[len(ratios) // 2]
        if med == 0:
            return name, mpf(0), mpf("inf"), "FAIL"
        max_dev = max(abs(r - med) / abs(med) for r in ratios)
        if max_dev < mpf("0.01"):
            verdict = "PASS"
        elif max_dev < mpf("0.2"):
            verdict = "NEAR-PASS"
        else:
            verdict = "FAIL"
        return name, med, max_dev, verdict

    # For candidate 3 we evaluate both ratio_real and ratio_abs.
    summary = []
    summary.append(evaluate("entropy_production", c1_results))
    summary.append(evaluate("path_KL", c2_results))
    summary.append(evaluate(
        "eichler_path_avg_real",
        [(be, I_real, gs, ratio_r) for (be, I_real, _, _, gs, ratio_r, _) in c3_results]
    ))
    summary.append(evaluate(
        "eichler_path_avg_abs",
        [(be, I_abs, gs, ratio_a) for (be, _, _, I_abs, gs, _, ratio_a) in c3_results]
    ))

    print(f"  {'candidate':>26}  {'median ratio':>14}  {'max rel dev':>14}  {'verdict':>10}")
    print("-" * 78)
    for name, med, max_dev, verdict in summary:
        print(f"  {name:>26}  {nstr(med, 6):>14}  {nstr(max_dev, 6):>14}  {verdict:>10}")

    # ---------- Cusp / large-beta sanity ----------
    print()
    print("Cusp limit g*(beta -> 0) and large-beta behavior:")
    y_cusp = mpf("1e-7")
    print(f"  g*(beta=2*pi*1e-7 ~ 0)       = {nstr(g_star_iy(y_cusp), 8)}")
    print(f"  g*(beta=10)                  = {nstr(g_star_iy(mpf(10)/(2*pi)), 8)}")
    print()

    # ---------- Closed-form constant check for candidate 3 (if it passes) ----------
    print("Closed-form constant analysis for candidate 3:")
    # Median ratio (real and abs)
    _, med_r, max_dev_r, verdict_r = summary[2]
    _, med_a, max_dev_a, verdict_a = summary[3]
    print(f"  median ratio (real) = {nstr(med_r, 8)}, max rel dev = {nstr(max_dev_r, 5)}, "
          f"verdict = {verdict_r}")
    print(f"  median ratio (abs)  = {nstr(med_a, 8)}, max rel dev = {nstr(max_dev_a, 5)}, "
          f"verdict = {verdict_a}")
    # Compare to candidate closed-form constants the conjecture would predict:
    #   - If g*(beta_end) = c * integral_0^1 g(i*beta(t)/(2pi)) * K(t) dt,
    #     then with no fudges in normalization, c should be a simple rational
    #     multiple of sqrt(2*pi) or similar. Print plausible values:
    print(f"  candidate closed-form constants:")
    print(f"    sqrt(pi)       = {float(sqrt(pi)):.6f}")
    print(f"    sqrt(2*pi)     = {float(sqrt(2*pi)):.6f}")
    print(f"    1/sqrt(2)      = {float(1/sqrt(2)):.6f}")
    print(f"    pi/sqrt(2)     = {float(pi/sqrt(2)):.6f}")
    print(f"    2/sqrt(pi)     = {float(2/sqrt(pi)):.6f}")
    if verdict_r in ("PASS", "NEAR-PASS"):
        print(f"    -> verdict {verdict_r} -- closed-form check warranted.")
    else:
        print(f"    -> verdict FAIL -- no constant exists that matches; the conjecture is FALSE.")

    # ---------- Write CSV ----------
    rows = []
    # Candidate 1 rows
    # Build a median ratio per candidate to attach rel_dev_from_median_ratio.
    med_c1 = sorted([r for (_, _, _, r) in c1_results])[len(c1_results) // 2]
    med_c2 = sorted([r for (_, _, _, r) in c2_results])[len(c2_results) // 2]
    med_c3r = sorted([r for (_, _, _, _, _, r, _) in c3_results])[len(c3_results) // 2]
    med_c3a = sorted([r for (_, _, _, _, _, _, r) in c3_results])[len(c3_results) // 2]

    def reldev(r, med):
        return float(abs(r - med) / abs(med)) if med != 0 else float("inf")

    for (be, S, gs, ratio) in c1_results:
        rows.append({
            "beta_end": float(be),
            "candidate_name": "entropy_production",
            "candidate_value": float(S),
            "g_star_value": float(gs),
            "ratio": float(ratio),
            "rel_dev_from_median_ratio": reldev(ratio, med_c1),
        })
    for (be, D, gs, ratio) in c2_results:
        rows.append({
            "beta_end": float(be),
            "candidate_name": "path_KL",
            "candidate_value": float(D),
            "g_star_value": float(gs),
            "ratio": float(ratio),
            "rel_dev_from_median_ratio": reldev(ratio, med_c2),
        })
    for (be, I_real, I_imag, I_abs, gs, ratio_r, ratio_a) in c3_results:
        rows.append({
            "beta_end": float(be),
            "candidate_name": "eichler_path_avg_real",
            "candidate_value": float(I_real),
            "g_star_value": float(gs),
            "ratio": float(ratio_r),
            "rel_dev_from_median_ratio": reldev(ratio_r, med_c3r),
        })
        rows.append({
            "beta_end": float(be),
            "candidate_name": "eichler_path_avg_abs",
            "candidate_value": float(I_abs),
            "g_star_value": float(gs),
            "ratio": float(ratio_a),
            "rel_dev_from_median_ratio": reldev(ratio_a, med_c3a),
        })

    header = ["beta_end", "candidate_name", "candidate_value", "g_star_value",
              "ratio", "rel_dev_from_median_ratio"]
    with open(out_path, "w", newline="") as fp:
        w = csv.DictWriter(fp, fieldnames=header)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in header})

    print()
    print(f"Wrote {out_path}")
    print()
    print("=" * 78)
    print("Falsification criteria (each candidate):")
    print("  - PASS  if max |candidate/g* - median|/median <= 1% across full sweep.")
    print("  - NEAR-PASS if (1%, 20%]; reported but NOT a match.")
    print("  - FAIL  otherwise.")
    print()
    print("Candidate 1 falsified if: ratio S_prod/g* varies by > 1% across the grid.")
    print("Candidate 2 falsified if: ratio D_path/g* varies by > 1% across the grid.")
    print("Candidate 3 falsified if: ratio Re(I_eich)/g* varies by > 1% across the grid.")
    print("  (Equivalent for |I_eich|/g*.)")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
