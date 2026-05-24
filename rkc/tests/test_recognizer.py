"""Unit tests for the rkc v2 recognizer.

Covers every kernel family + every degeneracy branch. These tests are the
truth oracle for the package; if a kernel passes the manual benchmark but
fails its unit test here, fix the test or the implementation — don't paper
over it.
"""
from __future__ import annotations

import sys
import pathlib
import sympy as sp
import pytest

# allow running from the ramanujan/ root: include the parent so `rkc` resolves
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from rkc import (
    recognize, best_match, recognize_composite, recognize_with_raw_string,
    Route, KernelFamily,
)


@pytest.fixture
def n():
    return sp.symbols("n", integer=True, nonnegative=True)


@pytest.fixture
def k():
    return sp.symbols("k", integer=True, nonnegative=True)


# ============================================================
# Strict matches — one test per kernel family
# ============================================================

def test_gaussian_quadratic(n):
    bm = best_match(sp.exp(-sp.Rational(1, 10) * n ** 2), n)
    assert bm is not None
    assert bm.kernel == "gaussian_quadratic"
    assert bm.family == KernelFamily.THETA_LIKE.value
    assert bm.route in (Route.DIRECT, Route.DUAL)
    assert bm.confidence == 1.0


def test_gaussian_quadratic_q_form(n):
    bm = best_match(sp.Rational(1, 2) ** (n ** 2), n)
    assert bm is not None
    assert bm.kernel == "gaussian_quadratic"


def test_bose_einstein(n):
    bm = best_match(1 / (1 - sp.exp(-sp.Rational(1, 5) * n)), n)
    assert bm is not None
    assert bm.kernel == "bose_einstein_geometric"


def test_lambert_divisor(n):
    q = sp.Rational(1, 3)
    bm = best_match(q ** n / (1 - q ** n), n)
    assert bm is not None
    assert bm.kernel == "lambert_divisor"


def test_mock_theta_f3(n, k):
    q = sp.Rational(1, 3)
    expr = q ** (n ** 2) / sp.Product((1 + q ** k) ** 2, (k, 1, n))
    bm = best_match(expr, n)
    assert bm is not None
    assert bm.kernel == "mock_theta_f3"


def test_mock_theta_f5(n, k):
    q = sp.Rational(1, 4)
    expr = q ** (n ** 2) / sp.Product(1 + q ** k, (k, 1, n))
    bm = best_match(expr, n)
    assert bm is not None
    assert bm.kernel == "mock_theta_f5"


def test_mock_theta_f7(n, k):
    q = sp.Rational(1, 5)
    expr = q ** (n ** 2) / sp.Product(1 + q ** k, (k, 1, 2 * n + 1))
    bm = best_match(expr, n)
    assert bm is not None
    assert bm.kernel == "mock_theta_f7"


def test_partial_theta(n):
    q = sp.Rational(1, 4)
    bm = best_match((-1) ** n * q ** (n * (n + 1) / 2), n)
    assert bm is not None
    assert bm.kernel == "partial_theta"


def test_q_pochhammer(n, k):
    q_sym, a_sym = sp.symbols("q a", positive=True)
    bm = best_match(sp.Product(1 - a_sym * q_sym ** k, (k, 0, sp.oo)), n)
    assert bm is not None
    assert bm.kernel == "q_pochhammer_infty"


def test_eisenstein_E4(n):
    q_sym = sp.symbols("q", positive=True)
    bm = best_match(sp.divisor_sigma(n, 3) * q_sym ** n, n)
    assert bm is not None
    assert bm.kernel == "eisenstein_E2k"
    assert bm.params.get("weight") == 4


def test_eisenstein_E6(n):
    q_sym = sp.symbols("q", positive=True)
    bm = best_match(sp.divisor_sigma(n, 5) * q_sym ** n, n)
    assert bm is not None
    assert bm.kernel == "eisenstein_E2k"
    assert bm.params.get("weight") == 6


