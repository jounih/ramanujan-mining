"""Operator-tagging schema for Hunt 5 (Quarterly Reports).

Implements the six abstract operators that HUNT_MAP §5 predicts will recur
80%+ of the time across Ramanujan's Quarterly Reports manipulations:

    1. Mellin inversion          (continuous Fourier on the multiplicative group)
    2. Master-theorem operator   (coefficient extraction from generating function)
    3. q-shift operator          (the q-analog of differentiation)
    4. Modular S-transform       (tau -> -1/tau)
    5. Eisenstein-style normal-ordering ("pull a residue")
    6. Class-field Galois average ("sum over Heegner orbit")

Each operator is a dataclass carrying:
    - name                : machine-readable string label
    - symbolic_signature  : AST/regex pattern (what notation denotes its use)
    - example             : a verbatim training-memory example. MUST be
                            re-verified against the actual Berndt
                            transcription when that lands — flagged
                            `verified_against_transcription = False` until then.
    - test(snippet) -> float in [0, 1]
                          : confidence the snippet uses this operator.

The schema is importable AND self-testing when run as `python3 <thisfile>`.

Provenance:
    The six operators are quoted verbatim from `insights/HUNT_MAP.md` §5
    (Hunt 5 — Quarterly Reports). The example manipulations below are
    training-memory recall of the standard textbook form of each
    operator; they are NOT yet verified against the Berndt 1984
    transcription (which has not landed in the env). Verification gate:
    flip `verified_against_transcription` to True once the corresponding
    Berndt §+page is identified.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from dataclasses import dataclass, field
from typing import Callable, List


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _normalize(snippet: str) -> str:
    """Light NFKC + whitespace + LaTeX-spacing normalization so heuristics
    can write a single canonical pattern instead of N variants.
    """
    s = unicodedata.normalize("NFKC", snippet)
    # collapse runs of whitespace (incl. newlines) so multi-line LaTeX
    # display math is matchable as one token stream
    s = re.sub(r"\s+", " ", s)
    # strip LaTeX cosmetic spacers
    s = s.replace(r"\,", " ").replace(r"\!", " ").replace(r"\;", " ")
    return s


def _any(snippet: str, patterns: List[str]) -> bool:
    return any(re.search(p, snippet) for p in patterns)


def _count(snippet: str, patterns: List[str]) -> int:
    return sum(1 for p in patterns if re.search(p, snippet))


# ---------------------------------------------------------------------------
# Operator dataclass
# ---------------------------------------------------------------------------

@dataclass
class Operator:
    """One of the six abstract operators in HUNT_MAP §5."""

    name: str
    description: str
    symbolic_signature: str
    example: str
    test: Callable[[str], float]
    verified_against_transcription: bool = False
    notes: str = ""

    # Per-operator threshold above which the snippet should be flagged
    # as "uses this operator". 0.5 is the default; an operator with a
    # crisper signature can set lower (more permissive) and one with a
    # noisier signature can set higher.
    flag_threshold: float = 0.5

    def __repr__(self) -> str:
        flag = "VERIFIED" if self.verified_against_transcription else "MEMORY-ONLY"
        return f"<Operator name={self.name!r} status={flag}>"

    def assess(self, snippet: str) -> float:
        """Return confidence ∈ [0, 1] that `snippet` invokes this operator."""
        c = self.test(snippet)
        # clamp defensively (matcher heuristics could over-shoot)
        if c < 0.0:
            return 0.0
        if c > 1.0:
            return 1.0
        return float(c)


# ---------------------------------------------------------------------------
# Operator 1 — Mellin inversion
# ---------------------------------------------------------------------------

def _test_mellin(snippet: str) -> float:
    s = _normalize(snippet)
    # Look for: an integral against x^{s-1} dx (forward Mellin), or
    # a Bromwich/Hankel-style contour integral 1/(2 pi i) ∫ x^{-s} F(s) ds
    # (inverse Mellin).
    forward_patterns = [
        r"\\int.*x\s*\^\s*\{?s\s*-\s*1\}?",        # \int ... x^{s-1} ...
        r"x\s*\^\s*\{?s\s*-\s*1\}?\s*[A-Za-z]\(x\)",   # x^{s-1} f(x)
        r"\\int_0\^\\infty",                       # ∫_0^∞ ... dx (Mellin range)
    ]
    inverse_patterns = [
        r"\\frac\{1\}\{2\s*\\pi\s*i\}\s*\\int",    # 1/(2 pi i) ∫
        r"\\int_\{?c\s*-\s*i\s*\\infty\}?\^\{?c\s*\+\s*i\s*\\infty\}?",  # Bromwich
        r"x\s*\^\s*\{?-\s*s\}?\s*[A-Za-z]\(s\)",   # x^{-s} F(s)
    ]
    gamma_pattern = [r"\\Gamma\s*\(\s*s\s*\)"]
    score = 0.0
    if _any(s, forward_patterns):
        score += 0.5
    if _any(s, inverse_patterns):
        score += 0.6
    if _any(s, gamma_pattern):
        score += 0.2  # Mellin transforms almost always invoke Gamma(s)
    return min(score, 1.0)


_OP_MELLIN = Operator(
    name="mellin_inversion",
    description="Continuous Fourier on the multiplicative group; "
                "Mellin transform M[f](s) = ∫_0^∞ x^{s-1} f(x) dx and its "
                "inverse via the Bromwich contour.",
    symbolic_signature=r"\int_0^\infty x^{s-1} f(x) dx   or   "
                       r"(1/2pi i) \int_{c-i\infty}^{c+i\infty} x^{-s} F(s) ds",
    example=r"""
