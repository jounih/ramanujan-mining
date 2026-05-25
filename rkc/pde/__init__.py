"""rkc.pde — modular-S-transform-based Green-function accelerators.

Currently houses one accelerator:

  annular_green : Green's function for the 2D Dirichlet Poisson problem
                  on a thin annulus, evaluated via either the standard
                  separated-Fourier series (slow when L is small) or the
                  closed-form modular one-image kernel (fast when L is
                  small).
"""
from __future__ import annotations

from .annular_green import (
    annular_green_fourier,
    annular_green_modular,
)

__all__ = [
    "annular_green_fourier",
    "annular_green_modular",
]
