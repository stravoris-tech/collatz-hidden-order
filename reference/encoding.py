"""
reference/encoding.py

Symbolic encodings for predecessor dynamics.

This module starts with a minimal, stable encoding of the smallest-predecessor chain:
it records which mod-6 branch was taken at each predecessor step until reaching a canonical seed.

This is intended as a foundation for richer orbit codes (e.g., ω* encodings) added later.
"""

from __future__ import annotations

from dataclasses import dataclass

from .arithmetic import assert_positive, assert_odd
from .canonical import canonical_chain, is_canonical_seed
from .predecessor import smallest_predecessor


@dataclass(frozen=True)
class PredecessorChainCode:
    """
    A minimal code for the smallest-predecessor chain of an odd integer n0.

    Fields
    ------
    seed : int
        The canonical terminal seed m0 (m0 ≡ 3, 9, 15 mod 24).
    branches : tuple[str, ...]
        A tuple of branch labels ("A" or "C") indicating which predecessor rule was used
        at each step. Length equals depth.
        - "A" corresponds to n ≡ 1 (mod 6): p = (4n - 1)/3
        - "C" corresponds to n ≡ 5 (mod 6): p = (2n - 1)/3
    depth : int
        Number of predecessor steps taken from n0 to reach the seed.
    """
    seed: int
    branches: tuple[str, ...]
    depth: int


def encode_predecessor_chain(n0: int, *, max_steps: int = 100_000) -> PredecessorChainCode:
    """
    Encode the smallest-predecessor chain of odd n0 as a finite symbolic code.

    The code records the canonical seed and the sequence of mod-6 branch choices.
    """
    assert_positive(n0)
    assert_odd(n0)

    if n0 < 3:
        raise ValueError("encode_predecessor_chain is defined for odd integers n0 >= 3.")

    branches: list[str] = []
    n = n0

    for _ in range(max_steps):
        if is_canonical_seed(n):
            seed = n
            return PredecessorChainCode(seed=seed, branches=tuple(branches), depth=len(branches))

        r = n % 6
        if r == 1:
            branches.append("A")
        elif r == 5:
            branches.append("C")
        elif r == 3:
            # Terminal under the paper's mod-6 predecessor rule.
            # Treat n itself as the terminal seed for this encoding.
            seed = n
            return PredecessorChainCode(seed=seed, branches=tuple(branches), depth=len(branches))
        else:
            # unreachable for odd n
            raise RuntimeError(f"Unexpected residue class for odd n: n={n}, n%6={r}")

        p = smallest_predecessor(n)
        if p == -1:
            raise RuntimeError(f"Encountered terminal marker -1 before reaching a canonical seed: n={n}")
        n = p

    raise RuntimeError(f"Did not reach a canonical seed within max_steps={max_steps} for start={n0}.")


def encode_predecessor_chain_via_chain(n0: int, *, max_steps: int = 100_000) -> PredecessorChainCode:
    """
    Alternate implementation using canonical_chain() for clarity.
    Useful as a cross-check during development.
    """
    chain = canonical_chain(n0, max_steps=max_steps)
    seed = chain[-1]

    branches: list[str] = []
    for n in chain[:-1]:
        r = n % 6
        if r == 1:
            branches.append("A")
        elif r == 5:
            branches.append("C")
        elif r == 3:
            # Terminal under the paper's mod-6 predecessor rule.
            # Treat n itself as the terminal seed for this encoding.
            seed = n
            return PredecessorChainCode(seed=seed, branches=tuple(branches), depth=len(branches))
        else:
            raise RuntimeError(f"Unexpected residue class for odd n: n={n}, n%6={r}")

    return PredecessorChainCode(seed=seed, branches=tuple(branches), depth=len(branches))
