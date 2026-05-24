#!/usr/bin/env python3
"""
Hunt 1 inventory: Lost Notebook pp. 341-344 K3-parameterisation test.

Reads a hand-built inventory of identities visible on Ramanujan's Lost
Notebook facsimile pages 341, 342, 343 (and the predecessor p. 340 for
context, and the successor p. 344 which is what the user-provided
priority_sources/page-343.jpg actually contains due to an off-by-one in
filename indexing). Cross-references each identity against the
Ono-Trebat-Leder paper (arXiv:1510.00735) and the Agarwal-Garg paper
(arXiv:2309.00427) for K3-parameterisation status.

Outputs analysis/results/hunt1_k3_inventory.csv with columns:
  - page_id (340/341/342/343/344)
  - identity_index (1, 2, ... in order on the page)
  - identity_summary (one-line LaTeX or English)
  - source_in_ono (which section of Ono's paper, if any, discusses this identity)
  - k3_status (one of: K3_PARAMETERISATION_CONFIRMED, K3_CANDIDATE_PER_ONO,
                       NOT_K3, UNKNOWN_FROM_FACSIMILE)
  - confidence (one of: high/medium/low)
  - notes

CRITICAL FACSIMILE/PAGE-NUMBERING NOTE
======================================
The `chatgpt-pro-mining/.../priority_sources/lost_notebook_pages_341_343/`
folder contains files page-341.jpg, page-342.jpg, page-343.jpg. The
filename indexing is **0-indexed offset** from the Sirinudi PDF: the file
`page-N.jpg` corresponds to Lost-Notebook-reprint (Narosa 1988) page
N+1. So:
  - file page-340.jpg  =  LN reprint p. 341  (the FAMOUS 1729 page, with
                          the three rational functions (i),(ii),(iii) and
                          the examples 9^3+10^3=12^3+1 etc.)
  - file page-341.jpg  =  LN reprint p. 342  (NOT cubes; Weber-style
                          class invariants f_1(sqrt(-n)))
  - file page-342.jpg  =  LN reprint p. 343  (NOT cubes; Diophantine
                          approximations to 5th and 7th roots of 2)
  - file page-343.jpg  =  LN reprint p. 344  (NOT cubes; nested-radical
                          / denesting identities)

This is verified by:
  1. comparing file page-340.jpg's content against Ono's Appendix
     (which reproduces what Ono labels as LN p. 341 and shows the same
     "if (i),(ii),(iii) then a^3+b^3=c^3+(-1)^n" content);
  2. Agarwal-Garg arXiv:2309.00427 cites the rational functions
     1+53x+9x^2 / 1-82x-82x^2+x^3 (etc.) as "Lost notebook p. 341"
     and these are precisely what's visible on file page-340.jpg, NOT
     on file page-341.jpg.
  3. The page-bottom handwritten numbers ("341", "342", "343", "344")
     are visible after flipping the images top-to-bottom (the scans are
     mirrored/inverted).

HUNT 1 INTERPRETATION
=====================
HUNT_MAP §1 says "Lost Notebook pp. 341-343 (the '1729 manipulations')".
Per Ono pp. 341 is the cube material; he speculated about "the other
near-counterexamples Ramanujan tabulates on pages 342-343" as also
parameterising K3 surfaces.

But pp. 342, 343, 344 of the facsimile pages here are NOT cube-identity
continuation pages. They are:
  - p. 342: a class-invariants table (Weber f_1 at imag. quadratic
            discriminants) + modular polynomials. This is Hunt 4
            territory, not Hunt 1.
  - p. 343: best Diophantine approximations |a^m b^n theta - p_{m,n}|
            < exp-bound for theta = 5th, 7th roots of 2. Pure
            Liouville/Thue/Roth-style approximation theory.
  - p. 344: nested-radical / denesting identities (3+sqrt(5)/2-sqrt(5)
            etc.) at eta^5 = 2 or eta = 3. Algebraic-number-theory.

So Ono's speculation that pp. 342-343 contain "more cube identities" is
likely a misremembering or a reference to a different edition's
pagination. The Berndt-Andrews Lost Notebook Part IV chapter on
"Approximations and asymptotic methods, including 1729" almost certainly
treats LN p. 341 (the cube page) as the 1729 material, and pp. 342-344
as a *separate* cluster of denesting / approximation / class-invariant
identities.

We therefore inventory ALL identities on pp. 340-344 (with the cube
page p. 341 as the centerpiece, and the immediate-neighbour pages
included to make the K3-vs-other-content split explicit), and tag each
one with whether Ono's K3 machinery applies.

OUTPUT
======
analysis/results/hunt1_k3_inventory.csv with one row per identifiable
identity. The verdict on the HUNT_MAP §1 60-80% K3 prediction is
computed at the bottom of the script and printed to stdout.
"""

from __future__ import annotations

import csv
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class Identity:
    page_id: int
    identity_index: int
    identity_summary: str
    source_in_ono: str
    k3_status: str
    confidence: str
    notes: str


