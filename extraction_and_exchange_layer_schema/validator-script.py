import json
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def make_validator(schema_path: Path, base_uri: str = "https://example.org/schemas/"):
    schema = load_json(schema_path)
    store = {base_uri + schema_path.name: schema}
    resolver = RefResolver(base_uri=base_uri, referrer=schema, store=store)
    return Draft202012Validator(schema, resolver=resolver)

def validate_instance(schema_path: Path, instance_path: Path):
    validator = make_validator(schema_path)
    instance = load_json(instance_path)
    errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
    if errors:
        print(f"Validation FAILED for {instance_path}:")
        for err in errors:
            print(f" - {'/'.join(map(str, err.path))}: {err.message}")
    else:
        print(f"Validation OK for {instance_path}")

if __name__ == "__main__":
    # examples
    base = Path("schemas")

    # validate a combined ESMS model (metadata + simulationModel)
    schema_combined = base / "esms-combined.json"
    instance_combined = Path("examples") / "nastran_esms_model.json"
    validate_instance(schema_combined, instance_combined)

    # validate a raw extractor output
    schema_extractor = base / "nastran-extraction.json"
    instance_extractor = Path("examples") / "nastran_extraction_output.json"
    validate_instance(schema_extractor, instance_extractor)
