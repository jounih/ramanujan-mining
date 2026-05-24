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
    """The six-step Project C loop with multi-step composition.

    For each of `budget` proposer rounds:
      1. propose op (or, when max_depth > 1, an op sequence of length
         1..max_depth — the proposer can return single ops; the engine
         chains them by repeated proposer calls on intermediate states)
      2. apply op-sequence to initial_state → state_after (None if any
         intermediate apply declines)
      3. router classifies the final state_after
      4. verifier tests initial_state ↔ final state_after (single pass at
         the end; verifying intermediate states is expensive and usually
         redundant — if the FINAL state is numerically equal to the initial
         AND the sequence is valid, the intermediate equalities are implied)
      5. cost model estimates improvement_ratio over the WHOLE sequence
      6. registry.store on accept, registry.reject on reject (with named reason)

    v0.6 multi-step composition: at depth d, the engine takes the
    proposer's d operator suggestions and chains them. The proposer can be
    stateful (NeuralProposer with context window) or stateless
    (RandomProposer; just samples d ops independently). The op_sequence is
    stored as a list in the SearchOutcome.

    Multi-step rejections at intermediate steps don't count toward
    n_proposed (the proposer effectively "used" multiple op-suggestions
    for one search attempt, but only one search attempt happened).
    """
    if max_depth < 1:
        raise ValueError(f"max_depth must be ≥ 1, got {max_depth}")

    n_proposed = 0
    n_accepted = 0
    n_rejected = 0
    reject_counts: dict[str, int] = {}
    accepted_hashes: list[str] = []

    # For depth-1, one budget unit = one proposer call. For depth-N, we
    # use N proposer calls per search attempt. So total proposer calls =
    # budget * max_depth (approximately — proposer-declines short-circuit).
    if max_depth == 1:
        proposals = list(proposer.propose(initial_state, budget=budget))
        proposal_iter = iter(proposals)
        n_attempts = budget
    else:
        # multi-step: proposer is called repeatedly during each search attempt
        proposal_iter = None
        n_attempts = budget

    for _ in range(n_attempts):
        n_proposed += 1
        # Build the operator sequence + chained intermediate states
        op_sequence: list[OperatorApplication] = []
        cur_state = initial_state
        decline_hit = False
        for depth in range(max_depth):
            if max_depth == 1:
                op_app = next(proposal_iter, None)
                if op_app is None:
                    break
            else:
                # call proposer with the CURRENT state (lets stateful
                # proposers condition on intermediate context)
                gen = proposer.propose(cur_state, budget=1)
                op_app = next(gen, None)
                if op_app is None:
                    break
            next_state = _apply_operator(op_app, cur_state)
            if next_state is None:
                # this op declined — for multi-step, count the partial
                # sequence as a single proposer-decline if depth == 0,
                # or as a partial-sequence rejection if depth > 0
                if depth == 0:
                    decline_hit = True
                break
            op_sequence.append(op_app)
            cur_state = next_state

        # If the very first op declined, log PROPOSER_DECLINED
        if decline_hit or not op_sequence:
            outcome = SearchOutcome(
                state_before=initial_state,
                op_sequence=op_sequence,
                state_after=initial_state,
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

        state_after = cur_state

        # Step 3: router classifies the final state_after
        route_label, route_payload = router.route(state_after)

        # Step 4: verifier tests initial ↔ final (intermediate equalities are
        # implied transitively if each operator preserves value)
        verification = verifier.verify(initial_state, op_sequence, state_after)
        if not verification.passed:
            reject_reason = (RejectReason.NUMERICAL_INSTABILITY
                             if verification.reason and "NUMERICAL_INSTABILITY" in verification.reason
                             else RejectReason.VERIFIER_FAILED)
            outcome = SearchOutcome(
                state_before=initial_state, op_sequence=op_sequence,
                state_after=state_after, verification=verification,
                cost=CostEstimate(direct_cost=-1, reduced_cost=-1,
                                  improvement_ratio=0.0, notes="skipped — verifier failed"),
                route=route_label, accepted=False, reject_reason=reject_reason,
            )
            registry.reject(outcome, reject_reason)
            n_rejected += 1
            reject_counts[reject_reason.value] = reject_counts.get(reject_reason.value, 0) + 1
            continue

        # Step 5: cost model — initial vs final, NOT per-step. The cumulative
        # cost is what matters for acceptance: did the WHOLE sequence yield
        # a cheaper representation?
        cost = cost_model.cost(initial_state, state_after)

        # Compose preliminary outcome to check registry
        outcome = SearchOutcome(
            state_before=initial_state, op_sequence=op_sequence,
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
            op_chain = " → ".join(op.op_id for op in op_sequence)
            print(f"  ACCEPT: [{op_chain}] → {route_label} "
                  f"(ratio={cost.improvement_ratio:.2f}×, hash={h})")

    return SearchSummary(
        budget=budget,
        n_proposed=n_proposed,
        n_accepted=n_accepted,
        n_rejected=n_rejected,
        reject_reason_counts=reject_counts,
        accepted_hashes=accepted_hashes,
    )
