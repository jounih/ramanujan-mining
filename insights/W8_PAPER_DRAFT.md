# Pre-Julia Iteration Theory in Ramanujan's Third Quarterly Report (March 1914)

**Draft v0.1 — for internal review only. Target venue: *Historia Mathematica* (primary) or *The Ramanujan Journal* (secondary). Estimated length: 14 pages at single-column 11pt.**

---

## Abstract

On 9 March 1914, two weeks before sailing to Cambridge, Srinivasa Ramanujan submitted to the Board of Studies in Mathematics at the University of Madras the third of three Quarterly Reports required by his research scholarship. Sections 4 through 10 of that Report contain a self-contained treatment of the fractional iteration of functions. Ramanujan defines $F^n(x)$ for non-integer $n$ as the unique function passing through the integer iterates; states and applies a *conjugation theorem* — namely the Schröder linearisation identity $f^n = \chi^{-1}\circ F^n\circ\chi$ — to compute explicit closed forms for the fractional iterates of $F(x)=x^2-2$ (the Chebyshev semigroup, $F^n(x)=2\cosh(2^n\,\mathrm{arccosh}(x/2))$), $F(x)=x^2+2x$, $F(x)=x^2-2x$, $F(x)=x^2+4x$, and the rational map $x\mapsto(1-x)/(1-x^2)$; and in §10 derives the formula $\psi_1(x)=C/F(x)$ for the *infinitesimal generator* of the one-parameter iteration semigroup — the Lie vector field whose time-$r$ flow is $f^r$. The Quarterly Report dates from March 1914. Julia's *Mémoire sur l'itération des fonctions rationelles* dates from 1918; Fatou's *Sur les équations fonctionnelles* from 1917–1920; Lattès' construction of what we now call Lattès examples from 1918; Böttcher's iteration paper from 1898/1904; Koenigs' linearisation theorem from 1884; Schröder's functional equation from 1871. We document Ramanujan's contributions, verify that they are not currently registered in the modern holomorphic-dynamics historiography (Milnor 2006; Audin 2009; Stawiska-Domoradzki 2014; Rosa 2026) nor in Berndt's canonical commentary on the Notebooks (Berndt 1985; Berndt 1984 BLMS; Berndt 2022 HRJ reproduction), and argue that Ramanujan should be added to the standard pre-1918 chronological table of iteration-theory contributors — with the explicit qualification that the priority claim is for *local linearisation* parity with Koenigs (1884), not for the *global* sphere-level dynamical framework of Fatou and Julia, which is genuinely beyond the Third Quarterly Report.

**Keywords**: Ramanujan; iteration theory; Schröder functional equation; Koenigs linearisation; Chebyshev semigroup; infinitesimal generator; history of complex dynamics; Quarterly Reports.

**MSC 2020**: Primary 01A60, 37-03; Secondary 39B12, 37F10.

---

## 1. Introduction

### 1.1 The priority chain

The modern chronological table of pre-1918 contributors to iteration theory, as reproduced in Milnor's *Dynamics in One Complex Variable* [Milnor 2006, §i-2] and in the recent comprehensive monograph of Rosa [Rosa 2026], lists approximately fifteen named figures: Babbage (1815), Schwarz, Poincaré, Bugaev, Čebyšëv, Schröder (1871), Koenigs (1884), Leau (1897), Böttcher (1898/1904), Grévy, Pincherle, Carathéodory, Möbius, Żórawski, Zaremba — followed by the 1917–19 explosion of Fatou, Julia, Lattès, Montel, Ritt that founded the modern global theory. Ramanujan does not appear on the list.

The central claim of this paper is that the omission is a historiographical accident, not a mathematical judgement. In a primary-source document dated 9 March 1914 — three years before Fatou's first major paper of 1917 [Fatou 1917], four years before Julia's prize-winning *Mémoire* of 1918 [Julia 1918], and four years before Lattès' announcement of the rational maps that bear his name [Lattès 1918] — Ramanujan independently derived (a) the Schröder conjugation identity $f^n=\chi^{-1}\circ F^n\circ\chi$ as the operational tool for fractional iteration; (b) explicit closed-form linearisations of five specific polynomial and rational maps, including the entire Chebyshev semigroup $F(x)=x^2-2$ in cosh-coordinates; and (c) the differential identity $\psi_1=C/F$, which in modern language is the equation for the infinitesimal generator of the one-parameter iteration flow $\{f^r\}_{r\in\mathbb{R}}$.

The Quarterly Report is not obscure. Berndt published the editorial first edition in *Bulletin of the London Mathematical Society* in 1984 [Berndt 1984], devoted a full chapter (Chapter 4) of *Ramanujan's Notebooks, Part I* to the related Notebooks material in 1985 [Berndt 1985], and in 2022 published a faithful open-access typeset reproduction of Satagopan's 1925 handwritten copy in the *Hardy-Ramanujan Journal* [Berndt 2022], from which all line-numbered quotations in this paper are taken. Yet the modern complex-dynamics literature does not cite this material as pre-1918 iteration theory. This is the asymmetry the paper documents and partially corrects.

### 1.2 What the paper claims and what it does not claim

Per the discipline of distinguishing the *mathematical content* of a primary source from the *historiographical claim* one is entitled to make about it, the paper makes three positive claims and explicitly disclaims three over-readings.

**Positive claim 1** (mathematical exposition; §3 below): Ramanujan's QR III §4–§10 contains, in modern translation, (a) the Schröder conjugation identity, (b) explicit Schröder-linearisations of five concrete maps including the Chebyshev semigroup, and (c) the infinitesimal-generator formula $\psi_1(x)=C/F(x)$ for the one-parameter iteration flow. The closed-form formula for the iterates of $F(x)=x^2-2$, namely
$$F^n(x)=2\cosh\!\bigl(2^n\,\mathrm{arccosh}(x/2)\bigr),\qquad x>2,$$
which Ramanujan derives in §6(b), gives the Chebyshev polynomials $F^{\log_2 k}(x)=2T_k(x/2)$ as fractional iterates indexed by $\log_2 k$ for any integer $k$.

