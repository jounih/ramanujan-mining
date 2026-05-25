"""rkc.ph -- port-Hamiltonian Bessel-image propagator accelerators.

Currently houses one accelerator:

  bessel_image_propagator : closed-form propagator for the periodic 1D
                            spring-mass chain (a quadratic port-Hamiltonian
                            system), evaluated as an aliased sum of Bessel
                            functions. Cost is O(1) per (n, t) query for
                            large N, instead of O(N) for direct DFT.
"""
from __future__ import annotations

from .bessel_image_propagator import (
    propagator_bessel,
    propagator_verlet,
    propagator_dft,
    chain_energy,
)

__all__ = [
    "propagator_bessel",
    "propagator_verlet",
    "propagator_dft",
    "chain_energy",
]
