# W8 — Paper Outline: "Pre-Julia Iteration Theory in Ramanujan's Third Quarterly Report (March 1914)"

**Status**: outline only; pending decision on whether to draft.
**Trigger condition**: written because [W8_PRE_JULIA_LIT_SCAN.md](W8_PRE_JULIA_LIT_SCAN.md)
returned verdict bucket GENUINELY_UNDER_NOTED at medium-high confidence
(~75%).

---

## Title (preferred)

**"Pre-Julia Iteration Theory in Ramanujan's Third Quarterly Report (March 1914)"**

Alternative working titles considered:
- "Ramanujan and the Schröder-Koenig Tradition: A Note on the Third Quarterly Report"
- "Fractional Iteration, the Chebyshev Semigroup, and Infinitesimal Generators in Ramanujan's March 1914 Quarterly Report"

The first title is preferred because it states the priority claim cleanly
(Julia is the modern field-founding date that everyone recognises; 1914 < 1918
is the load-bearing fact).

---

## Abstract (≈250 words, working draft)

> In March 1914, two weeks before sailing to Cambridge, Srinivasa Ramanujan
> submitted to the Board of Studies in Mathematics at the University of Madras
> the third of three Quarterly Reports required by his research scholarship.
> Sections 4 through 10 of this report contain a self-contained treatment of
> the fractional iteration of functions. Ramanujan defines `F^n(x)` for
> non-integer `n` as the unique function passing through the integer iterates,
> states and applies the conjugation theorem (which since 1884 has been known
> as the Koenig linearisation theorem, and since 1871 as the central result of
> Schröder's *Über iterirte Funktionen*), works out explicit closed forms for
> the fractional iterates of `F(x) = x²-2` (the Chebyshev semigroup, with
> `F^n` recoverable via a cosh formula), `F(x) = x²+2x`, `F(x) = x²-2x`,
> `F(x) = x²+4x`, and the rational map `x → (1-x)/(1-x²)`. Section 10 derives
> the formula `ψ₁(x) = C/F(x)`, the infinitesimal generator of the iteration
> semigroup — the Lie vector field whose flow realises the fractional iteration
> by integration. The Quarterly Report dates from March 9, 1914. Julia's
> *Mémoire sur l'itération des fonctions rationelles* dates from 1918, Fatou's
> *Sur les équations fonctionnelles* from 1917-1920, Böttcher's iteration paper
> from 1898/1904, Koenig's linearisation theorem from 1884, and Schröder's
> functional equation from 1871. We document Ramanujan's contributions and
> verify that they are not registered in the modern holomorphic-dynamics
> historiography (Milnor 2006; Audin 2009; Stawiska-Domoradzki 2014; Rosa
> 2026), nor in Berndt's canonical commentary on the Notebooks (Berndt 1985;
> Berndt 1984 BLMS; Berndt 2022 HRJ reproduction). We make the case that
> Ramanujan should be added to the standard pre-1918 chronological table of
> iteration-theory contributors.

---

## Section structure (5 sections + appendix)

### §1. Introduction (~2 pp)

Frame the priority question. Ramanujan March 1914 < Julia 1918 / Fatou 1917-19
< Lattès 1918 < Böttcher 1904 < Leau 1897 < Koenigs 1884 < Schröder 1871. The
QR III content has been in print since Berndt's 1984 BLMS commentary and
Berndt-Wilson's 1981 PRSE on Chapter 4, with a faithful reproduction in HRJ
2022; yet the modern holomorphic-dynamics literature does not register the
connection. State the paper's two contributions:
1. A self-contained mathematical exposition of QR III §4-§10 in modern
   notation, showing the line-by-line correspondence with the Schröder-Koenig
   linearisation framework.
2. A bibliographic verification that the standard modern holomorphic-dynamics
   historiography does not currently cite Ramanujan as a pre-1918 contributor
   to iteration theory.

Briefly note what the paper does NOT claim: not that Ramanujan founded
holomorphic dynamics (the global / Riemann-sphere framework of Fatou-Julia is
genuinely beyond QR III); not that Ramanujan was unaware of Schröder or
Koenigs (the QR has zero non-Indian-mathematics citations of any kind; the
question of Ramanujan's reading of European functional-equation literature is
open and addressed in §5); not that Ramanujan's results in §4-§10 are
mathematically deeper than Koenig's — they are similar in scope, but derived
independently and presented as primary material in a primary-source document.