def test_dirichlet_L(n):
    chi = sp.Function("chi")
    s = sp.symbols("s")
    bm = best_match(chi(n) * n ** (-s), n)
    assert bm is not None
    assert bm.kernel == "dirichlet_L"


def test_gauss_sum_odd_q(n):
    bm = best_match(sp.exp(2 * sp.pi * sp.I * 1 * n ** 2 / 3), n)
    assert bm is not None
    assert bm.kernel == "gauss_sum"
    assert bm.route == Route.DIRECT
    assert bm.degenerate is None


# ============================================================
# Gap 1 — scalar coefficient stripping
# ============================================================

def test_scalar_stripping_gaussian(n):
    """3 * exp(-beta n^2) — the v1 false negative — should now match."""
    bm = best_match(3 * sp.exp(-sp.Rational(1, 5) * n ** 2), n)
    assert bm is not None
    assert bm.kernel == "gaussian_quadratic"
    assert sp.simplify(bm.scalar_coefficient - 3) == 0


def test_scalar_stripping_lambert(n):
    """Outer rational coefficient on Lambert."""
    q = sp.Rational(1, 4)
    bm = best_match(sp.Rational(7, 2) * (q ** n / (1 - q ** n)), n)
    assert bm is not None
    assert bm.kernel == "lambert_divisor"


def test_scalar_stripping_does_not_strip_n_dependent(n):
    """Should NOT incorrectly strip an n-dependent factor."""
    # sin(n) is n-dependent; it can't be stripped, and the matcher should miss
    bm = best_match(sp.sin(sp.Rational(1, 10) * n), n)
    assert bm is None


# ============================================================
# Gap 2 — fuzzy second-pass matcher
# ============================================================

def test_fuzzy_shifted_theta(n):
    """q^(n^2 + n) — strict gaussian REJECTS, fuzzy theta-like FIRES."""
    q_sym = sp.symbols("q", positive=True)
    # strict should miss
    assert best_match(q_sym ** (n ** 2 + n), n) is None
    # fuzzy should hit
    bm = best_match(q_sym ** (n ** 2 + n), n, accept_fuzzy=True)
    assert bm is not None
    assert bm.route == Route.FUZZY
    assert bm.kernel == KernelFamily.THETA_LIKE.value
    assert 0 < bm.confidence < 1


def test_fuzzy_shifted_gaussian_exp_form(n):
    """exp(-beta n^2 - gamma n) — fuzzy theta-like."""
    expr = sp.exp(-sp.Rational(1, 5) * n ** 2 - sp.Rational(1, 10) * n)
    assert best_match(expr, n) is None
    bm = best_match(expr, n, accept_fuzzy=True)
    assert bm is not None
    assert bm.route == Route.FUZZY


def test_fuzzy_mock_theta_with_extra_factor(n, k):
    """mock-f3 * cos(n) — strict rejects, fuzzy mock-theta-like fires."""
    q_sym = sp.symbols("q", positive=True)
    expr = (q_sym ** (n ** 2) / sp.Product((1 + q_sym ** k) ** 2, (k, 1, n))) * sp.cos(n)
    assert best_match(expr, n) is None
    bm = best_match(expr, n, accept_fuzzy=True)
    assert bm is not None
    assert bm.route == Route.FUZZY
    assert bm.kernel == KernelFamily.MOCK_THETA_LIKE.value


def test_fuzzy_lambert_lookalike(n):
    """q^n / (1 - q^(2n)) — strict rejects, fuzzy lambert-like fires."""
    q_sym = sp.symbols("q", positive=True)
    expr = q_sym ** n / (1 - q_sym ** (2 * n))
    assert best_match(expr, n) is None
    bm = best_match(expr, n, accept_fuzzy=True)
    assert bm is not None
    assert bm.route == Route.FUZZY
    assert bm.kernel == KernelFamily.LAMBERT_LIKE.value


