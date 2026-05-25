# An explicit closed-form parameterization of the 4-divisor $E_2$ Lambert annihilator at squarefree composite level: autonomous LLM rediscovery

**Author:** Jouni Helminen
**Date:** 2026-05-25
**Status:** Expository draft v0.1
**Subject classification:** 11F11 (modular forms), 11F20 (Eisenstein series), 11M36 (Lambert series), 68T20 (problem solving, control methods)

## Abstract

We give an explicit closed-form parameterization of the unique (up to scale) linear relation among the four Lambert "conjugate-pair blocks"
$$T_d(\alpha,\beta) := d\,\alpha\,L(d\alpha) + \frac{\beta}{d}\,L\!\left(\frac{\beta}{d}\right), \qquad d \mid N, \qquad L(x) := \sum_{n \ge 1} \frac{n}{e^{2nx}-1},$$
on the hyperbola $\alpha\beta = \pi^2$ at squarefree composite level $N = pq$ with distinct primes $p,q$. With $g := \gcd(pq-1, q-p)$, $\delta := (q-p)/g$, and $m := (pq-1)/g$, the coefficient vector is
$$(c_1, c_p, c_q, c_{pq}) = (-\delta,\; m,\; -m,\; \delta).$$
The derivation requires only the Hardy-Ramanujan-Berndt base identity (1916) plus five lines of Gaussian elimination on a $3 \times 4$ rational system. The underlying structural fact — that exactly one linear relation must exist — is a consequence of the classical dimension formula $\dim E_2(\Gamma_0(pq)) = 3$ for the Eisenstein subspace of weight-$2$ modular forms at squarefree composite level. We verify the formula numerically across 18 instances to relative error $\le 10^{-100}$ at mpmath precision $200$ digits, map structural extensions (the formula is unique at $N = pq$, non-unique at $N = pqr$ and $N = p^2 q$, and does not extend to $N = p^2$), and offer the note as both a useful explicit parameterization and as an instance of autonomous rediscovery of classical material by an LLM-driven symbolic-search engine.

**Keywords:** Lambert series, Eisenstein series, $E_2$ quasi-modular form, level $\Gamma_0(N)$, Hardy-Ramanujan-Berndt identity, autonomous mathematical rediscovery.

---

## 1. Introduction

In their 1916 paper *Asymptotic formulae in combinatory analysis* [1, eq. (1.55)], Hardy and Ramanujan recorded the following identity, equivalent to the modular transformation law for the weight-$2$ Eisenstein series $E_2$: for $\alpha,\beta > 0$ with $\alpha\beta = \pi^2$,
$$\alpha L(\alpha) + \beta L(\beta) = \frac{\alpha + \beta}{24} - \frac{1}{4}, \tag{1}$$
where $L(x) := \sum_{n\ge1} n/(e^{2nx}-1)$ is the standard Lambert series. Berndt's commentary in *Ramanujan's Notebooks Part II* [2, Ch. 14, Entry 27(iii)] traces this identity to Ramanujan's second notebook and connects it directly to the $E_2$ inversion law
$$E_2(-1/\tau) = \tau^2 E_2(\tau) + \frac{6\tau}{\pi i}, \tag{2}$$
via the substitution $\tau = i\alpha/\pi$ and the standard $q$-expansion $E_2(\tau) = 1 - 24\sum_{n\ge 1} n q^n / (1-q^n)$ with $q = e^{2\pi i \tau}$.

A natural question is: given a level $N$, what is the dimension of the linear-relation space spanned by the "conjugate-pair blocks"
$$T_d(\alpha,\beta) := d\,\alpha\,L(d\alpha) + \frac{\beta}{d}\,L\!\left(\frac{\beta}{d}\right) \tag{3}$$
indexed by $d \mid N$? For $N = 1$ there is one block and identity (1) determines its value but gives no annihilator. For $N = p$ prime, there are two blocks $\{T_1, T_p\}$ but identity (1) applied at the two conjugate pairs $(\alpha,\beta)$ and $(p\alpha, \beta/p)$ produces no non-trivial linear relation (both blocks are affine in $(\alpha,\beta)$ with linearly independent coefficient vectors).

