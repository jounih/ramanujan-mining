"""Unit tests for the Brusselator + Lambert-W cousin verification (diary 68).

These tests are fast (<60s total) and guard the structural correctness of:

  * rkc.dynamics.brusselator_cousin.turning_points (Lambert-W identification)
  * rkc.dynamics.brusselator_cousin.period_cousin (quadrature formula)
  * rkc.dynamics.brusselator_cousin.period_cousin_ode (independent ODE check)
  * The mp.odefun-driven Poincare return map for the Brusselator (low-precision
    sanity check; full 30-digit run lives in analysis/38_).

The 30-digit Brusselator period itself is verified offline in
analysis/38_brusselator_period_verification.py; here we run a cheap
12-digit version as a smoke test.
"""
from __future__ import annotations

import mpmath as mp

from rkc.dynamics import (
    turning_points,
    period_cousin,
    period_cousin_ode,
    hamiltonian,
)


# ---------------------------------------------------------------------------
# Lambert-W turning points
# ---------------------------------------------------------------------------

def test_turning_points_satisfy_u_minus_log_u_eq_E():
    """For each E > 1, u_+/- must solve u - log u = E."""
    mp.mp.dps = 40
    for E in [mp.mpf("1.1"), mp.mpf(2), mp.mpf(5), mp.mpf(10), mp.mpf(100)]:
        u_minus, u_plus = turning_points(E)
        assert u_minus < 1 < u_plus, (
            "ordering wrong at E={}".format(E))
        assert abs(u_minus - mp.log(u_minus) - E) < mp.mpf("1e-35"), (
            "u_minus does not satisfy u - log u = E at E={}".format(E))
        assert abs(u_plus - mp.log(u_plus) - E) < mp.mpf("1e-35"), (
            "u_plus does not satisfy u - log u = E at E={}".format(E))


def test_hamiltonian_at_turning_points_is_E():
    """E(u, 0) = u - log u, which equals E at the turning points."""
    mp.mp.dps = 40
    for E in [mp.mpf(2), mp.mpf(5)]:
        u_minus, u_plus = turning_points(E)
        H_minus = hamiltonian(u_minus, mp.mpf(0))
        H_plus = hamiltonian(u_plus, mp.mpf(0))
        assert abs(H_minus - E) < mp.mpf("1e-35")
        assert abs(H_plus - E) < mp.mpf("1e-35")


def test_turning_points_E_lt_1_raises():
    """E < 1 has no real turning points; we raise."""
    import pytest
    mp.mp.dps = 30
    with pytest.raises(ValueError):
        turning_points(mp.mpf("0.5"))


# ---------------------------------------------------------------------------
# Cousin period: quadrature vs direct ODE
# ---------------------------------------------------------------------------

def test_period_quadrature_matches_ode_E_2():
    """Quadrature T_0(E=2) matches ODE result to >= 12 digits."""
    mp.mp.dps = 30
    T_quad = period_cousin(mp.mpf(2))
    T_ode = period_cousin_ode(mp.mpf(2), rk_dps=18)
    rel = abs(T_ode - T_quad) / abs(T_quad)
    assert rel < mp.mpf("1e-12"), (
        "T_quad={} vs T_ode={} disagree by relerr={}".format(
            mp.nstr(T_quad, 18), mp.nstr(T_ode, 18), mp.nstr(rel, 6)))


def test_period_quadrature_matches_ode_E_5():
    mp.mp.dps = 30
    T_quad = period_cousin(mp.mpf(5))
    T_ode = period_cousin_ode(mp.mpf(5), rk_dps=18)
    rel = abs(T_ode - T_quad) / abs(T_quad)
    assert rel < mp.mpf("1e-12")


def test_period_grows_with_energy():
    """T_0(E) increases monotonically in E for E > 1.

    Hand-tabulated at dps=20: T_0(1.1) ~ 6.336, T_0(2) ~ 6.815,
    T_0(5) ~ 8.392, T_0(10) ~ 10.631, T_0(100) ~ 29.128.
    """
    mp.mp.dps = 25
    Ts = [period_cousin(mp.mpf(s)) for s in ["1.1", "2", "5", "10", "100"]]
    for i in range(len(Ts) - 1):
        assert Ts[i] < Ts[i + 1], "T_0(E) not monotone at index {}".format(i)


