"""rkc.registry — kernel registry data.

Each `RegistryEntry` packages:

  - name           : unique registry key
  - family         : KernelFamily it belongs to (for fuzzy fallback)
  - match          : strict matcher (sympy AST -> dict|None)
  - fuzzy_match    : soft matcher (sympy AST -> (family, params, confidence)|None)
                     used in the second pass when no strict match wins.
  - degeneracy_check: dict -> reason str | None
  - per_term_cost  : (params, target_precision) -> float (ops/term)
  - notes          : human-readable description

Imported by `rkc.recognizer.recognize()`. v2 carries the same eleven kernels
as v1 with three structural changes:

  1. Each entry gets a `family` tag (THETA_LIKE, MOCK_THETA_LIKE, ...).
  2. Each entry gets a `per_term_cost` function (cf. insight §A7).
  3. The Gauss-sum degeneracy check is reachable via a `raw_coefficient`
     extracted BEFORE sympy auto-reduces 2/6 -> 1/3 (gap #5 in v2 plan).

The matchers themselves are unchanged from v1, with one exception: the
gaussian matcher returns its full degree-2 polynomial coefficients so the
fuzzy second pass can distinguish shifted (a1 != 0) from pure (a1 == 0)
gaussian without re-parsing.
"""
from __future__ import annotations

import math
import sympy as sp
from dataclasses import dataclass
from typing import Any, Callable, Optional

from .routing import KernelFamily
from . import costs


# ---------- match helpers ----------

def _safe(fn):
    def wrapped(expr, n):
        try:
            return fn(expr, n)
        except Exception:
            return None
    return wrapped


def _is_negative_number(x):
    try:
        return bool(sp.simplify(x).is_negative)
    except Exception:
        return False


@_safe
def _match_gaussian(expr, n):
    """exp(-beta n^2) or q^(n^2). Refuses linear-in-n terms (shifted theta)."""
    if expr.func == sp.Pow:
        base, exponent = expr.args
        if exponent.has(n):
            poly = sp.Poly(exponent, n)
            if poly.degree() == 2:
                a2, a1, a0 = poly.nth(2), poly.nth(1), poly.nth(0)
                if a1 == 0 and a0 == 0:
                    if base == sp.E or base == sp.exp(1):
                        if _is_negative_number(a2):
                            return {"beta": -a2}
                    elif a2 == 1:
                        if base.is_number and 0 < base < 1:
                            return {"beta": -sp.log(base), "q": base}
                        return {"q": base}
                    elif a2 == -1:
                        if base.is_number and base > 1:
                            return {"beta": sp.log(base), "q": 1 / base}
        return None
    if expr.func != sp.exp:
        return None
    arg = expr.args[0]
    if not arg.has(n):
        return None
    poly = sp.Poly(arg, n)
    if poly.degree() != 2:
        return None
    a2, a1, a0 = poly.nth(2), poly.nth(1), poly.nth(0)
    if a1 != 0 or a0 != 0:
        return None
    if not _is_negative_number(a2):
        return None
    return {"beta": -a2}


@_safe
def _match_bose_einstein(expr, n):
    if expr.func == sp.Pow and expr.args[1] == -1:
        inner = expr.args[0]
        if inner.func == sp.Add and len(inner.args) == 2:
            a, b = inner.args
            for one_term, exp_term in [(a, b), (b, a)]:
                if one_term == 1 and exp_term.func == sp.Mul:
                    coeffs = exp_term.args
                    if -1 in coeffs:
                        rest = sp.Mul(*[c for c in coeffs if c != -1])
                        if rest.func == sp.exp:
                            inner_arg = rest.args[0]
                            poly = sp.Poly(inner_arg, n) if inner_arg.has(n) else None
                            if poly is not None and poly.degree() == 1 and poly.nth(0) == 0:
                                lin = poly.nth(1)
                                if _is_negative_number(lin):
                                    return {"beta": -lin}
    return None


