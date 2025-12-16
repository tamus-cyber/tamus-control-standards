#!/usr/bin/env python3
"""
tamus_crosswalk.py

Create a crosswalk table from an OSCAL catalog for controls that contain
props[@name='tx_required_by'] or props[@name='tamus_required_by'].

Each row:
  - Control label (zero-padded)
  - Control title
  - One column per referenced back-matter resource title
    (links[@rel='reference'] -> back-matter.resources[uuid].title)

Output formats:
  - Markdown table (default)
  - CSV (--format csv)

Usage:
  python tamus_crosswalk.py catalog.yaml
  python tamus_crosswalk.py catalog.yaml --format csv -o crosswalk.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from typing import Any, Dict, List, Set

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
    return s.replace("|", "\\|").replace("\n", " ").strip()

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
            out[r["uuid"].lower()] = (
                r.get("title")
                or r.get("description")
                or f"resource:{r['uuid']}"
            )
    return out

def has_required_by(ctrl: Dict[str, Any]) -> bool:
    for p in as_list(ctrl.get("props")):
        if p.get("name") in ("tx_required_by", "tamus_required_by"):
            return True
    return False

def zero_padded_label(ctrl: Dict[str, Any]) -> str:
    for p in as_list(ctrl.get("props")):
        if p.get("name") == "label" and p.get("class") == "zero-padded":
            return str(p.get("value", ""))
    return ""

def normalize_uuid(href: str) -> str | None:
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
        if l.get("rel") == "reference":
            u = normalize_uuid(str(l.get("href", "")))
            if u and u in uuid_map:
                out.add(uuid_map[u])
    return out

def iter_controls(doc: Dict[str, Any]):
    def walk_control(c):
        yield c
        for sc in as_list(c.get("controls")):
            yield from walk_control(sc)

    def walk_group(g):
        for c in as_list(g.get("controls")):
            yield from walk_control(c)
        for sg in as_list(g.get("groups")):
            yield from walk_group(sg)

    catalog = doc.get("catalog", doc)
    for c in as_list(catalog.get("controls")):
        yield from walk_control(c)
    for g in as_list(catalog.get("groups")):
        yield from walk_group(g)

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

    rows = []
    all_refs: Set[str] = set()

    for ctrl in iter_controls(doc):
        if not has_required_by(ctrl):
            continue
        refs = referenced_titles(ctrl, uuid_map)
        rows.append((
            zero_padded_label(ctrl),
            str(ctrl.get("title", "")),
            refs
        ))
        all_refs |= refs

    ref_cols = sorted(all_refs, key=str.casefold)
    headers = ["Control", "Title"] + ref_cols

    table_rows: List[List[str]] = []
    for label, title, refs in rows:
        row = [label, title]
        row.extend("X" if c in refs else "" for c in ref_cols)
        table_rows.append(row)

    if args.format == "csv":
        out = emit_csv(headers, table_rows)
    else:
        out = emit_markdown(headers, table_rows)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
    else:
        sys.stdout.write(out)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
