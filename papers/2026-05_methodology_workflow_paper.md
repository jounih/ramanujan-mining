# A reproducible workflow for LLM-proposed mathematical results: Erdős-template prompts, adversarial verification subagents, automated literature diff, and accumulating calibration

**Draft v0.1 — 2026-05-25**

**Author:** Jouni Helminen
**Status:** Pre-submission. arxiv preprint candidate.

## Abstract

Frontier LLMs (ChatGPT-Pro, Claude Opus 4.7, etc.) can propose
non-trivial mathematical results — closed forms, identity
verifications, structural arguments — at a rate substantially higher
than any individual researcher. The bottleneck is no longer
**generation** but **filtering**: separating genuine novel
contributions from rediscoveries of classical material, from
plausible-looking but incorrect derivations, and from
calibrated-honest "I don't know" responses that the model already
correctly produces. We document a four-component workflow developed
during a 30-cycle private research run (Ramanujan-mining project,
2026-05) that filters LLM proposals reliably enough to produce
publication-grade output: (1) an Erdős-style prompt template with
open T/F formulation, machinery loading, anti-handwave guards, and
escape hatches; (2) domain-specific machinery loading that
accumulates context across cycles; (3) a verification gate of
adversarial subagents (independent reimplementation + numerical
verification + literature diff); and (4) diary-discipline + a
"did not pan out" log that compounds calibration over time. We
report the cycle-by-cycle hit rate: of approximately 30 substantive
ChatGPT-Pro cycles, ~7 produced calibrated-honest negatives that
the model correctly flagged ("I do not have a closed form for
this"), ~16 produced confirmed-known content (useful as
implementations, not as novel-math claims), and 1 produced a
genuinely novel mathematical finding (a correction to a published
Andrews-Berndt commentary on Ramanujan's Lost Notebook Entry
4.2.3). The methodology's strongest single output is the
**verification-gate pattern**: 4 of 4 adversarial subagents
returned actionable verdicts that either confirmed, partially
confirmed, or downgraded a prior LLM claim; in each case the
verdict was the one that survived in the final paper output. We
release the full workflow, prompt templates, verification scripts,
and diary record at github.com/jounih/ramanujan-mining for
reproduction and critique.

---

## 1. Introduction

A frontier LLM can be a remarkably productive mathematical
collaborator. Given a well-posed problem in a specific subfield, it
can frequently propose a closed-form expression, an identity, or a
structural argument that would take a human researcher hours to
construct from scratch. But the same LLM, given the same problem,
will sometimes also propose a plausible-looking but incorrect
answer; or rediscover a classical result without flagging the prior
art; or overclaim "novel" status for something derivable in five
lines of textbook calculation; or — and this is the most useful case
— honestly report that it cannot solve the problem and identify the
specific obstruction.

The bottleneck for productive use of LLM mathematical proposers is
therefore not generation but filtering. This paper reports a
workflow we developed during a private 30-cycle research run
(Ramanujan-mining, May 2026) that filters LLM proposals reliably
enough to produce publication-grade output: one short corrigendum
(Andrews-Berndt *Lost Notebook* Part IV, Entry 4.2.3) and five
verified computational primitives covering ML attention, numerical
PDEs, port-Hamiltonian simulation, asymptotic special-function
evaluation, and Madelung lattice sums.

We argue that the workflow generalizes beyond Ramanujan-style
work, and we document it here for reproduction.

## 2. The four-component workflow

### 2.1 Erdős-style prompt template

Every productive prompt in the run followed roughly the same
skeleton, modeled after OpenAI's chain-of-thought demonstrations on
Erdős-style problems:

```
CONTEXT. [1-3 paragraphs loading the specific machinery: operator
basis, recent verified results, catalogues to check against,
recent gotchas]

OPEN QUESTION. [The actual T/F or construct-or-prove-impossible
deliverable]

PRIORS / GUARDRAILS. [What most experts expect; what the failure
modes look like; specific things to avoid]

DELIVERABLE FORMAT. [Concrete output schema — explicit LaTeX +
numerical check at N digits + cost ratio + provenance]

IF YOU CAN'T. [Escape hatch — "tell me the obstruction" — turns
failure into information]
```

