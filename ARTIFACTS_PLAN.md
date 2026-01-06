# ARTIFACTS_PLAN — Collatz Hidden Order Repository

This document defines the **scope, structure, and quality bar** for adding non-paper artifacts to this repository.
It exists to prevent ad-hoc growth and to ensure any tooling remains aligned with the manuscript.

---

## 1. Purpose

This repository accompanies the paper:

**The Hidden Order of the Collatz Problem**
(“Collatz Hidden Order” for short)

It has two goals:

1. Host the stable, citable manuscript and figures.
2. Provide **reference-grade reproducibility artifacts** that act as executable witnesses to the paper’s definitions.

---

## 2. Non-goals

The repository is **not** intended to be:

- a general-purpose “Collatz solver” project,
- a performance-optimized implementation,
- a large-scale computational verification effort,
- a benchmarking suite,
- a claim of resolution of the Collatz conjecture.

Artifacts should support the paper; they should not introduce new claims.

---

## 3. Quality bar (“reference-grade”)

All code artifacts must satisfy:

- **Fidelity first:** implement the paper’s definitions as written.
- **Clarity over cleverness:** readable, minimal abstraction.
- **Deterministic behavior:** no randomness unless explicitly stated and seeded.
- **Light dependencies:** prefer pure Python (standard library only).
- **Stable I/O:** scripts and notebooks should be easy to rerun and interpret.
- **Traceability:** each module/function should point back to the relevant paper section / appendix entry.

---

## 4. Proposed repository structure

Target layout:

paper/ # PDF and manuscript artifacts
figures/ # figures referenced by the paper

reference/ # Appendix D mirrored as runnable modules
README.md # mapping from paper/appendix to modules
arithmetic.py
steps.py # A', C', K'
predecessor.py
successor.py
canonical.py
encoding.py
decoding.py

scripts/ # CLI entrypoints (thin wrappers over reference/)
README.md
encode_integer.py
decode_orbit.py
enumerate_terminal_seeds.py

notebooks/ # demonstrations (not experiments)
README.md
01_terminal_seeds.ipynb
02_encoding_decoding.ipynb
03_family_orbits.ipynb

tests/ # sanity tests (optional but encouraged)
test_steps.py
test_encoding_decoding.py

Notes:
- `reference/` is the authoritative implementation layer.
- `scripts/` and `notebooks/` must import from `reference/` (no duplicated logic).

---

## 5. Naming and conventions

- Function names should match the paper (e.g., `Aprime`, `Cprime`, `Kprime`) where practical.
- Docstrings should be concise and aligned with the manuscript’s definitions.
- Avoid “framework-style” engineering; keep modules small and explicit.
- If a helper appears in multiple appendix blocks, define it once in `reference/` and import it elsewhere.

---

## 6. Reproducibility scope

Artifacts may provide:

- small demonstrations of termination/uniqueness properties on bounded ranges,
- encoding/decoding round-trips that reconstruct integers exactly,
- regeneration of selected figures where feasible,
- minimal CLI entrypoints for readers who prefer scripts over notebooks.

Artifacts must **not** present computational evidence as proof.

---

## 7. Release discipline and promotion

Development occurs in the private dev mirror repository.
Only finished, coherent commits will be promoted to the public repository.

Promotion targets:

- a small number of intentional commits,
- stable filenames and directory structure,
- minimal “work-in-progress” history in public.

---

## 8. License

All added artifacts are released under the repository’s MIT license unless otherwise stated.

If any third-party assets or code are introduced, they must be clearly labeled with their licenses and provenance.

---

