# Diary 21 — Hunt 1: Lost Notebook pp. 341-343 (1729 K3 inventory)

**Date:** 2026-05-24
**Source:** Andrews-Berndt *Ramanujan's Lost Notebook* facsimile, pp. 340-344
(extracted from `chatgpt-pro-mining/.../primary_originals/page_images/lost_notebook/`,
which corresponds to the Narosa 1988 reprint scanned from Sirinudi at
`https://ramanujan.sirinudi.org/Volumes/04/04.pdf`); cross-referenced
against Ono & Trebat-Leder *The 1729 K3 Surface* (arXiv:1510.00735, 2016)
and Agarwal-Garg arXiv:2309.00427.
**Status:** Hunt 1 verdict reached at high confidence — but with a
**substantial scope correction** to the HUNT_MAP §1 framing.

## Setup

Per [HUNT_MAP §1](../insights/HUNT_MAP.md#hunt-1--lost-notebook-pp-341-343-the-1729-manipulations),
the prediction (training-data confidence: moderate per Ono's 2016 speculation)
was that **60-80% of the parameterised identities on LN pp. 341-343 should
trace out K3 surfaces** (extending Ono's Theorem 1.3 from the single Picard-18
K3 he identified on p. 341 to a small family of K3 / Calabi-Yau surfaces
covering the rest of the cube-identity continuation).

Inputs available locally:
- `priority_sources/lost_notebook_pages_341_343/page-{341,342,343}.jpg`
  (the user-curated "1729 page" bundle; **see filename-numbering correction
  below**)
- `priority_sources/open_access_context_pdfs/ono_trebat_leder_1729_k3_surface_arxiv_1510.00735.pdf`
- `priority_sources/open_access_context_pdfs/agarwal_garg_ramanujan_taxicab_identity_arxiv_2309.00427.pdf`
- the full 379-page facsimile image set under
  `primary_originals/page_images/lost_notebook/`

What is **not** available: Andrews-Berndt *Ramanujan's Lost Notebook Part IV*
(Springer 2013), which is the canonical scholarly commentary on these pages.
The published commentary is what would resolve the few "what is this exactly"
ambiguities the facsimile leaves.

## What I did

1. Inspected the user-curated `priority_sources/lost_notebook_pages_341_343/`
   bundle and discovered that **the filenames are off by one**:
   `page-N.jpg` corresponds to LN reprint p. `N+1`. The "famous 1729 page"
   that Ono reproduces in his Appendix as LN p. 341 is actually
   `page-340.jpg` (matched byte-for-byte against the main page_images
   directory). The user-pointed files page-341.jpg, page-342.jpg,
   page-343.jpg are actually LN reprint pp. 342, 343, 344.
2. Pre-processed the facsimile JPGs (flip top-to-bottom) so the
   handwriting is readable; viewed pp. 340-344 directly. Bottom-corner
   page numbers and Trinity-catalog `(81)`/`(82)`/`(83)` cross-checks
   confirm the off-by-one in filename indexing.
3. Compared `page-340.jpg` content (rational functions (i),(ii),(iii) with
   denominator `1 - 82x - 82x² + x³`, the master identity
   `a_n³ + b_n³ = c_n³ + (-1)^n`, the six numerical examples including
   135³+138³=172³-1, 9³+10³=12³+1, etc.) against Ono's Appendix image
   and Agarwal-Garg Theorem 1.1 — all match. This is the K3 page.
4. Read pp. 342, 343, 344 (the user's `page-341/342/343.jpg`) directly.
   **Found that none of these are cube-identity continuation pages.**
   Their content is summarised below in §"Numbers".
5. Built the inventory in [analysis/24_hunt1_k3_inventory.py](../analysis/24_hunt1_k3_inventory.py)
   with 48 identities across pages 340-344; tagged each with k3_status
   ∈ {K3_PARAMETERISATION_CONFIRMED, K3_CANDIDATE_PER_ONO, NOT_K3,
   UNKNOWN_FROM_FACSIMILE} and a confidence flag.
6. Wrote the CSV to [analysis/results/hunt1_k3_inventory.csv](../analysis/results/hunt1_k3_inventory.csv)
   and computed the HUNT_MAP §1 verdict.

Tagging is by *hand judgment from the facsimile*, calibrated against
typeset reproductions where they exist (the rational functions and 6
examples on p. 341 are in Agarwal-Garg's Theorem 1.1 essentially
verbatim). For p. 342 (Weber class invariants) I read the explicit
class-invariant labels `f₁(√-n)` and the discriminants `n = 20, 27, 26,
29, 35, 36, 38, 39, 41, 44, 50, 51, 52, 63, 87` directly off the
facsimile and matched them to known Weber-modular-function tables.
For p. 343 (Diophantine approximation) the explicit `θ = ⁵√2` and `θ
= ⁷√2` headers and the `O(…)` notation are unambiguous. For p. 344
(denesting) the explicit side conditions `η⁵ = 2` and `η⁵ = 3` are
readable; some of the polynomial-in-η right-hand sides have characters
I could not parse with full confidence (flagged as `confidence: low`
or `medium` in the CSV).

## Numbers

### Page-by-page K3 fraction (of *known*, i.e. excluding UNKNOWN_FROM_FACSIMILE)

| Page | What's there | n_total | n_unknown | n_known | n_K3 | K3 fraction (of known) |
|---|---|---|---|---|---|---|
| 340 | Quintic / 5th-power factorization (predecessor to 1729; "(x+a)⁵ - (x+b)⁵ = A(x+p)⁵ + …" plus a 2-variable 5th-power identity) | 5 | 0 | 5 | 0 | **0%** |
| **341** | **The famous 1729 page — three rational functions (i),(ii),(iii) over `1-82x-82x²+x³`; master identity `a_n³+b_n³ = c_n³+(-1)^n`; six numerical examples including 9³+10³=12³+1; plus one trailing continued-fraction identity below the horizontal rule** | 11 | 1 | 10 | 10 | **100%** |
| 342 | **Weber class invariants** — header self-corrections to notebook entries on pp. 378 and 500 (about `f(√-21)` and `f(√-41)`), then an explicitly-labelled "Weber's Results" table giving `f₁(√-n)` for `n ∈ {20,27,26,29,35,36,38,39,41,44,50,51,52,63,87}` with corresponding modular polynomials | 18 | 0 | 18 | 0 | **0%** |
| 343 | **Best Diophantine approximation** — two blocks: (a) `θ = ⁵√2` with two-multiplier `a^m b^n θ = p_{m,n} + ε_{m,n}` and explicit conjugate-product bound; (b) `θ = ⁷√2` with three-multiplier `a^ℓ b^m c^n θ = p_{ℓ,m,n} + ε_{ℓ,m,n}` and conjugate-product bound | 2 | 0 | 2 | 0 | **0%** |
| 344 | **Denesting / nested-radical identities** — eight `η^5=2` (or `η^5=3`) cases relating nested radicals to polynomials in η, then three multi-variable denesting identities in (a,b,c) | 12 | 0 | 12 | 0 | **0%** |

### HUNT_MAP §1 verdict (pp. 341-343, the targeted bundle)

| Metric | Value |
|---|---|
| n_total | 31 |
| n_unknown (UNKNOWN_FROM_FACSIMILE, excluded from fraction) | 1 |
| n_known | 30 |
| n_K3 (CONFIRMED or per-Ono candidates) | 10 |
| **K3 fraction (of known)** | **33.3%** |
| Prediction (60-80%) | **FALSIFIED** |

If we widen to pp. 341-344 (the user's `page-341.jpg` ... `page-343.jpg`
bundle plus the immediately following p. 344): K3 fraction is **10 / 42
= 23.8%**, also FALSIFIED. The K3 material is concentrated entirely on
p. 341 itself; pp. 342, 343, 344 are three distinct *non-cube*
mathematical topics that happen to live on the next three physical
pages of the Lost Notebook.

## Surprises

1. **The 60-80% K3 prediction is falsified at 33% — but the reason is
   topological, not arithmetic-geometric.** The K3 prediction
   presupposes that pp. 342-343 *continue the cube-identity material*
   from p. 341. They don't. The Lost Notebook is loose scrap paper
   compiled into a binding after Ramanujan's death; sequentially-
   numbered pages can be on entirely unrelated topics. pp. 342, 343,
   344 happen to be class invariants, Diophantine approximation, and
   denestings respectively — three distinct topics from three distinct
   research threads, none of which is cube-identity material at all.
   On the *cube material per se*, p. 341 is 100% K3 (10/10) and there
   simply isn't any more cube material in this neighbourhood of the
   facsimile.

2. **Ono's 2016 colloquium speculation about "near-counterexamples on
   pp. 342-343 parameterising different K3 / CY threefolds" appears
   not to refer to these facsimile pages.** I cannot rule out that
   Ono had access to a *different edition's* pagination (e.g. the
   2-volume Narosa reprint vs. Andrews-Berndt vol. IV's chapter pagination
   vs. the Trinity Add.Ms.a.94.13 folio-numbering) where pp. 342-343
   contains additional cube content. The Andrews-Berndt commentary in
   *Lost Notebook Part IV* would resolve this, but is not in the local
   corpus. **Recommended follow-up: obtain Andrews-Berndt Part IV
   chapter on "Approximations and asymptotic methods, including 1729"
   (the chapter heading the user's HUNT_MAP cites) and re-locate Ono's
   reference.**

3. **Hidden Hunt 4 / Hunt 1 overlap.** Page 342's "Weber's Results"
   table is precisely the kind of class-invariants material Hunt 4
   targets. Of the 15 class invariants on this page (`n = 20,27,26,29,
   35,36,38,39,41,44,50,51,52,63,87`), several discriminants
   (`-26, -38, -44, -50, -51, -52, -63, -87`) have class number ≥ 4
   and may be in the 18-invariants-still-unproved set Hunt 4 highlights.
   **Recommended follow-up: cross-check this list against Berndt-
   Chan-Kang-Zhang's table of class invariants reproved by 2000, and
   identify which (if any) of the 18 remaining unproven ones appear on
   this page.** This is a partial unblock of Hunt 4 from the Hunt 1
   work.

4. **Page 343's Diophantine-approximation work appears genuinely novel
   to me.** I am not aware of any modern paper that has analyzed
   Ramanujan's explicit `O(...)` bounds for `|a^m b^n ⁵√2 - p_{m,n}|`
   with the conjugate-product structure he gives. The expression is
   suspiciously close to a Mahler-measure / Lehmer-style bound, and
   the explicit "most unfavourable s ∈ {1,2,3,4}" picks out the worst
   conjugate. This is **a candidate for a new follow-up agent**: write
   a numerical verification that Ramanujan's bound is tight (or
   asymptotically tight) for some specific (m,n) and compare against
   the modern Thue-Siegel-Roth or Schmidt subspace bound. If it
   matches or improves modern bounds for explicit constants, it's a
   surprise and worth a dedicated diary entry.

5. **Page 344's denesting identities look like classical Ramanujan
   denesting (`∛(1/3) + ∛(5/3) = √[(∛5-1)/(2-∛5)] = …`), but at least
   one of the side conditions on the facsimile appears internally
   inconsistent** (e.g. `η = 3` annotated next to an identity using
   `η⁵ = 3` would force `3⁵ = 3`, contradiction). Either I am
   misreading the facsimile or Ramanujan made a transcription slip on
   his own scrap paper. Flagged in the CSV as `confidence: low/medium`
   for the affected rows. Berndt's commentary would resolve.

6. **A continued-fraction identity appears at the bottom of p. 341,
   below the horizontal rule that separates it from the cube-identity
   block** (identified as p. 341 identity #11 in the CSV). It involves
   the Binet form of a Fibonacci-like recurrence with parameter `a` and
   an explicit continued fraction. **This is not mentioned in Ono.**
   I tagged this as `UNKNOWN_FROM_FACSIMILE` because I cannot tell
   whether it is meant to be a cube-side identity (the `(-1)^n u²_{n+1}`
   factor under the square root is suggestive) or a separate unrelated
   entry that happens to be on the same physical page. **This is a
   candidate for a dedicated probe** — if this *is* a cube-related
   identity, it expands the cube-page material from 10 to 11
   identities (all still K3).

## Caveats

- **Page numbering is genuinely subtle.** The Lost Notebook circulated
  in multiple editions with different paginations: (a) the Sirinudi
  online facsimile (which the page-images here are extracted from),
  (b) the Narosa 1988 reprint, (c) the 5-volume Andrews-Berndt Springer
  series (where the relevant material is in Part IV ch. on
  "Approximations and asymptotic methods, including 1729"), (d) the
  Trinity Add.Ms.a.94.13 folio-numbering (visible as small circled
  `(81)`, `(82)`, `(83)` annotations on the facsimile). Ono cites
  "pg. 341 of his lost notebook" without qualifying which edition; the
  evidence is consistent with (a) and (b), but the speculation about
  "pp. 342-343" near-counterexamples *may* refer to a different
  pagination. This is what Andrews-Berndt Part IV would settle.
- **Hand judgment of the facsimile is not OCR.** I am reading
  Ramanujan's handwriting from images. Confidence is "high" only when
  the typeset version exists somewhere (Ono Appendix, Agarwal-Garg
  Theorem 1.1, standard class-invariant tables for the Weber values).
  For the more idiosyncratic identities on p. 344 (the multi-variable
  denestings) the confidence is "medium" or "low" because I cannot
  resolve every superscript-exponent unambiguously. **The CSV's
  `confidence` column is the audit trail.**
- **The "10/10 = 100% K3" claim for p. 341 is conservative-by-double-
  counting.** I count each of the three rational functions, the
  master identity, and each of the six numerical examples as separate
  "identities". They all parameterise the same K3 surface (Ono
  Theorem 1.3, Picard 18). If one prefers to count "distinct K3
  surfaces" rather than "distinct identities", p. 341 contributes
  exactly *one* K3, not ten. Either counting convention makes the
  60-80% prediction falsified (1/1 = 100% is in the prediction
  range, but the n_total denominator collapses to 1).

## Bottom line

**The HUNT_MAP §1 prediction (60-80% K3 parameterisation across pp.
341-343) is FALSIFIED at 33.3% K3 coverage on the inventoried
identities — but the reason is structural: pp. 342 and 343 of the
facsimile are not cube-identity continuation. They are entirely
different mathematical topics (Weber class invariants on p. 342;
best Diophantine approximations to ⁵√2 and ⁷√2 on p. 343). The K3
material is fully concentrated on p. 341, where it is 100% (10/10
identities, or equivalently 1 K3 surface).**

The headline finding is *not* "Ono's speculation was wrong about K3
density"; it is *"the LN pp. 342-343 corpus that Ono's speculation
needed is not on those pages of the facsimile under any reasonable
interpretation of his prediction."* Either:
- (a) Ono's speculation refers to a different edition's pagination,
  in which case the K3 inventory work waits on resolving that
  pagination ambiguity (Andrews-Berndt Part IV), OR
- (b) Ono's speculation was about *implicit* near-counterexamples
  hidden in the *cube-identity machinery itself* (different
  parameter slices of the same Pic-18 K3), in which case the work
  is closer to "compute the K3 mod-p L-function and look for cubic
  twists" — a completely different kind of follow-up than scanning
  more handwritten pages.

**Confidence**: high on the inventory itself (the cube material on
p. 341 is well-attested by Ono+Agarwal-Garg; the class-invariant /
Diophantine-approx / denesting content on pp. 342-344 is
unambiguously NOT cube material); medium on the verdict's *meaning*
(the pagination ambiguity is real).

**Status**: Hunt 1 closed for the literal HUNT_MAP §1 prediction
(falsified). Hunt 1 *spawns three new sub-leads*:
- 1a. Resolve the pagination ambiguity (Andrews-Berndt Part IV
  chapter on "Approximations and asymptotic methods, including
  1729" needed).
- 1b. Cross-check p. 342 class invariants against Berndt-Chan-Kang-
  Zhang to identify any of the 18 unresolved ones (partial Hunt 4
  unblock).
- 1c. Investigate p. 343 Diophantine-approximation bounds for
  novelty against modern Thue-Siegel-Roth / Schmidt-subspace
  literature.

## Follow-up leads (in priority order)

1. **Get Andrews-Berndt *Lost Notebook Part IV* chapter on
   "Approximations and asymptotic methods, including 1729"** and
   locate Ono's specific reference to "pp. 342-343". This is the
   single artefact that would resolve whether the K3 hunt is
   genuinely falsified or is on the wrong pages of the wrong
   edition. The chapter likely also identifies what Ramanujan's
   continued-fraction identity at the bottom of p. 341 (CSV row 11)
   is meant to compute.
2. **Cross-check the 15 class invariants on p. 342 against the
   modern Berndt-Chan-Kang-Zhang reproof table.** Of the 116 class
   invariants Ramanujan tabulated and the ~18 still unproven, how
   many appear on this page? Each unresolved invariant here is
   *both* a Hunt 1 deliverable (this diary) *and* a Hunt 4
   deliverable. The discriminants `-87` (class number ≥ 6 over `Q`)
   and `-63` (class number 4) are particularly suspect.
3. **Numerically verify Ramanujan's `O(...)` bound on p. 343 for
   ⁵√2 and ⁷√2.** For specific (m,n) compute `a^m b^n ⁵√2 -
   p_{m,n}` to high precision (mpmath, ~100 digits) and check
   whether the conjugate-product bound is tight, approximately
   tight, or loose. If tight, this is potentially a new diary
   entry on its own — Ramanujan anticipating effective Thue-Siegel-
   Roth bounds 25 years before Schneider-Mahler.
4. **Inventory Ramanujan's continued-fraction identity at the bottom
   of p. 341 (CSV row p341.11).** If it *is* a cube-side identity
   (the `(-1)^n u²_{n+1}` factor is suggestive), it would expand the
   K3-side parameterisation. If it is unrelated, it's a separate
   nice-CF entry for the recognizer's CF registry.
5. **Decide what to do about the user's `priority_sources/lost_
   notebook_pages_341_343/` filename mislabel.** Two options:
   (a) rename the files to `page-340-342.jpg` etc. with the correct
   LN page numbers, or (b) leave the filenames alone and add a
   README noting the off-by-one. Either is fine; the README
   already in that directory does NOT flag the off-by-one and
   should be updated. (Not a research follow-up; just bookkeeping.)