Mellin transform of $e^{-x}$:
\[
  \int_0^\infty x^{s-1} e^{-x}\, dx = \Gamma(s).
\]
Inverse:
\[
  e^{-x} = \frac{1}{2\pi i}\int_{c - i\infty}^{c + i\infty} x^{-s}\,\Gamma(s)\, ds.
\]
""",
    test=_test_mellin,
    verified_against_transcription=False,
    notes="HUNT_MAP §5: continuous Fourier on the multiplicative group. "
          "Strong textbook signature; expect to dominate Quarterly Report II "
          "(per Berndt 1984 §4).",
)


# ---------------------------------------------------------------------------
# Operator 2 — Master-theorem operator
# ---------------------------------------------------------------------------

def _test_master_theorem(snippet: str) -> float:
    s = _normalize(snippet)
    # Distinguishing pattern: F(x) = sum phi(n) (-x)^n / n!, paired with
    # int_0^infty x^{s-1} F(x) dx = Gamma(s) phi(-s).
    has_alt_sum = bool(re.search(
        r"\\sum.*\(\s*-\s*x\s*\)\s*\^\s*\{?n\}?", s
    )) or bool(re.search(
        r"\\sum.*\(\s*-\s*1\s*\)\s*\^\s*\{?n\}?.*x\s*\^\s*\{?n\}?", s
    ))
    has_factorial = bool(re.search(r"n\s*!", s)) or bool(re.search(r"\\Gamma", s))
    has_phi_neg_s = bool(re.search(
        r"\\phi\s*\(\s*-\s*s\s*\)|f\s*\(\s*-\s*s\s*\)", s
    ))
    has_master_keyword = bool(re.search(r"[Mm]aster\s+[Tt]heorem", s))
    score = 0.0
    if has_master_keyword:
        score += 0.7
    if has_alt_sum:
        score += 0.4
    if has_factorial:
        score += 0.2
    if has_phi_neg_s:
        score += 0.5
    return min(score, 1.0)


_OP_MASTER = Operator(
    name="master_theorem",
    description="Ramanujan's Master Theorem: extracts the analytic "
                "continuation of the coefficient generating function "
                "phi(n) via a Mellin integral against an alternating "
                "series with factorial normalization.",
    symbolic_signature=r"F(x)=\sum_{n\ge 0} \phi(n) (-x)^n / n!    \Rightarrow    "
                       r"\int_0^\infty x^{s-1} F(x) dx = \Gamma(s) \phi(-s)",
    example=r"""
