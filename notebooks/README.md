# Demonstration Notebooks

This directory contains notebooks that **demonstrate** key results of the paper.

They are not exploratory experiments.

## Characteristics

- Bounded ranges only
- Deterministic output
- Clear linkage to paper statements

## Intended notebooks

- Terminal seed uniqueness
- Encoding / decoding round-trips
- Terminal family and τ-chain structure

Notebooks must import from `reference/` rather than define logic inline.

# Notebooks

These notebook-style demos are provided as executable Python modules.

Run from the repository root:

```bash
python -m notebooks.01_predecessor_chain_roundtrip
```

