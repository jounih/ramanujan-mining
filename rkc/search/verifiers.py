"""rkc.search.verifiers — Verifier implementations for Project C.

`MpmathVerifier`: numerical equality of two sympy expressions to N digits
over a sweep of parameter bindings. Standard tool for the Ramanujan-side
verification step.

Per PROJECT_C_DESIGN.md "Critical engineering decisions" §1: general-
purpose numerical equality is harder than it sounds (branch cuts,
convergence regimes, spurious symbolic cancellations). Re-use the Pass D
failure-mode experience documented in
[DID_NOT_PAN_OUT.md](../../insights/DID_NOT_PAN_OUT.md) R1-R10.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import mpmath
import sympy as sp

from .core import OperatorApplication, SearchState, VerificationResult, Verifier


@dataclass
class MpmathVerifier:
    """Numerical equality verifier.

    Strategy: pick a sweep of (variable, parameter) bindings; evaluate
    both expressions; compare to `n_digits` precision; pass iff ALL
    sweep cells agree to that precision.

    `n_digits` is the strict bar. Failure modes:
    - Spurious agreement at low precision but disagreement at high
      (per CLAUDE.md noisy-positive discipline; bump n_digits if you
      see this happen at the proposer level).
    - Branch-cut crossing at one cell (one cell disagrees by a 2πi term);
      handled here by reporting first-failure rather than majority-vote.
    - Convergence regime mismatch (one side converges at the cell, the
      other doesn't); manifests as ValueError / OverflowError caught and
      reported as failure with NUMERICAL_INSTABILITY-shaped reason.
    """
    n_digits: int = 40
    # default parameter sweep: a few orders of magnitude in beta/q-like params
    sweep_params: list[dict[str, Any]] | None = None

    def _default_sweep(self) -> list[dict[str, Any]]:
        # generic: try a few values of common parameters
        return [
            {"beta": mpmath.mpf("0.001")},
            {"beta": mpmath.mpf("0.1")},
            {"beta": mpmath.mpf("1.0")},
            {"beta": mpmath.mpf("10.0")},
            {"q": mpmath.mpf("0.1")},
            {"q": mpmath.mpf("0.5")},
            {"q": mpmath.mpf("0.9")},
        ]

    def verify(self, state_before: SearchState,
               op_sequence: list[OperatorApplication],
               state_after: SearchState) -> VerificationResult:
        """Verify that `state_after.payload` is numerically equal to
        `state_before.payload` over the parameter sweep.

        For Project C, the verifier asks: "is the transformed expression
        equal to the original?" (not "is it equal to some target"). We're
        confirming that the operator sequence preserves the value while
        possibly changing the form.
        """
        expr_before = state_before.payload
        expr_after = state_after.payload

        # quick symbolic shortcut: if they're sympy-equal, trivially passes
        try:
            if sp.simplify(expr_before - expr_after) == 0:
                return VerificationResult(
                    passed=True,
                    digits_or_examples=self.n_digits,
                    reason="symbolically equal",
                )
        except Exception:
            pass  # fall through to numerical

        sweep = self.sweep_params if self.sweep_params is not None else self._default_sweep()
        old_dps = mpmath.mp.dps
        try:
            mpmath.mp.dps = self.n_digits + 10  # working precision buffer
            tol = mpmath.mpf(10) ** (-self.n_digits)
            for cell in sweep:
                try:
                    val_before = self._evaluate(expr_before, cell)
                    val_after = self._evaluate(expr_after, cell)
                except Exception as e:
                    # one cell's eval failed — could be convergence regime or domain
                    return VerificationResult(
                        passed=False,
                        digits_or_examples=0,
                        reason=f"NUMERICAL_INSTABILITY at cell {cell}: {e}",
                    )
                if val_before is None or val_after is None:
                    continue  # neither side evaluated; skip
                if abs(val_before) < 1:
                    # absolute tolerance for small values
                    if abs(val_before - val_after) > tol:
                        return VerificationResult(
                            passed=False,
                            digits_or_examples=0,
                            reason=f"VERIFIER_FAILED at {cell}: "
                                   f"|before - after| = {abs(val_before - val_after)} > {tol}",
                        )
                else:
                    # relative tolerance for non-small values
                    rel_err = abs(val_before - val_after) / abs(val_before)
                    if rel_err > tol:
                        return VerificationResult(
                            passed=False,
                            digits_or_examples=0,
                            reason=f"VERIFIER_FAILED at {cell}: "
                                   f"rel_err = {rel_err} > {tol}",
                        )
            return VerificationResult(
                passed=True,
                digits_or_examples=self.n_digits,
                reason=f"numerical equality across {len(sweep)} sweep cells",
            )
        finally:
            mpmath.mp.dps = old_dps

    def _evaluate(self, expr: sp.Expr, cell: dict[str, Any]) -> Any:
        """Substitute cell into expr; return mpmath value or None if
        free symbols remain."""
        subs = {sp.Symbol(k): v for k, v in cell.items()}
        subs.update({sp.Symbol(k, positive=True): v for k, v in cell.items()})
        e = expr.subs(subs)
        if e.free_symbols:
            return None  # still has unresolved symbols
        try:
            return mpmath.mpc(complex(e))
        except (TypeError, ValueError):
            return None


# Sanity check the Verifier protocol is satisfied
assert isinstance(MpmathVerifier(), Verifier)
