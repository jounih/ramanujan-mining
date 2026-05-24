"""rkc.recognizer — v2 of the kernel-fingerprint recognizer.

What changed vs v1 (analysis/13_recognizer_v1.py):

  GAP 1 — Scalar-coefficient stripping. v1's one false-negative was
          `3 * exp(-beta n^2)` predicted `none`. v2 peels outer scalar
          coefficients before dispatching to the strict matchers, then
          re-applies them in the cost estimate as `scalar_coefficient` on
          the result.

  GAP 2 — Soft fuzzy second-pass matcher. v1 had no intermediate "shape
          category" — it was strict-match or null. v2's second pass emits
          a kernel-family-ish RoutingResult with route=FUZZY and a
          confidence score in [0, 1]. Used for shifted-theta `q^(n^2+n)`,
          mock-f3 × cos(n), Lambert-look-alikes etc.

  GAP 3 — Per-component cost rollup. v1's composite wrapper detected
          sum/product decomposition but only reported one component's
          route. v2 walks every Add term / Mul factor, runs `recognize`
          on each, and reports `total_cost = sum_i total_cost(component_i)`
          via the `components` field of the composite result.

  GAP 4 — Per-term complexity. Each registry entry now carries a
          `per_term_cost(params, target_precision)` function (cf. costs.py)
          and the result reports `total_cost = num_terms * per_term_cost`.
          Bits-per-term is no longer the only routing signal — insight §A7.

  GAP 5 — Gauss-sum gcd-degeneracy fix. v1's diary noted the gcd branch
          was unreachable because sympy auto-reduces 2*n^2/6 -> n^2/3.
          v2 ships `recognize_with_raw_string` that re-extracts the
          pre-reduction (p_raw, q_raw) from the user-supplied string and
          stashes it as `raw_pq` for the Gauss-sum degeneracy detector.

  GAP 6 — Optional extra kernels. v1 already registered partial_theta,
          q_pochhammer_infty, and eisenstein_E2k. v2 keeps the same set
          but exposes them through the rkc/ package interface. (No new
          kernels added beyond v1; that's tracked in 'still missing'.)

The public surface is two functions:

    recognize(expr_summand, n_sym, target_precision=1e-12) -> list[RoutingResult]
    best_match(expr_summand, n_sym, target_precision=1e-12) -> RoutingResult|None

plus `recognize_composite` for sums/products and `recognize_with_raw_string`
for the Gauss-sum gcd workaround.
"""
from __future__ import annotations

import sympy as sp
from typing import Any, Optional

from .registry import (
    REGISTRY, FUZZY_MATCHERS, RegistryEntry, extract_raw_gauss_coefficient,
)
from .routing import (
    Route, RoutingResult, KernelFamily, degenerate_result, fuzzy_result,
)
from . import costs


def _strip_scalar_coefficient(expr: sp.Expr, n: sp.Symbol) -> tuple[sp.Expr, sp.Expr]:
    """Peel an outer constant (n-independent) scalar coefficient.

    Returns (core, scalar) where `core` is the n-dependent factor and
    `scalar` is the constant prefactor (1 if none). This is gap-1.

    Examples:
        3 * exp(-beta n^2)        -> (exp(-beta n^2), 3)
        (1/2) * q^n / (1 - q^n)   -> (q^n / (1 - q^n), 1/2)
        sin(n)                    -> (sin(n), 1)        # n-dependent
        exp(-beta n^2)            -> (exp(-beta n^2), 1)

    We treat ANY n-independent symbolic constant (positive symbols like
    `c`, `a`, etc.) as a scalar coefficient — i.e. we strip BEFORE
    consulting the matchers, so a downstream cost estimator can fold it
    back in. We refuse to strip when the n-dependent part is itself
    trivial (would make the whole expression a constant — no kernel).
    """
    if expr.func != sp.Mul:
        return expr, sp.Integer(1)
    n_dep = []
    n_indep = []
    for a in expr.args:
        if a.has(n):
            n_dep.append(a)
        else:
            n_indep.append(a)
    if not n_indep:
        return expr, sp.Integer(1)
    if not n_dep:
        # whole expression is n-independent; nothing to strip into
        return expr, sp.Integer(1)
    scalar = sp.Mul(*n_indep) if n_indep else sp.Integer(1)
    core = sp.Mul(*n_dep) if len(n_dep) > 1 else n_dep[0]
    return core, scalar


