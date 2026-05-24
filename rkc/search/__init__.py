"""rkc.search — Project C, the RKC-guided symbolic search system.

This is the v0.3.0 scaffold per [rkc/MILESTONES.md §v0.3](../MILESTONES.md)
and the design in [insights/PROJECT_C_DESIGN.md](../../insights/PROJECT_C_DESIGN.md).

Six-step loop:

  1. choose state               (input expression or current search node)
  2. proposer suggests action   (operator sequence)
  3. router normalises          (rkc.recognize + rkc.routing on the new state)
  4. verifier tests             (numerical equality to N digits)
  5. cost-model gate            (does the transformation improve over baseline?)
  6. registry update            (store accepted identity OR reject with named reason)

v0.3.0 (this commit) ships:
  - Core dataclasses + Protocols (SearchState, OperatorApplication,
    VerificationResult, CostEstimate, SearchOutcome, RejectReason)
  - RandomProposer (the v0 baseline)
  - MpmathVerifier (numerical-equality verifier using mpmath)
  - RkcRouter + RkcCostModel (wrap the existing rkc.recognize layer)
  - JsonlRegistry (accepted-identities log) + reject log

v0.3.1 will add NeuralProposer (per ChatGPT Pro suggestion: nonlinear ICA /
JEPA in latent operator space; see PROJECT_C_DESIGN.md §"v1").

v0.3.2 will extract the Proposer / Verifier / Router / CostModel / Registry
interfaces into a shared `compositional_search` package so arc-agi-ebm-agent
can plug in its ARC DSL as a second instance (X3 cross-repo).

Public API:

    from rkc.search import search, RandomProposer, MpmathVerifier, JsonlRegistry

    outcomes = search(
        initial_state=SearchState(payload=sympy_expr, metadata={'n': n}),
        proposer=RandomProposer(basis=QR7_OPERATOR_BASIS),
        verifier=MpmathVerifier(n_digits=40),
        router=RkcRouter(),
        cost_model=RkcCostModel(),
        registry=JsonlRegistry(path='accepted.jsonl'),
        budget=1000,
        max_depth=3,
    )
"""
from __future__ import annotations

from .core import (
    SearchState,
    OperatorApplication,
    VerificationResult,
    CostEstimate,
    SearchOutcome,
    RejectReason,
    Proposer,
    Verifier,
    Router,
    CostModel,
    Registry,
)
from .basis import QR7_OPERATOR_BASIS, Operator
from .proposers import RandomProposer
from .verifiers import MpmathVerifier
from .routers import RkcRouter, RkcCostModel
from .registries import JsonlRegistry
from .engine import search

__all__ = [
    # core types
    "SearchState", "OperatorApplication", "VerificationResult",
    "CostEstimate", "SearchOutcome", "RejectReason",
    # protocols
    "Proposer", "Verifier", "Router", "CostModel", "Registry",
    # operator basis
    "QR7_OPERATOR_BASIS", "Operator",
    # default implementations (the v0 baseline)
    "RandomProposer", "MpmathVerifier", "RkcRouter", "RkcCostModel",
    "JsonlRegistry",
    # the main loop
    "search",
]
