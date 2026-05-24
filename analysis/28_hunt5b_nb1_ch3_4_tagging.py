"""Hunt 5b — Berndt *Notebooks Part 1* Chapters 3 + 4 operator tagging.

Fourth chapter pass in the Hunt 5b operator-tagging study (after Ch. 32 in
diary 22, Ch. 36 in diary 24, Ch. 34 in diary 25). This pass crosses into a
DIFFERENT VOLUME of Berndt's commentary (Part 1 instead of Part V) and into
chapters that contain Ramanujan's first writeup of his Master Theorem and
his ingenious "f(x^n) -> phi(n)" formal technique — i.e. the QR-volume
analog of the material that Hunt 5 (diary 20) tagged separately in the
Quarterly Reports.

Source: `downloaded-pdfs/ramanujankitap1.pdf` (Berndt, *Ramanujan's
Notebooks Part 1*, Springer 1985):
  - Ch. 3 (pp. 44-83): "Combinatorial Analysis and Series Inversions"
  - Ch. 4 (pp. 85-108): "Iterates of the Exponential Function and an
    Ingenious Formal Technique"

Same hand-tagging methodology as diaries 22 / 24 / 25:
  - Unit of judgment is the atomic proof block (Entry / Theorem / Lemma /
    Example / Corollary).
  - Tags record whether the operator is primary or major-secondary in the
    PROOF (not the statement).
  - "Near match != match" — strict false-positive discipline.
  - The 11-operator vocabulary is the SAME as diaries 22 / 24 / 25 (6 from
    operator_tagging_schema.py + 5 from diary 20).

The blinded-experiment protocol means this tagging was performed WITHOUT
reading insights/HUNT5B_NB1_CH3_4_PREDICTION_REGISTRATION.md; the
comparison with the pre-registered prediction is done in the diary entry
only AFTER the tagging is encoded here.

Outputs:
  - analysis/results/hunt5b_nb1_ch3_4_tags.csv  (one row per proof unit)
  - stdout: per-operator saturation summary across both chapters

Run:
    python analysis/28_hunt5b_nb1_ch3_4_tagging.py
"""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = REPO_ROOT / "analysis/results"
TAGS_CSV = RESULTS_DIR / "hunt5b_nb1_ch3_4_tags.csv"


# 11-operator vocabulary (same as diary 22 / 24 / 25).
OPERATORS = [
    "modular_S_transform",
    "eisenstein_normal_ordering",
    "q_shift",
    "class_field_galois_average",
    "denesting_via_kummer_or_landau",
    "algebraic_number_field_norms",
    "cardano_cubic_formula",
    "master_theorem",
    "frullani_limit",
    "fractional_functional_iteration",
    "mellin_pair_reciprocity",
]


# ---------------------------------------------------------------------------
# Tagged proof units
# ---------------------------------------------------------------------------
#
# Each dict has:
#   chapter   : 3 or 4
#   unit_id   : human-readable identifier (e.g. "E10", "C2-of-E2")
#   page      : Berndt book page (best-effort, single page or range)
#   topic     : 1-line description of what the unit is about
#   operators : list of operator names from OPERATORS
#   note      : justification for the firings, with Berndt quote where possible
#
# Notes on counting:
#   - Corollaries / Examples following an Entry are counted as separate units
#     IF they have their own proof body and produce a distinct claim. This
#     matches the diary 22 / 24 / 25 convention (e.g. "Examples 9.4 (alpha_4,
#     alpha_12, alpha_28, alpha_60)" in diary 25 was a single aggregate row
#     when the 4 examples shared one proof; here, Ramanujan-style serial
#     examples 3(i)-3(viii) and 4(i)-4(iv) are each counted as ONE
#     aggregate group because they share the same proof skeleton).
#   - The "Theorem" / "Corollary" in §13 of Ch. 3 is the abstract Rota-Mullin
#     theorem; counted as 1 unit each.
#   - "Lemmas 1-4" preparing the Entry 10 proof are aggregated as 1 unit
#     ("L1-4") because they are pure setup lemmas with no in-schema operator
#     firings (analogous to Lemma 3.3 in diary 25 being noted as out-of-
#     schema-only without inflating counts).

