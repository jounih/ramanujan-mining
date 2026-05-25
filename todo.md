# Ramanujan Mining Run — Live TODO

The live list of open action items. The bottom of the file preserves the
historical record of completed work. New work goes near the top; finished work
gets moved into the historical record.

**Last major update:** 2026-05-25, after the user's "verification is key"
pivot. Adversarial verification subagents in-flight for the last batch of
ChatGPT-Pro claims (cycles 16-25).

---

## ★ EPISTEMIC POSTURE (per user 2026-05-25) ★

**User said:** "we are really just probing ChatGPT pro. Is cool... but not
sure we can publish something new based on this? Any closed form solutions
that accelerate will be useful though." then: "test the claims and also
find if they've already been discovered and published. Adversarial
verification (actively try to refute) + automated literature diff."

**Standing rule:** No new ChatGPT-Pro prompts until the in-flight
verification + literature-diff subagents return verdicts. If a claim is
CONFIRMED + NOVEL → keep it. If CONFIRMED + KNOWN → reframe as
"verified-implementation", not "novel finding". If REFUTED → retract in
diary + DID_NOT_PAN_OUT.md + paper draft.

## ★ VERIFICATION SUBAGENT VERDICTS (2026-05-25, ALL RETURNED) ★

All 4 verification subagents have returned. Headline:

| # | Agent ID | Scope | Verdict |
|---|---|---|---|
| #66 | `a523969af20acdada` | Adversarial AB LN Part IV Entry 4.2.3 defense | **CONFIRMED at HIGH confidence (diary 57)**. 5 independent paths converge. AB's error pinpointed at 3 levels. Recommended: Ramanujan Journal / HRJ corrigendum, 3-5 pages. **HEADLINE REAL CONTRIBUTION.** |
| #67 | `a1162a324b4618a72` | Adversarial Level-pq family + literature diff | **NUMERICALLY CONFIRMED (25/25 at dps=200), NOVELTY DOWNGRADED (diary 58)**. Structure is classical (dim E_2(Γ_0(pq)) = 3). Engine autonomously rediscovered. Recalibrated: 9.5/10 → 4.5/10; Math.Mag./Amer.Math.Monthly expository note, 2-4 pages. |
| #68 | `a7c6cab78eacccfea` | Implement + verify 4 cross-domain accelerators | **ALL 4 CONFIRMED CORRECTNESS (diary 59)**. (a) 50× attention; (b) 74,917× annular Green; (c) machine-eps PH; (d) 70+ digits Airy. Tests 118 → 132. |
| afdb928cbba37f1aa | Web prior-art audit of (a)-(d) | **3 KNOWN + 1 PARTIAL (diary 60)**. (a) = RetNet/SSD-multi-head; (b) = Crowdy-Marshall + packaging novelty; (c) = Schrödinger 1914 + Trovato 2016; (d) = DLMF has different params, specific form less documented. |

## ★ PUBLISHABLE OUTCOMES FROM THIS BATCH ★

1. **Ramanujan Journal corrigendum on AB Entry 4.2.3** (CONFIRMED, real
   novel contribution). Short note 3-5 pages. Courtesy heads-up to
   Bruce Berndt before submission.
2. **Tool paper: 4 verified computational primitives** at
   `rkc/{attention,pde,ph,special}` + benchmarks + prior-art
   citations (RetNet/SSD, Crowdy-Marshall, Schrödinger 1914 / Trovato,
   DLMF). Open-source release + arxiv announcement.
3. **C2 expository note on engine autonomously rediscovering classical
   Lambert/E_2 annihilator structure** — Math.Mag. or Amer.Math.
   Monthly, 2-4 pages.
4. **Methodology paper** (workflow + verification + prior-art audit
   pattern). Independent of math-novelty outcomes. arxiv preprint.

## Today's other update

- **Diary 61 (figure-8 three-body period)** — calibrated-honest result
  in the ζ(5)/XXX/Kepler class. ChatGPT explicitly framed as
  "30-digit near-closed hyperelliptic-period surrogate, NOT a proven
  exact closed form." Useful as computational primitive replacing
  iterative shooting solver. NOT paper-grade.
- 5 calibrated-honest cycles now (ζ(5), XXX, Kepler, M3 P_pq, figure-8)
  out of ~27 ChatGPT-Pro cycles — methodology's true-positive filter
  continues to work.

**Do not spawn new subagents until paper drafts have absorbed these
verdicts.**

---

## Now actionable (Hunts unblocked by the source pack)

### H2. Hunt 5b: 3rd chapter for full toolkit-split establishment

**Status:** 2 chapters complete; need 1 more with a 3rd distinct
operator-dominance pattern to lift the toolkit-split hypothesis from
"strong inter-chapter variance evidence" to "established".
- Ch. 32 (Eisenstein-CF, diary 22): SUPPORTED. q_shift 100% + modular_S
  91.7% — *q-Pochhammer-with-modular-quotient* dominant pair.
- Ch. 36 (modular equations, diary 24): PARTIALLY SUPPORTED. modular_S
  100% saturated, q_shift 4.8%, class_field 4.8% — *modular_S
  single-saturated* pattern.
- **NEEDED**: a chapter where neither q_shift nor modular_S dominates
  AND a 3rd operator does. The natural candidate: **class invariants Gₙ
  chapter** (Berndt NB Part V Ch. 34 + Lost Notebook Part I supplement,
  both in downloaded-pdfs/). Predicted-dominant by HUNT5b_PREDICTIONS:
  `class_field_galois_average` ≥60%, `modular_S_transform` ≥30%. If the
  prediction holds, that's the 3rd distinct dominance pattern — full
  toolkit-split establishment.

Effort: half-day to full-day for a focused agent. Same template as
Hunt 5b Ch. 32 + Ch. 36 agents.

### H1. Hunt 1 — Lost Notebook pp. 341-343 (1729 / two-cubes / K3) — CLOSED

Result in [diary/21](diary/21_hunt1_lost_notebook_341_343.md);
falsification in [DID_NOT_PAN_OUT §R16](insights/DID_NOT_PAN_OUT.md). K3
fraction 33% (10/30), well below the 60-80% prediction. K3 material is fully
concentrated on p. 341 itself; pp. 342-343 are different topics. Three
sub-leads spawned:

#### H1a. Resolve pagination ambiguity (need Andrews-Berndt Part IV)

Ono's 2016 colloquium speculation about "pp. 342-343 near-counterexamples"
may refer to a different edition than the Narosa/Sirinudi facsimile inventoried.
Andrews-Berndt *Lost Notebook Part IV* chapter on "Approximations and
asymptotic methods, including 1729" would resolve. Copyrighted Springer book;
not in the local pack. Lower priority than H1b.

#### H1b. Cross-check p. 342 Weber class invariants against Berndt-Chan-Kang-Zhang

**Hunt 4 partial unblock.** p. 342 has a 15-row Weber `f₁(√-n)` table for
n ∈ {20,27,26,29,35,36,38,39,41,44,50,51,52,63,87}. Some of these
discriminants (-63 class number ≥ 4, -87 class number ≥ 6) likely overlap
the ~18 of Ramanujan's 116 tabulated invariants that were unresolved as of
2000. Cross-check: which (if any) appear here? Each unresolved one is
simultaneously a Hunt 1 deliverable AND a Hunt 4 deliverable.

Concrete deliverable: a CSV adding a `proof_status_2000` column to the
p. 342 rows of `analysis/results/hunt1_k3_inventory.csv` based on the
modern reproof table. ~half-day of work given the table.

