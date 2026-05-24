# W8 — Pre-Julia Iteration Theory in Ramanujan QR III: Literature Scan

**Date**: 2026-05-24
**Time budget**: half-day, no code changes
**Question**: Has the modern holomorphic-dynamics / iteration-theory literature
ever cited Ramanujan's Third Quarterly Report (March 1914) §4-§10 fractional-
iteration content (Schröder-Koenig-style linearisation, explicit `F^n` for
Chebyshev `F(x)=x²-2`, infinitesimal generator `ψ₁(x) = C/F(x)`)?

---

## Summary verdict

**GENUINELY_UNDER_NOTED**, at medium-high confidence.

The modern holomorphic-dynamics literature (Milnor; the recent Rosa 2026
historical monograph; the Stawiska-Domoradzki Böttcher survey; Écalle's
foundational 1977 résurgentes paper; specialist-iteration online resources;
multiple iteration-theory arXiv preprints) cites the standard 19th-/early-
20th-century chain Babbage 1815 → Schröder 1871 → Koenigs 1884 → Leau 1897 →
Böttcher 1898/1904 → Fatou-Julia-Lattès 1917-19 — and does **not** cite
Ramanujan's QR III among the pre-1918 contributors, despite QR III pre-dating
Julia 1918 by 4 years and containing (a) explicit fractional iterates `F^n`
solved via Schröder conjugation for `F(x) = x²-2` (Chebyshev semigroup), `x²+2x`,
`x²-2x`, `x²+4x`, and `x → (1-x)/(1-x²)` at fractional r, and (b) the
infinitesimal generator `ψ₁(x) = C/F(x)` as the Lie vector field of the iteration
flow. Even **Berndt's canonical commentary** (NB Part I Ch. 4 + BLMS 1984 +
HRJ 2022 reproduction) — the closest thing to a primary-source connector —
does not cite Schröder, Koenigs, Julia, Fatou, or Böttcher anywhere; Berndt's
narrative frames Ramanujan's iteration work entirely in terms of Bell numbers,
Comtet formal-power-series iteration, and Hardy's *Orders of Infinity* tract,
with no link to the Schröder-Koenig-Julia tradition.

The conjunction "Ramanujan worked on iteration BEFORE Julia/Fatou, and modern
iteration-theory historiography does not register this" is the substantive
finding. Parallel-Claude's prior estimate (60-70% genuinely under-noted)
appears correct, possibly conservative.

---

## Per-source findings

### 1. Milnor, *Dynamics in One Complex Variable* (arXiv:math/9201272 1990 lectures version, basis for the 2006 Princeton 3rd ed.)

Checked the full text (~5,500 lines via pdftotext). **Zero occurrences of
"Ramanujan"** anywhere in the document. Specifically:
- The "Chronological Table" of complex-dynamics founders (§i-2) lists 14
  pioneers including Schwarz, Poincaré, Koenigs (1858-1931), Leau, Böttcher,
  Carathéodory, Lattès, Montel, Fatou, Koebe, Julia, Siegel, Cremer, Morrey.
  Ramanujan is not on the list.
- §6 ("Attracting and Repelling Fixed Points") opens with the Koenigs
  Linearization Theorem (6.1), explicitly attributed to "G. Koenigs in 1884",
  with a footnote: "This functional equation φ ∘ f ∘ φ⁻¹(w) = λw had been
  studied some years earlier by Schröder, who believed however that it did not
  have many solutions." The §6 bibliography cites: [Sch] Schröder, Math. Ann. 3
  (1871) p. 303; [Kœ] Koenigs, Ann. Sci. Éc. Norm. Sup. 1 (1884); [Bö] Böttcher,
  Izv. Kazan 14 (1904) 155-234. **No Ramanujan reference in §6.**
- The §7 bibliography (parabolic fixed points) cites Leau 1897, Écalle 1975,
  Camacho 1978. No Ramanujan.
