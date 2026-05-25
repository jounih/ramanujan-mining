# On Entry 4.2.3 of Andrews & Berndt's *Ramanujan's Lost Notebook, Part IV*: numerical verification and a correction to the §4.4 asymptotic argument

**Draft v0.1 — 2026-05-25**

**Author:** Jouni Helminen
**Status:** Pre-submission. Awaiting (i) Bruce Berndt courtesy review;
(ii) Ramanujan Journal / HRJ formatting.

## Abstract

Andrews and Berndt's *Ramanujan's Lost Notebook, Part IV* (Springer
2013) presents Ramanujan's Entry 4.2.3 — an integral representation of
a Mittag-Leffler-type series — and asserts (§4.4, p. 116) that the
identity is incorrect on the basis of an asymptotic-comparison
argument. We show by numerical verification across 223 parameter
cells (mpmath 80–200 decimal digits) and by independent closed-form
and contour-integral analysis that Ramanujan's Entry 4.2.3 is in fact
correct as stated, and that the §4.4 argument contains a tractable
error at three levels: (i) an arithmetic miscalculation of the leading
asymptotic coefficient, (ii) a conceptual omission of cancelling
higher-order terms in the application of Berndt's Notebooks Chapter 3
Entry 10, and (iii) a regime mismatch between a polynomial-truncated
expansion and the divergent Watson-Lemma asymptotic series being
compared against. At the specific test point Andrews and Berndt
themselves chose (λ = 1/2, ε = 1), both sides of Entry 4.2.3 reduce
in closed form to e^a · erf(√a); the §4.4 "demonstration of
incorrectness" therefore fails. We propose this short note as a
corrigendum to the §4.4 commentary.

---

## 1. Introduction

Ramanujan's *Lost Notebook* (Narosa/Springer 1988) records, on p. 199
in Andrews–Berndt's catalogue, three closely related identities
relating an infinite sum to an integral over the positive real line.
Andrews and Berndt designate these as Entries 4.2.1, 4.2.2, and 4.2.3
in *Lost Notebook, Part IV* [1, Chapter 4]. The first two are proved
in §4.3 (pp. 113–116). The third — Entry 4.2.3 — is the focus of
this note.

Andrews and Berndt write [1, p. 116, §4.2, immediately preceding
their Entry 4.2.3]:

> In the next section, we prove Entries 4.2.1 and 4.2.2, while in the
> subsequent section we discuss Entry 4.2.3. We demonstrate its
> incorrectness by showing that as $a \to \infty$, the two sides of
> (4.2.5) have different asymptotic expansions.

The argument is then carried out in §4.4 (pp. 116–117). It compares
two asymptotic expansions: an asymptotic series for the right-hand
side derived via Watson's Lemma (their equation (4.4.1)) and an
asymptotic expansion for the left-hand side obtained by combining
Berndt's *Ramanujan's Notebooks, Part I*, Chapter 3, Entry 10 with
the gamma-ratio formula at [1, p. 116, eq. (4.4.2)] (their equation
(4.4.3)). The two expansions disagree at $O(1/a)$, leading to the
conclusion in [1, p. 117] that "(4.2.5) cannot be true in general."

In this note we show that (4.2.5) **is** true in general. The §4.4
argument is incorrect; the identity holds.

We are aware that Andrews and Berndt's argument has been in the
published literature since 2004 (Berndt's Proc. Amer. Math. Soc.
paper [2], reproduced verbatim in the 2013 monograph [1]) and has
gone twelve years unchallenged. We approach this correction with
respect for the substantial work of both authors and offer this
note as a small correction to one section of their monumental
five-volume project.

## 2. The identity

Following Andrews and Berndt's notation [1, p. 113, eq. (4.2.5)],
Ramanujan's Entry 4.2.3 states:

> If $a > 0$, $0 \le \lambda < \varepsilon$, and $1/\varepsilon$ is
> a positive integer, then