#### H1c. Verify Ramanujan's `O(...)` bound on p. 343 against modern Thue-Siegel-Roth ★ SPECULATIVE BONUS

p. 343 has explicit conjugate-product bounds for `|a^m b^n ⁵√2 - p_{m,n}|`.
Numerically verify (mpmath, ~100 digits) for specific (m,n) whether the
bound is tight, approximately tight, or loose. Compare against the modern
effective Thue-Siegel-Roth or Schmidt-subspace bound for ⁵√2. **If tight,
this is Ramanujan anticipating effective Diophantine bounds by 13-16 years
(Mahler 1933, Schneider 1936)** — a dedicated diary entry / standalone
short note.

~0.5-1 day of work.

**Probability genuinely new (not in some obscure 1960s-90s paper):** **~40%**
(per parallel-Claude). Mahler covered the general case; the question is
whether Ramanujan's specific bounds for ⁵√2 / ⁷√2 are sharper or
methodologically different. If yes, candidate target: Math. of Computation
note or Acta Arithmetica.

### H2. Hunt 5b — Notebooks operator tagging — UNBLOCKED

**Source.** `chatgpt-pro-mining/.../primary_originals/pdfs/notebooks/` (4
facsimiles: NB1 380p, NB2 355p, NB3 35p, Lost Notebook 379p) +
`chatgpt-pro-mining/.../primary_originals/page_images/` (1,149 extracted page
images).

**Predict.** The 4 operators that did NOT fire in the QRs (`modular_S_transform`,
`eisenstein_normal_ordering`, `q_shift`, `class_field_galois_average`) *will*
fire heavily in specific Notebooks chapters per Berndt's TOC: NB II ch. 16
(q-series), ch. 17 (modular equations), ch. 21 (Eisenstein + class invariants).
Confirming this establishes the **QR-vs-Notebooks toolkit contrast** as the
real cog-sci finding (diary 20, BIG_IDEAS_REVIEW §2 + §4).

**Scope.** Don't try to tag all 1,149 pages. Pick 3-5 specific chapters
chosen to test the 4 unfired operators:
- NB II ch. 16 → q_shift
- NB II ch. 17 → modular_S_transform
- NB II ch. 21 → eisenstein_normal_ordering + class_field_galois_average
- LN ch. on partial-theta (pp. 28-39) → mock-theta context (cross-check rkc)

**Blocker.** Page images are handwritten facsimiles, not typeset text like
the QRs were. Will need OCR (Chandra) or careful image-reading. See H4.

### H3. f5/f7 Watson-Hickerson instrumentation for `rkc/completions.py`

**Source.** `chatgpt-pro-mining/.../primary_originals/pdfs/published/` may
contain Hickerson 1988 / Berndt-Chan; check first. If not, fetch directly
(open-access from arXiv / hrj.episciences.org).

**Concrete deliverable.** `rkc/completions.py` returns numerical values for
f5 and f7 mock-theta inputs at ≥30 digits with a certificate, just like f3
does today. Adds unit tests. Removes `CompletionNotImplemented` for f5/f7.
Diary entry. Per BIG_IDEAS_REVIEW §1, this closes the recognizer end-to-end
on all 3 registered mock-theta families.

### H4. Chandra 2 OCR via Datalab API — OPERATIONAL (smoke test passed)

**Status (2026-05-24, evening).** Local `chandra --method hf` is
**DEAD** (crashed user's Mac repeatedly; ~10 GB safetensors + working
memory exceeds what's stable). Pivoted to Datalab hosted Chandra 2 API:

- API key in `.env` (gitignored; `.env.example` committed)
- SDK `datalab-python-sdk` v0.5.0 in `.venv`
- Wrapper [`corpora/scripts/chandra_api_runner.py`](corpora/scripts/chandra_api_runner.py)
  with idempotent batching, JSONL log, dry-run + force flags
- Smoke test on `page-340.jpg` (LN reprint p. 341, canonical 1729 page):
  **OK in 8.76 s**, 16 blocks recognized, LaTeX math preserved in
  markdown + html + json outputs
- Best settings: `mode=accurate`, `output_format=markdown,html,json`,
  `disable_image_captions=True`
- Limits per Datalab: 200 MB file / 7000 pp / 400 req/min / 5000
  concurrent pages — full 1,149-page Notebook corpus is ~3 h
  sequential, ~20 min with async concurrency

See [`corpora/transcriptions/chandra_benchmark/README.md`](corpora/transcriptions/chandra_benchmark/README.md)
for full operational notes.

**Next-step ladder:**
1. Spot-check page-340.md vs Ono 2014 + Berndt-Andrews LN Part IV —
   character-for-character confirmation of OCR'd cube-near generators;
   catalogue which digit / subscript classes Chandra mis-reads on
   Ramanujan's hand.
2. Pick a 30-50 page Hunt-relevant subset (Hunt 4 class invariants,
   Hunt 1 reverification) — batch via wrapper.
3. Add `--async` flag using `AsyncDatalabClient` for bulk runs.
4. Feed accepted OCR'd identities into `rkc/search/seeds.py` (Project C).

---

## Status snapshot (2026-05-24, post Hunt 5b Ch. 32/36/34 + Project C v0.7 + v0.8a)

**Project C v0.8a SHIPPED** (diary 30) — `ClaudeProposer` (LLM-powered
step 2) joins `RandomProposer` as a second proposer option. Encodes the
Hunt 5b toolkit-split heuristics as system-prompt-resident rules.
Graceful `ClaudeStubProposer` fallback when `ANTHROPIC_API_KEY` is
missing. CLI flag `rkc {sweep,search} --proposer {random|claude}`
(default stays `random`). Cost discipline: SHA-256-cached responses,
default `max_api_calls=10` cap. 6 new `test_v08a_*` tests.

**Project C v0.7 SHIPPED** (diary 26) — `mellin_inversion` now handles
three Poisson identity classes via strict double-sided sums:
1. v0.4: pure Gaussian `exp(-β n²)` (~53× at β=1/100)
2. v0.7-A: half-shifted Gaussian `exp(-β(n+1/2)²)` (theta₂/theta₄;
   ~53× at β=1/100)
3. v0.7-B: weighted Gaussian `n²·exp(-β n²)` (second-moment derivative
   of v0.4; ~53× at β=1/100)
All three accepted end-to-end through the engine; correctly fail the
cost gate at β=5. The basis-coverage trajectory toward
`recover ≥80% of rkc's 11 known kernel identities within budget=1000`
inches forward. v0.8 covers the additive-correction operator class
(parallel subagent work; merges cleanly with v0.8a).

**Hunt 5b state**: TOOLKIT-SPLIT HYPOTHESIS ESTABLISHED (diary 25,
Ch. 34 was the 3rd distinct dominance pattern). Three chapters covered:
Ch. 32 q_shift+modular_S pair, Ch. 36 modular_S monoculture, Ch. 34
class_field+modular_S pair. `modular_S` is the always-on parent across
all three; secondary operator varies by problem domain.

**Tests**: 87/87 passing (67 v0.6 baseline + 6 v0.7 + 6 v0.8a + 8 v0.8b
tests). Recognizer benchmark `analysis/14b` still 55/55 = 100%.

### T0a. Project C v0.8a follow-ups (diary 30 deferred items)

1. **Live ClaudeProposer vs RandomProposer benchmark** — DEFERRED in
   diary 30; blocked on a usable `ANTHROPIC_API_KEY` in the run shell.
   Script ready at
   [`analysis/24_v08a_claude_vs_random_proposer.py`](analysis/24_v08a_claude_vs_random_proposer.py).
   Rerun once API key is configured; ~50 API calls bounded; should be
   ≪ $0.10. Output goes to
   [`analysis/results/v08a_claude_vs_random_proposer.csv`](analysis/results/v08a_claude_vs_random_proposer.csv).
2. **In-conversation Claude SDK hook** (architectural improvement per
   diary 29) — `proposers.InProcessClaudeProposer` that detects the
   surrounding agent context and routes through it instead of opening
   a new client. 1-2 days; v0.9 candidate.
3. **`OperatorApplication.params` exploration in the LLM prompt** —
   currently the proposer only suggests `op_id`; future v0.9 should
   let Claude suggest `(op_id, params)`. Requires per-op
   parameter-space documentation in the system prompt.
4. **Per-state structural-hint pre-pass** — run rkc's recognizer first,
   pass `result.family` as an explicit hint in the user prompt; let
   `ClaudeProposer` skip the LLM call for deterministically-pinned
   cases (e.g. `family=theta-like` → always `mellin_inversion`).
5. **Cross-validation of the system-prompt heuristics** — measure
   whether each of the 6 toolkit-split rules actually improves
   per-state op-id selection on a labelled test set. Drop unused
   rules for token discipline.

### T0b. Project C v0.9: InSessionClaudeProposer → SHIPPED (diary 34)

`InSessionClaudeProposer` formalizes the in-conversation
host-LLM-as-proposer pattern via file-based IPC (T0a item 2).
SHIPPED at commit TBD (pending push). The proposer:
- Writes a JSON inbox at `<session_dir>/proposer_inbox.json` per ask;
  blocks on `proposer_outbox.json` with `timeout_s` (default 60s).
- Reuses `ClaudeProposer`'s system+user prompt builders (byte-exact
  prompt equivalence — heuristics can't drift between API and
  in-session paths).
