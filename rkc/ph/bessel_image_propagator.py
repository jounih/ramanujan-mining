"""Closed-form propagator for the periodic 1D spring-mass port-Hamiltonian chain.

System.  N masses arranged on a ring, each of mass m, coupled to nearest
neighbours by springs of stiffness k. The Hamiltonian is

    H = sum_i p_i^2 / (2 m) + (k/2) sum_i (q_{i+1} - q_i)^2 ,    indices mod N .

The equations of motion are
    q_i'   = p_i / m ,
    p_i'   = k (q_{i+1} - 2 q_i + q_{i-1}) .

This is a quadratic port-Hamiltonian system. We evolve from the unit-impulse
initial condition
    q_j(0) = delta_{j,0} ,    p_j(0) = 0 .

Exact closed-form (Bessel-image kernel).
    q_n(t) = sum_{l in Z} J_{2(n + l*N)}(2 c t) ,      c = sqrt(k / m) ,
    p_n(t) = sqrt(m*k) * sum_{l in Z}
             [ J_{2(n + l*N) - 1}(2 c t) - J_{2(n + l*N) + 1}(2 c t) ] .

For large N and modest 2*c*t, only the |2(n + l*N)| <= 2*c*t + O(...) terms are
above any given precision floor: the Bessel function J_nu(x) decays like
(x/2)^|nu| / |nu|! for |nu| >> x. So the aliased sum truncates to a small
number of nonzero terms (often just l = 0 for short t).

We also implement two baselines:

  - propagator_verlet : standard symplectic Verlet/leapfrog integrator (the
                        order-2 baseline; just used as a sanity check at
                        small N, t).
  - propagator_dft    : the modal (spectral) form

        q_n(t) = (1/N) * sum_{j=0}^{N-1} cos( omega_j * t ) * exp(2*pi*i*n*j/N)

    with omega_j = 2 c |sin(pi j / N)|. Exact for the linear system; serves as
    the fast exact baseline against which we benchmark the Bessel form.
"""
from __future__ import annotations

import math
from typing import Iterable, Optional

import mpmath as mp
import numpy as np
import scipy.special as sp


# ---------------------------------------------------------------------------
# Bessel-image closed form
# ---------------------------------------------------------------------------

def _bessel_truncation_radius(arg: float, abs_tol: float) -> int:
    """Find the smallest L such that |J_nu(arg)| < abs_tol for all |nu| >= L.

    Uses the elementary bound |J_nu(x)| <= (|x|/2)^|nu| / |nu|! valid for
    |nu| >= 0, which becomes very tight once |nu| > e * |x| / 2.
    """
    if abs_tol <= 0:
        raise ValueError("abs_tol must be positive")
    half_arg = abs(arg) / 2.0
    if half_arg == 0:
        return 1
    log_tol = math.log(abs_tol)
    # |J_nu(x)| <= (x/2)^nu / nu!  ==>  log bound = nu*log(half_arg) - lgamma(nu+1)
    nu = max(1, int(2 * half_arg) + 1)
    while True:
        log_bound = nu * math.log(half_arg) - math.lgamma(nu + 1)
        if log_bound < log_tol:
            return nu
        nu += 1
        if nu > 10000:  # safety
            return nu


def propagator_bessel(
    n: int,
    t: float,
    N: int,
    k: float = 1.0,
    m: float = 1.0,
    abs_tol: float = 1e-30,
    use_mpmath: bool = False,
):
    """Closed-form Bessel-image propagator: returns (q_n(t), p_n(t)).

    Parameters
    ----------
    n      : site index in [-N//2, N//2). Wrapped mod N.
    t      : time.
    N      : number of masses.
    k, m   : spring constant, mass.
    abs_tol: per-term cut-off for which images to keep.
    use_mpmath: if True, evaluate with mpmath.besselj (high precision); else
                scipy.special.jv (double precision).
    """
    c = math.sqrt(k / m)
    arg = 2.0 * c * t

    L = _bessel_truncation_radius(arg, abs_tol)

    # We need to enumerate all l in Z such that some required Bessel order
    #   nu in { 2(n + l*N), 2(n + l*N) - 1, 2(n + l*N) + 1 }
    # has |nu| <= L.  Equivalently, |n + l*N| <= (L+1)/2.
    n_eff = n % N  # base offset
    # Express n_eff in (-N/2, N/2] for nicer image enumeration
    if n_eff > N // 2:
        n_eff -= N
    max_l = max(1, int((L + 1) / 2 / N) + 1)
    images = range(-max_l, max_l + 1)

    if use_mpmath:
        besselj = mp.besselj
        q_acc = mp.mpf(0)
        p_acc = mp.mpf(0)
    else:
        besselj = sp.jv
        q_acc = 0.0
        p_acc = 0.0

    for ell in images:
        nu = 2 * (n_eff + ell * N)
        q_acc += besselj(nu, arg)
        p_acc += besselj(nu - 1, arg) - besselj(nu + 1, arg)

    if use_mpmath:
        p_acc = mp.sqrt(mp.mpf(m) * mp.mpf(k)) * p_acc
    else:
        p_acc = math.sqrt(m * k) * p_acc
    return q_acc, p_acc


