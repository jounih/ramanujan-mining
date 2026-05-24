"""rkc.search.proposers — Proposer implementations for Project C.

v0.3 ships `RandomProposer` (the baseline). v0.8a adds `ClaudeProposer`
(LLM-powered, Anthropic API) and the `ClaudeStubProposer` graceful
fallback when no API key is available.

Motivating evidence for the LLM-proposer extension (per diary 30):
OpenAI's 22-May-2026 disproof of Erdős's unit-distance conjecture used
an internal model whose chain-of-thought made *meta-reasoning about the
search space* the load-bearing move ("number fields deserve a closer
look"). The same class-field / modular machinery dominates Ramanujan's
Notebooks Ch. 34 (per Hunt 5b, diary 25). A Claude-API proposer that
*knows* the toolkit-split finding can bias its operator suggestions
toward the cluster appropriate to the current state's structure, rather
than sampling uniformly.

The default `RandomProposer` controls for proposer-quality so the
verifier+router+cost+registry pipeline (steps 3-6) can be evaluated
independently. `ClaudeProposer` is the v1+ direction: a proposer with
mathematical taste.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import random
import re
from dataclasses import dataclass, field
from typing import Any, Iterator

from .core import OperatorApplication, Proposer, SearchState
from .basis import Operator, QR7_OPERATOR_BASIS


log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# RandomProposer (v0 baseline — unchanged from v0.3)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# ClaudeProposer (v0.8a — LLM-powered)
# ---------------------------------------------------------------------------

# The system-prompt context the proposer uses to decide operators. Includes
# (a) Project C's six-step loop framing so Claude knows its output's role,
# (b) the 7-operator basis with one-line descriptions, and (c) the Hunt 5b
# toolkit-split finding (per diary 25) so Claude can bias toward the cluster
# matching the state's structural family.

_SYSTEM_PROMPT_TEMPLATE = """\
You are the proposer step (step 2) in Project C, a symbolic-discovery engine
for mathematical identities at the Ramanujan-Mining repo. The engine runs a
six-step loop: (1) choose state, (2) YOU suggest an operator, (3) router
classifies, (4) verifier tests numerically, (5) cost-gate, (6) accept/reject.

Your job: given the current expression (a sympy expression as a string), pick
the SINGLE operator from the 7-operator basis below that is most likely to
yield an accepted transformation. Output ONLY a JSON object with the chosen
operator id and an optional one-line rationale.

THE 7-OPERATOR BASIS:

{operator_list}

THE TOOLKIT-SPLIT FINDING (Hunt 5b, diary 25 — ESTABLISHED across 3 NB
chapters; use this to bias your choice):

  - Continued-fraction problems / q-Pochhammer surface structure
    → favor a modular-family operator (Ch. 32 pattern; modular_S +
      q-shift in the Notebooks toolkit)
  - Modular-equation problems (algebraic α-β relations in K_0(N))
    → favor a modular_S-equivalent operator (Ch. 36 monoculture)
  - Class-invariant / singular-modulus / j-invariant problems
    → favor a class-field + modular_S combo (Ch. 34)
  - One-sided (n ≥ 1) Bose-Einstein 1/(1-exp(-β n)) or Lambert
    n·q^n/(1-q^n) summands
    → favor modular_transform_with_correction (v0.8b: the additive
      correction term it emits captures the log/E_2 anomaly)
  - Quarterly-Reports-style problems (Mellin transforms, Master Theorem,
    Frullani, Hardy orders, fractional iteration)
    → favor master_theorem + frullani_limit + fractional_functional_iteration
      + hardy_orders_of_infinity + mellin_pair_reciprocity
  - Pure-Gaussian / theta-like summands on n ∈ Z: exp(-β n²) and shifts/weights
    → favor mellin_inversion (the strict two-sided Poisson-summation route)
  - Integral expressions ∫ x^(s-1) f(x) dx
    → favor master_theorem (canonical Mellin reduction)

