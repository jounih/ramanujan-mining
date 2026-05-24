"""rkc.search.core — Project C protocols + dataclasses.

Per [insights/PROJECT_C_DESIGN.md](../../insights/PROJECT_C_DESIGN.md):
the search engine is instance-agnostic; per-instance plug-ins (Ramanujan
side / ARC side) implement the protocols below.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterator, Protocol, runtime_checkable


class RejectReason(str, Enum):
    """Per-instance reject taxonomy; new reasons are added as the
    proposer + verifier surface new failure modes. The names are
    machine-checkable; the per-instance descriptions live in the
    Registry's reject-log.
    """
    NOT_ENOUGH_DIGITS = "NOT_ENOUGH_DIGITS"          # verifier passed at low precision but failed at higher
    VERIFIER_FAILED = "VERIFIER_FAILED"              # numerical inequality at the target bar
    COST_NOT_IMPROVED = "COST_NOT_IMPROVED"          # transformation is correct but not faster
    ALREADY_IN_REGISTRY = "ALREADY_IN_REGISTRY"      # registry hash collision
    OPERATOR_DOMAIN_VIOLATION = "OPERATOR_DOMAIN_VIOLATION"  # operator applied outside its valid input class
    NUMERICAL_INSTABILITY = "NUMERICAL_INSTABILITY"  # cancellation / overflow / NaN
    TIMED_OUT = "TIMED_OUT"
    PROPOSER_DECLINED = "PROPOSER_DECLINED"          # proposer ran out of candidates
    DEGENERATE_ROUTE = "DEGENERATE_ROUTE"            # rkc router reported DEGENERATE on the result
    UNKNOWN = "UNKNOWN"


@dataclass
class SearchState:
    """Current state of a search step. Instance-specific payload.

    For the Ramanujan side: `payload` is a sympy Expr (the current
    expression), `metadata` carries the iteration variable + parameter
    bindings.

    For the ARC side (future): `payload` is the ARC frame state +
    rule-application history; `metadata` carries the task fingerprint.
    """
    payload: Any
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class OperatorApplication:
    """A proposed action. Per-instance op_id semantics.

    `op_id`: a string from the operator basis (e.g. "master_theorem",
    "mellin_inversion"; or for ARC: "gravity_down", "recolor_by_count").
    `params`: per-operator parameter dict.
    `confidence`: proposer's self-rating in [0, 1]. RandomProposer always
    uses 1.0 (no preference); NeuralProposer would use the softmax /
    likelihood from the model.
    """
    op_id: str
    params: dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0


@dataclass
class VerificationResult:
    """Outcome of the verifier step."""
    passed: bool
    digits_or_examples: int  # rkc: number of digits agreed; ARC: examples passed
    reason: str | None = None  # if not passed, the failure mode in human terms


@dataclass
class CostEstimate:
    """Outcome of the cost-model step."""
    direct_cost: float
    reduced_cost: float
    improvement_ratio: float = 1.0   # >1 means reduced is cheaper
    notes: str = ""


@dataclass
class SearchOutcome:
    """One full pass through the six-step loop. Stored in the registry
    on accept; logged in the reject-log on reject.
    """
    state_before: SearchState
    op_sequence: list[OperatorApplication]
    state_after: SearchState
    verification: VerificationResult
    cost: CostEstimate
    route: str                       # rkc Route.value, or per-instance route label
    accepted: bool
    reject_reason: RejectReason | None = None
    notes: str = ""


# ---------------------------------------------------------------------------
# Protocols (the per-instance plug-in interface)
# ---------------------------------------------------------------------------

@runtime_checkable
class Proposer(Protocol):
    """Propose the next operator application given current state."""

    def propose(self, state: SearchState, budget: int) -> Iterator[OperatorApplication]:
        """Yield candidate OperatorApplications, up to budget per call.

        The engine calls `propose(state, budget=1)` per step; the proposer
        can be stateless (RandomProposer) or stateful (NeuralProposer with
        a context-window).
        """
        ...


@runtime_checkable
class Verifier(Protocol):
    """Test whether applying op_sequence to state_before yields state_after
    correctly (per the per-instance correctness criterion)."""

    def verify(self, state_before: SearchState,
               op_sequence: list[OperatorApplication],
               state_after: SearchState) -> VerificationResult:
        ...


@runtime_checkable
class Router(Protocol):
    """Classify the state_after via the registry (rkc kernels / ARC rule
    fingerprints). Returns (route_label, payload_dict) where payload_dict
    carries route-specific info (e.g. kernel name, completion certificate,
    rejection reason)."""

    def route(self, state_after: SearchState) -> tuple[str, dict[str, Any]]:
        ...


@runtime_checkable
class CostModel(Protocol):
    """Score the transformation: cheaper than baseline?"""

    def cost(self, state_before: SearchState,
             state_after: SearchState) -> CostEstimate:
        ...


@runtime_checkable
class Registry(Protocol):
    """Persistent log of accepted identities + reject reasons."""

    def is_known(self, outcome: SearchOutcome) -> bool:
        """Has this transformation already been recorded?"""
        ...

    def store(self, outcome: SearchOutcome) -> str:
        """Record an accepted outcome; return a stable ID."""
        ...

    def reject(self, outcome: SearchOutcome, reason: RejectReason) -> None:
        """Record a rejected outcome with its named failure mode."""
        ...
