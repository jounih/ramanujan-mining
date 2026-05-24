"""
Experiment 07 — divisor sum σ_k(n) = Σ_{d|n} d^k via three routes.

Pass A item 07. Tests the central RKC hypothesis on a *number-theoretic*
kernel (rather than the analytic theta / partition kernels of exp 02 / 04).
The "representation switch" here is between trial-division enumeration of
divisors and the Lambert-series ↔ Eisenstein generating-function lens, the
same kernel-switch pattern as theta-dual and Dedekind-eta-S.

Methods:
  (A) DIRECT:     enumerate divisors of n by trial division up to √n, sum
                  d^k over divisors. Per call cost O(√n) integer ops.
  (B) MOBIUS:     factor n = ∏ p_i^{a_i} and use the multiplicative formula
                  σ_k(n) = ∏ (p_i^{k(a_i+1)} − 1) / (p_i^k − 1)  (k > 0)
                  σ_0(n) = ∏ (a_i + 1)                          (k = 0)
                  Per call cost dominated by integer factoring of n; for
                  n up to 10^9 trial-divide-up-to-√n still works, so the
                  asymptotic cost class is the same as (A) but the constant
                  is *better* because once a prime p is factored out we
                  apply the closed form rather than rediscovering every
                  divisor.
  (C) LAMBERT:    expand Σ_{n≥1} n^k q^n / (1 − q^n) as a power series in
                  q to order N. For k > 0 this is (up to a constant and a
                  scaling) the Eisenstein series E_{k+1}(q) and the
                  coefficient of q^m is exactly σ_k(m). The natural
                  implementation is the divisor-sum sieve:
                      for n = 1..N:
                          nk = n**k
                          for m = n, 2n, 3n, ... ≤ N:
                              sigma[m] += nk
                  Total work: Σ_{n=1..N} ⌊N/n⌋ ≈ N H_N ≈ N (ln N + γ) ops.
                  Amortized per σ_k(m): O(log N).

Two scenario classes:
  SINGLE: one σ_k(n) at a time. We compare A vs B per-call.
  BATCH:  σ_k(1), σ_k(2), …, σ_k(N) all returned at once. We compare A
          summed over the batch vs C amortized.

Cost metric:
  We count *Python-level inner-loop iterations* as our "op." Each op
  corresponds to one big-integer add / multiply / divmod in the inner
  loop of the respective method. This is a unit we can defend and reproduce
  without relying on wall-clock timings (which we also report, but treat as
  secondary because they include GC, interpreter overhead, etc.). For
  Method A we count one op per divisor-trial probe; for B one op per
  trial-divide probe in the factoring loop; for C one op per (n, multiple
  of n) cell update.

We also exhibit the crossover N* in the BATCH scenario: the smallest N for
which C amortized cost per element first beats A summed cost per element.

Outputs:
  results/divisor_sum_methods.csv  — scenario, n_or_N, k, method,
                                     ops_or_terms, wall_seconds, value or
                                     batch_checksum.
  console table + identified crossover N*.

Reproducibility:
  Python 3.11.15, sympy 1.14.0, mpmath 1.3.0 (sympy used only to cross-
  validate values, not in the inner loops). Inner loops use pure-Python
  big-int arithmetic so the "op" count is faithful to the runtime work.
"""
from __future__ import annotations
import csv
import math
import time
from pathlib import Path

# -------------- Method A: direct divisor enumeration --------------

def sigma_k_direct(n: int, k: int) -> tuple[int, int]:
    """σ_k(n) by trial-division divisor enumeration. Returns (value, ops).

    'ops' counts every probe d in 1..⌊√n⌋, plus one big-int power and one
    add per divisor pair. Dominant inner-loop term is the probe count, so we
    return that as a defensible ops figure.
    """
    if n <= 0:
        raise ValueError("n must be positive")
    total = 0
    ops = 0
    r = math.isqrt(n)
    for d in range(1, r + 1):
        ops += 1
        if n % d == 0:
            total += d ** k
            other = n // d
            if other != d:
                total += other ** k
    return total, ops


# -------------- Method B: Möbius / multiplicative formula --------------

