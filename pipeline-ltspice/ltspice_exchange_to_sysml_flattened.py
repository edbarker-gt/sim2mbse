#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path

PORT_ORDER = ["bassInput", "normalInput", "speakerOut", "ht1", "ht2", "ht3", "ht4", "biasControl", "gnd"]
ATTR_ORDER = ["bass", "treble", "volume", "brightSwitch", "deepSwitch", "presence", "middle", "gain"]

def ident(text: str | None, default: str = "Unnamed") -> str:
    raw = text if text else default
    cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", raw)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    if not cleaned:
        cleaned = default
    if cleaned[0].isdigit():
        cleaned = f"N_{cleaned}"
    return cleaned

def sort_ports(ports: list[dict]) -> list[dict]:
    order = {k: i for i, k in enumerate(PORT_ORDER)}
    return sorted(ports, key=lambda p: (order.get(p.get("id"), 999), p.get("id", "")))

def sort_attrs(attrs: list[dict]) -> list[dict]:
    order = {k: i for i, k in enumerate(ATTR_ORDER)}
    return sorted(attrs, key=lambda a: (order.get(a.get("id"), 999), a.get("id", "")))

def emit_sysml(exchange: dict) -> str:
    sys_id = exchange.get("systemIdentity", {})
    ports = sort_ports(exchange.get("ports", []))
    attrs = sort_attrs(exchange.get("attributes", []))
    pkg = ident(sys_id.get("name"), "LtspiceBlackBox")
    top = "BassmanAmp" if "Bassman" in sys_id.get("name", "") else ident(sys_id.get("name"), "System")
    lines = []
    a = lines.append
    a(f"package {pkg} {{")
    a("")
    a(f"  part {top} {{")
    a("")
    for p in ports:
        pid = ident(p.get("id"), "port")
        a(f"    port {pid}: {p.get('type', 'OtherPort')};")
    a("")
    for attr in attrs:
        aid = ident(attr.get("id"), "attr")
        a(f"    attribute {aid}: {attr.get('type', 'String')};")
    a("")
    a("  }")
    a("")
    a("  interface AudioIn {")
    a("    flow in signal: Real;")
    a("  }")
    a("")
    a("  interface AudioOut {")
    a("    flow out signal: Real;")
    a("  }")
    a("")
    a("  interface PowerIn {")
    a("    flow in voltage: Real;")
    a("  }")
    a("")
    a("  interface ControlIn {")
    a("    flow in control: Real;")
    a("  }")
    a("")
    a("  interface Ground { }")
    a("")
    a("  interface OtherPort { }")
    a("}")
    return "\n".join(lines) + "\n"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    exchange = json.loads(args.input_json.read_text(encoding="utf-8"))
    text = emit_sysml(exchange)
    stem = exchange.get("systemIdentity", {}).get("name") or args.input_json.stem.replace("_exchange", "")
    output_path = args.output or args.input_json.with_name(f"{stem}_presentation.sysml")
    output_path.write_text(text, encoding="utf-8")
    print(output_path)

if __name__ == "__main__":
    main()
