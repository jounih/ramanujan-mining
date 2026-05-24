"""25_in_session_claude_proposer_demo.py — Demonstrate "Claude as proposer"
without an API key, by routing decisions through the host Claude Code session.

Per v0.8a subagent's architectural follow-up #1 + user clarification
("you ARE Claude, why need API key?"), the cleanest in-conversation form
is: the engine emits its proposer prompt to a file; the host LLM (this
session) reads the prompt, decides, writes the answer to another file;
the engine reads and continues. No subprocess, no API key, no token cost.

This script demonstrates ONE STEP of that loop on the canonical v0.4
Gaussian Poisson test seed. The full integration would extend
proposers.py with `InSessionClaudeProposer` reading from a designated
inbox/outbox; this demo is the proof of concept.

Run modes:
  --print-prompt    : print the system+user prompt and the proposer-decision schema, exit
  --apply OP_ID     : pretend the host LLM picked OP_ID; run one engine
                      step and report whether it accepted
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

import sympy as sp

from rkc.search import (
    SearchState, RandomProposer, MpmathVerifier,
    RkcRouter, RkcCostModel, JsonlRegistry, search,
)
from rkc.search.basis import QR7_OPERATOR_BASIS, get_operator
from rkc.search.core import OperatorApplication
from rkc.search.proposers import ClaudeProposer


@dataclass
class FixedChoiceProposer:
    """Proposer that returns a hardcoded operator id on first call,
    then defers to RandomProposer for subsequent calls. Used to inject
    the host LLM's decision into the engine for one step.
    """
    op_id: str
    basis: list = field(default_factory=lambda: list(QR7_OPERATOR_BASIS))
    seed: int | None = 0

    def __post_init__(self):
        self._consumed = False
        self._fallback = RandomProposer(basis=self.basis, seed=self.seed)

    def propose(self, state, **kwargs):
        """Returns an iterable of OperatorApplication (matching the engine's
        Proposer protocol — RandomProposer returns a list of up to `budget`)."""
        if not self._consumed:
            self._consumed = True
            yield OperatorApplication(op_id=self.op_id, params={})
        else:
            for app in self._fallback.propose(state, **kwargs):
                yield app


def make_seed_state():
    """The canonical v0.4 test seed: Gaussian summand exp(-β·n²) at β=1/100."""
    n = sp.Symbol("n", integer=True, positive=True)
    expr = sp.exp(-sp.Rational(1, 100) * n**2)
    return SearchState(payload=expr, metadata={"var": n}), n


def build_prompt(state, n):
    """Build the same kind of prompt the API-based ClaudeProposer would
    send. Mirrors ClaudeProposer's prompt construction so a host LLM can
    answer in the same shape.

    NB: ClaudeProposer's internal helpers may evolve; this taps the
    public `_system_prompt` attribute and rebuilds a user prompt that
    matches what `propose()` would send.
    """
    proposer = ClaudeProposer(basis=list(QR7_OPERATOR_BASIS))
    sys_prompt = proposer._system_prompt()
    # User prompt: mirror what propose() sends (current expression + brief)
    var = state.metadata.get("var")
    expr_str = sp.sstr(state.payload)
    user_prompt = (
        f"Current state expression: {expr_str}\n"
        f"Iteration variable: {var}\n"
        f"\nWhich operator from the basis should I apply next? "
        f"Respond with a JSON object: "
        f'{{"op_id": "...", "reasoning": "one-line why"}}'
    )
    return sys_prompt, user_prompt


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--print-prompt", action="store_true",
                   help="Print the system+user prompt the engine would send to the proposer.")
    p.add_argument("--apply", type=str,
                   help="Inject this op_id as the proposer's first-call answer; "
                        "run one engine step.")
    args = p.parse_args()

    state, n = make_seed_state()

    if args.print_prompt:
        sys_prompt, user_prompt = build_prompt(state, n)
        print("=" * 70)
        print("SYSTEM PROMPT (what the engine would send to Claude as proposer):")
        print("=" * 70)
        print(sys_prompt)
        print()
        print("=" * 70)
        print("USER PROMPT (per-state):")
        print("=" * 70)
        print(user_prompt)
        print()
        print("=" * 70)
        print("EXPECTED RESPONSE SCHEMA:")
        print("=" * 70)
        print('A JSON object like: {"op_id": "mellin_inversion", "reasoning": "..."}')
        return 0

    if args.apply:
        op_id = args.apply
        if op_id not in {op.id for op in QR7_OPERATOR_BASIS}:
            print(f"ERROR: {op_id!r} not in basis. Choices: "
                  f"{[op.id for op in QR7_OPERATOR_BASIS]}", file=sys.stderr)
            return 2
        # Run one engine step with the host LLM's answer
        out_dir = Path("analysis/results/25_in_session_demo")
        out_dir.mkdir(parents=True, exist_ok=True)
        registry = JsonlRegistry.with_dir(out_dir)
        proposer = FixedChoiceProposer(op_id=op_id)
        summary = search(
            initial_state=state,
            proposer=proposer,
            verifier=MpmathVerifier(n_digits=10),
            router=RkcRouter(),
            cost_model=RkcCostModel(),
            registry=registry,
            budget=1,           # ONE step — that's the point of "in-session" pattern
            max_depth=1,
            verbose=True,
        )
        print()
        print("=" * 70)
        print(f"RESULT: budget=1, proposer picked {op_id}")
        print("=" * 70)
        print(f"  n_proposed:  {summary.n_proposed}")
        print(f"  n_accepted:  {summary.n_accepted}")
        print(f"  n_rejected:  {summary.n_rejected}")
        if summary.accepted_hashes:
            print(f"  accepted_hashes: {summary.accepted_hashes}")
        print(f"  reject_reason_counts: {summary.reject_reason_counts}")
        return 0 if summary.n_accepted else 1

    p.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