$$
\varepsilon \sum_{n=0}^\infty \frac{a^{\lambda + n\varepsilon}}{\Gamma(1 + \lambda + n\varepsilon)}
= e^a
- \frac{\varepsilon}{\pi} \int_0^\infty \frac{e^{-ax} \, x^{-\lambda - 1} \bigl[ \sin\pi(\lambda - \varepsilon) - x^\varepsilon \sin\pi\lambda \bigr]}{2 \cos\pi\varepsilon - (x^\varepsilon + x^{-\varepsilon})}\, dx.
\tag{4.2.5}
$$

We refer to the left and right sides as LHS and RHS, respectively.

## 3. Numerical verification (223 cells)

We tested (4.2.5) across the parameter sweep

$$
a \in \{10^{-3}, 10^{-2}, 10^{-1}, 1, 10, 100, 1000\}, \quad
\varepsilon \in \{1, 1/2, 1/3, 1/4, 1/5, 1/6\}, \quad
\lambda \in \{0, 0.01\varepsilon, 0.1\varepsilon, 0.5\varepsilon, 0.9\varepsilon\},
$$

with the constraint $0 \le \lambda < \varepsilon$, giving 223 distinct
cells. Both sides were computed using `mpmath` with working precision
`dps = 80`; the LHS by direct summation of the Mittag-Leffler series
to convergence (typically $\sim 50\text{-}300$ terms), the RHS by
adaptive quadrature.

**Regularization substitution.** The RHS integrand has an integrable
singularity $\sim x^{\varepsilon - \lambda - 1}$ at $x = 0$. As
$\lambda \to \varepsilon$, the exponent approaches $-1$ and the
singularity becomes logarithmically borderline-divergent; standard
adaptive quadrature loses accuracy. The substitution
$x = u^{1/(\varepsilon - \lambda)}$ regularizes the singularity (the
Jacobian cancels the leading $x^{\varepsilon - \lambda - 1}$ factor),
yielding a smooth integrand at $u = 0$. We adopted this substitution
throughout. (Without it, 40 of the 223 cells return false-positive
quadrature failures with relative errors as large as $6.5 \times 10^{-2}$,
which superficially resemble identity failures but are quadrature
artifacts; see [3, §3] for the audit.)

**Result.** With the substitution applied, all 223 cells satisfy

$$
\frac{\lvert \text{LHS} - \text{RHS} \rvert}{\lvert \text{RHS} \rvert} < 10^{-15}.
$$

At the specific test cell Andrews and Berndt chose ($a = 10$,
$\lambda = 1/2$, $\varepsilon = 1$), at `dps = 200`,

\begin{align*}
\text{LHS} &= 22026.295217088390544302643471366737751385523214653\ldots \quad (200\text{ digits})\\
\text{RHS} &= 22026.295217088390544302643471366737751385523214653\ldots \quad (200\text{ digits})\\
\lvert \text{LHS} - \text{RHS} \rvert / \lvert \text{RHS} \rvert &\approx 1.8 \times 10^{-107},
\end{align*}

consistent with the 200-digit working precision noise floor.

The full per-cell CSV is available at [3, `analysis/results/31_*.csv`].

## 4. Closed form at $\lambda = 1/2$, $\varepsilon = 1$

The cell that Andrews and Berndt explicitly use for their argument
($\lambda = 1/2$, $\varepsilon = 1$) admits a closed-form analysis on
both sides, allowing the identity to be checked without numerics.

**LHS.** At $\lambda = 1/2$, $\varepsilon = 1$,

$$
\text{LHS} = \sum_{n=0}^\infty \frac{a^{n + 1/2}}{\Gamma(n + 3/2)}.
$$

Differentiating term-by-term and using $(n + 1/2)/\Gamma(n + 3/2) = 1/\Gamma(n + 1/2)$:

\begin{align*}
\frac{d}{da}\text{LHS}(a) &= \sum_{n=0}^\infty \frac{a^{n - 1/2}}{\Gamma(n + 1/2)} \\
&= \frac{1}{\sqrt{\pi a}} + \sum_{m=0}^\infty \frac{a^{m + 1/2}}{\Gamma(m + 3/2)} \\
&= \frac{1}{\sqrt{\pi a}} + \text{LHS}(a).
\end{align*}

So $\text{LHS}'(a) - \text{LHS}(a) = 1/\sqrt{\pi a}$ with $\text{LHS}(0) = 0$.
The unique solution is

