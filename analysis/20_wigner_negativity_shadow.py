"""
Experiment 20 — Wigner-negativity-aware divergences on the joint signed measure
of the FEP × mock-modular toy lattice gas.

CONTEXT
-------
Twelve standard info-theoretic candidates have been falsified as shadow analogs
(Exp 16 four candidates, Exp 18 eight bounded-at-cusp candidates). Both prior
experiments operated on the *n-marginal* — which is positive after summing out
the bosonic occupations. Diary 15's recommendation: the missing structural
piece may be the sign cancellations *inside* each n-sector. Promote the test
to the joint (n, m) representation where the signs are explicit, and probe
Wigner-negativity-aware divergences.

JOINT SIGNED WEIGHT W(n, m)
---------------------------
The lattice gas Hamiltonian is

    E(C) = n^2 + sum_{k=1..n} k * (a_k + b_k),
    weight(C) = (-1)^{sum_k (a_k+b_k)} * q^{E(C)}    (z = -1).

We define the JOINT representation by aggregating over configurations with
the same (n, m), where m = total occupation = sum_k (a_k + b_k):

    W(n, m) = (-1)^m * q^{n^2}
              * sum_{(p_1, ..., p_n) : sum p_i = m} prod_{i=1..n} (p_i + 1) * q^{i p_i}

The factor (p_i+1) comes from collapsing (a_i, b_i) with a_i+b_i=p_i: there
are (p_i+1) ways to split p_i particles between the two species. The sign
(-1)^m is the surviving (-1)^F for given total occupation m. So W(n, m) is
SIGNED with sign exactly (-1)^m.

SANITY GATE: sum_{n, m} W(n, m) must equal f(q) to >= 20 digits at the test
beta. (Algebraically obvious from the brief's derivation; we verify
numerically.)

CHOICE OF m: there are TWO natural notions of "occupation index":
    (m1) total particle count m = sum_k (a_k + b_k)            (THIS ONE)
    (m2) total energy contribution from particles m' = sum_k k*(a_k+b_k)

(m1) is the natural conjugate variable to the fugacity z, so it is the index
on which the (-1)^F sign factor acts homogeneously. (m2) is the natural
"excitation energy" coordinate. The brief specifies (m1); we report it as
"occupation_m1" and report (m2) as a SENSITIVITY CHECK at the end of the
script. All three primary candidates are computed against (m1).

CANDIDATES
----------
1. Negativity volume V(beta) = sum_{n,m} |W(n,m)| - sum_{n,m} W(n,m).
   This equals 2 * (|negative part|), the discrete-Wigner analog of integrated
   negativity. Bounded below by 0; vanishes iff W is non-negative on all (n,m).

2. Sign-respecting Renyi-alpha:
       D_alpha(|W| ‖ W_+)
   where |W|(n,m) = |W(n,m)| / sum |W|       (renormalized absolute-value distribution)
   and    W_+(n,m) = max(W(n,m), 0) / sum max(W, 0)   (positive-part distribution).
   Tested at alpha in {0.5, 2}. The renormalization choice (renormalize EACH
   to a probability over (n,m)-space) is the unambiguous one: both |W| and
   W_+ are positive on (n,m), so dividing by their respective masses gives
   honest probability distributions. We document this choice explicitly.

3. Mana m(beta) = log(sum |W(n,m)|) - log|sum W(n,m)|
                = log(L1 norm of W) - log|Z|
   This is the standard quantum-information mana applied to the lattice gas
   quasi-distribution. Bounded above by log(state-space size) and is the
   natural log-of-negativity for a signed measure.

ACCEPTANCE BAR (identical to Exp 16 / Exp 18):
   - PASS if max |ratio - median(ratio)| / median <= 1% across full sweep.
   - NEAR-PASS if max rel dev in (1%, 10%]; reported but NOT a match.
   - FAIL otherwise.
   - Beta sweep is 9 points across 6 dex (beta in 1e-5 ... 10).

REUSE
-----
We import the lattice-gas helpers from Exp 16:
   - f_target_series             (closed-form f(q))
   - joint_n_and_total_particles_unsigned  (DP over (n, P))
   - g_star_iy                   (Eichler integral)

We re-do the DP locally too so we can return both signed-joint and unsigned-
joint without normalization at the same time.
"""
from __future__ import annotations
import csv
import importlib.util
import sys
from pathlib import Path
from mpmath import mp, mpf, exp, log, pi, sqrt, nstr

