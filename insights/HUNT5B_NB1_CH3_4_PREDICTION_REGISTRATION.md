# Pre-registration: Hunt 5b extended to Berndt NB Part 1 Ch. 3-4 (Master Theorem material)

**Date locked:** 2026-05-24 (before hand-tagging)
**Status:** PRE-REGISTERED. The hand-tagging experiment must be run by an
agent BLINDED to this document.

## Background

Hunt 5b's toolkit-split hypothesis (diary 25, established at high
confidence across 3 chapters of Berndt *Notebooks Part V*):
- Ch. 32 (continued fractions): `q_shift` + `modular_S_transform` dominant pair
- Ch. 34 (class invariants): `class_field_galois_average` + `modular_S_transform`
- Ch. 36 (modular equations): `modular_S_transform` monoculture
- ALL three: zero firing of QR-side operators (master_theorem,
  frullani_limit, fractional_functional_iteration, hardy_orders_of_infinity,
  mellin_pair_reciprocity)

The Quarterly Reports (1903-1914), hand-tagged in Hunt 5 (diary 20):
- 91% covered by the QR-side 5-operator cluster
- Zero firing of modular operators

This established what we called the "QR-vs-Notebooks toolkit split". Open
question per diary 25 follow-up: **is the split PROVENANCE-driven (some
property of where Ramanujan wrote — the Cambridge Letters/QRs vs the
India Notebooks period) or TOPIC-driven (which mathematical area is being
worked on)?**

## The experiment

**Hand-tag Berndt *Notebooks Part 1* Ch. 3-4** (the chapters covering the
Master Theorem + analysis material that QR I/II expand on; in
`downloaded-pdfs/ramanujankitap1.pdf`). This is **Notebooks-side
material BY PROVENANCE** but **QR-side material BY TOPIC**.

