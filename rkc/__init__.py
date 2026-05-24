"""rkc — Ramanujan Kernel Compiler / Recognizer package.

Standalone package wrapping the v2 kernel-fingerprint recognizer. Given a
symbolic AST for a sum or product, route it to direct evaluation vs a
closed-form / dual representation, using a registry of canonical kernels
(theta, mock theta, Lambert, Eisenstein, partial theta, q-Pochhammer,
Dirichlet L, Gauss sum).

Public API:

    from rkc import recognize, best_match, recognize_composite, Route, KernelFamily

    bm = best_match(expr_summand, n_symbol)
    if bm is not None:
        print(bm.kernel, bm.route, bm.total_cost)

See README.md for the kernel list and the silent-zero hazard note (§A4).
"""
from __future__ import annotations

from .recognizer import (
    recognize,
    best_match,
    recognize_composite,
    recognize_with_raw_string,
)
from .routing import Route, KernelFamily, RoutingResult
from .registry import REGISTRY, FUZZY_MATCHERS
from .completions import (
    compute_mock_theta_with_completion,
    CompletionNotImplemented,
    CompletionResult,
    CompletionCertificate,
    supported_families,
    coverage_report,
)

__all__ = [
    "recognize",
    "best_match",
    "recognize_composite",
    "recognize_with_raw_string",
    "Route",
    "KernelFamily",
    "RoutingResult",
    "REGISTRY",
    "FUZZY_MATCHERS",
    "compute_mock_theta_with_completion",
    "CompletionNotImplemented",
    "CompletionResult",
    "CompletionCertificate",
    "supported_families",
    "coverage_report",
]

__version__ = "0.3.0"
