# State of the Art on Open / Partially Proven / Debated Entries in Ramanujan's Notebooks and Lost Notebook

Compiled 2026-05-24. Scope: entries from the three "ordinary" notebooks (Berndt, *Ramanujan's Notebooks*, Parts I-V, Springer 1985-1998) and the *Lost Notebook* (Andrews-Berndt, *Ramanujan's Lost Notebook*, Parts I-V, Springer 2005-2018), with a bias toward what remains genuinely under-explored. Each section ends with arxiv IDs and a one-line "why this matters".

---

## 1. Status of the Berndt and Andrews-Berndt editorial project

Across the **five Berndt volumes** every one of Ramanujan's ~3,254 entries in the second and third notebooks now has a proof or a citation to one in the literature. The fifth volume itself contains many of Berndt's own "first" proofs. The **first notebook** (essentially a rougher draft of the second) was deliberately not given its own treatment; a handful of its uniquely-occurring entries are still unproven, scattered through Chapters 1-16 (theta-function fragments, isolated continued fractions, calculations in the theory of singular moduli).

The **Andrews-Berndt Lost Notebook series (Parts I-V, 2005-2018)** closes with a Commentary chapter in Part V that lists corrections to Parts I-IV but explicitly leaves a residue of entries the authors call "isolated", "not understood in context", or "without a known generalization". Berndt has stated in colloquia that roughly **3-5%** of the Lost Notebook entries remain without a fully satisfactory explanation - they are individually proven but conceptually orphaned.

Key references:
- Andrews-Berndt, *Ramanujan's Lost Notebook*, Part V (Springer 2018), Chapter "Commentary on and Corrections to the First Four Volumes" (Springer chapter DOI 10.1007/978-3-319-77834-1_18).
- Berndt, "An overview of Ramanujan's notebooks", reprinted in *Ramanujan: Essays and Surveys* (AMS/LMS HMath 22, 2001).

---

## 2. Mock theta functions (orders 3, 5, 6, 7, 8, 10)

Status after Zwegers (2002), Bringmann-Ono, Folsom, Hickerson, Mortenson:

- **Order 3 and 5**: All Ramanujan-Watson identities now proven. The **mock theta conjectures** (10 identities for fifth-order functions) - proven by Hickerson 1988; given a *unified* vector-valued modular forms proof by N. Andersen, **arXiv:1604.05294**. Open: a single uniformly motivated combinatorial proof (no q-series wizardry); see Garvan's program.
- **Order 6 and 8**: Eight sixth-order functions appear in the Lost Notebook. Mortenson 2024 (**arXiv:2209.13472**, *Bull. LMS* 56, 2024) proved three new tenth-order-style identities for them, explicitly closing identities Andrews-Berndt had flagged as "isolated". Three more conjectural sixth-order identities of the same flavour remain.
- **Order 7**: Modular completions known (Hickerson-Mortenson 2014). Open: a clean "Ramanujan-style" proof of the seventh-order multiplicative relations; closed expressions for shadows at quadratic irrationals.
- **Order 10**: Eight identities. Choi proved them in four papers (2007-2011). The arxiv synthesis is **arXiv:0905.1133** (Zwegers, "Tenth order mock theta functions revisited"). Open: structural origin of the "definite-integral" component in identities 7 and 8.
- **Bringmann-Jennings-Shaffer-Mahlburg**, **arXiv:1612.08219**: resolves an Andrews-Dixit-Schultz-Yee modularity conjecture for a variant of omega(q), but the *general* spt-style conjectures for the other classical third-order mock thetas remain open.

Why this matters: every mock theta still indexes an open question about its harmonic Maass / quantum modular completion, and these completions are the bridge to black-hole entropies (Dabholkar-Murthy-Zagier) and to AGT / VOA characters.

Modern survey: Folsom-Ono-Rhoades, "Mock theta functions and quantum modular forms", *Forum Math. Pi* 1 (2013), e2. arXiv:1311.3044 era.

---

## 3. Partial and false theta functions

Lost Notebook (LN) pages 4, 9, 12, 28, 36-38 contain ~25 partial theta identities. Status:

