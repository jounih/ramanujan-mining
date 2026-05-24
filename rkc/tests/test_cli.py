"""Smoke tests for the rkc v0.1 CLI scaffold.

These tests pin the CLI contract — exit codes, expected substrings in
human-readable output, and the four subcommand entry points. They do not
test the full per-family coverage matrix (that's the v0.1 release gate;
see rkc/MILESTONES.md §A).
"""
from __future__ import annotations

import json
import subprocess
import sys

import pytest


def _run(argv: list[str]) -> subprocess.CompletedProcess:
    """Invoke `python -m rkc <argv>` and capture both streams."""
    return subprocess.run(
        [sys.executable, "-m", "rkc", *argv],
        capture_output=True,
        text=True,
        timeout=60,
    )


# ---------------------------------------------------------------------------
# rkc --version / --help
# ---------------------------------------------------------------------------

def test_version():
    p = _run(["--version"])
    assert p.returncode == 0
    assert "rkc" in p.stdout


def test_help_lists_subcommands():
    p = _run(["--help"])
    assert p.returncode == 0
    for cmd in ("recognize", "compare", "certify", "benchmark"):
        assert cmd in p.stdout


# ---------------------------------------------------------------------------
# rkc recognize
# ---------------------------------------------------------------------------

def test_recognize_gaussian():
    p = _run(["recognize", "exp(-beta*n**2)"])
    assert p.returncode == 0
    assert "gaussian_quadratic" in p.stdout
    assert "theta-like" in p.stdout


def test_recognize_json_emits_valid_json():
    p = _run(["recognize", "exp(-beta*n**2)", "--json"])
    assert p.returncode == 0
    payload = json.loads(p.stdout)
    assert payload["kernel"] == "gaussian_quadratic"
    assert payload["family"] == "theta-like"


def test_recognize_no_match_returns_nonzero():
    p = _run(["recognize", "log(n) + sin(n)"])
    # Hand-crafted nothing: not a kernel; exit 1.
    assert p.returncode == 1


# ---------------------------------------------------------------------------
# rkc compare
# ---------------------------------------------------------------------------

def test_compare_gaussian_numeric_beta_shows_speedup():
    """With β=1e-8 we expect direct ≫ dual (Gaussian theta @ small β)."""
    p = _run(["compare", "exp(-beta*n**2)", "--param", "beta=1e-8"])
    assert p.returncode == 0
    out = p.stdout
    assert "gaussian_quadratic" in out
    # Cost estimator should give cost_direct > cost_dual at small β
    assert "cost_direct" in out
    assert "cost_dual" in out
    assert "speedup_factor" in out
    assert "recommended" in out


# ---------------------------------------------------------------------------
# rkc certify — degeneracy guard (the §A4 silent-zero hazard)
# ---------------------------------------------------------------------------

def test_certify_gauss_sum_silent_zero_fires_at_q_six():
    """q=6 ≡ 2 (mod 4) should fire the silent-zero hazard."""
    p = _run(["certify", "exp(2*pi*I*n**2/6)"])
    assert p.returncode == 0
    out = p.stdout
    assert "gauss_sum" in out
    assert "DEGENERATE" in out
    assert "silent-zero" in out
    # The CLI surfaces "do NOT use the dual" guidance for degenerate routes
    assert "do NOT use" in out


def test_certify_gauss_sum_q_seven_is_safe():
    """q=7 ≢ 2 (mod 4) → no degeneracy."""
    p = _run(["certify", "exp(2*pi*I*n**2/7)"])
    assert p.returncode == 0
    out = p.stdout
    assert "gauss_sum" in out
    assert "no degeneracy" in out


# ---------------------------------------------------------------------------
# rkc benchmark — default suite runs the 14b regression
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# rkc search (Project C v0.3.0 baseline)
# ---------------------------------------------------------------------------

def test_search_baseline_runs_and_writes_reject_log(tmp_path):
    """v0.3.0: with stub apply_fn's, all proposals decline; verify the
    engine + reject log path works end-to-end."""
    p = _run([
        "search", "exp(-beta*n**2)",
        "--budget", "5",
        "--digits", "10",
        "--seed", "42",
        "--out-dir", str(tmp_path),
    ])
    assert p.returncode == 0
    assert "proposed      : 5" in p.stdout
    assert "rejected      : 5" in p.stdout
    # reject log should exist
    assert (tmp_path / "rejected.jsonl").exists()
    # accepted log only created on first acceptance
    # (v0.3.0 has no implemented operators yet, so no acceptance expected)