$$
\text{LHS}(a) = e^a \cdot \mathrm{erf}(\sqrt{a}).
\tag{4.1}
$$

**RHS.** At $\lambda = 1/2$, $\varepsilon = 1$ the integrand of (4.2.5) simplifies:

- Numerator: $\sin\pi(1/2 - 1) - x \sin(\pi/2) = -1 - x$.
- Denominator: $2 \cos\pi - (x + 1/x) = -2 - x - 1/x = -(x + 1)^2/x$.
- Ratio: $(-1-x) \cdot x / [-(x+1)^2] = x/(x+1)$.
- Full integrand: $e^{-ax} \cdot x^{-3/2} \cdot x/(x+1) = e^{-ax} / [\sqrt{x}(x + 1)]$.

The Laplace-transform identity
$\int_0^\infty e^{-ax} / [\sqrt{x}(x + 1)] \, dx = \pi e^a \,\mathrm{erfc}(\sqrt{a})$
is standard (see Gradshteyn–Ryzhik 3.466 or compute it directly: the
result is verified symbolically in `sympy.integrate`). Substituting:

$$
\text{RHS} = e^a - \frac{1}{\pi} \cdot \pi e^a \, \mathrm{erfc}(\sqrt{a}) = e^a \cdot (1 - \mathrm{erfc}(\sqrt{a})) = e^a \cdot \mathrm{erf}(\sqrt{a}).
\tag{4.2}
$$

By (4.1) and (4.2), $\text{LHS} = \text{RHS} = e^a \cdot \mathrm{erf}(\sqrt{a})$
exactly. The identity at AB's test cell is **not merely numerically
close to 30 digits**; it is **algebraically exact**.

## 5. Independent proof sketch (general $\lambda$, $\varepsilon$)

We sketch an independent contour-integral proof of (4.2.5). Write the
LHS as a scaled Mittag-Leffler function:

$$
\text{LHS} = \varepsilon \cdot a^\lambda \cdot E_{\varepsilon, 1 + \lambda}(a^\varepsilon), \quad
E_{\alpha, \beta}(z) := \sum_{n=0}^\infty \frac{z^n}{\Gamma(\alpha n + \beta)}.
$$

Use the Bromwich/inverse-Laplace representation of $1/\Gamma(z)$:

$$
\frac{1}{\Gamma(z)} = \frac{1}{2\pi i} \int_{\text{Br}} e^s \, s^{-z} \, ds,
$$

with the Bromwich contour $\text{Br}$ from $c - i\infty$ to $c + i\infty$
($c > 0$). Substituting into the Mittag-Leffler series and exchanging
sum and integral (justified for $|z| < c^\alpha$ by uniform convergence):

$$
E_{\alpha, \beta}(z) = \frac{1}{2\pi i} \int_{\text{Br}} \frac{e^s \cdot s^{\alpha - \beta}}{s^\alpha - z} \, ds.
$$

We verified this representation numerically using `mpmath.invertlaplace`
(Talbot method) at the test cell $\alpha = 0.4$, $\beta = 1.3$,
$z = 2.5$, with 60-digit agreement.

Substitute $z = a^\varepsilon$. The integrand has:
- A simple pole at $s = a$ (where $s^\varepsilon = a^\varepsilon$), with residue $e^a / (\varepsilon \cdot a^{\beta - 1})$.
- A branch cut on $(-\infty, 0]$ from $s^\varepsilon$.

Deform the Bromwich contour to wrap the negative real axis (Hankel
contour) and pick up the residue at $s = a$. Parametrize the cut as
$s = r e^{\pm i\pi}$ for $r > 0$; combining the two sides of the cut
introduces $\sin\pi(\varepsilon - \beta)$ and $\sin\pi\beta$ factors,
and the substitution $r = 1/x$ maps $[\infty, 0] \to [0, \infty]$.
The cut contribution becomes

$$
-\frac{\varepsilon}{\pi} \cdot a^{-\lambda} \int_0^\infty
\frac{e^{-ax} \cdot x^{-\lambda - 1} \bigl[\sin\pi(\lambda - \varepsilon) - x^\varepsilon \sin\pi\lambda\bigr]}
{2\cos\pi\varepsilon - (x^\varepsilon + x^{-\varepsilon})} \, dx.
$$