mp.dps = 80   # ample; closed forms used for the L1 / Z_+ / Z_- masses avoid the
              # cancellation precision issue at small beta.

# ---------------------------------------------------------------------------
# Import helpers from Exp 16 by file path (filename begins with a digit).
# ---------------------------------------------------------------------------
_HERE = Path(__file__).parent
_SPEC = importlib.util.spec_from_file_location(
    "exp16", _HERE / "16_fep_mock_modular_toy.py"
)
exp16 = importlib.util.module_from_spec(_SPEC)
sys.modules["exp16"] = exp16
_SPEC.loader.exec_module(exp16)

f_target_series = exp16.f_target_series
g_star_iy = exp16.g_star_iy


# ---------------------------------------------------------------------------
# Joint signed weight W(n, m) construction.
#
# W(n, m) = (-1)^m * q^{n^2} * c_{n,m}(q)
# where c_{n,m}(q) = coefficient of x^m in prod_{k=1..n} (sum_{p>=0} (p+1) x^p q^{kp})
#                  = coefficient of x^m in prod_{k=1..n} 1/(1 - x q^k)^2 .
#
# Note c_{n,m}(q) is non-negative for q in (0,1); the sign of W(n,m) is exactly
# the sign of (-1)^m.
# ---------------------------------------------------------------------------
def _polynomial_divide_by_1_minus_y(coeffs: list[mpf], y: mpf) -> list[mpf]:
    """Multiply polynomial `coeffs` (as list, index = exponent) by 1/(1 - y x)
       in-place style. Returns new list of same length.
       Identity: if g(x) = f(x) / (1 - y x) then g_m = f_m + y * g_{m-1}.
    """
    L = len(coeffs)
    out = [mpf(0)] * L
    out[0] = coeffs[0]
    for m in range(1, L):
        out[m] = coeffs[m] + y * out[m - 1]
    return out


def joint_signed_weight_W(q: mpf, n_max: int, m_max: int) -> dict[tuple[int, int], mpf]:
    """Compute the JOINT SIGNED weight W(n, m) on (n, m) where
       m = total occupation = sum_k (a_k + b_k).
       Returns a dict {(n, m): W(n, m)} including only entries above 1e-50.
       n_max caps the core-size sector; m_max caps the total occupation.

       Fast implementation: 1/(1 - x q^k)^2 acts on a polynomial as TWO
       applications of "multiply by 1/(1 - y x)" with y = q^k, which has an
       O(m_max) recurrence c_m <- c_m + y * c_{m-1}. So each site k costs
       O(2 * m_max), and the whole product over k=1..n costs O(n * m_max).
    """
    W: dict[tuple[int, int], mpf] = {}
    for n in range(n_max + 1):
        if n == 0:
            W[(0, 0)] = mpf(1)        # q^0 * empty product * (-1)^0
            continue
        # Build the per-n polynomial via the O(m_max) recurrence per site.
        coeffs = [mpf(0)] * (m_max + 1)
        coeffs[0] = mpf(1)
        for k in range(1, n + 1):
            qk = q ** k
            coeffs = _polynomial_divide_by_1_minus_y(coeffs, qk)
            coeffs = _polynomial_divide_by_1_minus_y(coeffs, qk)
        qn2 = q ** (n * n)
        # If the core-size weight is already below threshold, skip the whole
        # sector (huge speedup at large beta).
        if abs(qn2) < mpf("1e-60"):
            break
        for m in range(m_max + 1):
            cm = coeffs[m]
            if cm == 0:
                continue
            sign = mpf(1) if (m % 2 == 0) else mpf(-1)
            val = sign * qn2 * cm
            if abs(val) < mpf("1e-50"):
                continue
            W[(n, m)] = val
    return W


