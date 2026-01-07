#!/usr/bin/env python3
"""
scripts/encode_decode.py

Small CLI utility to encode an odd integer using the predecessor-chain code and decode it back.

Examples:
  python scripts/encode_decode.py 27
  python scripts/encode_decode.py 955
  python scripts/encode_decode.py --range 3 101
"""

from __future__ import annotations

import argparse

from reference.encoding import encode_predecessor_chain
from reference.decoding import decode_predecessor_chain


def run_single(n: int) -> None:
    code = encode_predecessor_chain(n)
    back = decode_predecessor_chain(code)
    print(f"n       = {n}")
    print(f"code    = {code}")
    print(f"decoded = {back}")
    if back != n:
        raise SystemExit("ERROR: decode(encode(n)) != n")


def run_range(a: int, b: int) -> None:
    if a > b:
        a, b = b, a
    if a < 3:
        a = 3
    if a % 2 == 0:
        a += 1

    for n in range(a, b + 1, 2):
        code = encode_predecessor_chain(n)
        back = decode_predecessor_chain(code)
        ok = (back == n)
        print(f"{n:>6}  seed={code.seed:>6}  depth={code.depth:>4}  ok={ok}")
        if not ok:
            raise SystemExit(f"ERROR at n={n}: decoded={back}")


def main() -> None:
    p = argparse.ArgumentParser(description="Encode/decode predecessor-chain codes for odd integers.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("n", nargs="?", type=int, help="Odd integer n >= 3 to encode/decode")
    g.add_argument("--range", nargs=2, type=int, metavar=("A", "B"),
                   help="Run encode/decode check for odd n in [A,B] (bounded)")
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
