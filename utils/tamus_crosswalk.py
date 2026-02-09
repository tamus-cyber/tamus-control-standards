#!/usr/bin/env python3
"""
tamus_crosswalk.py

Create a crosswalk table from an OSCAL catalog for controls that contain
props[@name='tx_required_by'] or props[@name='tamus_required_by'].

Each row:
  - Parent Group (nearest enclosing group's title, if any)
  - Control label (zero-padded)
  - Control title
  - Required By: "TX DIR" if tx_required_by exists else "TAMUS" if tamus_required_by exists
  - One column per referenced back-matter resource title
    (links[@rel='reference'] -> back-matter.resources[uuid].title)

Output formats:
  - Markdown table (default)
  - CSV (--format csv)

Usage:
  python tamus_crosswalk.py catalog.yaml > crosswalk.md
  python tamus_crosswalk.py catalog.yaml --format csv -o crosswalk.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}$"
)

# -------------------------
# Generic helpers
# -------------------------

def load_oscal(path: str) -> Dict[str, Any]:
    ext = os.path.splitext(path.lower())[1]
    with open(path, "r", encoding="utf-8") as f:
        if ext in (".yaml", ".yml"):
            import yaml  # type: ignore
            return yaml.safe_load(f)
        return json.load(f)

def as_list(x: Any) -> List[Any]:
    return x if isinstance(x, list) else ([] if x is None else [x])

def md_escape(s: str) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ").strip()

# -------------------------
# OSCAL helpers
# -------------------------

def build_resource_map(doc: Dict[str, Any]) -> Dict[str, str]:
    root = doc.get("catalog", doc)
    bm = root.get("back-matter", {}) or {}
    res = as_list(bm.get("resources"))

    out: Dict[str, str] = {}
    for r in res:
        if isinstance(r, dict) and r.get("uuid"):
            out[str(r["uuid"]).lower()] = (
                r.get("title")
                or r.get("description")
                or f"resource:{r['uuid']}"
            )
    return out

def required_by(ctrl: Dict[str, Any]) -> Optional[str]:
    has_tx = False
    has_tamus = False
    for p in as_list(ctrl.get("props")):
        if not isinstance(p, dict):
            continue
        if p.get("name") == "tx_required_by":
            has_tx = True
        elif p.get("name") == "tamus_required_by":
            has_tamus = True
    if has_tx:
        return "TX DIR"
    if has_tamus:
        return "TAMUS"
    return None

def zero_padded_label(ctrl: Dict[str, Any]) -> str:
    for p in as_list(ctrl.get("props")):
        if isinstance(p, dict) and p.get("name") == "label" and p.get("class") == "zero-padded":
            return str(p.get("value", ""))
    return ""

def normalize_uuid(href: str) -> Optional[str]:
    if not href:
        return None
    h = href.strip()
    if h.startswith("#"):
        h = h[1:]
    if h.lower().startswith("urn:uuid:"):
        h = h.split(":", 2)[-1]
    return h.lower() if UUID_RE.match(h) else None

def referenced_titles(ctrl: Dict[str, Any], uuid_map: Dict[str, str]) -> Set[str]:
    out: Set[str] = set()
    for l in as_list(ctrl.get("links")):
        if not isinstance(l, dict):
            continue
        if l.get("rel") == "reference":
            u = normalize_uuid(str(l.get("href", "")))
            if u:
                out.add(uuid_map.get(u, f"resource:{u}"))
    return out

def iter_controls_with_group_title(doc: Dict[str, Any]) -> List[Tuple[Dict[str, Any], str]]:
    """
    Returns list of (control_dict, parent_group_title).
    Parent group title = nearest enclosing group.title, else "".
    Handles:
      - catalog.controls (group title empty)
      - catalog.groups[*].controls (group title set)
      - nested groups recurse; nearest title used
      - nested controls keep the same parent group title
    """
    out: List[Tuple[Dict[str, Any], str]] = []
    catalog = doc.get("catalog", doc)

    def walk_control(c: Dict[str, Any], group_title: str):
        out.append((c, group_title))
        for sc in as_list(c.get("controls")):
            if isinstance(sc, dict):
                walk_control(sc, group_title)

    def walk_group(g: Dict[str, Any], inherited_title: str = ""):
        gt = str(g.get("title") or inherited_title or "")
        for c in as_list(g.get("controls")):
            if isinstance(c, dict):
                walk_control(c, gt)
        for sg in as_list(g.get("groups")):
            if isinstance(sg, dict):
                walk_group(sg, gt)

    # top-level controls (no group)
    for c in as_list(catalog.get("controls")):
        if isinstance(c, dict):
            walk_control(c, "")

    # grouped controls
    for g in as_list(catalog.get("groups")):
        if isinstance(g, dict):
            walk_group(g, "")

    return out

# -------------------------
# Emitters
# -------------------------

def emit_markdown(headers: List[str], rows: List[List[str]]) -> str:
    lines = []
    lines.append("| " + " | ".join(md_escape(h) for h in headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for r in rows:
        lines.append("| " + " | ".join(md_escape(c) for c in r) + " |")
    return "\n".join(lines) + "\n"

def emit_csv(headers: List[str], rows: List[List[str]]) -> str:
    from io import StringIO
    buf = StringIO()
    w = csv.writer(buf)
    w.writerow(headers)
    w.writerows(rows)
    return buf.getvalue()

# -------------------------
# Main
# -------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("catalog")
    ap.add_argument("-o", "--output")
    ap.add_argument("--format", choices=["md", "csv"], default="md")
    args = ap.parse_args()

    doc = load_oscal(args.catalog)
    uuid_map = build_resource_map(doc)

    # Collect rows + reference columns
    collected: List[Tuple[str, str, str, str, Set[str]]] = []
    all_refs: Set[str] = set()

    for ctrl, group_title in iter_controls_with_group_title(doc):
        rb = required_by(ctrl)
        if not rb:
            continue

        label = zero_padded_label(ctrl)
        title = str(ctrl.get("title", "") or "")
        refs = referenced_titles(ctrl, uuid_map)

        collected.append((group_title, label, title, rb, refs))
        all_refs |= refs

    ref_cols = sorted(all_refs, key=str.casefold)
    headers = ["Group", "Control", "Title", "Required By"] + ref_cols

    rows: List[List[str]] = []
    for group_title, label, title, rb, refs in collected:
        row = [group_title, label, title, rb]
        row.extend("X" if c in refs else "" for c in ref_cols)
        rows.append(row)

    out = emit_csv(headers, rows) if args.format == "csv" else emit_markdown(headers, rows)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
    else:
        sys.stdout.write(out)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
