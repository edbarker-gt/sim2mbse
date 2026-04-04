#!/usr/bin/env python3
"""
Baseline-contract Nastran BDF -> decimated JSON extractor.

Purpose
-------
Read a Nastran .bdf/.dat file and emit a compact JSON document aligned to the
baseline Nastran Extraction Schema:

- executiveControl
- caseControl
- bulkDataSummary
- fileSummary

This version also preserves the original input filename and stem from the very
beginning of the pipeline so downstream stages can use the original source name
for labels and top-level presentation blocks.

Default output naming:
    <source_bdf_stem>_decimated.json
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

COMMENT_RE = re.compile(r"\$.*$")

ELEMENT_CARDS = {
    "CBAR", "CBEAM", "CBUSH", "CROD", "CONROD", "CELAS1", "CELAS2",
    "CELAS3", "CELAS4", "CQUAD4", "CQUAD8", "CTRIA3", "CTRIA6",
    "CHEXA", "CPENTA", "CTETRA", "CSHEAR",
}

RESULT_REQUEST_KEYS = {
    "DISPLACEMENT", "DISP", "STRESS", "STRAIN", "FORCE", "SPCFORCES",
    "GPFORCE", "ACCELERATION", "ACCEL", "VELOCITY", "ESE", "OLOAD",
}


def strip_comment(line: str) -> str:
    return COMMENT_RE.sub("", line).rstrip()


def merge_continuation_lines(lines: list[str]) -> list[str]:
    merged: list[str] = []
    current = ""

    for raw in lines:
        line = strip_comment(raw)
        if not line.strip():
            continue

        first = line[:8].strip()
        if first in {"+", "*"} or line.startswith("+") or line.startswith("*"):
            current += " " + (line[8:].strip() if len(line) > 8 else "")
            continue

        if current:
            merged.append(current)
        current = line

    if current:
        merged.append(current)

    return merged


def split_fields(line: str) -> list[str]:
    stripped = line.strip()

    if "," in stripped:
        return [f.strip() for f in stripped.split(",")]

    whitespace_fields = stripped.split()
    if len(whitespace_fields) > 1 and len(stripped) < 16:
        return whitespace_fields

    return [line[i:i + 8].strip() for i in range(0, len(line), 8) if line[i:i + 8].strip()]


def to_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(float(value.replace("D", "E")))
    except Exception:
        return None


def infer_analysis_type(sol: int | None) -> str | None:
    mapping = {
        101: "LinearStatic",
        103: "NormalModes",
        105: "Buckling",
        106: "NonlinearStatic",
        108: "DirectFrequencyResponse",
        111: "ModalFrequencyResponse",
        112: "DirectTransientResponse",
        129: "NonlinearTransient",
        144: "StaticAeroelasticity",
        145: "Flutter",
        146: "DynamicAeroelasticity",
        153: "HeatTransfer",
    }
    return mapping.get(sol)


def parse_bdf(input_path: Path) -> dict[str, Any]:
    logical_lines = merge_continuation_lines(
        input_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    )

    executive_control: dict[str, Any] = {
        "sol": None,
        "cendPresent": False,
        "otherCards": [],
    }
    case_control: dict[str, Any] = {"subcases": []}
    bulk_data_summary: dict[str, Any] = {
        "nodeCount": 0,
        "elementCountsByType": {},
        "materials": [],
    }
    file_summary: dict[str, Any] = {
        "inputFiles": [input_path.name],
        "outputFiles": [],
        "sourceFileName": input_path.name,
        "sourceFileStem": input_path.stem,
    }

    section = "executive"
    current_subcase: dict[str, Any] | None = None
    element_counts: Counter[str] = Counter()
    materials_seen: set[tuple[int | None, str]] = set()

    for line in logical_lines:
        uline = line.strip().upper()

        if uline == "CEND":
            executive_control["cendPresent"] = True
            section = "case"
            continue

        if uline == "BEGIN BULK":
            section = "bulk"
            continue

        if uline == "ENDDATA":
            break

        fields = split_fields(line)
        if not fields:
            continue

        card = fields[0].upper()

        if section == "executive":
            if card == "SOL" and len(fields) > 1:
                executive_control["sol"] = to_int(fields[1])
            elif card not in {"ID", "SOL"}:
                executive_control["otherCards"].append(" ".join(fields))
            continue

        if section == "case":
            if card == "SUBCASE" and len(fields) > 1:
                subcase_id = to_int(fields[1])
                current_subcase = {
                    "id": subcase_id,
                    "analysisType": infer_analysis_type(executive_control["sol"]),
                    "spc": None,
                    "load": None,
                }
                case_control["subcases"].append(current_subcase)
                continue

            if "=" in line:
                key, raw_value = [x.strip() for x in line.split("=", 1)]
                key_u = key.upper()
                value = raw_value

                if current_subcase is not None:
                    if key_u == "SPC":
                        current_subcase["spc"] = value
                    elif key_u in {"LOAD", "DLOAD"}:
                        current_subcase["load"] = value
                    elif key_u in RESULT_REQUEST_KEYS:
                        pass
                continue

            continue

        if card == "GRID":
            bulk_data_summary["nodeCount"] += 1
            continue

        if card in ELEMENT_CARDS:
            element_counts[card] += 1
            continue

        if card == "MAT1":
            mid = to_int(fields[1]) if len(fields) > 1 else None
            material_key = (mid, "MAT1")
            if material_key not in materials_seen:
                bulk_data_summary["materials"].append({
                    "mid": mid,
                    "type": "MAT1",
                })
                materials_seen.add(material_key)
            continue

    bulk_data_summary["elementCountsByType"] = dict(sorted(element_counts.items()))

    return {
        "executiveControl": executive_control,
        "caseControl": case_control,
        "bulkDataSummary": bulk_data_summary,
        "fileSummary": file_summary,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Create baseline decimated JSON from a Nastran BDF.")
    parser.add_argument("input_bdf", type=Path, help="Path to input .bdf or .dat file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output JSON path (default: <source_bdf_stem>_decimated.json)",
    )
    args = parser.parse_args()

    result = parse_bdf(args.input_bdf)
    output_path = args.output or args.input_bdf.with_name(f"{args.input_bdf.stem}_decimated.json")
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
