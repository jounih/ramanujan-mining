"""Annular Poisson Green's function via separated Fourier series and via
the modular one-image kernel.

The BVP. The 2D Dirichlet Laplacian on the annulus  A_L = { e^{-L} < |z| < 1 },
with zero boundary conditions on both circles. Using the logarithmic polar
coordinate y = log(r) + L in (0, L) and angular variable theta in [0, 2*pi),
the Laplacian becomes 1/(e^{2(y-L)}) * (d^2/dtheta^2 + d^2/dy^2) and the
"radial" Green function on the rectangle [0, 2pi) x [0, L] with periodic
boundary conditions in theta and Dirichlet in y is what we compute.

Slow form  (separated Fourier series).

    G_L(theta, y; phi, eta) =
        (1/(2*pi)) * [ y_<(L - y_>)/L
                      + 2 * sum_{m=1}^M cos(m*delta) * sinh(m*y_<) * sinh(m*(L - y_>))
                                       / (m * sinh(m*L)) ]

    where delta = theta - phi, y_< = min(y, eta), y_> = max(y, eta).

For L << 1 and a query close to the source, sinh(m*L) ~ m*L, sinh(m*y_<) ~ m*y_<
and sinh(m*(L-y_>)) ~ m*(L-y_>) for m up to ~ 1/L, so the series decays only
geometrically with ratio e^{-min(y_<, L-y_>)} after that, which makes truncation
extremely slow.

Fast form  (modular S-transform one-image kernel).

    G_L(theta, y; phi, eta) ~
        (1/(4*pi)) * log[ (cosh(pi*delta/L) - cos(pi*(y+eta)/L))
                        / (cosh(pi*delta/L) - cos(pi*(y-eta)/L)) ]

This is the n = 0 image of the Poisson-summed theta-quotient form of the same
Green function under tau = i*L/pi -> -1/tau. For thin annulus L << 1 the
first omitted image lives at scale exp(-pi*(2*pi - delta)/L), so a single
term already exceeds 30-digit precision.

We use mpmath throughout to be able to push to 80+ dps in the benchmark.
"""
from __future__ import annotations

import math
from typing import Optional

import mpmath as mp


def annular_green_fourier(
    theta: float,
    y: float,
    phi: float,
    eta: float,
    L: float,
    M: int = 100,
    dps: Optional[int] = None,
) -> mp.mpf:
    """Slow form -- separated Fourier series truncated at M modes.

    Parameters
    ----------
    theta, y : query point (theta in [0, 2*pi), y in (0, L))
    phi, eta : source point
    L        : annulus thickness
    M        : number of Fourier modes (more = more accurate, more time)
    dps      : optional mpmath precision in decimal digits (preserves caller's
               default if None)
    """
    if dps is not None:
        old_dps = mp.mp.dps
        mp.mp.dps = dps
    try:
        Lm = mp.mpf(L)
        delta = mp.mpf(theta) - mp.mpf(phi)
        ym = mp.mpf(y)
        em = mp.mpf(eta)
        if ym <= em:
            y_lo, y_hi = ym, em
        else:
            y_lo, y_hi = em, ym

        # zero-mode (linear ramp)
        out = y_lo * (Lm - y_hi) / Lm

        # higher modes: each term cos(m*delta)*sinh(m*y_<)*sinh(m*(L-y_>))/(m*sinh(m*L))
        for m in range(1, M + 1):
            mm = mp.mpf(m)
            sh_lo = mp.sinh(mm * y_lo)
            sh_hi = mp.sinh(mm * (Lm - y_hi))
            sh_L = mp.sinh(mm * Lm)
            term = 2 * mp.cos(mm * delta) * sh_lo * sh_hi / (mm * sh_L)
            out += term

        return out / (2 * mp.pi)
    finally:
        if dps is not None:
            mp.mp.dps = old_dps


def annular_green_modular(
    theta: float,
    y: float,
    phi: float,
    eta: float,
    L: float,
    dps: Optional[int] = None,
) -> mp.mpf:
    """Fast form -- modular one-image closed kernel.

    Approximation error is bounded by exp(-pi*(2*pi - |delta|)/L) per omitted
    image, so for L << 1 and modest |delta| this is far below double precision.
    """
    if dps is not None:
        old_dps = mp.mp.dps
        mp.mp.dps = dps
    try:
        Lm = mp.mpf(L)
        delta = mp.mpf(theta) - mp.mpf(phi)
        ym = mp.mpf(y)
        em = mp.mpf(eta)

        a = mp.cosh(mp.pi * delta / Lm)
        c_plus = mp.cos(mp.pi * (ym + em) / Lm)
        c_minus = mp.cos(mp.pi * (ym - em) / Lm)

        num = a - c_plus
        den = a - c_minus
        return mp.log(num / den) / (4 * mp.pi)
    finally:
        if dps is not None:
            mp.mp.dps = old_dps
