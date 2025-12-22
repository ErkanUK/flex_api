#!/usr/bin/env python3
"""
Extract OpenAPI components/schemas into separate JSON Schema files.
Usage:
  python tools/oas_extract_schemas.py path/to/openapi.yaml schemas/
"""
import sys, os, json
from pathlib import Path

try:
    import yaml
except Exception as e:
    print("PyYAML required. Run: pip install pyyaml")
    raise

if len(sys.argv) < 3:
    print("Usage: oas_extract_schemas.py <openapi.yaml> <outdir>")
    sys.exit(2)

openapi_path = Path(sys.argv[1])
outdir = Path(sys.argv[2])
outdir.mkdir(parents=True, exist_ok=True)

spec = yaml.safe_load(openapi_path.read_text(encoding='utf-8'))
components = spec.get('components', {}) or {}
schemas = components.get('schemas', {}) or {}

for name, schema in schemas.items():
    # Create a basic JSON Schema wrapper referencing the OAS schema
    json_schema = {"$schema": "http://json-schema.org/draft/2020-12/schema", "title": name}
    # Convert OAS subset directly (OAS schemas already JSON Schema-compatible)
    json_schema.update(schema)

    out_path = outdir / f"{name}.json"
    out_path.write_text(json.dumps(json_schema, indent=2), encoding='utf-8')
    print("Wrote", out_path)