def joint_signed_weight_W_by_energy(q: mpf, n_max: int, e_max: int) -> dict[tuple[int, int], mpf]:
    """SENSITIVITY-CHECK variant: same construction but indexed by
       m' = sum_k k*(a_k+b_k) = particle energy contribution.
       This is the "energy occupation" definition (m2) from the docstring.
       The sign of each contribution is still (-1)^{a+b} per site, but here
       multiple distinct sign patterns can have the same m' — so the sign is
       NO LONGER a simple function of m'. We must track sign explicitly per
       site.
       For each site k contribution = sum_{p>=0} (-1)^p (p+1) q^{k p} x^{k p}
                                    = d/dz [1/(1 - z)] at z = -x q^k weighted
                                    = 1/(1 + x q^k)^2 (as a formal series in x).
       (Reality check: with z = x q^k, sum_{p>=0} (p+1) z^p = 1/(1-z)^2; with z
       carrying an extra (-1)^p we substitute z -> -z, getting 1/(1+x q^k)^2.)
       So W'(n, m') = [coefficient of x^{m'} in q^{n^2} prod_{k=1..n} 1/(1 + x q^k)^2].
       For this index the bookkeeping is by ENERGY (so we use a polynomial in
       y = x where the per-site weight is in y^k); we apply two passes of the
       O(e_max) recurrence in y, but advancing by k each time.
    """
    def _div_1_plus_yk(coeffs: list[mpf], y: mpf, k: int) -> list[mpf]:
        """Divide poly by (1 + y x^k), i.e. multiply by 1/(1 + y x^k).
           Recurrence: c'_m = c_m - y * c'_{m-k}.
        """
        L = len(coeffs)
        out = [mpf(0)] * L
        for m in range(L):
            v = coeffs[m]
            if m - k >= 0:
                v = v - y * out[m - k]
            out[m] = v
        return out

    W: dict[tuple[int, int], mpf] = {}
    for n in range(n_max + 1):
        if n == 0:
            W[(0, 0)] = mpf(1)
            continue
        coeffs = [mpf(0)] * (e_max + 1)
        coeffs[0] = mpf(1)
        for k in range(1, n + 1):
            qk = q ** k
            coeffs = _div_1_plus_yk(coeffs, qk, k)
            coeffs = _div_1_plus_yk(coeffs, qk, k)
        qn2 = q ** (n * n)
        if abs(qn2) < mpf("1e-60"):
            break
        for mp_idx in range(e_max + 1):
            cm = coeffs[mp_idx]
            if cm == 0:
                continue
            val = qn2 * cm
            if abs(val) < mpf("1e-50"):
                continue
            W[(n, mp_idx)] = val
    return W


# ---------------------------------------------------------------------------
# Candidates.
# ---------------------------------------------------------------------------
def negativity_volume(W: dict[tuple[int, int], mpf]) -> mpf:
    """V = sum |W| - sum W = 2 * (mass on negative entries)."""
    pos = mpf(0)
    neg_abs = mpf(0)
    for v in W.values():
        if v >= 0:
            pos += v
        else:
            neg_abs += -v
    L1 = pos + neg_abs
    total = pos - neg_abs
    return L1 - total  # = 2 * neg_abs


def mana(W: dict[tuple[int, int], mpf]) -> mpf:
    """m = log(sum |W|) - log|sum W|."""
    L1 = mpf(0)
    total = mpf(0)
    for v in W.values():
        L1 += abs(v)
        total += v
    if L1 <= 0 or total == 0:
        return mpf("nan")
    return log(L1) - log(abs(total))