### §2. Ramanujan's construction (~5-6 pp)

Reproduce QR III §4-§10 content faithfully, in modern notation, with explicit
correspondence to the Schröder-Koenig framework. Subsections:

#### §2.1. The definition of `F^n` for fractional `n` (QR §4-§5)

Ramanujan: `F^n(x)` is the unique function passing through `F^0(x) = x`,
`F^1(x) = F(x)`, `F^2(x) = F(F(x))`, ..., extended via interpolation to
arbitrary real `n`. Modern: this is the requirement that `F^n` form a
one-parameter semigroup. Worked example: for `F(x) = ax^p`, Ramanujan derives
`F^n(x) = a^{(p^n-1)/(p-1)} x^{p^n}`, including the irrational-`n` extensions
`F^{√2}, F^{log 2}, F^e, F^π`. **Exhibit 1.**

#### §2.2. The conjugation theorem (QR §6)

Ramanujan: if `F^m(x) = φ(x)`, `F^n(x) = ψ(x)`, and `f^m(x) = χ^{-1}φ(χ(x))`,
then `f^n(x) = χ^{-1}ψ(χ(x))`. Modern: this is the Schröder conjugation
theorem (Schröder 1871; Koenigs 1884) — `f^n = χ^{-1} ∘ F^n ∘ χ`. Modern
interpretation: the iteration of `f` near a fixed point is conjugate to the
iteration of its "linearised normal form" `F`. Direct quote of QR §6 to be
included.

#### §2.3. The Chebyshev semigroup `F(x) = x²-2` (QR §6(b))

Ramanujan's worked example: for `F(x) = x²-2` (and `x > 2`), he derives
`F^n(x) = 2 cosh(2^n · cosh^{-1}(x/2))`. This is the **explicit Schröder
linearisation** of the Chebyshev semigroup at the doubling-map fixed point on
the circle. **Exhibit 1, continued.** Note that this same construction is what
modern holomorphic dynamics treats as the genus-0 degenerate limit of the
j-function modular dynamics (cf. Milnor's discussion of Lattès examples). The
Chebyshev case is in some sense the universal worked example. Ramanujan
computes specific fractional iterates:
- `F^{log₂ 3}(x) = x³ - 3x` (Chebyshev polynomial T₃ in disguise);
- `F^{log₂ 5}(x) = x⁵ - 5x³ + 5x` (T₅);
- and the general `F^{log₂ k}(x)` is the k-th Chebyshev polynomial.

This pre-dates Lattès' 1918 explicit construction of "Lattès maps" (the
rational maps whose Julia set is the whole sphere, of which the Chebyshev
case is the genus-0 prototype) — though Lattès' contribution is the
*sphere-level* dynamical interpretation, which Ramanujan does not address.

#### §2.4. Other explicit fractional iterates (QR §6(c, d))

Ramanujan computes `F^n` explicitly for `F(x) = x²+2x`, `F(x) = x²-2x`,
`F(x) = x²+4x`. He also iterates the rational map `x → (1-x)/(1-x²)` at
fractional `r` involving `log 3 / log 2`. These are direct applications of
the conjugation theorem with explicit choice of conjugacy `χ`.

#### §2.5. Hardy orders and self-defying functional equations (QR §7-§9)