def factor_trial(n: int) -> tuple[dict[int, int], int]:
    """Trial-divide factorization. Returns (factorization dict, ops).

    'ops' counts divisibility probes (one per candidate prime tried before
    we either divide it out or reject it). After fully extracting small
    primes up to √(remaining), the leftover (if >1) is itself prime.
    """
    ops = 0
    out: dict[int, int] = {}
    m = n
    # handle 2 specially
    while m % 2 == 0:
        ops += 1
        out[2] = out.get(2, 0) + 1
        m //= 2
    p = 3
    while p * p <= m:
        ops += 1
        if m % p == 0:
            cnt = 0
            while m % p == 0:
                m //= p
                cnt += 1
                ops += 1
            out[p] = cnt
        p += 2
    if m > 1:
        out[m] = 1
    return out, ops


def sigma_k_mobius(n: int, k: int) -> tuple[int, int]:
    """σ_k(n) via the multiplicative formula.

    For k == 0:   σ_0(n) = number-of-divisors = ∏ (a_i + 1)
    For k > 0:    σ_k(n) = ∏ (p_i^{k(a_i+1)} − 1) / (p_i^k − 1)
    """
    if n <= 0:
        raise ValueError("n must be positive")
    fac, ops = factor_trial(n)
    if k == 0:
        prod = 1
        for _, a in fac.items():
            prod *= (a + 1)
        return prod, ops
    prod = 1
    for p, a in fac.items():
        pk = p ** k
        prod *= (pk ** (a + 1) - 1) // (pk - 1)
    return prod, ops


# -------------- Method C: Lambert / Eisenstein batch sieve --------------

def sigma_k_batch_lambert(N: int, k: int) -> tuple[list[int], int]:
    """σ_k(1..N) all at once, via the divisor-sum sieve coming from the
    Lambert identity  Σ n^k q^n / (1 − q^n) = Σ σ_k(m) q^m.

    Inner-loop ops = Σ_{n=1..N} ⌊N/n⌋, the classical divisor-sieve cost,
    asymptotically  N (ln N + γ − 1) + O(√N).
    Returns (sigma_list[1..N], ops).
    """
    sigma = [0] * (N + 1)
    ops = 0
    for n in range(1, N + 1):
        nk = n ** k if k > 0 else 1
        m = n
        while m <= N:
            sigma[m] += nk
            ops += 1
            m += n
    return sigma, ops


def sigma_k_batch_direct(N: int, k: int) -> tuple[list[int], int]:
    """σ_k(1..N) by calling Method A on each value. Returns (list, total ops).
    Total ops = Σ_{n=1..N} ⌊√n⌋  ≈  (2/3) N^{3/2}.
    """
    out = [0] * (N + 1)
    total_ops = 0
    for n in range(1, N + 1):
        v, o = sigma_k_direct(n, k)
        out[n] = v
        total_ops += o
    return out, total_ops


# -------------- Drivers --------------

SINGLE_NS = [10, 100, 10_000, 1_000_000, 1_000_000_000]
SINGLE_KS = [1, 2, 5]
BATCH_NS  = [100, 1_000, 10_000, 100_000]
BATCH_KS  = [1, 2, 5]


def time_call(fn, *args):
    t0 = time.perf_counter()
    out = fn(*args)
    t1 = time.perf_counter()
    return out, t1 - t0


def run_single_scenarios(rows: list[dict]):
    print("=" * 96)
    print("SINGLE σ_k(n)  —  Method A (direct √n divisor enum) vs Method B (Möbius / factor)")
    print(f"{'n':>12} {'k':>3} {'sigma_k':>30} "
          f"{'A_ops':>10} {'A_s':>10} {'B_ops':>10} {'B_s':>10} {'B/A_ops':>10}")
    print("-" * 96)
    for n in SINGLE_NS:
        for k in SINGLE_KS:
            (va, ops_a), ta = time_call(sigma_k_direct, n, k)
            (vb, ops_b), tb = time_call(sigma_k_mobius, n, k)
            assert va == vb, (n, k, va, vb)
            v_str = str(va) if len(str(va)) < 28 else (str(va)[:24] + "...")
            ratio = ops_b / ops_a if ops_a else float("nan")
            print(f"{n:>12d} {k:>3d} {v_str:>30} "
                  f"{ops_a:>10d} {ta:>10.4g} {ops_b:>10d} {tb:>10.4g} {ratio:>10.3f}")
            rows.append(dict(scenario="single", n_or_N=n, k=k, method="A_direct",
                             ops_or_terms=ops_a, wall_seconds=ta, value=str(va)))
            rows.append(dict(scenario="single", n_or_N=n, k=k, method="B_mobius",
                             ops_or_terms=ops_b, wall_seconds=tb, value=str(vb)))