def test_period_near_E_1_approaches_2pi():
    """At E -> 1+, the orbit shrinks to the equilibrium u=1 (eigen of the
    linearised V'' = 1/u^2 = 1) and period -> 2 pi (sqrt(omega^2)=1)."""
    mp.mp.dps = 30
    T_close = period_cousin(mp.mpf("1.000001"))
    err = abs(T_close - 2 * mp.pi)
    # Quadratic in (E-1), so at E-1 = 1e-6 the discrepancy is O(1e-6).
    assert err < mp.mpf("1e-5"), (
        "T_0(1+) -> 2 pi expected; got T={} (err={})".format(
            mp.nstr(T_close, 12), mp.nstr(err, 4)))


# ---------------------------------------------------------------------------
# Brusselator smoke test (fast)
# ---------------------------------------------------------------------------

def test_brusselator_smoke_period_close_to_7p157():
    """One-shot Poincare return at low dps; period must be 7.156... to 6 digits.

    Full 30-digit verification lives in analysis/38_brusselator_period_verification.py.
    """
    mp.mp.dps = 20
    A = mp.mpf(1)
    B = mp.mpf(3)

    def f(t, y):
        x, yy = y[0], y[1]
        return [A - (B + 1) * x + x * x * yy, B * x - x * x * yy]

    # Start at (1, 4.4688930562090759), known to be near the cycle from prior runs
    y0 = [mp.mpf(1), mp.mpf("4.4688930562090759")]
    sol = mp.odefun(f, mp.mpf(0), y0)

    # Bracket the return: x should dip below 1 and come back near t ~ 7.15
    samples = [(t, sol(mp.mpf(t))[0]) for t in [4, 5, 6, 6.5, 7, 7.5, 8]]
    bracket = None
    prev_t, prev_x = samples[0]
    for t, x in samples[1:]:
        if prev_x < 1 and x >= 1:
            bracket = (mp.mpf(prev_t), mp.mpf(t))
            break
        prev_t, prev_x = t, x
    assert bracket is not None
    a, b = bracket
    for _ in range(200):
        m = (a + b) / 2
        x_m = sol(m)[0]
        if abs(x_m - 1) < mp.mpf("1e-15"):
            break
        if x_m < 1:
            a = m
        else:
            b = m

    # Period must agree with ChatGPT's 7.15691992... to 6 digits at dps=20
    expected = mp.mpf("7.15691992117987981979986960577")
    assert abs(m - expected) < mp.mpf("1e-6"), (
        "Brusselator smoke-period={} differs from expected by {}".format(
            mp.nstr(m, 15), mp.nstr(abs(m - expected), 4)))


def test_brusselator_y0_section_close_to_chatgpt_value():
    """The Poincare-return y-value at the section must be close to 4.46889..."""
    mp.mp.dps = 20
    A = mp.mpf(1)
    B = mp.mpf(3)

    def f(t, y):
        x, yy = y[0], y[1]
        return [A - (B + 1) * x + x * x * yy, B * x - x * x * yy]

    y0 = [mp.mpf(1), mp.mpf("4.4688930562090759")]
    sol = mp.odefun(f, mp.mpf(0), y0)
    samples = [(t, sol(mp.mpf(t))[0]) for t in [4, 5, 6, 6.5, 7, 7.5, 8]]
    bracket = None
    prev_t, prev_x = samples[0]
    for t, x in samples[1:]:
        if prev_x < 1 and x >= 1:
            bracket = (mp.mpf(prev_t), mp.mpf(t))
            break
        prev_t, prev_x = t, x
    a, b = bracket
    for _ in range(200):
        m = (a + b) / 2
        x_m = sol(m)[0]
        if abs(x_m - 1) < mp.mpf("1e-15"):
            break
        if x_m < 1:
            a = m
        else:
            b = m
    y_return = sol(m)[1]
    expected = mp.mpf("4.46889305620907548510997570325")
    # After one iteration of the contracting map from a 16-digit guess,
    # we expect ~12-digit agreement (|rho| ~ 2.5e-4 -> error * 2.5e-4 ~ 4e-20 -> 12+ correct).
    assert abs(y_return - expected) < mp.mpf("1e-10")