def _strict_match(expr: sp.Expr, n: sp.Symbol,
                  target_precision: float = 1e-12,
                  raw_pq: Optional[tuple[int, int]] = None,
                  scalar_coefficient: sp.Expr = sp.Integer(1)) -> list[RoutingResult]:
    """Run every strict matcher; return a RoutingResult per hit."""
    results: list[RoutingResult] = []
    for entry in REGISTRY:
        params = entry.match(expr, n)
        if params is None:
            continue
        # gap-5: stash raw (p, q) for the Gauss-sum degeneracy check
        if entry.name == "gauss_sum" and raw_pq is not None:
            params = dict(params)
            params["raw_pq"] = raw_pq
        deg = entry.degeneracy_check(params)
        if deg is not None:
            r = degenerate_result(entry.name, entry.family.value,
                                  {k: v for k, v in params.items() if k != "raw_pq"},
                                  deg, notes=entry.notes)
            r.scalar_coefficient = scalar_coefficient
            results.append(r)
            continue
        try:
            routing = entry.recommend_route(params, target_precision)
        except Exception as e:
            results.append(degenerate_result(
                entry.name, entry.family.value, params,
                f"routing failed: {e}", notes=entry.notes,
            ))
            continue
        # gap-4: per-term cost rollup
        try:
            per_term = entry.per_term_cost(params, target_precision)
        except Exception:
            per_term = costs.per_term_default(params, target_precision)
        num_terms = routing.get("num_terms", -1)
        if num_terms is None or num_terms <= 0:
            # fall back to whichever route was chosen
            if routing["route"] == Route.DUAL and routing.get("cost_dual", -1) > 0:
                num_terms = routing["cost_dual"]
            elif routing.get("cost_direct", -1) > 0:
                num_terms = routing["cost_direct"]
        total = costs.total_cost(num_terms, per_term, scalar_coefficient)
        r = RoutingResult(
            kernel=entry.name,
            family=entry.family.value,
            route=routing["route"],
            params={k: v for k, v in params.items() if k != "raw_pq"},
            num_terms=int(num_terms) if num_terms and num_terms > 0 else -1,
            per_term_cost=per_term,
            total_cost=total,
            cost_direct=int(routing.get("cost_direct", -1)),
            cost_dual=int(routing.get("cost_dual", -1)),
            reason=routing.get("reason"),
            notes=entry.notes,
            confidence=1.0,
            scalar_coefficient=scalar_coefficient,
        )
        results.append(r)
    return results


def _fuzzy_pass(expr: sp.Expr, n: sp.Symbol,
                target_precision: float = 1e-12,
                scalar_coefficient: sp.Expr = sp.Integer(1)) -> list[RoutingResult]:
    """Run fuzzy matchers and emit FUZZY-routed RoutingResults."""
    out: list[RoutingResult] = []
    for family, matcher, conf in FUZZY_MATCHERS:
        params = matcher(expr, n)
        if params is None:
            continue
        # fuzzy matches have no defensible cost prediction; we still hand back
        # a rough per-term cost using the family's default
        per_term = costs.per_term_default(params, target_precision)
        r = fuzzy_result(
            family, params,
            reason=f"matches {family.value} shape but failed strict matcher: {params.get('shape', 'unknown')}",
            confidence=conf,
            notes=f"fuzzy match — operator should inspect before routing",
        )
        r.per_term_cost = per_term
        r.scalar_coefficient = scalar_coefficient
        out.append(r)
    return out


def recognize(expr_summand: sp.Expr, n: sp.Symbol,
              target_precision: float = 1e-12,
              raw_pq: Optional[tuple[int, int]] = None,
              numerical_completion: bool = False,
              q_value: Any = None,
              target_digits: int = 30) -> list[RoutingResult]:
    """Walk every strict matcher; if none hit, run the fuzzy second pass.

    Gap-1: peel outer scalar coefficient BEFORE dispatching so
    `3 * exp(-beta n^2)` matches as gaussian with scalar_coefficient=3.

    Gap-2: if no strict matcher hits, the fuzzy second pass returns
    FUZZY-routed results. The caller can act on these or ignore them.

    Numerical-completion opt-in (default OFF for backward compatibility):
    when `numerical_completion=True` AND a strict mock-theta match yields
    route MODULAR_COMPLETION_REQUIRED, call the Watson-Hickerson Eichler
    integral pipeline (rkc.completions) and attach the resulting
    `(value, error_bound, certificate)` triple to the result's `completion`
    field. If `q_value` is not given, the matcher-extracted `q` from
    `params` is used. If that's not numerical, the completion is skipped
    silently (the flag remains).
    """
    core, scalar = _strip_scalar_coefficient(expr_summand, n)
    results = _strict_match(core, n, target_precision, raw_pq=raw_pq,
                            scalar_coefficient=scalar)
    if not results:
        # also try the original (unstripped) expression — some matchers may
        # be coefficient-tolerant and might match it directly (e.g. the
        # Eisenstein matcher would lose its rest-rejection if we always strip)
        if not core.equals(expr_summand):
            results = _strict_match(expr_summand, n, target_precision, raw_pq=raw_pq,
                                    scalar_coefficient=sp.Integer(1))
        if not results:
            # no strict hits — fall through to fuzzy
            results = _fuzzy_pass(core, n, target_precision, scalar_coefficient=scalar)

    if numerical_completion:
        _attach_completion(results, q_value, target_digits)
    return results