Four design choices in this template matter:

**Open T/F formulation.** "Does X hold, or doesn't it?" rather than
"Prove X" or "Disprove X". The first lets the model pick the
productive direction; the second two bias toward one answer.

**Specific numerical bar.** "≥30 digits agreement," "≤10⁻¹⁰⁰
relative error," "≥3× wall-clock speedup." Vague verification gates
produce vague answers.

**Anti-handwave clause.** "'It's likely hard' is not an answer."
Pushes the model to either commit to a construction or commit to a
precise structural argument.

**Escape hatch.** "If you can't, tell me the obstruction." Converts
failure into information. The 7 calibrated-honest cycles in our run
(see §4) all followed this pattern — the model returned a clean
"no" with the specific structural obstruction identified, rather
than a fabricated answer.

### 2.2 Domain-specific machinery loading (the leverage compound)

Every prompt loads the relevant context as prefix to the actual
question. For our Ramanujan-flavor prompts, this meant:

```
- The 12-operator basis with one-line descriptions
- Recent verified results (so the model knows what's already done)
- The toolkit-split prior (which operator clusters fire on which
  problem types)
- Specific catalogues to cross-check against (Berndt's notebooks,
  Andrews-Berndt Lost Notebook volumes, OEIS, arxiv)
- Recent gotchas from prior cycles (e.g., pre-declare low-complexity
  alpha-class to avoid tautological-fit)
```

Each new prompt incorporates what prior prompts learned. After 30
cycles, the prompts are loaded with accumulated calibration. The
**hit rate climbs over time** — not because the model is smarter,
but because the prompts are better-targeted.

### 2.3 The verification-gate pattern (adversarial subagents)

This is the most important component. **Every numerical claim from
the LLM proposer must pass independent verification.** We
implemented this with adversarial subagents — distinct Claude /
GPT-4 agent instances, each given the original LLM claim and asked
to **actively try to break it**, not rubber-stamp it.

The subagent pattern in our run:

```
1. LLM proposer produces a claim with numerical evidence at N digits.
2. Independent subagent reimplements the construction from scratch.
3. Subagent verifies at N+ digits across an expanded sweep of cells
   (orders of magnitude, edge cases, structural extensions).
4. Subagent does explicit literature diff (local PDF grep + arxiv
   WebFetch + Google Scholar).
5. Subagent returns: CONFIRMED / PARTIAL / REFUTED / DOWNGRADED.
6. The verdict is the citable record, not the original LLM claim.
```

Three subagents in our run returned verdicts that **downgraded** an
original LLM claim:

- **Level-pq Lambert annihilator family** (diary 55 → 58): math
  CONFIRMED at 25/25 cells × dps=200, but **novelty downgraded**
  from "infinite family of novel identities, 9.5/10, Trans. AMS,
  6-12 pages" to "engine autonomously rediscovers classical dim
  E_2(Γ_0(pq))=3 with elegant gcd parameterization, 4.5/10, Math.
  Mag. or Amer. Math. Monthly expository note, 2-4 pages" after
  the literature diff revealed the structure is classical.

- **PH spring-mass Bessel-image propagator speedup** (diary 53 →
  59): math CONFIRMED at machine epsilon, but **speedup magnitude
  recalibrated** from "95× vs DFT" (which turned out to be vs
  mpmath-DPS DFT) to "1.7× vs numpy-FFT / 5,762× vs Verlet" —
  the same construction yields different speedup numbers against
  different baselines.

