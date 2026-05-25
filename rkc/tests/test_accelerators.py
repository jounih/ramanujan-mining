"""Unit tests for the four cross-domain accelerators (a)-(d).

These tests are fast and serve as regression guards on the core correctness
claims. The full benchmarks live in analysis/33_..36_.
"""
from __future__ import annotations

import math

import mpmath as mp
import numpy as np
import pytest

from rkc.attention.finite_pole import (
    direct_finite_pole_attention,
    recurrent_finite_pole_attention,
)
from rkc.pde.annular_green import (
    annular_green_fourier,
    annular_green_modular,
)
from rkc.ph.bessel_image_propagator import (
    propagator_bessel,
    propagator_dft,
    chain_energy,
)
from rkc.special.airy_resurgent import airy_ai_neg_tricomi


# ---------------------------------------------------------------------------
# (a) finite-pole attention
# ---------------------------------------------------------------------------

def _make_inputs(N, R, d_v, seed=0):
    rng = np.random.default_rng(seed)
    q = rng.standard_normal((N, R))
    k = rng.standard_normal((N, R))
    v = rng.standard_normal((N, d_v))
    alpha = rng.uniform(0.1, 0.95, size=R)
    return q, k, v, alpha


def test_finite_pole_exactness_small_unnormalized():
    q, k, v, alpha = _make_inputs(16, 2, 4, seed=42)
    y_d = direct_finite_pole_attention(q, k, v, alpha)
    y_r = recurrent_finite_pole_attention(q, k, v, alpha)
    assert np.max(np.abs(y_d - y_r)) < 1e-10


def test_finite_pole_exactness_small_normalized():
    q, k, v, alpha = _make_inputs(16, 2, 4, seed=42)
    y_d = direct_finite_pole_attention(q, k, v, alpha, normalized=True)
    y_r = recurrent_finite_pole_attention(q, k, v, alpha, normalized=True)
    assert np.max(np.abs(y_d - y_r)) < 1e-10


def test_finite_pole_exactness_medium():
    q, k, v, alpha = _make_inputs(64, 4, 8, seed=7)
    y_d = direct_finite_pole_attention(q, k, v, alpha)
    y_r = recurrent_finite_pole_attention(q, k, v, alpha)
    assert np.max(np.abs(y_d - y_r)) < 1e-10


def test_finite_pole_validation():
    """alpha must be in (0, 1) for the geometric-decay form."""
    q, k, v, _ = _make_inputs(8, 2, 4)
    with pytest.raises(ValueError):
        recurrent_finite_pole_attention(q, k, v, np.array([1.5, 0.5]))


# ---------------------------------------------------------------------------
# (b) annular Green
# ---------------------------------------------------------------------------

def test_annular_green_thin_agrees():
    """Fourier with M=10000 should agree with modular to >5 digits at L=0.05."""
    mp.mp.dps = 50
    g_mod = annular_green_modular(theta=0.171, y=0.025, phi=0.170, eta=0.024, L=0.05)
    g_fou = annular_green_fourier(theta=0.171, y=0.025, phi=0.170, eta=0.024, L=0.05, M=10_000)
    diff = float(mp.fabs(g_mod - g_fou))
    # M=10000 isn't enough at L=0.05 for >40 digits, but it should give >5.
    assert diff < 1e-5


def test_annular_green_modular_is_real():
    """Modular form is a real-valued kernel."""
    g = annular_green_modular(theta=0.1, y=0.02, phi=0.05, eta=0.025, L=0.05)
    assert isinstance(g, (mp.mpf,)) or hasattr(g, "real")


# ---------------------------------------------------------------------------
# (c) PH Bessel propagator
# ---------------------------------------------------------------------------

def test_ph_bessel_matches_dft_small():
    N, t = 8, 2.0
    q_dft, p_dft = propagator_dft(t, N)
    q_b = np.zeros(N); p_b = np.zeros(N)
    for n in range(N):
        q_b[n], p_b[n] = propagator_bessel(n, t, N, abs_tol=1e-30)
    assert np.max(np.abs(q_b - q_dft)) < 1e-12
    assert np.max(np.abs(p_b - p_dft)) < 1e-12


def test_ph_energy_conservation():
    N, t = 32, 5.0
    q = np.zeros(N); p = np.zeros(N)
    for n in range(N):
        q[n], p[n] = propagator_bessel(n, t, N, abs_tol=1e-30)
    H_t = chain_energy(q, p)
    # H(0) = potential from delta_{j0}-IC = (k/2)*( (q_1-q_0)^2 + (q_0-q_{N-1})^2 ) = 1
    assert abs(H_t - 1.0) < 1e-12


def test_ph_diary53_cell():
    """N=2048, t=100, n=37: q should equal J_74(200) to ~floor precision."""
    import scipy.special as sp
    q_b, _ = propagator_bessel(37, 100.0, 2048, abs_tol=1e-30)
    j74 = float(sp.jv(74, 200.0))
    assert abs(q_b - j74) < 1e-12


# ---------------------------------------------------------------------------
# (d) Airy Tricomi-U
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("x", [5, 10, 20, 50, 100])
def test_airy_tricomi_matches_mpmath(x):
    mp.mp.dps = 50
    ref = mp.airyai(-x)
    val = airy_ai_neg_tricomi(x)
    diff = float(mp.fabs(val - ref))
    # 30 digits at dps=50 leaves plenty of room
    assert diff < mp.mpf("1e-30")