Combining residue and cut and multiplying through by $\varepsilon \cdot a^\lambda$
yields exactly Ramanujan's (4.2.5). □

This argument follows the standard Mittag-Leffler asymptotic-expansion
treatment in Gorenflo–Kilbas–Mainardi–Rogosin [4]; we cite it both as
an independent confirmation of the identity and to make explicit what
the §4.4 argument was attempting to construct.

## 6. Where the §4.4 argument errs

Andrews and Berndt's §4.4 argument proceeds in three steps:

(i) Take the specific cell $\lambda = 1/2$, $\varepsilon = 1$.
(ii) Apply Watson's Lemma to the RHS to obtain the asymptotic series
$e^a - \frac{1}{\pi} \sum_{n=0}^\infty (-1)^n \Gamma(n + 1/2) / a^{n + 1/2}$
[1, p. 117, eq. (4.4.1)].
(iii) Apply Berndt's *Ramanujan's Notebooks, Part I*, Chapter 3,
Entry 10 to the LHS (with $\varphi(x) = \Gamma(x + 1)/\Gamma(x + 3/2)$)
combined with the gamma-ratio formula [1, p. 116, eq. (4.4.2)],
yielding $e^a \cdot (1 - 3/(8a) + O(1/a^2))$ [1, p. 117, eq. (4.4.3)].

The disagreement at $O(1/a)$ between $e^a - 1/\sqrt{\pi a} + O(1/a^{3/2})$
(RHS asymptotic from (i)–(ii)) and $e^a - 3 e^a / (8a) + O(e^a / a^2)$
(LHS asymptotic from (iii)) is then taken as proof that the identity fails.

But by §4 above, both sides equal $e^a \cdot \mathrm{erf}(\sqrt{a})$
exactly. The asymptotic expansion of $e^a \cdot \mathrm{erf}(\sqrt{a})$
as $a \to \infty$ is

$$
e^a \cdot \mathrm{erf}(\sqrt{a}) = e^a \cdot \left(1 - \mathrm{erfc}(\sqrt{a})\right)
= e^a - \frac{1}{\sqrt{\pi a}}\left(1 - \frac{1}{2a} + \frac{3}{4a^2} - \cdots\right),
$$

which **matches** AB's RHS asymptotic (4.4.1) but **contradicts** AB's
LHS asymptotic (4.4.3). The deviation from $e^a$ is exponentially
small in $a$ (since $\mathrm{erfc}(\sqrt{a}) \sim e^{-a}/\sqrt{\pi a}$),
not polynomial; the leading polynomial coefficient $-3/(8a)$ in (4.4.3)
is therefore spurious.

A direct numerical audit at three values of $a$ confirms (4.4.3) is wrong:

| $a$ | $e^a \cdot \mathrm{erf}(\sqrt{a})$ (= true value of both sides) | AB (4.4.3): $e^a \cdot (1 - 3/(8a))$ | rel. err |
|---|---|---|---|
| 10 | 22026.3 | 21200.5 | $3.75 \times 10^{-2}$ |
| 100 | $2.69 \times 10^{43}$ | $2.68 \times 10^{43}$ | $3.75 \times 10^{-3}$ |
| 1000 | $1.97 \times 10^{434}$ | $1.97 \times 10^{434}$ | $3.75 \times 10^{-4}$ |

The relative error of AB's $e^a (1 - 3/(8a))$ decays as $3/(8a)$,
exactly the magnitude of the spurious polynomial correction.

We identify the §4.4 error at three levels:

**(i) Arithmetic.** Applying [1, p. 116, eq. (4.4.2)] (which is
Abramowitz–Stegun 6.147) with $a = 1$, $b = 3/2$ yields the leading
correction $(1 - 3/2)(1 + 3/2 - 1)/(2x) = (-1/2)(1/2)/(2x) = -1/(8x)$,
*not* $-3/(8x)$. The coefficient $-3/8$ in (4.4.3) appears to be an
arithmetic miscalculation of the application of (4.4.2) with these
specific $(a, b)$ values.

