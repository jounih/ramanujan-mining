# Diary 39 — Ramanujan-taste compression metric: pilot succeeds with sharp grammar-dependent caveat

**Date:** 2026-05-25
**Source:** ChatGPT Pro response to Prompt 5 from the v0.8a follow-up.
5th Erdős-style cycle.
**Status:** Pilot CONFIRMS a computable metric separates Ramanujan from
random-walk identities, BUT the metric is grammar-relative. Strong
"universal compression threshold" claim FALSIFIED; pragmatic
filter-grade version useful for Project C.

## What was tested

Open question (Prompt 5): can we define a computable "compression
ratio" metric on q-series identities such that Ramanujan's recorded
identities cluster at high ratio, "random" identities cluster low,
and the cutoff is sharp and matches a structural property?

## Result

### A. Concrete metric (computed)

For an identity `I` over a grammar `G` with primitives `{q, Z, +, -, ×,
/, q^m, (a;q)_∞, G_n, H_n, η_d}`:

- `K_G(I)` = canonical AST serialization bit length
- `W_N(I)` = total coefficient bits hidden inside the identity's
  q-expansions to depth N (Σ over atoms of Σ_{n≤N} (1+⌈log₂(|a_n|+1)⌉))
- **Compression score**: `S_N(I) = log₂(W_N(I)) / log₂(K_G(I))`

### B. Pilot data at N=200

**Ramanujan sample** — 13 Rogers-Ramanujan identities from
Frye-Garvan's catalogue (their G_n / H_n / η_d notation):

| Score range | Median | Sample |
|---|---|---|
| S_200 ∈ [1.36, 1.76] | 1.59 | 13 identities |

**Random-walk null model** — 10 finite identities generated from
distributive law + product rule + substitution composition, using
operators {S_m, Q_r, D, F_r, I_r, +, ×} on sparse q-polynomial seeds.
All verified exactly through q^200:

| Score range | Median | Sample |
|---|---|---|
| S_200 ∈ [0.80, 1.08] | 0.95 | 10 identities |

**Cutoff S_200 ≈ 1.20 cleanly separates** — `max(random) = 1.08 < 1.20
< 1.36 = min(Ramanujan)`. **Perfect separation on this sample**.

The structural correlate (predicted in Prompt 5): high-scoring
identities collapse `G·H` products to `η`-products or constants;
low-scoring identities are finite combinatorial/algebraic rewrites.
**Confirmed**.

### C. Critical caveats — strong claim falsified

ChatGPT identified three obstructions to "universal threshold":

1. **Grammar-dependent**: if `η_d, G_n, H_n, (a;q)_∞` are PRIMITIVES,
   Ramanujan-type identities score high. If they are expanded into
   infinite products or coefficient recurrences, the SAME identities
   score much lower. No mathematically canonical choice.

2. **Null-model-dependent**: a stress test where the random generator
   itself uses `G, H, η` primitives produced random-walk identities
   with `S_200 ∈ [1.23, 1.44]` — **overlapping the lower end of the
   Ramanujan range**. The metric detects "modular/eta-product
   compression", not "Ramanujan's mind in isolation".

3. **Raw LaTeX length is unstable** — e.g. `G_11·H_1 − q²·G_1·H_11 = 1`
   is highly compressed if `G, H` are primitives; less if expanded to
   q-Pochhammer; even less as coefficient recurrences.

### Verdict

| Claim | Verdict |
|---|---|
| "Computable metric separates Ramanujan from generic in some grammar" | **CONFIRMED** for the pilot (Frye-Garvan G/H/η grammar; finite-polynomial random-walk null) |
| "Universal notation-independent threshold recovering Ramanujan's taste" | **FALSIFIED** — the threshold is grammar-relative |
| "Threshold transfers from one mathematical period to another" | Untested — pilot is one subcorpus |

## What this means for Project C

ChatGPT Pro's specific recommendation: a discovery engine should
optimize a multi-term score, not raw compression:

