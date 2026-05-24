# Diary 20 — Hunt 5: Quarterly Reports operator tagging

**Date:** 2026-05-24
**Source:** Berndt, "Ramanujan's Quarterly Reports", Hardy-Ramanujan Journal **45**
(2022), 1-41 (faithful reproduction of Satagopan's 1925 handwritten copy of the
three original Quarterly Reports). Open-access at
[hrj.episciences.org](https://hrj.episciences.org/volume/view/id/727); local copy
at `chatgpt-pro-mining/ramanujan_claude_source_pack_v2/priority_sources/quarterly_reports/`
(directory gitignored; ~352 MB pack).
**Status:** Hunt 5 closed at high confidence — both prediction and correction.

## Setup

Per [HUNT_MAP §5](../insights/HUNT_MAP.md) and the schema at
[operator_tagging_schema.py](../corpora/transcriptions/operator_tagging_schema.py),
the latent-space-speedrun hypothesis predicted that **5-10 operators recur 80%+
of the time** across Ramanujan's QR manipulations, with a specific predicted
basis of 6 operators:

1. `mellin_inversion`
2. `master_theorem`
3. `q_shift`
4. `modular_S_transform`
5. `eisenstein_normal_ordering`
6. `class_field_galois_average`

Per the [Hunt 5 README](../corpora/transcriptions/quarterly_reports/README.md):
"The prediction is **confirmed** if ≥80% of labelled identities are flagged by
at least one of the six operators in the schema. If the prediction fails, the
failure modes themselves are informative." Both outcomes are publishable per
[insights/CANDIDATE_INSIGHTS.md §D](../insights/CANDIDATE_INSIGHTS.md).

## What I did

1. Read all 5,519 lines (~64 KB) of the Berndt 2022 HRJ text end to end.
2. Built a section-level index, one row per Ramanujan-numbered section, with
   line range, content summary, and operator tags from the 6-schema. Out-of-schema
   operators ("the empirical correction") tagged with a separate vocabulary.
   Output: [qr_section_index.json](../corpora/transcriptions/quarterly_reports/qr_section_index.json).
3. Wrote [analysis/23_hunt5_qr_operator_tagging.py](../analysis/23_hunt5_qr_operator_tagging.py)
   to load the index, tally, and write
   [analysis/results/qr_operator_tags.csv](../analysis/results/qr_operator_tags.csv) +
   [analysis/results/qr_hunt5_verdict.csv](../analysis/results/qr_hunt5_verdict.csv).

Tagging method is **hand-judgment, not regex**. Identifying the
*operator being applied* requires reading the move in context — the schema's
regex test in [operator_tagging_schema.py](../corpora/transcriptions/operator_tagging_schema.py)
is calibrated against textbook notation (`\\tau`, `D_q`, Bromwich contours)
and would systematically miss Ramanujan's archaic / unannotated notation (he
writes `Z ∞` for `∫₀^∞`, uses `n .` for `n!`, etc., and rarely names a theorem
he is invoking). I scored each section against the *substance* of the move, and
the score-vector for the predicted-basis schema is binary (1 if the section
uses the operator as its primary or secondary move, 0 otherwise).

I excluded `is_meta` sections (validity discussions, foundational interpolation
arguments) from the 80% denominator. These are sections *about* the
operators, not using them: e.g. QR I §3 ("When valid?") or QR III §1-§3 (the
uniqueness-of-`u_n` argument). 5 of 38 sections are meta; 33 are math-content.

## Numbers

### Per-report coverage by the 6-operator predicted basis

| Report | n_math | n_in_basis | % in basis | meets ≥80%? |
|---|---|---|---|---|
| QR1 (5 Aug 1913) | 13 | 13 | **100.0%** | YES |
| QR2 (7 Nov 1913) | 9  | 6  | **66.7%** | NO |
| QR3 (9 Mar 1914) | 11 | 0  | **0.0%**  | NO |
| **ALL** | 33 | 19 | **57.6%** | **NO** |

### Predicted-operator usage (across all math sections)

| Operator | n_sections |
|---|---|
| `master_theorem` | 19 |
| `mellin_inversion` | 17 |
| `q_shift` | 0 |
| `modular_S_transform` | 0 |
| `eisenstein_normal_ordering` | 0 |
| `class_field_galois_average` | 0 |

**4 of the 6 predicted operators never fire.** Vocabulary check on the raw
text (5519 lines): zero occurrences of `\tau`, `\theta`, `\eta`, "Bernoulli",
"Heegner", "Eisenstein", "modular", "class invariant", "elliptic", "Lambert",
"continued fraction". One occurrence of "Eulerian" (naming the gamma integral).