- **Andrews 1981 "Partial theta functions. I: Beyond the lost notebook"** classified the main family. Bringmann-Folsom-Rhoades, **arXiv:1109.6560**, treated them as q-hypergeometric mock objects.
- Open: a *complete* duality between partial-theta and mock-theta sides (a conjecture of Hickerson-Mortenson, still partial). Recent push: **arXiv:1607.08563** (Bringmann-Milas, higher-rank partial/false theta and W-algebras) and **arXiv:1604.01977** (asymptotics from Jacobi forms).
- Wang-Yee 2018 (**arXiv:1801.07956**) gave new proofs of five LN false-theta identities without Rogers-Fine / Bailey, suggesting an undiscovered algebraic mechanism behind several still-isolated LN entries.

Why this matters: partial theta is the "missing third pillar" between modular and mock-modular; its representation-theoretic meaning (logarithmic CFT characters) is conjectural.

---

## 4. Continued fractions

- **Rogers-Ramanujan continued fraction R(q)**: all entries in Chapter 16 of Notebook II and Chapters 1-6 of Andrews-Berndt I are proven; singular values for *most* imaginary quadratic tau are known via Shimura reciprocity (Gee-Honsbeek, *Ramanujan J.* 2006). Open: an *explicit* closed form for R(q) at all CM points with class number > 2; nested-radical normal form is conjectural beyond class number 4.
- **Entry II.16.12**: a continued-fraction evaluation; the unique-yet-still-not-conceptually-explained proof history is laid out in Bhatnagar-Ismail **arXiv:1908.03333**. The "moment problem" interpretation is open.
- Bhatnagar 2022 survey **arXiv:2208.12656**, "Ramanujan's q-continued fractions", explicitly catalogues which Berndt-Andrews entries still lack a unifying framework (notably entries in Chapter 32 of NB II - the "Eisenstein-style" continued fractions and the Selberg-Chan generalizations).
- Recent: **arXiv:2601.10752** (continued fractions of orders 5, 10, 20 and Eisenstein series).

Why this matters: each non-explained continued fraction is an open structural question about an underlying orthogonal polynomial system.

---

## 5. Class invariants g_n, G_n and singular moduli