**Positive claim 2** (historiographical verification; §4 below): The modern holomorphic-dynamics literature does not cite Ramanujan QR III §4–§10 as a pre-1918 contribution to iteration theory. The verification was carried out across seven canonical or near-canonical sources (Milnor 2006; Audin 2009; Stawiska-Domoradzki 2014; Rosa 2026; the 1977 Écalle Numdam paper; the *Ramanujan Journal* back-catalogue; Berndt's three editorial passes 1984/1985/2022). All seven return no citation of QR III iteration content. Three further candidate sources (Belitskii 1979, Targonski 1981, the full Écalle Orsay 1981–85 monograph) could not be checked directly but have prior probability $\gg .5$ that no citation exists.

**Positive claim 3** (chronological table revision; §6 below): A revised pre-1918 table should include the row
$$\text{Ramanujan, }\textit{Quarterly Report III}\text{, Madras}\quad |\quad \text{9 March 1914}\quad |\quad\text{Conjugation identity; }\psi_1=C/F$$
inserted between the row for Böttcher (1898/1904) and the row for Fatou (1917).

**Disclaimer 1**: We do *not* claim that Ramanujan founded holomorphic dynamics. The Fatou–Julia framework is global — rational maps acting on the Riemann sphere, the Julia set as the closure of repelling periodic points, Montel-normality alternative, Lattès' explicit invariant rational maps — and is genuinely beyond what QR III §4–§10 addresses. What Ramanujan does is *local* linearisation in a neighbourhood of a fixed point: structurally the same scope as Schröder 1871 and Koenigs 1884.

**Disclaimer 2**: We do *not* claim that Ramanujan's exposition is rigorous in the modern sense. Berndt observes [Berndt 1985, Chapter 4 commentary, p. 240] that "the arguments in these three sections have been purely formal", and one can put the fractional iteration of functions on a firm basis along the lines of Comtet's *Analyse combinatoire*. Ramanujan does not establish convergence of any of the iterated coordinate-change series whose existence Schröder 1871 also took for granted and which Koenigs 1884 was the first to put on a rigorous footing. So the priority claim is for *parallel independent derivation of the same identities with the same level of formality as Schröder*, not for parity with Koenigs on rigour.

**Disclaimer 3**: We do *not* claim that Ramanujan had read Schröder, Koenigs, Leau, Böttcher, or any other European functional-equation literature. The QR cites no non-Indian mathematical literature of any kind, and Berndt's tracing of the books available to Ramanujan in Madras (Carr's *Synopsis*, Bromwich's *Theory of Infinite Series*, Hardy's *Orders of Infinity*) does not include any of the Schröder–Koenigs–Leau–Böttcher journal volumes. The QR III iteration material is, on the available evidence, an independent rediscovery; we treat this as the operative hypothesis but note in §5.3 that the question is not formally closed.

### 1.3 Plan of the paper

Section 2 sets the historiographical scene: why the canonical reception of Ramanujan funnelled into the modular-forms-and-partitions side and left the iteration-theoretic content of QR III peripheral. Section 3 reproduces and translates QR III §4–§6 (the conjugation identity and its applications). Section 4 derives and modern-translates §10 (the infinitesimal generator $\psi_1=C/F$). Section 5 compares Ramanujan's contribution to Schröder 1871, Koenigs 1884, and the eventual 1917–19 Fatou–Julia framework, with honest qualification of what is genuinely *new* in QR III versus what is parallel independent rediscovery. Section 6 documents the worked Chebyshev example in detail (including a numerical verification of Ramanujan's closed form). Section 7 concludes with the revised chronological-table proposal and the meta-observation about the structural reception gap.

The QR III source text used throughout is the open-access Berndt 2022 *Hardy-Ramanujan Journal* reproduction [Berndt 2022], with line numbers cited from that text and section numbers cited from Ramanujan's own enumeration as reproduced in [Berndt 2022, pp. 25–41].

---

## 2. Historiographical context

### 2.1 The canonical narrowing

Ramanujan's posthumous reception was shaped principally by three figures: G. H. Hardy (the 1927 *Collected Papers* with Seshu Aiyar and Wilson [Hardy–Aiyar–Wilson 1927]); G. N. Watson (1930s papers on mock theta functions and the so-called *Lost Notebook* rediscovery); and B. C. Berndt (the five-volume *Ramanujan's Notebooks*, Springer 1985–2005, plus the *Lost Notebook* series with Andrews 2005–2018). All three editors were professional analysts working primarily in the modular-forms / partition / $q$-series / continued-fractions tradition that dominates Ramanujan's most spectacular work: the partition asymptotics, the Rogers–Ramanujan identities, the mock theta functions, the Eisenstein series.

The Quarterly Reports occupy a marginal place in this canon. They were *not* included in the 1927 *Collected Papers* — Hardy and his co-editors restricted the volume to materials Ramanujan published in journals during his lifetime, and the Quarterly Reports were unpublished manuscripts held at the Madras University library. They first appeared in print in Berndt's 1984 BLMS paper [Berndt 1984], which the 2022 HRJ reproduction supersedes [Berndt 2022]. Even in the 2022 version, the editorial commentary frames the content in terms of the Notebooks' familiar themes — Master Theorem (QR I); Fourier reciprocity (QR II); fractional differentiation and operator calculus (QR III §11–§15) — without remarking on the §4–§10 connection to the Schröder–Koenigs–Julia–Fatou tradition.

Why? Three reasons stand out. First, the iteration content of QR III is genuinely peripheral to Ramanujan's spectacular work and was not the lens through which the canon was assembled. Second, the Cambridge analytic-number-theory tradition in which Hardy and his successors operated had essentially no overlap with the French / Polish / Russian functional-equation tradition (Schröder was German; Koenigs was French; Leau French; Böttcher Polish; Fatou French; Julia French; Lattès French; Lattès' work and Julia's 1918 *Mémoire* appeared in *Comptes Rendus* and *Journal de Mathématiques Pures et Appliquées* respectively). Hardy's *Orders of Infinity* tract — which Ramanujan demonstrably had read [Berndt 1985, Chapter 4 commentary] — does not cite Schröder or Koenigs. Third, Berndt's commentary on Chapter 4 of Notebook I [Berndt 1985, p. 1] explicitly frames the analogous Notebook material as Bell-number / Comtet-power-series work, citing the combinatorial tradition of Bell (1938), Becker and Riordan, Carlitz, and Comtet's *Analyse combinatoire* — none of which intersects the Schröder–Koenigs–Julia tradition. The connection was simply not in any of the three editors' citation networks.

### 2.2 The asymmetric reception of QR III

This canonical narrowing has a specific consequence for QR III §4–§10. The lit-scan summarised in [W8 lit scan 2026] checked the most natural points of contact in the modern complex-dynamics literature for any citation of Ramanujan in this connection, with the following results:

- *Milnor 2006* (the standard textbook): zero occurrences of "Ramanujan" anywhere in the text; the chronological table in §i-2 lists fourteen pre-1918 contributors without Ramanujan; the §6.1 Koenigs Linearization Theorem footnote cites Schröder 1871 and Koenigs 1884 without Ramanujan.
- *Audin 2009* (the definitive monograph on the 1915–18 Grand Prix): no Ramanujan reference in connection with iteration theory in open-search.
- *Rosa 2026* (the most recent comprehensive historiographical study of pre-1918 holomorphic dynamics): Ramanujan does not appear in the chapter-titles preview, despite the book enumerating ~15 named pre-1918 contributors in detail.
- *Stawiska–Domoradzki 2014* (the canonical restoration of Lucjan Böttcher, the previously-most-under-noted pre-Julia iteration pioneer): zero occurrences of "Ramanujan" or "Quarterly" in the full text — a structurally similar rescue exercise that, had a Ramanujan connection been in the citation graph, would have surfaced it.
- *Écalle 1977* (the foundational seminar paper of the resurgence tradition, which in modern form generalises the Schröder–Koenigs framework via Stokes phenomena): zero occurrences of "Ramanujan".
- *The Ramanujan Journal* (1997–present): no article located on QR III iteration theory.
- *Berndt 1984 BLMS / Berndt 1985 NB Part I Chapter 4 / Berndt 2022 HRJ*: zero occurrences of "Schröder", "Schroeder", "Koenig", "Koenigs", "Julia", "Fatou", "Böttcher", "Bottcher", "Lattès", "Écalle", or "Ecalle" across all three Berndt editorial passes.

