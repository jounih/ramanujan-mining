"""Finite-pole semiseparable causal attention.

Defined by

    A_{ij} = 1_{j <= i} * sum_{r=1}^{R} q_{i,r} * k_{j,r} * alpha_r^(i-j)

with 0 < alpha_r < 1. The unnormalized output is

    y_i^(unn) = sum_{j <= i} A_{ij} v_j
              = sum_r q_{i,r} * S_{r,i}    where   S_{r,i} = sum_{j<=i} alpha_r^(i-j) k_{j,r} v_j .

The "normalized" variant divides by the row-sum

    Z_i = sum_{j <= i} A_{ij} = sum_r q_{i,r} * Z_{r,i}   where   Z_{r,i} = sum_{j<=i} alpha_r^(i-j) k_{j,r} .

S and Z each satisfy the one-step recurrence

    S_{r,i} = alpha_r * S_{r,i-1} + k_{i,r} * v_i ,
    Z_{r,i} = alpha_r * Z_{r,i-1} + k_{i,r} ,

so the entire output can be computed in O(N*R*d_v) time using only O(R*d_v)
state, with no approximation.

We expose:

  - direct_finite_pole_attention      : O(N^2 * R * d_v) reference
  - recurrent_finite_pole_attention   : O(N   * R * d_v) recurrence

Both return identical results to floating-point precision. This is an
EXACT closed form for this attention semantics, not an approximation to
softmax attention. (See diary 50.)
"""
from __future__ import annotations

import numpy as np


def _validate(q, k, v, alpha):
    q = np.asarray(q, dtype=np.float64)
    k = np.asarray(k, dtype=np.float64)
    v = np.asarray(v, dtype=np.float64)
    alpha = np.asarray(alpha, dtype=np.float64)
    if q.ndim != 2 or k.ndim != 2 or v.ndim != 2 or alpha.ndim != 1:
        raise ValueError(
            "Expected q, k of shape (N, R), v of shape (N, d_v), alpha of shape (R,). "
            f"Got q={q.shape}, k={k.shape}, v={v.shape}, alpha={alpha.shape}"
        )
    N, R = q.shape
    if k.shape != (N, R):
        raise ValueError(f"k must have shape (N, R) = ({N}, {R}); got {k.shape}")
    if v.shape[0] != N:
        raise ValueError(f"v must have N={N} rows; got {v.shape[0]}")
    if alpha.shape[0] != R:
        raise ValueError(f"alpha must have length R={R}; got {alpha.shape[0]}")
    if np.any(alpha <= 0) or np.any(alpha >= 1):
        # Outside (0,1) the recurrence is still mathematically well-defined,
        # but the closed-form "geometric decay" interpretation breaks. We
        # warn-via-error to surface this fast in tests.
        raise ValueError(
            f"poles alpha must lie in (0,1) for the geometric-decay form; got {alpha}"
        )
    return q, k, v, alpha


def direct_finite_pole_attention(q, k, v, alpha, normalized=False):
    """O(N^2 * R * d_v) reference implementation.

    Builds the full (N, N) attention matrix from the closed-form definition
    above and applies it to v. Used as the exactness oracle for the
    recurrence.

    Parameters
    ----------
    q, k : (N, R) arrays
    v    : (N, d_v) array
    alpha: (R,) array, each in (0, 1)
    normalized : if True, divide each row by Z_i = sum_{j<=i} A_{ij}.

    Returns
    -------
    y : (N, d_v) array
    """
    q, k, v, alpha = _validate(q, k, v, alpha)
    N, R = q.shape
    d_v = v.shape[1]

    # Precompute the lag matrix L[i,j] = i - j for j <= i, else 0 (masked).
    # Then for each pole r, build a_r[i,j] = q_{i,r} * k_{j,r} * alpha_r^L[i,j]
    # masked to j <= i, and accumulate into A.
    A = np.zeros((N, N), dtype=np.float64)
    rows = np.arange(N)[:, None]
    cols = np.arange(N)[None, :]
    lag = rows - cols
    causal_mask = (lag >= 0)

    for r in range(R):
        # alpha_r^lag, only where causal_mask is True.
        power = np.zeros_like(lag, dtype=np.float64)
        power[causal_mask] = alpha[r] ** lag[causal_mask]
        A += q[:, r:r+1] * k[:, r][None, :] * power

    y = A @ v
    if normalized:
        Z = A.sum(axis=1)
        # Avoid /0 at the very first row when k_{0,r}=0 for all r. In that
        # case y is already 0 and we leave it as 0.
        nz = Z != 0
        y_out = np.zeros_like(y)
        y_out[nz] = y[nz] / Z[nz, None]
        return y_out
    return y


def recurrent_finite_pole_attention(q, k, v, alpha, normalized=False):
    """O(N * R * d_v) recurrence implementation.

    Computes the same output as direct_finite_pole_attention using only the
    rank-(R*d_v) running state (S, Z). No approximation.

    Parameters
    ----------
    q, k : (N, R) arrays
    v    : (N, d_v) array
    alpha: (R,) array, each in (0, 1)
    normalized : if True, divide each row by Z_i.

    Returns
    -------
    y : (N, d_v) array
    """
    q, k, v, alpha = _validate(q, k, v, alpha)
    N, R = q.shape
    d_v = v.shape[1]

    # Running state per pole.
    S = np.zeros((R, d_v), dtype=np.float64)   # S[r, :]
    Zr = np.zeros(R, dtype=np.float64)         # Z_{r,i}
    y = np.zeros((N, d_v), dtype=np.float64)
    Z_total = np.zeros(N, dtype=np.float64)

    for i in range(N):
        # S_{r,i} = alpha_r * S_{r,i-1} + k_{i,r} * v_i
        # Z_{r,i} = alpha_r * Z_{r,i-1} + k_{i,r}
        S = alpha[:, None] * S + k[i][:, None] * v[i][None, :]
        Zr = alpha * Zr + k[i]

        # y_i^(unn) = sum_r q_{i,r} S_{r,i}
        y[i] = q[i] @ S                        # shape (d_v,)
        Z_total[i] = q[i] @ Zr

    if normalized:
        nz = Z_total != 0
        y_out = np.zeros_like(y)
        y_out[nz] = y[nz] / Z_total[nz, None]
        return y_out
    return y