The Notebooks chapters NEVER fired master_theorem/Mellin/QR-III operators
(toolkit-disjoint from the QR III corpus). Conversely the QR corpus never
fired modular_S / q_shift / class_field. The two toolkits are structurally
separate — pick from the right side.

OUTPUT FORMAT (strict — output NOTHING else):

{{"op_id": "<one of the 7 ids>", "rationale": "<≤ 12 words>"}}
"""


def _format_operator_list(basis: list[Operator]) -> str:
    lines = []
    for op in basis:
        # squash the docstring-style notes into a single line
        notes = " ".join(op.notes.split())
        lines.append(f"  - {op.id} ({op.family_tag}): {notes}")
    return "\n".join(lines)


def _build_user_prompt(state: SearchState,
                       prior_attempts: list[dict] | None = None,
                       route_hint: str | None = None) -> str:
    """Build the per-turn user prompt with current expression + history."""
    var = state.metadata.get("var", "n")
    parts = [
        f"Current expression: {state.payload}",
        f"Iteration variable: {var}",
    ]
    if route_hint:
        parts.append(f"Router's current classification: {route_hint}")
    if prior_attempts:
        parts.append("\nPrior attempts on this state (operator → reject reason):")
        for att in prior_attempts[-10:]:  # cap to last 10 for token discipline
            op_id = att.get("op_id", "?")
            reason = att.get("reason", "?")
            parts.append(f"  - {op_id} → {reason}")
        parts.append("\nAvoid operators that have repeatedly failed unless you "
                     "have a structural reason to try them again.")
    parts.append("\nWhich operator should I try next?")
    return "\n".join(parts)


@dataclass
class ClaudeStubProposer:
    """Graceful fallback when no `ANTHROPIC_API_KEY` is available.

    Prints the system prompt + per-state user prompt to stdout (or via
    the logger) for human inspection, then yields a random selection from
    the basis (like `RandomProposer`). Used by `ClaudeProposer.__init__`
    when the API key is missing so CI and offline test runs still work.

    Per CLAUDE.md "No silent failures": the stub logs WHY it's stubbing
    (missing API key) at construction time.
    """
    basis: list[Operator] = field(default_factory=lambda: list(QR7_OPERATOR_BASIS))
    seed: int | None = None
    print_prompts: bool = False

    def __post_init__(self):
        self._rng = random.Random(self.seed)
        log.info("ClaudeStubProposer active: ANTHROPIC_API_KEY not set; "
                 "falling back to random selection.")

    def propose(self, state: SearchState, budget: int) -> Iterator[OperatorApplication]:
        if self.print_prompts:
            sys_prompt = _SYSTEM_PROMPT_TEMPLATE.format(
                operator_list=_format_operator_list(self.basis))
            user_prompt = _build_user_prompt(state)
            print("=== ClaudeStubProposer system prompt ===")
            print(sys_prompt)
            print("=== ClaudeStubProposer user prompt ===")
            print(user_prompt)
        for _ in range(budget):
            op = self._rng.choice(self.basis)
            yield OperatorApplication(
                op_id=op.id, params={}, confidence=1.0 / len(self.basis),
            )

    def __repr__(self) -> str:
        return f"ClaudeStubProposer(basis={len(self.basis)} ops)"


@dataclass
class ClaudeProposer:
    """LLM-powered proposer using the Anthropic API.

    Per-turn behaviour: build a system prompt covering Project C's loop +
    the 7-operator basis + the Hunt 5b toolkit-split heuristics, and a
    user prompt with the current expression + prior rejected attempts on
    this state. Parse the JSON response and emit one OperatorApplication.

    Cost discipline:
    - Default model is `claude-sonnet-4-5` (cheap + capable).
    - `max_api_calls` caps the total Anthropic calls per `propose()` call
      (default 10). Excess `budget` is filled from random fallback.
    - Responses are cached by (system_prompt_hash, user_prompt_hash) so
      identical states don't re-spend (useful in multi-depth loops where
      the engine repeatedly proposes from the same intermediate state).

    Graceful degradation:
    - If `ANTHROPIC_API_KEY` is not set OR the anthropic SDK isn't
      installed, falls back to `ClaudeStubProposer` automatically (so
      tests can run in CI without network access). The fallback is
      LOGGED, not silent (per CLAUDE.md "no silent failures").
    - If a Claude response can't be parsed as JSON / chosen op_id is not
      in basis, falls back to a random op for that turn and logs the
      malformed payload.

    History tracking: the proposer accepts an external `history` list of
    `{"op_id": ..., "reason": ...}` dicts (e.g., from the search engine's
    reject_reason_counts) via `set_history()`. Useful when the engine
    wants the proposer to know what's been tried — though v0.8a's
    integration with the engine just uses the default empty history
    (engine doesn't yet thread per-state history into proposer calls).
    """
    basis: list[Operator] = field(default_factory=lambda: list(QR7_OPERATOR_BASIS))
    model: str = "claude-sonnet-4-5"
    max_api_calls: int = 10
    max_tokens: int = 512
    seed: int | None = None
    # If client is None, ClaudeProposer will look up the API key at
    # construction time. Override with a mock for testing.
    client: Any = None

    def __post_init__(self):
        self._rng = random.Random(self.seed)
        self._api_call_count = 0
        self._cache: dict[str, OperatorApplication] = {}
        self._history: list[dict] = []
        self._op_ids = {op.id for op in self.basis}
        self._fallback: ClaudeStubProposer | None = None

        if self.client is None:
            # Try to load API key from .env if present
            try:
                from dotenv import load_dotenv
                load_dotenv()
            except ImportError:
                pass
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                log.warning(
                    "ClaudeProposer: ANTHROPIC_API_KEY not set in environment; "
                    "falling back to ClaudeStubProposer (random selection). "
                    "Set ANTHROPIC_API_KEY in .env to enable live Claude calls."
                )
                self._fallback = ClaudeStubProposer(
                    basis=self.basis, seed=self.seed,
                )
                return
            try:
                import anthropic  # noqa: F401
                self.client = anthropic.Anthropic(api_key=api_key)
            except ImportError:
                log.warning(
                    "ClaudeProposer: anthropic SDK not installed; "
                    "falling back to ClaudeStubProposer. "
                    "Run `pip install anthropic` to enable Claude calls."
                )
                self._fallback = ClaudeStubProposer(
                    basis=self.basis, seed=self.seed,
                )
                return

    def set_history(self, history: list[dict]) -> None:
        """Inject prior-attempts history for the next propose() call."""
        self._history = list(history)

    def _system_prompt(self) -> str:
        return _SYSTEM_PROMPT_TEMPLATE.format(
            operator_list=_format_operator_list(self.basis),
        )

    def _cache_key(self, system_prompt: str, user_prompt: str) -> str:
        h = hashlib.sha256()
        h.update(system_prompt.encode("utf-8"))
        h.update(b"\x00")
        h.update(user_prompt.encode("utf-8"))
        return h.hexdigest()

    def _parse_response(self, text: str) -> tuple[str | None, str]:
        """Extract (op_id, rationale) from a Claude response.

        Accepts strict JSON or JSON wrapped in markdown code-fences /
        leading prose (common LLM artefacts). Returns (None, raw_text)
        if nothing parseable; the caller falls back to a random op.
        """
        # Try strict JSON first
        text = text.strip()
        # Strip markdown code fences if present
        fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text,
                                re.DOTALL)
        if fence_match:
            text = fence_match.group(1)
        # Try to locate the first {...} block
        brace_match = re.search(r"\{[^{}]*\}", text, re.DOTALL)
        if brace_match:
            text = brace_match.group(0)
        try:
            payload = json.loads(text)
        except (json.JSONDecodeError, ValueError):
            return None, text
        if not isinstance(payload, dict):
            return None, text
        op_id = payload.get("op_id")
        rationale = payload.get("rationale", "")
        if not isinstance(op_id, str):
            return None, text
        return op_id, rationale

    def _random_fallback(self, reason: str) -> OperatorApplication:
        """Construct a uniform-random OperatorApplication; log why."""
        op = self._rng.choice(self.basis)
        log.warning("ClaudeProposer fallback (%s) → random op_id=%s",
                    reason, op.id)
        return OperatorApplication(
            op_id=op.id, params={},
            confidence=1.0 / len(self.basis),
        )

    def _claude_one_call(self, state: SearchState) -> OperatorApplication:
        """One Anthropic API call → one OperatorApplication.

        Caches by (system_prompt, user_prompt) hash. Falls back to random
        on parse failure or basis-membership violation (logged).
        """
        sys_prompt = self._system_prompt()
        user_prompt = _build_user_prompt(state, prior_attempts=self._history)
        key = self._cache_key(sys_prompt, user_prompt)
        if key in self._cache:
            return self._cache[key]

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=sys_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )
            self._api_call_count += 1
        except Exception as exc:
            log.warning("ClaudeProposer: API call raised %s: %s",
                        type(exc).__name__, exc)
            return self._random_fallback(reason=f"API error: {exc}")

        # Extract the text content (Anthropic SDK returns a list of content blocks)
        try:
            text_parts: list[str] = []
            for block in response.content:
                if hasattr(block, "text"):
                    text_parts.append(block.text)
                elif isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))
            text = "\n".join(text_parts)
        except Exception as exc:
            log.warning("ClaudeProposer: response shape unexpected: %s", exc)
            return self._random_fallback(reason=f"response parse: {exc}")

        op_id, rationale = self._parse_response(text)
        if op_id is None:
            log.warning("ClaudeProposer: could not parse op_id from response: %r",
                        text[:200])
            return self._random_fallback(reason="malformed response")
        if op_id not in self._op_ids:
            log.warning("ClaudeProposer: returned op_id=%r not in basis (have %s)",
                        op_id, sorted(self._op_ids))
            return self._random_fallback(reason=f"op_id {op_id!r} not in basis")

        result = OperatorApplication(
            op_id=op_id, params={},
            confidence=0.8,  # high confidence because LLM picked it deliberately
        )
        self._cache[key] = result
        return result

    def propose(self, state: SearchState, budget: int) -> Iterator[OperatorApplication]:
        if self._fallback is not None:
            yield from self._fallback.propose(state, budget)
            return

        for _ in range(budget):
            if self._api_call_count >= self.max_api_calls:
                # Out of API budget — fill rest from random
                yield self._random_fallback(reason="max_api_calls exceeded")
                continue
            yield self._claude_one_call(state)

    def stats(self) -> dict[str, Any]:
        """Diagnostic: how many API calls were made + cache state."""
        return {
            "api_calls": self._api_call_count,
            "max_api_calls": self.max_api_calls,
            "cache_size": len(self._cache),
            "model": self.model,
            "fallback_active": self._fallback is not None,
        }

    def __repr__(self) -> str:
        return (f"ClaudeProposer(model={self.model!r}, "
                f"max_api_calls={self.max_api_calls}, "
                f"fallback={'on' if self._fallback else 'off'})")


# Sanity check the Proposer protocol is satisfied by all three classes.
assert isinstance(RandomProposer(), Proposer)
assert isinstance(ClaudeStubProposer(), Proposer)
# Note: ClaudeProposer can't be instantiated here for the assert without
# either an API key or a client mock (which would do a real-world API
# import); the protocol-conformance is guaranteed by structural typing of
# `propose()` and tested explicitly in test_v08a_*.
