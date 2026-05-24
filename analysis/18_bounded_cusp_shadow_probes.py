"""
Experiment 18 — bounded-at-cusp shadow probes for Ramanujan's third-order
mock theta f(q).

CONTEXT (see diary 13 / Exp 16 for the falsification this builds on):

Exp 16 falsified all four standard info-theoretic candidates (MI, KL,
Surprise, Fisher) as proxies for the Eichler integral g*(tau) of f's
shadow. The structural reason: g*(i*beta/(2*pi)) -> finite limit ~ 3.46
as beta -> 0, while KL/Surprise diverge there and MI/Fisher vanish.

Diary 13 explicitly recommends the next test class:
    "bounded-at-cusp candidates (Renyi-alpha, Bhattacharyya, entropic uncertainty)".

This script implements those three families and applies the SAME strict
acceptance bar as Exp 16:  |candidate/g* - median|/median <= 1% across
>= 2 dex of beta.

CONVENTION FOR THE SIGNED-WEIGHT SUBTLETY
-----------------------------------------
The "signed" weights w_signed(n) = q^(n^2) / prod_{k=1..n} (1+q^k)^2
arising from the (-1)^F insertion are ALL POSITIVE on the marginal in
the variable n (the sign cancellations happened in the SUMS over a_k,b_k
within each n-sector). So p_signed(n) is in fact a bona-fide probability
distribution on n; only the joint p(n, a_k, b_k) is signed.

We therefore adopt convention (a) from the brief: operate on the n-marginal
probability distributions p_signed(n) and p_unsigned(n) (both positive),
and compare candidates against g*(i*beta/(2*pi)). We do NOT extend into
Wigner-style quasi-probability for the three primary candidates, since the
n-marginals are honest probabilities and divergences between honest
probabilities are well-defined.

This is the same convention Exp 16 used implicitly. We document it
explicitly here.

CANDIDATES PROBED
-----------------
1. Renyi-alpha divergence D_alpha(P_unsigned || P_signed), alpha in
   {0.5, 1.5, 2, 5, "inf"}. Bounded for alpha < 1 in regimes where KL
   blows up; D_1 recovers KL. We also probe alpha = 1.5, 2, 5, inf to
   span the >=1 regime even though they may diverge at the cusp like KL.

2. Bhattacharyya coefficient and distance:
       BC(P,Q)  = sum_i sqrt(p_i q_i)    in [0, 1]
       d_B(P,Q) = -log BC                in [0, inf)
   d_B is bounded above by (1/2) * D_KL for any pair, and unlike KL it
   stays finite even when KL diverges, because sqrt(p*q) is integrable
   where p*log(p/q) is not. Quintessential bounded-at-cusp candidate.

3. Entropic-uncertainty form. Given the signed n-marginal p_signed(n)
   and the joint p(n, P) over (n, total_particles) in the unsigned
   measure (which we already computed in Exp 16), define
       U(beta) = H(n | P) - H(n)   in the unsigned measure
              = -[ I(n; P) ]
   That is, U(beta) is the NEGATIVE mutual information. We use this
   particular operational form because:
     - it is bounded in [-log(state_space_size), 0],
     - it is naturally "entropic uncertainty"-flavored (the conditional
       entropy minus marginal entropy),
     - we already have the joint from Exp 16 so the implementation is
       cheap.
   The cusp value of U is U(0) = -MI(0) = 0 (from Exp 16's MI ~ 0 at
   small beta). So this candidate VANISHES at the cusp — which means
   it shares the failure mode of MI. We probe it anyway, for honesty
   about the family, and so that if it FAILS we can state "the entire
   entropic-uncertainty-of-marginals family fails for the same
   structural reason MI does".

Additionally we probe a fourth candidate (variant of Bhattacharyya):

4. Hellinger distance squared
       H^2(P,Q) = 1 - BC(P,Q)        in [0, 1]
   Bounded by construction; this is the proper metric-style cousin of
   Bhattacharyya distance, often easier to read intuition off.

ACCEPTANCE BAR (identical to Exp 16):
   The candidate PASSES if max_{beta} |c/g* - median(c/g*)| / median <= 1%
   across the full beta sweep (>= 2 dex). Anything else FAILS.

   A NEAR-PASS is recorded when the max-rel-dev is below 20% but above 1%;
   we report the dispersion pattern (factor and beta regime) but do NOT
   call this a match.
"""
from __future__ import annotations
import csv
import importlib.util
import sys
from pathlib import Path
from mpmath import mp, mpf, exp, log, sqrt, pi, nstr

