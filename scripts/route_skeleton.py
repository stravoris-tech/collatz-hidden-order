#!/usr/bin/env python3
"""
scripts/route_skeleton.py

Appendix C-lite (but matching the paper-style diagram):
Generate a "Structural vs Accelerated" route-skeleton diagram for an odd n.

This script:
  - Computes ω(n) over {A,C,K} by iterating the odd accelerated Collatz map down to 1 (§5.8),
  - Decodes ω(n) into the full structural predecessor chain [1,...,n],
  - Builds the accelerated predecessor chain by suppressing A/C nodes immediately followed by K,
    and collapsing K-runs,
  - Computes the route skeleton nodes (phase boundary endpoints),
  - Emits Graphviz DOT that renders like the paper-style Appendix C diagram.

Reader-facing usage (from repo root):

  # Print DOT to stdout (paste into Graphviz Online)
  python -m scripts.route_skeleton 57 --dot

  # Write DOT to a file
  python -m scripts.route_skeleton 57 --out output/route_57.dot

  # Also render SVG (requires Graphviz "dot" on PATH)
  python -m scripts.route_skeleton 57 --out output/route_57.dot --render

Notes:
- This does not use an atlas; it computes ω(n) directly from the accelerated odd map.
- If you later want the signature/atlas pipeline, we can extend this script.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from typing import List, Dict, Set, Callable, Optional


# ============================================================
# Successor transform: A', C', K' and the successor symbol
# ============================================================

def successor_symbol(n: int) -> str:
    """
    Return the branch symbol in {A, C, K} for the successor transform s at odd n.

    Matches your rule:
      A  <-> n mod 8 == 1
      C  <-> n mod 8 in {3,7}
      K  <-> n mod 8 == 5
    """
    if n % 2 == 0:
        raise ValueError("Input must be an odd integer")
    r = n % 8
    if r == 1:
        return "A"
    if r in (3, 7):
        return "C"
    if r == 5:
        return "K"
    raise ValueError("Unexpected residue mod 8 for an odd integer.")


def Aprime(n: int) -> int:
    """A'-step: (3n+1)/4 (valid when n mod 8 == 1)."""
    return (3 * n + 1) // 4


def Cprime(n: int) -> int:
    """C'-step: (3n+1)/2 (valid when n mod 8 in {3,7})."""
    return (3 * n + 1) // 2


def Kprime(n: int) -> int:
    """K'-step: (n-1)/4 (valid when n mod 8 == 5)."""
    return (n - 1) // 4


def s(n: int) -> int:
    """
    Successor transform on odd n, chosen so s(n) is odd:
      A -> A'(n)
      C -> C'(n)
      K -> K'(n)
    """
    sym = successor_symbol(n)
    if sym == "A":
        return Aprime(n)
    if sym == "C":
        return Cprime(n)
    if sym == "K":
        return Kprime(n)
    raise RuntimeError("unreachable")


# ============================================================
# Orbit code ω(n)
# ============================================================

def orbit_code_from_n(n: int, max_steps: int = 100000) -> str:
    """
    Computes ω(n) over {A,C,K} by iterating the successor transform down to 1,
    recording symbols in {A,C,K}, then reversing.
    """
    if n % 2 == 0:
        raise ValueError("n must be an odd integer")
    if n == 1:
        return ""

    symbols: List[str] = []
    cur = n

    for _ in range(max_steps):
        if cur == 1:
            break
        symbols.append(successor_symbol(cur))
        cur = s(cur)
    else:
        raise RuntimeError("Max steps exceeded; orbit did not reach 1.")

    symbols.reverse()
    return "".join(symbols)


def orbit_code(n: int, max_steps: int = 100000) -> str:
    """
    Orbit code ω(n) in the sense of §5.8: compute the successor orbit starting at n,
    record symbols in {A,C,K}, then reverse.
    """
    return orbit_code_from_n(n, max_steps=max_steps)


# ============================================================
# Decode ω(n): structural and accelerated predecessor chains
# ============================================================