@_safe
def _match_lambert_divisor(expr, n):
    if expr.func != sp.Mul:
        return None
    if len(expr.args) != 2:
        as_frac = sp.fraction(expr)
        num, den = as_frac
    else:
        a, b = expr.args
        num, den = None, None
        for x, y in [(a, b), (b, a)]:
            if y.func == sp.Pow and y.args[1] == -1:
                num, den = x, y.args[0]
                break
        if num is None:
            return None
    try:
        v1n = sp.simplify(num.subs(n, 1))
        v2n = sp.simplify(num.subs(n, 2))
    except Exception:
        return None
    if v1n == 0:
        return None
    q_inferred = sp.simplify(v2n / v1n)
    if sp.simplify(num.subs(n, 3) - q_inferred ** 3) != 0:
        return None
    if sp.simplify(v1n - q_inferred) != 0:
        return None
    if sp.simplify(den - (1 - q_inferred ** n)) != 0:
        return None
    return {"q": q_inferred}


def _extract_mock_theta_denominator(expr, n):
    if expr.func != sp.Mul:
        return None
    num_q = None
    inv_parts = []
    other_parts = []
    for arg in expr.args:
        if arg.func == sp.Pow:
            base, expo = arg.args
            if expo == -1:
                inv_parts.append(base)
                continue
            if expo.has(n):
                try:
                    poly = sp.Poly(expo, n)
                except Exception:
                    poly = None
                if poly is not None and poly.degree() == 2 and poly.nth(1) == 0 and poly.nth(0) == 0:
                    a2 = poly.nth(2)
                    if a2 == 1:
                        num_q = base
                        continue
                    if a2 == -1 and base.is_number and base > 1:
                        num_q = sp.Rational(1) / base
                        continue
            other_parts.append(arg)
        else:
            other_parts.append(arg)
    if num_q is None or not inv_parts:
        return None
    return num_q, inv_parts, other_parts


@_safe
def _match_mock_theta_f3(expr, n):
    parsed = _extract_mock_theta_denominator(expr, n)
    if parsed is None:
        return None
    q, inv_parts, others = parsed
    if others:
        return None
    for inv in inv_parts:
        if inv.func == sp.Product:
            body, (kvar, lo, hi) = inv.args[0], inv.args[1]
            if not (lo == 1 and hi == n):
                continue
            if body.func == sp.Pow and body.args[1] == 2:
                inner = body.args[0]
                if sp.simplify(inner - (1 + q ** kvar)) == 0:
                    return {"q": q}
    return None


@_safe
def _match_mock_theta_f5(expr, n):
    parsed = _extract_mock_theta_denominator(expr, n)
    if parsed is None:
        return None
    q, inv_parts, others = parsed
    if others:
        return None
    for inv in inv_parts:
        if inv.func == sp.Product:
            body, (kvar, lo, hi) = inv.args[0], inv.args[1]
            if not (lo == 1 and hi == n):
                continue
            if sp.simplify(body - (1 + q ** kvar)) == 0:
                return {"q": q}
    return None


@_safe
def _match_mock_theta_f7(expr, n):
    parsed = _extract_mock_theta_denominator(expr, n)
    if parsed is None:
        return None
    q, inv_parts, others = parsed
    if others:
        return None
    for inv in inv_parts:
        if inv.func == sp.Product:
            body, (kvar, lo, hi) = inv.args[0], inv.args[1]
            if not (lo == 1 and sp.simplify(hi - (2 * n + 1)) == 0):
                continue
            if sp.simplify(body - (1 + q ** kvar)) == 0:
                return {"q": q}
    return None


def _try_match_triangular_q_power(arg, n):
    if arg.func != sp.Pow:
        return None
    base, expo = arg.args
    if not expo.has(n):
        return None
    try:
        poly = sp.Poly(expo, n)
    except Exception:
        return None
    if poly.degree() != 2 or poly.nth(0) != 0:
        return None
    a2, a1 = poly.nth(2), poly.nth(1)
    if a2 == sp.Rational(1, 2) and a1 == sp.Rational(1, 2):
        return base
    if a2 == sp.Rational(-1, 2) and a1 == sp.Rational(-1, 2):
        if base.is_number and base > 0:
            return sp.Rational(1) / base
    return None


@_safe
def _match_partial_theta(expr, n):
    sign_part = None
    q_part = None
    rest = []
    if expr.func == sp.Mul:
        for arg in expr.args:
            if arg.func == sp.Pow:
                base, expo = arg.args
                if base == -1 and expo == n:
                    sign_part = -1
                    continue
                q_try = _try_match_triangular_q_power(arg, n)
                if q_try is not None:
                    q_part = q_try
                    continue
            rest.append(arg)
    elif expr.func == sp.Pow:
        q_part = _try_match_triangular_q_power(expr, n)
        if q_part is not None:
            sign_part = 1
    if q_part is None:
        return None
    if rest:
        return None
    return {"q": q_part, "alternating_sign": sign_part == -1}


