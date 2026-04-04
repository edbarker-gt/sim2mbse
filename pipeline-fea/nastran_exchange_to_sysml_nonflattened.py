#!/usr/bin/env python3
"""
Baseline exchange JSON -> SysML v2-style text.

Purpose
-------
Convert the baseline exchange JSON into a deterministic SysML v2-style text
file for MBSE-facing review and downstream adaptation.

This version remains NON-FLATTENED:
- keeps `part def` blocks
- keeps typed `part ... : TypeName` usages

Applied fixes
-------------
- `elementCountsByType` is rendered as a readable string like `CQUAD4=10`
  instead of escaped JSON like `"{\"CQUAD4\": 10}"`.
- `sourceFiles` is rendered as a readable string like `test.bdf`
  instead of `["test.bdf"]`.

Default output naming:
    <source_bdf_stem>_model.sysml
"""

from __future__ import annotations

import argparse
import json
import re
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
    solver = exchange.get("solver", {})
    bulk = exchange.get("bulkData", {})
    nodes = bulk.get("nodes", {})
    elements = bulk.get("elements", {})
    materials = bulk.get("materials", [])
    subcases = exchange.get("caseControl", {}).get("subcases", [])
    provenance = exchange.get("provenance", {})

    pkg = ident(sim_id.get("name"), "NastranModel")
    element_counts_value = flatten_element_counts(elements.get("countsByType", {}))
    source_files_value = flatten_source_files(provenance.get("sourceFiles", []))

    lines: list[str] = []
    a = lines.append

    a(f"package {pkg} {{")
    a("")
    a("  doc /*")
    a("    Baseline deterministic SysML v2-style model generated from")
    a("    Nastran exchange JSON.")
    a("  */")
    a("")
    a("  part def SolverContext {")
    a("    attribute name : String;")
    a("    attribute version : String;")
    a("    attribute sol : Integer;")
    a("  }")
    a("")
    a("  part def StructuralSummary {")
    a("    attribute nodeCount : Integer;")
    a("    attribute elementCountsByType : String;")
    a("  }")
    a("")
    a("  part def MaterialSummary {")
    a("    attribute mid : Integer;")
    a("    attribute type : String;")
    a("  }")
    a("")
    a("  part def AnalysisCase {")
    a("    attribute id : Integer;")
    a("    attribute label : String;")
    a("    attribute analysisType : String;")
    a("    attribute spc : String;")
    a("    attribute load : String;")
    a("  }")
    a("")
    a("  part def ProvenanceRecord {")
    a("    attribute sourceFiles : String;")
    a("    attribute timestamp : String;")
    a("  }")
    a("")
    a("  part solverContext : SolverContext {")
    a(f"    name = {q(solver.get('name'))};")
    a(f"    version = {q(solver.get('version'))};")
    a(f"    sol = {int(solver.get('sol') or 0)};")
    a("  }")
    a("")
    a("  part structuralSummary : StructuralSummary {")
    a(f"    nodeCount = {int(nodes.get('count') or 0)};")
    a(f"    elementCountsByType = {q(element_counts_value)};")
    a("  }")
    a("")

    for material in materials:
        name = ident(f"material_{material.get('mid')}")
        a(f"  part {name} : MaterialSummary {{")
        a(f"    mid = {int(material.get('mid') or 0)};")
        a(f"    type = {q(material.get('type'))};")
        a("  }")
        a("")

    for subcase in subcases:
        name = ident(f"subcase_{subcase.get('id')}")
        a(f"  part {name} : AnalysisCase {{")
        a(f"    id = {int(subcase.get('id') or 0)};")
        a(f"    label = {q(subcase.get('label'))};")
        a(f"    analysisType = {q(subcase.get('analysisType'))};")
        a(f"    spc = {q(subcase.get('spc'))};")
        a(f"    load = {q(subcase.get('load'))};")
        a("  }")
        a("")

    a("  part provenance : ProvenanceRecord {")
    a(f"    sourceFiles = {q(source_files_value)};")
    a(f"    timestamp = {q(provenance.get('timestamp'))};")
    a("  }")
    a("")
    a("}")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Create SysML v2-style text from baseline exchange JSON.")
    parser.add_argument("input_json", type=Path, help="Path to <source>_exchange.json")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output SysML path (default: <source_bdf_stem>_model.sysml)",
    )
    args = parser.parse_args()

    exchange = json.loads(args.input_json.read_text(encoding="utf-8"))
    text = emit_sysml(exchange)

    source_name = exchange.get("simulationIdentity", {}).get("name") or args.input_json.stem.replace("_exchange", "")
    output_path = args.output or args.input_json.with_name(f"{source_name}_model.sysml")
    output_path.write_text(text, encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
