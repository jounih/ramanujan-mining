"""rkc.search.proposers — Proposer implementations for Project C.

v0 ships `RandomProposer` (the baseline). v0.3.1 adds `NeuralProposer`
once the basis size justifies it (per PROJECT_C_DESIGN.md §"v1": at
current basis size ~10, a categorical classifier suffices; nonlinear-ICA
/ JEPA framework becomes valuable at ~100s).
"""
from __future__ import annotations

import random
from typing import Iterator

from .core import OperatorApplication, Proposer, SearchState
from .basis import Operator, QR7_OPERATOR_BASIS


class RandomProposer:
    """Uniform-random sampling from the operator basis with no parameter
    learning. The v0 baseline; controls for proposer-quality so the
    rkc verifier+router+cost+registry pipeline (steps 3-6) can be
    evaluated independently.
    """

    def __init__(self, basis: list[Operator] | None = None, seed: int | None = None):
        self.basis = basis if basis is not None else QR7_OPERATOR_BASIS
        self._rng = random.Random(seed)

    def propose(self, state: SearchState, budget: int) -> Iterator[OperatorApplication]:
        """Yield up to `budget` candidate OperatorApplications uniformly at
        random. RandomProposer is stateless w.r.t. `state` — the search
        engine handles state evolution.
        """
        for _ in range(budget):
            op = self._rng.choice(self.basis)
            yield OperatorApplication(
                op_id=op.id,
                params={},  # v0: no parameter exploration
                confidence=1.0 / len(self.basis),  # uniform prior
            )

    def __repr__(self) -> str:
        return f"RandomProposer(basis={len(self.basis)} ops, seed={self._rng})"


# Sanity check the Proposer protocol is satisfied
assert isinstance(RandomProposer(), Proposer)