```
score(I) = S_N(I)
         − λ₁ · proof_length(I)
         − λ₂ · tautology_penalty(I)
         − λ₃ · family_duplication(I)
```

With a structural bonus for identities whose RHS is an **η/θ/Γ/algebraic
closed form** rather than a finite expansion. This would preferentially
surface Rogers-Ramanujan-style identities over generic random-walk
products.

**Concrete v1.x architectural feature**: add a `CompressionFilter` to
Project C's accept pipeline. After an identity passes the
verifier+cost-gate, compute `S_N(I)` against rkc's basis-as-grammar; if
`S_N < 1.20`, downrank to "auxiliary identity" registry; if `S_N >
1.20` AND RHS is a closed form, promote to "headline identity"
registry. The compressed-form bias is the Ramanujan-style filter.

**This is the first principled answer to "what should Project C
optimize beyond raw validity?"**

## Caveats on Project C application

- The grammar-dependent caveat MATTERS: rkc's recognizer already has
  η, θ, Γ, etc. as families. Using rkc's family as the metric grammar
  is the natural choice; we should NOT use raw LaTeX. This aligns
  Project C with the pilot's working grammar.
- The 1.20 cutoff is calibrated for the Frye-Garvan Rogers-Ramanujan
  subcorpus. Other Ramanujan subcorpora (class invariants, mock theta)
  may need different thresholds. v1.x should fit per-domain thresholds.
- The metric currently uses N=200 coefficient depth as a proxy for
  "certified to 30 digits". Production version should use
  N = N_30(I, ρ) — least depth + tail bound needed to certify to
  10^(-30) on |q| ≤ ρ. rkc's existing certificate machinery should
  produce N directly.

## Bottom line

**Pilot confirms a Ramanujan-taste compression metric is real and
computable RELATIVE TO A FIXED GRAMMAR.** Strong universal-threshold
claim falsified by grammar-relativity. Pragmatic filter-grade version
is directly actionable for Project C's accept pipeline — first
principled answer to "what should the engine optimize beyond validity".

**Confidence**: high on existence-relative-to-grammar (perfect
separation on the pilot); low on universality (grammar-dependent +
null-model-dependent obstructions are real). Medium on Project C
applicability (the natural rkc-family grammar should give similar
separation; needs prototype verification).

## Follow-up leads

1. **Prototype the CompressionFilter** as a v1.x feature in
   `rkc/search/filters.py`. Use rkc's existing family registry as the
   grammar. Test on the 5 v0.4-v0.8 accepted identities + 5 random-walk
   identities; see if the cutoff holds.
2. **Pre-registered blinded experiment**: canonicalize the full
   Ramanujan corpus (per CLAUDE.md scope: Notebooks + Lost Notebook +
   QRs + letters) under a fixed grammar; build matched non-Ramanujan
   controls from the same period (Euler / Jacobi / Hardy); test
   whether the per-period threshold survives. This is a serious
   cog-sci paper if positive.
3. **W8 paper update** — add a §"Discovery-engine optimization
   targets" section folding in the multi-term score formula. The
   compression-bias-toward-Ramanujan-style filter is the engine's
   "aesthetic" formalized.
4. **CANDIDATE_INSIGHTS update** — add to §A8 (generalized obstruction)
   or new §A10 (compression-metric existence).

## Cross-link

- diary/35 — B1.5 closure (1st ChatGPT-Pro cycle)
- diary/37 — 3rd-bridge generalization (2nd cycle)
- diary/38 — Hunt 5b latent algebra construction + obstruction
  (3rd cycle on Prompt 1)
- diary/39 — This entry: compression metric pilot (4th cycle on
  Prompt 5)
- HUNT5B_NB1_CH3_4_PREDICTION_REGISTRATION.md — locked-in
  pre-registration for Prompt 4 (reverse-Hunt-5b); blinded tagger
  still running

**5 of 5 ChatGPT-Pro Erdős-style cycles have produced
project-advancing results.** Cycle time still ~45 min each. Workflow
fully validated.
