"""rkc.special -- special-function accelerators.

Currently houses:

  airy_resurgent : Closed-form evaluator for Ai(-x) at x > 0 via the
                   Borel-summed two-lateral-sector representation
                   Ai(-x) = ... U(1/6, 1/3, -2i*eta) + c.c.
                   where eta = (2/3)*x^(3/2). The trick is that the WKB
                   asymptotic series's Borel transform IS Tricomi's U
                   (a known special function), so the Borel-Pade machinery
                   collapses to a single special-function call per lateral
                   sector.
"""
from __future__ import annotations

from .airy_resurgent import (
    airy_ai_neg_tricomi,
    airy_ai_neg_borel_pade,
)

__all__ = [
    "airy_ai_neg_tricomi",
    "airy_ai_neg_borel_pade",
]