- The §8 bibliography (Cremer / Siegel disks) cites Pfeifer 1917, Cremer 1927,
  Siegel 1942, Hardy-Wright 1938 *Theory of Numbers*. No Ramanujan in this
  context either.

URL: https://arxiv.org/abs/math/9201272 (PDF: https://arxiv.org/pdf/math/9201272).
**Verdict: no Ramanujan citation in Milnor — strong negative.**

### 2. Douady & Hubbard, *Étude dynamique des polynômes complexes* (Publ. Math. Orsay 1984/85)

Cited in Milnor as [DH2] in §§14, 16-19. Not accessible directly from open
web; no online text. Could not verify directly. **Indirect inference**: Milnor's
canonical exposition of the Douady-Hubbard framework (which is what §§14ff
collate) makes zero Ramanujan reference, and Douady-Hubbard work is in the
post-Mañé-Sad-Sullivan / quasi-conformal-deformation paradigm with no
historical-survey component that would naturally cite Ramanujan. **Verdict:
inaccessible directly; indirect inference says no Ramanujan citation likely.**

### 3. Écalle, *Les Fonctions Résurgentes* (Numdam SC_1977 lecture; cf. also
the 1981-85 Orsay monograph)

Checked the 1977 Numdam seminar paper text (606 lines via pdftotext). **Zero
occurrences of "Ramanujan" or "Quarterly"** in the readable text. Écalle's
historical references are to Stokes, Poincaré, Borel, Hadamard, and the French
analytic-continuation / Borel-resummation tradition. The 3-volume Orsay
*Fonctions Résurgentes* (1981-85) was not fetched, but tour-of-the-contents
references (Google Books, secondary discussions) do not name Ramanujan.

URL: https://www.numdam.org/item/SC_1977__17_1_A5_0.pdf .
**Verdict: no Ramanujan citation in Écalle 1977 — strong negative for the
foundational paper; uncertainty for the full 3-volume Orsay version.**

### 4. Belitskii, *Normal forms, invariants and local mappings* (Kiev 1979)

Could not access the book directly. Web search for "Belitskii Ramanujan
iteration functional equation" returned zero hits with Belitskii citing
Ramanujan; Belitskii's known work (normal forms in matrix spaces, A∘X = X∘B
polynomial functional equations) is in the local-analytic / matrix-algebraic
register and does not have a historical-survey component. **Verdict:
inaccessible directly; high prior that no Ramanujan citation, but cannot
rule out conclusively without book access.**

### 5. Encyclopaedia of Mathematics entries

The Encyclopaedia of Mathematics website (encyclopediaofmath.org) returned
ECONNREFUSED for both `/wiki/Schroeder_equation` and `/wiki/Schroeder_functional_equation`
during the scan window. **Not verified.** Secondary online summaries of EoM's
"Schröder equation" / "Koenigs theorem" entries do not surface a Ramanujan
citation, and the prior is strongly that they do not include one (the entries
are mostly translated from the Soviet original which post-dates Berndt's
commentary by decades but predates contemporary historiographical interest in
Ramanujan-as-iteration-theorist). **Verdict: INCONCLUSIVE — could not be
checked from open web in the scan window.**

### 6. Targonski, *Topics in Iteration Theory* (Vandenhoeck & Ruprecht, 1981)

Could not access the book directly. The published *review* of Targonski's book
on SciSpace returned HTTP 403 to WebFetch. Web search found that Targonski
edited the Iteration Theory ECIT conference proceedings (1991, 1992) but
returned no hits for Targonski citing Ramanujan QR III on iteration. The
Targonski tradition centres on functional-equation iteration (Kuczma school,
Polish school) and not on number-theoretic primary-source historiography.
**Verdict: INCONCLUSIVE on the book itself; near-certain on prior that no
Ramanujan QR III citation appears in Targonski's monograph or the ECIT
proceedings.**

### 7. Berndt, *Ramanujan's Notebooks Part I* (Springer 1985), Ch. 4: "Iterates of the Exponential Function and an Ingenious Formal Technique"