# ============================================================
# Gap 3 — per-component cost rollup for composites
# ============================================================

def test_composite_sum_rollup(n):
    expr = sp.exp(-sp.Rational(1, 4) * n ** 2) + 1 / (1 - sp.exp(-sp.Rational(1, 4) * n))
    cm = recognize_composite(expr, n)
    assert cm is not None
    assert "composite" in cm.kernel
    assert len(cm.components) == 2
    # total_cost should be the sum of component total_costs (both positive)
    s = sum(c["total_cost"] for c in cm.components if c["total_cost"] > 0)
    assert abs(cm.total_cost - s) < 1e-6


def test_composite_product_rollup(n):
    q = sp.Rational(1, 4)
    expr = sp.exp(-sp.Rational(1, 4) * n ** 2) * (q ** n / (1 - q ** n))
    cm = recognize_composite(expr, n)
    assert cm is not None
    assert len(cm.components) >= 1


# ============================================================
# Gap 4 — per-term cost tracking
# ============================================================

def test_per_term_cost_populated(n):
    """Every strict match should carry a positive per_term_cost and total_cost."""
    bm = best_match(sp.exp(-sp.Rational(1, 10) * n ** 2), n)
    assert bm is not None
    assert bm.per_term_cost > 0
    assert bm.total_cost > 0
    assert bm.num_terms > 0
    # total_cost should be ~ num_terms * per_term_cost
    assert abs(bm.total_cost - bm.num_terms * bm.per_term_cost) < bm.per_term_cost + 1e-6


def test_per_term_cost_kernel_distinction(n):
    """Mock theta should have higher per-term cost than gaussian (partial
    products are n-multiplications heavy)."""
    bm_gauss = best_match(sp.Rational(1, 3) ** (n ** 2), n)
    k = sp.symbols("k", integer=True, nonnegative=True)
    bm_mock = best_match(
        sp.Rational(1, 3) ** (n ** 2) /
        sp.Product((1 + sp.Rational(1, 3) ** k) ** 2, (k, 1, n)),
        n,
    )
    assert bm_gauss is not None and bm_mock is not None
    assert bm_mock.per_term_cost > bm_gauss.per_term_cost


# ============================================================
# Gap 5 — Gauss-sum gcd-degeneracy fix
# ============================================================

def test_gauss_sum_silent_zero_q_eq_2_mod_4(n):
    """q ≡ 2 (mod 4) — must DEGENERATE (silent-zero hazard §A4)."""
    for q_int in (6, 10, 14):
        bm = best_match(sp.exp(2 * sp.pi * sp.I * 1 * n ** 2 / q_int), n)
        assert bm is not None
        assert bm.kernel == "gauss_sum"
        assert bm.route == Route.DEGENERATE
        assert bm.degenerate is not None
        assert "2 (mod 4)" in bm.degenerate


def test_gauss_sum_gcd_via_raw_string(n):
    """Without the raw-string entry point, '2*n^2/6' gets auto-reduced by
    sympy and the gcd branch is unreachable. WITH the raw entry point,
    the (p_raw=2, q_raw=6) survives and the gcd guard fires."""
    results = recognize_with_raw_string("exp(2*pi*I*2*n**2/6)", n)
    # at least one result must be the gauss_sum with the gcd reason
    gauss = [r for r in results if r.kernel == "gauss_sum"]
    assert gauss
    g = gauss[0]
    assert g.route == Route.DEGENERATE
    assert g.degenerate is not None
    assert "raw" in g.degenerate.lower() or "gcd" in g.degenerate.lower()


def test_gauss_sum_post_reduction_still_works(n):
    """After sympy reduces 2/6 -> 1/3, the post-reduction (p=1, q=3) is
    non-degenerate and the recognizer should report DIRECT."""
    # sympify auto-reduces this; we don't use the raw entry point
    bm = best_match(sp.exp(2 * sp.pi * sp.I * 2 * n ** 2 / 6), n)
    assert bm is not None
    assert bm.kernel == "gauss_sum"
    assert bm.route == Route.DIRECT