@_safe
def _match_q_pochhammer_infty(expr, n):
    if expr.func != sp.Product:
        return None
    body, (kvar, lo, hi) = expr.args[0], expr.args[1]
    if not (lo == 0 and hi == sp.oo):
        return None
    if body.func != sp.Add or len(body.args) != 2:
        return None
    one_part = None
    other = None
    for t in body.args:
        if not t.has(kvar):
            one_part = t
        else:
            other = t
    if one_part is None or other is None:
        return None
    if sp.simplify(one_part - 1) != 0:
        return None
    try:
        v0 = sp.simplify(other.subs(kvar, 0))
        v1 = sp.simplify(other.subs(kvar, 1))
    except Exception:
        return None
    if v0 == 0:
        return None
    a = -v0
    q = sp.simplify(v1 / v0)
    v2 = sp.simplify(other.subs(kvar, 2))
    expected = -a * q ** 2
    if sp.simplify(v2 - expected) != 0:
        return None
    return {"a": a, "q": q}


@_safe
def _match_eisenstein_E2k(expr, n):
    if expr.func == sp.Mul:
        sigma_part = None
        qn_part = None
        rest = []
        for arg in expr.args:
            if arg.func == sp.divisor_sigma:
                sigma_part = arg
            elif arg.func == sp.Pow and arg.args[1] == n:
                qn_part = arg
            else:
                rest.append(arg)
        if sigma_part is not None and qn_part is not None and not rest:
            sigma_args = sigma_part.args
            if len(sigma_args) >= 1 and sigma_args[0] == n:
                k_index = sigma_args[1] if len(sigma_args) == 2 else 1
                k_index_val = sp.simplify(k_index)
                if k_index_val.is_integer and int(k_index_val) % 2 == 1:
                    weight = int(k_index_val) + 1
                    q = qn_part.args[0]
                    return {"q": q, "weight": weight}
    return None


@_safe
def _match_dirichlet_L(expr, n):
    if expr.func == sp.Mul and len(expr.args) == 2:
        a, b = expr.args
        for chi_term, n_term in [(a, b), (b, a)]:
            if chi_term.func == sp.Function("chi") or (
                hasattr(chi_term, 'func') and chi_term.func.__name__ == "chi"
            ):
                if n_term.func == sp.Pow:
                    base, expo = n_term.args
                    if base == n and expo.func == sp.Mul and -1 in expo.args:
                        rest = sp.Mul(*[c for c in expo.args if c != -1])
                        return {"s": rest, "chi": chi_term.func.__name__}
                    if base == n and getattr(expo, 'is_negative', False):
                        return {"s": -expo, "chi": chi_term.func.__name__}
    return None


@_safe
def _match_gauss_sum(expr, n):
    """exp(2 pi i p n^2 / q). Now returns the RAW Rational coefficient too
    so the degeneracy check can reach the gcd branch even after sympy
    auto-reduces (see _gauss_sum_degeneracy_v2).
    """
    if expr.func != sp.exp:
        return None
    arg = expr.args[0]
    if not arg.has(n):
        return None
    poly = sp.Poly(arg, n)
    if poly.degree() != 2:
        return None
    a2 = poly.nth(2)
    a1 = poly.nth(1)
    a0 = poly.nth(0)
    if a1 != 0 or a0 != 0:
        return None
    try:
        ratio = sp.simplify(a2 / (2 * sp.pi * sp.I))
    except Exception:
        return None
    if ratio == 0:
        return None
    if ratio.is_Rational:
        p, q = int(ratio.p), int(ratio.q)
        return {"p": p, "q": q, "ratio_pre_reduction": ratio}
    return None


# ---------- raw (pre-sympy) AST walker for Gauss-sum gcd fix ----------
# v1's diary noted that the gcd-based Gauss-sum degeneracy is unreachable
# because sympy auto-reduces 2*n^2/6 -> n^2/3 before the matcher sees it.
# Fix: walk the expression BEFORE sympify (or peek through Mul args before
# simplification) and stash the unreduced numerator/denominator.

