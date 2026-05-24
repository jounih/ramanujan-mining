# Hunt 5b — Notebooks operator tagging — predictions before testing

Per the discipline lesson from Hunt 5 (predicted basis was wrong; would have
been over-credited as "confirmed" if we'd been loose about what counts as a
hit), this file records the **sharpened predictions for Hunt 5b before any
Notebooks chapter is opened.** Lock them down now so the test is honest.

## Top-level hypothesis being tested

**The toolkit-split hypothesis** (sharpened after Hunt 5 closure, see
[BIG_IDEAS_REVIEW §2a](BIG_IDEAS_REVIEW.md)):

> Ramanujan carried at least two distinct compressed operator toolkits and
> deployed them by problem-domain. The QRs use the *analytic / operator-
> calculus* toolkit (Mellin + Master + Frullani + Fourier-reciprocity +
> fractional iteration + Hardy orders + Mellin-pair). The Notebooks use a
> *different* toolkit per chapter — modular machinery in the chapters on
> theta functions, modular equations, class invariants, eta function — with
> hard separation between domain-specific toolkits.

If true, this is substantively stronger than the original
latent-space-speedrun framing: not "a small basis" but "a *structured* basis
with a problem-type → operator-subset routing function." A concrete claim
about Ramanujan's mental representation, not a folk theorem.

## Per-chapter operator-distribution predictions

Predictions are stated as *per-chapter operator-fraction floors and ceilings*.
The chapter is the unit because Berndt's chapter boundaries follow Ramanujan's
own chapter boundaries.

### NB II Ch. 16 (theta functions)

| Operator | Predicted | Notes |
|---|---|---|
| `modular_S_transform` | **≥60%** | Theta inversion is the chapter's primary move |
| `q_shift` | **≥30%** | q-Pochhammer machinery should be ubiquitous |
| `eisenstein_normal_ordering` | low (~10-20%) | Some Eisenstein-style normalisation moves |
| `class_field_galois_average` | low (≤10%) | Not the chapter's subject |
| `master_theorem` | **≤10%** | Wrong tool for q-products |
| `mellin_inversion` | **≤10%** | Wrong tool |
| `FRACTIONAL_FUNCTIONAL_ITERATION` | **~0%** | Different mathematical universe |
| `HARDY_ORDERS_OF_INFINITY` | **~0%** | Different mathematical universe |
| `FOURIER_SELF_RECIPROCITY` | low (~10%) | Some Jacobi-theta-as-Fourier-self-reciprocity moves possible |

### NB II Ch. 17 (modular equations)

| Operator | Predicted | Notes |
|---|---|---|
| `modular_S_transform` | **≥50%** | Modular equations relate τ → -1/τ behaviour |
| `class_field_galois_average` | **≥30%** | Galois-conjugacy of modular polynomial roots |
| `q_shift` | moderate (~25%) | q-Pochhammer manipulations |
| `eisenstein_normal_ordering` | low (~10%) | Some Eisenstein-as-bilinear-form moves |
| `master_theorem` | **≤5%** | Almost zero |
| All QR III operators | **~0%** | Different universe |

### NB II Ch. 18-19 (class invariants Gₙ)

| Operator | Predicted | Notes |
|---|---|---|
| `class_field_galois_average` | **≥60%** | The chapter's primary move |
| `modular_S_transform` | **≥30%** | Singular moduli are CM-points of the j-function |
| `q_shift` | low (~15%) | Some q-Pochhammer at the singular-modulus level |
| `eisenstein_normal_ordering` | low (~10%) | |
| `master_theorem` | **≤5%** | |
| All QR III operators | **~0%** | |

### NB II Ch. 32 (Eisenstein-style continued fractions) — high-priority per HUNT_MAP §3

