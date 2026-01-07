"""
reference/canonical.py

Canonical terminal seed utilities.

A canonical terminal seed is an odd integer m0 satisfying:
    m0 ≡ 3, 9, 15 (mod 24)

This module provides a reference implementation for mapping an odd integer n0
to its canonical terminal seed via the smallest-predecessor chain.
"""

from __future__ import annotations

from .arithmetic import assert_positive, assert_odd
from .predecessor import smallest_predecessor


_CANONICAL_SEED_RESIDUES_MOD_24 = {3, 9, 15}


def is_canonical_seed(m: int) -> bool:
    """
    Return True iff m is a canonical terminal seed (m ≡ 3, 9, 15 mod 24).
    """
    return (m % 24) in _CANONICAL_SEED_RESIDUES_MOD_24


def canonical_chain(n0: int, *, max_steps: int = 100_000) -> list[int]:
    """
    Return the smallest-predecessor chain starting at odd n0,
    ending at the first canonical seed encountered.

    The returned list includes n0 as the first element and includes the seed as the last element.
    """
    assert_positive(n0)
    assert_odd(n0)

    chain = [n0]
    n = n0

    for _ in range(max_steps):
        if is_canonical_seed(n):
            return chain

        p = smallest_predecessor(n)

        # Terminal marker from the predecessor rule:
        # if encountered, something is inconsistent with the "canonical seed" convention.
        if p == -1:
            raise RuntimeError(
                f"Encountered terminal marker -1 before reaching a canonical seed: start={n0}, at n={n}."
            )

        chain.append(p)
        n = p

    raise RuntimeError(f"Did not reach a canonical seed within max_steps={max_steps} for start={n0}.")


def canonical_seed(n0: int, *, max_steps: int = 100_000) -> int:
    """
    Return the canonical terminal seed reached from odd n0 by following smallest predecessors.
    """
    return canonical_chain(n0, max_steps=max_steps)[-1]


def canonical_signature(n0: int, *, max_steps: int = 100_000) -> tuple[int, int]:
    """
    Return (m0, depth) where m0 is the canonical terminal seed and depth is the number of
    smallest-predecessor steps required to reach it from n0.

    depth = len(chain) - 1
    """
    chain = canonical_chain(n0, max_steps=max_steps)
    m0 = chain[-1]
    depth = len(chain) - 1
    return m0, depth
