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
