# Pre-registration: Gauss *Disquisitiones Arithmeticae* + diary corpus tagging (Hunt 5b extension)

**Date locked:** 2026-05-25 (before any hand-tagging)
**Status:** PRE-REGISTERED. The hand-tagging experiment must be run by an
agent BLINDED to this document.

## Background

Hunt 5b's toolkit-split hypothesis (diary 25, established at high
confidence across 4 chapters of Berndt material): Ramanujan's working
style decomposes hierarchically — modular ⊥ analytic at top level;
bipartite RMT ⊥ Schröder-Koenig within analytic; per-domain operator
clusters within modular.

Open question: is this Ramanujan-specific, or a **universal pattern**
of mathematical cognition?

## The experiment

**Hand-tag a representative subset of Gauss's mathematical corpus**:
- *Disquisitiones Arithmeticae* (1801), focusing on Sections III (residues),
  IV (quadratic reciprocity), V (quadratic forms — the largest section),
  VI (applications), VII (cyclotomy)
- *Mathematisches Tagebuch* (1796-1814) diary, 146 entries, including the
  17-gon construction (entry 1), polygonal-number theorem, AGM/elliptic
  material, last entry connecting biquadratic residues with lemniscatic
  functions

Source PDFs to acquire:
- Disquisitiones (Clarke or Maser English translation; original Latin
  freely available)
- Mathematisches Tagebuch (Klein-Schlesinger 1903 facsimile + commentary;
  Gray's English translation 1984)

Tagging granularity: one "proof unit" per theorem / corollary / section
subentry, same as Hunt 5b chapters.

## Pre-registered prediction (ChatGPT Pro, cycle 11)

**Point prediction**: **8 distinct Level-1 operator clusters**.
**Calibrated band**: 7-9.

### The 8 predicted clusters (verbatim from ChatGPT)

| Cluster | Predicted operator family | Typical Gaussian move |
|---|---|---|
| **G1. Congruence normalization** | Reduce equality, divisibility, Diophantine conditions to residue classes | Replace problem by congruences mod m; normalize by gcds; invert units; pass to canonical residues |
| **G2. Cyclic/power-residue calculus** | Orders, primitive roots, exponents, residue powers | Turn multiplicative residue questions into exponent arithmetic |
| **G3. Reciprocity transport** | Quadratic and higher-residue symbol movement | Transfer solvability information between moduli; track parity/sign correction terms |
| **G4. Quadratic-form reduction** | Equivalence, reduced representatives, transformations | Replace a form by an equivalent simpler form under unimodular substitution |
| **G5. Class/genus algebra of forms** | Composition, duplication, genera, character partitions | Treat form-classes as algebraic objects; compose or project into genera |
| **G6. Cyclotomic-period decomposition** | Roots of unity, period sums, resolvent towers | Partition roots into periods; descend cyclotomic equations by subgroup chains |
| **G7. Finite algorithm / exclusion / computation** | Tables, search, exclusion, primality/factorization procedures | Convert proof objective into finite eliminative computation |
| **G8. Transcendental arithmetic lift** | AGM, elliptic/lemniscatic functions, modular bridges | Move arithmetic residue problem into analytic/elliptic parametrization and return with an invariant |

### Pre-registered dominant cluster pattern per problem-domain

| Problem-domain | Dominant cluster pattern |
|---|---|
| General congruences and first-degree congruences | G1 → G7 |
| Residues of powers / primitive roots | G1 → G2 → G7 |
| Quadratic residues and quadratic reciprocity | G1 → G2 → G3 |
| Binary and ternary quadratic forms (Section V — the heaviest block) | G1/G3 → G4 → G5 |
| Representation theorems (sums of squares, indeterminate quadratic eqns) | G4 → G5 → G7, with G3 as local-solvability filter |
| Applications: primality, factoring, solving explicit congruences | G7 over G1/G2/G4 |
| Cyclotomy and constructible polygons | G2 → G6, with G1 underneath |
| Secret-notebook AGM / elliptic / lemniscatic material | G8 ↔ G2/G3/G6 — the cross-toolkit bridge |

### Pre-registered falsification signals

1. **More than 12 clusters** → the per-cluster prediction was too coarse;
   the methodology might not transfer (or Gauss's idiom is more diverse
   than expected)
2. **Fewer than 5 clusters** → the methodology is over-clustering; the
   "small toolkit" finding becomes vacuous
3. **G8 (transcendental arithmetic lift) fires <5%** → ChatGPT's
   identification of the diary's analytic bridge layer is wrong, OR the
   bridge is rarer than the famous last-entry hyped
4. **Section V (quadratic forms) does NOT show G4 → G5 dominance** →
   structural understanding of Gauss's main contribution is wrong

### Pre-registered Hasse skeleton

```
G1 → {G2, G4, G7}
G2 → {G3, G6, G8}
G4 → G5
G3 → {G5, G8}
G6 → G8
G7 = terminal "extraction" ideal
```

ChatGPT's argument: Gauss's writing is "more architectonic" than
Ramanujan's, so the Hasse poset should have fewer "wild long-range jumps"
and more visible scaffolding. The private diary material is what
prevents the skeleton from being merely expository.

## What it would mean for the universality claim

If the prediction lands within the calibrated 7-9 band AND the dominant
clusters per problem-domain match → **the toolkit-split is a UNIVERSAL
pattern of mathematical cognition, not Ramanujan-specific**. Major
cog-sci result. The Level-1 incidence algebra construction (diary 38)
generalizes.

If the prediction misses badly → either Gauss had a fundamentally
different cognitive structure, or the methodology over-fits to
Ramanujan-style corpora.

## Methodology constraints (must be followed by the tagger)

1. **The tagging agent MUST NOT read this file** until tagging is
   complete.
2. Define a "Gauss operator basis" from the predicted 8 clusters but
   **be open to the actual data forcing a different basis** — same
   discipline as Hunt 5b NB1 Ch.3-4 surfacing `fractional_iteration`
   as co-dominant when the prediction said only supporting.
3. Tag in the same per-proof-unit style as Hunt 5b chapters.
4. Output: `analysis/30_hunt5b_gauss_disquisitiones_tagging.py` +
   `analysis/results/hunt5b_gauss_disquisitiones_tags.csv` + diary
   entry comparing to this pre-registration.

## Source acquisition pending

Need to acquire:
- Disquisitiones Arithmeticae (Clarke English translation,
  Yale UP 1966)
- Mathematisches Tagebuch (Gray 1984 English translation, Springer)

Both should be findable on archive.org or via library.

## Cross-link

After tagging:
- Reference this file in the resulting diary entry
- Update CANDIDATE_INSIGHTS §D1 with the Gauss confirmation
- Update BIG_IDEAS_REVIEW §2c (or new §4 cog-sci section) with the
  universality result
