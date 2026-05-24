"""rkc.search.sweep — parallel sweep over the seed library.

For each seed in `rkc.search.seeds.SEED_LIBRARY` (or a user-provided
subset), run `rkc.search.search()` with the configured budget/depth and
aggregate the results into a single sweep summary.

Workers run in separate processes via `multiprocessing.Pool` so the
sweep scales near-linearly with core count. Each worker:
  1. Receives a seed_id (string-keyed in SEED_LIBRARY)
  2. Reconstructs the sympy expression via `build_seed()`
  3. Runs the search loop with its own JsonlRegistry (per-seed subdir)
  4. Returns a serializable summary dict

Why string-keyed: sympy Expr objects don't pickle cleanly across
processes (Symbol assumptions don't round-trip), so we pass seed IDs
and reconstruct inside each worker.

CLI: `rkc sweep [--seeds id1,id2,…] [--budget N] [--depth D] [--workers W]
                 [--digits K] [--out DIR] [--seed S]`
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass
from multiprocessing import get_context
from pathlib import Path
from typing import Any

from .core import SearchState
from .seeds import SEED_LIBRARY, Seed, build_seed


@dataclass
class SeedSweepResult:
    """One seed's sweep outcome — serialisable dict-of-strings."""
    seed_id: str
    description: str
    n_proposed: int
    n_accepted: int
    n_rejected: int
    reject_reason_counts: dict[str, int]
    accepted_hashes: list[str]
    walltime_seconds: float
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "seed_id": self.seed_id,
            "description": self.description,
            "n_proposed": self.n_proposed,
            "n_accepted": self.n_accepted,
            "n_rejected": self.n_rejected,
            "reject_reason_counts": self.reject_reason_counts,
            "accepted_hashes": self.accepted_hashes,
            "walltime_seconds": self.walltime_seconds,
            "error": self.error,
        }


def _run_one_seed(args: tuple) -> dict[str, Any]:
    """Worker function — runs `search` on a single seed. Top-level so it
    pickles cleanly across multiprocessing boundaries.

    args = (seed_id, budget, max_depth, n_digits, rng_seed, out_dir_str,
            proposer_kind, claude_model, claude_max_api_calls)

    proposer_kind: "random" (v0.6 default) or "claude" (v0.8a; uses the
    Anthropic API via ClaudeProposer with graceful fallback to random
    when ANTHROPIC_API_KEY is absent).
    """
    # Backward-compat: accept 6-tuple (legacy) or 9-tuple (v0.8a+)
    if len(args) == 6:
        (seed_id, budget, max_depth, n_digits, rng_seed, out_dir_str) = args
        proposer_kind = "random"
        claude_model = "claude-sonnet-4-5"
        claude_max_api_calls = 10
    else:
        (seed_id, budget, max_depth, n_digits, rng_seed, out_dir_str,
         proposer_kind, claude_model, claude_max_api_calls) = args
    # Re-import inside the worker so multiprocessing doesn't share module state
    from rkc.search.seeds import SEED_LIBRARY, build_seed
    from rkc.search import (
        SearchState, RandomProposer, ClaudeProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
    )
    out_dir = Path(out_dir_str) / seed_id
    out_dir.mkdir(parents=True, exist_ok=True)
    t_start = time.time()
    try:
        seed = SEED_LIBRARY[seed_id]
        expr, var = build_seed(seed)
        state = SearchState(payload=expr, metadata={"var": var})
        registry = JsonlRegistry.with_dir(out_dir)
        if proposer_kind == "claude":
            proposer = ClaudeProposer(
                seed=rng_seed, model=claude_model,
                max_api_calls=claude_max_api_calls,
            )
        else:
            proposer = RandomProposer(seed=rng_seed)
        summary = search(
            initial_state=state,
            proposer=proposer,
            verifier=MpmathVerifier(n_digits=n_digits),
            router=RkcRouter(),
            cost_model=RkcCostModel(),
            registry=registry,
            budget=budget,
            max_depth=max_depth,
            verbose=False,
        )
        elapsed = time.time() - t_start
        return SeedSweepResult(
            seed_id=seed_id,
            description=seed.description,
            n_proposed=summary.n_proposed,
            n_accepted=summary.n_accepted,
            n_rejected=summary.n_rejected,
            reject_reason_counts=summary.reject_reason_counts,
            accepted_hashes=summary.accepted_hashes,
            walltime_seconds=elapsed,
            error=None,
        ).to_dict()
    except Exception as e:
        elapsed = time.time() - t_start
        return SeedSweepResult(
            seed_id=seed_id,
            description=SEED_LIBRARY.get(seed_id, Seed(seed_id, "(unknown)", "", "", [], "", "", "")).description,
            n_proposed=0, n_accepted=0, n_rejected=0,
            reject_reason_counts={},
            accepted_hashes=[],
            walltime_seconds=elapsed,
            error=f"{type(e).__name__}: {e}",
        ).to_dict()


