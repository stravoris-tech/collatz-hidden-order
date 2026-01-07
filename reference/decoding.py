"""
reference/decoding.py

Decoding utilities for the minimal predecessor-chain encoding.

Given a PredecessorChainCode(seed, branches), reconstruct the original odd integer n0
by inverting each predecessor step in reverse order.

If the forward (predecessor) rules are:
  A-branch: p = (4n - 1) / 3
  C-branch: p = (2n - 1) / 3

then the inverses are:
  A-branch inverse: n = (3p + 1) / 4  == Aprime(p)
  C-branch inverse: n = (3p + 1) / 2  == Cprime(p)
"""

from __future__ import annotations

from .encoding import PredecessorChainCode
from .steps import Aprime, Cprime


def decode_predecessor_chain(code: PredecessorChainCode) -> int:
    """
    Decode a PredecessorChainCode back to the original odd integer n0.

    Decoding procedure:
      start at n = code.seed
      for each branch in reversed(code.branches):
        - if "A": n = (3n + 1)/4  (Aprime)
        - if "C": n = (3n + 1)/2  (Cprime)

    Returns the reconstructed n0.
    """
    if code.depth != len(code.branches):
        raise ValueError("Invalid code: depth must equal len(branches).")

    n = code.seed
    for b in reversed(code.branches):
        if b == "A":
            n = Aprime(n)
        elif b == "C":
            n = Cprime(n)
        else:
            raise ValueError(f"Unknown branch label: {b!r}")
    return n
