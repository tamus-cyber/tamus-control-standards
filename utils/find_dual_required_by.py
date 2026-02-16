#!/usr/bin/env python3
"""
Find OSCAL catalog controls that have BOTH:
  - props[@name="tx_required_by"]
  - props[@name="tamus_required_by"]
...set within the same control.

Usage:
  python find_dual_required_by.py /path/to/TAMUS_resolved-profile_catalog.yaml
"""

from __future__ import annotations

import argparse
import sys
from typing import Any, Dict, Iterable, List, Optional

try:
    import yaml  # PyYAML
except ImportError as e:
    raise SystemExit("Missing dependency: PyYAML (pip install pyyaml)") from e


def _is_set(prop: Dict[str, Any]) -> bool:
    """
    Treat a prop as 'set' if it exists and contains a non-empty 'value' (or 'values').
    Falls back to True if the prop exists but has no obvious value field.
    """
    if prop is None:
        return False
    # Common OSCAL prop shape: {"name": "...", "value": "..."}
    val = prop.get("value", None)
    if isinstance(val, str):
        return val.strip() != ""
    if val is not None:
        return True

    # Some variants use "values" (list) or other keys
    vals = prop.get("values", None)
    if isinstance(vals, list):
        return len([v for v in vals if (isinstance(v, str) and v.strip()) or (v is not None)]) > 0
    if vals is not None:
        return True

    # If the prop exists with the correct name but no value field, still consider it set.
    return True


def _control_has_both_required_props(control: Dict[str, Any]) -> bool:
    props = control.get("props", []) or []
    if not isinstance(props, list):
        return False

    has_tx = False
    has_tamus = False

    for p in props:
        if not isinstance(p, dict):
            continue
        name = p.get("name")
        if name == "tx_required_by" and _is_set(p):
            has_tx = True
        elif name == "tamus_required_by" and _is_set(p):
            has_tamus = True

        if has_tx and has_tamus:
            return True

    return False


def _iter_controls_in_group(group: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    """
    Yield controls in this group and any nested sub-groups.
    """
    controls = group.get("controls", []) or []
    if isinstance(controls, list):
        for c in controls:
            if isinstance(c, dict):
                yield c

    subgroups = group.get("groups", []) or []
    if isinstance(subgroups, list):
        for sg in subgroups:
            if isinstance(sg, dict):
                yield from _iter_controls_in_group(sg)


def find_matching_control_ids(doc: Dict[str, Any]) -> List[str]:
    """
    Return list of control ids that satisfy the condition.
    """
    catalog = doc.get("catalog", {}) or {}
    groups = catalog.get("groups", []) or []
    matches: List[str] = []

    if not isinstance(groups, list):
        return matches

    for g in groups:
        if not isinstance(g, dict):
            continue
        for control in _iter_controls_in_group(g):
            if _control_has_both_required_props(control):
                cid = control.get("id")
                if isinstance(cid, str) and cid.strip():
                    matches.append(cid.strip())

    # De-duplicate while preserving order
    seen = set()
    ordered: List[str] = []
    for cid in matches:
        if cid not in seen:
            seen.add(cid)
            ordered.append(cid)

    return ordered


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="List control IDs whose props include both tx_required_by and tamus_required_by."
    )
    parser.add_argument("path", help="Path to OSCAL catalog YAML file")
    args = parser.parse_args(argv)

    try:
        with open(args.path, "r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {args.path}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"ERROR: Failed to read/parse YAML: {e}", file=sys.stderr)
        return 3

    if not isinstance(doc, dict):
        print("ERROR: YAML root is not a mapping/object.", file=sys.stderr)
        return 4

    ids = find_matching_control_ids(doc)

    for cid in ids:
        print(cid)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
