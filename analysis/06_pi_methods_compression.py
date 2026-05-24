"""
Experiment 06 — Bits-per-term and notation-bits-per-bit-of-pi for four
historically-significant methods of computing pi.

Goal: substantiate the user's "latent-space speedrun" framing in concrete
numbers. Claim: Ramanujan-class identities compress the same target
computation (N digits of pi) into a much shorter program-AND-execution
than naive methods. We measure both axes:

  bits_per_term      = bits of precision contributed by each summand
  notation_length    = length of the symbolic expression for one term
                        (a proxy for "what fits in working memory")

Methods compared:
  1. MACHIN     pi/4 = 4 atan(1/5) - atan(1/239), via Taylor series.
  2. AGM        Brent-Salamin (quadratic convergence).
  3. RAMANUJAN  Ramanujan's 1914 series, ~8 bits/term.
  4. CHUDNOVSKY Chudnovsky 1987, ~14 bits/term.

For each method, run k terms / iterations, compute pi, measure relative
error vs mpmath's high-precision pi, derive empirical bits/term, and emit
a notation-length number (lines of code, characters).
"""
from __future__ import annotations
import csv
import math
from pathlib import Path
from mpmath import mp, mpf, sqrt, factorial, pi as mp_pi, log, atan, fac


def bits_correct(approx, true_val) -> float:
    err = abs(approx - true_val) / abs(true_val)
    if err == 0:
        return float('inf')
    return float(-log(err) / log(2))


def machin_atan_series(x: mpf, K: int) -> mpf:
    """atan(x) = sum_{k>=0} (-1)^k x^(2k+1) / (2k+1), |x| < 1."""
    s = mpf(0)
    for k in range(K):
        s += (-1) ** k * x ** (2 * k + 1) / (2 * k + 1)
    return s


def pi_machin(K: int) -> mpf:
    return 4 * (4 * machin_atan_series(mpf(1) / 5, K) - machin_atan_series(mpf(1) / 239, K))


def pi_agm(iters: int) -> mpf:
    """Brent-Salamin AGM iteration. Quadratic convergence."""
    a = mpf(1)
    b = 1 / sqrt(mpf(2))
    t = mpf(1) / 4
    p = mpf(1)
    for _ in range(iters):
        an = (a + b) / 2
        bn = sqrt(a * b)
        t -= p * (a - an) ** 2
        a, b = an, bn
        p *= 2
    return (a + b) ** 2 / (4 * t)


def pi_ramanujan_1914(K: int) -> mpf:
    """Ramanujan's 1914 series:
        1/pi = (2 sqrt(2) / 9801) sum_{k>=0} (4k)! (1103 + 26390 k) / (k!^4 * 396^(4k)).
    Converges ~8 decimals per term.
    """
    s = mpf(0)
    for k in range(K):
        kf = factorial(k)
        s += factorial(4 * k) * (1103 + 26390 * k) / (kf ** 4 * mpf(396) ** (4 * k))
    return mpf(9801) / (2 * sqrt(mpf(2)) * s)


def pi_chudnovsky(K: int) -> mpf:
    """Chudnovsky brothers 1987:
        1/pi = 12 sum_{k>=0} (-1)^k (6k)! (13591409 + 545140134 k) / ((3k)! k!^3 (640320)^(3k+3/2)).
    Converges ~14 decimals per term.
    """
    s = mpf(0)
    C = mpf(640320)
    for k in range(K):
        kf = factorial(k)
        num = (-1) ** k * factorial(6 * k) * (13591409 + 545140134 * k)
        den = factorial(3 * k) * kf ** 3 * C ** (3 * k)
        s += num / den
    return C * sqrt(C) / (12 * s)


METHOD_NOTATION_CHARS = {
    "MACHIN":   len("pi/4 = 4 atan(1/5) - atan(1/239); atan(x) = sum (-1)^k x^(2k+1)/(2k+1)"),
    "AGM":      len("a=1; b=1/sqrt(2); t=1/4; p=1; loop: an=(a+b)/2; bn=sqrt(ab); t-=p(a-an)^2; a,b=an,bn; p*=2; pi=(a+b)^2/(4t)"),
    "RAMANUJAN_1914": len("1/pi = (2 sqrt 2 /9801) sum (4k)!(1103+26390k)/(k!^4 * 396^(4k))"),
    "CHUDNOVSKY":     len("1/pi = 12 sum (-1)^k (6k)!(13591409+545140134k)/((3k)!k!^3 * 640320^(3k+3/2))"),
}


def main():
    out_path = Path(__file__).parent / "results" / "pi_methods_compression.csv"
    out_path.parent.mkdir(exist_ok=True)
    mp.dps = 200
    true_pi = +mp_pi
    rows = []
    print(f"{'method':<14} {'K':>5} {'bits_correct':>14} {'bits/K':>10} {'notation_chars':>15}")
    print("-" * 65)
    for K in (1, 2, 4, 8, 16, 32):
        for name, fn in [("MACHIN", pi_machin),
                          ("RAMANUJAN_1914", pi_ramanujan_1914),
                          ("CHUDNOVSKY", pi_chudnovsky)]:
            try:
                p = fn(K)
                b = bits_correct(p, true_pi)
                rows.append(dict(method=name, K=K, bits_correct=b,
                                  bits_per_term=b / K,
                                  notation_chars=METHOD_NOTATION_CHARS[name]))
                print(f"{name:<14} {K:>5} {b:>14.2f} {b/K:>10.2f} {METHOD_NOTATION_CHARS[name]:>15}")
            except Exception as e:
                print(f"{name:<14} {K:>5} FAIL {e}")

    print()
    print(f"{'AGM iters':<14} {'k':>5} {'bits_correct':>14} {'bits/iter':>10} {'notation_chars':>15}")
    for k in (1, 2, 3, 4, 5, 6, 7, 8):
        p = pi_agm(k)
        b = bits_correct(p, true_pi)
        rows.append(dict(method="AGM", K=k, bits_correct=b,
                          bits_per_term=b / k,
                          notation_chars=METHOD_NOTATION_CHARS["AGM"]))
        print(f"{'AGM':<14} {k:>5} {b:>14.2f} {b/k:>10.2f} {METHOD_NOTATION_CHARS['AGM']:>15}")

    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {out_path}")

    # Compression metric: bits-of-pi per character of notation, for K large enough
    # that the asymptotic rate dominates
    print()
    print("Asymptotic compression: bits-of-pi per character-of-formula, at K = 32:")
    for name in ("MACHIN", "RAMANUJAN_1914", "CHUDNOVSKY"):
        rs = [r for r in rows if r["method"] == name and r["K"] == 32]
        if not rs:
            continue
        r = rs[0]
        per_char = r["bits_correct"] / r["notation_chars"]
        print(f"  {name:<16} {r['bits_correct']:>10.1f} bits / {r['notation_chars']:>3} chars = {per_char:6.2f} bits-per-char")
    rs_agm = [r for r in rows if r["method"] == "AGM" and r["K"] == 8]
    if rs_agm:
        r = rs_agm[0]
        per_char = r["bits_correct"] / r["notation_chars"]
        print(f"  {'AGM (k=8)':<16} {r['bits_correct']:>10.1f} bits / {r['notation_chars']:>3} chars = {per_char:6.2f} bits-per-char")
    print()
    print("Interpretation: the Ramanujan/Chudnovsky identities are not 'shorter to write'")
    print("than Machin, but they output many more bits per term executed. The 'compression'")
    print("lives in the kernel structure (modular function evaluation at a CM point), not")
    print("in the surface notation. That's the latent-space speedrun made quantitative.")


if __name__ == "__main__":
    main()