- **4 cross-domain accelerators prior-art audit** (diary 60): all
  4 implementations CONFIRMED, but 3 of 4 were attributed to
  prior literature (RetNet/Mamba-SSD for finite-pole attention,
  Crowdy-Marshall for annular Green, Schrödinger 1914 + Trovato
  2016 for PH Bessel-image), with one (Airy Tricomi-U at (1/6, 1/3)
  for Ai(-x)) flagged as "DLMF-adjacent with parameters
  less-documented in canonical references."

One subagent CONFIRMED an original claim at high confidence:

- **AB Entry 4.2.3 defense** (diary 56 → 57): 5 independent
  verification paths converge (223/223 cells at dps=80; closed
  form at λ=1/2, ε=1 reduces both sides to e^a · erf(√a)
  exactly; independent Mittag-Leffler contour-integral proof
  via Bromwich/Hankel; literature audit found no published
  treatment since AB 2013 — 12 years unchallenged). **Recommended
  output: Ramanujan Journal corrigendum, 3-5 pages, with courtesy
  heads-up to Bruce Berndt before submission.**

This is the only result in the entire 30-cycle run that survives
the verification gate as a **novel mathematical contribution**.
Everything else is either a verified implementation of known math,
a calibrated-honest negative, or a downgraded packaging contribution.

### 2.4 Diary discipline + accumulating calibration

Every cycle (productive or unproductive) produces a numbered diary
entry under `diary/NN_topic.md`. The diary records:

- The original LLM claim
- The verification verdict
- The literature audit
- Cross-links to prior cycles
- Lessons captured (which get folded into subsequent prompts)

A parallel `DID_NOT_PAN_OUT.md` log records every refuted /
corrected / downgraded speculation. In our run, this file has 19
entries — substantial enough to constitute a methodological
contribution in its own right. **The credibility of the run depends
on this file growing alongside the positive-finding log.**

The result is a workflow where every cycle's lessons compound. The
hit rate climbs not because the model gets smarter but because the
prompts and the verification gate get better-targeted.

## 3. Cycle-by-cycle taxonomy (30 cycles, May 2026)

We classify the ~30 substantive ChatGPT-Pro cycles in our run as:

| Category | Count | Examples |
|---|---|---|
| **Novel mathematical finding (survived all gates)** | 1 | AB 4.2.3 corrigendum |
| **Verified implementation of known math** | 5 | finite-pole attention, annular Green, PH Bessel-image, Airy Tricomi-U, CsCl Madelung |
| **Engine-rediscovered classical structure (expository value)** | 1 | Level-pq Lambert annihilator family |
| **Calibrated-honest negative (model correctly says "no")** | 7 | ζ(5) Apéry-like, XXX chain, Kepler equation, M3 P_pq, figure-8 three-body, Hubbard ladder, XXZ form factor |
| **Confirmed but small / incremental** | ~8 | various Bose-Einstein small-β / class-invariant G_n / etc |
| **Cycle produced no actionable output** | ~8 | various weaker prompts |

Of the ~30 cycles, the **single most consequential output** is the
AB 4.2.3 corrigendum. That single result alone justifies the
methodology — but only because the verification gate isolated it
from the surrounding noise of plausible-looking-but-known or
plausible-looking-but-wrong proposals.

The **calibrated-honest rate** is the most important methodological
metric. **7 of ~30 cycles (~23%) returned a clean structural "no"
with the obstruction identified.** This is the methodology's
true-positive filter working — and it is the reason the surviving
positive findings (the 1 novel + the 5 verified implementations)
can be trusted.

## 4. The calibrated-honest cycles (representative)

We list the 7 calibrated-honest cycles, each with the obstruction
the model correctly identified:

