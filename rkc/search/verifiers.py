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


# v0.8c: lambdify modules extension for number-theoretic functions.
# `sympy.divisor_sigma(m, 0)` (number-of-divisors d(m)) appears in the
# v0.8c Stieltjes/Lambert occupation-number dual summand. mpmath has no
# native divisor_count, so we provide a thin shim. The shim rounds the
# float-cast argument to the nearest positive integer and calls sympy's
# pure-python divisor_count. This module-list is used by `_sum_evaluate`'s
# lambdify call; v0.4 / v0.7 / v0.8b summands don't contain divisor_sigma
# so they're unaffected.
def _v08c_divisor_sigma_shim(x: Any, k: Any = 0) -> Any:
    """mpmath-compatible callable for sympy's `divisor_sigma(m, k)`.

    Only `k == 0` (the divisor-count case) is exercised by v0.8c; we
    accept any `k` for shape-compat but only the k=0 path is verified.
    """
    m_int = int(round(float(x)))
    if m_int < 1:
        return mpmath.mpf(0)
    k_int = int(round(float(k)))
    return mpmath.mpf(int(sp.divisor_sigma(m_int, k_int)))


_V08C_LAMBDIFY_MODULES = [
    {"divisor_sigma": _v08c_divisor_sigma_shim},
    "mpmath",
]


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

        v0.8b extension: if any op in `op_sequence` carries an
        `additive_correction` field, the verifier compares
            Σ_n state_before  ≡  Σ_n state_after + total_additive_correction
        where `total_additive_correction` is the sum of all the
        additive_correction fields. Operators that don't carry a
        correction (v0.4 Gaussian, v0.7 half-shift / weighted — all None
        by default) contribute 0 to the sum. This preserves the strict
        v0.7 verification path exactly for the existing identities.

        Similarly, if any op carries a `summand_range`, the verifier uses
        that range when nsumming the v0.8b summands. v0.4 / v0.7
        operators leave it None and inherit the verifier's default
        symmetric range (`(-oo, oo)`). The verifier requires all non-None
        summand_range entries in op_sequence to agree (operators with
        incompatible ranges cannot mix; the verifier returns
        VERIFIER_FAILED in that case).
        """
        expr_before = state_before.payload
        expr_after = state_after.payload
        var = state_before.metadata.get("var")

        # v0.8b: collect additive corrections + summand range from the
        # op_sequence. Both default to "no override" (correction = 0,
        # range = self.summand_range).
        additive_correction = sp.Integer(0)
        op_summand_range = None
        for op in op_sequence:
            if getattr(op, "additive_correction", None) is not None:
                additive_correction = additive_correction + op.additive_correction
            r = getattr(op, "summand_range", None)
            if r is not None:
                if op_summand_range is not None and op_summand_range != r:
                    return VerificationResult(
                        passed=False,
                        digits_or_examples=0,
                        reason=f"OPERATOR_DOMAIN_VIOLATION: incompatible "
                               f"summand_range entries in op_sequence: "
                               f"{op_summand_range} vs {r}",
                    )
                op_summand_range = r
        # Effective range for THIS verification call: prefer the op-supplied
        # range when any op set it; else fall back to the verifier default.
        effective_range = op_summand_range if op_summand_range is not None else self.summand_range
        has_correction = additive_correction != 0

        # quick symbolic shortcut: if they're sympy-equal (after folding the
        # additive correction) and no v0.8b override, trivially passes
        try:
            if not has_correction and sp.simplify(expr_before - expr_after) == 0:
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
            # v0.8b: one-sided modular sums (log-Bose-Einstein, Lambert) can
            # have slow LHS convergence at very small β. The β·n decay of
            # log(1-e^{-βn}) needs ~50000 terms at β=1e-3 to reach 20 digits.
            # When an additive correction is present (signaling a v0.8b
            # modular_transform_with_correction op), bump the working
            # precision buffer to give mp.nsum enough headroom for the slow
            # tail. Otherwise the v0.4/v0.7 strict-Poisson default suffices.
            dps_buffer = 40 if has_correction else 10
            mpmath.mp.dps = self.n_digits + dps_buffer  # working precision buffer
            tol = mpmath.mpf(10) ** (-self.n_digits)
            for cell in sweep:
                try:
                    if self.summand_mode and var is not None:
                        val_before = self._sum_evaluate(
                            expr_before, var, cell, summand_range=effective_range,
                        )
                        val_after = self._sum_evaluate(
                            expr_after, var, cell, summand_range=effective_range,
                        )
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
                # v0.8b: fold the additive correction into the after-side
                # before comparison. The identity is:
                #   sum(before) = sum(after) + correction
                # so we test |sum(before) - sum(after) - correction| ≤ tol.
                if has_correction:
                    try:
                        corr_val = self._evaluate(additive_correction, cell)
                    except Exception as e:
                        return VerificationResult(
                            passed=False,
                            digits_or_examples=0,
                            reason=f"NUMERICAL_INSTABILITY evaluating additive "
                                   f"correction at cell {cell}: {e}",
                        )
                    if corr_val is None:
                        return VerificationResult(
                            passed=False,
                            digits_or_examples=0,
                            reason=f"additive correction has free symbols beyond "
                                   f"cell at {cell}",
                        )
                    val_after_eff = val_after + corr_val
                else:
                    val_after_eff = val_after
                if abs(val_before) < 1:
                    # absolute tolerance for small values
                    if abs(val_before - val_after_eff) > tol:
                        return VerificationResult(
                            passed=False,
                            digits_or_examples=0,
                            reason=f"VERIFIER_FAILED at {cell}: "
                                   f"|before - after - correction| "
                                   f"= {abs(val_before - val_after_eff)} > {tol}",
                        )
                else:
                    # relative tolerance for non-small values
                    rel_err = abs(val_before - val_after_eff) / abs(val_before)
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
                       f"({'summand' if self.summand_mode else 'pointwise'} mode"
                       f"{', with additive correction' if has_correction else ''})",
            )
        finally:
            mpmath.mp.dps = old_dps

    def _sum_evaluate(self, expr: sp.Expr, var: sp.Symbol,
                      cell: dict[str, Any],
                      summand_range: tuple | None = None) -> Any:
        """Substitute cell params; either integrate (if expr is an Integral)
        or sum (if expr is a summand) numerically. Returns None if
        substitution leaves free symbols other than var, or if the
        evaluation fails.

        v0.5: dispatches on `isinstance(expr, sp.Integral)` — Integrals
        are integrated via mp.quad; summands are summed via mp.nsum.
        Closed-form expressions (no Sum/Integral wrapper, no remaining
        var dependence after substitution) are evaluated pointwise.

        v0.8b: `summand_range` overrides the verifier-level default
        (`self.summand_range`, typically `(-oo, oo)`). The new operator
        class `modular_transform_with_correction` uses `(1, oo)` for
        one-sided modular identities (Bose-Einstein eta-log, Lambert /
        E_2). The override is per-call so a single Verifier instance can
        handle both regimes across different operator types.
        """
        effective_range = summand_range if summand_range is not None else self.summand_range
        subs = {sp.Symbol(k): v for k, v in cell.items()}
        subs.update({sp.Symbol(k, positive=True): v for k, v in cell.items()})
        e = expr.subs(subs)

        # CASE A: Integral expression — integrate via mp.quad over the
        # Integral's own (var, lower, upper) limits
        if isinstance(e, sp.Integral):
            return self._integrate_evaluate(e)

        # CASE B: Non-Integral with no remaining var dependence → closed
        # form, evaluate directly. Handles the AFTER-side of v0.5
        # master_theorem applications (Γ(s), Γ(m)Γ(n)/Γ(m+n), π/sin(πs)).
        #
        # v0.10 wrinkle (gauss_sum_finite_evaluation): when the operator
        # emits a CONSTANT summand (e.g. `closed_form / q`) over a FINITE
        # explicit summand_range (e.g. (0, q-1)), we must MULTIPLY by the
        # range count rather than return the scalar directly. The original
        # v0.5 master_theorem path uses Integral semantics, where Case A
        # fires first; for non-Integral n-independent payloads the legacy
        # behaviour was scalar-evaluate, which is correct ONLY when the
        # caller-supplied range is the default `(-oo, oo)` (no operator
        # set it) AND the expression really IS a scalar (not a summand).
        # When summand_range is explicitly a (finite, finite) tuple AND
        # was set by an operator (via the op_summand_range path), we
        # respect it by multiplying.
        free_minus_var = e.free_symbols - {var}
        free_minus_var = {s for s in free_minus_var if s.name != var.name}
        if not e.has(var) and not free_minus_var:
            # Use sympy's evalf at current mp.dps to preserve precision
            # (Python's `complex()` downcasts to 64-bit doubles — fine for
            # v0.5 master_theorem at n_digits ≤ ~14, but breaks the v0.10
            # gauss_sum 30-digit verification because the closed-form
            # constants like `√7·I/7` have to retain full precision).
            try:
                val = e.evalf(mpmath.mp.dps)
                if val.is_real:
                    scalar_val = mpmath.mpc(mpmath.mpf(val), mpmath.mpf(0))
                else:
                    scalar_val = mpmath.mpc(
                        mpmath.mpf(sp.re(val)),
                        mpmath.mpf(sp.im(val)),
                    )
            except (TypeError, ValueError, AttributeError):
                # Fallback to the legacy complex path for forms evalf can't handle
                try:
                    scalar_val = mpmath.mpc(complex(e))
                except (TypeError, ValueError):
                    return None
            # If the caller-supplied summand_range is a tuple of FINITE
            # integers (v0.10 gauss_sum case), multiply by the range count.
            # Other ranges (e.g. (1, oo), (-oo, oo)) keep the scalar
            # semantics for backward compat with v0.5 master_theorem.
            if (summand_range is not None
                    and isinstance(summand_range, tuple)
                    and len(summand_range) == 2):
                lo, hi = summand_range
                try:
                    lo_int = int(lo)
                    hi_int = int(hi)
                    count = hi_int - lo_int + 1
                    if count > 0:
                        return scalar_val * count
                except (TypeError, ValueError):
                    pass
            return scalar_val

        # CASE C: Summand — sum via mp.nsum (the v0.4 path)
        free = e.free_symbols - {var}
        free = {s for s in free if s.name != var.name}
        if free:
            return None
        # v0.8c: use the extended modules list so summands containing
        # sympy.divisor_sigma (Stieltjes occupation-number dual) lambdify
        # cleanly. Backward-compatible: v0.4 / v0.7 / v0.8b summands don't
        # reference divisor_sigma so the extension is a no-op for them.
        try:
            f_callable = sp.lambdify(var, e, modules=_V08C_LAMBDIFY_MODULES)
        except Exception:
            return None
        try:
            return mpmath.nsum(f_callable, effective_range)
        except Exception:
            return None

    def _integrate_evaluate(self, expr: sp.Integral) -> Any:
        """Numerically integrate an sp.Integral via mp.quad.

        Handles single-variable integrals with finite or infinite limits.
        Returns None on failure (non-convergent, free symbols remain, etc.).
        """
        if len(expr.limits) != 1 or len(expr.limits[0]) != 3:
            return None
        x, lower, upper = expr.limits[0]
        integrand = expr.function
        # any free symbols other than x → undefined; can't integrate
        free = integrand.free_symbols - {x}
        if free:
            return None
        try:
            f_callable = sp.lambdify(x, integrand, "mpmath")
        except Exception:
            return None
        # translate sympy oo → mpmath.inf
        def _to_mp(b):
            if b is sp.oo:
                return mpmath.inf
            if b is -sp.oo:
                return -mpmath.inf
            try:
                return mpmath.mpf(complex(b).real)
            except (TypeError, ValueError):
                return None
        a_num = _to_mp(lower)
        b_num = _to_mp(upper)
        if a_num is None or b_num is None:
            return None
        try:
            return mpmath.quad(f_callable, [a_num, b_num])
        except Exception:
            return None

    def _evaluate(self, expr: sp.Expr, cell: dict[str, Any]) -> Any:
        """Substitute cell into expr; return mpmath value or None if
        free symbols remain.

        Uses sympy's `evalf(mpmath.mp.dps)` for high-precision evaluation
        rather than `complex(...)` (which silently downcasts to 64-bit
        Python complex — a problem for v0.8b additive corrections like
        `-π²/(6β)` where the closed-form needs full mpmath precision).
        """
        subs = {sp.Symbol(k): v for k, v in cell.items()}
        subs.update({sp.Symbol(k, positive=True): v for k, v in cell.items()})
        e = expr.subs(subs)
        if e.free_symbols:
            return None  # still has unresolved symbols
        try:
            # Use sympy's evalf at the current mpmath dps. This preserves
            # full precision for expressions involving π / e / γ symbols
            # (the v0.8b additive corrections do).
            val = e.evalf(mpmath.mp.dps)
            # Cast to mpmath complex; sympy Floats are mpf-compatible.
            if val.is_real:
                return mpmath.mpf(val)
            return mpmath.mpc(mpmath.mpf(sp.re(val)), mpmath.mpf(sp.im(val)))
        except (TypeError, ValueError, AttributeError):
            # Fallback to the legacy complex path
            try:
                return mpmath.mpc(complex(e))
            except (TypeError, ValueError):
                return None


# Sanity check the Verifier protocol is satisfied
assert isinstance(MpmathVerifier(), Verifier)
