"""Unit tests for the Demkov-Kunike closed-form propagator.

These are fast regression guards on the correctness claims. The full
verification + benchmarking lives in analysis/39_*.
"""
from __future__ import annotations

import math

import mpmath as mp
import numpy as np
import pytest

from rkc.quantum.demkov_kunike import (
    demkov_kunike_propagator,
    demkov_kunike_magnus,
    dopri8_propagator,
    chi_of_t,
    z_of_t,
    hamiltonian,
)


PARAMS = dict(Delta=1.0, V=0.5, Omega=2.0, tau=1.0)
CELLS = [(-3.0, 3.0), (-2.2, -0.4), (-0.7, 1.6)]


def _unitarity(U):
    return float(np.linalg.norm(U.conj().T @ U - np.eye(2)))


# ---------------------------------------------------------------------------
# Specific claimed matrix values at (-3, +3)
# ---------------------------------------------------------------------------

CLAIMED_U_M3_P3 = np.array([
    [complex(-0.0941568365, +0.9057603680), complex(-0.2368006078, +0.3386120465)],
    [complex(+0.2368006078, +0.3386120465), complex(-0.0941568365, -0.9057603680)],
], dtype=np.complex128)


def test_matrix_value_at_minus_three_plus_three():
    """Closed-form U(3, -3) matches the published 10-digit values."""
    U = demkov_kunike_propagator(-3.0, 3.0, dps=40, **PARAMS)
    diff = float(np.max(np.abs(U - CLAIMED_U_M3_P3)))
    assert diff < 1e-9, f"matrix mismatch: max-abs-diff = {diff}"


# ---------------------------------------------------------------------------
# Cross-checks vs DOP853 at each cell
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("cell", CELLS)
def test_closed_form_matches_dop853(cell):
    T1, T2 = cell
    U_cf = demkov_kunike_propagator(T1, T2, dps=40, **PARAMS)
    U_dop = dopri8_propagator(T1, T2, rtol=1e-13, atol=1e-15, **PARAMS)
    diff = float(np.linalg.norm(U_cf - U_dop))
    assert diff < 1e-12, f"cell {cell}: ||cf - DOP853|| = {diff}"


# ---------------------------------------------------------------------------
# Unitarity
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("cell", CELLS)
def test_unitarity(cell):
    T1, T2 = cell
    U = demkov_kunike_propagator(T1, T2, dps=40, **PARAMS)
    assert _unitarity(U) < 1e-12


# ---------------------------------------------------------------------------
# Omega = 0 fallback
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("cell", CELLS)
def test_omega_zero_fallback(cell):
    T1, T2 = cell
    U_cf = demkov_kunike_propagator(T1, T2, Delta=1.0, V=0.5, Omega=0.0, tau=1.0, dps=40)
    chi_diff = chi_of_t(T2, 1.0, 0.5, 1.0) - chi_of_t(T1, 1.0, 0.5, 1.0)
    expected = np.diag([np.exp(-1j * chi_diff / 2), np.exp(+1j * chi_diff / 2)])
    diff = float(np.linalg.norm(U_cf - expected))
    assert diff < 1e-13


def test_omega_zero_off_diagonals_are_exactly_zero():
    U = demkov_kunike_propagator(-3.0, 3.0, Delta=1.0, V=0.5, Omega=0.0, tau=1.0, dps=40)
    assert abs(U[0, 1]) < 1e-30
    assert abs(U[1, 0]) < 1e-30


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def test_z_of_t_endpoints():
    assert abs(z_of_t(0.0, 1.0) - 0.5) < 1e-15
    assert z_of_t(100.0, 1.0) > 1.0 - 1e-15
    assert z_of_t(-100.0, 1.0) < 1e-15


def test_chi_of_t_zero():
    assert abs(chi_of_t(0.0, 1.0, 0.5, 1.0)) < 1e-15


def test_hamiltonian_hermiticity():
    for t in [-1.0, 0.0, 1.0, 2.5]:
        H = hamiltonian(t, **PARAMS)
        assert np.linalg.norm(H - H.conj().T) < 1e-15


def test_hamiltonian_at_large_t_diagonal_dominates():
    """At t -> +inf, tanh -> 1, sech -> 0, so H -> ((Delta+V)/2) sigma_z."""
    H = hamiltonian(50.0, **PARAMS)
    diag_expected = 0.5 * (1.0 + 0.5)
    assert abs(H[0, 0] - diag_expected) < 1e-15
    assert abs(H[1, 1] + diag_expected) < 1e-15
    assert abs(H[0, 1]) < 1e-15


# ---------------------------------------------------------------------------
# Magnus reference convergence (loose: just that it converges)
# ---------------------------------------------------------------------------

def test_magnus_self_consistency_converges():
    """Magnus error 32 -> 64 -> 128 should decrease."""
    T1, T2 = -3.0, 3.0
    U_cf = demkov_kunike_propagator(T1, T2, dps=40, **PARAMS)
    errs = []
    for N in [32, 64, 128]:
        U_mag = demkov_kunike_magnus(T1, T2, n_cells=N, order=6, **PARAMS)
        errs.append(np.linalg.norm(U_cf - U_mag))
    assert errs[1] < errs[0]
    assert errs[2] < errs[1]


def test_propagator_identity_at_T1_equals_T2():
    U = demkov_kunike_magnus(1.5, 1.5, n_cells=8, **PARAMS)
    assert np.linalg.norm(U - np.eye(2)) < 1e-15


# ---------------------------------------------------------------------------
# Composition: U(T_3, T_2) U(T_2, T_1) = U(T_3, T_1)
# ---------------------------------------------------------------------------

def test_composition_consistency():
    """For T_1 < T_2 < T_3, U(T_3, T_1) = U(T_3, T_2) U(T_2, T_1)."""
    T1, T2, T3 = -2.0, 0.5, 1.5
    U_31 = demkov_kunike_propagator(T1, T3, dps=40, **PARAMS)
    U_32 = demkov_kunike_propagator(T2, T3, dps=40, **PARAMS)
    U_21 = demkov_kunike_propagator(T1, T2, dps=40, **PARAMS)
    composed = U_32 @ U_21
    diff = np.linalg.norm(U_31 - composed)
    assert diff < 1e-10