- Falls back to `RandomProposer` on timeout / malformed / unknown
  op_id, with `n_round_trips / n_cache_hits / n_timeouts /
  n_malformed` stats accessible via `proposer.stats()`.
- CLI: `--proposer in-session [--in-session-dir DIR]
  [--in-session-timeout SECONDS]` on both `rkc sweep` and `rkc
  search`. Tests: 7 new `test_v09b_*` cases; 99/99 total.

Deferred to v0.9.1:
1. Thread per-state reject history through `set_history()` so the
   host LLM sees prior failed attempts (parity with `ClaudeProposer`).
2. Live "Claude Code session as host" demo — record a run where this
   Claude session writes outbox files in response to inbox files and
   produces ≥1 LLM-selected acceptance (not random fallback).

## Tool-side priority stack (after ChatGPT-Pro reranking — see [BIG_IDEAS_REVIEW](insights/BIG_IDEAS_REVIEW.md))

The headline target: **rkc v0.1** as a usable degeneracy-aware special-
function routing compiler. The Hunts feed into this as transform-mining
work. See [rkc/MILESTONES.md](rkc/MILESTONES.md) for the v0.1 spec.

### T0. Project C v0.8b: additive-correction operator → SHIPPED (diary 31)

**Status:** SHIPPED. Both Bose-Einstein log and Lambert seeds now accept
end-to-end with 2800× / 13× cost ratios respectively.

Specifically v0.8b shipped:
1. `OperatorApplication` gained `additive_correction: Optional[sp.Expr]`
   and `summand_range: Optional[tuple]` fields, both None-default for
   backward compat.
2. `MpmathVerifier` folds the correction into the comparison
   (`Σ before ≡ Σ after + correction`), respects per-call summand_range
   override, and upgrades to high-precision `evalf` for correction values.
3. `modular_transform_with_correction` operator handles two cases:
   - **Bose-Einstein log** `Σ log(1-e^{-βn})` via Dedekind eta.
   - **Lambert** `Σ n·q^n/(1-q^n)` via E_2 quasi-modular (Hecke trick).
4. Numerical verification at dps=80: rel-err ≤ 1e-30 across 4 dex of β.
5. Seeds `bose_einstein_beta_1em2` (log form, replaces divergent original)
   and `lambert_divisor_q_p1` enabled and recovering identity end-to-end.

87/87 tests passing (78 baseline + 8 new `test_v08b_*` + 1 slow).
Recognizer benchmark 55/55 = 100% (no regression). R17 in
DID_NOT_PAN_OUT closed → RESOLVED.

**Operator basis is now 8** (the 7 QR-derived ops + the new
modular_transform_with_correction). Three of four high-leverage rkc
routing families now have working apply_fn: Gaussian (v0.4 + v0.7),
Bose-Einstein, Lambert. Mock-theta-via-completion is the remaining one
(needs Watson-Hickerson plumbing in apply_fn; rkc's completions module
already has the route for f3 to ≥30 digits — would need to wire it).

### T0.5. Project C v0.8c: Stieltjes occupation-number → SHIPPED (diary 32)

**Status:** SHIPPED. Stieltjes/Lambert occupation-number identity for
`Σ 1/(e^{βn}-1)` operational as CASE C of
`modular_transform_with_correction` per ChatGPT Pro proposer answer
(2026-05-24, Rank 2).

  * Identity: `Σ 1/(e^{βn}-1) = (log(1/β)+γ)/β + 1/4 − (2/β)·Σ d(m)·[e^{-z_m}Ei(z_m) − e^{z_m}E_1(z_m)]`
    with z_m = 4π²m/β.
  * Numerical verification: rel-err ≤ 1e-9 across 4 dex of β at dps=50
    (small-β regime); large-β cells truncation-limited due to dual's
    polynomial `1/m²` convergence. See diary 32 §"Surprises" for the
    convergence-regime caveat.
  * Tests: 99 → 102 passing (3 new `test_v08c_*`). Backward-compat
    maintained: all v0.4/v0.7/v0.8a/v0.8b/v0.9a/v0.9b paths still
    green.
  * End-to-end engine acceptance: 2800× cost ratio at β=1/100 on the
    new seed `bose_occupation_beta_1em2`.

The `modular_transform_with_correction` operator now spans 3 distinct
one-sided modular identity classes (Dedekind eta, E_2 quasi-modular,
Stieltjes/Ei). Future v0.8d candidate: quadratic Lambert
`Σ 1/(e^{β·n²}-1)` (heat-kernel / Riemann-zeta dual) — would extend the
pattern to a 4th class.

**Subsequent operator order** (from the v0.5+ ladder, unchanged):

- **v0.5 SHIPPED**: master_theorem on Integral patterns (Gamma, Beta,
  1/(1+x)) — see diary 14b commit `3cbe013`.
- **v0.6 SHIPPED**: sweep harness across 15 seeds — commit `a7d3bcc`.
- **v0.9: fourier_self_reciprocity** — recognise cos/sin integral pairs
  and apply (π/2) F·F = Id. Requires Integral AST recognition (sympy's
  Integral class); slightly heavier lift. ~1 day.
- **v0.10: frullani_limit** — recognise `(f(ax) - f(bx))/x` integrals
  and return `(f(0) - f(∞)) log(b/a)`. ~half-day with f(0)/f(∞) helpers.
- **v0.11: mellin_pair_reciprocity** — generalised Mellin-pair
  self-inversion per QR III §15. ~1 day. Bridges to W7 (Berndt-Dixit
  αβ=1 transformation is an instance of this).
