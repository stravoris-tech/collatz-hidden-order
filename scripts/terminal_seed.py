#!/usr/bin/env python3
"""
scripts/terminal_seed.py

CLI utility to compute the terminal seed (mod-6 terminal point) reached by following the
smallest-predecessor chain, and to display the associated predecessor-chain code.

Examples:
  python -m scripts.terminal_seed 955
  python -m scripts.terminal_seed --range 3 201
"""

from __future__ import annotations

import argparse

from reference.encoding import encode_predecessor_chain
from reference.decoding import decode_predecessor_chain


def run_single(n: int) -> None:
    code = encode_predecessor_chain(n)
    back = decode_predecessor_chain(code)
    if back != n:
        raise SystemExit("ERROR: decode(encode(n)) != n")

    print(f"n            = {n}")
    print(f"terminal seed = {code.seed}")
    print(f"depth        = {code.depth}")
    print(f"branches     = {' '.join(code.branches) if code.branches else '(none)'}")


def run_range(a: int, b: int) -> None:
    if a > b:
        a, b = b, a
    if a < 3:
        a = 3
    if a % 2 == 0:
        a += 1

    for n in range(a, b + 1, 2):
        code = encode_predecessor_chain(n)
        ok = (decode_predecessor_chain(code) == n)
        print(f"{n:>6}  seed={code.seed:>6}  depth={code.depth:>4}  ok={ok}")
        if not ok:
            raise SystemExit(f"ERROR at n={n}")


def main() -> None:
    p = argparse.ArgumentParser(description="Compute terminal seed and predecessor-chain code for odd integers.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("n", nargs="?", type=int, help="Odd integer n >= 3")
    g.add_argument("--range", nargs=2, type=int, metavar=("A", "B"),
                   help="Run on odd n in [A,B] (bounded)")
    args = p.parse_args()

    if args.range is not None:
        a, b = args.range
        run_range(a, b)
    else:
        n = args.n
        if n is None:
            raise SystemExit("Provide n or --range A B")
        run_single(n)


if __name__ == "__main__":
    main()
