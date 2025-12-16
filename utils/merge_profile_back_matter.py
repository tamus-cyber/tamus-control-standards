#!/usr/bin/env python3
"""
merge_profile_back_matter.py

Post-process an OSCAL resolved catalog by merging back-matter resources from
a source OSCAL profile into the resolved catalog's back-matter.

Primary use: oscal-cli profile resolve drops profile-level back-matter/resources.

What it does:
- Reads PROFILE (YAML/JSON) expecting: profile.back-matter.resources[*].uuid
- Reads RESOLVED CATALOG (YAML/JSON) expecting: catalog.back-matter.resources[*].uuid
- Merges resources by UUID (resolved wins on conflicts by default)
- Writes updated resolved catalog (YAML by default; JSON optional)

Usage:
  python merge_profile_back_matter.py TAMUS_profile.yaml TMAUS_resolved-profile_catalog.yaml -o fixed.yaml
  python merge_profile_back_matter.py TAMUS_profile.yaml resolved.json -o fixed.json --out-format json
  python merge_profile_back_matter.py TAMUS_profile.yaml resolved.yaml --inplace

Notes:
- Only merges back-matter.resources. (Easy to extend if you want rlinks, citations, etc.)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

def _load(path: str) -> Dict[str, Any]:
    ext = os.path.splitext(path.lower())[1]
    with open(path, "r", encoding="utf-8") as f:
        if ext in (".yaml", ".yml"):
            try:
                import yaml  # type: ignore
            except ImportError as e:
                raise SystemExit("PyYAML is required for YAML. Install: pip install pyyaml") from e
            obj = yaml.safe_load(f)
        else:
            obj = json.load(f)
    if not isinstance(obj, dict):
        raise SystemExit(f"{path}: expected a top-level object")
    return obj

def _dump_yaml(obj: Dict[str, Any]) -> str:
    try:
        import yaml  # type: ignore
    except ImportError as e:
        raise SystemExit("PyYAML is required for YAML output. Install: pip install pyyaml") from e
    # keep output stable-ish
    return yaml.safe_dump(obj, sort_keys=False, allow_unicode=True)

def _dump_json(obj: Dict[str, Any]) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"

def _ensure_dict(d: Any) -> Dict[str, Any]:
    return d if isinstance(d, dict) else {}

def _ensure_list(x: Any) -> List[Any]:
    return x if isinstance(x, list) else ([] if x is None else [x])

def _get_profile_resources(profile_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    profile = _ensure_dict(profile_doc.get("profile", profile_doc))
    back_matter = _ensure_dict(profile.get("back-matter"))
    resources = _ensure_list(back_matter.get("resources"))
    out: List[Dict[str, Any]] = []
    for r in resources:
        if isinstance(r, dict) and r.get("uuid"):
            out.append(r)
    return out

def _get_catalog_resources(resolved_doc: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Returns (catalog_obj_ref, resources_list_ref).
    Mutates resolved_doc to ensure catalog/back-matter/resources exists.
    """
    catalog = resolved_doc.get("catalog")
    if not isinstance(catalog, dict):
        # Sometimes users give a catalog object directly; normalize to dict wrapper
        if any(k in resolved_doc for k in ("metadata", "groups", "controls", "back-matter")):
            # treat the whole object as a catalog
            resolved_doc = {"catalog": resolved_doc}
            catalog = resolved_doc["catalog"]
        else:
            resolved_doc["catalog"] = {}
            catalog = resolved_doc["catalog"]

    back_matter = catalog.get("back-matter")
    if not isinstance(back_matter, dict):
        back_matter = {}
        catalog["back-matter"] = back_matter

    resources = back_matter.get("resources")
    if not isinstance(resources, list):
        resources = []
        back_matter["resources"] = resources

    # Return references (catalog dict, resources list)
    return catalog, resources  # type: ignore[return-value]