### Out-of-schema operators that fired (the empirical correction)

| Operator | n_sections | Where |
|---|---|---|
| `FOURIER_SELF_RECIPROCITY` | 5 | QR II §7 (Theorem III); QR III §13, §14, §15 |
| `FRACTIONAL_FUNCTIONAL_ITERATION` | 5 | QR III §4-§6, §8, §9, §10 |
| `HARDY_ORDERS_OF_INFINITY` | 3 | QR III §7, §8, §9 |
| `FRULLANI_LIMIT` | 2 | QR II §4 (Theorem II), §5 |
| `MULTISECTION_ROOTS_OF_UNITY` | 1 | QR II — the cubic-roots-of-unity factoring of `1 - x³/3! + x⁶/6! - …` (lines 2086-2280) |
| `RIEMANN_LIOUVILLE_FRACTIONAL_DIFF` | 1 | QR III §11 |
| `UMBRAL_OPERATOR_SUBSTITUTION` | 1 | QR III §12 |
| `PARTIAL_FRACTION_OF_INFINITE_PRODUCT` | 1 | QR III §13 |
| `BANDLIMITED_FOURIER_DISCONTINUITY` | 1 | QR III §14 |
| `MELLIN_PAIR_RECIPROCITY` | 1 | QR III §15 |

## Surprises

1. **The 80% prediction failed by ~23 percentage points** (57.6% vs ≥80%), but
   not in the way one might naïvely expect. **QR I confirmed it cleanly**
   (13/13 = 100%); the failure is entirely in QR II (Theorem III ≠ Mellin/Master)
   and QR III (an entirely different mathematical universe).

2. **Modular forms simply don't appear in the QRs.** Three of the six predicted
   operators (`modular_S_transform`, `eisenstein_normal_ordering`,
   `class_field_galois_average`) were predicted by HUNT_MAP §5 on the basis of
   "QR III demonstrates Ramanujan's modular toolkit." That prediction is
   falsified: there is no `\tau`, no `\theta`, no `\eta`, no `j(\tau)`, no
   class-invariant `G_n`, no Heegner orbit, no Eisenstein series, no Lambert /
   divisor sum, no continued fraction — anywhere in the 5519 lines. (The
   *Notebooks* are the place modular machinery lives; the QRs are not.)

3. **`q_shift` also doesn't fire**, despite the surface presence of an infinite
   product `(1+x)(1+ax)(1+a²x)···` in QR I §5(v). Ramanujan treats this as an
   ordinary Taylor series in `x` whose coefficients are products `1/∏(1-a^k)`,
   and reduces to the Master Theorem. He never invokes `(a;q)_n` notation, the
   `q`-binomial theorem, the `D_q` operator, or Heine's transformations. The
   move at QR I §5(v) is `master_theorem`, not `q_shift`. The infinite product
   *is* what would later be called a `q`-Pochhammer up to sign, but the
   *operator move* on it is purely Mellin-Master.

4. **QR III is a different mathematical universe from QR I and QR II.**
   - QR I: Master Theorem manifesto. One operator, ~10 worked applications.
   - QR II: Master-Theorem-with-extensions. Adds Frullani limit (Theorem II)
     and Fourier cos/sin self-reciprocity (Theorem III), plus a brief multisection.
   - QR III: **Foundations and operator calculus.** Discusses uniqueness of
     interpolation (§1-§3), defines fractional iteration of functions via
     Schröder/Koenig (§4-§6, §10), develops Hardy's orders of infinity (§7-§9),
     defines Riemann-Liouville fractional differentiation (§11), works with
     shift and difference operators umbrally (§12), partial-fraction-decomposes
     infinite products (§13), and proves Mellin-pair self-reciprocity theorems
     (§14, §15). **The Master Theorem appears in QR III only as a
     consistency check** on the operator calculus (§12), not as a primary move.

5. **The latent-space-speedrun hypothesis is supported by a small toolkit,
   just not the predicted one.** In total, 12 distinct operators appear across
   all three QRs (2 predicted + 10 out-of-schema). But within each report the
   active toolkit is much smaller: QR I uses essentially 2 (Mellin + Master),
   QR II uses ~4 (those + Frullani-limit + Fourier-reciprocity), QR III uses
   ~6-7 (Fourier-reciprocity + the QR III-specific cluster of fractional iteration
   / Hardy orders / operator calculus / partial fractions / Mellin-pair).

