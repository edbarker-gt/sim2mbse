#!/usr/bin/env python3
"""
Baseline decimated JSON -> exchange/simulation JSON.

Purpose
-------
Transform the baseline extraction-contract JSON into a fuller simulation /
exchange JSON aligned to the baseline Nastran Simulation Schema.

This version carries the original input filename and stem forward so the
downstream SysML emitter can label the top-level presentation part with the
original source filename stem rather than a derived suffix name.

Default output naming:
    <source_bdf_stem>_exchange.json
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def infer_solver_name() -> str:
    return "NASTRAN"


def infer_solver_version() -> str:
    return "unknown"


def build_exchange(decimated: dict[str, Any]) -> dict[str, Any]:
    file_summary = decimated.get("fileSummary", {})
    input_files = file_summary.get("inputFiles", [])
    source_name = file_summary.get("sourceFileName") or (input_files[0] if input_files else "unknown.bdf")
    source_stem = file_summary.get("sourceFileStem") or Path(source_name).stem

    return {
        "simulationIdentity": {
            "name": source_stem,
            "identifier": f"SIM_{source_stem}",
            "description": "Baseline Nastran simulation/exchange representation generated from decimated extraction JSON.",
            "sourceFileName": source_name,
            "sourceFileStem": source_stem,
        },
        "solver": {
            "name": infer_solver_name(),
            "version": infer_solver_version(),
            "sol": decimated.get("executiveControl", {}).get("sol"),
        },
        "files": {
            "inputDecks": [
                {
                    "path": file_name,
                    "role": "primary_input_deck",
                }
                for file_name in input_files
            ],
            "outputFiles": [
                {
                    "path": file_name,
                    "type": "unknown",
                }
                for file_name in file_summary.get("outputFiles", [])
            ],
        },
        "executiveControl": decimated.get("executiveControl", {}),
        "caseControl": {
            "subcases": [
                {
                    "id": subcase.get("id"),
                    "label": f"SUBCASE_{subcase.get('id')}" if subcase.get("id") is not None else "SUBCASE",
                    "analysisType": subcase.get("analysisType"),
                    "spc": subcase.get("spc"),
                    "load": subcase.get("load"),
                    "outputRequests": [],
                }
                for subcase in decimated.get("caseControl", {}).get("subcases", [])
            ]
        },
        "bulkData": {
            "nodes": {
                "count": decimated.get("bulkDataSummary", {}).get("nodeCount", 0),
            },
            "elements": {
                "countsByType": decimated.get("bulkDataSummary", {}).get("elementCountsByType", {}),
            },
            "materials": decimated.get("bulkDataSummary", {}).get("materials", []),
            "properties": [],
        },
        "results": {
            "resultSets": [],
        },
        "provenance": {
            "sourceFiles": input_files,
            "sourceFileName": source_name,
            "sourceFileStem": source_stem,
            "tool": {
                "name": "nastran_exchange_layer_baseline.py",
                "version": "1.1",
            },
            "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build baseline exchange JSON from baseline decimated JSON.")
    parser.add_argument("input_json", type=Path, help="Path to <source>_decimated.json")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output JSON path (default: <source_bdf_stem>_exchange.json)",
    )
    args = parser.parse_args()

    decimated = json.loads(args.input_json.read_text(encoding="utf-8"))
    result = build_exchange(decimated)

    file_summary = decimated.get("fileSummary", {})
    input_files = file_summary.get("inputFiles", [])
    source_stem = file_summary.get("sourceFileStem") or (Path(input_files[0]).stem if input_files else args.input_json.stem.replace("_decimated", ""))
    output_path = args.output or args.input_json.with_name(f"{source_stem}_exchange.json")

    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
