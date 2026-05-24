"""27_v09_in_session_proposer_demo.py — Demonstrate Project C v0.9
`InSessionClaudeProposer`: host-LLM-as-proposer via file-based IPC.

Per v0.9 (diary 34), the proposer writes its prompt to a JSON inbox file,
blocks waiting for a JSON outbox file to appear, then reads the host
LLM's decision. The proof-of-concept that motivated this formalization
is `analysis/25_in_session_claude_proposer_demo.py`.

This demo runs a small sweep (3 seeds × budget=5 × depth=1) under the
new proposer. For the first proposer ask, it prints a clear instruction
explaining how a host LLM could respond:

  - inbox path
  - outbox path
  - expected JSON shape

It then continues without a host (i.e., each ask times out fast and falls
back to RandomProposer). This way the script TERMINATES without a human
in the loop while still exercising the v0.9 codepath end-to-end.

For an INTERACTIVE run with a real host (e.g., this Claude Code session
acting as the proposer), use `--interactive` and the script will block on
each ask until you write the outbox file.

Run modes:
  python analysis/27_v09_in_session_proposer_demo.py
      One sweep with short timeouts (no host) — terminates in seconds.

  python analysis/27_v09_in_session_proposer_demo.py --interactive
      One sweep with 5-minute timeouts; blocks waiting for a host to
      write the outbox after each ask. Useful when running INSIDE a
      Claude Code session: print the inbox path, ask Claude to pick an
      op_id, write the outbox.

  python analysis/27_v09_in_session_proposer_demo.py --print-protocol
      Print the inbox/outbox JSON schema + an example exchange, exit.
"""
from __future__ import annotations

import argparse
import json
import sys
import threading
import time
from pathlib import Path

import sympy as sp

from rkc.search import (
    SEED_LIBRARY,
    InSessionClaudeProposer,
    SearchState,
    MpmathVerifier,
    RkcRouter,
    RkcCostModel,
    JsonlRegistry,
    search,
    build_seed,
)


def print_protocol() -> int:
    """Document the inbox/outbox JSON contract for human / host-LLM readers."""
    print("=" * 72)
    print("InSessionClaudeProposer file-IPC protocol — v0.9")
    print("=" * 72)
    print()
    print("Each propose() call:")
    print("  1. The engine writes `proposer_inbox.json` to the session_dir.")
    print("  2. The engine blocks on `proposer_outbox.json` (with timeout).")
    print("  3. The host LLM (or test fake) reads the inbox, decides on an")
    print("     op_id, writes the outbox.")
    print("  4. The engine consumes the outbox, deletes both files, returns")
    print("     an OperatorApplication.")
    print()
    print("INBOX SCHEMA (engine → host):")
    print(json.dumps({
        "version": "v0.9",
        "state_hash": "<first 16 chars of sha256(system_prompt + user_prompt)>",
        "system_prompt": "<the same prompt ClaudeProposer would send via the API>",
        "user_prompt": "<per-state user prompt: current expression + var + ...>",
        "expected_response_schema": {
            "op_id": "<one of the basis op ids>",
            "rationale": "<≤12 words>",
        },
        "basis_op_ids": [
            "master_theorem", "fractional_functional_iteration",
            "frullani_limit", "...",
        ],
    }, indent=2))
    print()
    print("OUTBOX SCHEMA (host → engine):")
    print(json.dumps({
        "op_id": "<one of basis_op_ids>",
        "rationale": "<optional one-liner, ≤12 words>",
    }, indent=2))
    print()
    print("FALLBACK:")
    print("  - Outbox never written within timeout_s → fall back to")
    print("    RandomProposer for that turn, log a warning, continue.")
    print("  - Outbox written but unparseable / op_id not in basis → same.")
    return 0