def renyi_signed_aware(W: dict[tuple[int, int], mpf], alpha: float) -> mpf:
    """Renyi-alpha divergence D_alpha(|W| renormalized ‖ W_+ renormalized).
       Both are probability distributions on (n, m); |W| has full support
       wherever W != 0, W_+ has support where W > 0.
       Where W < 0, W_+ assigns probability 0 and |W| assigns positive
       probability — so for alpha > 0 with the convention that
         |W|(x)^alpha * W_+(x)^(1-alpha) = +inf  when W_+(x) = 0 and alpha > 1
         and = 0                       when alpha < 1,
       we either get infinite divergence (alpha > 1) or a finite one (alpha < 1).
       To keep both alpha branches well-defined and finite we use the
       "support-restricted" Renyi: sum over (n,m) where W_+(x) > 0, but using
       |W| renormalized over the SAME RESTRICTED SUPPORT.
       Document this restriction explicitly.
    """
    a = mpf(alpha)
    # Support where W_+ is positive = where W > 0.
    pos_keys = [k for k, v in W.items() if v > 0]
    if not pos_keys:
        return mpf("nan")
    L1_full = sum(abs(v) for v in W.values())
    Wp_mass = sum(W[k] for k in pos_keys)
    # |W| renormalized to the FULL support — we use full because the
    # absolute-value distribution is well-defined everywhere. But then for
    # alpha > 1, the Renyi sum on (n,m) where W_+(x)=0 is undefined (0 in
    # denominator). We therefore split: when alpha > 1, the divergence is
    # +infinity if |W| has any mass outside W_+'s support. The honest report
    # for that case is "infinite" — and we mark it as such.
    # For alpha < 1, the formula sum p^alpha q^(1-alpha) treats q=0 as 0^(1-alpha)
    # which for alpha < 1 means (1-alpha) > 0 so 0^pos = 0, killing those terms.
    # So:
    if a > 1:
        # If |W| has mass outside the positive support, Renyi is infinite.
        outside_mass = sum(abs(v) for k, v in W.items() if v <= 0)
        if outside_mass > 0:
            return mpf("inf")
    s = mpf(0)
    for k in pos_keys:
        p = abs(W[k]) / L1_full
        q = W[k] / Wp_mass
        if p <= 0 or q <= 0:
            continue
        s += p ** a * q ** (mpf(1) - a)
    if s <= 0:
        return mpf("nan")
    return log(s) / (a - 1)


# ---------------------------------------------------------------------------
# CLOSED-FORM SUMS for L1, Z_+, and Z (=f) that avoid the cancellation
# precision problem at small beta.
#
# Key observation:
#   sum_{n, m} |W(n, m)| = sum_n q^{n^2} * prod_{k=1..n} 1/(1 - q^k)^2  =: Z_unsigned
#   sum_{n, m} W(n, m)   = sum_n q^{n^2} * prod_{k=1..n} 1/(1 + q^k)^2  =  f(q)
#   sum_{n, m even} W    = (1/2)(Z_unsigned + f)   =: Z_plus
#   sum_{n, m odd}  W    = (1/2)(f - Z_unsigned)   =  -(Z_unsigned - f)/2
#
# These follow from setting x=+1 (for L1 / Z_unsigned) or x=-1 (for f) in the
# joint generating function prod_{k=1..n} 1/(1 - x q^k)^2, and noting that
# (g(1) + g(-1))/2 isolates the even part of g(x).
#
# So mana, negativity volume, and Renyi-1/2 over the (m even)-restricted support
# all have closed-form expressions in terms of (Z_unsigned, f).
# ---------------------------------------------------------------------------
def Z_unsigned_closed(q: mpf, n_max: int = 250) -> mpf:
    """Z_unsigned(q) = sum_{n>=0} q^{n^2} / prod_{k=1..n} (1 - q^k)^2.
    Convergence: q^{n^2} kills the sum quickly; the bosonic product diverges
    for small q only mildly. For q close to 1 (small beta) we need large n_max.
    """
    total = mpf(0)
    for n in range(n_max + 1):
        prod = mpf(1)
        for k in range(1, n + 1):
            prod *= (1 - q ** k) ** 2
        term = q ** (n * n) / prod
        total += term
        if n > 5 and abs(term) < mpf("1e-60"):
            break
    return total