- Ramanujan tabulated **116** class invariants. After Berndt-Chan-Zhang (1995-2000) and subsequent work, ~98 are fully reproved by modular-equation methods. **~18 remained until very recently**, all in fields of class number 8 with two classes per genus (Berndt-Chan-Kang-Zhang, *Acta Arith.* 73, 1995; Watson's "empirical process" closed several).
- Open: a single algorithm (rather than ad hoc Kronecker-limit applications) producing the radical form of G_n for arbitrary n. Heuristic via Shimura reciprocity exists but is not effective for huge discriminants.
- See **arXiv:2004.05854** ("Explicit evaluations formula for Ramanujan's singular moduli and Ramanujan-Selberg continued fraction") and **arXiv:2005.05302** (new P-Q modular equation of degree 2).

Why this matters: G_n values are the modular building blocks of Ramanujan's pi formulae and his class-field theoretic identities.

---

## 6. Modular equations of high level

Berndt Notebooks III-V proved Ramanujan's modular equations of degrees up to ~47. Recorded but not concept-anchored:

- **23 P-Q "mixed" modular equations** in NB II (Berndt-Zhang proved them, but the "ladder" structure - why these particular mixed degrees - is unexplained).
- High-prime levels: levels **23, 29, 31, 47** appear in scattered entries; Berndt notes (Part V, Chapter X) that no general "theory" exists analogous to the level-7 and level-11 theta-function theories.
- Recent: **arXiv:1907.01634** (P-Q mixed of degree 5), **arXiv:2105.05759** (geometric deduction).
- Levels **14, 15** alternative-base theories: Cooper, *Trans. AMS* 368 (2016), 8023-8068, extended Ramanujan's signatures r = 3, 4, 6 to 14, 15. Open: a Ramanujan-style signature theory for level 17 and higher.

Why this matters: every missing level is potentially a new explicit class field tower that Ramanujan glimpsed.

---

## 7. Ramanujan-Sato series for 1/pi (and 1/pi^2)

Classification of Ramanujan-Sato series by level of the underlying modular form:

- Levels 1-4 (Ramanujan 1914); 5 (Chan-Cooper 2012); 6A-D (Chan-Tanigawa-Yang-Zudilin; Sato; Chan-Chan-Liu; Chan-Verrill); 7-12 covered systematically by Cooper's 2017 book *Ramanujan's Theta Functions*; **levels 13-35** scattered, including **arXiv:1711.00459** (level 17, Huber-Schultz-Ye).
- Open: a complete classification at levels with non-trivial Atkin-Lehner involutions and at all moonshine-relevant levels (the Conway-Norton groups beyond level 12). See **arXiv:2202.13253** (generalized R-S from modular forms, 2022).
- Cooper-Zudilin supercongruences: **arXiv:2312.16827** (heuristic derivation 2023) and **arXiv:2408.08844** (11 new explicit R-S series with proved supercongruences, 2024).
- Open: a Galois-theoretic explanation of why Ramanujan's rational coefficients always work; algorithmic discovery of 1/pi^2 series beyond Guillera's small list.

Why this matters: Ramanujan-Sato is the most computationally celebrated branch, but the structural classification is incomplete and connects to mirror symmetry / modular Calabi-Yau periods.

---

## 8. The "1729 letter" / K3 surfaces

Ono-Trebat-Leder, **arXiv:1510.00735** ("The 1729 K3 Surface", *Res. Number Theory* 1, 2015): showed Ramanujan's manipulations in a 1913 letter (the so-called "1729 manuscript page") implicitly describe a K3 surface with Picard rank 18, and produce families of near-counterexamples to Euler's diagonal-cube conjecture.

Open:
- Are Ramanujan's *other* taxicab-style manipulations in the Lost Notebook (pp. 341-343) likewise hiding K3 or Calabi-Yau threefolds? Ono speculates yes; no proof.
- Modularity of the associated motive at higher discriminants.

Why this matters: the strongest single piece of evidence that Ramanujan anticipated objects from arithmetic geometry without language to describe them.

---

## 9. Ramanujan's Master Theorem - generalizations

Ramanujan's Master Theorem (NB I, Chapter VIII) is Mellin-transform formalism with non-rigorous convergence.

- Hardy gave conditions (in *Ramanujan: Twelve Lectures*).
- Amdeberhan-Espinosa-Gonzalez-Harrison-Moll-Straub, *Ramanujan J.* 29 (2012), 103-120: modern survey; flagged open question of meromorphic extensions.
- **arXiv:2209.03399** (Bradshaw-Vignat, operational calculus extension, 2022).
- **arXiv:2408.08725** (Bradshaw et al., extension to meromorphic functions with arbitrary-order poles, 2024).

Open: a Master Theorem for several variables that recovers all known multi-Mellin identities; rigorous conditions in the p-adic setting.

Why this matters: physicists use it daily in Feynman-integral evaluation; the validity conditions remain folklore.

---

## 10. Ramanujan's tau, partition congruences, crank / rank

- **Lehmer's conjecture**: tau(n) is never 0. Variations: Balakrishnan-Craig-Ono showed tau(n) avoids many odd values (2020-2022). Still open in full.
- **Dyson rank / Andrews-Garvan crank**: Garvan, "A new approach to the Dyson rank conjectures", *Ramanujan J.* 60 (2023). Recent **arXiv:2301.10991** (transformation symmetries). A unified combinatorial proof of all of Ramanujan's mod-5, 7, 11 congruences from a single statistic is still missing.
- 2024 survey: "Survey on deviations and arithmetic properties of combinatorial statistics after Dyson, Andrews, and Garvan" (J. Math. Sci., 2025).
- Variations of Lehmer's conjecture: **arXiv:2005.10345** (Balakrishnan-Craig-Ono).

Why this matters: tau(n) sits at the core of the Langlands program; Lehmer remains a touchstone open problem.

---

## 11. Berndt-Dixit "incorrect claims" of Ramanujan

Berndt-Kim-Zaharescu and Dixit-Kim-Murty-Sahu, **arXiv:1608.03670** ("New pathways and connections in Number Theory and Analysis motivated by two incorrect claims of Ramanujan"): two claims in the Lost Notebook turn out to be wrong, but the *correct* identities and the analytic theory they spawn are still being developed - in particular, a Voronoi-style summation formula whose precise error term is open.

Why this matters: even Ramanujan's "mistakes" are now research programs.

---

## 12. Three to five additional recent arxiv survey IDs

- **arXiv:2103.14002** - Berndt-Dixit, "Ramanujan's Beautiful Integrals" (2021): catalogue of LN integrals; identifies ~10 entries lacking conceptual proofs.
- **arXiv:1901.00946** - McLaughlin-Sills-Zimmer, "Rogers-Ramanujan-Slater Type Identities" (2nd ed. 2022, *Electron. J. Combin.* DS15): definitive list, includes LN identities not in Slater. Open: bijective proofs for >120 of the ~250 entries.
- **arXiv:1812.05563** - "Identities of the Rogers-Ramanujan-Slater Type" (2018).
- **arXiv:2412.12361** - "The Ramanujan Library - Automated Discovery" (2024): machine-checking pipeline for Ramanujan-style identities, has found candidates not in any current proof catalogue.
- **arXiv:2411.06412** - "The Rogers-Ramanujan dissection of a theta function" (2024).
- **arXiv:2411.03574** - Evaluation of beta integrals of Ramanujan type (2024).
- **arXiv:2210.04659** - Finite trigonometric sums from Ramanujan's theta functions (2022).
- **arXiv:2112.11882** - Explicit values for Ramanujan's theta function phi(q) (2021): survey of singular values; numerous still-conjectural cases at high discriminant.
- **arXiv:2112.06653** - Ramanujan's products of theta functions and applications (2021).
- **arXiv:1208.2694** - Schneider, "Uncovering Ramanujan's Lost Notebook: An Oral History" (good context on the editorial frontier).

---

## 13. Open problem aggregators

- No formal "Berndt open list" exists in print, but his colloquium handouts (Aachen 2008; Urbana retrospective talks 2018, 2022) circulate informally and name specific entries. The Aachen PDF is hosted at https://faculty.math.illinois.edu/~berndt/articles/aachen.pdf (server returns 403 to non-browser clients; mirrored in some preprint servers).
- The *Hardy-Ramanujan Journal* publishes one yearly volume on December 22 (https://hrj.episciences.org/) - vol 43 (2020) and vol 45 (2022) carry several entries explicitly labelled "open" in their problem sections.
- The *Ramanujan Journal* (Springer) carries frequent "research problem" notes by Berndt, Andrews, Garvan, Chan, Cooper.

---

## 14. Highest-payoff areas for an original reader of the scans

Based on the survey above, the genuinely under-explored material clusters into:

1. **First Notebook unique entries** (not duplicated in NB II): the chapter on theta-function fragments and singular moduli.
2. **Lost Notebook pages 28-39 and 341-343**: partial theta + the 1729 / K3 manipulations.
3. **Mixed modular equations at levels 23, 29, 31, 47** in NB II Chapters 19-21.
4. **Eisenstein-style continued fractions in NB II Chapter 32** (Andrews-Berndt LN Part V Chapter X).
5. **Class invariants of class-number-8, two-class-per-genus discriminants** - the last ~18 require Kronecker-limit techniques Ramanujan apparently used without writing down.
6. **Ramanujan-Sato candidates at moonshine levels** beyond 17.

These are the regions where a careful reader, alert to modern arxiv literature, can plausibly find a result that is genuinely on the research frontier rather than already in Andrews-Berndt.

---

### Sources (selected; arxiv IDs are clickable on arxiv.org)

- arxiv: 1510.00735, 1604.05294, 1109.6560, 1311.3044, 1604.01977, 1607.08563, 1612.08219, 1711.00459, 1801.07956, 1812.05563, 1901.00946, 1908.03333, 1907.01634, 0905.1133, 2005.05302, 2004.05854, 2005.10345, 2103.14002, 2105.05759, 2112.06653, 2112.11882, 2202.13253, 2208.12656, 2209.03399, 2209.13472, 2210.04659, 2301.10991, 2312.16827, 2408.08725, 2408.08844, 2411.03574, 2411.06412, 2412.12361, 2601.10752, 1608.03670, 1208.2694.
- Books: Berndt, *Ramanujan's Notebooks*, Parts I-V (Springer, 1985-1998); Andrews-Berndt, *Ramanujan's Lost Notebook*, Parts I-V (Springer, 2005-2018); Cooper, *Ramanujan's Theta Functions* (Springer, 2017).
- Journals: *Hardy-Ramanujan Journal* (open access, https://hrj.episciences.org/); *Ramanujan Journal* (Springer); *Research in Number Theory* (Springer).
