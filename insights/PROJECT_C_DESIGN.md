# Project C — RKC-guided symbolic search (the "practical Ramanujan latent speedrun" system)

User-supplied framing from a parallel chat:

> Project C — RKC-guided symbolic search.
> Use a neural model to propose transformations, but only keep candidates
> that pass RKC + numerical verification.
>
> Loop:
> 1. choose expression
> 2. neural model proposes operator sequence
> 3. RKC normalizes and routes
> 4. verifier tests to high precision
> 5. cost model decides whether it is actually useful
> 6. store accepted identity or reject with failure reason
>
> *This is the practical "Ramanujan latent speedrun" system.*

Plus ChatGPT's one-sentence consolidation: *"use nonlinear ICA / JEPA to
learn latent operator representations and propose transformations, while
RKC acts as the symbolic verifier/router that prunes the search space and
safely accelerates structured physics/EBM computations"* — with reference
to [Hyvärinen, Khemakhem, Morioka 2023, arXiv:2303.16535](https://arxiv.org/abs/2303.16535)
(review of nonlinear ICA identifiability).

This file is the concrete design + scope for that system in the context
of this run.

## Relationship to existing run threads

Project C unifies three previously-separate todo items:

- **W5** (small operator-composition search prototype) — *the v0
  pure-symbolic baseline of Project C*
- **T3** (operator-composition search engine as v0.3 rkc milestone) — *the
  full implementation of Project C with the neural proposer*
- **X3** (build T3 as shared artefact with arc-agi-ebm-agent) — *the
  cross-repo reusable extraction of Project C's `search` module*

Going forward, **W5 / T3 / X3 are collectively Project C**. The label
"Project C" is the one to use externally; "W5/T3/X3" stays as the internal
priority tags.

## The six-step loop, mapped to existing rkc surface

| Step | Project C says | rkc surface available today | Status |
|---|---|---|---|
| 1. choose expression | (user / harness picks) | n/a (harness concern) | n/a |
| 2. neural model proposes operator sequence | nonlinear ICA / JEPA proposer | **not yet present** — needs design | TODO |
| 3. RKC normalizes and routes | `rkc.recognize` + `rkc.routing` | **shipped (v0.3)** + CLI `rkc recognize` / `rkc compare` | done |
| 4. verifier tests to high precision | mpmath PSLQ + per-kernel certificates | partially shipped via `rkc.completions` (Watson-Hickerson); needs general "is X numerically equal to Y to N digits" wrapper | partial |
| 5. cost model decides whether it is actually useful | `rkc.costs` per-term + per-route cost | **shipped (v0.3)** | done |
| 6. store accepted identity or reject with failure reason | (a registry of accepted identities + a reject log with reason taxonomy) | **not yet present** — `rkc.registry` holds *kernels* (pre-defined), not *discovered identities* | TODO |

**What we have:** steps 3 and 5 are operational and exposed via the
[rkc v0.1 CLI](../rkc/cli.py) (`recognize`, `compare`, `certify`).

**What's missing:** steps 2 (proposer), 4 (general verifier wrapper), and 6
(accepted-identity registry + reject log).

## v0 baseline — pure-symbolic Project C without the neural proposer

The right first step is NOT to start training a JEPA / nonlinear-ICA model.
The right first step is the **pure-symbolic baseline**: random
operator-composition + RKC verification + cost-model gate. This is W5
restated; it produces a controlled baseline that:

- exercises steps 3, 5, 6 of the loop end-to-end
- gives a baseline "how many genuinely-new identities per 1000 random
  compositions" number to beat
- exposes whether step 4 (general verifier) is the bottleneck (likely yes)
- exposes whether step 6 (registry of discovered identities) needs schema
  work (likely yes)
- lets us measure: of N random compositions, what fraction (a) collapse to
  a known kernel, (b) collapse to a tautology, (c) produce a numerically-
  verifiable but already-known identity, (d) produce a numerically-
  verifiable genuinely-new identity. (a)-(c) are "rediscovery"; (d) is the
  signal.

**v0 scope (bounded ~1-2 weeks):**

1. Define the operator basis. Start with the Hunt 5 revised 7-operator
   set: `mellin_inversion`, `master_theorem`, `FOURIER_SELF_RECIPROCITY`,
   `FRACTIONAL_FUNCTIONAL_ITERATION`, `HARDY_ORDERS_OF_INFINITY`,
   `FRULLANI_LIMIT`, `MELLIN_PAIR_RECIPROCITY`. As `rkc.search.OperatorBasis`.
2. Define the composition rule. Each operator is `Op: Expr × Params →
   Expr | None`. Compositions are sequences of length 1-5 operators.
3. Define the verifier. `verify(expr_a, expr_b, n_digits=40) → bool` —
   numerical equality to n_digits over a sweep of parameter values.
4. Define the cost-model gate. `gate(expr_a, expr_b) → ACCEPT | REJECT(reason)`
   where ACCEPT requires (a) verifier passes, (b) expr_b has lower
   `total_cost` per rkc than expr_a, (c) expr_b is not trivially equal to
   expr_a (no nullable composition).
5. Define the registry. `DiscoveredIdentitiesRegistry` = JSONL of accepted
   (input_expr, operator_sequence, output_expr, certificate, savings)
   records, with content-addressable IDs.
6. Define the reject taxonomy. NOT_ENOUGH_DIGITS, VERIFIER_FAILED,
   COST_NOT_IMPROVED, ALREADY_IN_REGISTRY, OPERATOR_DOMAIN_VIOLATION,
   NUMERICAL_INSTABILITY, TIMED_OUT.

Output: `rkc/search/` module with a CLI `rkc search --basis qr7 --max-depth 3
--budget 1000 --seed-expressions examples/seeds.yaml`.

## v1 — neural proposer (the actual Project C)

After v0 baseline, add the neural proposer. Architectural caveats:

1. **The neural proposer is a SEPARATE module from rkc.** Keep `rkc.search`
   pluggable so the proposer interface is `Proposer.next_candidate(state)
   → OperatorSequence`. v0's proposer is `RandomProposer`; v1 adds
   `NeuralProposer`. arc-agi-ebm-agent's proposer would be a third
   instance.
2. **Nonlinear ICA / JEPA is a defensible default but not the only choice.**
   The Hyvärinen-Khemakhem-Morioka 2023 review summarises why
   identifiable nonlinear ICA needs auxiliary information (operator label
   during training; class label at test time). JEPA gives the
   self-supervised loss; nonlinear-ICA-style identifiability conditions
   give the theoretical guarantee that the learned latents correspond to
   the operators. Together they're a principled choice. But the
   **interface** is just "given current expression state, propose next
   operator(s)" — any neural / symbolic / hybrid module satisfying that
   works.
3. **Caveat on basis size.** The current 7-operator basis is too small for
   nonlinear ICA to be the right tool — a categorical classifier with
   7 classes is overkill territory. ICA becomes valuable when the basis
   scales to ~100s (e.g. parameterised operator families:
   `master_theorem(φ_class)` × `mellin_inversion` × …). Plan: start
   categorical; switch to ICA latent space when basis cardinality
   crosses a threshold that makes search-over-discrete-sequences
   intractable.

## Critical engineering decisions

1. **Verifier scope (step 4).** General-purpose "is f(α, β) numerically
   equal to g(α, β) to N digits" is harder than it sounds. Failure modes:
   - Branch cuts (log, fractional powers) on different sides
   - Different convergence regimes (one side converges at α=0.1, the other
     needs α<0.01)
   - Spurious symbolic cancellations that hide divergences
   The B1 closure investigation hit these repeatedly (see
   [DID_NOT_PAN_OUT.md R1, R2, R7-R10](DID_NOT_PAN_OUT.md)). Re-using
   that experience is critical.

2. **"Cost model decides whether it is actually useful" (step 5)** —
   needs to commit to *useful for what*:
   - **Speedup mode**: keep transformations that reduce per-term cost or
     term count at fixed precision. This is the Pass A criterion.
   - **Identity discovery mode**: keep transformations that produce a
     numerically-true identity not already in the registry. Cost is not
     the criterion — novelty is.
   - **Hybrid**: keep transformations that are (novel) OR (known-but-
     cheaper-than-current). This is what Ramanujan himself was doing.

   v0 commits to *hybrid*; v1+ can refine.

3. **The reject-with-failure-reason log is methodologically critical.**
   It's the analogue of [DID_NOT_PAN_OUT.md](DID_NOT_PAN_OUT.md) for the
   automated search. Per CLAUDE.md noisy-positive discipline: a candidate
   that passes verification at 30 digits but fails at 100 is a near-match,
   NOT an accepted identity. The reject taxonomy needs to capture this
   granularity.

## Mapping to the sibling repos (per CROSS_REPO_LEVERAGE)

- **arc-agi-ebm-agent**: Project C IS the architecture. ARC's
  program-induction loop = Project C with (a) ARC DSL operators replacing
  the Hunt 5 basis, (b) "task examples match" replacing "numerical
  equality to N digits", (c) "rule passes hidden test pairs" replacing
  "cost model decides useful". The `rkc.search` interface (proposer,
  verifier, gate, registry) is the shared spine; the per-instance
  operator basis + verifier + gate are repo-specific. X3 = pull this
  spine out as a shared package.

- **aether-hardware-ebm**: Project C is less direct. EqProp has a fixed
  energy function; it doesn't *propose* new energy functions. But the
  Project C *registry* schema (input, transformation, output, cost,
  certificate) is the H4 evidence-claim format the hardware repo wants
  for its boundary-evidence contracts. X2 + the Project C registry
  schema overlap.

- **aether-audio**: Project C is mostly irrelevant. Audio identification
  is parameter-fitting (continuous), not symbolic search (discrete).
  Possible exception: searching over physical-audio *topologies*
  (resonator configurations) is discrete and could use a Project C-style
  loop — but that's a future direction, not an immediate transfer.

## Open questions

1. Is the current rkc registry — which holds 11 *predefined kernels* — the
   right substrate for the Project C *accepted-identities registry* —
   which would hold thousands of discovered identities? Probably not; the
   data structure is different (sparse symbolic kernels vs dense identity
   records). v0 should use a separate JSONL store.

2. How does Project C interact with the umbral / fractional / Eisenstein
   extensions (W6, T2, T4)? Those extend the operator basis. Project C
   composition search would benefit from the larger basis but requires
   each new operator to expose the matcher/cost/verifier interface
   uniformly. Refactor: define `Operator` protocol in `rkc/search/`
   before adding new kernels so they all satisfy it.

3. What's the controlled-validation case? For W5/Project C v0, the
   answer is: random composition of the 7-op basis on a curated set of
   ~20 seed Ramanujan identities; the metric is "of N random
   compositions, how many recover one of the ~50 known kernel identities
   in the rkc registry". Targets to beat: ≥80% of registry identities
   recovered within budget=1000 compositions of length ≤3.

## See also

- [BIG_IDEAS_REVIEW.md §7](BIG_IDEAS_REVIEW.md) — original framing of the
  operator-composition search engine as W5
- [rkc/MILESTONES.md §v0.3](../rkc/MILESTONES.md) — Project C is the v0.3
  milestone
- [CROSS_REPO_LEVERAGE.md §arc-agi-ebm-agent](CROSS_REPO_LEVERAGE.md) — why
  Project C is the right shared artefact with the ARC repo
- [todo.md "Y1"](../todo.md) — Project C v0 pure-symbolic baseline
