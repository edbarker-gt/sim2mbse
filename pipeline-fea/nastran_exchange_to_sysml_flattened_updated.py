#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import Any

def ident(text: str | None, default: str = "Unnamed") -> str:
    raw = text if text else default
    cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", raw)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    if not cleaned:
        cleaned = default
    if cleaned[0].isdigit():
        cleaned = f"N_{cleaned}"
    return cleaned

def q(text: Any) -> str:
    if text is None:
        return '""'
    return json.dumps(str(text))

def int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0

def flatten_source_files(source_files: list[Any]) -> str:
    if not source_files:
        return ""
    if len(source_files) == 1:
        return str(source_files[0])
    return ", ".join(str(x) for x in source_files)

def flatten_element_counts(counts: dict[str, Any]) -> str:
    if not counts:
        return ""
    parts = [f"{k}={counts[k]}" for k in sorted(counts.keys())]
    return ", ".join(parts)

def emit_sysml(exchange: dict[str, Any]) -> str:
    sim_id = exchange.get("simulationIdentity", {})
    provenance = exchange.get("provenance", {})
    solver = exchange.get("solver", {})
    bulk = exchange.get("bulkData", {})
    nodes = bulk.get("nodes", {})
    elements = bulk.get("elements", {})
    materials = bulk.get("materials", [])
    subcases = exchange.get("caseControl", {}).get("subcases", [])
    pkg = ident(sim_id.get("name"), "NastranModel")
    original_stem = sim_id.get("sourceFileStem") or provenance.get("sourceFileStem") or sim_id.get("name") or "presentationView"
    root_name = ident(original_stem, "presentationView")
    source_files_value = flatten_source_files(provenance.get("sourceFiles", []))
    element_counts_value = flatten_element_counts(elements.get("countsByType", {}))
    lines = []
    a = lines.append
    a(f"package {pkg} {{")
    a("  private import ScalarValues::*;")
    a("")
    a(f"  part {root_name} {{")
    a("")
    a("    part solverContext {")
    a(f"      attribute name : ScalarValues::String = {q(solver.get('name'))};")
    a(f"      attribute version : ScalarValues::String = {q(solver.get('version'))};")
    a(f"      attribute sol : ScalarValues::Integer = {int_or_zero(solver.get('sol'))};")
    a("    }")
    a("")
    a("    part structuralSummary {")
    a(f"      attribute nodeCount : ScalarValues::Integer = {int_or_zero(nodes.get('count'))};")
    a(f"      attribute elementCountsByType : ScalarValues::String = {q(element_counts_value)};")
    a("    }")
    a("")
    for material in materials:
        name = ident(f"material_{material.get('mid')}")
        a(f"    part {name} {{")
        a(f"      attribute mid : ScalarValues::Integer = {int_or_zero(material.get('mid'))};")
        a(f"      attribute type : ScalarValues::String = {q(material.get('type'))};")
        a("    }")
        a("")
    for subcase in subcases:
        name = ident(f"subcase_{subcase.get('id')}")
        a(f"    part {name} {{")
        a(f"      attribute id : ScalarValues::Integer = {int_or_zero(subcase.get('id'))};")
        a(f"      attribute label : ScalarValues::String = {q(subcase.get('label'))};")
        a(f"      attribute analysisType : ScalarValues::String = {q(subcase.get('analysisType'))};")
        a(f"      attribute spc : ScalarValues::String = {q(subcase.get('spc'))};")
        a(f"      attribute load : ScalarValues::String = {q(subcase.get('load'))};")
        a("    }")
        a("")
    a("    part provenance {")
    a(f"      attribute sourceFiles : ScalarValues::String = {q(source_files_value)};")
    a(f"      attribute timestamp : ScalarValues::String = {q(provenance.get('timestamp'))};")
    a("    }")
    a("")
    a("  }")
    a("}")
    return "\n".join(lines) + "\n"

def main() -> None:
    parser = argparse.ArgumentParser(description="Create flattened presentation-mode SysML v2 text from baseline exchange JSON.")
    parser.add_argument("input_json", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    exchange = json.loads(args.input_json.read_text(encoding="utf-8"))
    text = emit_sysml(exchange)
    sim_id = exchange.get("simulationIdentity", {})
    provenance = exchange.get("provenance", {})
    source_name = sim_id.get("sourceFileStem") or provenance.get("sourceFileStem") or sim_id.get("name") or args.input_json.stem.replace("_exchange", "")
    output_path = args.output or args.input_json.with_name(f"{source_name}_presentation.sysml")
    output_path.write_text(text, encoding="utf-8")
    print(output_path)

if __name__ == "__main__":
    main()
