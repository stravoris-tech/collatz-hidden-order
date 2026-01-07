"""
reference/successor.py

Accelerated Collatz successor maps.

This module implements the accelerated successor map used throughout the paper:
powers of two are stripped, the odd step is applied, and powers of two are stripped again.

The implementation follows the symbolic formulation rather than numerical iteration.
"""

from __future__ import annotations

from .arithmetic import strip_twos, assert_positive
from .steps import Aprime, Cprime, Kprime


def accelerated_successor(n: int) -> int:
    """
    Return the accelerated Collatz successor of a positive integer n.

    Procedure:
    1. Write n = 2^z * m with m odd.
    2. Apply the appropriate odd successor rule to m.
    3. Strip all powers of two from the result.

    Returns the next odd integer in the accelerated orbit.
    """
    assert_positive(n)

    # Step 1: reduce to odd
    _, m = strip_twos(n)

    # Step 2: apply odd successor rule
    r = m % 8
    if r in (1, 5):
        y = Aprime(m)
    elif r == 3:
        y = Cprime(m)
    elif r == 7:
        y = Cprime(m)
    else:
        # unreachable for odd m
        raise RuntimeError(f"Unexpected odd residue class: m={m}")

    # Step 3: reduce to odd again
    _, m_next = strip_twos(y)
    return m_next