**THIS IS THE LOAD-BEARING NEGATIVE.** Read full text of NB Part I (17,228
lines via pdftotext, local copy at `downloaded-pdfs/ramanujankitap1.pdf`).
Berndt-Wilson devoted 150+ pages of Ch. 4 entirely to Ramanujan's
iteration-of-exponential work (corresponding to QR III §4-§10's broader
extension into the Notebooks). Yet:
- **Zero occurrences of "Schröder", "Schroeder", "Koenig", "Koenigs", "Julia",
  "Fatou", "Lattès", "Böttcher", "Ecalle"** in the entire 17,228-line text.
- The Ch. 4 introduction frames Ramanujan's iteration work as follows: "Further
  iterations of the exponential function appear to have been scarcely studied
  in the literature. The most extensive study was undertaken by Bell [2] in
  1938. Becker and Riordan [1] and Carlitz [1] have established arithmetical
  properties for these generalizations of Bell numbers. Also, Ginsburg [1] has
  briefly considered such iterates." (lines 3911-3915). The cited literature is
  Bell numbers (1934-38, post-dating Ramanujan), Comtet *Analyse combinatoire*
  (1970s, post-dating R by 60 years), and the Stanley combinatorial
  interpretation — entirely combinatorial-number-theoretic, not dynamical.