def decode_orbit_code(code: str) -> List[int]:
    """
    Decode ω(n) over {A,C,K} into the full structural predecessor chain [1,...,n]
    using the predecessor step maps:
      A: m -> (4m - 1)/3
      C: m -> (2m - 1)/3
      K: m -> 4m + 1
    """
    m = 1
    chain = [m]
    for ch in code:
        if ch == "A":
            m = (4 * m - 1) // 3
        elif ch == "C":
            m = (2 * m - 1) // 3
        elif ch == "K":
            m = 4 * m + 1
        else:
            raise ValueError(f"Invalid symbol '{ch}' in ω(n)")
        chain.append(m)
    return chain


def accelerated_predecessor_chain_from_code(code: str) -> List[int]:
    """
    Build the accelerated predecessor chain [1,...,n] from ω(n) by:
      - suppress values produced by A or C steps immediately followed by K,
      - collapse each maximal K^r into a single step (record only the final lifted value).
    """
    m = 1
    chain = [m]
    i = 0
    L = len(code)

    while i < L:
        ch = code[i]

        if ch == "A":
            m = (4 * m - 1) // 3
            if i + 1 >= L or code[i + 1] != "K":
                chain.append(m)
            i += 1
            continue

        if ch == "C":
            m = (2 * m - 1) // 3
            if i + 1 >= L or code[i + 1] != "K":
                chain.append(m)
            i += 1
            continue

        if ch == "K":
            while i < L and code[i] == "K":
                m = 4 * m + 1
                i += 1
            chain.append(m)
            continue

        raise ValueError(f"Invalid symbol '{ch}' in ω(n)")

    return chain


# ============================================================
# Route skeleton endpoints (phase boundary endpoints)
# ============================================================

def parse_blocks(code: str) -> List[str]:
    """
    Split ω(n) into maximal blocks of:
      - K^r
      - (A/C)^r
    """
    blocks: List[str] = []
    i = 0
    while i < len(code):
        ch = code[i]
        if ch == "K":
            j = i
            while j < len(code) and code[j] == "K":
                j += 1
            blocks.append(code[i:j])
            i = j
        else:
            j = i
            while j < len(code) and code[j] in ("A", "C"):
                j += 1
            blocks.append(code[i:j])
            i = j
    return blocks


def route_skeleton_from_code(code: str, structural_chain: List[int]) -> List[int]:
    """
    Junction nodes (phase boundaries): endpoints of maximal blocks in ω(n).
    """
    if len(structural_chain) != len(code) + 1:
        raise ValueError("Expected len(structural_chain) == len(ω(n)) + 1")
    blocks = parse_blocks(code)
    endpoints = [structural_chain[0]]  # start (1)
    idx = 0
    for b in blocks:
        idx += len(b)
        endpoints.append(structural_chain[idx])
    return endpoints


# ============================================================
# DOT generation (paper-style)
# ============================================================