6. **The actual revised operator basis appears to be ~6-8 operators**, dropping
   the 3 modular-machinery operators and adding the 5 most-frequent
   out-of-schema operators:
   - **Kept**: `mellin_inversion`, `master_theorem`
   - **Dropped**: `q_shift`, `modular_S_transform`, `eisenstein_normal_ordering`, `class_field_galois_average`
   - **Added**: `FOURIER_SELF_RECIPROCITY`, `FRACTIONAL_FUNCTIONAL_ITERATION`,
     `HARDY_ORDERS_OF_INFINITY`, `FRULLANI_LIMIT`, `MELLIN_PAIR_RECIPROCITY`
   - This revised 7-operator basis covers **30 of 33 = 90.9%** of QR math
     sections (the 3 left out are QR II's multisection, QR III §11, §12, §13
     specialised moves; 3 of these would be covered by adding one or two more
     QR-III-specific operators).

## Caveats

- **The Berndt HRJ 2022 reproduction is a typeset, lightly-edited version of
  Satagopan's 1925 handwritten copy of originals that no longer exist.**
  Editorial substitutions are documented: Berndt replaced `n .` with `!` and
  `Π(x)` with `Γ(x+1)`. He also "occasionally inserted commas and periods"
  and re-formatted display math from in-line math. The substantive content is
  preserved per Berndt's testimony, but it is one OCR/transcription generation
  removed from Ramanujan's hand.
- **Section boundaries are Ramanujan's own.** Every section is numbered by
  Ramanujan (§1, §2, ...; (i), (ii), ...; (a), (b), ...). I did not impose
  granularity; I used what Ramanujan himself drew. This is the most faithful
  unit available without primary scans of the Satagopan copy.
