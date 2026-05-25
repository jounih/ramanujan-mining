"""rkc.quantum -- closed-form propagators for solvable two-state quantum systems.

Currently houses one accelerator:

  demkov_kunike : closed-form propagator U(T_2, T_1) for the Demkov-Kunike
                  level-crossing Hamiltonian
                      H(t) = (1/2)[Delta + V * tanh(t/tau)] sigma_z
                             + (Omega/2) * sech(t/tau) * sigma_x
                  expressed in terms of Gauss hypergeometric functions
                  evaluated at z(t) = (1 + tanh(t/tau))/2. O(1) per propagator
                  evaluation (one pair of 2F1 calls), independent of T_2 - T_1.
"""
from __future__ import annotations

from .demkov_kunike import (
    demkov_kunike_propagator,
    demkov_kunike_propagator_mp,
    demkov_kunike_magnus,
    magnus_step_order8,
    chi_of_t,
    z_of_t,
    M_matrix,
)

__all__ = [
    "demkov_kunike_propagator",
    "demkov_kunike_propagator_mp",
    "demkov_kunike_magnus",
    "magnus_step_order8",
    "chi_of_t",
    "z_of_t",
    "M_matrix",
]