mp.dps = 50

# ---------------------------------------------------------------------------
# Import helpers from Exp 16 by file path (the filename starts with a digit
# so a regular `import` statement won't work).
# ---------------------------------------------------------------------------
_HERE = Path(__file__).parent
_SPEC = importlib.util.spec_from_file_location(
    "exp16", _HERE / "16_fep_mock_modular_toy.py"
)
exp16 = importlib.util.module_from_spec(_SPEC)
sys.modules["exp16"] = exp16
_SPEC.loader.exec_module(exp16)

# Bring the relevant helpers into local scope.
f_target_series = exp16.f_target_series
signed_marginal_n = exp16.signed_marginal_n
unsigned_marginal_n = exp16.unsigned_marginal_n
joint_n_and_total_particles_unsigned = exp16.joint_n_and_total_particles_unsigned
g_star_iy = exp16.g_star_iy


# ---------------------------------------------------------------------------
# New candidates.
# ---------------------------------------------------------------------------
def _aligned_marginals(beta: mpf, n_max: int) -> tuple[list[mpf], list[mpf]]:
    """Return (p_signed, p_unsigned) on the SAME truncated support, each
    renormalized over that support, so divergences are comparable. We use
    the same adaptive n_max policy as Exp 16 (capped at 800)."""
    q = exp(-beta)
    ps, _ = signed_marginal_n(q, n_max=n_max)
    pu, _ = unsigned_marginal_n(q, n_max=n_max)
    # Both are already normalized over [0, n_max]; the residual mass missing
    # for the unsigned distribution at small beta is the same truncation we
    # acknowledge in Exp 16.
    return ps, pu


def renyi_divergence(beta: mpf, alpha: float | str, n_max: int) -> mpf:
    """D_alpha(P_unsigned || P_signed) with the standard convention
        D_alpha(P||Q) = 1/(alpha-1) log sum_i p_i^alpha q_i^(1-alpha)    (alpha != 1)
        D_inf(P||Q)  = log max_i p_i/q_i
        D_1(P||Q)    = KL(P||Q)  [recovered as alpha -> 1; not probed here]
    """
    ps, pu = _aligned_marginals(beta, n_max)
    if alpha == "inf" or alpha == float("inf"):
        m = mpf(0)
        for pi_u, pi_s in zip(pu, ps):
            if pi_u <= 0 or pi_s <= 0:
                continue
            r = pi_u / pi_s
            if r > m:
                m = r
        return log(m) if m > 0 else mpf("nan")
    a = mpf(alpha)
    if a == 1:
        # Not implemented here; would be KL.
        return mpf("nan")
    s = mpf(0)
    for pi_u, pi_s in zip(pu, ps):
        if pi_u <= 0 or pi_s <= 0:
            continue
        s += pi_u ** a * pi_s ** (1 - a)
    if s <= 0:
        return mpf("nan")
    return log(s) / (a - 1)


def bhattacharyya_coefficient(beta: mpf, n_max: int) -> mpf:
    """BC(P_unsigned, P_signed) = sum_i sqrt(p_i q_i) in [0, 1]."""
    ps, pu = _aligned_marginals(beta, n_max)
    s = mpf(0)
    for pi_u, pi_s in zip(pu, ps):
        if pi_u <= 0 or pi_s <= 0:
            continue
        s += sqrt(pi_u * pi_s)
    return s


def bhattacharyya_distance(beta: mpf, n_max: int) -> mpf:
    """d_B = -log BC; in [0, inf), bounded for any well-defined pair."""
    bc = bhattacharyya_coefficient(beta, n_max)
    if bc <= 0:
        return mpf("inf")
    return -log(bc)


def hellinger_sq(beta: mpf, n_max: int) -> mpf:
    """H^2 = 1 - BC; in [0, 1]."""
    return 1 - bhattacharyya_coefficient(beta, n_max)


