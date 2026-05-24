# Diary 34 — Project C v0.9: `InSessionClaudeProposer` (host-LLM-as-proposer via file IPC)

**Date:** 2026-05-24
**Source:** New class `rkc.search.proposers.InSessionClaudeProposer`
formalising the file-based IPC pattern proved out in
[`analysis/25_in_session_claude_proposer_demo.py`](../analysis/25_in_session_claude_proposer_demo.py)
(the v0.8b commit `9630799`). CLI flag `--proposer in-session` on `rkc
sweep` and `rkc search`, with `--in-session-dir` and
`--in-session-timeout` parameters. New 7 v0.9b tests in
`rkc/tests/test_cli.py` (all `test_v09b_*`). New demo script
[`analysis/27_v09_in_session_proposer_demo.py`](../analysis/27_v09_in_session_proposer_demo.py).
**Status:** SHIPPED. **99/99 tests passing** (87 baseline + 5 from
parallel v0.9-hardy `ConvergenceClass` work + 7 new v0.9b tests).

## Setup

The v0.8a `ClaudeProposer` (diary 30, commit `a5d512d`) ships an LLM
proposer that calls the Anthropic API per turn. User feedback after
shipping v0.8a was sharp: *"you ARE Claude, why do you need an API
key?"* The cleanest form for an in-conversation run is to have the
**host LLM** (the agent driving the Claude Code session) BE the
proposer directly — no separate API call, no token cost, no extra
context window.

The proof-of-concept (`analysis/25_*.py`, shipped with v0.8b) showed
the round-trip works: the canonical Gaussian seed, budget=1, 1
proposed → 1 accepted, cost ratio 54×. v0.9's job: formalise that
pattern as a production proposer.

## Design

**File-based IPC** between the engine (a Python loop) and the host LLM
(a separate agent). The protocol:

  1. On each `propose()`, write the (system prompt + user prompt +
     state hash + basis op_ids) to `<session_dir>/proposer_inbox.json`.
  2. Poll `<session_dir>/proposer_outbox.json` for at most
     `timeout_s` seconds.
  3. Host LLM reads inbox, decides on an op_id, writes outbox.
  4. Engine reads outbox, parses, returns `OperatorApplication`.
  5. Both files are cleaned up before the next turn so `outbox.exists()`
     unambiguously means "the host responded to THIS ask".

The inbox payload is the SAME prompt-building path as `ClaudeProposer`
uses (`_SYSTEM_PROMPT_TEMPLATE` + `_build_user_prompt`) so the two
implementations can't drift on prompt engineering. The Hunt 5b
toolkit-split heuristics (per diary 25) ride along automatically.

Outbox parsing reuses the same logic as `ClaudeProposer._parse_response`:
accepts strict JSON, JSON-in-code-fences, or first `{...}` block.

## Fallback / safety semantics

The proposer NEVER blocks forever and NEVER throws from `propose()`:

  | Failure mode | Behaviour |
  |---|---|
  | Outbox not written within `timeout_s` | Fall back to `RandomProposer` for THIS TURN; log a warning; continue |
  | Outbox is unparseable JSON | Same |
  | Outbox parsed but `op_id` not in basis | Same |
  | Same state called twice | Second call served from in-process cache (zero round-trips) |

The fallback `RandomProposer` shares the in-session proposer's `seed`,
so timeout-degradation is **deterministic** under a fixed seed. This
matters for reproducibility in long sweeps where some asks time out
mid-run.

Per CLAUDE.md "no silent failures": every fallback logs the reason at
WARNING. Stats are tracked in `proposer.stats()`:
`n_round_trips / n_cache_hits / n_timeouts / n_malformed / cache_size`.

## Host-side helper

`InSessionClaudeProposer.poll_and_respond(session_dir, decide_fn)` —
a static helper for the host LLM side. The host can either watch the
session dir directly (read inbox, write outbox) or call this helper
with a `decide_fn(payload_dict) → op_id_str_or_dict` callback.

The helper terminates on:
  - `max_responses` rounds served, OR
  - `max_idle_s` seconds elapsed since last activity, OR
  - `decide_fn` returns `None`.

Primary use cases: tests (spawn `poll_and_respond` in a thread, run
`propose()` in main thread, verify the contract end-to-end) and
scripted hosts. **The Claude Code session driving the engine does not
need this helper** — it can just `Read` and `Write` the files directly.

## What shipped

- `rkc/search/proposers.py::InSessionClaudeProposer` + the
  `poll_and_respond` helper.
- Exposed via `rkc.search.__init__` alongside the existing
  `RandomProposer / ClaudeProposer / ClaudeStubProposer`.
- CLI: `rkc sweep --proposer in-session [--in-session-dir DIR]
  [--in-session-timeout SECONDS]`. Same flags on `rkc search`. The
  sweep worker (`rkc/search/sweep.py::_run_one_seed`) was extended to
  accept and forward the in-session params; backward-compat 6-tuple +
  9-tuple paths are preserved alongside the new 11-tuple.