The first non-trivial case is therefore $N = pq$ with $p \ne q$ both prime: four blocks indexed by $d \in \{1, p, q, pq\}$. **The main result of this note is that this case admits exactly one non-trivial linear relation, with explicit closed-form coefficients.**

**Theorem 1.** *Let $p < q$ be distinct primes. With $g := \gcd(pq-1, q-p)$, $\delta := (q-p)/g$, and $m := (pq-1)/g$, the unique (up to scale) integer-lowest-height annihilator is*
$$-\delta\,T_1 + m\,T_p - m\,T_q + \delta\,T_{pq} = 0. \tag{4}$$

The remainder of this note is an exposition of (4): we derive it in five lines (Section 2), connect it to the classical $E_2$ Eisenstein-subspace dimension formula (Section 3), tabulate eighteen numerically verified instances (Section 4), map its structural extensions to richer divisor sets (Section 5), and close with a provenance note on how the formula was rediscovered (Section 6).

The underlying mathematics is entirely classical. The fact that exactly one such relation must exist at $N = pq$ follows immediately from $\dim E_2(\Gamma_0(pq)) = 3$. The explicit $\gcd(pq-1, q-p)$ parameterization for the integer-lowest-height representative may not appear in this form in the standard references; if it does, we have not located it. The note is offered both as a convenient explicit form and as a worked example of LLM-assisted autonomous rediscovery of a classical structural identity.

---

## 2. Closed-form coefficients

### 2.1 The five-line derivation

Identity (1) collapses each conjugate-pair block to a three-parameter affine function of $(\alpha,\beta)$ alone. Substituting the conjugate pair $(d\alpha, \beta/d)$ into (1) — which is permissible because $d\alpha \cdot \beta/d = \alpha\beta = \pi^2$ — we obtain
$$T_d(\alpha,\beta) = \frac{d\alpha + \beta/d}{24} - \frac{1}{4} = \frac{d\,\alpha}{24} + \frac{\beta}{24\,d} - \frac{1}{4}. \tag{5}$$

A linear combination $\sum_{d \mid pq} c_d T_d$ therefore equals
$$\frac{\alpha}{24}\sum_{d} d\,c_d + \frac{\beta}{24}\sum_{d} \frac{c_d}{d} - \frac{1}{4}\sum_d c_d. \tag{6}$$

The combination vanishes identically in $(\alpha,\beta)$ iff the three coefficient sums all vanish:
$$\sum_d c_d = 0, \qquad \sum_d d\,c_d = 0, \qquad \sum_d \frac{c_d}{d} = 0. \tag{7}$$

With $d \in \{1, p, q, pq\}$ and unknowns $(c_1, c_p, c_q, c_{pq})$, this is a $3 \times 4$ rational linear system. Five lines of Gaussian elimination solve it:

1. $E_2 - E_1$: $\; (p-1)c_p + (q-1)c_q + (pq-1)c_{pq} = 0$.
2. $-pq(E_3 - E_1)$: $\; q(p-1)c_p + p(q-1)c_q + (pq-1)c_{pq} = 0$.
3. Step 1 $-$ Step 2: $\; -(p-1)(q-1)(c_p + c_q) = 0$, so $c_q = -c_p$.
4. Substituting in Step 1: $(pq-1)c_{pq} = (q-p)\,c_p$, i.e. $m\,(q-p) = \delta\,(pq-1)$ with $c_p =: m$ and $c_{pq} =: \delta$.
5. Substituting in $E_1$ with $c_q = -c_p$: $c_1 = -c_{pq} = -\delta$.

The integer-lowest-height representative is then obtained by dividing through by $g := \gcd(pq-1, q-p)$, yielding $\delta = (q-p)/g$, $m = (pq-1)/g$, and the coefficient vector $(c_1, c_p, c_q, c_{pq}) = (-\delta, m, -m, \delta)$ as claimed.

