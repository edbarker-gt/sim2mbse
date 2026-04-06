#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path

PORT_ORDER = ["usb32TypeC","usb32TypeAStacked","gigabitEthernet","displayPort","m2KeyE","m2KeyM4Lane","m2KeyM2Lane","cameraConnector","expansionHeader40Pin","buttonHeader","canBusHeader","fanConnector","dcPowerJack"]

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
    order = {k:i for i,k in enumerate(PORT_ORDER)}
    return sorted(ports, key=lambda p: (order.get(p.get("id"), 999), p.get("id","")))

def emit_sysml(exchange: dict) -> str:
    sys_id = exchange.get("systemIdentity", {})
    ports = sort_ports(exchange.get("ports", []))
    pkg = ident(sys_id.get("name"), "StepConnectorPorts")
    top = "BoardAssembly" if "P3766" in sys_id.get("name","") or "P3768" in sys_id.get("name","") else ident(sys_id.get("name"), "System")
    lines = []
    a = lines.append
    a(f"package {pkg} {{")
    a("")
    for ptype in ["Usb32TypeC","Usb32TypeAStacked","Rj45Ethernet","DisplayPort","M2KeyE","M2KeyM4Lane","M2KeyM2Lane","CameraConnector","ExpansionHeader40Pin","ButtonHeader","CanBusHeader","FanConnector","DcPowerJack","OtherPort"]:
        a(f"  part def {ptype} {{}}")
    a("")
    a(f"  part {top} {{")
    a("")
    for p in ports:
        a(f"    port {ident(p.get('id'),'port')}: {p.get('type','OtherPort')};")
    a("")
    a("  }")
    a("}")
    return "\n".join(lines) + "\n"

def main() -> None:
    parser = argparse.ArgumentParser(description="Create non-flattened SysML from STEP connector-port exchange JSON.")
    parser.add_argument("input_json", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    exchange = json.loads(args.input_json.read_text(encoding="utf-8"))
    text = emit_sysml(exchange)
    stem = exchange.get("systemIdentity", {}).get("name") or args.input_json.stem.replace("_exchange","")
    output_path = args.output or args.input_json.with_name(f"{stem}_model.sysml")
    output_path.write_text(text, encoding="utf-8")
    print(output_path)

if __name__ == "__main__":
    main()