def make_route_dot(
    n: int,
    code: str,
    structural_chain: List[int],
    accelerated_chain: List[int],
    *,
    graph_name: str | None = None,
    fillcolor_route: str = "#7FA6E6",
    nodesep: float = 0.15,
    ranksep: float = 0.65,
    font_node: str = "Helvetica",
    font_edge: str = "Helvetica",
    fontsize_node: int = 12,
    fontsize_edge: int = 11,
    penwidth_solid: float = 2.2,
    penwidth_dashed: float = 0.55,

    # Level-indicator extension
    predecessor_chain_fn: Optional[Callable[[int], List[int]]] = None,
    add_level_indicators: bool = False,

    # Styling for “true terminal” of a level chain when it’s an extension-only node
    level_terminal_color: str = "#E57373",  # soft red

    # NEW: also treat any of these as “indicator seeds”, even if not suppressed
    extra_indicator_seeds: Optional[List[int]] = None,
) -> str:
    gname = graph_name or f"Collatz{n}"

    route_nodes = set(route_skeleton_from_code(code, structural_chain))

    structural_set: Set[int] = set(structural_chain)
    accel_set: Set[int] = set(accelerated_chain)

    suppressed: Set[int] = {x for x in structural_set if x not in accel_set}

    # Node ids
    def nid(x: int) -> str:
        return f"n_{x}"

    def lid(seed: int, x: int) -> str:
        return f"lvl_{seed}_{x}"

    # ---------
    # Helper: build the FULL “level chain” by repeatedly chaining predecessor_chain(last)
    # until we hit the diagram’s target n (e.g., 27), or we can’t progress.
    # Returns a list of values to place to the RIGHT of the seed.
    # ---------
    def transitive_level_chain(seed: int) -> List[int]:
        if predecessor_chain_fn is None:
            return []

        seen: Set[int] = set()
        out: List[int] = []

        cur = seed
        while True:
            if cur in seen:
                break
            seen.add(cur)

            chain = predecessor_chain_fn(cur) or []
            # drop -1 if present (your predecessor_chain ends with -1)
            chain = [x for x in chain if x != -1]

            if not chain:
                break

            # If your predecessor_chain(cur) returns a list that ends in cur itself,
            # drop that self-repeat so we only draw nodes to the right.
            if chain and chain[-1] == cur:
                chain = chain[:-1]
                if not chain:
                    break

            # Append, but stop early if we reach the target n
            for x in chain:
                out.append(x)
                if x == n:
                    return out

            cur = out[-1]

        return out

    # ---------
    # Build level chains for:
    #   - all suppressed nodes (as before)
    #   - plus any extra indicator seeds (e.g., [137]) you want
    # ---------
    level_chains: Dict[int, List[int]] = {}
    indicator_seeds: Set[int] = set(suppressed)
    if extra_indicator_seeds:
        indicator_seeds |= set(extra_indicator_seeds)

    if add_level_indicators:
        if predecessor_chain_fn is None:
            raise ValueError("add_level_indicators=True requires predecessor_chain_fn.")

        for s in indicator_seeds:
            chain = transitive_level_chain(s)
            level_chains[s] = chain

    # Track “true terminal endpoints” of level chains (e.g., 27)
    level_terminals: Set[int] = set()
    for s, ch in level_chains.items():
        if ch:
            level_terminals.add(ch[-1])

    # ---------
    # Main nodes
    # ---------
    node_lines: List[str] = []
    for x in structural_chain:
        styles: List[str] = []
        label = str(x)

        is_supp = x in suppressed
        is_route = x in route_nodes

        # Terminals are the *endpoints* of the transitive level chains,
        # plus any indicator seed whose chain is empty (e.g., 3).
        terminal_indicators: Set[int] = set(level_terminals)
        if add_level_indicators:
            for s in indicator_seeds:
                if not level_chains.get(s, []):
                    terminal_indicators.add(s)

        is_terminal_indicator = add_level_indicators and (x in terminal_indicators)

        extra_attrs_parts: List[str] = []

        if is_supp:
            label = f"{x}\\n(suppressed)"
            styles.append("dashed")

        if is_route:
            styles.append("filled")

        # Red dashed outline ONLY for terminal indicators (123,39,33,9,3 in your example)
        if is_terminal_indicator:
            extra_attrs_parts.append('color="#C62828"')
            extra_attrs_parts.append("penwidth=2.6")
            if "dashed" not in styles:
                styles.append("dashed")

        extra_attrs = ""
        if extra_attrs_parts:
            extra_attrs = ", " + ", ".join(extra_attrs_parts)

        if styles:
            style_str = ",".join(styles)
            if "filled" in styles:
                node_lines.append(
                    f'  {nid(x)} [label="{label}", style="{style_str}", fillcolor="{fillcolor_route}"{extra_attrs}];'
                )
            else:
                node_lines.append(
                    f'  {nid(x)} [label="{label}", style="{style_str}"{extra_attrs}];'
                )
        else:
            node_lines.append(f'  {nid(x)} [label="{label}"{extra_attrs}];')

    # ---------
    # Rank lanes (your existing logic)
    # ---------
    pos: Dict[int, int] = {v: i for i, v in enumerate(structural_chain)}
    rs = route_skeleton_from_code(code, structural_chain)
    accel_index = {v: i for i, v in enumerate(accelerated_chain)}

    def is_skip_target(b: int) -> bool:
        j = accel_index.get(b)
        if j is None or j == 0:
            return False
        prev = accelerated_chain[j - 1]
        return abs(pos[prev] - pos[b]) > 1

    rank_lines: List[str] = []
    for a, b in zip(rs[:-1], rs[1:]):
        if is_skip_target(b):
            continue
        i, j = pos[a], pos[b]
        lane = structural_chain[i : j + 1] if i <= j else structural_chain[j : i + 1]
        rank_lines.append("  { rank=same; " + "; ".join(nid(x) for x in lane) + " }")

    # ---------
    # Level-indicator extension nodes/edges/ranks
    #   IMPORTANT: reuse existing main nodes when possible (avoid duplicates)
    # ---------
    level_node_lines: List[str] = []
    level_edge_lines: List[str] = []
    level_rank_lines: List[str] = []

    def ref_for(seed: int, x: int) -> str:
        return nid(x) if x in structural_set else lid(seed, x)

    if add_level_indicators:
        for s, chain in level_chains.items():
            if not chain:
                continue

            # Create extension-only nodes (only those NOT in main structural chain)
            for i, x in enumerate(chain):
                if x in structural_set:
                    continue  # reuse existing node
                is_terminal = (i == len(chain) - 1)
                if is_terminal:
                    level_node_lines.append(
                        f'  {lid(s, x)} [label="{x}", shape=box, '
                        f'style="dashed,filled", fillcolor="{level_terminal_color}", '
                        f'fontname="{font_node}", fontsize={fontsize_node}, margin="0.12,0.08"];'
                    )
                else:
                    level_node_lines.append(
                        f'  {lid(s, x)} [label="{x}", shape=box, style="dashed", '
                        f'fontname="{font_node}", fontsize={fontsize_node}, margin="0.12,0.08"];'
                    )

            # dashed edges: s -> chain[0] -> chain[1] -> ...
            level_edge_lines.append(f'  edge [penwidth={penwidth_dashed}, style="dashed"];')
            level_edge_lines.append(f"  {nid(s)} -> {ref_for(s, chain[0])};")
            for a, b in zip(chain[:-1], chain[1:]):
                level_edge_lines.append(f"  {ref_for(s, a)} -> {ref_for(s, b)};")

            # same rank: s and all chain nodes
            level_rank_lines.append(
                "  { rank=same; " + "; ".join([nid(s)] + [ref_for(s, x) for x in chain]) + " }"
            )

    # ---------
    # Accelerated backbone + 01-lift bridges (unchanged)
    # ---------
    edge_solid: List[str] = []
    edge_dashed: List[str] = []

    def structural_path(u: int, v: int) -> List[int]:
        iu, iv = pos[u], pos[v]
        if iu <= iv:
            return structural_chain[iu : iv + 1]
        return structural_chain[iv : iu + 1]

    edge_solid.append(f'  edge [penwidth={penwidth_solid}, style="solid"];')
    for u, v in zip(accelerated_chain[:-1], accelerated_chain[1:]):
        path = structural_path(u, v)
        if len(path) == 2:
            edge_solid.append(f"  {nid(u)} -> {nid(v)};")
        else:
            edge_solid.append(f'  {nid(u)} -> {nid(v)} [label="accelerated"];')
            edge_dashed.append(f'  edge [penwidth={penwidth_dashed}, style="dashed"];')
            for a, b in zip(path[:-1], path[1:]):
                if b == path[-1]:
                    edge_dashed.append(
                        f'  {nid(a)} -> {nid(b)} [label=" 01-lift", style="dashed", weight=5];'
                    )
                else:
                    edge_dashed.append(f"  {nid(a)} -> {nid(b)};")

    # ---------
    # Assemble DOT
    # ---------
    dot: List[str] = []
    dot.append(f"digraph {gname} {{")
    dot.append("  rankdir=BT;")
    dot.append("  splines=true;")
    dot.append(f"  nodesep={nodesep};")
    dot.append(f"  ranksep={ranksep};")
    dot.append("")
    dot.append(
        f'  node [shape=box, fontname="{font_node}", fontsize={fontsize_node}, margin="0.12,0.08"];'
    )
    dot.append(f'  edge [fontname="{font_edge}", fontsize={fontsize_edge}, arrowsize=0.7];')
    dot.append("")

    dot.append("  // Nodes")
    dot.extend(node_lines)

    if level_node_lines:
        dot.append("")
        dot.append("  // Level-indicator extension nodes")
        dot.extend(level_node_lines)

    dot.append("")
    dot.append("  // Rank lanes (optional)")
    dot.extend(rank_lines)

    if level_rank_lines:
        dot.append("")
        dot.append("  // Level-indicator rank lanes")
        dot.extend(level_rank_lines)

    dot.append("")
    dot.append("  // Accelerated backbone + dashed 01-lift bridges")
    dot.extend(edge_solid)
    if edge_dashed:
        dot.append("")
        dot.extend(edge_dashed)

    if level_edge_lines:
        dot.append("")
        dot.append("  // Level-indicator dashed edges")
        dot.extend(level_edge_lines)

    dot.append("")
    dot.append('  edge [penwidth=1.0, style="solid"];')
    dot.append("}")
    return "\n".join(dot)


