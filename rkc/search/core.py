"""rkc.search.core — Project C protocols + dataclasses.

Per [insights/PROJECT_C_DESIGN.md](../../insights/PROJECT_C_DESIGN.md):
the search engine is instance-agnostic; per-instance plug-ins (Ramanujan
side / ARC side) implement the protocols below.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterator, Optional, Protocol, runtime_checkable

import sympy as sp


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


class ConvergenceClass(str, Enum):
    """v0.9a (Project C v0.9-hardy): divergence-diagnostic classification
    emitted by `hardy_orders_of_infinity`.

    The operator is a NON-TRANSFORMING annotator — it leaves the summand
    expression alone but tags the state with the asymptotic behaviour of
    the summand as n → ∞. Downstream proposers (and the verifier) can use
    this tag to decide whether the literal `Σ_n payload(n)` makes sense
    at all, and which routing strategy is appropriate.

    Values:

    - **CONVERGENT** — summand → 0 as n → ∞. The series may or may not
      converge in absolute value (alternating series with slow decay can
      still sum), but the necessary condition for absolute convergence is
      met. v0.9a does not attempt a finer speed-of-convergence split.

    - **DIVERGENT_LITERAL** — summand → c ≠ 0 (finite) as n → ∞. The
      literal sum cannot converge; downstream proposers MUST transform
      before any numerical comparison. Motivating example:
      `1/(1 - exp(-βn)) → 1` as n → ∞.

    - **NEEDS_REGULARIZATION** — summand → ∞ as n → ∞. The literal sum
      diverges to infinity; an Abel / zeta-regularization or a modular
      transformation is required before sums make sense. Examples: `n`,
      `n²`, `log(n)`, `n^s` for s > 0.

    - **UNKNOWN** — sympy's `limit` raised, returned an AccumulationBounds
      (oscillatory), or otherwise didn't yield a classifiable value. The
      proposer should treat this as a "no information" signal and not
      special-case routing on it.

    Tag location: emitted into `SearchState.metadata['convergence_class']`
    (string-valued) and mirrored to the top-level
    `SearchState.convergence_class` field for direct access. The
    JsonlRegistry persists it via the existing `state_after_meta` /
    `state_before_meta` JSONL fields, so audit trails survive.
    """
    CONVERGENT = "CONVERGENT"
    DIVERGENT_LITERAL = "DIVERGENT_LITERAL"
    NEEDS_REGULARIZATION = "NEEDS_REGULARIZATION"
    UNKNOWN = "UNKNOWN"


@dataclass
class SearchState:
    """Current state of a search step. Instance-specific payload.

    For the Ramanujan side: `payload` is a sympy Expr (the current
    expression), `metadata` carries the iteration variable + parameter
    bindings.

    For the ARC side (future): `payload` is the ARC frame state +
    rule-application history; `metadata` carries the task fingerprint.

    v0.9a extension (Project C v0.9-hardy): `convergence_class` is a
    top-level field carrying the asymptotic-behaviour classification of
    the summand `payload` as the iteration variable → ∞. It is populated
    by `hardy_orders_of_infinity`'s apply_fn (a NON-TRANSFORMING
    annotator) and mirrored from `metadata['convergence_class']`. Default
    is None — un-classified states are simply "we haven't asked yet".

    The classification values are the `ConvergenceClass` enum:
    `CONVERGENT` (summand → 0), `DIVERGENT_LITERAL` (summand → c ≠ 0,
    finite), `NEEDS_REGULARIZATION` (summand → ∞), `UNKNOWN` (couldn't
    classify in one pass). The string value is stored for JSONL-
    serialization friendliness.

    The convergence_class field is the LOAD-BEARING addition for v0.9a:
    downstream proposers (notably ClaudeProposer in v0.9b) can read it
    off the state and refuse to chain operators that don't make sense
    for divergent summands (e.g. don't try strict Poisson on a
    DIVERGENT_LITERAL state).
    """
    payload: Any
    metadata: dict[str, Any] = field(default_factory=dict)
    convergence_class: Optional[str] = None


@dataclass
class OperatorApplication:
    """A proposed action. Per-instance op_id semantics.

    `op_id`: a string from the operator basis (e.g. "master_theorem",
    "mellin_inversion"; or for ARC: "gravity_down", "recolor_by_count").
    `params`: per-operator parameter dict.
    `confidence`: proposer's self-rating in [0, 1]. RandomProposer always
    uses 1.0 (no preference); NeuralProposer would use the softmax /
    likelihood from the model.

    v0.8b extensions for one-sided modular transformations with additive
    scalar correction terms (Bose-Einstein eta-log, Lambert / E_2
    quasi-modular). These are OPT-IN — operators that don't set them
    preserve v0.7 strict-Poisson semantics exactly.

    `additive_correction`: a scalar sympy expression with NO dependence
    on the iteration variable, such that
        Σ_n state_before_summand  ≡  Σ_n state_after_summand + additive_correction
    where the equality is across the operator's `summand_range`. When
    multiple operators chain in an op_sequence, the verifier sums their
    additive_correction fields. Defaults to None for backward compat
    (v0.4, v0.7 strict Poisson identities don't use it — their
    transformations are clean term-by-term equalities).

    `summand_range`: a (lower, upper) tuple identifying the index range
    over which the sums in the modular identity are taken. The v0.4 /
    v0.7 strict-Poisson identities run over Z (i.e., (-oo, oo) — set None
    to inherit the verifier's default symmetric range). The v0.8b one-
    sided modular transforms run over positive n only ((1, oo)). When
    multiple operators chain, the verifier requires their summand_range
    fields to be consistent — operators with different ranges cannot mix.

    Why both fields live on OperatorApplication (and not on the basis
    entry / Operator): the same operator id can in principle produce
    different additive corrections for different inputs (e.g. an operator
    that handles BOTH the Bose-Einstein eta-log AND the Lambert / E_2
    case would emit different corrections per input). Carrying these on
    the per-application record keeps the data model honest: each emitted
    application IS a complete identity instance, additive correction +
    summand range included.
    """
    op_id: str
    params: dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    additive_correction: Optional[sp.Expr] = None
    summand_range: Optional[tuple] = None


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
