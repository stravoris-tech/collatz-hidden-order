"""
notebooks/01_predecessor_chain_roundtrip.py

Demonstration notebook (script form): predecessor-chain encoding/decoding round-trip.

Run from repository root:
  python notebooks/01_predecessor_chain_roundtrip.py
"""

from collections import Counter

from reference.encoding import encode_predecessor_chain
from reference.decoding import decode_predecessor_chain


def round_trip_range(a: int, b: int) -> None:
    assert a >= 3 and a % 2 == 1
    assert b >= a and b % 2 == 1

    for n in range(a, b + 1, 2):
        code = encode_predecessor_chain(n)
        back = decode_predecessor_chain(code)
        if back != n:
            raise RuntimeError(f"Round-trip failed at n={n}: decoded={back}, code={code}")
    print(f"Round-trip OK for odd n in [{a}, {b}]")


def show_examples(values: list[int]) -> None:
    for n in values:
        code = encode_predecessor_chain(n)
        back = decode_predecessor_chain(code)
        print(f"n={n} -> {code} -> decoded={back}")


def seed_distribution(a: int, b: int, top_k: int = 15) -> None:
    c = Counter()
    for n in range(a, b + 1, 2):
        c[encode_predecessor_chain(n).seed] += 1

    print(f"\nTop {top_k} terminal seeds by frequency on odd n in [{a}, {b}]:")
    for seed, count in c.most_common(top_k):
        print(f"  seed={seed:>6}  count={count}")


def main() -> None:

    print("Run from repo root:  python -m notebooks.01_predecessor_chain_roundtrip\n")

    # Small example set
    show_examples([3, 5, 7, 11, 19, 21, 31, 37, 955])

    # Bounded verification
    round_trip_range(3, 5001)

    # Simple distribution glance
    seed_distribution(3, 5001, top_k=20)


if __name__ == "__main__":
    main()