\textbf{Master Theorem.}  If $F(x) = \sum_{n \ge 0} \phi(n)\,(-x)^n / n!$
then
\[
  \int_0^\infty x^{s-1} F(x)\, dx = \Gamma(s)\,\phi(-s).
\]
""",
    test=_test_master_theorem,
    verified_against_transcription=False,
    notes="HUNT_MAP §5: coefficient extraction from generating function. "
          "Expected to be the SIGNATURE move of QR I (per Berndt 1984 §3).",
)


# ---------------------------------------------------------------------------
# Operator 3 — q-shift operator
# ---------------------------------------------------------------------------

def _test_q_shift(snippet: str) -> float:
    s = _normalize(snippet)
    # q-Pochhammer notation (a;q)_n or (a;q)_\infty, q-derivative D_q f
    # = (f(qx) - f(x)) / ((q-1) x), Heine's transformations, etc.
    patterns = [
        r"\(\s*[A-Za-z]\s*;\s*q\s*\)\s*_\s*\{?(?:n|\\infty|\d+)\}?",  # (a;q)_n
        r"D_q\b",
        r"f\s*\(\s*q\s*x\s*\)\s*-\s*f\s*\(\s*x\s*\)",       # q-derivative numerator
        r"\\theta\s*_q\b",                                  # q-analogue
        r"\bq\s*-\s*[Ss]hift",
        r"\bq\s*-\s*[Dd]erivative",
        r"\bq\s*-\s*[Pp]ochhammer",
    ]
    score = 0.0
    for p in patterns:
        if re.search(p, s):
            score += 0.35
    # boost if multiple distinct patterns hit
    return min(score, 1.0)


_OP_Q_SHIFT = Operator(
    name="q_shift",
    description="q-analog of differentiation: D_q f(x) = (f(qx) - f(x))/((q-1)x); "
                "manifests in q-Pochhammer manipulations (a; q)_n, q-binomial "
                "theorem, Heine transformations.",
    symbolic_signature=r"(a; q)_n,  (a; q)_\infty,  D_q f(x) = (f(qx)-f(x))/((q-1)x)",
    example=r"""
The q-binomial theorem uses a q-shift:
\[
  \sum_{n \ge 0} \frac{(a; q)_n}{(q; q)_n} z^n \;=\; \frac{(a z; q)_\infty}{(z; q)_\infty}.
\]
Equivalently, $D_q [(z; q)_\infty] = -(z; q)_\infty / (1-z)$.
""",
    test=_test_q_shift,
    verified_against_transcription=False,
    notes="HUNT_MAP §5: q-analog of differentiation. Less prominent in QRs "
          "than in NB II ch. 16; still expected to appear in QR III where "
          "Ramanujan demonstrates the q-MA partner of the Master Theorem.",
)


# ---------------------------------------------------------------------------
# Operator 4 — Modular S-transform
# ---------------------------------------------------------------------------

def _test_modular_S(snippet: str) -> float:
    s = _normalize(snippet)
    patterns_arg = [
        r"-\s*1\s*/\s*\\?tau",                  # -1/tau
        r"-\s*1\s*/\s*\\tau",                   # \tau form
        r"\\tau\s*\\to\s*-\s*1\s*/\s*\\tau",    # explicit S-transform
        r"\\eta\s*\(\s*-\s*1\s*/\s*\\tau\s*\)", # eta(-1/tau)
        r"\\theta\s*_?\d?\s*\(\s*-\s*1\s*/\s*\\tau\s*\)",  # theta(-1/tau)
        r"\\theta\s*\(\s*-\s*1\s*/\s*\\beta\s*\)",         # theta(-1/beta) plain
        r"[Mm]odular\s+S",                                 # narrative
        r"\\sqrt\{?\s*-\s*i\s*\\?tau\s*\}?",               # the prefactor sqrt(-i tau)
        r"[Pp]oisson\s+summation",                         # Poisson summation
        r"[Jj]acobi\s+(?:theta\s+)?(?:transformation|inversion)",
    ]
    score = 0.0
    for p in patterns_arg:
        if re.search(p, s):
            score += 0.35
    return min(score, 1.0)


_OP_MODULAR_S = Operator(
    name="modular_S_transform",
    description="The modular S-transform tau -> -1/tau (equivalently the "
                "Jacobi-theta / Dedekind-eta transformation, equivalently "
                "Poisson summation on a 1D Gaussian lattice).",
    symbolic_signature=r"\eta(-1/\tau) = \sqrt{-i\tau}\,\eta(\tau)   or   "
                       r"\theta(-1/\tau) = \sqrt{-i\tau}\,\theta(\tau)",
    example=r"""