- **Tagging is hand-judgment, not the schema's regex test.** The schema's
  `assess()` function would heavily under-fire on the actual text because
  Ramanujan rarely names operators (no "Mellin transform", no "modular
  S-transform"). The regex was a useful sanity check on textbook examples
  (self-tests pass at all 6 operators) but is not the right tool for tagging
  this corpus. The hand-judgment can be audited by reading the cited lines
  in the section index.

## Updates to the schema

Updating [operator_tagging_schema.py](../corpora/transcriptions/operator_tagging_schema.py):
- Set `verified_against_transcription = True` for `mellin_inversion` and
  `master_theorem` with a `notes` line citing QR I §2 (lines 158-308 in the
  HRJ text) for both.
- Leave `verified_against_transcription = False` for the four operators that
  did not fire in the QRs (`q_shift`, `modular_S_transform`,
  `eisenstein_normal_ordering`, `class_field_galois_average`), with a `notes`
  line for each pointing to this diary entry as the "did not fire in QR
  corpus" record. This does **not** mean these operators don't appear in
  Ramanujan's work in general — only that the QRs are not the venue. The
  Notebooks (Berndt's five-volume edition) and the Lost Notebook are where
  modular machinery should be tested next.

## Per-operator marginal coverage (added after parallel-Claude review)

The 91% "covered by any of 7" headline overstates the basis's flatness. The
honest per-operator marginal contribution to the cumulative coverage is:

| Add to basis | New sections covered | Cumulative | % |
|---|---|---|---|
| `master_theorem` | 19 | 19 | 57.6% |
| + `mellin_inversion` | 0 (subset of master) | 19 | 57.6% |
| + `FOURIER_SELF_RECIPROCITY` | 5 | 24 | 72.7% |
| + `FRACTIONAL_FUNCTIONAL_ITERATION` | 5 | 29 | 87.9% |
| + `HARDY_ORDERS_OF_INFINITY` | 1 | 30 | 90.9% |
| + `FRULLANI_LIMIT` | 0 (subset of master in QR II §4-5) | 30 | 90.9% |
| + `MELLIN_PAIR_RECIPROCITY` | 0 (subset of FOURIER in QR III §15) | 30 | 90.9% |

So the "7-operator basis" is really **3 dominant operators + 1 helper** that
do the actual coverage work:

- `master_theorem` (19 sections, dominant in QR I + QR II);
- `FOURIER_SELF_RECIPROCITY` (5 marginal, the QR II Theorem III + QR III §13-§15 thread);
- `FRACTIONAL_FUNCTIONAL_ITERATION` (5 marginal, the QR III §4-§10 Schröder/Koenig thread);
- `HARDY_ORDERS_OF_INFINITY` (1 marginal, QR III §7 standalone);

The other 3 in the 7-basis (`mellin_inversion`, `FRULLANI_LIMIT`,
`MELLIN_PAIR_RECIPROCITY`) are **structural subsets** — they always co-occur
with master_theorem or FOURIER_SELF_RECIPROCITY in this corpus and add no
marginal coverage. Useful as separate tags for *what kind of move* a section
makes, but not as separate basis elements for *coverage* counting.

This sharpens the latent-space-speedrun framing: not "7 equally-weighted
operators" but **"~3-4 dominant moves with domain-specific specialisations"**.

## Bottom line

The HUNT_MAP §5 prediction (≥80% recurrence of the specified 6-operator
basis) is **falsified at 57.6% coverage**, and the 6-operator basis was wrong
because it over-weighted modular machinery. The QRs are about
Mellin/Master-Theorem analysis (QR I + QR II) and functional / operator
calculus (QR III), not theta or eta functions. A revised 7-operator basis
(dropping the 4 modular operators, adding Fourier-self-reciprocity / Frullani-
limit / fractional-functional-iteration / Hardy-orders / Mellin-pair-reciprocity)
covers **~91%** of QR math sections — though as the per-operator marginal-
coverage table above shows, **the real basis is 3-4 dominant operators with
the rest as domain-specific specialisations / structural subsets**, not 7
equally-weighted elements.

**Confidence (split per parallel-Claude review):**
- **High** on the negative: the ≥80% prediction is decisively falsified
  (57.6% well below 80%; the gap is structural — 4 of 6 predicted operators
  never fire at all).
- **Medium-high** on the positive: the revised 3-4-dominant-operator basis
  is the natural empirical correction but is one-pass hand-tagging without
  inter-rater reliability check; ±5-8 points on the 57.6% headline is the
  honest uncertainty. The revised basis stands pending replication (Hunt 5b
  on Notebooks is the natural test of whether THIS basis holds beyond the
  QR corpus).

**Status**: Hunt 5 closed. The revised operator basis is the artefact. The
durable record is [qr_section_index.json](../corpora/transcriptions/quarterly_reports/qr_section_index.json),
[qr_operator_tags.csv](../analysis/results/qr_operator_tags.csv), and
[qr_hunt5_verdict.csv](../analysis/results/qr_hunt5_verdict.csv). The
analogous test on the *Notebooks* (where the modular machinery should
actually appear) is the natural follow-up — this would be Hunt 5b.

## Follow-up leads (in priority order)

1. **Hunt 5b: extend the operator-tagging exercise to the Notebooks.** Use the
   Berndt-edited five-volume series (Springer 1985-2005) as the source. The
   hypothesis to test there is the symmetric one: modular machinery should
   *dominate* the Notebooks (chapters on Eisenstein series, eta function,
   class invariants, theta function are all listed in Berndt's TOC). If so,
   the QR-vs-Notebooks contrast becomes the *real* finding — Ramanujan
   carried at least two distinct operator toolkits, deployed in
   different report-vs-personal contexts. Berndt Part V Ch. 32 is the
   priority section per [HUNT_MAP](../insights/HUNT_MAP.md) Hunt 3.
2. **Revise the schema basis in
   [operator_tagging_schema.py](../corpora/transcriptions/operator_tagging_schema.py)
   to incorporate the 5 added operators** and re-run the recognizer
   benchmark. Recognizer routing should not change (none of the
   recognizer-detected kernels is in the revised set), but having the
   QR-validated basis as the canonical 7-operator schema brings the
   schema into agreement with primary-source evidence.
3. **Cross-validate against the Berndt 1984 BLMS paper.** The HRJ 2022 paper
   is described as a "faithful reproduction" of the original Satagopan copy
   the BLMS paper was also based on. The BLMS paper is more compact and
   contains additional editorial commentary on what's "really new" vs
   "rederivation of known results"; that commentary should be merged into
   the section index as a `known_reference_status` field per
   [phase2_context/formula_record_schema.json](../chatgpt-pro-mining/ramanujan_claude_source_pack_v2/phase2_context/formula_record_schema.json).
4. **The fractional-iteration / Schröder thread of QR III §4-§10 deserves
   independent investigation.** Ramanujan computes explicit closed forms for
   `F^n(x)` where `F(x) = x²-2` (Chebyshev semigroup), `F(x) = x²+2x`,
   `F(x) = x²-2x`, `F(x) = x²+4x` — and the iteration of `x → (1-x)/(1-x²)`
   at fractional `r`. This is essentially what would now be called
   *holomorphic dynamics / iteration-theoretic linearisation* (Koenig 1884,
   Schröder 1871), and Ramanujan's `ψ_1(x) = C/F(x)` (QR III §10) is the
   infinitesimal-generator-of-flow formula. None of this is in the modern
   "Ramanujan in iteration theory" literature that I know of; worth a
   literature scan.