def render_svg(dot_text: str, svg_path: str) -> None:
    if shutil.which("dot") is None:
        raise RuntimeError("Graphviz 'dot' not found. Install Graphviz to render SVG.")
    proc = subprocess.run(
        ["dot", "-Tsvg"],
        input=dot_text.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    with open(svg_path, "wb") as f:
        f.write(proc.stdout)


# ============================================================
# Smallest-predecessor chain (for level indicators)
# ============================================================

def smallest_predecessor(n: int) -> int:
    """
    Return the smallest predecessor of an odd integer n in the accelerated Collatz graph.
    """
    return (((n - 3) % 6) * n - 1) // 3


def predecessor_chain(n: int) -> list[int]:
    pred_chain = []
    while n not in (1, -1):
        n = smallest_predecessor(n)
        pred_chain.append(n)
    # if predecessors[-1] == -1:   # don't keep the sentinel if not needed
    #     predecessors.pop()
    return pred_chain


# ============================================================
# CLI
# ============================================================

def main() -> None:
    p = argparse.ArgumentParser(description="Appendix C-lite: structural vs accelerated route skeleton DOT for odd n.")
    p.add_argument("n", type=int, help="Odd integer n >= 1")
    p.add_argument("--max-steps", type=int, default=100000, help="Max steps for orbit-to-1 computation")
    p.add_argument("--dot", action="store_true", help="Print DOT to stdout (for Graphviz Online)")
    p.add_argument("--out", type=str, default=None, help="Write DOT to this path (e.g. output/route_57.dot)")
    p.add_argument("--render", action="store_true", help="Render SVG next to --out using Graphviz dot")
    args = p.parse_args()

    n = args.n
    if n % 2 == 0 or n < 1:
        raise SystemExit("n must be a positive odd integer")

    code = orbit_code_from_n(n, max_steps=args.max_steps)
    structural_chain = decode_orbit_code(code)
    accelerated_chain = accelerated_predecessor_chain_from_code(code)

    dot_text = make_route_dot(
        n=n,
        code=orbit_code(n),
        structural_chain=structural_chain,
        accelerated_chain=accelerated_chain,
        graph_name="Collatz_StructuralVsAccelerated_level",
        predecessor_chain_fn=predecessor_chain,
        add_level_indicators=True,
        extra_indicator_seeds=[n],
    )

    # Helpful terminal output
    print(f"n = {n}")
    print(f"ω(n) = {code}")
    print(f"structural chain length  = {len(structural_chain)}")
    print(f"accelerated chain length = {len(accelerated_chain)}")
    print(f"route skeleton R(n)      = {route_skeleton_from_code(code, structural_chain)}")

    if args.dot:
        print("\n# --- Graphviz DOT (paste into Graphviz Online) ---\n")
        print(dot_text, end="")

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(dot_text)
        print(f"\nWrote DOT: {args.out}")

        if args.render:
            svg_path = args.out.rsplit(".", 1)[0] + ".svg" if "." in args.out else args.out + ".svg"
            render_svg(dot_text, svg_path)
            print(f"Wrote SVG: {svg_path}")
    else:
        if args.render:
            raise SystemExit("--render requires --out so we know where to write the SVG.")


if __name__ == "__main__":
    main()
