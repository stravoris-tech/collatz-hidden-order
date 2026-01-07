# Command-Line Scripts

This directory contains small CLI entrypoints that exercise the reference
implementation layer.

## Principles

- Scripts are thin wrappers over `reference/`
- No duplicated logic
- Designed for reproducibility and inspection, not speed

## Intended use

These scripts allow readers to:

- enumerate terminal seeds on bounded ranges,
- encode integers symbolically,
- decode orbit codes back to integers,

without interacting with notebooks.
