"""
Experiment 13 — Kernel-Fingerprint Recognizer v1.

Expansion of experiment 09's three-kernel registry to ~10 kernels, with three
deliberate additions over v0:

  1. A wider canonical zoo — mock theta f (3rd order), f_5 (5th), f_7 (7th),
     partial theta, q-Pochhammer (a;q)_inf, Eisenstein E_{2k}, Dirichlet
     L-series, Gauss sums.
  2. A *route* enum that distinguishes DIRECT / DUAL / DEGENERATE /
     MODULAR_COMPLETION_REQUIRED instead of v0's binary DIRECT/DUAL.
  3. A per-entry `degeneracy_check()` that returns None or a reason string,
     hardcoded against the silent-zero hazard documented in CANDIDATE_INSIGHTS
     §A4 (most notably Gauss sums with q ≡ 2 (mod 4) which evaluate to 0
     identically).

The v0 file is kept untouched as a stable reference; this file imports nothing
from it so a downstream user can adopt v1 independently. Test cases here are
sanity checks only — the routing benchmark with precision/recall numbers lives
in experiment 14.

Registry entries (in order):
  * gaussian_quadratic              q^(n^2)-shaped, direct or theta-S dual
  * bose_einstein_geometric         1/(1-e^(-beta n)), Dedekind-eta dual
  * lambert_divisor                 q^n/(1-q^n), Eisenstein-style dual
  * mock_theta_f3                   q^(n^2) / prod (1+q^k)^2; modular completion req'd
  * mock_theta_f5                   q^(n^2) / (-q;q)_n (5th order family); modular completion req'd
  * mock_theta_f7                   q^(n^2) / (-q;q)_(2n+1) (7th order family); modular completion req'd
  * partial_theta                   (-1)^n q^(n(n+1)/2), positive-n only; no clean dual
  * q_pochhammer_infty              prod_{k>=0} (1 - a q^k); direct converges fast for |q|<1
  * eisenstein_E2k                  1 - (2k/B_{2k}) sum sigma_{2k-1}(n) q^n; modular S-dual when q near 1
  * dirichlet_L                     sum chi(n) n^(-s); functional-equation dual when Re(s) < 1/2
  * gauss_sum                       sum_{n=0..q-1} exp(2 pi i p n^2 / q); DEGENERATE at q ≡ 2 (mod 4)

Routing semantics:
  DIRECT                        — converges fast as written, use the summand.
  DUAL                          — exact closed-form / modular transform exists; cheaper.
  MODULAR_COMPLETION_REQUIRED   — no clean dual; non-holomorphic Eichler integral needed
                                  to repair modular behavior. Recognizer flags but does
                                  not perform the completion itself.
  DEGENERATE                    — kernel evaluates to a trivial value (zero, infinity)
                                  for the given parameters; do NOT report a numerical
                                  routing recommendation — the answer is the trivial value.

This is the cleanest place where the §A4 silent-zero defense lives: the
degeneracy_check fires BEFORE any cost predictor or route recommender, and the
result short-circuits the rest of the pipeline.
"""
from __future__ import annotations

import math
import sympy as sp
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Optional
from mpmath import mp, mpf, mpc, exp, sqrt, pi, log, erfc, ceil


# ---------- routing enum ----------

class Route(str, Enum):
    DIRECT = "DIRECT"
    DUAL = "DUAL"
    MODULAR_COMPLETION_REQUIRED = "MODULAR_COMPLETION_REQUIRED"
    DEGENERATE = "DEGENERATE"


# ---------- registry entry ----------

@dataclass
class RegistryEntry:
    name: str
    match: Callable[[sp.Expr, sp.Symbol], Optional[dict]]
    recommend_route: Callable[[dict, mpf], dict]
    degeneracy_check: Callable[[dict], Optional[str]]
    notes: str = ""


