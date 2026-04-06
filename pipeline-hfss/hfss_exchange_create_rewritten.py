#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def map_material_type(src_type: str | None) -> str:
    lower = (src_type or "").lower()
    return lower if lower in {"dielectric","magnetic","conductor","lossy","other"} else "other"

def map_port_type(src_type: str | None) -> str:
    lower = (src_type or "").lower()
    if "wave" in lower:
        return "waveport"
    if "lump" in lower:
        return "lumped"
    if "gap" in lower:
        return "gap"
    if "terminal" in lower:
        return "terminal"
    return "other"

def map_boundary_type(src_type: str | None) -> str:
    lower = (src_type or "").lower()
    if "pec" in lower:
        return "PEC"
    if "pmc" in lower:
        return "PMC"
    if "radiation" in lower:
        return "radiation"
    if "pml" in lower:
        return "PML"
    if "symmetry" in lower:
        return "symmetry"
    return "other"

def build_exchange(decimated: dict[str, Any], source_stem: str, source_name: str) -> dict[str, Any]:
    solver_info = decimated.get("solverInfo", {})
    mesh_summary = decimated.get("meshSummary", {})
    material_summary = decimated.get("materialSummary", [])
    port_summary = decimated.get("portSummary", [])
    boundary_summary = decimated.get("boundaryConditionSummary", [])
    frequency_setup = decimated.get("frequencySetup", {})
    file_summary = decimated.get("fileSummary", {})

    materials = []
    for idx, mat in enumerate(material_summary, start=1):
        name = mat.get("name")
        materials.append({
            "id": name or f"material_{idx}",
            "type": map_material_type(mat.get("type")),
            "properties": {k: v for k, v in {
                "epsilonR": mat.get("epsilonR"),
                "muR": mat.get("muR"),
                "conductivity": mat.get("conductivity"),
                "lossTangent": mat.get("lossTangent"),
            }.items() if v is not None},
        })

    ports = []
    for idx, port in enumerate(port_summary, start=1):
        ports.append({
            "id": port.get("id") or f"port_{idx}",
            "type": map_port_type(port.get("type")),
            "location": port.get("location"),
            "impedance": port.get("impedance"),
        })

    boundaries = []
    for idx, bc in enumerate(boundary_summary, start=1):
        boundary_id = bc.get("id") or (bc.get("appliesTo") or [f"bc_{idx}"])[0]
        boundaries.append({
            "id": boundary_id,
            "type": map_boundary_type(bc.get("type")),
            "appliesTo": bc.get("appliesTo", []),
        })

    return {
        "simulationIdentity": {
            "name": source_stem,
            "identifier": f"SIM_{source_stem}",
            "description": "Electromagnetics simulation representation generated from HFSS extractor output.",
        },
        "solver": {
            "name": solver_info.get("solverName", "HFSS"),
            "version": solver_info.get("solverVersion", "unknown"),
            "method": solver_info.get("method", "FEM"),
        },
        "geometry": {"entities": []},
        "mesh": {} if mesh_summary is None else mesh_summary,
        "materials": materials,
        "ports": ports,
        "boundaryConditions": boundaries,
        "solverSettings": {
            "frequencyRange": {k: v for k, v in {
                "startHz": frequency_setup.get("startHz"),
                "stopHz": frequency_setup.get("stopHz"),
                "points": frequency_setup.get("points"),
            }.items() if v is not None},
            "convergenceCriteria": {},
        },
        "results": {"sParameters": [], "fieldPlots": []},
        "provenance": {
            "sourceFiles": file_summary.get("inputFiles", [source_name]),
            "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        },
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    decimated = json.loads(args.input_json.read_text(encoding="utf-8"))
    source_name = (decimated.get("fileSummary", {}).get("inputFiles") or ["unknown.hfss"])[0]
    source_stem = Path(source_name).stem
    result = build_exchange(decimated, source_stem, source_name)
    output_path = args.output or args.input_json.with_name(f"{source_stem}_exchange.json")
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(output_path)

if __name__ == "__main__":
    main()