def entropic_uncertainty_neg_mi(beta: mpf, n_max: int = 18, P_max: int = 80) -> mpf:
    """U(beta) = H(n|P) - H(n) = -I(n; P) in the unsigned measure.
    Bounded in [-log(state_space), 0].
    Implementation: reuse Exp 16's joint computation, then form MI and negate.
    """
    q = exp(-beta)
    joint, _ = joint_n_and_total_particles_unsigned(q, n_max=n_max, P_max=P_max)
    p_n = {}
    p_P = {}
    for (n, P), pr in joint.items():
        p_n[n] = p_n.get(n, mpf(0)) + pr
        p_P[P] = p_P.get(P, mpf(0)) + pr
    mi = mpf(0)
    for (n, P), pr in joint.items():
        if pr <= 0:
            continue
        denom = p_n[n] * p_P[P]
        if denom <= 0:
            continue
        mi += pr * log(pr / denom)
    return -mi


# ---------------------------------------------------------------------------
# Adaptive n_max (matches Exp 16 policy).
# ---------------------------------------------------------------------------
def adaptive_nmax(beta: mpf) -> int:
    nm = max(50, int(20 / float(beta)) if beta > mpf("0.01") else 800)
    return min(nm, 800)


# ---------------------------------------------------------------------------
# Driver.
# ---------------------------------------------------------------------------
def main():
    out_path = _HERE / "results" / "bounded_cusp_shadow_probes.csv"
    out_path.parent.mkdir(exist_ok=True)

    # Beta grid: replicate Exp 16's grid; add 3 cusp-adjacent points.
    base_betas = [mpf("0.001"), mpf("0.003"), mpf("0.01"), mpf("0.03"),
                  mpf("0.05"), mpf("0.1"), mpf("0.2"), mpf("0.3"),
                  mpf("0.5"), mpf("1"), mpf("2"), mpf("3"), mpf("10")]
    cusp_extra = [mpf("0.00001"), mpf("0.0001"), mpf("0.0003")]
    betas = sorted(set(base_betas + cusp_extra))

    print("=" * 78)
    print("Experiment 18 — bounded-at-cusp shadow probes.")
    print("Convention: signed and unsigned n-marginals are positive distributions;")
    print("divergences/ratios computed between them. See module docstring.")
    print("=" * 78)
    print()

    # Candidate definitions.
    renyi_alphas = [0.5, 1.5, 2.0, 5.0, "inf"]
    candidate_names = (
        [f"renyi_a{a}" for a in renyi_alphas]
        + ["bhattacharyya_dist", "hellinger_sq", "entropic_uncertainty"]
    )

    # Header for the CSV.
    rows = []
    # Pretty table header for stdout.
    print(("{:>10}" + " {:>14}" * (1 + len(candidate_names))).format(
        "beta", "g_star", *candidate_names))
    print("-" * (10 + 15 * (1 + len(candidate_names))))

    for beta in betas:
        nm = adaptive_nmax(beta)
        y = beta / (2 * pi)
        gs = g_star_iy(y)

        # Compute every candidate.
        cvals = {}
        for a in renyi_alphas:
            try:
                cvals[f"renyi_a{a}"] = renyi_divergence(beta, a, nm)
            except Exception as e:  # noqa: BLE001
                cvals[f"renyi_a{a}"] = mpf("nan")
        try:
            cvals["bhattacharyya_dist"] = bhattacharyya_distance(beta, nm)
        except Exception:
            cvals["bhattacharyya_dist"] = mpf("nan")
        try:
            cvals["hellinger_sq"] = hellinger_sq(beta, nm)
        except Exception:
            cvals["hellinger_sq"] = mpf("nan")
        # Entropic uncertainty uses the much-more-expensive joint computation.
        # Cap parameters to keep runtime bounded.
        try:
            cvals["entropic_uncertainty"] = entropic_uncertainty_neg_mi(
                beta, n_max=18, P_max=80
            )
        except Exception:
            cvals["entropic_uncertainty"] = mpf("nan")

        # Per-candidate row in the long format.
        for cname in candidate_names:
            cv = cvals[cname]
            ratio = (cv / gs) if (gs != 0 and not (cv != cv)) else mpf("nan")
            rows.append({
                "beta": float(beta),
                "candidate_name": cname,
                "candidate_value": float(cv) if not (cv != cv) else float("nan"),
                "g_star_value": float(gs),
                "ratio": float(ratio) if not (ratio != ratio) else float("nan"),
                # rel_dev_from_median_ratio: filled in after the full sweep.
                "rel_dev_from_median_ratio": None,
            })

        print(("{:>10.4g}" + " {:>14.6g}" * (1 + len(candidate_names))).format(
            float(beta), float(gs),
            *(float(cvals[cn]) for cn in candidate_names)))

    # Compute rel_dev_from_median_ratio for each candidate.
    by_candidate: dict[str, list[dict]] = {}
    for r in rows:
        by_candidate.setdefault(r["candidate_name"], []).append(r)

    print()
    print("=" * 78)
    print("Proportionality tests (strict bar: max |ratio - median|/median <= 1%).")
    print(f"Beta sweep: [{float(min(betas)):.4g}, {float(max(betas)):.4g}] "
          f"({float(log(max(betas)/min(betas))/log(10)):.2f} dex)")
    print()
    print(f"  {'candidate':>22}  {'median ratio':>14}  {'max rel dev':>14}  "
          f"{'verdict':>10}")
    print("-" * 78)

    verdicts: dict[str, str] = {}
    medians: dict[str, float] = {}
    max_devs: dict[str, float] = {}

    for cname, crows in by_candidate.items():
        ratios = [mpf(r["ratio"]) for r in crows
                  if r["ratio"] == r["ratio"] and r["ratio"] not in (float("inf"), float("-inf"))]
        if not ratios:
            print(f"  {cname:>22}  {'NaN':>14}  {'NaN':>14}  {'SKIP':>10}")
            verdicts[cname] = "SKIP"
            for r in crows:
                r["rel_dev_from_median_ratio"] = float("nan")
            continue
        med = sorted(ratios)[len(ratios) // 2]
        if med == 0:
            max_dev = mpf("inf")
        else:
            max_dev = max(abs(r - med) / abs(med) for r in ratios)
        for r in crows:
            if r["ratio"] == r["ratio"]:
                r["rel_dev_from_median_ratio"] = float(
                    abs(mpf(r["ratio"]) - med) / abs(med) if med != 0 else mpf("inf")
                )
            else:
                r["rel_dev_from_median_ratio"] = float("nan")
        if max_dev < mpf("0.01"):
            verdict = "PASS"
        elif max_dev < mpf("0.2"):
            verdict = "NEAR-PASS"
        else:
            verdict = "FAIL"
        verdicts[cname] = verdict
        medians[cname] = float(med)
        max_devs[cname] = float(max_dev)
        print(f"  {cname:>22}  {nstr(med, 6):>14}  {nstr(max_dev, 6):>14}  "
              f"{verdict:>10}")

    # Cusp-bounded check.
    print()
    print("Cusp-boundedness of each candidate (small-beta behavior):")
    print(f"  {'candidate':>22}  {'val(beta=1e-5)':>16}  {'val(beta=10)':>14}")
    for cname, crows in by_candidate.items():
        sm = next((r["candidate_value"] for r in crows if r["beta"] == 1e-5), float("nan"))
        lg = next((r["candidate_value"] for r in crows if r["beta"] == 10.0), float("nan"))
        print(f"  {cname:>22}  {sm:>16.6g}  {lg:>14.6g}")

    # Write CSV.
    header = ["beta", "candidate_name", "candidate_value", "g_star_value",
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
    print("Summary verdict table (also written to diary 15):")
    for cname in candidate_names:
        v = verdicts.get(cname, "SKIP")
        med = medians.get(cname, float("nan"))
        md = max_devs.get(cname, float("nan"))
        print(f"  {cname:>22}: median ratio = {med:.4g}, max rel dev = "
              f"{md:.4g}    [{v}]")
    print()
    print("FALSIFICATION CRITERIA (each candidate, identical to Exp 16):")
    print("  - PASS if max |candidate/g* - median| / median <= 1% across full sweep.")
    print("  - NEAR-PASS if max rel dev in (1%, 20%]; reported but not a match.")
    print("  - FAIL otherwise.")


if __name__ == "__main__":
    main()
