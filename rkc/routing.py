"""rkc.routing — routing-decision primitives.

Five route states (v2 adds FUZZY to v1's four):

  DIRECT                        — converges fast as written, use the summand.
  DUAL                          — exact closed-form / modular transform exists;
                                  cheaper than direct.
  MODULAR_COMPLETION_REQUIRED   — no clean dual; non-holomorphic Eichler
                                  integral needed to repair modular behavior.
                                  (Mock theta family.)
  DEGENERATE                    — kernel evaluates to a trivial value (zero,
                                  infinity) for the given parameters; do NOT
                                  report a numerical recommendation — the
                                  answer is the trivial value.
  FUZZY                         — soft second-pass match: the AST looks like a
                                  member of a known kernel FAMILY but fails the
                                  strict matcher. Emits a confidence-tagged
                                  warning rather than a strict null.

A `RoutingResult` packages everything a downstream routing planner needs:
the route, both cost estimates, the dominant per-term cost, the total cost,
the chosen kernel family, the parameter dict, an optional `reason` string,
and a `confidence` in [0, 1] (always 1.0 for strict matches; <1.0 for FUZZY).
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Optional


class Route(str, Enum):
    DIRECT = "DIRECT"
    DUAL = "DUAL"
    MODULAR_COMPLETION_REQUIRED = "MODULAR_COMPLETION_REQUIRED"
    DEGENERATE = "DEGENERATE"
    FUZZY = "FUZZY"


class KernelFamily(str, Enum):
    """Coarse 'shape category' for the fuzzy second-pass matcher.

    The strict matcher returns a kernel NAME (e.g. 'gaussian_quadratic').
    The fuzzy matcher returns a kernel FAMILY (e.g. THETA_LIKE) — i.e. it
    says 'this is theta-shaped' without committing to a specific registry
    entry. The fuzzy result is meant to surface mock-theta-ish or
    shifted-theta-ish forms that the strict matcher rejects.
    """
    THETA_LIKE = "theta-like"              # q^(quadratic in n); incl. shifted/offset
    MOCK_THETA_LIKE = "mock-theta-like"    # q^(quadratic) / Pochhammer-shape denom
    LAMBERT_LIKE = "lambert-like"          # q^n / (1 - q^(linear)) style
    PARTIAL_THETA_LIKE = "partial-theta-like"  # triangular exponent w/ extra factor
    EISENSTEIN_LIKE = "eisenstein-like"    # arithmetic-function coefficient * q^n
    POCHHAMMER_LIKE = "pochhammer-like"    # Π(1 - ... q^k)
    GAUSS_SUM_LIKE = "gauss-sum-like"      # exp(i * rational * n^2)
    UNKNOWN = "unknown"


@dataclass
class RoutingResult:
    """One recognizer result — strict or fuzzy.

    `kernel` is the registry name for strict matches, or the family enum
    value string for fuzzy matches. `confidence` is 1.0 for strict matches
    and <1.0 for fuzzy matches (currently a hand-tuned constant per family).

    `per_term_cost` is approximate big-int / mpmath ops per term (insight §A7).
    `total_cost = num_terms * per_term_cost` for the chosen route.
    """
    kernel: str
    family: str                 # one of KernelFamily values
    route: Route
    params: dict[str, Any]
    num_terms: int = -1         # -1 sentinel = unknown / N/A
    per_term_cost: float = -1.0
    total_cost: float = -1.0
    cost_direct: int = -1
    cost_dual: int = -1
    degenerate: Optional[str] = None
    reason: Optional[str] = None
    confidence: float = 1.0
    notes: str = ""
    # for composites: per-component breakdown
    components: list[dict] = field(default_factory=list)
    scalar_coefficient: Any = 1   # the outer scalar that was peeled off
    # opt-in numerical completion for MODULAR_COMPLETION_REQUIRED route.
    # Populated by `recognize(..., numerical_completion=True)` when the
    # route handler succeeds; remains None for the default flag-only path.
    completion: Optional[Any] = None
    completion_error: Optional[str] = None

    def to_dict(self) -> dict:
        # asdict() can't introspect arbitrary dataclasses from another module
        # (it would deep-copy mpf values opaquely); we serialize manually.
        d = {
            "kernel": self.kernel,
            "family": self.family,
            "route": self.route.value,
            "params": {k: str(v) for k, v in self.params.items()},
            "num_terms": self.num_terms,
            "per_term_cost": self.per_term_cost,
            "total_cost": self.total_cost,
            "cost_direct": self.cost_direct,
            "cost_dual": self.cost_dual,
            "degenerate": self.degenerate,
            "reason": self.reason,
            "confidence": self.confidence,
            "notes": self.notes,
            "components": list(self.components),
            "scalar_coefficient": str(self.scalar_coefficient),
            "completion_error": self.completion_error,
        }
        if self.completion is not None:
            comp = self.completion
            d["completion"] = {
                "value": str(comp.value),
                "error_bound": comp.error_bound,
                "certificate": {
                    "family": comp.certificate.family,
                    "method": comp.certificate.method,
                    "source": comp.certificate.source,
                    "alpha": comp.certificate.alpha,
                    "beta_dual": comp.certificate.beta_dual,
                    "working_dps": comp.certificate.working_dps,
                    "modular_residual": comp.certificate.modular_residual,
                    "shadow_eichler_integral": comp.certificate.shadow_eichler_integral,
                    "modular_term": comp.certificate.modular_term,
                    "regime": comp.certificate.regime,
                    "confidence": comp.certificate.confidence,
                    "notes": comp.certificate.notes,
                    "extras": comp.certificate.extras,
                },
            }
        else:
            d["completion"] = None
        return d


# convenience constructors used by the recognizer

def degenerate_result(kernel: str, family: str, params: dict, reason: str,
                      notes: str = "") -> RoutingResult:
    return RoutingResult(
        kernel=kernel, family=family, route=Route.DEGENERATE,
        params=params, degenerate=reason, reason=reason, notes=notes,
        confidence=1.0,
    )


def fuzzy_result(family: KernelFamily, params: dict, reason: str,
                 confidence: float = 0.5, notes: str = "") -> RoutingResult:
    """A soft-match result: not a strict kernel hit but family-shaped."""
    return RoutingResult(
        kernel=family.value, family=family.value, route=Route.FUZZY,
        params=params, reason=reason, confidence=confidence, notes=notes,
    )