The Jacobi theta inversion (a modular $S$-transform applied to $\theta_3$):
\[
  \theta_3(\tau) \;=\; \frac{1}{\sqrt{-i\tau}}\;\theta_3(-1/\tau).
\]
Equivalently for the Gaussian sum:
$\sum_{n} e^{-\beta n^2} = \sqrt{\pi/\beta}\,\sum_n e^{-\pi^2 n^2/\beta}$.
""",
    test=_test_modular_S,
    verified_against_transcription=False,
    notes="HUNT_MAP §5: tau -> -1/tau. Already in the RKC recognizer "
          "(analysis/13_recognizer_v1.py); expect QR III to show this as "
          "a primitive operation, not a derived calculation.",
)


# ---------------------------------------------------------------------------
# Operator 5 — Eisenstein-style normal-ordering ("pull a residue")
# ---------------------------------------------------------------------------

def _test_eisenstein_normal_order(snippet: str) -> float:
    s = _normalize(snippet)
    patterns = [
        r"\\operatorname\{[Rr]es\}|\bRes\b|\\mathop\{Res\}",  # residue operator
        r"E_\s*\{?\d+\}?",                                    # E_2, E_4, E_6, E_{2k}
        r"\\sigma\s*_?\s*\{?k\}?\s*\(\s*n\s*\)",              # sigma_k(n)
        r"\\sum.*\bn\b.*q\s*\^\s*\{?n\}?\s*/\s*\(\s*1\s*-\s*q\s*\^\s*\{?n\}?\s*\)",  # Lambert
        r"normal[\s-]?order",
        r"[Pp]ull\s+a?\s+residue",
        r"[Ee]isenstein\s+(?:series|normalization|completion)",
        r"E_2\^\*|\\widehat\s*\{?E_2\}?",                     # quasi-modular E_2*
        r"-\s*\\frac\{6\}\{\\pi\s*\\?,?\s*\\mathrm\{Im\}\s*\\tau\}",  # E_2 completion
    ]
    score = 0.0
    for p in patterns:
        if re.search(p, s):
            score += 0.3
    return min(score, 1.0)


_OP_EISENSTEIN_NORMAL = Operator(
    name="eisenstein_normal_ordering",
    description="Pulling a residue / normal-ordering an Eisenstein-style "
                "Lambert series, e.g. completing E_2 to a non-holomorphic "
                "modular form by subtracting 3/(pi Im tau), or extracting "
                "the constant Eisenstein contribution before summing a "
                "divisor-sum generating function.",
    symbolic_signature=r"E_{2k}(\tau) = 1 - \frac{4k}{B_{2k}} \sum_{n\ge 1} \sigma_{2k-1}(n) q^n   "
                       r"(constant-term extraction);  "
                       r"\widehat E_2 = E_2 - 3/(\pi \mathrm{Im}\tau)   (anomaly cancellation)",
    example=r"""
Normal-ordering the Eisenstein series $E_4$ separates the constant term
from the Lambert-style $q$-series:
\[
  E_4(\tau) \;=\; 1 + 240\,\sum_{n \ge 1} \sigma_3(n)\, q^n
            \;=\; 1 + 240\,\sum_{n \ge 1} \frac{n^3 q^n}{1 - q^n}.
\]
The constant term 1 is the residue $\mathrm{Res}_{q = 0}$ pulled out before
recognising the Lambert series.
""",
    test=_test_eisenstein_normal_order,
    verified_against_transcription=False,
    notes="HUNT_MAP §5: the 'pull a residue' move. Most distinctive in QR II "
          "(Berndt's 'calculus of zeta values', §4). Heuristic is broader "
          "than the strict residue operator — also picks up E_{2k} normal "
          "forms because that is operationally the same move.",
)


# ---------------------------------------------------------------------------
# Operator 6 — Class-field Galois average ("sum over Heegner orbit")
# ---------------------------------------------------------------------------

def _test_galois_average(snippet: str) -> float:
    s = _normalize(snippet)
    patterns = [
        r"\\sum_\{?\\?tau\b",                       # \sum_tau ...
        r"[Hh]eegner\b",
        r"[Cc]lass\s+(?:field|invariant|number)",
        r"j\s*\(\s*\\?tau\s*\)",                    # j(tau)
        r"G_\s*\{?n\}?|g_\s*\{?n\}?",               # Weber class invariants G_n, g_n
        r"\\mathrm\{Cl\}|\\operatorname\{Cl\}",     # Cl(K)
        r"\\sqrt\{?\s*-\s*[0-9]+\s*\}?",            # sqrt(-d) discriminant
        r"\\sum.*\\sigma\s*\\in\s*\\mathrm\{Gal\}",  # sum_{sigma in Gal}
        r"[Cc]lass\s+(?:polynomial|equation)",
        r"\\mathrm\{Tr\}_\{?K/\\Q\}?|\\mathrm\{Tr\}",  # trace from class field
    ]
    score = 0.0
    for p in patterns:
        if re.search(p, s):
            score += 0.3
    return min(score, 1.0)


_OP_GALOIS_AVERAGE = Operator(
    name="class_field_galois_average",
    description="Sum over a Heegner orbit / Galois orbit in a ring class "
                "field: averaging a modular function value over conjugate "
                "CM points to land in a rational (or radical) class "
                "invariant. The move underlying Ramanujan's 116 G_n / g_n "
                "tabulations.",
    symbolic_signature=r"\sum_{\tau \in \mathrm{Heegner}(D)} j(\tau)    "
                       r"or    \prod_{\sigma \in \mathrm{Gal}(H/K)} \sigma(G_n)",
    example=r"""
