# State of the Art: Ramanujan's Mathematics in Physics & Computation

A structured survey of where Ramanujan-style mathematics genuinely intersects modern physics, computation, and information theory. Compiled as a baseline for judging novelty of observations from Ramanujan's notebooks.

---

## 1. Mock Theta Functions and Physics

**Headline result.** Zwegers' 2002 PhD thesis finally explained what Ramanujan's "mock theta functions" really were: holomorphic parts of harmonic Maass forms whose modular completion involves a non-holomorphic Eichler integral (the "shadow"). This unlocked a decade of physics applications.

**Black hole microstate counting.** Dabholkar, Murthy, and Zagier (arXiv:1208.4074, 2012, "Quantum Black Holes, Wall Crossing, and Mock Modular Forms") show that the meromorphic Jacobi form counting 1/4-BPS dyons in N=4 string compactifications splits canonically into a mock Jacobi form (single-centered black hole degeneracies) plus an Appell-Lerch sum (multi-centered bound states that decay across walls of marginal stability). The mock part is what is "genuinely quantum-gravitational"; the Appell-Lerch piece tracks wall-crossing.

**Mathieu and umbral moonshine.** Eguchi, Ooguri, Tachikawa (arXiv:1008.1858 / 1004.0956 era; key paper arXiv:1008.3778 "Mathieu Moonshine in the elliptic genus of K3", 2010) observed that the elliptic genus of K3, decomposed in N=4 superconformal characters, yields multiplicities that are dimensions of irreducible reps of the Mathieu group M24. Cheng, Duncan, Harvey then generalized this to 23 cases of "umbral moonshine" (arXiv:1204.2779, 2012, "Umbral Moonshine"), each pairing a Niemeier lattice with a vector-valued mock modular form. Duncan, Griffin, Ono proved the conjecture (arXiv:1503.01472, 2015, "Proof of the Umbral Moonshine Conjecture").

**Recent and review literature.** Murthy's review arXiv:2305.11732 ("Black holes and modular forms in string theory", 2023) is the canonical reference; arXiv:2505.02572 ("Mock Modularity at Work, or Black Holes in a Forest", 2025) extends to compact and non-compact Calabi-Yau invariants. Non-compact SCFTs and AdS3/CFT2 mock modularity: arXiv:2004.05742 (2020). Gaiotto-Johnson-Freyd secondary elliptic genus arXiv:1904.05788 (2019) ties mock modularity to deformation invariants of 2d SUSY theories.

*Open / less explored:* the **physical meaning of the shadow** as an information-theoretic quantity (entropy of "missing" multi-center states) is still informal. No clean "shadow = mutual information" theorem exists.

---

## 2. Rogers-Ramanujan Identities in Statistical Mechanics

**Baxter's breakthrough.** Baxter solved the hard-hexagon model (triangular-lattice gas with nearest-neighbor exclusion) in 1980 and discovered that its order-parameter generating functions are exactly the Rogers-Ramanujan products. Andrews-Baxter-Forrester (ABF) generalized this in 1984 to a family of RSOS models whose one-point functions yield Rogers-Ramanujan-Andrews-Gordon identities. See arXiv:2405.08425 ("Rogers-Ramanujan identities in Statistical Mechanics", 2024) for a modern review.

**Fermionic vs bosonic characters in CFT.** Kedem, Klassen, McCoy, Melzer (arXiv:hep-th/9301046 "Fermionic Sum Representations for Conformal Field Theory Characters", 1993; arXiv:hep-th/9303013 "Quasi-Particles, Conformal Field Theory, and q-Series", 1993) gave fermionic-sum companions to the Rocha-Caridi (bosonic) characters of Virasoro minimal models. The "bosonic = fermionic" q-series identities reflect dual quasi-particle descriptions: one in terms of vacuum + null-state subtractions, the other in terms of free fermion-like excitations.

**Bailey machinery.** Bailey pairs, chains, and lattices (Andrews, Berkovich, Warnaar; see arXiv:0910.2062 "50 Years of Bailey's Lemma", 2009) are the systematic engine producing infinite hierarchies of Rogers-Ramanujan-type identities, each often corresponding to a different RSOS or coset CFT character identity. The trinomial analogue of Bailey's lemma connects to N=2 superconformal invariance.

**Bose-Fermi correspondence in 1+1d QFT.** arXiv:hep-th/9304056 ("The sums of Rogers, Schur and Ramanujan and the Bose-Fermi correspondence", 1993) made the operator-algebraic connection explicit.

*Open / less explored:* For non-rational and irrational CFTs, fermionic character formulas are rare. Bailey machinery for **logarithmic CFTs** and for **higher-rank coset models beyond ADE** remains patchy.