def extract_raw_gauss_coefficient(expr_or_str, n) -> Optional[tuple[int, int]]:
    """Pre-simplification extractor for the rational coefficient of n^2 in
    exp(2 pi i * <rat> * n^2). Returns (p_raw, q_raw) WITHOUT gcd reduction,
    or None if the structure doesn't match.

    Accepts either:
      - a string like "exp(2*pi*I*2*n**2/6)" (preferred — strings preserve
        the user's intent before sympy ever touches the coefficient)
      - a sympy expression where the coefficient was passed as a Rational
        with `gcd=False` flag (rare in practice — strings are simpler)

    Strategy for the string path: walk the AST of the parsed expression with
    `evaluate=False`, locate the imaginary quadratic exponent, and pull out
    the numerator and denominator of the coefficient as they were written.
    """
    if isinstance(expr_or_str, str):
        try:
            expr = sp.sympify(expr_or_str, evaluate=False)
        except Exception:
            return None
    else:
        expr = expr_or_str
    if expr.func != sp.exp:
        return None
    arg = expr.args[0]
    # arg should be Mul(... , n**2, ...) with a constant factor 2*pi*I*p/q
    # Walk Mul args; collect everything that isn't n^2, then split into
    # numerator and denominator. Compare on symbol *name* not identity —
    # the parsed `n` is a fresh Symbol without the caller's assumptions, so
    # `a.args[0] == n` fails on assumption mismatch.
    if arg.func != sp.Mul:
        return None
    n_name = n.name if hasattr(n, "name") else str(n)
    quad_factor = None
    other_factors = []
    for a in arg.args:
        if a.func == sp.Pow and getattr(a.args[0], "name", None) == n_name and a.args[1] == 2:
            quad_factor = a
        else:
            other_factors.append(a)
    if quad_factor is None:
        return None
    # Combine other_factors back into a single product, then separate the
    # numerator and denominator (each Pow with exponent -1 is a denominator).
    # We must absorb exactly one each of (2, pi, I) into the constant prefactor;
    # the remaining integer / rational factors go into p_raw / q_raw.
    p_raw = 1
    q_raw = 1
    found_pi = 0
    found_I = 0
    consumed_two = False
    for f in other_factors:
        if f == sp.pi:
            found_pi += 1
        elif f == sp.I:
            found_I += 1
        elif f.is_Integer:
            if int(f) == 2 and not consumed_two:
                consumed_two = True   # absorb one 2 into "2*pi*I"
                continue
            p_raw *= int(f)
        elif f.is_Rational:
            p_raw *= f.p
            q_raw *= f.q
        elif f.func == sp.Pow and f.args[1] == -1:
            base = f.args[0]
            if base.is_Integer:
                q_raw *= int(base)
            elif base.is_Rational:
                q_raw *= base.p
                p_raw *= base.q
            else:
                return None
        else:
            return None
    if not (found_pi == 1 and found_I == 1 and consumed_two):
        return None
    return (p_raw, q_raw)


# ---------- fuzzy matchers (soft second-pass) ----------
# These run ONLY when no strict match wins. They emit a kernel-family-ish
# warning with a confidence score, not a hard route recommendation.

@_safe
def _fuzzy_match_shifted_theta(expr, n):
    """q^(quadratic in n) WITH non-zero linear or constant term, or
    exp(-beta n^2 + linear n + ...). Family: THETA_LIKE, confidence 0.6.

    This is the gap-2 fuzzy fallback. v1 documented `q^(n^2+n)` as
    correctly REJECTED by the strict gaussian matcher; that's still the
    right call, but v2 lifts the rejection into a soft 'theta-like' hint
    so a downstream operator can choose to apply the shifted-theta dual
    if they so wish.
    """
    arg = None
    base = None
    if expr.func == sp.Pow:
        base, exponent = expr.args
        if exponent.has(n):
            arg = exponent
    elif expr.func == sp.exp:
        a = expr.args[0]
        if a.has(n):
            arg = a
            base = sp.E
    if arg is None:
        return None
    try:
        poly = sp.Poly(arg, n)
    except Exception:
        return None
    if poly.degree() != 2:
        return None
    a2, a1, a0 = poly.nth(2), poly.nth(1), poly.nth(0)
    if a1 == 0 and a0 == 0:
        return None  # strict match would have caught this
    return {
        "base": base, "a2": a2, "a1": a1, "a0": a0,
        "shape": "q^(a2*n^2 + a1*n + a0)",
    }


