# Reference Implementation Layer

This directory contains **reference-grade implementations** of the symbolic
constructions defined in the paper *The Hidden Order of the Collatz Problem*.

The intent is fidelity to the manuscript, not performance or generality.

## Scope

- One-to-one mappings from Appendix D constructions to runnable code
- Clear function names aligned with the paper
- Minimal abstraction and minimal dependencies

This directory is the **authoritative implementation layer** for the repository.
All scripts and notebooks must import logic from here rather than reimplement it.

## Planned modules

- `arithmetic.py` — 2-adic helpers and odd-integer utilities
- `steps.py` — accelerated successor steps A′, C′, K′
- `predecessor.py` — predecessor rules
- `successor.py` — accelerated successor map
- `canonical.py` — canonical terminal seed logic
- `encoding.py` — symbolic orbit encoding
- `decoding.py` — inverse decoding

Each module will reference the relevant section or appendix entry in the paper.