| Operator | Predicted | Notes |
|---|---|---|
| `eisenstein_normal_ordering` | **≥40%** | The chapter's namesake |
| `modular_S_transform` | **≥30%** | CFs of Eisenstein series carry weight-2 anomaly |
| `q_shift` | **≥30%** | q-Pochhammer machinery in CF expansions |
| `class_field_galois_average` | moderate (~20%) | Some CM-point evaluations |
| `master_theorem` | **≤10%** | |
| `mellin_inversion` | **≤10%** | |
| All QR III operators | **~0%** | |

## Inter-chapter variance prediction (the stronger claim)

The toolkit-split hypothesis is *strongly* supported if the per-chapter
operator distributions look structurally different (Ch. 16 is theta-heavy,
Ch. 17 is modular-eqn-heavy, Ch. 18-19 is class-invariant-heavy, Ch. 32 is
Eisenstein-CF-heavy), with each chapter showing a small number of operators
dominating ~70-90% of that chapter's identities and a long tail of others
near zero.

The hypothesis is *weakly* supported if the distributions are similar across
chapters (every chapter uses a broad mix; no chapter has a clear dominant
operator).

The hypothesis is *falsified* if the distributions look like the QRs
(Mellin/Master dominate everywhere; modular machinery low across the board).

## Methodological commitments (per Hunt 5 lessons)

1. **Pick a spanning sample, not a single chapter.** Test Hunt 5b on at least
   3-4 chapters (e.g., NB II Ch. 16 + Ch. 17 + Ch. 18 + Ch. 32) to avoid
   over-fitting to one chapter's idiosyncrasies. ChatGPT-Pro pack has all 4
   Notebooks PDFs.

2. **Hand-tag, not regex.** Same discipline as Hunt 5 (see diary 20). The
   schema's regex tests would systematically under-fire on facsimile-OCR'd
   text the way they would have on the QR text.

3. **Section-level granularity, using Ramanujan's own boundaries.** Same
   discipline as Hunt 5. Don't impose granularity.

4. **Strict "near match ≠ match" discipline.** A section that looks like it
   *might* use modular_S_transform but doesn't actually invoke τ → -1/τ
   anywhere is NOT a hit. Hunt 5's near-match notes (e.g., "q-Pochhammer-
   shaped product → tagged Master Theorem, not q-shift, because the operator
   move is Master") are the template.

5. **Discipline split on confidence:**
   - The toolkit-split hypothesis is *strongly supported* only if multiple
     chapters show the predicted operator-dominance pattern, with the
     dominant operators differing across chapters.
   - A single chapter matching its predictions is "consistent with" the
     hypothesis but not "confirms" it.
   - Inter-rater reliability is not testable in a single-pass run — flag the
     hand-tagging as one-pass and ±5-8% on the per-operator percentages.

6. **OCR dependency.** Notebook pages are handwritten facsimiles. If Chandra
   OCR (per task H4 in todo.md) doesn't work well enough, fall back to
   careful image-by-image reading of the relevant Ramanujan-numbered
   sections. The latter is slower but possible since each chapter is bounded.

## When to call the hypothesis "established" vs "open"

