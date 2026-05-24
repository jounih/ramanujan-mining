"""rkc CLI — degeneracy-aware special-function routing compiler (v0.1 scaffold).

Four subcommands wrapping the existing public API:

    rkc recognize  "<expr>" [--var n]
        → identify the kernel family + route + confidence.

    rkc compare    "<expr>" [--var n] [--param k=v ...] [--digits N]
        → recognize + emit direct vs dual cost estimates + recommended route
          + estimated speedup factor.

    rkc certify    "<expr>" [--var n] [--param k=v ...]
        → recognize + surface degeneracy guard + completion certificate if
          available. Refuses unsafe transformations in known degenerate
          regimes (e.g. Gauss sums q ≡ 2 mod 4 silent-zero hazard).

    rkc benchmark  <yaml-file>
        → read a YAML configuration of (expr, params, digits) test cells
          and print a per-cell speedup table. Intended for batch regression
          checks against `analysis/14b_recognizer_v2_benchmark.py`.

Output is human-readable by default; pass `--json` for a machine-readable
dump (suitable for piping into downstream tools).

This is a v0.1 scaffold: per [rkc/MILESTONES.md](MILESTONES.md), the v0.1
release gates this CLI through `pip install -e .` as the `rkc` entry point
and adds CLI-level tests. The scaffold here is the contract — flags and
output shapes pin down what subsequent commits flesh out.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import sympy as sp

from rkc import (
    best_match,
    recognize,
    recognize_with_raw_string,
    Route,
    RoutingResult,
)


# ---------------------------------------------------------------------------
# Shared parsing helpers
# ---------------------------------------------------------------------------

def _parse_expr(expr_string: str, var_name: str) -> tuple[sp.Expr, sp.Symbol]:
    """Parse a user expression into a sympy Expr + the integer iteration symbol.

    Uses sympy's standard parser (no `eval()` shortcuts). Defines the
    iteration variable as a positive integer symbol so kernel matchers that
    assume integer indexing work as expected.
    """
    n = sp.Symbol(var_name, integer=True, positive=True)
    # Add common locals so users can write `beta`, `q`, `p`, etc. without
    # them being parsed as undefined functions.
    locals_ = {
        var_name: n,
        "beta": sp.Symbol("beta", positive=True),
        "alpha": sp.Symbol("alpha", positive=True),
        "q": sp.Symbol("q"),
        "p": sp.Symbol("p"),
        "x": sp.Symbol("x"),
        "I": sp.I,
        "pi": sp.pi,
        "oo": sp.oo,
        "Sum": sp.Sum,
        "Product": sp.Product,
        "exp": sp.exp,
        "log": sp.log,
        "sin": sp.sin,
        "cos": sp.cos,
        "sqrt": sp.sqrt,
        "Rational": sp.Rational,
        "Integer": sp.Integer,
    }
    expr = sp.sympify(expr_string, locals=locals_)
    # If the user wrapped in Sum/Product, peel back to the summand for the
    # recognizer (which operates on the summand, not the outer Sum object).
    if isinstance(expr, (sp.Sum, sp.Product)):
        expr = expr.function
    return expr, n


def _parse_params(param_pairs: list[str]) -> dict[str, Any]:
    """Convert a list of `key=value` CLI args into a dict of sympy-evaluable
    values. Numeric literals are parsed as mpmath-friendly Python floats;
    non-numeric values pass through unchanged.
    """
    out: dict[str, Any] = {}
    for pair in param_pairs:
        if "=" not in pair:
            raise SystemExit(
                f"rkc: --param expected key=value, got {pair!r}"
            )
        key, _, value = pair.partition("=")
        # try int → float → string
        try:
            out[key.strip()] = int(value)
            continue
        except ValueError:
            pass
        try:
            out[key.strip()] = float(value)
            continue
        except ValueError:
            pass
        out[key.strip()] = value
    return out


def _result_to_human(r: RoutingResult | None) -> str:
    """Pretty-print a single RoutingResult for terminal output."""
    if r is None:
        return "  (no match — neither strict nor fuzzy)"
    lines = [
        f"  kernel         : {r.kernel}",
        f"  family         : {r.family}",
        f"  route          : {r.route.value}",
        f"  confidence     : {r.confidence:.2f}",
        f"  scalar_coef    : {r.scalar_coefficient}",
    ]
    if r.params:
        lines.append(f"  params         : {dict(r.params)}")
    if r.num_terms >= 0:
        lines.append(f"  num_terms      : {r.num_terms}")
    if r.per_term_cost > 0:
        lines.append(f"  per_term_cost  : {r.per_term_cost:.2f}")
    if r.total_cost > 0:
        lines.append(f"  total_cost     : {r.total_cost:.2f}")
    if r.cost_direct >= 0:
        lines.append(f"  cost_direct    : {r.cost_direct} terms")
    if r.cost_dual >= 0:
        lines.append(f"  cost_dual      : {r.cost_dual} terms")
    if r.degenerate:
        lines.append(f"  DEGENERATE     : {r.degenerate}")
    if r.reason:
        lines.append(f"  reason         : {r.reason}")
    if r.notes:
        lines.append(f"  notes          : {r.notes}")
    if r.completion is not None:
        lines.append(f"  completion     : value={r.completion.value!r}, "
                     f"err={r.completion.error_bound!r}")
    if r.completion_error:
        lines.append(f"  completion_err : {r.completion_error}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Subcommand: recognize
# ---------------------------------------------------------------------------

def cmd_recognize(args: argparse.Namespace) -> int:
    expr, n = _parse_expr(args.expr, args.var)
    r = best_match(expr, n, accept_fuzzy=args.accept_fuzzy)
    if args.json:
        print(json.dumps(r.to_dict() if r else None, indent=2, default=str))
    else:
        print(f"recognize: {args.expr!r}")
        print(_result_to_human(r))
    return 0 if r is not None else 1


# ---------------------------------------------------------------------------
# Subcommand: compare
# ---------------------------------------------------------------------------

def cmd_compare(args: argparse.Namespace) -> int:
    expr, n = _parse_expr(args.expr, args.var)
    params = _parse_params(args.param)
    # Substitute params before recognize so the cost estimator can see
    # actual numerical β / q / etc. Use sp.nsimplify (Rational form) on
    # numeric values — the matchers' regex patterns match against Rationals,
    # not floats; passing 1e-8 directly turns the AST into `Float(1e-8)*n²`
    # which doesn't match the matcher's `negative_real_coeff * n²` pattern.
    if params:
        subst: dict[sp.Symbol, Any] = {}
        for k, v in params.items():
            sym_pos = sp.Symbol(k, positive=True)
            sym = sp.Symbol(k)
            if isinstance(v, (int, float)):
                v_exact = sp.nsimplify(v, rational=True) if isinstance(v, float) else sp.Integer(v)
            else:
                v_exact = v
            subst[sym_pos] = v_exact
            subst[sym] = v_exact
        expr = expr.subs(subst)
    r = best_match(expr, n, accept_fuzzy=False)
    if args.json:
        print(json.dumps(r.to_dict() if r else None, indent=2, default=str))
        return 0 if r else 1
    print(f"compare: {args.expr!r}")
    print(f"  params         : {params}")
    print(f"  digits         : {args.digits}")
    print(_result_to_human(r))
    if r and r.cost_direct >= 0 and r.cost_dual >= 0:
        cd, cu = r.cost_direct, max(r.cost_dual, 1)
        ratio = cd / cu if cu else float("inf")
        rec = "dual" if cd > cu else "direct"
        print(f"  recommended    : {rec}")
        print(f"  speedup_factor : {ratio:.1f}× ({cd} → {cu} terms)")
    return 0 if r is not None else 1


# ---------------------------------------------------------------------------
# Subcommand: certify
# ---------------------------------------------------------------------------

def cmd_certify(args: argparse.Namespace) -> int:
    """Surface the degeneracy guard + any completion certificate.

    This subcommand uses `recognize_with_raw_string` so the Gauss-sum
    pre-reduction (raw_pq) hits the degeneracy detector — sympy's auto-
    simplification of e.g. 2n²/6 → n²/3 would otherwise hide the q≡2 mod 4
    silent-zero case.
    """
    n = sp.Symbol(args.var, integer=True, positive=True)
    results = recognize_with_raw_string(args.expr, n)
    r = None
    if results:
        # prefer DEGENERATE if present (the whole point of certify)
        deg = [x for x in results if x.route == Route.DEGENERATE]
        r = deg[0] if deg else results[0]
    # numerical completion is a post-recognize attach (recognize_with_raw_string
    # doesn't take the flag). Only meaningful for MODULAR_COMPLETION_REQUIRED.
    if args.numerical and r is not None and r.route == Route.MODULAR_COMPLETION_REQUIRED:
        from rkc.recognizer import _attach_completion  # internal API; OK for v0.1 CLI
        _attach_completion([r], q_value=None, target_digits=args.digits)
    if args.json:
        print(json.dumps(r.to_dict() if r else None, indent=2, default=str))
        return 0 if r else 1
    print(f"certify: {args.expr!r}")
    print(_result_to_human(r))
    if r is None:
        print("  no recognized kernel; no certificate produced.")
    elif r.route == Route.DEGENERATE:
        print(f"  ▲ CERTIFICATE: {r.degenerate or r.reason or 'degeneracy detected'}")
        print(f"    do NOT use the dual / closed-form route here — answer is "
              f"the trivial value.")
    elif r.route == Route.MODULAR_COMPLETION_REQUIRED and r.completion:
        print(f"  ✓ CERTIFICATE: Watson-Hickerson Eichler completion")
        print(f"    value     = {r.completion.value}")
        print(f"    err_bound = {r.completion.error_bound}")
        print(f"    method    = {r.completion.certificate.method}")
    elif r.route == Route.MODULAR_COMPLETION_REQUIRED:
        print(f"  → MCR route detected; pass --numerical to attempt Watson-Hickerson "
              f"and emit a value+certificate.")
    else:
        print(f"  ✓ no degeneracy detected; route {r.route.value} safe to use.")
    return 0


# ---------------------------------------------------------------------------
# Subcommand: benchmark
# ---------------------------------------------------------------------------

def cmd_benchmark(args: argparse.Namespace) -> int:
    """Read a YAML file of (expr, params, digits) cells and print a per-cell
    speedup table. v0.1 scaffold: emits a structured stub when no YAML is
    given, and a not-implemented notice for the YAML path until v0.1.

    This wires to `analysis/14b_recognizer_v2_benchmark.py`'s 55-case suite
    for regression purposes; the YAML format is documented as part of the
    v0.1 release.
    """
    if args.yaml is None:
        # default: run the 14b benchmark and report its summary
        import importlib.util as _ilu
        from pathlib import Path
        bench = Path(__file__).resolve().parents[1] / "analysis" / "14b_recognizer_v2_benchmark.py"
        if not bench.exists():
            print(f"benchmark: default suite not found at {bench}", file=sys.stderr)
            return 2
        spec = _ilu.spec_from_file_location("rkc_default_bench", bench)
        mod = _ilu.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)
        # The script's `if __name__ == "__main__": run()` guard is bypassed
        # under exec_module — invoke run() explicitly.
        if hasattr(mod, "run"):
            mod.run()
        return 0
    print(f"benchmark: YAML cell-suite path provided ({args.yaml!r}).",
          file=sys.stderr)
    print("benchmark: YAML cell-suite executor is a v0.1 gate (see "
          "rkc/MILESTONES.md §A); not yet implemented.", file=sys.stderr)
    return 3


# ---------------------------------------------------------------------------
# Argparse wiring
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="rkc",
        description="rkc — degeneracy-aware special-function routing compiler",
    )
    p.add_argument("--version", action="version", version="rkc 0.1.0-dev")
    sub = p.add_subparsers(dest="cmd", required=True)

    # recognize
    pr = sub.add_parser("recognize",
                        help="Identify the kernel family + route + confidence.")
    pr.add_argument("expr", help='Symbolic summand expression, e.g. "exp(-beta*n**2)"')
    pr.add_argument("--var", default="n",
                    help="Iteration variable (default: n).")
    pr.add_argument("--accept-fuzzy", action="store_true",
                    help="Return FUZZY-routed matches if no strict match exists.")
    pr.add_argument("--json", action="store_true",
                    help="Emit JSON instead of human-readable output.")
    pr.set_defaults(func=cmd_recognize)

    # compare
    pc = sub.add_parser("compare",
                        help="Show direct vs dual cost estimates + speedup.")
    pc.add_argument("expr", help='Symbolic summand expression.')
    pc.add_argument("--var", default="n")
    pc.add_argument("--param", action="append", default=[], metavar="K=V",
                    help="Numerical parameter, e.g. --param beta=1e-8 (repeatable).")
    pc.add_argument("--digits", type=int, default=30,
                    help="Target precision in decimal digits (default: 30).")
    pc.add_argument("--json", action="store_true")
    pc.set_defaults(func=cmd_compare)

    # certify
    pf = sub.add_parser("certify",
                        help="Surface degeneracy guard + completion certificate.")
    pf.add_argument("expr", help='Symbolic summand expression.')
    pf.add_argument("--var", default="n")
    pf.add_argument("--numerical", action="store_true",
                    help="For MCR routes, actually compute the Watson-Hickerson "
                         "Eichler completion and emit value + error bound.")
    pf.add_argument("--digits", type=int, default=30,
                    help="Target digits for the Watson-Hickerson completion "
                         "(default: 30; only used with --numerical).")
    pf.add_argument("--json", action="store_true")
    pf.set_defaults(func=cmd_certify)

    # benchmark
    pb = sub.add_parser("benchmark",
                        help="Run the recognizer benchmark suite.")
    pb.add_argument("yaml", nargs="?", default=None,
                    help="Optional YAML cell-file (v0.1 gate; defaults to the 55-case "
                         "regression suite from analysis/14b_recognizer_v2_benchmark.py).")
    pb.set_defaults(func=cmd_benchmark)

    # search (Project C v0.3.0)
    ps = sub.add_parser("search",
                        help="Run Project C operator-composition search (v0.3.0 baseline).")
    ps.add_argument("expr", help='Initial expression to search from.')
    ps.add_argument("--var", default="n", help="Iteration variable.")
    ps.add_argument("--budget", type=int, default=100,
                    help="Number of operator proposals to try (default: 100).")
    ps.add_argument("--digits", type=int, default=20,
                    help="Verifier precision in decimal digits (default: 20).")
    ps.add_argument("--out-dir", default=".rkc_search_out",
                    help="Directory for accepted.jsonl + rejected.jsonl (default: .rkc_search_out).")
    ps.add_argument("--seed", type=int, default=None, help="RandomProposer seed.")
    ps.add_argument("--verbose", action="store_true")
    ps.set_defaults(func=cmd_search)

    return p


def cmd_search(args: argparse.Namespace) -> int:
    """Project C v0.3.0 search loop (single-step composition baseline)."""
    expr, n = _parse_expr(args.expr, args.var)
    from rkc.search import (
        SearchState, RandomProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
    )
    state = SearchState(payload=expr, metadata={"var": n})
    registry = JsonlRegistry.with_dir(args.out_dir)
    summary = search(
        initial_state=state,
        proposer=RandomProposer(seed=args.seed),
        verifier=MpmathVerifier(n_digits=args.digits),
        router=RkcRouter(),
        cost_model=RkcCostModel(),
        registry=registry,
        budget=args.budget,
        max_depth=1,
        verbose=args.verbose,
    )
    print(f"search: {args.expr!r}")
    print(f"  budget        : {summary.budget}")
    print(f"  proposed      : {summary.n_proposed}")
    print(f"  accepted      : {summary.n_accepted}")
    print(f"  rejected      : {summary.n_rejected}")
    print(f"  reject reasons: {summary.reject_reason_counts}")
    print(f"  accepted hashes: {summary.accepted_hashes[:5]}{' …' if len(summary.accepted_hashes) > 5 else ''}")
    print(f"  output dir    : {args.out_dir}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
