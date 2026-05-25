# Verification Pending — claims awaiting subagent verdicts

**Status:** 2026-05-25, after user's "verification is key" pivot. Three
adversarial subagents in-flight. This file tracks every unverified
ChatGPT-Pro claim that could land in a paper, plus what would refute each
one, plus pre-drafted confirmation/retraction language so updates are fast
when the subagents return.

## Decision rule

For each claim:
- **CONFIRMED + NOVEL** → keep in the paper as "verified result"
- **CONFIRMED + KNOWN** → reframe as "verified implementation" / "new
  packaging", not "novel finding"
- **REFUTED** → retract in diary + `DID_NOT_PAN_OUT.md` + paper draft
- **PARTIAL** → split into the part that survives + the part that doesn't

## Claims pending

### C1 — AB Entry 4.2.3 defense (diary 56 Result 1)

**ChatGPT-Pro claim:** Andrews-Berndt *Lost Notebook Part IV* §4.4
(p. 116) flags Ramanujan's Entry 4.2.3 (formula 4.2.5) as incorrect by
asymptotic argument. ChatGPT verifies LHS = RHS to 200 digits at the test
point AB chose (a=10, λ=1/2, ε=1) and gives a contour proof showing AB's
commentary erred — the formula is actually true.

**Local-grep evidence (2026-05-25):** AB §4.4 *literally exists* (corpus
hit `Ramanujan_39_s_Lost_Notebook_Part_IV_2013.txt` L7309). AB themselves
note small-a numerical agreement to 30+ digits (L7337). AB's asymptotic
divergence claim invokes Watson's Lemma + a Ramanujan Entry 10 of Ch. 3 to
derive LHS ~ e^a (1 - 3/(8a) + ...) — which is the part ChatGPT challenges.

**Subagent:** #66 (`a523969af20acdada`). Independent 300-dps verification
across 7 orders × 5 λ × 6 ε; reconstruct AB's argument; independent
contour proof; arxiv literature search.

**Refutation bar:** any (a, λ, ε) cell with rel-err > 10⁻²⁹⁰ that
*genuinely* fails (not at the noise floor of 300-dps) → REFUTE. If AB's
3/(8a) asymptotic is actually correct (and ChatGPT's contour proof has a
sign/branch error), then the cells we tested were too small-a to see
divergence → PARTIAL (formula is wrong but not in our checked range).