def run_batch_scenarios(rows: list[dict]):
    print()
    print("=" * 96)
    print("BATCH σ_k(1..N)  —  Method A summed over batch vs Method C (Lambert sieve)")
    print(f"{'N':>10} {'k':>3} {'A_ops':>14} {'A_s':>10} {'C_ops':>14} {'C_s':>10} "
          f"{'C/A_ops':>10} {'cheap':>6}")
    print("-" * 96)
    crossover_by_k: dict[int, int | None] = {k: None for k in BATCH_KS}
    for k in BATCH_KS:
        for N in BATCH_NS:
            (a_list, ops_a), ta = time_call(sigma_k_batch_direct, N, k)
            (c_list, ops_c), tc = time_call(sigma_k_batch_lambert, N, k)
            assert a_list == c_list, f"mismatch at N={N}, k={k}"
            checksum = sum(a_list)
            ratio = ops_c / ops_a if ops_a else float("nan")
            cheap = "C" if ops_c < ops_a else "A"
            if cheap == "C" and crossover_by_k[k] is None:
                crossover_by_k[k] = N
            print(f"{N:>10d} {k:>3d} {ops_a:>14d} {ta:>10.4g} "
                  f"{ops_c:>14d} {tc:>10.4g} {ratio:>10.4f} {cheap:>6}")
            rows.append(dict(scenario="batch", n_or_N=N, k=k, method="A_direct_summed",
                             ops_or_terms=ops_a, wall_seconds=ta,
                             value=f"checksum={checksum}"))
            rows.append(dict(scenario="batch", n_or_N=N, k=k, method="C_lambert",
                             ops_or_terms=ops_c, wall_seconds=tc,
                             value=f"checksum={checksum}"))
    return crossover_by_k


def locate_crossover_fine() -> tuple[int, int]:
    """Search the small-N range one step at a time to locate exactly where
    C first beats A in op count. Returns (N*, N** = first N s.t. C strictly
    beats A and stays ahead). Op counts here are k-independent (they count
    inner-loop iterations, not big-int multiplies).
    """
    first_cross = -1
    stable_cross = -1
    streak = 0
    for N in range(1, 5000):
        ops_a = sum(math.isqrt(n) for n in range(1, N + 1))
        ops_c = sum(N // n for n in range(1, N + 1))
        if ops_c < ops_a:
            if first_cross < 0:
                first_cross = N
            streak += 1
            if streak >= 50 and stable_cross < 0:
                stable_cross = N - 49
                break
        else:
            streak = 0
    return first_cross, stable_cross


def main():
    out_path = Path(__file__).parent / "results" / "divisor_sum_methods.csv"
    out_path.parent.mkdir(exist_ok=True)
    rows: list[dict] = []

    run_single_scenarios(rows)
    crossover_by_k = run_batch_scenarios(rows)

    # All three methods independent of k for ops count → derive an analytic
    # crossover by counting probes directly, finer-grained than the BATCH_NS
    # grid (which only samples decade powers).
    print()
    print("Fine-grained crossover localization (op-count only, k-independent because")
    print("ops are integer-arithmetic probes, not big-int multiplies):")
    first_cross, stable_cross = locate_crossover_fine()
    print(f"  First N where Σ N//n < Σ √n  is  N* = {first_cross}  (single sporadic crossing)")
    print(f"  First N from which C stays ahead for 50+ consecutive N  is  N** = {stable_cross}")

    print()
    print("Per-k crossover N* in the BATCH grid (first N at which C beats A):")
    for k, N in crossover_by_k.items():
        print(f"  k = {k}:  N* in coarse grid = {N}")

    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["scenario", "n_or_N", "k",
                                          "method", "ops_or_terms",
                                          "wall_seconds", "value"])
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {out_path}")
    print(f"Rows: {len(rows)}")


if __name__ == "__main__":
    main()