This completes the proof of Theorem 1. $\square$

### 2.2 Worked example: $N = 33 = 3 \cdot 11$

Here $p = 3$, $q = 11$, so $q - p = 8$, $pq - 1 = 32$, and $g = \gcd(32, 8) = 8$. Therefore $\delta = 8/8 = 1$ and $m = 32/8 = 4$, giving
$$-T_1(\alpha,\beta) + 4\,T_3(\alpha,\beta) - 4\,T_{11}(\alpha,\beta) + T_{33}(\alpha,\beta) = 0. \tag{8}$$

Expanding the blocks explicitly:
$$\alpha\bigl[-L(\alpha) + 12\,L(3\alpha) - 44\,L(11\alpha) + 33\,L(33\alpha)\bigr] + \beta\bigl[-L(\beta) + \tfrac{4}{3}\,L(\beta/3) - \tfrac{4}{11}\,L(\beta/11) + \tfrac{1}{33}\,L(\beta/33)\bigr] = 0.$$

Numerically: at the canonical cell $\alpha = 1$, $\beta = \pi^2$, the left-hand side evaluates to magnitude $\le 10^{-199}$ at mpmath working precision $200$ digits, against blocks of magnitude $\sim 10^{-1}$ — relative error $\le 10^{-199}$.

---

## 3. Connection to classical modular forms

### 3.1 The dimension formula

For squarefree $N = q_1 q_2 \cdots q_t$ with $t$ distinct prime factors, the Eisenstein subspace of weight-$2$ modular forms on $\Gamma_0(N)$ has dimension
$$\dim E_2(\Gamma_0(N)) = 2^t - 1. \tag{9}$$

This is a standard fact; see Diamond-Shurman [3, §3.5] or Stein [4, Ch. 5]. For $t = 2$ (the squarefree composite case $N = pq$) this gives $\dim E_2(\Gamma_0(pq)) = 3$.

The four functions $\{E_2(\tau), E_2(p\tau), E_2(q\tau), E_2(pq\tau)\}$ are weight-$2$ Eisenstein-style forms on $\Gamma_0(pq)$ (each $E_2(d\tau)$ is a quasi-modular form on $\Gamma_0(d) \supseteq \Gamma_0(pq)$, and the standard "old form" construction places it in the Eisenstein subspace of $M_2(\Gamma_0(pq))$ after subtracting the appropriate quasi-modular anomaly; see [3, §5.6]). Because four candidate forms live in a three-dimensional space, they must satisfy at least one linear relation. The argument of Section 2 — which used only identity (1), not the Eisenstein-subspace framework — shows that the linear-relation space is exactly one-dimensional.

The LMFDB database [5] confirms the dimension count at $N = 33$: the space $M_2(\Gamma_0(33))$ has total dimension $9$, cuspidal subspace dimension $6$, and Eisenstein subspace dimension $3$.

### 3.2 The Hardy-Ramanujan-Berndt identity in this light

Identity (1) is precisely the manifestation, at the level of one conjugate pair of Lambert blocks, of the transformation law (2) for $E_2$. The "anomaly" $6\tau/(\pi i)$ in (2) becomes the constant correction $-1/4$ and the linear piece $(\alpha + \beta)/24$ in (1). The fact that this anomaly is *itself a polynomial of low degree in $(\alpha, \beta)$* — specifically of degree at most one — is what reduces the four-divisor annihilator equation to only three linear constraints (Section 2.1, Equation (7)), and hence to a kernel of dimension $4 - 3 = 1$ in the generic case.

Said differently: the Hardy-Ramanujan-Berndt identity is the dimension reduction $\dim E_2(\Gamma_0(pq)) = 3$ in disguise, working at the level of Lambert summands rather than modular forms.

---

## 4. Numerical verification