The class polynomial of discriminant $-D$ is built by averaging $j$ over a
Heegner orbit:
\[
  H_D(X) \;=\; \prod_{\tau \in \mathrm{Heegner}(D)} \bigl( X - j(\tau) \bigr).
\]
Ramanujan's class invariant $G_n$ is then a radical-tower expression for one
factor of $H_{-4n}$ at the Weber-modular level.
""",
    test=_test_galois_average,
    verified_against_transcription=False,
    notes="HUNT_MAP §5: 'sum over Heegner orbit'. Expected to appear "
          "wherever Ramanujan quotes a numerical value of G_n or 1/pi at a "
          "CM point. Most relevant to QR III if Berndt's commentary on "
          "Hardy's 'Twelve Lectures' ch. 11 holds.",
)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

OPERATORS: List[Operator] = [
    _OP_MELLIN,
    _OP_MASTER,
    _OP_Q_SHIFT,
    _OP_MODULAR_S,
    _OP_EISENSTEIN_NORMAL,
    _OP_GALOIS_AVERAGE,
]


def tag(snippet: str) -> dict:
    """Return {operator_name: confidence ∈ [0,1]} for every registered
    operator. Convenience entry point for downstream agents."""
    return {op.name: op.assess(snippet) for op in OPERATORS}


def flagged(snippet: str) -> List[str]:
    """Return the names of operators whose confidence on `snippet`
    exceeds their per-operator flag_threshold."""
    return [op.name for op in OPERATORS if op.assess(snippet) >= op.flag_threshold]


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def _self_test() -> int:
    """Each operator must score >= its own flag_threshold on its own example.
    Returns the number of failures (0 means all green).
    """
    failures = 0
    print("operator_tagging_schema self-test")
    print("=" * 64)
    for op in OPERATORS:
        score = op.assess(op.example)
        ok = score >= op.flag_threshold
        status = "OK " if ok else "FAIL"
        verified = "verified" if op.verified_against_transcription else "memory-only"
        print(f"  [{status}] {op.name:<32s}  score={score:0.2f}  "
              f"thresh={op.flag_threshold:0.2f}  ({verified})")
        if not ok:
            failures += 1

    # cross-check: each operator's example should not over-fire wildly on
    # OTHER operators (sanity guard for distinct fingerprints). We allow
    # cross-fire because some examples genuinely use two operators (e.g. the
    # Master Theorem example invokes Mellin inversion + Gamma function), but
    # we report it so a human can audit.
    print()
    print("cross-fire matrix (rows = example owner, cols = operator name):")
    header = "  " + " ".join(f"{op.name[:18]:>18s}" for op in OPERATORS)
    print(header)
    for owner in OPERATORS:
        row = [owner.assess.__name__]  # placeholder; replaced below
        scores = [other.assess(owner.example) for other in OPERATORS]
        cells = " ".join(f"{s:18.2f}" for s in scores)
        print(f"  {owner.name[:16]:<16s} {cells}")

    print()
    print(f"{'all green' if failures == 0 else f'{failures} FAILURE(S)'}")
    return failures


if __name__ == "__main__":
    sys.exit(_self_test())