- **v0.12: fractional_functional_iteration** — Schröder linearisation
  for one-parameter iteration semigroups. ~2-3 days; ties to W8 paper +
  the aether-audio X6 cross-repo Schröder probe.
- **v0.9-hardy SHIPPED (out of order, ahead of v0.10/v0.11/v0.12)**:
  hardy_orders_of_infinity as engine divergence diagnostic — see
  diary 33. Resolves the v0.3 stub. Non-transforming annotator using
  new 2-tuple `(payload_unchanged, metadata_dict)` return convention.
  4-class taxonomy: CONVERGENT / DIVERGENT_LITERAL /
  NEEDS_REGULARIZATION / UNKNOWN populates `SearchState.convergence_class`.
  92/92 tests green.
- **v0.13 (originally planned slot for hardy_orders) — REASSIGNED**.
  hardy_orders shipped ahead-of-order at v0.9. v0.13 slot now open for
  the next deepest behaviour shift (likely an Abel/zeta regularization
  operator that fires when convergence_class = NEEDS_REGULARIZATION).

After v0.8 (4 routing families covered), run the controlled-validation
case: random composition of operators on a curated seed-identity set;
metric = fraction of rkc's 11 known kernel identities recovered within
budget=1000 compositions of length ≤3. Target ≥80%.

### T1. rkc v0.1 CLI + Python API milestone

CLI: `rkc recognize`, `rkc compare`, `rkc certify`, `rkc benchmark`.
Python: `from rkc import route; route(expr, var, params, digits)`.
Internal: minimal public API surface; pin the cost/certificate contract;
benchmark table per family (recognize / route / certify / degeneracy
guard / benchmark).

See [rkc/MILESTONES.md](rkc/MILESTONES.md) for the full spec. Effort:
~2-4 weeks for v0.1 (CLI scaffold ~1 day; per-family hardening ~3-5 days;
docs + examples ~3-5 days; benchmark suite ~3-5 days).

### T2. Eisenstein-CF registry expansion (Hunt 3 repurposed) — SCOPED

Scoping pass complete in
[insights/T2_EISENSTEIN_CF_SCOPING.md](insights/T2_EISENSTEIN_CF_SCOPING.md).
HUNT_MAP §3 framing corrected: "Eisenstein-style CFs" actually splits into
~30 weight-0 q-CFs (Rogers-Ramanujan + Andrews-Gordon-Selberg family,
no quasi-modular anomaly) + 1 genuinely-quasi-modular cubic-base CF
in NB V §33.

**Four registry families to implement (recommended granularity: separate
entries per family, matching the existing `mock_theta_f3/f5/f7` pattern):**

- **Family A** (~3 entries): `rogers_ramanujan_cf` + sign variations.
  Closed-form via Rogers-Ramanujan identities; well-studied.
- **Family B** (~5 entries): `rogers_ramanujan_special_values` at
  q=exp(-πk) — radical closed forms; bridges to Hunt 4 class invariants.
- **Family C** (~13 entries): `eisenstein_cf_level_N` for N ∈ {2,3,4,8} —
  Andrews-Gordon-Selberg q-CFs; bulk of NB V Ch. 32 §2.
- **Family D** (~1 entry): `cubic_eisenstein_cf` (NB V §33) — the only
  truly quasi-modular entry; weight-2 anomaly handling needed.

**Implementation cut-points:**
- **Day 12** (Families A + C): clean partial-ship cut. Registry grows
  11 → 14 entries. No quasi-modular machinery needed.
- **Day 17-20** (Families B + D added): full v0.2 ship. Registry grows
  11 → 17 entries. Family D requires the quasi-modular route flag
  threaded through the routing layer.

**The single concrete decision before implementation:** confirmed in scope
doc — go with 4 separate registry entries per family, NOT one
parameterised entry. Cleaner matchers; easier to extend to Bhatnagar's
level 5/7 q-CFs later.

**Cross-validation gate per CLAUDE.md gotcha #5:** the T2 scope doc lists
the 2-3 specific (kernel, param) cells per family to run the ≥40-digit
agreement gate on before benchmarking.

### T3. Operator-composition search engine (W5 sharpened)

Generate 100-1000 candidate identities by composing the 7-operator basis
on simple inputs; numerically verify via mpmath/PSLQ; route through rkc;
classify each as classical-known / numerically-false / numerically-true-but-
slower / faster-than-baseline. Identity-discovery engine.

Effort: ~1-2 weeks for the first cut (composition framework ~3-5 days;
verification harness ~2-3 days; classifier + benchmark ~3-5 days). Even
1-2 genuinely-new identities would validate the approach.

### T4. H10 sharpened: Berndt-Dixit αβ=1 as a new rkc transform family

Read [downloaded-pdfs/0904.1053v2.pdf](downloaded-pdfs/0904.1053v2.pdf)
carefully; extract Theorem 1.1's αβ=1 Mellin-pair structure; add it as
`mellin_pair_alpha_beta_one` (or similar) to rkc/registry.py with a
degeneracy detector for the natural failure modes. Possibly opens the
door to fractional-operator / anomalous-diffusion / spectral-sum routing.

Effort: ~1 day for the careful read + registry sketch; ~3-5 days for the
full registry entry + tests + benchmark.

## Tractable without primary scans

### W1. Architecture paper draft: kernel-fingerprint compiler

**From BIG_IDEAS_REVIEW §1.** Recognizer is shipped + benchmarked. Draft from
existing artefacts (rkc/, A1-A7, DID_NOT_PAN_OUT). Target: Computing in
Science & Engineering, ACM TOMS, or workshops (ML4PS at NeurIPS, JuliaCon).
1-2 weeks of focused writing.

### W2. Closure paper draft: cohomological irreducibility of the mock-theta shadow

**From BIG_IDEAS_REVIEW §3.** Pass D is closed at high confidence; 20
candidates across 5 structurally-different families all fail; two decisive
structural arguments. Target: Comm. Math. Phys. or Physical Review Research.
The honest "we tested hard, none works, here's why structurally" is itself
the result.

### W3. Watson-identity calibration regime extension

The W-partner formula in `analysis/17_*.py` is calibrated only for α ≤ 0.7;
(0.7, π) flagged `regime="near-cusp-warning"` with uncomputed q₁⁴ correction.
Computing the next-order correction extends the calibrated regime. Small,
self-contained, useful.

### W4. `recognize_composite` `numerical_completion` propagation

Cheap fix flagged in diary 16; deferred. Wire the opt-in flag through to
per-component calls so composites return values not flags. <1 day of work.

### W5. Small operator-composition search prototype — NOW LABELED Y1 / "Project C v0"

**Reframed (user-supplied "Project C" naming):** this is now the
**v0 pure-symbolic baseline of Project C — the RKC-guided symbolic search
system**. Full design in
[insights/PROJECT_C_DESIGN.md](insights/PROJECT_C_DESIGN.md).

W5 = T3 v0 = X3 spine-extraction = Project C v0. The label "Project C" is
the external name; W5/T3/X3 are the internal priority tags. All refer to
the same system at different stages of maturity:

- **Project C v0 (W5)**: pure-symbolic baseline — random operator-composition
  + rkc verification + cost-model gate + accepted-identities JSONL registry
  + reject-with-reason taxonomy. ~1-2 weeks.
