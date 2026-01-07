"""
reference/predecessor.py

Odd predecessor utilities for the accelerated Collatz successor.

Given an odd integer n, this module enumerates odd integers p such that:
    accelerated_successor(p) == n

The functions here are intended for bounded, reproducible demonstrations and
for validating symbolic constructions from the paper.
"""

from __future__ import annotations

from .arithmetic import assert_positive, assert_odd
from .successor import accelerated_successor


def odd_predecessors_bruteforce(n: int, *, search_limit: int = 1_000_000) -> list[int]:
    """
    Return a sorted list of odd predecessors p such that accelerated_successor(p) == n.

    This implementation is intentionally simple: it performs a bounded search.
    It is suitable for small demonstrations and sanity checks, not large-scale computation.

    Parameters
    ----------
    n : int
        Target odd integer (must be positive and odd).
    search_limit : int
        Upper bound on candidate predecessors to test (odd candidates up to this value).

    Returns
    -------
    list[int]
        Sorted list of odd predecessors within the search bound.
    """
    assert_positive(n)
    assert_odd(n)

    preds: list[int] = []
    for p in range(1, search_limit + 1, 2):
        if accelerated_successor(p) == n:
            preds.append(p)
    return preds


def min_odd_predecessor(n: int, *, search_limit: int = 1_000_000) -> int | None:
    """
    Return the smallest odd predecessor of n (within a bounded search), or None if not found.
    """
    preds = odd_predecessors(n, search_limit=search_limit)
    return preds[0] if preds else None


def smallest_predecessor(n: int) -> int:
    """
    Return the smallest predecessor in the predecessor class of an odd integer n.

    This implements the paper's mod-6 decision rule:

        n ≡ 1 (mod 6) -> (4n - 1)/3
        n ≡ 3 (mod 6) -> -1   (no predecessor / terminal)
        n ≡ 5 (mod 6) -> (2n - 1)/3

    Returns -1 exactly in the terminal case.
    """
    assert_positive(n)
    assert_odd(n)

    r = n % 6
    if r == 1:
        return (4 * n - 1) // 3
    if r == 3:
        return -1
    if r == 5:
        return (2 * n - 1) // 3

    # unreachable for odd n
    raise RuntimeError(f"Unexpected residue class for odd n: n={n}, n%6={r}")


def Pred_k(n: int, k: int) -> int:
    """
    Return the k-th odd predecessor in the immediate predecessor class of n.

    Pred_k(n) = 4^k * p0 + (4^k - 1)/3,  k >= 0
    where p0 = smallest_predecessor(n).

    If n is terminal (smallest_predecessor(n) == -1), raises ValueError.
    """
    assert_positive(n)
    assert_odd(n)
    if k < 0:
        raise ValueError(f"k must be >= 0; got {k}.")

    p0 = smallest_predecessor(n)
    if p0 == -1:
        raise ValueError(f"n={n} has no predecessors (terminal class).")

    pow4 = 4 ** k
    return pow4 * p0 + (pow4 - 1) // 3


def predecessor_chain(n0: int, *, max_steps: int = 10_000) -> list[int]:
    """
    Follow the smallest-predecessor chain starting at odd n0 until -1 (or max_steps).

    Returns the list of successive smallest predecessors (excluding the start n0).
    """
    assert_positive(n0)
    assert_odd(n0)
    if max_steps <= 0:
        raise ValueError("max_steps must be positive.")

    out: list[int] = []
    n = n0
    for _ in range(max_steps):
        p = smallest_predecessor(n)
        out.append(p)
        if p == -1:
            return out
        n = p
    raise RuntimeError(f"Chain did not terminate within max_steps={max_steps} for n0={n0}.")


def validate_smallest_predecessor(*, up_to: int = 10_000, search_limit: int = 1_000_000) -> None:
    """
    Cross-check the paper-faithful smallest_predecessor() against the bounded brute enumerator
    odd_predecessors()/min_odd_predecessor() on odd n in [1, up_to].

    This is a development-time sanity check, not a proof.
    """
    if up_to <= 0:
        raise ValueError("up_to must be positive.")

    for n in range(1, up_to + 1, 2):
        sym = smallest_predecessor(n)

        # brute: for terminal case, brute should find no predecessor (within search_limit)
        brute = min_odd_predecessor(n, search_limit=search_limit)

        if sym == -1:
            if brute is not None:
                raise AssertionError(f"Expected no predecessor for n={n}, but brute found {brute}.")
        else:
            if brute != sym:
                raise AssertionError(f"Mismatch for n={n}: symbolic={sym}, brute={brute}")

    # If we get here, all checks passed.


def predecessor_class(n: int, *, k_max: int) -> list[int]:
    """
    Return the first (k_max + 1) odd predecessors in the immediate predecessor class of n:
        [Pred_0(n), Pred_1(n), ..., Pred_k_max(n)]

    Raises ValueError if n is terminal (smallest_predecessor(n) == -1).
    """
    assert_positive(n)
    assert_odd(n)
    if k_max < 0:
        raise ValueError(f"k_max must be >= 0; got {k_max}.")

    p0 = smallest_predecessor(n)
    if p0 == -1:
        raise ValueError(f"n={n} has no predecessors (terminal class).")

    out: list[int] = []
    pow4 = 1
    for _k in range(k_max + 1):
        # Pred_k = 4^k * p0 + (4^k - 1)/3
        out.append(pow4 * p0 + (pow4 - 1) // 3)
        pow4 *= 4
    return out


def predecessor_class_iter(n: int):
    """
    Yield the infinite predecessor class Pred_0(n), Pred_1(n), Pred_2(n), ...

    Raises ValueError if n is terminal.
    """
    assert_positive(n)
    assert_odd(n)

    p0 = smallest_predecessor(n)
    if p0 == -1:
        raise ValueError(f"n={n} has no predecessors (terminal class).")

    pow4 = 1
    k = 0
    while True:
        yield (pow4 * p0 + (pow4 - 1) // 3)
        pow4 *= 4
        k += 1


def odd_predecessors(n: int, *, k_max: int = 25) -> list[int]:
    """
    Return a finite list of odd predecessors of n using the closed-form predecessor class.

    Parameters
    ----------
    n : int
        Target odd integer.
    k_max : int
        Number of predecessor-class elements to generate (controls output size).

    Returns
    -------
    list[int]
        [Pred_0(n), Pred_1(n), ..., Pred_k_max(n)].
    """
    return predecessor_class(n, k_max=k_max)


