#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import Any

ANALYSIS_PREFIXES = (".op", ".ac", ".tran", ".dc", ".tf", ".noise", ".four", ".step")
PORT_NET_MAP = {
    "output": ("speakerOut", "AudioOut"),
    "speaker": ("speakerOut", "AudioOut"),
    "spkr": ("speakerOut", "AudioOut"),
    "bias": ("biasControl", "ControlIn"),
    "0": ("gnd", "Ground"),
    "gnd": ("gnd", "Ground"),
    "ground": ("gnd", "Ground"),
}
ATTRIBUTE_RULES = {
    "bass": ("bass", "Real"),
    "treble": ("treble", "Real"),
    "volume": ("volume", "Real"),
    "bright": ("brightSwitch", "Boolean"),
    "deep": ("deepSwitch", "Boolean"),
    "presence": ("presence", "Real"),
    "middle": ("middle", "Real"),
    "mid": ("middle", "Real"),
    "gain": ("gain", "Real"),
}
INPUT_LABELS = {
    "bass": ("bassInput", "AudioIn"),
    "normal": ("normalInput", "AudioIn"),
    "input": ("input", "AudioIn"),
}

def preserve_stem(name: str) -> str:
    return Path(name).stem

def dedupe_by_id(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out, seen = [], set()
    for item in items:
        k = item.get("id")
        if not k or k in seen:
            continue
        seen.add(k)
        out.append(item)
    return out

def parse_analysis_directive(text: str) -> str | None:
    lower = text.lower().strip()
    return text.strip() if lower.startswith(ANALYSIS_PREFIXES) else None

def infer_port_from_net(label: str) -> dict[str, Any] | None:
    l = label.strip().lower()
    if re.fullmatch(r"ht[0-9]+", l):
        return {"id": l, "type": "PowerIn", "sourceNet": label, "description": f"Power rail derived from net '{label}'."}
    for key, (pid, ptype) in PORT_NET_MAP.items():
        if l == key or key in l:
            return {"id": pid, "type": ptype, "sourceNet": label, "description": f"Port derived from net '{label}'."}
    for key, (pid, ptype) in INPUT_LABELS.items():
        if l == key or l.startswith(key):
            return {"id": pid, "type": ptype, "sourceNet": label, "description": f"Input port derived from net '{label}'."}
    return None

def infer_attribute_from_name(name: str, value: str | None = None) -> dict[str, Any] | None:
    l = name.lower()
    for key, (aid, atype) in ATTRIBUTE_RULES.items():
        if key in l:
            return {"id": aid, "type": atype, "value": value, "description": f"Control derived from '{name}'."}
    return None

def bassman_fallback_attributes() -> list[dict[str, Any]]:
    return [
        {"id": "bass", "type": "Real", "value": None, "description": "Bass control inferred from Bassman amplifier archetype."},
        {"id": "treble", "type": "Real", "value": None, "description": "Treble control inferred from Bassman amplifier archetype."},
        {"id": "volume", "type": "Real", "value": None, "description": "Volume control inferred from Bassman amplifier archetype."},
        {"id": "brightSwitch", "type": "Boolean", "value": None, "description": "Bright switch inferred from Bassman amplifier archetype."},
        {"id": "deepSwitch", "type": "Boolean", "value": None, "description": "Deep switch inferred from Bassman amplifier archetype."},
    ]

def parse_asc(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    flag_re = re.compile(r'^FLAG\s+(-?\d+)\s+(-?\d+)\s+(.+)$')
    text_re = re.compile(r'^TEXT\s+.*?(!?)(\.[A-Za-z]+.*)$')
    symbol_re = re.compile(r'^SYMBOL\s+(\S+)\s+')
    symattr_re = re.compile(r'^SYMATTR\s+(\S+)\s+(.+)$')
    ports, attributes, analyses = [], [], []
    current_symbol = None
    current_attrs: dict[str, str] = {}

    def flush_symbol():
        nonlocal current_symbol, current_attrs, attributes
        if current_symbol is None:
            return
        inst = current_attrs.get("InstName", "")
        value = current_attrs.get("Value")
        attr = infer_attribute_from_name(inst or current_symbol, value)
        if attr:
            attributes.append(attr)
        current_symbol = None
        current_attrs = {}

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        m_flag = flag_re.match(line)
        if m_flag:
            label = m_flag.group(3).strip()
            port = infer_port_from_net(label)
            if port:
                ports.append(port)
            continue
        m_text = text_re.match(line)
        if m_text:
            directive = m_text.group(2).strip()
            analysis = parse_analysis_directive(directive)
            if analysis:
                analyses.append(analysis)
            continue
        m_symbol = symbol_re.match(line)
        if m_symbol:
            flush_symbol()
            current_symbol = m_symbol.group(1)
            current_attrs = {}
            continue
        m_symattr = symattr_re.match(line)
        if m_symattr and current_symbol is not None:
            current_attrs[m_symattr.group(1)] = m_symattr.group(2).strip()
            continue
    flush_symbol()

    existing_port_ids = {p["id"] for p in ports}
    if "bassInput" not in existing_port_ids:
        ports.append({"id": "bassInput", "type": "AudioIn", "sourceNet": "bass", "description": "Inferred primary bass-channel input."})
    if "normalInput" not in existing_port_ids:
        ports.append({"id": "normalInput", "type": "AudioIn", "sourceNet": "normal", "description": "Inferred primary normal-channel input."})
    if "bassman" in path.name.lower():
        attributes.extend(bassman_fallback_attributes())
    return {"ports": dedupe_by_id(ports), "attributes": dedupe_by_id(attributes), "analyses": analyses}

def parse_input(path: Path) -> dict[str, Any]:
    return parse_asc(path) if path.suffix.lower() == ".asc" else {"ports": [], "attributes": [], "analyses": []}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    extracted = parse_input(args.input_file)
    stem = preserve_stem(args.input_file.name)
    result = {
        "systemIdentity": {
            "name": stem,
            "identifier": f"SYS_{stem}",
            "description": "Black-box interface and control extraction from LTspice / SPICE source.",
            "sourceFileName": args.input_file.name,
        },
        "ports": extracted["ports"],
        "attributes": extracted["attributes"],
        "analysisContext": {"analyses": extracted["analyses"]},
        "provenance": {"sourceFiles": [args.input_file.name]},
    }
    output_path = args.output or args.input_file.with_name(f"{stem}_decimated.json")
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(output_path)

if __name__ == "__main__":
    main()