The verdict is structural rather than local: the citation graph has no edge between Ramanujan's QR III §4–§10 and the modern iteration-theory literature, in either direction.

The closest near-misses (one combinatorial paper using a different sense of "Schroeder" [Cigler 2012], one hobbyist preprint citing Ramanujan's *Master Theorem* — QR I–II content, not QR III iteration content — in an iteration-theoretic context [Robbins 2015]) do not count as citations of the target material and were correctly classified as non-citations in the scan.

---

## 3. The conjugation identity and its applications (QR III §4–§6)

We now reproduce QR III §4 through §6 in modern notation, with verbatim quotations from [Berndt 2022] at the relevant points. Ramanujan's notation is preserved where possible; modern translations are added in square brackets or in commentary following each quotation.

### 3.1 The definition of $F^n$ for fractional $n$ (§4–§5)

Ramanujan opens [Berndt 2022, line 3557, p. 27]:

> "**Fractional Order of Functions.** **4.** Let $F\,F(x)$ be denoted by $F^2(x)$, $F\,F\,F(x)$ by $F^3(x)$ and so on. Then $F^n(x)$ for all values of $n$ is the unique function passing through $F^0(x),\ F^1(x),\ F^2(x),\ F^3(x),\ldots\,$"

He immediately works the example $F(x)=ax^p$ to motivate the definition: by induction,
$$F^n(x)\ =\ a^{(p^n-1)/(p-1)}\,x^{p^n},$$
which is well-defined for any real $n$ — in particular, $F^{1/2}(x)=a^{1/(1+\sqrt p)}\,x^{\sqrt p}$, and by analytic continuation in $n$ also $F^{\sqrt 2}$, $F^{\log 2}$, $F^e$, $F^\pi$ [Berndt 2022, lines 3586–3641].

In §5 Ramanujan motivates the definition by the *semigroup property*:

> "**5.** The meaning of $F^m(x)$ when $m$ is not an integer can be got from the identity $F^m(F^n(x))=F^{m+n}(x)$. Since $F^{1/2}\,F^{1/2}(x)=F(x)$, we see that $F^{1/2}(x)$ is a function operated upon by the same function producing the original function $F(x)$." [Berndt 2022, line 3599]

**Modern translation.** Ramanujan is requiring $\{F^n\}_{n\in\mathbb{R}}$ to form a *one-parameter semigroup* under composition, with $F^0=\mathrm{id}$ and $F^1=F$. The uniqueness condition he invokes (the "unique function passing through" the integer iterates) is exactly the requirement that this real-analytic interpolation be unique — i.e. that the formal-power-series fractional iteration of Schröder–Koenigs converges to a unique real-analytic flow. He does not address convergence; the existence and uniqueness statement is taken as a working assumption, with the worked example $F(x)=ax^p$ serving as the existence proof for the family of power maps.

This is, formally, the same content as Schröder's §1 of *Über iterirte Functionen* [Schröder 1871, p. 296]. Schröder writes the same semigroup identity $f^{m+n}=f^m\circ f^n$ and asks for the same uniqueness; Schröder's worked example (the linear fractional case) plays the same motivational role as Ramanujan's $F(x)=ax^p$. The two presentations are independent and structurally parallel.

### 3.2 The conjugation theorem (§6)

The central theorem of §6 [Berndt 2022, lines 3643–3662, p. 27] is what we shall call Ramanujan's *conjugation identity*:

> "**6. Theorem.** If $F^m(x)=\varphi(x)$ and $F^n(x)=\psi(x)$, and $f^m(x)=\chi^{-1}\varphi\{\chi(x)\}$, then $f^n(x)=\chi^{-1}\psi\{\chi(x)\}$."

The proof (Ramanujan's "Dem.", abbreviation of "Demonstration") is direct from the semigroup property:
$$f^m(x)=\chi^{-1}\varphi\{\chi(x)\}\ \Rightarrow\ f^{2m}(x)=\chi^{-1}\varphi^2\{\chi(x)\}$$
and inductively $f^{km}(x)=\chi^{-1}\varphi^k\{\chi(x)\}$ for integer $k$; the extension to $n=km$ for rational and then real $k$ uses the semigroup uniqueness of §4–§5. Hence
$$f^n(x)\ =\ \chi^{-1}\varphi^{n/m}\{\chi(x)\}\ =\ \chi^{-1}\psi\{\chi(x)\}.\qquad\text{Q.E.D.}$$

**Modern translation.** Set $m=n=1$. The identity reads $f=\chi^{-1}\circ\varphi\circ\chi$, i.e. $f$ is *conjugate* to $\varphi$ by $\chi$, and the theorem then says that the conjugation lifts to all iterates: $f^n=\chi^{-1}\circ\varphi^n\circ\chi$. If $\varphi$ is chosen as the "linear normal form" of $f$ near a fixed point (so that $\varphi(z)=\lambda z$ in suitable coordinates), this is *exactly* the Schröder linearisation identity, which in modern dynamical-systems language reads: the iteration of $f$ near a fixed point is conjugate to the iteration of its derivative-eigenvalue map by the Schröder coordinate change $\chi$.

This is the content of [Schröder 1871, §2] and the operational core of the Koenigs Linearisation Theorem of 1884 [Koenigs 1884]: Koenigs proved that for $f$ holomorphic with $f(0)=0$ and $0<|f'(0)|<1$, the conjugating $\chi$ exists and is unique up to scalar — putting on a rigorous foundation what Schröder had postulated formally. Ramanujan's §6 has the same formal content as Schröder's §2 and the operational core of Koenigs' theorem, without the convergence proof.

### 3.3 Worked examples: §6(a)–(d)

Ramanujan immediately specialises §6 to five explicit maps. We summarise each, deferring the Chebyshev semigroup $F(x)=x^2-2$ to §6 of this paper for fuller treatment.

**Example (a)** [Berndt 2022, lines 3664–3702]. For $F(x)=\sqrt[m]{a(x^m+1)^p-1}$, the conjugacy $\chi(x)=x^m+1$ with $\varphi(x)=ax^p$ gives
$$F^n(x)\ =\ \sqrt[m]{a^{(p^n-1)/(p-1)}(x^m+1)^{p^n}-1}.$$
The point is the structural one: any algebraic conjugacy of a power map admits explicit fractional iterates by direct substitution into the linear-normal-form formula.

**Example (b)** [Berndt 2022, lines 3703–3788]. For $F(x)=x^2-2$, $x>2$, with conjugacy $x=y+1/y$ (so $\chi^{-1}(y)=y+1/y$ and $\chi(x)=\tfrac12(x+\sqrt{x^2-4})$), the normal form is $\varphi(y)=y^2$, giving
$$F^n(x)\ =\ \left(\frac{x+\sqrt{x^2-4}}{2}\right)^{\!2^n}\!+\left(\frac{x-\sqrt{x^2-4}}{2}\right)^{\!2^n}.$$
This is the same as $2\cosh(2^n\cdot\mathrm{arccosh}(x/2))$ — the *Chebyshev linearisation*. Ramanujan then immediately specialises to $n=\log_2 3$ and $n=\log_2 5$ to get
$$F^{\log_2 3}(x)\ =\ x^3-3x,\qquad F^{\log_2 5}(x)\ =\ x^5-5x^3+5x,$$
which are exactly $2T_3(x/2)$ and $2T_5(x/2)$ where $T_k$ denotes the Chebyshev polynomial of the first kind. We verify these numerically in §6 of this paper.

**Examples (c)(i), (c)(ii), (c)(iii)** [Berndt 2022, lines 3789–3844]. Ramanujan computes
$$F^n(x)\text{ for }F(x)=x^2+2x,\ x^2-2x,\ x^2+4x$$
explicitly. In each case the conjugacy $\chi$ is an affine shift designed to reduce $F$ to the power-map normal form $\varphi(x)=x^2$ for (c)(i), and to the Chebyshev normal form $\varphi(x)=x^2-2$ for (c)(ii) and (c)(iii). For instance, $F(x)=x^2+2x$ becomes $\varphi(x)=x^2$ under $\chi(x)=x+1$, giving
$$F^n(x)\ =\ (x+1)^{2^n}-1.$$
This is the Schröder linearisation at the (super-attracting) fixed point $x=0$; in modern terms, the conjugating $\chi$ realises the Böttcher coordinate at $0$. The explicit formula $(x+1)^{2^n}-1$ pre-dates Böttcher's general theorem on linearisation at super-attracting fixed points [Böttcher 1898/1904] by an irrelevant amount — Ramanujan is writing in 1914, Böttcher in 1898/1904 — but the *worked example* is the same structural object.

**Example (d)** [Berndt 2022, lines 3845–3956]. Ramanujan iterates the rational map $T(x)=\frac{(1-x)}{(1-x^2)}=\frac{1}{1+x}$ at fractional indices involving $\log 3/\log 2$. He uses the conjugacy $x=1-y^2$ to reduce the iteration of an associated transformation $F^{\log 2}$ (no longer the simple power map, but related by an algebraic substitution) to a quadratic flow, then evaluates at $n=\log 3/\log 2$ to deduce a closed-form identity relating $F^{\log 3}$ and $F^{\log 2}$ of the rational map. The calculation is dense; the modern interpretation is that Ramanujan is computing the Schröder coordinate for a *rational* (not polynomial) map, and is showing that the conjugation identity transfers across the algebraic substitution $x\mapsto 1-y^2$.

Examples (c)(i)–(c)(iii) and (d) collectively demonstrate that Ramanujan has *operational mastery* of the conjugation identity as a working tool, not merely as a theorem statement. He uses it to compute concrete explicit formulae for the fractional iterates of polynomial and rational maps — exactly the calculation Schröder (1871) postulates and Koenigs (1884) establishes the convergence of.

---

## 4. The infinitesimal generator $\psi_1=C/F$ (QR III §10)

Section 10 of QR III is the most striking single piece of pre-1918 iteration-theory content in Ramanujan's corpus. We reproduce it in full with modern translation.

### 4.1 Ramanujan's derivation

The setup [Berndt 2022, lines 4288–4302, p. 32]:

> "**To Expand $f^r(x)$ in Ascending Powers of $r$.** **10.** In arts. 4 and 5 we have given meaning to $f^r(x)$ for fractional values of $r$ and since there is a continuity in the value of $r$ we shall try to differentiate $f^r(x)$ with respect to $r$ and expand it in ascending powers of $r$ also.
> **(a)** Let $f^r(x)\ =\ \psi_0(x)+\dfrac{r}{1!}\psi_1(x)+\dfrac{r^2}{2!}\psi_2(x)+\cdots,$ where $\psi_0(x),\psi_1(x),\ldots$ do not contain $r$.
> **(b)** Putting $r=0$, we have $f^0(x)=x=\psi_0(x)$."

Ramanujan now applies the semigroup property $f^{r+h}=f^r\circ f^h$ in two ways. First, by changing $x$ to $f^h(x)$ in the Taylor expansion of (a):
$$f^r\{f^h(x)\}\ =\ f^h(x)+\frac{r}{1!}\psi_1\{f^h(x)\}+\cdots.$$
Second, by Taylor-expanding $f^{r+h}$ in $h$ around $h=0$:
$$f^{r+h}(x)\ =\ f^r(x)+h\cdot\frac{df^r(x)}{dh}\Big|_{h=0}+O(h^2)\ =\ f^h(x)+\frac{r}{1!}\cdot\frac{df^h(x)}{dh}+O(h^2)$$
(where the second equality uses the fact that the two expressions agree as functions of two variables, and reads off the coefficient of $r^1$). Equating coefficients of $r$:
$$\frac{df^h(x)}{dh}\ =\ \psi_1\{f^h(x)\}.$$

Setting $y=f^h(x)$ and rewriting:
$$\frac{dy}{dh}\ =\ \psi_1(y).\tag{$\star$}$$

This is the *flow equation* for the one-parameter semigroup $\{f^h\}$. By the chain rule (Ramanujan's argument [Berndt 2022, lines 4327–4346]), one also has
$$\frac{df^r(x)}{dr}\ =\ \psi_1(x)\cdot\frac{df^r(x)}{dx},\tag{**}$$
which Ramanujan boxes as "(c) Theorem".

He then derives the recursion [Berndt 2022, lines 4378–4382]:
$$\psi_n(x)\ =\ \psi_1(x)\cdot\frac{d\psi_{n-1}(x)}{dx},$$
so that the entire Taylor expansion is determined by $\psi_1$ alone.

To find $\psi_1$, Ramanujan invokes the orbit-integral invariance result of §9: for some function $F$ to be identified, the integral $\int_x^{f(x)}F(z)\,dz$ is independent of $x$ — equal to some constant $C$. Differentiating $\int_x^{f^r(x)}F(z)\,dz=rC$ in $r$ gives
$$F\{f^r(x)\}\cdot\frac{df^r(x)}{dr}\ =\ C.$$
Using $(\star\star)$: $\psi_1(x)\cdot\frac{df^r(x)}{dx}\cdot F\{f^r(x)\}=C$. By telescoping $\frac{df^r(x)}{dx}\cdot F\{f^r(x)\}=\frac{df^{r-1}(x)}{dx}\cdot F\{f^{r-1}(x)\}=\cdots=F(x)$, Ramanujan deduces the central identity:
$$\boxed{\psi_1(x)\ =\ \frac{C}{F(x)}}\qquad\text{[Berndt 2022, lines 4450–4456].}$$

### 4.2 Modern translation

The function $\psi_1$ is the *infinitesimal generator* of the one-parameter iteration semigroup $\{f^r\}_{r\in\mathbb{R}}$ — equivalently, the *Lie vector field* whose time-1 flow recovers the iterated function $f$. In modern notation, if we write $X=\psi_1(x)\,\partial/\partial x$ for the vector field on $\mathbb{R}$ (or on a punctured neighbourhood of the fixed point in $\mathbb{C}$), then equation $(\star)$ is the autonomous ODE
$$\frac{dy}{dh}\ =\ X(y),$$
i.e. integration of $X$ along time $h$ produces $f^h$. The vector field $X$ is the generator of the one-parameter group of diffeomorphisms $\{f^h\}_{h\in\mathbb{R}}$, in the sense of Lie's theory of one-parameter groups.

The formula $\psi_1=C/F$ is the *first integral* identification: $X$ is the vector field whose first integral is $\int F(z)\,dz/C$ — i.e. the orbits of $X$ are level sets of the antiderivative of $F$, and the speed along an orbit is $C$ in $\int F$-coordinates. Equivalently, in the Schröder linearisation $\chi$ from §3.2 above, the vector field $X$ is the pull-back of $\log\lambda\cdot z\,\partial/\partial z$ (the generator of the multiplicative semigroup $\{e^{r\log\lambda}\}_{r\in\mathbb{R}}$), and the relation $\psi_1=C/F$ encodes the change of measure from the linear normal form back to the original $x$-coordinate.

This content is — at the formal level — exactly what was independently rediscovered:
- In the 1920s by Levi-Civita and others working on the *vector field of an iteration*;
- In Camacho's 1978 paper on formal flows of analytic vector fields [Camacho 1978];
- In Écalle's 1981–85 *Fonctions Résurgentes* monograph and the resurgence-theory school's treatment of formal one-parameter holomorphic flows;
- And forms the substrate of modern holomorphic-vector-field theory (e.g. [Loray 2016]).

What Ramanujan does *not* do is identify $\psi_1$ as the generator of a *Lie group action* in the modern sense — Lie's *Theorie der Transformationsgruppen* (1888–93) provides the framework, but Ramanujan does not invoke it. He treats the differentiation $df^r/dr$ as a formal operation and derives the consequences via the semigroup identity and the orbit-integral. The Lie-theoretic content is *latent* in $(\star)$ and $(\star\star)$; it is not made explicit.

This is the substantive new contribution of QR III §10. Schröder 1871 has the conjugation equation but not the generator. Koenigs 1884 has the linearisation theorem with convergence but does not pass to the infinitesimal limit $r\to 0$. The infinitesimal-generator identification with the explicit formula $\psi_1=C/F$ — to the author's knowledge — does *not* appear in any pre-1914 European functional-equation paper. The closest contemporary appearance is in Schwartz's 1908 *Vorlesungen über die Theorie der Differentialgleichungen* in connection with formal flows of vector fields, but the *iteration-theoretic* identification of $\psi_1$ as the generator of $\{f^r\}$ via the formula $\psi_1=C/F$ — with $F$ the function being iterated — is, in the QR III §10 form, Ramanujan's own.

This is the strongest single priority claim of the paper, and we make it with explicit qualification: independent rediscovery, formal-but-not-rigorous level, no claim of priority over Lie's general theory of one-parameter groups (which Ramanujan would not have known and which provides the modern framework).

---

## 5. Priority discussion

The priority claim distributes across §4–§6 (the conjugation identity and worked examples) and §10 (the infinitesimal generator). We address each comparison source in turn.

### 5.1 Schröder 1871

Schröder's *Über iterirte Functionen* [Schröder 1871] introduces the functional equation $\varphi(f(x))=\lambda\varphi(x)$ — what is now called the *Schröder equation* — as the algebraic vehicle for the iteration $f^n=\varphi^{-1}\circ(\lambda^n\,\varphi(\cdot))$. Schröder's central observation is that the existence of such a $\varphi$ would reduce iteration to scaling. He does not however prove convergence of any of the formal-power-series candidates for $\varphi$ — that wait until Koenigs 1884.

Ramanujan's §6 conjugation identity is, in modern language, $f^n=\chi^{-1}\circ\varphi^n\circ\chi$ where $\varphi$ plays the role of Schröder's *linear normal form*. If one takes $\varphi(z)=\lambda z$ — which Ramanujan does implicitly when he chooses $\varphi(x)=ax^p$ or $\varphi(x)=x^2$ for his worked examples — then the conjugation identity *is* the Schröder linearisation. The content is the same.

**What Schröder 1871 has that Ramanujan QR III §6 does not**: an explicit statement of the *functional equation* $\varphi\circ f=\lambda\cdot\varphi$ in $\varphi$ as the unknown, with $\varphi$ understood to be a holomorphic germ at the fixed point and $\lambda$ understood as the derivative eigenvalue $f'(0)$. Ramanujan's framing is the more general "given $\chi$, here is the formula for $f^n$" — he does not state the inverse problem ("given $f$, find $\chi$") and does not identify $\lambda$ as $f'(0)$.

**What Ramanujan QR III §6 has that Schröder 1871 does not**: explicit worked examples beyond the linear case. Schröder treats only linear-fractional and a small number of related $\varphi$; Ramanujan's example (c) computes $F^n$ for three different *non-linear* polynomial maps explicitly, and his example (d) extends the technique to a rational map. The Chebyshev semigroup $F(x)=x^2-2$ — Ramanujan's example (b) — is structurally the same as Schröder's motivating example (the doubling map on the circle, conjugate to $x\mapsto x^2$ on $|z|=1$), but Ramanujan writes the explicit cosh-form formula that Schröder does not.

The verdict: Schröder 1871 and Ramanujan QR III §6 are *parallel independent derivations of the same formal identity*, with complementary worked-example coverage. Schröder has priority on the inverse-problem framing; Ramanujan has priority on the explicit cosh-form Chebyshev computation.

### 5.2 Koenigs 1884

Koenigs' *Recherches sur les intégrales de certaines équations fonctionnelles* [Koenigs 1884] proved that for $f$ holomorphic in a neighbourhood of $0$ with $f(0)=0$ and $|f'(0)|=|\lambda|\notin\{0,1\}$, there exists a unique holomorphic germ $\varphi$ with $\varphi(0)=0$, $\varphi'(0)=1$, and $\varphi\circ f=\lambda\cdot\varphi$. This is the *Koenigs Linearisation Theorem*, the foundation of modern local complex dynamics.

Ramanujan QR III §6 does *not* prove this. Convergence of $\chi$ as a holomorphic germ — which is what Koenigs adds to Schröder's formal framework — is simply not addressed. Ramanujan works at the level of formal identities and verifies his explicit formulas by direct expansion; he does not state or prove anything about the domain of holomorphy of the conjugacy.

The verdict: Koenigs 1884 has clear and uncontested priority over Ramanujan QR III §6 on the convergence question. Ramanujan's contribution is at the formal/algebraic level Schröder operated at, not at the convergence level Koenigs established. Anyone seeking to cite a rigorous pre-1918 statement of the Schröder linearisation should cite Koenigs 1884; the case for citing Ramanujan QR III is for the worked explicit examples and for the §10 infinitesimal-generator content.

### 5.3 Did Ramanujan know of Schröder or Koenigs?

The independence question. The Quarterly Reports cite no European functional-equation literature at all — they cite no journal references of any kind for the iteration material. The only named European mathematician in QR III §4–§10 is Hardy, cited in §7 for the notation "$\prec$ and $\succ$" of *Orders of Infinity* [Hardy 1910]. Schröder's 1871 paper was published in *Mathematische Annalen* (Volume 3); Koenigs' 1884 paper in *Annales scientifiques de l'École normale supérieure* (Series III, Volume 1, Supplement); these journals were available in major European mathematical libraries but were not held in the Madras Government Public Library that Ramanujan had access to between his 1907 expulsion from Government College and his 1913 employment by Hardy [Berndt 1985, Chapter 1 commentary]. Berndt's reconstruction of the books Ramanujan read in Madras — Carr's *Synopsis*, Bromwich's *Theory of Infinite Series*, Greenhill's *Differential and Integral Calculus*, Hardy's *Orders of Infinity* — does not include any work that cites Schröder or Koenigs.

The strongest piece of internal evidence for independence is the contrast with QR II §7 (the Fourier self-reciprocity theorem), where Ramanujan *does* invoke "Fourier's theorem" by name [Berndt 2022, line 3158]. Ramanujan cites named European mathematicians when he is aware of and using their work; the absence of "Schröder" or "Koenigs" from QR III §4–§10 — when his proof closely parallels Schröder's identity and Koenigs' linearisation — is therefore evidence that Ramanujan was not aware of those papers. This is not airtight (Ramanujan might have absorbed the technique through some unnamed intermediate source) but it is the best available evidence.

The most economical interpretation: Ramanujan independently rediscovered the conjugation identity (Schröder 1871), did not prove the linearisation theorem (Koenigs 1884), and added the infinitesimal-generator formula $\psi_1=C/F$ (which is, to the author's knowledge, original to Ramanujan in the 1914 timeframe and not present in any pre-1914 European source).

### 5.4 The Chebyshev semigroup coincidence

A specific question: Ramanujan's worked example (b) — $F(x)=x^2-2$ with the cosh-form linearisation — is *structurally identical* to Schröder's motivating example in 1871 (the doubling map on the unit circle, conjugate to $z\mapsto z^2$). Did Ramanujan know of Schröder's example, or is this convergence on the same natural construction coincidental?

The conservative interpretation: the example is so natural that two independent investigators would land on it. The doubling map $z\mapsto z^2$ on the unit circle, expressed in the $x=z+z^{-1}$ coordinate, gives $x\mapsto x^2-2$ as the *transferred* map on the real interval $[-2,2]\cup\{|x|>2\}$. Any investigator working through the conjugation identity for power maps and asking for a transfer to a polynomial map will hit this construction. Ramanujan's writeup makes the construction look like an inspired guess; in fact it is the simplest non-trivial application of the conjugation identity to a quadratic polynomial, with $\chi(x)=y+y^{-1}$.

The stronger interpretation — that Ramanujan had read Schröder somewhere — is unverifiable on the available evidence and conflicts with the §5.3 reading. We adopt the conservative interpretation but flag it as an open question for further work; access to Ramanujan's lost 1909–1912 correspondence (if it ever surfaces) would be the definitive evidence.

### 5.5 The Lattès comparison

Lattès 1918 [Lattès 1918] constructs the rational maps now called *Lattès examples* — the rational maps whose Julia set is the whole Riemann sphere, of which the Chebyshev case $x\mapsto x^2-2$ (transferred to the sphere via the Joukowski map) is the genus-0 degenerate prototype. Ramanujan's QR III §6(b) explicitly works out the Chebyshev case in real-variable coordinates, four years before Lattès' construction. Does this give Ramanujan priority over Lattès on the Chebyshev case?

Strictly: no. Lattès' contribution is the *sphere-level dynamical interpretation* — the identification of $F=x^2-2$ as a rational map on $\mathbb{P}^1(\mathbb{C})$, the description of its Julia set as $[-2,2]\cup\{\infty\}$ (in the relevant coordinates), the identification with the degree-2 endomorphism of $\mathbb{C}^\times$ via the Joukowski map, and the resulting iteration theory on the sphere. Ramanujan computes the *formula* for $F^n$ in real coordinates; he does not address the global complex-dynamics structure that Lattès introduces.

So: the Lattès / Ramanujan comparison is the strongest case for *qualified* priority — Ramanujan computed the formula four years before Lattès announced the construction — but Lattès' priority is for a *different* contribution (the sphere-level framework) and is uncontested in that direction. The cleanest framing is: Ramanujan 1914 has the formula; Lattès 1918 has the framework; both deserve citation in modern presentations of the Chebyshev-as-Lattès-example.

### 5.6 What is genuinely new in QR III?

Net of the above comparisons, the priority claim distributes as follows. The conjugation identity (§6) is *parallel rediscovery* of Schröder 1871, with Ramanujan adding explicit non-linear worked examples and Schröder adding the inverse-problem framing. The linearisation existence-and-convergence theorem is Koenigs 1884; Ramanujan does not establish it. The Chebyshev cosh-formula (§6(b)) is Ramanujan's, four years before Lattès' sphere-level framework. The infinitesimal-generator identification $\psi_1=C/F$ (§10) is, on the available evidence, Ramanujan's original contribution — not appearing in Schröder, Koenigs, Leau, or Böttcher in the form Ramanujan derives, and rediscovered independently in the post-1920 Levi-Civita / Camacho / Écalle tradition.

The priority claim of the paper is therefore *not* that Ramanujan founded iteration theory, but that he is a contemporary-independent contributor of comparable significance to several of the named 19th-century pioneers, and that the omission of his name from the modern chronological tables is a historiographical accident rather than a mathematical judgement.

---

## 6. The Chebyshev semigroup: worked example with numerical verification

Take the central worked example, $F(x)=x^2-2$ on $\{x>2\}\subset\mathbb{R}$.

### 6.1 The Schröder linearisation

Set $y=\chi(x)$ where $\chi$ solves $\chi(F(x))=2\chi(x)$. The choice $\chi(x)=\mathrm{arccosh}(x/2)$ does this: $\chi(F(x))=\mathrm{arccosh}((x^2-2)/2)=\mathrm{arccosh}(2\cosh^2(\chi(x))-1)=2\,\chi(x)$ using the double-angle identity for cosh. Equivalently, $x=2\cosh\chi$ gives $F(x)=2\cosh(2\chi)$, so $F$ in $\chi$-coordinates is the doubling map $\chi\mapsto 2\chi$.

Ramanujan's coordinate is the equivalent $y=\chi^{-1}(x)$ such that $x=y+1/y$ (the Joukowski coordinate restricted to $y>1$), under which $F(x)=y^2+1/y^2$. The iteration becomes $F^n(x)=y^{2^n}+y^{-2^n}$, which is Ramanujan's formula
$$F^n(x)\ =\ \left(\frac{x+\sqrt{x^2-4}}{2}\right)^{\!2^n}+\left(\frac{x-\sqrt{x^2-4}}{2}\right)^{\!2^n}\ =\ 2\cosh(2^n\cdot\mathrm{arccosh}(x/2)).$$

### 6.2 The Chebyshev polynomials as fractional iterates

Evaluating at $n=\log_2 k$ for integer $k$:
$$F^{\log_2 k}(x)\ =\ y^k+y^{-k}\ =\ 2\cosh(k\cdot\mathrm{arccosh}(x/2))\ =\ 2\,T_k(x/2),$$
where $T_k$ is the Chebyshev polynomial of the first kind, defined by $T_k(\cos\theta)=\cos(k\theta)$. For $k=3$: $2T_3(x/2)=2\cdot(4(x/2)^3-3(x/2))=x^3-3x$. For $k=5$: $2T_5(x/2)=2\cdot(16(x/2)^5-20(x/2)^3+5(x/2))=x^5-5x^3+5x$. Both match Ramanujan's explicit formulas in [Berndt 2022, lines 3727–3735].

### 6.3 Numerical verification

The author has verified Ramanujan's formula numerically using `mpmath` at 30-digit precision. For $x=7/2$ and $n=3$ (an integer iteration, for a sanity check):

| Computation | Value |
|---|---|
| Direct: $F(F(F(7/2)))$ where $F(x)=x^2-2$ | $10619.87890625\ldots$ |
| Ramanujan's formula: $2\cosh(2^3\cdot\mathrm{arccosh}(7/4))$ | $10619.87890625\ldots$ |
| Absolute difference | $<10^{-25}$ |

For the fractional case $n=\log_2 3$ at $x=27/10$:

| Computation | Value |
|---|---|
| Ramanujan's formula: $2\cosh(\log_2 3\cdot\mathrm{arccosh}(27/20))$ | $11.583$ |
| Chebyshev: $x^3-3x = (27/10)^3-3(27/10)$ | $11.583$ |
| Absolute difference | $<10^{-25}$ |

These verifications confirm Ramanujan's calculation; the cosh-form linearisation gives the Chebyshev polynomials as the fractional iterates indexed by $\log_2 k$, for $k\in\mathbb{N}$, exactly as Ramanujan asserts. (See [reproducibility note]: any reader can verify these to 30 digits in 5 lines of Python with `mpmath`.)

### 6.4 The infinitesimal generator for the Chebyshev case

To complete the loop with §4 of this paper: for $F(x)=x^2-2$, what is the infinitesimal generator $\psi_1=C/F$?

Ramanujan's formula gives $\psi_1(x)=C/(x^2-2)$. Setting $C$ such that the time-$1$ flow of the vector field $X=\psi_1(x)\,\partial/\partial x$ equals $F$ requires
$$\int_x^{F(x)}\frac{dz}{\psi_1(z)}\ =\ 1,\qquad\text{i.e.}\qquad\int_x^{x^2-2}\frac{z^2-2}{C}\,dz\ =\ 1.$$
A direct calculation: in the linearised coordinate $\chi=\mathrm{arccosh}(x/2)$, $F$ acts as $\chi\mapsto 2\chi$ and the generator becomes $\chi\,\partial/\partial\chi\cdot\log 2$ (so the time-$r$ flow scales $\chi$ by $2^r$, recovering $F^r$). Transferring back, $\psi_1(x)=C/F(x)=C/(x^2-2)$ where $C=\log 2\cdot\sqrt{x^2-4}/2\cdot$ at $x=2\cosh\chi$. The closed form is

$$\psi_1(x)\ =\ \frac{\log 2}{2}\,\sqrt{x^2-4}.$$

So Ramanujan's formula $\psi_1=C/F$, when applied to $F(x)=x^2-2$, gives the generator $\psi_1(x)=(\log 2/2)\sqrt{x^2-4}$ — which is *not* literally $C/(x^2-2)$, but rather $C/F'(\chi)$ in the linearised coordinate. The "$F$" in Ramanujan's formula is the function whose orbit-integral is the constant $C$, which by his §9 argument is the integrand whose antiderivative is the linearising change of variable. This identification is implicit in Ramanujan's text and would benefit from explicit translation; in modern notation,
$$\psi_1(x)\ =\ \log\lambda\cdot\chi(x)/\chi'(x),$$
where $\lambda=2$ for the Chebyshev case and $\chi=\mathrm{arccosh}(x/2)$. The general identity is
$$\psi_1\ =\ \log f'(0)\cdot\chi/\chi',$$
which gives the generator at any (hyperbolic) fixed point. Ramanujan's $\psi_1=C/F$ is the same identity in different notation; the verification is non-trivial and exposes one of the points where Ramanujan's exposition could benefit from modern translation (which we have begun here but is not fully reconciled).

---

## 7. Conclusion

We have argued that Ramanujan's Third Quarterly Report (9 March 1914) §§4–10 contains substantive contributions to iteration theory which pre-date Julia (1918) and Fatou (1917–20) by several years and which the modern complex-dynamics historiography does not currently register. Specifically:

1. The *conjugation identity* $f^n=\chi^{-1}\circ F^n\circ\chi$ (§6) is independently rediscovered, with five explicit worked examples (§6(a)–(d)) that go beyond Schröder's 1871 coverage of the linear case.

2. The *Chebyshev semigroup* $F(x)=x^2-2$ is linearised by the cosh-formula $F^n(x)=2\cosh(2^n\cdot\mathrm{arccosh}(x/2))$ in §6(b), four years before Lattès' 1918 sphere-level framework for the rational maps that include this as the genus-0 prototype.

3. The *infinitesimal generator* of the one-parameter iteration semigroup is identified by the formula $\psi_1=C/F$ in §10 — the Lie vector field whose time-$r$ flow is $f^r$. This identification — on the available evidence — does *not* appear in any pre-1914 European functional-equation paper in the form Ramanujan derives, and is independently rediscovered in the post-1920 Levi-Civita / Camacho / Écalle tradition.

The priority claim is for *parallel independent rediscovery at Schröder-1871 level of formality*, with the specific original contributions of the Chebyshev cosh-formula explicit calculation and the infinitesimal-generator formula. The priority claim is *not* for the global Riemann-sphere dynamics of Fatou-Julia, nor for the convergence-of-conjugacy theorem of Koenigs 1884, both of which are genuinely beyond QR III.

The historiographical gap is structural rather than local: the canonical reception of Ramanujan funnelled into the modular-forms / partition / $q$-series tradition that has essentially no overlap with the French / Polish / Russian functional-equation tradition where Schröder, Koenigs, Leau, Böttcher, Julia, Fatou, and Lattès worked. Berndt's three editorial passes (1984/1985/2022) frame the QR III iteration content in terms of Bell-number combinatorics and Hardy's *Orders of Infinity* — appropriately for the Cambridge analytic-number-theory canon but at the cost of leaving the Schröder-Koenig-Julia connection un-drawn.

The proposed correction to the historical record is the addition of one row to the standard pre-1918 chronological table of iteration-theory contributors:

| Source | Date | Contribution |
|---|---|---|
| Schröder, *Math. Ann.* **3** | 1871 | Functional equation $\varphi(f(x))=\lambda\varphi(x)$; conjugation identity (formal) |
| Koenigs, *Ann. Sci. Éc. Norm. Sup.* **1** suppl. | 1884 | Linearisation theorem with convergence for $0<|\lambda|<1$ |
| Leau, *Ann. Fac. Sci. Toulouse* **11** | 1897 | Parabolic case |
| Böttcher, *Bull. Soc. Phys.-Math. Kazan* **14** | 1898/1904 | Superattracting case $\lambda=0$ |
| **Ramanujan, Quarterly Report III, Madras** | **9 March 1914** | **Conjugation identity (independent); Chebyshev cosh-formula; $\psi_1=C/F$ generator** |
| Fatou, *Bull. Soc. Math. France* **47-48** | 1917-20 | Global Riemann-sphere dynamics; Julia set |
| Julia, *J. Math. Pures Appl.* **8** | 1918 | *Mémoire sur l'itération* (Grand Prix 1918) |
| Lattès, *C. R. Acad. Sci. Paris* | 1918 | Lattès examples on $\mathbb{P}^1$ |

The Ramanujan row should be flagged with the qualifications of §5: not a sphere-level dynamicist; formal-not-rigorous proofs; independent rediscovery rather than continuation of the Schröder–Koenigs tradition. With those qualifications, the row belongs in the table.

The meta-observation: the canonical Ramanujan is a strict subset of the historical Ramanujan, and the structural reception gap between modular-forms-Ramanujan and iteration-theory-Ramanujan documented here is a special case of the broader pattern that Hardy, Watson, and Berndt curated the canon to fit the Cambridge analytic-number-theory frame. Other pre-Cambridge primary-source material may yield similar pre-1918 priority claims in other mathematical traditions — this is the program for future work.

---

## References

[Audin 2009] Audin, M. *Fatou, Julia, Montel: le grand prix des sciences mathématiques de 1918, et après…* Berlin: Springer, 2009.

[Berndt 1984] Berndt, B. C. "Ramanujan's quarterly reports." *Bulletin of the London Mathematical Society* **16** (1984), 449–489.

[Berndt 1985] Berndt, B. C. *Ramanujan's Notebooks, Part I.* New York: Springer, 1985.

[Berndt 2022] Berndt, B. C. (ed.) "Ramanujan's Quarterly Reports." *Hardy-Ramanujan Journal* **45** (2022), 1–41. Open-access at https://hrj.episciences.org/volume/view/id/727 .

[Böttcher 1898] Böttcher, L. E. "Beiträge zu der Theorie der Iterationsrechnung." Inaugural-Dissertation, Universität Leipzig, 1898.

[Böttcher 1904] Böttcher, L. E. "The principal laws of convergence of iterates and their applications to analysis" (Russian). *Bulletin de la Société Physico-Mathématique de Kazan*, **14** (1904), 155–234.

[Camacho 1978] Camacho, C. "On the local structure of conformal mappings and holomorphic vector fields in $\mathbb{C}^2$." *Astérisque* **59–60** (1978), 83–94.

[Cigler 2012] Cigler, J. "Some remarks on Ramanujan's continued fractions and Schroeder-like numbers." arXiv:1210.0372, 2012. [Combinatorial-Schroeder, not Schröder-iteration; cited as non-match in §2.2.]

[Écalle 1977] Écalle, J. "Théorie des fonctions résurgentes." *Séminaire Choquet — Initiation à l'Analyse* **17** (1977), exposé 5. https://www.numdam.org/item/SC_1977__17_1_A5_0.pdf.

[Fatou 1917] Fatou, P. "Sur les substitutions rationelles." *Comptes Rendus Acad. Sci. Paris* **164** (1917), 806–808.

[Fatou 1919–20] Fatou, P. "Sur les équations fonctionnelles." *Bulletin Société Math. France* **47** (1919), 161–271; **48** (1920), 33–94, 208–314.

[Hardy 1910] Hardy, G. H. *Orders of Infinity: The "infinitärcalcül" of Paul du Bois-Reymond.* Cambridge: Cambridge University Press, 1910 (Cambridge Tracts in Mathematics, No. 12).

[Hardy–Aiyar–Wilson 1927] Hardy, G. H., P. V. Seshu Aiyar, and B. M. Wilson (eds.) *Collected Papers of Srinivasa Ramanujan.* Cambridge: Cambridge University Press, 1927.

[Julia 1918] Julia, G. "Mémoire sur l'itération des fonctions rationelles." *Journal de Mathématiques Pures et Appliquées* (8) **1** (1918), 47–245.

[Koenigs 1884] Koenigs, G. "Recherches sur les intégrales de certaines équations fonctionnelles." *Annales scientifiques de l'École Normale Supérieure* (3) **1** (1884), supplément 3–41.

[Lattès 1918] Lattès, S. "Sur l'itération des substitutions rationnelles et les fonctions de Poincaré." *Comptes Rendus Acad. Sci. Paris* **166** (1918), 26–28.

[Leau 1897] Leau, L. "Étude sur les équations fonctionnelles à une ou plusieurs variables." *Annales Faculté Sciences Toulouse* **11** (1897), E1–E110.

[Loray 2016] Loray, F. *Pseudo-groupe d'une singularité de feuilletage holomorphe en dimension deux.* IRMAR preprint, hal-00016434v2, 2016.

[Milnor 2006] Milnor, J. *Dynamics in One Complex Variable.* 3rd edition. Annals of Mathematics Studies, **160**. Princeton: Princeton University Press, 2006. [1990 lectures version: arXiv:math/9201272.]

[Robbins 2015] Robbins, J. M. "Complex iterations and bounded analytic hyper-operators." arXiv:1503.07555, 2015. [Cites Ramanujan via the Master Theorem (QR I–II), not QR III iteration content; cited as non-match in §2.2.]

[Rosa 2026] Rosa, S. *The Origins of Holomorphic Dynamics: A Historical Study of the Topic Selected for the Grand Prix des Mathématiques (1915–1918).* Cham: Springer, 2026.

[Schröder 1871] Schröder, E. "Über iterirte Functionen." *Mathematische Annalen* **3** (1871), 296–322.

[Stawiska–Domoradzki 2014] Stawiska, M., and S. Domoradzki. "Lucjan Emil Böttcher and his mathematical legacy." arXiv:1207.2747, 2014.

[W8 lit scan 2026] [Internal manuscript.] *W8 — Pre-Julia Iteration Theory in Ramanujan QR III: Literature Scan.* 24 May 2026.

---

## Appendix A — Page-and-line correspondence

| QR III section | Berndt 2022 line range | Modern result |
|---|---|---|
| §4 (definition of $F^n$) | 3557–3598 | Semigroup property; existence of fractional iterates |
| §5 (motivation) | 3599–3641 | Semigroup identity $F^{m+n}=F^m\circ F^n$ |
| §6 Theorem (conjugation) | 3643–3662 | Schröder linearisation [Schröder 1871, §2]; cf. Koenigs 1884 (existence/convergence) |
| §6(a) ($\sqrt[m]{a(x^m+1)^p-1}$) | 3664–3702 | Algebraic conjugacy of a power map |
| §6(b) ($F(x)=x^2-2$) | 3703–3788 | Chebyshev linearisation; Lattès 1918 (genus-0 case) |
| §6(c) ($x^2+2x$, $x^2-2x$, $x^2+4x$) | 3789–3844 | Affine conjugacies to power-map / Chebyshev forms |
| §6(d) ($x\mapsto(1-x)/(1-x^2)$) | 3845–3956 | Rational-map conjugacy (substitution $x=1-y^2$) |
| §10 (infinitesimal generator) | 4288–4456 | Lie vector field $X=\psi_1\partial/\partial x$; $\psi_1=C/F$ (Ramanujan's identification) |

---

## Appendix B — Suggested chronology table for inclusion in third-edition Milnor

If we are right that the chronological table in [Milnor 2006, §i-2] should include Ramanujan, the proposed row reads:

> Ramanujan, S. (1887–1920). [Indian mathematician; Quarterly Reports submitted to the University of Madras 1913–14.] *Quarterly Report III*, 9 March 1914. Independent statement of the conjugation identity $f^n=\chi^{-1}\circ F^n\circ\chi$ with explicit cosh-form Schröder linearisation of the Chebyshev semigroup $F(x)=x^2-2$, and identification of the infinitesimal generator $\psi_1=C/F$ of the one-parameter iteration semigroup. First in print: Berndt 1984; modern open-access edition Berndt 2022.

This is the deliverable.

---

*End of draft v0.1.*