TAGGED_UNITS: list[dict] = [
    # -------------------------------------------------------------------
    # Chapter 3 — Combinatorial Analysis and Series Inversions
    # -------------------------------------------------------------------
    # §1 — Generating-function inversion via Taylor expansion (Entry 1)
    {
        "chapter": 3,
        "unit_id": "C3-E1",
        "page": "45-46",
        "topic": "Entry 1: \\sum P_n f^(n)(0) = \\sum Q_n f^(n)(1) "
                 "given e^z g(z) = \\sum P_k z^k",
        "operators": [],
        "note": "Pure generating-function manipulation; Taylor expansion + "
                "swap order of summation. No modular / q-shift / Mellin / "
                "class-field structure. Out-of-schema: formal power series + "
                "coefficient extraction (Cauchy product).",
    },
    {
        "chapter": 3,
        "unit_id": "C3-E1-C1",
        "page": "45",
        "topic": "Corollary 1: f(z) = (1+xz)^n specialization of E1",
        "operators": [],
        "note": "Direct specialization. Binomial-coefficient identity. "
                "No in-schema operators.",
    },
    # §2 — Entry 2: phi(z) = sum (-1)^k x^k / [z(z+1)...(z+k-1)]
    {
        "chapter": 3,
        "unit_id": "C3-E2",
        "page": "46",
        "topic": "Entry 2: phi(z) := \\sum_k x^{k-1}/((z+k-1)!/(k-1)!) "
                 "evaluated by repeated parts integration of x^{z-1} e^{-x}",
        "operators": [],
        "note": "First proof: 'integrating termwise' the Maclaurin series for "
                "e^x and using \\int_0^infty x^{z-1} e^{-x} dx / (x^k) ... "
                "'upon infinitely many integrations by parts'. This is "
                "Gamma-function evaluation; no Mellin transform STRUCTURE "
                "(not f(x) -> M[f](s)) and no Master Theorem (no alternating-"
                "sign sum). Second proof: pure recursion-formula manipulation. "
                "No in-schema operators fire.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-E2-C1",
        "page": "46",
        "topic": "Corollary 1: f satisfying E1 hypotheses",
        "operators": [],
        "note": "Direct application of E2 in E1. No in-schema operators.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-E2-C2",
        "page": "47",
        "topic": "Corollary 2: 1 + x/2 + x^2/3 + ... evaluated",
        "operators": [],
        "note": "Differentiate (2.3) wrt z then set z=0. Pure calculus. "
                "No in-schema operators.",
    },
    # §3 — Asymptotic expansion psi(z) ~ sum_k (-1)^{k-1} f_{k-1}(x) / z^k
    {
        "chapter": 3,
        "unit_id": "C3-E3",
        "page": "47",
        "topic": "Entry 3: psi(z) ~ sum_{k>=1} (-1)^{k-1} f_{k-1}(x) / z^k "
                 "asymptotic in R_0",
        "operators": [],
        "note": "Asymptotic expansion of a Heaviside-type meromorphic function. "
                "Proof deferred to E8 Example 1 (next major proof unit). "
                "No in-schema operators (Mellin transform NOT used; the "
                "expansion is in negative powers of z, but the derivation "
                "is via inverse-factorial series + Stirling formula).",
    },
    # §4 — Entry 4: generating function identity for f_n
    {
        "chapter": 3,
        "unit_id": "C3-E4",
        "page": "47-48",
        "topic": "Entry 4: \\sum_n f_n(x) a^n / n! = e^a e^{x(e^a - 1)}",
        "operators": [],
        "note": "Pure formal-power-series manipulation. No in-schema operators.",
    },
    # §5 — Entry 5: recursion for f_n(x) (Bell polynomial recursion)
    {
        "chapter": 3,
        "unit_id": "C3-E5",
        "page": "48",
        "topic": "Entry 5: f_n recursion = n single-variable Bell polynomial "
                 "recursion",
        "operators": [],
        "note": "Bell-polynomial / Stirling-2 recursion derived by "
                "differentiating E4. Out-of-schema combinatorial machinery.",
    },
    # §6 — Entry 6: Stirling-2 evaluation
    {
        "chapter": 3,
        "unit_id": "C3-E6",
        "page": "49",
        "topic": "Entry 6: \\sum_{k=0}^{r-1} phi_{k+1}(n) / k! = r^n / (r-1)!",
        "operators": [],
        "note": "Coefficient extraction in generating function (6.2). "
                "Out-of-schema (Stirling-2 / Bell).",
    },
    # §7 — Entry 7: Stirling-2 explicit formula
    {
        "chapter": 3,
        "unit_id": "C3-E7",
        "page": "49",
        "topic": "Entry 7: r! phi_{r+1}(n) = \\sum_k (-1)^k C(r,k)(r+1-k)^n",
        "operators": [],
        "note": "Multiply E6 by e^{-x}, equate coefficients. "
                "Out-of-schema (Stirling-2).",
    },
    # §8 — Entry 8: Pascal-like recursion + Example 5 Bell numbers
    {
        "chapter": 3,
        "unit_id": "C3-E8",
        "page": "49",
        "topic": "Entry 8: phi_r(n+1) = r phi_r(n) + phi_{r-1}(n) "
                 "(Pascal-like)",
        "operators": [],
        "note": "Direct manipulation of Entry 7. Out-of-schema.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Cor-E8-fn-table",
        "page": "50",
        "topic": "Corollary: f_0,...,f_6 polynomial table",
        "operators": [],
        "note": "Pure tabulation by recursion. No in-schema operators.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Ex1-of-E8",
        "page": "50",
        "topic": "Example 1 of §8: Entry 3's deferred proof in greater "
                 "generality (with parameter lambda)",
        "operators": [],
        "note": "Asymptotic expansion in negative powers of z using generating "
                "function for Stirling-2. The 'Abramowitz-Stegun 24.1.4B' "
                "tool. No Mellin transform; no q-shift; no modular. "
                "Out-of-schema (asymptotic / Stirling-2).",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Ex2-of-E8",
        "page": "51",
        "topic": "Example 2 of §8: r! phi_{r+1}(n) = coeff of x^n / n! "
                 "in e^x (e^x - 1)^r",
        "operators": [],
        "note": "Direct from E7. Out-of-schema.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Ex3-of-E8",
        "page": "51",
        "topic": "Example 3 of §8: identity for n^* sum derived from E4",
        "operators": [],
        "note": "Coefficient extraction. Out-of-schema.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Ex4-of-E8",
        "page": "51-52",
        "topic": "Example 4 of §8: integral involving Bernoulli numbers",
        "operators": [],
        "note": "Substitute x->t in E4 and integrate; equate coefficients of "
                "a^{n+1}. Bernoulli numbers appear via the explicit definition "
                "(8.2) Ramanujan uses (different from modern). No Eisenstein, "
                "no E_2k Lambert series; just the Bernoulli-numbers formal "
                "power series. Out-of-schema.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Ex5-of-E8",
        "page": "52",
        "topic": "Example 5(i)+5(ii) of §8: Bell numbers A_n, C_n tables",
        "operators": [],
        "note": "Bell numbers / difference-equation tabulation. Pure "
                "combinatorial. Out-of-schema.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Ex6-of-E8",
        "page": "53",
        "topic": "Example 6 of §8: 5 specific Bell-polynomial identities",
        "operators": [],
        "note": "Direct numerical verification from Examples 5(i)+5(ii). "
                "Out-of-schema.",
    },
    # §9 — Entry 9: generalization F_n(a, b; x) of f_n
    {
        "chapter": 3,
        "unit_id": "C3-E9i",
        "page": "54",
        "topic": "Entry 9(i): F_n(a,b) generalization of Entry 3 (asymptotic)",
        "operators": [],
        "note": "Direct Taylor + (9.2). Out-of-schema asymptotic.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-E9ii",
        "page": "54",
        "topic": "Entry 9(ii): F_n(a,b;x) generating function generalizing E4",
        "operators": [],
        "note": "Pure formal power series. Out-of-schema.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-E9iii",
        "page": "55",
        "topic": "Entry 9(iii): recursion for F_n generalizing E5",
        "operators": [],
        "note": "Differentiate (9.4); same machinery as E5. Out-of-schema.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-E9iv-vii",
        "page": "55-56",
        "topic": "Entries 9(iv)-(vii) + F_n table + Examples (i)-(iv)",
        "operators": [],
        "note": "Generalizations of Entries 6-7-8 to F_n. Aggregated because "
                "all share the same proof skeleton (omitted by Berndt as "
                "'completely analogous'). Out-of-schema.",
    },
    # §10 — Entry 10: the asymptotic expansion (chapter's deepest result)
    # Lemmas 1-4 are setup; aggregating since they only feed Entry 10's proof.
    {
        "chapter": 3,
        "unit_id": "C3-L1-4-of-E10",
        "page": "60-61",
        "topic": "Lemmas 1, 2, 3, 4 setup for Entry 10 proof",
        "operators": [],
        "note": "Pure technical setup (exponential decay rates, bound on b_kn, "
                "Stirling-2 recursion via E8, polynomial-expansion lemma). "
                "No in-schema operators.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-E10",
        "page": "57-64",
        "topic": "Entry 10: phi_x(x) = phi(x) + \\sum bkn x^{2-k+1} "
                 "phi^{(j)}(x) / k! + O(G(x) x^{-M}) (asymptotic expansion of "
                 "phi(x) at large x as expected value E(phi(U)) for U Poisson(x))",
        "operators": [],
        "note": "The CHAPTER'S deepest result. Asymptotic expansion as x->infty. "
                "Ramanujan's own formal proof uses Bell-polynomial machinery; "
                "Berndt's rigorous proof uses Taylor + delicate exponential-"
                "tail estimates (Lemmas 1, 2, 4). This is NOT Mellin "
                "inversion (no \\int_0^infty x^{s-1} f(x) dx); it is NOT the "
                "Master Theorem (no Gamma(s) phi(-s) form). It IS related to "
                "Borel summability via the Poisson-expected-value reading but "
                "Berndt remarks 'no other material in the second notebook "
                "pertains to Borel summability'. Out-of-schema "
                "(asymptotic-expansion / Poisson-expectation).",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Ex1-of-E10",
        "page": "64",
        "topic": "Example 1 of E10: log of Bell-number generating function "
                 "= x + (1/2) log x - 1/(8x) - 11/(16x^2) + O(1/x^3)",
        "operators": [],
        "note": "Direct application of E10 with phi = G = sqrt(x). "
                "Asymptotic series. Out-of-schema.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Ex2-of-E10",
        "page": "65",
        "topic": "Example 2 of E10: asymptotic for log e^{-x} \\sum x^k log(k+1)/k!",
        "operators": [],
        "note": "Direct application of E10 with phi(x) = log(x+1). "
                "Out-of-schema.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Ex3-of-E10",
        "page": "65",
        "topic": "Example 3 of E10: log(phi_100(9)) approx 100 + log(phi(110)+phi(90))/2",
        "operators": [],
        "note": "Rough approximation phi_x(x) ~ phi(x) + corrections, set x=100. "
                "Out-of-schema.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Ex4-of-E10",
        "page": "65",
        "topic": "Example 4 of E10: e^{-x} \\sum_k x^k psi(k)/k! ~ log x + gamma "
                 "asymptotic",
        "operators": [],
        "note": "Substitute the asymptotic for psi(x) = log x + gamma + O(1/x) "
                "into E10 applied to phi = log. Out-of-schema. Euler's gamma "
                "appears but only as a numerical constant, not as a structural "
                "operator.",
    },
    # §11 — Entry 11: convolution of generating functions (sum of products)
    {
        "chapter": 3,
        "unit_id": "C3-E11",
        "page": "66",
        "topic": "Entry 11: n p_n = \\sum A_k p_{n-k} where p_n is generated "
                 "by exp(f(x))",
        "operators": [],
        "note": "Logarithmic derivative of exp(f(x)). Out-of-schema (formal "
                "exp-log identity, related to Faa di Bruno but pure "
                "manipulation).",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Cor-E11",
        "page": "66",
        "topic": "Corollary of E11: Newton-Girard formula n p_n = "
                 "\\sum_{k=1}^n (-1)^{k-1} S_k p_{n-k} for symmetric functions",
        "operators": [],
        "note": "Apply Entry 11 with A_k = (-1)^{k-1} S_k. Newton-Girard. "
                "Out-of-schema (classical symmetric function theory).",
    },
    # §12 — Entry 12: Recursion for F_r(n) = \\sum (n+k)^{r+k} / a^k k!
    {
        "chapter": 3,
        "unit_id": "C3-E12",
        "page": "67",
        "topic": "Entry 12: F_{r+1}(n) = n F_r(n) + (1/a) sum F_r(k+1) ...",
        "operators": [],
        "note": "Direct manipulation of the defining series for F_r(n). "
                "Out-of-schema.",
    },
    # §13 — Entry 13: Lagrange-inversion-style: x = a log x has root x^n = f(n)
    # Preparation: Theorem + Corollary on Gould polynomials
    {
        "chapter": 3,
        "unit_id": "C3-Thm-pre-E13",
        "page": "67-69",
        "topic": "Theorem: polynomials f_n satisfying f_n(x+q) - f_n(x) "
                 "= qf_{n-1}(x+p) and initial conditions satisfy "
                 "f_n(x+y) = sum f_k(x) f_{n-k}(y) (Gould-polynomial framework)",
        "operators": [],
        "note": "The Rota-Mullin Theorem in disguise (Berndt: 'now part of a "
                "general theory developed by Rota and Mullin'). Pure inductive "
                "polynomial manipulation. Out-of-schema (Sheffer / "
                "Gould-polynomial machinery).",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Cor-pre-E13",
        "page": "69",
        "topic": "Corollary: explicit Gould polynomials f_n(x) = (x/n) "
                 "prod_{k=0}^{n-1} (x + np - kq) satisfy the convolution",
        "operators": [],
        "note": "Direct from the Theorem. Out-of-schema.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-E13",
        "page": "69",
        "topic": "Entry 13: x^n = f(n) := n F_{-1}(n) where x = a log x, |a|>=e "
                 "(Lambert-W / Lagrange-inversion result)",
        "operators": ["fractional_functional_iteration"],
        "note": "This is essentially Lagrange's celebrated 'Lagrange inversion "
                "formula' applied to x = a log x. The key move: f(n) = "
                "f(1)^n = x^n where x solves a functional equation x = a log x. "
                "This is FRACTIONAL FUNCTIONAL ITERATION territory: an "
                "analytic function defined implicitly through a fixed-point "
                "equation, extended to all real (and complex) n by analytic "
                "continuation of the integer iterate. Berndt: 'Entries 13 and "
                "14 have a long history. Entry 14 was first established by "
                "Lambert [1, pp. 38-40] in a paper published in 1758. In "
                "1770, Lagrange [1] published a proof of the celebrated "
                "Lagrange inversion formula. As an application, he derived "
                "Entry 14.' The 'Schroder/Koenig fractional iteration' from "
                "the diary-20 operator definition includes Lagrange-inversion-"
                "style implicitly defined solutions of functional equations.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Cor-E13",
        "page": "70",
        "topic": "Corollary of E13: e^z = sum_k z(z+kw)^{k-1} e^{-kw} / k! "
                 "(Abel-type identity)",
        "operators": ["fractional_functional_iteration"],
        "note": "Inherits the Lagrange-inversion / fractional-iteration "
                "structure of E13 (Berndt: 'Apply Entry 13 with x = e^w'). "
                "Same operator.",
    },
    # §14 — Entry 14: generalization of Entry 13 (a^q x^p - x^q + 1 = 0 root)
    {
        "chapter": 3,
        "unit_id": "C3-E14",
        "page": "71",
        "topic": "Entry 14: phi(n) = x^n where x satisfies a^q x^p - x^q + 1 = 0",
        "operators": ["fractional_functional_iteration"],
        "note": "Direct generalization of E13. Implicit-function / "
                "Lagrange-inversion / fractional-iteration of the algebraic-"
                "equation root x = x(a). Berndt notes Entry 14 IS Lagrange "
                "inversion: 'Entry 14 [is derived from] the celebrated "
                "Lagrange inversion formula' (p. 72).",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Cor1-E14",
        "page": "71",
        "topic": "Corollary 1 of E14: closed form ((1-sqrt(1-4aq))/(2aq))^q "
                 "via Lagrange inversion",
        "operators": ["fractional_functional_iteration"],
        "note": "Apply E14 with p = 2q. Inherits E14's fractional-iteration tag.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Cor2-E14",
        "page": "72",
        "topic": "Corollary 2 of E14: (a + sqrt(a^2 + 1))^n = 1 + na + sum b_k(n) a^k",
        "operators": ["fractional_functional_iteration"],
        "note": "Apply E14 with q = 2p. Inherits.",
    },
    # §15 — Entry 15: u - log u = 1 + x^2/2, expansion of u in x
    {
        "chapter": 3,
        "unit_id": "C3-E15",
        "page": "73",
        "topic": "Entry 15: u defined by u - log u = 1 + x^2/2, then "
                 "expand u = sum b_k x^k via Lagrange inversion variant",
        "operators": ["fractional_functional_iteration"],
        "note": "Application of E13 with x = e^u, a = e^u/u. Same "
                "Lagrange-inversion / fractional-iteration substrate. The "
                "F(u) = 2(u - 1 - log u) = x^2 fixed-point-equation framing "
                "gives an analytic inverse u = G^{-1}(x), exactly the "
                "fractional-iteration motif.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Ex1-of-E15",
        "page": "73-75",
        "topic": "Example 1 of E15: sum m Gamma(m+kn) / Gamma(m+kn-k+1) "
                 "1/(2^{kn} k!) = x^m where x is a root of 2^{-n} x^n - x + 1 = 0",
        "operators": ["fractional_functional_iteration"],
        "note": "Application of E14 (special case): inverts an algebraic "
                "equation to express x^m as a hypergeometric series. "
                "Inherits fractional-iteration tag.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Ex2-of-E15",
        "page": "75",
        "topic": "Example 2 of E15: (log x)^n = a x^m gives x^p = "
                 "p sum (mp+nk)^{k-1} a^{k/n} / (m^{k-1} k!)",
        "operators": ["fractional_functional_iteration"],
        "note": "Same Lagrange-inversion / fractional-iteration framework. "
                "Derived by applying E13 to an auxiliary y, with various "
                "substitutions.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Ex3-and-4-of-E15",
        "page": "75-77",
        "topic": "Examples 3(i)-(viii) + 4(i)-(iv) of E15: variants of E13 "
                 "via substitutions (x = ae^x, x = a^x, etc.)",
        "operators": ["fractional_functional_iteration"],
        "note": "12 examples aggregated into 1 unit per diary-25 convention "
                "(e.g. §11 j-invariant catalogues). All share the same "
                "skeleton: rewrite an implicit equation as x = b log x (or "
                "similar) and apply E13. The famous Eisenstein 'x^{x^{x^...}}' "
                "iterated-power tower notation Ramanujan uses here is the "
                "purest possible fractional-iteration display.",
    },
    # §16 — Entry 16: generalization phi_r(n) = x^r phi(n) via F_r(n)
    {
        "chapter": 3,
        "unit_id": "C3-E16a",
        "page": "78",
        "topic": "Entry 16(a): r phi_r(n) recursion linking phi_{r-1}, "
                 "phi_{r+1} and Logx",
        "operators": ["fractional_functional_iteration"],
        "note": "Uses E12 + the relation x/a = log x (the Lagrange-inversion "
                "fixed-point equation defining x). Inherits fractional-iteration "
                "tag because the underlying functional-iteration structure of "
                "E13 is what makes phi_r(n) = x^r phi(n) work.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-E16b",
        "page": "79",
        "topic": "Entry 16(b): recursion on psi_k(r, n)",
        "operators": ["fractional_functional_iteration"],
        "note": "Uses (16.4) in E16(a). Inherits.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Cor1-E16",
        "page": "80",
        "topic": "Corollary 1 of E16: Maclaurin-like e^x = sum (x+kn)^k a^k / k! "
                 "for la|<e, generalising Maclaurin series for e^x",
        "operators": ["fractional_functional_iteration"],
        "note": "Direct from E16 + (16.8). Inherits.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Cor2-E16",
        "page": "81",
        "topic": "Corollary 2 of E16: n^* = lim phi_r(n) = sum_k psi_k(r, n)",
        "operators": ["fractional_functional_iteration"],
        "note": "From definitions. Inherits.",
    },
    # §17 — Entry 17: A_r coefficients in x = a e^h expansion (Lambert W tail)
    {
        "chapter": 3,
        "unit_id": "C3-E17",
        "page": "82",
        "topic": "Entry 17: recursion A_r = n(r-2) A_{r-1} + n sum A_k A_{r-k} / "
                 "(k! (r-k)!) where x defined by x^x = a^n e^h",
        "operators": ["fractional_functional_iteration"],
        "note": "Power-series expansion of x(h) in terms of h, where x is the "
                "solution of x^x = a^n e^h — implicit-function-defined "
                "function = fractional-iteration substrate. Derivative dx/dh = "
                "1/(1+log x) makes this transparent.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Ex1-of-E17",
        "page": "83",
        "topic": "Example 1 of E17: for n=1, sum a(r, k) = A_r = (r-1)^{r-1} "
                 "(Cayley-tree counting)",
        "operators": ["fractional_functional_iteration"],
        "note": "Apply E13 with n=-1 and substitute x = 1/y. Inherits.",
    },
    {
        "chapter": 3,
        "unit_id": "C3-Ex2-of-E17",
        "page": "83",
        "topic": "Example 2 of E17: x^{1/x} = a^{1/a} e^h",
        "operators": ["fractional_functional_iteration"],
        "note": "Substitute x = 1/y in E17. Inherits.",
    },
    # -------------------------------------------------------------------
    # Chapter 4 — Iterates of the Exponential Function and an Ingenious
    # Formal Technique
    # -------------------------------------------------------------------
    # §1 — Entry 1: F_r(x) = exp(F_{r-1}(x)) - 1, fractional iteration
    {
        "chapter": 4,
        "unit_id": "C4-E1-def",
        "page": "85-87",
        "topic": "Entry 1: F_r(x) defined for ALL real r by exp-iteration of "
                 "f(x) = e^x - 1, expanded as F_r(x) = sum phi_k(r) x^k = "
                 "sum f_k(x) r^k",
        "operators": ["fractional_functional_iteration"],
        "note": "EXPLICITLY fractional iteration. Berndt: 'Ramanujan tacitly "
                "assumes that F_r(x) can be defined for all real values of r. "
                "He gives no indication how to do this, but Comtet [1, "
                "pp. 144-148] describes how to define arbitrary real iterates "
                "of formal power series.' phi_k(r) is a polynomial in r of "
                "degree k-1 (i.e. iteration index r enters polynomially). "
                "Cleanest possible firing of fractional_functional_iteration.",
    },
    # §2 — Entry 2: F_r'(x) = (1 + F_r) F_{r-1}'
    {
        "chapter": 4,
        "unit_id": "C4-E2",
        "page": "87",
        "topic": "Entry 2: F_r'(x) = (1 + F_r(x)) F_{r-1}'(x) (chain rule on "
                 "iteration)",
        "operators": ["fractional_functional_iteration"],
        "note": "Differentiate F_{r-1}(x) = log(1 + F_r(x)). Inherits.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Cor1-E2",
        "page": "87",
        "topic": "Corollary 1 of E2: F_r'(x) = prod_{k=0}^{r-1} (1 + F_k(x))",
        "operators": ["fractional_functional_iteration"],
        "note": "Apply (2.1) r times. Inherits.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Cor2-E2",
        "page": "87",
        "topic": "Corollary 2 of E2: recursion phi_n(r) - phi_n(r-1) = "
                 "sum (n-k) phi_k(r) phi_{n-k}(r-1) / (n-k)",
        "operators": ["fractional_functional_iteration"],
        "note": "Equate coefficients of x^{n-1} in (2.1). Inherits.",
    },
    # §3 — Entry 3: f_1(x) = x + sum B_n f_n(x) Euler-Maclaurin on iteration
    {
        "chapter": 4,
        "unit_id": "C4-E3",
        "page": "87-88",
        "topic": "Entry 3: f_1(x) = x + sum_{n>=1} B_n f_n(x) (Euler-Maclaurin "
                 "on the iterates)",
        "operators": ["fractional_functional_iteration"],
        "note": "Apply Euler-Maclaurin to the polynomials phi_k(n) summed from "
                "k=0 to r-1. Equate coefficients of r^0. Bernoulli numbers "
                "appear formally (not as Eisenstein-anchored constants) — "
                "Out-of-schema for eisenstein_normal_ordering. Inherits "
                "fractional-iteration tag.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Cor-E3",
        "page": "88",
        "topic": "Corollary of E3: log(f_1(x)) = integral 0 to x of "
                 "(t - f_1(t)) / f_1(t) dt",
        "operators": ["fractional_functional_iteration"],
        "note": "Set r=0 in (3.4). Inherits.",
    },
    # §4 — Entry 4: n f_n(x) = f_1(x) f_{n-1}'(x)
    {
        "chapter": 4,
        "unit_id": "C4-E4",
        "page": "89",
        "topic": "Entry 4: n f_n(x) = f_1(x) f'_{n-1}(x)",
        "operators": ["fractional_functional_iteration"],
        "note": "Apply (4.2) F_{k+r}(x) = F_k(F_r(x)), expand and equate "
                "coefficients of r. The COMPOSITION law for the iterates is "
                "the canonical move of fractional iteration.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Cor1-E4",
        "page": "89",
        "topic": "Corollary 1 of E4: psi_k(n) recursions (parts (i) and (ii))",
        "operators": ["fractional_functional_iteration"],
        "note": "Substitute (4.3) into (4.1). Inherits.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Cor2-E4",
        "page": "90",
        "topic": "Corollary 2 of E4: (n+1) psi_n(1) = n psi_{n-1}(1) + "
                 "2 sum_k B_{2k} 2^{1-2k} psi_{n-2k}(2k)",
        "operators": ["fractional_functional_iteration"],
        "note": "Substitute (4.3) into E3. Bernoulli numbers used as plain "
                "expansion coefficients (no Eisenstein-anchored q-series). "
                "Inherits.",
    },
    # §5 — Entry 5: f_1(x) = (1+x) f_1(log(1+x))
    {
        "chapter": 4,
        "unit_id": "C4-E5",
        "page": "90",
        "topic": "Entry 5: f_1(x) = (1+x) f_1(log(1+x))",
        "operators": ["fractional_functional_iteration"],
        "note": "Apply F_{r-1}(x) = F_r(F_{-1}(x)) = F_r(log(1+x)). Inherits.",
    },
    # §6 — Entry 6(i)-(ii): formulas for phi_n(1), phi_n(-1) and psi_k(n)
    {
        "chapter": 4,
        "unit_id": "C4-E6i",
        "page": "90-91",
        "topic": "Entry 6(i): formulas for phi_n(1) = 1/n! and phi_n(-1) = "
                 "(-1)^{n-1}/n",
        "operators": ["fractional_functional_iteration"],
        "note": "From (1.1)+(1.2): F_1(x) = e^x - 1 so phi_n(1) = 1/n!. From "
                "F_{-1}(x) = log(1+x). Apply Cor 1(ii) of E4. Inherits.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-E6ii",
        "page": "91-92",
        "topic": "Entry 6(ii): psi_1, psi_2, psi_3, psi_4(2r), psi_5(2r), "
                 "psi_6(2r), psi_7(2r) closed forms; f_1(x) explicit through x^7",
        "operators": ["fractional_functional_iteration"],
        "note": "Recursive computation using Cor 1 + Cor 2 of E4. Inherits.",
    },
    # §7 — Entry 7: F_{2r}(x) = y + (r/6) y^2 log z + (r/72) y^3 (...) + ...
    {
        "chapter": 4,
        "unit_id": "C4-E7",
        "page": "92-93",
        "topic": "Entry 7: explicit expansion of F_{2r}(x) when x = y(1 - rx), "
                 "z = 1 - rx — first three terms",
        "operators": ["fractional_functional_iteration"],
        "note": "Direct expansion of (7.2) using (6.3)-(6.5). The 2r-iterate "
                "structure is the fractional iteration index.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Ex1-of-E7",
        "page": "93-94",
        "topic": "Example 1 of E7: f_1(x) f_1'(x) = f_1(x) - f_2(x) + "
                 "sum (2k+1) B_{2k} f_{2k+1}(x)",
        "operators": ["fractional_functional_iteration"],
        "note": "Differentiate E3, multiply by f_1(x), apply E4. Inherits.",
    },
    # §8 — Entry 8: H_x harmonic-number identities
    {
        "chapter": 4,
        "unit_id": "C4-E8",
        "page": "94-95",
        "topic": "Entry 8: sum_{k=1}^x H_k, H_k^2, H_k^3 identities",
        "operators": [],
        "note": "Pure harmonic-sum manipulation by Abel summation. "
                "Out-of-schema (classical analytic number theory).",
    },
    # §9 — "Ingenious Formal Technique": substitute f(x^n) -> phi(n)
    # This is Ramanujan's signature pre-Master move.
    # The §9 framework + Examples 1-4 are all variants on contour-integral
    # evaluations via residue theorem applied to functions where x is to be
    # replaced by phi-substitution.
    {
        "chapter": 4,
        "unit_id": "C4-S9-framework",
        "page": "95-96",
        "topic": "§9 Ramanujan's 'ingenious formal technique': f(x^n) -> phi(n) "
                 "via Maclaurin expansion + substitution",
        "operators": ["master_theorem"],
        "note": "Berndt: \"If two functions of x be equal, then a general "
                "theorem can be formed by simply writing phi(n) instead of x^n "
                "in the original theorem.\" THIS IS THE PROTO-MASTER-THEOREM "
                "move: replace x^n by phi(n) in any identity. The illustrative "
                "example tan^{-1} x + tan^{-1}(1/x) = pi/2 -> sum (-1)^n "
                "(phi(2n+1) + phi(-2n-1))/(2n+1) = (pi/2) phi(1) IS the "
                "Master-Theorem-style coefficient-extraction move. Although the "
                "modern Master-Theorem form (with Gamma(s) phi(-s)) doesn't "
                "fire until Entry 11, this framework section IS the pre-form. "
                "Tagging master_theorem because Berndt explicitly: 'In the "
                "introductory chapter of his book [20, p. 15] on the work of "
                "Ramanujan, Hardy quotes Corollary 1 [of E11] and remarks that "
                "this particularly interesting formula was one of Ramanujan's "
                "favorite formulas.' The §9 framework is the precursor.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Ex1-S9",
        "page": "96",
        "topic": "Example 1 of §9: residue-theorem evaluation of integral "
                 "of phi(z) / (z sin(pi z)) gives sum (-1)^k phi(2k+1)/(2k+1) = "
                 "phi(0) pi/4",
        "operators": ["master_theorem"],
        "note": "Strict residue-theorem version of the §9 framework move. "
                "Coefficient extraction via residues. Inherits master_theorem tag.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Ex2-S9",
        "page": "96-97",
        "topic": "Example 2 of §9: similar residue-theorem proof for sum "
                 "(-1)^{k-1} phi(k) = phi(0)",
        "operators": ["master_theorem"],
        "note": "Same machinery applied to x/(1+x) + (1/x)/(1+1/x) = 1. "
                "Inherits.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Ex3-S9",
        "page": "97",
        "topic": "Example 3 of §9: sum (-1)^{k-1} phi(k)/k = phi'(0) "
                 "via log(1+x) - log(1+1/x) = log x",
        "operators": ["master_theorem"],
        "note": "Same machinery. Inherits.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Ex4-S9",
        "page": "97-98",
        "topic": "Example 4 of §9: sum (-1)^{k-1} psi(k)/(k! k) = "
                 "(1/2)(gamma + psi(0))^2 (Euler-gamma evaluation)",
        "operators": ["master_theorem"],
        "note": "Apply Example 3 with phi = psi / Gamma(z+1). Inherits.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Cor1-of-S9",
        "page": "98",
        "topic": "Corollary 1 of §9: sum (-1)^{k-1} x^k / (k! k) ~ "
                 "log x + gamma asymptotic",
        "operators": ["master_theorem"],
        "note": "Berndt mentions this is Ramanujan's pre-Master-Theorem approach "
                "via the §9 framework. The associated INTEGRAL identity is "
                "shown in (9.2), which is integral_0^1 (1-e^{-t})/t dt - "
                "integral_1^x e^{-t}/t dt. Connects to Ch.3 E10 Example 4. "
                "Inherits master_theorem.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Cor2-of-S9",
        "page": "98-99",
        "topic": "Corollary 2 of §9: sum (-1)^{k-1} x^{nk}/(k! k) ~ "
                 "n log x + n gamma (FALSE for n > 2, per Berndt)",
        "operators": ["master_theorem"],
        "note": "Ramanujan's incorrect claim (Berndt corrects it). Apply §9 "
                "machinery to the n-th moment. Even though the claim is wrong, "
                "the OPERATOR fired is the §9-framework substitute-and-expand "
                "move. Inherits master_theorem.",
    },
    # §10 — Entry 10: contour-integral formula for asymptotic generating
    # function via phi(z) cot(pi z) cot(pi(z - n)) / [Gamma(z+1) Gamma(n-z+1)]
    {
        "chapter": 4,
        "unit_id": "C4-E10",
        "page": "100",
        "topic": "Entry 10: contour-integral identity sum phi(k)/[k! (n-k)!] = "
                 "sum phi(n-k) cot(pi n) / [k! Gamma(n-k+1)]",
        "operators": ["master_theorem"],
        "note": "Cot-cot integrand with residues at integers k>=0 AND at "
                "z = n + r for nonpositive integer r — the closest possible "
                "approach to the Master-Theorem form short of the integral "
                "transform itself. Berndt: the corollary specializes to "
                "f(0) = phi(r) which IS the Master-Theorem-style coefficient "
                "extraction at s = r. Inherits master_theorem.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Cor-E10",
        "page": "100-101",
        "topic": "Corollary of E10: 'generating function' framework — "
                 "f(x) = sum phi(k) x^{r-k} / k! gives f(0) = phi(r)",
        "operators": ["master_theorem"],
        "note": "Inherits.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Ex1-E10",
        "page": "101",
        "topic": "Example 1 of E10: with phi(z) = phi(z+1), r = -1, f(0) = phi(0)",
        "operators": ["master_theorem"],
        "note": "Direct application of Corollary. Inherits.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Ex-of-E10-tan-inv",
        "page": "101",
        "topic": "Example of E10: tan^{-1}(1/x) representation gives "
                 "f(0) = pi/2",
        "operators": ["master_theorem"],
        "note": "Apply with phi(z) = sin(pi z / 2) / z. Inherits.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Ex2-E10-v1",
        "page": "101-102",
        "topic": "Example 2 of E10 First Version: f(x) = integral_0^infty "
                 "e^{-t} log(x + t) dt ~ sum k! / x^{k+1} divergent; lim_{x->0} = infty",
        "operators": ["master_theorem"],
        "note": "Asymptotic series, integration by parts. The associated "
                "Master-Theorem application is phi(z) = Gamma(z) in Example 1 "
                "(Berndt: 'Ramanujan deduces this result by setting phi(z) = "
                "Gamma(z) in Example 1'). Inherits.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Ex2-E10-v2",
        "page": "102",
        "topic": "Example 2 of E10 Second Version: continued-fraction "
                 "expansion of f(x) = 1/(x+1) - 1^2/(x+3) - 2^2/(x+5) - ...",
        "operators": [],
        "note": "Standard CF from Wall's book [1, p. 356]. NOT q-Pochhammer, "
                "NOT a Ramanujan-style q-CF; this is a Stieltjes-type analytic "
                "CF expansion of an analytic function. No in-schema operators "
                "fire on this entry itself.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Ex2-E10-v3",
        "page": "102-103",
        "topic": "Example 2 of E10 Third Version: f(x) = e^x integral_x^infty "
                 "e^{-t}/t dt, with closed form via Ch3-Cor2-E2",
        "operators": ["master_theorem"],
        "note": "Applies Ch3-Cor2 of E2 (the §11 sum (-1)^{k-1} x^k / (k! k) = "
                "integral_0^1 (1-e^{-t})/t dt) and the gamma-evaluation (10.7). "
                "Asymptotic series. The Master-Theorem motif is operating "
                "underneath via phi(z) = Gamma(z+1) for the integration-by-parts "
                "expansion. Inherits.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Ex3-E10",
        "page": "103-104",
        "topic": "Example 3 of E10: integral_0^infty e^{-t} (x+t)^n dt ~ "
                 "sum Gamma(n+1) x^{n-k} / Gamma(n-k+1) asymptotic; f(0) = Gamma(n+1)",
        "operators": ["master_theorem"],
        "note": "Berndt: 'Ramanujan deduced this value by letting phi(z) = "
                "Gamma(z+1) and r = n in the Corollary [of E10].' This IS the "
                "Master Theorem applied to the Gamma function. Inherits.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Ex4-E10",
        "page": "104-105",
        "topic": "Example 4 of E10: f(x) = integral_x^infty sin(t-x)/t dt "
                 "evaluated via sum (-1)^k psi(2k+1) x^{2k+1} / (2k+1)!",
        "operators": ["master_theorem"],
        "note": "Berndt: 'Ramanujan evidently put phi(z) = Gamma(z) sin(pi z / 2) "
                "in Example 1 to achieve the value of f(0).' Inherits master_theorem.",
    },
    # §11 — Entry 11: The Master Theorem itself + Corollaries 1-5
    {
        "chapter": 4,
        "unit_id": "C4-E11",
        "page": "105",
        "topic": "Entry 11: integral_0^infty x^{n-1} sum phi(k) (-x)^k / k! dx = "
                 "Gamma(n) phi(-n) — THE MASTER THEOREM",
        "operators": ["master_theorem"],
        "note": "EXPLICIT MASTER THEOREM. This is the chapter's centerpiece. "
                "Berndt: 'In the introductory chapter of his book [20, p. 15] "
                "on the work of Ramanujan, Hardy quotes Corollary 1 and remarks "
                "that this particularly interesting formula was one of "
                "Ramanujan's favorite formulas.' Same form as the QR I "
                "version tagged in diary 20. Canonical master_theorem firing.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Cor1-E11",
        "page": "105",
        "topic": "Corollary 1 of E11: integral_0^infty x^{n-1} sum phi(k)(-x)^k dx = "
                 "pi phi(-n) / sin(pi n) — Master Theorem with Gamma reflection",
        "operators": ["master_theorem"],
        "note": "Replace phi(x) by Gamma(x+1) phi(x) in E11. Use Gamma "
                "reflection formula Gamma(n) Gamma(1-n) = pi/sin(pi n). "
                "This is the version 'of which Ramanujan was especially fond "
                "and made continual use' (per Berndt p. 85). The Hardy "
                "quotation. Inherits master_theorem.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Cor2-E11",
        "page": "105",
        "topic": "Corollary 2 of E11: cosine-Master version with phi(2k)(-x^2)^k",
        "operators": ["master_theorem"],
        "note": "Replace phi(x) by phi(x) cos(pi x / 2) in E11. Inherits.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Cor3-E11",
        "page": "105",
        "topic": "Corollary 3 of E11: half-line cosine transform "
                 "integral cos(nx) sum phi(k)(-x)^k/k! dx = "
                 "sum phi(-2k-1)(-n^2)^k",
        "operators": ["master_theorem", "mellin_pair_reciprocity"],
        "note": "Expand cos(nx) in its Maclaurin series, invert order of "
                "integration and summation, apply E11. The cosine-transform "
                "framing is on the borderline of mellin_pair_reciprocity / "
                "Fourier self-reciprocity. Diary 20 tagged similar QR-II "
                "corollaries as FOURIER_SELF_RECIPROCITY but that operator is "
                "not in the 11-operator basis we're using here (Hunt 5b uses "
                "the diary-25 11-operator vocabulary which dropped FOURIER_"
                "SELF_RECIPROCITY but kept mellin_pair_reciprocity for the "
                "alpha*beta=1 substrate). The α∗β=1 substrate is implicit in "
                "the cosine-transform pair when scaled with 2pi factor. "
                "Tagging both master_theorem and mellin_pair_reciprocity "
                "(borderline, but Berndt's deferral to QRs and the symmetric "
                "x<->n structure make it apt).",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Cor4-E11",
        "page": "105",
        "topic": "Corollary 4 of E11: integral cos(nx) sum phi(2k)(-x^2)^k /(2k)! dx = "
                 "(pi/2) sum phi(-k-1/2)(-n)^k",
        "operators": ["master_theorem", "mellin_pair_reciprocity"],
        "note": "Berndt: 'Corollary 4, which also appears as Corollary (vii) "
                "in Ramanujan's second quarterly report, is more difficult to "
                "prove. We defer a proof and full discussion of Corollary 4 "
                "until our examination of the quarterly reports.' SAME as the "
                "QR II §4(vii) entry tagged in diary 20. Inherits both master + "
                "mellin-pair-reciprocity (the alpha-beta=1 reciprocity is "
                "explicit in the QR II original).",
    },
    {
        "chapter": 4,
        "unit_id": "C4-Cor5-E11",
        "page": "106",
        "topic": "Corollary 5 of E11: Beta-function integral as direct "
                 "Master-Theorem consequence",
        "operators": ["master_theorem"],
        "note": "Beta function B(m+1,n+1) = Gamma(m+1)Gamma(n+1)/Gamma(m+n+2). "
                "Berndt: 'This example is also given in Ramanujan's first "
                "quarterly report, and we defer Ramanujan's proof until then.' "
                "Master Theorem applied to (1-x)^n.",
    },
    # §12 — Entry 12: Fourier-cosine inversion + Parseval
    {
        "chapter": 4,
        "unit_id": "C4-E12",
        "page": "106",
        "topic": "Entry 12(i) + (ii): Fourier cosine transform inversion + "
                 "Parseval (sqrt(2/pi) factor)",
        "operators": [],
        "note": "Fourier cosine transform inversion. The mellin_pair_reciprocity "
                "operator concerns specifically alpha*beta = (1 or pi or 2pi) "
                "Mellin-pair self-dual identities (QR III §15). Pure cosine "
                "self-reciprocity is NOT mellin_pair_reciprocity in the strict "
                "diary-25 sense. Out-of-schema (Fourier self-reciprocity, but "
                "that operator was DROPPED from the 11-op basis between "
                "diaries 20 and 22/24/25 — only the alpha*beta=1 form is "
                "kept). 0 in-schema firings.",
    },
    # §13 — Entry 13(i)-(ii): sin^m x cos^n x and cos^m x cos(nx) integrals
    {
        "chapter": 4,
        "unit_id": "C4-E13i",
        "page": "107",
        "topic": "Entry 13(i): integral sin^m x cos^n x dx = "
                 "Gamma(m/2+1/2) Gamma(n/2+1/2) / (2 Gamma((m+n)/2+1))",
        "operators": ["master_theorem"],
        "note": "Berndt: 'an easy consequence of Corollary 5 of Entry 11'. "
                "Master Theorem application.",
    },
    {
        "chapter": 4,
        "unit_id": "C4-E13ii",
        "page": "107",
        "topic": "Entry 13(ii): integral cos^m x cos(nx) dx = "
                 "pi Gamma(m+1) / (2^{m+1} Gamma((m+n)/2+1) Gamma((m-n)/2+1))",
        "operators": [],
        "note": "Berndt: 'well known. One of the simplest proofs is found in "
                "Whittaker and Watson exercise 39, p. 263.' This is a beta-"
                "integral evaluation. Not specifically Master Theorem-routed in "
                "Berndt's proof (he points to W&W). No in-schema operators fire "
                "in the proof PER SE; the result is in the master_theorem "
                "neighborhood but the proof goes through binomial expansion + "
                "complex exponentials. Marking 0 firings per 'near match != "
                "match' discipline.",
    },
    # §14 — Entry 14: sinh / cos / cosh product identity
    {
        "chapter": 4,
        "unit_id": "C4-E14",
        "page": "107-108",
        "topic": "Entry 14: prod (1 + x^3/n^3) = (sinh(2 pi x) - 2 sinh(pi x) "
                 "cos(pi x sqrt(3))) / (4 pi^3 x^3)",
        "operators": [],
        "note": "Uses the familiar sinh product representation evaluated at "
                "complex points x, x*omega, x*omega-bar where omega = "
                "exp(2 pi i / 3) (a cube root of unity). This is genuinely a "
                "GALOIS-AVERAGE structure (sum over Galois orbit {x, x*omega, "
                "x*omega-bar} of Q(omega) = Q(sqrt(-3))), but the operator "
                "class_field_galois_average per diary 25's decision rule "
                "requires CLASS-FIELD machinery (Galois of Hilbert class field "
                "/ Heegner orbit / class invariants), not just a primitive "
                "cube-root sum on the unit circle. Per diary 22 E32-19's "
                "near-match exclusion convention (omega^j sums for primitive "
                "cube-roots are NOT class_field unless the class-field "
                "structure is explicitly invoked), NOT tagging "
                "class_field_galois_average. Out-of-schema (cyclotomic "
                "evaluation of an infinite product).",
    },
    # §15 — Entry 15: e^{-x} sum G_k x^k / k! representation
    {
        "chapter": 4,
        "unit_id": "C4-E15",
        "page": "108",
        "topic": "Entry 15: e^x sum (-2)^{k-1} x^k / k! sum_{j} 1/(2j+1) = "
                 "sum G_k x^k / k! where G_k = sum_{j<(k-1)/2} 1/(2j+1)",
        "operators": [],
        "note": "Direct integral evaluation. Out-of-schema.",
    },
]


