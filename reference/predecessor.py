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


def odd_predecessors(n: int, *, search_limit: int = 1_000_000) -> list[int]:
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
