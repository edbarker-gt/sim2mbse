#!/usr/bin/env python3
"""
Final HFSS text-project decimator.

Purpose
-------
Read a text-based Ansys HFSS project file (`.hfss` or ASCII `.aedt`) and emit a
compact JSON document containing EM-relevant metadata suitable for downstream
exchange-layer construction.

Supported source styles
-----------------------
1. HFSS-style text projects with block-based material definitions:
      $begin 'Materials'
          $begin 'vacuum'
          ...
          $end 'vacuum'
      $end 'Materials'

2. AEDT-style text projects with attribute-based material references:
      MaterialValue='"air"'
      GlobalMaterialEnv='"vacuum"'

This script is intentionally conservative and deterministic. It extracts
high-value semantics while ignoring verbose internal records.

Retained
--------
- project identity and file provenance
- design names
- solution type
- analysis setups and sweeps
- boundary summary
- excitation / port summary
- material names
- basic EM environment settings

Dropped intentionally
---------------------
- low-level geometry internals
- full object trees
- mesh details
- plot formatting
- post-processing display settings
- raw project text in output

Default output naming
---------------------
    <source_hfss_stem>_decimated.json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

BEGIN_RE = re.compile(r"^\s*\$begin\s+'([^']+)'\s*$")
END_RE = re.compile(r"^\s*\$end\s+'([^']+)'\s*$")
KV_RE = re.compile(r"^\s*([^=\n]+?)\s*=\s*(.+?)\s*$")

MATERIAL_QUOTED_RE = re.compile(r"(?:MaterialValue|Material)\s*=\s*(['\"].+)", re.IGNORECASE)
DESIGN_NAME_RE = re.compile(r"DesignName='([^']+)'")
PROJECT_CREATED_RE = re.compile(r"Created='([^']+)'")
PROJECT_PRODUCT_RE = re.compile(r"Product='([^']+)'")
GLOBAL_ENV_RE = re.compile(r"GlobalMaterialEnv=(.+)")
SOLUTION_TYPE_RE = re.compile(r"SolutionType=(.+)")
PORT_IMPEDANCE_RE = re.compile(r"PortImpedance=(.+)")
HFSS_MODEL_NAME_RE = re.compile(r"^\s*Name='([^']+)'\s*$", re.MULTILINE)


def normalize_quoted_string(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    s = value.strip()

    prev = None
    while s != prev:
        prev = s
        if len(s) >= 2 and s.startswith("'") and s.endswith("'"):
            s = s[1:-1].strip()
        s = s.replace(r"\'", "'").replace(r"\"", '"')
        if len(s) >= 2 and s.startswith('"') and s.endswith('"'):
            s = s[1:-1].strip()

    if s in {"", '""', "''"}:
        return ""
    return s


def parse_scalar(value: str) -> Any:
    value = value.strip()

    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False

    try:
        if "." in value:
            return float(value)
        return int(value)
    except Exception:
        return normalize_quoted_string(value)


def read_text_project(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if "$begin 'AnsoftProject'" not in text:
        raise ValueError(
            f"Unsupported file structure for {path.name}. "
            "This decimator supports text-based HFSS/AEDT project files only."
        )
    return text


def extract_block(text: str, block_name: str) -> str | None:
    pattern = re.compile(rf"^\s*\$begin\s+'{re.escape(block_name)}'\s*$", re.MULTILINE)
    m = pattern.search(text)
    if not m:
        return None

    start = m.end()
    depth = 1
    i = start
    while i < len(text):
        next_begin = BEGIN_RE.search(text, i)
        next_end = END_RE.search(text, i)
        if next_end is None:
            return None
        if next_begin and next_begin.start() < next_end.start():
            depth += 1
            i = next_begin.end()
        else:
            depth -= 1
            if depth == 0:
                return text[start:next_end.start()]
            i = next_end.end()
    return None


def extract_named_subblocks(text: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    i = 0
    while i < len(text):
        m = BEGIN_RE.search(text, i)
        if not m:
            break
        name = normalize_quoted_string(m.group(1))
        start = m.end()
        depth = 1
        j = start
        while j < len(text):
            nb = BEGIN_RE.search(text, j)
            ne = END_RE.search(text, j)
            if ne is None:
                break
            if nb and nb.start() < ne.start():
                depth += 1
                j = nb.end()
            else:
                depth -= 1
                if depth == 0:
                    blocks.append((name, text[start:ne.start()]))
                    j = ne.end()
                    break
                j = ne.end()
        i = j
    return blocks


def first_normalized_match(pattern: re.Pattern[str], text: str) -> str | None:
    m = pattern.search(text)
    return normalize_quoted_string(m.group(1)) if m else None


def find_design_blocks(text: str) -> list[tuple[str, str]]:
    blocks = []
    for name, content in extract_named_subblocks(text):
        if str(name).startswith(("HFSSDesign", "HFSSModel")):
            blocks.append((name, content))
    return blocks


def extract_materials_from_hfss_blocks(text: str) -> list[str]:
    definitions = extract_block(text, "Definitions")
    if not definitions:
        return []

    materials_block = extract_block(definitions, "Materials")
    if not materials_block:
        return []

    names = []
    for name, content in extract_named_subblocks(materials_block):
        normalized = normalize_quoted_string(name)
        if normalized:
            names.append(normalized)
    return sorted(set(names))


def extract_materials_from_aedt_attributes(text: str) -> list[str]:
    referenced = set()

    for m in MATERIAL_QUOTED_RE.finditer(text):
        normalized = normalize_quoted_string(m.group(1))
        if normalized:
            referenced.add(normalized)

    global_env = first_normalized_match(GLOBAL_ENV_RE, text)
    if global_env:
        referenced.add(global_env)

    return sorted(referenced)


def summarize_materials(text: str) -> dict[str, Any]:
    hfss_materials = extract_materials_from_hfss_blocks(text)
    if hfss_materials:
        return {
            "sourceMode": "hfss_block_definitions",
            "count": len(hfss_materials),
            "names": hfss_materials,
        }

    aedt_materials = extract_materials_from_aedt_attributes(text)
    return {
        "sourceMode": "aedt_attribute_references",
        "count": len(aedt_materials),
        "names": aedt_materials,
    }


def summarize_boundaries(boundary_text: str) -> list[dict[str, Any]]:
    boundaries_block = extract_block(boundary_text, "Boundaries")
    if not boundaries_block:
        return []

    summaries: list[dict[str, Any]] = []
    for bname, bcontent in extract_named_subblocks(boundaries_block):
        summary: dict[str, Any] = {"name": normalize_quoted_string(bname)}

        for line in bcontent.splitlines():
            kv = KV_RE.match(line)
            if not kv:
                continue
            key = kv.group(1).strip()
            value = parse_scalar(kv.group(2))
            if key in {"ID", "BoundType", "Impedance", "RenormImp", "CharImp"}:
                summary[key] = normalize_quoted_string(value)

        if "Modes" in bcontent:
            summary["hasModes"] = True

        summaries.append(summary)

    return summaries


def summarize_analysis_setups(design_text: str) -> list[dict[str, Any]]:
    analysis_text = extract_block(design_text, "AnalysisSetup")
    if not analysis_text:
        return []

    solve_setups = extract_block(analysis_text, "SolveSetups")
    if not solve_setups:
        return []

    setups: list[dict[str, Any]] = []
    for sname, scontent in extract_named_subblocks(solve_setups):
        setup: dict[str, Any] = {"name": normalize_quoted_string(sname)}
        sweeps: list[dict[str, Any]] = []

        for line in scontent.splitlines():
            kv = KV_RE.match(line)
            if not kv:
                continue
            key = kv.group(1).strip()
            value = parse_scalar(kv.group(2))
            if key in {
                "ID", "SetupType", "SolveType", "Frequency", "MaxDeltaS",
                "MaximumPasses", "MinimumPasses", "MinimumConvergedPasses",
                "PercentRefinement", "IsEnabled", "DrivenSolverType"
            }:
                setup[key] = normalize_quoted_string(value)

        sweeps_block = extract_block(scontent, "Sweeps")
        if sweeps_block:
            for wname, wcontent in extract_named_subblocks(sweeps_block):
                sweep: dict[str, Any] = {"name": normalize_quoted_string(wname)}
                for line in wcontent.splitlines():
                    kv = KV_RE.match(line)
                    if not kv:
                        continue
                    key = kv.group(1).strip()
                    value = parse_scalar(kv.group(2))
                    if key in {
                        "ID", "IsEnabled", "RangeType", "RangeStart", "RangeEnd",
                        "RangeStep", "RangeCount", "Type", "SaveFields", "SaveRadFields",
                        "GenerateFieldsForAllFreqs"
                    }:
                        sweep[key] = normalize_quoted_string(value)
                sweeps.append(sweep)

        setup["sweeps"] = sweeps
        setups.append(setup)

    return setups


def summarize_design(design_name: str, design_text: str) -> dict[str, Any]:
    boundary_setup = extract_block(design_text, "BoundarySetup") or ""
    boundaries = summarize_boundaries(boundary_setup)
    setups = summarize_analysis_setups(design_text)

    excitations = []
    for b in boundaries:
        bound_type = str(b.get("BoundType", ""))
        if "Port" in bound_type:
            excitations.append({
                "name": normalize_quoted_string(b.get("name")),
                "type": normalize_quoted_string(b.get("BoundType")),
                "impedance": normalize_quoted_string(
                    b.get("Impedance") or b.get("RenormImp") or b.get("CharImp")
                ),
            })

    return {
        "designName": normalize_quoted_string(design_name),
        "solutionType": first_normalized_match(SOLUTION_TYPE_RE, design_text),
        "globalMaterialEnvironment": first_normalized_match(GLOBAL_ENV_RE, design_text),
        "portImpedanceGlobal": first_normalized_match(PORT_IMPEDANCE_RE, design_text),
        "boundaries": boundaries,
        "excitations": excitations,
        "analysisSetups": setups,
    }


def collect_design_names(text: str, design_blocks: list[tuple[str, str]]) -> list[str]:
    explicit = [normalize_quoted_string(x) for x in DESIGN_NAME_RE.findall(text)]
    if explicit:
        return explicit

    inferred = []
    for block_name, block_text in design_blocks:
        m = HFSS_MODEL_NAME_RE.search(block_text)
        if m:
            inferred.append(normalize_quoted_string(m.group(1)))
        else:
            inferred.append(normalize_quoted_string(block_name))
    return inferred


def parse_hfss_text_project(input_path: Path) -> dict[str, Any]:
    text = read_text_project(input_path)

    created = first_normalized_match(PROJECT_CREATED_RE, text)
    product = first_normalized_match(PROJECT_PRODUCT_RE, text)
    design_blocks = find_design_blocks(text)
    design_names = collect_design_names(text, design_blocks)

    design_summaries: list[dict[str, Any]] = []
    for idx, (block_name, block_text) in enumerate(design_blocks):
        dname = design_names[idx] if idx < len(design_names) else normalize_quoted_string(block_name)
        design_summaries.append(summarize_design(dname, block_text))

    return {
        "projectIdentity": {
            "sourceFileName": input_path.name,
            "sourceFileStem": input_path.stem,
            "projectFormat": input_path.suffix.lower().lstrip("."),
            "created": created,
            "product": product,
        },
        "solverContext": {
            "solverName": "HFSS",
            "product": product,
            "designCount": len(design_summaries),
        },
        "designSummary": {
            "designNames": [d["designName"] for d in design_summaries],
            "designs": design_summaries,
        },
        "materialSummary": summarize_materials(text),
        "fileSummary": {
            "inputFiles": [input_path.name],
            "outputFiles": [],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create decimated JSON from a text-based HFSS/AEDT project file."
    )
    parser.add_argument("input_project", type=Path, help="Path to input .hfss or ASCII .aedt file")
    parser.add_argument(
        "-o", "--output", type=Path,
        help="Output JSON path (default: <source_stem>_decimated.json)"
    )
    args = parser.parse_args()

    if args.input_project.suffix.lower() not in {".hfss", ".aedt"}:
        raise ValueError("Supported extensions are .hfss and .aedt for text-based project files.")

    result = parse_hfss_text_project(args.input_project)
    output_path = args.output or args.input_project.with_name(f"{args.input_project.stem}_decimated.json")
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