- **Project C v1 (T3)**: adds the neural proposer. Default architectural
  choice per ChatGPT: nonlinear ICA / JEPA proposing in latent operator
  space (Hyvärinen et al. arXiv 2303.16535 for the identifiability
  framework). Categorical classifier suffices at current basis size (~10);
  ICA becomes valuable when the basis scales to ~100s.
- **Project C v2 (X3)**: extract the `rkc.search` interface (proposer,
  verifier, gate, registry) as a shared spine so arc-agi-ebm-agent can
  plug in ARC's DSL as a second instance.

Honest caveat from the design doc: the novelty of Project C is in steps
3+4+5+6 (RKC verifier + router + cost model + registry-with-reject-log),
NOT in the neural proposer step 2. Many people have built neural proposers
for math reasoning (Drori; AlphaProof; AlphaGeometry; Lean-Copilot); few
have built a *certified, degeneracy-aware, cost-modelled* verifier that
prunes the proposer's output. That's where rkc earns its keep.

Even 1-2 genuinely-new identities from the v0 baseline would validate the
approach. See [insights/PROJECT_C_DESIGN.md](insights/PROJECT_C_DESIGN.md)
for the controlled-validation case (random composition recovering ≥80% of
the rkc registry's 11 known kernel identities within budget=1000
compositions of length ≤3) and the v0 scope breakdown.

### W6. Add umbral-operator kernels to the rkc/ recognizer

**From BIG_IDEAS_REVIEW §2b (added after parallel-Claude review).** QR III §12
uses formal-power-series operator algebra (shift E, difference Δ, RL fractional
D^α) — structurally the natural lens for the recognizer. Add umbral-operator
primitives to `rkc/registry.py` as new kernels with degeneracy detectors.
After this, the recognizer can route QR III-style identities, not just the
QR I + QR II Mellin/Master cluster. Concrete + bounded (~1 week).

### W7-pre. Check QR II §3 cubic-roots-of-unity for Gauss-sum degeneracy awareness — CLOSED (NEGATIVE)

**From parallel-Claude review.** QR II §3 (lines 2086-2280 of the HRJ text)
uses the cubic-roots-of-unity multisection
`1 - x³/3! + x⁶/6! - ... = (e^{-x} + e^{-xω} + e^{-xω²}) / 3`. This is the
same operator family as the **Gauss-sum silent-zero hazard** the recognizer
guards against ([CANDIDATE_INSIGHTS §A4](insights/CANDIDATE_INSIGHTS.md);
implemented at `rkc/registry.py` for q ≡ 2 mod 4). Quick test: does QR II §3
mention or implicitly guard against the q ≡ 2 mod 4 case (the cube-root case
analogue would be q ≡ 0 mod 3 or some sub-case where the sum degenerates)?

If yes → bibliographic evidence that the silent-zero hazard was in
Ramanujan's working knowledge, not a modern engineering catch. Strengthens
the §A4 finding. A small note to add to diary 20 or as a new short diary
entry.

If no → still informative: Ramanujan happened not to hit the degeneracy
because he restricted to specific cubic roots, but didn't generalise the
caveat. Still worth a one-line note.

**Effort:** ~30 minutes (just careful re-read of QR II §3, lines 2086-2280,
plus 1-2 paragraphs of write-up).

**Result (diary 23):** NEGATIVE. Ramanujan applies the cube-roots-of-
unity multisection to `1 - x³/3! + x⁶/6! - ···` cleanly but does NOT
comment on the silent-zero case (when target function has no `n ≡ 0
(mod 3)` Taylor coefficients). §A4's silent-zero detector at Gauss sums
q ≡ 2 (mod 4) is a modern engineering catch, not a re-statement of a
Ramanujan caveat.

### W8. "Pre-Julia iteration theory in Ramanujan's third Quarterly Report" — DRAFT v0.1 IN HAND ★

**From parallel-Claude review.** QR III §4-§10 contains explicit fractional-
iteration computations (Chebyshev semigroup F(x) = x²-2 with `F^n(x)` via
cosh-formula; F(x) = x²+2x, x²-2x, x²+4x; iteration of `x → (1-x)/(1-x²)` at
fractional r) and the infinitesimal generator `ψ_1(x) = C/F(x)` of the
iteration flow. Schröder (1871) and Koenig (1884) predate Ramanujan; the
ψ_1 = C/F identification, however, is the Lie-theoretic content — the bridge
between iteration theory and one-parameter semigroups that becomes the
renormalisation-group setup decades later. **Notably this prefigures Julia
(1918) and Fatou (1917-19) by 3-4 years.**

**Concrete first step:** literature scan. Has modern work on Ecalle resurgence,
Belitskii normal forms, or holomorphic dynamics integrated Ramanujan's QR III
fractional-iteration work? If no → a short standalone paper "Pre-Julia
iteration theory in Ramanujan's third Quarterly Report" is the natural
deliverable, with the explicit linearizations + the ψ_1 = C/F identification
as the historical artefact. Target: Historia Mathematica or a focused
math-history note in a number-theory venue.

**Effort:** literature scan ~0.5-1 day; paper ~2-3 weeks if the lit scan
confirms novelty.

**Probability genuinely under-noted:** **~75%** (upgraded after W8 agent
lit scan, see [insights/W8_PRE_JULIA_LIT_SCAN.md](insights/W8_PRE_JULIA_LIT_SCAN.md)).
The Ramanujan canon is curated by number theorists; the dynamics community
(Milnor, Douady-Hubbard, Ecalle, Belitskii) doesn't typically read Ramanujan
source material directly. **Confirmed concretely:**
- Milnor's *Dynamics in One Complex Variable*: zero "Ramanujan" anywhere.
  Chronological table of 14 pre-1918 founders does NOT include Ramanujan.
- Berndt's NB Part I: zero mentions of Schröder/Koenigs/Julia/Fatou/
  Böttcher/Écalle across 17,228 lines including 150+ pages of Ch. 4 on
  iteration of exponentials. Berndt frames Ramanujan's iteration work
  in terms of Bell numbers + Comtet + Hardy's *Orders of Infinity*,
  never drawing the Schröder-Koenig connection across 1981/1984/1985/2022.
- Rosa 2026 Springer monograph (most recent historiography) names ~15
  pre-1918 contributors in preview — Ramanujan NOT among them.
- Robbins 2015 cites Schröder AND Ramanujan side-by-side BUT the
  Ramanujan citation is to Amdeberhan-Moll Master Theorem, NOT QR III
  iteration content. Cited-for-the-wrong-reason near-match (agent
  flagged with appropriate discipline).

**Paper outline ready** at
[insights/W8_PRE_JULIA_PAPER_OUTLINE.md](insights/W8_PRE_JULIA_PAPER_OUTLINE.md);
**draft v0.1 in hand** at [insights/W8_PAPER_DRAFT.md](insights/W8_PAPER_DRAFT.md)
(7,140 words / ~14-16 typeset pages). Target: *Historia Mathematica*
(primary) or *The Ramanujan Journal* (secondary).

The draft structures three claims with explicit qualifications:
1. Conjugation identity = parallel rediscovery of Schröder 1871 (with
   non-linear worked examples beyond Schröder)
2. Cosh-form Chebyshev linearisation precedes Lattès 1918 (framework-vs-
   formula distinction honoured)
3. **The ψ₁ = C/F infinitesimal-generator identification in QR III §10
   is genuinely original pre-1914** — load-bearing priority claim;
   not in Schröder / Koenigs / Leau / Böttcher