---

## 3. Hardy-Ramanujan Circle Method as a Partition-Function Technique

**Rademacher's exact formula** (1937) refined the Hardy-Ramanujan 1918 asymptotic into a convergent series for p(n) involving Kloosterman sums and Bessel functions. This is now a workhorse for asymptotic analysis of any modular generating function.

**Physics uses.** Dijkgraaf-Maldacena-Moore-Verlinde (hep-th/0005003 / 0005029, 2000) used Rademacher expansions to argue that the BTZ black hole entropy in AdS3 string theory is reproduced microscopically by polar (light) states via the circle method. Manschot, Pioline, Sen developed this systematically for N=4 dyons (arXiv:1702.02755 "Mixed Rademacher and BPS Black Holes", 2017; arXiv:1812.08152 "Mock modularity from black hole scattering states", 2018). Dabholkar's review arXiv:1905.04060 ("Ramanujan and Quantum Black Holes", 2019) is the most accessible source.

**Other physics applications.** Vafa-Witten partition functions on P^2 admit Rademacher expansions from their mock modular character (arXiv:1803.09270, 2018, "An exact formula for U(3) Vafa-Witten invariants on P^2"). 2d CFT partition functions: Maloney-Witten and later "Rademacher expansions and the spectrum of 2d CFT" (arXiv:1907.01151 era). Sphere partition functions in supersymmetric gauge theory, instanton sums in topologically twisted N=4 SYM, and machine-learning attempts to predict automorphic structures (arXiv:2505.05549, 2025).

*Open / less explored:* The circle method has not been seriously combined with **resurgence / trans-series** structure of non-perturbative QFT, even though both produce exponentially small corrections from saddle-points. A unified "Rademacher = resurgent" picture would be major.

---

## 4. Ramanujan Graphs and Computation

**Foundational construction.** Lubotzky-Phillips-Sarnak (1988, "Ramanujan Graphs", Combinatorica) and independently Margulis built explicit infinite families of k-regular graphs whose nontrivial spectral gap saturates the Alon-Boppana bound (eigenvalues bounded by 2 sqrt(k-1)). The construction uses Hecke operators on PSL_2(F_p) and quaternionic arithmetic; the key input is Deligne's bound (i.e., the Ramanujan conjecture for weight-2 modular forms).

**Applications.**
- **Expander codes** (Sipser-Spielman 1996): linear-time decodable codes.
- **Derandomization and Markov-chain mixing**: optimal mixing time bounds.
- **Cryptographic hash functions** (Charles-Goren-Lauter 2009), now studied as post-quantum candidates.
- **Quantum complexity**: quantum expanders (arXiv:quant-ph/0702129, 2007).

**Golden gates for quantum computing.** Sarnak and collaborators turned the LPS construction into an explicit optimal universal gate set for PU(2): "Super-Golden-Gates for PU(2)" (Parzanchevski-Sarnak, arXiv:1704.02106, 2017). Evra-Parzanchevski extended this to PU(3) via Ramanujan complexes (arXiv:1810.04710, 2018, "Ramanujan complexes and Golden Gates in PU(3)"). Most recently, Dalal-Evra-Parzanchevski "Multi-Qubit Golden Gates" (arXiv:2509.09047, 2025) used Sarnak-Xue density and endoscopic classification to give multi-qubit gate sets that need ~10x fewer T-gates than Clifford+T.

*Open / less explored:* **Ramanujan complexes beyond rank 2** as building blocks for fault-tolerant codes (LDPC, qLDPC) is active but not yet at the level of practical quantum hardware. Connection to **topological codes** via arithmetic groups is sparse.

---

## 5. Ramanujan Tau Function and L-Functions

**Definitions.** tau(n) is defined by Delta(q) = q prod (1-q^n)^24 = sum tau(n) q^n; equivalently Delta = eta^24 where eta is the Dedekind eta. Delta is the unique cusp form of weight 12 level 1. Ramanujan conjectured multiplicativity (proved by Mordell, 1917) and the sharp bound |tau(p)| <= 2 p^{11/2} (proved by Deligne 1974 as a corollary of the Weil conjectures).

**Langlands.** Tau is the Hecke eigenvalue prototype: the L-function L(s, Delta) has an Euler product and functional equation. The Ramanujan-Petersson conjecture (purity of Hecke eigenvalues for all automorphic cusp forms on GL_n) is one of the deepest open problems in the Langlands program. Recent: Lehmer's conjecture (tau(n) != 0) proof attempt arXiv:2503.23498 (2025).

