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

### C3 — Finite-pole attention closed form (diary 50)

**ChatGPT-Pro claim:** ~8192× speedup at N=65536, R=8 vs standard
softmax attention via semiseparable representation when the attention
kernel has finite pole count R.

**Subagent:** #68 (`a7c6cab78eacccfea`) — implementation in
`rkc/attention/finite_pole.py`. Verify exactness at N=16, benchmark at
N=4096.

**Refutation bar:** if the actual speedup at N=4096 is < 0.5× claimed
(< ~4000×) OR exactness at N=16 fails to rel-err 10⁻¹⁰ → REFUTE.

**If CONFIRMED + KNOWN (already in attention literature):** The
semiseparable / finite-rank attention literature exists (Linear
Attention, Performers, Linformer, etc.). Need to verify whether the
specific finite-pole construction is novel or a special case of
existing methods. Probably "known structure, new application" framing.

**If CONFIRMED + NOVEL:** ML systems paper venue (NeurIPS systems track,
MLSys, or arxiv).

**If REFUTED:** Withdraw the claim from diary 50, document in
`DID_NOT_PAN_OUT.md` what specifically failed.

**Confidence going in:** ~60% the math is correct but the result is in
the broader linear-attention literature; ~30% genuinely novel; ~10%
fails to verify at claimed scale.

### C4 — Annular Poisson Green modular acceleration (diary 51)

**ChatGPT-Pro claim:** ~7.1×10⁴× speedup at L=0.05 (thin annulus) for
the modular θ₁-quotient Green-function representation vs the standard
mode-expansion (which is slow precisely because L→0 makes terms decay
slowly).

**Subagent:** #68. Implementation in `rkc/pde/annular_green.py` in
mpmath; verify > 40 digits at the L=0.05 cell.

**Refutation bar:** if rel-err > 10⁻³⁰ at the L=0.05 cell → REFUTE. If
speedup at L=0.05 is < 0.5× claimed → PARTIAL.

**If CONFIRMED + NOVEL:** PDE numerics paper venue (J. Comp. Phys. or
SIAM J. Sci. Comput.).

**If CONFIRMED + KNOWN:** Theta-quotient Green function for thin
annulus likely has antecedents in the spectral-theory literature
(Borwein-Bailey?); reframe as "first implementation" not "first
discovery."

**Confidence going in:** ~75% the math is correct (the modular S
transform is well-established for theta-functions); ~50% the specific
packaging is the first practical implementation at the L→0 thin
limit.

### C5 — PH Bessel-image propagator (diary 53)

**ChatGPT-Pro claim:** For periodic 1D spring-mass PH chain at N=2048,
~95× speedup vs DFT-based 80-digit modal solution; much-larger speedup
vs symplectic Verlet.

**Subagent:** #68. Implementation in `rkc/ph/bessel_image_propagator.py`
using scipy.special. Verify vs Verlet integrator.

**Refutation bar:** energy drift > 10⁻⁷⁰ at H(0)=1 over the t=100
interval (ChatGPT claimed 2.1×10⁻⁸¹) → REFUTE. Speedup < 0.5× claimed →
PARTIAL.

**If CONFIRMED + NOVEL:** PH systems community paper (Automatica or
similar; or arxiv announcement).

**If CONFIRMED + KNOWN:** Sullivan-Friesecke harmonic-chain literature
already has the q_n(t) = Σ J_{2(n+ℓN)}(2ct) solution. The packaging as
a "PH simulation primitive" with 30-digit truncation rule is what
might be novel; reframe accordingly.

**Confidence going in:** ~85% the math is correct (classical
Jacobi-Anger + Bessel recurrence); ~30% the packaging is novel
(literature has the solution, but not necessarily as a usable
primitive).

### C6 — Airy WKB Tricomi-U closed form (diary 56 Result 2)

**ChatGPT-Pro claim:** 50-113× speedup vs Borel-Padé for Airy/Bessel
WKB prefactor evaluation, via recognizing the Borel transform as a
₂F₁(1/6, 5/6; 1; -s) hypergeometric function that admits a closed
Tricomi-U form.

**Subagent:** #68. Implementation in `rkc/special/airy_resurgent.py` in
mpmath. Verify vs `mp.airyai` at x=5, 10, 20, 50, 100.

**Refutation bar:** rel-err > 10⁻⁶⁰ at any tested x (ChatGPT claimed
4.1×10⁻⁷¹ at x=20) → REFUTE. Speedup < 0.5× claimed → PARTIAL.

**If CONFIRMED + KNOWN:** ChatGPT explicitly framed this as "packaging
contribution, not new theorem" — the special-function identities are
classical. So this is borderline already; in confirm-mode, we'd publish
the implementation + benchmark, not the math.

**Confidence going in:** ~90% the math is correct (classical
hypergeometric ↔ Tricomi U); ~95% the packaging is useful but not
novel.

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
