"""rkc.attention — structured-attention accelerator prototypes.

Currently houses one accelerator:

  finite_pole : exact finite-pole semiseparable causal attention
                A_{ij} = 1_{j<=i} * sum_r q_{ir} k_{jr} alpha_r^(i-j),
                evaluated in O(N*R*d_v) by a per-pole recurrence
                instead of the naive O(N^2*d_v) outer-product form.
"""
from __future__ import annotations

from .finite_pole import (
    direct_finite_pole_attention,
    recurrent_finite_pole_attention,
)

__all__ = [
    "direct_finite_pole_attention",
    "recurrent_finite_pole_attention",
]