@_safe
def _fuzzy_match_mock_theta_ish(expr, n):
    """q^(quadratic) / Π(weird denom) — anything where the numerator looks
    like a theta core but the denominator doesn't strictly match f3/f5/f7,
    OR there's an extra factor that strict matching rejects.
    Family: MOCK_THETA_LIKE, confidence 0.5.
    """
    if expr.func != sp.Mul:
        return None
    parsed = _extract_mock_theta_denominator(expr, n)
    if parsed is None:
        return None
    q, inv_parts, others = parsed
    # If `others` is non-empty (extra unrecognized factor) OR the inv_parts
    # contain a Product but with the wrong index range/body, this is fuzzy.
    has_product_denom = any(
        (hasattr(inv, 'func') and inv.func == sp.Product) for inv in inv_parts
    )
    if not has_product_denom and not others:
        return None
    # Extra factor case is the canonical 'mock-f3 * cos(n)' adversarial
    if others:
        return {"q": q, "extra_factors": [str(o) for o in others],
                "shape": "theta-core * extra-factor"}
    if has_product_denom:
        return {"q": q, "shape": "theta-core / non-standard-product"}
    return None


@_safe
def _fuzzy_match_lambert_ish(expr, n):
    """q^n / (1 - q^(linear-in-n)) where the linear coefficient is not 1.
    Family: LAMBERT_LIKE, confidence 0.55.
    Catches the adversarial `q^n / (1 - q^(2n))` case.
    """
    if expr.func != sp.Mul:
        return None
    # find a Pow with -1 exponent
    den_inner = None
    num = None
    for a in expr.args:
        if a.func == sp.Pow and a.args[1] == -1:
            den_inner = a.args[0]
        else:
            num = a if num is None else num * a
    if den_inner is None or num is None:
        return None
    # numerator should be q^(linear in n)
    if num.func != sp.Pow:
        return None
    base_num, expo_num = num.args
    if not expo_num.has(n):
        return None
    try:
        pn = sp.Poly(expo_num, n)
    except Exception:
        return None
    if pn.degree() != 1:
        return None
    # denominator inner: 1 - base^(c*n)
    if den_inner.func != sp.Add or len(den_inner.args) != 2:
        return None
    found_neg_pow = None
    found_one = False
    for term in den_inner.args:
        if term == 1:
            found_one = True
        elif term.func == sp.Mul and -1 in term.args:
            rest = sp.Mul(*[c for c in term.args if c != -1])
            if rest.func == sp.Pow:
                found_neg_pow = rest
        elif term.func == sp.Pow:
            # could be base^(c*n) alone with implicit -1 sign... unusual
            pass
    if not found_one or found_neg_pow is None:
        return None
    base_den, expo_den = found_neg_pow.args
    if not expo_den.has(n):
        return None
    try:
        pd = sp.Poly(expo_den, n)
    except Exception:
        return None
    if pd.degree() != 1:
        return None
    # if bases match and the denominator exponent != n (i.e. coefficient !=1),
    # it's lambert-shaped but NOT a strict lambert hit
    if sp.simplify(base_num - base_den) != 0:
        return None
    if pn.nth(1) == 1 and pd.nth(1) == 1 and pn.nth(0) == 0 and pd.nth(0) == 0:
        return None  # this would be the strict lambert case
    return {"q": base_num,
            "num_exponent_coeff": pn.nth(1),
            "den_exponent_coeff": pd.nth(1),
            "shape": "q^(a*n) / (1 - q^(b*n)) with a != 1 or b != 1"}


# ---------- routing & cost predictors (ported from v1, lightly extended) ----------

from mpmath import mpf, exp, sqrt, pi, log, ceil  # noqa: E402

from .routing import Route, RoutingResult, degenerate_result  # noqa: E402


def _route_gaussian(params, tol):
    beta = mpf(params.get("beta", -log(mpf(params["q"])) if "q" in params else 1))
    direct_cost = int(ceil(sqrt(-log(mpf(tol)) / beta))) + 1
    dual_beta = pi * pi / beta
    dual_cost = int(ceil(sqrt(-log(mpf(tol)) / dual_beta))) + 1
    route = Route.DUAL if dual_cost < direct_cost else Route.DIRECT
    return {"route": route, "cost_direct": direct_cost, "cost_dual": dual_cost,
            "num_terms": min(direct_cost, dual_cost) if dual_cost > 0 else direct_cost}