- Tests (7 new `test_v09b_*` cases):
  - `test_v09b_in_session_proposer_uses_inbox_outbox` — full round-trip
    with a fake host in a thread; verifies inbox shape, outbox parsing,
    returned op_id.
  - `test_v09b_in_session_proposer_timeout_falls_back` — no host;
    proposer times out, falls back to random, returns a basis op_id,
    inbox/outbox are cleaned up.
  - `test_v09b_in_session_proposer_parses_malformed_response` — three
    malformed cases (non-JSON prose, wrong-shape JSON, unknown op_id);
    each one falls back cleanly + increments `n_malformed`.
  - `test_v09b_in_session_proposer_cache_hit` — same state called
    twice; second call is a cache hit (zero host round-trips).
  - `test_v09b_cli_search_accepts_in_session_flag` — CLI plumbing
    (short timeout, search completes with fallback).
  - `test_v09b_cli_sweep_accepts_in_session_flag` — same for sweep.
  - `test_v09b_in_session_proposer_protocol_conformance` — structural
    typing satisfies the `Proposer` protocol.
- Demo: `analysis/27_v09_in_session_proposer_demo.py` with three modes:
  `--print-protocol` (schema reference), default (one scripted
  round-trip + 3-seed sweep with fast timeout fallback), and
  `--interactive` (5-minute timeout, blocks on each ask waiting for a
  real host).

## Numerical sanity (non-interactive demo run)

```
Step 1: demonstrating ONE round-trip with a scripted host
  [engine] proposer.propose(...) — writing inbox at:
           /tmp/rkc_in_session_demo_18873/_round_trip_demo/proposer_inbox.json
  [host] inbox received (91 chars of user prompt)
  [host] picking mellin_inversion (Gaussian → Poisson dual)
  [engine] received op_id='mellin_inversion'
  [engine] stats: {'n_round_trips': 1, 'n_cache_hits': 0,
                   'n_timeouts': 0, 'n_malformed': 0, 'cache_size': 1}

Step 2: running the sweep (auto-fallback — short timeout → RandomProposer)
  gaussian_beta_1em2:         5/1/4  (1.9s)  timeouts=5
  gaussian_beta_1em4:         5/0/5  (1.8s)  timeouts=5
  beta_function_integral:     5/1/4  (3.5s)  timeouts=5
```

The fallback path is exercised end-to-end and the engine still produces
acceptances (2 of 3 seeds) because RandomProposer's random ops include
the matching choice often enough at budget=5.

## Coordination with parallel subagents

Two other subagents ran in parallel for v0.9:

- **v0.8c** extending `_modular_transform_with_correction_apply` in
  `basis.py`. Uses `test_v08c_*` tests.
- **v0.9-hardy** implementing `_hardy_orders_apply` in `basis.py`
  + adding `ConvergenceClass` field to `SearchState`. Uses `test_v09a_*`
  tests.

My v0.9-proposer agent stayed entirely in `proposers.py`, `cli.py`,
`sweep.py`, `__init__.py`, the new test file additions, and the new
demo + diary. No `basis.py` overlap. The only `__init__.py` merge
point was the v0.9-hardy `ConvergenceClass` export; my edit added
`InSessionClaudeProposer` to the existing imports/`__all__` cleanly.

## Bottom-line claim (confidence: high)

The in-session proposer pattern is now a production code path with
deterministic fallback, structured logging, byte-exact prompt
equivalence to `ClaudeProposer`, and 7 dedicated tests covering the
core contract + error paths.

This unblocks the "use the host Claude Code session as the proposer"
workflow for in-conversation runs — the natural form when the agent
driving the session is itself an LLM and the API round-trip would be
wasteful. The headline cost saving: ZERO token cost for proposer
decisions when running inside Claude Code, vs. the per-call
Anthropic-API cost of `ClaudeProposer`.

## What's not shipped (deferred to v0.9.1)

1. **A live end-to-end run inside this Claude Code session** — the
   demo script exists and the round-trip is proven, but the actual
   "Claude Code session drives the engine, makes per-turn decisions"
   loop is a follow-up: it requires either an interactive run with the
   user iterating on responses, or a background-task watcher that the
   host LLM polls.
2. **Per-state history forwarding.** Like v0.8a, the engine doesn't
   yet thread per-state reject history into the proposer's user
   prompt. The hook is in place (`InSessionClaudeProposer` builds the
   user prompt via the shared `_build_user_prompt` which accepts
   `prior_attempts`); we just need the engine to call `set_history()`
   per state. Trivial follow-up.
3. **Multi-host arbitration.** If two engines write to the same
   session_dir simultaneously, the contract breaks. The per-worker
   `session_dir = base / seed_id` partitioning in `sweep.py` handles
   the multiprocessing-sweep case but not arbitrary multi-engine
   scenarios. v0.9.1 could add a lock file if needed.

Add to `todo.md`:
- T0c: v0.9 in-session proposer — thread per-state reject history
  through `set_history()` so the host LLM sees prior failed attempts
  (parity with v0.8a `ClaudeProposer.set_history`).
- T0d: v0.9 interactive demo — record a live run where this Claude
  Code session is the host (writing outbox files in response to inbox
  files) and the engine produces ≥1 acceptance from the LLM's
  decisions, not the random fallback.