# ---------------------------------------------------------------------------
# Computation
# ---------------------------------------------------------------------------

def compute_saturation(units: list[dict]) -> dict[str, dict]:
    """Per-operator saturation = #units where op fires / #total units.

    Returns a per-operator dict of {n_fires, total, percent}.
    """
    n_total = len(units)
    counts = Counter()
    for u in units:
        for op in u["operators"]:
            counts[op] += 1
    return {
        op: {
            "n_fires": counts.get(op, 0),
            "total": n_total,
            "percent": round(100.0 * counts.get(op, 0) / n_total, 1)
                       if n_total else 0.0,
        }
        for op in OPERATORS
    }


def compute_per_chapter_saturation(units: list[dict]) -> dict[int, dict]:
    """Per-chapter version of saturation."""
    by_chapter: dict[int, list[dict]] = {}
    for u in units:
        by_chapter.setdefault(u["chapter"], []).append(u)
    return {ch: compute_saturation(items) for ch, items in by_chapter.items()}


def write_tags_csv(units: list[dict]) -> None:
    RESULTS_DIR.mkdir(exist_ok=True, parents=True)
    with open(TAGS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "chapter",
                "unit_id",
                "page",
                "topic",
                "operators",
                "note",
            ],
        )
        writer.writeheader()
        for u in units:
            writer.writerow(
                {
                    "chapter": u["chapter"],
                    "unit_id": u["unit_id"],
                    "page": u["page"],
                    "topic": u["topic"],
                    "operators": ";".join(u["operators"]),
                    "note": u["note"],
                }
            )


