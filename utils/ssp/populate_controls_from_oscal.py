#!/usr/bin/env python3
"""
Populate the Control Implementation table in an SSP DOCX from an OSCAL Catalog (YAML or JSON).

Usage:
  python populate_controls_from_oscal.py --source <path-or-url-to-oscal-catalog> \
      --template tamus-ssp-template.docx --out SSP_Populated.docx

Notes:
- Requires: python-docx, pyyaml (if YAML), requests (for URL sources).
- Extracts control id + title from each control in groups[].controls[].
- Filters to controls that appear in the catalog (i.e., the "required" set you provided).
- Leaves implementation-related fields blank for you to complete.
"""
import argparse
import io
import json
import re
import sys

from docx import Document

def load_text_from_source(source):
    if re.match(r'^https?://', source):
        try:
            import requests
        except Exception as e:
            print("ERROR: 'requests' is required to load from URL. Install with: pip install requests", file=sys.stderr)
            sys.exit(1)
        resp = requests.get(source, timeout=30)
        resp.raise_for_status()
        return resp.text
    else:
        with open(source, 'r', encoding='utf-8') as f:
            return f.read()

def parse_controls(text):
    # Try YAML first if available
    try:
        import yaml
        data = yaml.safe_load(text)
        # OSCAL catalog at root key 'catalog' with 'groups' -> each has 'controls'
        catalog = data.get('catalog', {})
        groups = catalog.get('groups', [])
        controls = []
        for g in groups:
            fam_title = g.get('title', '') or g.get('id', '')
            for c in g.get('controls', []) or []:
                cid = c.get('id', '').upper()
                ctitle = c.get('title', '').strip()
                if cid and ctitle:
                    controls.append((cid, ctitle, fam_title))
        if controls:
            return controls
    except Exception:
        pass

    # Fallback regex parse for lines like: "- id: ac-3 class: SP800-53 title: Access Enforcement"
    controls = []
    current_family = None
    for line in text.splitlines():
        # Try to detect family header lines like: "groups: - id: ac class: family title: Access Control"
        m_fam = re.search(r'\bid:\s*([a-z]{2,3})\b.*?\bclass:\s*family\b.*?\btitle:\s*([^\n]+)', line)
        if m_fam:
            current_family = m_fam.group(2).strip()
        m = re.search(r'-\s*id:\s*([a-z0-9\-\.\(\)]+)\s+class:\s*SP800-53\s+title:\s*([^;]+)', line, re.IGNORECASE)
        if m:
            cid = m.group(1).upper()
            ctitle = m.group(2).strip()
            controls.append((cid, ctitle, current_family or ""))
    return controls

def find_control_table(doc):
    # Find the table with the header cell "Control ID"
    for tbl in doc.tables:
        if tbl.rows and tbl.rows[0].cells and "Control ID" in tbl.rows[0].cells[0].text:
            return tbl
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="Path or URL to the OSCAL catalog (YAML or JSON)")
    ap.add_argument("--template", required=True, help="Path to the SSP DOCX template to populate")
    ap.add_argument("--out", required=True, help="Output DOCX path")
    args = ap.parse_args()

    text = load_text_from_source(args.source)
    controls = parse_controls(text)
    if not controls:
        print("No controls parsed from source. Verify the file.", file=sys.stderr)
        sys.exit(2)

    doc = Document(args.template)
    tbl = find_control_table(doc)
    if tbl is None:
        print("Could not find the Control table (header 'Control ID').", file=sys.stderr)
        sys.exit(3)

    # Append controls as rows
    for cid, title, fam in controls:
        row = tbl.add_row().cells
        row[0].text = cid
        row[1].text = title
        row[2].text = ""     # Implementation (How)
        row[3].text = ""     # Inherited? (Y/N)
        row[4].text = ""     # Inherited From
        row[5].text = ""     # Parameters / ODPs
        row[6].text = ""     # Responsible Role(s)
        row[7].text = ""     # Status
        row[8].text = ""     # Evidence / Artifacts
        row[9].text = ""     # Comments

    doc.save(args.out)
    print(f"Wrote populated SSP to: {args.out}  (controls added: {len(controls)})")

if __name__ == "__main__":
    main()