**Honest weakness in draft v0.1** (per agent's self-report): §6.4's
reconciliation between Ramanujan's ψ₁ = C/F and the modern formula
ψ₁ = log λ · χ/χ′ is partial. Referee target.

Future revision items (per agent):
- Pull Berndt 1984 BLMS directly (still missing per CLAUDE.md);
  strengthens §2.2 negative
- Fully reconcile §6.4
- Expand §6(d) (the rational map x → (1-x)/(1-x²)) — most modern-
  rational-dynamics-adjacent example

### W7. B1.5 fractional-Fokker-Planck bridge experiment

**From BIG_IDEAS_REVIEW §3b (NEW).** Parallel to the closed B1 modular bridge:
pick a 1D fractional Fokker-Planck system with a known closed-form propagator
(plenty in the Klafter / Metzler anomalous-diffusion literature), compute its
partition function, and test whether the "Markovian-surrogate residual" is
recognisable from QR III's Schröder / RL / umbral machinery.

If yes: write up as the second Ramanujan-style FEP bridge, parallel to the
closed (and falsified-for-candidate-families) modular bridge.

If no: structural reason for closure becomes a sharper result — both modular
and fractional-calculus generative-model classes resist Ramanujan-style
completion, suggesting whatever "completion" means is even more specific than
B1 closure already implied.

Status: SCOPED but UNTESTED. Single-experiment scope ~2-3 weeks.

---

## Newly unblocked by downloaded-pdfs/

The user obtained Berndt-family commentary volumes directly from the
authors for personal use; they're now committed to this private repo at
[downloaded-pdfs/](downloaded-pdfs/) (see
[downloaded-pdfs/README.md](downloaded-pdfs/README.md) for the manifest).

### H9. Hunt 5 calibration against Berndt *Notebooks Part 1* — NEWLY UNBLOCKED

`ramanujankitap1.pdf` is Berndt *Ramanujan's Notebooks Part 1* (Springer 1985)
Ch. 1-9, which includes Ch. 3-4 — Berndt's commentary on the Master Theorem
and analysis material that Ramanujan re-presented (and extended) in QR I + QR II.

**Test:** read Berndt's per-entry "rederivation" annotations on NB Ch. 3-4
and cross-tag the QR I + QR II identities against this. If most of QR I's
ten worked examples are "rederivations of NB Ch. 3 material", that adjusts
the headline from "QR I is the Master Theorem manifesto" to "QR I is the
Master Theorem manifesto, *presented to the Board as if novel even though
most examples were already in NB Ch. 3*". That's a substantive sharpening
of the Hunt 5 narrative.

Effort: ~half-day for the cross-tagging pass. Output: a new column
`berndt_nb1_status` in `analysis/results/qr_operator_tags.csv` per QR I/II
section, plus a short addendum to diary 20.

### H10. W7 fractional-bridge starter — Berndt-Dixit 2009 αβ=1 transformation

`0904.1053v2.pdf` (Berndt & Dixit arXiv:0904.1053v2, 2009) contains an
explicit Ramanujan transformation formula with **αβ=1 duality** structure —
the same operator family as QR III §15 Mellin-pair reciprocity. It treats
LN pp. 219-227 ("Copied from the Loose Papers", Watson's hand). Theorem 1.1
gives a series-to-integral identity involving Γ'/Γ + Riemann Ξ, with αβ=1
as the natural parameter pairing.

**Why it matters for W7:** the W7 fractional-Fokker-Planck bridge needs a
*concrete* Ramanujan identity that has the right operator-pair structure to
test the bridge against. Berndt-Dixit's Theorem 1.1 is that identity — it
already lives in the right operator-class.

Effort: ~1 day to read carefully + sketch the bridge wiring. Then W7
becomes a concrete numerical experiment rather than a scoping exercise.

### H5. Hunt 1a — Resolve Ono pagination ambiguity (Andrews-Berndt Part IV)

Sub-lead from H1 closure. Read AB *Lost Notebook Part IV* (2013) chapter on
"Approximations and asymptotic methods, including 1729". Locate Berndt's
own commentary on Ramanujan's pp. 341-343 cube material; identify where
Ono's "near-counterexamples on pp. 342-343" speculation maps to. Source:
[downloaded-pdfs/Ramanujan_39_s_Lost_Notebook_Part_IV_2013.pdf](downloaded-pdfs/Ramanujan_39_s_Lost_Notebook_Part_IV_2013.pdf).
Effort: ~half-day if the chapter is well-organised. Should close the
H1a ambiguity in DID_NOT_PAN_OUT §R16.

### H6. Hunt 2 — Modular equations at level ≥23 — NEWLY UNBLOCKED

Berndt *Notebooks Part V* (Ch. X) now available at
[downloaded-pdfs/ramanujan-notebooks-v.pdf](downloaded-pdfs/ramanujan-notebooks-v.pdf).
Ready to run the prediction in [HUNT_MAP §2](insights/HUNT_MAP.md): level-23
entries decompose into two Atkin-Lehner families; level-29 same pattern;
level-47 entries hide higher-genus modular curve. Algorithmic win on
SEA point-counting if confirmed.

### H7. Hunt 3 — Eisenstein-style continued fractions — NEWLY UNBLOCKED

Berndt *Notebooks Part V* Ch. 32 at
[downloaded-pdfs/ramanujan-notebooks-v.pdf](downloaded-pdfs/ramanujan-notebooks-v.pdf);
focused secondary source at
[downloaded-pdfs/1274-16.pdf](downloaded-pdfs/1274-16.pdf) (Berndt-Yee 2002
RIMS survey). Bhatnagar in chatgpt-pro-mining. Ready to run the
~20-Eisenstein-CFs clustering analysis in HUNT_MAP §3.

### H8. Hunt 4 — Unproven class invariants Gₙ — NEWLY UNBLOCKED

AB *Lost Notebook Part I* supplement (pp. 200-220) at
[downloaded-pdfs/Ramanujan_39_s_Lost_Notebook_Part_I_2005.pdf](downloaded-pdfs/Ramanujan_39_s_Lost_Notebook_Part_I_2005.pdf).
Plus Berndt *Notebooks Part V* Ch. 33-34 commentary. **Overlaps with H1b**:
the Weber class invariants on LN p. 342 are likely a subset of the same
list; cross-checking H1b with H8 in one pass is the efficient play.

## Still partially blocked

### B4. Hunt 6 — Ramanujan-Sato at moonshine levels

Have NB II facsimile + open-access context PDFs; missing Cooper *Theta
Functions* (Springer 2017). Worth emailing Shaun Cooper for a personal-use
PDF — see [VALIDATION_CONTACTS.md](insights/VALIDATION_CONTACTS.md).
Workaround: re-derive level-by-level catalogue from Berndt's open-access
papers on theta functions.

---

## Cross-repo (sibling projects, see [insights/CROSS_REPO_LEVERAGE.md](insights/CROSS_REPO_LEVERAGE.md))

User asked whether rkc/Ramanujan work is useful for: `/Users/jouni/Documents/
aether-audio` (PHS-flavoured differentiable audio), `/Users/jouni/Documents/
aether-hardware-ebm` (mixed-signal EBM with EqProp), and `/Users/jouni/
Documents/arc-agi-ebm-agent` (ARC-AGI program induction + EBM ranking).

Honest read: the Ramanujan-specific kernels are unlikely to fire on any
of those, but the **rkc architecture** (registry + matcher + cost model
+ certificate + degeneracy detector) is a transferable pattern; there
are 3-4 specific narrow connections too. Three cross-repo tasks:

### X1. Scope a `rkc_phs` registry for aether-audio

Borrow the rkc/ architecture; plug in the first 3-5 passive physical-audio
primitives (resonator, all-pass, waveguide, FDN topology, modal expansion).
Per-kernel: matcher on adjacency/parameter structure; per-route cost
(time-domain vs frequency-domain vs modal); certificate (passivity bound);
degeneracy detector (silent passivity violations at parameter edges).

The Gaussian-theta dual representation moves from `rkc` to `rkc_phs`
unchanged — high-Q resonators at low damping are exactly where the
β\* = c·π crossover applies. See
[insights/CROSS_REPO_LEVERAGE.md §aether-audio](insights/CROSS_REPO_LEVERAGE.md).

Effort: ~half-week for scope + skeleton; ~2-3 weeks for first 3 primitives
fully wired.

### X2. Import rkc/certify pattern as H4 evidence-claim template for aether-hardware-ebm

aether-hardware-ebm's H4 evidence accounting is the same fail-closed
discipline as rkc/certify. The CLI shape (recognize / compare / certify)
maps cleanly onto the existing hardware\_\* scripts. Bonus: the B1 closure
result (cohomological irreducibility of g\*) tells aether-hardware-ebm
which EBM classes its analog tiles can NOT replicate — a real architectural
constraint.

Effort: ~half-week to draft the H4-template mapping + a one-pass
back-port from rkc/cli.py:cmd_certify into a hardware\_certify.py prototype.

### X3. Build the operator-composition search engine (T3) as a shared rkc+arc-agi artefact

The W5/T3 operator-composition search engine maps DIRECTLY onto ARC-AGI's
program-induction loop: generate candidates by composing operators from a
small DSL, numerically verify, rank by energy. Build the engine on the
Ramanujan 7-operator basis as the validation case; refactor so the operator
basis is pluggable; plug in ARC's DSL as the second test case.

Reusable artefact: `rkc.search` module or a separate `compositional_search`
package that both repos depend on. The Ramanujan side gives the controlled
validation; the ARC side gives the high-payoff target.

Effort: ~1-2 weeks for the shared engine; per-repo plug-in another week each.

### X4. Document B1 cohomological-irreducibility as architectural constraint in aether-hardware-ebm

The B1 closure (g\* irreducibly an Eichler cocycle in H¹(Γ, V_k), per
diary 19 + Exp 22's (K+1)² S-transform dimension mismatch) is a hard
architectural constraint on what aether-hardware-ebm's analog tiles can
promise: **any EBM with mock-modular partition function structure is
fundamentally beyond crosspoint reach** (no finite-K intertwiner exists).
Add a forbidden-class entry to aether-hardware-ebm's
`docs/analog-acceleration-map.md` so the H4 effort doesn't get spent
trying. ~half-day. See
[insights/CROSS_REPO_LEVERAGE.md "Broader read"](insights/CROSS_REPO_LEVERAGE.md).

### X5. Pre-register per-task-family operator predictions for ARC-AGI

Adopt the [HUNT5b_PREDICTIONS.md](insights/HUNT5b_PREDICTIONS.md) template
for arc-agi-ebm-agent: pre-register per-task-family rule-subset predictions
for ARC tasks BEFORE running the solver. Falsifier discipline: solver-found
rule must match the pre-registered family at ≥70% to call the toolkit-split
hypothesis "supported" for ARC. Directly extends Hunt 5's discipline (predict
before testing, near-match ≠ match) onto ARC-AGI experimental design.

The Hunt 5 finding ("structured-multidimensional working representation:
small basis per problem-domain with hard separation between domains") IS the
architectural pattern ARC needs. Today the ARC solver searches the union of
all rules per task; pre-registering per-family expectations forces the
solver into a routing function rather than blind search.

Effort: ~1-2 days to draft per-family predictions; locks down the
experimental contract.

### X6. Schröder-linearization probe for nonlinear audio resonators (aether-audio)

Per QR III §6's closed-form `F^n(x)` for `F(x) = x²-2` (Chebyshev semigroup
via cosh-formula Schröder linearization): scope a probe applying the same
idea to a nonlinear audio resonator (Duffing oscillator suggested). Compute
the Schröder eigenfunction `σ(x)` numerically; test whether
`F^n(x) = σ⁻¹(s^n σ(x))` matches direct N-step time-domain integration to
≥6 digits at steady-state.

If yes, this is a real audio-DSP win for steady-state evaluation of
nonlinear-resonator topologies (Duffing, Van der Pol, soft/hard clipping
chains) and validates the W8 angle with applied evidence. ~1 week scope;
~2-3 weeks for a tested implementation if the probe succeeds.

### X7. "Did not pan out" log discipline across all three sibling repos

aether-audio has `docs/feedback.md`; aether-hardware-ebm has H4 failure-mode
docs; arc-agi-ebm-agent has `docs/feedback.md`. None has an explicit
"refuted speculations" log alongside positive findings. Adding one (per the
[DID_NOT_PAN_OUT.md](insights/DID_NOT_PAN_OUT.md) template — REFUTED /
CORRECTED / PARTIALLY REFUTED / DOWNGRADED / OUTSTANDING tags, every entry
citing the experiment that closed it) would lift methodological credibility
consistently across the run.

~half-day per repo; mostly a back-port of existing claims that turned
out wrong.

## Standing items (per BIG_IDEAS_REVIEW)

- **Cohomological generative model** (BIG_IDEAS §3). Research-grade math
  question, not a well-scoped experiment. Entry points in diary 19 §"what next".
- **LLM + symbolic-verification operator search** (BIG_IDEAS §7). Long-running
  research project; W5 above is the smallest first step.
- **Library-design / silent-zero technical note** (BIG_IDEAS §5). The
  silent-zero hazard at Gauss sums q ≡ 2 mod 4 → 1-2 page note for
  Mathematics of Computation. Cheap, citable.

## Sourcing follow-ups (only when needed)

[VALIDATION_CONTACTS.md](insights/VALIDATION_CONTACTS.md) has the directory
of expert contacts (Zagier, Ono, Bringmann, Berndt, Andrews, Cooper) with
"why them for this run" notes. Open asks once we have a result firm enough
to take to a real expert:

- **Berndt 1984 BLMS paper** ("Ramanujan's Quarterly Reports", Bull. London
  Math. Soc. 16, 449-489). Contains Berndt's per-section assessment of
  "really new" vs "rederivation of known results" for the QRs — would let
  us calibrate the Hunt 5 findings against Berndt's editorial judgment.
  Ask Berndt next time we're in touch (he's already provided
  [downloaded-pdfs/](downloaded-pdfs/)).
- **Cooper *Ramanujan's Theta Functions*** (Springer 2017) for Hunt 6 —
  what we'd uniquely gain: (1) systematic RS-series catalogue by level N
  up to N=12, indexed for "is there a 1/π series at level N" lookups;
  (2) extension of Ramanujan's "signatures" / "alternative bases" to
  levels 14-15 (Cooper *Trans. AMS* 368, 2016, open-access via author site);
  (3) theta-function-only synthesis (Berndt *NB Part V* mixes theta with
  class invariants + Eisenstein CFs + singular moduli). ~70-80% of the
  content is reachable from Cooper's open arXiv papers on his Massey
  page; the book is convenience over necessity. Ask Cooper directly OR
  reconstruct from ~12 open papers if Hunt 6 becomes a priority.
- **Berndt *Notebooks Parts III & IV*** (1991, 1994) — lower priority than
  Part V which is now in.

---

## Sourcing — gaps remaining

What the ChatGPT-Pro pack does NOT cover (copyrighted books):

| Source | Unlocks | Notes |
|---|---|---|
| Andrews-Berndt *Lost Notebook Part IV* (Springer 2013) | Hunt 1 deeper, Hunt 4 | Have the LN facsimile + Ono context; missing the editorial commentary |
| Berndt *Notebooks Part V* (1998), ch. 32 + ch. 34-37 | Hunt 3, Hunt 4 | Have the NB facsimiles; missing the chapter-organisation map |
| Berndt *Notebooks Parts III-V* (1991-1998), modular equations | Hunt 2 | Have NB II facsimile; missing the level-by-level map |
| Cooper *Ramanujan's Theta Functions* (Springer 2017) | Hunt 6 | Have NB + papers; missing the synthesis |
| Berndt-Rankin *Ramanujan: Letters and Commentary* (AMS 1995) | Letters/QR context | QRs themselves unlocked via the open-access HRJ 2022 reprint |

Trinity / Wren IIIF (Add. MS a/94) — high-resolution scans of original papers
— are also not in the pack. The pack ships a downloader
(`chatgpt-pro-mining/.../phase2_context/wren_ramanujan_downloader.py`) that
can run on this machine.

---

## Constraints in this environment

- Full network access (arXiv, HuggingFace, GitHub, ...).
- macOS / zsh; Python 3.12.7 in `.venv/`.
- PARI/GP can be installed locally if needed.
- The primary-source corpus lives at `chatgpt-pro-mining/` (gitignored,
  ~352 MB). See CLAUDE.md for the inventory.

---

# Historical record (completed)

## Pass A — substantiate the central hypothesis on diverse kernels

- [x] **02 Theta-dual switching curve.**
- [x] **03 RKC v0 with rigorous erfc tail bounds.**
- [x] **04 Lambert ↔ Eisenstein switching** (shipped as Exp 12). Crossover
  β* = 2π; gain up to 1.21×10⁶× at extreme β. Two normalization gotchas
  caught (sign factor, Bernoulli prefactor cancellation). Diary 10.
- [x] **05 HRR exact p(n) vs Euler-product recurrence.** Term-count crossover
  small n; wall-clock crossover n=10⁵ (HRR per-term cost is enormous without
  binary-splitting + FLINT). Diary 07. Caught a silent-zero failure mode
  (`round(float(mpf))` mangles p(1000)); fixed with `int(mpmath.nint(...))`.
- [x] **06 Ramanujan 1/π vs AGM vs Chudnovsky vs Machin-like.** Diary 06.
- [x] **07 Divisor sum σ_k(n).** Batch crossover N* = 41. At N=10⁵
  method C uses 5.5% of A's ops. Diary 08.
- [x] **08 Class invariants Gₙ direct vs radical.** 8 invariants PSLQ-verified
  to ≥100 digits. Radical/direct cost ratio grows 1× → 369× as precision
  climbs 30 → 1000 digits. Diary 09.

## Pass B — automated recognition layer

- [x] **09 Kernel-fingerprint matcher v0.** Diary 04.
- [x] **10 RKC routing benchmark v1.** 11 kernels; benchmark 54/55 = 98.2%,
  macro precision 1.00 (zero false positives). Silent-zero Gauss-sum hazard
  fires on every q ≡ 2 mod 4 case. Diary 11.
- [x] **14b RKC routing benchmark v2.** **55/55 = 100%**. Macro precision 1.00,
  macro recall 0.95. No v1 regressions. Diary 14.

## Pass D — FEP / mock-modular bridge

- [x] **15 Generative model whose evidence is a mock theta.** Lattice gas
  with two bosonic species at z = -1; Z(q) = f(q) verified to 25-50 digits
  across β ∈ [0.05, 10]. Diary 13.
- [x] **16 "Shadow = mutual information?" probe.** 4 candidates (MI, KL,
  Surprise, Fisher) all fail; structural reason (g* bounded at cusp). Diary 13.
- [x] **17 Mock-theta residual EBM v1.** Exact Hickerson-Mortenson shadow +
  Eichler integral via Watson 1936; bias reduction ~258 bits at small β;
  modular cross-check at ≥30 digits. **Caught a real v0 bug**: even Kronecker
  character used when odd primitive mod 12 was required. Diary 12.
- [x] **18 Bounded-at-cusp shadow probes.** 8 new candidates fail (Rényi-α,
  Bhattacharyya, Hellinger², entropic uncertainty). Sharpened conjecture:
  g* is an **Eichler cocycle in H¹(Γ, V_k)**. Diary 15.
- [x] **20 Wigner-negativity-aware divergences.** 4 candidates fail. One
  zero-parameter cusp-asymptote coincidence (log(2)/g*(0) = 0.20025 vs
  empirical 0.20033); bulk shape fails 100% → coincidence not proportionality.
  Diary 17.
- [x] **21 Path-measure functionals.** 3 candidates fail. **Decisive
  structural finding**: cooling path traverses imaginary-axis half-line in
  the wrong direction (cusp 0 → interior vs Eichler interior → ∞). Rules
  out the partition-function-path-integral interpretation. Diary 18.
- [x] **22 Direct Eichler-cocycle reconstruction from transfer matrix.**
  STRUCTURAL NEGATIVE: trivial spectrum + (K+1)² S-transform dim mismatch
  + K→∞ defect reduces to Watson 1936 (tautological). Diary 19.

**Pass D closed.** 20 candidates across 5 structurally-different families
all fail. Cohomological-irreducibility conjecture established at
medium-high → high confidence.

## Pass B follow-up — recognizer ↔ Eichler integration

- [x] **19 `MODULAR_COMPLETION_REQUIRED` → Watson-Hickerson.**
  `rkc/completions.py` shipped. f3 mock-theta inputs return numerical values
  to ≥30 digits with a certificate. 50/50 unit tests. Diary 16.

## Hunt 5 — Quarterly Reports operator tagging

- [x] **23 QR operator tagging.** Hand-tagged all 33 math-content sections of
  Berndt's 2022 HRJ reproduction. 80% prediction FALSIFIED at 57.6% coverage;
  4 of 6 predicted operators NEVER fire. Revised 7-operator basis covers
  ~91%. QR III is fractional iteration / Hardy orders / operator calculus,
  not modular forms. **Hunt 5 closed.** Diary 20.

## Cross-cutting deliverables (shipped)

- [x] `insights/CANDIDATE_INSIGHTS.md` — substantiated findings (A1-A7, B1,
  C, D, D1, E synthesis).
- [x] `insights/DID_NOT_PAN_OUT.md` — 15 entries (4 REFUTED, 4 CORRECTED,
  5 PARTIALLY REFUTED, 2 DOWNGRADED) + OUTSTANDING.
- [x] `insights/HUNT_MAP.md` — Hunt-by-Hunt with current unblock status.
- [x] `insights/BIG_IDEAS_REVIEW.md` — running judgment on the 7 big-picture
  ideas from the brainstorm.
- [x] `corpora/transcriptions/operator_tagging_schema.py` — 6-operator
  schema; now flagged 2 verified / 4 falsified-for-QR-corpus.
- [x] `rkc/` standalone package (recognizer, registry, costs, routing,
  completions, tests).
- [x] `diary/` (20 entries) + `diary/INDEX.md`.
- [x] `manifest/` (cataloguing of primary sources).
- [x] `sota_comparisons/` (physics & computation, open problems / under-mined
  corners).