def _route_bose_einstein(params, tol):
    beta = mpf(params["beta"])
    rhs = -log(mpf(tol) * (1 - exp(-beta)))
    direct_cost = max(1, int(ceil(rhs / beta)))
    dual_beta = 4 * pi * pi / beta
    rhs2 = -log(mpf(tol) * (1 - exp(-dual_beta)))
    dual_cost = max(1, int(ceil(rhs2 / dual_beta)))
    route = Route.DUAL if dual_cost < direct_cost else Route.DIRECT
    return {"route": route, "cost_direct": direct_cost, "cost_dual": dual_cost,
            "num_terms": min(direct_cost, dual_cost)}


def _route_lambert(params, tol):
    q = mpf(params["q"])
    if q >= 1:
        return {"route": Route.DEGENERATE, "cost_direct": -1, "cost_dual": -1,
                "reason": "Lambert series diverges for |q| >= 1", "num_terms": -1}
    direct_cost = max(1, int(ceil(log(mpf(tol) * (1 - q)) / log(q))))
    neg_log_q = -log(q)
    q_prime = exp(-4 * pi * pi / neg_log_q)
    if q_prime > 0 and q_prime < 1:
        dual_cost = max(1, int(ceil(log(mpf(tol) * (1 - q_prime)) / log(q_prime))))
    else:
        dual_cost = direct_cost + 1
    route = Route.DUAL if dual_cost < direct_cost else Route.DIRECT
    return {"route": route, "cost_direct": direct_cost, "cost_dual": dual_cost,
            "num_terms": min(direct_cost, dual_cost)}


def _route_mock_theta(params, tol):
    q = mpf(params["q"])
    if q <= 0 or q >= 1:
        return {"route": Route.DEGENERATE, "cost_direct": -1, "cost_dual": -1,
                "reason": "Mock theta requires 0 < q < 1", "num_terms": -1}
    direct_cost = max(1, int(ceil(sqrt(-log(mpf(tol)) / (-log(q))))))
    if -log(q) < pi:
        return {"route": Route.MODULAR_COMPLETION_REQUIRED,
                "cost_direct": direct_cost, "cost_dual": -1,
                "reason": "near q=1 cusp; Zwegers completion needed for modular accuracy",
                "num_terms": direct_cost}
    return {"route": Route.DIRECT, "cost_direct": direct_cost, "cost_dual": -1,
            "num_terms": direct_cost}


def _route_partial_theta(params, tol):
    q = mpf(params["q"])
    if q <= 0 or q >= 1:
        return {"route": Route.DEGENERATE, "cost_direct": -1, "cost_dual": -1,
                "reason": "Partial theta requires 0 < q < 1", "num_terms": -1}
    rhs = -log(mpf(tol)) / (-log(q))
    direct_cost = max(1, int(ceil((sqrt(1 + 8 * rhs) - 1) / 2)))
    return {"route": Route.DIRECT, "cost_direct": direct_cost, "cost_dual": -1,
            "reason": "no clean dual (one-sided in n); direct truncation suffices",
            "num_terms": direct_cost}


def _route_q_pochhammer(params, tol):
    q = mpf(params["q"])
    a = params.get("a", 1)
    if q <= 0 or q >= 1:
        return {"route": Route.DEGENERATE, "cost_direct": -1, "cost_dual": -1,
                "reason": "q-Pochhammer (a;q)_inf requires |q| < 1", "num_terms": -1}
    a_abs = abs(mpf(a)) if not isinstance(a, sp.Symbol) else mpf(1)
    if a_abs == 0:
        return {"route": Route.DEGENERATE, "cost_direct": 1, "cost_dual": -1,
                "reason": "a = 0 -> product is 1", "num_terms": 1}
    rhs = log(mpf(tol) / a_abs) / log(q)
    direct_cost = max(1, int(ceil(rhs)))
    return {"route": Route.DIRECT, "cost_direct": direct_cost, "cost_dual": -1,
            "reason": "Pochhammer converges geometrically in k",
            "num_terms": direct_cost}