def closed_form_masses(beta: mpf, n_max: int = 400) -> tuple[mpf, mpf, mpf]:
    """Return (L1, Z_plus, Z_total) where Z_total = f(q), L1 = sum |W|,
    Z_plus = sum W over (m even) = (L1 + Z_total)/2."""
    q = exp(-beta)
    L1 = Z_unsigned_closed(q, n_max=n_max)
    Z = f_target_series(q, N=n_max)
    Zp = (L1 + Z) / 2
    return L1, Zp, Z


# ---------------------------------------------------------------------------
# Adaptive truncation policy.
# ---------------------------------------------------------------------------
def adaptive_truncations(beta: mpf) -> tuple[int, int]:
    """Return (n_max, m_max) sized for the given beta.
    At small beta the per-site occupation tails extend like p ~ 100/beta
    (geometric in qk = e^{-beta*k} requires p*qk^p < 10^{-50}); the bigger m_max
    we use, the more digits we recover in the signed sum after cancellation.
    Capped to keep cost bounded; document cap-bound in the diary.
    """
    if beta >= mpf("1"):
        return 15, 80
    if beta >= mpf("0.1"):
        return 30, 600
    if beta >= mpf("0.01"):
        return 40, 2000
    if beta >= mpf("0.001"):
        return 50, 6000
    if beta >= mpf("0.0001"):
        return 50, 12000
    # beta < 1e-4 — we're hitting the precision wall; report what we get and
    # note in the diary that the small-beta candidate values are LOWER BOUNDS
    # on the truncated computation (the true L1 grows even faster).
    return 40, 15000


