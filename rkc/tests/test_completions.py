"""Unit tests for the rkc completions module (Watson-Hickerson Eichler
integral route handler for MODULAR_COMPLETION_REQUIRED).

These tests are the truth oracle for the rkc <-> exp 17 wiring. They:

  1. Cross-check the package's f3 value against analysis/17's value at
     β ∈ {0.001, 0.01, 0.1, 0.5} to ≥30 digits. (Four parameterised cases.)
  2. Confirm that with `numerical_completion=False` the recognizer still
     returns the flag (not the value) — backward compatibility.
  3. Confirm that non-mock-theta inputs never trigger the completion path.
  4. Confirm that mock_theta_f5 / mock_theta_f7 raise
     `CompletionNotImplemented` with the family name (unimplemented gap).
  5. Plus: positional unpacking, certificate provenance,
     small-α calibrated regime tagging.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys

import sympy as sp
import pytest
from mpmath import mp, mpf, exp, log, pi, sqrt

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from rkc import (
    best_match,
    recognize,
    Route,
    compute_mock_theta_with_completion,
    CompletionNotImplemented,
    CompletionResult,
    supported_families,
    coverage_report,
)
from rkc import completions as _completions_mod


# ---------------------------------------------------------------------------
# Helper: load exp 17 the same way completions.py does (so the cross-check
# tests are tied to the script we wrap)
# ---------------------------------------------------------------------------

EXP17_PATH = ROOT / "analysis" / "17_mock_theta_residual_ebm_v1.py"


@pytest.fixture(scope="module")
def exp17():
    spec = importlib.util.spec_from_file_location("ramanujan_exp17_test", EXP17_PATH)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@pytest.fixture
def n():
    return sp.symbols("n", integer=True, nonnegative=True)


@pytest.fixture
def k():
    return sp.symbols("k", integer=True, nonnegative=True)


# ===========================================================================
# 1. Cross-check the package value against the analysis/17 value at four
#    β values to ≥30 digits. β here = α in exp 17's notation (the inverse
#    temperature; q = exp(-β)).
# ===========================================================================

@pytest.mark.parametrize("beta_str", ["0.001", "0.01", "0.1", "0.5"])
def test_f3_package_value_matches_exp17_to_30_digits(beta_str, exp17):
    """Pipeline check: compute_mock_theta_with_completion(...) reconstructs
    f(q) and the direct series f_mock_theta(q) at ≥30-digit agreement.

    The math: Watson's identity gives
        F(α) = q^{-1/24} f(q) = modular_term + M(α)
    so the reconstructed value should agree with the direct series to
    whatever precision both are computed at (working dps).
    """
    saved = mp.dps
    try:
        mp.dps = 60
        beta = mpf(beta_str)
        q = exp(-beta)

        # package path
        result = compute_mock_theta_with_completion("mock_theta_f3", q, target_digits=40)
        assert isinstance(result, CompletionResult)

        # exp 17 direct-series ground truth
        f_q_direct = exp17.f_mock_theta(q)

        diff = abs(mpf(result.value) - f_q_direct)
        digits_agree = -log(diff + mpf(10) ** (-(mp.dps - 2))) / log(10)
        assert float(digits_agree) >= 30.0, (
            f"β={beta_str}: only {float(digits_agree):.1f} digits of agreement "
            f"(value={result.value!s}, direct={f_q_direct!s}, |diff|={float(diff):.3e})"
        )
        # also: certificate's modular_residual must be tight at small β
        assert result.error_bound < 1e-25
    finally:
        mp.dps = saved


# ===========================================================================
# 2. Backward compatibility — numerical_completion=False (default) leaves
#    the result a flag with no .completion attached
# ===========================================================================

def test_default_keeps_flag_only_behavior(n, k):
    """The mock_theta_f3 strict match should still come back with route
    MODULAR_COMPLETION_REQUIRED and `.completion = None` when
    `numerical_completion` is not requested. v1/v2 behavior preserved.
    """
    q = sp.Rational(1, 3)
    expr = q ** (n ** 2) / sp.Product((1 + q ** k) ** 2, (k, 1, n))
    bm = best_match(expr, n)
    assert bm is not None
    assert bm.kernel == "mock_theta_f3"
    # the matcher at q=1/3 routes MODULAR_COMPLETION_REQUIRED (small α)
    assert bm.route == Route.MODULAR_COMPLETION_REQUIRED
    # default opt-out path: NO numerical answer attached
    assert bm.completion is None
    assert bm.completion_error is None


# ===========================================================================
# 3. Non-mock-theta input — completion is not triggered even with the flag on
# ===========================================================================

def test_non_mock_theta_completion_not_triggered(n):
    """Asking for numerical_completion on a gaussian should leave .completion
    None (the route isn't MODULAR_COMPLETION_REQUIRED)."""
    bm = best_match(
        sp.exp(-sp.Rational(1, 10) * n ** 2), n,
        numerical_completion=True, q_value=0.5,
    )
    assert bm is not None
    assert bm.kernel == "gaussian_quadratic"
    assert bm.route in (Route.DIRECT, Route.DUAL)
    assert bm.completion is None
    assert bm.completion_error is None


# ===========================================================================
# 4. Unimplemented mock-theta family — clear exception with family name
# ===========================================================================

def test_unimplemented_family_raises_with_family_name():
    """mock_theta_f5 is registered with the recognizer but has no
    Watson-Hickerson instrumentation in this run. Asking for its
    completion directly must raise CompletionNotImplemented carrying the
    family name."""
    with pytest.raises(CompletionNotImplemented) as exc_info:
        compute_mock_theta_with_completion("mock_theta_f5", q=mpf("0.5"))
    assert exc_info.value.family == "mock_theta_f5"
    assert "mock_theta_f5" in str(exc_info.value)


def test_unimplemented_family_via_recognizer(n, k):
    """When the recognizer matches mock_theta_f5 and the user opts in to
    numerical completion, the result should carry a completion_error
    rather than a value (because f5 is not instrumented)."""
    q = sp.Rational(1, 4)
    expr = q ** (n ** 2) / sp.Product(1 + q ** k, (k, 1, n))
    bm = best_match(expr, n, numerical_completion=True, q_value=q)
    assert bm is not None
    assert bm.kernel == "mock_theta_f5"
    # f5 is registered but not instrumented: completion path returns the
    # error message instead of mutating .completion
    assert bm.completion is None
    assert bm.completion_error is not None
    assert "mock_theta_f5" in bm.completion_error


# ===========================================================================
# 5. Recognizer integration: opt-in path attaches a real value
# ===========================================================================

def test_recognizer_opt_in_attaches_value(n, k):
    """End-to-end through the recognizer: mock_theta_f3 + opt-in flag
    should yield a result with .completion populated and a tight
    error_bound.

    We use a small-α q (q=exp(-0.1)≈0.9048) where the Watson identity
    is calibrated to ≥30 digits (diary 12 §6a). q=1/3 would put us in
    α=log(3)≈1.099, the 'near-cusp-warning' regime where the residual
    is dominated by uncomputed q_1^4 corrections to W, not by the
    Eichler-integral pipeline itself.
    """
    # Use a rational q that lands inside the calibrated regime
    # (α = -log(q) ≤ 0.7). q=1/2 gives α=log(2)≈0.693, just calibrated.
    q_sym = sp.Rational(1, 2)
    expr = q_sym ** (n ** 2) / sp.Product((1 + q_sym ** k) ** 2, (k, 1, n))
    bm = best_match(expr, n, numerical_completion=True, target_digits=35)
    assert bm is not None
    assert bm.kernel == "mock_theta_f3"
    assert bm.route == Route.MODULAR_COMPLETION_REQUIRED
    assert bm.completion is not None
    val, err, cert = bm.completion  # positional unpacking
    assert err < 1e-25, f"error_bound={err}"
    assert cert.family == "mock_theta_f3"
    assert cert.method.startswith("Watson-Hickerson")
    assert cert.regime == "calibrated"


# ===========================================================================
# 6. Coverage report shape
# ===========================================================================

def test_coverage_report_lists_registered_mock_thetas():
    """The coverage_report() must list every registered MOCK_THETA_LIKE
    family with an honest end-to-end / flag-only tag."""
    rep = coverage_report()
    assert "mock_theta_f3" in rep
    assert rep["mock_theta_f3"] == "end-to-end"
    # f5 and f7 are registered but not instrumented in this run
    assert "mock_theta_f5" in rep
    assert "flag-only" in rep["mock_theta_f5"]
    assert "mock_theta_f7" in rep
    assert "flag-only" in rep["mock_theta_f7"]


def test_supported_families_is_subset_of_coverage():
    s = supported_families()
    cov = coverage_report()
    assert s.issubset(set(cov.keys()))


# ===========================================================================
# 7. Calibrated-regime tagging — α ≤ 0.7 → "calibrated", α > 0.7 → warning
# ===========================================================================

def test_calibrated_regime_at_small_alpha():
    """β=0.1 → α=0.1 ≤ 0.7 → 'calibrated' regime, 'high' confidence."""
    result = compute_mock_theta_with_completion("mock_theta_f3",
                                                q=exp(-mpf("0.1")),
                                                target_digits=30)
    assert result.certificate.regime == "calibrated"
    assert result.certificate.confidence == "high"


def test_near_cusp_warning_at_large_alpha():
    """β=1.5 → α=1.5 > 0.7 → 'near-cusp-warning' regime, lower confidence.
    The residual will be larger than at small α (W identity not pinned)."""
    result = compute_mock_theta_with_completion("mock_theta_f3",
                                                q=exp(-mpf("1.5")),
                                                target_digits=30)
    assert result.certificate.regime == "near-cusp-warning"
    assert result.certificate.confidence in ("low", "medium")


# ===========================================================================
# 8. Bad input — q outside (0, 1)
# ===========================================================================

def test_rejects_q_out_of_range():
    with pytest.raises(ValueError):
        compute_mock_theta_with_completion("mock_theta_f3", q=mpf("1.5"))
    with pytest.raises(ValueError):
        compute_mock_theta_with_completion("mock_theta_f3", q=mpf("0"))


# ===========================================================================
# 9. Provenance — certificate's source must point at the exp 17 script
# ===========================================================================

def test_certificate_provenance_points_at_exp17():
    result = compute_mock_theta_with_completion("mock_theta_f3",
                                                q=mpf("0.5"),
                                                target_digits=30)
    assert "17_mock_theta_residual_ebm_v1.py" in result.certificate.source
