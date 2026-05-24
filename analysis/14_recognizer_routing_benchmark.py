"""
Experiment 14 — Routing benchmark for the v1 recognizer.

A battery of >= 50 synthetic test energies, organized in four cohorts:

  - canonical   : one per registered kernel + a few "should-return-none" cases
  - perturbed   : kernel x rational coefficient / sign-flipped / shifted in q
  - composed    : sum or product of two canonical kernels
  - adversarial : kernels that LOOK like one family but aren't (q^(n^2+n) is
                  shifted-theta — must NOT match gaussian; Gauss sum with
                  q ≡ 2 (mod 4) must trigger DEGENERATE)

For each case we record:
  case_id, cohort, true_family, predicted_family, route,
  degenerate_flag, correct

then dump the per-case log to
  ramanujan/analysis/results/recognizer_routing_benchmark.csv

and print a precision/recall table grouped by `true_family`.

A note on `true_family` semantics:
  - For canonical and perturbed cases, `true_family` is the kernel that
    SHOULD be matched (or "none" for explicit non-matches).
  - For composed cases, `true_family` is a sorted-tuple-string of the
    underlying components (e.g. "gaussian_quadratic+lambert_divisor"). The
    recognizer is expected to peel one of them at top level; we mark
    `correct=True` if the predicted kernel is one of the components.
  - For adversarial cases, `true_family` is "none" when the case should
    NOT match anything (or, for the Gauss-sum silent-zero case, "gauss_sum"
    with degenerate_flag True).
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from collections import defaultdict, Counter
from importlib import import_module
import sympy as sp
from mpmath import mpf

sys.path.insert(0, str(Path(__file__).parent))
v1 = import_module("13_recognizer_v1")
best_match = v1.best_match
recognize = v1.recognize
Route = v1.Route


def best_match_composite(expr, n_sym, tol=mpf("1e-12")):
    """Composite wrapper: if `expr` is a Sum or Product, walk its terms/factors
    and return the FIRST best-match from any sub-piece (registry-priority order).
    Falls back to direct best_match on the atomic case.
    """
    direct = best_match(expr, n_sym, tol)
    if direct is not None:
        return direct, "atomic"
    # try decomposition
    if expr.func == sp.Add:
        for term in expr.args:
            bm = best_match(term, n_sym, tol)
            if bm is not None:
                return bm, "sum_component"
    if expr.func == sp.Mul:
        for factor in expr.args:
            bm = best_match(factor, n_sym, tol)
            if bm is not None:
                return bm, "product_component"
    return None, None

OUT_CSV = Path(__file__).parent / "results" / "recognizer_routing_benchmark.csv"
OUT_CSV.parent.mkdir(exist_ok=True)

n = sp.symbols("n", integer=True, nonnegative=True)
k = sp.symbols("k", integer=True, nonnegative=True)
chi = sp.Function("chi")
s_sym = sp.symbols("s")


# ---------- helpers for building test cases ----------

def gauss_summand(beta):
    """exp(-beta n^2)"""
    return sp.exp(-beta * n ** 2)


def gauss_qform(q):
    """q^(n^2)"""
    return q ** (n ** 2)


def bose_summand(beta):
    return 1 / (1 - sp.exp(-beta * n))


def lambert_summand(q):
    return q ** n / (1 - q ** n)


def mock_f3_summand(q):
    return q ** (n ** 2) / sp.Product((1 + q ** k) ** 2, (k, 1, n))


def mock_f5_summand(q):
    return q ** (n ** 2) / sp.Product(1 + q ** k, (k, 1, n))


def mock_f7_summand(q):
    return q ** (n ** 2) / sp.Product(1 + q ** k, (k, 1, 2 * n + 1))


def partial_theta_summand(q):
    return (-1) ** n * q ** (n * (n + 1) / 2)


def q_poch_infty(a, q):
    return sp.Product(1 - a * q ** k, (k, 0, sp.oo))


def eisenstein_summand(q, weight=4):
    return sp.divisor_sigma(n, weight - 1) * q ** n


def dirichlet_summand(s):
    return chi(n) * n ** (-s)


def gauss_sum_summand(p, q_int):
    return sp.exp(2 * sp.pi * sp.I * p * n ** 2 / q_int)


# ---------- the test battery ----------

CASES = []

def add(cohort, true_family, expr, expect_degenerate=False, comment="", accept_families=None):
    """For composed cases, `accept_families` may be a list of kernel names any
    of which counts as a correct prediction (composite-decomposition is
    component-order-dependent so we don't want to over-specify)."""
    CASES.append({
        "case_id": len(CASES),
        "cohort": cohort,
        "true_family": true_family,
        "expr": expr,
        "expect_degenerate": expect_degenerate,
        "comment": comment,
        "accept_families": accept_families or [true_family],
    })


# --- canonical (12 cases, one per family + 2 should-return-none) ---
q_sym = sp.symbols("q", positive=True)
a_sym = sp.symbols("a", positive=True)

add("canonical", "gaussian_quadratic", gauss_summand(sp.Rational(1, 10)),
    comment="theta_3 at beta=0.1")
add("canonical", "gaussian_quadratic", gauss_qform(sp.Rational(1, 2)),
    comment="q^(n^2) form, q=1/2")
add("canonical", "bose_einstein_geometric", bose_summand(sp.Rational(1, 20)),
    comment="Bose at beta=0.05")
add("canonical", "lambert_divisor", lambert_summand(sp.Rational(99, 100)),
    comment="Lambert q=0.99")
add("canonical", "mock_theta_f3", mock_f3_summand(q_sym),
    comment="symbolic q; ensures near-cusp completion flag")
add("canonical", "mock_theta_f5", mock_f5_summand(q_sym))
add("canonical", "mock_theta_f7", mock_f7_summand(q_sym))
add("canonical", "partial_theta", partial_theta_summand(q_sym))
add("canonical", "q_pochhammer_infty", q_poch_infty(a_sym, q_sym),
    comment="(a;q)_inf with symbolic a, q")
add("canonical", "eisenstein_E2k", eisenstein_summand(q_sym, weight=4),
    comment="E_4 summand")
add("canonical", "dirichlet_L", dirichlet_summand(s_sym),
    comment="L(s, chi) summand at symbolic s")
add("canonical", "gauss_sum", gauss_sum_summand(1, 3),
    comment="Gauss sum p=1 q=3 (odd, non-degenerate)")
# unknown / none cases
add("canonical", "none", sp.sin(sp.Rational(1, 10) * n),
    comment="sin(n) — not in any registered family")
add("canonical", "none", sp.cos(n) + 1,
    comment="cos(n) + 1 — also not registered")

# --- perturbed (20 cases) ---
# Multiplied by rational coefficient
add("perturbed", "gaussian_quadratic", 3 * gauss_summand(sp.Rational(1, 5)),
    comment="3 * gaussian — coefficient prefix should not match (we expect MISS)")
# (we expect this to MISS — the recognizer matchers are strict and don't
# strip outer scalar coefficients. This is a documented honest limitation
# that the benchmark surfaces; we'd add a scalar-stripping wrapper in v2.)
add("perturbed", "gaussian_quadratic", gauss_summand(sp.Rational(1, 5)),
    comment="bare gaussian, no perturbation (control)")
add("perturbed", "gaussian_quadratic", gauss_summand(sp.Rational(7, 13)),
    comment="rational beta=7/13")
add("perturbed", "gaussian_quadratic", gauss_summand(sp.Rational(100, 1)),
    comment="beta=100, deep in direct regime")
add("perturbed", "gaussian_quadratic", gauss_summand(sp.Rational(1, 10000)),
    comment="beta=1e-4, deep in dual regime")
# shifted q (different bases)
add("perturbed", "lambert_divisor", lambert_summand(sp.Rational(1, 3)),
    comment="Lambert at q=1/3 (small q, fast direct)")
add("perturbed", "lambert_divisor", lambert_summand(sp.Rational(999, 1000)),
    comment="Lambert at q very close to 1 (dual region)")
# sign-flipped partial theta
add("perturbed", "partial_theta", partial_theta_summand(sp.Rational(1, 4)),
    comment="alternating partial theta q=1/4")
add("perturbed", "partial_theta", q_sym ** (n * (n + 1) / 2),
    comment="non-alternating partial theta (no (-1)^n factor)")
# Bose at varying betas
add("perturbed", "bose_einstein_geometric", bose_summand(sp.Rational(1, 100)),
    comment="Bose at beta=0.01 (dual region)")
add("perturbed", "bose_einstein_geometric", bose_summand(sp.Rational(5, 1)),
    comment="Bose at beta=5 (direct region)")
# mock theta with concrete q
add("perturbed", "mock_theta_f3", mock_f3_summand(sp.Rational(1, 3)),
    comment="mock f3 at q=1/3")
add("perturbed", "mock_theta_f5", mock_f5_summand(sp.Rational(1, 4)))
add("perturbed", "mock_theta_f7", mock_f7_summand(sp.Rational(1, 5)))
# q-Pochhammer parameter sweeps
add("perturbed", "q_pochhammer_infty", q_poch_infty(sp.Rational(1, 2), q_sym))
add("perturbed", "q_pochhammer_infty", q_poch_infty(a_sym, sp.Rational(1, 3)))
# Eisenstein at varying weights
add("perturbed", "eisenstein_E2k", eisenstein_summand(q_sym, weight=6),
    comment="E_6")
add("perturbed", "eisenstein_E2k", eisenstein_summand(q_sym, weight=8),
    comment="E_8")
# Gauss sums at varying p, q (all non-degenerate)
add("perturbed", "gauss_sum", gauss_sum_summand(2, 5),
    comment="p=2 q=5 (q odd, non-degenerate)")
add("perturbed", "gauss_sum", gauss_sum_summand(3, 7),
    comment="p=3 q=7 (q odd)")

# --- composed (10 cases) ---
# Sums and products of two canonical kernels. We expect the recognizer to
# match ONE of the two components at top level (it won't decompose without
# the composite-recognizer of experiment 11, which we don't reload here).

add("composed", "gaussian_quadratic", gauss_summand(sp.Rational(1, 5)) + bose_summand(sp.Rational(1, 5)),
    accept_families=["gaussian_quadratic", "bose_einstein_geometric"],
    comment="gaussian + bose; composite-wrapper should peel either component")
add("composed", "lambert_divisor", lambert_summand(sp.Rational(1, 3)) + lambert_summand(sp.Rational(1, 5)),
    accept_families=["lambert_divisor"],
    comment="lambert + lambert")
add("composed", "gaussian_quadratic", gauss_summand(sp.Rational(1, 4)) * bose_summand(sp.Rational(1, 4)),
    accept_families=["gaussian_quadratic", "bose_einstein_geometric"],
    comment="gaussian * bose product")
add("composed", "gaussian_quadratic", gauss_summand(sp.Rational(1, 4)) * lambert_summand(sp.Rational(1, 2)),
    accept_families=["gaussian_quadratic", "lambert_divisor"],
    comment="gaussian * lambert")
add("composed", "partial_theta", partial_theta_summand(sp.Rational(1, 2)) + partial_theta_summand(sp.Rational(1, 4)),
    accept_families=["partial_theta"],
    comment="two partial thetas")
add("composed", "mock_theta_f3", mock_f3_summand(sp.Rational(1, 3)) + gauss_summand(sp.Rational(1, 3)),
    accept_families=["mock_theta_f3", "gaussian_quadratic"],
    comment="mock-theta + gaussian (canonical mock-modular decomposition shape)")
add("composed", "bose_einstein_geometric", bose_summand(sp.Rational(1, 10)) * lambert_summand(sp.Rational(1, 2)),
    accept_families=["bose_einstein_geometric", "lambert_divisor"],
    comment="bose * lambert")
add("composed", "q_pochhammer_infty", q_poch_infty(sp.Rational(1, 3), sp.Rational(1, 2)) * q_poch_infty(sp.Rational(1, 5), sp.Rational(1, 4)),
    accept_families=["q_pochhammer_infty"],
    comment="product of two q-Pochhammers (each a Product object)")
add("composed", "eisenstein_E2k", eisenstein_summand(q_sym, 4) + eisenstein_summand(q_sym, 6),
    accept_families=["eisenstein_E2k"],
    comment="E_4 + E_6")
add("composed", "gauss_sum", gauss_sum_summand(1, 3) + gauss_sum_summand(1, 5),
    accept_families=["gauss_sum"],
    comment="sum of two non-degenerate Gauss sums")

# --- adversarial (10+ cases) ---
# 1. Shifted-theta q^(n^2 + n) — looks gaussian but has a linear term
add("adversarial", "none", q_sym ** (n ** 2 + n),
    comment="shifted theta — must NOT match gaussian (gaussian matcher refuses linear-in-n)")
add("adversarial", "none", sp.exp(-sp.Rational(1, 5) * n ** 2 - sp.Rational(1, 10) * n),
    comment="shifted gaussian via exp form — must NOT match")

# 2. Gauss sum at q ≡ 2 (mod 4) — must DEGENERATE
add("adversarial", "gauss_sum", gauss_sum_summand(1, 6),
    expect_degenerate=True,
    comment="q=6: SILENT ZERO HAZARD §A4 — must emit DEGENERATE")
add("adversarial", "gauss_sum", gauss_sum_summand(1, 10),
    expect_degenerate=True,
    comment="q=10: also ≡ 2 (mod 4)")
add("adversarial", "gauss_sum", gauss_sum_summand(1, 14),
    expect_degenerate=True,
    comment="q=14: ≡ 2 (mod 4)")
add("adversarial", "gauss_sum", gauss_sum_summand(2, 6),
    expect_degenerate=False,
    comment="p=2 q=6: sympy auto-simplifies to p=1 q=3 BEFORE the matcher sees it — "
            "the non-coprime degeneracy never fires because the fraction is reduced. "
            "Diagnostic note: the recognizer's degeneracy_check sees only the simplified "
            "form; gcd-based hazards are unreachable through the sympy AST.")

# 3. Mock theta with a perturbing extra factor: should we still match? We
#    deliberately add a non-recognized factor; the matcher's `if others: return None`
#    means we will MISS. Document the false-negative.
add("adversarial", "none", mock_f3_summand(q_sym) * sp.cos(n),
    comment="mock-f3 * cos(n) — we expect MISS (matcher rejects extra factors)")

# 4. Lambert-look-alike with wrong denominator: q^n / (1 - q^(2n))
add("adversarial", "none", q_sym ** n / (1 - q_sym ** (2 * n)),
    comment="q^n / (1 - q^(2n)) — NOT a Lambert divisor; we expect MISS")

# 5. Partial-theta look-alike with q^(n^2 + n + 1) (constant offset)
add("adversarial", "none", q_sym ** (n ** 2 + n + 1),
    comment="extra constant offset; must NOT match partial_theta or gaussian")

# 6. Dirichlet with positive exponent — n^(+s) is divergent; expect MISS
add("adversarial", "none", chi(n) * n ** s_sym,
    comment="positive exponent n^s — not a Dirichlet L-summand")

# 7. Eisenstein with non-divisor function: σ disguised as a generic function
generic_f = sp.Function("f")
add("adversarial", "none", generic_f(n) * q_sym ** n,
    comment="generic f(n) q^n — not divisor sigma")

# --- run the benchmark ---

def evaluate(case):
    # For composed cases, use the composite wrapper that peels Add/Mul.
    if case["cohort"] == "composed":
        bm, mode = best_match_composite(case["expr"], n, tol=mpf("1e-12"))
    else:
        bm = best_match(case["expr"], n, tol=mpf("1e-12"))
    if bm is None:
        predicted = "none"
        route = "NONE"
        degen = False
    else:
        predicted = bm["kernel"]
        route = bm["route"].value
        degen = bm["degenerate"] is not None
    if case["expect_degenerate"]:
        correct = (predicted == case["true_family"]) and degen
    else:
        accept = case.get("accept_families", [case["true_family"]])
        correct = (predicted in accept)
    return predicted, route, degen, correct


def run():
    rows = []
    for case in CASES:
        predicted, route, degen, correct = evaluate(case)
        rows.append({
            "case_id": case["case_id"],
            "cohort": case["cohort"],
            "true_family": case["true_family"],
            "predicted_family": predicted,
            "route": route,
            "degenerate_flag": degen,
            "correct": correct,
            "comment": case["comment"],
        })

    # write CSV
    with open(OUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "case_id", "cohort", "true_family", "predicted_family",
            "route", "degenerate_flag", "correct", "comment",
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} cases to {OUT_CSV}")
    print()

    # ---------- per-family precision / recall ----------
    # Composed cases declare an `accept_families` set; if the prediction is
    # in that set we count it as TP for the predicted family (the composite
    # is genuinely multi-component, so peeling any registered piece counts).
    # For non-composed cases we use the strict per-case `true_family`.
    families = sorted(set([r["true_family"] for r in rows]) | set([r["predicted_family"] for r in rows]))
    tp = Counter()
    fp = Counter()
    fn = Counter()
    accept_lookup = {c["case_id"]: set(c["accept_families"]) for c in CASES}
    for r in rows:
        accept = accept_lookup[r["case_id"]]
        if r["predicted_family"] in accept:
            tp[r["predicted_family"]] += 1
        else:
            fp[r["predicted_family"]] += 1
            fn[r["true_family"]] += 1

    print(f"{'family':<26} {'#true':>6} {'#pred':>6} {'TP':>4} {'FP':>4} {'FN':>4} {'prec':>6} {'recall':>7} {'F1':>6}")
    print("-" * 80)
    total_correct = sum(1 for r in rows if r["correct"])
    macro_prec = []
    macro_rec = []
    for fam in families:
        # n_true = how many cases would accept `fam` as a correct answer
        n_true = sum(1 for c in CASES if fam in c["accept_families"])
        n_pred = sum(1 for r in rows if r["predicted_family"] == fam)
        t = tp[fam]
        prec = t / n_pred if n_pred > 0 else float("nan")
        rec = t / n_true if n_true > 0 else float("nan")
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else float("nan")
        print(f"{fam:<26} {n_true:>6} {n_pred:>6} {t:>4} {fp[fam]:>4} {fn[fam]:>4} {prec:>6.2f} {rec:>7.2f} {f1:>6.2f}")
        if not math.isnan(prec):
            macro_prec.append(prec)
        if not math.isnan(rec):
            macro_rec.append(rec)
    print("-" * 80)
    macro_p = sum(macro_prec) / len(macro_prec) if macro_prec else float("nan")
    macro_r = sum(macro_rec) / len(macro_rec) if macro_rec else float("nan")
    print(f"{'MACRO AVG':<26} {'':>6} {'':>6} {'':>4} {'':>4} {'':>4} {macro_p:>6.2f} {macro_r:>7.2f}")
    print(f"Overall accuracy: {total_correct}/{len(rows)} = {total_correct/len(rows):.2%}")
    print()

    # ---------- adversarial spotlight ----------
    print("Adversarial cohort detail:")
    for r in rows:
        if r["cohort"] == "adversarial":
            tag = "OK " if r["correct"] else "FAIL"
            print(f"  [{tag}] case {r['case_id']:>2}: true={r['true_family']:<22} pred={r['predicted_family']:<22} "
                  f"route={r['route']:<28} deg={int(r['degenerate_flag'])}  {r['comment']}")

    return rows


if __name__ == "__main__":
    run()
