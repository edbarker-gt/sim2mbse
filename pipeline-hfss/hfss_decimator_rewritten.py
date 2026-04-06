#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import Any

BEGIN_RE = re.compile(r"^\s*\$begin\s+'([^']+)'\s*$")
END_RE = re.compile(r"^\s*\$end\s+'([^']+)'\s*$")
KV_RE = re.compile(r"^\s*([^=\n]+?)\s*=\s*(.+?)\s*$")
MATERIAL_QUOTED_RE = re.compile(r"(?:MaterialValue|Material)\s*=\s*(['\"].+)", re.IGNORECASE)
DESIGN_NAME_RE = re.compile(r"DesignName='([^']+)'")
PROJECT_PRODUCT_RE = re.compile(r"Product='([^']+)'")
GLOBAL_ENV_RE = re.compile(r"GlobalMaterialEnv=(.+)")
HFSS_MODEL_NAME_RE = re.compile(r"^\s*Name='([^']+)'\s*$", re.MULTILINE)
OBJECT_KIND_RE = re.compile(r"\b(?:CreateBox|CreateCylinder|CreateSphere|CreatePolyline|CreateRectangle|CreateCircle)\b")

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
        raise ValueError(f"Unsupported file structure for {path.name}.")
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
        nb = BEGIN_RE.search(text, i)
        ne = END_RE.search(text, i)
        if ne is None:
            return None
        if nb and nb.start() < ne.start():
            depth += 1
            i = nb.end()
        else:
            depth -= 1
            if depth == 0:
                return text[start:ne.start()]
            i = ne.end()
    return None

def extract_named_subblocks(text: str) -> list[tuple[str, str]]:
    blocks = []
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
    return [(n,c) for n,c in extract_named_subblocks(text) if str(n).startswith(("HFSSDesign","HFSSModel"))]

def collect_design_names(text: str, design_blocks: list[tuple[str, str]]) -> list[str]:
    explicit = [normalize_quoted_string(x) for x in DESIGN_NAME_RE.findall(text)]
    if explicit:
        return explicit
    inferred = []
    for block_name, block_text in design_blocks:
        m = HFSS_MODEL_NAME_RE.search(block_text)
        inferred.append(normalize_quoted_string(m.group(1)) if m else normalize_quoted_string(block_name))
    return inferred

def extract_materials_from_hfss_blocks(text: str) -> list[str]:
    definitions = extract_block(text, "Definitions")
    if not definitions:
        return []
    materials_block = extract_block(definitions, "Materials")
    if not materials_block:
        return []
    names = []
    for name, _ in extract_named_subblocks(materials_block):
        n = normalize_quoted_string(name)
        if n:
            names.append(n)
    return sorted(set(names))

def extract_materials_from_aedt_attributes(text: str) -> list[str]:
    referenced = set()
    for m in MATERIAL_QUOTED_RE.finditer(text):
        n = normalize_quoted_string(m.group(1))
        if n:
            referenced.add(n)
    global_env = first_normalized_match(GLOBAL_ENV_RE, text)
    if global_env:
        referenced.add(global_env)
    return sorted(referenced)

def classify_material_type(name: str) -> str:
    lower = name.lower()
    if lower in {"pec","copper","gold","silver","aluminum","aluminium","steel"}:
        return "conductor"
    if lower in {"vacuum","air"}:
        return "dielectric"
    return "other"

def summarize_materials(text: str) -> list[dict[str, Any]]:
    names = extract_materials_from_hfss_blocks(text) or extract_materials_from_aedt_attributes(text)
    return [{"name": n, "type": classify_material_type(n)} for n in names]

