#!/usr/bin/env python3
"""
HFSS exchange JSON -> SysML v2-style text (non-flattened).

Purpose
-------
Convert the normalized HFSS exchange JSON into a deterministic SysML v2-style
text file that preserves a formal MBSE structure with `part def` blocks and
typed `part : Type` usages.

This version avoids escaped JSON strings in visible SysML values by flattening
lists/dictionaries into readable strings before quoting them for SysML.

Default output naming:
    <source_aedt_stem>_model.sysml
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


def int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def flatten_list(values: list[Any]) -> str:
    if not values:
        return ""
    return ", ".join(str(v) for v in values if v is not None and str(v) != "")


def flatten_files(files: list[Any]) -> str:
    return flatten_list(files)


def flatten_names(items: list[dict[str, Any]], key: str = "name") -> str:
    return flatten_list([x.get(key) for x in items if isinstance(x, dict)])


def flatten_design_boundaries(boundaries: list[dict[str, Any]]) -> str:
    parts = []
    for b in boundaries:
        if not isinstance(b, dict):
            continue
        name = b.get("name")
        btype = b.get("BoundType")
        if name and btype:
            parts.append(f"{name} ({btype})")
        elif name:
            parts.append(str(name))
    return ", ".join(parts)


def flatten_design_excitations(excitations: list[dict[str, Any]]) -> str:
    parts = []
    for e in excitations:
        if not isinstance(e, dict):
            continue
        name = e.get("name")
        etype = e.get("type")
        imp = e.get("impedance")
        text = None
        if name and etype and imp:
            text = f"{name} ({etype}, {imp})"
        elif name and etype:
            text = f"{name} ({etype})"
        elif name:
            text = str(name)
        if text:
            parts.append(text)
    return ", ".join(parts)


def flatten_design_setups(setups: list[dict[str, Any]]) -> str:
    parts = []
    for s in setups:
        if not isinstance(s, dict):
            continue
        name = s.get("name")
        freq = s.get("Frequency")
        if name and freq:
            parts.append(f"{name} @ {freq}")
        elif name:
            parts.append(str(name))
    return ", ".join(parts)


def emit_sysml(exchange: dict[str, Any]) -> str:
    sim_id = exchange.get("simulationIdentity", {})
    solver = exchange.get("solver", {})
    designs = exchange.get("designs", [])
    materials = exchange.get("materials", [])
    provenance = exchange.get("provenance", {})

    pkg = ident(sim_id.get("name"), "HFSSModel")
    source_files_value = flatten_files(provenance.get("sourceFiles", []))

    lines: list[str] = []
    a = lines.append

    a(f"package {pkg} {{")
    a("")
    a("  doc /*")
    a("    Baseline deterministic SysML v2-style model generated from")
    a("    HFSS exchange JSON.")
    a("  */")
    a("")
    a("  part def SolverContext {")
    a("    attribute name : String;")
    a("    attribute family : String;")
    a("    attribute product : String;")
    a("    attribute designCount : Integer;")
    a("  }")
    a("")
    a("  part def DesignSummary {")
    a("    attribute designName : String;")
    a("    attribute solutionType : String;")
    a("    attribute globalMaterialEnvironment : String;")
    a("    attribute portImpedanceGlobal : String;")
    a("    attribute boundaryNames : String;")
    a("    attribute excitationNames : String;")
    a("    attribute setupNames : String;")
    a("  }")
    a("")
    a("  part def MaterialSummary {")
    a("    attribute name : String;")
    a("  }")
    a("")
    a("  part def ProvenanceRecord {")
    a("    attribute sourceFiles : String;")
    a("    attribute sourceFileName : String;")
    a("    attribute sourceFileStem : String;")
    a("    attribute timestamp : String;")
    a("  }")
    a("")
    a("  part solverContext : SolverContext {")
    a(f"    name = {q(solver.get('name'))};")
    a(f"    family = {q(solver.get('family'))};")
    a(f"    product = {q(solver.get('product'))};")
    a(f"    designCount = {int_or_zero(solver.get('designCount'))};")
    a("  }")
    a("")

    for idx, design in enumerate(designs, start=1):
        name = ident(design.get("designName"), f"design_{idx}")
        a(f"  part {name} : DesignSummary {{")
        a(f"    designName = {q(design.get('designName'))};")
        a(f"    solutionType = {q(design.get('solutionType'))};")
        a(f"    globalMaterialEnvironment = {q(design.get('globalMaterialEnvironment'))};")
        a(f"    portImpedanceGlobal = {q(design.get('portImpedanceGlobal'))};")
        a(f"    boundaryNames = {q(flatten_design_boundaries(design.get('boundaries', [])))};")
        a(f"    excitationNames = {q(flatten_design_excitations(design.get('excitations', [])))};")
        a(f"    setupNames = {q(flatten_design_setups(design.get('analysisSetups', [])))};")
        a("  }")
        a("")

    for idx, material in enumerate(materials, start=1):
        name = ident(material.get("name"), f"material_{idx}")
        a(f"  part {name} : MaterialSummary {{")
        a(f"    name = {q(material.get('name'))};")
        a("  }")
        a("")

    a("  part provenance : ProvenanceRecord {")
    a(f"    sourceFiles = {q(source_files_value)};")
    a(f"    sourceFileName = {q(provenance.get('sourceFileName'))};")
    a(f"    sourceFileStem = {q(provenance.get('sourceFileStem'))};")
    a(f"    timestamp = {q(provenance.get('timestamp'))};")
    a("  }")
    a("")
    a("}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Create SysML v2-style text from HFSS exchange JSON.")
    parser.add_argument("input_json", type=Path, help="Path to <source>_exchange.json")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output SysML path (default: <source_aedt_stem>_model.sysml)",
    )
    args = parser.parse_args()

    exchange = json.loads(args.input_json.read_text(encoding="utf-8"))
    text = emit_sysml(exchange)

    sim_id = exchange.get("simulationIdentity", {})
    source_name = sim_id.get("sourceFileStem") or sim_id.get("name") or args.input_json.stem.replace("_exchange", "")
    output_path = args.output or args.input_json.with_name(f"{source_name}_model.sysml")
    output_path.write_text(text, encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