def sweep(seed_ids: list[str] | None = None,
          budget: int = 100,
          max_depth: int = 2,
          n_digits: int = 10,
          workers: int = 4,
          rng_seed: int | None = None,
          out_dir: str | Path = ".rkc_sweep_out",
          proposer_kind: str = "random",
          claude_model: str = "claude-sonnet-4-5",
          claude_max_api_calls: int = 10) -> dict[str, Any]:
    """Run `search()` over multiple seeds in parallel; aggregate results.

    Parameters
    ----------
    seed_ids : list[str] | None
        Subset of SEED_LIBRARY keys to run. None = run all 16 seeds.
    budget : int
        Per-seed search budget (proposer rounds).
    max_depth : int
        Max operator-sequence length per attempt (1 = depth-1 like v0.4;
        2 = composition like v0.6).
    n_digits : int
        Verifier precision in decimal digits.
    workers : int
        Number of worker processes (parallel seeds; not parallel within a seed).
    rng_seed : int | None
        Optional RNG seed for the RandomProposer. Same seed across all
        workers means each per-seed search is deterministic.
    out_dir : str | Path
        Output directory; one subdir per seed with accepted.jsonl + rejected.jsonl
        Plus a sweep_summary.json + sweep_summary.csv at the top.

    Returns
    -------
    dict
        Sweep summary with per-seed results + aggregate stats.
    """
    seed_ids = seed_ids if seed_ids is not None else list(SEED_LIBRARY.keys())
    # Filter to known seeds
    seed_ids = [sid for sid in seed_ids if sid in SEED_LIBRARY]
    if not seed_ids:
        raise ValueError("no valid seed_ids; check SEED_LIBRARY")

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    args_list = [
        (sid, budget, max_depth, n_digits, rng_seed, str(out_dir),
         proposer_kind, claude_model, claude_max_api_calls)
        for sid in seed_ids
    ]

    t_start = time.time()
    if workers > 1:
        # Use "spawn" context for cross-platform safety (especially macOS)
        ctx = get_context("spawn")
        with ctx.Pool(workers) as pool:
            results = pool.map(_run_one_seed, args_list)
    else:
        results = [_run_one_seed(args) for args in args_list]
    t_elapsed = time.time() - t_start

    # Aggregate
    n_seeds = len(results)
    n_accepted_total = sum(r["n_accepted"] for r in results)
    n_rejected_total = sum(r["n_rejected"] for r in results)
    n_proposed_total = sum(r["n_proposed"] for r in results)
    n_errors = sum(1 for r in results if r["error"] is not None)
    seeds_with_acceptance = sum(1 for r in results if r["n_accepted"] > 0)

    summary = {
        "n_seeds": n_seeds,
        "budget_per_seed": budget,
        "max_depth": max_depth,
        "n_digits": n_digits,
        "workers": workers,
        "rng_seed": rng_seed,
        "proposer_kind": proposer_kind,
        "claude_model": claude_model if proposer_kind == "claude" else None,
        "claude_max_api_calls": claude_max_api_calls if proposer_kind == "claude" else None,
        "walltime_total_seconds": t_elapsed,
        "walltime_per_seed_avg_seconds": t_elapsed / n_seeds if n_seeds else 0.0,
        "n_proposed_total": n_proposed_total,
        "n_accepted_total": n_accepted_total,
        "n_rejected_total": n_rejected_total,
        "n_seeds_with_acceptance": seeds_with_acceptance,
        "acceptance_rate_per_seed": seeds_with_acceptance / n_seeds if n_seeds else 0.0,
        "n_errors": n_errors,
        "per_seed": results,
    }

    # Write summary
    with (out_dir / "sweep_summary.json").open("w") as f:
        json.dump(summary, f, indent=2)
    # Also a flat CSV for spreadsheet-friendly review
    import csv
    with (out_dir / "sweep_summary.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["seed_id", "n_proposed", "n_accepted", "n_rejected",
                    "walltime_s", "top_reject_reason", "error"])
        for r in results:
            top_reject = max(r["reject_reason_counts"].items(),
                             key=lambda kv: kv[1], default=("", 0))[0]
            w.writerow([r["seed_id"], r["n_proposed"], r["n_accepted"],
                        r["n_rejected"], f"{r['walltime_seconds']:.2f}",
                        top_reject, r["error"] or ""])

    return summary