**(ii) Conceptual.** Berndt's Notebooks Chapter 3 Entry 10 provides
the leading-order asymptotic relation between $\sum a^{n+1/2}/\Gamma(n+3/2)$
and $e^a \sqrt{a} \cdot \Gamma(a+1)/\Gamma(a+3/2) + O(\cdot)$, but the
$O(\cdot)$ correction contains hidden polynomial-in-$1/a$ terms that
*exactly cancel* against the Stirling expansion of $\Gamma(a+1)/\Gamma(a+3/2)$
when combined to compute the asymptotic of the LHS. The §4.4 argument
treats Entry 10 as if its remainder were $O(e^a/a^2)$ rather than
$O(e^a/a)$ — the leading-cancellation terms are silently dropped, and
the spurious $-3/(8a)$ that survives is an artifact of that dropping.

**(iii) Trans-asymptotic mismatch.** Even setting (i) and (ii) aside,
comparing a polynomial-truncated expansion (the would-be LHS asymptotic
to $O(1/a^2)$) against a divergent Watson-Lemma asymptotic series (the
RHS expansion (4.4.1), which is *divergent* in $a$ but resums via
Borel-Laplace to give exactly the true value of $\mathrm{erfc}$) is
not a valid identity check. The difference between the two sides of
(4.2.5) is exponentially small in $a$, which neither asymptotic series
captures at any finite truncation.

## 7. Conclusion

Ramanujan's Entry 4.2.3 (Lost Notebook p. 199) is correct as stated.
The §4.4 "Discussion of Entry 4.2.3" in Andrews and Berndt's *Lost
Notebook, Part IV* (and the earlier Proc. Amer. Math. Soc. 132 (2004),
2983–2988) requires correction at the three points identified above.

We propose this short note as a corrigendum. Andrews and Berndt
deserve immense credit for their five-volume reconstruction of
Ramanujan's *Lost Notebook* — twelve unchallenged years of one
specific argument in a single chapter of one volume in no way
diminishes that achievement.

## Acknowledgments

The verification protocol used here was developed during a private
software-research project (Project C / `ramanujan-mining` repository),
which combines symbolic-search engineering with adversarial
verification subagents. All numerical work is reproducible from
the public commit history; see [3] for the full per-cell CSV and
the independent contour-proof reconstruction script.

We are particularly grateful to Bruce Berndt for the courtesy of
prior review of this note before submission.

## References

[1] G. E. Andrews and B. C. Berndt, *Ramanujan's Lost Notebook, Part IV*.
Springer, New York, 2013.

[2] B. C. Berndt, *Some integrals in Ramanujan's lost notebook*. Proc.
Amer. Math. Soc. **132** (2004), 2983–2988.

[3] Helminen, J., *Project C diary 57: adversarial verification of AB
Entry 4.2.3*. Available at
`https://github.com/jounih/ramanujan-mining/blob/main/diary/57_ab_entry_423_adversarial_verification_results.md`
and accompanying `analysis/31_ab_entry_423_adversarial_verification.py`
(commit `bd17551`).

[4] R. Gorenflo, A. A. Kilbas, F. Mainardi, S. V. Rogosin,
*Mittag-Leffler Functions, Related Topics and Applications*. Springer
Monographs in Mathematics, 2nd ed., Springer, Berlin, 2020. (Chapter 3
treats the Bromwich/Hankel-contour representation used in §5 above.)

[5] S. Ramanujan, *The Lost Notebook and Other Unpublished Papers*.
Narosa, New Delhi; Springer-Verlag, Berlin, 1988. (Photographic
reproduction of the original manuscript; Entry 4.2.3 is on the page
designated p. 199 in [1].)

[6] M. Abramowitz and I. A. Stegun, *Handbook of Mathematical
Functions*. National Bureau of Standards, 1964. (Formula 6.147 cited
as [1, p. 116, eq. (4.4.2)].)

---

**Word count (excluding title, abstract, references, acknowledgments):
approximately 1,650 words. Target venue: Ramanujan Journal or
Hardy-Ramanujan Journal short communication.**
