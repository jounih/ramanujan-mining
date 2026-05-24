"""rkc.search.engine — the six-step Project C search loop.

The orchestration is instance-agnostic; per-instance plug-ins (Proposer,
Verifier, Router, CostModel, Registry) implement the protocols in
[core.py](core.py).

v0.3.0 implements single-step composition (max_depth=1 effectively). v0.4
will add multi-step composition (apply N operators in sequence before
verifying).
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from .basis import Operator, get_operator
from .core import (
    CostEstimate,
    OperatorApplication,
    RejectReason,
    Registry,
    Router,
    Proposer,
    SearchOutcome,
    SearchState,
    Verifier,
    VerificationResult,
    CostModel,
)


@dataclass
class SearchSummary:
    """Aggregate stats from a `search()` run."""
    budget: int
    n_proposed: int
    n_accepted: int
    n_rejected: int
    reject_reason_counts: dict[str, int]
    accepted_hashes: list[str]


def _apply_operator(op_app: OperatorApplication,
                    state: SearchState) -> SearchState | None:
    """Apply a single operator to a state via its basis apply_fn.

    Returns None if the operator doesn't apply (PROPOSER_DECLINED equivalent).
    """
    try:
        op = get_operator(op_app.op_id)
    except KeyError:
        return None
    var = state.metadata.get("var")
    if var is None:
        return None
    new_payload = op.apply_fn(state.payload, var)
    if new_payload is None:
        return None
    return SearchState(payload=new_payload, metadata=dict(state.metadata))


def search(initial_state: SearchState,
           proposer: Proposer,
           verifier: Verifier,
           router: Router,
           cost_model: CostModel,
           registry: Registry,
           budget: int = 1000,
           max_depth: int = 1,
           verbose: bool = False) -> SearchSummary:
    """The six-step Project C loop.

    v0.3.0 scope: single-step composition (max_depth=1). For each of `budget`
    proposer-emitted operator candidates:

      1. propose op
      2. apply op to initial_state → state_after (or None if op declines)
      3. router classifies state_after
      4. verifier tests state_before ↔ state_after
      5. cost model estimates improvement_ratio
      6. registry.store on accept, registry.reject on reject (with named reason)

    Returns a SearchSummary with the run's aggregate stats.
    """
    if max_depth != 1:
        raise NotImplementedError("v0.3.0 supports max_depth=1; multi-step "
                                  "composition deferred to v0.4")

    n_proposed = 0
    n_accepted = 0
    n_rejected = 0
    reject_counts: dict[str, int] = {}
    accepted_hashes: list[str] = []

    proposals = list(proposer.propose(initial_state, budget=budget))
    for op_app in proposals:
        n_proposed += 1
        # Step 2: apply the operator
        state_after = _apply_operator(op_app, initial_state)
        if state_after is None:
            # operator declined — log as PROPOSER_DECLINED for visibility
            outcome = SearchOutcome(
                state_before=initial_state,
                op_sequence=[op_app],
                state_after=initial_state,  # placeholder
                verification=VerificationResult(passed=False, digits_or_examples=0,
                                               reason="operator declined / not applicable"),
                cost=CostEstimate(direct_cost=-1, reduced_cost=-1,
                                  improvement_ratio=0.0, notes="not evaluated"),
                route="N/A",
                accepted=False,
                reject_reason=RejectReason.PROPOSER_DECLINED,
            )
            registry.reject(outcome, RejectReason.PROPOSER_DECLINED)
            n_rejected += 1
            reject_counts["PROPOSER_DECLINED"] = reject_counts.get("PROPOSER_DECLINED", 0) + 1
            continue

        # Step 3: router classifies
        route_label, route_payload = router.route(state_after)

        # Step 4: verifier tests
        verification = verifier.verify(initial_state, [op_app], state_after)
        if not verification.passed:
            reject_reason = (RejectReason.NUMERICAL_INSTABILITY
                             if verification.reason and "NUMERICAL_INSTABILITY" in verification.reason
                             else RejectReason.VERIFIER_FAILED)
            outcome = SearchOutcome(
                state_before=initial_state, op_sequence=[op_app],
                state_after=state_after, verification=verification,
                cost=CostEstimate(direct_cost=-1, reduced_cost=-1,
                                  improvement_ratio=0.0, notes="skipped — verifier failed"),
                route=route_label, accepted=False, reject_reason=reject_reason,
            )
            registry.reject(outcome, reject_reason)
            n_rejected += 1
            reject_counts[reject_reason.value] = reject_counts.get(reject_reason.value, 0) + 1
            continue

        # Step 5: cost model
        cost = cost_model.cost(initial_state, state_after)

        # Compose preliminary outcome to check registry
        outcome = SearchOutcome(
            state_before=initial_state, op_sequence=[op_app],
            state_after=state_after, verification=verification, cost=cost,
            route=route_label, accepted=False, reject_reason=None,
            notes=str(route_payload),
        )

        # Step 6a: dedup against registry
        if registry.is_known(outcome):
            registry.reject(outcome, RejectReason.ALREADY_IN_REGISTRY)
            n_rejected += 1
            reject_counts["ALREADY_IN_REGISTRY"] = reject_counts.get("ALREADY_IN_REGISTRY", 0) + 1
            continue

        # Step 6b: cost gate
        if cost.improvement_ratio < 1.0:
            outcome.reject_reason = RejectReason.COST_NOT_IMPROVED
            registry.reject(outcome, RejectReason.COST_NOT_IMPROVED)
            n_rejected += 1
            reject_counts["COST_NOT_IMPROVED"] = reject_counts.get("COST_NOT_IMPROVED", 0) + 1
            continue

        # Step 6c: route degeneracy
        if route_label == "DEGENERATE":
            outcome.reject_reason = RejectReason.DEGENERATE_ROUTE
            registry.reject(outcome, RejectReason.DEGENERATE_ROUTE)
            n_rejected += 1
            reject_counts["DEGENERATE_ROUTE"] = reject_counts.get("DEGENERATE_ROUTE", 0) + 1
            continue

        # All gates passed — store
        outcome.accepted = True
        h = registry.store(outcome)
        accepted_hashes.append(h)
        n_accepted += 1
        if verbose:
            print(f"  ACCEPT: {op_app.op_id} → {route_label} "
                  f"(ratio={cost.improvement_ratio:.2f}×, hash={h})")

    return SearchSummary(
        budget=budget,
        n_proposed=n_proposed,
        n_accepted=n_accepted,
        n_rejected=n_rejected,
        reject_reason_counts=reject_counts,
        accepted_hashes=accepted_hashes,
    )
