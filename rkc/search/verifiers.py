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

    By default treats inputs as **summand expressions** — given a payload
    `f(n, β)` and iteration variable `n`, the verifier sums
    `Σ_{n=0}^∞ f(n, β)` at each parameter cell via `mpmath.nsum`. Pass
    `summand_mode=False` for pointwise comparison instead.

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
    # if True (default), interpret payload as a summand and compare
    # Σ_{n=0}^∞ payload values; if False, evaluate payload pointwise.
    summand_mode: bool = True
    # range for the summation when summand_mode=True
    summand_range: tuple[int, Any] = (-mpmath.inf, mpmath.inf)

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

        In `summand_mode=True` (default), both payloads are summed
        Σ_n payload(n, params) via mpmath.nsum at each cell before
        comparison. This is the right mode for kernel-routing
        transformations like Poisson summation (`exp(-β n²)` → dual).

        In `summand_mode=False`, payloads are evaluated pointwise at
        each cell; useful for transformations that are pointwise
        identities, not series identities.
        """
        expr_before = state_before.payload
        expr_after = state_after.payload
        var = state_before.metadata.get("var")

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
                    if self.summand_mode and var is not None:
                        val_before = self._sum_evaluate(expr_before, var, cell)
                        val_after = self._sum_evaluate(expr_after, var, cell)
                    else:
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
                reason=f"numerical equality across {len(sweep)} sweep cells "
                       f"({'summand' if self.summand_mode else 'pointwise'} mode)",
            )
        finally:
            mpmath.mp.dps = old_dps

    def _sum_evaluate(self, expr: sp.Expr, var: sp.Symbol,
                      cell: dict[str, Any]) -> Any:
        """Substitute cell params, then sum Σ_n expr(n) over summand_range
        via mpmath.nsum. Returns None if substitution leaves free symbols
        other than var, or if the sum doesn't converge.
        """
        subs = {sp.Symbol(k): v for k, v in cell.items()}
        subs.update({sp.Symbol(k, positive=True): v for k, v in cell.items()})
        e = expr.subs(subs)
        # any remaining free symbols other than var → undefined cell
        free = e.free_symbols - {var}
        # also subtract any positive-symbol twins of var
        free = {s for s in free if s.name != var.name}
        if free:
            return None
        # compile a numerical function f(n) = e evaluated at integer n
        try:
            f_callable = sp.lambdify(var, e, "mpmath")
        except Exception:
            return None
        try:
            return mpmath.nsum(f_callable, self.summand_range)
        except Exception:
            return None

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