**Physics interpretations.**
- eta^24 = Delta is **the partition function of 24 transverse bosons on a worldsheet torus** in bosonic string theory; the weight 12 / dimension 24 underlies anomaly cancellation in critical dimension 26.
- The Leech lattice and Conway-Monster moonshine sit inside this same modular-form architecture; Frenkel-Lepowsky-Meurman's Monster module realizes J as a graded character.
- Mass formulas for BPS states in heterotic compactifications are governed by Delta and its theta-series cousins.

*Open / less explored:* No serious "**energy-based interpretation of tau(n)**" exists. The fact that tau(n) is a *Hecke eigenvalue* (i.e., simultaneous eigenvalue of an infinite commuting family of operators) is suggestive of a thermodynamic-like "free spectrum" picture, but nothing rigorous links it to entropy or free energy.

---

## 6. Friston's Free-Energy Principle / Active Inference

**Setup.** Friston's variational free energy is F = -log p(o|m) + KL(q(s) || p(s|o,m)) = -log Z + KL term, where minimizing F simultaneously approximates Bayesian inference and bounds surprise. The most current statements: arXiv:1906.10184 ("A Free Energy Principle for a Particular Physics", 2019), arXiv:2201.06387 ("The free energy principle made simpler but not too simple", 2022, Friston-Da Costa-Sajid-Heins-Ueltzhoffer-Pavliotis-Parr). These derive FEP from Langevin dynamics with a particular Markov-blanket partition, landing in Bayesian mechanics.

**Connection to physics partition functions.** Z appears as a normalizer in the generative model p(o,s|m); the analogy to Helmholtz free energy F = U - TS is structural, not a quantitative identification. There IS recent work explicitly framing FEP in non-equilibrium statistical mechanics language (arXiv:2406.11630 "A framework for the use of generative modelling in non-equilibrium statistical mechanics", 2024).

**The Ramanujan / modular-form gap.** Targeted searches ("active inference modular form", "free energy principle q-series", "Friston Ramanujan", "variational Bayesian mock modular") return essentially nothing. The closest hits are:
- General Z-as-partition-function language in Friston's papers.
- Ken Ono's "Modularity from q-series" (arXiv:2509.20316, 2025), which is pure math.
- Energy-based generative models (Hinton, LeCun-style EBMs) use Z as normalizer but no q-series structure.

This is a **near-complete white space**: there is no published bridge between mock modular generating functions / Bailey-type fermionic-bosonic q-series and variational families on the FEP side. The conceptual analogy (both have a generating function whose "shadow" or "completion" measures departure from a clean equilibrium description) is suggestive but unexploited.

*Open / less explored:* **Everything in this direction.** Even formulating a precise question -- e.g., "is there a generative model whose evidence is a mock theta function?" -- would be new.

---

## 7. Ramanujan-Style Fast Convergence Formulas

**Lineage.** Ramanujan's 1914 paper "Modular equations and approximations to pi" gave a 1/pi series converging ~8 digits/term. The Chudnovsky brothers (1987) sharpened this using class-number-2 quadratic fields and a level-1 modular function to ~14 digits/term -- the basis of every multi-trillion-digit pi computation since 1994. Proof: arXiv:2003.06668 (2020); extensions arXiv:2403.07291 (2024).

**BBP and Bellard.** Bailey-Borwein-Plouffe (1995) gave the first digit-extraction (BBP) formula for pi in hexadecimal. Bellard's variant (1997, found by PSLQ) is ~43% faster and was the basis for the PiHex distributed project (250 CPU-years, 1734 computers) computing the quadrillionth bit. Recent: arXiv-discussed Intel Xeon Phi cluster computation of the 100-quadrillionth bit.

**Verifiable computation.** Digit-extraction formulas enable spot-checking long pi computations without recomputing prefixes -- effectively a verifiable computation primitive. There are scattered uses in interactive-proof / sumcheck literature but no comprehensive "Ramanujan-series-as-PCP" framework.

*Open / less explored:* Use of these series for **non-pi constants** in physics (e.g., Feynman periods, multiple zeta values appearing in QFT amplitudes) is patchy. Connections to **modular bootstrap** numerics are unexploited.

---

## 8. Continued Fractions and Quantum / Signal Processing

**Vaidyanathan's Ramanujan-sum signal processing.** Ramanujan sums c_q(n) form an orthogonal periodic basis with integer entries. Vaidyanathan and Tenneti (IEEE Trans. Signal Processing, 2014, Parts I and II) built **Ramanujan filter banks** for period estimation that outperform DFT-based methods on short, noisy, multi-periodic signals (e.g., DNA tandem repeats, biomedical signals). Recent: arXiv:2512.16190 (2025) "Ramanujan sums in signal recovery and uncertainty principle inequalities". Transmultiplexer designs with integer coefficients (2020+).