def summarize_boundaries(boundary_text: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    boundaries_block = extract_block(boundary_text, "Boundaries")
    if not boundaries_block:
        return [], []
    port_summary, boundary_summary = [], []
    for bname, bcontent in extract_named_subblocks(boundaries_block):
        summary = {"name": normalize_quoted_string(bname)}
        for line in bcontent.splitlines():
            kv = KV_RE.match(line)
            if not kv:
                continue
            key = kv.group(1).strip()
            value = parse_scalar(kv.group(2))
            if key in {"ID","BoundType","Impedance","RenormImp","CharImp"}:
                summary[key] = normalize_quoted_string(value)
        btype = str(summary.get("BoundType",""))
        if "Port" in btype:
            port_summary.append({
                "id": summary.get("name"),
                "type": btype,
                "location": summary.get("name"),
                "impedance": summary.get("Impedance") or summary.get("RenormImp") or summary.get("CharImp"),
            })
        else:
            boundary_summary.append({
                "type": btype or "other",
                "appliesTo": [summary.get("name")] if summary.get("name") else [],
            })
    return port_summary, boundary_summary

def summarize_analysis_setups(design_text: str) -> tuple[dict[str, Any], str | None]:
    analysis_text = extract_block(design_text, "AnalysisSetup")
    if not analysis_text:
        return {}, None
    solve_setups = extract_block(analysis_text, "SolveSetups")
    if not solve_setups:
        return {}, None
    freq_setup = {}
    method = None
    for _, scontent in extract_named_subblocks(solve_setups):
        if not method:
            method = "FEM"
        for line in scontent.splitlines():
            kv = KV_RE.match(line)
            if not kv:
                continue
            key = kv.group(1).strip()
            value = parse_scalar(kv.group(2))
            if key == "Frequency" and not freq_setup:
                freq_setup = {"startHz": value, "stopHz": value, "points": 1}
        sweeps_block = extract_block(scontent, "Sweeps")
        if sweeps_block:
            for _, wcontent in extract_named_subblocks(sweeps_block):
                sweep = {}
                for line in wcontent.splitlines():
                    kv = KV_RE.match(line)
                    if not kv:
                        continue
                    key = kv.group(1).strip()
                    value = parse_scalar(kv.group(2))
                    if key in {"RangeStart","RangeEnd","RangeCount"}:
                        sweep[key] = value
                if not freq_setup:
                    if "RangeStart" in sweep:
                        freq_setup["startHz"] = sweep["RangeStart"]
                    if "RangeEnd" in sweep:
                        freq_setup["stopHz"] = sweep["RangeEnd"]
                    if "RangeCount" in sweep:
                        freq_setup["points"] = sweep["RangeCount"]
    return freq_setup, method

def summarize_geometry(text: str) -> dict[str, Any]:
    count = len(OBJECT_KIND_RE.findall(text))
    return {"entityCount": count, "entityTypes": {"other": count} if count else {}}

def parse_hfss_text_project(input_path: Path) -> dict[str, Any]:
    text = read_text_project(input_path)
    product = first_normalized_match(PROJECT_PRODUCT_RE, text)
    design_blocks = find_design_blocks(text)
    _ = collect_design_names(text, design_blocks)
    method = None
    frequency_setup = {}
    all_ports, all_boundaries = [], []
    for _, block_text in design_blocks:
        ports, boundaries = summarize_boundaries(extract_block(block_text, "BoundarySetup") or "")
        all_ports.extend(ports)
        all_boundaries.extend(boundaries)
        freq, mth = summarize_analysis_setups(block_text)
        if freq and not frequency_setup:
            frequency_setup = freq
        if mth and not method:
            method = mth
    return {
        "solverInfo": {
            "solverName": "HFSS",
            "solverVersion": product or "unknown",
            "method": method or "FEM",
        },
        "geometrySummary": summarize_geometry(text),
        "meshSummary": {},
        "materialSummary": summarize_materials(text),
        "portSummary": all_ports,
        "boundaryConditionSummary": all_boundaries,
        "frequencySetup": frequency_setup,
        "fileSummary": {
            "inputFiles": [input_path.name],
            "outputFiles": [],
        },
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_project", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    if args.input_project.suffix.lower() not in {".hfss", ".aedt"}:
        raise ValueError("Supported extensions are .hfss and .aedt.")
    result = parse_hfss_text_project(args.input_project)
    output_path = args.output or args.input_project.with_name(f"{args.input_project.stem}_decimated.json")
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(output_path)

if __name__ == "__main__":
    main()