def _route_eisenstein(params, tol):
    q = mpf(params["q"])
    if q <= 0 or q >= 1:
        return {"route": Route.DEGENERATE, "cost_direct": -1, "cost_dual": -1,
                "reason": "Eisenstein requires 0 < q < 1", "num_terms": -1}
    weight = int(params.get("weight", 4))
    K = mpf(1)
    while True:
        bound = (K ** weight) * (q ** K)
        if bound < mpf(tol):
            break
        K *= 2
        if K > mpf(1e8):
            break
    direct_cost = int(K)
    if -log(q) < pi:
        dual_cost = 1 + int(ceil(sqrt(-log(mpf(tol)) / (pi * pi / (-log(q))))))
        return {"route": Route.DUAL, "cost_direct": direct_cost,
                "cost_dual": dual_cost,
                "reason": "near q=1; use modular S-transform of E_{2k}",
                "num_terms": min(direct_cost, dual_cost)}
    return {"route": Route.DIRECT, "cost_direct": direct_cost, "cost_dual": -1,
            "num_terms": direct_cost}


def _route_dirichlet_L(params, tol):
    s = params["s"]
    try:
        s_val = float(sp.re(s)) if hasattr(s, "is_Number") and s.is_Number else float(s)
    except Exception:
        s_val = 1.0
    if s_val <= 0:
        return {"route": Route.DUAL, "cost_direct": -1, "cost_dual": 100,
                "reason": "Re(s) <= 0; use functional equation L(s) = chi-factor * L(1-s)",
                "num_terms": 100}
    if s_val > 1:
        try:
            N = int(math.ceil((1.0 / (float(tol) * (s_val - 1))) ** (1.0 / (s_val - 1))))
        except Exception:
            N = 10**6
        if s_val < 0.5:
            return {"route": Route.DUAL, "cost_direct": N, "cost_dual": 100,
                    "reason": "Re(s) < 1/2; functional-equation reflection is cheaper",
                    "num_terms": min(N, 100)}
        return {"route": Route.DIRECT, "cost_direct": N, "cost_dual": 100,
                "num_terms": N}
    return {"route": Route.DUAL, "cost_direct": -1, "cost_dual": 100,
            "reason": "0 < Re(s) <= 1; direct sum at boundary, prefer functional equation",
            "num_terms": 100}


def _route_gauss_sum(params, tol):
    p, q = params["p"], params["q"]
    return {"route": Route.DIRECT, "cost_direct": q, "cost_dual": -1,
            "reason": f"Gauss sum of length {q}; direct evaluation",
            "num_terms": q}


# ---------- degeneracy checks ----------

def _no_degeneracy(params):
    return None


def _gauss_sum_degeneracy_v2(params):
    """v2: in addition to v1's q ≡ 2 (mod 4) and gcd checks on the
    POST-reduction (p, q), also check the RAW pre-reduction coefficient if
    it was passed in `raw_pq`. That's how the gcd branch becomes reachable
    when the user constructs the AST through `extract_raw_gauss_coefficient`.
    """
    p, q = params["p"], params["q"]
    if q <= 0:
        return f"q = {q} is not a positive modulus"
    raw_pq = params.get("raw_pq")
    if raw_pq is not None:
        p_raw, q_raw = raw_pq
        g_raw = math.gcd(abs(p_raw), q_raw)
        if g_raw > 1 and (p_raw, q_raw) != (p, q):
            return (f"gcd(p_raw={p_raw}, q_raw={q_raw}) = {g_raw} > 1; "
                    f"reduces to ({p_raw // g_raw}, {q_raw // g_raw}); "
                    f"raw form preserved a degeneracy hidden by sympy auto-reduction")
    g = math.gcd(abs(p), q)
    if g > 1:
        return f"gcd(p={p}, q={q}) = {g} > 1; sum reduces to a smaller Gauss sum (possibly zero)"
    if q % 4 == 2:
        return f"q={q} ≡ 2 (mod 4); G(p,q) = 0 identically (silent-zero hazard, CANDIDATE_INSIGHTS §A4)"
    return None


def _q_in_unit_disk(params):
    q = params.get("q")
    if q is None:
        return None
    try:
        qv = mpf(q)
    except Exception:
        return None
    if qv <= 0:
        return f"q = {qv} not in (0, 1)"
    if qv >= 1:
        return f"q = {qv} >= 1; series diverges"
    return None


def _pochhammer_degeneracy(params):
    deg = _q_in_unit_disk(params)
    if deg:
        return deg
    a = params.get("a", 1)
    if a == 0:
        return "a = 0; (0;q)_inf = 1 trivially"
    if sp.simplify(sp.sympify(a) - 1) == 0:
        return "a = 1; (1;q)_inf = 0 (zero factor at k=0)"
    return None