**Continued fractions in quantum mechanics.** Stieltjes / J-fraction expansions of resolvents are standard in tight-binding density-of-states calculations (the recursion / Lanczos method). Quantum walks on the integer lattice: arXiv:1505.07292 ("Spreading Estimates for Quantum Walks via Power-Law Bounds on Transfer Matrices", 2015) uses CMV-matrix transfer-matrix continued-fraction technology. Perfect quantum state transfer relates to Serret-type continued-fraction identities (arXiv:1912.11978, 2019).

**Rogers-Ramanujan continued fraction in physics.** Appears in the corner-transfer-matrix solution of the hard-hexagon model (Baxter) and in characters of certain Virasoro modules. No direct quantum-information use known.

*Open / less explored:* Ramanujan's own q-continued fractions (e.g., the Ramanujan-Selberg, Ramanujan-Gollnitz-Gordon CFs) have **almost no engineering uptake**. They are not in the standard filter-design or quantum-walk toolkits despite formal analogies.

---

## Summary of Where Novelty Is Plausible

| Area | Density of existing work | Where genuine novelty is most plausible |
|------|--------------------------|----------------------------------------|
| Mock theta in physics | Very high (15+ years, dozens of groups) | Info-theoretic meaning of the shadow |
| RR identities / stat mech | High but mature | Logarithmic CFT, higher-rank cosets |
| Circle method in QFT | Moderate, active | Marriage with resurgence |
| Ramanujan graphs / quantum gates | Active frontier | Topological / qLDPC codes |
| tau function / Langlands | Mature pure math | "Energy-like" interpretation |
| **FEP / active inference + Ramanujan** | **Essentially zero overlap** | **Almost anything thoughtful would be new** |
| Pi-series / verifiable computation | Engineering-heavy | Apply to physics constants / amplitudes |
| Continued fractions in signal/quantum | Specialist | Ramanujan's q-CFs in engineering |

The single largest white space is the intersection of Friston-style variational free energy with Ramanujan-flavored generating functions (mock modular, q-series, fermionic-bosonic duality). The conceptual parallel -- generating function whose "anomalous" piece carries the action of an algebraic structure -- has not been formalized in published literature.

---

## Key arXiv IDs (compact reference)

- **1208.4074** Dabholkar-Murthy-Zagier, Quantum Black Holes, Wall Crossing, Mock Modular Forms (2012)
- **1008.3778** Eguchi-Ooguri-Tachikawa, Mathieu Moonshine in elliptic genus of K3 (2010)
- **1204.2779** Cheng-Duncan-Harvey, Umbral Moonshine (2012)
- **1503.01472** Duncan-Griffin-Ono, Proof of Umbral Moonshine Conjecture (2015)
- **1211.5531** Gannon, Much ado about Mathieu (2012)
- **2305.11732** Murthy, Black holes and modular forms (review, 2023)
- **2505.02572** Mock Modularity at Work (2025)
- **2004.05742** Non-Compact SCFT and Mock Modular Forms (2020)
- **hep-th/9301046** Kedem-Klassen-McCoy-Melzer, Fermionic CFT characters (1993)
- **hep-th/9303013** Quasi-Particles, CFT and q-Series (1993)
- **hep-th/9304056** Sums of Rogers/Schur/Ramanujan and Bose-Fermi correspondence (1993)
- **0910.2062** Warnaar, 50 Years of Bailey's Lemma (2009)
- **2405.08425** Rogers-Ramanujan in Statistical Mechanics (2024 review)
- **1702.02755** Manschot-Pioline-Sen, Mixed Rademacher and BPS Black Holes (2017)
- **1905.04060** Dabholkar, Ramanujan and Quantum Black Holes (2019 review)
- **1803.09270** Vafa-Witten on P^2 Rademacher (2018)
- **1704.02106** Parzanchevski-Sarnak, Super-Golden-Gates for PU(2) (2017)
- **1810.04710** Evra-Parzanchevski, Ramanujan complexes and Golden Gates in PU(3) (2018)
- **2509.09047** Dalal-Evra-Parzanchevski, Multi-Qubit Golden Gates (2025)
- **2503.23498** Proof attempt of Lehmer's conjecture on tau (2025)
- **1906.10184** Friston, Free Energy Principle for a Particular Physics (2019)
- **2201.06387** Friston et al., FEP made simpler but not too simple (2022)
- **2406.11630** Generative modelling in non-equilibrium statistical mechanics (2024)
- **2003.06668** Proof of Chudnovsky 1/pi series (2020)
- **1505.07292** Quantum Walks via Transfer Matrices (2015)
- **2509.20316** Ono, Modularity from q-series (2025)