# ---------------------------------------------------------------------------
# Exact DFT/modal baseline
# ---------------------------------------------------------------------------

def propagator_dft(
    t: float,
    N: int,
    k: float = 1.0,
    m: float = 1.0,
    return_sites: Optional[Iterable[int]] = None,
):
    """Modal (spectral) exact propagator: returns (q_all, p_all) at time t.

    For the unit-impulse initial condition q_j(0) = delta_{j,0}, p_j(0) = 0,
    the modal expansion gives
        q_n(t) = (1/N) * sum_{j=0}^{N-1} cos(omega_j t) * exp(2*pi*i*n*j/N)
        p_n(t) = -(m/N) * sum_{j=0}^{N-1} omega_j * sin(omega_j t) * exp(2*pi*i*n*j/N)
    with omega_j = 2*sqrt(k/m) * |sin(pi j / N)|.

    Returns real arrays (the imaginary parts vanish by symmetry up to fp error).
    If return_sites is given, returns only those sites; otherwise returns all.
    """
    c = math.sqrt(k / m)
    j = np.arange(N)
    omega = 2.0 * c * np.abs(np.sin(np.pi * j / N))
    # Use real DFT: q_n is the inverse DFT of cos(omega_j t).
    cos_omt = np.cos(omega * t)
    sin_omt = np.sin(omega * t)

    # q[n] = (1/N) sum_j cos_omt[j] * exp(2*pi*i*n*j/N) -- this is ifft.
    q_all = np.real(np.fft.ifft(cos_omt))   # ifft already divides by N
    # p[n] = -(m/N) sum_j omega_j * sin_omt[j] * exp(...)
    p_all = -m * np.real(np.fft.ifft(omega * sin_omt))

    if return_sites is None:
        return q_all, p_all
    sites = np.asarray(list(return_sites)) % N
    return q_all[sites], p_all[sites]


# ---------------------------------------------------------------------------
# Reference symplectic Verlet integrator (sanity check at small N, t)
# ---------------------------------------------------------------------------

def propagator_verlet(
    t: float,
    N: int,
    k: float = 1.0,
    m: float = 1.0,
    dt: Optional[float] = None,
):
    """Velocity-Verlet integration from impulse IC. Returns (q, p) at time t.

    The default step is dt = 0.01 / omega_max with omega_max = 2 * sqrt(k/m).
    This is a sanity check at small (N, t); convergence is O(dt^2).
    """
    c = math.sqrt(k / m)
    omega_max = 2.0 * c
    if dt is None:
        dt = 0.01 / omega_max

    n_steps = int(round(t / dt))
    dt = t / n_steps if n_steps > 0 else dt

    q = np.zeros(N)
    p = np.zeros(N)
    q[0] = 1.0  # unit impulse

    def force(q):
        # F_i = k * (q_{i+1} - 2 q_i + q_{i-1})
        return k * (np.roll(q, -1) - 2 * q + np.roll(q, 1))

    a = force(q) / m
    for _ in range(n_steps):
        # velocity Verlet
        v = p / m
        q_new = q + v * dt + 0.5 * a * dt * dt
        a_new = force(q_new) / m
        v_new = v + 0.5 * (a + a_new) * dt
        q, p, a = q_new, m * v_new, a_new

    return q, p


def chain_energy(q, p, k=1.0, m=1.0):
    """Hamiltonian H = sum p^2/(2m) + (k/2) sum (q_{i+1} - q_i)^2."""
    q = np.asarray(q)
    p = np.asarray(p)
    kinetic = float(np.sum(p * p) / (2.0 * m))
    diffs = np.roll(q, -1) - q
    potential = float(0.5 * k * np.sum(diffs * diffs))
    return kinetic + potential