Brief subsection, mostly as bridging material. Ramanujan re-derives Hardy's
*Orders of Infinity* hierarchy and constructs (§8) a function `φ` defying all
logarithmic scales via the functional equation `xφ(x) = φ(log x)`. Berndt
notes (NB Part I, lines 15694-15756) that this construction was inspired by
Hardy's tract but the specific functional equation is Ramanujan's. Modern
context: this functional equation is in the same family as the Abel equation
`f(φ(x)) = f(x) + 1` (the additive cousin of Schröder's `f(φ(x)) = λ f(x)`),
and the function `φ` Ramanujan constructs is essentially an iterated-
logarithm function — relevant to the broader iteration-theory landscape but
not to the Schröder-Koenig linearisation specifically.

#### §2.6. The infinitesimal generator `ψ₁(x) = C/F(x)` (QR §10) — Exhibit 2

This is the most striking single result. Ramanujan Taylor-expands
`f^r(x) = ψ₀(x) + r/1! ψ₁(x) + r²/2! ψ₂(x) + ...`, where `f^r` is a fractional
iterate parameterised by real `r`. He shows `ψ₀(x) = x` and, by differentiating
`f^{r+h} = f^r ∘ f^h` in two ways, derives:
- `df^r/dr = ψ₁(x) · df^r/dx`,
- `ψ_n(x) = ψ₁(x) · dψ_{n-1}/dx`.

Combined with QR §9's invariance result (∫ F is constant along the f-orbit),
Ramanujan deduces `ψ₁(x) = C/F(x)` for some integration constant C.

**Modern interpretation.** The function `ψ₁` is the **infinitesimal
generator** of the one-parameter iteration semigroup `f^r` at `r = 0`. The
ODE `df^r/dr = ψ₁(f^r)` is the *flow equation*, and `ψ₁(x) ∂/∂x` is the *Lie
vector field* whose time-1 flow is `F`. The formula `ψ₁ = C/F` makes the
iteration semigroup explicit as the flow of a vector field with first integral
related to `F`. This is the same content as the modern theory of holomorphic
flows (Camacho 1978, Écalle 1981-85); it is also Levi-Civita's "vector field
of an iteration" construction, which post-dates Ramanujan and is independently
in print in the 1910s. **Exhibit 2.**

### §3. Bibliographic verification: the historiographical gap (~3 pp)

Document the absence in the modern literature, source-by-source, citing
[W8_PRE_JULIA_LIT_SCAN.md](W8_PRE_JULIA_LIT_SCAN.md) for the methodology.

Subsections:
- **§3.1.** The standard textbook chronologies: Milnor 2006 (3rd ed.; cf.
  arXiv:math/9201272 1990 lectures), §i-2 chronological table. The 14 named
  founders. Ramanujan is not on the list. The Koenigs Theorem §6.1
  bibliography cites Schröder 1871, Koenigs 1884, Böttcher 1904 — no
  Ramanujan reference.
- **§3.2.** The recent historiographical monographs. Audin 2009 *Fatou,
  Julia, Montel* — no Ramanujan reference. Rosa 2026 *Origins of Holomorphic
  Dynamics* — TOC and chapter previews list ~15 named pre-1918 contributors;
  Ramanujan is not among them.
- **§3.3.** The under-appreciated-pioneer-rescue literature. Stawiska-
  Domoradzki 2014 *Lucjan Emil Böttcher and his mathematical legacy*
  (arXiv:1207.2747) — Böttcher was the original "forgotten pre-Julia
  iteration pioneer", and the paper is a deliberate exercise in rescuing his
  reputation. Yet Ramanujan is not mentioned. This is the cleanest evidence
  that the citation graph has a structural gap, not just an isolated
  omission.
- **§3.4.** Berndt's canonical Ramanujan commentary. Notebooks Part I (1985)
  Ch. 4 "Iterates of the Exponential Function and an Ingenious Formal
  Technique" — 150+ pages of commentary on iteration content, with zero
  mention of Schröder, Koenigs, Julia, Fatou, Böttcher, Écalle, or Lattès.
  Berndt frames the work as Bell-number / Comtet-power-series /
  Hardy-orders-of-infinity material; the Schröder-Koenig connection is not
  drawn. Same for the 1984 BLMS commentary (per its 1985 NB Part I successor)
  and the 2022 HRJ reproduction.

### §4. Counterpoint and qualifications (~2 pp)

Address the strongest counterarguments honestly. The CLAUDE.md "near-match is
not a match" discipline applies in both directions.

#### §4.1. Ramanujan's work is *not* sphere-level dynamics

The Fatou-Julia framework is global: rational maps acting on the Riemann
sphere, the Julia set as the closure of repelling periodic points, etc.
Ramanujan's QR III work is local: fractional iteration in a neighbourhood of
a fixed point. The two are not the same thing. What Ramanujan does in QR III
is closer to Schröder 1871 and Koenig 1884 in scope (local linearisation
near a fixed point) than to Fatou-Julia (global rational-map dynamics). So
"Ramanujan founded holomorphic dynamics" is **not** the claim. The claim is
that he made local-linearisation results contemporaneous with Koenig 1884
(rediscovered 30 years later, independently) and preceding Fatou-Julia 1917-
19.

#### §4.2. Ramanujan's proofs are not modern-rigorous

Berndt notes "the arguments in these three sections have been purely
formal" (NB Part I line 15670). The Schröder-Koenig modern statements
require convergence of an iterated-coordinate-change series, which
Ramanujan does not address. So in terms of rigour, Schröder 1871 and Koenig
1884 are the canonical citations and that is appropriate. The QR III
material is a parallel independent rediscovery with the same formal content
but no convergence analysis. This is a real qualification on any priority
claim.

#### §4.3. Ramanujan's reading

Did Ramanujan know of Schröder or Koenigs? The QR cites no European
functional-equation literature. The standard mathematical sources Ramanujan
had access to via the Madras Government Public Library were Carr's
*Synopsis*, Bromwich, and (per Berndt's tracing) Hardy's *Orders of
Infinity* tract. Schröder's *Math. Ann.* paper and Koenig's *Ann. Sci. Éc.
Norm. Sup.* paper are in journals Ramanujan demonstrably did not have
access to in Madras. Berndt's commentary (NB Part I) treats the iteration
work as independent rediscovery on the basis of this access analysis. Note
the contrast with QR II §7 (Theorem III) on Fourier self-reciprocity, where
Ramanujan does invoke "Fourier's theorem" by name. The absence of
"Schröder" or "Koenigs" from the QR text supports independence-of-discovery.

#### §4.4. The "Chebyshev semigroup" point

Ramanujan's `F(x) = x²-2` explicit formula `F^n = 2 cosh(2^n cosh^{-1}(x/2))`
is the *same* construction Schröder used as his motivating example in 1871.
This may or may not be a coincidence. The conservative interpretation is:
the example is so natural that two independent investigators would land on
it; the formal Schröder linearisation of any conjugate of the doubling map
yields exactly this formula. The stronger interpretation — that Ramanujan
read Schröder somewhere — is unverifiable from available evidence.

### §5. Why the citation gap persists (~1 p)

Brief speculative subsection on historiographical mechanism. Three contributing
factors:
1. Hardy / Watson / Berndt all worked the modular-forms-and-q-series side of
   Ramanujan because that is where his most spectacular results lay (partition
   asymptotics, mock theta, Eisenstein series). The analysis / iteration
   material was peripheral to their research programmes; Berndt addressed it
   completely in commentary but did not connect it to the holomorphic-dynamics
   side.
2. Conversely, the Schröder-Koenig-Julia-Fatou tradition was a French / Polish
   / Russian programme almost entirely; the Cambridge analytic-number-theory
   programme (in which Ramanujan operated post-1914) had no overlap with it.
   Hardy's *Orders of Infinity* tract (which Ramanujan read) does not cite
   Schröder or Koenigs.
3. The 2022 HRJ reproduction by Berndt is recent enough that it has not yet
   been digested by the dynamics community. The 1984 BLMS paper is paywalled;
   the 1985 NB Part I commentary is well-known to Ramanujan scholars but not
   to dynamics historians. The result is two non-intersecting expert
   communities each looking at the material with their own canon.

This is a special case of the broader "canonical Ramanujan ⊊ historical
Ramanujan" meta-finding documented in [BIG_IDEAS_REVIEW.md §5b](BIG_IDEAS_REVIEW.md).

### §6. Conclusion (~0.5 p)

Re-state the contribution: a Ramanujan-side primary-source documentation +
a dynamics-side bibliographic verification, together establishing that the
modern chronological table of pre-1918 iteration-theory contributors should
add Ramanujan as a 1914 entry (independent of, but contemporaneous with,
Koenig and the European tradition).

The result is *not* a refoundation of the field; it is a correction of the
historical record.

### Appendix A — Page-and-line correspondence table

A two-column table:
- Left column: QR III §-numbers and line-ranges in the Berndt 2022 HRJ
  reproduction.
- Right column: corresponding modern result (Schröder 1871 §, Koenig 1884
  §, Milnor 2006 Theorem reference).

This is the "exhibit map" for verification by referees, and would be ~1 page.

### Appendix B — Verbatim transcriptions

Long-form quotations of QR III §6(b) (Chebyshev), QR III §10 (infinitesimal
generator derivation), with side-by-side modern notation. ~1-2 pages.

---

## Key exhibits (called out for the abstract / introduction)

**Exhibit 1.** QR III §6(b): for `F(x) = x²-2`, `x > 2`, Ramanujan derives
`F^n(x) = 2 cosh(2^n cosh^{-1}(x/2))`. The fractional iterates `F^{log₂ k}(x)`
are explicitly the Chebyshev polynomials `2 T_k(x/2)`. This is the explicit
Schröder linearisation of the Chebyshev semigroup, 4 years before Lattès'
1918 introduction of the rational-map families now called "Lattès examples".

**Exhibit 2.** QR III §10: `ψ₁(x) = C/F(x)`, where `ψ₁` is the infinitesimal
generator of the one-parameter iteration semigroup. The flow equation
`df^r/dr = ψ₁(f^r)` is derived by formally differentiating
`f^{r+h} = f^r ∘ f^h`. This is the Lie vector field of the iteration,
expressed as `(C/F(x)) ∂/∂x`. Modern: the time-1 flow of a holomorphic vector
field; equivalent to the Camacho-Écalle local-flow theory at the formal
level.

**Exhibit 3.** Date precedence table:
| Source | Date | Result |
|---|---|---|
| Schröder, *Math. Ann.* **3** | 1871 | Functional equation `φ(f(x)) = λφ(x)` |
| Koenigs, *Ann. Sci. Éc. Norm. Sup.* **1** suppl. | 1884 | Linearisation thm for `|λ| ≠ 0, 1` |
| Leau, *Ann. Fac. Sci. Toulouse* **11** | 1897 | Parabolic case |
| Böttcher, *Izv. Kazan* **14** | 1898/1904 | Superattracting case `λ = 0` |
| **Ramanujan, Quarterly Report III, Madras** | **March 9, 1914** | **Explicit `F^n` for Chebyshev; ψ₁ = C/F generator** |
| Fatou, *Bull. Soc. Math. France* **47-48** | 1917-20 | Global Riemann-sphere dynamics |
| Julia, *J. Math. Pures Appl.* **8** | 1918 | Mémoire sur l'itération |
| Lattès, *C. R. Acad. Sci. Paris* | 1918 | Lattès examples |

---

## Target venue

**Primary candidate: *Historia Mathematica*** (Elsevier; the standard journal
for primary-source-based history of mathematics). The paper is short, the
finding is bibliographic-historical with a primary-source verification
component, and the venue audience overlaps both the iteration-theory and
Ramanujan-studies communities.

**Secondary candidates:**
- ***The Ramanujan Journal*** (Springer): natural home for Ramanujan-side
  primary-source work; might prefer a slightly heavier mathematical
  exposition.
- ***The American Mathematical Monthly*** or ***Mathematics Magazine***: if
  the paper is rewritten in expository / popularisation style, this is a
  good destination. Lower citation impact but very high readership.
- ***Hardy-Ramanujan Journal***: open-access; Berndt is the editor; would
  publish a Ramanujan-iteration-theory historical note quickly. But the
  audience is exclusively Ramanujan scholars; the dynamics-community half of
  the readership would not see it. This is a strong negative.
- ***Notices of the AMS***: a short expository version (4-6 pp) would be a
  good fit for the historical-note section.

**Recommended target**: *Historia Mathematica* as the primary outlet, with
*The American Mathematical Monthly* as the expository backup. *Historia
Mathematica* is the right venue because (a) the half of the paper that is
*verification of a historiographical gap* requires the historian-of-math
audience to fully appreciate, and (b) the journal regularly publishes
priority-discovery and rediscovery-rescue pieces of exactly this length and
shape.

---

## Estimated paper length

**12-18 pages** at *Historia Mathematica* / *Ramanujan Journal* style
formatting:
- §1 Introduction: 2 pp
- §2 Mathematical exposition: 5-6 pp (sub-sub-sections; ~5 pp at *AMS Monthly*
  density)
- §3 Bibliographic verification: 3 pp
- §4 Counterpoint and qualifications: 2 pp
- §5 Historiographical mechanism: 1 pp
- §6 Conclusion: 0.5 pp
- Appendices A + B: 2 pp
- References: 1-2 pp

A 6-8 pp version is feasible if §2 is compressed by dropping §2.5 (the Hardy
orders subsection) and §2.4 (the other explicit fractional iterates), and §3
is condensed to a single paragraph per source. The shorter version would
target *AMS Monthly* / *Mathematics Magazine* / *Math. Intelligencer*.

---

## Drafting cost estimate

- §1 + §2.1 + §2.6 + §3 + §6: 1-2 days of focused writing from a clean
  outline; most of the load-bearing content is already in
  [W8_PRE_JULIA_LIT_SCAN.md](W8_PRE_JULIA_LIT_SCAN.md) and
  [diary 20](../diary/20_hunt5_qr_operator_tagging.md) §"Follow-up leads"
  item 4. The QR III primary text is already transcribed in
  [qr_section_index.json](../corpora/transcriptions/quarterly_reports/qr_section_index.json).
- §2.2, §2.3, §2.4, §2.5: requires careful re-reading of QR III §4-§10 to
  write modern-notation versions; ~2 days.
- §4 counterpoint: requires honest engagement with the "near-match is not
  a match" discipline; 1 day.
- §5 historiographical analysis: 0.5 day.
- Appendix A: trivial once §2 is written.
- Appendix B: requires careful side-by-side transcription; 0.5 day.

**Total: ~5-7 person-days of writing** for the 12-18 pp version; ~3 days for
the 6-8 pp version. Both are well-bounded relative to the rkc/ tooling work
or the Hunt 5b cog-sci paper, which are much larger commitments.

---

## What needs to happen before drafting

Per [W8_PRE_JULIA_LIT_SCAN.md](W8_PRE_JULIA_LIT_SCAN.md) "Citation candidates
the agent could verify but did not", three pre-drafting verifications would
lock in the verdict bucket:

1. **Pull Berndt 1984 BLMS paper directly** (priority 1; settles the
   load-bearing missing data point).
2. **Targonski 1981 *Topics in Iteration Theory*** check (priority 2).
3. **MathSciNet keyword query** with MSC 37* filter (priority 3; the cheapest
   high-value verification).

If any of these surface an existing citation of QR III iteration content,
the paper outline needs to be revised — likely toward "we add a modern
mathematical exposition to a recently-noted but mathematically-incomplete
historical observation" rather than the priority-rescue framing above. But
the prior is strongly that none of the three verifications will return a
positive.

---

## Risk register

- **R1**: A specialist iteration-theory historian has noted this and the
  paper is scooped. Probability: ~25% per the scan. Mitigation: pre-drafting
  verification step above.
- **R2**: Reviewers reject on grounds of "this is well-known to Ramanujan
  scholars" (i.e. Berndt commentary already covered it). Counterargument:
  Berndt covered the *mathematics* but not the *historiographical connection
  to the Schröder-Koenig-Julia tradition* — those are different contributions.
  The paper should make this distinction clearly in §1.
- **R3**: Reviewers reject on grounds of "Ramanujan's work is not
  sphere-level dynamics, so the priority claim is mis-stated". Mitigation:
  §4.1 addresses this honestly; the claim is local-linearisation parity with
  Koenig 1884, not founding-of-holomorphic-dynamics.
- **R4**: Reviewers note that Ramanujan's "proofs" are not rigorous and
  question the priority claim. Mitigation: §4.2 addresses this; the
  qualification is real and stated honestly.

The risk profile is moderate; the paper is publishable if the verification
step doesn't surface a prior citation.

---

## Cross-references

- [W8_PRE_JULIA_LIT_SCAN.md](W8_PRE_JULIA_LIT_SCAN.md) — the bibliographic
  verification that triggers this outline.
- [diary 20 §"Follow-up leads" item 4](../diary/20_hunt5_qr_operator_tagging.md)
  — the original lead.
- [BIG_IDEAS_REVIEW.md §2b](BIG_IDEAS_REVIEW.md) — the "QR III operators
  connect to modern math" addendum where the priority observation first
  appears.
- [qr_section_index.json](../corpora/transcriptions/quarterly_reports/qr_section_index.json)
  — primary-source transcription pointer for sections `qr3_sec_4_5`,
  `qr3_sec_6`, `qr3_sec_10`.
- [downloaded-pdfs/ramanujankitap1.pdf](../downloaded-pdfs/) — Berndt NB
  Part I local copy used in the scan.