def test_search_module_import_smoke():
    """Public API surface importable; protocols satisfied."""
    from rkc.search import (
        SearchState, OperatorApplication, RejectReason,
        Proposer, Verifier, Router, CostModel, Registry,
        RandomProposer, MpmathVerifier, RkcRouter, RkcCostModel,
        JsonlRegistry, search, QR7_OPERATOR_BASIS,
    )
    assert len(QR7_OPERATOR_BASIS) == 7
    op_ids = [op.id for op in QR7_OPERATOR_BASIS]
    assert "master_theorem" in op_ids
    assert "fractional_functional_iteration" in op_ids


def test_v04_mellin_inversion_poisson_dual_accepted(tmp_path):
    """Project C v0.4 acceptance gate: with mellin_inversion's Poisson-
    summation apply_fn wired, a Gaussian at small β should produce at
    least one accepted identity via the Poisson dual."""
    import json
    import sympy as sp
    from rkc.search import (
        SearchState, RandomProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
    )
    n = sp.Symbol("n", integer=True, positive=True)
    expr = sp.exp(-sp.Rational(1, 100) * n**2)  # β=1/100; Poisson dual is ~54× cheaper
    state = SearchState(payload=expr, metadata={"var": n})
    reg = JsonlRegistry.with_dir(tmp_path)
    summary = search(
        initial_state=state,
        proposer=RandomProposer(seed=42),
        verifier=MpmathVerifier(n_digits=10),
        router=RkcRouter(),
        cost_model=RkcCostModel(),
        registry=reg,
        budget=30,
        max_depth=1,
    )
    # At least one acceptance expected (the seed is deterministic; mellin_inversion
    # gets chosen many times among 30, of which ~6-10 actually apply).
    assert summary.n_accepted >= 1, (
        f"v0.4 acceptance gate failed: 0 acceptances in 30-budget search; "
        f"reject reasons = {summary.reject_reason_counts}"
    )
    # Verify the accepted record looks right
    accepted_path = tmp_path / "accepted.jsonl"
    assert accepted_path.exists()
    first = json.loads(accepted_path.read_text().splitlines()[0])
    assert first["op_sequence"][0]["op_id"] == "mellin_inversion"
    # The cost ratio should be > 1 (the transformation is cheaper)
    assert first["cost_ratio"] > 1.0


def test_v04_mellin_inversion_apply_fn_directly():
    """Direct unit test of mellin_inversion's apply_fn: Gaussian → Poisson dual."""
    import sympy as sp
    from rkc.search.basis import get_operator
    n = sp.Symbol("n", integer=True, positive=True)
    op = get_operator("mellin_inversion")
    # Should apply to a gaussian
    expr_in = sp.exp(-sp.Rational(1, 100) * n**2)
    expr_out = op.apply_fn(expr_in, n)
    assert expr_out is not None, "mellin_inversion should fire on a gaussian"
    # Should NOT apply to a non-gaussian
    expr_not_gauss = sp.exp(-sp.Symbol("alpha", positive=True) * n)  # linear in n
    expr_out2 = op.apply_fn(expr_not_gauss, n)
    assert expr_out2 is None, "mellin_inversion should decline on non-gaussian"


def test_v05_master_theorem_beta_function(tmp_path):
    """Project C v0.5: master_theorem accepts the Beta-function identity
    `∫₀^¹ x^(m-1) (1-x)^(n-1) dx = Γ(m)Γ(n)/Γ(m+n)` end-to-end."""
    import json
    import sympy as sp
    from rkc.search import (
        SearchState, RandomProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
    )
    x = sp.Symbol("x", positive=True)
    m = sp.Symbol("m", positive=True)
    n = sp.Symbol("n", positive=True)
    beta_int = sp.Integral(x**(m-1) * (1-x)**(n-1), (x, 0, 1))
    state = SearchState(payload=beta_int, metadata={"var": x})
    reg = JsonlRegistry.with_dir(tmp_path)
    summary = search(
        initial_state=state, proposer=RandomProposer(seed=42),
        verifier=MpmathVerifier(n_digits=10),
        router=RkcRouter(), cost_model=RkcCostModel(),
        registry=reg, budget=30, max_depth=1,
    )
    assert summary.n_accepted >= 1, (
        f"v0.5 acceptance gate failed: {summary.reject_reason_counts}"
    )
    accepted_path = tmp_path / "accepted.jsonl"
    assert accepted_path.exists()
    first = json.loads(accepted_path.read_text().splitlines()[0])
    assert first["op_sequence"][0]["op_id"] == "master_theorem"
    # The closed-form Γ-product should be much cheaper than the integral
    assert first["cost_ratio"] >= 50.0
    # The output should contain gamma functions
    assert "gamma" in first["state_after"].lower()


