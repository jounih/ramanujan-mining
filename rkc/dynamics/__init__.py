"""rkc.dynamics -- dynamical-systems primitives and benchmarks.

Currently houses:

  brusselator_cousin : Lambert-W conservative-cousin of the Brusselator
                       u'' + 1 - 1/u = 0 with Hamiltonian
                           E = (1/2)(u')^2 + u - log u
                       and one-quadrature period formula
                           T_0(E) = sqrt(2) * int_{u_-}^{u_+} du/sqrt(E-u+log u)
                       where the turning points solve u - log u = E and have
                       explicit Lambert-W form:
                           u_-(E) = -W_0(-e^{-E})
                           u_+(E) = -W_{-1}(-e^{-E})
"""
from __future__ import annotations

from .brusselator_cousin import (
    turning_points,
    period_cousin,
    period_cousin_ode,
    hamiltonian,
)

__all__ = [
    "turning_points",
    "period_cousin",
    "period_cousin_ode",
    "hamiltonian",
]
