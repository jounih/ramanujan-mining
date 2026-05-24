"""rkc.completions — numerical completion for MODULAR_COMPLETION_REQUIRED route.

When the recognizer matches a mock-theta family input AND the user opts in
to numerical completion, this module is the route handler: it calls the
Watson-Hickerson Eichler-integral machinery from `analysis/17_mock_theta_residual_ebm_v1.py`
and returns a (value, error_bound, certificate_metadata) tuple.

Architecturally this is a THIN WRAPPER around exp 17's existing code — not a
reimplementation. The exp 17 script is imported at runtime via importlib
(the script lives in `ramanujan/analysis/` and starts with a digit, so the
ordinary `import` statement won't reach it without renaming).

Mock-theta family coverage (this run):

  - mock_theta_f3 : END-TO-END. The bias-corrected value f(q) is computed
                    via Watson's identity:
                        f(q) = q^{1/24} · [2 √(2π/α) · q_1^{4/3} · W(q_1²) + M(α)]
                    with q = exp(-α), q_1 = exp(-π²/α), and M(α) the
                    Mordell/Eichler integral. Returns (value, |residual|,
                    certificate) where |residual| is the numerically-measured
                    Watson identity residual (≥30-digit cross-check at α ≤ 0.7).
  - mock_theta_f5 : NOT INSTRUMENTED (only f3 has Watson-Hickerson data in
                    this run). Raises `CompletionNotImplemented`.
  - mock_theta_f7 : NOT INSTRUMENTED. Raises `CompletionNotImplemented`.

Honest gap: extending to f5 and f7 requires the 5th- and 7th-order Watson
identities (Hickerson 1988; Berndt-Chan), which have different modular
partners and Mordell integrand structure. The fuzzy MOCK_THETA_LIKE family
catches them as warnings; only f3 has a numerical completion shipped.
"""
from __future__ import annotations

import importlib.util
import pathlib
from dataclasses import dataclass, field
from typing import Any, Optional

from mpmath import mp, mpf, exp, log, pi, sqrt


# ----------------------------------------------------------------------------
# Exception types
# ----------------------------------------------------------------------------

class CompletionNotImplemented(Exception):
    """Raised when the recognizer matches a mock-theta family for which no
    Watson-Hickerson Eichler-integral instrumentation has been wired in
    this run. Carries the family name so the caller can decide whether to
    fall back to the flag-only behavior."""

    def __init__(self, family: str, msg: Optional[str] = None):
        self.family = family
        if msg is None:
            msg = (f"mock-theta family {family!r} has no numerical "
                   f"completion instrumented in this run; only mock_theta_f3 "
                   f"has Watson-Hickerson Eichler-integral data wired in. "
                   f"See diary 16 for the gap.")
        super().__init__(msg)


# ----------------------------------------------------------------------------
# Lazy import of exp 17 (the Watson-Hickerson Eichler-integral implementation)
# ----------------------------------------------------------------------------

_EXP17_MODULE: Optional[Any] = None
_EXP17_PATH = (pathlib.Path(__file__).resolve().parents[1]
               / "analysis" / "17_mock_theta_residual_ebm_v1.py")