# ============================================================
# Degeneracy branches — one test per branch
# ============================================================

def test_degeneracy_lambert_q_eq_1(n):
    bm = best_match(sp.Integer(1) ** n / (1 - sp.Integer(1) ** n), n)
    # this is structurally 1 / 0 — sympy may simplify to zoo or fail to match
    # the matcher; either way, no clean non-degenerate result should appear
    if bm is not None:
        assert bm.route == Route.DEGENERATE or bm.degenerate is not None


def test_degeneracy_pochhammer_a_eq_1(n, k):
    q_sym = sp.symbols("q", positive=True)
    bm = best_match(sp.Product(1 - 1 * q_sym ** k, (k, 0, sp.oo)), n)
    assert bm is not None
    assert bm.kernel == "q_pochhammer_infty"
    assert bm.route == Route.DEGENERATE
    assert "a = 1" in bm.degenerate or "(1;" in bm.degenerate


def test_degeneracy_partial_theta_q_gte_1(n):
    bm = best_match((-1) ** n * sp.Integer(2) ** (n * (n + 1) / 2), n)
    assert bm is not None
    assert bm.kernel == "partial_theta"
    assert bm.route == Route.DEGENERATE


def test_degeneracy_eisenstein_q_outside(n):
    # the eisenstein matcher accepts q symbolically; the degeneracy_check
    # only fires when q is numerically outside (0, 1). With q=2 it should.
    bm = best_match(sp.divisor_sigma(n, 3) * sp.Integer(2) ** n, n)
    assert bm is not None
    assert bm.kernel == "eisenstein_E2k"
    assert bm.route == Route.DEGENERATE


# ============================================================
# Backwards-compatibility — every v1 strict positive must remain a v2 positive
# ============================================================

def test_v1_canonical_strict_matches_all_pass(n, k):
    """A subset of the v1 benchmark canonical cohort. All must strict-match."""
    q_sym = sp.symbols("q", positive=True)
    a_sym = sp.symbols("a", positive=True)
    s_sym = sp.symbols("s")
    chi = sp.Function("chi")
    cases = [
        sp.exp(-sp.Rational(1, 10) * n ** 2),
        sp.Rational(1, 2) ** (n ** 2),
        1 / (1 - sp.exp(-sp.Rational(1, 20) * n)),
        sp.Rational(99, 100) ** n / (1 - sp.Rational(99, 100) ** n),
        q_sym ** (n ** 2) / sp.Product((1 + q_sym ** k) ** 2, (k, 1, n)),
        q_sym ** (n ** 2) / sp.Product(1 + q_sym ** k, (k, 1, n)),
        q_sym ** (n ** 2) / sp.Product(1 + q_sym ** k, (k, 1, 2 * n + 1)),
        (-1) ** n * q_sym ** (n * (n + 1) / 2),
        sp.Product(1 - a_sym * q_sym ** k, (k, 0, sp.oo)),
        sp.divisor_sigma(n, 3) * q_sym ** n,
        chi(n) * n ** (-s_sym),
        sp.exp(2 * sp.pi * sp.I * 1 * n ** 2 / 3),
    ]
    for case in cases:
        bm = best_match(case, n)
        assert bm is not None, f"v2 regression on {case}"


def test_no_false_positive_on_sin(n):
    assert best_match(sp.sin(sp.Rational(1, 10) * n), n) is None


def test_no_false_positive_on_cos_plus_one(n):
    assert best_match(sp.cos(n) + 1, n) is None


# ============================================================
# Smoke test for the package import surface
# ============================================================

def test_package_exports():
    import rkc
    assert hasattr(rkc, "recognize")
    assert hasattr(rkc, "best_match")
    assert hasattr(rkc, "Route")
    assert hasattr(rkc, "KernelFamily")
    assert Route.FUZZY  # v2-new
