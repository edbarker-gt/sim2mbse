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
    return '""' if text is None else json.dumps(str(text))

def flatten_applies(items: list[Any]) -> str:
    return ", ".join(str(x) for x in items if x is not None and str(x) != "")

def flatten_frequency(freq: dict[str, Any]) -> str:
    if not isinstance(freq, dict):
        return ""
    parts = []
    if freq.get("startHz") is not None:
        parts.append(f"startHz={freq['startHz']}")
    if freq.get("stopHz") is not None:
        parts.append(f"stopHz={freq['stopHz']}")
    if freq.get("points") is not None:
        parts.append(f"points={freq['points']}")
    return ", ".join(parts)

def flatten_material_props(props: dict[str, Any]) -> str:
    if not isinstance(props, dict):
        return ""
    return ", ".join(f"{k}={v}" for k, v in props.items())

def emit_sysml(exchange: dict[str, Any]) -> str:
    sim_id = exchange.get("simulationIdentity", {})
    solver = exchange.get("solver", {})
    materials = exchange.get("materials", [])
    ports = exchange.get("ports", [])
    bcs = exchange.get("boundaryConditions", [])
    settings = exchange.get("solverSettings", {})
    provenance = exchange.get("provenance", {})
    pkg = ident(sim_id.get("name"), "HFSSModel")
    root_name = ident(sim_id.get("name"), "presentationView")
    lines = []
    a = lines.append
    a(f"package {pkg} {{")
    a("  private import ScalarValues::*;")
    a("  private import ISQ::*;")
    a("  private import SI::*;")
    a("")
    a("  doc /*")
    a("    Flattened presentation-mode SysML v2-style model generated from")
    a("    Electromagnetics simulation JSON.")
    a("  */")
    a("")
    a(f"  part {root_name} {{")
    a("")
    a("    part solverContext {")
    a(f"      attribute name : ScalarValues::String = {q(solver.get('name'))};")
    a(f"      attribute version : ScalarValues::String = {q(solver.get('version'))};")
    a(f"      attribute method : ScalarValues::String = {q(solver.get('method'))};")
    a(f"      attribute frequencyRange : ScalarValues::String = {q(flatten_frequency(settings.get('frequencyRange', {})))};")
    a("    }")
    a("")
    for idx, mat in enumerate(materials, start=1):
        name = ident(mat.get("id"), f"material_{idx}")
        a(f"    part {name} {{")
        a(f"      attribute id : ScalarValues::String = {q(mat.get('id'))};")
        a(f"      attribute type : ScalarValues::String = {q(mat.get('type'))};")
        a(f"      attribute properties : ScalarValues::String = {q(flatten_material_props(mat.get('properties', {})))};")
        a("    }")
        a("")
    for idx, port in enumerate(ports, start=1):
        name = ident(port.get("id"), f"port_{idx}")
        a(f"    part {name} {{")
        a(f"      attribute id : ScalarValues::String = {q(port.get('id'))};")
        a(f"      attribute type : ScalarValues::String = {q(port.get('type'))};")
        a(f"      attribute location : ScalarValues::String = {q(port.get('location'))};")
        a(f"      attribute impedance : ScalarValues::String = {q(port.get('impedance'))};")
        a("    }")
        a("")
    for idx, bc in enumerate(bcs, start=1):
        name = ident(bc.get("id"), f"boundary_{idx}")
        a(f"    part {name} {{")
        a(f"      attribute id : ScalarValues::String = {q(bc.get('id'))};")
        a(f"      attribute type : ScalarValues::String = {q(bc.get('type'))};")
        a(f"      attribute appliesTo : ScalarValues::String = {q(flatten_applies(bc.get('appliesTo', [])))};")
        a("    }")
        a("")
    a("    part provenance {")
    a(f"      attribute sourceFiles : ScalarValues::String = {q(flatten_applies(provenance.get('sourceFiles', [])))};")
    a(f"      attribute timestamp : ScalarValues::String = {q(provenance.get('timestamp'))};")
    a("    }")
    a("")
    a("  }")
    a("}")
    return "\n".join(lines) + "\n"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    exchange = json.loads(args.input_json.read_text(encoding="utf-8"))
    text = emit_sysml(exchange)
    source_name = exchange.get("simulationIdentity", {}).get("name") or args.input_json.stem.replace("_exchange", "")
    output_path = args.output or args.input_json.with_name(f"{source_name}_presentation.sysml")
    output_path.write_text(text, encoding="utf-8")
    print(output_path)

if __name__ == "__main__":
    main()
