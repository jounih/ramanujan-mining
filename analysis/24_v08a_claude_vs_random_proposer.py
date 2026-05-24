"""Mini-benchmark: ClaudeProposer vs RandomProposer on 5 seeds × budget=20 × depth=2.

Per Project C v0.8a (diary 30). Writes results to
`analysis/results/v08a_claude_vs_random_proposer.csv`.

Honest constraints:
  - Requires a working ANTHROPIC_API_KEY.
  - Skips the Claude side (writes a "deferred" row instead) if the key
    isn't usable; the Random side always runs.
  - Per-seed budget of 20, depth=2 — small enough to be affordable
    (~10 API calls per seed × 5 seeds = ~50 API calls, well under the
    ClaudeProposer.max_api_calls cap and well under any reasonable
    daily limit).

Comparison metric: how many seeds yield ≥1 acceptance + total acceptances.
A Claude win = strictly more accepted seeds OR strictly more acceptances
when the seed-count ties. A null result (Claude ties or loses) is
reported honestly per CLAUDE.md "strict honesty" discipline.

Run:
    source .venv/bin/activate
    python analysis/24_v08a_claude_vs_random_proposer.py

Output:
    analysis/results/v08a_claude_vs_random_proposer.csv
    stdout: per-seed table + summary
"""
from __future__ import annotations

import csv
import os
import sys
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

# Try to load .env early so ANTHROPIC_API_KEY (if present) gets onto os.environ
try:
    from dotenv import load_dotenv
    load_dotenv(REPO_ROOT / ".env")
except ImportError:
    pass

OUT_CSV = REPO_ROOT / "analysis" / "results" / "v08a_claude_vs_random_proposer.csv"

# 5-seed benchmark slice — picked to cover the v0.7 operational subset:
#   - 2 Gaussians (mellin_inversion should fire)
#   - 1 half-shift + 1 weighted (v0.7 Poisson dual variants)
#   - 1 Beta integral (master_theorem should fire)
# Same budget=20 across both proposers; same RNG seed for random-fallback
# determinism inside ClaudeProposer.
SEED_IDS = [
    "gaussian_beta_1em2",
    "gaussian_beta_1em4",
    "gaussian_half_shift_beta_1em2",
    "gaussian_weighted_beta_1em2",
    "beta_function_integral",
]
BUDGET = 20
DEPTH = 2
DIGITS = 8
RNG_SEED = 42