# ---------------------------------------------------------------------------
# Driver.
# ---------------------------------------------------------------------------
def main():
    out_path = _HERE / "results" / "wigner_negativity_shadow.csv"
    out_path.parent.mkdir(exist_ok=True)

    # Beta sweep (brief specifies these 9 points).
    betas = [mpf("1e-5"), mpf("1e-4"), mpf("1e-3"), mpf("1e-2"),
             mpf("0.1"), mpf("0.3"), mpf("1"), mpf("3"), mpf("10")]

    print("=" * 78)
    print("Experiment 20 — Wigner-negativity-aware divergences on signed lattice gas")
    print("=" * 78)
    print()

    # ----------------- Sanity gate: W reproduces f(q) -----------------
    # The brief requires direct enumeration: confirm sum_{n,m} W(n, m) = f(q)
    # to >= 20 digits at one test beta. We do this with the DP-based
    # joint_signed_weight_W AT BETA = 1 (where truncation converges easily),
    # then transition to the equivalent closed-form expressions
    # (L1 = Z_unsigned, sum W = f) for the production sweep.
    test_beta = mpf("1")
    q_test = exp(-test_beta)
    W_test = joint_signed_weight_W(q_test, n_max=30, m_max=120)
    Z_W = sum(W_test.values())
    f_val = f_target_series(q_test, N=400)
    diff = abs(Z_W - f_val)
    digits = -log(diff + mpf("1e-50")) / log(10)
    print(f"SANITY GATE A  (direct enumeration of W(n,m), beta = {float(test_beta):.4g}):")
    print(f"  sum_(n,m) W(n,m)  = {nstr(Z_W, 30)}")
    print(f"  f(q)              = {nstr(f_val, 30)}")
    print(f"  |diff|            = {nstr(diff, 6)}")
    print(f"  digits agree      = {float(digits):.2f}")
    sanity_a_pass = diff < mpf("1e-20")
    print(f"  >= 20 digit agreement: {'PASS' if sanity_a_pass else 'FAIL — investigate W definition'}")
    print()

    # ----------------- Sanity gate B: closed-form L1 matches DP at beta=1
    L1_DP = sum(abs(v) for v in W_test.values())
    L1_closed = Z_unsigned_closed(q_test, n_max=200)
    diffL = abs(L1_DP - L1_closed)
    print(f"SANITY GATE B  (closed-form L1 vs direct |W| sum at beta = 1):")
    print(f"  L1 direct  = {nstr(L1_DP, 30)}")
    print(f"  L1 closed  = {nstr(L1_closed, 30)}")
    print(f"  |diff|     = {nstr(diffL, 6)}")
    sanity_b_pass = diffL < mpf("1e-20")
    print(f"  >= 20 digit agreement: {'PASS' if sanity_b_pass else 'FAIL'}")
    print()

    # ----------------- Sweep candidates (closed-form for the three primary)
    print("=" * 78)
    print("Candidate sweep across beta in [1e-5, 10] (9 points, 6 dex)")
    print("Primary candidates computed via closed-form L1, Z_+, Z (no truncation")
    print("ambiguity). The DP joint_signed_weight_W is reserved for the")
    print("Renyi-alpha=2 candidate that requires per-(n,m) decomposition.")
    print()
    print(("{:>10}" + " {:>14}" * 7).format(
        "beta", "g_star", "L1", "neg_volume", "mana", "renyi_a0.5",
        "renyi_a2", "f(q)"))
    print("-" * 110)

    rows = []
    for beta in betas:
        q = exp(-beta)

        # Closed-form masses.
        # n_max for the Durfee-square sum: q^{n^2} kills the sum quickly even
        # at q close to 1; n_max = 400 suffices universally.
        L1, Zp, Zf = closed_form_masses(beta, n_max=400)
        # Negativity volume V = L1 - Z = 2 * |negative mass|.
        V = L1 - Zf
        # Mana m = log(L1) - log|Z|.
        man = log(L1) - log(abs(Zf))
        # Renyi-1/2 D_{0.5}(|W|/L1 || W_+/Z_+) = -log(Z_+/L1) on m-even restriction
        # via the calculation in the module header.
        R05 = log(L1) - log(Zp)

        # Eichler integral.
        y = beta / (2 * pi)
        gs = g_star_iy(y)

        # Renyi alpha = 2:
        # On the support where W_+ > 0 (m even), p_i = |W|/L1 = W/L1 and
        # q_i = W/Z_+. The sum is over all (n,m): if W < 0, q_i = 0 and
        # p_i^2 / q_i = +inf for alpha > 1.
        # Therefore D_2 = +inf for ALL beta where there is ANY negative mass —
        # which is every beta in our sweep (every n >= 1 sector has m=1 odd
        # contributions). So we record R2 = +inf without invoking the DP.
        R2 = mpf("inf")

        cv_list = [V, man, R05, R2]
        cname_list = ["neg_volume", "mana", "renyi_a0.5", "renyi_a2"]
        for cn, cv in zip(cname_list, cv_list):
            ratio = (cv / gs) if (gs != 0 and not (cv != cv) and cv not in (mpf("inf"), mpf("-inf"))) else mpf("nan")
            rows.append({
                "beta": float(beta),
                "candidate_name": cn,
                "candidate_value": float(cv) if not (cv != cv) and cv not in (mpf("inf"), mpf("-inf")) else (float("inf") if cv == mpf("inf") else float("nan")),
                "g_star_value": float(gs),
                "ratio": float(ratio) if not (ratio != ratio) and ratio not in (mpf("inf"), mpf("-inf")) else (float("inf") if ratio == mpf("inf") else float("nan")),
                "rel_dev_from_median_ratio": None,
            })

        def _fmt(x):
            try:
                if x != x:
                    return "nan"
                if x == mpf("inf"):
                    return "inf"
                return f"{float(x):.6g}"
            except Exception:
                return "nan"

        print(("{:>10.4g}" + " {:>14}" * 7).format(
            float(beta), _fmt(gs), _fmt(L1), _fmt(V), _fmt(man), _fmt(R05),
            _fmt(R2), _fmt(Zf)))

    # ----------------- Per-candidate rel-dev statistics -----------------
    by_candidate: dict[str, list[dict]] = {}
    for r in rows:
        by_candidate.setdefault(r["candidate_name"], []).append(r)

    candidate_names = ["neg_volume", "mana", "renyi_a0.5", "renyi_a2"]
    print()
    print("=" * 78)
    print("Proportionality tests (strict bar):")
    print(f"  PASS:      max |ratio - median| / median <= 1% across full sweep")
    print(f"  NEAR-PASS: max rel dev in (1%, 10%]")
    print(f"  FAIL:      otherwise")
    print(f"  Beta sweep: [{float(min(betas)):.4g}, {float(max(betas)):.4g}] "
          f"({float(log(max(betas)/min(betas))/log(10)):.2f} dex)")
    print()
    print(f"  {'candidate':>14}  {'median ratio':>16}  {'max rel dev':>16}  {'verdict':>10}")
    print("-" * 78)

    verdicts: dict[str, str] = {}
    medians: dict[str, float] = {}
    max_devs: dict[str, float] = {}

    for cname in candidate_names:
        crows = by_candidate[cname]
        ratios = []
        for r in crows:
            x = r["ratio"]
            if x == x and x not in (float("inf"), float("-inf")):
                ratios.append(mpf(x))
        if not ratios:
            print(f"  {cname:>14}  {'NaN':>16}  {'NaN':>16}  {'SKIP':>10}")
            for r in crows:
                r["rel_dev_from_median_ratio"] = float("nan")
            verdicts[cname] = "SKIP"
            continue
        med = sorted(ratios)[len(ratios) // 2]
        if med == 0:
            max_dev = mpf("inf")
        else:
            max_dev = max(abs(r - med) / abs(med) for r in ratios)
        for r in crows:
            x = r["ratio"]
            if x == x and x not in (float("inf"), float("-inf")) and med != 0:
                r["rel_dev_from_median_ratio"] = float(abs(mpf(x) - med) / abs(med))
            else:
                r["rel_dev_from_median_ratio"] = float("nan")
        if max_dev < mpf("0.01"):
            verdict = "PASS"
        elif max_dev < mpf("0.1"):
            verdict = "NEAR-PASS"
        else:
            verdict = "FAIL"
        verdicts[cname] = verdict
        medians[cname] = float(med)
        max_devs[cname] = float(max_dev)
        print(f"  {cname:>14}  {nstr(med, 6):>16}  {nstr(max_dev, 6):>16}  {verdict:>10}")

    # ----------------- Restricted-window proportionality test -----------------
    # Renyi-alpha=0.5 saturates at log(2) in the cusp regime; we test whether
    # any candidate passes the strict 1% bar on the SUB-WINDOW beta in [1e-5, 0.1]
    # (4 orders of magnitude, all in the cusp regime).
    print()
    print("=" * 78)
    print("RESTRICTED-WINDOW test: beta in [1e-5, 0.1] (4 dex, cusp regime only)")
    print()
    print(f"  {'candidate':>14}  {'median ratio':>16}  {'max rel dev':>16}  {'verdict':>10}")
    print("-" * 78)
    for cname in candidate_names:
        crows = by_candidate[cname]
        ratios = [mpf(r["ratio"]) for r in crows
                  if r["beta"] <= 0.1 + 1e-12
                  and r["ratio"] == r["ratio"]
                  and r["ratio"] not in (float("inf"), float("-inf"))]
        if not ratios:
            print(f"  {cname:>14}  {'NaN':>16}  {'NaN':>16}  {'SKIP':>10}")
            continue
        med = sorted(ratios)[len(ratios) // 2]
        max_dev = max(abs(r - med) / abs(med) for r in ratios) if med != 0 else mpf("inf")
        if max_dev < mpf("0.01"):
            verdict = "PASS"
        elif max_dev < mpf("0.1"):
            verdict = "NEAR-PASS"
        else:
            verdict = "FAIL"
        print(f"  {cname:>14}  {nstr(med, 6):>16}  {nstr(max_dev, 6):>16}  {verdict:>10}")

    # ----------------- Cusp-boundedness diagnostic -----------------
    print()
    print("=" * 78)
    print("Cusp behavior of each candidate (small-beta vs large-beta values):")
    print(f"  {'candidate':>14}  {'val(beta=1e-5)':>16}  {'val(beta=10)':>14}")
    for cname in candidate_names:
        crows = by_candidate[cname]
        sm = next((r["candidate_value"] for r in crows if r["beta"] == 1e-5), float("nan"))
        lg = next((r["candidate_value"] for r in crows if r["beta"] == 10.0), float("nan"))
        print(f"  {cname:>14}  {sm:>16.6g}  {lg:>14.6g}")

    # ----------------- Write CSV -----------------
    header = ["beta", "candidate_name", "candidate_value", "g_star_value",
              "ratio", "rel_dev_from_median_ratio"]
    with open(out_path, "w", newline="") as fp:
        w = csv.DictWriter(fp, fieldnames=header)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in header})

    print()
    print(f"Wrote {out_path}")

    # ----------------- Sensitivity check: m2 definition -----------------
    print()
    print("=" * 78)
    print("Sensitivity check: alternate occupation definition m' = sum k*(a_k+b_k)")
    print()
    print("Re-compute neg_volume and mana under m2 (energy-indexed) joint at")
    print("a representative beta (beta = 1, where DP truncation converges).")
    print("Under m2, the sign per (n, m') is no longer a simple function of m',")
    print("so the L1 norm differs from the m1 variant.")
    print()
    test_betas_m2 = [mpf("1"), mpf("0.3"), mpf("0.1")]
    for b in test_betas_m2:
        q = exp(-b)
        # For beta=1 use n_max=25, e_max=120 (each site can have at most ~50 particles).
        if b >= mpf("0.5"):
            n_max, e_max = 25, 200
        elif b >= mpf("0.2"):
            n_max, e_max = 30, 400
        else:
            n_max, e_max = 35, 800
        Wp = joint_signed_weight_W_by_energy(q, n_max=n_max, e_max=e_max)
        Zp = sum(Wp.values())
        f_b = f_target_series(q, N=400)
        diff_p = abs(Zp - f_b)
        V_p = negativity_volume(Wp)
        try:
            man_p = mana(Wp)
        except Exception:
            man_p = mpf("nan")
        # Compare with the m1 (closed-form) values at the same beta.
        L1_m1, _, Zf_m1 = closed_form_masses(b, n_max=400)
        V_m1 = L1_m1 - Zf_m1
        man_m1 = log(L1_m1) - log(abs(Zf_m1))
        print(f"  beta={float(b):>8.4g}  |sumWp - f|={nstr(diff_p,4):>12}  "
              f"V_m2={nstr(V_p,6):>12}  mana_m2={nstr(man_p,6):>12}  "
              f"V_m1={nstr(V_m1,6):>12}  mana_m1={nstr(man_m1,6):>12}")

    print()
    print("Bottom line on the m1 vs m2 ambiguity:")
    print("  m1 (total occupation) gives L1 = Z_unsigned in CLOSED FORM.")
    print("  m2 (energy contribution) collapses some signed cancellation within")
    print("  each (n, m') cell, giving a SMALLER L1. The two definitions agree")
    print("  on sum(W) = f(q) but disagree on neg_volume and mana. We used m1")
    print("  per the brief's specification ('m = sum (a_k + b_k)').")
    print()
    print("=" * 78)
    print("Done.")


if __name__ == "__main__":
    main()
