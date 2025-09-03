#!/usr/bin/env python3
"""
DOCX -> OSCAL SSP converter

Behavior (per user request):
1) Put Implementation (How) text ONLY into `statements[].remarks`.
2) Create `statements` ONLY IF:
   - Implementation text is non-empty, OR
   - an explicit Statements column exists with one or more IDs.
3) If both Implementation text is empty AND no statement IDs are provided, OMIT the `statements` array.
4) NEVER fall back to the control title for remarks or description.
5) DO NOT include UUIDs on statements by default. (Use --add-statement-uuids to include them.)

Usage:
  python word_ssp_to_oscal.py --in TAMUX_SSP_Populated.docx --out SSP_OSCAL.json \
      [--system-id SYS-123] [--system-name "My System"] [--add-statement-uuids]
"""
import argparse
import datetime as dt
import json
import sys
import uuid
from docx import Document

REQUIRED_FIRST_HEADER = "Control ID"
STATEMENT_HEADER_ALIASES = {
    "statement", "statements", "statement id", "statement ids",
    "statement id(s)", "statement(s)"
}

def canonicalize(text):
    return (text or "").strip().lower().replace("  ", " ")

def get_header_map(header_row):
    headers = [canonicalize(c.text) for c in header_row.cells]
    idx = {h: i for i, h in enumerate(headers)}

    def find_contains(keywords, required=False):
        for h, i in idx.items():
            for kw in keywords:
                if kw in h:
                    return i
        if required:
            raise RuntimeError(f"Required header containing {keywords} not found")
        return None

    # Required
    id_col = find_contains(["control id"], required=True)
    title_col = find_contains(["control title"], required=True)

    # Optional
    impl_col = find_contains(["implementation"], required=False)
    inherited_col = find_contains(["inherited?"], required=False)
    inherited_from_col = find_contains(["inherited from"], required=False)
    params_col = find_contains(["parameter", "odp"], required=False)
    roles_col = find_contains(["responsible role"], required=False)
    status_col = find_contains(["status"], required=False)
    evidence_col = find_contains(["evidence", "artifact"], required=False)
    comments_col = find_contains(["comment"], required=False)

    # Statement column (optional)
    statement_col = None
    for alias in STATEMENT_HEADER_ALIASES:
        for h, i in idx.items():
            if alias == h:
                statement_col = i
                break
        if statement_col is not None:
            break
    if statement_col is None:
        statement_col = find_contains(["statement"], required=False)

    return {
        "id": id_col, "title": title_col, "impl": impl_col,
        "inh": inherited_col, "inh_from": inherited_from_col,
        "params": params_col, "roles": roles_col, "status": status_col,
        "evidence": evidence_col, "comments": comments_col, "stmts": statement_col
    }

def cell_text(row_cells, idx):
    if idx is None:
        return ""
    return (row_cells[idx].text or "").strip()

def split_statement_ids(text):
    if not text:
        return []
    parts = []
    for chunk in text.replace("\\r", "\\n").split("\\n"):
        for piece in chunk.split(","):
            for sub in piece.split(";"):
                t = sub.strip()
                if t:
                    parts.append(t)
    # De-duplicate preserving order
    seen, unique = set(), []
    for p in parts:
        if p not in seen:
            unique.append(p); seen.add(p)
    return unique

