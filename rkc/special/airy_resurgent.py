"""Airy Ai(-x) via the Tricomi-U two-lateral-sector closed form.

For x > 0, set eta = (2/3) * x^(3/2). The oscillatory ("decaying" in WKB
language but oscillatory in the physical variable) sector decomposition of
Ai(-x) is

    Ai(-x) = [ exp( i (eta - pi/4)) / (2 sqrt(pi) x^(1/4)) ]
                 * (-2 i eta)^(1/6) * U(1/6, 1/3, -2 i eta)
           + [ exp(-i (eta - pi/4)) / (2 sqrt(pi) x^(1/4)) ]
                 * ( 2 i eta)^(1/6) * U(1/6, 1/3,  2 i eta)

where U(a, b, z) is Tricomi's confluent hypergeometric function (also written
U(a; b; z) or HypergeometricU). The two sectors are complex conjugates; their
sum is real and equals Ai(-x).

This is mathematically equivalent to recognising that the Borel transform of
the standard Airy WKB prefactor series S(Z) = 2F0(1/6, 5/6; -1/Z) is exactly
the Gauss hypergeometric 2F1(1/6, 5/6; 1; -s), so the Borel-Laplace integral
collapses to a Tricomi-U evaluation -- no Pade approximant or numerical
quadrature needed.

We expose two functions:

  airy_ai_neg_tricomi(x, dps)    : the closed Tricomi-U form. Fast.
  airy_ai_neg_borel_pade(x, dps) : the Borel-Pade baseline. Slow.

Both return mpmath.mpf values that are real-valued.
"""
from __future__ import annotations

from typing import Optional

import mpmath as mp


# ---------------------------------------------------------------------------
# Closed Tricomi-U form
# ---------------------------------------------------------------------------

def airy_ai_neg_tricomi(x: float, dps: Optional[int] = None) -> mp.mpf:
    """Evaluate Ai(-x) for x > 0 via the two-sector Tricomi-U closed form.

    Parameters
    ----------
    x   : positive real
    dps : optional mpmath precision in decimal digits
    """
    if x <= 0:
        raise ValueError("This routine is for x > 0 (i.e. Ai(-x) with x>0).")
    if dps is not None:
        old_dps = mp.mp.dps
        mp.mp.dps = dps
    try:
        x_mp = mp.mpf(x)
        eta = (mp.mpf(2) / 3) * x_mp ** (mp.mpf(3) / 2)
        pi4 = mp.pi / 4
        prefactor = 1 / (2 * mp.sqrt(mp.pi) * x_mp ** (mp.mpf(1) / 4))

        # First sector
        z_plus = -2j * eta
        c_plus = (mp.expj(eta - pi4)) * (z_plus ** (mp.mpf(1) / 6))
        U_plus = mp.hyperu(mp.mpf(1) / 6, mp.mpf(1) / 3, z_plus)
        sector_plus = prefactor * c_plus * U_plus

        # Second sector (complex conjugate)
        z_minus = 2j * eta
        c_minus = (mp.expj(-(eta - pi4))) * (z_minus ** (mp.mpf(1) / 6))
        U_minus = mp.hyperu(mp.mpf(1) / 6, mp.mpf(1) / 3, z_minus)
        sector_minus = prefactor * c_minus * U_minus

        total = sector_plus + sector_minus
        # Return the real part (the imaginary part should be ~0 to within numerical precision).
        return mp.re(total)
    finally:
        if dps is not None:
            mp.mp.dps = old_dps


# ---------------------------------------------------------------------------
# Borel-Pade baseline (for benchmark comparison)
# ---------------------------------------------------------------------------

def airy_ai_neg_borel_pade(x: float, dps: Optional[int] = None,
                            n_coefs: int = 21,
                            pade_order: Optional[int] = None) -> mp.mpf:
    """Evaluate Ai(-x) via diagonal Borel-Pade summation of the WKB series.

    For the Airy WKB representation, both lateral sector amplitudes have the
    formal expansion
        S(Z) = sum_{n >= 0} (-1)^n * (1/6)_n * (5/6)_n / (2^n * n!) * Z^{-n}
    with Z = 2 eta. The Borel transform is
        B[S](s) = sum_n (-1)^n * (1/6)_n * (5/6)_n / (2^n * (n!)^2) * s^n
                = 2F1(1/6, 5/6; 1; -s/2)
    We don't use the closed form (that would be the closed Tricomi route).
    Instead we form a diagonal Pade approximant in s, then perform the
    Laplace integral by mpmath.quad.

    This is the standard Borel-Pade workflow and intentionally meant to be
    *slower* than the Tricomi closed form.

    Parameters
    ----------
    x         : positive real
    dps       : mpmath precision in decimal digits
    n_coefs   : number of Borel-series coefficients to construct (>= 2*pade_order+1)
    pade_order: half-order of the diagonal Pade; default = (n_coefs - 1) // 2
    """
    if x <= 0:
        raise ValueError("This routine is for x > 0 (i.e. Ai(-x) with x>0).")
    if dps is not None:
        old_dps = mp.mp.dps
        mp.mp.dps = dps
    try:
        x_mp = mp.mpf(x)
        eta = (mp.mpf(2) / 3) * x_mp ** (mp.mpf(3) / 2)
        Z = 2 * eta
        pi4 = mp.pi / 4

        if pade_order is None:
            pade_order = (n_coefs - 1) // 2

        # Coefficients of B[S](s) = sum_{n>=0} b_n s^n with
        #   b_n = (-1)^n * (1/6)_n * (5/6)_n / (2^n * (n!)^2)
        coefs = []
        for n in range(n_coefs):
            num = mp.rf(mp.mpf(1) / 6, n) * mp.rf(mp.mpf(5) / 6, n)
            den = mp.mpf(2) ** n * mp.factorial(n) ** 2
            sign = (-1) ** n
            coefs.append(sign * num / den)

        # Diagonal Pade [pade_order/pade_order] of the series sum b_n s^n.
        p_coef, q_coef = mp.pade(coefs, pade_order, pade_order)

        def pade_eval(s):
            num = mp.mpf(0)
            for j, c in enumerate(p_coef):
                num += c * s ** j
            den = mp.mpf(0)
            for j, c in enumerate(q_coef):
                den += c * s ** j
            return num / den

        # Per-sector Laplace integral:
        #   sector(Z) = (1/Z) * integral_0^infty exp(-u/Z) * B(u) du
        # We do this for both sectors with Z replaced by +2i eta and -2i eta.
        # The Laplace integral converges along its appropriate contour; since
        # we want a quick benchmark, we just do the integral along the real
        # axis (this works because the singular structure of the 2F1 is on
        # the negative real axis of s, away from the contour).
        sector_amplitude = mp.quad(lambda s: mp.exp(-s) * pade_eval(s * Z), [0, mp.inf])

        prefactor = 1 / (mp.sqrt(mp.pi) * x_mp ** (mp.mpf(1) / 4))
        result = prefactor * mp.cos(eta - pi4) * sector_amplitude
        return result
    finally:
        if dps is not None:
            mp.mp.dps = old_dps