If the QR-vs-Notebooks split is **provenance-driven**: Ch. 3-4 should
fire modular operators (because it's in the Notebooks).

If the split is **topic-driven**: Ch. 3-4 should fire QR-side operators
(because it's Master Theorem material), even though it's physically in
the Notebooks corpus.

## Pre-registered predictions

**Correction (2026-05-24):** an earlier version of this file attributed
the meta-prediction "split breaks as provenance / holds as topic" to
both the human user AND ChatGPT Pro. That was a transcription error —
ALL pre-registered prediction content below is ChatGPT Pro's, delivered
in response to the Erdős-style prompt designed in this session
(Prompt 4 from the v0.8a follow-up: "reverse-Hunt-5b predictive
validation"). The human user forwarded it without an independent
prediction of their own.

The pre-registration remains valid as a single-agent prediction; the
"two independent agents converge" framing was wrong and is retracted.

### Meta-prediction (ChatGPT Pro)

> **"Ch. 3-4 will break the QR-side/Notebooks-side split as a corpus/
> provenance claim, but it will preserve the split as a topic/toolkit
> claim. I would expect a clean analytic/RMT cluster, not a modular
> surprise."**

I.e., Ch. 3-4 will fire the QR-side analytic cluster, NOT the
Notebooks-side modular cluster, even though it physically lives in a
Notebooks volume.

### ChatGPT Pro prediction (verbatim, 2026-05-24)

Full prediction transcribed exactly as delivered. Operator-by-operator
predictions with calibrated confidence:

| Operator | Predicted saturation | Bucket | Confidence |
|---|---|---|---|
| `master_theorem` | 85-95% | Dominant | 0.75 |
| `mellin_pair_reciprocity` | 70-88% | Dominant / high support | 0.55 |
| `frullani_limit` | 15-30% | Supporting | 0.60 |
| `fractional_iteration` | 8-20% | Low support / supporting | 0.35 |
| `modular_S_transform` | 0-3% | Near zero | 0.85 |
| `class_field_galois_average` | 0-1% | Near zero | 0.92 |
| `q_shift` | 0-5% | Near zero | 0.75 |

ChatGPT's bottom-line probability distribution over outcomes:
- 70% probability: Ch. 3-4 is QR-side analytic by operator profile
- 20%: mixed analytic, master_theorem dominant but Mellin/Frullani/
  fractional_iteration distributed more evenly than expected
- 7%: novel generalized-Gamma operator pattern emerges (not in current
  basis — the *interesting* outcome per ChatGPT)
- 3%: modular operators unexpectedly appear at meaningful frequency

ChatGPT's caveats:
1. The `mellin_pair_reciprocity` prediction is tagging-granularity
   sensitive. If we allow it to co-fire with `master_theorem` whenever
   the proof uses RMT as a Mellin-transform identity, it should exceed
   80%. If reserved strictly for explicit transform-pair reversals, it
   may fall to high supporting frequency.
2. The `fractional_iteration` prediction depends on whether the chapter
   treats generalized Gamma functions through recurrence/extension
   machinery. If yes → >10%. If mostly Mellin/RMT → <10%.
3. The `q_shift` near-zero prediction has a caveat: ordinary coefficient/
   index/Gamma-recurrence shifts should NOT count as `q_shift`. If the
   tagging rubric accidentally conflates ordinary analytic shifts with
   q-shifts, false positives could enter.

## Pre-registered falsification signals (per ChatGPT Pro)

The strongest evidence AGAINST the joint topic-toolkit prediction would be:

1. **`modular_S_transform` > 10%** — would suggest hidden modular
   structure in the chapter, not just topical analytic material.
2. **`q_shift` > 10% under strict q-operator definition** — would imply
   a real q-series or q-difference grammar intrudes into the Master
   Theorem material.
3. **`master_theorem` stays below 50%** — would mean either the chapter's
   surface topic is misleading relative to proof-unit mechanics, OR the
   tagging unit is much finer than predicted.
4. **A novel operator outside the QR/Notebooks split exceeds 30%** —
   would be the most interesting outcome: not "QR-side wins" or
   "Notebooks-side wins", but a third analytic subcluster for
   generalized-Gamma / integral-transformation material.

## What it would mean for the project

| Outcome | Interpretation | Project impact |
|---|---|---|
| **Topic-toolkit hypothesis confirmed** (master_theorem 85-95%, modular ops < 5%) | Toolkit-split is TOPIC-driven, not author-driven. The cog-sci finding becomes more universal — predicts ANY mathematician working in modular forms vs analytic territory would deploy the same per-domain operator clusters. | Strengthens Pass D § cog-sci framing of the W8 paper; promotes the toolkit-split from "Ramanujan-specific" to "domain-conditional general principle". |
| **Provenance hypothesis re-emerges** (modular_S_transform > 10% in chapter despite being Master Theorem material) | The split has a corpus/authorial component independent of topic. Implies something about *how* Ramanujan deployed his toolkit that's specific to him. | Strengthens the personal-cognitive story; weakens the universalist reading. |
| **Novel operator emerges** (>30% on something not in current 11-basis) | Third analytic subcluster exists (generalized-Gamma family?) that we missed. Expands the operator basis from 11 to 12+. | Direct architectural input to v0.8c+ — add the new operator, retest Hunt 5b chapters with the expanded basis. |
| **Master Theorem under-dominant** (<50%) | Tagging-granularity issue OR the chapter is differently structured than expected. | Methodological — review tagging conventions; may need to re-tag earlier chapters with same finer granularity. |

## Methodology constraints (must be followed by the tagger)

1. **The tagging agent MUST NOT read this file** until the tagging is
   complete. Run the experiment blinded.
2. **Use the EXACT same 11-operator basis** as Hunt 5b Ch. 32/34/36 (per
   `corpora/transcriptions/operator_tagging_schema.py` and the 5
   chapters of tagging already done).
3. **Tag the same way** as Hunt 5b — one row per proof unit (Theorem /
   Lemma / Entry / Corollary), with operator-firing indicators per row.
4. **Output the per-operator saturation rate** in the same format as
   diaries 22, 24, 25 (e.g. `analysis/24_hunt5b_ch36.py` format).
5. **Write a diary entry** comparing actual to pre-registered prediction;
   explicitly note which predictions were confirmed / falsified / mixed.

## Source

`downloaded-pdfs/ramanujankitap1.pdf` — Berndt, *Ramanujan's Notebooks
Part 1* (Springer 1985). Chapters 3-4 cover Master Theorem material
per the existing downloaded-pdfs/README.md note: "Ch. 3-4 (Master Theorem
+ analysis material that QR I + QR II expand on)".

The agent should confirm the chapter scope via the PDF's TOC and tag
ALL proof units in those two chapters.

## Cross-link

After tagging:
- Reference this file in the resulting diary entry
- Update `insights/BIG_IDEAS_REVIEW.md §4` (cog-sci framing)
- Update `insights/HUNT_MAP.md` Hunt 5b status to "extended to NB Part 1
  Ch. 3-4 with [confirmed/falsified] pre-registered prediction"