def main() -> None:
    units = TAGGED_UNITS
    write_tags_csv(units)

    print("Hunt 5b — NB Part 1 Ch. 3 + Ch. 4 operator tagging")
    print("=" * 70)
    print()
    print(f"Total tagged proof units: {len(units)}")
    print(f"  Ch. 3 (Combinatorial Analysis + Series Inversions): "
          f"{sum(1 for u in units if u['chapter'] == 3)}")
    print(f"  Ch. 4 (Iterates of Exp Fn + Ingenious Formal Technique): "
          f"{sum(1 for u in units if u['chapter'] == 4)}")
    print()
    print("Output:")
    print(f"  {TAGS_CSV.relative_to(REPO_ROOT)}")
    print()

    overall = compute_saturation(units)
    print(f"Per-operator saturation (across all {len(units)} units):")
    print("-" * 70)
    print(f"  {'Operator':<35s} {'Fires':>7s} {'Total':>7s} {'Sat %':>7s}")
    print("-" * 70)
    for op in OPERATORS:
        info = overall[op]
        marker = "  " if info["n_fires"] > 0 else " *"
        print(f"  {marker}{op:<33s} {info['n_fires']:>7d} {info['total']:>7d} "
              f"{info['percent']:>6.1f}%")
    n_unfired = sum(1 for op in OPERATORS if overall[op]["n_fires"] == 0)
    print(f"  ({n_unfired} of {len(OPERATORS)} operators NEVER fire — marked *)")
    print()

    by_chapter = compute_per_chapter_saturation(units)
    for ch in sorted(by_chapter):
        n = sum(1 for u in units if u["chapter"] == ch)
        print(f"Per-operator saturation (Ch. {ch}, {n} units):")
        print("-" * 70)
        for op in OPERATORS:
            info = by_chapter[ch][op]
            if info["n_fires"] > 0:
                print(f"  {op:<35s} {info['n_fires']:>4d}/{info['total']:<4d} "
                      f"= {info['percent']:>5.1f}%")
        # show the zero-firing operators tersely
        zeros = [op for op in OPERATORS if by_chapter[ch][op]["n_fires"] == 0]
        if zeros:
            print(f"  (zero-firing in Ch. {ch}: {', '.join(zeros)})")
        print()


if __name__ == "__main__":
    main()