# ---------- match helpers ----------
# Conventions:
#   - all matchers receive a sympy Expr representing the *summand* (the body
#     of a Sum over the dummy `n`) plus the dummy itself.
#   - matchers return None on miss; on hit they return a dict of extracted
#     parameters (numerical or symbolic, depending on whether the kernel takes
#     a symbolic q vs a numerical one).
#
# All matchers run in a try/except to guarantee that an exotic AST never
# crashes the recognizer; downstream code only sees None / dict.


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
    """E(n) summand exp(-beta n^2) or q^(n^2) with q = e^{-beta}.

    We refuse to match if the polynomial argument in the exponent contains a
    linear term in n — that's a SHIFTED gaussian (shifted theta), not the
    pure quadratic kernel of theta_3.  This is one of the adversarial cases
    in the benchmark.
    """
    if expr.func == sp.Pow:
        base, exponent = expr.args
        # q^(n^2): exponent polynomial in n must be n^2 (no linear part)
        if exponent.has(n):
            poly = sp.Poly(exponent, n)
            if poly.degree() == 2:
                a2 = poly.nth(2)
                a1 = poly.nth(1)
                a0 = poly.nth(0)
                if a1 == 0 and a0 == 0:
                    # exponent is c * n^2 for some constant c
                    # case A: exp(c n^2) with base = e
                    if base == sp.E or base == sp.exp(1):
                        if _is_negative_number(a2):
                            return {"beta": -a2}
                    # case B: q^(c n^2) with rational base: q^(n^2) means c=1 base in (0,1)
                    elif a2 == 1:
                        # q^(n^2)
                        if base.is_number and 0 < base < 1:
                            return {"beta": -sp.log(base), "q": base}
                        return {"q": base}
                    elif a2 == -1:
                        # q^(-n^2) with q probably an integer >1; treat as theta with beta = log q
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
        return None  # shifted / off-center — refuse
    if not _is_negative_number(a2):
        return None
    return {"beta": -a2}


@_safe
def _match_bose_einstein(expr, n):
    """1 / (1 - exp(-beta n)) summand for log Z of a Bose oscillator."""
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
    """q^n / (1 - q^n).

    Robust to sympy's rewriting: when the base is an integer rational like
    1/3, sympy will write (1/3)^n as 3^(-n). We test the function's value at
    n=1 and n=2 to recover q regardless of internal form.
    """
    if expr.func != sp.Mul:
        return None
    # peel into numerator * denominator^(-1)
    if len(expr.args) != 2:
        # could be many; try grouping
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
    # `num` should be q^n; sample at n=1 and n=2 to recover q
    try:
        v1n = sp.simplify(num.subs(n, 1))
        v2n = sp.simplify(num.subs(n, 2))
    except Exception:
        return None
    if v1n == 0:
        return None
    q_inferred = sp.simplify(v2n / v1n)
    # `num` should equal q^n; verify at n=3
    if sp.simplify(num.subs(n, 3) - q_inferred ** 3) != 0:
        return None
    # also v1n should be q (not c*q for some c)
    if sp.simplify(v1n - q_inferred) != 0:
        return None
    # denominator should be (1 - q^n)
    if sp.simplify(den - (1 - q_inferred ** n)) != 0:
        return None
    return {"q": q_inferred}


# Mock theta f, f_5, f_7 — these share a common structural fingerprint:
#   q^(n^2) divided by a product whose factors are (1 +/- q^(linear in k)).
# We distinguish them by inspecting the denominator structure:
#   f3:  prod_{k=1..n} (1 + q^k) ^ 2
#   f5:  prod_{k=1..n} (1 + q^k)            (single power; "5th order family")
#   f7:  prod_{k=1..2n+1} (1 + q^k)         (range up to 2n+1 instead of n)
#
# The historical 5th- and 7th-order mock thetas have many sibling forms; here we
# pick canonical representatives whose denominators have these characteristic
# index ranges. The benchmark perturbations test against minor reshufflings
# (sign-flip, index reparameterization) without breaking these specific
# fingerprints.

def _extract_mock_theta_denominator(expr, n):
    """Return (q, inv_parts, others) for an expr of shape
    q^(n^2) * prod-thing^{-1}, else None.

    Handles the sympy quirk where rational bases get rewritten with negative
    exponents: (1/2)^(n^2) becomes 2^(-n^2). We recover q either way.
    inv_parts is a list of sympy expressions that appeared as denominators.
    """
    if expr.func != sp.Mul:
        return None
    num_q = None
    inv_parts = []
    other_parts = []
    for arg in expr.args:
        if arg.func == sp.Pow:
            base, expo = arg.args
            # candidate denominator: Pow(thing, -1) where thing is a Product
            if expo == -1:
                inv_parts.append(base)
                continue
            # candidate numerator q^(n^2) or its rewritten form base^(-n^2)
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
                        # rewritten (1/base)^(n^2)
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
    """q^(n^2) / prod_{k=1..n} (1 + q^k)^2 — 3rd order mock theta f."""
    parsed = _extract_mock_theta_denominator(expr, n)
    if parsed is None:
        return None
    q, inv_parts, others = parsed
    if others:
        return None
    # Look for a Product over k from 1 to n of (1 + q^k)^2
    for inv in inv_parts:
        if inv.func == sp.Product:
            body, (kvar, lo, hi) = inv.args[0], inv.args[1]
            if not (lo == 1 and hi == n):
                continue
            # body should be (1 + q^k)^2
            if body.func == sp.Pow and body.args[1] == 2:
                inner = body.args[0]
                if sp.simplify(inner - (1 + q ** kvar)) == 0:
                    return {"q": q}
    return None