def merge_resources(
    profile_resources: List[Dict[str, Any]],
    catalog_resources: List[Dict[str, Any]],
    *,
    prefer: str = "catalog",
) -> Tuple[List[Dict[str, Any]], int, int, int]:
    """
    prefer:
      - 'catalog' => keep existing catalog resource on UUID collision
      - 'profile' => overwrite catalog resource on UUID collision with profile resource
      - 'merge'   => shallow-merge dicts (catalog fields preserved unless missing)

    Returns (merged_list, added_count, updated_count, skipped_count)
    """
    prefer = prefer.lower()
    if prefer not in ("catalog", "profile", "merge"):
        raise ValueError("prefer must be one of: catalog, profile, merge")

    by_uuid: Dict[str, Dict[str, Any]] = {}
    order: List[str] = []

    def add_existing(r: Dict[str, Any]) -> None:
        u = str(r.get("uuid")).strip().lower()
        if not u:
            return
        if u not in by_uuid:
            by_uuid[u] = r
            order.append(u)

    for r in catalog_resources:
        if isinstance(r, dict) and r.get("uuid"):
            add_existing(r)

    added = updated = skipped = 0

    for pr in profile_resources:
        if not isinstance(pr, dict) or not pr.get("uuid"):
            continue
        u = str(pr.get("uuid")).strip().lower()
        if not u:
            continue

        if u not in by_uuid:
            by_uuid[u] = pr
            order.append(u)
            added += 1
            continue

        # collision
        if prefer == "catalog":
            skipped += 1
        elif prefer == "profile":
            by_uuid[u] = pr
            updated += 1
        else:  # merge
            cr = by_uuid[u]
            # shallow merge: keep catalog values, fill missing from profile
            merged = dict(pr)
            merged.update(cr)  # catalog overwrites profile on key conflict
            by_uuid[u] = merged
            updated += 1

    merged_list = [by_uuid[u] for u in order]
    return merged_list, added, updated, skipped

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("profile_path", help="OSCAL profile (YAML/JSON) containing back-matter.resources")
    ap.add_argument("resolved_catalog_path", help="Resolved OSCAL catalog (YAML/JSON) to patch")
    ap.add_argument("-o", "--output", help="Output path (default: stdout unless --inplace)")
    ap.add_argument("--inplace", action="store_true", help="Overwrite resolved catalog file in-place")
    ap.add_argument("--prefer", choices=["catalog", "profile", "merge"], default="catalog",
                    help="Collision behavior when same UUID exists in both (default: catalog)")
    ap.add_argument("--out-format", choices=["yaml", "json"], default="yaml",
                    help="Output format (default: yaml)")
    args = ap.parse_args()

    if args.inplace and args.output:
        raise SystemExit("Use either --inplace or -o/--output, not both.")

    profile_doc = _load(args.profile_path)
    resolved_doc = _load(args.resolved_catalog_path)

    profile_resources = _get_profile_resources(profile_doc)
    if not profile_resources:
        raise SystemExit("No profile back-matter.resources found (profile.back-matter.resources).")

    _catalog_obj, catalog_resources = _get_catalog_resources(resolved_doc)

    merged, added, updated, skipped = merge_resources(
        profile_resources, catalog_resources, prefer=args.prefer
    )

    # Replace catalog resources list contents (preserve same list object if possible)
    catalog_resources[:] = merged

    out_text = _dump_yaml(resolved_doc) if args.out_format == "yaml" else _dump_json(resolved_doc)

    if args.inplace:
        with open(args.resolved_catalog_path, "w", encoding="utf-8") as f:
            f.write(out_text)
        sys.stderr.write(
            f"OK: merged back-matter.resources. added={added}, updated={updated}, skipped={skipped}\n"
        )
        return 0

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out_text)
        sys.stderr.write(
            f"OK: wrote {args.output}. added={added}, updated={updated}, skipped={skipped}\n"
        )
        return 0

    # stdout
    sys.stderr.write(
        f"OK: merged back-matter.resources. added={added}, updated={updated}, skipped={skipped}\n"
    )
    sys.stdout.write(out_text)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