def _load_exp17():
    """Import analysis/17_mock_theta_residual_ebm_v1.py via importlib.

    The script lives in ramanujan/analysis/ and its filename starts with a
    digit, so `import` from the package won't reach it. Use
    importlib.util.spec_from_file_location to load it on demand.
    """
    global _EXP17_MODULE
    if _EXP17_MODULE is not None:
        return _EXP17_MODULE
    if not _EXP17_PATH.exists():
        raise FileNotFoundError(
            f"Exp 17 source not found at {_EXP17_PATH}. The mock-theta "
            f"completion pipeline depends on its Watson-Hickerson code."
        )
    spec = importlib.util.spec_from_file_location(
        "ramanujan_exp17", _EXP17_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _EXP17_MODULE = module
    return module


# ----------------------------------------------------------------------------
# Result types
# ----------------------------------------------------------------------------

@dataclass
class CompletionCertificate:
    """Metadata accompanying a numerical mock-theta completion result.

    Carries the provenance, the regime tag (calibrated vs near-cusp warning),
    the modular cross-check residual, and an honest confidence tag.
    """
    family: str                            # e.g. "mock_theta_f3"
    method: str                            # e.g. "Watson-Hickerson Eichler integral"
    source: str                            # provenance pointer (script path)
    alpha: float                           # alpha = -log(q) used
    beta_dual: float                       # π²/α (the modular dual variable)
    working_dps: int                       # mpmath precision used
    modular_residual: float                # |Watson identity residual|
    shadow_eichler_integral: float         # M(α)
    modular_term: float                    # 2√(2π/α) q_1^{4/3} W(q_1²)
    regime: str                            # "calibrated" if α ≤ 0.7 else "near-cusp-warning"
    confidence: str                        # "high" / "medium" / "low"
    notes: str = ""                        # free-form caveats
    extras: dict = field(default_factory=dict)


@dataclass
class CompletionResult:
    """The triple `(value, error_bound, certificate)` returned by
    `compute_mock_theta_with_completion`.

    Also iterable as a tuple for callers that prefer positional unpacking.
    """
    value: Any                              # mpf — the bias-corrected value
    error_bound: float                      # numerical upper bound on the error
    certificate: CompletionCertificate

    def __iter__(self):
        yield self.value
        yield self.error_bound
        yield self.certificate


# ----------------------------------------------------------------------------
# Main entry point
# ----------------------------------------------------------------------------

# Families for which we ship a numerical completion in this run.
_SUPPORTED_FAMILIES = {"mock_theta_f3"}


def compute_mock_theta_with_completion(
    family: str,
    q: Any,
    target_digits: int = 30,
) -> CompletionResult:
    """Compute a mock-theta value with rigorous Watson-Hickerson bias correction.

    Parameters
    ----------
    family : str
        Registry name of the matched kernel — must be one of
        {'mock_theta_f3'} for this run. Other registered mock-theta
        families (mock_theta_f5, mock_theta_f7) raise
        `CompletionNotImplemented`.
    q : numeric
        The value of q ∈ (0, 1) at which to evaluate. Accepted as
        mpf-coercible (mpf, float, Rational, str).
    target_digits : int
        Working precision in decimal digits. The function bumps `mp.dps`
        to `max(target_digits + 10, 50)` to leave headroom. The Watson
        cross-check itself is the error-bound.

    Returns
    -------
    CompletionResult(value, error_bound, certificate)
        * value: f(q) reconstructed from Watson's identity:
              f(q) = q^{1/24} · [modular_term + M(α)]
          where modular_term = 2 √(2π/α) · q_1^{4/3} · W(q_1²),
                M(α) = 4 √(3α/(2π)) · ∫₀^∞ sinh(αt)/sinh(3αt/2) e^{-3αt²/2} dt,
                q = e^{-α}, q_1 = e^{-π²/α}.
        * error_bound: |F(α) - (modular_term + M(α))| measured directly,
          which equals 0 analytically (Watson's identity) and bounds the
          numerical error at the chosen precision.
        * certificate: provenance + regime + confidence metadata.

    Raises
    ------
    CompletionNotImplemented
        If `family` is registered with the recognizer but no numerical
        completion is wired in this run (mock_theta_f5, mock_theta_f7).
    ValueError
        If q is not in (0, 1).
    """
    if family not in _SUPPORTED_FAMILIES:
        raise CompletionNotImplemented(family)

    # Bump precision with headroom; restore on the way out.
    saved_dps = mp.dps
    try:
        mp.dps = max(int(target_digits) + 10, 50)

        q_mpf = mpf(q)
        if q_mpf <= 0 or q_mpf >= 1:
            raise ValueError(
                f"mock-theta completion requires q in (0, 1); got q={q_mpf}"
            )

        exp17 = _load_exp17()

        alpha = -log(q_mpf)
        beta_dual = pi * pi / alpha
        q1 = exp(-beta_dual)

        # Watson-Hickerson modular term (the "modular dual") and the
        # Mordell/Eichler integral piece (the "bias correction").
        W_val = exp17.W_watson(q1 ** 2)
        modular_term = 2 * sqrt(2 * pi / alpha) * q1 ** (mpf(4) / 3) * W_val
        shadow_eichler = exp17.watson_mordell_integral(alpha)

        # Reconstructed f(q) via Watson's identity:
        #   F(α) = q^{-1/24} f(q) = modular_term + M(α)
        #   ⇒  f(q) = q^{1/24} · (modular_term + M(α))
        f_q_reconstructed = q_mpf ** (mpf(1) / 24) * (modular_term + shadow_eichler)

        # Direct-series cross-check (for the error bound). This gives a
        # numerical upper bound on the reconstruction error WITHOUT assuming
        # the identity holds — both sides are computed independently and the
        # difference is the residual.
        f_q_direct = exp17.f_mock_theta(q_mpf)
        residual = abs(f_q_reconstructed - f_q_direct)

        # The Watson identity is calibrated to ≥30 digits for α ≤ 0.7
        # (diary 12 §6a). At α > 0.7 the W partner picks up uncomputed
        # next-order corrections in q_1; the residual scales as q_1^4.
        if alpha <= mpf("0.7"):
            regime = "calibrated"
            confidence = "high"
            notes = (f"α = {float(alpha):.4f} ≤ 0.7; Watson identity "
                     f"calibrated to ≥30 digits in this regime.")
        else:
            regime = "near-cusp-warning"
            confidence = "low" if alpha > 1 else "medium"
            notes = (f"α = {float(alpha):.4f} > 0.7; Watson identity has "
                     f"uncomputed next-order q_1^4 corrections; residual "
                     f"reflects that gap, not a precision-floor limit. "
                     f"Use direct f_mock_theta for this regime instead.")

        cert = CompletionCertificate(
            family=family,
            method="Watson-Hickerson Eichler integral (exp 17)",
            source=str(_EXP17_PATH),
            alpha=float(alpha),
            beta_dual=float(beta_dual),
            working_dps=int(mp.dps),
            modular_residual=float(residual),
            shadow_eichler_integral=float(shadow_eichler),
            modular_term=float(modular_term),
            regime=regime,
            confidence=confidence,
            notes=notes,
            extras={
                "q1": float(q1),
                "W_watson_value": float(W_val),
                "target_digits": int(target_digits),
                "f_q_direct_series_cross_check": float(f_q_direct),
            },
        )
        return CompletionResult(
            value=f_q_reconstructed,
            error_bound=float(residual),
            certificate=cert,
        )
    finally:
        mp.dps = saved_dps


# ----------------------------------------------------------------------------
# Convenience: family-coverage reporter (used by the e2e demo and the diary)
# ----------------------------------------------------------------------------

def supported_families() -> set[str]:
    """Return the set of mock-theta families that have a numerical completion
    wired in this run."""
    return set(_SUPPORTED_FAMILIES)


def all_registered_mock_theta_families() -> list[str]:
    """List every registry entry whose family is MOCK_THETA_LIKE.

    Crosschecks against rkc.registry.REGISTRY rather than hard-coding the
    list, so adding a new mock-theta entry to the registry automatically
    surfaces here as an unimplemented gap.
    """
    from .registry import REGISTRY
    from .routing import KernelFamily
    return [e.name for e in REGISTRY if e.family == KernelFamily.MOCK_THETA_LIKE]


def coverage_report() -> dict:
    """Return a dict mapping each registered mock-theta family to its
    completion-availability status."""
    supported = supported_families()
    return {
        name: ("end-to-end" if name in supported else "flag-only (CompletionNotImplemented)")
        for name in all_registered_mock_theta_families()
    }