def _attach_completion(results: list[RoutingResult],
                       q_value: Any,
                       target_digits: int) -> None:
    """For every RoutingResult with route=MODULAR_COMPLETION_REQUIRED, try
    to attach a numerical completion via rkc.completions. Mutates the
    results in place — adds a `completion` attribute (or sets it to a
    string-tagged exception when unimplemented).
    """
    from . import completions as _comp
    for r in results:
        if r.route != Route.MODULAR_COMPLETION_REQUIRED:
            continue
        q_use = q_value
        if q_use is None:
            q_use = r.params.get("q")
        # decline gracefully if q is not numerically reducible
        try:
            from mpmath import mpf as _mpf
            q_num = _mpf(q_use)
        except Exception:
            r.completion_error = (
                f"numerical_completion requested but q is not numerical "
                f"(got {q_use!r}); pass q_value=<numeric> to recognize()"
            )
            continue
        try:
            result = _comp.compute_mock_theta_with_completion(
                family=r.kernel, q=q_num, target_digits=target_digits,
            )
            r.completion = result
        except _comp.CompletionNotImplemented as e:
            r.completion_error = (
                f"CompletionNotImplemented({e.family}): {e}"
            )


def best_match(expr_summand: sp.Expr, n: sp.Symbol,
               target_precision: float = 1e-12,
               raw_pq: Optional[tuple[int, int]] = None,
               accept_fuzzy: bool = False,
               numerical_completion: bool = False,
               q_value: Any = None,
               target_digits: int = 30) -> Optional[RoutingResult]:
    """Return the single best match, or None.

    Strict matches always win over fuzzy. Among strict matches, prefer
    non-degenerate; among non-degenerate, prefer lowest total_cost.

    Set `accept_fuzzy=True` to return FUZZY results when no strict match
    fires (default False — matches v1's strict-or-null semantics for
    benchmark backward-compatibility).

    `numerical_completion=True` enables the mock-theta route handler
    (rkc.completions); see `recognize()` for details. Default OFF.
    """
    results = recognize(expr_summand, n, target_precision, raw_pq=raw_pq,
                        numerical_completion=numerical_completion,
                        q_value=q_value, target_digits=target_digits)
    if not results:
        return None
    strict = [r for r in results if r.route != Route.FUZZY]
    if strict:
        non_deg = [r for r in strict if r.degenerate is None]
        if non_deg:
            return min(non_deg, key=lambda r: (
                r.total_cost if r.total_cost > 0 else 10**18
            ))
        return strict[0]
    if accept_fuzzy:
        # highest confidence wins
        return max(results, key=lambda r: r.confidence)
    return None