We verified identity (4) across eighteen instances using `mpmath` at working precision $200$ digits, evaluating the left-hand side at five cells on the hyperbola $\alpha\beta = \pi^2$ chosen to stress the formula at small $\alpha$, large $\alpha$, and the symmetric point $\alpha = \beta = \pi$. Strict acceptance bar: relative error $\le 10^{-100}$, where the relative error is measured against $\max_d |c_d \cdot T_d|$ (the cancellation scale).

The table below summarizes the seven "main" instances plus eleven adversarial edge cases.

| $N$ | $(p, q)$ | Coefficients $(c_1, c_p, c_q, c_{pq})$ | $g, \delta, m$ | Worst rel-err / 5 cells |
|---|---|---|---|---|
| $33$ | $(3, 11)$ | $(-1, 4, -4, 1)$ | $8, 1, 4$ | $\le 10^{-199}$ |
| $35$ | $(5, 7)$ | $(-1, 17, -17, 1)$ | $2, 1, 17$ | $2.76\times 10^{-200}$ |
| $51$ | $(3, 17)$ | $(-7, 25, -25, 7)$ | $2, 7, 25$ | $2.85\times 10^{-200}$ |
| $65$ | $(5, 13)$ | $(-1, 8, -8, 1)$ | $8, 1, 8$ | $4.42\times 10^{-200}$ |
| $77$ | $(7, 11)$ | $(-1, 19, -19, 1)$ | $4, 1, 19$ | $1.27\times 10^{-200}$ |
| $87$ | $(3, 29)$ | $(-13, 43, -43, 13)$ | $2, 13, 43$ | $1.99\times 10^{-199}$ |
| $95$ | $(5, 19)$ | $(-7, 47, -47, 7)$ | $2, 7, 47$ | $4.88\times 10^{-200}$ |
| $115$ | $(5, 23)$ | $(-3, 19, -19, 3)$ | $6, 3, 19$ | $1.07\times 10^{-199}$ |
| $143$ | $(11, 13)$ | $(-1, 71, -71, 1)$ | $2, 1, 71$ | $1.93\times 10^{-200}$ |
| $323$ | $(17, 19)$ | $(-1, 161, -161, 1)$ | $2, 1, 161$ | $6.99\times 10^{-134}$ |
| $187$ | $(11, 17)$ | $(-1, 31, -31, 1)$ | $6, 1, 31$ | $9.60\times 10^{-200}$ |
| $391$ | $(17, 23)$ | $(-1, 65, -65, 1)$ | $6, 1, 65$ | $3.46\times 10^{-110}$ |
| $6$ | $(2, 3)$ | $(-1, 5, -5, 1)$ | $1, 1, 5$ | $4.02\times 10^{-200}$ |
| $10$ | $(2, 5)$ | $(-1, 3, -3, 1)$ | $3, 1, 3$ | $1.91\times 10^{-200}$ |
| $14$ | $(2, 7)$ | $(-5, 13, -13, 5)$ | $1, 5, 13$ | $2.70\times 10^{-200}$ |
| $22$ | $(2, 11)$ | $(-3, 7, -7, 3)$ | $3, 3, 7$ | $1.22\times 10^{-199}$ |

(The $N = 33$ entry was verified in a separate run at the same precision; see Section 6 for code references.)

The bar-marginal entries at $N = 323$ (twin primes $17 \cdot 19$) and $N = 391$ (far-apart primes $17 \cdot 23$) reflect numerical cancellation eating $\sim 66$ and $\sim 90$ digits respectively in the most extreme cell; both remain comfortably inside the $10^{-100}$ bar. All other entries achieve relative error $\le 10^{-199}$, i.e. essentially the working-precision floor.

The formula is symmetric under $p \leftrightarrow q$ (substituting flips $\delta \to -\delta$ and the labels $c_p \leftrightarrow c_q$, leaving the relation invariant up to an overall sign) and the derivation in Section 2.1 nowhere assumed $p > 2$; the small-prime entries $N \in \{6, 10, 14, 22\}$ confirm this.

---

## 5. Structural extensions

