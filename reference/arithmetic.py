"""
reference/arithmetic.py

Small arithmetic helpers used throughout the reference implementation.

This module intentionally stays minimal and dependency-free.
"""

from __future__ import annotations


def nu2(n: int) -> int:
    """
    2-adic valuation ν2(n): the largest k >= 0 such that 2^k divides n.

    Requires n != 0.
    """
    if n == 0:
        raise ValueError("nu2 is undefined for n = 0.")
    n = abs(n)
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k


def strip_twos(n: int) -> tuple[int, int]:
    """
    Factor out powers of two: n = 2^z * m with m odd.

    Returns (z, m). Requires n != 0.
    """
    if n == 0:
        raise ValueError("strip_twos is undefined for n = 0.")
    z = nu2(n)
    m = n // (2 ** z)
    return z, m


def is_odd(n: int) -> bool:
    """Return True iff n is odd."""
    return (n % 2) != 0


def assert_odd(n: int, *, name: str = "n") -> None:
    """Raise ValueError if n is not odd."""
    if n % 2 == 0:
        raise ValueError(f"{name} must be odd; got {n}.")


def assert_positive(n: int, *, name: str = "n") -> None:
    """Raise ValueError if n is not positive."""
    if n <= 0:
        raise ValueError(f"{name} must be positive; got {n}.")
