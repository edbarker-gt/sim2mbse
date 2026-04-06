#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

def build_exchange(decimated: dict) -> dict:
    return {
        "systemIdentity": decimated.get("systemIdentity", {}),
        "ports": decimated.get("ports", []),
        "analysisContext": decimated.get("analysisContext", {}),
        "provenance": {
            "sourceFiles": decimated.get("provenance", {}).get("sourceFiles", []),
            "tool": {"name": "step_connector_exchange_create.py", "version": "1.0"},
            "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        },
    }

def main() -> None:
    parser = argparse.ArgumentParser(description="Build STEP connector-port exchange JSON.")
    parser.add_argument("input_json", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    decimated = json.loads(args.input_json.read_text(encoding="utf-8"))
    result = build_exchange(decimated)
    stem = decimated.get("systemIdentity", {}).get("name") or args.input_json.stem.replace("_decimated","")
    output_path = args.output or args.input_json.with_name(f"{stem}_exchange.json")
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(output_path)

if __name__ == "__main__":
    main()