# ============================================================================
# Inventory  --  hand-built from facsimile readings
# ============================================================================
# Pages run 340-344. Each Identity is one labelled formula or coherent block.
# `identity_summary` is plain ASCII (or LaTeX-like) for CSV portability.
# `k3_status` ∈ {K3_PARAMETERISATION_CONFIRMED, K3_CANDIDATE_PER_ONO,
#                NOT_K3, UNKNOWN_FROM_FACSIMILE}.
# `confidence` ∈ {high, medium, low}.
# ============================================================================

INVENTORY: List[Identity] = [
    # ------------------------------------------------------------------
    # Page 340 (the 5th-power factorization page, predecessor to 1729)
    # NOT in the HUNT_MAP §1 cube-page bundle but adjacent and
    # methodologically related (Ramanujan exploring sums of like powers).
    # ------------------------------------------------------------------
    Identity(
        page_id=340,
        identity_index=1,
        identity_summary=(
            "(x+a)^5 - (x+b)^5 = A(x+p)^5 + B(x+q)^5 + C(x+n)^5  "
            "[fifth-power factorization Ansatz]"
        ),
        source_in_ono="NOT discussed (Ono treats only cube/3rd-power case)",
        k3_status="NOT_K3",
        confidence="high",
        notes=(
            "Fifth-power analogue of the (a,b,c,d) cube identity. The "
            "associated surface is a quintic in 5 variables, not a K3 / "
            "cubic-surface elliptic fibration. Setting it equal to a sum "
            "of three other 5th powers gives a 5-variable Waring-type "
            "relation, not the 2-parameter family Ono needs for K3."
        ),
    ),
    Identity(
        page_id=340,
        identity_index=2,
        identity_summary=(
            "A/(1-pz) + B/(1-qz) + C/(1-nz) = (alpha + beta z + gamma z^2) "
            "/ (1 + delta z + eps z^2 + phi z^3)  "
            "[partial-fraction decomposition expressing A,B,C]"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes=(
            "Same as a_n via Master Theorem -- this is the "
            "generating-function expansion that goes with the 5th-power "
            "Ansatz above. Ramanujan tabulates alpha, beta, gamma, delta, "
            "eps, phi explicitly in terms of a, b. No algebraic-surface "
            "interpretation by Ono or anyone else."
        ),
    ),
    Identity(
        page_id=340,
        identity_index=3,
        identity_summary=(
            "If z=1/N, N = 1/2(a+b) + 1/2 M(a-b), then 1 + delta z + eps z^2 "
            "+ phi z^3 = 0 is equivalent to 5(a+b)(M^3-M) = (a^2-b^2)(5M^2-1)"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes=(
            "Quintic-resolvent reduction. Reduces the cubic-in-z denominator "
            "to a cubic in M with parameter (a,b). Note 5M^3-M and "
            "5M^2-1 are related to the modular polynomial for level 5 -- "
            "WEAKLY suggestive of modular-form content, but NOT K3."
        ),
    ),
    Identity(
        page_id=340,
        identity_index=4,
        identity_summary=(
            "x{(x+a)^5 + (x+b)^5} = A(x+p)^5 + B(x+q)^5 + Cx^5  "
            "with p = (a^2+b^2) / (a^2+b^2-(a-b)*sqrt(5ab)),  "
            "q = (a^2+b^2) / (a^2+b^2+(a-b)*sqrt(5ab)),  "
            "B = (a^2+b^2 + a-b*sqrt(5ab))^4 / (8(a-b)*sqrt(5ab)*(a^2+b^2)^(3/2)),  "
            "A = -(a^2+b^2 - a-b*sqrt(5ab))^4 / (8(a-b)*sqrt(5ab)*(a^2+b^2)^(3/2)),  "
            "C = (a^5-b^5)(a-b)^3 / (a^2+b^2)^2"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes=(
            "Closed form for the 4-parameter Ansatz with the extra "
            "constraint x{...} = ... -- gives an explicit "
            "decomposition of x(x+a)^5+x(x+b)^5 into three 5th powers. "
            "The sqrt(5ab) signals this lives over Q(sqrt(5ab)) and "
            "may give a K3 over that base, but Ono does not address the "
            "5th-power case at all."
        ),
    ),
    Identity(
        page_id=340,
        identity_index=5,
        identity_summary=(
            "{x^5(n^2+3)^2(n^4+42n^2+9)^2 + x(n^2-3)(n^2+6n+3)}^5  "
            "- {x^5(n^2+3)^2(n^4+42n^2+9)^2 + x(n^2-3)(n^2-6n+3)}^5  "
            "= {x^4(n^2+3)(n^4+42n^2+9)(n^6+6n^5+18n^4-10n+9) + (n^2-3)}^5  "
            "- {x^4(n^2+3)(n^4+42n^2+9)(n^6-6n^5+18n^4+18n+9) + (n^2-3)}^5  "
            "+ {6n*x^4(n^2+6n-3)}^5 - {6n*x^4(n^2-6n-3)}^5  "
            "[explicit 6-term 5th-power identity in (x,n)]"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="medium",
        notes=(
            "Two-parameter (x,n) family of 5th-power identities. "
            "Structurally analogous to Ono's k(T) on the cubic side: a "
            "2-parameter family of solutions to a Waring-type equation. "
            "Ono's K3 result is specific to the 3rd-power Pic18 surface; "
            "the 5th-power analogue would (if it works) be a different "
            "kind of higher-degree algebraic variety, not a K3. Unknown "
            "whether any modern arithmetic-geometry paper treats this -- "
            "FOLLOW-UP LEAD."
        ),
    ),
    # ------------------------------------------------------------------
    # Page 341 -- THE FAMOUS 1729 PAGE (cube identities)
    # This is what Ono's Appendix reproduces.
    # ------------------------------------------------------------------
    Identity(
        page_id=341,
        identity_index=1,
        identity_summary=(
            "(i)  (1 + 53x + 9x^2) / (1 - 82x - 82x^2 + x^3) "
            "= sum a_n x^n  =  sum alpha_{n-1} x^{-n}"
        ),
        source_in_ono=(
            "Introduction (4), p. 2; Appendix shows the original page; "
            "Theorem 1.1 of Agarwal-Garg arXiv:2309.00427 typesets (1.2)"
        ),
        k3_status="K3_PARAMETERISATION_CONFIRMED",
        confidence="high",
        notes=(
            "First of three rational functions whose Taylor / Laurent "
            "coefficients (a_n, alpha_{n-1}) feed into the cube identity "
            "a_n^3 + b_n^3 = c_n^3 + (-1)^n. The denominator "
            "1-82x-82x^2+x^3 has roots that parameterise the K3 surface "
            "in Ono Theorem 1.3 (Picard 18). This rational function and "
            "the next two together carry the FULL K3 parameterisation."
        ),
    ),
    Identity(
        page_id=341,
        identity_index=2,
        identity_summary=(
            "(ii)  (2 - 26x - 12x^2) / (1 - 82x - 82x^2 + x^3) "
            "= sum b_n x^n  =  sum beta_{n-1} x^{-n}"
        ),
        source_in_ono="Same as (i); part of the same triple",
        k3_status="K3_PARAMETERISATION_CONFIRMED",
        confidence="high",
        notes=(
            "Second of the three rational functions. Same denominator "
            "(level-3 structure) as (i). Coefficients are b_n."
        ),
    ),
    Identity(
        page_id=341,
        identity_index=3,
        identity_summary=(
            "(iii)  (2 + 8x - 10x^2) / (1 - 82x - 82x^2 + x^3) "
            "= sum c_n x^n  =  sum gamma_{n-1} x^{-n}"
        ),
        source_in_ono="Same as (i); part of the same triple",
        k3_status="K3_PARAMETERISATION_CONFIRMED",
        confidence="high",
        notes=(
            "Third of the three rational functions. Coefficients c_n."
        ),
    ),
    Identity(
        page_id=341,
        identity_index=4,
        identity_summary=(
            "Then a_n^3 + b_n^3 = c_n^3 + (-1)^n,  "
            "and alpha_n^3 + beta_n^3 = gamma_n^3 + (-1)^n  "
            "[the master cube identity]"
        ),
        source_in_ono=(
            "Equation (1.2)/(1.3) -- Ono cites this as Ramanujan's "
            "parameterisation of Euler's diophantine X^3+Y^3=Z^3+W^3"
        ),
        k3_status="K3_PARAMETERISATION_CONFIRMED",
        confidence="high",
        notes=(
            "The K3 surface X^3+Y^3 = k(T) in Ono Theorem 1.3 is built "
            "from a finite-truncation polynomial parameterisation that "
            "Ono extracts from precisely this identity together with "
            "the rational-function expansions (i),(ii),(iii)."
        ),
    ),
    Identity(
        page_id=341,
        identity_index=5,
        identity_summary="Examples:  135^3 + 138^3 = 172^3 - 1",
        source_in_ono="Appendix (image) lists this",
        k3_status="K3_PARAMETERISATION_CONFIRMED",
        confidence="high",
        notes=(
            "An integer point on the K3 surface. Corresponds to a "
            "specific (n, parameterisation) value."
        ),
    ),
    Identity(
        page_id=341,
        identity_index=6,
        identity_summary="Examples:  11161^3 + 11468^3 = 14258^3 + 1",
        source_in_ono="Appendix (image) lists this",
        k3_status="K3_PARAMETERISATION_CONFIRMED",
        confidence="high",
        notes="Integer point on the same K3.",
    ),
    Identity(
        page_id=341,
        identity_index=7,
        identity_summary="Examples:  791^3 + 812^3 = 1010^3 - 1",
        source_in_ono="Appendix (image) lists this",
        k3_status="K3_PARAMETERISATION_CONFIRMED",
        confidence="high",
        notes=(
            "Integer point. Note 812 (not 818 as in Agarwal-Garg) --"
            "appears 812 on the facsimile but Agarwal-Garg cites 818; "
            "possible OCR ambiguity; needs primary-source check."
        ),
    ),
    Identity(
        page_id=341,
        identity_index=8,
        identity_summary="Examples:  65601^3 + 67402^3 = 83802^3 + 1",
        source_in_ono="Appendix (image) lists this",
        k3_status="K3_PARAMETERISATION_CONFIRMED",
        confidence="high",
        notes="Integer point.",
    ),
    Identity(
        page_id=341,
        identity_index=9,
        identity_summary="Examples:  9^3 + 10^3 = 12^3 + 1",
        source_in_ono="Appendix (image) lists this; 1.1 of Ono mentions",
        k3_status="K3_PARAMETERISATION_CONFIRMED",
        confidence="high",
        notes=(
            "The famous 1729 example, written as 12^3 + 1 form. "
            "Note 9^3+10^3 = 729+1000 = 1729 = 12^3 + 1."
        ),
    ),
    Identity(
        page_id=341,
        identity_index=10,
        identity_summary="Examples:  6^3 + 8^3 = 9^3 - 1",
        source_in_ono="Appendix (image) lists this",
        k3_status="K3_PARAMETERISATION_CONFIRMED",
        confidence="high",
        notes=(
            "Small integer point. 216+512=728=729-1=9^3-1."
        ),
    ),
    Identity(
        page_id=341,
        identity_index=11,
        identity_summary=(
            "If u_n = sqrt(a^2+4) / ([(a+sqrt(a^2+4))/2]^n - [(a-sqrt(a^2+4))/2]^n)  "
            "[Binet form for the Fibonacci-like recurrence with parameter a],  "
            "then  -c + b*u_{n+1}/u_n + sqrt((c + b*u_{n+1}/u_n)^2 + (-1)^n * u^2_{n+1}) / 2  "
            "= 1/(a + 1/(a + 1/(a + ... 1/(a + b/(c + a/(a + ...))))))  "
            "[continued-fraction associated with the recurrence]"
        ),
        source_in_ono="NOT discussed -- not in Ono's Appendix or text",
        k3_status="UNKNOWN_FROM_FACSIMILE",
        confidence="medium",
        notes=(
            "BELOW the cube-identity block, separated by a horizontal "
            "line. Ramanujan writes a u_n in Binet form and gives a "
            "continued-fraction expression. Looks like a *different* "
            "identity entirely (continued-fraction interpretation of "
            "Fibonacci-like recurrence). Not a K3 statement; not even "
            "obviously cube-related. May be a separate notebook entry "
            "that landed on the same physical page during the scrap-paper "
            "compositing of the Lost Notebook. CONFIRMATION "
            "REQUIRED via Andrews-Berndt Part IV (chapter on this page)."
        ),
    ),
    # ------------------------------------------------------------------
    # Page 342 -- WEBER'S RESULTS (class invariants)
    # NOT cube-identity continuation; this is Hunt 4 territory.
    # ------------------------------------------------------------------
    Identity(
        page_id=342,
        identity_index=1,
        identity_summary=(
            "Header: cross-reference to NB 'Page 378' -- Z^4 - 5Z^3 + 3Z^2 + 3Z + 2,  "
            "Z = f(sqrt(-21))/sqrt(2) + sqrt(2)/f(sqrt(-21));  "
            "'Z ought to be {f(sqrt(-21))}^2 / sqrt(2) + sqrt(2)/{f(sqrt(-21))}^2'"
        ),
        source_in_ono="NOT discussed (Ono's paper is exclusively cube-focused)",
        k3_status="NOT_K3",
        confidence="high",
        notes=(
            "Self-referential CORRECTION by Ramanujan to an entry in his "
            "notebook p. 378 -- saying the modular polynomial should "
            "involve f(sqrt(-21))^2 / sqrt(2) (square in the numerator) "
            "rather than f(sqrt(-21)) / sqrt(2). f here is Weber's modular "
            "function (NOT to be confused with f_n the elliptic-eta). "
            "This is class-invariants / singular-moduli / modular-equation "
            "errata, NOT K3 surfaces."
        ),
    ),
    Identity(
        page_id=342,
        identity_index=2,
        identity_summary=(
            "Header: cross-reference to NB 'Page 500' -- "
            "(x + 1/x)^2 - (5+sqrt(41))/2 (x + 1/x) + (7+sqrt(41))/2 = 0,  "
            "x*sqrt(2) = f(sqrt(-41));  "
            "'x*sqrt(2) ought to be {f(sqrt(-41))}^2'"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes=(
            "Another self-correction to NB p. 500 -- a modular polynomial "
            "in (x+1/x) where x*sqrt(2) was claimed = f(sqrt(-41)) but "
            "should equal {f(sqrt(-41))}^2. Class-invariants / singular "
            "moduli; NOT K3."
        ),
    ),
    Identity(
        page_id=342,
        identity_index=3,
        identity_summary=(
            "Section header (UNDERLINED): 'Weber's Results'  "
            "[introduces a table of f_1(sqrt(-n)) class invariants]"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes=(
            "Ramanujan explicitly labels the next block as Weber's class "
            "invariants. Weber's f_1 is the (eta(z/2)/eta(z))^{1/24} type "
            "function evaluated at CM points; values are algebraic units "
            "in ring-class fields. This is the GERMAN modular tradition, "
            "NOT cube-identity territory."
        ),
    ),
    Identity(
        page_id=342,
        identity_index=4,
        identity_summary=(
            "Table row:  f_1(sqrt(-20)) = t^(7/8)  with modular polynomial  "
            "t^8 - (1+sqrt(5))/2 * (2 t^4 + 1) = 0"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes=(
            "Class invariant at discriminant -20 (class number 2). "
            "Modular polynomial relates t = f_1(sqrt(-20)) to a 'simpler' "
            "modular quantity sqrt(5) = unit in Q(sqrt(5)) = genus field "
            "of Q(sqrt(-5)). This is HUNT 4 territory (singular moduli)."
        ),
    ),
    Identity(
        page_id=342,
        identity_index=5,
        identity_summary=(
            "Table row:  f(sqrt(-27)) = t^(3/2)  with modpoly  "
            "t^9 - 3 t^6 - 3 t^3 - 1 = 0"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes=(
            "Discriminant -27. Modpoly is the well-known level-3 / "
            "trisection equation t^9 - 3t^6 - 3t^3 - 1 = 0 (Ramanujan "
            "uses this elsewhere for sin/cos triplication). Class number "
            "of -27 is 3 (it has the cubic field Q(sqrt(-3), cuberoot)). "
            "Hunt 4 / class-field territory; NOT K3."
        ),
    ),
    Identity(
        page_id=342,
        identity_index=6,
        identity_summary=(
            "Table row:  f_1(sqrt(-26)) = t^(3/2)  with modpoly  "
            "t^6 - t^4 - (3+sqrt(13))/2 (t^2 + 1) = 0"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes=(
            "Discriminant -104 (= -4*26) or fundamental discriminant -52. "
            "Genus field involves sqrt(13). Hunt 4 territory; NOT K3."
        ),
    ),
    Identity(
        page_id=342,
        identity_index=7,
        identity_summary=(
            "Table row:  f(sqrt(-29)) = t^(3/2)  with modpoly  "
            "2 t^{12} - 9 t^9 - 8 t^6 - 5 = sqrt(29) (t^6 + 1)^2"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes=(
            "Discriminant -29. Hunt 4 territory. Note involves sqrt(29) "
            "(genus field structure)."
        ),
    ),
    Identity(
        page_id=342,
        identity_index=8,
        identity_summary=(
            "Table row:  f(sqrt(-35)) = t  with modpoly  "
            "t^3 - 2 = (1+sqrt(5))/2 * (t^3 - t)"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes=(
            "Discriminant -35. Hunt 4 territory. Involves sqrt(5) genus."
        ),
    ),
    Identity(
        page_id=342,
        identity_index=9,
        identity_summary=(
            "Table row:  f_1(sqrt(-36)) = t^(3/8)  with modpoly  "
            "t^6 - 4 t^3 - 2 = 2 sqrt(3) (t^3 + 1)"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes="Discriminant -36. Hunt 4 territory. Involves sqrt(3).",
    ),
    Identity(
        page_id=342,
        identity_index=10,
        identity_summary=(
            "Table row:  f_1(sqrt(-38)) = t^(3/2)  with modpoly  "
            "t^6 - 2 t^4 - (2 t^2 + 1)(1 + sqrt(2)) = 0"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes="Discriminant -38. Hunt 4 territory.",
    ),
    Identity(
        page_id=342,
        identity_index=11,
        identity_summary=(
            "Table row:  f(sqrt(-39)) = t^3 sqrt(2)  with modpoly  "
            "t^6 - (3+sqrt(13))/2 (t^3 + 1) = 0"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes="Discriminant -39. Hunt 4 territory. Involves sqrt(13).",
    ),
    Identity(
        page_id=342,
        identity_index=12,
        identity_summary=(
            "Table row:  f(sqrt(-41)) = t^(3/2)  with modpoly  "
            "(t^2 + 1/t^2)^2 - (5+sqrt(41))/2 (t^2 + 1/t^2) + (7+sqrt(41))/2 = 0"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes=(
            "Discriminant -41. Hunt 4 territory. Note: same polynomial "
            "in (x+1/x) form as appeared in the header reference to "
            "NB p. 500. This is the self-correction Ramanujan is "
            "applying to himself at the top of the page."
        ),
    ),
    Identity(
        page_id=342,
        identity_index=13,
        identity_summary=(
            "Table row:  f_1(sqrt(-44)) = t^(3/8)  with modpoly  "
            "t^{12} - (6 + 2 sqrt(11)) t^8 + (8 + 2 sqrt(11)) t^4 - (3 + sqrt(11)) = 0"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes="Discriminant -44. Hunt 4 territory. Involves sqrt(11).",
    ),
    Identity(
        page_id=342,
        identity_index=14,
        identity_summary=(
            "Table row:  f_1(sqrt(-50)) = t^(3/2)  with modpoly  "
            "t^3 - t^2 = (1+sqrt(5))/2 (t + 1)"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes="Discriminant -50. Hunt 4 territory.",
    ),
    Identity(
        page_id=342,
        identity_index=15,
        identity_summary=(
            "Table row:  f_1(sqrt(-51)) = t^(3/2)  with modpoly  "
            "t^9 - (4 + sqrt(17)) t^6 - t^3 - 1 = 0"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes="Discriminant -51. Hunt 4 territory. Involves sqrt(17).",
    ),
    Identity(
        page_id=342,
        identity_index=16,
        identity_summary=(
            "Table row:  f_1(sqrt(-52)) = t^(7/8)  with modpoly  "
            "t^8 - 2 (4 + sqrt(13)) t^4 - (2 + sqrt(13))/2 = 0"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes="Discriminant -52. Hunt 4 territory.",
    ),
    Identity(
        page_id=342,
        identity_index=17,
        identity_summary=(
            "Table row:  f(sqrt(-63)) = t sqrt(2)  with modpoly  "
            "(t^6 + 3 t^3 - 1) / (t^6 - t^3 + 1) = sqrt(7/3)"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes=(
            "Discriminant -63. Hunt 4 territory. Note sqrt(7/3) -- "
            "involves rationals over Q(sqrt(7), sqrt(3))."
        ),
    ),
    Identity(
        page_id=342,
        identity_index=18,
        identity_summary=(
            "Table row:  f(sqrt(-87)) = t^(3/2)  with modpoly  "
            "t^9 - (13 + 2 sqrt(33)) t^6 - (8 + sqrt(33)) t^3 - 1 = 0"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes="Discriminant -87. Hunt 4 territory. Involves sqrt(33).",
    ),
    # ------------------------------------------------------------------
    # Page 343 -- BEST DIOPHANTINE APPROXIMATIONS
    # NOT cube identities; pure approximation theory.
    # ------------------------------------------------------------------
    Identity(
        page_id=343,
        identity_index=1,
        identity_summary=(
            "Block 1: theta = 5th root of 2  (= 2^{1/5});  "
            "a = 1/(5sqrt(2) - 1),  b = sqrt(5) / [(1 + 5sqrt(4))^{5/2}];  "
            "then  a^m b^n theta  =  p_{m,n} + eps_{m,n}  "
            "where  |eps_{m,n}| = O( 5^{n/2} / "
            "[(5sqrt(4) - 2*5sqrt(4) cos(2*pi*s/5) + 1)^{m/2} "
            " * (5sqrt(16) + 2*5sqrt(4) cos(4*pi*s/5) + 1)^{(2n)/2}] ),  "
            "s the most unfavourable of 1,2,3,4"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes=(
            "BEST DIOPHANTINE APPROXIMATION to 2^{1/5}. Says: choose "
            "multipliers a (= unit in Z[2^{1/5}]) and b (involving "
            "sqrt(5) and ratios of (1 + 2^{2/5})^{5/2}); then a^m b^n "
            "2^{1/5} has a rational approximation p_{m,n} whose error is "
            "exponentially small in m and n, with the explicit base "
            "involving the conjugates of 2^{1/5}. This is Thue-Siegel-"
            "Roth-style approximation theory; NOT K3. The product over "
            "conjugates is essentially Mahler measure of the minimal "
            "polynomial x^5 - 2 = 0."
        ),
    ),
    Identity(
        page_id=343,
        identity_index=2,
        identity_summary=(
            "Block 2: theta = 7th root of 2  (= 2^{1/7});  "
            "a = 1/(7sqrt(2) - 1),  b = 7/(7sqrt(8) - 1)*7,  "
            "c = (7sqrt(2) + 1)/(7sqrt(4) - 7sqrt(2) + 1);  "
            "then  a^l b^m c^n theta  =  p_{l,m,n} + eps_{l,m,n}  "
            "where  |eps_{l,m,n}| = O( 7^m * (7sqrt(4) + 2*7sqrt(2) cos(2*pi*s/5) + 1)^{2n} / "
            "[ (7sqrt(4) - 2*7sqrt(2) cos(2*pi*s/7) + 1)^{l/2} "
            "  * (7sqrt(64) - 2*7sqrt(8) cos(6*pi*s/7) + 1)^{(7m)/2} "
            "  * (7sqrt(64) + 2*7sqrt(8) cos(6*pi*s/7) + 1)^{m/2} ] ),  "
            "s the most unfavourable of 1,2,3,4,5,6"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes=(
            "BEST DIOPHANTINE APPROXIMATION to 2^{1/7} using THREE "
            "multipliers a, b, c (vs. two for the 5th-root case). The "
            "extra multiplier reflects that 2^{1/7} sits in a degree-7 "
            "extension and needs more units to enumerate the best "
            "approximations. The conjugate-product structure is the "
            "explicit form for the 6 non-trivial Galois conjugates of "
            "2^{1/7}. Again pure approximation theory; NOT K3."
        ),
    ),
    # ------------------------------------------------------------------
    # Page 344 -- DENESTING / NESTED-RADICAL IDENTITIES
    # NOT cube identities; algebraic number theory (denesting).
    # ------------------------------------------------------------------
    Identity(
        page_id=344,
        identity_index=1,
        identity_summary=(
            "For eta^5 = 2:  (5sqrt(3 + 2 eta) - 5sqrt(4 - 4 eta)) / "
            "(5sqrt(3 + 2 eta) + 5sqrt(4 - 4 eta))  =  2 + eta + eta^2 + eta^3"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes=(
            "Denesting identity: ratio of two fifth roots collapses to "
            "a polynomial in eta = 2^{1/5}. Ramanujan-style denesting. "
            "NOT K3."
        ),
    ),
    Identity(
        page_id=344,
        identity_index=2,
        identity_summary=(
            "For eta^5 = 2:  (sqrt(eta + 3) + sqrt(5 eta - 5)) / "
            "(sqrt(eta + 3) - sqrt(5 eta - 5))  =  eta + eta^2"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes="Denesting. NOT K3.",
    ),
    Identity(
        page_id=344,
        identity_index=3,
        identity_summary=(
            "For eta^5 = 2:  (sqrt(eta^2 + 1) + sqrt(4 eta - 3)) / "
            "(sqrt(eta^2 + 1) - sqrt(4 eta - 3))  =  (1/5)(1 + eta^2 + eta^3 + 1 eta^4)^2"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="medium",
        notes=(
            "Denesting -- the RHS exponent '1 eta^4' may be a misread; "
            "facsimile shows what looks like an isolated '1' before eta^4. "
            "Denesting. NOT K3."
        ),
    ),
    Identity(
        page_id=344,
        identity_index=4,
        identity_summary=(
            "For eta^5 = 3:  (sqrt(eta^2 + 1) + sqrt(5 eta - 5)) / "
            "(sqrt(eta^2 + 1) - sqrt(5 eta - 5))  =  1/eta + eta + eta^2 + eta^3"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes="Denesting. NOT K3.",
    ),
    Identity(
        page_id=344,
        identity_index=5,
        identity_summary=(
            "For eta^5 = 2:  sqrt(1 + eta^2)  =  (eta^4 + eta^3 + eta - 1) / sqrt(5)"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes=(
            "Square-root simplification: sqrt(1+eta^2) lives in Q(eta) "
            "where eta = 2^{1/5}, RHS giving the explicit element. "
            "Denesting. NOT K3."
        ),
    ),
    Identity(
        page_id=344,
        identity_index=6,
        identity_summary=(
            "For eta^5 = 2:  sqrt(4 eta - 3)  =  (1 eta^7 + 1 eta^? - 1 eta^6 - 1) / sqrt(5)"
            "  [some exponents likely misread from facsimile]"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="low",
        notes=(
            "Denesting. Exact RHS hard to read on facsimile; possible "
            "transcription errors. NOT K3."
        ),
    ),
    Identity(
        page_id=344,
        identity_index=7,
        identity_summary=(
            "For eta^5 = 3:  3sqrt(2 - eta^2)  =  (1 + eta - eta^2) / 3sqrt(5),  "
            "where  eta = 3."
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="medium",
        notes=(
            "Denesting cube root. eta = 3 in the side condition is "
            "suspicious -- if eta = 3 then eta^5 = 243, not 3. The annotation "
            "may be a separate side note. Denesting. NOT K3."
        ),
    ),
    Identity(
        page_id=344,
        identity_index=8,
        identity_summary=(
            "For eta^5 = 2:  5sqrt(1 + eta + eta^3)  =  sqrt(1 + eta^2) / 10sqrt(5),  "
            "where  eta^5 + 5 eta^2 + 5 eta + 2 = 0"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="medium",
        notes=(
            "Denesting with a side polynomial condition eta^5 + 5 eta^2 + 5 eta + 2 = 0. "
            "Note this is NOT compatible with eta^5 = 2 (the side conditions "
            "are inconsistent -- if eta^5 = 2 then eta^5+5eta^2+5eta+2 = 4+5eta^2+5eta "
            "which is generally nonzero). May be two distinct identities run "
            "together on the facsimile. NOT K3."
        ),
    ),
    Identity(
        page_id=344,
        identity_index=9,
        identity_summary=(
            "3sqrt(1/3) + 3sqrt(5/3)  =  sqrt[(3sqrt(5) - 1)/(2 - 3sqrt(5))]  "
            "=  3sqrt[(3 + 3sqrt(5))/(3sqrt(5) - 1)]  "
            "=  5sqrt[(3*3sqrt(2) + 3sqrt(15))/(2 - 3sqrt(5))]"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="high",
        notes=(
            "Classic Ramanujan denesting of cube roots: 3sqrt(1/3) + "
            "3sqrt(5/3) is shown to equal three other progressively-"
            "more-nested radicals -- the most famous form of Ramanujan's "
            "denesting machinery. Citation: Berndt vol IV ch. 16, "
            "Andrews-Berndt vol IV nested-radical pages. NOT K3."
        ),
    ),
    Identity(
        page_id=344,
        identity_index=10,
        identity_summary=(
            "{3sqrt((a+b)(c^2 + b^2)) - a} {3sqrt((a+b)(a^2 + b^2)) - b}  "
            "=  (3sqrt((a+b)^2) - 3sqrt(a^2 + b^2)) / (3sqrt((a+b)^2) + 3sqrt(a^2 + b^2)) "
            "* (a^2 + a b + b^2)"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="medium",
        notes=(
            "Multi-variable denesting / cube-root identity in (a,b). "
            "Three explicit radicals on LHS times each other equal a "
            "ratio of cube roots on RHS. NOT K3."
        ),
    ),
    Identity(
        page_id=344,
        identity_index=11,
        identity_summary=(
            "(sqrt(a^2 + ab + b^2) - a) * (sqrt(a^2 + ab + b^2) - b) "
            "/ (a + b - sqrt(a^2 + ab + b^2))  =  a + b"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="medium",
        notes=(
            "Square-root identity in (a,b). NOT K3."
        ),
    ),
    Identity(
        page_id=344,
        identity_index=12,
        identity_summary=(
            "{a + sqrt((b+c)(c+a))} * {b + sqrt((c+a)(a+b))} * {-b + sqrt((a+b)(b+c))}  "
            "=  2(ab + ac + b^2) * (sqrt(a+b) + sqrt(b+c) + sqrt(c+a))^2 / (2(b + c + a))"
        ),
        source_in_ono="NOT discussed",
        k3_status="NOT_K3",
        confidence="low",
        notes=(
            "Three-variable nested-radical identity in (a,b,c). "
            "Symmetric-function structure on the RHS. NOT K3."
        ),
    ),
]


def compute_verdict(inv: List[Identity]) -> dict:
    """
    Compute the HUNT_MAP §1 verdict.
    The K3 prediction was for pp. 341-343 specifically; we also report
    on the inclusive 340-344 set since pp. 342-344 of the facsimile turn
    out to not be cube continuation.
    """
    # Bucket per the K3 status
    status_buckets: dict = {}
    for ident in inv:
        status_buckets.setdefault(ident.k3_status, []).append(ident)

    def pct(n, d):
        return f"{100.0 * n / d:.1f}%" if d > 0 else "N/A"

    verdict = {}
    # Per page
    for page in sorted({i.page_id for i in inv}):
        page_inv = [i for i in inv if i.page_id == page]
        n_total = len(page_inv)
        n_unknown = sum(1 for i in page_inv if i.k3_status == "UNKNOWN_FROM_FACSIMILE")
        n_known = n_total - n_unknown
        n_k3 = sum(
            1 for i in page_inv
            if i.k3_status in ("K3_PARAMETERISATION_CONFIRMED", "K3_CANDIDATE_PER_ONO")
        )
        verdict[f"p{page}"] = {
            "n_total": n_total,
            "n_unknown": n_unknown,
            "n_known": n_known,
            "n_k3": n_k3,
            "k3_fraction_of_known": pct(n_k3, n_known),
        }

    # HUNT_MAP §1 specific: pp. 341-343 (the targeted bundle)
    hunt_inv = [i for i in inv if i.page_id in {341, 342, 343}]
    n_total = len(hunt_inv)
    n_unknown = sum(1 for i in hunt_inv if i.k3_status == "UNKNOWN_FROM_FACSIMILE")
    n_known = n_total - n_unknown
    n_k3 = sum(
        1 for i in hunt_inv
        if i.k3_status in ("K3_PARAMETERISATION_CONFIRMED", "K3_CANDIDATE_PER_ONO")
    )
    verdict["HUNT_MAP_§1_target_pp341_342_343"] = {
        "n_total": n_total,
        "n_unknown": n_unknown,
        "n_known": n_known,
        "n_k3": n_k3,
        "k3_fraction_of_known": pct(n_k3, n_known),
        "prediction_60_to_80_percent": "FALSIFIED",
        "interpretation": (
            "pp. 342 and 343 of the Lost Notebook are NOT continuation of "
            "the 1729 cube identities. They are a class-invariants table "
            "(Weber's f_1 at sqrt(-n) values, n = 20..87, Hunt 4 territory) "
            "and a Diophantine-approximation table (best approx to 2^{1/5} "
            "and 2^{1/7}). Only p. 341 itself is the K3 / cube material."
        ),
    }

    # Including p. 344 (which is what user's file page-343.jpg actually is)
    hunt_inv_b = [i for i in inv if i.page_id in {341, 342, 343, 344}]
    n_total = len(hunt_inv_b)
    n_unknown = sum(1 for i in hunt_inv_b if i.k3_status == "UNKNOWN_FROM_FACSIMILE")
    n_known = n_total - n_unknown
    n_k3 = sum(
        1 for i in hunt_inv_b
        if i.k3_status in ("K3_PARAMETERISATION_CONFIRMED", "K3_CANDIDATE_PER_ONO")
    )
    verdict["user_intended_pp341_344_inclusive"] = {
        "n_total": n_total,
        "n_unknown": n_unknown,
        "n_known": n_known,
        "n_k3": n_k3,
        "k3_fraction_of_known": pct(n_k3, n_known),
        "prediction_60_to_80_percent": "FALSIFIED",
    }
    return verdict


def main():
    out_path = Path(__file__).parent / "results" / "hunt1_k3_inventory.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "page_id",
                "identity_index",
                "identity_summary",
                "source_in_ono",
                "k3_status",
                "confidence",
                "notes",
            ]
        )
        for ident in INVENTORY:
            w.writerow(
                [
                    ident.page_id,
                    ident.identity_index,
                    ident.identity_summary,
                    ident.source_in_ono,
                    ident.k3_status,
                    ident.confidence,
                    ident.notes,
                ]
            )

    print(f"Wrote {len(INVENTORY)} identities to {out_path}")

    verdict = compute_verdict(INVENTORY)
    print()
    print("=" * 78)
    print("HUNT 1 VERDICT  (Lost Notebook pp. 341-343 K3 parameterisation)")
    print("=" * 78)
    for key, val in verdict.items():
        print(f"\n  {key}:")
        for k, v in val.items():
            print(f"    {k}: {v}")
    print()
    print("=" * 78)


if __name__ == "__main__":
    main()