def _eisenstein_degeneracy(params):
    deg = _q_in_unit_disk(params)
    if deg:
        return deg
    weight = params.get("weight", 4)
    if weight % 2 != 0 or weight < 2:
        return f"Eisenstein E_{weight} only defined for positive even weight"
    return None


# ---------- registry entry dataclass ----------

@dataclass
class RegistryEntry:
    name: str
    family: KernelFamily
    match: Callable[[sp.Expr, sp.Symbol], Optional[dict]]
    recommend_route: Callable[[dict, float], dict]
    degeneracy_check: Callable[[dict], Optional[str]]
    per_term_cost: Callable[[dict, float], float]
    notes: str = ""


REGISTRY: list[RegistryEntry] = [
    RegistryEntry("gaussian_quadratic", KernelFamily.THETA_LIKE,
                  _match_gaussian, _route_gaussian, _no_degeneracy,
                  costs.per_term_gaussian,
                  "theta_3 family; classic Poisson summation / modular S dual"),
    RegistryEntry("bose_einstein_geometric", KernelFamily.LAMBERT_LIKE,
                  _match_bose_einstein, _route_bose_einstein, _no_degeneracy,
                  costs.per_term_bose,
                  "Dedekind-eta modular S dual when beta is small"),
    RegistryEntry("lambert_divisor", KernelFamily.LAMBERT_LIKE,
                  _match_lambert_divisor, _route_lambert, _q_in_unit_disk,
                  costs.per_term_lambert,
                  "Eisenstein-form dual when q is near 1"),
    RegistryEntry("mock_theta_f3", KernelFamily.MOCK_THETA_LIKE,
                  _match_mock_theta_f3, _route_mock_theta, _q_in_unit_disk,
                  costs.per_term_mock_theta,
                  "3rd-order mock theta f; modular completion via Zwegers required near cusp"),
    RegistryEntry("mock_theta_f5", KernelFamily.MOCK_THETA_LIKE,
                  _match_mock_theta_f5, _route_mock_theta, _q_in_unit_disk,
                  costs.per_term_mock_theta,
                  "5th-order family representative; modular completion required near cusp"),
    RegistryEntry("mock_theta_f7", KernelFamily.MOCK_THETA_LIKE,
                  _match_mock_theta_f7, _route_mock_theta, _q_in_unit_disk,
                  costs.per_term_mock_theta,
                  "7th-order family representative; modular completion required near cusp"),
    RegistryEntry("partial_theta", KernelFamily.PARTIAL_THETA_LIKE,
                  _match_partial_theta, _route_partial_theta, _q_in_unit_disk,
                  costs.per_term_partial_theta,
                  "one-sided over n>=0; no clean dual"),
    RegistryEntry("q_pochhammer_infty", KernelFamily.POCHHAMMER_LIKE,
                  _match_q_pochhammer_infty, _route_q_pochhammer, _pochhammer_degeneracy,
                  costs.per_term_q_pochhammer,
                  "prod_{k>=0}(1 - a q^k); direct truncation OK for |q|<1"),
    RegistryEntry("eisenstein_E2k", KernelFamily.EISENSTEIN_LIKE,
                  _match_eisenstein_E2k, _route_eisenstein, _eisenstein_degeneracy,
                  costs.per_term_eisenstein,
                  "modular S-transform for q near 1; explicit even-weight Eisenstein E_{2k}"),
    RegistryEntry("dirichlet_L", KernelFamily.UNKNOWN,
                  _match_dirichlet_L, _route_dirichlet_L, _no_degeneracy,
                  costs.per_term_dirichlet,
                  "functional equation reflection across Re(s) = 1/2"),
    RegistryEntry("gauss_sum", KernelFamily.GAUSS_SUM_LIKE,
                  _match_gauss_sum, _route_gauss_sum, _gauss_sum_degeneracy_v2,
                  costs.per_term_gauss_sum,
                  "silent-zero hazard at q ≡ 2 (mod 4) — see CANDIDATE_INSIGHTS §A4"),
]


# Fuzzy matchers run only when no strict match wins. (family, matcher_fn, confidence)
FUZZY_MATCHERS = [
    (KernelFamily.THETA_LIKE,        _fuzzy_match_shifted_theta, 0.6),
    (KernelFamily.MOCK_THETA_LIKE,   _fuzzy_match_mock_theta_ish, 0.5),
    (KernelFamily.LAMBERT_LIKE,      _fuzzy_match_lambert_ish,    0.55),
]