def run_sweep(session_dir: Path, interactive: bool) -> int:
    """Run a 3-seed × budget=5 × depth=1 sweep under InSessionClaudeProposer.

    In non-interactive mode (default): short timeouts so each ask falls
    through to RandomProposer fast and the script terminates.

    In interactive mode: 5-minute timeouts; the FIRST ask is printed
    loudly; subsequent asks are also written to disk (the host can
    respond to each at its own pace).
    """
    seed_ids = ["gaussian_beta_1em2", "gaussian_beta_1em4",
                "beta_function_integral"]
    timeout_s = 300.0 if interactive else 0.3

    print("=" * 72)
    print(f"v0.9 in-session proposer demo — {len(seed_ids)} seeds × budget=5 × depth=1")
    print("=" * 72)
    print(f"  session_dir : {session_dir}")
    print(f"  timeout_s   : {timeout_s} ({'INTERACTIVE' if interactive else 'auto-fallback'})")
    print(f"  seeds       : {seed_ids}")
    print()

    out_dir = Path("analysis/results/27_v09_in_session_demo")
    out_dir.mkdir(parents=True, exist_ok=True)

    # In non-interactive mode, demonstrate ONE clean round-trip first —
    # the user sees what a successful exchange looks like, before the
    # rest of the sweep falls through on timeout.
    if not interactive:
        demo_dir = session_dir / "_round_trip_demo"
        demo_dir.mkdir(parents=True, exist_ok=True)
        print("-" * 72)
        print("Step 1: demonstrating ONE round-trip with a scripted host")
        print("-" * 72)
        demo_proposer = InSessionClaudeProposer(
            session_dir=demo_dir, timeout_s=5.0, poll_interval_s=0.02, seed=0,
        )

        def scripted_host():
            def decide(payload):
                inbox_size = len(payload.get("user_prompt", ""))
                print(f"  [host] inbox received ({inbox_size} chars of user prompt)")
                print(f"  [host] picking mellin_inversion (Gaussian → Poisson dual)")
                return {"op_id": "mellin_inversion",
                        "rationale": "Gaussian Poisson dual"}
            InSessionClaudeProposer.poll_and_respond(
                demo_dir, decide_fn=decide,
                poll_interval_s=0.02, max_responses=1, max_idle_s=5.0,
            )

        t = threading.Thread(target=scripted_host, daemon=True)
        t.start()
        n = sp.Symbol("n", integer=True, positive=True)
        demo_state = SearchState(
            payload=sp.exp(-sp.Rational(1, 100) * n**2), metadata={"var": n},
        )
        print(f"  [engine] proposer.propose(...) — writing inbox at:")
        print(f"           {demo_proposer.inbox_path}")
        result = next(iter(demo_proposer.propose(demo_state, budget=1)))
        t.join(timeout=10.0)
        print(f"  [engine] received op_id={result.op_id!r}")
        print(f"  [engine] stats: {demo_proposer.stats()}")
        print()

    # ---- Sweep proper -----
    print("-" * 72)
    print("Step 2: running the sweep " + (
        "(interactive — host LLM responds to each ask)" if interactive
        else "(auto-fallback — short timeout → RandomProposer)"))
    print("-" * 72)
    if interactive:
        print()
        print("INSTRUCTIONS FOR HOST LLM:")
        print(f"  Watch for files appearing under:  {session_dir}")
        print(f"  Each ask creates a file named:     proposer_inbox.json")
        print(f"  Respond by writing JSON to:        proposer_outbox.json")
        print(f"  Run `python {__file__} --print-protocol` for the schema.")
        print()

    per_seed_summary: list[dict] = []
    for sid in seed_ids:
        seed_def = SEED_LIBRARY[sid]
        expr, var = build_seed(seed_def)
        seed_out = out_dir / sid
        seed_out.mkdir(parents=True, exist_ok=True)
        sess_for_seed = session_dir / sid
        sess_for_seed.mkdir(parents=True, exist_ok=True)
        proposer = InSessionClaudeProposer(
            session_dir=sess_for_seed,
            timeout_s=timeout_s,
            poll_interval_s=0.05,
            seed=42,
        )
        registry = JsonlRegistry.with_dir(seed_out)
        state = SearchState(payload=expr, metadata={"var": var})
        t0 = time.time()
        summary = search(
            initial_state=state,
            proposer=proposer,
            verifier=MpmathVerifier(n_digits=10),
            router=RkcRouter(),
            cost_model=RkcCostModel(),
            registry=registry,
            budget=5,
            max_depth=1,
            verbose=False,
        )
        elapsed = time.time() - t0
        s = proposer.stats()
        print(f"  {sid}:")
        print(f"    proposed/accepted/rejected = "
              f"{summary.n_proposed}/{summary.n_accepted}/{summary.n_rejected}  "
              f"({elapsed:.1f}s)")
        print(f"    proposer stats: round_trips={s['n_round_trips']} "
              f"cache_hits={s['n_cache_hits']} timeouts={s['n_timeouts']} "
              f"malformed={s['n_malformed']}")
        per_seed_summary.append({
            "seed_id": sid,
            "n_proposed": summary.n_proposed,
            "n_accepted": summary.n_accepted,
            "n_rejected": summary.n_rejected,
            "elapsed_s": elapsed,
            "proposer_stats": s,
        })

    print()
    print("=" * 72)
    print("Sweep complete")
    print("=" * 72)
    print(f"  per-seed JSON summary:    {out_dir}/sweep_summary.json")
    with (out_dir / "sweep_summary.json").open("w") as f:
        json.dump({"seeds": per_seed_summary, "timeout_s": timeout_s,
                   "interactive": interactive}, f, indent=2)
    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        description="v0.9 InSessionClaudeProposer demo")
    p.add_argument("--interactive", action="store_true",
                   help="Block on each ask waiting for a host LLM "
                        "(default: short timeout + RandomProposer fallback)")
    p.add_argument("--print-protocol", action="store_true",
                   help="Print the inbox/outbox JSON schema, exit")
    p.add_argument("--session-dir", default=None,
                   help="Session dir for file IPC "
                        "(default: /tmp/rkc_in_session_demo_<pid>/)")
    args = p.parse_args()

    if args.print_protocol:
        return print_protocol()

    session_dir = Path(args.session_dir) if args.session_dir else Path(
        f"/tmp/rkc_in_session_demo_{__import__('os').getpid()}")
    session_dir.mkdir(parents=True, exist_ok=True)
    return run_sweep(session_dir, interactive=args.interactive)


if __name__ == "__main__":
    raise SystemExit(main())