def _api_key_usable() -> tuple[bool, str]:
    """Probe whether a real API call can be made. Returns (ok, reason)."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key or not key.strip():
        return False, "ANTHROPIC_API_KEY env var is unset or empty"
    try:
        import anthropic
    except ImportError:
        return False, "anthropic SDK not installed"
    try:
        client = anthropic.Anthropic(api_key=key.strip())
        # Minimal-cost probe: 1-token response to a 1-token prompt.
        r = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=5,
            messages=[{"role": "user", "content": "OK"}],
        )
        _ = r.content
        return True, "ok"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def _run_seed(seed_id, proposer_kind, *, claude_max_api_calls=10):
    """Run search() on one seed with one proposer. Returns metrics dict."""
    import tempfile
    from rkc.search import (
        SearchState, RandomProposer, ClaudeProposer, MpmathVerifier,
        RkcRouter, RkcCostModel, JsonlRegistry, search,
        SEED_LIBRARY, build_seed,
    )
    seed = SEED_LIBRARY[seed_id]
    expr, var = build_seed(seed)
    if proposer_kind == "claude":
        proposer = ClaudeProposer(
            seed=RNG_SEED, max_api_calls=claude_max_api_calls,
        )
    else:
        proposer = RandomProposer(seed=RNG_SEED)
    with tempfile.TemporaryDirectory() as tmp:
        registry = JsonlRegistry.with_dir(tmp)
        t0 = time.time()
        summary = search(
            initial_state=SearchState(payload=expr, metadata={"var": var}),
            proposer=proposer,
            verifier=MpmathVerifier(n_digits=DIGITS),
            router=RkcRouter(),
            cost_model=RkcCostModel(),
            registry=registry,
            budget=BUDGET,
            max_depth=DEPTH,
        )
        elapsed = time.time() - t0
    extra = {}
    if proposer_kind == "claude" and hasattr(proposer, "stats"):
        s = proposer.stats()
        extra["api_calls"] = s.get("api_calls", 0)
        extra["fallback_active"] = s.get("fallback_active", False)
    return {
        "seed_id": seed_id,
        "proposer": proposer_kind,
        "n_proposed": summary.n_proposed,
        "n_accepted": summary.n_accepted,
        "n_rejected": summary.n_rejected,
        "walltime_s": round(elapsed, 2),
        **extra,
    }


def main() -> int:
    print(f"Project C v0.8a mini-benchmark — Claude vs Random proposer")
    print(f"  seeds   : {SEED_IDS}")
    print(f"  budget  : {BUDGET}")
    print(f"  depth   : {DEPTH}")
    print(f"  digits  : {DIGITS}")
    print()

    ok, reason = _api_key_usable()
    rows: list[dict] = []

    # Always run the random side
    print("=== RandomProposer side ===")
    for sid in SEED_IDS:
        r = _run_seed(sid, "random")
        print(f"  {sid:40s}  proposed={r['n_proposed']:3d}  "
              f"accepted={r['n_accepted']:3d}  walltime={r['walltime_s']:.2f}s")
        rows.append(r)

    print()
    if ok:
        print("=== ClaudeProposer side (live API) ===")
        for sid in SEED_IDS:
            try:
                r = _run_seed(sid, "claude")
            except Exception as e:
                r = {
                    "seed_id": sid, "proposer": "claude",
                    "n_proposed": 0, "n_accepted": 0, "n_rejected": 0,
                    "walltime_s": 0.0, "api_calls": 0,
                    "fallback_active": False, "error": str(e),
                }
            note = ""
            if "fallback_active" in r and r["fallback_active"]:
                note = "  [STUB FALLBACK — no live calls made]"
            elif "api_calls" in r:
                note = f"  [api_calls={r['api_calls']}]"
            print(f"  {r['seed_id']:40s}  proposed={r['n_proposed']:3d}  "
                  f"accepted={r['n_accepted']:3d}  walltime={r['walltime_s']:.2f}s{note}")
            rows.append(r)
    else:
        print(f"=== ClaudeProposer side: SKIPPED ===")
        print(f"  Reason: {reason}")
        print(f"  This row is recorded as 'deferred' in the CSV; rerun this script")
        print(f"  once a working ANTHROPIC_API_KEY is available.")
        for sid in SEED_IDS:
            rows.append({
                "seed_id": sid, "proposer": "claude_deferred",
                "n_proposed": 0, "n_accepted": 0, "n_rejected": 0,
                "walltime_s": 0.0,
                "note": f"deferred — {reason}",
            })

    # Write CSV — collect union of keys, write deterministic order
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "seed_id", "proposer", "n_proposed", "n_accepted", "n_rejected",
        "walltime_s", "api_calls", "fallback_active", "note", "error",
    ]
    with OUT_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)
    print()
    print(f"Wrote: {OUT_CSV.relative_to(REPO_ROOT)}")

    # Summary
    print()
    print("=== Summary ===")
    rand_rows = [r for r in rows if r.get("proposer") == "random"]
    claude_rows = [r for r in rows if r.get("proposer") == "claude"]
    rand_acc = sum(r["n_accepted"] for r in rand_rows)
    claude_acc = sum(r["n_accepted"] for r in claude_rows)
    rand_seeds_with_acc = sum(1 for r in rand_rows if r["n_accepted"] > 0)
    claude_seeds_with_acc = sum(1 for r in claude_rows if r["n_accepted"] > 0)
    print(f"  Random : {rand_acc:3d} total acceptances across "
          f"{rand_seeds_with_acc}/{len(rand_rows)} seeds")
    if claude_rows:
        print(f"  Claude : {claude_acc:3d} total acceptances across "
              f"{claude_seeds_with_acc}/{len(claude_rows)} seeds")
        if claude_acc > rand_acc:
            print("  Verdict: Claude > Random (more total acceptances)")
        elif claude_acc < rand_acc:
            print("  Verdict: Claude < Random (Random found more)")
        else:
            print("  Verdict: tie on acceptances")
    else:
        print("  Claude : DEFERRED — no live API access")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