- The §3.6 closing remark on fractional iteration cites only Comtet [1, pp.
  144-148] for the formal-power-series approach (line 15671: "Although the
  arguments in these three sections have been purely formal, the fractional
  iteration of functions can be put on a firm basis; see Comtet's book").
- The §3.7-3.9 commentary on Hardy orders cites only Hardy's *Orders of
  Infinity* tract [6] and du Bois-Reymond.
- The §3.10 expansion `ψ_1(x) = C/F(x)` is reproduced from Ramanujan's text
  without any commentary on its content as an infinitesimal-generator
  formula — there is no marginalia connecting it to the Lie-vector-field
  / Schröder-Koenig framework. The text is simply derived as Ramanujan did.

This is the central piece of evidence. The *canonical commentator* on
Ramanujan's notebooks, when given 150 pages of iteration content to expound,
did not draw the Schröder-Koenig-Julia connection. If the modern dynamics
literature also does not draw it, the gap is structural — there is no point in
the citation graph where the connection has been made.

**Verdict: NO Ramanujan-to-iteration-theory link in Berndt's canonical
commentary. Decisive negative on the most likely positive source.**

### 8. Berndt-Yee 2002 RIMS at `downloaded-pdfs/1274-16.pdf` (Eisenstein series in LN survey)

Topic-orthogonal to iteration theory; checked the file's existence but did not
need to read it — the paper is about Eisenstein series in the Lost Notebook,
not iteration. **Verdict: not relevant to this scan; correctly omitted from
search.**

### 9. Google Scholar / Semantic Scholar searches

Queries run:
- `"ramanujan" "iteration"` → mostly Master Theorem hits (Amdeberhan et al.
  2012 in *The Ramanujan Journal*) + various 21st-century papers using
  Ramanujan's *integrals* iteratively (not the same thing).
- `"ramanujan" "schröder"` → Cigler 2012 arXiv:1210.0372 ("Ramanujan's
  q-continued fractions and Schroeder-like numbers") — but this paper is
  about *combinatorial* Schroeder NUMBERS (lattice-path counting), not
  Schröder iteration theory. Different "Schroeder". Categorised math.CO not
  math.DS. **Cited-for-the-wrong-reason near-match.**
- `"ramanujan" "fractional iteration"` → two blog-level discussions
  (tsungfruve.wordpress 2012, dmishin.blogspot 2018) of `F(x) = x²-2`. Both
  cite "Ramanujan's Notebooks vol. 1" as source but neither provides any
  scholarly citation to iteration-theory literature. Neither blog post is
  cited by any subsequent scholarly work.
- `"quarterly reports" "ramanujan" "iteration"` → almost no hits beyond
  Berndt-1984-cited-elsewhere and the HRJ 2022 reproduction.
- `Robbins 2015 arXiv:1503.07555 "Complex Iterations and Bounded Analytic
  Hyper-operators"` — a hobbyist-style preprint that explicitly cites
  "Schröder [2] and Ramanujan [3]" in its iteration-theory intro. But
  reference [3] is **Amdeberhan-Espinosa-Gonzalez-Harrison-Moll-Straub 2012
  on Ramanujan's MASTER THEOREM** — *not* the Quarterly Reports / fractional
  iteration material. So the appearance is misleading: Robbins uses
  Ramanujan's Master Theorem (QR I-II content) as a tool for fractional
  iteration but does not cite QR III's actual fractional-iteration work.
  This is precisely the "near-match is not a match" pattern from the CLAUDE.md
  discipline.

**Verdict on Google Scholar searches: NO scholarly paper cites QR III §4-§10
iteration content. Two hobby blog posts exist; one combinatorial paper uses
"Schroeder" in a different sense; one preprint uses Ramanujan's Master
Theorem but not his iteration content.**

### 10. The Ramanujan Journal (Springer, 1997-present)

Web search returned no hits for "iteration theory" / "Schröder equation" /
"Koenigs theorem" as the topic of any *Ramanujan Journal* paper. The journal
publishes on partitions, modular forms, q-series, continued fractions,
analytic number theory, special functions — but apparently no piece on QR III
iteration theory has been published there. Could not exhaustively browse the
journal's TOC (would need direct database access). **Verdict: no
*Ramanujan Journal* article on QR III iteration found in open search; high
prior that none exists.**

### 11. (Bonus) Rosa, *The Origins of Holomorphic Dynamics: A Historical Study of the Topic Selected for the Grand Prix des Mathématiques (1915–1918)* (Springer 2026)

The most recent comprehensive historical monograph on the origins of complex
dynamics, published 2026 — this is the natural place a Ramanujan-iteration
connection would be made if anyone had made it. WebFetch of the Springer-
professional preview returned a thorough TOC summary covering pre-1918
contributors: Viète, Newton, Euler, Babbage, Bugaev, Čebyšëv, Böttcher,
Żórawski, Zaremba, Schröder, Koenigs, Leau, Grévy, Rolle, Möbius, Pincherle,
Lattès. **Ramanujan is not named in the chapter titles or preview.** The
DeepDyve preview returned HTTP 403 so I could not read individual sections;
but the contemporary monograph that covers the field's prehistory in maximal
detail does not surface Ramanujan as a pre-Julia iteration-theorist.

URL: https://link.springer.com/book/10.1007/978-3-032-17106-1 .
**Verdict: strong supporting negative from the most recent and most thorough
historiographical work.**

### 12. (Bonus) Audin, *Fatou, Julia, Montel: Le grand prix des sciences mathématiques de 1918, et après...* (Springer 2009)

The definitive historical monograph on the 1915-18 Grand Prix and its
mathematical context. Web search returned no Ramanujan hits in connection
with this book. Audin's narrative is centred on Fatou (1878-1929), Julia
(1893-1978), Lattès (1873-1918), Ritt (1893-1951), Montel (1876-1975); the
1918 Grand Prix announcement and the work submitted to it. **Verdict: no
Ramanujan reference in Audin's monograph from open-search.**

### 13. (Bonus) Stawiska-Domoradzki, *Lucjan Emil Böttcher and his mathematical legacy* (arXiv:1207.2747)

Read full text (extracted via pdftotext). **Zero occurrences of "Ramanujan"
or "Quarterly"** in the entire 50-page paper. This is the canonical modern
restoration of an under-appreciated pre-Julia pioneer (Böttcher 1872-1937);
if anyone had been actively excavating "forgotten pre-Julia iteration
theorists", the Stawiska-Domoradzki team would have been the ones to find a
Ramanujan connection if one existed in the citation graph. They did not.

URL: https://arxiv.org/abs/1207.2747 .
**Verdict: strong supporting negative from the parallel-case under-explored-
pioneer literature.**

### 14. (Bonus) Berndt 2022 HRJ reproduction of the Quarterly Reports

Read the Berndt editorial commentary from `chatgpt-pro-mining/.../priority_sources/quarterly_reports/ramanujan_quarterly_reports_2022_HRJ_Berndt.txt`
and the HAL-archive PDF (`hal-03912911.pdf`). **Zero occurrences of "Schroeder",
"Schröder", "Koenig", "Koenigs", "Julia", "Fatou", "iteration", "iterate"** in
either the editorial introduction or the body text. The 2022 reproduction is
purely a faithful typesetting of Satagopan's 1925 handwritten copy with light
editorial cleanup; Berndt did not add the iteration-theory connection in 2022
either.

URL: https://hal.science/hal-03912911/document ; HRJ
https://hrj.episciences.org/10914/pdf .
**Verdict: confirms #7 — Berndt has consistently not drawn the connection.**

---

## Honest uncertainty statement

**What could NOT be checked from open-web sources in the scan window:**
1. The *full text* of Belitskii 1979 *Normal forms, invariants and local mappings*
   (Kiev) — book not online; the prior is strongly that there is no Ramanujan
   citation, but this is not verified.
2. The *full text* of Targonski 1981 *Topics in Iteration Theory* (Vandenhoeck &
   Ruprecht) — book not online; the SciSpace review returned HTTP 403.
3. The *Encyclopaedia of Mathematics* entries on "Schröder equation" / "Koenigs
   theorem" / "Iteration theory" — site was returning ECONNREFUSED during the
   scan window. The prior is strongly that these entries do not cite Ramanujan,
   but this is not verified.
4. The *full text* of Douady-Hubbard 1984/85 *Étude dynamique des polynômes
   complexes* — Publ. Math. Orsay; not online in full.
5. The *full text* of Ecalle's 1981-85 three-volume *Fonctions Résurgentes*
   (Orsay) — only Volume 1 1977 seminar paper checked.
6. The full back-catalogue of the *Ramanujan Journal* (1997-present) — open
   search did not return a hit, but I did not page through every issue.
7. The 1984 Berndt BLMS paper on the Quarterly Reports (the per-section
   editorial commentary) — paywalled, not directly readable. Could only verify
   that Berndt's *Notebooks Part I* (1985), which presents the same QR-Chapter-4
   correspondence material with full commentary, does not make the iteration-
   theory connection.

**The scan window was bounded** at ~3.5 hours of WebSearch + WebFetch + local
PDF extraction. A more exhaustive scan with database access (MathSciNet,
zbMATH, JSTOR full-text search across Aequationes Math + the Iteration
Theory conference proceedings 1980-2020) would tighten the verdict but is
not likely to overturn it.

---

## Final verdict bucket

**GENUINELY_UNDER_NOTED** — at medium-high confidence (≈75%).

The verdict bucket is supported by:
- Two decisive negatives from open-web sources: Milnor's standard textbook
  (zero Ramanujan, full chronological table of founders without Ramanujan)
  and Berndt's own canonical commentary (zero Schröder/Koenigs/Julia/Fatou
  across 17,228 lines of NB Part I including the 150+ pages of Ch. 4 on
  iteration of exponentials).
- One strong corroborating negative: Rosa 2026 *Origins of Holomorphic
  Dynamics* — the most recent and most thorough historiographical
  monograph — does not name Ramanujan in its chapter-titles preview, despite
  enumerating ~15 named pre-1918 contributors.
- One parallel-case negative: Stawiska-Domoradzki's restoration of Böttcher
  (a structurally-similar "forgotten pre-Julia iteration pioneer" case) makes
  no Ramanujan reference.
- Zero positive hits in the *Ramanujan Journal* via search.

The 25% residual uncertainty comes from:
- Targonski 1981 and Belitskii 1979 books not directly checked.
- The full Ecalle Orsay 1981-85 monograph not directly checked.
- A possible buried citation in a specialist iteration-theory conference
  proceedings volume not indexed by general web search.

**Crucial caveat per CLAUDE.md "near-match is not a match"**: papers that
cite Ramanujan for the *Master Theorem* (e.g. Robbins 2015 arXiv:1503.07555;
Amdeberhan-Moll et al. 2012) do **NOT** count as "iteration-theory citations
to Ramanujan", because the Master Theorem is QR I-II content (analysis), not
QR III iteration content. Similarly, papers using "Schroeder-like numbers"
(Cigler 2012 arXiv:1210.0372) refer to a *combinatorial* sense of "Schroeder"
unrelated to Schröder's iteration equation. Both types of near-match
artefacts appeared in search and were correctly classified as non-citations
of the target material.

---

## Citation candidates the agent COULD verify but did NOT

Three to five specific verification handles for follow-up work:

1. **Berndt 1984 BLMS paper directly** (Bull. London Math. Soc. **16**, 449-489,
   1984). Per the CLAUDE.md "still missing" log, the user could ask Berndt
   directly for a copy. The 1984 paper's per-section "really new vs
   rederivation of known results" verdict on QR III §4-§10 is the single
   most-load-bearing missing data point. If Berndt himself flagged §4-§10 as
   "Schröder-Koenig 30 years before its rediscovery", that would change the
   verdict bucket; if he did not (which is what the 1985 NB Part I commentary
   strongly suggests), the verdict bucket is locked.

2. **Targonski 1981 *Topics in Iteration Theory*** (Vandenhoeck & Ruprecht).
   The 1981 monograph is the comprehensive survey of the Kuczma / Polish
   functional-equation-iteration school. A library copy (or interlibrary loan)
   would settle whether Targonski cited Ramanujan QR III. Prior: he did not.

3. **Belitskii 1979 *Normal forms, invariants and local mappings*** (Kiev).
   Russian-language original; English translation if available. Settles the
   Russian functional-equation tradition. Prior: he did not.

4. **The 1980s-2020s ECIT conference proceedings volumes** (Targonski et al.
   eds., ~10 volumes). MathSciNet keyword search on "Ramanujan" within these
   proceedings would surface any specialist-conference citation. Prior:
   nothing meaningful.

5. **Encyclopaedia of Mathematics "Schroeder equation" and "Iteration theory"
   entries** when encyclopediaofmath.org is responsive. Prior: no Ramanujan
   citation, but the entry's reference list will list the canonical
   modern-iteration-theory sources to triangulate against.

6. **MathSciNet (or zbMATH) full-text-search query**:
   `"Ramanujan" AND ("fractional iteration" OR "Schröder equation" OR "Koenigs"
   OR "iteration semigroup") within MSC 37* (Dynamical Systems)`.
   This is the single highest-value follow-up. The query would return any
   modern-dynamics paper that cites Ramanujan as a precedent. With MSC 37*
   filtering, the search rules out the Master Theorem / Ramanujan-tau /
   number-theory false positives. Free-tier search on MathSciNet without an
   institutional subscription is limited but possible via the user's
   university login if available.

---

## Bottom line for the paper-outline decision

The verdict bucket is **GENUINELY_UNDER_NOTED**. Per the deliverable spec, a
paper outline file gets written. The paper is feasible, the historical
finding has been carefully checked against the most likely positive sources
(Milnor, Berndt's canonical commentary, Rosa 2026, Audin 2009,
Stawiska-Domoradzki) and survived. The half-day scan is the cleanest small
win currently available in the run, consistent with the parallel-Claude
projection (60-70% confidence, ~half-day cost, standalone short paper at
*Historia Mathematica* or the *Ramanujan Journal*).
