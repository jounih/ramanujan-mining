"""
Experiment 19 — Recognizer mock-theta end-to-end demo.

This script demonstrates the closed loop wired up by the rkc/ completions
route handler:

  1. A user writes a mock-theta-f3 sympy expression.
  2. `rkc.best_match(..., numerical_completion=True, target_digits=N)`
     recognises it as mock_theta_f3 with route MODULAR_COMPLETION_REQUIRED
     AND calls the Watson-Hickerson Eichler-integral pipeline (exp 17)
     to return a numerical value with a certificate.
  3. We cross-check the bias-corrected value against direct-series
     evaluation from `analysis/15_mock_theta_residual_demo.py::f_mock_theta`
     to ≥30 digits.

Outputs to stdout: the recognised kernel, the bias-corrected value, the
modular_residual (error bound), the Eichler-integral M(α), and the cross
check residual vs exp 15's direct evaluator.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys

import sympy as sp
from mpmath import mp, mpf, exp, log


HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

from rkc import best_match, Route  # noqa: E402
from rkc.completions import compute_mock_theta_with_completion  # noqa: E402


def _load_exp15():
    """exp 15's f_mock_theta is the v0 direct-series evaluator."""
    spec = importlib.util.spec_from_file_location(
        "ramanujan_exp15", HERE / "15_mock_theta_residual_demo.py",
    )
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def demo():
    mp.dps = 60
    print("=" * 78)
    print("Experiment 19 — rkc end-to-end mock-theta completion demo")
    print("=" * 78)

    n, k = sp.symbols("n k", integer=True, nonnegative=True)

    # ------------------------------------------------------------
    # Step 1: user writes a mock-theta-f3 sympy expression
    # ------------------------------------------------------------
    # f3 summand: q^(n^2) / Π_{k=1..n} (1 + q^k)^2
    # Use q=1/2 (α=log 2 ≈ 0.693, inside the calibrated α ≤ 0.7 regime).
    q_rat = sp.Rational(1, 2)
    expr = q_rat ** (n ** 2) / sp.Product((1 + q_rat ** k) ** 2, (k, 1, n))
    print()
    print("Input AST:")
    print(f"  expr = {expr}")
    print(f"  n    = {n}")

    # ------------------------------------------------------------
    # Step 2: recognise with numerical completion opted in
    # ------------------------------------------------------------
    print()
    print("Step 2: recognize with numerical_completion=True")
    bm = best_match(expr, n, numerical_completion=True, target_digits=40)
    assert bm is not None, "recognizer failed to match — abort"
    assert bm.kernel == "mock_theta_f3"
    assert bm.route == Route.MODULAR_COMPLETION_REQUIRED
    assert bm.completion is not None, "completion not attached"
    print(f"  kernel              = {bm.kernel}")
    print(f"  family              = {bm.family}")
    print(f"  route               = {bm.route.value}")
    print(f"  scalar_coefficient  = {bm.scalar_coefficient}")
    print(f"  completion attached = True")

    # ------------------------------------------------------------
    # Step 3: unpack the completion result
    # ------------------------------------------------------------
    value, error_bound, cert = bm.completion
    print()
    print("Step 3: completion result")
    print(f"  value (40-dps)      = {value}")
    print(f"  error_bound         = {error_bound:.3e}")
    print(f"  family              = {cert.family}")
    print(f"  method              = {cert.method}")
    print(f"  source              = {cert.source}")
    print(f"  α  = -log(q)        = {cert.alpha:.6f}")
    print(f"  β  = π²/α  (dual)   = {cert.beta_dual:.6f}")
    print(f"  working_dps         = {cert.working_dps}")
    print(f"  modular_term        = {cert.modular_term:.6e}")
    print(f"  shadow_eichler M(α) = {cert.shadow_eichler_integral:.6e}")
    print(f"  regime              = {cert.regime}")
    print(f"  confidence          = {cert.confidence}")
    print(f"  notes               = {cert.notes}")

    # ------------------------------------------------------------
    # Step 4: cross-check against exp 15's direct evaluator
    # ------------------------------------------------------------
    exp15 = _load_exp15()
    q_num = mpf(q_rat)
    f_direct = exp15.f_mock_theta(q_num, N=300)
    diff = abs(mpf(value) - f_direct)
    digits = -log(diff + mpf(10) ** (-(mp.dps - 2))) / log(10)

    print()
    print("Step 4: cross-check against exp 15 direct evaluator")
    print(f"  exp 15 direct f(q)  = {f_direct}")
    print(f"  rkc package value   = {value}")
    print(f"  |diff|              = {float(diff):.3e}")
    print(f"  digits of agreement = {float(digits):.1f}")

    assert float(digits) >= 30.0, (
        f"e2e cross-check failed: only {float(digits):.1f} digits"
    )
    print()
    print("PASS: ≥30 digits of agreement between rkc completion and exp 15.")

    # ------------------------------------------------------------
    # Step 5: also exercise a small-α sweep to show consistency
    # ------------------------------------------------------------
    print()
    print("=" * 78)
    print("Mini β sweep — package value vs exp 15 direct evaluator")
    print("=" * 78)
    print(f"{'β = α':>10}  {'|diff|':>14}  {'digits':>8}  {'regime':>20}")
    for beta_str in ("0.001", "0.01", "0.1", "0.5"):
        a = mpf(beta_str)
        q_test = exp(-a)
        cr = compute_mock_theta_with_completion("mock_theta_f3", q_test,
                                                target_digits=40)
        f_d = exp15.f_mock_theta(q_test, N=300)
        d = abs(mpf(cr.value) - f_d)
        digs = -log(d + mpf(10) ** (-(mp.dps - 2))) / log(10)
        print(f"{beta_str:>10}  {float(d):>14.3e}  {float(digs):>8.1f}  "
              f"{cr.certificate.regime:>20}")


if __name__ == "__main__":
    demo()