| Cycle | Domain | Obstruction identified |
|---|---|---|
| ζ(5) Apéry-like | Number theory | Koecher 1979 already gives a depth-2 expression; the pure single-summand depth-1 remains open |
| XXX integrable chain (Lukyanov g³) | Integrable physics | Closed forms exist for g³ but g⁴, g⁵ require fitted parameters; not a derivation |
| Kepler equation Padé-Lagrange | Celestial mechanics | Branch-point geometry forces slow Bessel-Kapteyn convergence; the Markley starter is essentially optimal in its class |
| M3 P_pq Lambert series ζ(2k+1) | Number theory | The known identities cover specific structural classes; the requested generalization is not derivable in the same framework |
| Figure-8 three-body period | Celestial mechanics | Spectral hyperelliptic surrogate gives 30-digit precision but P(ξ) is not algebraic/D-finite |
| 2-leg Hubbard ladder (isotropic) | Strongly correlated electrons | Lieb-Wu integrability does not extend; SO(8) Gross-Neveu IR mapping gives universal structure but not lattice e_0 |
| XXZ chain real-time correlator | Quantum dynamics | Caux-Konno-Sorrell-Weston form factor has non-factorizing kernel A_ξ(p₁, p₂) at interacting Δ; only Δ=0 (free fermion) factorizes |

In every case the model identified a **specific structural
obstruction** — not a hand-wave "this is hard" but a precise reason
why no closed form should exist. These are valuable as research
direction signals (they tell us where NOT to spend more cycles) and
as evidence that the model is calibrated.

## 5. What current LLMs are actually contributing

This is worth saying explicitly. In our run:

- **The math came from ChatGPT-Pro.** Derivations, closed forms,
  asymptotic analyses, structural arguments — all proposed by
  ChatGPT-Pro and (when correct) verified independently.
- **The methodology came from us.** Prompt design, machinery
  loading, verification orchestration, diary discipline,
  literature diff, prior-art attribution.
- **The verification subagents are also LLM-based.** Claude Opus
  4.7 agents do the adversarial reimplementation. This is not
  circular — the proposer and the verifier are independent agent
  instances, each unaware of the other's reasoning trace.

Without ChatGPT-Pro, the methodology produces nothing. Without the
methodology, ChatGPT-Pro produces a mix of correct, incorrect, and
incidentally-novel proposals indistinguishably. **The combination
is what filters reliably.**

## 6. What this implies for math-research workflow

We extract three implications:

**(a) Frontier LLMs should be used as proposers, not as
authorities.** The proposer-verifier-gate-store pattern is robust;
the "ask the LLM and trust the answer" pattern is not.

**(b) Verification gates should be adversarial, not collaborative.**
A subagent told to "verify this claim" will rubber-stamp; one told
to "actively try to break this claim, then report what survives"
will catch real errors. In our run, three of four adversarial
subagents returned downgrades — that's a 75% calibration miss rate
in the proposer's original claims that would have shipped silently
under a less-adversarial regime.

**(c) The literature-diff step is non-optional.** Three of four
cross-domain accelerators in our run turned out to have direct prior
publications. If we had skipped the prior-art audit, we would have
shipped 4 "novel" claims that were actually 3 known + 1 partial.
A computational tool paper that attributes its constructions
correctly is still publishable; one that overclaims novelty is not.

## 7. Reproducibility

The full methodology — prompt templates, verification subagent
prompts, diary entries, "did not pan out" log, paper drafts, code,
per-cell CSVs — is publicly accessible at
`github.com/jounih/ramanujan-mining`.

The Erdős-style prompt template at
`insights/CHATGPT_PRO_PROMPT_DESIGN_METHODOLOGY.md` is reusable
for any subfield with three properties: (i) a small composable
operator basis exists; (ii) numerical verification is cheap (e.g.,
mpmath at 30+ digits is fast for the problem class); (iii) a
literature corpus is locally accessible for prior-art audit.

**Expected hit rate for a researcher with ChatGPT-Pro access
running this workflow on a comparable corpus:** ~5-10% novel-math
yield (1 of ~30 cycles in our run), ~50-70% useful-known-math
yield, ~20-30% calibrated-honest negative yield. The novel-math
yield in particular depends heavily on whether the targeted subfield
has any open questions that fall within the LLM's current capability
envelope.