What happens at richer divisor sets? Section 2.1 shows that any divisor set $D = \{d_1, \ldots, d_n\}$ on which $T_d$ is defined yields the same three linear constraints (7), whose kernel has dimension $n - \text{rank}(M)$ where $M$ is the $3 \times n$ matrix with rows $(1, \ldots, 1)$, $(d_1, \ldots, d_n)$, $(1/d_1, \ldots, 1/d_n)$. The interesting structural extensions are:

**Squarefree $N = pqr$ (three distinct primes).** Eight divisors $\{1, p, q, r, pq, pr, qr, pqr\}$, $3 \times 8$ rational system, kernel dimension $\boxed{5}$. The closed-form parameterization of Theorem 1 does *not* extend uniquely; the kernel is non-unique. Numerically verified at $N \in \{30, 105, 165\}$. The first basis vector is typically a "sub-divisor annihilator" supported on $\{1, p, q, r\}$ alone; the lifted Theorem-1 annihilators on the embedded $pq$-, $pr$-, $qr$-sublattices also live inside the kernel.

**Prime power $N = p^2$.** Three divisors $\{1, p, p^2\}$. The $3 \times 3$ constraint matrix is Vandermonde-type in $(1, p, p^2)$ and $(1, 1/p, 1/p^2)$, of full rank $3$, kernel dimension $\boxed{0}$. *The family does not extend to prime powers.* Verified at $N \in \{49, 121\}$. The construction structurally requires at least two distinct prime factors.

**Mixed $N = p^2 q$.** Six divisors $\{1, p, q, p^2, pq, p^2 q\}$, kernel dimension $\boxed{3}$. The closed form is non-unique. Verified at $N \in \{18, 45\}$. As at $pqr$, sub-divisor annihilators and lifts of the Theorem-1 $p \cdot q$ annihilator both populate the kernel.

The clean uniqueness of Theorem 1 is therefore special to the squarefree composite case $N = pq$.

A subtler point: at $N = pqr$ the Eisenstein-subspace dimension formula (9) gives $\dim E_2(\Gamma_0(pqr)) = 2^3 - 1 = 7$, so the eight forms $\{E_2(d\tau) : d \mid pqr\}$ satisfy exactly one linear relation at the level of modular forms — yet our Lambert-block construction yields a kernel of dimension $5$, not $1$. The discrepancy is because identity (1) captures only the affine truncation of the full $E_2$ $q$-expansion under modular inversion; it loses information about the higher-order terms that modular-form linear-relation theory tracks in full. At $N = pq$ the kernel dimensions coincide ($1 = 1$); at higher $N$ they generically diverge. This is a useful caveat: the H-R-B identity is a *strictly weaker* constraint than full $E_2$-modularity, and the "Lambert-annihilator" picture and the "Eisenstein-subspace linear-relation" picture only agree at $N = pq$.

---

## 6. Provenance: autonomous rediscovery by symbolic search

The closed-form formula (4) was rediscovered autonomously by Project C, an LLM-driven symbolic-search engine for Ramanujan-style identities developed during the 2026 *Ramanujan mining* research run [6]. The engine's basis of operators — `mellin_inversion`, `master_theorem`, `modular_transform_with_correction`, and others — was applied iteratively to a small library of seed identities under an mpmath cost model with a strict $\le 10^{-30}$ relative-error acceptance bar. The Level-$33$ instance was the first the engine surfaced (after several thousand seed-operator compositions); a prompted exploration cycle then enumerated the seven additional instances $N \in \{35, 51, 65, 77, 87, 95, 115\}$ from a hand-tabulated guess of the integer-lowest-height coefficient pattern, yielding the explicit $\gcd(pq-1, q-p)$ form.

Crucially, the engine did *not* use the classical dimension formula (9) or the Eisenstein-subspace framework of Section 3. It worked entirely from identity (1) and elementary linear algebra over the rationals. The structural connection to $\dim E_2(\Gamma_0(pq)) = 3$ was identified only after the formula was produced, by an adversarial verification subagent performing a literature audit.