@_safe
def _match_mock_theta_f5(expr, n):
    """q^(n^2) / prod_{k=1..n} (1 + q^k)  — a 5th-order-family representative."""
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
            # body should be (1 + q^k) (no outer power, i.e. exponent 1)
            if sp.simplify(body - (1 + q ** kvar)) == 0:
                return {"q": q}
    return None


@_safe
def _match_mock_theta_f7(expr, n):
    """q^(n^2) / prod_{k=1..2n+1} (1 + q^k)  — a 7th-order-family representative."""
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
    """Return q if `arg` looks like q^(n(n+1)/2), accounting for sympy's
    rewriting of (1/x)^(...) as x^(-...)."""
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
    """(-1)^n q^(n(n+1)/2). One-sided (positive n only); the recognizer also
    accepts an inferred-sign form (positive coefficient + q^(triangular)).

    We refuse to match the FULL theta line q^(n^2) — that would be the
    gaussian/theta_3 entry. The triangular exponent n(n+1)/2 is the
    distinguishing fingerprint.
    """
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
    """(a; q)_infty = prod_{k>=0} (1 - a q^k).

    Robust to sympy's tendency to combine numerics: 1 - (1/2) (1/3)^k may
    appear as 1 - 1/(2 * 3^k) or 1 - (1/6)^k * something. We treat the body
    as a polynomial in q^k once we have established it's an Add 1 + (k-dep
    term).
    """
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
    # one_part must equal 1
    if sp.simplify(one_part - 1) != 0:
        return None
    # other = -a * q^kvar  for some constants a, q (which may be Rationals
    # combined into a single power). Strategy: evaluate other at kvar=0 and
    # kvar=1, then a = -other(0), and q = other(1) / other(0).
    try:
        v0 = sp.simplify(other.subs(kvar, 0))
        v1 = sp.simplify(other.subs(kvar, 1))
    except Exception:
        return None
    if v0 == 0:
        return None
    a = -v0
    q = sp.simplify(v1 / v0)
    # sanity: verify that other = -a q^kvar matches at kvar=2
    v2 = sp.simplify(other.subs(kvar, 2))
    expected = -a * q ** 2
    if sp.simplify(v2 - expected) != 0:
        return None
    return {"a": a, "q": q}


@_safe
def _match_eisenstein_E2k(expr, n):
    """E_{2k}(q) = 1 - (2k/B_{2k}) * sum_{n>=1} sigma_{2k-1}(n) q^n.

    We are matching the *summand* sigma_{2k-1}(n) * q^n. The 2k weight is
    recovered from the power of the divisor index. To keep the matcher
    deterministic we look for an explicit 'divisor sum factor' represented by
    a sympy DivisorSigma function call.
    """
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
            # sigma signature: divisor_sigma(n, k_index)
            sigma_args = sigma_part.args
            if len(sigma_args) >= 1 and sigma_args[0] == n:
                k_index = sigma_args[1] if len(sigma_args) == 2 else 1
                # 2k - 1 = k_index  ->  k = (k_index + 1) / 2
                k_index_val = sp.simplify(k_index)
                if k_index_val.is_integer and int(k_index_val) % 2 == 1:
                    weight = int(k_index_val) + 1
                    q = qn_part.args[0]
                    return {"q": q, "weight": weight}
    return None