def recognize_composite(expr: sp.Expr, n: sp.Symbol,
                        target_precision: float = 1e-12,
                        numerical_completion: bool = False,
                        q_value: Any = None,
                        target_digits: int = 30) -> Optional[RoutingResult]:
    """Composite wrapper for sum/product decomposition with per-component
    cost rollup (gap 3).

    If `expr` matches atomically, return that. Otherwise, walk Add terms
    or Mul factors, run `best_match` on each, and return a synthetic
    RoutingResult whose `components` field lists per-component results
    and whose `total_cost` is the sum of component total_costs.

    Returns None if no component matches.

    The `numerical_completion`, `q_value`, and `target_digits` flags
    propagate to per-component `best_match` calls (W4 fix per diary 16
    deferred follow-up). When any component is MODULAR_COMPLETION_REQUIRED
    AND `numerical_completion=True`, that component's `.completion` field
    will hold the Watson-Hickerson Eichler integral result; the composite
    result's components list preserves this. (The composite's own value
    is not yet computed — that would require knowing how to combine
    component values under Add vs Mul, which is the v0.4 follow-up.)
    """
    direct = best_match(expr, n, target_precision,
                        numerical_completion=numerical_completion,
                        q_value=q_value, target_digits=target_digits)
    if direct is not None:
        return direct
    components: list[RoutingResult] = []
    decomposition = None
    if expr.func == sp.Add:
        decomposition = "sum"
        for term in expr.args:
            bm = best_match(term, n, target_precision,
                            numerical_completion=numerical_completion,
                            q_value=q_value, target_digits=target_digits)
            if bm is not None:
                components.append(bm)
    elif expr.func == sp.Mul:
        decomposition = "product"
        for factor in expr.args:
            bm = best_match(factor, n, target_precision,
                            numerical_completion=numerical_completion,
                            q_value=q_value, target_digits=target_digits)
            if bm is not None:
                components.append(bm)
    if not components:
        return None
    # synthesize composite result
    total = costs.composite_total_cost([c.to_dict() for c in components])
    # route: if any component is DEGENERATE, the composite likely is too;
    # if all DIRECT, composite is DIRECT; if any DUAL, that's the cheapest
    # available cross-component (a conservative heuristic).
    routes = [c.route for c in components]
    if Route.DEGENERATE in routes and all(r == Route.DEGENERATE for r in routes):
        composite_route = Route.DEGENERATE
    elif Route.DUAL in routes:
        composite_route = Route.DUAL
    elif Route.MODULAR_COMPLETION_REQUIRED in routes:
        composite_route = Route.MODULAR_COMPLETION_REQUIRED
    else:
        composite_route = Route.DIRECT
    primary = components[0]
    return RoutingResult(
        kernel=f"composite[{decomposition}]({','.join(c.kernel for c in components)})",
        family="composite",
        route=composite_route,
        params={"decomposition": decomposition,
                "n_components": len(components)},
        num_terms=sum(max(c.num_terms, 0) for c in components),
        per_term_cost=-1.0,  # not meaningful for composites
        total_cost=total,
        cost_direct=-1,
        cost_dual=-1,
        reason=f"composite {decomposition} of {len(components)} component(s); "
               f"total_cost = sum of per-component total_cost",
        notes="composite — see `components` for per-piece breakdown",
        components=[c.to_dict() for c in components],
        scalar_coefficient=sp.Integer(1),
    )


def recognize_with_raw_string(expr_string: str, n: sp.Symbol,
                              target_precision: float = 1e-12) -> list[RoutingResult]:
    """Gauss-sum gcd-degeneracy entry point (gap 5).

    Takes the EXPRESSION SOURCE as a string, walks the unevaluated parse
    to extract the raw (p, q) before sympy reduces them, then runs the
    normal `recognize` pipeline with `raw_pq` injected.

    For non-Gauss-sum expressions the raw extraction returns None and
    this behaves identically to `recognize(sympify(expr_string), n)`.
    """
    expr = sp.sympify(expr_string)
    # sympify creates a FRESH `n` symbol without the caller's assumptions;
    # rewrite it to the caller's `n` so the strict matchers compare cleanly.
    n_name = n.name if hasattr(n, "name") else str(n)
    for sym in list(expr.free_symbols):
        if getattr(sym, "name", None) == n_name and sym != n:
            expr = expr.subs(sym, n)
    raw_pq = None
    try:
        raw_pq = extract_raw_gauss_coefficient(expr_string, n)
    except Exception:
        raw_pq = None
    return recognize(expr, n, target_precision, raw_pq=raw_pq)


def main():
    """Sanity demo. The full benchmark lives in analysis/14*.py."""
    n = sp.symbols("n", integer=True, nonnegative=True)
    k = sp.symbols("k", integer=True, nonnegative=True)

    cases = [
        ("plain gaussian beta=1",   sp.exp(-1 * n ** 2)),
        ("scaled gaussian (gap-1)", 3 * sp.exp(-1 * n ** 2)),
        ("shifted theta (gap-2)",   sp.exp(-sp.Rational(1, 5) * n ** 2 - sp.Rational(1, 10) * n)),
        ("Gauss sum p=1 q=6",       sp.exp(2 * sp.pi * sp.I * 1 * n ** 2 / 6)),
    ]
    for desc, expr in cases:
        bm = best_match(expr, n, accept_fuzzy=True)
        if bm is None:
            print(f"{desc:<32} -> <no match>")
        else:
            tag = bm.degenerate or bm.reason or ""
            print(f"{desc:<32} -> {bm.kernel:<22} route={bm.route.value:<28} "
                  f"conf={bm.confidence:.2f}  cost={bm.total_cost:.1f}  {tag}")


if __name__ == "__main__":
    main()