- **Established** if Hunt 5b shows the predicted operator-dominance pattern
  in ≥3 chapters with at least 2 different dominant operators across them
  (so we know it's not just "every chapter is modular_S-dominated").
- **Partially supported** if 1-2 chapters show the pattern but others are
  ambiguous.
- **Falsified** if all surveyed chapters look like a uniform mix or are
  Mellin/Master-dominated like the QRs.

## Cross-references

- [diary/20_hunt5_qr_operator_tagging.md](../diary/20_hunt5_qr_operator_tagging.md) — Hunt 5 closure
- [diary/22_hunt5b_nb_v_ch32_tagging.md](../diary/22_hunt5b_nb_v_ch32_tagging.md) — Hunt 5b Ch. 32 first chapter (see addendum below)
- [BIG_IDEAS_REVIEW §2a, §2b, §4](BIG_IDEAS_REVIEW.md) — sharpened framings
- [HUNT_MAP.md](HUNT_MAP.md) — original predictions
- [todo.md H2](../todo.md) — Hunt 5b is unblocked

---

## Ch. 32 result (2026-05-24, see diary 22)

Pre-registered predictions for Ch. 32 (above) are NOT modified — this section
records the *outcome* of the first Hunt 5b chapter pass.

**Verdict: SUPPORTED** (per the rubric: ≥3 of 4 predicted-dominant operators
hit floor; ≥3 of 4 predicted-rare operators under ceiling), with one genuine
prediction miss (`eisenstein_normal_ordering`).

| Operator | Predicted (Ch. 32) | Actual (24 entries) | Hit? |
|---|---|---|---|
| `eisenstein_normal_ordering` | ≥40% | **8.3%** | **MISS** (only Family D + E10 proof-chain) |
| `modular_S_transform` | ≥30% | **91.7%** | hit (×3 floor) |
| `q_shift` | ≥30% | **100.0%** | hit (×3 floor) |
| `class_field_galois_average` | ~20% | **33.3%** | hit (above bracket) |
| `master_theorem` | ≤10% | 0.0% | under |
| `mellin_inversion` | ≤10% | 0.0% | under |
| All QR III operators | ~0% | 0.0% | under |

**Headline:** Ch. 32 has zero overlap with the QR operator toolkit. The
chapter's dominant pair is `q_shift + modular_S_transform` (100%, 91.7%);
the QR's dominant operators (`master_theorem`, `FRACTIONAL_FUNCTIONAL_ITERATION`,
`FOURIER_SELF_RECIPROCITY`) all fire 0% in Ch. 32. The toolkit-split
hypothesis is **supported on this chapter**.

**Reason for the `eisenstein_normal_ordering` miss:** the chapter name is
misleading — per [T2_EISENSTEIN_CF_SCOPING §"TL;DR"](T2_EISENSTEIN_CF_SCOPING.md),
only **1-2 entries** in Ch. 32 are genuinely Eisenstein (Family D cubic-base
CF). The other ~22 entries are theta-quotient CFs at small levels N=2,3,4,5,8
— modular machinery (Jacobi triple product, η-quotients, modular equations)
not Eisenstein series. T2's scoping doc explicitly flagged this risk; the
HUNT5b prediction did not propagate the flag to its `eisenstein_normal_ordering`
floor. The corrected per-Ch. 32 prediction for any re-run should be
`eisenstein_normal_ordering` ≤15% (firing only on E10 + E32-cubic).

**Per-family distribution (T2 clustering A/B/C-ambig/C/D)** — see diary 22
for the table. Family B (R(q) special values) is the only family where
`class_field_galois_average` is dominant (4/4 = 100%), validating T2's
"separate sub-route, not a CF family" call. Family C (Andrews-Gordon-Selberg
bulk, 6 entries) fires `q_shift + modular_S` at 100% each but 0%
`class_field_galois_average` — pure q-product identities at fixed q.

**What's still needed to call the toolkit-split hypothesis "Established":**
≥3 chapters with different dominant operators across them. The most-informative
single next chapter is **NB V Ch. 34** (class invariants and singular moduli,
pp. 183-321 in the same volume, no extra commentary needed). Then either Ch. 16
(theta functions), Ch. 17 (modular equations), or Ch. 36 (modular equations
+ theta-function identities, also in this volume) for a third.

**Ambiguous-rate:** ~17% (4 near-match decisions in 24 entries), in line
with diary 20's QR tagging (~12%). All four near-matches sit at the
`class_field_galois_average` boundary; including them all would shift the
operator to 50% (still in the "moderate" predicted range, just at the
upper end).

**Confidence:** medium-high on the Ch. 32 SUPPORTED verdict; medium on
the broader hypothesis (one chapter, replication needed). The
`eisenstein_normal_ordering` miss is the genuine prediction failure and
is honest.