@_safe
def _match_dirichlet_L(expr, n):
    """chi(n) * n^(-s)  for a Dirichlet character chi (presented as a sympy
    Function chi).
    """
    if expr.func == sp.Mul and len(expr.args) == 2:
        a, b = expr.args
        for chi_term, n_term in [(a, b), (b, a)]:
            if chi_term.func == sp.Function("chi") or (hasattr(chi_term, 'func') and chi_term.func.__name__ == "chi"):
                # n_term should be n^(-s) or 1/n^s
                if n_term.func == sp.Pow:
                    base, expo = n_term.args
                    if base == n and expo.func == sp.Mul and -1 in expo.args:
                        # expo = -s for some symbol s
                        rest = sp.Mul(*[c for c in expo.args if c != -1])
                        return {"s": rest, "chi": chi_term.func.__name__}
                    if base == n and getattr(expo, 'is_negative', False):
                        return {"s": -expo, "chi": chi_term.func.__name__}
    return None


@_safe
def _match_gauss_sum(expr, n):
    """exp(2 pi i p n^2 / q) over n=0..q-1.

    Recognizes the summand as a sympy exp whose argument is purely imaginary
    and quadratic in n, with rational coefficient p/q. The DEGENERACY CHECK
    happens downstream — here we only extract (p, q).
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
    # a2 must be of the form 2 pi i p / q
    # Try to factor 2 pi i out:
    try:
        ratio = sp.simplify(a2 / (2 * sp.pi * sp.I))
    except Exception:
        return None
    if ratio == 0:
        return None
    # ratio should be Rational p/q (or symbol)
    if ratio.is_Rational:
        p, q = int(ratio.p), int(ratio.q)
        return {"p": p, "q": q}
    # Allow symbolic p, q if the user passes them as such
    return None


# ---------- routing & cost predictors ----------

def _route_gaussian(params, tol):
    beta = mpf(params.get("beta", -log(mpf(params["q"])) if "q" in params else 1))
    # mirror v0: direct cost is sqrt(log(1/tol)/beta); dual cost uses 4 pi^2/beta scale
    direct_cost = int(ceil(sqrt(-log(mpf(tol)) / beta))) + 1
    dual_beta = pi * pi / beta
    dual_cost = int(ceil(sqrt(-log(mpf(tol)) / dual_beta))) + 1
    route = Route.DUAL if dual_cost < direct_cost else Route.DIRECT
    return {"route": route, "cost_direct": direct_cost, "cost_dual": dual_cost}


def _route_bose_einstein(params, tol):
    beta = mpf(params["beta"])
    rhs = -log(mpf(tol) * (1 - exp(-beta)))
    direct_cost = max(1, int(ceil(rhs / beta)))
    dual_beta = 4 * pi * pi / beta
    rhs2 = -log(mpf(tol) * (1 - exp(-dual_beta)))
    dual_cost = max(1, int(ceil(rhs2 / dual_beta)))
    route = Route.DUAL if dual_cost < direct_cost else Route.DIRECT
    return {"route": route, "cost_direct": direct_cost, "cost_dual": dual_cost}


def _route_lambert(params, tol):
    q = mpf(params["q"])
    if q >= 1:
        return {"route": Route.DEGENERATE, "cost_direct": -1, "cost_dual": -1,
                "reason": "Lambert series diverges for |q| >= 1"}
    direct_cost = max(1, int(ceil(log(mpf(tol) * (1 - q)) / log(q))))
    neg_log_q = -log(q)
    q_prime = exp(-4 * pi * pi / neg_log_q)
    if q_prime > 0 and q_prime < 1:
        dual_cost = max(1, int(ceil(log(mpf(tol) * (1 - q_prime)) / log(q_prime))))
    else:
        dual_cost = direct_cost + 1
    route = Route.DUAL if dual_cost < direct_cost else Route.DIRECT
    return {"route": route, "cost_direct": direct_cost, "cost_dual": dual_cost}


def _route_mock_theta(params, tol):
    """Mock thetas: no clean dual exists. Modular completion (Zwegers'
    non-holomorphic Eichler integral) is what fixes the modular behavior.
    Direct truncation is cheap WHEN q is not too close to 1; near the
    cusp the divergent shadow needs the completion.
    """
    q = mpf(params["q"])
    if q <= 0 or q >= 1:
        return {"route": Route.DEGENERATE, "cost_direct": -1, "cost_dual": -1,
                "reason": "Mock theta requires 0 < q < 1"}
    direct_cost = max(1, int(ceil(sqrt(-log(mpf(tol)) / (-log(q))))))
    # Heuristic: if q is close to 1 (specifically -log q < pi), the modular
    # completion is what you actually need.
    if -log(q) < pi:
        return {"route": Route.MODULAR_COMPLETION_REQUIRED,
                "cost_direct": direct_cost, "cost_dual": -1,
                "reason": "near q=1 cusp; Zwegers completion needed for modular accuracy"}
    return {"route": Route.DIRECT, "cost_direct": direct_cost, "cost_dual": -1}


def _route_partial_theta(params, tol):
    q = mpf(params["q"])
    if q <= 0 or q >= 1:
        return {"route": Route.DEGENERATE, "cost_direct": -1, "cost_dual": -1,
                "reason": "Partial theta requires 0 < q < 1"}
    # n-th summand magnitude q^(n(n+1)/2); solve n(n+1)/2 >= log(1/tol) / (-log q)
    rhs = -log(mpf(tol)) / (-log(q))
    direct_cost = max(1, int(ceil((sqrt(1 + 8 * rhs) - 1) / 2)))
    return {"route": Route.DIRECT, "cost_direct": direct_cost, "cost_dual": -1,
            "reason": "no clean dual (one-sided in n); direct truncation suffices"}


def _route_q_pochhammer(params, tol):
    q = mpf(params["q"])
    a = params.get("a", 1)
    if q <= 0 or q >= 1:
        return {"route": Route.DEGENERATE, "cost_direct": -1, "cost_dual": -1,
                "reason": "q-Pochhammer (a;q)_inf requires |q| < 1"}
    # Factors are 1 - a q^k; magnitude of log(factor) ~ |a| q^k. Truncate at k
    # where |a| q^k < tol.
    a_abs = abs(mpf(a)) if not isinstance(a, sp.Symbol) else mpf(1)
    if a_abs == 0:
        return {"route": Route.DEGENERATE, "cost_direct": 1, "cost_dual": -1,
                "reason": "a = 0 -> product is 1"}
    rhs = log(mpf(tol) / a_abs) / log(q)
    direct_cost = max(1, int(ceil(rhs)))
    return {"route": Route.DIRECT, "cost_direct": direct_cost, "cost_dual": -1,
            "reason": "Pochhammer converges geometrically in k"}


def _route_eisenstein(params, tol):
    q = mpf(params["q"])
    if q <= 0 or q >= 1:
        return {"route": Route.DEGENERATE, "cost_direct": -1, "cost_dual": -1,
                "reason": "Eisenstein requires 0 < q < 1"}
    # Direct truncation: sigma_{2k-1}(n) ~ n^{2k-1}; q^n dominates. Conservative:
    weight = int(params.get("weight", 4))
    # require sigma_{w-1}(N) q^N < tol; bound sigma_{w-1}(N) <= N^w; solve.
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
        return {"route": Route.DUAL, "cost_direct": direct_cost,
                "cost_dual": 1 + int(ceil(sqrt(-log(mpf(tol)) / (pi * pi / (-log(q)))))),
                "reason": "near q=1; use modular S-transform of E_{2k}"}
    return {"route": Route.DIRECT, "cost_direct": direct_cost, "cost_dual": -1}


def _route_dirichlet_L(params, tol):
    s = params["s"]
    try:
        s_val = float(sp.re(s)) if hasattr(s, "is_Number") and s.is_Number else float(s)
    except Exception:
        s_val = 1.0
    if s_val <= 0:
        # below critical strip — direct sum doesn't converge
        return {"route": Route.DUAL, "cost_direct": -1, "cost_dual": 100,
                "reason": "Re(s) <= 0; use functional equation L(s) = chi-factor * L(1-s)"}
    # direct: truncate at N with N^(1-s) / (s-1) < tol  (for s > 1)
    if s_val > 1:
        # truncation N ~ (tol * (s-1))^(1/(1-s))  with negative exponent
        try:
            N = int(math.ceil((1.0 / (float(tol) * (s_val - 1))) ** (1.0 / (s_val - 1))))
        except Exception:
            N = 10**6
        if s_val < 0.5:
            return {"route": Route.DUAL, "cost_direct": N, "cost_dual": 100,
                    "reason": "Re(s) < 1/2; functional-equation reflection is cheaper"}
        return {"route": Route.DIRECT, "cost_direct": N, "cost_dual": 100}
    # 0 < s <= 1: critical strip-ish, conditionally convergent; needs care
    return {"route": Route.DUAL, "cost_direct": -1, "cost_dual": 100,
            "reason": "0 < Re(s) <= 1; direct sum at boundary, prefer functional equation"}


def _route_gauss_sum(params, tol):
    # Defer to degeneracy_check; if non-degenerate, the cost is O(q).
    p, q = params["p"], params["q"]
    return {"route": Route.DIRECT, "cost_direct": q, "cost_dual": -1,
            "reason": f"Gauss sum of length {q}; direct evaluation"}


# ---------- degeneracy checks ----------

def _no_degeneracy(params):
    return None


def _gauss_sum_degeneracy(params):
    """Classical fact: G(p, q) = 0 when q ≡ 2 (mod 4) and gcd(p, q) = 1.

    Also: if gcd(p, q) > 1, the sum reduces and can vanish or be reweighted;
    we flag those too (but with a different reason).
    """
    p, q = params["p"], params["q"]
    if q <= 0:
        return f"q = {q} is not a positive modulus"
    g = math.gcd(abs(p), q)
    if g > 1:
        return f"gcd(p={p}, q={q}) = {g} > 1; sum reduces to a smaller Gauss sum (possibly zero)"
    if q % 4 == 2:
        return f"q={q} ≡ 2 (mod 4); G(p,q) = 0 identically (silent-zero hazard, CANDIDATE_INSIGHTS §A4)"
    return None


def _q_in_unit_disk(params):
    """Generic degeneracy: any kernel that wants q in (0,1) and got something else."""
    q = params.get("q")
    if q is None:
        return None
    try:
        qv = mpf(q)
    except Exception:
        # symbolic q; cannot evaluate
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
    # (1; q)_inf has the k=0 factor = 0 -> whole product = 0
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


# ---------- registry ----------

REGISTRY = [
    RegistryEntry(
        name="gaussian_quadratic",
        match=_match_gaussian,
        recommend_route=_route_gaussian,
        degeneracy_check=_no_degeneracy,
        notes="theta_3 family; classic Poisson summation / modular S dual",
    ),
    RegistryEntry(
        name="bose_einstein_geometric",
        match=_match_bose_einstein,
        recommend_route=_route_bose_einstein,
        degeneracy_check=_no_degeneracy,
        notes="Dedekind-eta modular S dual when beta is small",
    ),
    RegistryEntry(
        name="lambert_divisor",
        match=_match_lambert_divisor,
        recommend_route=_route_lambert,
        degeneracy_check=_q_in_unit_disk,
        notes="Eisenstein-form dual when q is near 1",
    ),
    RegistryEntry(
        name="mock_theta_f3",
        match=_match_mock_theta_f3,
        recommend_route=_route_mock_theta,
        degeneracy_check=_q_in_unit_disk,
        notes="3rd-order mock theta f; modular completion via Zwegers required near cusp (cf. experiment 15)",
    ),
    RegistryEntry(
        name="mock_theta_f5",
        match=_match_mock_theta_f5,
        recommend_route=_route_mock_theta,
        degeneracy_check=_q_in_unit_disk,
        notes="5th-order family representative; modular completion required near cusp",
    ),
    RegistryEntry(
        name="mock_theta_f7",
        match=_match_mock_theta_f7,
        recommend_route=_route_mock_theta,
        degeneracy_check=_q_in_unit_disk,
        notes="7th-order family representative; modular completion required near cusp",
    ),
    RegistryEntry(
        name="partial_theta",
        match=_match_partial_theta,
        recommend_route=_route_partial_theta,
        degeneracy_check=_q_in_unit_disk,
        notes="one-sided over n>=0; no clean dual",
    ),
    RegistryEntry(
        name="q_pochhammer_infty",
        match=_match_q_pochhammer_infty,
        recommend_route=_route_q_pochhammer,
        degeneracy_check=_pochhammer_degeneracy,
        notes="prod_{k>=0}(1 - a q^k); direct truncation OK for |q|<1",
    ),
    RegistryEntry(
        name="eisenstein_E2k",
        match=_match_eisenstein_E2k,
        recommend_route=_route_eisenstein,
        degeneracy_check=_eisenstein_degeneracy,
        notes="modular S-transform for q near 1",
    ),
    RegistryEntry(
        name="dirichlet_L",
        match=_match_dirichlet_L,
        recommend_route=_route_dirichlet_L,
        degeneracy_check=_no_degeneracy,
        notes="functional equation reflection across Re(s) = 1/2",
    ),
    RegistryEntry(
        name="gauss_sum",
        match=_match_gauss_sum,
        recommend_route=_route_gauss_sum,
        degeneracy_check=_gauss_sum_degeneracy,
        notes="silent-zero hazard at q ≡ 2 (mod 4) — see CANDIDATE_INSIGHTS §A4",
    ),
]


# ---------- top-level recognizer ----------

def recognize(expr_summand, n, tol=mpf("1e-12")) -> list[dict]:
    """Walk every registry entry, return a list of recognition results.

    Each result dict has the fields:
      - kernel        : str (registry name)
      - params        : dict of extracted parameters
      - degenerate    : Optional[str] (reason; None if non-degenerate)
      - route         : Route enum value (DEGENERATE if degenerate)
      - cost_direct   : int (or -1 if N/A)
      - cost_dual     : int (or -1 if N/A)
      - notes         : str (kernel notes)

    Degeneracy check ALWAYS runs before cost prediction; if it fires, the
    route is forced to DEGENERATE and cost estimates are suppressed.
    """
    results = []
    for entry in REGISTRY:
        params = entry.match(expr_summand, n)
        if params is None:
            continue
        deg = entry.degeneracy_check(params)
        if deg is not None:
            results.append({
                "kernel": entry.name,
                "params": {k: str(v) for k, v in params.items()},
                "degenerate": deg,
                "route": Route.DEGENERATE,
                "cost_direct": -1,
                "cost_dual": -1,
                "notes": entry.notes,
            })
            continue
        try:
            routing = entry.recommend_route(params, tol)
        except Exception as e:
            routing = {"route": Route.DEGENERATE, "cost_direct": -1, "cost_dual": -1,
                       "reason": f"routing failed: {e}"}
        results.append({
            "kernel": entry.name,
            "params": {k: str(v) for k, v in params.items()},
            "degenerate": None,
            "route": routing["route"],
            "cost_direct": routing.get("cost_direct", -1),
            "cost_dual": routing.get("cost_dual", -1),
            "reason": routing.get("reason"),
            "notes": entry.notes,
        })
    return results


def best_match(expr_summand, n, tol=mpf("1e-12")) -> Optional[dict]:
    """Return the SINGLE best match, or None if no kernel fits.

    Tie-break rule: prefer non-degenerate matches; among non-degenerate
    matches, prefer the one with the smallest cheap-route cost (lower is
    better). If only degenerate matches are present, return the first one
    (the registry order encodes a structural priority).
    """
    results = recognize(expr_summand, n, tol)
    if not results:
        return None
    non_deg = [r for r in results if r["degenerate"] is None]
    if non_deg:
        return min(non_deg, key=lambda r: min([c for c in (r["cost_direct"], r["cost_dual"]) if c > 0],
                                              default=10**9))
    return results[0]


def main():
    """Sanity-check demo — see experiment 14 for the full benchmark."""
    n = sp.symbols("n", integer=True, nonnegative=True)
    k = sp.symbols("k", integer=True, nonnegative=True)
    q_sym, a_sym, s_sym, beta_sym = sp.symbols("q a s beta", positive=True)

    cases = [
        ("gaussian beta=1",        sp.exp(-1 * n ** 2)),
        ("mock theta f3 q=0.5",    sp.Rational(1, 2) ** (n ** 2) /
                                    sp.Product((1 + sp.Rational(1, 2) ** k) ** 2, (k, 1, n))),
        ("partial theta q=0.5",    (-1) ** n * sp.Rational(1, 2) ** (n * (n + 1) / 2)),
        ("q-pochhammer (1/2;1/3)", sp.Product(1 - sp.Rational(1, 2) * sp.Rational(1, 3) ** k, (k, 0, sp.oo))),
        ("Gauss sum p=1 q=4",      sp.exp(2 * sp.pi * sp.I * 1 * n ** 2 / 4)),
        ("Gauss sum p=1 q=6 (SILENT ZERO)",
                                    sp.exp(2 * sp.pi * sp.I * 1 * n ** 2 / 6)),
    ]
    for desc, expr in cases:
        bm = best_match(expr, n)
        if bm is None:
            print(f"{desc:<40} -> <no match>")
        else:
            tag = bm["degenerate"] or bm.get("reason") or ""
            print(f"{desc:<40} -> {bm['kernel']:<22} route={bm['route'].value:<26} {tag}")


if __name__ == "__main__":
    main()