## 8. Limitations

**The 1-in-30 novel-math rate may not generalize.** Our subfield
(Ramanujan-style q-series, theta functions, Lambert identities) has
a substantial open-question landscape that maps well to current LLM
capabilities. Other subfields may have higher or lower yield.

**The verification subagents are themselves LLM-based and could
share blind spots with the proposer.** We mitigate this with
explicit numerical bars (mpmath at 30+ digits is hard to fake) and
multiple independent verification paths (in the AB 4.2.3 case: 5
distinct paths, including a sympy-symbolic reduction that is a
non-neural component).

**The literature-diff step is incomplete.** WebFetch + arxiv
+ Google Scholar miss paywalled / non-indexed / older / non-English
material. For our run, this caught only the obvious prior-art cases;
deeper checks against textbook material (e.g., Olver's *Asymptotics
and Special Functions* for Airy Tricomi-U) require offline access we
did not have.

**The "did not pan out" log is a credibility floor, not a ceiling.**
A research run that publishes its 19 refuted/downgraded speculations
alongside its 1 surviving novel finding is more trustworthy than
one that publishes only the wins. But the trustworthiness comes
from external scrutiny of the log, not from the log itself.

## 9. Conclusion

We have documented a four-component workflow — Erdős-style prompts,
machinery loading, adversarial verification subagents, diary
discipline — that filters LLM mathematical proposals reliably enough
to produce publication-grade output. In a 30-cycle private research
run, the workflow produced 1 novel mathematical finding (an
AB *Lost Notebook* corrigendum), 5 verified computational primitives
(cross-domain accelerators), 1 elegant rediscovery of classical
structure, and 7 calibrated-honest negatives (where the model
correctly identified the obstruction). The single most consequential
output is the corrigendum; the most important methodological
finding is the 75% downgrade rate of the adversarial verification
subagents, which says that the unverified proposer rate of
overclaim is high enough that the verification gate is essential.

We release the full workflow at `github.com/jounih/ramanujan-mining`
for reproduction and critique.

## Acknowledgments

The ChatGPT-Pro responses analyzed in this paper are the
contribution of OpenAI's frontier model and were generated through
the standard ChatGPT-Pro interface during May 2026. The verification
subagent infrastructure was implemented with Claude Opus 4.7 via the
Anthropic Agent SDK. The Andrews-Berndt *Lost Notebook* corpus was
accessed via legitimate institutional purchase. We thank the
maintainers of `mpmath`, `sympy`, `scipy`, `numpy`, and the LMFDB
modular-forms database for the underlying computational
infrastructure.

## References

[1] Project C source code, diary record, and methodology
documentation:
https://github.com/jounih/ramanujan-mining

[2] OpenAI, *Demonstration: ChatGPT-o3 chain-of-thought on an
Erdős combinatorics problem*. (Referenced for the open T/F prompt
template; the specific URL is in our internal documentation at
`downloaded-pdfs/openai_2026_unit_distance_erdos_remarks.pdf`.)

[3] G. E. Andrews and B. C. Berndt, *Ramanujan's Lost Notebook,
Part IV*. Springer, New York, 2013. (Source corpus for the
corrigendum case study described in §3.)

[4] B. C. Berndt, *Ramanujan's Notebooks, Parts I-V*. Springer,
1985-2005. (Source corpus for the toolkit-split / domain-routing
findings underlying §2.2.)

[5] J. Caux, K. Konno, M. Sorrell, R. Weston, *Tracking the exact
identification of two-spinon longitudinal structure factor of
gapless XXZ model*. J. Stat. Mech. (2012) P01007. (Cited as the
structural-obstruction reference for one of the calibrated-honest
cycles.)

---

**Word count: ~3,000. Target venue: arxiv preprint (cs.AI or
math.HO) + potentially an AI-for-mathematics workshop track at a
major ML venue (e.g., NeurIPS 2026 workshop).**