def build_oscal_skeleton(sys_id, sys_name):
    now = dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    return {
        "system-security-plan": {
            "uuid": str(uuid.uuid4()),
            "metadata": {
                "title": f"System Security Plan – {sys_name or sys_id or 'Unnamed System'}",
                "last-modified": now,
                "version": "1.0",
                "oscal-version": "1.1.2",
                "props": [{"name": "generator", "value": "word_ssp_to_oscal.py"}]
            },
            "import-profile": {"href": ""},
            "system-characteristics": {
                "system-ids": [{"identifier": sys_id or str(uuid.uuid4())}],
                "system-name": sys_name or "Unnamed System",
                "status": {"state": "operational"},
                "system-information": {"information-types": []}
            },
            "control-implementation": {"implemented-requirements": []}
        }
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True, help="Input populated SSP DOCX")
    ap.add_argument("--out", dest="outp", required=True, help="Output OSCAL SSP path (.json)")
    ap.add_argument("--system-id", default="", help="System identifier to include in OSCAL")
    ap.add_argument("--system-name", default="", help="System name to include in OSCAL")
    ap.add_argument("--add-statement-uuids", action="store_true",
                    help="Include 'uuid' on each statement (off by default).")
    args = ap.parse_args()

    doc = Document(args.inp)
    control_tbl = None
    for tbl in doc.tables:
        if tbl.rows and tbl.rows[0].cells and REQUIRED_FIRST_HEADER.lower() in (tbl.rows[0].cells[0].text or "").lower():
            control_tbl = tbl; break
    if control_tbl is None:
        print("ERROR: Could not find Control Implementation table (first header cell should contain 'Control ID').", file=sys.stderr)
        sys.exit(2)

    hdr_map = get_header_map(control_tbl.rows[0])
    oscal = build_oscal_skeleton(args.system_id, args.system_name)

    for r in control_tbl.rows[1:]:
        cells = r.cells
        cid = cell_text(cells, hdr_map["id"])
        if not cid:
            continue  # skip rows without control id

        impl = cell_text(cells, hdr_map["impl"])
        inh_flag = cell_text(cells, hdr_map["inh"]).lower().startswith("y") if hdr_map["inh"] is not None else False
        inh_from = cell_text(cells, hdr_map["inh_from"])
        params = cell_text(cells, hdr_map["params"])
        roles = cell_text(cells, hdr_map["roles"])
        status = cell_text(cells, hdr_map["status"])
        evidence = cell_text(cells, hdr_map["evidence"])
        comments = cell_text(cells, hdr_map["comments"])
        stmts_raw = cell_text(cells, hdr_map["stmts"]) if hdr_map["stmts"] is not None else ""
        stmt_ids = split_statement_ids(stmts_raw)

        impl_req = {"uuid": str(uuid.uuid4()), "control-id": cid, "props": []}

        # Build statements only when there is content to preserve or IDs to respect
        build_statements = bool(impl) or bool(stmt_ids)
        if build_statements:
            if not stmt_ids:
                stmt_ids = [f"{cid}_impl"]
            impl_req["statements"] = []
            for sid in stmt_ids:
                stmt = {"statement-id": sid}
                if args.add_statement_uuids:
                    stmt["uuid"] = str(uuid.uuid4())
                if impl:  # only add remarks when we actually have implementation prose
                    stmt["remarks"] = impl
                impl_req["statements"].append(stmt)

        if params:
            impl_req.setdefault("set-parameters", []).append({"param-id": "custom", "values": [params]})
        if roles:
            impl_req.setdefault("responsible-roles", []).append({"role-id": "implementer", "remarks": roles})
        if status:
            impl_req["props"].append({"name": "status", "value": status})
        if evidence:
            impl_req.setdefault("by-components", []).append({
                "component-uuid": str(uuid.uuid4()),
                "description": "Evidence reference",
                "props": [{"name": "evidence", "value": evidence}]
            })
        if inh_flag:
            impl_req["props"].append({"name": "inherited", "value": "true"})
            if inh_from:
                impl_req["props"].append({"name": "inherited-from", "value": inh_from})
        if comments:
            impl_req["remarks"] = comments

        oscal["system-security-plan"]["control-implementation"]["implemented-requirements"].append(impl_req)

    with open(args.outp, "w", encoding="utf-8") as f:
        json.dump(oscal, f, indent=2)
    print(f"Wrote OSCAL SSP to: {args.outp}")

if __name__ == "__main__":
    main()
