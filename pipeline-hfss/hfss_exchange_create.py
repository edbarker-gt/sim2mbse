#!/usr/bin/env python3
"""
HFSS decimated JSON -> exchange / simulation JSON.

Purpose
-------
Transform the decimated HFSS JSON into a normalized exchange-layer JSON
suitable for downstream SysML v2 generation.

This script mirrors the architectural role used in the Nastran pipeline:
it takes extracted/decimated domain facts and promotes them into a more
canonical, solver-agnostic system-of-record representation.

Default output naming:
    <source_aedt_stem>_exchange.json
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def infer_solver_name() -> str:
    return "HFSS"


def infer_solver_family() -> str:
    return "Electromagnetics"


def flatten_materials(material_summary: dict[str, Any]) -> list[dict[str, Any]]:
    names = material_summary.get("names", []) if isinstance(material_summary, dict) else []
    return [{"name": name} for name in names]


def normalize_designs(design_summary: dict[str, Any]) -> list[dict[str, Any]]:
    designs = design_summary.get("designs", []) if isinstance(design_summary, dict) else []
    normalized: list[dict[str, Any]] = []

    for design in designs:
        normalized.append({
            "designName": design.get("designName"),
            "solutionType": design.get("solutionType"),
            "globalMaterialEnvironment": design.get("globalMaterialEnvironment"),
            "portImpedanceGlobal": design.get("portImpedanceGlobal"),
            "boundaries": design.get("boundaries", []),
            "excitations": design.get("excitations", []),
            "analysisSetups": design.get("analysisSetups", []),
        })

    return normalized


def build_exchange(decimated: dict[str, Any]) -> dict[str, Any]:
    project_identity = decimated.get("projectIdentity", {})
    solver_context = decimated.get("solverContext", {})
    design_summary = decimated.get("designSummary", {})
    material_summary = decimated.get("materialSummary", {})
    file_summary = decimated.get("fileSummary", {})

    source_name = project_identity.get("sourceFileName") or "unknown.aedt"
    source_stem = project_identity.get("sourceFileStem") or Path(source_name).stem
    product = project_identity.get("product") or solver_context.get("product")

    designs = normalize_designs(design_summary)
    materials = flatten_materials(material_summary)

    exchange = {
        "simulationIdentity": {
            "name": source_stem,
            "identifier": f"SIM_{source_stem}",
            "description": "Baseline HFSS exchange representation generated from decimated AEDT JSON.",
            "sourceFileName": source_name,
            "sourceFileStem": source_stem,
            "projectFormat": project_identity.get("projectFormat"),
            "created": project_identity.get("created"),
        },
        "solver": {
            "name": infer_solver_name(),
            "family": infer_solver_family(),
            "product": product,
            "designCount": solver_context.get("designCount", len(designs)),
        },
        "files": {
            "inputProjects": [
                {
                    "path": file_name,
                    "role": "primary_input_project",
                }
                for file_name in file_summary.get("inputFiles", [])
            ],
            "outputFiles": [
                {
                    "path": file_name,
                    "type": "unknown",
                }
                for file_name in file_summary.get("outputFiles", [])
            ],
        },
        "designs": designs,
        "materials": materials,
        "results": {
            "resultSets": []
        },
        "provenance": {
            "sourceFiles": file_summary.get("inputFiles", []),
            "sourceFileName": source_name,
            "sourceFileStem": source_stem,
            "tool": {
                "name": "hfss_exchange_create.py",
                "version": "1.0",
            },
            "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        },
    }

    return exchange


def main() -> None:
    parser = argparse.ArgumentParser(description="Build HFSS exchange JSON from decimated HFSS JSON.")
    parser.add_argument("input_json", type=Path, help="Path to <source>_decimated.json")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output JSON path (default: <source_aedt_stem>_exchange.json)",
    )
    args = parser.parse_args()

    decimated = json.loads(args.input_json.read_text(encoding="utf-8"))
    result = build_exchange(decimated)

    project_identity = decimated.get("projectIdentity", {})
    source_stem = project_identity.get("sourceFileStem") or args.input_json.stem.replace("_decimated", "")
    output_path = args.output or args.input_json.with_name(f"{source_stem}_exchange.json")

    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
