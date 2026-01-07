"""
reference/steps.py

Reference definitions for the accelerated successor step maps used throughout the paper.

These functions implement the three normalized successor rules on odd integers:

- A'(n) = (3n + 1) / 4   (integer when n mod 8 in {1, 5})
- C'(n) = (3n + 1) / 2   (integer for all odd n)
- K'(n) = (n - 1) / 4    (integer when n mod 8 == 5)

This module prioritizes fidelity to the manuscript over performance.
"""

from __future__ import annotations


def Aprime(n: int) -> int:
    """
    Successor A'-step: A'(n) = (3n + 1) / 4.

    Defined on odd integers n where (3n + 1) is divisible by 4.
    In the paper's residue classification, this corresponds to n mod 8 in {1, 5}.
    """
    if n % 2 == 0:
        raise ValueError("Aprime is defined on odd integers only.")
    x = 3 * n + 1
    if x % 4 != 0:
        raise ValueError(f"Aprime requires (3n+1) divisible by 4; got n={n}.")
    return x // 4


def Cprime(n: int) -> int:
    """
    Successor C'-step: C'(n) = (3n + 1) / 2.

    Defined on odd integers n (since 3n+1 is always even for odd n).
    """
    if n % 2 == 0:
        raise ValueError("Cprime is defined on odd integers only.")
    return (3 * n + 1) // 2


def Kprime(n: int) -> int:
    """
    Successor K'-step: K'(n) = (n - 1) / 4.

    Defined on odd integers n where (n - 1) is divisible by 4.
    In the paper's residue classification, this corresponds to n mod 8 == 5.
    """
    if n % 2 == 0:
        raise ValueError("Kprime is defined on odd integers only.")
    x = n - 1
    if x % 4 != 0:
        raise ValueError(f"Kprime requires (n-1) divisible by 4; got n={n}.")
    return x // 4