**If CONFIRMED.** Draft paragraph:
> Subagent (#66) independently verifies Entry 4.2.3 across (a, λ, ε)
> cells spanning [10⁻², 10⁵] × {λ ∈ ...} × {ε ∈ ...} at mpmath dps=300.
> Worst observed rel-err: [N.NN × 10⁻²⁹X]. Independent contour
> derivation produces ChatGPT's RHS without invoking the AB Ch.3 Entry 10
> step that injects the spurious 3/(8a) asymptotic. AB's §4.4 argument
> erred at the Watson-Lemma application of Ramanujan's Entry 10
> Chapter 3, not at Ramanujan's original formula. Corrigendum draft is
> publishable as a short note to Ramanujan Journal.

**If REFUTED.** Draft retraction:
> The claim in diary 56 §Result 1 that AB *Lost Notebook Part IV* §4.4 is
> in error and Ramanujan's Entry 4.2.3 is valid is **withdrawn**.
> Subagent (#66) found [SPECIFIC FAILURE]. The numerical agreement
> ChatGPT-Pro reported at a=10, λ=1/2, ε=1 was [misleading because ... /
> at the wrong precision / etc.]. AB's asymptotic argument stands. No
> corrigendum to AB Part IV is warranted.

**Confidence going in (my estimate):** ~70% the claim survives (AB's
small-a numerical agreement + the e^a · erf(√a) identity for λ=1/2 are
algebraically sound). ~25% partial (formula valid in some range, fails
elsewhere). ~5% fully refuted.

### C2 — Level-pq infinite family (diary 55 Result 1)

**ChatGPT-Pro claim:** For every squarefree N=pq with q > p, the unique
non-trivial 4-divisor Lambert/E_2 annihilator has coefficients
(c_1, c_p, c_q, c_{pq}) = (-δ, m, -m, δ) where g=gcd(pq-1, q-p),
δ=(q-p)/g, m=(pq-1)/g. 7 new instances verified at dps=120.

**Local-grep evidence (2026-05-25):**
- "Lambert" + "annihilator" = 0/14 file matches in our corpus.
- "Eisenstein" appears in 8 files (broad context but not this construction).
- "level 33" specifically: 0 matches.
- "Lambert series" appears in 4 files (KSR + AB LN I, II, III).
- AB LN III §10.75 (line 22701-22735) has *adjacent* material — Lambert
  series expressions for ϕ²(q)·ϕ²(q²) at levels that are powers of 2
  (10.75.409), and 18.2.9-18.2.11 of Chapter 18 of Berndt's NB Part [?]
  has Lambert-series formulas from Ramanujan's lost notebook fragments.
- **Berndt 1999** *"Fragments by Ramanujan on Lambert series"* in
  Kanemitsu-Győry Number Theory and Its Applications (Kluwer) is the
  highest-risk overlap candidate — exactly the kind of Lambert-series
  paper where a divisor-annihilator pattern might have been published.
  Subagent #67 should specifically check this. (Cited as [59] in AB LN
  III bibliography line 23453.)
- **S.H. Chan thesis (2005)** "On Cranks of Partitions, Generalized
  Lambert Series, and Basic Hypergeometric Series" — another high-risk
  overlap. Subagent should check.

**Patterns NOT in our corpus (supports novelty):**
- "L(q^d)" sum patterns explicitly: 0 hits
- "P_1 - n·P_n" Ramanujan-style annihilator language: 0 hits
- "level 33" / "level pq" explicit: 0 hits

**This is the strongest novelty signal we have so far** — the
*language* of the construction (Lambert annihilator, level-pq with
explicit (-δ, m, -m, δ) coefficients) does not appear in the standard
Andrews-Berndt + Berndt corpus. The risk is in the Berndt 1999 +
S.H. Chan 2005 work that is cited but not in our local PDFs.

**Subagent:** #67 (`a1162a324b4618a72`). All 7 levels at dps=200, 5
cells each, edge cases (twin primes, far-apart, p=2), 3-prime
squarefree + prime power extensions, arxiv WebFetch.

**Refutation bar:** any single (level, cell) failure at dps=200 → REFUTE.
If the formula extends but to a different structural class than claimed
(e.g., 3-prime gives 5-divisor annihilator without ChatGPT's specific
parameterization) → PARTIAL with the extension restricted.

**If CONFIRMED:** This is the headline finding. Paper draft positioning
shifts from "first novel identity" to "infinite family with closed-form
coefficients." Venue: Trans. AMS or Math. Comp. (number theory).

**If CONFIRMED + KNOWN (someone else published it):** Cited in
`DID_NOT_PAN_OUT.md` as "novel-to-us but discovered earlier by [X]."
Still a useful verification of an existing result; not paper material.

**If REFUTED:** Draft retraction:
> The Level-pq infinite family claim from diary 55 is **withdrawn**.
> Subagent (#67) found the closed-form coefficients (-δ, m, -m, δ) with
> δ=(q-p)/g, m=(pq-1)/g fail at level [N=pq]. The Level-33 instance
> (verified by subagent c at commit ba13b38) remains a genuine
> single-result; the generalization to all squarefree N=pq does not
> hold without additional constraints [SPECIFIC].

**Confidence going in:** ~85% the family survives at the 7 ChatGPT-tested
levels. ~10% partial (some levels fail). ~5% the closed-form
coefficients are wrong but the family exists with different
coefficients.

### C3 — Finite-pole attention closed form (diary 50) — VERDICT 2026-05-25

**ChatGPT-Pro claim:** ~8192× speedup at N=65536, R=8 vs standard
softmax attention via semiseparable representation when the attention
kernel has finite pole count R.

**Subagent verdict (diary 59):** **CONFIRMED (correctness); PARTIAL
(speedup magnitude).** Implementation in `rkc/attention/finite_pole.py`
exact to machine epsilon (3e-15 at N=256, 1e-14 at N=4096). Speedup
measured: 50× at N=4096, R=8, d_v=64 (NOT the 8192× projected at
N=65536). The asymptotic O(N) vs O(N²) scaling is clean and verified
(speedup doubles when N doubles: 2.7× → 6.6× → 14.9× → 28.5× → 50×).
The 50× vs 512× gap at N=4096 is constant-factor (numpy BLAS matmul in
the direct reference is highly tuned; the recurrence is a Python loop).

**Net call:** Math correct. Claim of "~N/R speedup ~8192× at N=65536"
is OVERSTATED for double-precision numpy baselines but TRUE for the
asymptotic scaling. For a paper: claim O(N) vs O(N²) scaling + the
measured 50× at N=4096; the asymptotic 512× would manifest at larger
N or against a slower direct baseline.

**Novelty:** linear-attention literature (Performers, Linformer, etc.)
covers semiseparable kernels broadly; the specific finite-pole
construction may be a special case. Not yet audited against literature.

**Next steps:** extend to complex poles (RoPE) per diary 50 footnote.

### C4 — Annular Poisson Green modular acceleration (diary 51) — VERDICT 2026-05-25

**ChatGPT-Pro claim:** ~7.1×10⁴× speedup at L=0.05 (thin annulus) for
the modular θ₁-quotient Green-function representation vs the standard
mode-expansion.

**Subagent verdict (diary 59):** **CONFIRMED.** Implementation in
`rkc/pde/annular_green.py` (mpmath dps=80). At L=0.05: 46.4 digits of
agreement with M=100,000-mode Fourier baseline (vs diary 51's claimed
4.03×10⁻⁴⁷ = 46.4 digits — exact match). Wall-clock speedup at L=0.05:
**74,917×** (modular: 53 µs vs Fourier: 4.0 s), almost exactly the
diary's 7.1×10⁴ claim.

**Edge case identified:** at L≥0.5 ("thick" annulus), one-image
truncation degrades accuracy to 3.8 digits. The accelerator is valid
in the L<<1 thin-annulus regime, as diary claimed.

**Net call:** Both correctness AND speedup magnitude verified to high
precision. This is the cleanest of the 4 accelerators.

**Novelty:** Theta-quotient Green functions for annular domains have
precedent in spectral theory (Borwein-Bailey-ish). Whether the
one-image closed-form expression at the thin-annulus limit has been
specifically published as a numerical-PDE primitive needs a
literature check.

**Next steps:** literature audit; potential J. Comp. Phys. or SIAM J.
Sci. Comput. note if novel as a primitive.

### C5 — PH Bessel-image propagator (diary 53) — VERDICT 2026-05-25

**ChatGPT-Pro claim:** For periodic 1D spring-mass PH chain at N=2048,
~95× speedup vs DFT-based 80-digit modal solution; much-larger speedup
vs symplectic Verlet.

**Subagent verdict (diary 59):** **CONFIRMED (correctness, energy
conservation, diary-cell exact match); PARTIAL (speedup magnitude vs
DFT depends on baseline choice).** Implementation in
`rkc/ph/bessel_image_propagator.py`. Diary 53's published cell
(N=2048, t=100, n=37) reproduces to 50 digits at dps=50. Energy drift
at machine eps (~10⁻¹⁶) across t ∈ {0.5, 1, 5, 10}.

**Speedup table:**
- Bessel-image: 40 µs per sparse query
- numpy.fft.ifft: 68 µs (so 1.7× speedup — NOT diary's 95×)
- Verlet integration: 230,744 µs (so 5,762× speedup)

**Net call:** Diary 53's headline "95× vs DFT" was vs an **mpmath-80dps
DFT** baseline (slow because mpmath is a Python interpreter). Against
numpy.fft.ifft in double precision, the speedup at N=2048 is only
1.7× (FFT constant factor wins at moderate N). Against Verlet (a
fair time-stepper baseline), the speedup is 5,762×. The asymptotic
O(1) per sparse query vs O(N log N) per FFT would manifest the
expected speedup at much larger N.

**Methodological lesson:** When reporting accelerator speedups, the
**baseline must be named explicitly**. "95× vs DFT" without specifying
"mpmath-dps DFT" or "numpy-FFT" is misleading.

**Novelty:** the q_n(t) = Σ J_{2(n+ℓN)}(2ct) propagator is in
Sullivan-Friesecke harmonic-chain literature. The packaging as a PH
simulation primitive with 30-digit truncation rule may be novel.

**Next steps:** re-run benchmark at N=10⁶ to confirm asymptotic
crossover where the closed-form beats numpy-FFT in double precision.

### C6 — Airy WKB Tricomi-U closed form (diary 56 Result 2) — VERDICT 2026-05-25

**ChatGPT-Pro claim:** 50-113× speedup vs Borel-Padé for Airy/Bessel
WKB prefactor evaluation, via recognizing the Borel transform as a
₂F₁(1/6, 5/6; 1; -s) hypergeometric function that admits a closed
Tricomi-U form.

**Subagent verdict (diary 59):** **CONFIRMED.** Implementation in
`rkc/special/airy_resurgent.py` (mpmath dps=70). Accuracy at every
x ∈ {5, 10, 20, 50, 100}: ≥ 70 digits (target was 30+ per diary 56).
Speedup vs Borel-Padé baseline: 21× to 328× across the x range
(diary's 50-113× is within this range).

**Edge cases:** Works at small x (50+ digits at x=0.1, where WKB
intuition breaks but the closed-form formula still holds) AND very
large x (68 digits at x=10,000). No observed failure mode in the
tested envelope.

**Caveat:** the subagent's Borel-Padé baseline only achieved 1-2
digits because it used straight real-axis quadrature rather than
sector-rotated contour. Diary 56 reported 38-digit Borel-Padé using
the tuned-contour variant. So the 21-328× speedup is "Tricomi vs
poorly-tuned Borel-Padé"; against a tuned Borel-Padé the speedup
should be in diary's 50-113× range exactly.

**Net call:** Core claim (Tricomi-U gives 70+ digits at every x in
~ms) is unambiguously confirmed. Speedup magnitude is favorable
across the diary's claimed range. As ChatGPT itself framed: "packaging
contribution, not new theorem" — the special-function math is
classical. This is "verified implementation of known math".

**Next steps:** re-tune Borel-Padé baseline using sector-rotated
contour to give a like-for-like 50-113× comparison.

## Adjacent claims NOT pending verification (already verified or already
calibrated)

| Claim | Diary | Status |
|---|---|---|
| Level-33 Lambert annihilator (single instance) | 47, 48 | VERIFIED (subagent c, dps=200, commit ba13b38) |
| Warnaar 1.7 + AB Entry 1.6.6 cost ratios | various | VERIFIED (subagent a) |
| ζ(5) Apéry-like depth-1 | 52 | CALIBRATED-HONEST (Koecher 1979 depth-2 already known) |
| XXX integrable chain g³ | 52 | CALIBRATED-HONEST (Lukyanov + fitted, not derived) |
| Kepler equation Padé-Lagrange | 54 | CALIBRATED-HONEST (Markley-style starter, not global closed form) |
| Two-branch §A8 obstruction principle | 49 | THEORETICAL (no numerical claim to verify) |
| Hunt 5b toolkit-split (4 chapters tagged) | 22, 24, 25, +1 | VERIFIED (200+ proof units, zero cross-firing) |
| Erdős template + machinery loading methodology | 56's CHATGPT_PRO_PROMPT_DESIGN_METHODOLOGY.md | DOCUMENTED (workflow contribution; orthogonal to specific math claims) |

## When the subagents return

For each subagent verdict:
1. Open the subagent's diary (57 / 58 / 59).
2. Find this file's matching section (C1 / C2 / C3-C6).
3. Fill in the actual verdict, replacing the `[BRACKETED]` placeholders.
4. Update the source diary (50 / 51 / 53 / 55 / 56) with a header note
   pointing to the verification verdict.
5. If REFUTED or PARTIAL: open `DID_NOT_PAN_OUT.md` and add an entry.
6. If CONFIRMED: open `CANDIDATE_INSIGHTS.md` and add an entry.
7. Update the paper draft (`papers/2026-05_project_c_first_results_short_note.md`)
   accordingly — fill in or remove the relevant section.
8. Commit + push.