A subsequent literature diff [6, diary 58] across six volumes of Berndt's *Ramanujan's Notebooks* and *Lost Notebook* commentary [2, 7], Berndt-Yee [8], Berndt-Dixit [9], plus the LMFDB database, the OEIS, and approximately twelve targeted arXiv and AMS searches, did not locate the explicit $\gcd(pq-1, q-p)$ parameterization in this exact form. The underlying *structure* — a one-dimensional linear-relation space among the four Eisenstein candidates at squarefree composite level — is, however, classical and well-documented.

We therefore offer this note in two registers. **First**, as a useful explicit closed form for a relation that is *guaranteed to exist* by Eisenstein-subspace dimension counting but is rarely written down in this elementary form, and which evaluates exactly to zero at every $(\alpha, \beta)$ on $\alpha\beta = \pi^2$. **Second**, as a worked instance of autonomous rediscovery: an LLM-driven engine, operating with no prior modular-forms machinery and only a small basis of structural operators, rediscovered in explicit form a classical structural identity that has been implicit in the modular-forms literature for decades. We regard the latter as the more interesting contribution. The mathematics is classical; what is novel is the demonstration that a small, structured operator basis plus a strict numerical acceptance gate suffices to surface this structure autonomously.

The full computational verification — numerical code, raw results, and the literature audit — is available at [6] in `analysis/30_level33_lambert_e2_annihilator_verification.py` and `analysis/32_level_pq_family_adversarial_verification.py`.

---

## Acknowledgments

The author thanks the developers of `mpmath`, `sympy`, the LMFDB project, and the maintainers of the open-access portions of Berndt's *Ramanujan's Notebooks* series.

---

## References

[1] G. H. Hardy and S. Ramanujan, *Asymptotic formulae in combinatory analysis*, Proc. London Math. Soc. (2) **17** (1918), 75-115. (Submitted 1916.)

[2] B. C. Berndt, *Ramanujan's Notebooks, Part II*, Springer, New York, 1989. (See Ch. 14, Entries 26-27 for the Hardy-Ramanujan-Berndt Lambert/$E_2$ identity.)

[3] F. Diamond and J. Shurman, *A First Course in Modular Forms*, Graduate Texts in Mathematics **228**, Springer, New York, 2005. (See §3.5, §3.9, §5.6 for the Eisenstein-subspace dimension formula and the old-form construction at composite level.)

[4] W. A. Stein, *Modular Forms, A Computational Approach*, Graduate Studies in Mathematics **79**, AMS, Providence, 2007. (See Ch. 5 for the Eisenstein subspace at squarefree level.)

[5] The LMFDB Collaboration, *The L-functions and Modular Forms Database*, available at https://www.lmfdb.org. (Modular form space $M_2(\Gamma_0(33))$: total dimension $9$, cuspidal $6$, Eisenstein $3$.)

[6] J. Helminen, *Ramanujan mining: a research run*, GitHub repository at https://github.com/jounih/ramanujan-mining (private). See in particular `diary/55_*.md` (original engine claim), `diary/58_*.md` (adversarial verification and literature audit), `insights/DID_NOT_PAN_OUT.md` §R19 (honest framing), and `analysis/30_*.py`, `analysis/32_*.py` (verification code).

[7] G. E. Andrews and B. C. Berndt, *Ramanujan's Lost Notebook, Parts I-IV*, Springer, New York, 2005, 2008, 2012, 2013.

[8] B. C. Berndt and A. J. Yee, *A page on Eisenstein series in Ramanujan's lost notebook*, RIMS Kokyuroku **1274** (2002), 138-153.

[9] B. C. Berndt and A. Dixit, *A transformation formula involving the gamma and Riemann zeta functions in Ramanujan's lost notebook*, in *The Legacy of Alladi Ramakrishnan in the Mathematical Sciences*, Springer, 2010, 199-210. (arXiv:0904.1053)