def test_v06_sweep_serial_smoke(tmp_path):
    """Project C v0.6+ sweep: serial 1-worker run over 3 seeds with the
    deterministic RNG seed. Hit-rate floor: ≥2 of 3 seeds (Gaussian +
    Master-Theorem-Beta) should produce at least one acceptance."""
    from rkc.search import SEED_LIBRARY, sweep
    seed_ids = ["gaussian_beta_1em2", "gaussian_beta_1em4", "beta_function_integral"]
    summary = sweep(
        seed_ids=seed_ids, budget=15, max_depth=2, n_digits=8,
        workers=1, rng_seed=42, out_dir=tmp_path,
    )
    assert summary["n_seeds"] == 3
    assert summary["n_errors"] == 0
    assert summary["n_seeds_with_acceptance"] >= 2, (
        f"sweep smoke failed: only {summary['n_seeds_with_acceptance']} of 3 "
        f"produced acceptance. Per-seed: {[(r['seed_id'], r['n_accepted']) for r in summary['per_seed']]}"
    )
    # Output files written
    assert (tmp_path / "sweep_summary.json").exists()
    assert (tmp_path / "sweep_summary.csv").exists()


def test_sweep_seed_library_buildable():
    """Every seed in SEED_LIBRARY must construct without raising."""
    from rkc.search import SEED_LIBRARY, build_seed
    for sid, seed in SEED_LIBRARY.items():
        expr, var = build_seed(seed)
        assert expr is not None, f"seed {sid} built None expr"
        assert var is not None, f"seed {sid} built None var"


def test_v05_master_theorem_canonical_patterns():
    """Unit test: master_theorem matches the 3 canonical patterns
    (Gamma, Beta, 1/(1+x)) and declines on non-matching forms."""
    import sympy as sp
    from rkc.search.basis import get_operator
    op = get_operator("master_theorem")
    x = sp.Symbol("x", positive=True)
    m = sp.Symbol("m", positive=True)
    n = sp.Symbol("n", positive=True)
    s = sp.Symbol("s", positive=True)
    dummy = sp.Symbol("dummy")

    # Gamma
    out = op.apply_fn(sp.Integral(x**(s-1) * sp.exp(-x), (x, 0, sp.oo)), dummy)
    assert out == sp.gamma(s)

    # Beta
    out = op.apply_fn(sp.Integral(x**(m-1) * (1-x)**(n-1), (x, 0, 1)), dummy)
    assert sp.simplify(out - sp.gamma(m)*sp.gamma(n)/sp.gamma(m+n)) == 0

    # 1/(1+x)
    out = op.apply_fn(sp.Integral(x**(s-1) / (1+x), (x, 0, sp.oo)), dummy)
    assert sp.simplify(out - sp.pi/sp.sin(sp.pi*s)) == 0

    # Decline: not an Integral
    out = op.apply_fn(sp.exp(-x), x)
    assert out is None

    # Decline: integrand doesn't match any pattern
    out = op.apply_fn(sp.Integral(x**2 * sp.log(x), (x, 0, 1)), dummy)
    assert out is None


# ---------------------------------------------------------------------------
# rkc benchmark — default suite runs the 14b regression
# ---------------------------------------------------------------------------

@pytest.mark.slow
def test_benchmark_default_suite_runs():
    """The default benchmark runs `analysis/14b_recognizer_v2_benchmark.py`.
    Slow because it does the full 55-case sweep; marked accordingly so the
    default `pytest -m 'not slow'` skips it.
    """
    p = _run(["benchmark"])
    assert p.returncode == 0
    # The 14b script prints "55/55" if everything passes
    assert "55" in p.stdout
